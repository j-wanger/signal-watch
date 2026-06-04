# Active Phase Context

Phase: 3 - Multi-typology (M2)
Objective: Add a second typology (Trade-based ML) as config only; build-time switch to per-typology dist/<id>/index.html; prove the engine is typology-agnostic (no engine edits).
Scope: config/typologies/*.json, scripts/build.py, dist/**
Key constraints:
- NO edits to index.html (the engine). Adding a typology = 1 JSON file. `git diff index.html` must be empty at phase close.
- TBML advisory text PARAPHRASED from public sources (FinCEN Apr-2025, FATF 2024) — no verbatim copyright. All figures illustrative; badge stays.
- Author strictly within the existing schema. If a generic field is genuinely missing, add it as OPTIONAL + backward-compatible (DISCOVERY) and rebuild fentanyl to prove no regression.
- Switch = build-time (dist/<id>/index.html). No runtime selector.
- build.py validates config against schema at the boundary and fails loud.
Exit criteria:
- config/typologies/trade-based.json authored + passes build-time validation
- TBML builds + renders all six acts, both gates, lift; self-contained
- fentanyl still builds byte-identical to baseline (regression); index.html untouched
Abort: if blocked >3 attempts on any task, run /dev adjust

Gates:
- [x] Direction confirmed by user (TBML + build-time switch, approved 2026-06-04)
- [x] Delivery accepted (2026-06-04 — TBML verified, engine untouched, fentanyl regression clean; debrief + commit)
