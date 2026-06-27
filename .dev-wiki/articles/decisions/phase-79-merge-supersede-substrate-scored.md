---
title: "Phase 79: the merge console SUPERSEDED the consensus-66 with substrate-scored real cases"
aliases: [merge-supersede, substrate-scored-replaces-consensus, anchored-oracle-scored]
category: decisions
tags: [cross-pillar, merge-console, anchored-oracle, synthetic-substrate, oracle-provenance, supersede, honesty]
parents: [phase-79-consume-sibling-emissions]
created: 2026-06-27
updated: 2026-06-27
source: plan
confidence: high
---

# Decision — substrate-scored real population replaces the consensus-66

## Context

The merge console (Phase 76) shipped 66 REAL candidate SHARES as **consensus-not-ground-truth,
NO oracle** — the load-bearing honesty stance was "no fabricated truth on real data." Phase 77
attempted to score them against substrate's `--identity` `true_entities` and STOPPED at the abort
rule (the oracle was content-addressed `ENT-<entity_ref>` — a 1:1 relabel of the spine's own
decision key → circular). Phase 79's T3 measure-first gate then reproduced substrate's Phase-32/33
`--anchored --emit-eval-oracles` emit CLEAN and confirmed a NON-circular `GT-<hash>` oracle where
`entity_ref ≠ cluster` (257 entity_refs → 233 opaque clusters; 17 same-person fragment clusters /
31 latent should-merge pairs — Phase-77 had ZERO). With a genuine oracle in hand, the user called
"supersedes."

## Decision

REPLACE the merge console's real population with **29 substrate-anchored SCORED cases** (the
Phase-75 over-merge-refused residual, re-curated from the anchored 400-client slice). BOTH
populations now scored, **split by oracle PROVENANCE** (not consensus-vs-scored): substrate-scored
(GT- oracle) and synthetic-scored (`true_entities`). The honesty pivot retires the "no oracle on
real data" stance — substrate data was never PRODUCTION-real (it is synthetic-substrate); it merely
LACKED an independent oracle until the anchored fork. Scoring synthetic-substrate against its own
latent truth is legitimate, qualified "synthetic-substrate-anchored, no production ground truth."

**Alternatives rejected.** (a) Keep the 66 as a 3rd consensus population (additive, lower-risk) —
rejected: an independent oracle now exists, so consensus would understate what we can honestly show.
(b) Preserve the exact committed 66 `entity_ref`s — impossible: the anchored slice is a different
400-client population (only 1/104 overlap), so the residual is a fresh 29.

## Consequences

`curate_merge_cases.enumerate_substrate_scored` replaces `enumerate_real_shares`; `validate_merge_cases`
(build.py) mirrors it in EXACT parity (the Phase-76 lesson) + a masking firewall (no real email
domain ships). `merge.html` + `merge-console.test.mjs` (73→74) updated; `dist/merge` RE-FROZEN
(90,831 B — the ONE sanctioned dist touch). The substrate population scores the DEMOTED spine
(Phase-75 noise-floor) → it refuses all 29, so the ORACLE discriminates (13 fragmentation-gap uphold /
16 correct-rejection reject). LIMITATION stated plainly in the console: that population is
constant-verdict; only the synthetic-13 spans all four quadrants incl. the over-merge trap. A1 held
(`evidence_requirements.py` byte-unchanged); build.py firewall clean.

Related: [[decisions/phase-79-merge-measure-first-before-dist]] ·
[[decisions/phase-77-consume-3-true-entities-one-sided]] · `docs/substrate-open-reference-data-fork-PLAN-BRIEF.md`.
