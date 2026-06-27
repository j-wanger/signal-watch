---
title: "Phase 79: merge real-data consume is measure-first companion-only before any dist re-freeze"
aliases: [merge-measure-first, anchored-oracle-de-risk]
category: decisions
tags: [cross-pillar, merge-oracle, measure-first, substrate, abort-rule, honesty, firewall]
parents: [phase-79-consume-sibling-emissions]
created: 2026-06-27
updated: 2026-06-27
source: plan
confidence: high
---

# Decision — merge real-data consume is measure-first before any dist touch

## Context

Substrate Phase 32 mints `entity_ref ≠ cluster` anchored fragments (opaque `GT-<sha1>` cluster
ids), the property that cures the Phase-77 circular merge oracle. **But** the live
`--anchored --emit-eval-oracles` run **CRASHED today** with a substrate `ReplayError`
(`fin-2023-alert003:IND-05` at n=400/seed0). The non-circular property is proven only by substrate
tests that drive `build_dataset` directly — they bypass the full CLI replay — so end-to-end emit
reproduction across the CLI boundary is **UNKNOWN**.

## Decision

Make the merge real-data consume **measure-first, companion-only FIRST** (the Phase-78
determination-validation harness pattern), and gate the `dist/merge` re-freeze (T4) on a clean,
two-sided, non-tautological result:

1. Pin a known-good substrate param set (route around the n=400/seed0 ReplayError), drive the
   `--anchored --emit-eval-oracles` emit, score the spine's real refusals + fragment should-merges
   against the non-circular `GT-` oracle, and commit a **no-substrate-replayable** confusion
   capture + baseline (`tests/fixtures/merge-anchored-oracle/`).
2. THEN, only on a clean result, re-curate `data/merge/cases.json` (consensus → scored) and
   re-freeze `dist/merge` (the ONE sanctioned dist touch this phase).

Measure-first de-risks BOTH the emit reproduction and the ship-dist boundary, and matches the
project's measure-first DNA. The **Phase-77 abort rule governs**: emit won't reproduce after
bounded attempts / tautological / one-sided → STOP the merge track to consensus + author a
substrate emit-stability brief; T4 does NOT run; ship the Lakeshore floor + the honest non-result.

**Alternative rejected.** Commit to the `dist/merge` re-freeze up front — given the live emit crash,
that would couple a ship-dist change to an unverified cross-pillar emission and risk presenting a
fabricated "scored" claim under pressure to ship.

## Consequences

The dist re-freeze is conditional, not assumed. The honesty seam holds either way: a clean result
ships as scored with the synthetic-substrate-anchored qualifier; an abort ships as consensus with no
catch-rate/lift/precision/recall wording, never a fabricated number. `assert_no_cluster_leak` + the
firewall hold; `evidence_requirements.py` byte-unchanged.

**Outcome (2026-06-27):** the gate cleared GREEN — the emit reproduced clean (the ReplayError was
`--monitor`/`--emit-evidence`, orthogonal to the emit path), the `GT-` oracle was non-circular/two-sided
(13 should-merge / 16 correct-reject), so T4 ran and `dist/merge` was re-frozen (scored). See
[[decisions/phase-79-merge-supersede-substrate-scored]].

Related: [[decisions/phase-79-floor-plus-gated-upside-bundle]] ·
[[decisions/phase-79-merge-supersede-substrate-scored]] · [[cross-pillar-review-verify-sibling-repo]] ·
the Phase-77 circular-oracle abort · [[measuring-to-controlling-pivot]].
