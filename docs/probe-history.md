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

## Phase 62 — the GROUNDED consume (substrate P22)

The §12 Role-2 stats above ran over the SYNTHETIC Phase-48 fixture. Phase 62 re-points the same
measurement at a **grounded** probe-history projected by the aml-substrate P22 loop-closure
projector — `data/probe-history/grounded/alert-history.json` (pin + reproduce command in
`grounded/provenance.json`: `aml-substrate@ae98924`, `--clients 1000 --months 10 --seed 42
--probe-history`, byte-deterministic). Run it with `python3 scripts/probe_history_stats.py
--grounded`; the synthetic default path is byte-unchanged (regression baseline).

**The honesty split (the load-bearing point).** The grounded history's alert FIRINGS are REAL
label-blind detector output — which entity (substrate `account_id`), which capability (`rule_id`
is a substrate C-code), the count, the near-misses. But the DISPOSITIONS are ILLUSTRATIVE: the
substrate's chosen-not-measured §7 operating-funnel shape, seeded from observable alert content,
never the hidden label. So:
- **Firing-derived metrics are GROUNDED:** `alerts_total` (4,966 over C2/C3/C5/C15),
  `silent_rules`, `below_the_line_count`.
- **Disposition-derived metrics measure the ILLUSTRATIVE process, not analyst behaviour:**
  `re_review_rate` (72.6%), `disposition_inconsistency_rate` (100% — a structural artefact of
  the illustrative seed's spread over many alerts/capability, surfaced not hidden), `data_gap_rate`
  (3.8%), `alert_to_escalation_rate` (2.5%). Each grounded line is tagged `[over illustrative
  dispositions]`. This is NOT a claim about real re-review or escalation rates.

**The namespace seam (`capability-tm-map.json`).** The grounded history speaks capability
C-codes; the §12 `silent_rules` metric (and the §14 console) speak legacy `TM-###` ids. The
committed `data/probe-history/capability-tm-map.json` maps each substrate per-account capability
to the legacy TM rule(s) that express it, validated by `--selftest` (closed vocab + inversion
faithfulness vs the rulebook + taxonomy). One **honest null**: C15 (shell/nominee) fires but the
legacy rulebook authored no rule for it — the substrate capability is *ahead* of the rulebook.

**Grounded `silent_rules` becomes CAPABILITY-level silence** (the substrate detects per-capability,
not per-rule-variant): 8/12 legacy rules are silent — **4 have a substrate detector that did not
fire** at this build (C4, C6) and **4 have no substrate detector at all** (C1/C10/C19/C20, the
un-built capabilities). That split is the genuinely useful §12 measurement: it separates "dead at
this scale" from "never buildable here."

`below_the_line_count: 0` at this build is a measured 0 (the near-miss sampler found no qualifying
accounts at seed42-n1000-m10), not an omission — the synthetic fixture had no such field at all.

**Why §14 (the triage console) stays frozen on the synthetic source (the Phase-62 boundary).**
The §14 triage console (`dist/triage/`) is NOT re-grounded on this substrate output, and the
unfreeze authorized at the direction gate was stood down at the T4 checkpoint — on evidence, not
preference. The two consoles need different inputs: §12 measures *firings + dispositions* (exactly
what the substrate emits), but §14 needs **adjudicable fact patterns** — customer profile, activity
narrative, KYC note — so an analyst can render a judgment. `curate_triage_scenarios.py` pulls only
5 metadata fields (`alert_id, disposition, analyst, date, entity_id`) from the history into 7 of 20
scenarios; everything substantive (the panels, the TM-rule pairing, the divergent-disposition pair,
the controls) is hand-authored. The substrate's **label-blind alerts carry no fact pattern**, and
the console's signature beat (the S-01/S-02 process-inconsistency pair on **TM-104 = C20**) is
anchored on a capability the substrate has **no detector for** — structurally ungroundable. So the
grounded probe-history is the right source for §12 (measurement) and the **wrong source for §14**
(adjudication scenarios); §14 stays synthetic-curated by design. A genuinely grounded §14 would
need a fact-pattern synthesizer pairing substrate alerts with adjudicable narratives — its own
future phase, not a drop-in here.

## What this probe is NOT

- NOT a performance claim: every figure is a property of authored fixtures, useful only as the
  mechanical demonstration that the measurement definitions compute.
- NOT a calibration: dispositions here are invented; at adoption, real dispositions are
  evidence about *decisions*, never ground truth about correctness (blueprint §12 doctrine).
- NOT a ship artifact: nothing in `data/probe-history/` is read by `build.py`, merged into any
  demo, or carried into the corpus counts.
