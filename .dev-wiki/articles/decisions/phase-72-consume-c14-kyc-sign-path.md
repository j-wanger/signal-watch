---
title: "Phase 72 — Consume the C14 kyc sign-path (re-pin substrate, re-vendor casework, close the §12 kyc determine→sign half)"
status: active
confidence: medium
source: plan
created: 2026-06-23
tags: [cross-pillar, consume, kyc, c14, evidence-sufficiency, workbench, substrate, casework]
---

## Context

Phase 71 closed the §12 ML determination loop from real signals (81/342 reach the ≥2-leg ML bar)
but DEFERRED kyc — the substrate deliberately non-emitted C14. Cross-pillar review this session
(code-verified live, not from loaded pins per [[memory:cross-pillar-review-verify-sibling-repo]])
found the deferred half is now BUILT on both sibling sides:

- **aml-substrate@f15c241** (Phase 26): C14 `KycIntegrityDetector` flipped into
  `SCREENING_EMISSION_DETECTORS`; txn-less party-leaf emit via `Alert.party_ref`; person-scoped;
  fires on `elevated_obligation and source_of_funds is None`. The "C8-ONLY" marker was lifted.
- **aml-casework@bf15535** (Phase 14): `_screen_c14_kyc_integrity()` broadened to the full
  `elevated_obligation` predicate; tests prove C14 cases SIGN. Fixes a stale `_kyc_defect` drift
  the vendored copy (157554b) still carries. 295 tests green.

The committed `data/workbench/evidence-requirements.json` `kyc_integrity` profile needs
`mechanism_required:1, additional_legs_required:0` — **C14 alone licenses a kyc determination**.

## Decision

Phase 72 = the matching CONSUME phase. Re-pin substrate `443e4a6→f15c241` (curate),
re-vendor casework `157554b→bf15535` (vendor_casework.sh), re-curate → kyc cases appear,
reach KYC-A1, and SIGN end-to-end. Measure-first keystone (T1 STOP+REPORT) before committing.

## Load-bearing assumptions (gate)

- **A1 (direction):** the kyc-consume is the right Phase 72, over the carried alternatives
  (roll sufficiency into the triage/gate consoles; gather robustness). The sibling halves are done.
- **A2 (weakest — T1 probe target):** the per-customer MERGE (`_merge_bundles`) × the dual-map
  firewall COLLIDE — folding a C14 party-leaf into a customer with ML caps reclassifies it as
  money_laundering (C14→ML-A7, single leg) and suppresses the kyc determination. A curate firewall
  (keep C14-pure customers separable) is likely REQUIRED. Measure, don't assume.
- **A3:** kyc determines on C14 ALONE (`additional_legs_required:0` — verified in the committed
  profile); C15/KYC-A2 not required.
- **A4:** the re-vendor preserves the existing ML signings/funnel (broadened C14 grounding is
  additive); T1 measures regression.
- **A5:** boundary/honesty holds — companion-only, build.py imports none of it, 8 dists byte-frozen,
  zero precision/lift, structured facts record-sourced, illustrative badge.
- **A6:** TF stays OUT — no live path in any of the 3 pillars.

## What stays deferred (NOT consumable now)

C1 (principled measured null — substrate refuses it as a C8/C6 double-count; will never be built),
C7 (screening-only/deferred), TF (no crime_type / population / emission / verifier in any pillar).
