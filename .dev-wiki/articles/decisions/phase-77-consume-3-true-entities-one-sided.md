---
title: "Consume #3: revert the real 66 to CONSENSUS and DEFER real scoring — the captured true_entities oracle is CIRCULAR"
aliases: ["one-sided merge scoring deferred", "true_entities oracle is circular", "content-addressed clusters one-sided oracle", "real-66 stays consensus"]
category: decisions
tags: [phase-77, merge-console, true-entities, scored-oracle, honesty, entity-resolution, consume, abort-rule]
parents: [phase-77-consume-sibling-emissions]
created: 2026-06-26
updated: 2026-06-26
source: debrief
confidence: high
---

## Context

Phase 76 shipped the merge console scoring only the 13 SYNTHETIC cases against `true_entities`; the
66 REAL substrate candidate SHARES carried no oracle (consensus-not-ground-truth). The Phase-77 plan
intended to score the real 66 ONE-SIDED — substrate's Phase-29 `--identity` emission writes a
`true_entities.parquet` (`party_id,cluster_id`) for the slice, so the real 66 could in principle be
scored against substrate's own declared ground truth. The weakest planned assumption (A1) was that
this scoring is meaningful, not circular.

At T4 the captured `--identity` parquet (re-emitted from a pinned slice @f2da3e4, party-id-aligned to
the committed slice) was examined: every emitted cluster is content-addressed `ENT-<entity_ref>` — a
1:1 relabel of the SAME `entity_ref` field the deterministic spine keys its merge/refuse decision on,
across all 441 slice persons, with ZERO cross-`entity_ref` merges. Mapping the committed 66 real SHARES
gave 66/66 DISTINCT, 0 same — they are exhaustively substrate's deliberate collision noise floor.

## Decision

REVERT the real 66 to CONSENSUS and DEFER real merge scoring. The user weighed (a) keep "scored" but
reframe it as a true-by-construction consistency check vs (b) revert to consensus + defer, and chose
(b) (2026-06-26: "revert real to consensus, defer"). Scoring the spine against an oracle that is a
relabel of the spine's own key is true-by-construction agreement — zero discriminating signal, not a
measurement. This fired the phase abort rule directly ("a scored number presented as a real catch-rate
→ STOP; if the oracle can't yield ambiguous scored cases honestly → consensus + defer"). The circular
parquet capture was NOT committed.

Alternatives rejected: ship the tautological number reframed as a consistency check (still reads as a
catch-rate to an audience, A1 honesty violation); score the human adjudicator instead of the spine
(the plan's framing — but with 66/66 distinct there is no should-merge to test, so even human-scoring
is one-sided AND the truth is still a relabel of the spine key, so it cannot disagree).

## Consequences

`merge.html`, `data/merge/cases.json`, `tests/merge-console.test.mjs`, `curate_merge_cases.py`, and
the `build.py merge` target are reverted to their Phase-76 CONSENSUS state (real-66 no oracle); the
genuinely two-sided synthetic-13 oracle (resolver verdict and truth DIVERGE independent of any spine
key) is untouched and still scored. `dist/merge` stays BYTE-FROZEN (no dist touch this phase — the one
planned dist change is voided). Real merge scoring needs `entity_ref ≠ cluster` — a genuine identity
layer where the truth is not a relabel of the spine key (real same-person fragments / the open-data
fork's real collisions) → parked in `docs/substrate-emit-cli-wiring-PLAN-BRIEF.md` (deeper-gap section)
and `docs/substrate-open-reference-data-fork-PLAN-BRIEF.md`. The open-data fork is the unblocking move.
