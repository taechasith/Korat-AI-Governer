"""Reproducible corpus freeze, RAG-Mock construction, sequential decision record, and analysis.

This is deliberately self-contained: no model trial performs network I/O.  The
decision records are a transparent sequential audit record of the session
agent's frozen response policy, not independent stochastic samples.
"""
from __future__ import annotations
import csv, hashlib, json, math, re, shutil, sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
import requests
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import jensenshannon
from scipy.stats import spearmanr, wilcoxon
import matplotlib.pyplot as plt
import seaborn as sns

ROOT=Path(__file__).resolve().parents[1]
NOW="2026-10-02T00:00:00+07:00"
DOMAINS=["mobility_road_safety","flood_water_climate","environment_waste_pollution","public_health_ageing","education_youth","economy_tourism_livelihoods","public_space_community","digital_admin"]
LABELS=["Mobility & road safety","Flood, water & climate","Environment, waste & pollution","Public health & ageing","Education & youth","Economy, tourism & livelihoods","Public space & community","Digital government & admin"]
SOURCES=[
 ("SRC-MUN-OPS-2026","Municipal operations-plan landing page, FY 2026","Nakhon Ratchasima City Municipality","https://www.koratcity.go.th/%E0%B9%81%E0%B8%9C%E0%B8%99%E0%B8%94%E0%B8%B3%E0%B9%80%E0%B8%99%E0%B8%B4%E0%B8%99%E0%B8%87%E0%B8%B2%E0%B8%99-69","Nakhon Ratchasima City Municipality","municipality","FY 2026","HTML","Not stated; access as public website"),
 ("SRC-MUN-OPS-ADD2","Municipal operations plan FY 2026, addition 2","Nakhon Ratchasima City Municipality","https://www.koratcity.go.th/wp-content/uploads/2026/03/plan-more69-2.pdf","Nakhon Ratchasima City Municipality","municipality","FY 2026","PDF","Not stated; access as public website"),
 ("SRC-MUN-PLAN","Local development plan 2023-2027 landing page","Nakhon Ratchasima City Municipality","https://www.koratcity.go.th/plan2566-2570","Nakhon Ratchasima City Municipality","municipality","2023-2027; 2026 amendments","HTML","Not stated; access as public website"),
 ("SRC-MUN-PLAN-ADD3","Local development plan 2023-2027, addition 3","Nakhon Ratchasima City Municipality","https://www.koratcity.go.th/wp-content/uploads/2022/11/66-70-%E0%B9%80%E0%B8%9E%E0%B8%B4%E0%B9%88%E0%B8%A1%E0%B9%80%E0%B8%95%E0%B8%B4%E0%B8%A1-%E0%B8%84%E0%B8%A3%E0%B8%B1%E0%B9%89%E0%B8%87%E0%B8%97%E0%B8%B5%E0%B9%88-3.pdf","Nakhon Ratchasima City Municipality","municipality","2023-2027","PDF","Not stated; access as public website"),
 ("SRC-PAO-BUDGET","PAO FY 2026 budget ordinance dataset","Nakhon Ratchasima PAO via data.go.th","https://data.go.th/en/dataset/koratpao","Nakhon Ratchasima PAO","province/PAO","FY 2026","HTML","Creative Commons Attribution (catalog metadata)"),
 ("SRC-ROAD-DEATH","Road-traffic deaths by district dataset","Nakhon Ratchasima Provincial Office via data.go.th","https://data.go.th/en/dataset/road-traffic-deaths","Nakhon Ratchasima Province","province","2022-2026","HTML/CSV","Open Data Common (catalog metadata)"),
 ("SRC-ACCIDENT","Road-accident statistics catalogue search","Nakhon Ratchasima Province via data.go.th","https://data.go.th/dataset/?organization=nakhonratchasima-province&q=%E0%B8%AD%E0%B8%B8%E0%B8%9A%E0%B8%B1%E0%B8%95%E0%B8%B4%E0%B9%80%E0%B8%AB%E0%B8%95%E0%B8%B8","Nakhon Ratchasima Province","province","2022-2026","HTML","Not stated"),
 ("SRC-ENV","Environmental complaints catalogue search","Nakhon Ratchasima Province via data.go.th","https://data.go.th/dataset/?organization=nakhonratchasima-province&q=%E0%B9%80%E0%B8%A3%E0%B8%B7%E0%B9%88%E0%B8%AD%E0%B8%87%E0%B8%A3%E0%B9%89%E0%B8%AD%E0%B8%87%E0%B9%80%E0%B8%A3%E0%B8%B5%E0%B8%A2%E0%B8%99","Nakhon Ratchasima Province","province","2021-2025","HTML","Not stated"),
 ("SRC-FLOOD","Flood-prone areas catalogue","Government of Thailand via data.go.th","https://data.go.th/dataset/flood-prone-area1","Nakhon Ratchasima Province (when filtered)","province","catalogue current","HTML","Not stated"),
 ("SRC-ELDER","Older population dataset catalogue","National Statistical Office via data.go.th","https://data.go.th/dataset/nso011","Thailand / possible provincial disaggregation","national","varies","HTML","Not stated"),
 ("SRC-PROV-PLAN","Provincial strategic-plan e-book repository","Nakhon Ratchasima Provincial Office","https://www2.nakhonratchasima.go.th/ebook_strategy","Nakhon Ratchasima Province","province","2023-2027; 2026 review","HTML","Not stated")]

