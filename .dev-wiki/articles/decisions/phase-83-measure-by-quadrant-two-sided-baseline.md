---
title: "Phase 83: report agreement BY QUADRANT against a two-sided stub baseline (not a single aggregate)"
aliases: [phase-83-by-quadrant, two-sided-baseline, agent-ties-the-spine]
category: decisions
tags: [agentification, merge, measurement, baseline, honesty, quadrant]
parents: [phase-83-merge-adjudicator-oracle-scored]
created: 2026-06-29
updated: 2026-06-29
source: implementation
confidence: high
---

## Context

The pre-adjudication evidence SHOWS `spine_verdict`, so a lazy agent can echo it and score exactly what
the deterministic StubAdjudicator (echo `spine_verdict` → uphold/reject) scores. The StubAdjudicator
baseline is TWO-SIDED over the 66 committed scored cases: right on 33, wrong on 33 (30
fragmentation-gap where same-person fragments share an email but the demoted spine kept them distinct +
3 over-merge-trap). The question: how to report the agent's agreement so the measurement is honest and
informative even when the agent ties the spine?

## Decision

Report agreement broken out **BY QUADRANT + provenance** (the four `resolution_scorer` klasses:
real-co-reference / over-merge-trap / fragmentation-gap / correct-rejection) against the two-sided stub
baseline (right 33/66, wrong 33). The headline is WHERE the agent does (or does not) beat the spine —
specifically on the 33 cases the spine gets WRONG. "The agent ties the spine" is itself an HONEST
result, not a failure; the MEASUREMENT is the deliverable.

Rejected: a single aggregate agreement number — it hides where the spine errs (the fragmentation-gap +
over-merge-trap quadrants), which is the entire reason the merge gate exists; an aggregate that "looks
good" because it inherits the stub's 33 correct-by-echo would mislead.

## Consequences

- The harness emits a per-quadrant + per-provenance count table (stub baseline + agent), deferrals
  separate, every number synthetic-substrate-qualified.
- The credible claim is "the agent matched the oracle on N of the 33 cases the spine got wrong" — a
  measured, two-sided, counts-only statement (never a rate/lift/precision).
- The stub baseline is the always-available deterministic reference (no model needed) — it ships as the
  measured result even if the live agent capture is a named follow-on.
- **OUTCOME (implemented 2026-06-29):** the by-quadrant breakout did its job — the agent did NOT tie
  the spine; it BEAT it on exactly the two ambiguous quadrants (18 of 30 fragmentation-gaps + all 3
  over-merge-traps = 21 of the 33 the spine got wrong), for 54/66 vs the stub's 33. The honest credible
  statement landed as a measured, two-sided, counts-only claim. Small-N caveat surfaced (over-merge-trap
  =3, real-co-reference=3 — a richer slice would strengthen those cells). Confidence → high.
