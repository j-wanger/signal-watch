---
title: "Phase 72: Consume the C14 kyc sign-path — re-pin substrate + re-vendor casework, close the §12 kyc determine→sign half"
aliases: []
category: journal
tags: [companion, cross-pillar, consume, kyc, c14, evidence-sufficiency, vendor, lfcm]
parents: [phase-72-consume-c14-kyc-sign-path]
created: 2026-06-23
updated: 2026-06-23
source: debrief
duration: ~half-day (single session, post-compaction estimate)
---

# Phase 72: Consume the C14 kyc sign-path — re-pin substrate + re-vendor casework, close the §12 kyc determine→sign half

## What Happened
- CONSUMED the kyc/C14 sign-path Phase 71 deferred as sibling-rooted. The two sibling halves were already built — substrate Phase-26 C14 emission, casework Phase-14 C14 grounding — so this phase was the matching adopter step: re-pin substrate `443e4a6→f15c241`, re-vendor casework `157554b→bf15535`, re-curate `342→355`.
- **The T1 measure-first PROBE was the keystone** (scratch emit at substrate@f15c241; STOP+REPORT). It RESOLVED the weakest assumption A2 and surfaced the honest frontier:
  - **A2 RESOLVED — the merge does NOT suppress kyc.** 727 C14-PURE customers classify `kyc_integrity` and ALL determine from KYC-A1 (C14 alone, `additional_legs_required:0`). 926 C14-MIXED customers fold into money_laundering — and that is CORRECT, not a firewall need: a customer with ML signals AND a source-of-funds gap IS money_laundering (C14 lights ML-A7, the SoF leg corroborating the ML case). The dual-map is honest.
  - **A4 CLEAN** — the re-vendor preserves the existing ML signings (0 regressions).
  - The honest FRONTIER surfaced: **kyc SIGNING.** Txn-bearing C14 cases SIGN through the re-vendored casework; purely txn-less C14 party-leaf bundles fail-CLOSED at casework's foundational no-transactions contract (the bundle has no transactions, refused at casework's first scaffold 08b06df — BEFORE the C14 verifier even runs). Surfaced via an honest `e2e_note`, never loosened.
