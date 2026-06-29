# Active Phase Context

**Phase 84 — *Rich render at scale: surface the workbench slice cases' emitted identity/network + re-sharpen the substrate decisiveness handoff*** (signal-watch-local, STANDARD, companion-only RENDER) — DELIVERED 2026-06-29, READY FOR COMPLETION (all 6 tasks [x], exit criteria met). The "no counterparty names" gap was DIAGNOSED as a STALE RENDER PATH in `workbench.html` — NOT a substrate emit gap, NOT a curation drop; the rich identity was already in the bundles. DISCOVERY: the adapter went CLIENT-SIDE (`sliceShowcaseDetail`/`sliceNetworks` in `workbench.html`), NOT the planned server-side `showcaseSurface` route (which would have stripped the existing §12 surface); `serve_workbench.py` untouched.

## Objective
Surface the rich identity/network the slice cases ALREADY carry in their committed bundles (real counterparty names, money-flow + resolution surface) — closing the case-quality gap vs the hand-authored Northgate/Lakeshore pair — via a CLIENT-SIDE slice→sc*-builder adapter in `workbench.html` (reusing `scMoneyFlowGraph`/`scResolutionGraph`). And re-sharpen the substrate handoff for the DECISIVE half (FILE/CLEAR), which stays substrate-gated. Companion-only; all 9 ship dists byte-frozen.

## Scope (file globs)
`scripts/serve_workbench.py` · `workbench.html` · `tests/workbench.test.mjs` · `docs/substrate-northstar-evidence-emission-PLAN-BRIEF.md` · `docs/rich-case-target-contract.md` · `docs/cross-pillar-build-order.md` · `CLAUDE.md` · `HANDOFF.md`

## Key constraints
- Companion-only / dist boundary: ALL 9 ship dists BYTE-FROZEN (`--check all` 9/9 — the workbench touches NO dist); `evidence_requirements.py` UNTOUCHED (this is RENDER, not §12); the 256/376 casework signing funnel byte-unchanged (render is decoupled from signing).
- build.py imports NO companion module (serve_workbench/curate/casework/spine — grep guard).
- Adapter, NOT a one-line `showcase:True` flip (the slice flat shape differs from the authored `case.json`); GATED by the T1 feasibility probe — if the rich graphs do NOT degrade gracefully on heterogeneous slice data, fall back to an in-place name fix only.
- Names honest WITHIN-account/by-ref with a no-cross-account-ER badge (per-account-local synthetic names → never imply ER; no fuzzy name-matching, the >90%-FP discipline); multi-hop BO degrades to flat named BO + an "Ask #4 pending" marker; never fabricate a name where `counterparty_name` is absent (code-fallback).
- Honesty: counts-only; the synthetic-substrate qualifier on every number; the word-ban (no catch-rate/lift/precision/recall) extends to the new render markers + the docs.
- Decisiveness (slice cases FILE/CLEAR like northstar) is OUT OF SCOPE — substrate-gated (Ask #3 = 2nd-leg measured-null, Ask #4 = ownership_edges CLI-null); the brief re-sharpen is the handoff.

## Exit criteria
T1 feasibility-probe go/no-go recorded; the slice→showcase adapter in `case_detail` (counterparty{name,country,role} + entities[] display_name + resolution_edges passthrough + single-hop BO, code-fallback when name absent); slice cases render NAMES not CP- codes (ledger + money-flow with the no-cross-account-ER badge + resolution graph + named BO + the "Ask #4 pending" marker); the substrate brief re-grounded to HEAD `3716f77` (Ask #3 measured-null, Ask #4 CLI-null) + the SUB-1 "bare codes" claim trued + the consume noted in `cross-pillar-build-order.md`; `--check all` 9/9 byte-frozen + `evidence_requirements.py` git-diff empty + the 256/376 funnel re-asserted unchanged; `node tests/workbench.test.mjs` green + `python3 scripts/serve_workbench.py --selftest` PASS; honesty swept; CLAUDE.md + HANDOFF trued IN PLACE (no per-phase bullet).

## Abort rule
Any unsanctioned dist drift (any of the 9 not byte-identical) / an `evidence_requirements.py` change / a build.py companion import / a change to the 256/376 funnel / any render implying cross-account ER (no fuzzy match; badge mandatory) / a fabricated counterparty name / any count presented as a catch-rate/lift/precision/recall → STOP-and-surface. Measure-first: the T1 probe gates the adapter route (fail → in-place name fix only). DECISIVENESS stays OUT OF SCOPE. If blocked >3 attempts: ask user — skip or abort.

## Gates
- [x] spec (`## Formal Spec` IN the phase article [[phases/phase-84-workbench-rich-case-render-at-scale]] — standard ceremony, no separate /spec round; the contract is fully determined)
- [x] Direction confirmed by user (2026-06-29, AskUserQuestion two rounds — 4 surfaced assumptions taken as accept-all positions: scope = render-parity, decisiveness = re-sharpen-the-brief; all_accept tracked, NOT silent; ledger Phase-84)
- [x] Delivery accepted (2026-06-29 — delivery report accepted; impl + debrief committed `a3e669a`, pushed to main; all 9 dists byte-frozen, workbench tests 184→195, `evidence_requirements.py` unchanged)

Decisions [[decisions/phase-84-render-drop-not-emit-gap]] · [[decisions/phase-84-adapter-gated-by-probe]] · [[decisions/phase-84-decisiveness-substrate-gated]] · [[decisions/phase-84-names-honest-without-implied-ER]]; plan [[phases/phase-84-workbench-rich-case-render-at-scale]]; ledger Phase-84.
