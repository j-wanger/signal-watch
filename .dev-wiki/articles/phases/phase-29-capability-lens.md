---
title: "Phase 29: Capability lens — institution coverage-by-capability view over the corpus"
aliases: ["phase-29-capability-lens"]
category: phases
tags: [m7, corpus-explorer, capability-lens, taxonomy, re-projection]
parents: []
created: 2026-06-07
updated: 2026-06-08
source: plan
status: completed
scope: ["data/capability-taxonomy.json", "scripts/build.py", "corpus.html", "dist/corpus/index.html", "tests/corpus-explorer.test.mjs", "tests/smoke-checklist.md", "CLAUDE.md", "HANDOFF.md"]
entry_criteria: "Phase 28 complete + accepted + committed (24e4a08); the corpus is the primary demo; the per-indicator capability/data_source taxonomy from the Phase-28 interview is committed in every derived record but UNUSED in the ship artifact. Direction approved at the goal gate 2026-06-07."
exit_criteria: "A committed, build-validated data/capability-taxonomy.json; a Capabilities Select mode (per-capability demand count + institution posture + coverage breakdown, gap-sorted) with drill-through into the per-doc arc + Back; honest counts only (no fabricated/similarity/overlap/lift number; always-on badge stays); --check all 4/4 zero drift; --selftest PASS; all 42 records --check-derived clean; harness extended + green; NO non-negotiable change."
---

# Phase 29: Capability lens — institution coverage-by-capability view over the corpus

## Objective

Surface the Phase-28 C1–C28 capability / D1–D20 data-source taxonomy as a CAPABILITY LENS in the corpus explorer: answer coverage PER DETECTION CAPABILITY across the whole corpus (vs PER DOCUMENT today), cross-referenced against the institution's interview posture — the executive buy-in view and the realized payoff of the Phase-28 28+20 interview, which currently ships invisible in `dist/corpus`.

## Scope

Files and modules affected:
- `data/capability-taxonomy.json` (NEW committed overlay — promoted from `.dev-wiki/tmp/ph28-{taxonomy,answers}.json`)
- `scripts/build.py` (`load_capability_taxonomy` + `validate_capability_taxonomy`; thread codes + taxonomy into `__CORPUS__`)
- `corpus.html` (the Capabilities Select mode + per-capability aggregate view + drill-through)
- `dist/corpus/index.html` (rebuilt)
- `tests/corpus-explorer.test.mjs`, `tests/smoke-checklist.md`, `CLAUDE.md`, `HANDOFF.md`

## Exit Criteria

- [x] `data/capability-taxonomy.json` committed (code → {name, desc, group, posture}; 28 capabilities + 20 data sources); `build.py corpus` validates it fail-loud (shape + posture ∈ {y,n,partial} + closed-vocab referential integrity against all 875 indicator codes across the 42 records) and inlines it + the per-indicator codes into `__CORPUS__`
- [x] A Capabilities mode on the Select toggle (Documents / Typologies / Capabilities): per capability — name, institution posture (have/partial/gap), # indicators demanding it, covered/partial/gap micro-bar, gap-sorted; honest counts only
- [x] Drill-through: pick a capability → its indicators pooled across all docs (each traceable to source doc + jurisdiction) + a "Depends on data" data-source row → drill into the doc's per-doc arc; Back returns to the capability view (`fromCapability`)
- [x] `node tests/corpus-explorer.test.mjs` green with new capability assertions (165→190, incl. a no-fabricated-number assertion); `--check all` 4/4 zero drift; `--selftest` PASS; all 42 records `--check-derived` clean

## Constraints

- The honesty model is RE-PROJECTION only (the Phase-24 precedent): per-capability DEMAND = honest count of corpus indicators mapping to that capability; institution POSTURE = the interview answers re-grouped by capability — prevents fabricating a new metric the records don't carry.
- NO fabricated / similarity / overlap / lift number; the always-on "Illustrative data & outputs" badge stays — prevents presenting synthetic numbers as real (the standing non-negotiable).
- `build.py` must NEVER read from `.dev-wiki/` — the taxonomy MUST be a committed `data/` artifact (prevents coupling the ship build to intermediate planning files).
- FROZEN byte-clean: the showcase (`index.html` + `config/**` + the 3 typology dists), every source md, every `corpus-status.json`, `data/typology-map.json`, the grounding core `scripts/derive_signals.py`, AND every derived `data/*/derived/*.json` record (they already carry the codes — NO re-derivation) — prevents scope creep into a corpus re-derivation.

## Assumptions

- Every derived indicator already carries valid `capability` + `data_source` codes that exist in the taxonomy, and every used code has a posture answer. PRE-VERIFIED this round (all 875 indicators, 0 unresolved codes). If false at impl: surface the gap and FIX the taxonomy (abort rule) — never silently drop an indicator's code.

## Notes

The two engineering-rigor candidates the Phase-28 debrief left behind were disposed by a read-only grounding inspection before the gate: exact-equality dedup already exists at `derive_signals.py:353-361` (only the harder overlap/near-dup case remains, low ROI); the full-motion streaming harness path already exists at `tests/corpus-explorer.test.mjs:654-685`. The capability taxonomy being entirely unused in the ship artifact made the lens the highest genuine value. Lite ceremony; 4 M tasks.
