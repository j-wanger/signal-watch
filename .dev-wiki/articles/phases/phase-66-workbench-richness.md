---
title: "Phase 66: Workbench richness — richer slice + OSINT corpus depth + the substrate BO-graph emission handoff brief"
aliases: [workbench richness, richer slice, OSINT corpus depth, beneficial-owner graph, ownership graph, RelationshipEdge mirror, BO-graph emission brief]
category: phases
tags: [m9, lfcm, workbench, richness, osint, beneficial-owner, cross-pillar-brief]
parents: []
created: 2026-06-21
updated: 2026-06-21
source: plan
status: active
scope:
  - "scripts/curate_workbench_cases.py"
  - "data/workbench/** (re-vendored, re-pinned)"
  - "data/osint/corpus.json"
  - "scripts/osint_tools.py"
  - "workbench.html (richer gather rendering)"
  - "docs/substrate-bo-graph-emission-PLAN-BRIEF.md (NEW)"
  - "docs/case-workbench.md"
  - "tests/workbench.test.mjs"
  - "tests/smoke-checklist.md"
  - "scripts/build.py (NEVER imports aml_substrate/aml_casework — the substrate emit + casework coverage-measure run as subprocess TOOL-USE, file-contract)"
entry_criteria: "Phase 65 delivered + accepted (committed 761a446); the workbench (workbench.html + serve_workbench.py + the Phase-65 GATHER beat, companion-only, NOT a build target) is in place. Recon code-verified this session (signal-watch consume side + aml-substrate generation side @9d2e65c): the substrate is single-signal-separable (composition architecturally subsumed by network linkage — P16) so MORE cases/typologies/detectors add visible VOLUME, not detection difficulty; the richness that compounds is the NETWORK (the generated-but-unprojected RelationshipEdge BO/director graph — the recon's ranked #1 lever); the workbench slice is a DETERMINISTIC substrate emit (`--clients 40000 --seed 0 …`, re-runnable as TOOL-USE, gen unchanged from the f90bd39 pin — VERIFIED)."
exit_criteria: "The 4 tasks' success fields met: the ~320-case slice re-vendored + re-pinned (`curate_workbench_cases.py --selftest` green over the wider slice — more distinct fired-signal combos than the prior 23, the 4 exemplars re-tagged, route() faithful to the baked gate); the deepened OSINT corpus (9 → ~50 records) validates + renders, the registry ownership records shaped as RelationshipEdge-MIRRORING edges (BENEFICIAL_OWNER/DIRECTOR_OF/ownership_pct), GATHER returns grounded findings on >4 distinct subjects with the honesty seam unchanged (`osint_tools.py --selftest` + the gather arc green); the aml-substrate BO-graph EMISSION handoff brief authored (named sections, mirrors the T2 OSINT shape, pinned aml-substrate@9d2e65c); the single-signal-separable GOVERNOR documented; `uv run pytest` + `node tests/workbench.test.mjs` green; `build.py --check all` 8/8 ZERO dist drift; no aml_substrate/aml_casework import in build.py; companion-only (workbench/osint NOT ship targets)."
---

# Phase 66: Workbench richness — richer slice + OSINT corpus depth + the substrate BO-graph emission handoff brief

## Objective

Add demo-VISIBLE richness to the investigator workbench now (more cases + a deeper synthetic OSINT
corpus) AND author the durable network lever as a sibling brief — so the two repos stay coherent. Two
signal-watch-LOCAL richness wins are built here; the highest-value-but-sibling-rooted network lever (the
substrate beneficial-owner / ownership graph) ships as a handoff brief executed in aml-substrate. The
delta: (1) re-vendor a wider ~320-case slice via a DETERMINISTIC substrate re-emit + re-curate; (2)
deepen `data/osint/corpus.json` (9 → ~50 records) with its registry ownership records shaped to MIRROR
the substrate `RelationshipEdge` schema (BENEFICIAL_OWNER / DIRECTOR_OF / ownership_pct) so the local win
previews the emitted BO graph; (3) author the aml-substrate BO-graph EMISSION handoff brief. Companion-
only (workbench/osint are NOT ship targets); `--check all` stays 8/8 with ZERO dist drift; build.py
NEVER imports the siblings.

**The starting point (code-verified this session, signal-watch consume side + aml-substrate generation
side @9d2e65c):**
- **The substrate is single-signal-separable.** Composition is architecturally subsumed by network
  linkage (P16), so MORE cases / typologies / detectors add visible VOLUME, NOT detection difficulty —
  this is THE GOVERNOR for every richness claim in the phase (documented, never hidden).
