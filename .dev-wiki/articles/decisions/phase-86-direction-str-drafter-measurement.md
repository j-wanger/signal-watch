---
title: "Phase 86 — Direction = Stage 3 STR drafter, but the deliverable is the MEASUREMENT FRAME (the infra shipped Phase 57, there is no correctness oracle)"
aliases: [phase-86-direction, str-drafter-measurement-frame, agentification-stage-3-direction]
category: decisions
tags: [agentification, stage-3, str-drafter, measurement, consistency-not-correctness, planning]
parents: [phase-86-str-drafter-consistency-measure]
created: 2026-06-29
updated: 2026-06-29
source: plan
confidence: medium
---

## Context

Phase 86 is the agentification roadmap's Stage 3 — the STR drafter. The state-loader surfaced a
finding that reshaped the frame BEFORE the gate: the STR drafter and its verifier gate ALREADY
SHIPPED in Phase 57 — the Drafter Protocol (casework's pluggable `Drafter` boundary,
`vendor/aml-casework/src/aml_casework/narrative_generator.py`), the
`--drafter {stub,claude,openai,opencode}` switch with all four backend adapters, the backend mapping
in `serve_chain.py:188`, and the live-draft staged reveal in chain.html/workbench.html. A live model
is up on `127.0.0.1:8080`. So Stage 3 is NOT new infrastructure — the roadmap's "near-zero new code"
is literally true. The drafter also has NO correctness oracle (free-text drafting). The open question
at the gate: with the agent + gate built, what does Phase 86 actually ADD?

## Decision

Direction = Stage 3 STR drafter, with the deliverable being the **MEASUREMENT FRAME** — a drafter
quality harness (`tests/drafter_quality_harness.py`, the `gather_quality_harness.py` pattern) + an
honest counts-only headline + marking roadmap Stage 3 BUILT — NOT new infrastructure. Because there
is no narrative correctness oracle, this lands in the roadmap's own **consistency-not-correctness**
class (the GATHER model: stub-vs-live + the verifier as the measurable gate), NOT a Stage-1/2
oracle-scored headline. Roadmap-sequenced after Stage 2 (now satisfied, Phase 85).

Chosen over the alternatives surfaced at the gate:
- a DECISION-TABLE render of the Phase-85 §12 agent's per-cap-signature policy — narrower (one
  agent's artifact, no new agent);
- a DEFER/ANCHORING ablation on the Stage-2 agent — analysis-only, no new loop;
- a BASE-RATE-AWARE proposer tool — overfit hazard (no held-out calibration set exists; see
  [[phase-85-base-rate-remeasure-not-overfit]]).

## Consequences

The phase is deliberately thin: a harness + one execute-once measurement + a docs/roadmap true-up,
companion-only. The headline is honest but NOT an accuracy — it is consistency (stub-vs-live
sign/refuse) + a fabrication-guard catch count + grounding consistency. This makes the drafter the
SECOND consistency-not-correctness harness in the program (GATHER is the first), and keeps the
roadmap's cross-cutting evaluation discipline intact (oracle-scored where truth exists, consistency
where it does not). The genuine risk carried to impl is degeneracy — if the population proves
one-sided, an honest NULL is surfaced (the narrative-seam case is the named contrast; see
[[phase-86-stub-vs-live-narrative-seam-contrast]]).
