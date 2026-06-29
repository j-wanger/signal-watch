---
title: "Phase 84: light the rich showcaseSurface for slice cases via a shape-adapter — gated by a feasibility probe"
aliases: ["adapter-gated-by-probe", "slice-to-showcase-adapter", "measure-first-render"]
category: decisions
tags: ["workbench", "render", "adapter", "measure-first", "companion", "reuse"]
parents: ["phase-84-workbench-rich-case-render-at-scale"]
created: 2026-06-29
updated: 2026-06-29
source: plan
confidence: high
---

## Context

Once diagnosed as a render drop ([[phase-84-render-drop-not-emit-gap]]), the question is HOW to surface
the emitted names. Two routes: (1) a minimal in-place fix to the thin slice renderers (`txTable` /
`counterpartySummary` prefer `counterparty_name`), or (2) reuse the rich northstar `showcaseSurface`
(`scMoneyFlowGraph` / `scResolutionGraph` / `scBOGraph` — names-not-codes + 3 graphs) for slice cases.
The rich surface is hard-gated to the 2 authored cases via `showcase:True`, set only in
`casefile_list` (`serve_workbench.py:119`). But it is NOT a one-line `showcase:True` flip — the slice
bundle shape (flat `counterparty_name`, `related_parties[]`+`parties[]`, flat `ownership_pct`) differs
from the authored `case.json` object shape `showcaseSurface` reads.

## Decision

**Reuse over duplication, but measure-first before committing the structural flip.** Build a
slice→showcase shape ADAPTER in `serve_workbench.case_detail` (flat `counterparty_name` →
`counterparty{name,country,role}`; `related_parties[]`+`parties[]` → `entities[]` with `display_name`;
flat `ownership_pct` → single-hop BO; `resolution_edges` passthrough) and light `showcaseSurface` for
slice cases — REUSING the rich renderer rather than rewriting the thin slice path.

GATE the gate-flip on a **T1 feasibility probe**: confirm `scMoneyFlowGraph` + `scResolutionGraph` +
`scBOGraph` degrade gracefully on real heterogeneous slice data BEFORE committing the flip. Edge cases
the probe must clear: ~11% of legs have no counterparty name (CASH/internal → code-fallback); some
bundles have no `related_parties`; a single-owner BO is degenerate. **If the probe fails, fall back to
an in-place name fix only.**

## Resolution (impl 2026-06-29) — the DISCOVERY: client-side, NOT server-side

The T1 probe resolved **GO**, but the design was REFINED from the planned SERVER-SIDE adapter (in
`serve_workbench.case_detail`, routing slice cases through `showcaseSurface`) to a **CLIENT-SIDE in-place
enrichment** (`sliceShowcaseDetail` / `sliceNetworks` in `workbench.html`). The probe surfaced that the
existing slice surface is ALREADY a rich §12 investigation surface (risk→KYC→counterparties→BO→audit-walk→
gather→determine→decide); piping it through the northstar `showcaseSurface` would have STRIPPED that §12
machinery and bolted on a file/cleared determination that slice cases don't have. The client-side adapter
reuses the sc* GRAPH BUILDERS (`scMoneyFlowGraph` + `scResolutionGraph`) via a small flat-bundle→sc*-readable
mapper, fixes the 3 coded renderers (`txTable`/`counterpartySummary`/`boGraphHTML`) in place, and leaves
`serve_workbench.py` UNTOUCHED (the bundle is already delivered whole — a Python shaping layer would just
duplicate it). The sc* builders degrade gracefully by construction (`if(!nm)return` / `if(!edges.length)return ''`)
— A1 HELD, no in-place-only fallback needed. Confidence raised medium→high: the reuse route was right and the
empirical degradation cleared cleanly; the only refinement was WHERE the adapter lives.

## Consequences

- Reuses the proven rich GRAPH BUILDERS (one builder set, the sc* functions) without re-routing the whole
  surface — the lesson is "reuse the builders, not the whole surface": before "reuse the rich renderer via an
  adapter," check what the existing surface already provides.
- The money-flow graph groups WITHIN-ACCOUNT / by-ref with an explicit honesty note — substrate
  counterparties are per-account-LOCAL synthetic names → never imply cross-account ER (see
  [[phase-84-names-honest-without-implied-ER]]).
- The multi-hop BO CHAIN degrades honestly to flat named BO with a "multi-hop ownership chain pending
  substrate emission (Ask #4)" marker — substrate-blocked, not a local defect.
- `serve_workbench.py` byte-unchanged; all 9 dists byte-frozen; `tests/workbench.test.mjs` 184→195.
