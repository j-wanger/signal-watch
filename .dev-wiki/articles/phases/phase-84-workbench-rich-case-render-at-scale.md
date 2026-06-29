---
title: "Phase 84: Rich render at scale — surface the slice cases' emitted identity/network + re-sharpen the substrate decisiveness handoff"
aliases: ["phase-84", "rich-render-at-scale", "slice-render-parity"]
category: phases
tags: ["workbench", "companion", "render", "northstar", "cross-pillar", "adapter", "diagnostic"]
parents: ["phase-73-rich-investigation-case-live-workbench", "phase-82-consume-sibling-northstar-evidence-at-scale", "phase-83-merge-adjudicator-oracle-scored"]
created: 2026-06-29
updated: 2026-06-29
source: plan
status: completed
scope: ["scripts/serve_workbench.py", "workbench.html", "tests/workbench.test.mjs", "docs/substrate-northstar-evidence-emission-PLAN-BRIEF.md", "docs/rich-case-target-contract.md", "docs/cross-pillar-build-order.md", "CLAUDE.md", "HANDOFF.md"]
entry_criteria: "Phase 83 DELIVERED + accepted (impl db7e3ae). The user's complaint — workbench slice cases show coded counterparties, no case quality matches the northstar pair — DIAGNOSED this session (parallel code-verification of both pillars) as a STALE RENDER PATH in workbench.html, NOT a substrate emit gap, NOT a curation drop. The rich identity is already in the bundles (counterparty_name 372/376, related_parties[].display_name 56/56); the render reads the code."
exit_criteria: "T1 feasibility-probe go/no-go recorded. Slice cases render counterparty NAMES (ledger + money-flow with within-account/no-cross-account-ER honesty badge + resolution graph) + named BO with the multi-hop degradation marker. The substrate handoff brief re-sharpened to verified HEAD 3716f77 (Ask #3 measured-null, Ask #4 CLI-null); the stale SUB-1 'bare codes' claim trued. Companion-only: --check all 9/9 byte-frozen, evidence_requirements.py byte-unchanged, build.py imports nothing new, the 256/376 funnel unchanged. node tests/workbench.test.mjs green + serve_workbench --selftest PASS. Honesty swept (counts-only, synthetic-substrate-qualified, no catch-rate/lift/precision/recall)."
---

# Phase 84: Rich render at scale — surface the slice cases' emitted identity/network + re-sharpen the substrate decisiveness handoff

## Objective

Surface the rich identity/network the workbench slice cases ALREADY carry in their committed bundles
(real counterparty names, the entity/money-flow/resolution surface) — closing the case-quality gap
versus the hand-authored Northgate/Lakeshore pair — and re-sharpen the substrate handoff for the
DECISIVE half (FILE/CLEAR), which stays substrate-gated. Companion-only; all 9 ship dists byte-frozen.

## The diagnosis (measured this planning session)

The premise ("slice cases lack real counterparty names") is a **STALE RENDER PATH in `workbench.html`,
not an emit gap and not a curation drop** — verified by parallel code-level agents on both pillars:

1. **The data is emitted at scale.** `counterparty_name` in 372/376 bundles (≈89% of legs — e.g.
   `CASE-O-000000` txn[0] `"counterparty_name":"Lucas Ahmed"` beside `"counterparty_ref":"CP-O-000000-07"`),
   `counterparty_country`, `related_parties[].display_name` (56/56 bundles / 162 party rows),
   `ownership_pct`. aml-substrate has emitted these since ~its Phase 27/71 (HEAD verified `3716f77`).
2. **Curate + server carry it through.** `curate_workbench_cases.py` carries txns + `related_parties`
   whole (lines 277, 281); `serve_workbench.py` passes the bundle to the browser verbatim (lines 132-133).
3. **The DROP is at render.** The slice functions read the CODE: `txTable` (`workbench.html:580`) +
   `counterpartySummary` (`:556`) render `counterparty_ref || counterparty_account_id`; `boGraphHTML`
   (`:733,752`) reads `party_id`. The NORTHSTAR path (`scLedger`/`railFields`, `scBOGraph`+`scNameOf`)
   reads the NAME fields — the ONLY reason the 2 authored cases look rich. The rich `showcaseSurface`
   (`scMoneyFlowGraph`/`scResolutionGraph`/`scBOGraph`) is hard-gated to the 2 authored cases via
   `showcase:True`, set only in `casefile_list` (`serve_workbench.py:119`).

