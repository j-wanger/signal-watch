# Active Phase Context

**Phase 64 — *Precedent-confidence gating engine + the elicitation loop (live)*** (signal-watch-local, LITE) — direction gate accepted 2026-06-21 (all_accept:true). Turn the Phase-63 workbench's STATIC precedent-confidence bucketer into a LIVE, parameterized gating CONTROL + the LFCM elicitation loop, executed once over the 200-case slice.

## Objective
Lift the static `_confidence(combo, n_precedent)` (hardcoded 500/50 + cleared-% 88/62/28 in `curate_workbench_cases.py`; 129/52/19 funnel baked into cases.json) into a visible `gating_policy` + a pure `route(confidence, sample_size, policy)`; APPLY the decision (auto-clear → illustrative disposition; human-gate → escalate); add the session-only ELICITATION LOOP (adjudicate → grow precedent → recompute → re-route, persists nothing); EXECUTE ONCE live over the real 200-case slice (funnel re-derived + the loop shifting one decision).

## Scope
`workbench.html` · `scripts/serve_workbench.py` · `scripts/curate_workbench_cases.py` · `tests/{workbench.test.mjs,test_selftests.py}` · `docs/case-workbench.md` · `tests/smoke-checklist.md` (build.py NEVER imports aml_substrate/aml_casework).

## Key constraints
- Companion-only / NOT a 9th ship target / LITE holds; the loop is session-only / persists nothing.
- THE §12-routing / §14-illustrative-disposition seam (load-bearing): route on REAL firing frequency; dispositions stay ILLUSTRATIVE; NO §14 re-grounding from probe-history (the Phase-62 boundary).
- Records byte-frozen / recompute from cases.json (n_precedent stored); no substrate re-emit, no sibling import.
- Always-on "Illustrative data & outputs" badge; ZERO catch-rate/detection-lift number; `--check all` 8/8 ZERO dist drift.

## Exit criteria
The 5 tasks' success fields met; `--check all` 8/8 ZERO dist drift; no sibling import; the engine EXECUTED ONCE live.

## Abort
If the live loop can't be kept honest over illustrative dispositions (reads as "learns correct answers") → scope to display-only batch routing, report don't force (the A0 fallback). Any new ship target / dist drift / sibling import in build.py / a validator loosened to force a fit → STOP-and-surface.

## Gates
- [x] spec — waived under LITE ceremony (dev-plan Step 2 is a Lite skip; the assumption-ledger gate IS the direction gate)
- [x] Direction confirmed by user (assumption positions taken 2026-06-21, all_accept:true)
- [x] Delivery accepted (post-implementation report 2026-06-21; framing accepted; committed)

Plan [[phases/phase-64-precedent-confidence-gating-engine]]; ledger Phase-64.
