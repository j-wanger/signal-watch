---
title: "Phase 75 — Consume the substrate v0.5 entity-resolution emission: the spine's real-data memory lever"
status: completed
created: 2026-06-25
updated: 2026-06-25
ceremony: standard
tags: [cross-pillar, consume, entity-resolution, entity-spine, substrate, contract-v05, companion]
---

# Phase 75 — Consume the substrate v0.5 entity-resolution emission

## Objective

Adopt aml-substrate's Phase 27/28 ADDITIVE emission (named-identity **v0.4** + entity-resolution **v0.5**) into the companion-only consume path (`curate_workbench_cases` → `entity_spine` → `workbench`), grounding the Phase-74 memory short-circuit in **real substrate-emitted graded identifiers** — sized by a **measure-first cross-case-overlap gate**. Re-ground the 3 sibling briefs to live HEADs. Companion-only: dists byte-frozen, build.py imports nothing new.

## The check (code-verified 2026-06-25, two Explore agents over the live siblings)

- **aml-substrate** `a3fb02b`(P27) → `fc98b09`(P28): BUILT real consumable work. v0.4 = `display_name` (parties/related_parties) + `counterparty_name` (transactions). v0.5 = party-level `identifiers[]` `{kind,value,normalized,strength}` (email/phone="strong"), `RelationshipEdge.strength` ("strong"/"weak"/None), top-level `resolution_edges[]` `{between,status,shared,reading,cross_institution}`, `entity_ref`, multi-hop BO-graph (max_hops=2). Both ADDITIVE — v0.3 readers parse v0.5 untouched.
  - graded-counterparty-identifiers brief → **BUILT** (different shape: party-level + resolution_edges, not txn-row).
  - exogenous-disposition-label brief → **NOT BUILT** (deferred).
  - determination-signals (C1/C7/TF) → **PARTIAL** (only related_parties[]).
- **aml-casework** `cfd989f`(P15) → `4a858e6`(P16): NOTHING consume-relevant. P15/P16 = internal reconciliation harnesses (verdict engine + subprocess contract byte-identical). The affirmative-`cleared` verdict + the confidence-graded-resolution brief remain UNBUILT; still `KNOWN_CONTRACT_VERSIONS=("0.1","0.2","0.3")`. C14 SoF widening already BUILT (landed P14).

## The seam (pre-cut by Phase 74)

`entity_spine.observe()` already takes `party.identifiers[]` filtered on `strength=="strong"` (`entity_spine.py:188-227`) — byte-aligned to substrate v0.5. `curate_workbench_cases.py` pins `SUBSTRATE_HEAD="f15c241"` (v0.3) and reads only `related_parties[]`; it runs substrate's CLI as a subprocess (seed 0, deterministic) and vendors bundles verbatim under `data/workbench/bundles/`. The consume: bump the pin, re-curate at fc98b09, read the v0.5 fields, feed graded identifiers + resolution_edges into the spine, render real names + edges.

## The load-bearing unknown (T0 weakest assumption)

The spine's MEMORY lever (real priors across cases) needs the SAME strong identifier in 2+ DIFFERENT customer cases. Substrate's `resolution_edges` are within-bundle; cross-CUSTOMER overlap is unverified (the news-fixture-disjoint failure mode was real — Phase 42). **T1 measures it first.** If >0, the memory short-circuit becomes a real-data number; if 0, the consume down-scopes to render + within-case ER and the memory lever stays labeled synthetic (no fabricated number).

## T1 FINDING (2026-06-25) — the measure-first gate caught a mechanism error → A3 revised

The gate's zero-branch did NOT fire (the signal is non-zero) — instead it caught that the PLANNED mechanism (strong-merge substrate `identifiers[]`) is WRONG, while confirming the memory signal is real on a DIFFERENT key:

- Substrate's shared strong identifiers are NOT same-entity signals: `gen/identity.py` deliberately plants a coincidental-collision noise floor (email~6%/phone~4%) + controller-cluster `SHARES_EMAIL` between DISTINCT beneficial owners ("the reference resolver must be robust to over-merging on noise"). Substrate's v0.5 `resolution_edges` (`status:"resolved"`) emit for ANY shared-strong-id pair → they OVER-MERGE distinct people (verified: "Chloe Ali" emitted "resolved" to both "Charlotte Wilson" AND "Daniel Campbell"). The reliable same-entity key is `entity_ref` (party_id) — 100% name-consistent.
- Two-signal split (3k probe; full 40k for the record): **229 entity_refs re-surface cross-case** (REAL co-reference — the honest memory-lever signal); **99 over-merge traps** (shared strong id across distinct entity_refs — the naive strong-merge would falsely fuse); 168 same-entity_ref corroborations.

