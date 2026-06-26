---
title: "Codebase snapshot — 2026-06-25 (Phase 75 close)"
category: status
created: 2026-06-25
updated: 2026-06-25
source: debrief
---

# Codebase Snapshot — 2026-06-25 (Phase 75 close)

## Phase
Phase 75 (Consume the substrate v0.5 entity-resolution emission) DELIVERED + accepted, STANDARD ceremony. No active signal-watch-local phase.

## Module structure (durable detail in `_ARCHITECTURE.md`)
- **5 ship artifacts** (each a single self-contained offline file): `index.html`→dist/<id> (six-act showcase) · `corpus.html`→dist/corpus · `news.html`→dist/news · `console.html`→dist/console · `triage.html`→dist/triage. Plus the launcher `dist/index.html` (8 dists under `--check all`).
- **Companion-only (NOT ship/build targets; build.py imports none):** the investigator workbench (`workbench.html` + `scripts/{serve_workbench,curate_workbench_cases,evidence_requirements,osint_tools}.py`) · the chain workbench (`chain.html` + `serve_chain.py`) · the LIVE news/corpus companions · the entity intelligence spine (`scripts/{entity_spine,resolution_scorer,measure_xcase_overlap}.py`).
- `scripts/` = 28 Python files (authoring pipeline + companions, dep-free except DuckDB selftests under `.venv`). `docs/` = 7 PLAN-BRIEFs + the program blueprint + the 4 Phase-74 standards + workbench/case docs.

## This phase's deltas (Phase 75)
- NEW `scripts/measure_xcase_overlap.py` (the measure-first cross-case-overlap gate).
- `entity_spine.py`: `entity_ref` added to `STRONG_KINDS` + `entities_in_multiple_records` (stable sort).
- `serve_workbench.py`: `_observe_substrate_party` + `substrate_memory` + a `/memory` route.
- `curate_workbench_cases.py`: SUBSTRATE_HEAD f15c241→fc98b09 (v0.5 additive; `validate_v05_bundle` on the boundary; co-reference selection pass; casework v0.3-view; venv-path fix).
- `workbench.html`: the "Persistent entity intelligence" `/memory` panel.
- `data/workbench/**` re-curated to the v0.5 slice (376 cases; coverage 128/376; funnel 202/111/63).

## Test status (all green at close)
- `python3 scripts/build.py --check all` → 8/8 dists byte-identical (companion-only held).
- `node tests/workbench.test.mjs` 159 · `node tests/news-stream.test.mjs` 150 · gate-console 68 · triage-console 93 · corpus OK.
- `python3 tests/news_live_test.py` PASS · `gather_quality_harness --check` PASS · `uv run pytest` 22.
- `evidence_requirements.py` + `news_store.py` BYTE-UNCHANGED (the A1 file-bar + M8 firewalls held).
- build.py imports neither the spine, the scorer, nor substrate (the companion-only grep guard clean).

## Recent commits
- 727a8ba docs: make the 3 sibling handoff briefs dev-plan-ready (Phase 74 follow-on)
- 18784ac chore(dev-wiki): close Phase 74 — delivery gate accepted (e18eba9)
- e18eba9 Phase 74: persistent entity intelligence spine — consumer slice, standards, sibling briefs
- ef4bf83 docs: rich-case target contract — the substrate/casework handoff (Phase 73 follow-on)
- ebc2c20 chore(dev-wiki): close Phase 73 — delivery gate accepted (f804722)

(Phase 75's delivery commit is the orchestrator's next step; this snapshot precedes it.)
