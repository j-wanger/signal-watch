# Active Phase Context

**Phase 65 — *Agentic tool-calling: the investigator evidence-gathering loop (companion)*** (signal-watch-local, LITE) — direction gate accepted 2026-06-21 (all_accept:true; A0/A2/A4 positioned explicitly, A1/A3 by precedent). Build signal-watch's FIRST multi-step tool-calling agent loop: on a selected investigator case, the agent proposes a tool → calls a deterministic tool over a COMMITTED SYNTHETIC evidence universe → each finding is GROUNDED-OR-STRIPPED (reusing news_ground) → grounded tool-evidence extends the case's grounding chain + a network view. Executed once live.

## Objective
Add a GATHER beat to the workbench arc (between SIGNALS and DECIDE). A companion agent loop (backend by NAME — Phase-57 §4.5; deterministic-STUB fallback so the demo runs model-free) gathers counterparty/OSINT/adverse-media evidence over a committed synthetic corpus; the reused `news_ground` gate disposes (a finding's claim ⊂ the tool's returned text; ungrounded findings DROP); grounded evidence extends the case grounding chain + feeds a `liveGraphLayout` network view. EXECUTE the loop ONCE live over a marquee exemplar (grounded + dropped evidence captured as delivery evidence — the measuring→controlling / execute-once pattern).

## Scope
`scripts/serve_workbench.py` · `workbench.html` · `data/osint/**` (new committed synthetic corpus) · `tests/{workbench.test.mjs,test_selftests.py}` · `docs/case-workbench.md` · `tests/smoke-checklist.md`. REUSE `news_ground` (grounding gate) + `liveGraphLayout` (pure-JS network layout) as LIBRARIES; do NOT import `news_store` (companion-doctrine — session-only, persists nothing). build.py NEVER imports aml_substrate/aml_casework; the OSINT corpus is companion data (NOT a build target → validated by a deterministic shape validator at serve_workbench load + `--selftest`, NOT in build.py).

## Key constraints
- THE HONESTY SEAM (load-bearing, A0): tools query COMMITTED SYNTHETIC data; the agent proposes, the deterministic gate disposes; ungrounded findings DROP; the consistency-not-correctness limit is surfaced honestly (badge on; ZERO catch-rate/detection-lift number). Fallback: network-ER over the existing committed counterparty edges only.
- Companion-only / NOT a 9th ship target / LITE holds; the loop is session-only / persists nothing (reuse `liveGraphLayout`, NOT the DuckDB `news_store`).
- BUILD-NEW agent loop (none exists — verified), BOUNDED: a fixed 2-3 deterministic tool set, capped iterations (the Phase-47 D3 max-iteration mandate), a deterministic-STUB fallback; agent runs server-side, browser sends a backend NAME only.
- 8 ship dists byte-frozen; `--check all` 8/8 ZERO dist drift; build.py never imports the siblings.

## Exit criteria
The 5 tasks' success fields met; the agent loop authored + the grounding seam HELD (grounded KEPT / ungrounded DROPPED, verified in `--selftest`); the GATHER beat in workbench.html (stage-completion reveal — never a token stream — evidence network, badge, both motion modes, XSS-escape); the loop EXECUTED ONCE live over a marquee case; `serve_workbench.py --selftest` + `node tests/workbench.test.mjs` + `uv run pytest` green; `build.py --check all` 8/8 ZERO dist drift; no sibling import; companion-only (NOT a 9th build target).

## Abort
If the live tool-evidence can't be kept honest over synthetic data (reads as "real OSINT" / a claim can't be grounded to its synthetic source) → fall back to network-ER over the existing committed edges only, report don't force (the A0 fallback). The live loop needs real debugging beyond creds → surface as a FINDING, ship the deterministic stub (the demo stays robust). Any new ship target / dist drift / a sibling import in build.py / a validator loosened to force a fit → STOP-and-surface.

## Gates
- [x] spec — waived under LITE ceremony (dev-plan Step 2 is a Lite skip; the assumption-ledger gate IS the direction gate)
- [x] Direction confirmed by user (assumption positions taken 2026-06-21; A0/A2/A4 explicit, A1/A3 by precedent; all_accept:true)
- [x] Delivery accepted (post-implementation report 2026-06-21; two adversarial passes [pre-build design + post-build code], all confirmed findings fixed; framing accepted; committed)

Plan [[phases/phase-65-agentic-tool-calling]]; ledger Phase-65.