**Decision (user's checkpoint pick): "Entity_ref memory + SHARES adjudication."** A3 REVISED — FALSE in the strong-merge sense. The spine keys cross-case accumulation on `entity_ref` (the reliable identity); shared identifiers + resolution_edges are CANDIDATE SHARES_* links the spine ADJUDICATES (refuses to merge distinct entity_refs — the 99 traps become a demo beat: the spine is robust where substrate's naive resolution over-merges); the spine's independent strong-merge stays for the no-resolver domains (OSINT/news/casefile). Richer than planned, on-ramps the deferred Class-J merge-adjudication console. The A1 file-bar guard is unaffected (spine/provenance-path only). Full detail: ledger Phase-75 T1 resolution.

## Approach

1. **T1 (measure-first gate):** re-run substrate's emitter at fc98b09 (seed 0); scan the emitted bundles for normalized strong identifiers (email/phone) appearing on parties across 2+ distinct customer cases; record the count. Gates T3's framing. CHECKPOINT: STOP + report the number.
2. **T2:** bump `curate_workbench_cases` `SUBSTRATE_HEAD` f15c241→fc98b09; read `display_name`/`counterparty_name`/`identifiers`/`resolution_edges` additively; validate the new shape at the curate boundary; keep the v0.3 path + `--measure-casework` stub green.
3. **T3:** wire the workbench cases' `party.identifiers[]` + `resolution_edges[]` through `spine.observe()`; cross-case accumulation now runs on real substrate data; extend `entity_spine --selftest`.
4. **T4:** render real `display_name`/`counterparty_name` + resolution edges on the workbench (`showcaseSurface`/`boGraphHTML`); extend `workbench.test.mjs`.
5. **T5:** re-ground the 3 sibling briefs to live HEADs (substrate `fc98b09`, casework `4a858e6`) with BUILT/PARTIAL/NOT-BUILT status + the outstanding items; SKIP the casework re-vendor (no-op).
6. **T6:** verify + true-up — `--check all` 8/8, `entity_spine --selftest`, `workbench.test.mjs`, news + news_live + gather + pytest green, `evidence_requirements.py` byte-unchanged; CLAUDE.md + HANDOFF.md §8.

## Constraints / abort

The A1 file-bar guard (no change to `evaluate_sufficiency()`); companion-only (dists byte-frozen, no new build.py import); measure-don't-fabricate (A1); additive-only (A2); M8 not regressed. Abort: new ship target / dist drift / build.py sibling-or-companion import / loosened validator / determination-bar touched / breaking contract change / fabricated cross-case number → STOP-and-surface.

## Out of scope (deferred, named not built)

Casework re-vendor; executing the still-open sibling briefs (exogenous-disposition-label, C1/C7/TF, casework `cleared` + graded-resolution); probabilistic/Splink ER; the merge-adjudication Class-J console; graph/Kuzu projection; the medallion/DuckLake stack; `news_store` convergence onto the shared spine core.

## Review (STANDARD gate — adversarial workflow, 4 dimensions × per-finding verification, 8 agents)

0 must-fix · 2 should-fix · 1 nit · 1 refuted — ALL fixed:
- **[should-fix] non-deterministic memory examples** — `entities_in_multiple_records` tie-broke on a random per-run UUID, so the `/memory` top-N changed every page load. FIX: stable sort by (reach desc, lowest record_id, display_name) in the spine method + a determinism assertion in the selftest. Verified: examples now identical across runs.
- **[should-fix] `validate_v05_bundle` dead on the boundary** — it ran only on selftest fixtures, never on the committed bundles (a future bad emit with a dangling resolution_edge could land silently). FIX: wired it into `validate()` over every committed bundle (the "deterministic validators at boundaries" posture).
- **[nit] stale "355-of-23k" in two new comments** — the slice is 376; de-staled (never rendered/committed).
- **[refuted]** 1 finding (false positive). Honesty/A1/boundary dimensions: all PRAISE, zero confirmed issues — the co-reference pass disclosure, the casework v0.3-view, the over-merge framing, and the file-bar guard all held. Re-verified after fixes: workbench.test.mjs 159, --check all 8/8, pytest 22, A1 byte-unchanged.

## Spec

`specs/phase-75-consume-substrate-v05-er-emission.md` (STANDARD). Ledger: `assumption-ledger.md` Phase 75 (A1 accept-measure-first-gate; A2–A6 accept-with-evidence).
