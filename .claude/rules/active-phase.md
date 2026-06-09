# Active Phase Context

Phase: 37 — Per-indicator typology (corpus Typologies lens). PLANNED → IN PROGRESS (0/5 tasks; direction approved 2026-06-08). Next: BEGIN T1 (the measure-first probe). Lite ceremony.

Objective: the corpus Typologies lens groups each DOC by ONE money-laundering typology (`data/typology-map.json`, 27-term vocab); that collapsed 7 of the 10 FINTRAC sector-guidance pages into a catch-all `fintrac-sector-baselines` (a sector page enumerates indicators across MANY typologies). Tag typology PER INDICATOR so a sector page distributes across the real typology clusters and the catch-all retires. Investigation (this session): all 10 derived pages RENDER (3 under casino-gaming/real-estate/VC; all 10 in the Documents lens); the FINTRAC SOURCE side is complete (11 pages, 10 derived, crown-agents skipped; STR + sanctions guidance enumerate nothing). The /intel/ special-bulletin frontier (OA001 + 3 SBs) was offered + DEFERRED.

Approach (the project's grain): MEASURE-FIRST → assign-per-unique-text → verify-as-AGREEMENT → human cluster adjudication → byte-surgical OVERLAY → regate.

Scope (UNFREEZE): `data/indicator-typology-map.json` (NEW overlay) · `scripts/build.py` (load/validate/resolve/inject) · `corpus.html` (the Typologies lens + synthesis) · `data/typology-map.json` (the 7 catch-all doc entries) · `dist/corpus/index.html` (rebuilt — new frozen baseline) · `tests/corpus-explorer.test.mjs` · `.dev-wiki/tmp/**` (probe + assignment) · `docs/**` · `tests/smoke-checklist.md` · CLAUDE.md (in-place `## Current state`) · this file.

Tasks: T1 (M) measure-first probe + model CHECKPOINT (no tagging) · T2 (L) assign per unique text + blind-agreement + cluster adjudication → resolved indicator-id→typology (Workflow candidate) · T3 (M) overlay + build.py validate/inherit/inject (records + core byte-frozen) · T4 (M) rewire the lens + synthesis to group by indicator typology; retire the catch-all · T5 (S) regate + rebuild dist/corpus + docs + in-place state/CLAUDE.md.

Key constraints (D1/D2):
- MEASURE-FIRST: no tagging before the T1 probe + the user's model checkpoint (single / multi-label / sector-general bucket). The T0 risk — cross-cutting indicators may relocate the catch-all to indicator level.
- OVERLAY, not record edits: typology in `data/indicator-typology-map.json`; ALL 56 derived records + `derive_signals.py` BYTE-FROZEN. Build-time: overlay value ELSE inherit the doc typology (the ~1,231 single-typology indicators inherit free; only ~1,020 sector-page indicators, ~589 unique, need neural assignment). Validated at the build boundary (closed vocab + referential integrity, fail-loud).
- Assign per UNIQUE text (Phase-34 method); verify as INTER-RATER AGREEMENT (consensus, NEVER "correct"); the user adjudicates ambiguous CLUSTERS. The rate is a journal/quality artifact, NOT a new demo number.
- HONESTY: combined coverage = honest union arithmetic over per-indicator statuses; NO lift/similarity/cross-regulator dedup; the always-on "Illustrative data & outputs" badge stays.

FROZEN byte-clean: the six-act showcase (`index.html` + `config/**` + 3 typology dists), the ENTIRE news stream (`news.html` + `dist/news` + `data/news/**` + `scripts/{serve_news,news_store,news_ground}.py`), ALL 56 derived records, the grounding core `derive_signals.py`, `data/capability-taxonomy.json`. `--check all` ZERO DRIFT on the 3 typology dists + dist/news (dist/corpus is the rebuilt new baseline). NO non-negotiable change.

Exit criteria: the Typologies lens groups by INDICATOR typology; the 7 FINTRAC sector pages distribute across real typology clusters; `fintrac-sector-baselines` retired; per-indicator typology in the overlay; 56 records + `derive_signals.py` byte-frozen; combined coverage union-honest (no lift/dedup; badge intact); `--check all` 5/5; node corpus + news harnesses + derive `--selftest` green; agreement reported as consensus; NO non-negotiable change.

Abort rule: if the T1 probe shows most indicators are genuinely cross-cutting → adopt the multi-label or honest indicator-level "sector-general" model the checkpoint surfaces; do NOT force one-typology. If the overlay can't keep the 56 records byte-frozen → STOP + re-confirm store-as-overlay vs Phase-34-style record edits. If T4 exceeds an M → STOP + split the synthesis sub-task. Blocked >3 attempts on a task → mark [blocked: …] + ask the user: skip or abort.

Gates:
- [x] Direction confirmed by user (per-indicator typology, measure-first overlay approach; approved 2026-06-08)
- [ ] Delivery accepted (post-implementation report)
