---
title: "Merge console is a 6th SHIP artifact (dist/merge), not a workbench beat"
aliases: ["dist/merge sixth artifact", "merge.html ship target"]
category: decisions
tags: [phase-76, merge-console, class-j, ship-artifact, console-family]
parents: [phase-76-merge-adjudication-console]
created: 2026-06-25
updated: 2026-06-25
source: plan
confidence: high
---

## Context

Phase 75 surfaced the over-merge residual — 66 candidate SHARES links the deterministic spine
refuses to merge (distinct entity_refs sharing a strong identifier). The blueprint's Class-J
merge-adjudication gate is the human gate over exactly this residual. Two forms were available to
dramatize it: (a) a beat inside the existing companion investigator workbench (the GATHER/DECIDE
arc's home), or (b) a first-class offline single-file SHIP console, sibling to the gate + triage
consoles.

## Decision

Build it as a 6th SHIP artifact — `merge.html` → `dist/merge/index.html` (the user's Step-9 pick).
This elevates the Class-J merge gate to a first-class artifact, consistent with the console family
(gate console / triage console), each a self-contained offline single file driven by committed,
build-boundary-validated data. The workbench-beat alternative was rejected: the merge gate is a
distinct human-judgment workload (a Class-J gate, not an investigation step), and the console form
gives it a presentable, byte-frozen, drift-guarded artifact rather than a companion-only screen.

## Consequences

`--check all` grows from 8 to 9 targets. The new artifact follows the console pattern exactly:
`build.py` reads committed `data/merge/cases.json` and validates at the boundary
(`validate_merge_cases`), importing no spine/scorer/sibling — the deterministic verdict + scored
oracle are curated at build time (companion-side `curate_merge_cases.py`), never a live call in the
dist. The sanctioned launcher cascade gains a merge card (the only existing dist that changes); the
other 8 dists stay byte-frozen. The console family now has three members, all sharing the
Queue → Evidence → (Adjudication/Disposition) → Reveal → Ledger idiom.