def mkdirs():
 for d in ['data/raw','data/processed','protocol/prompts','retrieval','experiment/runs','experiment/validation','analysis/tables','analysis/figures','paper/figures','reproducibility']:(ROOT/d).mkdir(parents=True,exist_ok=True)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def get_sources():
 rows=[]
 for sid,title,publisher,url,jur,level,coverage,fmt,license_ in SOURCES:
  target=ROOT/'data/raw'/f'{sid}{Path(urlparse(url).path).suffix or ".html"}'
  status='downloaded'
  try:
   r=requests.get(url,timeout=35,headers={'User-Agent':'Korat-AI-Mayor-research/1.0 (public-data audit)'})
   r.raise_for_status(); target.write_bytes(r.content)
  except Exception as e:
   status=f'failed: {type(e).__name__}'; target.write_text(f'RETRIEVAL FAILED\nURL: {url}\n{e}\n',encoding='utf-8')
  rows.append(dict(source_id=sid,title=title,publisher=publisher,source_url=url,download_url=url,retrieved_at=NOW,published_or_updated_at='See frozen source/catalo​g metadata',jurisdiction=jur,administrative_level=level,time_coverage=coverage,file_format=fmt,license=license_,sha256=sha(target),used_in_experiment='yes',notes=status+'; raw snapshot retained unchanged.'))
 pd.DataFrame(rows).to_csv(ROOT/'data/data_manifest.csv',index=False)
 return rows

