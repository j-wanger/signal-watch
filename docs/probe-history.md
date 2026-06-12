# Phase-48 History-Decomposition Probe — SYNTHETIC

> **Everything in `data/probe-history/` is SYNTHETIC** — an invented institution (Northbridge
> Bank), invented rules, entities, analysts, dates, and dispositions. No real customer,
> transaction, alert, or institutional data exists anywhere in this probe (non-negotiable #4).
> The probe's outputs sit OUTSIDE every `build.py`-read path: nothing here enters
> `__CORPUS__` or any ship artifact.

## What the probe demonstrates

The program blueprint's history section (§12, Role 1) claims an institution's legacy TM
rulebook can be **decomposed through the same inverted extraction boundary the corpus proved**
— agent extracts, deterministic gate disposes, coverage derives mechanically. This probe runs
that claim end to end on synthetic material:

1. A 12-rule synthetic legacy rulebook (`data/probe-history/legacy-rulebook.md`) was authored
   **advisory-shaped** and derived through the **UNCHANGED** frozen gate: the agent proposed
   each rule's verbatim indicator quote + C/D codes + a `red_flag` translation; the committed
   `derive_signals.check_record` disposed (quote-grounding under `normalize()` inside
   `rf_region`, the cover×data matrix, the `red_flag` shape check). Zero edits to
   `derive_signals.py` (`git diff --quiet` held throughout); the rulebook anchors under the
   existing Tier-1 `_RF_HEADER` form. Result: **12/12 gate-green, zero violations**, coverage
   derived deterministically from the committed Phase-28 interview posture via the ph33_apply
   downstream (no neural coverage authoring).
2. A synthetic 44-alert disposition history (`alert-history.json`) was aggregated by
   `scripts/probe_history_stats.py` (stdlib-only) into the Role-2/Role-3 measurement shapes —
   every number carrying its `definition:` line.

## The shape caveat (read before citing this probe)

The synthetic rulebook was **authored advisory-shaped** — its indicator section sits under a
heading the existing `rf_region` anchors already recognize, and each rule carries an
enumerated, self-contained indicator sentence. The shape was free because the material is
synthetic. Therefore the probe demonstrates **"a legacy rulebook CAN be a derivation surface
through the unchanged gate"** — it does NOT demonstrate that any real institution's rulebook
parses unchanged. Real rulebooks (vendor rule exports, parameter tables, SQL) may need the
regression-gated anchor-extension path (every existing md's region byte-unchanged,
`--selftest` fixtures pinning each anchor) or a deterministic pre-shaping step. That is the
same honesty class as the news pipeline's fixture discipline: the mechanism is proven, the
input-shape generality is not claimed.

## Measured results (regenerate: `python3 scripts/probe_history_stats.py`)

All numbers below are over SYNTHETIC fixture material; each metric's definition is emitted by
the script beside the number and is the only authority on what the number means.

- `rules_decomposed: 12` of 12 authored — gate-green through the unchanged gate.
- `coverage_map: BUILD_NOW 1 · COVERED 8 · ENHANCE 3` — the decomposition's honest output: the
  modern capability posture already subsumes most of this (synthetic) legacy rulebook, with
  one buildable gap (TM-110, originator-info screening C10) and three enhancement candidates.
- `capability_spread: 9 distinct C-codes, 5 distinct D-codes; 19 C-codes with no legacy rule` —
  the rulebook-vs-taxonomy coverage statement (about the rulebook, never about risk).
- `alerts_total: 44` (dismissed 28 · escalated 10 · sar_filed 2 · data_requested 4).
- `re_review_rate: 12/44 = 27.3%` — the already-reviewed-and-discounted class (the wiki's
  documented real-world analogue ran ~70% at one institution; the synthetic figure is a
  fixture property, not a claim).
- `disposition_inconsistency_rate: 4/6 = 66.7%` (TM-102, TM-104, TM-108, TM-110) — the
  process-inconsistency discovery class, surfaced for adjudication, never auto-resolved.
- `data_gap_rate: 4/44 = 9.1%` — the need-more-information class the §14 loop wires into the
  C/D coverage model.
- `alert_to_escalation_rate: 12/44 = 27.3%` — the §6 A/B baseline shape: what a candidate
  signal must beat on the same (synthetic) population.
- `silent_rules: 1/12` (TM-111) — a silent rule is itself a finding at adoption.

## What this probe is NOT

- NOT a performance claim: every figure is a property of authored fixtures, useful only as the
  mechanical demonstration that the measurement definitions compute.
- NOT a calibration: dispositions here are invented; at adoption, real dispositions are
  evidence about *decisions*, never ground truth about correctness (blueprint §12 doctrine).
- NOT a ship artifact: nothing in `data/probe-history/` is read by `build.py`, merged into any
  demo, or carried into the corpus counts.
