---
title: "Phase 58 — Corpus→substrate signal-coverage map (design the detection layer FROM the corpus)"
type: phase
status: completed
ceremony: lite
milestone: M9
created: 2026-06-18
updated: 2026-06-18
tags: [cross-pillar, corpus-coverage, signal-coverage-map, detection-layer, emergence-doctrine, capability-scaling, measure-first, sibling-briefs, non-ship]
---

# Phase 58 — Corpus→substrate signal-coverage map

## Objective

Close the gap the user named at the dev-plan gate: the synthetic-data + detection layer (Pillar 1,
aml-substrate) was built **bottom-up** — 6 detectors with "chosen-not-measured" thresholds authored from
individual advisory flags — with **no systematic join to the corpus catalog** (2,251 indicators / 523
buildable). The corpus is the program's signal source-of-truth. Produce the **executable
corpus→substrate signal-coverage map** that grounds "build 200+ corpus signals" in MEASURED reachability,
the **doctrine-safe mapping design**, and the **prioritized sibling build briefs** that turn the map into
a corpus-driven 200+-signal build plan. signal-watch's architecture role; the build itself runs in
sibling-rooted sessions (the P55/P56/P57 rhythm).

## Direction (gated 2026-06-18, all_accept: true)

The user reframed: the detection layer should be designed AGAINST the corpus, targeting 200+ grounded
signals to demonstrate signal/atom monitoring + narrative generation at scale. Three positions taken,
all at the recommended option:

- **Scope/target** → the deliverable is the measured map + briefs HERE; "200+ signals" = 200+ grounded
  corpus indicators backed by ~15-20 capability detectors (NOT 200 detector implementations —
  grounding_replay is capability-scaled); the build is sibling-rooted.