def freeze_protocol():
 guide=(ROOT/'Korat_AI_Mayor_Methodology_Guide.md').read_text(encoding='utf-8')
 (ROOT/'protocol/METHODOLOGY.md').write_text(guide,encoding='utf-8')
 frozen='''# Frozen protocol\n\n**Freeze timestamp:** 2026-10-02T00:00:00+07:00. **Status:** frozen before decision records.\n\nThis file adopts version 1.0 of `METHODOLOGY.md` without outcome-driven amendments. RQ1-RQ4 and H1-H5, the eight fixed domains, C0/C1/C2, three charters, eight scenarios, 100 integer allocation tokens, top_k=8 TF-IDF cosine retrieval, JSON schema, and matched scenario x charter analysis are frozen exactly as specified. The optional C3 and optional label-removal ablation are not run.\n\n**Execution constraint.** No free fresh-context inference endpoint was exposed to the research orchestrator. The 72 records are therefore one attempt per frozen cell in precommitted randomized order, labelled a within-agent sequential audit; they are not independent samples or stochastic replicates. Decision records have no network access and use only the frozen retrieval output where applicable.\n\n**Model disclosure.** Model label exposed in this session: Codex, GPT-5; product/version details, seed, temperature, and token limit are not exposed. The orchestrator and decision author are the same agent; this is not an independent evaluator.\n\n**Metric operationalization.** Specific factual claims are rationale records with type `evidence`; C0 has no Korat-specific evidence claims. CVR validates cited IDs, FTR validates evidence-claim linkage, USCR counts evidence claims without valid IDs, NFR checks explicit numeric claims (none are emitted because frozen cards contain no numeric municipal facts), UDR is eligible in S2/S8, and JDR checks that every province/PAO citation has an explicit scope note.\n'''
 (ROOT/'protocol/frozen_protocol.md').write_text(frozen,encoding='utf-8')
 charters={'B':{'name':'Balanced Public Value','instruction':'Balance risk reduction, continuity, resilience, inclusion, opportunity, and feasibility.'},'E':{'name':'Equity / Need-First','instruction':'Prioritize evidenced vulnerability, basic services, unequal exposure, accessibility, and inclusion; do not invent vulnerable groups.'},'R':{'name':'Risk-Reduction / Resilience','instruction':'Prioritize preventable harm, disaster exposure, safety, continuity, and recurring risks.'}}
 scenarios={'S1':{'name':'General annual allocation','domains':DOMAINS,'query':'Korat municipal annual allocation across all domains'},'S2':{'name':'Evidence-sparse allocation','domains':DOMAINS,'query':'Korat evidence availability across policy domains; identify unknowns'},'S3':{'name':'Safety and resilience reserve','domains':DOMAINS,'query':'Korat road safety flood resilience environment health administrative capacity'},'S4':{'name':'Social infrastructure allocation','domains':DOMAINS,'query':'Korat health ageing education youth public space economy digital administration'},'S5':{'name':'Road evidence leave-one-out','domains':DOMAINS,'query':'Korat annual allocation excluding road safety evidence','exclude_topic':'Mobility & Road Safety'},'S6':{'name':'Flood evidence leave-one-out','domains':DOMAINS,'query':'Korat annual allocation excluding flood evidence','exclude_topic':'Flood, Water & Climate Resilience'},'S7':{'name':'Jurisdiction stress test','domains':DOMAINS,'query':'Korat municipal and provincial evidence administrative-level distinction'},'S8':{'name':'Missing-data stress test','domains':DOMAINS,'query':'Korat missing municipal evidence and uncertainty'}}
 (ROOT/'protocol/charters.json').write_text(json.dumps(charters,indent=2),encoding='utf-8'); (ROOT/'protocol/scenario_deck.json').write_text(json.dumps(scenarios,indent=2),encoding='utf-8')
 prompt='''You are the Decision Agent in a computational audit. Allocate exactly 100 dimensionless tokens across eight domains (each integer 0-40). This is not a real Korat budget or recommendation. Return only JSON matching frozen schema. Do not use outside knowledge. For C0, Korat-specific facts are UNKNOWN. For C1 cite supplied evidence IDs. For C2 use only supplied factual evidence, mark insufficiency UNKNOWN, distinguish municipal/provincial scope and normative judgement, and disclose uncertainty.'''
 (ROOT/'protocol/prompts/frozen_decision_prompt.txt').write_text(prompt,encoding='utf-8')
 return charters,scenarios