- **T3 was a measured NO-OP.** The planned curate firewall was unnecessary — T1 proved the dual-map is correct. Forcing C14-mixed cases to kyc would be dishonest; no firewall added, no validator loosened.
- **T2 committed the pins** and fixed a re-curate-exposed demo coupling: the gather/finale demo now resolves its case from the OSINT corpus (`serve_workbench.gather_demo_case_id`) rather than the volatile mule exemplar — a re-curate reshuffles the slice and moves the exemplar off the corpus-tailored subject. Also applied to `tests/gather_quality_harness.py`. The casework pin in `cases.json` is now READ from `vendor/aml-casework/VENDORED_AT` (`curate._casework_pin`), not hardcoded — the Phase-71 stale-pin lesson.
- **T4** added the §12 KYC closure selftest assertion + made the determination verdict text crime-type-HONEST (a kyc determination states its own sufficiency basis — the KYC-integrity mechanism + a named risk — not the ML legs/mitigation checklist it doesn't require) + surfaced the honest `e2e_note` for the won't-sign frontier. `workbench.test.mjs` 124→127.

## Decisions Made
- **Phase 72 = the C14 kyc consume** (direction-gated): the two sibling halves were already built; signal-watch consumed them (re-pin f15c241, re-vendor bf15535, re-curate 342→355).
- **The dual-map is CORRECT, not a firewall.** A C14-mixed customer (ML signals + SoF gap) IS money_laundering; only C14-PURE customers (727) classify `kyc_integrity`. The planned T3 firewall was a measured NO-OP.
- **kyc SIGNING is the honest cross-pillar FRONTIER.** Txn-bearing C14 cases sign; purely txn-less party-leaf bundles fail-CLOSED at casework's no-transactions contract — surfaced via `e2e_note`, never loosened. A named casework follow-on.
- **Resolve the gather/finale demo case from the OSINT corpus** (`gather_demo_case_id`), not the volatile mule exemplar (re-curate-robust).
- **The casework pin in cases.json is READ from VENDORED_AT** (`curate._casework_pin`), not hardcoded — the Phase-71 stale-pin lesson.
- **The determination verdict text is crime-type-HONEST** — a kyc determination states its own sufficiency basis, not the ML legs it doesn't require.
- (Lite ceremony — no decision articles; positions captured in the ledger Phase-72 block + the _CURRENT_STATE decisions table.)

## Problems Solved
- A2 (would the per-customer merge × dual-map firewall suppress kyc closure?) — resolved by the T1 probe: 727 C14-pure customers close kyc cleanly; the merge does not suppress it; the firewall was a NO-OP.
- The re-curate-exposed demo coupling (the gather/finale demo + gather_quality_harness pinned to the volatile mule exemplar) — fixed by the `gather_demo_case_id` corpus resolver (a DISCOVERY during T2).
- The won't-sign txn-less kyc cases — surfaced honestly via an `e2e_note` ("casework refused at the contract boundary: bundle: no transactions") rather than loosening casework's contract.

## Open Questions
- The casework txn-less-contract follow-on (a sibling casework phase): make the 651 txn-less kyc cases signable — relax casework's no-transactions contract for a `kyc_integrity` filing, or drop `transaction_details` from the kyc STR profile.

## Artifacts Changed
- `scripts/curate_workbench_cases.py` (re-pin `SUBSTRATE_HEAD` 443e4a6→f15c241; `_casework_pin` reads VENDORED_AT; re-curate 342→355)
- `scripts/vendor_casework.sh`, `vendor/aml-casework/**`, `vendor/aml-casework/VENDORED_AT` (re-vendor 157554b→bf15535 — now grounds + signs C14)
- `data/workbench/**` (re-curated population: 342→355 cases, coverage 107/342→128/355, funnel 183/110/62; the won't-sign kyc cases carry an honest `e2e_note`)
- `scripts/serve_workbench.py` (the §12 KYC closure path; `gather_demo_case_id` corpus resolver; `_measure_grounding` honest contract-rejection note)
- `scripts/evidence_requirements.py` (the `kyc_integrity` profile consumed; crime-type-honest determination verdict)
- `workbench.html` (surfaces kyc cases + the honest `e2e_note` for the won't-sign frontier)
- `tests/workbench.test.mjs` (124→127, +3 kyc tests), `tests/gather_quality_harness.py` (corpus-resolver-robust)
- `docs/case-workbench.md`, `docs/evidence-driven-filing.md`, the coherence brief, `tests/smoke-checklist.md`, `CLAUDE.md` (Current-state, replace-in-place)

## Related
- [[phases/phase-72-consume-c14-kyc-sign-path|Phase 72]] — parent phase
- [[phases/phase-71-substrate-v03-slice-determination-loop|Phase 71]] — deferred this kyc/C14 path as sibling-rooted; Phase 72 consumes it

## Health Delta
- `node tests/workbench.test.mjs` 124→127 (+3 kyc tests); `uv run pytest` 20 (unchanged); `serve_workbench`/`curate`/`evidence_requirements`/`gather_quality_harness` selftests green; the 4 other arc suites unchanged (corpus, gate 68, triage 93, news 150).
- `build.py --check all` 8/8 ZERO dist drift; build.py imports no companion/sibling layer (grep clean); honesty greps clean.
- Re-curated slice: 342→355 cases, coverage 107/342→128/355, funnel 183/110/62. **727 C14-pure customers determine kyc from KYC-A1; ML signings 126/349, 0 regressions.**
- All COMPANION-ONLY — the 8 ship dists stay byte-frozen; vendoring stayed distribution-not-coupling.

## Soft Observations / Phase N+1 Candidates
- The casework txn-less-contract follow-on → make the 651 txn-less C14 party-leaf cases signable (relax casework's no-transactions contract for a `kyc_integrity` filing, or drop `transaction_details` from the kyc STR profile). Sibling (casework) phase. | Evidence: `data/workbench/cases.json` (4 of 6 kyc cases carry `e2e_note` "casework refused at the contract boundary: bundle: no transactions").
- Roll the determination/sufficiency model into the triage + gate consoles (still disposition-only) — carried from Phase 69/70. | Evidence: `docs/case-workbench.md`.
- C1/C7/TF stay sibling-rooted — C1 a PRINCIPLED measured null (won't be built), C7 screening-only, TF no live path in any pillar. | Evidence: the §12 brief STATUS header.
- A kyc OSINT subject / exemplar — the 6 kyc cases sit in the queue but aren't a tagged exemplar; if kyc becomes a headline demo beat, add a kyc-specific OSINT corpus subject + a kyc exemplar (deferred as polish per the scale-over-showcase preference). | Evidence: `data/osint/corpus.json`.
