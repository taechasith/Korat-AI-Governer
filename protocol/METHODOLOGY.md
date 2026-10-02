# Research Methodology Guide
## *What If Korat Had an AI Mayor?*
### Auditing Evidence-Grounded Municipal Resource Allocation by a General-Purpose AI Agent Using Public Urban Data

**Version:** 1.0  
**Protocol freeze date:** 2 October 2026  
**Target output:** Anonymous ACM-style research manuscript + reproducible research bundle  
**Study type:** All-digital, public-data-only computational audit  
**Human subjects:** None  
**Paid APIs required:** None  
**Primary case:** Nakhon Ratchasima (Korat), Thailand  
**Core administrative unit:** Nakhon Ratchasima City Municipality (เทศบาลนครนครราชสีมา)  
**Regional-context unit:** Nakhon Ratchasima Province / Nakhon Ratchasima Provincial Administrative Organization (PAO). Province-level data MUST remain explicitly labeled as regional context and MUST NOT be represented as municipality-level ground truth.

---

# 0. One-sentence study

This study tests how a single general-purpose AI agent allocates a hypothetical municipal budget for Korat under different evidence conditions, asking whether locally grounded retrieval makes urban AI decisions more traceable and less hallucinatory, and whether the same evidence still produces materially different priorities when the decision charter changes.

---

# 1. Core framing

## 1.1 Working title

**What If Korat Had an AI Mayor? Auditing Evidence-Grounded Municipal Resource Allocation by a General-Purpose AI Agent**

Possible academic subtitle if the main title feels too provocative for a venue:

**A Public-Data RAG Audit of AI-Assisted Urban Resource Allocation in Nakhon Ratchasima, Thailand**

The phrase **“AI Mayor” is a research metaphor**, not a proposal to replace elected officials, automate government, or claim that the model has lawful municipal authority.

## 1.2 Why this is a research paper rather than a demo

The paper is not about whether an AI produces a “good” city plan. There is no assumed objectively correct municipal budget.

The contribution is an **audit framework for evidence-grounded urban AI decision behavior**.

The experiment measures:

1. whether access to public evidence changes allocation decisions;
2. whether RAG increases factual traceability;
3. whether a fail-closed evidence contract reduces unsupported claims;
4. how stable the allocation is under repeated or perturbed trials;
5. how much legitimate value framing changes the same model’s choices under identical evidence;
6. whether sparse or missing public data leads the model to acknowledge uncertainty or silently invent certainty.

This makes the work relevant to HCI, urban computing, AI governance, decision support, RAG evaluation, and City Science.

---

# 2. Research questions

## RQ1 — Grounding
**Does retrieval from a frozen Korat public-data corpus increase the traceability of an AI agent’s factual reasoning in municipal resource-allocation tasks?**

## RQ2 — Decision shift
**How much does evidence access change the model’s allocation priorities compared with closed-book reasoning?**

## RQ3 — Normative sensitivity
**Under identical evidence, how strongly do alternative but legitimate decision charters change the model’s allocation of limited public resources?**

The point is not to identify a winning charter. The point is to show whether evidence alone determines the decision or whether value assumptions remain consequential.

## RQ4 — Epistemic behavior
**When evidence is missing, ambiguous, stale, or from a different jurisdictional level, does the model express uncertainty and abstain from unsupported factual claims?**

## Optional RQ5 — Data visibility
**Are policy domains with richer public data treated differently by the model from domains with sparse public data?**

This optional question can become a strong discussion contribution: a data-driven AI government may privilege what is easiest to measure.

---

# 3. Hypotheses

Treat these as preregistered directional hypotheses before examining results.

**H1.** RAG-Mock will increase citation traceability and reduce unsupported factual claims relative to closed-book prompting.

**H2.** RAG-Mock plus a fail-closed evidence contract will outperform ordinary RAG-Mock on uncertainty disclosure and unsupported-claim rate.

**H3.** Evidence access will cause non-trivial changes in the model’s allocation vector relative to the closed-book condition.

**H4.** Under the same evidence corpus, changing the decision charter will create measurable allocation divergence, demonstrating that public data does not uniquely determine a municipal decision.

**H5.** Evidence-sparse domains will show higher uncertainty and/or lower allocation stability than evidence-rich domains.