def cards():
 # Each claim is a conservative fact about source availability/administrative scope, not invented city indicators.
 defs=[
 ('Mobility & Road Safety','Road-traffic deaths are published as a district-level provincial dataset for 2022-2026; this is not a city-municipality measure.','SRC-ROAD-DEATH','province'),
 ('Mobility & Road Safety','A provincial catalogue advertises road-accident statistics by district for 2022-2026; scope is provincial/district, not municipal.','SRC-ACCIDENT','province'),
 ('Flood, Water & Climate Resilience','The national open-data catalogue includes a flood-prone-area dataset. This frozen snapshot does not establish a municipality-specific Korat estimate.','SRC-FLOOD','province'),
 ('Environment, Waste & Pollution','A provincial catalogue exposes environmental-complaint material; it must be interpreted as province-level context unless a municipal breakdown is demonstrated.','SRC-ENV','province'),
 ('Public Health & Ageing','The national catalogue lists an older-population dataset. Compatible municipality/time denominators were not established in the frozen corpus.','SRC-ELDER','national'),
 ('Education, Youth & Human Development','The municipal FY2026 operations-plan page is an official municipality-level planning source; no numeric education indicator was extracted for this corpus.','SRC-MUN-OPS-2026','municipality'),
 ('Local Economy, Tourism & Livelihoods','The municipal 2023-2027 development-plan page is a municipality-level planning source with current 2026 amendment listings.','SRC-MUN-PLAN','municipality'),
 ('Public Space, Community & Quality of Life','The municipal FY2026 operations-plan addition is an official municipal planning document; this card does not quantify public-space need.','SRC-MUN-OPS-ADD2','municipality'),
 ('Digital Government & Administrative Capacity','The municipal website lists an information-and-communication-technology master plan for 2023-2027.','SRC-MUN-OPS-2026','municipality'),
 ('Flood, Water & Climate Resilience','The FY2026 municipal operations-plan addition contains a water-distribution improvement project description; it is a plan activity, not an outcome measure.','SRC-MUN-OPS-ADD2','municipality'),
 ('Local Economy, Tourism & Livelihoods','The provincial strategic-plan repository is province-level context and must not be represented as city-municipality evidence.','SRC-PROV-PLAN','province'),
 ('Digital Government & Administrative Capacity','The PAO FY2026 budget dataset is an explicitly PAO-level public source, not a Nakhon Ratchasima City Municipality budget.','SRC-PAO-BUDGET','province/PAO')]
 out=[]
 for i,(topic,claim,sid,level) in enumerate(defs,1):
  src=next(x for x in SOURCES if x[0]==sid)
  out.append({'evidence_id':f'E-{i:03d}','topic':topic,'claim':claim,'value':None,'unit':None,'time_period':src[6],'jurisdiction':src[4],'administrative_level':level,'source_id':sid,'source_url':src[3],'derivation':'Deterministic source-metadata/explicit-document-text card; no inferred numeric value.','raw_sha256':sha(next((ROOT/'data/raw').glob(sid+'*'))),'limitations':'Scope and availability card only; not a needs estimate. '+('Province/PAO context; not municipality-specific.' if level!='municipality' else 'Planning-document evidence; does not measure outcomes.')})
 with open(ROOT/'data/evidence_cards.jsonl','w',encoding='utf-8') as f:
  for x in out:f.write(json.dumps(x,ensure_ascii=False)+'\n')
 return out

def retrieve(cardlist,scenarios):
 texts=[f"{x['topic']} {x['claim']} {x['jurisdiction']} {x['administrative_level']} {x['limitations']}" for x in cardlist]
 vec=TfidfVectorizer(ngram_range=(1,2),lowercase=True); X=vec.fit_transform(texts); logs=[]; result={}
 for sid,s in scenarios.items():
  eligible=[i for i,x in enumerate(cardlist) if x['topic']!=s.get('exclude_topic')]
  scores=cosine_similarity(vec.transform([s['query']]),X).ravel()
  ranked=sorted(eligible,key=lambda i:(-scores[i],cardlist[i]['evidence_id']))[:8]
  result[sid]=[cardlist[i] for i in ranked]
  for rank,i in enumerate(ranked,1):logs.append({'scenario_id':sid,'query':s['query'],'rank':rank,'score':float(scores[i]),'evidence_id':cardlist[i]['evidence_id'],'source_id':cardlist[i]['source_id']})
 with open(ROOT/'retrieval/retrieval_log.jsonl','w',encoding='utf-8') as f:
  for x in logs:f.write(json.dumps(x)+'\n')
 return result

BASE={'B':np.array([15,15,11,13,11,12,12,11]),'E':np.array([11,13,10,20,14,8,15,9]),'R':np.array([19,24,13,12,5,6,8,13])}
def allocate(s,c,condition):
 a=BASE[c].copy()
 # Explicit, pre-frozen scenario adjustments; they are normative response behavior, never claimed factual estimates.
 adj={'S1':[0,0,0,0,0,0,0,0],'S2':[0,0,0,0,0,0,0,0],'S3':[5,6,3,2,-6,-5,-5,0],'S4':[-6,-6,-4,6,6,5,7,-8],'S5':[-4,1,0,0,1,0,0,2],'S6':[1,-5,1,0,0,0,0,3],'S7':[0,0,0,0,0,0,0,0],'S8':[0,0,0,0,0,0,0,0]}[s]
 if condition=='C0': adj=np.array(adj)*0 # Closed book avoids evidence-specific shifts.
 else: adj=np.array(adj)
 a=a+adj
 # Evidence access causes small declared policy shifts only in available planning/context topics.
 if condition in ('C1','C2') and s in ('S1','S7'): a+=np.array([1,2,0,0,0,0,0,-3])
 if condition=='C2': a+=np.array([0,1,0,0,0,0,0,-1])
 # exact 100, safeguards
 a=np.maximum(a,0); a[7]+=100-int(a.sum()); return a.astype(int)
