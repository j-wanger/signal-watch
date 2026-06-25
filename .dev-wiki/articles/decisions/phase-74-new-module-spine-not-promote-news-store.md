---
title: "Phase 74: new-module spine, not promote-news_store — drop the M8-separability dependency"
aliases: ["new-module spine", "entity_spine new module", "news_store byte-untouched", "drop separability dependency"]
category: decisions
tags: [phase-74, entity-spine, news_store, companion, m8, cross-pillar, persistent-entity]
parents: [phase-74-entity-intelligence-spine]
created: 2026-06-25
updated: 2026-06-25
source: plan
confidence: medium
---

## Context

The spec frames a "persistent entity intelligence spine" generalized from `news_store.py`'s
observation/provenance/conflict/reversible machinery. The load-bearing risk (ledger A1, the T0
weakest assumption, a DON'T-KNOW at the gate): is that machinery actually separable from
`news_store`'s exact-normalized-name anchor key + its `serve_news`/`/anchor`/dossier coupling, so a
pillar-neutral core can be extracted WITHOUT rewriting the anchor table out from under the M8 news
arc (the 13-fixture replay + the DuckDB selftests + `/anchor`)? Promoting in place couples the news
arc to the workbench arc and risks the live M8 pillar; greenfielding duplicates DuckDB machinery the
spec explicitly says to reuse.

## Decision

Build the spine as a NEW module `scripts/entity_spine.py`; leave `news_store.py` **byte-untouched**.
This DROPS the separability dependency entirely rather than betting on it — the M8 arc is inherently
safe because nothing in it changes. Confidence/observation/link machinery is authored fresh in the
neutral module against the standards (T1), not extracted from `news_store`. The directional firewall
is asserted: `entity_spine.py` imports no `news_store`/`serve_news`, and its `--selftest` asserts the
news disposition vocabulary (`set_disposition`, the escalation watchlist) is NOT in the core.
Alternatives rejected: **promote-in-place** (migration risk to the M8 13-fixture replay + DuckDB
selftests + `/anchor`; the spec's own load-bearing scope risk); **layer-on-news_store** (anchors
become one observation type pointing into a new `persistent_entity`) — DEFERRED to Phase-75+ as the
convergence question, informed by the coupling read but not built now.

## Consequences

- The M8 news pillar cannot regress from this work — it is not touched (the exit criterion
  `news-stream.test.mjs` + `news_live_test.py` green is a guard, not a migration verification).
- Convergence (news later adopting the shared core) is a NAMED Phase-75+ follow-on, not a silent
  debt — two DuckDB stores coexist in the companion layer until then (acceptable: both gitignored,
  127.0.0.1, companion-only).
- The neutral core is authored to the standards (T1) first, so the spine and the cross-repo contract
  share one vocabulary by construction — the briefs (T6) reference the same docs.
- If a future phase proves the cores should merge, the deferred coupling read is the input; this
  decision does not foreclose it.
</content>
</invoke>