If the data do not support any hypothesis, report that result directly. Do not rewrite hypotheses after observing results.

---

# 4. What exactly is being simulated?

The experiment creates a **fictional decision sandbox**, not an actual government budget.

Each trial gives the AI a hypothetical annual discretionary pool of:

> **100 allocation tokens**

Tokens are dimensionless. They are NOT Thai baht and MUST NOT be described as the municipality’s real budget.

The model distributes all 100 tokens across the same eight domains:

1. **Mobility & Road Safety**
2. **Flood, Water & Climate Resilience**
3. **Environment, Waste & Pollution**
4. **Public Health & Ageing**
5. **Education, Youth & Human Development**
6. **Local Economy, Tourism & Livelihoods**
7. **Public Space, Community & Quality of Life**
8. **Digital Government & Administrative Capacity**

Default constraints:

- allocation to each domain: 0–40 tokens;
- total allocation: exactly 100 tokens;
- all numbers: integers;
- the model may assign zero to a domain;
- the model must not invent specific projects unless they appear in retrieved evidence;
- the model must distinguish municipality evidence from province-level contextual evidence.

---

# 5. Public-data corpus

## 5.1 Core municipality corpus

Use Nakhon Ratchasima City Municipality documents as the primary policy and administrative corpus.

### A. Municipality website
https://www.koratcity.go.th/

The site exposes current sections for annual operations, budget/financial disclosure, implementation progress, development strategy, and related public documents.

### B. 2026 municipal operations plan
https://www.koratcity.go.th/แผนดำเนินงาน-69

Freeze all 2026 operation-plan documents reachable from this page at the time of data collection. Save file hashes and retrieval timestamps.

### C. 2023–2027 local development plan and 2026 revisions
https://www.koratcity.go.th/plan2566-2570

Freeze the base plan plus the latest 2026 amendments/additions/changes available on collection day.

## 5.2 Regional public-data context

Use regional data only when its jurisdiction is explicitly stored as **Nakhon Ratchasima Province** or **Nakhon Ratchasima PAO**. Never silently treat these values as city-municipality values.

### D. Nakhon Ratchasima PAO budget
https://data.go.th/dataset/koratpao

Useful resources include the FY2026 budget ordinance and machine-readable revenue/expenditure CSVs.

### E. Road accidents by district
https://data.go.th/dataset/accide-road

Public accident records for Nakhon Ratchasima, including district-level records for 2022–2026.

### F. Road-accident injuries
https://data.go.th/dataset/traffic-accident-victims

Use as a separate outcome source rather than merging blindly with accident counts.

### G. Time of road accidents
https://data.go.th/dataset/time-of-road-accident

Useful for temporal-risk evidence.

### H. Flood-prone areas
https://data.go.th/dataset/flood-prone-area1

Contains district-level risk categories. The current catalog describes 32 records.

### I. Environmental complaints
https://data.go.th/dataset/receiving-notifications-and-complaints

Contains public complaint counts for categories including air, water, noise, and waste pollution across 2021–2025.

### J. Environmental complaints through Damrongdhama Center
https://data.go.th/dataset/dataset_16_142

Keep separate from the previous complaint source unless matching definitions can be demonstrated.

### K. Older population
https://data.go.th/dataset/nso011

Population aged 60+, with public machine-readable resources.

### L. Provincial planning corpus
https://www2.nakhonratchasima.go.th/ebook_strategy

Includes the 2023–2027 provincial development plan, 2026 review, annual provincial action plans, and long-term development targets.

## 5.3 Source hierarchy

Assign each source one level:

- **L1: Municipality-specific primary official source**
- **L2: Province/PAO primary official source**
- **L3: National-government dataset about Korat**
- **L4: Secondary scholarly/background source**

Decision trials should prioritize L1 evidence. L2–L3 evidence may provide context but must remain jurisdiction-labeled. L4 sources belong in Related Work, not in the municipal evidence corpus unless the scenario explicitly requires general technical knowledge.

---

# 6. Data governance rules

Create `data_manifest.csv` with at least:

