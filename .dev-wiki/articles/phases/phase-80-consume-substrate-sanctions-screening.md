---
title: "Phase 80: Consume substrate Phase 34 — OFAC name-collision merge case class + a non-tautological C14 §12 leg"
aliases: [phase-80]
category: phases
tags: [cross-pillar, consume, substrate, sanctions-screening, ofac, name-collision, merge-oracle, c14-kyc, measure-first, firewall]
parents: []
created: 2026-06-27
updated: 2026-06-27
source: plan
status: active
ceremony: standard
scope: ["tests/fixtures/merge-sanctions-oracle/**", "scripts/resolution_scorer.py", "scripts/curate_merge_cases.py", "data/merge/cases.json", "scripts/build.py", "merge.html", "dist/merge/**", "tests/merge-console.test.mjs", "scripts/serve_workbench.py", "data/casefile/**", "docs/*-PLAN-BRIEF.md", "docs/cross-pillar-build-order.md", "CLAUDE.md"]
entry_criteria: "substrate Phase 34 @1f5901e code-verified live (seam-5 sanctions-screening realism: dead sanctions_flag made LIVE under --anchored via a label-blind real-OFAC-watchlist NAME COLLISION + a revived non-tautological C14 KYC-integrity branch). Phases 32/33 already consumed in the Phase-79 merge slice (the sanctions layer is the delta). Direction gate closed (Consume P34: merge + workbench)."
exit_criteria: "T1 measure-first: the Phase-34 --anchored sanctions emit captured + two-sided assessed (THE ABORT GATE; one-sided → abort merge to workbench-only + a substrate emit-two-sidedness brief). On a clean result: the OFAC name-collision merge basis curated (validate↔curate EXACT parity) + dist/merge re-frozen + tests/merge-console.test.mjs updated. ALWAYS: the workbench §12 non-tautological sanctions-driven C14 leg lights kyc (companion-only, additive); the substrate P35 brief + cross-pillar-build-order + the casework C14-fails-closed drift correction trued up; --check all → the 8 non-merge dists byte-frozen + dist/merge re-frozen-or-untouched; evidence_requirements.py byte-unchanged; uv run pytest green."
grounded_against:
  signal-watch: HEAD (Phase 79 committed, 031a33a)
  aml-substrate: 1f5901e (Phase 34 seam-5 sanctions-screening realism)
  aml-casework: 076fb8e (Phase 19, the Phase-79 vendor pin — nothing new to consume)
---

# Phase 80 — Consume substrate Phase 34

## Objective

Consume aml-substrate's one unconsumed emission (Phase 34 @`1f5901e` — seam-5 sanctions-screening
realism: the previously-dead `sanctions_flag` made LIVE under `--anchored` via a label-blind
real-OFAC-watchlist **NAME COLLISION** + a revived **non-tautological C14 KYC-integrity branch**).
Two consumes + a queue: **(1) MERGE CONSOLE** — add an OFAC watchlist name-collision case class
(a synthetic party's real-frequency name collides with a real public-domain OFAC entry → same latent
entity [uphold the link] vs common-name false positive [reject]), MEASURE-FIRST gated; **(2)
WORKBENCH §12** — a non-tautological sanctions-driven C14 leg lights the kyc determination (additive
to the v0.5 slice; the C14→kyc path already exists from Phase 72); **(3)** author the substrate P35
handoff brief (TF slice / broader C7 / org-name sanctions / Stage-2-3 open data — the confirmed
remaining frontier) + cross-pillar true-ups.

## Why now (the verified delta)

Phases 32/33 (`--anchored` same-person fragments + real-frequency names) were **ALREADY consumed in
the Phase-79 merge slice** — verified, not assumed: the `"Anna Vega"`/`"Anna eVga"` fragment pairs
sit in `data/merge/cases.json`. Phase 34's **sanctions layer is the delta**: the committed slice has
NO sanctions / watchlist / OFAC / C14 content, so the seam-5 emission is genuinely unconsumed and
genuinely additive (not a re-grind of work already landed). substrate's remaining emissions
(TF slice / C1 [a documented measured null, not a gap] / broader C7 / org-name sanctions / Stage-2-3
open data) are **P35+ and NOT yet built** — so this is likely signal-watch's last substantial local
consume for a while (`docs/cross-pillar-build-order.md`).

## The two consumes + a queue

