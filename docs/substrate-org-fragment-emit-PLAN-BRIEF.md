# PLAN-BRIEF — aml-substrate: extend the anchored fragment overlay to ORGANIZATIONS

> **A signal-watch → aml-substrate handoff brief** (the Phase-55–58 / 74–79 pattern: signal-watch authors the
> contract; the sibling implements + measures it on its own lifecycle — *no code lands in substrate from here*).
> Synthetic / illustrative; **no rate, score, or multiplier is claimed.** **Re-measured against substrate HEAD
> `294d3e5` (Phase 40 — the org fork is now BUILT), code-verified + MEASURED 2026-06-29 (signal-watch Phase 82
> T2a).** Companion to [`cross-pillar-build-order.md`](cross-pillar-build-order.md) and the Phase-79 person merge
> oracle ([`substrate-open-reference-data-fork-PLAN-BRIEF.md`](substrate-open-reference-data-fork-PLAN-BRIEF.md) Stage-2 seam-5).

## UPDATE (Phase 82 T2a — substrate BUILT the org fork, but it is STILL one-sided on our path; the ask is SHARPER)

substrate Phase 38 (`a9a088a`, "org-fragment-emit") **implemented this brief**: `apply_anchored_org_fork` mints
364 `O-FRAG-` records, intersects the OFAC flag (16 flagged-org uphold *clusters* in `true_entities.parquet`),
and merges them into the gen linkage with `entity_ref != cluster`. **But signal-watch Phase 82's T2a measure-first
gate replayed it through our OWN distill/scorer path and it is STILL ONE-SIDED — for a NEW, sharper reason:**

1. **The fragments are absent from the CONSUMABLE slice oracle.** `--anchored --emit-eval-oracles` writes the org
   fragments to `true_entities.parquet` (the gen linkage), but `identity/true_entities.json` (the slice oracle our
   `distill_sanctions_slice` reads, built by `emit_true_entities` from `iter_slice_cases`) carries **0 of 364
   `O-FRAG`** — org fragments are not slice-participating evidence parties, so they are excluded. Person fragments
   work only because persons ARE slice parties (519 `P-FRAG` present, 354 two-sided clusters).
2. **Even reading the parquet, the fragments have NO RESOLUTION HANDLE.** Measured across all 364 base↔fragment
   pairs: they share only broad *categories* (org_type / incorporation_jurisdiction / NAICS / nature_of_business —
   all 364 pairs, a category shared by thousands of orgs) and NEVER a unique identifier (`incorporation_number` /
   `business_number` / `registered_office` / `email` / `phone` shared in 0 of 364 pairs); the perturbed
   `legal_name` normalizes-equal in only 15 of 364. So our resolver (which enumerates a merge candidate only on a
   shared strong/weak identifier OR an exact-normalized name — loosened fuzzy name-matching WITHOUT identifier
   layering is a known false-positive explosion, the entity-resolution caveat, so it is
   correctly excluded) **never proposes the base↔fragment merge** → 0 uphold candidates. Measured: 5
   sanctions-touching org candidates, ALL `correct-rejection` (distinct namesakes), **0 uphold / 5 reject**.

**The SHARPENED ask (supersedes the original below):** for the org UPHOLD face to be an *adjudicable merge
candidate*, each `O-FRAG` fragment must RETAIN at least one shared OBSERVABLE identifier with its base — the
realistic corporate-screening-evasion pattern: a **SAME company** (same `incorporation_number` **or**
`business_number` **or** `registered_office` address) that appears under a perturbed **name** variant that evaded
the watchlist name-match. Then entity resolution links them on the retained corp-number/address (the handle) while
the NAME evaded screening — "resolution is prerequisite to correct sanctions coverage" made real. AND emit the org
fragments into the **slice** oracle `identity/true_entities.json` (make them slice-participating, or emit a
dedicated org oracle), so the consumable artifact — not just `true_entities.parquet` — carries them. Until BOTH
land, the org merge class cannot ship two-sided. signal-watch did NOT fabricate a handle to force two-sidedness
(`dist/merge` stayed BYTE-FROZEN; the honest non-result routes here, the Phase-77/81 discipline).

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