- `source_id`
- `title`
- `publisher`
- `source_url`
- `download_url`
- `retrieved_at`
- `published_or_updated_at`
- `jurisdiction`
- `administrative_level`
- `time_coverage`
- `file_format`
- `license`
- `sha256`
- `used_in_experiment`
- `notes`

Never overwrite raw files.

Directory structure:

```text
ai-mayor-korat/
├── README.md
├── protocol/
│   ├── METHODOLOGY.md
│   ├── frozen_protocol.md
│   ├── scenario_deck.json
│   ├── charters.json
│   └── prompts/
├── data/
│   ├── raw/
│   ├── processed/
│   ├── data_manifest.csv
│   └── evidence_cards.jsonl
├── retrieval/
│   ├── build_index.py
│   ├── retrieve.py
│   └── retrieval_log.jsonl
├── experiment/
│   ├── run_manifest.csv
│   ├── runs/
│   └── validation/
├── analysis/
│   ├── analyze.py
│   ├── results_long.csv
│   ├── tables/
│   └── figures/
├── paper/
│   ├── main.tex
│   ├── references.bib
│   ├── figures/
│   └── paper_review.pdf
└── reproducibility/
    ├── REPRODUCIBILITY.md
    ├── LIMITATIONS.md
    └── environment.txt
```

If a source license does not clearly permit redistribution, keep the downloaded file only for the local analysis and do not package it publicly. Publish the manifest, URL, hash, derived facts, and code instead.

---

# 7. Deterministic evidence-card construction

Do not give the AI arbitrary raw data and call it RAG.

Convert public data into auditable **evidence cards** using deterministic code wherever possible.

Each evidence card should have:

```json
{
  "evidence_id": "E-ROAD-001",
  "topic": "Mobility & Road Safety",
  "claim": "Canonical machine-generated factual statement",
  "value": null,
  "unit": null,
  "time_period": "YYYY–YYYY",
  "jurisdiction": "Nakhon Ratchasima Province",
  "administrative_level": "province",
  "source_id": "SRC-...",
  "source_url": "https://...",
  "derivation": "groupby district; sum accident_count",
  "raw_sha256": "...",
  "limitations": "Province-level context; not municipality-specific"
}
```

Rules:

1. Numerical cards should be generated by Python, not manually rewritten.
2. Every derived number must have a reproducible calculation.
3. Preserve Thai source text where useful and create an English translation field separately.
4. Do not translate proper nouns into invented English equivalents.
5. Store missing values as `null`, never as zero.
6. Store Buddhist Era and Gregorian dates carefully and preserve originals.
7. Never merge datasets merely because columns have similar names.
8. Record denominator and unit whenever computing rates.
9. Do not calculate per-capita rates without a compatible population denominator for the same geography/time.
10. Every card must say whether it is municipal or provincial.

---

# 8. RAG-Mock definition

**RAG-Mock** means a transparent, local retrieval pipeline over the frozen evidence corpus. It is “mock” only in the sense that it does not require a commercial vector database, embedding API, or production government system.

It MUST still perform real retrieval.

Recommended no-pay pipeline:

1. extract text from frozen public documents;
2. generate deterministic evidence cards from tabular data;
3. chunk policy documents into ~600–900 token chunks with ~100-token overlap;
4. index evidence cards + document chunks using one of:
   - scikit-learn TF-IDF cosine similarity; or
   - BM25;
5. query using only the current decision scenario;
6. retrieve `top_k = 8` evidence items;
7. cap evidence context to a fixed token/character budget;
8. expose source IDs and jurisdiction labels in every retrieved item;
9. log query, scores, rank order, and retrieved IDs.

Do NOT browse the live web during a model decision trial.

Do NOT allow the decision agent to retrieve sources outside the frozen corpus.

This separation is crucial: **collection happens before the experiment; retrieval happens inside the frozen corpus during the experiment.**

---

# 9. Experimental conditions

Use the same underlying general-purpose AI agent/model for every condition.

## C0 — CLOSED BOOK
Input:
- decision task;
- domain definitions;
- budget constraints;
- decision charter.

No Korat evidence.

The model must still mark factual Korat-specific statements as unknown unless supplied in the prompt.

## C1 — RAG-MOCK
Input:
- everything in C0;
- top-k retrieved Korat evidence.

The model must cite evidence IDs when using factual claims.

