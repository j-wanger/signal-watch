---
title: "Codebase Snapshot — 2026-06-28 (post Phase 81)"
category: status
tags: [snapshot, phase-81, sanctions-arc, c17-exposure, observable-only, org-merge-abort, measure-first, substrate-consume]
created: 2026-06-28
updated: 2026-06-28
source: debrief
---

# Codebase Snapshot — 2026-06-28

Captured at the Phase 81 debrief (consume substrate Phases 35–37: the sanctions arc). Both planned
consumes hit their measure-first branches → an HONEST reshape. **Companion-only — NO dist touched**
(the org-merge track aborted, so the would-be 3rd-consecutive `dist/merge` re-freeze never happened).

## Ship artifacts (9 `--check` targets; offline single files)

`dist/` byte-frozen artifacts: `fentanyl` · `trade-based` · `elder-financial-exploitation` · `corpus` ·
`news` · `console` · `triage` · `merge` + the `launcher`. This phase: **ALL 9 BYTE-FROZEN** (`--check all`
9/9; `dist/merge` UNTOUCHED — the org track aborted at T1a). No ship/engine change at all.

## Module / data delta this phase (companion-only)

- NEW `data/casefile/sanctions-c17-exposure-demo.bundle.json` — the C17 exposure-via-ownership demo bundle
  (sanctioned-BO exposure; `resolution_edges` emails masked to example.test).
- `scripts/serve_workbench.py` — NEW `/sanctions-c17-exposure` route + the C17 consume path (the engine SHOWS
  the case does NOT reach the determination bar; the §12 discovery feed classes all 13 sanctioned-BO cases as
  over-flag — a defensive-exposure basis, `sanctions_flag` label-blind, corr≈0 by design).
- `workbench.html` — NEW `sanctionsC17PanelHTML` (the observable, names-not-codes; honesty-word-banned "N pct").
- `evidence_requirements.py` + `data/workbench/evidence-requirements.json` BYTE-UNCHANGED (A1) — the C17 leg
  shipped OBSERVABLE-ONLY, not a determination atom (the planned §12-advance was DEGENERATE: DELTA=0 to the bar
  on the rigorous engine re-measure — the cohort has no ML mechanism).
- NO merge change (the org-collision oracle is STRUCTURALLY one-sided — substrate fragments PERSONS, 0 org GT
  clusters → all-reject; T1a's reject-branch fired). `data/merge/cases.json`, `merge.html`, `dist/merge` all
  byte-frozen; build.py imports no spine/scorer/sibling/curate.
- DOCS: NEW `docs/{open-sanctions-data-fork,substrate-org-fragment-emit,substrate-exposure-signal}-PLAN-BRIEF.md`;
  reconciled `docs/substrate-p35-determination-signals-PLAN-BRIEF.md` (TF/C7 substrate-CUT, org-name DONE);
  trued-up `docs/cross-pillar-build-order.md` (substrate f7fbdb0 / casework 076fb8e); `CLAUDE.md`.

## Tests

- 8 zero-dep Node DOM-shim arcs unchanged except **workbench (167→178)** — the C17 block incl. the
  honesty-governor word-ban assertion. corpus-explorer (303), news-stream (150), gate-console (68),
  triage-console (93), merge-console (74), chain, launcher.
- pytest umbrella (`uv run pytest`): **27**.
- `serve_workbench --selftest` extended (the C17 observable block); `--check all` 9/9 byte-frozen.

## Dependencies

Offline ship artifacts: zero-dep, stdlib (Python 3.10). Live/companion tier: `markitdown` (gitignored .venv),
DuckDB (companion stores), optional local llama-cpp / openai backend. No runtime deps in the dists.

## Recent commits (Phase 81 impl not yet committed at snapshot time — orchestrator handles it)

- `a0896da` Phase 80: Consume substrate Phase 34 — OFAC name-collision merge class + non-tautological C14 §12 leg
- `cd44c6a` chore(dev-wiki): close Phase 79 — delivery gate accepted (031a33a)
- `031a33a` Phase 79: consume sibling emissions — Lakeshore `cleared` co-sign + merge console supersede
- `92ac6d0` Phase 78: Consume the disposition oracle — determination-validation harness + the §12 discovery feed
- `5afdb96` chore(dev-wiki): close Phase 77 — delivery gate accepted (676b549)

## Related

- Prior `*-codebase-snapshot.md` for the full module/dependency maps (this summarizes the Phase-81 delta).
- [[phases/phase-81-consume-substrate-sanctions-arc|Phase 81 — Consume substrate Phases 35–37: the sanctions arc]]
- NOTE: `scripts/check-assumption-ledger.sh` is ABSENT in this project — the Phase-81 ledger revisit fill was
  verified manually (all 6 rows A1–A6 carry `revisit-status:` + a closing `revisit-note:`).
