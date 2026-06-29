---
title: "Phase 82 — merge-org class ABORTED again, sharper reason: P38 fragments share no resolution handle with their base"
aliases: [phase-82-merge-org-abort-no-handle, phase-82-org-fragment-no-handle]
category: decisions
tags: [cross-pillar, consume, substrate, merge-oracle, org-name-collision, measure-first, abort, entity-resolution, firewall]
parents: [phase-82-consume-sibling-northstar-evidence-at-scale]
created: 2026-06-29
updated: 2026-06-29
source: debrief
confidence: high
---

## Context

Phase 81 aborted the merge ORG name-collision track because substrate's anchored fragment overlay was
PERSON-ONLY (0 org GT clusters) — a flagged org could never have a same-org fragment, so the oracle was
one-sided. substrate Phase 38 (`a9a088a`) DID build the org fork (364 `O-FRAG` fragments + 16
flag-intersected), so Phase 82 set out to un-abort the track as a 4th SCORED merge population, gated
measure-first (A2: two-sided on signal-watch's OWN distill/scorer path before any `dist/merge` touch).

## Decision

ABORT the merge-org track AGAIN — for a sharper reason than Phase 81. Although P38 emits the org
fragments, **each fragment shares NO resolution handle with its base**: a perturbed name plus a fresh
`incorporation_number` and address mean **0 of 364 fragment-base pairs share a unique identifier**. So
`candidate_pairs()` never proposes the base→fragment merge → 0 uphold candidates → the oracle is again
one-sided on our own path (5 sanctions-touching candidates, all correct-rejection). `dist/merge` BYTE-FROZEN.

Rejected: **adding fuzzy name-matching** to manufacture base→fragment candidates from the perturbed
names. The wiki ER caveat is explicit — loosened name matching WITHOUT identifier layering pushes false
positives >90% ([[wiki:entity-resolution-and-network-analytics]]). The honest move is to ask substrate
to RETAIN a shared identifier on the fragment (the sharpened org-fragment-emit brief), not to fabricate
two-sidedness on our side.

## Consequences

- `dist/merge` BYTE-FROZEN (the planned 4th-consecutive re-freeze never happened — the org track aborted
  at the measure-first gate). The 8 non-merge dists were already byte-frozen.
- `docs/substrate-org-fragment-emit-PLAN-BRIEF.md` sharpened: the ask moves from "emit org fragments" (P38
  did that) to "retain a SHARED RESOLUTION HANDLE on the fragment" (a stable identifier the base also
  carries) so the base→fragment merge becomes a candidate. When substrate emits that, the merge-org class
  becomes buildable two-sided — a clean Phase N+1 candidate.
- The measure-first gate did exactly its job for the 3rd merge-track abort in a row (Phase 77 circular /
  Phase 81 person-only / Phase 82 no-handle). The pattern: substrate's self-reported magnitudes (here
  16-uphold/35-reject) must always be re-measured on our own path — the self-report counted intersections
  that never become merge candidates.
- No fabrication; the no-synthetic-uphold discipline held.
