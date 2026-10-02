# Reproducibility

## Scope

This bundle is a public-data-only, all-digital audit. It freezes the corpus before trials. It does not reproduce a real budget, citizen preferences, or a deployment.

## Requirements

Python 3.10+ with `requests`, `pandas`, `numpy`, `scikit-learn`, `scipy`, `matplotlib`, and `seaborn`. Install the listed packages in an isolated environment if absent.

## Rebuild

1. Run `python scripts/pipeline.py` from the repository root. This downloads the listed public URLs, overwrites derived artifacts, freezes their then-current raw snapshots, builds cards/retrieval logs, regenerates the 72 sequential records, analysis tables, and figures.
2. Inspect `data/data_manifest.csv`; every raw-file hash is listed there. A failed download is retained as a plainly labelled failure snapshot rather than substituted with data.
3. Compile `paper/main.tex` with a TeX installation containing `acmart`. The checked-in `paper/paper_review.pdf` was compiled with Tectonic 0.17.0 using the requested `acmart` review class.

## Key files

- `protocol/frozen_protocol.md`: fixed design and exposed execution limitation.
- `protocol/scenario_deck.json`, `protocol/charters.json`, and `protocol/prompts/`: frozen experimental inputs.
- `retrieval/retrieval_log.jsonl`: query, rank, score, evidence ID, source ID.
- `experiment/runs/`: immutable-style raw and parsed JSON for each attempted cell.
- `experiment/validation/`: validation records.
- `analysis/analyze.py`: analysis entrypoint shim; `scripts/pipeline.py` is the full executable pipeline.
- `analysis/tables/results_macros.tex`: programmatically generated manuscript numerals.

Do not treat the cells as independent replicates. The model identity exposed by the session is limited to `Codex GPT-5`; seed, temperature, and detailed version are unavailable.
