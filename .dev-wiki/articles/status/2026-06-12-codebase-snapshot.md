---
title: "Codebase snapshot 2026-06-12 (Phase 47 ready for completion — pre-delivery, first design phase)"
aliases: []
category: status
tags: [snapshot, phase-47, design, gate-console, blueprint]
parents: [phase-47-agentic-aml-program-design]
created: 2026-06-12
updated: 2026-06-12
source: debrief
---

# Codebase Snapshot — 2026-06-12

Taken at the Phase-47 debrief (7/7 [x], READY FOR COMPLETION; delivery gate pending; phase work
UNCOMMITTED in the working tree). First design phase: blueprint + 4th ship artifact + E-23 wiki gap.

## File Metrics
- NEW this phase: docs/program-blueprint.md 276 lines (M9 design deliverable, §1–§12) ·
  console.html 571 (4th ship template) · dist/console/index.html 305,180 bytes ·
  data/console/cases.json 5,328 lines (213 cases) · scripts/curate_console_cases.py 150
  (deterministic regeneration-only) · tests/gate-console.test.mjs 372 (68 assertions) ·
  wiki/articles/concepts/osfi-e-23-model-risk-management.md (aml-wiki, primary-source) ·
  specs/phase-47-agentic-aml-program-design.md
- scripts/build.py 1,236 lines (was 1,042 — console target + load/validate_console_cases, additive)
- CLAUDE.md 286 lines (vs ~200 target — trim residual carried, heavier; 263 pre-phase)
- dist/ now SIX artifacts: 3 typologies + corpus + news + console (all in --check all)

## Module Structure
- Unchanged core: 5 corpus sources + 3 overlays; grounding core derive_signals.py FROZEN;
  news pipeline scripts FROZEN; existing 3 ship artifacts + dists BYTE-IDENTICAL (reviewer-verified).
- New committed data domain: data/console/ (validated at the build boundary; FINTRAC attribution
  metadata on 212/213 rows; adjudicated codes re-verified 213/213 at build).

## Test Status (all green at debrief)
- node: corpus-explorer 303 · news-stream 150 · gate-console 68 (NEW)
- python: derive_signals/serve_corpus/serve_news/news_ground/news_fetch --selftest ·
  news_quality_harness --check (17 within baseline) · news_live_test · news_store (.venv)
- build.py --check all 6/6 zero drift

## Dependencies
- Unchanged: ship zero-dep; markitdown + duckdb confined to the gitignored uv .venv.

## Recent Commits (pre-phase; Phase-47 work uncommitted)
- d4cbfd1 Booth loop layout fix · 4cf6cbb Phase 46 gate flip · 5981b41 Phase 46 corpus live
  derivation · 5da6ec5 Booth draw-in loop · 7e9fa23 Phase 45 gate flip
