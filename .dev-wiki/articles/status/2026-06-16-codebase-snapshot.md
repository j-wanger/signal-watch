---
title: "Codebase snapshot 2026-06-16 (Phase 54 ready for completion — the C/D tag control made real, non-ship)"
aliases: []
category: status
tags: [snapshot, phase-54, measure-first, control, non-ship, c-d-tags, sr-11-7, krippendorff]
parents: [phase-54-cd-tag-control]
created: 2026-06-16
updated: 2026-06-16
source: debrief
---

# Codebase Snapshot — 2026-06-16

Taken at the Phase-54 debrief (T1–T5 [x], READY FOR COMPLETION; delivery accepted this session,
phase work UNCOMMITTED in the working tree — the orchestrator commits + flips the gate). The
measure-first workstream's CONTROL phase: the blueprint §4–§5 measured-not-gated control class made
concrete + executable for the C/D tag; NON-ship, ship corpus byte-frozen.

## File Metrics
- NEW this phase: scripts/cd_rate_independent.py 325 lines (dev-time companion — urllib → 127.0.0.1
  local model; the ONLY model/network code; never imported by build.py / cd_correctness.py) ·
  docs/cd-tag-control.md 179 (the SR-11-7 Pillar-2 + OSFI E-23 control, non-ship, Illustrative badge) ·
  data/cd-correctness/independent-sample.json (n=96 Qwen-context-matched rating; non-corpus) ·
  data/cd-correctness/cd-control-baseline.json (the committed control baseline; non-corpus)
- EXTENDED: scripts/cd_correctness.py 855 lines (Krippendorff-α [nominal] + join_raters/pairwise +
  the INDEPENDENT report stratum + the control harness --control-check/--control-freeze +
  evaluate_trip_wires) · docs/cd-correctness-report.md (Phase-54 section + "named follow-up delivered")
- scripts/build.py UNCHANGED — 0 references to cd_correctness / cd_rate_independent / cd-tag-control
  (grep-verified); the build boundary holds.
- ZERO ship artifacts in the diff: no *.html, no dist/, no data/*/derived/, no overlay touched.
- dist/ still SEVEN artifacts (3 typologies + corpus + news + console + triage); --check all 7/7 zero drift.

## Module Structure
- Unchanged core: 5 corpus sources + 3 overlays; grounding core derive_signals.py FROZEN; news pipeline
  scripts FROZEN; all 5 ship artifacts + dists BYTE-IDENTICAL.
- The C/D-correctness measurement family (scripts/cd_correctness.py + data/cd-correctness/* +
  docs/cd-correctness-report.md) now carries a CONTROL layer atop the Phase-51/52/53 instrument: a pure
  stdlib deterministic replay core (cd_correctness.py) + an isolated model-calling companion
  (cd_rate_independent.py) that produces the independent fixture once, then replays. Non-ship,
  read-only, outside every build.py-read path.

## Dependency Versions
- Python 3.14.4 (stdlib only for cd_correctness.py + cd_rate_independent.py — no new deps;
  cd_rate_independent.py uses urllib to reach the local 127.0.0.1 llama-cpp model)
- Node v22.22.2 (zero-dep DOM-shim test harnesses)
- Local model: Qwen3.6-35B on 127.0.0.1:8080 (dev/authoring-time only; the independent rater)

## Test Status
- python3 scripts/cd_correctness.py --selftest — GREEN (random/divergence/decomposition math +
  Phase-54: Krippendorff-α perfect/disagreement/mixed/degenerate/3-rater, join_raters + pairwise,
  control trip-wires clean-PASS / injected-drift-BREACH)
- python3 scripts/cd_rate_independent.py --selftest — GREEN (offline, stubbed model: context-matched
  prompt carries the source-doc region + posture + closed vocab + blind to committed; parse
  strict/fenced/think-wrapped; 96/96 source-doc regions resolve; no build.py import)
- python3 scripts/build.py --check all — 7/7 zero drift (ship corpus + all 5 dists byte-identical)
- The 6 existing suites unaffected (corpus-explorer, news-stream, gate-console, triage-console,
  news_quality_harness, derive_signals --selftest — no regressions; baseline diff captured at delivery)

## Recent Commits (last 5, pre-this-phase)
- 9ba9261 Phase 53 DELIVERED: C/D disagreement decomposed (the unguarded dimension, finished)
- 4f049ab Phase 52 report: tighten the finding (honesty correction)
- 4b2c29a Phase 52 DELIVERED: C/D-tag reliability measured (the unguarded dimension)
- 9045747 Phase 51 debrief: full-session capture (substream review + measure-first delivered)
- 65971a1 Phase 51 T2-T4 DELIVERED: corpus redundancy measured (the §13 fm-1 frontier)
