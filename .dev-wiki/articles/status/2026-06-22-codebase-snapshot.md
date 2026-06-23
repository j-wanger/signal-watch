---
title: "Codebase snapshot — 2026-06-22 (Phase 70 debrief)"
aliases: []
category: status
tags: [snapshot, phase-70]
created: 2026-06-22
updated: 2026-06-22
source: debrief
---

# Codebase snapshot — 2026-06-22

Captured at the Phase 70 debrief (Gather extraction quality measured + the consolidated §12 substrate handoff). For full module/dependency maps see `_ARCHITECTURE.md`; this is a point-in-time metrics summary.

## Structure
- Ship templates (single-injection-point, offline): index.html · corpus.html · news.html · console.html · triage.html — built to **8 byte-frozen dist targets** (3 typologies + corpus + news + console + triage + launcher dist/index.html).
- Companion HTML (NOT ship/build targets): chain.html · workbench.html.
- `scripts/` 25 Python files (stdlib build + authoring + the news/corpus/chain/workbench companions; `osint_tools.py` + `evidence_requirements.py` the determination/gather control layer).
- `tests/` 7 `.test.mjs` arc suites + `tests/test_selftests.py` (pytest umbrella) + 2 Python quality-regression gates (`news_quality_harness.py`, `gather_quality_harness.py` NEW this phase).
- `docs/` 2 PLAN-BRIEF handoffs (`substrate-determination-signals-PLAN-BRIEF.md` consolidated/active; `substrate-bo-graph-emission-PLAN-BRIEF.md` → SUPERSEDED redirect stub) + program-blueprint.md (M9) + the live-mode + workbench docs.

## Test status (Phase 70 health-delta)
- `uv run pytest` umbrella **20 cases** (19→20, added `test_gather_quality_harness`).
- `node tests/workbench.test.mjs` **117** assertions (116→117).
- `tests/gather_quality_harness.py --check`: PASS — finding_coverage=1.0, target_closure=1.0, ML-A5 closes, replays with no model.
- `python3 scripts/build.py --check all` **8/8 ZERO dist drift**; build.py imports no casework/substrate/osint_tools (boundary clean).
- All `.mjs` arcs + serve_workbench/osint_tools/evidence_requirements/news_ground selftests green.

## Recent commits (pre-Phase-70 HEAD; the Phase-70 commit is the orchestrator's)
- fbd2291 Phase 69 — Evidence-sufficiency filing control
- 268f84b Phase 68 — re-vendor the FINTRAC-STR-rich casework + render the structured STR
- 1398e46 live workbench: openai backend defaults to 127.0.0.1:8080
- b95a379 live workbench: enable all backend options + a "server unavailable" banner
- 81544e7 Phase 67 follow-up — cross-platform live-workbench setup (Windows) + ship a wheel

## Cross-pillar pins (code-verified this phase)
- aml-substrate@b53855c (the consolidated determination-signals handoff brief pin).

## Related
- [[phases/phase-70-gather-quality-substrate-handoff|Phase 70]] · `_ARCHITECTURE.md` · [[2026-06-21-codebase-snapshot]] (prior)
