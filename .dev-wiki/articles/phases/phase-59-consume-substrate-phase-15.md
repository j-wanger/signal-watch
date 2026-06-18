---
title: "Phase 59 — Consume the substrate Phase 15 build into the coverage map (re-ground · re-freeze · document the exposure≠reachable-now coupling)"
type: phase
status: completed
ceremony: lite
milestone: M9
created: 2026-06-18
updated: 2026-06-18
tags: [cross-pillar, corpus-coverage, signal-coverage-map, consume, re-ground, exposure-coupling, emergence-doctrine, measure-first, sibling-briefs, non-ship]
---

# Phase 59 — Consume the substrate Phase 15 build into the coverage map

## Objective

Finish the consume that the half-edited pin started. After Phase 58 committed the corpus→substrate
coverage map (fc75dd9), **aml-substrate Phase 15 (@5875241, DELIVERED)** shipped the SUBSTRATE HALF of
Phase 58's brief — a label-blind **PartyView** (exposes D8 KYC + D12 pep) + 4 **SCREENING_DETECTORS**
(C7 BusinessActivityAnomaly · C14 KycIntegrity · C8 IncomeMismatch · C26 ScamVulnerable). The working tree
has a re-grounded `substrate-pin.json` but `coverage.json` was left un-frozen → `signal_coverage_map.py
--check` fails (a non-committable intermediate state). Re-freeze the map at the verified pin and document
the honest finding.

## The finding (measured this session)

Re-deriving from the re-grounded pin, the tier movement is:

| tier | committed (df23bba) | fresh (5875241) | Δ |
|---|---|---|---|
| reachable-now | 93 | 93 | **0** |
| needs-detector | 62 | 62 | 0 |
| needs-view-exposure | 312 | **70** | −242 |
| needs-behavior | 54 | **296** | +242 |
| out-of-reach | 2 | 2 | 0 |

**Landing the substrate detectors + views moved 0 signals into reachable-now.** Reachability is a 3-way AND
(`has_detector ∧ has_casework_assertion ∧ behavior_emergence=="emerges"`); the substrate half satisfied only
*exposure*. The 242 KYC/pep signals (D8/D12) are now `exposed:true` but the vendored emission
(CASE-P-0010361) is txn-only — no party rows — so the classifier's `modeled-inactive` branch moves them to
needs-behavior, NOT reachable-now. The 62 C7 signals keep the `needs-detector` label even though the C7
detector now exists, because they lack the casework grounding_replay assertion.

## Direction (gated 2026-06-18, all_accept: true; verification-gated)

The user chose **direction A** — re-freeze + document the coupling, **tiers unchanged** — over (C) re-tiering
with a per-signal `blocked_on` field and (B) hold-and-revert (defer the consume until both halves land). The
per-capability `basis` strings + the per-signal `data_source_class` / `behavior_confirmed:false` already carry
the real blocker; option A documents the coupling in prose rather than reshaping the classifier.

The user then chose **"verify first, then re-confirm"** — so A0/A1 were code-verified against the real sibling
source BEFORE any freeze:
- **A0 (pin ↔ substrate@5875241) — HELD.** PartyView's 16 fields match `monitor/detectors/views.py` exactly
  (the 4 label/PII fields omitted); the 4 detector classes + capabilities + signal_ids + `SCREENING_DETECTORS`
  membership match; D8/D12 exposed via PartyView.
- **A1 (the tiering is intended classifier semantics, not a pin-edit bug) — HELD.** `classify()` (lines
  146-161): 242→needs-behavior via `modeled-inactive` (exposed:true, emission_probe:null); 62-C7→needs-detector
  via the `emerges` branch (has_detector:true but not `is_live`). Deliberate multi-way AND.

The user re-confirmed proceed. Grounded against **aml-substrate@5875241 + aml-casework@4ac9523 +
signal-watch-corpus@472b44e**.

## Approach (single-beat, signal-watch-local, LITE)

- **T1** code-verifies the re-grounded pin against the real sibling HEAD (the re-ground-before-commit rule),
  confirms the classifier movement is intended, then `--freeze`s coverage.json. `--check` byte-identical,
  `--selftest` green, no sibling import.