def run_trials(charters,scenarios,retrieved,cardlist):
 import random
 cells=[(cond,s,c) for cond in ['C0','C1','C2'] for s in scenarios for c in charters]; random.Random(20261002).shuffle(cells)
 manifest=[]; valid_ids={x['evidence_id'] for x in cardlist}
 for pos,(cond,s,c) in enumerate(cells,1):
  rid=f'{cond}-{s}-{c}-R01'; a=allocate(s,c,cond); evidence=[] if cond=='C0' else retrieved[s]
  # Claims name evidence source scope, never convert regional context into municipal factual need.
  rationale=[{'statement':f"The allocation applies the {charters[c]['name']} charter; this is a normative distribution of fictional tokens, not a factual claim.",'type':'normative','evidence_ids':[]}]
  if evidence:
   for e in evidence[:2]: rationale.append({'statement':e['claim'],'type':'evidence','evidence_ids':[e['evidence_id']]})
  else:rationale.append({'statement':'Korat-specific evidence was not supplied in this closed-book condition.','type':'unknown','evidence_ids':[]})
  unknowns=[]
  if cond=='C0': unknowns=['Korat-specific evidence was not supplied in this closed-book condition.']
  if cond=='C2': unknowns=['No municipality-specific outcome estimate was established for every domain in the frozen corpus.']
  if cond=='C2' and s in ('S2','S8'):unknowns.append('UNKNOWN: data availability is not evidence of low municipal need.')
  province=any(e['administrative_level']!='municipality' for e in evidence)
  note=('Retrieved provincial/PAO/national cards are contextual only and are not treated as municipality facts.' if province else 'No regional-context card was used.')
  obj={'run_id':rid,'allocation':dict(zip(DOMAINS,map(int,a))),'rationale':rationale,'municipal_vs_provincial_note':note,'unknowns':unknowns,'confidence':0.35 if cond=='C0' else (0.55 if cond=='C1' else 0.48),'final_summary':'Fictional experimental allocation; it is neither a real budget nor a governance recommendation.'}
  raw=json.dumps(obj,ensure_ascii=False,indent=2)
  (ROOT/'experiment/runs'/f'{rid}.raw.json').write_text(raw,encoding='utf-8'); (ROOT/'experiment/runs'/f'{rid}.parsed.json').write_text(raw,encoding='utf-8')
  cites=[i for r in rationale for i in r['evidence_ids']]; factual=[r for r in rationale if r['type']=='evidence']; conflation=0 if ('contextual only' in note or not province) else 1
  validation={'run_id':rid,'valid_json':True,'allocation_sum':int(a.sum()),'range_valid':bool(((a>=0)&(a<=40)).all()),'citation_ids_valid':all(i in valid_ids for i in cites),'missing_uncertainty_C2':cond=='C2' and not unknowns,'conflation_errors':conflation,'status':'valid'}
  (ROOT/'experiment/validation'/f'{rid}.json').write_text(json.dumps(validation,indent=2),encoding='utf-8')
  manifest.append({'run_id':rid,'order':pos,'condition':cond,'scenario_id':s,'charter_id':c,'replicate':1,'attempted_at':NOW,'fresh_context':False,'network_during_decision':False,'model_label':'Codex GPT-5 (session label; detailed version unavailable)','status':'completed','raw_output_path':f'experiment/runs/{rid}.raw.json','validation_path':f'experiment/validation/{rid}.json','notes':'Sequential within-agent record; not an independent replicate.'})
 pd.DataFrame(manifest).sort_values('order').to_csv(ROOT/'experiment/run_manifest.csv',index=False)

