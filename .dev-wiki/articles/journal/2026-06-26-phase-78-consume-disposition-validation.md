---
type: journal
date: 2026-06-26
slug: phase-78-consume-disposition-validation
phase: 78
tags: [cross-pillar, consume, substrate, determination-validation, circularity-exit, discovery-feed, measure-first, adversarial-review]
---

# Phase 78 — Consume the disposition oracle: the determination-validation harness + the §12 discovery feed

## What shipped
Consumed aml-substrate Phase 31's now-CLI-wired `--emit-eval-oracles` (substrate `f2da3e4`→`9677a37`) — the exact handoff Phase-77 A2 deferred to. Built the **determination-validation harness** (`scripts/determination_validation_harness.py`, the "circularity exit") + the **§12 discovery-feed control** in `serve_workbench`. Companion-only — `evidence_requirements.py` BYTE-UNCHANGED (A1), all 9 dists byte-frozen, build.py imports nothing new.

- **T1** boundary capture (`--freeze --emit-dir`): joins substrate's exogenous `intended_disposition` oracle ↔ screening+monitoring bundles by `case_id`, merges caps per customer → committed `tests/fixtures/determination-validation/capture.json` (6935 cases, seed 0).
- **T2** the `--check` measure-first gate: re-runs the engine per case on the BUNDLE-ONLY structure (mechanism + ≥legs, human-gate inputs held out) vs the oracle → a per-class confusion structure vs `baseline.json`. **Gate PASSED non-degenerate.**
- **T3** the §12 discovery feed: a read-only `/discovery` route + workbench panel surfacing the *missed* / *over-flag* disagreement cells (each annotated by the engine's own `missing[]`); oracle presentation-only.
- **T4** doc + true-up + pytest registration (24→26).

## The result (the strategic payoff)
The exogenous oracle (authored blind to the sufficiency rule) revealed a real engine weakness it didn't know about itself — a genuine measurement, unlike the Phase-77 merge-66 circular oracle:
- ML signals discriminate (file-ready on 50 of 121 oracle-file vs 593 of 6087 oracle-clear) but **miss 71 of 121** file cases — the §12 signal gap.
- The **KYC bar is a pure structural over-flag**: all 727 C14-pure cases are oracle-clear, yet all 727 score file-ready (a source-of-funds gap alone is not laundering; `additional_legs_required=0`).

## Key decisions
- [[decisions/phase-78-bundle-only-non-circular-validation]] — score the bundle-only signal structure (mechanism + ≥legs), hold out the human gate, never derive it from the oracle basis. The non-circular frame.
- [[decisions/phase-78-measure-then-control-discovery-feed]] — pivot the measurement into the §12 discovery feed (the measuring→controlling pivot); firewall keeps the oracle presentation-only.

## Method notes
- An **Understand workflow** (3 parallel readers) mapped the substrate bundle/oracle shape + the engine's mechanism-vs-leg recipe + the patterns to mirror, BEFORE writing — surfaced the load-bearing finding that the oracle keys to the SCREENING slice (merge monitoring for the mechanism caps).
- The 40k substrate emit pre-warmed in the background while the harness was written.

### Review Gate (STANDARD — adversarial, 4 dims → 14 agents)
**0 must-fix · 3 confirmed → all fixed · 3 refuted · 10 praise.** Confirmed + fixed:
1. The deliverable doc presented banned rate/%/lift tokens while the honesty governor only swept JSON/HTML → rewrote counts-only + extended `_assert_doc_clean` to sweep the doc; reworded disclaimers to "no rate/score/multiplier" (the bare words trip the regex — recurring).
2. The degenerate criterion pooled rates across crime_types (Simpson's-paradox, could falsely report non-degenerate) → per-crime-type with `n>0` guards + a selftest.
3. `--freeze` wrote before the honesty assert → assert-first.
Refuted/leave-as-is: the inert `/discovery except RunError` (consistent route pattern), the 2MB capture provenance (auditable). Praise confirmed: firewall airtight, oracle genuinely independent ("a real circularity exit, not a repeat of merge-66"), A1/boundary/determinism hold.

### Gate Compliance
Direction gate `approved` (all-accept, A1 accept-as-falsifiable = the T2 gate, which passed). Delivery gate accepted by the user 2026-06-26.

## Verification
`--check all` 9/9 byte-frozen · build.py imports no harness/serve_workbench/substrate · `evidence_requirements.py` byte-unchanged · `determination_validation_harness.py --check` PASS · `serve_workbench --selftest` PASS · `node tests/workbench.test.mjs` 169 · `uv run pytest` 26.

## Soft Observations / Phase 79 candidates
- The §12 discovery-feed PANEL was verified by test assertions but NOT opened live in a browser — a visual pass is the one unverified surface.
- The honesty governor now sweeps `docs/determination-validation.md`; the spec / decision-articles / cross-pillar-build-order still carry "no catch-rate/lift" disclaimer words (planning-internal, ungated). A future generalization could sweep all phase docs — but it over-reaches on disclaimer prose; left scoped to the deliverable.
- The deferred consumes are now the frontier: **merge real-66** needs `entity_ref ≠ cluster` (the open-data fork — `docs/substrate-open-reference-data-fork-PLAN-BRIEF.md`); **Lakeshore `cleared` co-sign** needs casework C3 fan-in (`docs/casework-c3-fan-in-PLAN-BRIEF.md`). Both sibling-rooted.
- The KYC structural-over-flag finding is itself a §12 signal: the kyc sufficiency rule (`additional_legs_required=0`) may warrant a corroborating-leg requirement — a determination-engine design question for a future phase.
