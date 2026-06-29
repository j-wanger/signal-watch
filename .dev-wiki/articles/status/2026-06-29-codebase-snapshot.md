---
title: "Codebase Snapshot — 2026-06-29 (post Phase 82)"
category: status
tags: [snapshot, phase-82, north-star-at-scale, predicate-reference, mitigation-evidence, grounded-evidence, org-merge-abort, casework-re-vendor, measure-first, substrate-consume]
created: 2026-06-29
updated: 2026-06-29
source: debrief
---

# Codebase Snapshot — 2026-06-29

Captured at the Phase 82 debrief (consume sibling emissions: north-star evidence AT SCALE). The §12 loop
closes from GROUNDED bundle evidence at scale; two of four deltas were honest non-results (each
measure-first gate doing its job). **Companion-only — NO dist touched** (the merge-org track aborted, so
the would-be 4th-consecutive `dist/merge` re-freeze never happened).

## Ship artifacts (9 `--check` targets; offline single files)

`dist/` byte-frozen artifacts: `fentanyl` · `trade-based` · `elder-financial-exploitation` · `corpus` ·
`news` · `console` · `triage` · `merge` + the `launcher`. This phase: **ALL 9 BYTE-FROZEN** (`--check all`
9/9; `dist/merge` UNTOUCHED — the merge-org track aborted at T2a). No ship/engine change at all.

## Module / data delta this phase (companion-only)

- `scripts/serve_workbench.py` — NEW `_bundle_evidence` reader + `determine_case` wiring: READS the P39
  prior-STR predicate (`named_predicate_risk` via a `flagged` resolution edge) + the P40 affirmative
  mitigation (`mitigation_evidence`) from each substrate bundle as DATA the FROZEN engine already
  consumes → the 376-case slice resolves 1 KYC-integrity determination + 17 ML affirmative `cleared`
  (was 0/0); grounded-evidence-with-human-override (the human still adjudicates the disposition).
- `workbench.html` — `paintDet` gained the grounded-evidence panel + the `.detv.clear` verdict branch
  (slice cases that affirmatively clear now render a documented-dismissal, was mis-rendered as
  needs-more-info).
- `scripts/curate_workbench_cases.py` — SUBSTRATE_HEAD fc98b09→**294d3e5** + the P39 flagged-edge
  validator branch + the honest CONTRACT-boundary-vs-NARRATIVE-SEAM `e2e_note`.
- `data/workbench/bundles/*.json` — the 376 re-emitted with the predicate + mitigation field families.
- `vendor/aml-casework/**` (+ `VENDORED_AT`) — re-vendored 076fb8e→**04cc335** (Phase 20 C15/C4 reconcile,
  coverage 128→256; the kyc-sign 2→1 honest relaxation — a txn-bearing C14 MAY fail-closed at the
  narrative seam, "≥1 must sign" preserved; NOT a code regression).
- `evidence_requirements.py` + `data/workbench/evidence-requirements.json` BYTE-UNCHANGED (A1) — P39/P40
  enter as bundle DATA the engine already reads (line 310-312); the sufficiency rule byte-frozen.
- NO merge change (the merge-org class is one-sided AGAIN, sharper reason — P38's org fragments share no
  resolution handle with their base → 0 uphold candidates). `data/merge/cases.json`, `merge.html`,
  `dist/merge` all byte-frozen; build.py imports no spine/scorer/sibling/curate/casework.
- DOCS: the org-fragment-emit + northstar-evidence-emission briefs sharpened/re-pinned; trued-up
  `docs/cross-pillar-build-order.md` (substrate 294d3e5 / casework 04cc335); `CLAUDE.md`.

## Tests

- 8 zero-dep Node DOM-shim arcs unchanged except **workbench (178→184)** — the +6 Phase-82 tests
  (grounded-evidence panel, the `cleared` branch, the kyc-relaxation). corpus-explorer (303),
  news-stream (150), gate-console (68), triage-console (93), merge-console (74), chain, launcher.
- pytest umbrella (`uv run pytest`): **27** (stable).
- `--check all` 9/9 byte-frozen; build.py imports no spine/scorer/sibling/curate/casework (firewall clean).

## Dependencies

Offline ship artifacts: zero-dep, stdlib (Python 3.10). Live/companion tier: `markitdown` (gitignored .venv),
DuckDB (companion stores), optional local llama-cpp / openai backend. No runtime deps in the dists.

## Recent commits (Phase 82 impl not yet committed at snapshot time — orchestrator handles it)

- `b0893bd` docs: north-star-at-scale cross-pillar handoffs (substrate evidence emission + casework signing + build order)
- `202f174` chore(dev-wiki): close Phase 81 — delivery gate accepted (52c5d10)
- `52c5d10` Phase 81: Consume substrate Phases 35–37 (sanctions arc) — measure-first non-results → C17 exposure observable + briefs
- `a0896da` Phase 80: Consume substrate Phase 34 — OFAC name-collision merge class + non-tautological C14 §12 leg
- `cd44c6a` chore(dev-wiki): close Phase 79 — delivery gate accepted (031a33a)

## Related

- Prior `*-codebase-snapshot.md` for the full module/dependency maps (this summarizes the Phase-82 delta).
- [[phases/phase-82-consume-sibling-northstar-evidence-at-scale|Phase 82 — Consume sibling emissions: north-star evidence AT SCALE]]
- NOTE: `scripts/check-assumption-ledger.sh` is ABSENT in this project — the Phase-82 ledger revisit fill was
  verified manually (all 4 rows A1–A4 carry `revisit-status:` + a closing block-level note).
