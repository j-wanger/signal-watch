---
title: "Phase 84: the 'no counterparty names' gap is a STALE RENDER PATH, not a substrate emit gap"
aliases: ["render-drop-not-emit-gap", "counterparty-names-render-bug", "SUB-1-stale"]
category: decisions
tags: ["workbench", "render", "diagnosis", "cross-pillar", "northstar", "companion"]
parents: ["phase-84-workbench-rich-case-render-at-scale"]
created: 2026-06-29
updated: 2026-06-29
source: plan
confidence: high
---

## Context

The user's complaint: "the workbench still doesn't have real names for counterparties; no case
quality matches the northstar cases." Three candidate causes had to be distinguished before any fix:
(a) a substrate EMIT gap (the names were never produced upstream), (b) a CURATION drop
(`curate_workbench_cases.py` discarded them), or (c) a local RENDER gap (the data arrives but the
browser never paints it). The fix and the cross-pillar handoff diverge completely by cause — an emit
gap routes to substrate; a render gap is signal-watch-local and shippable now.

## Decision

Diagnosed (parallel code-verification of BOTH pillars) as **(c) a stale render path in
`workbench.html`** — high confidence, verified at the code level:

- The committed slice bundles ALREADY carry the rich identity: `counterparty_name` in 372/376 bundles
  (e.g. `CASE-O-000000` txn[0] `"counterparty_name":"Lucas Ahmed"` beside
  `"counterparty_ref":"CP-O-000000-07"`), `counterparty_country`, `related_parties[].display_name`
  (56/56 bundles / 162 party rows), `ownership_pct`. aml-substrate has emitted these since ~its
  Phase 27/71 (HEAD verified at `3716f77`).
- `curate_workbench_cases.py` carries txns + `related_parties` through whole (lines 277, 281);
  `serve_workbench.py` passes the bundle to the browser verbatim (lines 132-133).
- The DROP is at render: the slice functions read the CODE — `txTable` (`workbench.html:580`) +
  `counterpartySummary` (`:556`) render `counterparty_ref || counterparty_account_id`;
  `boGraphHTML` (`:733,752`) reads `party_id`. The NORTHSTAR path (`scLedger`/`railFields`, `scBOGraph`
  + `scNameOf`) reads the NAME fields — the ONLY reason the 2 authored cases look rich.

This **corrects the stale SUB-1 claim** in `docs/rich-case-target-contract.md` ("counterparties are
bare codes") — false since substrate Phase 27.

## Consequences

- The fix is signal-watch-local and shippable this phase (companion-only, no substrate dependency for
  the name surface). The render-drop is the smoking gun, not an upstream gap.
- Two of three rich graphs (money-flow from `counterparty_name`, resolution from `resolution_edges`)
  are locally reachable NOW; only multi-hop BO is genuinely substrate-blocked (Ask #4 ownership_edges,
  CLI-null) — see [[phase-84-decisiveness-substrate-gated]].
- "Verify the CONTENT, not the 'wrote' log" (Phase-79 lesson) applied in reverse: a parallel
  code-level read of both pillars overturned a premise that read as an emit gap.
- CONFIRMED in impl (2026-06-29): the names render with a workbench.html-only fix (`tests/workbench.test.mjs`
  184→195 — slice transactions show the counterparty NAME, the CP- code is hidden when a name is present);
  `serve_workbench.py` + `evidence_requirements.py` + all 9 dists byte-unchanged. The diagnosis held.
