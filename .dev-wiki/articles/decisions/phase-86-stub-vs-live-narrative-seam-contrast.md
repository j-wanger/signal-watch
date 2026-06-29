---
title: "Phase 86 — The measure is non-degenerate because the stub drafter fail-closes on the narrative-seam case (the two-sided contrast)"
aliases: [phase-86-narrative-seam-contrast, stub-vs-live-contrast, measure-first-classify-population]
category: decisions
tags: [agentification, stage-3, str-drafter, measure-first, two-sided, narrative-seam, planning]
parents: [phase-86-str-drafter-consistency-measure]
created: 2026-06-29
updated: 2026-06-29
source: plan
confidence: medium
---

## Context

A stub-vs-live consistency measure is only meaningful if the population spans both gate outcomes — if
the stub drafter SIGNS every committed casefile bundle, "live matches stub" is degenerate (no
contrast to measure). The risk is the same one-sided-population trap that aborted the merge-org class
twice (Phases 81/82). The measure must be classified-first before any live claim.

## Decision

The measure is non-degenerate because the deterministic STUB drafter fail-closes on the hard
narrative-seam case (Phase-82's `CASE-P-0025128`, a txn-bearing C14 where casework's stub drafter
fails narrative verification — "seam left open"). The committed casefile bundles (`data/casefile/*.bundle.json`,
the designed file/clear/narrative-seam scenarios) therefore span both SIGN and REFUSE — that case is
the two-sided contrast point: does the live agent sign where the stub couldn't, or does the
fabrication guard catch it? T1 measure-first CLASSIFIES the population first (run the stub per bundle,
confirm at least one fail-close); an honest NULL is surfaced if it proves degenerate, with a
deliberately-ungrounded case as the named fallback. Population = the committed casefile bundles (scale
via a slice sample deferred). User-positioned at the gate (Q1 + Q3 = Accept).

## Consequences

The measurement frame has a real fulcrum, not a vacuous "live == stub". The narrative-seam case
doubles as the demo's defensibility climax: the verifier refuses what the agent cannot ground. If T1
finds the stub signs everything (the population is one-sided after all), the abort rule fires — ship
the honest NULL + the deliberately-ungrounded fallback case, never a manufactured contrast. Scale
(a substrate slice sample) is explicitly out of scope this phase; the committed bundles are the
population.
