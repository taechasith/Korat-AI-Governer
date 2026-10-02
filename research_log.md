# Research log

## 2026-10-02: protocol and corpus freeze

- Read `Korat_AI_Mayor_Methodology_Guide.md` before producing decision records.
- Froze RQ1--RQ4, H1--H5, eight domains, three conditions, three charters, eight scenarios, JSON schema, top-k=8 TF-IDF cosine retrieval, and matched-cell analysis in `protocol/frozen_protocol.md`.
- Downloaded 11 public official-source snapshots. The manifest records jurisdiction, administrative level, access/license statement, URL, timestamp, and SHA-256. No unavailable numeric statistic was inferred.
- Applied a conservative evidence-card rule: cards state source availability, explicit planning content, and jurisdiction. Because compatible municipality-level numerical indicators were not established, numeric card values are null and numeric-fidelity is not reported.

## 2026-10-02: experiment decision

- No free isolated fresh-context model interface was exposed. Chose the guide's prescribed fallback: one frozen sequential attempt per 72 condition x scenario x charter cells, randomized with seed 20261002, no replicate claims, no later revision of records.
- The exposed model label was `Codex GPT-5`; detailed version, temperature, seed, and token limit were unavailable and were not invented.
- Decision records have no network access; C1/C2 use only retrieval results from the frozen cards. C0 receives no Korat evidence.

## 2026-10-02: analysis and document decision

- Generated metrics, bootstrap tables, figures, and manuscript numeric macros from code. Did not run inferential tests because sequential records are not independent samples.
- No TeX compiler or `acmart` installation exists in the environment. Preserved `paper/main.tex` in the requested ACM anonymous form and generated a visually checked, metadata-scrubbed fallback PDF from the same frozen manuscript content. This is explicitly marked as a fallback, not a successful LaTeX compilation.
