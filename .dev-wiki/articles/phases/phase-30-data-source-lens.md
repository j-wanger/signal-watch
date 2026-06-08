---
title: "Phase 30: Data-source lens — institution coverage-by-data-source view over the corpus"
aliases: ["phase-30-data-source-lens"]
category: phases
tags: [m7, corpus-explorer, data-source-lens, taxonomy, re-projection]
parents: []
created: 2026-06-08
updated: 2026-06-08
source: plan
status: active
delivery: ready-for-completion
scope: ["corpus.html", "dist/corpus/index.html", "tests/corpus-explorer.test.mjs", "tests/smoke-checklist.md", "CLAUDE.md", "HANDOFF.md", "README.md"]
entry_criteria: "Phase 29 delivered + accepted + committed/pushed to main (029f33c); the corpus is the primary demo. The Phase-29 capability lens surfaced the C1–C28 axis; the symmetric D1–D20 data-source axis is still unused as a front-door view. The Phase-29 taxonomy already carries the data_sources block and build.py already validates + inlines the data_source codes — the backend is built. Direction approved at the goal gate 2026-06-08 (D-lens only; OSFI disposed as non-derivable; no clean second Canadian indicator-source exists)."
exit_criteria: "A Data-sources Select mode (per-data-source demand count + institution posture + covered/partial/gap breakdown, gap-sorted) with drill-through into the per-doc arc + Back; honest counts only (no similarity/overlap/lift number; always-on badge stays); build.py + data/capability-taxonomy.json + all 42 derived records BYTE-FROZEN; --check all 4/4 zero drift; --selftest PASS; all 42 records --check-derived clean; harness extended + green; NO non-negotiable change."
---

# Phase 30: Data-source lens — institution coverage-by-data-source view over the corpus

## Objective

Surface the D1–D20 data-source axis as a DATA-SOURCE LENS in the corpus explorer — the symmetric counterpart to the Phase-29 capability lens. Answer coverage PER DATA SOURCE across the whole corpus: "across every regulator-published red flag, here are the data feeds the indicators depend on, ranked by demand, cross-referenced against what the institution can actually access." Where the capability lens asks "do we have the detection CAPABILITY" (a build problem), the data-source lens asks "do we even have the DATA FEED" (an access/vendor problem). The distinct payoff: 7 of the 20 data sources have posture "n" (not yet available) — exactly the SOURCE_DATA indicators currently buried per-doc — so the lens makes corpus-wide legible "here are all the indicators, across every regulator, you can't act on until you acquire e.g. blockchain analytics / beneficial-ownership data."

## Scope

Files and modules affected:
- `corpus.html` (the Data-sources Select mode + per-data-source aggregate view + drill-through `renderDataSource` + Back)
- `dist/corpus/index.html` (rebuilt)
- `tests/corpus-explorer.test.mjs`, `tests/smoke-checklist.md`, `CLAUDE.md`, `HANDOFF.md`, `README.md`

KEY SCOPE FACT — the BACKEND IS ALREADY BUILT (Phase 29): `data/capability-taxonomy.json` already carries the `data_sources` block (20 entries {id,name,desc,posture}; posture 9 y / 4 partial / 7 n); `build.py` already loads + referential-integrity-validates `data_source` codes (`validate_capability_taxonomy`) and already inlines `taxonomy.data_sources` + the per-indicator `data_source` codes into `__CORPUS__`; `corpus.html` already has `DS_BY` / `DSRC` / `dsNum` helpers (used inside `renderCapability`). Phase 30 needs ZERO change to build.py, the taxonomy, or any of the 42 derived records.

## Exit Criteria

- [ ] A Data-sources mode on the Select toggle (Documents / Typologies / Capabilities / Data sources — the 4th co-equal mode): per data source — name, institution posture (have/partial/gap), # indicators demanding it, covered/partial/gap breakdown, gap-sorted; group line OMITTED (data sources have empty `group`); honest counts only (`dsAgg`/`indsForDS` mirror `capAgg`/`indsForCap`)
- [ ] Drill-through: pick a data source → its indicators pooled across all docs (each traceable to source doc + jurisdiction), grouped by source document → drill into the doc's per-doc arc; a coverage gauge + the detection capabilities those indicators implement; Back returns to the data-source view (`fromDataSource`, mirroring `fromCapability`)
- [ ] `node tests/corpus-explorer.test.mjs` green with new data-source-lens assertions (incl. a no-similarity/overlap/lift assertion); `--check all` 4/4 zero drift; `--selftest` PASS; all 42 records `--check-derived` clean

## Constraints

- The honesty model is RE-PROJECTION only (the Phase-24/29 precedent): per-data-source DEMAND = honest count of corpus indicators carrying that `data_source` code; institution POSTURE = the interview answers re-grouped by data source; covered/partial/gap = honest counts over existing per-indicator status — prevents fabricating a new metric the records don't carry.
- NO similarity / overlap / lift number; the always-on "Illustrative data & outputs" badge stays — prevents presenting synthetic numbers as real (the standing non-negotiable).
- FROZEN byte-clean: the showcase (`index.html` + `config/**` + the 3 typology dists), every source md, every `corpus-status.json`, `data/typology-map.json`, `data/capability-taxonomy.json`, `scripts/build.py`, the grounding core `scripts/derive_signals.py`, AND every derived `data/*/derived/*.json` record (the `data_sources` axis was already inlined/validated in Phase 29 — NO data/build change this phase) — prevents scope creep into a corpus re-derivation or a build-layer change.

## Assumptions

- Every derived indicator already carries a valid `data_source` code that exists in the taxonomy, and every used code has a posture answer (all 20 data sources used; posture 9 y / 4 partial / 7 n). VERIFIED this round directly from the derived records. If false at impl: build.py's existing `validate_capability_taxonomy` already fails loud — surface the gap, do not silently drop a code.

## Notes

Direction chosen over "data-source lens + OSFI as a new source": a read-only feasibility check disposed OSFI (Guideline B-8 is principles-based supervisory guidance that DEFERS to FINTRAC/FATF — no enumerated red-flag list, so not a red-flag corpus source honestly), and a landscape check found no clean second Canadian indicator-source exists (FINTRAC is Canada's sole enumerated-indicator publisher; OSFI/CIRO/AMF defer to it). Completing the multi-jurisdiction setup honestly points to a THIRD jurisdiction (AUSTRAC / UK) — offered, but the user chose the D-lens-only win. Lite ceremony; 3 M tasks; the tightest phase since the capability-lens plumbing already exists.
