---
title: "Phase 72: Consume the C14 kyc sign-path: re-pin substrate + re-vendor casework, close the §12 kyc determine→sign half"
aliases: []
category: phases
tags: [companion, cross-pillar, consume, kyc, c14, evidence-sufficiency, vendor, lfcm]
parents: []
created: 2026-06-23
updated: 2026-06-23
source: plan
status: delivered
scope: ["data/workbench/**", "vendor/aml-casework/**", "workbench.html", "scripts/serve_workbench.py", "scripts/curate_workbench_cases.py", "scripts/evidence_requirements.py", "scripts/vendor_casework.sh", "tests/workbench.test.mjs", "docs/case-workbench.md", "docs/evidence-driven-filing.md", "CLAUDE.md"]
entry_criteria: "Phase 71 DELIVERED + accepted; the kyc/C14 sign-path it deferred as sibling-rooted is now BUILT on both sibling sides (code-verified live): aml-substrate@f15c241 (Phase 26) emits C14 (KycIntegrityDetector in SCREENING_EMISSION_DETECTORS; txn-less party-leaf via Alert.party_ref; fires on elevated_obligation and source_of_funds is None); aml-casework@bf15535 (Phase 14) broadened _screen_c14_kyc_integrity() so C14 cases SIGN and fixes a stale _kyc_defect drift the vendored copy (157554b) carries. The committed evidence-requirements.json kyc_integrity profile needs mechanism_required:1, additional_legs_required:0 → C14 alone licenses a kyc determination."
exit_criteria: "kyc cases appear in the re-curated population, reach KYC-A1, and SIGN end-to-end; the existing ~107 ML-determined cases now actually SIGN (the determine→SIGN gap, scope=BOTH); the kyc determine+sign path + an ML-sign assertion are covered by workbench.test.mjs (both motion modes, XSS-escaped); substrate re-pinned 443e4a6→f15c241, casework re-vendored 157554b→bf15535 (VENDORED_AT + SUBSTRATE_HEAD bumped); --check all 8/8 ZERO dist drift; build.py imports no casework/substrate/osint_tools; uv run pytest + workbench.test.mjs + all selftests green; docs trued up; CLAUDE.md ≤~200 lines."
---

# Phase 72: Consume the C14 kyc sign-path: re-pin substrate + re-vendor casework, close the §12 kyc determine→sign half

## Objective

CONSUME the kyc/C14 sign-path Phase 71 deferred as sibling-rooted — now BUILT on both sibling
sides (code-verified live this session, not from loaded pins). Re-pin substrate `443e4a6→f15c241`
(it now emits C14), re-vendor casework `157554b→bf15535` (it now grounds + signs C14 and fixes a
stale `_kyc_defect` drift the vendored copy carries), re-curate → kyc cases appear, reach KYC-A1
(C14 ALONE licenses a kyc determination), and SIGN end-to-end. Scope=BOTH: close the kyc slice AND
verify the existing ~107 ML-determined cases now actually SIGN (the determine→SIGN gap).
Companion-only; the 8 offline dists stay byte-frozen.

## Scope

Files and modules affected:
- `scripts/curate_workbench_cases.py` — re-pin `SUBSTRATE_HEAD` 443e4a6→f15c241; re-curate; the
  curate firewall (keep C14-pure customers classifiable as kyc through the per-customer merge)
- `scripts/vendor_casework.sh` + `vendor/aml-casework/**` — re-vendor casework@bf15535
  (`VENDORED_AT` re-pinned; the vendored copy now grounds + signs C14)
- `data/workbench/**` — the re-curated v0.3 population (kyc cases present)
- `scripts/evidence_requirements.py` — the kyc_integrity profile consumed (C14 alone → KYC-A1)
- `scripts/serve_workbench.py` — the kyc determination + SIGN render path; the ML-sign verify (BOTH)
- `workbench.html` — surface kyc cases (KYC-A1 + the signed STR; reuse `boGraph` for KYC-A2 if C15)
- `tests/workbench.test.mjs` — the kyc determine+sign arc + the ML-sign assertion
- `docs/case-workbench.md`, `docs/evidence-driven-filing.md`, the coherence brief, `CLAUDE.md` — true-up

## Exit Criteria

- [ ] T1 STOP+REPORT (scratch only, nothing committed): a written measurement report — kyc-case
      count / KYC-A1 reach / kyc sign count / the existing ML sign count before+after (no-regression)
      / the merge-suppression verdict (does the per-customer merge × dual-map firewall suppress kyc
      closure?) — and the user gate passed before T2 commits anything