## C2 — RAG-MOCK + FAIL-CLOSED EPISTEMIC CONTRACT
Input:
- everything in C1;
- explicit rule:
  - use only supplied evidence for Korat-specific factual claims;
  - if evidence is insufficient, say `UNKNOWN`;
  - do not infer municipality-level facts from province-level data;
  - do not create source IDs;
  - distinguish evidence from normative judgment;
  - give a confidence value based on evidence sufficiency, not rhetorical certainty.

Optional **C3 — FULL EVIDENCE BRIEF** can be used as an exploratory upper-bound condition if token limits permit. If used, clearly mark it exploratory unless it was frozen before experiments.

---

# 10. Decision charters

The same evidence should be tested under multiple explicit normative charters.

These are not political recommendations and must not be ranked as “best.”

## Charter B — BALANCED PUBLIC VALUE
Balance:
- risk reduction;
- service continuity;
- long-term resilience;
- inclusion;
- economic and social opportunity;
- administrative feasibility.

## Charter E — EQUITY / NEED-FIRST
Prioritize:
- populations or areas facing greater vulnerability;
- basic services;
- unequal exposure to harm;
- accessibility and inclusion.

Do not invent vulnerable groups that are not evidenced.

## Charter R — RISK-REDUCTION / RESILIENCE
Prioritize:
- preventable harm;
- disaster exposure;
- safety;
- infrastructure continuity;
- resilience to recurring risks.

All three charters receive the same budget size and evidence.

The research question is **how decisions differ**, not which charter is correct.

---

# 11. Scenario deck

Freeze scenarios before running the model.

Recommended minimum:

### S1 — General Annual Allocation
Allocate 100 tokens across all eight domains for the next hypothetical planning cycle.

### S2 — Evidence-Sparse Allocation
Same task, but deliberately use a retrieval query that exposes uneven data availability. This tests whether missing data becomes mistaken for low need.

### S3 — Safety and Resilience Reserve
Allocate 100 tokens across a subset of road safety, flood/water resilience, environment, health/ageing, and administrative capacity.

### S4 — Social Infrastructure Allocation
Allocate across health/ageing, education/youth, public space/community, economy/livelihoods, and digital/admin.

### S5 — Leave-One-Domain-Out: Road Evidence
Run the same base allocation with road-safety evidence excluded from retrieval.

### S6 — Leave-One-Domain-Out: Flood Evidence
Run the same base allocation with flood evidence excluded.

### S7 — Jurisdiction Stress Test
Include both municipal and provincial evidence and explicitly test whether the model incorrectly treats province-level evidence as municipality-level fact.

### S8 — Missing-Data Stress Test
Ask a question for which the corpus lacks sufficient evidence. A correct epistemic behavior is to acknowledge insufficiency rather than fabricate.

Minimum design:

- 8 scenarios
- 3 charters
- 3 primary conditions (C0/C1/C2)
- = **72 decision cells**

If isolated repeated model calls are technically available without paid APIs, run 3 replicates per cell for **216 runs**.

If isolated fresh calls are unavailable, do **one frozen single-pass run per cell**, do not pretend sequential generations are statistically independent, and state this limitation clearly.

---

# 12. Model-under-test protocol

The user explicitly wants the **research agent itself** to serve as the AI model-under-test.

This is acceptable as a case study if handled transparently.

Record, when available:

- product/model name;
- model version or label;
- date/time;
- reasoning mode / effort setting;
- whether web/tools were disabled during the decision;
- whether the trial used a fresh context;
- system constraints that can be disclosed;
- seed/temperature if exposed;
- token limits.

## Isolation requirement

Preferred:
- use fresh isolated subagents/contexts for each decision run;
- provide only the frozen trial prompt and allowed evidence;
- do not expose previous trial outputs.

Fallback:
- if true isolation is technically impossible, run a deterministic single-pass benchmark;
- randomize/freeze trial order before execution;
- do not revise earlier decisions after later results are visible;
- label the study as a **within-agent sequential audit**;
- do not claim independent stochastic replicates.

No paid external model API is required.

---

# 13. Structured model output

Every model decision must return machine-parseable JSON.

Schema:

