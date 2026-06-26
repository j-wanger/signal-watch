---
title: "build.py companion firewall holds for the merge console; curation is companion-side"
aliases: ["curate_merge_cases companion-side", "build.py imports no spine/scorer", "build-time curation merge"]
category: decisions
tags: [phase-76, merge-console, build-boundary, companion-firewall, curate, resolver-input-firewall]
parents: [phase-76-merge-adjudication-console]
created: 2026-06-25
updated: 2026-06-25
source: plan
confidence: high
---

## Context

The merge console needs each case's deterministic spine verdict (kept-distinct vs merged) and, for
synthetic cases, the scored oracle. Both come from companion-only machinery — `entity_spine.py` and
`resolution_scorer.py`. A naive implementation would have `build.py` call the spine/scorer at build
time. But `build.py` has a load-bearing invariant: it imports NO companion/sibling layer (the
`--check all` byte-frozen dists depend on it, and the boundary is what keeps the ship artifacts
offline and self-contained). The console-family precedent (gate/triage) is: an authoring tool
curates a committed JSON; `build.py` reads and validates that JSON at the boundary with a standalone
validator.

## Decision

Keep the firewall. `build.py` imports ONLY stdlib + `news_ground` (the single sanctioned
build→companion import that predates this phase) — no spine/scorer/serve_workbench/curate. The new
authoring tool `curate_merge_cases.py` (companion-side) reuses `entity_spine` + `resolution_scorer`
and emits committed `data/merge/cases.json`. `build.py` reads the committed JSON and validates it at
the boundary with a STANDALONE `validate_merge_cases` (referential integrity + closed adjudication
vocab + the resolver-input firewall + the synthetic-only scoring qualifier). The resolver-input
firewall is translated into the ship artifact: the latent truth rides ONLY each scored case's
`oracle` block (revealed post-disposition); the pre-adjudication evidence carries no truth field;
`MERGE_TRUTH_LEAK_KEYS` enforces it at the build boundary.

## Consequences

The deterministic verdict + scored oracle are baked at BUILD time — no live spine/scorer in the
dist (the gate-console pattern: build-time-derived adjudicated outcomes). `dist/merge` is fully
offline and byte-frozen. The two validators (curate's firewall + build's `validate_merge_cases`)
enforce the same contract and must stay in EXACT parity — the adversarial review found and fixed a
parity gap where the build validator was the weaker of the two (see
[[phase-76-validator-parity-build-mirrors-curate]]). Adding the merge console did not weaken the
`build.py` boundary; `--check all` still proves it imports no spine/scorer/sibling.
