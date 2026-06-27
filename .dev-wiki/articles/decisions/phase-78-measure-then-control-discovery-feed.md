---
type: decision
slug: phase-78-measure-then-control-discovery-feed
title: "Pivot the measurement into a control — the §12 discovery feed over the disagreement cases"
phase: 78
status: accepted
confidence: high
source: plan
created: 2026-06-26
tags: [cross-pillar, measure-then-control, discovery-feed, workbench, lfcm, firewall]
---

# Decision — measure → control (the §12 discovery feed)

**Context.** The user's direction-gate pick: the deliverable is not a measurement alone but a control
built on it (the [[measuring-to-controlling-pivot]] — after several internal-consistency harnesses,
build the control the measurement was for).

**Decision.** The harness's confusion structure becomes a live **§12 discovery feed** in
`serve_workbench`: the two disagreement cells —
- *missed* = oracle-`file` the deterministic signals did NOT assemble to file-readiness (a signal/gather
  gap), and
- *over-flag* = signals file-ready on an oracle-`clear` (the defensive-filing exposure) —
surface as an analyst gather/build queue, each row annotated by the engine's own `missing[]`
gap-naming. A read-only `/discovery` route; companion-only; persists nothing.

**The firewall (intensified by the control).** The feed surfaces oracle-vs-engine divergence to the
ANALYST (presentation), but `determine`/`evaluate_sufficiency` read none of it — the Phase-74
priors-are-provenance-only precedent. `evidence_requirements.py` stays BYTE-UNCHANGED (the A1 guard).

**Gated on the measurement.** If T2's matrix is degenerate (signals don't discriminate the oracle
classes), the feed is down-scoped to an honest-degeneracy report — the control is only built over a
real result.

**Boundary.** No ship dist touched (the workbench is companion-only, port 8030); build.py imports
nothing new.

Related: [[decisions/phase-78-bundle-only-non-circular-validation]].