- [ ] substrate re-pinned (`SUBSTRATE_HEAD` 443e4a6→f15c241) + casework re-vendored (`VENDORED_AT`
      bf15535) + the population re-curated; `node tests/workbench.test.mjs` green; `--check all` 8/8
      byte-frozen; `uv run pytest` green
- [ ] kyc cases reach KYC-A1 and classify as `kyc_integrity` (NOT money_laundering) through the
      per-customer merge; the curate selftest re-derives dynamically (no hardcoded re-baseline); no
      validator loosened  *(T3 — skipped if the T1 probe shows no firewall needed)*
- [ ] `tests/workbench.test.mjs` covers the kyc determine+sign path + an ML-sign assertion (the
      determine→SIGN gap, scope=BOTH); both motion modes; XSS-escaped; companion-only (no dist drift)
- [ ] docs reflect the new pins (case-workbench / evidence-driven-filing / the coherence brief;
      `VENDORED_AT` + `SUBSTRATE_HEAD` bumped); `--check all` 8/8; build.py imports no companion
      layer; CLAUDE.md ≤~200 lines

## Constraints

- Companion-only — NOT a ship target; build.py imports no casework/substrate/osint_tools; the 8
  offline dists stay BYTE-FROZEN (`--check all` 8/8); the agent runs server-side (browser sends a
  backend NAME only — §4.5). Vendoring is DISTRIBUTION not coupling — the companion subprocesses the
  vendored CLI over the file-handoff. *Prevents: a companion edit leaking into a ship artifact / a
  sibling import into build.py.*
