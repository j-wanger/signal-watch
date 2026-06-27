---
title: "Codebase Snapshot — 2026-06-27 (post Phase 79)"
category: status
tags: [snapshot, phase-79, merge-console, supersede, casework, fan-in-c3, lakeshore]
created: 2026-06-27
updated: 2026-06-27
source: debrief
---

# Codebase Snapshot — 2026-06-27

Captured at the Phase 79 debrief (consume sibling emissions — the Lakeshore fan-in C3 floor + the
merge real-data oracle supersede). Companion-only EXCEPT the ONE sanctioned `dist/merge` re-freeze.

## Ship artifacts (9 `--check` targets; offline single files)

`dist/` byte-frozen artifacts: `fentanyl` · `trade-based` · `elder-financial-exploitation` · `corpus` ·
`news` · `console` · `triage` · `merge` + the `launcher`. This phase: the 8 non-merge dists BYTE-FROZEN;
**`dist/merge/index.html` RE-FROZEN (91,443 B)** — the ONE sanctioned change (the consensus-66 →
substrate-scored supersede). `--check all` 9/9.

## Module / data delta this phase

- `data/merge/cases.json` — **42 cases (29 substrate-anchored SCORED + 13 synthetic-scored)**, split by
  oracle PROVENANCE; SUPERSEDED the Phase-76 consensus-66. `curate_merge_cases.enumerate_substrate_scored`
  replaces `enumerate_real_shares` (both populations scored; removed `_safe_value` + the `EntitySpine` import).
- NEW `data/entity-spine/substrate-anchored-slice.json` — the no-substrate-replayable merge oracle capture
  (32 candidate-relevant obs + the non-circular `GT-<hash>` cluster truth, `entity_ref ≠ cluster`; emails
  masked to example.test, email/phone demoted to weak).
- `build.py` `validate_merge_cases` mirrored in EXACT parity + a masking firewall; imports no spine/scorer/sibling/curate.
- FLOOR: `vendor/aml-casework/` b3546d4→**076fb8e** (Phase 19 `_c3_fan_in`; wheel + `VENDORED_AT`); NEW
  `data/casefile/case-b.bundle.json` (window-compressed ≤7d, IND-02-grounded) + `serve_workbench.lakeshore_cosign_consume`
  → Lakeshore CASE-B signs `cleared` end-to-end; the matched pair BOTH route through casework.
- `evidence_requirements.py` BYTE-UNCHANGED (A1).

## Tests

- 8 zero-dep Node DOM-shim arcs: corpus-explorer (303), news-stream (150), gate-console (68),
  triage-console (93), **merge-console (73→74)**, workbench (169), chain, launcher (23).
- pytest umbrella (`uv run pytest`): **26** (stable); curate broken-fixtures 7→9.
- `serve_workbench --selftest` PASS (Lakeshore co-sign + the matched pair + the fixture-drift bridge);
  `resolution_scorer --selftest` scores the anchored slice.

## Dependencies

Offline ship artifacts: zero-dep, stdlib (Python 3.10). Live/companion tier: `markitdown` (gitignored .venv),
DuckDB (companion stores), optional local llama-cpp / openai backend. No runtime deps in the dists.

## Recent commits (Phase 79 impl not yet committed at snapshot time — orchestrator handles it)

- `92ac6d0` Phase 78: Consume the disposition oracle — determination-validation harness + the §12 discovery feed
- `5afdb96` chore(dev-wiki): close Phase 77 — delivery gate accepted (676b549)
- `676b549` Phase 77: Consume the three sibling emissions — casework `cleared` (C5 proxy); harness + real-66 deferred
- `b18ef71` chore(dev-wiki): close Phase 76 — delivery gate accepted (c28d6a3)
- `c28d6a3` Phase 76: the merge-adjudication Class-J console — the 6th ship artifact

## Related

- Prior `*-codebase-snapshot.md` for the full module/dependency maps (this summarizes the Phase-79 delta).
- [[phases/phase-79-consume-sibling-emissions|Phase 79 — Consume sibling emissions]]
