---
title: "Phase 82 — north-star evidence AT SCALE: consume P39 predicate + P40 mitigation so the GENERATED slice carries north-star-quality determinations"
aliases: [phase-82-northstar-evidence-at-scale-frame, phase-82-scale-frame]
category: decisions
tags: [cross-pillar, consume, substrate, predicate-reference, mitigation-evidence, determination, north-star, scale, a1-guard]
parents: [phase-82-consume-sibling-northstar-evidence-at-scale]
created: 2026-06-29
updated: 2026-06-29
source: plan
confidence: medium
---

## Context

The same workbench engine that decides the 2 hand-authored north-star cases (Northgate FILES /
Lakeshore CLEARS, Phase 73) cannot yet decide the GENERATED 376-case slice end-to-end: the slice
lacks the decision-layer evidence the bar requires. Every slice case stalls at `needs_more_info`
because there is no grounded *named predicate risk* (a measured **0-of-376** gap) and no affirmative
*mitigation* path — the engine had the params but the data never carried the values. Substrate just
shipped exactly those two field families: P39 (`1483c84`, predicate-reference layer — Ask #1 of
signal-watch's own `substrate-northstar-evidence-emission-PLAN-BRIEF.md`, the keystone) and P40
(`978c8fe`, affirmative-mitigation evidence — Ask #2, the clear-side mirror). The decisive fact:
`scripts/evidence_requirements.py` ALREADY exposes the `named_predicate_risk` + `mitigation_established`
params (line 310-312), so consuming P39/P40 is pure bundle DATA the FROZEN engine reads — NOT a rule edit.

## Decision

Consume P39 predicate-reference + P40 mitigation-evidence so the GENERATED slice carries
north-star-quality determinations AT SCALE — predicate → reach the FILE bar; mitigation → affirmatively
CLEAR — while the sufficiency RULE stays byte-frozen (the A1 guard holds by construction: the consume
work lives in the curate/serve layer, the engine derives legs from capabilities and never sees
provenance). The advance is proven by a rigorous with/without-`determine()` regression, never asserted
from coverage.

Alternatives rejected: (a) **per-emission incoherent separate consumes** — treating P39/P40 as two
unrelated additions misses that together they make the GENERATED slice decide like the hand-authored
pair; the unifying frame is "north-star at scale", not "two more atoms". (b) **Re-attempting the C17
exposure leg** (Phase 81) — that leg was degenerate (label-blind, corr≈0, DELTA=0 to the bar); P39/P40
are *required-and-currently-missing* rule components (the engine already demands them), so the cohort
that already carries mechanism+2legs should move — but the count is MEASURED with the rigorous engine,
not assumed.

## Consequences

- The §12 loop closes from the GENERATED slice, not just the 2 authored cases — the demo scales.
- A1 guard (`evidence_requirements.py` byte-unchanged) holds by construction; any consume that would
  force an engine edit (e.g. a same-predicate dedup the engine can't express) STOPS-and-surfaces.
- The advance is conditional on a non-degenerate measured delta (T2b/c); degenerate → the consume
  degrades to a rendered observable + a brief (the Phase-81 honest-reshape pattern), not a false claim.
- Honesty governor: the magnitudes ship as honest COUNTS with definitions — no catch-rate / lift /
  precision / recall, swept across DOCS too (the Phase-78 lesson).
