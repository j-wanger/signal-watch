---
title: "Phase 81 — Consume substrate Phases 35–37: the sanctions arc (both planned consumes hit measure-first branches → C17 observable-only + org-merge abort) (standard, planned+delivered same session)"
aliases: []
category: journal
tags: [cross-pillar, consume, substrate, sanctions-screening, ofac, org-name-collision, merge-oracle, c17-exposure, exposure-via-ownership, geo, open-sanctions, measure-first, firewall, observable-only]
parents: [phase-81-consume-substrate-sanctions-arc]
created: 2026-06-28
updated: 2026-06-28
source: debrief
duration: ~4-5h (post-compaction estimate; may undercount)
---

# Phase 81 — Consume the substrate sanctions arc: both planned consumes hit measure-first branches

## What Happened
- Set out to consume aml-substrate Phases 35–37 (the **sanctions arc** beyond our Phase-34 pin `1f5901e` → HEAD **f7fbdb0**, both sibling HEADs code-verified LIVE this session, file:line): P35 `4f49e53` org-name OFAC SDN collision, P36 `1651b1e` the C17 exposure-via-ownership leg, P37 `5b5cf32` geo enrichment. Planned: a merge ORG-collision case class (the Phase-80 person-class's sibling) + the C17 leg as a §12 evidence-breadth advance + a P37 geo render + an open-sanctions plan-brief.
- **Both planned consumes hit their measure-first abort/reframe branches — the gates did exactly their job.** The phase delivered an HONEST reshape, not the planned shape: the C17 leg ships **observable-only** and the merge ORG track is **aborted** (`dist/merge` byte-frozen). The §12 geo render, the three briefs, the cross-pillar true-ups, and the verification all landed as planned.
- **T1a (merge org two-sidedness) → reject-branch FIRED (the Phase-77 trap, structural).** Drove substrate @f7fbdb0 `--anchored` as TOOL-USE (subprocess; build.py never imports it). The org-collision oracle is STRUCTURALLY one-sided: substrate's anchored fragment overlay is PERSON-ONLY (354 multi-record GT clusters, 100% person; ZERO org fragment clusters), so a flagged org can never have a same-org fragment → every org-name collision is between DISTINCT orgs → all-reject (10 flagged orgs, 3 candidates, 0 uphold), unfixable by scale or seed. Per A2's reject-branch the merge org track (T2/T3) did NOT run; `dist/merge` BYTE-FROZEN; routed to `docs/substrate-org-fragment-emit-PLAN-BRIEF.md`. The no-fabrication discipline held (no synthetic "uphold" minted to force two-sidedness).
- **T1b (C17 exposure-leg) → DEGENERATE on the rigorous re-measure, after a planning-stage measurement ERROR.** My T1b estimate ("9 of 13 sanctioned-BO customers reach file-ready") counted ≥2 related parties as a leg — a LOOSE PROXY that never checked for a money-laundering MECHANISM. The T4 surface-map workflow's rigorous data-path read caught it; re-measured with the ACTUAL engine (`determine()` with/without the leg) → DELTA = **0**: the 13-case sanctioned-BO cohort carries only C8/C14 (a leg / kyc), no C2/C3/C5/C4 mechanism, so a *leg* can never satisfy `mechanism + 2 legs`. The planned "§12 breadth advance" was unachievable.
- **The in-flight pivot (USER OVERRIDE).** Surfaced the correction to the user; per "accept both abort fallbacks" + a re-asked disposition (AskUserQuestion 2026-06-28), shipped the C17 consume **OBSERVABLE-ONLY**: a `/sanctions-c17-exposure` companion route + `sanctionsC17PanelHTML` panel + the demo bundle `data/casefile/sanctions-c17-exposure-demo.bundle.json` surface the exposure, and the LIVE engine SHOWS the case does NOT reach the determination bar (the §12 discovery feed classifies all 13 as over-flag — a defensive-exposure basis, not a latent-laundering discriminator; substrate's `sanctions_flag` is label-blind, corr≈0 by DESIGN). Honest framing: neither the "§12 breadth" overclaim nor a silent drop. NO `evidence_requirements.py` change, NO dist/engine change.
- **Companion-only, NO ship-dist drift.** All 8 non-merge dists byte-frozen; `dist/merge` UNTOUCHED (the org abort means the would-be-3rd-consecutive re-freeze never happened); build.py imports no spine/scorer/sibling/curate (firewall clean); `git diff --quiet scripts/evidence_requirements.py` (A1 held).

## Decisions Made
- [[phase-81-consume-sanctions-arc-all-three|Phase 81 — consume the FULL sanctions arc (P35 org + P36 C17 + P37 geo), open-sanctions plan-only]] — extracted at the direction gate (Q1 "All three (+ P37 geo)" · Q2 "Plan-only brief + license matrix").
- [[phase-81-exposure-leg-evidence-advance|Phase 81 — the C17 leg as an A1-preserving EVIDENCE atom, rule frozen]] — Q3 "Evidence-advance, rule frozen"; **OVERTAKEN by the T1b degeneracy** (the leg moves 0 cases to the bar — see its OUTCOME note) → re-scoped to observable-only by the in-flight USER OVERRIDE.

## Problems Solved
- **The org-collision is STRUCTURALLY one-sided** (substrate fragments PERSONS, not orgs — 0 org GT clusters) → can't mint a true org same-entity match without fabrication → ABORTED the merge org track per A2's reject-branch, `dist/merge` byte-frozen, routed to `docs/substrate-org-fragment-emit-PLAN-BRIEF.md`.
- **My T1b "9 reach file-ready" was a measurement ERROR** (a loose ≥2-related-parties proxy, no mechanism check) → caught by the T4 surface-map workflow's rigorous data-path read → re-measured with the actual engine → DELTA = 0 (the cohort lacks an ML mechanism) → corrected WITH the user → shipped observable-only.
- **The demo bundle's `resolution_edges` emails were unmasked** (caught by the adversarial review) → fixed (all `@`-strings → example.test), matching the real-substrate domain-masking convention.

## Open Questions
- The signal-watch LOCAL consume frontier is now EXHAUSTED until substrate ships a new emission — the next phase likely AWAITS a substrate emission (org-fragment overlay / a discriminating exposure SIGNAL / open-data Stage 2/3 / a C20 jurisdiction observable over P37's geo) OR pivots to a non-consume direction (a quality/durability true-up of the built artifacts).

## Artifacts Changed
- `scripts/serve_workbench.py` (NEW `/sanctions-c17-exposure` route + the C17 consume path — companion-only)
- `workbench.html` (NEW `sanctionsC17PanelHTML` panel — the observable, names-not-codes; "N pct" not "N%")
- `data/casefile/sanctions-c17-exposure-demo.bundle.json` (NEW companion demo bundle; resolution_edges emails masked to example.test)
- `tests/workbench.test.mjs` (167→178; the C17 block incl. the honesty-governor word-ban assertion)
- `docs/open-sanctions-data-fork-PLAN-BRIEF.md` (NEW — per-source license matrix; OFAC PD / UK OGL ship vs OpenSanctions CC-BY-NC no-ship)
- `docs/substrate-org-fragment-emit-PLAN-BRIEF.md` (NEW — the org two-sidedness handoff, T1a's abort destination)
- `docs/substrate-exposure-signal-PLAN-BRIEF.md` (NEW — a discriminating exposure SIGNAL handoff, the T1b-degeneracy frontier)
- `docs/substrate-p35-determination-signals-PLAN-BRIEF.md` (reconciled: TF + broader-C7 substrate-CUT; org-name DONE)
- `docs/cross-pillar-build-order.md` (trued up to substrate f7fbdb0 / casework 076fb8e; the casework-C17-SIGN gap noted moot for observable-only)
- `CLAUDE.md` (the sanctions-arc consume + the observable-only C17 beat)

## Related
- [[phase-81-consume-substrate-sanctions-arc|Phase 81 — Consume substrate Phases 35–37: the sanctions arc]] — parent phase

## Soft Observations / Phase N+1 Candidates
- The signal-watch LOCAL consume frontier is EXHAUSTED until substrate ships a new emission | Phase N+1 likely AWAITS a substrate emission (org-fragment overlay / a discriminating exposure signal / open-data Stage 2/3 / a C20 jurisdiction observable) OR pivots to a non-consume direction (quality/durability true-up) | evidence: T1a + T1b both hit substrate-structural limits this phase; the 3 new handoff briefs.
- LESSON — a measure-first gate must run the RIGOROUS engine (the actual `determine()` with/without X), never a PROXY | the T1b "9 reach file-ready" error came from counting ≥2 related parties as a leg without a mechanism check; the gate that should have aborted instead produced a false "non-degenerate" signal | evidence: the T4 surface-map catch; the engine re-measure DELTA=0.
- LESSON — a label-blind signal (corr≈0) is structurally an OBSERVABLE, not a determination leg | don't plan a "detection breadth" beat on it; the honest form is an observable + the §12 discovery-feed over-flag framing | evidence: substrate's `sanctions_flag` is label-blind by design (all 13 exposure cases oracle-CLEAR); this is the same shape as Phase 78's over-flag cell.
