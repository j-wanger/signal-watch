---
title: "Phase 84 — Rich render at scale: surface the slice cases' emitted identity/network + re-sharpen the substrate decisiveness handoff (standard, planned+delivered same session)"
aliases: []
category: journal
tags: [workbench, render, companion, northstar, cross-pillar, adapter, diagnostic, honesty]
parents: [phase-84-workbench-rich-case-render-at-scale]
created: 2026-06-29
updated: 2026-06-29
source: debrief
duration: ~3h
---

# Phase 84 — Rich render at scale: surface the slice cases' emitted identity/network

## What Happened

- Closed a signal-watch-side RENDER DROP in the companion investigator workbench. The user's complaint
  ("the workbench still doesn't have real names for counterparties; no case quality matches the northstar
  cases") was DIAGNOSED this session via parallel code-verification of BOTH pillars as a **STALE RENDER PATH
  in `workbench.html`** — NOT a substrate emit gap, NOT a curation drop. The committed slice bundles
  (`data/workbench/bundles/CASE-*.json`) ALREADY carry `counterparty_name` (372/376 bundles ≈89% of legs),
  `counterparty_country`, `related_parties[].display_name` (56/56), `ownership_pct`; `curate_workbench_cases.py`
  carries them whole (lines 277,281); `serve_workbench.py` delivers the bundle verbatim (lines 132-133); only
  the slice render fns read the CODE (`txTable`:580 / `counterpartySummary`:556 → `counterparty_ref`;
  `boGraphHTML`:733/752 → `party_id`). The NORTHSTAR path read the names — the only reason the 2 authored
  cases looked rich.
- **The T1 feasibility probe resolved GO — but with a DISCOVERY that REFINED the design.** The plan called for
  a SERVER-SIDE adapter piping slice cases through the northstar `showcaseSurface`. The probe surfaced that the
  existing slice surface is ALREADY a rich §12 investigation surface (risk→KYC→counterparties→BO→audit-walk→
  gather→determine→decide); routing it through `showcaseSurface` would have STRIPPED that §12 machinery and
  bolted on a file/cleared determination slice cases don't have. So the adapter went **CLIENT-SIDE in
  `workbench.html`** (`sliceShowcaseDetail` flat-bundle→sc*-readable mapper + `sliceNetworks` reusing
  `scMoneyFlowGraph` + `scResolutionGraph`); the 3 coded renderers were fixed in place; `serve_workbench.py`
  was left UNTOUCHED (the bundle is already delivered whole — a Python shaping layer would just duplicate it).
  The sc* builders degrade gracefully by construction (`if(!nm)return` / `if(!edges.length)return ''`).
- Rendered the rich slice surface: named ledger (counterparty NAME + country, em-dash code-fallback on
  CASH/internal legs), the reused money-flow + resolution panels, a named BO graph (`display_name`, not
  `party_id`), all with an explicit "no cross-account entity resolution implied" honesty note (substrate
  counterparties are per-account-local synthetic names → the >90%-FP ER discipline applied to RENDER) and a
  "multi-hop ownership chain pending substrate emission" degradation marker.
- Re-sharpened the substrate handoff for the DECISIVE half (FILE/CLEAR), which stays substrate-gated: Ask #3
  (2nd corroborating leg) is a substrate Phase-41 MEASURED-NULL at HEAD `3716f77`; Ask #4 (`ownership_edges`)
  is CLI-null. Re-grounded `docs/substrate-northstar-evidence-emission-PLAN-BRIEF.md` + corrected the stale
  SUB-1 "bare codes" claim in `docs/rich-case-target-contract.md`.
- Companion-only throughout: all 9 ship dists byte-frozen (`--check all` 9/9), `evidence_requirements.py`
  byte-unchanged (git-diff empty), build.py imports nothing new, the 256/376 casework signing funnel
  unchanged. `tests/workbench.test.mjs` 184→195 (+11 P84 assertions); `serve_workbench --selftest` PASS
  (378 cases).

## Decisions Made

- [[phase-84-render-drop-not-emit-gap|The gap is a stale render path, not a substrate emit gap]] (high) — confirmed in impl.
- [[phase-84-adapter-gated-by-probe|Reuse the rich builders via an adapter, gated by a probe]] (medium→high) — RESOLVED with the client-side DISCOVERY.
- [[phase-84-decisiveness-substrate-gated|Slice cases LOOK like northstar but don't RESOLVE — decisiveness is substrate-gated]] (high) — confirmed.
- [[phase-84-names-honest-without-implied-ER|Surface names within-account, never imply cross-account ER]] (high) — confirmed.

## Problems Solved

- The "missing data" premise — overturned by diagnosing the FULL pipeline (emit→curate→serve→render) before
  blaming upstream; the data was present at every stage, dropped only at render. The stale sibling doc
  (`rich-case-target-contract.md` SUB-1, pinned at a 3-week-old substrate commit) had asserted the emit gap.
- The planned server-side adapter would have stripped the §12 surface — caught at the T1 probe, redesigned to
  a client-side in-place enrichment that reuses the graph builders without re-routing the whole surface;
  `serve_workbench.py` stayed untouched.

## Artifacts Changed

- `workbench.html` (slice render reads `counterparty_name`/`display_name` with code-fallback; NEW
  `sliceShowcaseDetail` + `sliceNetworks` client adapter reusing `scMoneyFlowGraph`/`scResolutionGraph`;
  `boGraphHTML` single-hop/multi-hop-pending degradation marker; new `.cpcc` CSS for the counterparty country)
- `tests/workbench.test.mjs` (184→195: names render, code-hidden, country, CASH-leg fallback, money-flow +
  resolution panels, honesty note, multi-hop degradation marker, honesty word-ban)
- `docs/substrate-northstar-evidence-emission-PLAN-BRIEF.md` (re-grounded to HEAD `3716f77` — Ask #3
  measured-null, Ask #4 CLI-null)
- `docs/rich-case-target-contract.md` (stale SUB-1 "bare codes" claim trued)
- `CLAUDE.md` + `HANDOFF.md` (current-state trued in place; no per-phase bullet)
- `scripts/serve_workbench.py` UNCHANGED (the DISCOVERY — the adapter went client-side); `evidence_requirements.py` byte-unchanged

## Related

- [[phase-84-workbench-rich-case-render-at-scale|Phase 84 — Rich render at scale]] — parent phase
- [[phase-73-rich-investigation-case-live-workbench|Phase 73]] — authored the northstar pair + `showcaseSurface` (the builders Phase 84 reuses)
- [[phase-82-consume-sibling-northstar-evidence-at-scale|Phase 82]] — the grounded-evidence consume this builds on

## Soft Observations / Phase N+1 Candidates

- The workbench's signal-watch-LOCAL render/consume frontier is now largely CLOSED. The next case-quality
  lever — DECISIVENESS (FILE/CLEAR at scale), the SUB-1-remainder per-rail email/phone, SUB-4 cross-account
  counterparty resolution, the multi-hop ownership chain — is SUBSTRATE-gated. | Phase 85 candidate: either
  (a) a substrate emission consume once the open-reference-data fork / a discriminating corroboration signal
  lands, or (b) a non-consume direction. | Evidence: `docs/substrate-northstar-evidence-emission-PLAN-BRIEF.md`
  (Ask #3 measured-null, Ask #4 CLI-null), `docs/rich-case-target-contract.md` SUB-1/SUB-4.
- Possible signal-watch-side follow-on (deferred): route slice cases through the full determination panel
  HONESTLY (showing needs_more_info), so the §12 verdict is visible on the bulk cases — needs careful honest
  framing (most slice cases don't resolve). | Evidence: this session's decisiveness-out-of-scope boundary.
