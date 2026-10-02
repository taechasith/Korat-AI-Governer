# What If Korat Had an AI Mayor?

> A reproducible public-data audit of how an AI agent changes fictional municipal allocations when its evidence, uncertainty, and values are made visible.

This project asks an uncomfortable question with care: what changes when an AI must show its evidence before it makes a fictional city-allocation decision? It is a research probe, not a proposal to automate government.

The case study is Nakhon Ratchasima (Korat), Thailand. A frozen official-source corpus, transparent local retrieval (RAG-Mock), and a constrained 100-token sandbox make traceability, uncertainty, jurisdiction discipline, and value-charter sensitivity inspectable.

## What this is not

- A real municipal budget or Thai-baht recommendation.
- An evaluation or endorsement of any politician.
- A simulation of residents or public preferences.
- A human-subject study or evidence that AI should replace governance.

## Why this exists

Public data can make an AI response look authoritative even where it is incomplete, stale, or collected at the wrong administrative scale. This repository exposes the complete chain: sources, permitted evidence, model records, validations, and analysis. Retrieval can improve provenance without making a policy choice objectively correct; the same evidence can still support different allocations under legitimate, explicit value charters.

## Repository map

| Path | Purpose |
| --- | --- |
| `protocol/` | Frozen design, charters, scenarios, and prompts. |
| `data/` | Public-source manifest, hashes, processed material, and evidence cards. |
| `retrieval/` | Deterministic TF-IDF RAG-Mock logs. |
| `experiment/` | Run manifest, raw outputs, parsed outputs, and validations. |
| `analysis/` | Reproducible code, tables, and figures. |
| `paper/` | Anonymous ACM-style source, figures, bibliography, and review PDF. |
| `reproducibility/` | Environment, limitations, and rebuild instructions. |

Raw public-source snapshots remain local in `data/raw/` because redistribution rights are not always clear. The public manifest preserves URLs, timestamps, SHA-256 hashes, scope, and access/license statements.

## Quick start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python scripts/pipeline.py
```

This rebuilds source snapshots, manifest, evidence cards, local RAG-Mock logs, sequential audit records, analysis tables, and figures. Read [REPRODUCIBILITY.md](reproducibility/REPRODUCIBILITY.md) before interpreting or republishing results.

Compile the paper from `paper/` with [Tectonic](https://tectonic-typesetting.github.io/) or another TeX engine supporting `acmart`:

```powershell
tectonic -X compile main.tex --outdir .
```

`paper/paper_review.pdf` is the checked, anonymous four-page ACM-style review artifact.

## Responsible reuse

1. Freeze protocol and corpus before inspecting outputs.
2. Preserve jurisdiction and administrative level on every evidence item.
3. Treat missing data as missing, never as zero need.
4. Never call province or PAO context municipal evidence.
5. Never equate grounding or numerical compliance with policy correctness.
6. Never present sequential agent records as independent model samples.

## Contributing

Contributions improving provenance, deterministic analysis, accessibility, documentation, or critical scrutiny are welcome. Please discuss changes to the frozen protocol or evidence-card schema before opening a pull request. Preserve output/validation history and never add private or sensitive data.

Be kind, precise, and generous in review. The people represented by public data deserve more than a confident-looking answer.

## License

Code and original documentation are available under the [MIT License](LICENSE). Government-source material remains subject to the terms recorded in `data/data_manifest.csv`; it is not relicensed here.

## Citation

When building on this audit, cite `paper/main.tex` and identify the exact commit, frozen protocol, manifest, and result artifacts used.
