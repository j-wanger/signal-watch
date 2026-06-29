---
title: "Phase 85: when the live measurement contradicted the A1 prediction, add population base-rate context and re-measure ONCE — not iterate-to-fit"
aliases: [phase-85-base-rate-remeasure, remeasure-not-overfit, base-rate-context, one-principled-revision]
category: decisions
tags: [agentification, determination, measurement, honesty, overfit, base-rate, user-override]
parents: [phase-85-determination-pre-proposer, phase-85-over-flag-headroom-not-miss-recovery]
created: 2026-06-29
updated: 2026-06-29
source: debrief
confidence: high
---

## Context

Mid-implementation the live agent capture CONTRADICTED the optimistic half of the A1 over-flag-recovery
prediction ([[phase-85-over-flag-headroom-not-miss-recovery]]): the agent corrected the structural KYC
over-flag (abstained on all 727) and recovered more files (74 vs the engine's 50), but it OVER-files on
the volume ML class (committed-wrong 4482 vs the engine's 593) — it files the dominant `C2|C3|C8`
signature (4040 cases, 4029 benign) because it reasons from per-case red-flag co-occurrence, blind to the
population base rate the calibrated deterministic rule encodes. The orchestrator surfaced this to the
user (not silent — the honesty governor's mid-build obligation). The risk on the table: chase a "better"
number by iterating the prompt against the oracle until the over-file shrinks — which would be
overfitting to the single synthetic oracle (no held-out calibration set exists).

## Decision

Make ONE principled prompt revision — add the public typology-monitoring false-positive / base-rate
context to the proposer prompt — and re-measure ONCE. The revision is grounded in the PUBLIC TM
false-positive standard (a population fact the agent legitimately lacked), NOT tuned against the oracle's
labels. The honest two-sided finding (the agent trades conservatism for sensitivity; over-files on the
volume class even WITH base-rate context) STANDS as the deliverable. The measurement is the deliverable,
not a target to optimize.

Rejected: iterating the prompt to-fit against the oracle until the over-file count shrank (overfitting
to one synthetic oracle, no held-out set — dishonest); suppressing or re-framing the over-file finding
to preserve the optimistic prediction (the honesty governor forbids it); pinning the harness to the
pre-revision capture (would hide that base-rate context was tried and the over-file persisted).

## Consequences

- The committed live capture is the base-rate-informed run; the over-file finding is recorded honestly
  (counts-only, synthetic-substrate-qualified) in the phase article, `docs/determination-live.md`, the
  commit message, and the roadmap Stage-2-BUILT note.
- The deviation is logged as a USER OVERRIDE escape hatch (the mid-build measurement contradicted the
  A1 prediction; the user directed the remeasure; one revision, reported honestly, not iterated-to-fit).
- The finding VINDICATES propose→gate→decide rather than undermining the phase: a sensitivity-rich
  proposer + a population-calibrated deterministic gate + a human decision is exactly the architecture.
- A base-rate-aware tool (a population prior / a held-out calibration set) is a named future candidate —
  but it must avoid overfitting to the single oracle (no held-out set exists yet), so it needs careful
  honest framing before it is built.
- Pattern (reusable): when a live agent measurement contradicts a planning prediction, surface it,
  make at most ONE principled (publicly-grounded) revision, re-measure, and report the honest outcome —
  do not grind the prompt against the oracle.
