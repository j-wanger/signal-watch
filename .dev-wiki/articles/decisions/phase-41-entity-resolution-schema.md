---
title: "Phase 41 direction: entity-resolution schema enrichment (live news)"
aliases: [entity-enrichment, er-schema, phase-41-direction]
category: decisions
tags: [news-live, entity-resolution, schema, grounding-gate]
parents: [phase-41-entity-resolution-schema]
created: 2026-06-09
updated: 2026-06-09
source: plan
confidence: high
---

## Context

At the Phase 41 dev-plan gate the user set the direction aside from the offered
candidates (FINTRAC /intel/ depth, flag-quality round 2, AUSTRAC/UK, QOL bundle)
and reframed: the live entity scan's schema is too thin for proper ENTITY
RESOLUTION. Today an entity is `{name, type, location, age, profession, context}`;
ungrounded attributes are stripped; aliases are treated as NOISE (alias-dedup
DROPS token-subset names, monikers dropped); relationships exist only as loose
`context` prose; nothing marks the main subject. The user wants: additional
identifying attributes when available (address, phone, email, …), name
variations/aliases KEPT, and structured inter-entity relationships — especially
who the main subject is and how the others relate to it.

## Decision

CONFIRMED at the assumption gate (2026-06-09; ledger Phase 41 block — A1 + A3
rejected round 1, revised, all accepted round 2). The user's A1 reject revealed
the LOAD-BEARING fact: the system will be fed PRIVATE INVESTIGATION NOTES —
the input domain is not just public articles. Schema slots are designed for
that domain (incl. client_number + account_number), NOT census-limited.

1. TWO-LAYER data model (A1'): per-scan extraction JSON stays NESTED (entities
   with aliases[] + properties[] {kind, value} + record-level relationships[]
   {from, to, label, evidence} + main_subject), grounded-or-stripped by the
   gate. The DuckDB store normalizes to the ANCHOR design: entity anchor table
   (+ entity SOURCE TYPE — document types differ in significance:
   gov-enforcement / commercial-news / investigation-note) + ONE monolithic
   property association table (anchor×kind×value edge w/ detail JSON, evidence,
   scan provenance, grounded status; confidence column RESERVED, not
   model-populated until a measured basis; per-property subtables revisited
   only on measured divergence) + a relationship edge table.
2. Property-kind closed vocab: address, phone, email, client_number,
   account_number, dob, id_registration, wallet, domain (+ existing
   location/age/profession). Relation vocab FROZEN at implementation (the
   DRQ3 decision; single authority `news_ground.RELATION_LABELS`, 9 terms):
   co-conspirator, owner-or-controller-of, front-for, family-or-associate-of,
   employee-or-agent-of, professional-intermediary-for, counterparty-of,
   recipient-of-funds-from, other. DRQ3 measurement (the 3 `.ph41` federal
   captures, 13 gate-passed edges): owner-or-controller-of 9 ·
   employee-or-agent-of 3 · co-conspirator 1 · other 0 — the vocab covers
   federal enforcement articles; the honest `other` bucket did NOT dominate.
   Labels stay neural judgments — vocab-checked, never correctness-checked
   (C/D-code split).
3. Gate (A2/A4): aliases verbatim-grounded; properties grounded-or-stripped;
   relationships = grounded evidence + referential integrity + vocab; alias
   DROPs invert to FOLDs (subset-name/moniker attach to the fuller entity).
4. ER payoff: screen matches name ∪ aliases; exact-normalized-name cross-scan
   ACCUMULATION on anchors (A3'b); fuzzy cross-scan MERGE adjudication DEFERRED.
5. Privacy boundary (A5, NEW): private/client data confined to the local live
   layer (gitignored DuckDB + live session, local 127.0.0.1 model — notes never
   leave the machine); never committed, never fixture-promoted (US-federal-only),
   never in ship artifacts. Offline demo artifacts byte-frozen (A3'a).

## Consequences

The watchlist/screen step becomes alias-aware (the first real ER capability);
the relationship graph gives the disposition gate subject-centric context.
Fixture-pinned drop behavior changes deterministically (fold vs drop). The
offline demo does NOT show the enrichment this phase (live-only scope).

NEXT-PHASE SEAM (named, not built): `news_store.anchor_summary(name)` is the
accumulated-identity read (scans, per-row-provenance properties incl. kept
conflicts, relationship edges) with NO consumer yet beyond its selftest — the
"anchor view" UI/route that surfaces conflicts to the analyst is the natural
next live-layer phase, alongside fuzzy-merge adjudication. Known structural
limitations carried: same-name-different-person collisions share an anchor
(split deferred with merge); _adjacent_parent needs the FULL parent name
printed beside a handle ("Zhdanova (via her moniker @monalisa7)" does not fold
— the model's own aliases[] extraction covers that case, as the .ph41 capture
proved).
