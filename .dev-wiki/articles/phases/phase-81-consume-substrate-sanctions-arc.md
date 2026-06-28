---
title: "Phase 81 — Consume substrate Phases 35–37: the sanctions arc (OFAC org name-collision merge class + the C17 exposure-via-ownership §12 leg + geo) + open-sanctions data-fork brief"
aliases: [phase-81]
category: phases
tags: [cross-pillar, consume, substrate, sanctions-screening, ofac, org-name-collision, merge-oracle, c17-exposure, exposure-via-ownership, geo, open-sanctions, measure-first, firewall]
parents: []
created: 2026-06-28
updated: 2026-06-28
source: plan
status: delivered
ceremony: standard
scope: ["scripts/curate_merge_cases.py", "data/merge/cases.json", "scripts/build.py", "merge.html", "dist/merge/**", "tests/merge-console.test.mjs", "tests/fixtures/merge-sanctions-org-oracle/**", "data/entity-spine/**", "scripts/resolution_scorer.py", "scripts/curate_workbench_cases.py", "scripts/serve_workbench.py", "data/workbench/**", "workbench.html", "tests/workbench.test.mjs", "docs/*-PLAN-BRIEF.md", "docs/cross-pillar-build-order.md", "CLAUDE.md"]
entry_criteria: "substrate is 3 phases ahead of our pin (we consumed Phase 34; 35/36/37 are the delta) — code-verified LIVE this session @f7fbdb0 (Phase 37): P35 @4f49e53 (org-name OFAC SDN collision, the org sibling of Phase-80's person class), P36 @1651b1e (the C17 exposure-via-ownership leg), P37 @5b5cf32 (geo/jurisdiction enrichment, observable-only). casework unchanged at the Phase-79 pin @076fb8e (does NOT ground C17). Direction gate closed 2026-06-28 (scope = All three + P37 geo; open-sanctions = plan-only brief + license matrix; bar invariant = evidence-advance, rule frozen; measure-first = accept both abort fallbacks)."
exit_criteria: "T1 dual measure-first: T1a (the org-collision two-sidedness, non-circular `GT-<hash>`) + T1b (the C17 exposure cohort fires non-degenerately + ≥1 case reaches the bar via ≥2 independent legs) — captures committed + no-substrate replayable + both gate decisions documented. IF T1a two-sided: the OFAC org-name collision merge basis curated (validate↔curate EXACT parity) + `dist/merge` re-frozen + `tests/merge-console.test.mjs` updated; ELSE `dist/merge` BYTE-FROZEN + a substrate org-emit-two-sidedness brief. IF T1b non-degenerate: the C17 exposure leg lights ≥1 case to the determination bar via ≥2 INDEPENDENT legs (the determination-bar regression proves the RULE frozen); ELSE the leg ships as a rendered observable + a brief. ALWAYS: P37's geo observable renders; the open-sanctions data-fork PLAN-ONLY brief (per-source license matrix + non-commercial boundary + substrate emit asks); the stale substrate-P35 brief reconciled (TF/C7 substrate-CUT, org-name DONE); cross-pillar-build-order trued up to substrate-P37 HEAD; the casework-C17-SIGN-gap noted; substrate re-pinned `f7fbdb0`; `--check all` (8 non-merge dists byte-frozen + dist/merge re-frozen-or-untouched); `scripts/evidence_requirements.py` byte-unchanged (the A1 guard); `uv run pytest` green."
grounded_against:
  signal-watch: HEAD (Phase 80 committed, a0896da)
  aml-substrate: f7fbdb0 (Phase 37 — P35 4f49e53 org-name OFAC / P36 1651b1e C17 exposure / P37 5b5cf32 geo)
  aml-casework: 076fb8e (Phase 19, the Phase-79 vendor pin — unchanged; does NOT ground C17)
---

# Phase 81 — Consume substrate Phases 35–37: the sanctions arc

## Objective

Consume aml-substrate's three unconsumed emissions — the **sanctions arc** beyond signal-watch's
Phase-34 pin (`1f5901e` → HEAD `f7fbdb0`):