- **The network is the richness that compounds.** The generated-but-unprojected `RelationshipEdge`
  BO/director graph is the recon's ranked #1 lever — but it is SIBLING-rooted (lives in aml-substrate),
  so it ships here as a PLAN-BRIEF, not a build.
- **The slice is a deterministic, re-runnable emit.** `--clients 40000 --seed 0 --emergence --monitor
  --emit-evidence --emit-screening`, re-runnable as TOOL-USE, gen unchanged from the f90bd39 pin
  (VERIFIED) → a wider re-vendor is a re-emit + re-curate + re-pin, not new generation.
- **The OSINT corpus exists (Phase 65) and can deepen + mirror.** `data/osint/corpus.json` is committed
  synthetic; deepening it AND shaping its ownership records to the substrate `RelationshipEdge` schema
  makes the local win double as the brief's rendering prototype.

## The four tasks

1. **T1 — Richer vendored slice.** Re-run the DETERMINISTIC substrate emit (tool-use; build.py never
   imports it) + re-curate with wider caps (~200 → ~320 cases, more 4+-cap exemplars + a wider combo
   spread) + re-measure casework coverage + re-vendor `data/workbench/cases.json` + bundles, re-pinned to
   the current gen HEAD. Honest framing: visible VOLUME, NOT detection difficulty (single-signal-
   separable). `curate_workbench_cases.py --selftest` validates the new slice (schema, exemplars span the
   gates, MEASURED coverage matches per-case grounds_e2e, route() faithful to the baked gate);
   slice_total ~320 with MORE distinct fired-signal combos than the prior 23; the 4 exemplars re-tagged.
2. **T2 (PRIMARY) — Deepen the OSINT corpus + MIRROR the substrate ownership schema.** Expand
   `data/osint/corpus.json` (9 → ~50 records — named counterparties / jurisdictions / sanctions /
   adverse-media / PEP, keyed across MANY more workbench subjects, not just the 4 exemplars); shape the
   registry ownership records as `RelationshipEdge`-MIRRORING edges (`BENEFICIAL_OWNER` / `DIRECTOR_OF` /
   `ownership_pct`); `validate_osint_corpus` + the gate handle the new fields (the banned-token sweep
   extended to any new rendered field); the gather UI (workbench.html) renders the richer findings
   (jurisdiction) + the ownership edges (the relationship label + ownership_pct). The honesty seam
   (consistency-not-correctness, the synthetic-provenance line, the entity-exact-against-declared-names
   gate) is UNCHANGED. GATHER returns grounded findings on >4 distinct subjects.
3. **T3 — The aml-substrate BO-graph EMISSION handoff brief.** Author
   `docs/substrate-bo-graph-emission-PLAN-BRIEF.md` (the Phase-55–58 sibling-brief pattern) — expose the
   generated-but-unprojected `RelationshipEdge` BENEFICIAL_OWNER/DIRECTOR_OF edges via a
   `PartyGraphView`; emit `related_parties[]` (with ownership_pct) in the evidence bundle; a NON-
   tautological C14 BO-disclosure detector (a beneficial owner missing CDD, NOT the cdd_level↔risk_rating
   tautology); the contract/version bump; the CONSUME-side mapping (how the workbench network view +
   GATHER render the emitted graph — MIRRORS the T2 OSINT schema). Executed in the sibling, NOT built
   here; pinned aml-substrate@9d2e65c.
4. **T4 — Suites + drift + docs + the governor.** Re-run the suites against the richer slice + deeper
   corpus; `--check all` 8/8 ZERO dist drift (workbench/osint companion-only); `docs/case-workbench.md` +
   `tests/smoke-checklist.md` updated for the bigger slice + the richer gather + the ownership network;
   the single-signal-separable GOVERNOR documented (visible-richness-not-detection-difficulty).

## The governor (LOAD-BEARING, A0)

Every richness claim is demo-VISIBLE (more cases / deeper profiles / richer network), NEVER a detection-
difficulty / catch-rate / lift claim. The substrate is single-signal-separable — composition is
architecturally subsumed by network linkage (P16) — so adding cases/typologies/detectors grows VOLUME,
not the difficulty of detection; this finding is DOCUMENTED, not hidden. The GATHER findings stay
consistency-not-correctness (the Phase-65 seam). If any framing reads as "harder to detect / better
catch" → re-word; never claim detection lift. ZERO catch-rate/detection-difficulty/lift number anywhere;
the always-on "Illustrative data & outputs" badge stays.

