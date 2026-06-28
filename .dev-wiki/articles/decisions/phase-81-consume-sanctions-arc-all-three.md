---
title: "Phase 81: Consume the FULL substrate sanctions arc (P35 org-collision + P36 exposure leg + P37 geo); the open-sanctions thread is plan-only"
aliases: [phase-81-consume-all-three, sanctions-arc-full-consume]
category: decisions
tags: [cross-pillar, consume, substrate, sanctions-screening, ofac, org-name-collision, c17-exposure, geo, open-sanctions, license, ceremony]
parents: [phase-81-consume-substrate-sanctions-arc]
created: 2026-06-28
updated: 2026-06-28
source: plan
confidence: medium
---

# Decision — consume the full substrate sanctions arc; open-sanctions plan-only

## Context

aml-substrate is **3 phases ahead** of signal-watch's Phase-34 pin (`1f5901e` → HEAD `f7fbdb0`,
code-verified LIVE this session). The delta is a coherent **sanctions arc**: Phase 35 (`4f49e53`) makes
the dead `Organization.sanctions_flag` LIVE under `--anchored` via a label-blind real-OFAC-SDN **org**
name collision (the org sibling of what signal-watch's Phase 80 consumed for persons); Phase 36
(`1651b1e`) adds the C17 exposure-via-ownership leg (a corroborating determination leg fired when a
customer's beneficial owner / controlled entity carries a `sanctions_flag`); Phase 37 (`5b5cf32`) enriches
geo (`counterparty_country` `{US,CA}` → 22 countries with a FATF high-risk tail, observable-only). The
question at the direction gate: which slice of the arc to consume, and how far to push the open-sanctions
data thread (real cross-jurisdiction sanctions data). The minimal A1-clean move is P35-only (the merge
org-collision class, the direct sibling of Phase 80, with no profile change). casework (`076fb8e`) is
unchanged and does NOT ground C17. Substrate **CUT** the old P35-brief asks (TF / broader-C7) and retains
them as honest-null artifacts — those asks are dead.

## Decision

Consume the **FULL substrate sanctions arc** — P35 org name-collision + P36 the C17 exposure leg + P37
geo — not the minimal A1-clean P35 sibling alone:

- **MERGE CONSOLE** — add an OFAC **org-name** collision case class (the person-class's org sibling),
  scored against substrate's non-circular `GT-<hash>` oracle, MEASURE-FIRST gated.
- **WORKBENCH §12** — consume the C17 exposure-via-ownership leg as a new EVIDENCE atom so a customer with
  a sanctioned BO + a distinct ML mechanism genuinely reaches the determination bar (see
  [[decisions/phase-81-exposure-leg-evidence-advance]]); plus render P37's richer geo observable (no leg).
- **OPEN-SANCTIONS** — a **PLAN-ONLY** brief: a per-source license/compliance matrix + the non-commercial
  boundary + what substrate should emit (Stage-2/3 open reference data). The data work is substrate-side.

The open-sanctions thread is plan-only because **OpenSanctions is CC-BY-NC** — no-ship: the demo's
buy-in purpose is arguably commercial, so the non-commercial licence does not cover it. The clean ship
path is the **public-domain / open-gov source lists** (the existing OFAC SDN under 17 USC §105); no
CC-BY-NC bytes enter the repo (ship or companion) this phase.

Rationale: the exposure leg is the higher-value §12-breadth beat (a customer reaches the bar via genuinely
independent legs — the program thesis), and P37 geo is cheap richness; bundling all three under one
STANDARD phase keeps cross-pillar coherence and amortizes the regate, the Phase-77/79/80 precedent.
Direction gate: Q1 "All three (+ P37 geo)" + Q2 "Plan-only brief + license matrix" (AskUserQuestion
2026-06-28); Q3 the bar invariant is covered in [[decisions/phase-81-exposure-leg-evidence-advance]].

**Alternatives rejected.** (a) **P35-only** (the minimal A1-clean sibling, deferring the exposure leg +
geo) — Jake picked the higher-value exposure leg + geo; P35-only under-uses an arc that lights three
surfaces and leaves the §12-breadth beat unbuilt. (b) **Integrate a real cross-jurisdiction sanctions
dataset now** — plan first, to contain licensing risk; OpenSanctions' CC-BY-NC makes a live integration a
compliance hazard for a buy-in demo, and the data work properly belongs substrate-side.

## Consequences

The merge org-collision class is behind its T1a measure-first abort gate (one-sided → workbench-only + a
substrate org-emit-two-sidedness brief). The exposure leg is behind its T1b gate (degenerate → a rendered
observable + a brief). The P37 geo render + the open-sanctions brief + the true-ups land unconditionally.
STANDARD ceremony stands (cross-pillar arc + a conditional ship-dist touch + an L task). `dist/merge` is
the ONE sanctioned, gated re-freeze (its 3rd consecutive); the 8 non-merge dists stay byte-frozen; the
A1 guard holds (`evidence_requirements.py` byte-unchanged); the firewall holds (build.py imports no
spine/scorer/sibling/curate). Real OFAC **org** names ship clean under 17 USC §105, framed STRICTLY as the
false-positive trap (the synthetic org ≠ the sanctioned entity). The open-sanctions brief names the clean
ship path (public-domain / open-gov lists) and parks the CC-BY-NC integration as substrate-side work — the
real cross-jurisdiction sanctions data remains a future thread, not a foreclosed one.

Related: [[phase-81-consume-substrate-sanctions-arc]] ·
[[decisions/phase-81-exposure-leg-evidence-advance]] ·
[[decisions/phase-80-merge-plus-workbench-consume]] ·
[[decisions/phase-79-merge-supersede-substrate-scored]] · `docs/cross-pillar-build-order.md`.