- **substrate Phase 35** (`4f49e53`) — *org-name* OFAC sanctions screening: the dead
  `Organization.sanctions_flag` made LIVE under `--anchored` via a label-blind real-OFAC-SDN **entity**
  name collision (the direct sibling of what signal-watch's Phase 80 consumed for *persons*).
- **substrate Phase 36** (`1651b1e`) — exposure-via-ownership leg (capability **C17**): a corroborating
  determination leg fired when a customer's beneficial owner / controlled entity carries a
  `sanctions_flag`, walked over the existing BO `RelationshipEdge` graph.
- **substrate Phase 37** (`5b5cf32`) — geo/jurisdiction enrichment: `counterparty_country` expands
  `{US,CA}` → 22 countries with a FATF high-risk tail (an observable, no leg yet).

Three consumes + a plan + true-ups: **(1) MERGE CONSOLE** — add an **OFAC org-name collision** case
class (a synthetic org's real-frequency legal name collides with a real public-domain OFAC SDN entity
→ same latent entity [uphold the link] vs common-name false positive [reject]), scored against
substrate's non-circular `GT-<hash>` oracle — the person-class's org sibling, MEASURE-FIRST gated;
**(2) WORKBENCH §12** — consume the C17 **exposure-via-ownership leg** as a new EVIDENCE atom so a
customer with a sanctioned beneficial owner + a *distinct* ML mechanism genuinely reaches the
determination bar (the §12 breadth beat), plus render P37's richer geo observable (no leg);
**(3) OPEN-SANCTIONS DATA-FORK BRIEF** (PLAN-ONLY) — a per-source license/compliance matrix + the
non-commercial boundary + what substrate should emit (Stage-2/3 open reference data). Plus reconcile
the now-stale substrate-P35 brief, true up `cross-pillar-build-order.md`, re-pin substrate → `f7fbdb0`.

## Context (the verified delta)

- Substrate is **3 phases ahead** of our pin (we consumed Phase 34; 35/36/37 are the delta). The phase
  numbers in the two repos are independent (substrate-P34 ≠ signal-watch-P80). Both sibling HEADs were
  code-verified LIVE this session (file:line, not loaded facts): aml-substrate @`f7fbdb0`; aml-casework
  unchanged at the Phase-79 pin @`076fb8e`.
- Substrate already ships a **REAL OFAC SDN watchlist** (`data/reference/watchlist_ofac.csv`, 2,500
  primary names, US-Gov **public domain**); `data/reference/PROVENANCE.md` is explicit: *no substrate
  party IS a real designated person; the collision is coincidental-by-construction* — the
  false-positive-trap framing matches signal-watch's compliance posture exactly. The `sanctions_flag`
  is **label-blind synthetic** (`crc32` draw, `corr(flag, illicit) ≈ 0` proven).
- Substrate **CUT** the old P35-brief asks this session and retains them as honest-null artifacts: TF =
  `already-null` (no TF crime type; `{US,CA}`-only jurisdiction; high-blast gen change forbidden);
  broader-C7 = `tell-unavoidable` (at m=1 a pure magnitude screen). So those two brief asks are **dead**
  — reconcile, don't pursue.
- Substrate's emission boundary: `SCREENING_EMISSION_DETECTORS` is **C8 + C14 only**; the new C17
  exposure detector is NOT in the emitted bundle (it READS, never generates) — so signal-watch
  **COMPUTES** the exposure leg itself from the rendered `related_parties[]` + `sanctions_flag`, not from
  a bundle firing. The org-sanctions (P35) + geo (P37) overlays ride `--anchored` on the producer side;
  all three phases prove substrate default-build byte-identical.
- **The engine derives legs from capabilities via profile DATA** (`evidence_requirements.determine` →
  `present_atoms()` reads `data/workbench/evidence-requirements.json`, counts `kind=="leg"` atoms). The
  engine never sees provenance → the C17 leg is a *profile-data atom + companion-side assembly*;
  `evidence_requirements.py` stays byte-frozen, and the same-OFAC-hit double-count dedup lives in the
  consume layer where provenance exists.
- casework (`076fb8e`) is unchanged from the Phase-79 pin; it does NOT ground C17 → a sanctioned-exposure
  case may DETERMINE (signal-watch engine) but not SIGN through casework (the Lakeshore-C3 fail-closed
  class); the determination is the demo beat, the casework SIGN gap is a NAMED handoff (not a blocker).

## The three consumes + a plan

**MERGE (gated, measure-first):** the OFAC **org-name** collision is the natural next merge case class —
the org sibling of Phase-80's person class. A candidate LINK between a synthetic org and a real OFAC SDN
entity sharing a high-frequency legal name, where the latent truth is same-entity (uphold) or a
common-name false positive (reject), split non-circularly by `GT-<hash>`. **T1a is the abort gate.** Only
on a clean, two-sided, non-circular result do T2/T3 curate the basis and re-freeze `dist/merge` (the ONE
sanctioned dist touch, 3rd consecutive). The Phase-77/79 abort rule governs: emit won't reproduce /
tautological / one-sided → STOP the merge org track + a substrate org-emit-two-sidedness brief.

**WORKBENCH §12 (the exposure leg, gated T1b):** the C17 exposure-via-ownership leg is consumed
A1-PRESERVING as a new EVIDENCE atom — profile DATA in `evidence-requirements.json` + companion-side
assembly in `serve_workbench` + the same-OFAC-hit double-count dedup. Cases that newly reach the bar do
so by genuinely presenting ≥2 INDEPENDENT legs (the determination-bar regression proves it). P37's geo
observable renders (no leg). `evidence_requirements.py` byte-unchanged (the A1 guard).

**OPEN-SANCTIONS BRIEF (plan-only, always):** the open-sanctions thread is a PLAN-ONLY brief — the data
work is substrate-side. OpenSanctions is CC-BY-NC (no-ship: the demo's buy-in purpose is arguably
commercial); the public-domain / open-gov source lists are the clean ship path. No CC-BY-NC bytes enter
the repo (ship or companion) this phase.

## Scope

`scripts/curate_merge_cases.py` · `data/merge/cases.json` · `scripts/build.py` (validate_merge_cases) ·
`merge.html` · `dist/merge/**` · `tests/merge-console.test.mjs` ·
`tests/fixtures/merge-sanctions-org-oracle/**` · `data/entity-spine/**` · `scripts/resolution_scorer.py`
(the org-collision merge oracle) · `scripts/curate_workbench_cases.py` · `scripts/serve_workbench.py` ·
`data/workbench/**` (incl. `evidence-requirements.json`) · `workbench.html` · `tests/workbench.test.mjs`
(the C17 exposure leg + P37 geo) · `docs/*-PLAN-BRIEF.md` · `docs/cross-pillar-build-order.md` ·
`CLAUDE.md` (the open-sanctions brief + the substrate-P35 reconcile + docs true-up). **NO change to
`scripts/evidence_requirements.py`.**

## Approach (six tasks, measure-first gated)

- **T1 (the dual gate)** — run substrate @`f7fbdb0` `--anchored --emit-eval-oracles` + the screening
  bundles as TOOL-USE (subprocess, the curate pattern; build.py never imports it). **T1a:** distill the
  org-collision slice; assess two-sidedness (some collisions TRUE latent-entity matches [uphold] + some
  common-name false positives [reject], split non-circularly by `GT-<hash>`). **T1b:** measure the C17
  exposure cohort — does it fire non-degenerately, and (with the same-hit dedup) does ≥1 case reach the
  bar BECAUSE of the exposure leg? Commit no-substrate-replayable captures; document both gate decisions.
- **T2 (gated T1a)** — curate the `sanctions-org-collision` basis into `data/merge/cases.json`
  (validate↔curate parity; firewall held; org emails domain-masked).
- **T3 (gated T1a)** — render the org false-positive-trap framing in `merge.html`; rebuild + re-freeze
  `dist/merge`; extend `tests/merge-console.test.mjs`.
- **T4 (L; the exposure leg gated T1b)** — add the C17 leg atom to the profile
  (`evidence-requirements.json`); assemble it + the same-hit dedup in `serve_workbench`; render the §12
  sanctioned-BO-exposure beat in `workbench.html`; render P37's geo observable (no leg).
  `evidence_requirements.py` byte-unchanged; a determination-bar regression proves the rule frozen + the
  ≥2-independent-leg determinations.
- **T5 (always)** — `docs/open-sanctions-data-fork-PLAN-BRIEF.md` (per-source license matrix +
  non-commercial boundary + substrate emit asks) + reconcile the stale substrate-P35 brief +
  `cross-pillar-build-order.md` true-up + re-pin substrate `f7fbdb0` + the casework-C17-SIGN-gap note.
- **T6 (always)** — full verification: `--check all`, A1 byte-unchanged + the determination-bar
  regression, build.py firewall grep, validate↔curate parity, `uv run pytest`, the .mjs arcs, the
  honesty word-ban (incl. the new doc), CLAUDE.md true-up.

## Exit Criteria

- [ ] T1a + T1b captures committed + replay with NO substrate; both gate decisions documented; firewall holds
- [ ] (gated T1a, two-sided) the OFAC org-name collision merge basis curated; validate↔curate EXACT
      parity; `dist/merge` re-frozen; `tests/merge-console.test.mjs` updated — ELSE `dist/merge`
      BYTE-FROZEN + a substrate org-emit-two-sidedness brief (honest non-result)
- [ ] (gated T1b, non-degenerate) the C17 exposure leg lights ≥1 case to the determination bar via ≥2
      INDEPENDENT legs; the determination-bar regression proves the RULE frozen — ELSE the leg ships as a
      rendered observable + a brief (honest null; no false §12-advance claim)
- [ ] P37's geo observable renders (no leg)
- [ ] the open-sanctions data-fork PLAN-ONLY brief exists (per-source license matrix + non-commercial
      boundary + substrate emit asks); the stale substrate-P35 brief reconciled (TF/C7 cut, org-name
      done); cross-pillar-build-order trued up to substrate-P37 HEAD; the casework-C17-SIGN-gap noted;
      substrate re-pinned `f7fbdb0`
- [ ] `--check all` → the 8 non-merge dists byte-frozen + `dist/merge` re-frozen-or-untouched
- [ ] `scripts/evidence_requirements.py` BYTE-UNCHANGED (the A1 guard); build.py imports no
      spine/scorer/sibling/curate
- [ ] `uv run pytest` green; honesty governor (no catch-rate/lift/precision/recall/multiplier wording —
      sweep the new doc too); OFAC org names ship clean (17 USC §105, false-positive-trap framing);
      synthetic-substrate-anchored qualifier; badge always-on

## Constraints

- `scripts/evidence_requirements.py` BYTE-UNCHANGED (the A1 guard — the sufficiency RULE [mechanism + ≥2
  independent legs + named predicate + no unrebutted mitigation] stays byte-frozen; prevents the file-bar
  regression).
- **Evidence-advance, rule frozen** (user-positioned): the C17 leg is a new EVIDENCE atom (profile data +
  companion assembly + same-hit dedup). Cases that NEWLY reach the bar do so by genuinely presenting ≥2
  INDEPENDENT legs (prevents a silent bar-weakening dressed as §12 breadth).
- **Double-count independence** (substrate's explicit warning): the C17 exposure leg and a C14 escalation
  leg tracing to the SAME OFAC hit are NOT two independent legs (distinct only when they trace to DISTINCT
  sanctioned parties); the consume layer dedups by hit provenance before `determine`.
- build.py imports no spine/scorer/sibling/curate (prevents the companion-into-build firewall breach); the
  8 non-merge dists byte-frozen; `dist/merge` the ONE sanctioned re-freeze, gated on T1a (3rd consecutive).
- validate↔curate EXACT parity (the Phase-76 lesson); the post-disposition `oracle` block never leaks into
  pre-adjudication evidence (`assert_no_*_leak`).
- Real OFAC **org** names ship clean under 17 USC §105 (US-federal public domain — the existing exception
  explicitly covers OFAC), framed STRICTLY as the false-positive trap (the synthetic org ≠ the sanctioned
  entity; never "we caught a sanctioned party"). **No CC-BY-NC data enters the repo (ship or companion)
  this phase** — OpenSanctions is plan-only.
- Honesty governor: no catch-rate / lift / precision / recall / multiplier wording (sweep DOCS too — the
  Phase-78 doc-gap lesson); a confusion or cohort count is never a catch-rate.

## Abort

Any UNSANCTIONED ship-dist drift (the 8 non-merge dists, or `dist/merge` before its T1a gate) / a build.py
spine-scorer-sibling-curate import / a `scripts/evidence_requirements.py` change / a real OFAC org name
framed as a real sanctions catch (not the false-positive trap) / a CC-BY-NC byte entering the repo / a
confusion or cohort count presented as a catch-rate/precision/lift/recall → STOP-and-surface.
Measure-first (T1 the dual abort gate): the anchored org sanctions emit won't reproduce after bounded
attempts / the oracle is one-sided or tautological → STOP the merge org track (T2/T3 do NOT run) + a
substrate org-emit-two-sidedness brief; the C17 exposure cohort is degenerate (fires on too few /
already-determined cases) → the leg ships as a rendered observable + a brief (honest null), no false
§12-advance claim. The geo render + the open-sanctions brief + the true-ups land regardless.

## Decisions

[[decisions/phase-81-consume-sanctions-arc-all-three]] · [[decisions/phase-81-exposure-leg-evidence-advance]]

Spec `specs/phase-81-consume-substrate-sanctions-arc.md`; ledger Phase-81.

## Outcome (DELIVERED 2026-06-28 — pending the delivery-flow commit)

**Both planned consumes hit their measure-first branches → an HONEST reshape, not the planned shape.**

- **T1a (merge org two-sidedness) → reject-branch FIRED (structural).** Substrate's anchored fragment overlay
  is PERSON-ONLY (354 multi-record GT clusters, 100% person; ZERO org fragment clusters), so a flagged org can
  never have a same-org fragment → every org-name collision is between DISTINCT orgs → all-reject (10 flagged
  orgs / 3 candidates / 0 uphold), unfixable by scale/seed. The merge org track (T2/T3) did NOT run; `dist/merge`
  BYTE-FROZEN (untouched — the would-be 3rd-consecutive re-freeze never happened); routed to
  `docs/substrate-org-fragment-emit-PLAN-BRIEF.md`. No synthetic uphold fabricated.
- **T1b (C17 exposure leg) → DEGENERATE after a planning-stage measurement ERROR.** My "9 of 13 reach
  file-ready" estimate counted ≥2 related parties as a leg (a loose proxy, no MECHANISM check); the T4
  surface-map workflow's rigorous data-path read caught it; the actual engine re-measure (`determine()`
  with/without the leg) showed DELTA = 0 — the 13 sanctioned-BO cohort carries only C8/C14, no C2/C3/C5/C4
  mechanism, so a *leg* can never satisfy `mechanism + 2 legs`. Per USER OVERRIDE (AskUserQuestion, "accept both
  abort fallbacks" + a re-asked disposition) the C17 consume shipped **OBSERVABLE-ONLY**: a
  `/sanctions-c17-exposure` route + `sanctionsC17PanelHTML` panel + `data/casefile/sanctions-c17-exposure-demo.bundle.json`
  surface the exposure and the engine SHOWS the case does NOT reach the bar (the §12 discovery feed classes all
  13 as over-flag — a defensive-exposure basis, `sanctions_flag` label-blind, corr≈0 by design).
- **Always-landed:** the P37 geo render; the open-sanctions plan-brief + 2 substrate handoff briefs; the
  reconciled P35 brief; the cross-pillar-build-order true-up; `CLAUDE.md`.
- **Boundary/health:** companion-only — 8 non-merge dists byte-frozen + `dist/merge` UNTOUCHED; build.py firewall
  clean; `evidence_requirements.py` BYTE-UNCHANGED (A1); `node tests/workbench.test.mjs` 167→178; `--check all`
  9/9; `uv run pytest` 27. Escape hatches: DISCOVERY (the T1b measurement-error correction) + USER OVERRIDE
  (observable-only re-pick). 4-dim adversarial review (10 opus agents that RAN the commands): 0 must-fix · 2
  should-fix FIXED (email masking; tasks.md unchecked) · 14 praise.

Journal: [[journal/2026-06-28-phase-81-consume-sanctions-arc]].
