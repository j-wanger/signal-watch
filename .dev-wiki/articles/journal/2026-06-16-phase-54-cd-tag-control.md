---
title: "Phase 54 — C/D tag control: the measured-not-gated control made real (lite, planned+delivered+accepted same session)"
aliases: []
category: journal
tags: [measure-first, corpus, honesty, c-d-tags, non-ship, control, sr-11-7, ongoing-monitoring, independent-rater, krippendorff, consensus, cross-family]
parents: [phase-54-cd-tag-control]
created: 2026-06-16
updated: 2026-06-16
source: debrief
duration: ~half-day (post-compaction estimate — may undercount)
---

# Phase 54 — C/D tag control: the measured-not-gated control made real

## What Happened
- The measure-first workstream PIVOTED from a 4th C/D point-measurement to the **control** the three
  measurements (51/52/53) were FOR. Direction = the user's REFRAME at the dev-plan gate ("prototype the
  tag control" over the context-matched-rater close-out OR the heading→capability determinism probe) +
  a rigor ESCALATION ("execute the independent effectiveness challenge ONCE this phase" over scheduling
  it — a control whose key activity has never run is also prose). Built the blueprint §4–§5
  **measured-not-gated control class** CONCRETE + EXECUTABLE for the C/D tag, closing the named-OPEN
  Phase-47 T2/T3 control-story blocker.
- **The independent effectiveness challenge, EXECUTED** (the Phase-52/53 deferred follow-up). A NEW
  dev-time companion `scripts/cd_rate_independent.py` called a LOCAL, genuinely **cross-family** rater
  (Qwen3.6-35B on 127.0.0.1:8080), **context-matched** (the source-doc region for the gid + the 28+20
  interview posture + the closed C/D vocab — NOT the Phase-53 flag-only frame), over the SAME committed
  n=96 enlarged-random sample → `independent-sample.json`. Probe-gated (Phase-46 pattern): the T1 8-item
  `--probe` was user-adjudicated COMPETENT (8/8 in-vocab, sane picks, hit the named C8/C14 neighbour,
  flagged a plausible committed mis-tag) → ran the full n=96 AS-IS; the named Opus-context-matched
  fallback was not needed (A0 held with a positive surprise).
- **MEASURED:** Qwen-context-matched vs committed → **C 0.604** (58/96, κ 0.583) / **D 0.646** (62/96,
  κ 0.599); cross-rater (Opus-blind-flag-only vs Qwen-cm) C 0.677 / D 0.646; **Krippendorff's α** over
  {committed, Opus-blind, Qwen-cm} **C 0.634 / D 0.618**. The context-matched cross-family agreement is
  *statistically indistinguishable* from the same-family self-consistency (0.677; Wilson CIs overlap) →
  the unguarded dimension's reliability is GENUINE (survives a family change, chance-corrected, ~0.6/axis,
  never validated-correct), and **context-matching resolves the Phase-53 confound** (the flag-only
  comparison overstated apparent disagreement).
- **The CONTROL, made real.** `docs/cd-tag-control.md` — the SR-11-7 Pillar-2 + OSFI E-23 grounded
  measured-not-gated control (scope · risk-tier [BUILD_NOW codes tighter] · the Phase 51-54 baseline ·
  quarterly cadence · 3 trip-wire classes · the independent challenge · three-lines-of-defense ownership ·
  re-baseline trail · the audit walk). Executable: `cd_correctness.py --control-check` (PASS 7/7 on the
  frozen corpus) / `--control-freeze` (`cd-control-baseline.json`); BREACH demonstrated on injected drift
  (selftest + a live perturb-and-restore, baseline byte-restored).

## Decisions Made
- [[phase-54-cd-tag-control|Phase 54 DIRECTION]] — the user's REFRAME ("prototype the tag control") +
  rigor escalation ("execute the independent challenge once"); all_accept:true (A0 local-model
  availability+competence [T0 weakest, probe-gated + named Opus fallback] · A1 context-matched =
  committed-inputs · A2 replay-core-pure / model-isolated · A3 non-ship + no-blueprint-edit). [Decision
  article + ledger Phase-54 block already exist — no duplicate created.]
- T1 checkpoint adjudication (user): the local Qwen probe was COMPETENT → proceed to the full n=96 run
  AS-IS, over tightening the context window / adding an Opus-context-matched arm; the named fallback was
  not needed.