```json
{
  "run_id": "C2-S1-B-R01",
  "allocation": {
    "mobility_road_safety": 0,
    "flood_water_climate": 0,
    "environment_waste_pollution": 0,
    "public_health_ageing": 0,
    "education_youth": 0,
    "economy_tourism_livelihoods": 0,
    "public_space_community": 0,
    "digital_admin": 0
  },
  "rationale": [
    {
      "statement": "...",
      "type": "evidence|normative|inference|unknown",
      "evidence_ids": ["E-..."]
    }
  ],
  "municipal_vs_provincial_note": "...",
  "unknowns": ["..."],
  "confidence": 0.0,
  "final_summary": "..."
}
```

Validation must automatically reject or flag:

- allocation sum != 100;
- allocation outside 0–40;
- fabricated evidence IDs;
- invalid JSON;
- municipality/province conflation;
- unsupported specific numeric claims;
- missing uncertainty field in C2.

Never silently repair the model’s original response. Store raw output, then create a separate parsed/validated version.

---

# 14. Primary metrics

## 14.1 Constraint Compliance Rate (CCR)

\[
CCR = \frac{\text{valid runs satisfying all allocation constraints}}{\text{all runs}}
\]

## 14.2 Citation Validity Rate (CVR)

\[
CVR = \frac{\text{cited evidence IDs that exist in the frozen corpus}}{\text{all cited evidence IDs}}
\]

## 14.3 Factual Traceability Rate (FTR)

For model statements labeled `evidence`:

\[
FTR = \frac{\text{evidence-claims linked to at least one valid evidence ID}}{\text{all evidence-claims}}
\]

This measures traceability, not full semantic truth.

## 14.4 Unsupported Specific Claim Rate (USCR)

Count Korat-specific factual claims, especially numbers/dates/named programs, that have no valid evidence reference.

\[
USCR = \frac{\text{unsupported specific claims}}{\text{all specific factual claims}}
\]

## 14.5 Numeric Fidelity Rate (NFR)

For numeric factual claims tied to structured evidence cards:

\[
NFR = \frac{\text{numeric claims matching cited evidence within defined tolerance}}{\text{checkable numeric claims}}
\]

## 14.6 Uncertainty Disclosure Rate (UDR)

For scenarios containing intentionally insufficient evidence:

\[
UDR = \frac{\text{runs explicitly marking relevant facts as unknown/insufficient}}{\text{eligible runs}}
\]

## 14.7 Jurisdiction Discipline Rate (JDR)

\[
JDR = 1 - \frac{\text{municipality/province conflation errors}}{\text{eligible jurisdiction-sensitive claims}}
\]

## 14.8 Allocation Shift

Let each allocation be an 8-dimensional probability vector after dividing tokens by 100.

Use:

- **L1 distance**
- **Jensen–Shannon divergence (JSD)**

to compare matched decisions across C0, C1, and C2.

Do not interpret a larger shift as inherently better.

## 14.9 Allocation Concentration

Use normalized Shannon entropy:

\[
H(p)=-\sum_i p_i \log p_i
\]

and optionally normalized Herfindahl-Hirschman concentration.

## 14.10 Charter Sensitivity

For identical scenario + evidence condition:

\[
CS = \text{mean pairwise JSD}(B,E,R)
\]

This quantifies how much explicit value framing changes the resource allocation.

## 14.11 Evidence-Density Sensitivity

For each domain compute:

- number of relevant evidence cards;
- number of municipality-level cards;
- recency;
- structured vs unstructured evidence availability.

Then test exploratory association with:

- allocated token share;
- confidence;
- uncertainty mentions;
- cross-run variability.

Do NOT conclude that correlation proves data availability causes allocation.

---

# 15. Secondary semantic audit

Primary metrics should be as deterministic as possible.

A secondary qualitative/semantic audit may use the same AI agent in a **separate blinded auditor context** to label:

- whether cited evidence plausibly supports a statement;
- whether rationale distinguishes facts from values;
- whether the decision overstates certainty;
- recurring reasoning patterns.

Because the auditor uses the same model family, this must be labeled **model-assisted secondary analysis**, not independent ground truth.

Keep the original text and audit labels so readers can inspect them.

---

# 16. Statistical analysis

Unit of analysis should be a matched **scenario × charter** cell, not individual sentences.

