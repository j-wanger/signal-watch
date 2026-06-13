---
title: Phase 50 — AML program build kickoff (data-substrate pillar spun out)
date: 2026-06-13
phase: 50
tags: [program-build, spin-out, aml-substrate, synthetic-data, emergence]
---

# Phase 50 — The demo became the program

A major user REFRAME at the dev-plan gate: stop building incremental signal-watch ship artifacts;
build the **real AML program** the blueprint designed (§3 design-stage workloads → real systems),
**one real-system-class repo per pillar**. signal-watch becomes the program-architecture home; the
build moves to sibling repos. Pillar 1 = the **data substrate** → `/Users/jwang/aml-substrate`
(Python). Its phases are tracked in that repo (DESIGN.md + docs/phase-*.md) — the `/dev-*` skills
don't operate cross-repo.

## How the design was grounded

Interview (Jake's institutional knowledge) + **3 parallel research agents** (synthetic-AML
generators · real field-level schemas · distributions/topology/benchmarks). Adopted: AMLworld's
virtual-world emergent method + transitive labeling; ISO 20022 / Interac e-Transfer / Payments
Canada Std 005–007 / FINTRAC STR-LCTR-EFTR schemas; log-normal+Pareto amounts re-anchored to
Canadian medians + Hawkes temporal. Captured in `aml-substrate/DESIGN.md` with cited sources.

## Gate (Phase 50, all_accept: false)

A1 foundation-first / emergence-ready ACCEPT · A2 build-on-research (user OVERRODE the offered
review-first checkpoint) · A3 1M-scale REJECT → parameterized small-first · A4 hybrid eyes-open →
DEFERRED to phase-2's flow engine. Ledger: Phase-50 block, revisit-status filled at Phase-1 delivery.

## Delivered (in aml-substrate)

- **Phase 1 — Foundation** (commits 44ad9b1→9256dc5, 54 tests): canonical data model w/ inert
  emergence hooks · deterministic population + KYC graph (15 Canadian archetypes, PEP 0.5% / HR 2%
  / active 60%) · 6-channel background transaction engine (Hawkes seasonality, Canadian channel
  medians, round-number snapping) · net-new **EMT** channel detail · parquet + realism report.
  Scale **~161s/1M linear**, byte-identical regen, Benford-clean 0.001 baseline.
- **Phase 2 — Emergence** (commits 42b0c17→5632816, 83 tests total): criminal/mule/shell
  designation (hidden ground-truth only — **no KYC label leak**) · fresh-Python laundering behavior
  engine (structuring → funnel → layering → shell, margin skim) · transitive taint labeling
  (bounded; ground-truth cases) · coverage checklist (6/7; **cycle honestly uncovered**) · the **A1
  permutation-null separability gate** (passes clean, fires on an injected artifact) · emergence
  realism. Class imbalance calibrated to **1:21,657 @100k**; structuring breaks Benford 0.18>0.01.

## Process note (high-signal)

Jake caught that the first Phase-2 "assumptions" were **direction choices mislabeled as
assumptions** — a real assumption is a falsifiable belief with an "if-false" consequence, per the
prior phases' ledger. Re-ran a proper gate: A1 (emergent-not-stamps) took a DON'T-KNOW → defended +
**down-scoped to the separability gate**. That gate then earned its keep by catching *its own naive
version* — a fixed 0.20 threshold failed at 1:5462 imbalance (sampling noise), forcing the
statistically-honest permutation-null design. Down-scope-to-measured > argue-it's-fine.

## signal-watch state

Tidied to Phase-50 (program-architecture home): `_CURRENT_STATE`, `active-phase.md`, the ledger
Phase-50 block. All 5 ship artifacts + dists FROZEN (no further demo-track work unless re-opened).

## Soft Observations / Phase N+1 Candidates

- **Phase 3 — FINTRAC reporting + alert/case monitoring layer**: signals fire over the labelled
  substrate → grounded alerts (the §3 monitoring workload); the A2 grounding chain (alert cites
  signal + data) becomes real. The natural next pillar phase.
- **Cross-repo lifecycle**: aml-substrate has no dev-wiki; its phases live in DESIGN.md + docs/. If
  the program grows, consider running `/dev-init` from a session rooted there for full parity.
- **Coverage tail**: `cycle` typology is uncovered by the behavior engine (honest). If a detection
  use-case needs it, add a cycle/round-trip strategy — but only as a real behavior, never a stamp.
- **Per-criminal deposit volume**: $50k–$500k income → up to ~59 structuring deposits/criminal; at
  1:21,000 this means very few criminals. Fine, but worth a calibration helper if tuning gets fiddly.
