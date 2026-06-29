---
title: "Phase 82 — measure-first via four rigorous non-ship deltas, each with an honest fallback"
aliases: [phase-82-measure-first-four-deltas, phase-82-four-deltas]
category: decisions
tags: [cross-pillar, consume, measure-first, rigorous-engine, determination, merge-oracle, casework-funnel, honesty]
parents: [phase-82-consume-sibling-northstar-evidence-at-scale]
created: 2026-06-29
updated: 2026-06-29
source: plan
confidence: medium
---

## Context

Phase 81 taught the load-bearing lesson the hard way: a measure-first gate MUST run the rigorous
engine, never a coverage proxy. The C17 planning estimate ("9 of 13 reach file-ready") counted ≥2
related parties as a leg without a mechanism check — a loose proxy — and the rigorous `determine()`
with/without re-measure showed the real DELTA was 0. Phase 82 has four gated builds (merge-org class,
§12 predicate, §12 mitigation, casework funnel), each with a substrate self-report that may not
replay through signal-watch's own path (substrate's 16-uphold/35-reject merge claim; substrate's 40%
predicate / 6% mitigation coverage). Replaying a substrate self-report as our result is the Phase-77/81
trap.

## Decision

Every gated build runs a RIGOROUS non-ship measure FIRST, on signal-watch's own path, and each has an
honest fallback:

- **T2a merge two-sidedness** — distill the org slice + score uphold/reject through
  `resolution_scorer`/`curate_merge_cases` on OUR path (not substrate's self-report). One-sided → ABORT
  the org track, `dist/merge` BYTE-FROZEN, route to a brief.
- **T2b §12 predicate delta** — `determine()` WITH/WITHOUT the predicate over the slice; count cases
  moved to FILE. DELTA≈0 → observable + brief.
- **T2c §12 mitigation delta** — `determine()` WITH/WITHOUT mitigation; count cases moved to CLEAR.
  DELTA≈0 → observable + brief.
- **T2d casework funnel delta** — re-vendor in scratch, re-measure the signing funnel; moves must be
  fail-close→sign, not sign→fail-close.

Rejected: trusting substrate's self-reported magnitudes (the Phase-77/81 trap — a self-report is not a
measurement on our path); a coverage proxy (the explicit Phase-81 error).

## Consequences

- The four deltas are recorded as non-ship numbers in the journal; each gate decision (build / degrade
  / abort) is documented before any ship-dist touch.
- `git diff --quiet scripts/evidence_requirements.py` — the measure READS the engine, never edits it.
- Any track can degrade to observable/brief without forcing the others (the tracks are independently
  gated — decision `phase-82-full-batch-four-tracks`).
- The honesty governor sweep covers the recorded deltas: counts with definitions, no rate/lift/precision/recall.
