---
title: "Phase 82 — full batch of four independently-gated tracks (Both clusters)"
aliases: [phase-82-full-batch-four-tracks, phase-82-both-clusters]
category: decisions
tags: [cross-pillar, consume, scope, batch, independently-gated, honest-reshape]
parents: [phase-82-consume-sibling-northstar-evidence-at-scale]
created: 2026-06-29
updated: 2026-06-29
source: plan
confidence: medium
---

## Context

Four sibling emissions landed since signal-watch's last pins, all code-verified READY this session
(substrate @294d3e5: P38 `a9a088a` org-fragment, P39 `1483c84` predicate, P40 `978c8fe` mitigation;
casework @04cc335: P20 `a059fc5` C15/C4 reconcile). Three of the four directly answer handoff briefs
signal-watch itself authored. The scope question: consume one cluster (the §12 evidence) or take the
full batch (§12 + merge + casework)?

## Decision

Take the **full batch** — all four tracks (user chose "Both clusters (full batch)" at the direction
gate, AskUserQuestion 2026-06-29) — but structure each track as INDEPENDENTLY gated so any can degrade
to an observable/brief without forcing the others. The §12 predicate (T4) and mitigation (T5) gate on
their own rigorous deltas (T2b/c); the merge-org class (T3) gates on its own two-sidedness (T2a); the
casework re-vendor (T6) gates on a fail-close→sign funnel direction (T2d). The substrate re-emit (T1)
is a shared dependency with its own emit-stability abort.

Rejected: a single all-or-nothing consume (one degenerate track would sink the others); deferring three
tracks to bank one thin consume (the Phase-77/79/80/81 batch-consume precedent shows the batch is the
efficient unit when each track is independently gated).

## Consequences

- Independent gating = the Phase-81 honest-reshape pattern at the batch level: a degenerate §12 delta
  ships an observable while the merge class still ships (or vice versa); the phase delivers whatever
  survives its gates plus the always-landed true-ups (briefs, re-pin, cross-pillar build-order).
- `dist/merge` is the ONE conditional re-freeze (4th consecutive), GATED on T2a two-sided; the 8
  non-merge dists stay byte-frozen regardless.
- The blast radius per track is contained: a track abort routes to a named brief, not a phase failure.
- STANDARD ceremony fits — the breadth is four independently-gated consumes, the precedent unit.