## Problems Solved
- The model dependency vs the deterministic replay core — isolated `cd_rate_independent.py` (the ONLY
  model/network code) as a dev-time companion; `build.py` and `cd_correctness.py` import NEITHER, so the
  measurement replays from committed fixtures forever (A2 held; --check all proves the boundary).
- The Phase-53 confound (flag-only re-rate vs full-doc committed) — context-matching the cross-family
  rater pulled agreement up to same-family levels, bounding the confound's DIRECTION. (Caveat: this is an
  INFERENCE from the aggregate ~0.6 ≈ self-consistency, NOT a re-run of the forced-pairwise decomposition
  with the Qwen rater — it bounds the direction, not the exact share.)

## Open Questions
- A human (domain-expert) independent rater — the gold standard beyond cross-family model consensus; the
  control SCHEDULES it, this phase executed the model leg only.

## Artifacts Changed
- `scripts/cd_rate_independent.py` (NEW — dev-time companion; urllib → 127.0.0.1 local model; the ONLY
  model/network code in the workstream; never imported by build.py / cd_correctness.py's replay path)
- `scripts/cd_correctness.py` (EXTENDED — Krippendorff's α [nominal], join_raters + pairwise_agreement,
  the INDEPENDENT report stratum, the CONTROL harness `--control-check`/`--control-freeze` +
  evaluate_trip_wires over `cd-control-baseline.json`; --selftest extended)
- `docs/cd-tag-control.md` (NEW — the blueprint §4–§5 measured-not-gated control for the C/D tag;
  non-ship, SR-11-7 Pillar-2 + OSFI E-23 grounded, always-on Illustrative badge)
- `data/cd-correctness/{independent-sample.json, cd-control-baseline.json}` (NEW — non-corpus; build.py
  never reads them)
- `docs/cd-correctness-report.md` (EXTENDED — the Phase-54 section + the "named follow-up delivered" line)
- `.dev-wiki/*`, `HANDOFF.md` §8 (lifecycle). No CLAUDE.md edit (non-ship, matches 51-53; trim debt carried).

## Related
- [[phase-54-cd-tag-control|Phase 54 — C/D tag control]] — parent phase
- [[2026-06-16-phase-53-cd-disagreement-decomposition|Phase 53 — C/D disagreement decomposition]] — the
  prior measurement (this phase executed its named-deferred context-matched independent rater)

## Soft Observations / Phase N+1 Candidates
- The independent cross-family agreement (C 0.604 / D 0.646) is statistically indistinguishable from the
  same-family self-consistency (0.677; Wilson CIs overlap) — a mild surprise (cross-family was expected to
  agree notably LESS). Reading: context-matching pulls a cross-family rater UP to same-family levels, i.e.
  the committed C/D codes are reproducible across model families when document context is held constant. |
  Phase N+1: a human-rater panel would test whether this holds against a NON-model rater. | Evidence:
  cd_correctness.py --report INDEPENDENT stratum; docs/cd-correctness-report.md Phase-54 section.
- "Context-matching resolves the Phase-53 confound" is an INFERENCE from the aggregate agreement (~0.6 ≈
  self-consistency), NOT a re-run of the forced-pairwise decomposition with the Qwen rater — it bounds the
  confound's DIRECTION, not its exact share. | Phase N+1: a Qwen forced-pairwise decomposition over the
  n=96 mismatches converts the bound to a measured share. | Evidence: docs/cd-tag-control.md "what this
  stratum does not do"; docs/cd-correctness-report.md Phase-54 section.
- The control is the FIRST concrete instance of the blueprint's measured-not-gated control class; the
  reusable PROGRAM-WIDE control pattern (other judgmental dims, e.g. the news red_flag translation) was the
  gate's not-chosen broader option and is the natural next control phase. | Phase N+1: extend the control
  to the whole measured-not-gated class, C/D as the proven instance. | Evidence: docs/cd-tag-control.md;
  the Phase-54 ledger A1.
- The deterministic section-heading→capability residual (the Phase-37 thread) — the deterministic
  alternative to a neural tag on the subset where a section heading constrains C — stays deferred (a new
  dimension, not this phase).
- (process) Institutional-knowledge memory "measuring → controlling pivot" was ALREADY captured to
  auto-memory this session (after 2-3 honest numbers in a measure-first vein, Jake pivots to building the
  control + wants the prototype's key activity executed once). No further memory harvest needed for that.