- **T2** documents the measured movement + the 3-way-AND finding + the stale-label/composite-needs-behavior
  caveat in `docs/corpus-substrate-coverage.md` + the integration contract §8; HEADs re-pinned inline.
- **T3** re-grounds both sibling briefs: the substrate detector/view half is DONE (mark it) → the remaining
  substrate increment is a PARTY-BEARING emission bundle (so the 242 become map-measurable); the casework brief
  re-grounds to @4ac9523 → the 4 paired grounding_replay assertions (C7/C8/C14/C26) still needed. Shared
  acceptance: reachable-now rises only when BOTH halves land. Doctrine constraint: detectors +
  observable-exposure ONLY, never behavior/label stamping.

## Scope

- `data/coverage-map/**` (the re-grounded pin + the re-frozen coverage.json) · `scripts/signal_coverage_map.py`
  (read-only verify; the classifier is unchanged) · `tests/` (the existing `--selftest` re-run) ·
  `docs/corpus-substrate-coverage.md` · `docs/pillar-integration-contract.md` (§8) ·
  `aml-substrate/docs/corpus-coverage-build-PLAN-BRIEF.md` + `aml-casework/docs/capability-assertions-PLAN-BRIEF.md`
  (sibling, re-grounded — authored here, executed in sibling sessions)
- NOT touched: the 8 build targets / offline dists; the committed corpus records + overlays (read-only);
  `build.py` never imports `signal_coverage_map.py`; no sibling import.

## Exit criteria

1. `substrate-pin.json` verified faithful to @5875241 (HEAD in the regrounding_note); `signal_coverage_map.py
   --check` byte-identical (re-frozen) + `--selftest` green; `! grep import aml_substrate|aml_casework`;
   build.py never imports it; `--check all` 8/8.
2. `docs/corpus-substrate-coverage.md` + contract §8 carry the measured movement (312→70, 54→296,
   reachable-now 93) + the 3-way-AND finding + the composite-tier caveat; HEADs re-pinned
   (substrate@5875241, casework@4ac9523, corpus@472b44e).
3. Both sibling briefs re-grounded (substrate detector/view half DONE → party-bearing emission next; casework
   → the 4 paired assertions; shared acceptance + doctrine constraint).
4. `--check all` 8/8 (the 8 ship dists byte-identical); the change set contains ZERO ship artifacts.

## Delivery gate (the reachable-now rise — GATED on the siblings)

reachable-now rises above 93 only when BOTH sibling halves land: a party-bearing emission bundle
(aml-substrate) so the 242 KYC/pep observables become map-measurable, AND the 4 paired grounding_replay
assertions C7/C8/C14/C26 (aml-casework). Both are sibling-rooted (the briefs hand them off); single-beat here.

## Assumptions (ledger: Phase-59 block, all_accept: true; verification-gated)

- **A0 [HIGH, T0 weakest]** The uncommitted pin faithfully matches substrate@5875241. ACCEPT (VERIFIED before
  freeze). If false → freeze a map grounded on a wrong pin.
- **A1 [HIGH]** The 242→needs-behavior / 62-C7→needs-detector tiering is intended classifier semantics, not a
  pin-edit bug. ACCEPT (VERIFIED). If false → keeping tiers + prose bakes in a wrong number.
- **A2 [HIGH]** reachable-now genuinely can't move on the substrate half alone (the 3-way AND). ACCEPT (held by
  evidence across 3 repos).
- **A3 [MED]** NON-ship — re-freezing coverage.json touches no ship dist; --check all stays 8/8. ACCEPT.

## Abort

Any of the 8 offline dists drift, or a ship artifact is touched → STOP and surface (never re-baseline). A brief
that stamps behavior or labels → out of bounds (the emergence doctrine, A0/A1's abort-line). The companion
importing sibling code → out of bounds (vendored-pin / file-contract only). A validator/selftest looks like it
needs loosening → fix the data/design, never the check. Grounding HEADs: aml-substrate@5875241 ·
aml-casework@4ac9523 · corpus@472b44e (re-grounded this phase).
