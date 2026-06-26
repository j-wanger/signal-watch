---
title: "Skip the casework re-vendor (no observable change — the subtraction test)"
aliases: ["skip casework re-vendor", "casework re-vendor no-op"]
category: decisions
tags: [phase-75, cross-pillar, casework, vendoring, subtraction-test]
parents: [phase-75-consume-substrate-v05-er-emission]
created: 2026-06-25
updated: 2026-06-25
source: plan
confidence: high
---

## Context

Phase 75 re-pins substrate `f15c241 → fc98b09` to consume v0.5. The parallel question: re-vendor
aml-casework from the held pin to its live HEAD `4a858e6`? The code-verified check found aml-casework's
P15/P16 are internal reconciliation harnesses — the verdict engine and the subprocess contract are
byte-identical to the held pin; the affirmative-`cleared` verdict and the confidence-graded-resolution
path are still UNBUILT.

## Decision

SKIP the casework re-vendor. Re-vendoring changes nothing observable (verdict engine + subprocess contract
byte-identical; `cleared`/graded-resolution still unbuilt), so by the subtraction test it does not earn the
churn. The casework brief is re-grounded to `4a858e6` with the `cleared`/graded-resolution targets recorded
as still NOT-BUILT.

Alternative rejected: re-vendor for pin-currency hygiene — rejected because a vendoring bump that changes
no observable behavior is churn, not value (the Phase-62 "a pin re-ground alone is a zero-movement no-op"
pattern).

## Consequences

- No vendored-tree churn; the `--measure-casework` consume behavior is unchanged.
- If re-vendoring is later found to change observable behavior (e.g. once casework builds `cleared`), the
  skip is reconsidered — it's a named sibling follow-on, not a closed door.