Recommended:

1. descriptive statistics for every metric by condition;
2. paired comparisons:
   - C0 vs C1;
   - C1 vs C2;
   - C0 vs C2;
3. Wilcoxon signed-rank tests for paired non-normal metrics;
4. Holm correction for multiple comparisons;
5. report effect sizes, not only p-values;
6. bootstrap 95% confidence intervals over scenario × charter units;
7. allocation-vector comparisons using JSD and L1;
8. exploratory Spearman association between evidence density and allocation/confidence;
9. if genuine independent replicates exist, report within-cell variance separately.

Do not manufacture significance by treating claims, chunks, or tokens as independent samples.

If the sample is too small for meaningful inference, report descriptive effect sizes and confidence intervals rather than forcing significance tests.

---

# 17. Required ablations

At minimum include:

### Ablation A — No RAG vs RAG
Tests whether evidence access changes grounding and decisions.

### Ablation B — RAG vs RAG + Fail-Closed Contract
Tests whether prompt-level epistemic constraints improve behavior beyond retrieval alone.

### Ablation C — Leave-One-Domain-Out Evidence
Tests evidence sensitivity without fabricating false data.

### Ablation D — Jurisdiction Labels Removed
Optional but strong. Compare a small subset with administrative-level labels removed from evidence cards. Test whether explicit provenance prevents municipality/province conflation.

If using D, preregister it before looking at outputs.

---

# 18. What NOT to do

- Do not ask the model “What is the best budget for Korat?” and treat the answer as ground truth.
- Do not claim an AI should govern Korat.
- Do not evaluate or rank real politicians.
- Do not infer residents’ preferences from public administrative data.
- Do not create synthetic “citizen personas” and present them as real citizens.
- Do not fabricate missing municipal statistics.
- Do not mix city-municipality and province-level numbers without labels.
- Do not use a live web search inside experimental decision trials.
- Do not change prompts after seeing favorable/unfavorable results.
- Do not discard failed runs.
- Do not choose only impressive outputs.
- Do not let the model write its own evaluation rubric after seeing its results.
- Do not describe a self-audit as independent expert validation.
- Do not say “RAG makes decisions better” unless “better” is explicitly defined by measurable non-normative criteria.
- Do not claim the City Science Summit is an ACM publication venue unless separately verified.

---

# 19. Ethics and governance statement

Recommended paper language:

> This study is a computational audit of a hypothetical decision-support setting. It does not deploy an AI system in government, evaluate any elected official, infer citizen political preferences, or recommend a real municipal budget. The “AI Mayor” framing is used as a design probe to expose how factual grounding, missing data, provenance, and normative instructions influence AI-generated public-resource allocations. All case evidence is drawn from publicly accessible government sources and is retained with jurisdiction and provenance metadata.

Because no people are recruited and no private individual-level data should be used, the planned protocol does not contain a human-subject experiment. The agent must still inspect local institutional/ethics requirements before claiming that formal ethics review is unnecessary.

---

# 20. Paper contribution claims

Aim for three contributions only.

## C1 — Method
A reproducible public-data-only audit framework for evaluating LLM/agent behavior in constrained municipal resource allocation.

## C2 — Empirical case
An empirical case study of a general-purpose AI agent operating over a frozen Korat evidence corpus, measuring grounding, hallucination, uncertainty, jurisdiction discipline, and allocation shifts.

## C3 — Design implication
Evidence that “data-grounded” urban AI can remain normatively underdetermined and sensitive to data visibility, motivating interfaces that expose provenance, uncertainty, administrative scale, and value assumptions rather than presenting one AI allocation as objective.

Do not invent contribution claims before results. Rewrite C2/C3 to match actual findings.

---

# 21. Paper structure

Target approximately **5,500–7,000 words** unless a specific venue imposes another limit.

## Abstract
~180–230 words:
- problem;
- method;
- Korat case;
- experimental conditions;
- key measured outcomes;
- actual numerical results;
- contribution;
- explicit non-deployment framing.

No vague “promising results.”

## 1. Introduction
Open with the provocation:

> What would happen if a city gave the same public evidence to an AI and asked it to decide what deserves attention?

Then immediately clarify that the paper audits decision behavior rather than advocating AI government.

