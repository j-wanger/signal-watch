---
title: "Phase 59 — Consume the substrate Phase 15 build into the coverage map"
type: journal
date: 2026-06-18
phase: 59
tags: [cross-pillar, coverage-map, consume, re-ground, exposure-coupling, emergence-doctrine, measure-first, non-ship]
---

# Phase 59 — Consume the substrate Phase 15 build into the coverage map

## What happened

`/dev-plan continue` landed on a working tree with an uncommitted `data/coverage-map/substrate-pin.json`
and a failing `signal_coverage_map.py --check`. Investigation across the three repos showed the cause: a
**half-finished consume of a sibling landing**. After Phase 58 committed the coverage map (fc75dd9),
**aml-substrate Phase 15 (@5875241, DELIVERED)** shipped the *substrate half* of Phase 58's brief — a
label-blind `PartyView` (exposes D8 KYC + D12 pep) + 4 `SCREENING_DETECTORS` (C7/C14/C8/C26). The pin was
re-grounded to reflect it, but `coverage.json` was deliberately left un-frozen ("pin drifts ahead… until
both halves land") — a non-committable intermediate state.

Phase 59 finished the consume: re-froze the map at the verified pin and documented the honest finding.

## The finding

**Landing the substrate detectors + views moved 0 signals into reachable-now.** Reachability is a 3-way
AND (`has_detector ∧ has_casework_assertion ∧ behavior_emergence=="emerges"`); the substrate half
satisfied only *exposure*. Measured (corpus@472b44e × substrate@5875241 × casework@4ac9523):

| tier | df23bba | 5875241 | Δ |
|---|---:|---:|---:|
| reachable-now | 93 | 93 | **0** |
| needs-view-exposure | 312 | 70 | −242 |
| needs-behavior | 54 | 296 | +242 |

The 242 D8/D12 signals left needs-view-exposure (the PartyView exposes them) but landed in needs-behavior,
not reachable-now — because the **still-vendored emission `CASE-P-0010361` is txn-only** (no party rows →
the classifier's `modeled-inactive` branch can't measure KYC active). The 62 C7 keep `needs-detector` even
though the C7 detector exists, because they lack the casework assertion. So the tier NAMES went composite:
needs-behavior=296 = ~242 exposed-but-unmeasurable (an emission-sample limit) + ~54 genuine emergence gaps;
needs-detector=62 = detector-exists-blocked-on-the-assertion.

## Decisions

- **Direction A** (re-freeze + document the coupling in prose, tiers unchanged) over (C) re-tiering with a
  per-signal `blocked_on` field and (B) hold-and-revert. The per-signal `data_source_class` +
  `behavior_confirmed:false` already carry the real blocker; A documents the coupling without reshaping the
  classifier (minimal, honest-enough for a LITE non-ship artifact).
- **"Verify first, then re-confirm"** — A0 (pin ↔ substrate@5875241) + A1 (the tiering is intended
  classifier semantics, not a pin-edit bug) were code-verified against the real sibling source BEFORE any
  freeze; both HELD; the user re-confirmed proceed.

## Problems / solutions

- **`--selftest` failed after the re-freeze** — 2 assertions (L324 `D8 → generated-unexposed`, L350 `C13/D8
  → needs-view-exposure`) encoded the pre-PartyView df23bba reality. This is the abort-rule's
  "validator-needs-changing" trigger, so I stopped and read the test rather than papering over it. Verdict:
  **re-grounding stale golden snapshots to the verified new reality, not loosening** — the structural
  integrity tests (the D17 tamper test, determinism, closed-set sweep) are untouched and still pass; the
  two snapshots simply pin the exact Phase-15 movement now (D8 → `modeled-inactive`; C13/D8 →
  `needs-behavior`). Corrected both; surfaced the change explicitly in the delivery report.

## Health Delta

No test count change (the coverage-map `--selftest` is the same suite; 2 golden values re-grounded).
`--check all` 8/8 zero drift; coverage map `--check` byte-identical + `--selftest` green. No sibling import;
build.py never imports the script. ZERO ship artifacts in the change set.

## Gate Compliance

Direction gate: approved (assumption positions taken; A0/A1 verify-first → verified HELD → re-confirmed;
A2/A3 held by evidence; no unresolved reject/don't-know). Delivery gate: accepted (the user's "continue").
Ledger Phase-59 revisit-status filled (A0 HELD verified-clean-before-freeze · A1 HELD · A2 HELD · A3 HELD).

## Soft Observations / Phase N+1 Candidates

- **Phase 60 candidate — consume the reachable-now rise (gated on both sibling halves).** reachable-now
  moves above 93 only when (1) aml-substrate emits a *party-bearing* evidence bundle (`--emit-evidence`
  carrying PartyView rows) + re-vendor it, AND (2) aml-casework registers the 4 paired `grounding_replay`
  assertions C7/C8/C14/C26. Both are sibling-rooted (the re-grounded §5 briefs hand them off). C7 is the
  cleanest first win (transaction-grounded → no party bundle needed; +62 once its assertion lands). When
  either lands, re-ground the pin + re-run `--check` — the count finally climbs. Evidence:
  `docs/corpus-substrate-coverage.md` §3a + the two sibling briefs.
- **The tier-model overloading will recur.** Direction A's prose-caveat works for one partial landing; if
  more partial sibling landings accumulate, the composite tier names (needs-detector/needs-behavior) get
  harder to read honestly. Option C (a per-signal `blocked_on` field: detector/assertion/exposure/
  emission-sample/behavior) becomes the cleaner representation IF the map is ever presented or used to
  drive cross-pillar sequencing. Deferred — not earned yet for a non-ship measure artifact.
- **The party-bearing-emission increment is small + measure-only** (extend `--emit-evidence` to carry the
  PartyView rows). It converts the 242 from "exposed-but-unmeasurable" to map-measurable without any
  emergence-engine work — a high-leverage, low-cost substrate increment.
