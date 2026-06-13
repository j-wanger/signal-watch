---
title: "Phase 49: Triage-loop embryo made demo-able — §14's continuous adjudication loop as the 5th ship artifact (triage console)"
aliases: [phase-49-triage-loop-embryo, triage-console]
category: phases
tags: [triage-loop, adjudication, lfcm, ship-artifact, synthetic-history, m9]
parents: []
created: 2026-06-12
updated: 2026-06-12
source: plan
status: active
ceremony: standard
scope: [scripts/curate_triage_scenarios.py, data/triage/**, scripts/build.py, triage.html, tests/triage-console.test.mjs, dist/triage/**, specs/phase-49-*.md, CLAUDE.md, HANDOFF.md, tests/smoke-checklist.md]
entry_criteria: "Phase 48 closed (committed 83e4218 + gate flip e53f8f0, both gates accepted 2026-06-12)."
exit_criteria: "scenarios.json committed + validated; build.py triage target in all/--check; dist/triage single-file offline full arc; harness ~50+ green; honesty greps + full regate (7 targets, zero drift)."
---

# Phase 49: Triage-loop embryo made demo-able — §14's continuous adjudication loop as the 5th ship artifact (triage console)

## Objective

Build blueprint §14's continuous adjudication loop as a demo-able FIFTH ship artifact:
`triage.html` → `dist/triage/index.html` (single self-contained offline file; the gate console
stays byte-frozen — sibling, not extension). Scenario source = NEW committed SYNTHETIC
`data/triage/scenarios.json`, deterministically curated by `scripts/curate_triage_scenarios.py`
from `data/probe-history` (AUTHORING time only — build.py never reads probe-history; rule text
embedded) + US-federal-allowlist-only corpus indicators (synthetic-novel stratum). ~16 scenarios
across the 4 §14 strata + ~4 known-disposition controls; evidence panels shared BY REFERENCE
across divergent-disposition pairs (process-inconsistency beat STRUCTURAL, build-validated);
fired-rule state universal; seeded LABELED second-rater dispositions. Arc: Queue (stratum chips)
→ Evidence → Disposition (§14 grammar incl. need-more-info naming a C/D code + the policy-gap
escape; rationale REQUIRED) → Reveal (decisions-not-correctness; second-rater replay;
process-inconsistency surfacing) → Discovery ledger (signal/data/process/policy gaps;
render-computed agreement arithmetic w/ measurement definitions; params "chosen, not measured";
JSON export; persists nothing). Badge always-on; NO LLM/fetch; NO blueprint edit.

## Scope

`scripts/curate_triage_scenarios.py` + `data/triage/**` (T1) · `scripts/build.py` triage target
+ validators (T2) · `triage.html` + `tests/triage-console.test.mjs` + `dist/triage/**` (T3, T4)
· `CLAUDE.md` (5 ship artifacts, trim toward ~200) + `HANDOFF.md` §8 + `tests/smoke-checklist.md`
(T5).

## Exit Criteria

- [x] 1. `data/triage/scenarios.json` committed: 20 scenarios (16 + 4 controls), 4 strata
  10/3/3/4, regen-twice byte-identical, US-federal-only novel stratum, the TM-104 pair shares
  P-HF-104 by reference, fired-rule state universal, 6 labeled second-rater seeds, synthetic meta flag.
- [x] 2. build.py `triage` target wired into all/--check; 4 tamper classes + 2 drift classes fail
  loud; probe-history in build.py comments ONLY (claim-shaped grep — concretized at T2 VERIFY).
- [x] 3. `triage.html` → dist/triage single-file offline with the full arc (96,686 B); badge always-on.
- [x] 4. `tests/triage-console.test.mjs` fully green — 93 assertions (gate-console precedent:
  TEMPLATE + injected stub dataset; both motion modes, XSS, keyboard guards incl. SELECT,
  reveal-locked-pre-disposition, hand-computed agreement fixture).
- [x] 5. Honesty greps green + FULL REGATE: `--check all` zero drift (7 targets incl. triage),
  derive_signals.py AND program-blueprint.md byte-untouched, all existing suites green.

All 5 verified empirically by the review gate 2026-06-12 (9/10 ACCEPT, zero HIGH) — READY FOR
COMPLETION; status flips at the delivery flow (delivery gate pending, work uncommitted).

## Gate record

Assumption gate closed 2026-06-12, all_accept: false — A1 (HIGH) demo-first ACCEPT
(instrument-first = natural follow-on, sequencing not dismissal) · A2 (HIGH) data path
DON'T-KNOW round 1 → defended (Phase-48 A4 verbatim + console-cases curation precedent + §14
purpose) → ACCEPT round 2 · A3 (HIGH, T0 weakest) authored panels believable within the ~16+4
ceiling ACCEPT (D7 mitigation; believability adjudicated by the user at the delivery gate) ·
A4 (MED) 5th SHIP artifact ACCEPT (non-ship docs/ shape surfaced and declined). Reviews:
approach 7/10 → revised (D7 panel verifier + D8 no-fake-instrumentation added); plan 7/10 →
revised → 9/10 ACCEPT. Ledger block in assumption-ledger.md.

## Notes

- Decisions D1–D8: [[phase-49-triage-loop-embryo|articles/decisions/phase-49-triage-loop-embryo.md]]
  (approved, confidence high). Spec: `specs/phase-49-triage-loop-embryo.md`.
- FROZEN: all 4 existing ship dists byte-identical; derive_signals.py; news pipeline; derived
  data + overlays; docs/program-blueprint.md + blueprint-report.html; data/probe-history/**
  (read-only curation input).
- Abort: existing dists drift → STOP and surface (never re-baseline); panels won't fit the
  ceiling → split per the T1 valve; a validator looks like it needs loosening → fix the DATA.