## Formal Spec

> Standard-ceremony spec captured in-article (no separate `/spec` round; the contract is fully
> determined).

**Objective.** (a) RENDER-PARITY: build a slice→showcase shape ADAPTER in `serve_workbench.case_detail`
and light `showcaseSurface` for slice cases (reusing the rich renderer), gated by a T1 feasibility
probe; if the probe fails, fall back to an in-place name fix only. (b) RE-SHARPEN the substrate
handoff brief to verified HEAD `3716f77`; true the stale SUB-1 claim.

**Scope.** `scripts/serve_workbench.py` · `workbench.html` · `tests/workbench.test.mjs` ·
`docs/{substrate-northstar-evidence-emission-PLAN-BRIEF,rich-case-target-contract,cross-pillar-build-order}.md`
· `CLAUDE.md` · `HANDOFF.md`. Companion-only — the workbench is NOT a build/dist target; build.py
imports none of it.

**Constraints (load-bearing).**
- Companion-only: `evidence_requirements.py`, all 9 ship dists (`build.py --check all` 9/9
  byte-identical), and the 256/376 casework signing funnel stay BYTE-UNCHANGED (the A1 guard + dist
  boundary). build.py imports nothing new.
- No determination/§12 change — this is RENDER.
- The adapter, NOT a one-line `showcase:True` flip (the slice bundle shape differs from the authored
  `case.json`); gated by the T1 probe (graceful degradation on heterogeneous slice data).
- Money-flow groups WITHIN-ACCOUNT / by-ref with an explicit honesty badge — substrate's counterparties
  are per-account-LOCAL synthetic names → NEVER imply cross-account ER (the >90%-FP discipline). No
  fuzzy name-matching in any new render.
