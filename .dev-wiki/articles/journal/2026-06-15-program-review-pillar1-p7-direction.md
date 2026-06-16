---
title: Program review of pillar-1 (aml-substrate P1–P6) + P7 direction set
date: 2026-06-15
type: journal
phase: phase-50-aml-program-build
tags: [aml-substrate, program-review, pillar-1, p7-direction, cross-pillar]
mode: quick-debrief
---

# Program review of pillar-1 (aml-substrate P1–P6) + P7 direction set

Cross-pillar review conducted from the signal-watch program-architecture home (no signal-watch code
changed; the work output landed in aml-substrate). An 18-agent review workflow + deterministic
verification assessed aml-substrate's delivered state against DESIGN.md, the program blueprint, and an
open-tooling dossier; the user then set pillar-1's next direction and chose to hand the actual
planning/implementation to an aml-substrate-rooted session.

## What happened

- **Verified state:** aml-substrate **P1–P6 all delivered** (P6 closed Gate 2 at `ad96c16`) — far
  past what this repo's lifecycle record said ("Active: Phase 3"). 239 tests green; `gen/` freeze
  byte-stable; the standout asset is P6's measured negative finding (entity resolution ⊥ laundering
  structure; the cross-account unit is the case/network).
- **Real findings (code-verified):** (1) `counterparty_ref` carries a recoverable case-id leak
  (`gen/flows.py:95`; 5/5 cases recovered from the ref alone) — latent today, a landmine for any
  future graph baseline; (2) the freeze has NO positive guard and `ruff-format` (write-in-place,
  no `gen/` exclude) is one `git add` from silently corrupting frozen `gen/` — the hazard already
  materialized once; (3) DESIGN §6 temporal spec (Hawkes + dormancy/burst) outruns the code
  (memoryless Poisson), missing a deferred marker.
- **Direction set (user):** next phase = **Observable network linkage** (the keystone `gen/`
  unfreeze + re-baseline: populate `counterparty_account_id` + a mirrored credit leg on laundering
  AND legit internal transfers; extend the A1 separability gate; fix the ref leak; re-baseline under
  a new positive freeze guard) — chosen over (b) substrate→program loop closure and (c)
  honesty-infra hardening-only.
- **Handoff:** planning/implementation handed to an aml-substrate-rooted session (its dev-* hooks +
  assumption gate bind there). Pre-staged brief written:
  `aml-substrate/docs/phase-7-observable-network-PLAN-BRIEF.md` (code-verified facts, unfreeze/
  re-baseline contract, six cost-sorted assumptions with if-false consequences, a 7-task shape).

## Tooling dossier disposition

It's a program-wide 10-layer stack map; aml-substrate is Pillar 1, so most of it is downstream.
Substrate-now (after observable edges land): AMLGentex GNN/GBT as an external realism validator,
NetworkX, DuckDB (already a dep), SDMetrics (MIT). Next-pillar: lineage contract now / governance
stack later. Later: Splink, LangGraph+Outlines+Docling, Tazama. License trap: OpenSanctions data is
CC-BY-NC (OFAC SDN is public-domain).

## Soft Observations / Phase N+1 Candidates

- signal-watch's `active-phase.md` + `_CURRENT_STATE` Active Phase facts were STALE (said Phase 3);
  synced this debrief. The program-architecture home will keep drifting on aml-substrate progress
  because aml-substrate's dev-* run in its own repo — a periodic cross-pillar sync is the standing fix.
- The pre-staged brief lives in aml-substrate's `docs/` (uncommitted there); the re-rooted `/dev-plan`
  consumes it, then the brief can be removed or left as a planning artifact.
- Additive aml-substrate optimizations parked for later plans: CDD AccountView exposure (verified
  non-label), a measurement-baseline `--check`/`--freeze` gate, persist LCTR/EFTR/STR + verify.