**MERGE (gated, measure-first):** the OFAC collision is the natural second merge case class — a
candidate LINK between a synthetic party and a real OFAC entry sharing a high-frequency name, where
the latent truth is either same-entity (a genuine sanctions hit the demoted spine should uphold) or a
common-name false positive (the spine correctly refuses). T1 captures the Phase-34 `--anchored`
sanctions emit companion-only and assesses two-sidedness — **THE ABORT GATE.** Only on a clean,
two-sided, non-tautological result do T2/T3 curate the basis and re-freeze `dist/merge` (the ONE
sanctioned dist touch). The Phase-77 / Phase-79 abort rule governs: emit won't reproduce / tautological
/ one-sided → STOP the merge track to workbench-only + a substrate emit-two-sidedness brief; T3 does
not run.

**WORKBENCH §12 (always):** a non-tautological sanctions-driven C14 leg lights the kyc determination
— ADDITIVE to the committed v0.5 slice (provenance-tagged, not a population swap), exercising the
C14→kyc path that already exists from Phase 72. Companion-only; `evidence_requirements.py`
byte-unchanged (the A1 guard).

## Scope

`tests/fixtures/merge-sanctions-oracle/**` + `scripts/resolution_scorer.py` +
`scripts/curate_merge_cases.py` (the measure-first oracle + the curated basis) · `data/merge/cases.json`
+ `scripts/build.py` + `merge.html` + `dist/merge/**` + `tests/merge-console.test.mjs` (the gated
re-freeze) · `scripts/serve_workbench.py` + `data/casefile/**` (the workbench C14 leg) ·
`docs/*-PLAN-BRIEF.md` + `docs/cross-pillar-build-order.md` + `CLAUDE.md` (the substrate P35 brief +
the casework C14-fails-closed drift correction + docs true-up).

## Exit Criteria

- [ ] T1 measure-first: the Phase-34 `--anchored` sanctions emit captured (no-substrate replayable) +
      two-sidedness assessed — THE ABORT GATE (one-sided → abort merge, workbench-only + brief)
- [ ] (gated) the OFAC name-collision merge basis curated; validate↔curate EXACT parity; `dist/merge`
      re-frozen; `tests/merge-console.test.mjs` updated
- [ ] the workbench §12 non-tautological sanctions-driven C14 leg lights kyc (companion-only, additive,
      provenance-tagged)
- [ ] `--check all` → the 8 non-merge dists byte-frozen + `dist/merge` re-frozen-or-untouched
- [ ] `evidence_requirements.py` BYTE-UNCHANGED (the A1 guard); build.py imports no
      spine/scorer/sibling/curate
- [ ] the substrate P35 brief + cross-pillar-build-order trued up; the casework C14-fails-closed drift
      correction + stale FOLLOW-ON markers reconciled
- [ ] `uv run pytest` green; honesty governor (no catch-rate/lift/precision/recall wording);
      synthetic-substrate-anchored qualifier; OFAC false-positive-trap framing; badge always-on

## Constraints

- `evidence_requirements.py` BYTE-UNCHANGED (prevents the file-bar A1 regression).
- build.py imports no spine/scorer/sibling/curate (prevents the companion-into-build firewall breach).
- The 8 non-merge dists byte-frozen; `dist/merge` the ONE sanctioned re-freeze — gated on the T1
  measure-first result (a second consecutive sanctioned re-freeze).
- validate↔curate EXACT parity (the Phase-76 lesson) (prevents a weaker build-boundary validator than
  the authoring curator).
- Real OFAC ships clean under 17 USC §105 (US-federal public domain — covers OFAC), framed STRICTLY
  as the false-positive trap (the synthetic party ≠ the sanctioned entity).

## Abort

Any non-merge dist drift / a build.py spine/scorer/sibling/curate import / an `evidence_requirements.py`
change / a confusion number presented as a catch-rate or lift → STOP-and-surface. Merge track: the
Phase-34 sanctions emit won't reproduce after bounded attempts / tautological / one-sided → STOP to
workbench-only + a substrate emit-two-sidedness brief; T3 (the dist re-freeze) does NOT run; the
workbench C14 leg + the P35 brief still land.

## Decisions

[[decisions/phase-80-merge-plus-workbench-consume]] · [[decisions/phase-80-sanctions-oracle-measure-first]]

Spec `specs/phase-80-consume-substrate-sanctions-screening.md`; ledger Phase-80.
