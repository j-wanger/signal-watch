---
title: "Phase 74: a genuine persistent store + prove the scorer here (the user's Step-9 picks)"
aliases: ["genuine persistent store", "prove the scorer here", "gitignored DuckDB write seam", "resolver-input firewall", "true_entities scorer"]
category: decisions
tags: [phase-74, entity-spine, persistence, duckdb, scorer, true-entities, resolver-firewall, companion]
parents: [phase-74-entity-intelligence-spine]
created: 2026-06-25
updated: 2026-06-25
source: plan
confidence: medium
---

## Context

Two design forks at the planning gate (the user's Step-9 picks, both the more-rigorous option). (1)
The "memory" re-surfacing demo could be a scripted two-surfacing replay over committed fixtures (the
news-replay pattern — no live write) OR a genuine persistent store the workbench writes a disposition
into and reads back. The companion contract states "persists nothing", and the casefile pair is
authored — both argue for the replay. But the pKYC frame is event-driven (a prior disposition is the
event that short-circuits the next review), which argues for a real store. (2) Resolution-correctness
could be asserted from the grammar OR a minimal scorer could be PROVEN here over a tiny synthetic
`true_entities`. The substrate holds ground-truth clusters in `true_entities.parquet` with a
ground-truth-blind resolver — the in-family reference (its `test_resolution_lift.py`).

## Decision

Build a GENUINE gitignored DuckDB write seam in `serve_workbench` (write a disposition, read it back
on re-surface) — a DELIBERATE, companion-firewalled crossing of "persists nothing", justified by the
`news_store` precedent (a 127.0.0.1 gitignored DuckDB store is §4.5-clean — §4.5 forbids browser
keys/backends, not a localhost companion store). And PROVE a minimal scorer HERE over a tiny
synthetic `true_entities` (pairwise precision/recall or cluster-F1/B-cubed; cite the substrate's
`test_resolution_lift.py` as the in-family reference), behind a **resolver-input firewall**: no
resolver-input field is the cluster id NOR 1:1-correlated with cluster identity (renaming the cluster
field must NOT pass); the cluster id lives only in the scorer's evaluation-only channel. Every
resolver-quality number carries the "measured on synthetic clusters; production has no ground truth"
qualifier. Alternatives rejected: the fixture-replay memory demo (under-proves persistence — the
event-driven short-circuit is the lever); asserting resolver quality from the grammar (un-measured —
the scorer is what makes "probabilistic only if measured" real).

## Consequences

- The companion boundary is crossed CONSCIOUSLY and guarded: `--check all` 8/8 byte-identical + a
  `build.py` no-spine-import grep; the store is gitignored, 127.0.0.1, never committed; build.py
  never imports the spine or scorer.
- The scorer makes the confidence-grade decision honest end-to-end: a probabilistic score is now
  admissible where measured, and the synthetic-only qualifier is enforced (not optional).
- The resolver-input firewall is a SCHEMA-boundary guard, not a convention — a contract test fails
  on a 1:1-correlated surrogate, closing the synthetic-ground-truth-leak class the firewall exists
  to prevent.
- The DuckDB seam is the substrate of the memory demo: the re-surfacing short-circuit reads a
  genuinely persisted prior, so the targets-to-close drop is a real read-back, not a replayed
  fixture.
</content>
</invoke>