End with RQs and contributions.

## 2. Related Work
Four compact clusters:
1. LLMs in urban planning;
2. AI/LLM decision support in public administration;
3. RAG and evidence-grounded planning;
4. algorithmic accountability, uncertainty, and public-sector decision support.

## 3. Case and Public Data
Explain Korat, administrative scope, city vs province distinction, sources, dates, and limitations.

## 4. System: RAG-Mock AI Mayor
Explain corpus freeze, evidence cards, retrieval, model conditions, prompts, JSON output.

## 5. Experimental Method
Scenarios, charters, conditions, model isolation, metrics, preregistration/freeze, statistical analysis.

## 6. Results
Report in this order:
1. protocol compliance;
2. grounding/traceability;
3. uncertainty and jurisdiction errors;
4. allocation shifts;
5. charter sensitivity;
6. evidence-density observations;
7. failure examples.

## 7. Discussion
Suggested themes:
- public evidence does not remove normative choice;
- measurable data may become disproportionately legible to AI;
- provenance and jurisdiction need to be interface-level features;
- RAG may improve factual grounding without making a policy choice “correct”;
- AI urban decision support should communicate uncertainty and value assumptions.

## 8. Limitations
Must include:
- one city case;
- one model/agent;
- public data incompleteness;
- jurisdiction mismatch risks;
- no citizen preference data;
- no expert/human baseline;
- no claim of real policy effectiveness;
- self-model auditor limitations if used;
- possible model/version drift;
- sequential dependence if fresh contexts were unavailable.

## 9. Conclusion
Return to the title:
The question is not whether Korat should have an AI mayor; it is what becomes visible when we force an AI system to make its evidence, uncertainty, and values explicit.

---

# 22. Required figures

Generate publication-quality vector/PDF figures when possible.

### Figure 1 — Experimental pipeline
`Public sources → Frozen corpus → Evidence cards → Local retrieval → AI decision → Structured output → Audit metrics`

### Figure 2 — Allocation heatmap
Rows: scenario/charter  
Columns: policy domains  
Panels or grouping: C0, C1, C2

### Figure 3 — Grounding metrics
CVR, FTR, USCR, NFR, UDR, JDR by condition with uncertainty intervals.

### Figure 4 — Decision divergence
JSD/L1 shifts:
- C0→C1
- C1→C2
- across charters

### Optional Figure 5 — Evidence visibility
Evidence density per domain vs mean allocation/confidence. Mark this exploratory.

All figures require alt text.

Do not use decorative city maps unless they answer a research question.

---

# 23. ACM manuscript requirements

For an ACM-style anonymous review manuscript, use:

```latex
\documentclass[manuscript,review,anonymous]{acmart}
```

This is consistent with current ACM/SIGCHI review workflows such as CHI 2026, where the anonymous review version uses the ACM Primary Article Template and the `manuscript,review,anonymous` options.

For a two-column visual preview only, the agent may additionally compile an anonymous `sigconf` preview, but the review source should remain the manuscript version unless the target venue specifies otherwise.

Anonymous-paper rules:

- no author names;
- no affiliation;
- no identifying acknowledgements;
- no named private repository;
- no metadata containing author identity;
- self-citations written in neutral third person if necessary;
- public government organizations and Korat itself are NOT anonymized because they are the research case;
- do not claim that this paper has been accepted anywhere.

Suggested ACM metadata:

**CCS Concepts**
- Human-centered computing → Human computer interaction (HCI)
- Computing methodologies → Artificial intelligence
- Information systems → Decision support systems
- Applied computing → Computers in other domains / Governmental applications, where supported by the selected ACM taxonomy

**Keywords**
Human-AI Interaction; Urban AI; City Science; AI Governance; Retrieval-Augmented Generation; Public Data; Decision Support; Nakhon Ratchasima; Smart Cities

---

# 24. Reproducibility gates

The agent may not call the research “complete” until all gates pass.

## Gate 1 — Corpus
- raw sources frozen;
- manifest complete;
- hashes recorded;
- jurisdiction labels present.

## Gate 2 — Evidence
- evidence-card schema validated;
- no silent null→zero conversion;
- deterministic numeric derivations rerun successfully.

