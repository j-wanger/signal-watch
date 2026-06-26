---
title: "Entity_ref-keyed cross-case memory + SHARES adjudication (not strong-id merge)"
aliases: ["over-merge trap", "entity_ref memory", "SHARES adjudication", "measure-first mechanism reframe"]
category: decisions
tags: [phase-75, entity-resolution, entity-spine, cross-pillar, over-merge, measure-first, aml-substrate]
parents: [phase-75-consume-substrate-v05-er-emission]
created: 2026-06-25
updated: 2026-06-25
source: plan
confidence: high
---

## Context

Phase 75's planned consume was: feed aml-substrate's v0.5 party `identifiers[]` (email/phone marked
`strength=="strong"`) into the Phase-74 `entity_spine` STRONG-ID MERGE, so cross-case priors accumulate
on real substrate-emitted graded identifiers. The seam was pre-cut — `entity_spine.observe()` already
filters `party.identifiers[]` on `strength=="strong"`. The T1 measure-first gate was framed to catch the
**zero-overlap** failure mode (the news-fixture-disjoint case from Phase 42): if no strong identifier
re-surfaced across 2+ distinct customer cases, the memory lever would down-scope to labeled-synthetic.

The gate's zero-branch did **not** fire — the signal is non-zero. Instead it caught that the planned
*mechanism* is wrong: substrate's shared strong identifiers are NOT same-entity signals. `gen/identity.py`
DELIBERATELY plants a coincidental-collision noise floor (email~6% / phone~4%) PLUS controller-cluster
`SHARES_EMAIL` edges between DISTINCT beneficial owners — its own docstring: "the reference resolver must
be robust to over-merging on noise." Substrate's v0.5 `resolution_edges` (`status:"resolved"`) emit for
ANY shared-strong-id pair, so they OVER-MERGE distinct people (verified: "Chloe Ali" emitted "resolved"
to both "Charlotte Wilson" AND "Daniel Campbell"). Strong-merging on these identifiers would falsely fuse
distinct entities. The reliable same-entity key is `entity_ref` (party_id) — 100% name-consistent.

Two-signal split (3k probe; full 40k for the record): **229 entity_refs re-surface cross-case** (real
co-reference — the honest memory signal); **99 over-merge traps** (shared strong id across distinct
entity_refs); 168 same-entity_ref corroborations.

## Decision

User's Step-13-checkpoint pick: **"Entity_ref memory + SHARES adjudication"** (A3 REVISED — false in the
strong-merge sense). The spine keys cross-case accumulation on substrate's reliable `entity_ref`; substrate
email/phone are DEMOTED to weak candidate-SHARES (never a merge key); identifiers/resolution_edges become
CANDIDATE SHARES links the spine ADJUDICATES — it refuses to merge distinct entity_refs. The spine's
independent strong-merge stays ONLY for the no-upstream-resolver domains (OSINT/news/casefile, where Phase
74 proved it).

Alternative considered and rejected: trust substrate's `resolution_edges`/shared identifiers as merge keys
(the planned mechanism) — rejected because it over-merges substrate's deliberate noise floor + controller
clusters. The down-scope-to-synthetic alternative was moot (the signal is real on `entity_ref`).

## Consequences

- The consume is RICHER than planned: the 99 over-merge traps become a demo beat — the spine is robust
  where substrate's naive resolution over-merges. This demonstrates the resolver-robustness the Phase-74
  standard is about and on-ramps the deferred Class-J merge-adjudication console.
- Implementation: T2 carries identifiers/resolution_edges as candidate SHARES links (not merge keys); T3
  adds `entity_ref` to `STRONG_KINDS` and keys the spine on it (merge logic byte-unchanged); the
  committed slice measures **36 cross-case co-references + 66 over-merge-refused**.
- The A1 file-bar guard is UNAFFECTED — all of this rides the spine/provenance path; `evidence_requirements.py`
  stays byte-unchanged.
- Reusable lesson: when consuming an upstream resolver's identifiers, don't trust its emitted "resolved"
  edges as same-entity assertions — verify whether they encode a deliberate noise floor / candidate
  baseline; prefer the declared identity key. Reinforces [[cross-pillar-review-verify-sibling-repo]].
