# Active Phase Context

**Phase 79 — *Consume sibling emissions*: Lakeshore fan-in C3 floor + the merge real-data oracle (gated)** (signal-watch-local, STANDARD) — DELIVERED + accepted 2026-06-27 (committed 031a33a). Net: BOTH tracks landed. FLOOR — Lakeshore CASE-B SIGNS `cleared` via casework's Phase-19 fan-in C3 (re-vendor 076fb8e; honest window-compression ≤7d + an IND-02-grounded bundle) → the matched pair both route through casework. GATED UPSIDE — the merge measure-first gate cleared GREEN (the emit reproduced clean; `GT-<hash>` oracle non-circular, two-sided 13/16), so at the user's "supersedes" call `dist/merge` was re-frozen with 29 substrate-scored + 13 synthetic-scored (split by oracle provenance). Adversarial review (3 dims): 1 must-fix (mid-flight stale `cases.json`) resolved / 2 should-fix addressed / 1 self-refuted.

## Objective
Consume the two Phase-77-deferred sibling emissions as a floor + gated-upside bundle: (FLOOR) Lakeshore
co-signs `cleared` via fan-in C3, completing the north-star pair; (GATED UPSIDE) the merge real-data
oracle — measure-first, then gate the `dist/merge` re-freeze on a clean two-sided result.

## Scope
`vendor/aml-casework/**` · `data/casefile/**` · `scripts/serve_workbench.py` · `scripts/curate_merge_cases.py`
· `data/entity-spine/substrate-anchored-slice.json` · `data/merge/cases.json` · `scripts/build.py` ·
`merge.html` · `dist/merge/**` · `tests/merge-console.test.mjs` · `docs/*-PLAN-BRIEF.md` · `docs/cross-pillar-build-order.md` · `CLAUDE.md`

## Key constraints (LOAD-BEARING)
- **A1 guard:** `evidence_requirements.py` BYTE-UNCHANGED (held).
- **Firewall:** build.py imports no spine/scorer/sibling/curate; the 8 non-merge dists byte-frozen (held).
- **dist/merge** the ONE sanctioned re-freeze; validate↔curate EXACT parity; synthetic-substrate-anchored qualifier; no rate/score/multiplier wording; badge always-on.

## Exit criteria — ALL MET
`--check all` 9/9 (8 byte-frozen + dist/merge re-frozen); `evidence_requirements.py` byte-unchanged;
`uv run pytest` 26; merge 74/0; workbench 169/0; the three briefs + cross-pillar-build-order trued up.

## Abort rule
Any non-merge dist drift / a build.py spine/scorer/sibling/curate import / an `evidence_requirements.py`
change / a confusion number as a catch-rate or lift → STOP-and-surface.

## Gates
- [x] spec (`specs/phase-79-consume-sibling-emissions.md`)
- [x] Direction confirmed by user (2026-06-27, AskUserQuestion — "Bundle, gated upside"; ledger Phase-79)
- [x] Delivery accepted (post-implementation report 2026-06-27; committed 031a33a)

Spec `specs/phase-79-consume-sibling-emissions.md`; plan
[[phases/phase-79-consume-sibling-emissions]]; ledger Phase-79.
