---
title: "Codebase Snapshot — 2026-06-26 (post Phase 76)"
category: status
tags: [snapshot, phase-76, merge-console, ship-artifact]
created: 2026-06-26
updated: 2026-06-26
source: debrief
---

# Codebase Snapshot — 2026-06-26

Captured at the Phase 76 debrief (the merge-adjudication Class-J console — the 6th ship artifact).

## Ship artifacts (9 `--check` targets; offline single files)

`dist/` byte-frozen artifacts: `fentanyl` · `trade-based` · `elder-financial-exploitation` (the 3
showcase typologies) · `corpus` · `news` · `console` · `triage` · **`merge` (NEW Phase 76)** + the
`launcher` (dist/index.html — the sanctioned cascade, regenerated to add the merge card; the only
existing dist that changed this phase). `--check all` = 9 targets; the 8 existing byte-frozen except
the launcher.

## Module structure

- 29 `scripts/*.py` (build.py + the authoring pipeline + the companion layer: serve_news/corpus/chain/workbench, news_{ground,store,fetch}, entity_spine, resolution_scorer, measure_xcase_overlap, curate_{console,triage,workbench,merge}_cases, evidence_requirements, osint_tools, …).
- NEW this phase: `scripts/curate_merge_cases.py` (companion authoring tool; reuses entity_spine + resolution_scorer; NOT imported by build.py) → committed `data/merge/cases.json` (76 KB; 66 real consensus + 13 synthetic scored).
- `merge.html` (39 KB template) → `dist/merge/index.html` (115 KB, self-contained, offline).
- build.py gained the `merge` target (MERGE_* constants, load_merge_cases, STANDALONE validate_merge_cases, render/build/check_merge); imports no spine/scorer/sibling/curate.
- `resolution_scorer.py` oracle expanded (`data/entity-spine/true_entities.json`: 8→25 obs / 5→17 clusters; + candidate_pairs() + KLASS_*).

## Tests

- 8 zero-dep Node DOM-shim arcs: corpus-explorer (303), news-stream (150), gate-console (68), triage-console (93), **merge-console (73, NEW)**, workbench (151+), chain, launcher (23).
- pytest umbrella (`uv run pytest`): 22 → **24** (added curate_merge_cases selftest + the merge-console arc to `tests/test_selftests.py`).
- Python selftests: derive_signals, news_ground, serve_*, entity_spine, resolution_scorer, measure_xcase_overlap, curate_*, evidence_requirements, osint_tools (DuckDB-gated ones run under .venv, SKIP gracefully without it).
- M8 news pillar not regressed; `news_store.py` + `evidence_requirements.py` BYTE-UNCHANGED.

## Dependencies

Offline ship artifacts: zero-dep, stdlib (Python 3.10). Live/companion tier: `markitdown` (gitignored .venv), DuckDB (companion stores), optional local llama-cpp / openai backend. No runtime deps in the dists.

## Recent commits

- `bfed9a6` chore(dev-wiki): close Phase 75 — delivery gate accepted (daef922)
- `daef922` Phase 75: Consume the substrate v0.5 entity-resolution emission — entity_ref-keyed cross-case memory + SHARES adjudication
- `727a8ba` docs: make the 3 sibling handoff briefs dev-plan-ready (Phase 74 follow-on)
- `18784ac` chore(dev-wiki): close Phase 74 — delivery gate accepted (e18eba9)
- `e18eba9` Phase 74: persistent entity intelligence spine — consumer slice, standards, sibling briefs

(Phase 76 implementation not yet committed at snapshot time — the orchestrator handles the commit.)

## Related

- Scan articles: see prior `*-codebase-snapshot.md` for the full module/dependency maps (this snapshot summarizes the Phase-76 delta).
- [[phases/phase-76-merge-adjudication-console|Phase 76 — The merge-adjudication Class-J console]]
