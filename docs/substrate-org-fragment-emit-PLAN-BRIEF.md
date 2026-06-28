# PLAN-BRIEF — aml-substrate: extend the anchored fragment overlay to ORGANIZATIONS

> **A signal-watch → aml-substrate handoff brief** (the Phase-55–58 / 74–79 pattern: signal-watch authors the
> contract; the sibling implements + measures it on its own lifecycle — *no code lands in substrate from here*).
> Synthetic / illustrative; **no rate, score, or multiplier is claimed.** **Pinned to verified substrate HEAD
> `f7fbdb0` (Phase 37), code-verified + MEASURED 2026-06-28.** Companion to
> [`cross-pillar-build-order.md`](cross-pillar-build-order.md) and the Phase-79 person merge oracle
> ([`substrate-open-reference-data-fork-PLAN-BRIEF.md`](substrate-open-reference-data-fork-PLAN-BRIEF.md) Stage-2 seam-5).

## The finding (Phase 81 T1a measure-first gate — ABORT)

signal-watch Phase 81 set out to consume substrate Phase 35's **org-name OFAC collision** (`4f49e53`) as a merge
console case class — the organization sibling of the Phase-80 PERSON name-collision class. The measure-first gate
**ABORTED it as STRUCTURALLY ONE-SIDED.**

Measured on the `f7fbdb0` `--clients 12000 --months 3 --seed 0 --emergence --anchored --screen --emit-screening
--emit-eval-oracles` emit:

- **354 multi-record GT clusters — all 354 person-only. ZERO organization fragment clusters.** Substrate's anchored
  fragment overlay (Phase 32, `anchored_fragment_entities`) fragments **persons but not organizations**: a person
  can appear as a flagged record + a typo'd same-person fragment (same `GT-<hash>` cluster, different `entity_ref`),
  but every ORGANIZATION `entity_ref` is its own singleton cluster.
- **Consequence for the merge gate:** the two faces of a sanctions merge decision are (UPHOLD) a flagged record +
  its same-entity FRAGMENT that evaded screening, and (REJECT) two DISTINCT entities sharing a watchlisted name.
  Without org fragments, the UPHOLD face **cannot exist for organizations** — every org-name collision is between
  distinct orgs (different clusters) → **all-reject, one-sided by construction** (the Phase-77 trap). Verified: 10
  flagged orgs, 3 sanctions-touching merge candidates, **0 uphold / 3 reject**.
- This is **structural, not seed/scale luck** — scaling clients or changing the seed cannot create an org fragment
  the overlay never emits. signal-watch did NOT fabricate org fragments to force two-sidedness (the no-fabrication
  discipline); `dist/merge` stayed BYTE-FROZEN and the honest non-result routes here.

## What substrate should emit (the ask)

**Extend the anchored fragment overlay to organizations** — the exact mirror of the existing person-fragment path:

1. A deterministic SUBSET of organizations gets a **same-org FRAGMENT record**: a second `O-` record with a
   perturbed `legal_name` (suffix/abbreviation/typo variant — e.g. `ACME TRADING LTD` ↔ `Acme Trading Limited`),
   **the SAME `GT-<hash>` cluster** as the parent (so the oracle marks them same-entity), a distinct `entity_ref`.
2. **Intersect a deterministic share of the fragmented orgs with the Phase-35 OFAC org-name collision** so a
   FLAGGED org has a same-org fragment that evaded screening (the UPHOLD face), alongside the existing distinct-org
   name collisions (the REJECT face). Target: a genuinely TWO-SIDED org merge oracle (some uphold, some reject),
   the same shape the PERSON overlay already yields (Phase-79: 13 uphold / 16 reject for persons).
3. **Keep it label-blind + contract-neutral:** the fragment is an identity-realism artifact, not a laundering
   signal (`corr(fragment, illicit) ≈ 0`); the emission shape (v0.5 bundles + `true_entities` with `entity_ref ≠
   cluster` + `intended_disposition`) is UNCHANGED — signal-watch's `curate_merge_cases` reads the identical shape
   it reads for persons, no consume-side rework (the org slice would distill exactly like the Phase-80 person
   `distill_sanctions_slice.py`, just over `organizations.parquet`).

## The payoff (why this serves the north star)

The merge console is the ONE gate with a measurable correctness oracle. A two-sided ORG collision class completes
the sanctions-screening realism (person + org) the Phase-80/81 arc opened — the org case is arguably MORE
recognizable to a bank (corporate-name screening false positives are the dominant sanctions-screening pain). Until
substrate fragments orgs, the org merge case cannot be scored two-sided, so it cannot ship.

## Boundary + status

- **Contract-neutral:** no change to the v0.5 emission contract, the determination engine, or any signal-watch dist.
- **Consume-ready on landing:** signal-watch's `curate_merge_cases` / `distill_sanctions_slice` already handle the
  person path; the org path is the same code over `organizations.parquet` once org fragments exist.
- **Status: NOT BUILT** (the named handoff). **Pin `f7fbdb0` (Phase 37).** Out of scope: any code landing in
  substrate from signal-watch; the sanctions DETECTION question (the flag is label-blind by design — this is an
  entity-resolution realism ask, not a detection ask).