## Scope

Files and modules affected (companion-only — NOT a build target):
- `scripts/curate_workbench_cases.py` — re-curate with wider caps; the wider slice re-vendored + re-pinned
  to the current gen HEAD via subprocess TOOL-USE (build.py never imports the siblings).
- `data/workbench/**` — the re-vendored ~320-case slice + bundles (re-pinned; `meta.synthetic:true`).
- `data/osint/corpus.json` — deepened 9 → ~50 records; the ownership records shaped to MIRROR the
  substrate `RelationshipEdge` schema (BENEFICIAL_OWNER / DIRECTOR_OF / ownership_pct).
- `scripts/osint_tools.py` — `validate_osint_corpus` + the gate handle the new fields; the banned-token
  sweep extended to any new rendered field.
- `workbench.html` — the gather UI renders the richer findings (jurisdiction) + the ownership edges (the
  relationship label + ownership_pct); the honesty seam unchanged.
- `docs/substrate-bo-graph-emission-PLAN-BRIEF.md` — NEW; the sibling-executed handoff brief.
- `tests/workbench.test.mjs` — the gather arc re-run over the richer corpus (ownership-edge rendering,
  XSS, NO %/lift).
- `tests/smoke-checklist.md` — updated for the bigger slice + the richer gather + the ownership network.
- `docs/case-workbench.md` — updated for the bigger slice + the richer gather; the governor documented.
- `scripts/build.py` — NEVER imports aml_substrate / aml_casework; the substrate emit + casework
  coverage-measure run as subprocess TOOL-USE (file-contract).

## Exit Criteria

- [ ] T1: the ~320-case slice re-vendored + re-pinned; `curate_workbench_cases.py --selftest` validates
      the new slice (schema, exemplars span the gates, MEASURED coverage matches per-case grounds_e2e,
      route() faithful to the baked gate); slice_total ~320 with MORE distinct fired-signal combos than
      the prior 23; the 4 exemplars re-tagged; `! grep -E 'import (aml_substrate|aml_casework)'
      scripts/build.py`.
- [ ] T2: `osint_tools.py --selftest` passes (the bigger corpus validates; the ownership-edge records
      ground + build into the graph; every gate bypass still closed; persists-nothing); `node
      tests/workbench.test.mjs` gather arc green over the richer corpus (ownership-edge rendering, XSS, NO
      %/lift); GATHER returns grounded findings on >4 distinct subjects.
- [ ] T3: `docs/substrate-bo-graph-emission-PLAN-BRIEF.md` exists with the named sections (`grep -q` for:
      PartyGraphView · related_parties · C14 · ownership_pct · the consume-side mapping to the T2 OSINT
      shape); pinned to aml-substrate@9d2e65c.
- [ ] T4: `uv run pytest` green + `node tests/workbench.test.mjs` green + `python3 scripts/build.py
      --check all` 8/8 ZERO dist drift; `docs/case-workbench.md` carries the governor statement (`grep -q`
      for the single-signal-separable / visible-richness boundary).

## Constraints

- Companion-only — `workbench.html` / `data/osint` / `data/workbench` are NOT ship targets; the 8 dists
  byte-frozen; `--check all` 8/8 ZERO dist drift — prevents the new-ship→standard ceremony escalation.
- THE GOVERNOR (A0, load-bearing): demo-VISIBLE richness only; ZERO catch-rate/detection-difficulty/lift
  number; GATHER findings stay consistency-not-correctness; the single-signal-separable finding
  documented, not hidden.
- The OSINT ownership records MIRROR the substrate `RelationshipEdge` schema (A1) — the local win doubles
  as the BO-graph brief's rendering prototype; the repos stay coherent at the data-contract level.
- The slice is a DETERMINISTIC substrate re-emit + re-curate (A2) — `--seed 0`, re-runnable; if the
  re-emit drifts from the pin's population → re-pin honestly + accept the new deterministic slice (do NOT
  force the old slice).
- The BO-graph emission is a PLAN-BRIEF authored here, executed in aml-substrate (A3, the Phase-55–58
  sibling-brief pattern) — NOT built here.
- The honesty seam (consistency-not-correctness, the synthetic-provenance line, the banned-token sweep,
  the always-on badge) is UNCHANGED.