- Measure-first — T1 re-pins + re-vendors + re-curates in a SCRATCH dir and STOP+REPORTs the kyc /
  no-regression / merge-suppression numbers before ANYTHING commits (mirrors Phase 71's T1 shape).
  *Prevents: committing a re-pinned slice that silently regresses the existing ML signings or fails
  to close the kyc loop.*
- The per-customer merge × dual-map firewall — folding a C14 party-leaf into a customer that ALSO
  carries ML capabilities ties `crime_type` to money_laundering (C14→ML-A7 single leg) and
  suppresses the kyc determination. If suppressed, T3 keeps C14-pure customers separable — never
  pad/fabricate, never loosen a validator. *Prevents: a forced kyc close that mis-classifies a
  C14-pure customer.*
- The Phase-66 honesty guard — structured facts (ownership label/pct/direction) read from the
  BUNDLE, never the model; "N pct" not "N%"; demo-visible richness, ZERO catch-rate/precision/lift
  number (the single-signal-separable governor); the always-on "Illustrative data & outputs" badge.
  *Prevents: the model authoring an ownership fact / a detection-difficulty framing.*
- C1 / C7 / TF stay DEFERRED (NOT consumable): C1 a PRINCIPLED measured null (substrate refuses it
  as a C8/C6 double-count — will never be built), C7 screening-only (C8 carries ML-A3), TF has no
  crime_type / population / emission / verifier in ANY of the 3 pillars. *Prevents: scope-creep into
  un-built sibling detectors.*

## Checkpoints

- After T1 (the keystone): STOP+REPORT the measurements. If the merge suppresses kyc and no honest
  curate firewall recovers it → STOP-and-surface (report, do not force). If the re-vendor regresses
  the existing ML signings → STOP-and-surface (do not commit T2). If the slice yields zero kyc-pure
  customers → STOP-and-surface.
- If a live run shows a model-authored structured fact → record-source / sweep / fail-closed, never
  render the fabrication (the Phase-66 lesson).

## Assumptions

- A1 [direction, accept] the kyc-consume is the right Phase 72 over the carried alternatives (roll
  sufficiency into the triage/gate consoles; gather robustness) — the sibling halves are built; this
  is the matching adopter step (Phase-71 candidate #1 + coherence-brief step #3). If the T1 probe
  shows the consume is thin/blocked → pivot to the alternatives.
- A2 [T0 weakest, don't-know → T1 probe] the per-customer MERGE (`_merge_bundles`) × the dual-map
  firewall COLLIDE — folding a C14 party-leaf into a customer with ML caps reclassifies it
  money_laundering (C14→ML-A7 single leg) → kyc never classifies as kyc → ZERO kyc closure. T1
  MEASURES it before T2 commits. If kyc survives the merge cleanly: no firewall needed (skip T3). If
  suppressed: T3 keeps C14-pure customers separable. If zero kyc-pure customers: STOP-and-surface.
- A3 [accept] kyc determines on C14 ALONE (`additional_legs_required:0` — verified in the committed
  profile); C15/KYC-A2 not required. If the profile reads otherwise at impl: re-verify, do not force.
- A4 [accept] the re-vendor PRESERVES the existing ML signings/funnel (broadened C14 grounding is
  additive). T1 MEASURES regression. If it regresses: STOP-and-surface, do not commit T2.
- A5 [accept] boundary/honesty holds — companion-only, build.py imports none of it, 8 dists
  byte-frozen, zero precision/lift, structured facts record-sourced, illustrative badge. If false:
  STOP-and-surface.
- A6 [accept] TF stays OUT — no live path (crime_type / population / emission / verifier) in any of
  the 3 pillars. If a TF path is discovered live: it is a later phase, not this one.

## Notes

LITE phase. The planning decisions (the decision article finalized at
[[decisions/phase-72-consume-c14-kyc-sign-path]], confidence medium, source plan):

1. **Phase 72 = the kyc-consume** (re-pin substrate + re-vendor casework + re-curate) — accepted at
   the direction gate. The sibling halves are built (code-verified live).
2. **A2 (the per-customer merge × dual-map firewall collision) is a don't-know → the T1 measure-first
   probe** (STOP+REPORT before committing curate rework).
3. **Scope=BOTH** — close kyc AND verify the existing ML-determined cases now SIGN (the determine→SIGN
   gap).
4. **kyc determines on C14 ALONE** (`additional_legs_required:0`, verified in the committed profile).
5. **Companion-only boundary holds** (build.py imports nothing; 8 dists byte-frozen; the honesty
   governor — zero precision/lift, structured facts record-sourced, illustrative badge). TF out of
   scope (no live path in any pillar).

Cross-pillar reality CODE-VERIFIED at planning (the cross-pillar rule — verify the sibling's live
state, never reason from loaded pins; memory `cross-pillar-review-verify-sibling-repo`):
- **aml-substrate @f15c241** (Phase 26) — C14 `KycIntegrityDetector` is now in
  `SCREENING_EMISSION_DETECTORS`; txn-less party-leaf emit via `Alert.party_ref`; person-scoped; fires
  on `elevated_obligation and source_of_funds is None`. The Phase-71-era "C8-ONLY (C26/C14 deliberate
  non-emission)" suppression was LIFTED.
- **aml-casework @bf15535** (Phase 14) — `_screen_c14_kyc_integrity()` broadened to the full
  `elevated_obligation` predicate; tests prove C14 cases SIGN. Fixes a stale `_kyc_defect` drift the
  vendored copy (157554b) still carries (it false-blocks elevated-non-EDD subjects).
- **signal-watch @175678f** authored the coherence briefs that specified both halves. The committed
  `data/workbench/evidence-requirements.json` `kyc_integrity` profile = `mechanism_required:1,
  additional_legs_required:0` → C14 alone licenses a kyc determination.

Grounding (no wiki articles — the knowledge wiki is empty): the cross-pillar code-verify rule
(memory `cross-pillar-review-verify-sibling-repo`, `cross-pillar-consume-batch-not-thin` — a pin
re-ground with NO new detector is a no-op, but here C14 IS a newly-emitted detector so the consume
moves the slice); the Phase-66 record-sourced ownership-fact lesson; the single-signal-separable
honesty governor (demo-visible richness, never catch-rate/lift); vendoring is
distribution-not-coupling (the Phase-67 vendor pattern; `scripts/vendor_casework.sh` + `VENDORED_AT`);
the §12 `determine`/`signal_brief` mechanism (`evidence_requirements.py`); the Phase-71 finding that
the closure leg pair was C8+C15 via the per-customer merge (the firewall context for A2); the
Phase-71/70 finding that kyc was unreachable because the substrate non-emitted C14 (now lifted).

Knowledge gaps carried to impl (resolved by T1's STOP+REPORT): A2 — does the per-customer merge ×
dual-map firewall suppress kyc closure? A4 — the exact regression-free signed count after re-vendor.

Direction gate 2026-06-23 (NOT all-accept): A1 accept · A2 don't-know → T1 probe · A3/A4/A5/A6 accept.
Ledger Phase-72 block. Grounded against signal-watch HEAD 175678f / the Phase-71 workbench (342
cases, 81/342 §12-closed) / aml-substrate@f15c241 / aml-casework@bf15535.
