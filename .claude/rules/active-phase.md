# Active Phase Context

**Phase 63 — *Investigator Case Workbench (capstone sales-pitch demo)*** (signal-watch-local, LITE) — DELIVERED 2026-06-21, READY FOR COMPLETION (delivery gate pending the commit). A companion-served investigator case workbench over a REAL (synthetic) aml-substrate alert POPULATION, walking clutter → clarity → live decisioning.

## Objective (DELIVERED)
`workbench.html` + `scripts/serve_workbench.py` (companion-only, NOT a 9th build/dist target — lite holds) over a 200-case deterministic slice vendored into `data/workbench/`, pinned aml-substrate@f90bd39 (`meta.synthetic:true`), produced via TOOL-USE / file-contract (build.py imports NO sibling — the Phase-62 pattern). RE-SCOPED post-gate to option B (USER OVERRIDE — A0 flipped → substrate-grounded real population VERIFIED feasible @f90bd39). Beats: clutter (real PartyView KYC + cross-account aggregation + txn detail + REAL counterparty edges; synthetic display identity over the real KYC) → signals-on clarity (grounding/corroboration; ZERO catch-rate number) → live finale (serve_chain → casework consume; default Claude, stub fallback). PLUS a thin pytest wrapper (USER OVERRIDE — `pyproject.toml` package=false + `tests/test_selftests.py` + `uv.lock`; NOT full py-init).

## The T4 finding → the fail-closed defensibility climax
Coverage is MEASURED (curate runs casework's stub over all 200 bundles → 57/200 sign end-to-end); composed cases fail on a real substrate↔casework C3/C15 replay divergence → the gate REFUSING → escalate-to-human. The verifier was NEVER loosened (abort rule held); the user accepted the framing. Precedent-confidence anchored to REAL firing frequency (gate funnel 129 auto-clear / 52 review / 19 human-gate); DISPOSITION direction stays ILLUSTRATIVE (the Phase-62 split).

## Scope
`workbench.html` · `scripts/{serve_workbench,curate_workbench_cases}.py` · `data/workbench/**` · `tests/{workbench.test.mjs,test_selftests.py}` · `pyproject.toml` · `uv.lock` · `docs/case-workbench.md` · `tests/smoke-checklist.md`. build.py NEVER imports aml_substrate/aml_casework.

## Key constraints
- Companion-only, off by default, scripted stub fallback; NO keys in the frontend (creds server-side, browser sends a backend NAME only — Phase-57 §4.5); synthetic data only (`meta.synthetic:true`, pinned @f90bd39); `--check all` 8/8 with ZERO dist drift.
- Coverage REAL/measured; dispositions label-blind ILLUSTRATIVE; the always-on "Illustrative data & outputs" badge stays; ZERO catch-rate/detection-lift number (the triple-null governs).

## Exit criteria (MET)
`uv run pytest` 17 passed; `build.py --check all` 8/8 ZERO dist drift; `tests/workbench.test.mjs` 61 assertions green; no sibling import in build.py; `data/workbench/cases.json` = 200 cases, coverage 57/200, pinned aml-substrate@f90bd39 / aml-casework@c6d8401; docs/case-workbench.md written.

## Abort (held)
build.py importing aml_substrate/aml_casework / any dist drift / a keys-token reaching the browser / a validator loosened to force the fit → STOP-and-surface. (All held: the T4 finding was surfaced + measured, never absorbed by loosening the gate.)

## Deferred follow-on phases
(1) C3/C15 cross-pillar contract alignment (substrate fan-IN vs casework fan-OUT C3 + C15 shell-threshold — a sibling-repo phase); (2) agentic tool-calling (OSINT / counterparty / network-ER); (3) the precedent-confidence GATING engine (the LFCM elicitation-loop path); (4) the substrate ownership/beneficial-owner graph emission.

## Gates
- [x] Direction confirmed by user (direction gate 2026-06-21, all_accept:true; RE-SCOPED post-gate to option B — A0 flipped → verified-revised-accept, all_accept now false)
- [x] Delivery accepted (post-implementation report 2026-06-21; framing accepted; committed a3fde1e)

Plan [[phases/phase-63-investigator-case-workbench]]; ledger Phase-63.
