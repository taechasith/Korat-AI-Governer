# Frozen protocol

**Freeze timestamp:** 2026-10-02T00:00:00+07:00. **Status:** frozen before decision records.

This file adopts version 1.0 of `METHODOLOGY.md` without outcome-driven amendments. RQ1-RQ4 and H1-H5, the eight fixed domains, C0/C1/C2, three charters, eight scenarios, 100 integer allocation tokens, top_k=8 TF-IDF cosine retrieval, JSON schema, and matched scenario x charter analysis are frozen exactly as specified. The optional C3 and optional label-removal ablation are not run.

**Execution constraint.** No free fresh-context inference endpoint was exposed to the research orchestrator. The 72 records are therefore one attempt per frozen cell in precommitted randomized order, labelled a within-agent sequential audit; they are not independent samples or stochastic replicates. Decision records have no network access and use only the frozen retrieval output where applicable.

**Model disclosure.** Model label exposed in this session: Codex, GPT-5; product/version details, seed, temperature, and token limit are not exposed. The orchestrator and decision author are the same agent; this is not an independent evaluator.

**Metric operationalization.** Specific factual claims are rationale records with type `evidence`; C0 has no Korat-specific evidence claims. CVR validates cited IDs, FTR validates evidence-claim linkage, USCR counts evidence claims without valid IDs, NFR checks explicit numeric claims (none are emitted because frozen cards contain no numeric municipal facts), UDR is eligible in S2/S8, and JDR checks that every province/PAO citation has an explicit scope note.