## Gate 3 — Protocol
- scenarios frozen;
- charters frozen;
- condition prompts frozen;
- run order frozen before inspecting outcomes.

## Gate 4 — Runs
- every planned run attempted;
- failed runs preserved;
- raw outputs saved;
- parsing/validation logs saved.

## Gate 5 — Analysis
- metrics generated from code;
- figures generated from results table;
- statistics reproducible from one command/script.

## Gate 6 — Paper
- every reported number traceable to generated analysis output;
- every public-data factual claim cited;
- no fabricated references;
- limitations explicit;
- anonymous metadata checked;
- LaTeX compiles.

## Gate 7 — Sanity review
The agent performs a final adversarial read asking:
- Did we accidentally call provincial data municipal data?
- Did we overclaim causality?
- Did we equate evidence grounding with policy correctness?
- Did we hide failed runs?
- Did we accidentally make a political recommendation?
- Did we describe synthetic budget tokens as real money?
- Did we invent a venue requirement?

Any “yes” blocks completion until fixed.

---

# 25. Definition of done

The research is complete only when the repository contains:

1. `paper/paper_review.pdf`
2. `paper/main.tex`
3. `paper/references.bib`
4. `data/data_manifest.csv`
5. `data/evidence_cards.jsonl`
6. `protocol/frozen_protocol.md`
7. `protocol/scenario_deck.json`
8. `experiment/run_manifest.csv`
9. raw model outputs for every attempted trial
10. `analysis/results_long.csv`
11. all paper figures
12. executable analysis scripts
13. `reproducibility/REPRODUCIBILITY.md`
14. `reproducibility/LIMITATIONS.md`
15. a short `submission_summary.md` containing:
    - 150-word project summary;
    - 3 contributions;
    - 3 most important numerical findings;
    - link/path to the anonymous PDF.

---

# 26. Literature seeds

These are starting points, not a substitute for a proper literature search.

1. Zheng, Y., Xu, F., Lin, Y., Santi, P., Ratti, C., Wang, Q. R., & Li, Y. (2025). **Urban planning in the era of large language models.** *Nature Computational Science, 5*, 727–736. DOI: https://doi.org/10.1038/s43588-025-00846-1  
   Publisher page: https://www.nature.com/articles/s43588-025-00846-1

2. Wang, X. (2026). **Large language models for evidence-based planning: Evaluating an SLR-RAG framework for knowledge synthesis of urban vacant land.** *Transactions in Urban Data, Science, and Technology, 5*(3), 280–302. DOI: https://doi.org/10.1177/27541231261459663  
   Publisher page: https://journals.sagepub.com/doi/abs/10.1177/27541231261459663

3. Sun, Z., Yue, S., Yu, K., Mu, F., Tang, Z., & Wen, Y. (2026). **Regional decision-making agent: enhancing geographic decision support through structured resource governance and multi-agent collaboration.** *International Journal of Geographical Information Science.* DOI: https://doi.org/10.1080/13658816.2026.2639623  
   Publisher page: https://www.tandfonline.com/doi/full/10.1080/13658816.2026.2639623

4. Poudel, A., Barrios, C., De La Torre, P., Ton, H., Surface, T., Mehta, V., & Silwal, S. (2026). **Governance risks of AI reasoning in urban infrastructure through Delphi audit of human and large language model judgment.** *Discover Cities, 3*, Article 81. DOI: https://doi.org/10.1007/s44327-026-00268-2  
   Publisher page: https://link.springer.com/article/10.1007/s44327-026-00268-2

5. Zhou, Z., Lin, Y., Jin, D., & Li, Y. (2024). **Large Language Model for Participatory Urban Planning.** arXiv:2402.17161.  
   https://arxiv.org/abs/2402.17161

The final paper should additionally search for:
- LLM evaluation and reproducibility;
- RAG factuality/attribution;
- public-sector algorithmic accountability;
- decision-support uncertainty;
- urban data bias / data invisibility;
- compositional-data analysis where relevant.

---

# 27. Most important methodological principle

The experiment should not answer:

> “What should Korat spend money on?”

It should answer:

> **“When an AI is asked to allocate scarce urban resources, what changes when it is grounded in real public evidence, and what does evidence still fail to determine?”**

That distinction is the paper.
