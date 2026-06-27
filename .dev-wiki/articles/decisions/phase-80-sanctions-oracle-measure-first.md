---
title: "Phase 80: the OFAC sanctions-collision merge oracle is measure-first before any dist re-freeze (the abort gate)"
aliases: [phase-80-measure-first, sanctions-collision-two-sidedness-gate]
category: decisions
tags: [cross-pillar, merge-oracle, measure-first, substrate, sanctions-screening, ofac, abort-rule, honesty, firewall]
parents: [phase-80-consume-substrate-sanctions-screening]
created: 2026-06-27
updated: 2026-06-27
source: plan
confidence: medium
---

# Decision — the sanctions-collision merge oracle is measure-first before any dist touch

## Context

substrate Phase 34 makes the dead `sanctions_flag` LIVE under `--anchored` via a label-blind
real-OFAC-watchlist NAME COLLISION. The intent is to score the demoted spine's refusals + the genuine
same-entity sanctions hits against substrate's own anchored latent oracle (the `GT-<hash>` clusters
that the Phase-79 fork proved non-circular, `entity_ref ≠ cluster`). **But** the two-sidedness of the
SANCTIONS slice specifically is UNKNOWN before measurement: a watchlist name collision could in
principle reduce to all-coincidence (every synthetic party is a common-name false positive → only
correct-rejects, no should-uphold) — the same one-sidedness trap that voided the Phase-77 real-66
(content-addressed `ENT-<entity_ref>`, 66/66 distinct, zero should-merge). An oracle with no
discriminating signal is a tautology dressed as a catch-rate, not a measurement.
[[cross-pillar-review-verify-sibling-repo]]: code-verify the sibling's live state, never reason from
the loaded snapshot — and here, MEASURE the slice's two-sidedness rather than assume it.

## Decision

Make the merge sanctions-collision consume **measure-first, companion-only FIRST** (the Phase-78
determination-validation harness + Phase-79 anchored-oracle pattern), and gate the `dist/merge`
re-freeze on a clean, two-sided, non-tautological result:

1. **T1 (the abort gate):** capture the Phase-34 `--anchored` sanctions emit (no-substrate replayable,
   `tests/fixtures/merge-sanctions-oracle/`), map the OFAC name-collision candidates, score the demoted
   spine's refuse / uphold calls against the non-circular `GT-` oracle, and ASSESS two-sidedness —
   does the slice carry BOTH genuine same-entity sanctions hits (should-uphold) AND common-name false
   positives (correct-reject)?
2. **THEN, only on a clean two-sided result:** curate the OFAC name-collision basis into
   `data/merge/cases.json` (validate↔curate EXACT parity), re-freeze `dist/merge` (the ONE sanctioned
   dist touch this phase, its second consecutive), and update `tests/merge-console.test.mjs`.

The **Phase-77 / Phase-79 abort rule governs**: emit won't reproduce after bounded attempts /
tautological / one-sided → STOP the merge track, route the consume to workbench-only, and author a
substrate emit-two-sidedness brief; T3 does NOT run; ship the workbench C14 leg + the P35 brief + the
honest non-result. Measure-first de-risks BOTH the emit reproduction and the ship-dist boundary, and
matches the project's measure-first DNA.

**Alternative rejected.** Commit to the `dist/merge` re-freeze up front — that couples a ship-dist
change to an unverified two-sidedness assumption on the sanctions slice and risks presenting a
fabricated "scored" claim under pressure to ship (the exact failure the Phase-77 circular oracle
forced into the open).

## Consequences

The dist re-freeze is conditional, not assumed. The honesty seam holds either way: a clean result
ships as scored with the synthetic-substrate-anchored qualifier (the OFAC collision framed STRICTLY as
the false-positive trap — the synthetic party ≠ the sanctioned entity); an abort ships the workbench
leg as the phase value, with no catch-rate / lift / precision / recall wording, never a fabricated
number. The resolver-input firewall + `assert_no_cluster_leak` hold; `evidence_requirements.py`
byte-unchanged (the A1 guard); build.py imports no spine/scorer/sibling/curate. Real OFAC ships clean
under 17 USC §105 (US-federal public domain covers OFAC).

Related: [[phase-80-consume-substrate-sanctions-screening]] ·
[[decisions/phase-80-merge-plus-workbench-consume]] ·
[[phase-79-merge-supersede-substrate-scored]] · [[cross-pillar-review-verify-sibling-repo]] ·
the Phase-77 circular-oracle abort · [[measuring-to-controlling-pivot]].
