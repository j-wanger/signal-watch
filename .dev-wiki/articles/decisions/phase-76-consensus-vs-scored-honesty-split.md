---
title: "Consensus-vs-scored split is the merge console's load-bearing honesty seam"
aliases: ["consensus not ground truth", "synthetic-only scored oracle", "real-consensus synthetic-scored split"]
category: decisions
tags: [phase-76, merge-console, honesty, scored-oracle, true-entities, consensus]
parents: [phase-76-merge-adjudication-console]
created: 2026-06-25
updated: 2026-06-25
source: plan
confidence: high
---

## Context

The merge console's architectural novelty is that — unlike the consensus-only gate console and the
label-blind §14 triage — the merge gate can have a measurable correctness ORACLE (`true_entities`):
the Reveal can SHOW whether an adjudication matched truth. But the REAL substrate candidate SHARES
(the 66 from the committed v0.5 slice) have NO ground truth — production entity resolution has none,
and fabricating truth on real data would violate the project's honesty non-negotiable. The question:
how does a single console honestly carry both a scored dimension and real un-scored cases?

## Decision

Split the populations and make the split visible. REAL substrate candidate SHARES are
consensus-not-ground-truth and carry NO oracle (no fabricated truth on real data). Only SYNTHETIC
cases are scored against the `true_entities` oracle, and every scored number carries the mandatory
synthetic-only qualifier ("measured on synthetic clusters; production has no ground truth"). The
Reveal screen and the ledger visibly SPLIT real-consensus from synthetic-scored. Scoring over real
substrate stays a NAMED sibling handoff (the substrate-true-entities-emission brief), never faked
here. No catch-rate / lift / precision-as-detection claim anywhere; the always-on "Illustrative data
& outputs" badge stays.

## Consequences

The console honestly delivers its differentiator (a scored merge gate) without claiming a real
catch-rate. The scored cases come from the expanded synthetic oracle (T1: 8→25 obs / 5→17 clusters,
13 candidates, 9 ambiguous); the real cases come from the committed slice and are adjudicated on
consensus. The split is structural, not a disclaimer — the Reveal renders two distinct populations.
The path to scoring real cases is a documented substrate-emit dependency (pinned fc98b09), not a
gap to be papered over. This mirrors the Phase-74/75 resolver discipline (synthetic-only-qualified
scoring; no ground truth in production) carried into a ship artifact.