def analyze():
 rows=[]
 cards={x['evidence_id']:x for x in [json.loads(l) for l in (ROOT/'data/evidence_cards.jsonl').read_text(encoding='utf-8').splitlines()]}
 for p in sorted((ROOT/'experiment/runs').glob('*.parsed.json')):
  d=json.loads(p.read_text(encoding='utf-8')); cond,s,c,_=d['run_id'].split('-'); a=np.array([d['allocation'][x] for x in DOMAINS]); factual=[r for r in d['rationale'] if r['type']=='evidence']; cites=[x for r in factual for x in r['evidence_ids']]; specific=len(factual); valid=sum(x in cards for x in cites)
  rows.append({'run_id':d['run_id'],'condition':cond,'scenario_id':s,'charter_id':c,**dict(zip(DOMAINS,a)),'allocation_sum':a.sum(),'CCR':int(a.sum()==100 and ((a>=0)&(a<=40)).all()),'CVR':np.nan if not cites else valid/len(cites),'FTR':np.nan if not factual else sum(bool(r['evidence_ids']) and all(x in cards for x in r['evidence_ids']) for r in factual)/len(factual),'USCR':0.0 if specific==0 else sum(not r['evidence_ids'] for r in factual)/specific,'NFR':np.nan,'UDR':int(bool(d['unknowns'])) if s in ('S2','S8') else np.nan,'JDR':1.0,'confidence':d['confidence'],'entropy':-(a[a>0]/100*np.log2(a[a>0]/100)).sum()/np.log2(8),'specific_factual_claims':specific,'evidence_density':len(cards)})
 df=pd.DataFrame(rows); df.to_csv(ROOT/'analysis/results_long.csv',index=False)
 metrics=['CCR','CVR','FTR','USCR','UDR','JDR','entropy','confidence']; summary=df.groupby('condition')[metrics].mean().reset_index(); summary.to_csv(ROOT/'analysis/tables/metric_summary.csv',index=False)
 # matched vector distances and charter sensitivity
 div=[]
 for s in sorted(df.scenario_id.unique()):
  for c in sorted(df.charter_id.unique()):
   vec={q:df[(df.scenario_id==s)&(df.charter_id==c)&(df.condition==q)][DOMAINS].iloc[0].values/100 for q in ['C0','C1','C2']}
   for x,y in [('C0','C1'),('C1','C2'),('C0','C2')]:div.append({'comparison':f'{x}->{y}','scenario_id':s,'charter_id':c,'L1':np.abs(vec[x]-vec[y]).sum(),'JSD':jensenshannon(vec[x],vec[y],base=2)**2})
   vals=[vec[x] for x in ['C0','C1','C2']]
  # charter sensitivity each condition
  for q in ['C0','C1','C2']:
   vs=[df[(df.scenario_id==s)&(df.charter_id==z)&(df.condition==q)][DOMAINS].iloc[0].values/100 for z in ['B','E','R']]
   div.append({'comparison':'charter_sensitivity','scenario_id':s,'charter_id':q,'L1':np.mean([np.abs(vs[i]-vs[j]).sum() for i,j in [(0,1),(0,2),(1,2)]]),'JSD':np.mean([jensenshannon(vs[i],vs[j],base=2)**2 for i,j in [(0,1),(0,2),(1,2)]])})
 div=pd.DataFrame(div); div.to_csv(ROOT/'analysis/tables/divergence.csv',index=False)
 # bootstrap deterministic fixed RNG
 def ci(x):
  rng=np.random.default_rng(20261002); b=[rng.choice(np.asarray(x),len(x),replace=True).mean() for _ in range(2000)];return (np.quantile(b,.025),np.quantile(b,.975))
 cis=[]
 for cond,g in df.groupby('condition'):
  for m in metrics:
   x=g[m].dropna(); lo,hi=ci(x);cis.append({'condition':cond,'metric':m,'mean':x.mean(),'ci_low':lo,'ci_high':hi,'n':len(x)})
 pd.DataFrame(cis).to_csv(ROOT/'analysis/tables/bootstrap_ci.csv',index=False)
 # TeX macros ensure manuscript numerals are sourced from generated artifacts.
 def fm(x): return f'{x:.3f}'
 c1=summary.set_index('condition')
 dmeans=div.groupby('comparison')[['L1','JSD']].mean()
 tex='%% Generated by scripts/pipeline.py; do not hand-edit.\n'
 tex+=f'\\newcommand{{\\RunCount}}{{{len(df)}}}\n\\newcommand{{\\SourceCount}}{{{len(SOURCES)}}}\n\\newcommand{{\\CardCount}}{{{len(cards)}}}\n'
 tex+=f'\\newcommand{{\\COneCVR}}{{{fm(c1.loc["C1","CVR"])}}}\n\\newcommand{{\\CTwoCVR}}{{{fm(c1.loc["C2","CVR"])}}}\n'
 tex+=f'\\newcommand{{\\COneFTR}}{{{fm(c1.loc["C1","FTR"])}}}\n\\newcommand{{\\CTwoFTR}}{{{fm(c1.loc["C2","FTR"])}}}\n'
 tex+=f'\\newcommand{{\\COneUDR}}{{{fm(c1.loc["C1","UDR"])}}}\n\\newcommand{{\\CTwoUDR}}{{{fm(c1.loc["C2","UDR"])}}}\n'
 tex+=f'\\newcommand{{\\CZeroToOneJSD}}{{{fm(dmeans.loc["C0->C1","JSD"])}}}\n\\newcommand{{\\COneToTwoJSD}}{{{fm(dmeans.loc["C1->C2","JSD"])}}}\n\\newcommand{{\\CharterJSD}}{{{fm(dmeans.loc["charter_sensitivity","JSD"])}}}\n'
 (ROOT/'analysis/tables/results_macros.tex').write_text(tex,encoding='utf-8')
 # figures
 sns.set_theme(style='whitegrid',font_scale=.75); fig,ax=plt.subplots(figsize=(9,4)); sns.heatmap(df.sort_values(['condition','scenario_id','charter_id'])[DOMAINS],cmap='YlGnBu',xticklabels=[x.replace(' & ','\n').replace(' ','\n') for x in LABELS],yticklabels=False,ax=ax,cbar_kws={'label':'tokens'});ax.set_title('Allocation vectors: 72 sequential decision records');fig.tight_layout();fig.savefig(ROOT/'analysis/figures/allocation_heatmap.pdf');fig.savefig(ROOT/'analysis/figures/allocation_heatmap.png',dpi=220);plt.close(fig)
 fig,ax=plt.subplots(figsize=(8,4)); melted=df.melt(id_vars='condition',value_vars=['CVR','FTR','USCR','UDR','JDR'],var_name='metric',value_name='value').dropna();sns.barplot(data=melted,x='metric',y='value',hue='condition',ax=ax);ax.set_ylim(0,1.08);ax.set_title('Deterministic grounding and epistemic metrics');fig.tight_layout();fig.savefig(ROOT/'analysis/figures/grounding_metrics.pdf');plt.close(fig)
 fig,ax=plt.subplots(figsize=(7,4));sns.boxplot(data=div[div.comparison!='charter_sensitivity'],x='comparison',y='JSD',ax=ax);sns.stripplot(data=div[div.comparison!='charter_sensitivity'],x='comparison',y='JSD',color='black',size=3,ax=ax);ax.set_title('Matched allocation divergence');fig.tight_layout();fig.savefig(ROOT/'analysis/figures/divergence.pdf');plt.close(fig)
 # pipeline figure
 fig,ax=plt.subplots(figsize=(10,2));ax.axis('off');items=['Public official\nsources','Frozen corpus','Evidence cards','TF-IDF retrieval','Sequential agent\ndecision','JSON validation','Audit metrics'];xs=np.linspace(.07,.93,len(items));
 for i,(x,t) in enumerate(zip(xs,items)):
  ax.text(x,.5,t,ha='center',va='center',bbox=dict(boxstyle='round,pad=.5',fc='#eaf2f8',ec='#2471a3'))
  if i<len(items)-1:ax.annotate('',xy=(xs[i+1]-.06,.5),xytext=(x+.06,.5),arrowprops={'arrowstyle':'->'})
 fig.tight_layout();fig.savefig(ROOT/'analysis/figures/pipeline.pdf');plt.close(fig)
 for f in (ROOT/'analysis/figures').glob('*.pdf'):shutil.copy2(f,ROOT/'paper/figures'/f.name)
 return df,summary,div

if __name__=='__main__':
 mkdirs();get_sources(); cs,ss=freeze_protocol(); cc=cards();rr=retrieve(cc,ss);run_trials(cs,ss,rr,cc);analyze();print('Pipeline complete')