- Multi-hop BO CHAIN degrades honestly to flat named BO with a "single-hop; multi-hop ownership chain
  pending substrate emission (Ask #4)" marker.
- Honesty governor: counts-only, synthetic-substrate-qualified, the word-ban (no
  catch-rate/lift/precision/recall) extends to the new render markers + the docs.
- Decisiveness (slice cases FILE/CLEAR like northstar) is explicitly OUT OF SCOPE — substrate-gated
  (Ask #3 = 2nd-leg measured-null, Ask #4 = ownership_edges CLI-null); the brief re-sharpen is the
  handoff.

**Exit criteria.** See `## Exit Criteria` below (bidirectional with tasks T1-T6).

**Assumptions.** See `## Assumptions` below; each has a stop-if-violated fallback.

## Scope

Files and modules affected (companion-only — NO ship/dist target):
- `scripts/serve_workbench.py` — the slice `case_detail` → showcase-shaped adapter + the feasibility probe
- `workbench.html` — light `showcaseSurface` for slice cases; the named ledger / money-flow + honesty
  badge / resolution graph / named BO + degradation marker; residual coded-table fallback to prefer the name
- `tests/workbench.test.mjs` — slice cases render NAMES not CP- codes; the honesty badge; BO display_name + marker
- `docs/{substrate-northstar-evidence-emission-PLAN-BRIEF, rich-case-target-contract, cross-pillar-build-order}.md`
- `CLAUDE.md`, `HANDOFF.md` — current-state true-up (replace in place; no per-phase bullet)

## Exit Criteria

- [x] T1 feasibility-probe go/no-go recorded — **GO; DISCOVERY: the adapter went CLIENT-SIDE** (`sliceShowcaseDetail`/`sliceNetworks` in `workbench.html`), NOT server-side via `showcaseSurface` (which would have stripped the §12 surface). See [[phase-84-adapter-gated-by-probe]].
- [x] The slice→showcase adapter — built client-side: `sliceShowcaseDetail` maps the flat bundle (`counterparty_name`→`counterparty{name,country,role}`; `related_parties[]`+`parties[]`→`entities[]` with `display_name`; flat `ownership_pct`→single-hop BO; `resolution_edges` passthrough) with code-fallback when `counterparty_name` absent; `serve_workbench.py` UNCHANGED (bundle already delivered whole)
- [x] Slice cases render counterparty NAMES (not CP- codes) in the ledger + a money-flow graph with name-labeled nodes + the within-account/no-cross-account-ER honesty note + a resolution graph from emitted edges
- [x] Slice BO nodes render `display_name` + the "multi-hop ownership chain pending substrate emission (Ask #4)" marker
- [x] The substrate handoff brief re-sharpened to verified HEAD `3716f77` (Ask #3 = Phase-41 measured-null; Ask #4 = CLI-null); the stale SUB-1 "bare codes" claim in `rich-case-target-contract.md` trued. (NOTE: the consume was recorded in the brief + contract docs; `cross-pillar-build-order.md` was not separately edited this session.)
- [x] Companion-only: `--check all` 9/9 byte-frozen; `evidence_requirements.py` git-diff empty; build.py imports nothing new; the 256/376 funnel unchanged
- [x] `node tests/workbench.test.mjs` green (184→195); `python3 scripts/serve_workbench.py --selftest` PASS (378 cases)
- [x] Honesty swept (no catch-rate/lift/precision/recall in the new markers/docs; synthetic qualifier held; the P84 word-ban assertion is green)

## Constraints

- Companion-only — prevents a ship/dist drift: the workbench is not a build target; all 9 dists stay byte-frozen.
- `evidence_requirements.py` UNTOUCHED — prevents conflating this RENDER phase with a §12 determination change.
- The 256/376 signing funnel byte-unchanged — prevents a stricter/looser detector slipping in under a render edit.
- No fuzzy name-matching + the within-account/no-cross-account-ER badge — prevents the >90%-FP ER discipline breach.
- Synthetic-substrate qualifier + the always-on badge held; honesty word-ban (no rate/lift/precision/recall) on any new copy/doc.

## Checkpoints

- After T1 (the feasibility probe): record the go/no-go. If the rich graphs do NOT degrade gracefully on
  the sampled heterogeneous slice data, STOP the adapter route and fall back to the in-place name fix only.
- Before any doc edit (T5): re-verify the substrate HEAD (`3716f77`) and the two Asks at the code level —
  the brief must cite a verified HEAD, not a loaded fact.

## Assumptions

- A1 [the measure-first gate] The rich graphs (money-flow, resolution, BO) degrade gracefully on real
  heterogeneous slice data (CASH/no-name legs ≈11%; no-related_parties bundles; single-owner BO). If false
  (the T1 probe fails): fall back to an in-place name fix only (`txTable`/`counterpartySummary` prefer
  `counterparty_name`); do NOT light `showcaseSurface`.
- A2 The slice's emitted `counterparty_name` density (≈89%) is sufficient for a credible money-flow render.
  If false: render only the named legs + an honest code-fallback for the rest (never fabricate a name).
- A3 The multi-hop BO chain is NOT reachable locally (0/376 `ownership_edges`, CLI-null at substrate HEAD
  `3716f77`). If false (re-measure live): a local multi-hop render becomes in-scope.
- A4 Decisiveness (slice cases FILE/CLEAR) is substrate-gated (Ask #3 measured-null / Ask #4 CLI-null) and
  OUT OF SCOPE. If false (substrate emits a 2nd leg): a determination phase opens — not this one.

## Notes

- The diagnosis corrects the stale SUB-1 claim in `rich-case-target-contract.md` ("counterparties are bare
  codes") — false since substrate Phase 27. See [[phase-84-render-drop-not-emit-gap]].
- The adapter reuses the rich GRAPH BUILDERS rather than rewriting the thin slice path. **DISCOVERY (impl):**
  the adapter went CLIENT-SIDE (`sliceShowcaseDetail`/`sliceNetworks` in `workbench.html`), NOT server-side via
  `showcaseSurface` — the existing slice surface is already a rich §12 investigation surface, so routing it
  through `showcaseSurface` would have stripped that §12 machinery; `serve_workbench.py` stayed untouched. See
  [[phase-84-adapter-gated-by-probe]].
- 2 of 3 rich graphs (money-flow, resolution) are locally reachable now; multi-hop BO is substrate-blocked
  (Ask #4: 0/376 ownership_edges in the CLI, verified `3716f77`). See [[phase-84-decisiveness-substrate-gated]].
- Names are honest only WITHIN-account/by-ref with the no-cross-account-ER badge — substrate names are
  per-account-local synthetic. See [[phase-84-names-honest-without-implied-ER]].
- Render is DECOUPLED from signing: 256/376 sign end-to-end (120 fail-close on C3 fan-in / C15 — casework-rooted).
  A rendered rich case need not be a signed one; this phase does not touch the signing funnel.
- Verification gates (toolchain confirmed this session): `node tests/workbench.test.mjs`;
  `python3 scripts/serve_workbench.py --selftest` (no .venv needed for the base selftest).
