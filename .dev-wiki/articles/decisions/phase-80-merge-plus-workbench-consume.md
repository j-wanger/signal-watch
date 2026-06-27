---
title: "Phase 80: consume substrate Phase 34 as a merge case class + a workbench §12 C14 leg (two consumes + a queue)"
aliases: [phase-80-consume, ofac-collision-merge-plus-c14]
category: decisions
tags: [cross-pillar, consume, substrate, sanctions-screening, ofac, merge-console, c14-kyc, ceremony]
parents: [phase-80-consume-substrate-sanctions-screening]
created: 2026-06-27
updated: 2026-06-27
source: plan
confidence: medium
---

# Decision — consume Phase 34 as a merge case class + a workbench §12 C14 leg

## Context

substrate Phase 34 (`1f5901e`, seam-5 sanctions-screening realism) is aml-substrate's ONE unconsumed
emission: the previously-dead `sanctions_flag` is made LIVE under `--anchored` via a label-blind
real-OFAC-watchlist **NAME COLLISION** plus a revived **non-tautological C14 KYC-integrity branch**.
Phases 32/33 (`--anchored` same-person fragments + real-frequency names) were ALREADY consumed in the
Phase-79 merge slice — code-verified, not from the snapshot: the `"Anna Vega"`/`"Anna eVga"` fragment
pairs are in `data/merge/cases.json`. So the sanctions layer is the genuine delta (the committed slice
has no sanctions / watchlist / OFAC / C14 content). casework @`076fb8e` (Phase 19) sits at the Phase-79
vendor pin — nothing new to consume there. The seam-5 emission has two natural consumption surfaces:
the merge console (the collision shapes as an entity-LINK candidate) and the workbench §12 loop (the
C14 leg lights kyc via the path already built in Phase 72). Jake's direction: "Consume P34: merge +
workbench."

## Decision

Consume Phase 34 across BOTH surfaces in ONE STANDARD phase, plus author the substrate P35 handoff:

- **MERGE CONSOLE** — add an OFAC watchlist name-collision case class: a candidate LINK between a
  synthetic party (real-frequency name) and a real public-domain OFAC entry, where the latent truth is
  same-entity (uphold the link — a genuine sanctions hit) vs common-name false positive (reject). This
  is MEASURE-FIRST gated (see [[decisions/phase-80-sanctions-oracle-measure-first]]).
- **WORKBENCH §12** — a non-tautological sanctions-driven C14 leg lights the kyc determination,
  ADDITIVE to the v0.5 slice (provenance-tagged, not a population swap), exercising the established
  C14→kyc path.
- **QUEUE** — author the substrate P35 brief (TF slice / broader C7 / org-name sanctions / Stage-2-3
  open data — the confirmed remaining frontier) + the cross-pillar true-ups, including the casework
  drift correction (its txn-less C14 party-leaf is NO LONGER fails-closed — completes via the resolving
  party leaf; the test fixture reaches `signed`).

Rationale: the Phase-77 / Phase-79 precedent (bundle independent modest consumes under one STANDARD
phase) holds; both surfaces consume the SAME emission, so bundling keeps cross-pillar coherence and
amortizes the regate. The workbench leg lands phase value unconditionally even if the merge track
aborts. Direction gate: the user picked "Consume P34: merge + workbench" via AskUserQuestion
2026-06-27 (all_accept, with A1's measure-first gate user-positioned); the one-sided fallback is
"Abort merge → companion + brief".

**Alternatives rejected.** (a) Merge-only this phase, deferring the workbench leg — under-uses an
emission that lights two surfaces and leaves the §12 C14 path unexercised on real-ish data.
(b) Workbench-only, skipping the merge consume up front — forecloses the upside before the measure-first
gate runs; the gate, not a planning guess, should decide it. (c) Three separate phases — ceremony
overhead for independent, modest, same-emission consumes.

## Consequences

The workbench C14 leg + the P35 brief land unconditionally; the merge case class is genuinely optional
behind its abort gate. STANDARD ceremony stands (cross-pillar + a conditional ship-dist touch). The A1
guard holds across both surfaces (`evidence_requirements.py` byte-unchanged); the firewall (build.py
imports no spine/scorer/sibling/curate) and the 8 non-merge dists stay frozen; `dist/merge` is the ONE
sanctioned, gated re-freeze (its second consecutive — see A3 in the ledger). Real OFAC ships clean
under 17 USC §105, framed STRICTLY as the false-positive trap (the synthetic party ≠ the sanctioned
entity). This is likely signal-watch's last substantial local consume until a substrate P35.

Related: [[phase-80-consume-substrate-sanctions-screening]] ·
[[decisions/phase-80-sanctions-oracle-measure-first]] ·
[[phase-79-merge-supersede-substrate-scored]] · [[cross-pillar-review-verify-sibling-repo]] ·
`docs/cross-pillar-build-order.md`.
