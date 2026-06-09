---
title: "Phase 37 — Per-indicator typology (corpus Typologies lens)"
date: 2026-06-08
type: journal
phase: phase-37-per-indicator-typology
tags: [corpus, typology, typologies-lens, fintrac, overlay, measure-first, cross-corpus-synthesis, deterministic]
---

# Phase 37 — Per-indicator typology

## What shipped

The corpus Typologies lens now groups by **indicator** typology, not document. A multi-typology FINTRAC
sector page distributes across the real typology clusters instead of collapsing into a catch-all.
`corruption` (293 ind / 11 docs) and `terrorist-financing` (169 ind / 14 docs) are now **cross-jurisdiction
US+Canada** clusters drawing indicators from the FINTRAC sector pages; the `fintrac-sector-baselines`
catch-all is **retired**, replaced by an honest `cross-cutting-indicators` bucket (746 ind) for the
genuinely generic remainder. Per-indicator typology rides in a NEW sparse overlay
`data/indicator-typology-map.json` (350 deterministic corruption/TF assignments; everything else inherits
its doc typology at build time) — **all 56 derived records + `derive_signals.py` stay byte-frozen**.

## How it got here (the reframe chain)

The user invoked /dev-plan over the queued candidates (live-mode verify / 3rd jurisdiction / demo-the-loop)
and reframed THREE times, each sharper: "FINTRAC completeness?" → "the suspicious-transaction-indicators
section?" → "why only 7 docs under the FINTRAC guidance typology?". Investigation disproved the literal
premise (the 11 per-sector indicator pages are complete + fully extracted; the STR/sanctions guidance pages
enumerate nothing) but found the spirit right: the "7" was the `fintrac-sector-baselines` catch-all CLUSTER
(7 of 10 docs), because a doc→one-typology overlay can't place an inherently multi-typology sector page.
The user chose the PROPER fix (per-indicator typology) over a lite relabel and over adding the /intel/
special-bulletin scale (both offered, both deferred).

## The measure-first payoff (the headline)

The T1 probe earned its keep twice:
1. It caught a bug in my own section→typology classifier (`\btf\b` matched the generic "ML/TF" prefix,
   inflating "typology-clean" to a bogus 95%). Corrected: **27% clean / 73% cross-cutting**.
2. The user chose Model C (deterministic floor + bounded neural rescue). Measuring the rescue surface
   BEFORE building it: only 8 of 377 residual unique texts even mentioned a specific typology, and on
   inspection all 8 were generic risk-jurisdiction boilerplate → **0 genuine rescues**. So **C converged to
   A**: the whole assignment is deterministic (350 corruption/TF by source SECTION heading), no workflow, no
   neural pass, nothing to agreement-verify. The planned [L] T2 dissolved into a deterministic step.

This is the project's grain working as intended — measurement before optimization, deterministic validators
over neural judges, the subtraction test killing a neural pass that measured to worthless.

## Health Delta

- corpus harness: 235 → **239** assertions (+5 Phase-37 assertions: catch-all retired, cross-cutting bucket,
  corruption+TF clusters, sector page distributes ≥3 typologies, corruption draws from multiple sector pages;
  −1 removed the old `fintrac-sector-baselines` cluster assertion).
- news harness: 76 (unchanged, frozen). derive `--selftest`: PASS (grounding core untouched).
- `--check all`: 5/5 zero drift (3 typology dists + dist/news byte-identical; dist/corpus = new baseline).

## Escape hatches

- **DISCOVERY** — the planned neural assign/verify (T2 as an [L] workflow with inter-rater agreement) was
  dissolved by the T1 measurement: per-indicator typology is 27% deterministic (section heading) + 73%
  honestly-cross-cutting, and the bounded neural rescue measured to 0. Executed Model C faithfully; it
  converged to A. No agreement rate to report (nothing neural) — documented in `.dev-wiki/tmp/ph37_probe.md`.

## Soft Observations / Phase N+1 Candidates

- The derivable FINTRAC /intel/ frontier (OA001 tax-evasion-real-estate + sanctions-evasion SB +
  Russia-linked-ML SB + dual-use advisory) — genuine source scale, the Phase 22/23 extend pattern; offered + deferred.
- A third jurisdiction (AUSTRAC CC BY / UK OGL) — the standing scale frontier now the Canadian source frontier
  is exhausted; would also make `cross-cutting-indicators` cross-jurisdiction.
- The live-mode `call_llm` verification gap (stubbed across Phase 35/36) — still open; a recorded-fixture
  integration test would close it.
- A watchlist-management VIEW (it only grows — no UI to view/prune).
