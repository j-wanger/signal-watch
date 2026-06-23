---
title: "Codebase snapshot — 2026-06-23 (Phase 71 debrief)"
aliases: []
category: status
tags: [snapshot, phase-71]
created: 2026-06-23
updated: 2026-06-23
source: debrief
---

# Codebase snapshot — 2026-06-23

Captured at the Phase 71 debrief (Adopt the substrate v0.3 slice; close the §12 determination loop in the workbench). For full module/dependency maps see `_ARCHITECTURE.md`; this is a point-in-time metrics summary.

## Structure
- Ship templates (single-injection-point, offline): index.html · corpus.html · news.html · console.html · triage.html — built to **8 byte-frozen dist targets** (3 typologies + corpus + news + console + triage + launcher dist/index.html).
- Companion HTML (NOT ship/build targets): chain.html · workbench.html (now renders the bundle's real `related_parties[]` BO network via `boGraphHTML`).
- `scripts/` 25 Python files (stdlib build + authoring + the news/corpus/chain/workbench companions; `osint_tools.py` + `evidence_requirements.py` the determination/gather control layer; `curate_workbench_cases.py` now does a per-customer MERGE).
- `data/workbench/` slice **342 bundles** (was 294) — re-vendored+merged v0.3 population; coverage 107/342, gate funnel 181/79/82.
- `vendor/aml-casework/` pinned **157554b** (accepts contract v0.3 + carries `fin-2025-a003`); subprocess file-handoff boundary — build.py never imports it.
- `tests/` 7 `.test.mjs` arc suites + `tests/test_selftests.py` (pytest umbrella) + 2 Python quality-regression gates (`news_quality_harness.py`, `gather_quality_harness.py`).
- `docs/` 2 PLAN-BRIEF handoffs (`substrate-determination-signals-PLAN-BRIEF.md` consolidated/active; `substrate-bo-graph-emission-PLAN-BRIEF.md` → SUPERSEDED redirect stub) + program-blueprint.md (M9) + the live-mode + workbench docs.

## Test status (Phase 71 health-delta)
- `uv run pytest` umbrella **20 cases** (unchanged count — extended existing entries).
- `node tests/workbench.test.mjs` **124** assertions (117→124, +7 BO-graph render tests).
- `tests/gather_quality_harness.py --check`: PASS (no model). curate/serve/evidence_requirements selftests extended + green.
- **§12 closure: 0→81 cases** reach the ≥2-leg ML determination bar from REAL signals (per-customer MERGE; C8 ML-A3 + C15/related_parties ML-A4).
- `python3 scripts/build.py --check all` **8/8 ZERO dist drift**; build.py imports no casework/substrate/osint_tools (boundary clean).
- All `.mjs` arcs (news/gate/triage/corpus) green; casework sibling 289 tests green.

## Recent commits (pre-Phase-71 HEAD; the Phase-71 commit is the orchestrator's)
- 9a7637a Phase 70 — Gather extraction quality (measured) + the consolidated §12 substrate handoff
- fbd2291 Phase 69 — Evidence-sufficiency filing control
- 268f84b Phase 68 — re-vendor the FINTRAC-STR-rich casework + render the structured STR
- 1398e46 live workbench: openai backend defaults to 127.0.0.1:8080
- b95a379 live workbench: enable all backend options + a "server unavailable" banner

## Cross-pillar pins (code-verified this phase)
- aml-substrate@443e4a6 (v0.3 — `CONTRACT_VERSION="0.3"`, `related_parties[]` emitted).
- aml-casework@157554b (vendored — `KNOWN_CONTRACT_VERSIONS` includes "0.3" + the `fin-2025-a003` corpus file).

## Related
- [[phases/phase-71-substrate-v03-slice-determination-loop|Phase 71]] · `_ARCHITECTURE.md` · [[2026-06-22-codebase-snapshot]] (prior)