- **Doctrine (the weakest assumption)** → the corpus drives DETECTOR + observable-exposure design
  top-down; data generation + labels stay bottom-up/emergent. The map MEASURES behavioral gaps, never
  stamps them. (Authoring detectors to find known typologies isn't injection.)
- **Rigor** → reachability is MEASURED against pinned real emitted data, tiered honestly:
  observable-surface = measured; behavioral-emergence = reasoned-and-flagged.

Grounding (code-verified this session): **aml-substrate@df23bba** [Phase 14 — the persist seam is BUILT
(`--emit-evidence`); 6 detectors (C2/C3/C4/C5/C6/C15); the synthetic data is already RICH (6 channels +
full KYC/CDD + ownership graph); the top-5 corpus D-codes (D8/D1/D3/D13/D2 = 62%) all modeled → the gap
is detector breadth + view exposure + behavioral coverage, NOT data fields]; **aml-casework@2381d71**
[grounding_replay registers 5 capability assertions (C2/C3/C4/C5/C15); one capability grounds many corpus
signals].

## Approach (single-beat, signal-watch-local; the build is the sibling follow-on)

- **The map (T1)** reads the committed corpus's 523 buildable indicators + a PINNED snapshot of the
  substrate observable schema + detector/assertion registries + the already-vendored emitted sample
  (CASE-P-0010361) → a per-signal tiered reachability classification: `reachable-now` /
  `needs-detector` / `needs-view-exposure` / `needs-behavior` / `out-of-reach`. Deterministic +
  re-runnable (`--check` byte-identical, `--selftest` validates the classifier). The measured answer to
  "how many of 200+ are reachable, and what's the itemized gap."
- **The design (T2)** states the corpus→D-code→substrate-field→C-code→detector→casework-assertion
  mapping contract + the emergence boundary (observable/detector top-down OK; label/behavior bottom-up
  only) + the measured findings; extends the integration contract; re-grounded with HEADs pinned inline.
- **The briefs (T3)** rank capabilities by signals-unlocked-per-capability (mechanically from the map) →
  which ~15-20 capabilities to wire + which observables to expose (aml-substrate), which assertions to
  add (aml-casework). Authored here, executed in sibling sessions.

## Scope

- `scripts/signal_coverage_map.py` (NEW) · `data/coverage-map/**` (the pinned substrate snapshot +
  the frozen output) · `tests/` (a selftest) · `docs/corpus-substrate-coverage.md` (NEW) ·
  `docs/pillar-integration-contract.md` (extend with the mapping subsection)
- `aml-substrate/docs/corpus-coverage-build-PLAN-BRIEF.md` + `aml-casework/docs/capability-assertions-PLAN-BRIEF.md`
  (authored here, executed in sibling sessions)
- NOT touched: the 8 build targets / offline dists; the committed corpus records + overlays (read-only);
  `build.py` never imports the new script; no sibling import.

## Exit criteria

1. `scripts/signal_coverage_map.py` — reads the 523 buildable corpus indicators + the pinned
   `data/coverage-map/substrate-pin.json` (schema fields + detector/assertion C-codes, HEADs inline) +
   the vendored CASE-P-0010361 emission → a per-signal tiered reachability classification; observable
   reachability MEASURED, behavioral reachability flagged `behavior_confirmed:false`; `--check`
   re-derives a byte-identical committed `data/coverage-map/coverage.json`; `--selftest` green (a
   tampered pin / a fabricated reachable-now must fail); `! grep import aml_substrate|aml_casework`;
   build.py never imports it; `--check all` 8/8.
2. `docs/corpus-substrate-coverage.md` — the mapping contract + the emergence boundary stated
   explicitly + the measured numbers (the 5 tier counts + the itemized path to 200+); the integration
   contract gains a "signal-coverage mapping" subsection; re-grounded (df23bba / 2381d71 pinned inline).
3. Both sibling briefs written, ranked by signals-unlocked-per-capability, carrying code-verified
   current-HEAD facts + the shared acceptance + the doctrine constraint (no behavior/label stamping).
4. `--check all` 8/8 (the 8 ship dists byte-identical); the change set contains ZERO ship artifacts.

## Delivery gate (the 200+ build — GATED on the siblings)

The corpus-driven 200+-signal build closes when the aml-substrate detectors/views + the aml-casework
assertions land (sibling-rooted sessions) and the coverage map's `reachable-now` count rises to the
target. Single-beat here (the map + design + briefs); the build is the sibling follow-on.

## Assumptions (ledger: Phase-58 block, all_accept: true)

- **A0 [HIGH, T0 weakest]** Doctrine reconcilability — corpus drives detectors + observable-exposure
  (top-down); data + labels stay emergent (bottom-up); the map measures behavioral gaps, never stamps.
  ACCEPT. If false → reframe to the scoreboard ("measure what the emergent data already supports").
- **A1 [HIGH]** Deliverable = the map + briefs HERE; the 200+ build runs sibling-rooted. ACCEPT.
- **A2 [HIGH]** "200+ signals" = 200+ grounded corpus indicators backed by ~15-20 capability detectors
  (capability-scaled), NOT 200 detector implementations. ACCEPT.
- **A3 [MED]** Reachability MEASURED against pinned real emitted data + honest tiering (observable
  measured / behavioral reasoned-flagged). ACCEPT.
- **A4 [MED]** NON-ship — 8 dists byte-frozen, --check all 8/8; build.py never imports the script;
  cross-pillar artifacts re-grounded with HEADs pinned inline. ACCEPT.

## Abort

Any of the 8 offline dists drift, or a ship artifact is touched → STOP and surface (never re-baseline).
The map/briefs author corpus-driven detectors + observable-exposure ONLY — a brief that stamps
behavior or labels is out of bounds (the emergence doctrine, A0's abort-line). The companion importing
sibling code → out of bounds (subprocess/file-contract/vendored-pin only). A validator/selftest looks
like it needs loosening → fix the data/design, never the check. Grounding HEADs: aml-substrate@df23bba ·
aml-casework@2381d71 (re-grounded this phase).