- build.py NEVER imports aml_substrate / aml_casework — the substrate emit + casework coverage-measure
  run as subprocess TOOL-USE (file-contract).

## Assumptions (gate-resolved — the GOVERNOR carries the weakest, T0)

- **A0 [HIGH — T0 weakest, the GOVERNOR].** Every richness claim is demo-VISIBLE (more cases / deeper
  profiles / richer network), NEVER a detection-difficulty / catch-rate / lift claim; the GATHER findings
  stay consistency-not-correctness; the substrate single-signal-separable finding (composition subsumed
  by network linkage — P16) is DOCUMENTED, not hidden. ACCEPT. If false (a framing reads as "harder to
  detect / better catch") → re-word, never claim detection lift.
- **A1 [HIGH — chosen at the gate].** The deepened OSINT corpus's ownership records MIRROR the substrate
  `RelationshipEdge` schema (BENEFICIAL_OWNER / DIRECTOR_OF / ownership_pct) → the local win doubles as
  the BO-graph brief's rendering prototype + the repos stay coherent at the data-contract level. ACCEPT
  (mirror the substrate schema). If false (the substrate schema differs materially) → the brief documents
  the delta; the OSINT shape stays a valid synthetic stand-in.
- **A2 [MED — chosen at the gate].** The slice is a DETERMINISTIC substrate re-emit (tool-use, `--clients
  … --seed 0`, re-runnable — verified) + re-curate with wider caps → ~320-case slice (more 4+-cap
  exemplars, wider combo spread), re-measured coverage, re-vendored + re-pinned; OSINT depth is the
  PRIMARY win, the slice secondary volume. ACCEPT (modest ~320). If the re-emit drifts from the pin's
  population → re-pin honestly + accept the new deterministic slice.
- **A3 [MED].** The BO-graph emission is a PLAN-BRIEF authored HERE (docs/), executed in aml-substrate
  (the Phase-55–58 sibling-brief pattern); signal-watch defines the contract (`RelationshipEdge` →
  `related_parties[]` bundle emission + a `PartyGraphView` projection + a non-tautological C14
  BO-disclosure detector), NOT built here. ACCEPT.
- **A4 [MED].** COMPANION-ONLY: workbench.html / data/osint / data/workbench are NOT ship targets
  (build.py never imports the siblings or osint_tools; the 8 dists byte-frozen, --check all 8/8 ZERO dist
  drift); the honesty seam (consistency-not-correctness, the synthetic-provenance line, the banned-token
  sweep, the always-on badge) is UNCHANGED. ACCEPT (by precedent). If false → STOP-and-surface.

## Notes

- **Two-repo coherence is the design center.** The T2 OSINT ownership records are shaped to MIRROR the
  substrate `RelationshipEdge` schema deliberately: the signal-watch-local win (a richer GATHER over
  ownership edges) doubles as the rendering prototype for the BO graph the sibling brief (T3) will emit.
  The local build PREVIEWS the emitted graph so the repos stay coherent at the data-contract level — when
  aml-substrate ships the `PartyGraphView` + `related_parties[]` emission, the workbench's consume side
  already speaks the shape.
- **`news_ground` stays a third consumer.** The GATHER grounding gate reuses `news_ground` (Phase 65);
  deepening the corpus + adding ownership fields extends what the gate grounds, not the gate itself — the
  banned-token sweep is extended to any new rendered field, the grounding contract unchanged.
- **The BO-graph emission is sibling-executed.** T3 authors the contract HERE; the `PartyGraphView`
  projection, the `related_parties[]` bundle emission, and the non-tautological C14 BO-disclosure detector
  are built in aml-substrate (the Phase-55–58 sibling-brief pattern, [[cross-pillar-review-verify-sibling-repo]]).
  Pinned aml-substrate@9d2e65c.
- **The governor is the load-bearing honesty invariant** ([[grounding-universal-substrate-varies]],
  [[honesty-over-demo-drama]]) — the single-signal-separable finding is DOCUMENTED, not hidden; richness
  reads as visible volume, never as a detection-difficulty claim ([[composition-detection-lift-retired]]).
- **Follow-on (still sequenced OUT):** the C3/C15 cross-pillar contract alignment (a sibling-repo phase,
  the composed-case grounding frontier) remains the other un-driven-from-here frontier
  ([[cross-pillar-consume-batch-not-thin]]).
