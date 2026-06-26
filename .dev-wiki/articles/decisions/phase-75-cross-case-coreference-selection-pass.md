---
title: "A cross-case co-reference selection pass makes the memory beat demonstrable on the real slice"
aliases: ["co-reference pass", "DEFAULT_COREF_ENTITIES_CAP", "slice co-reference selection"]
category: decisions
tags: [phase-75, curate, slice-selection, entity-spine, honesty, entity-ref]
parents: [phase-75-consume-substrate-v05-er-emission]
created: 2026-06-25
updated: 2026-06-25
source: plan
confidence: high
---

## Context

The Phase-75 memory beat needs the SAME `entity_ref` to appear in 2+ different cases in the committed
workbench slice. But the slice is a few-hundred-case sample of substrate's ~23k population, and the
default curate selection optimizes for capability-richness — that selection scattered the population's
real cross-case co-reference signal OUT of the slice. Measured: the committed slice had **0** cross-case
co-references. Asserting the memory lever exists without it in the slice would be a fabricated-signal
honesty failure (Honesty over demo drama).

## Decision

Add a deterministic cross-case CO-REFERENCE selection pass to curate (`DEFAULT_COREF_ENTITIES_CAP=15`):
pull 2+ cases of the top re-surfacing `entity_refs` into the slice, lifting the slice from **0 → 36**
real co-references. The pass is DISCLOSED in `slice_rule`, mirroring the existing combo-coverage
selection pass. It is honest because `entity_ref == party_id` — it surfaces a REAL population co-reference,
never a fabricated link.

Alternative rejected: assert the memory lever on the default capability-richness slice (which carries 0
co-references) — that would either be a fabricated number or a labeled-synthetic down-scope when the real
signal demonstrably exists in the population.

## Consequences

- The memory beat is demonstrable on real substrate data with a measured number (36), not a synthetic note.
- The selection is a second disclosed pass alongside combo-coverage; the slice grew 355 → 376 cases.
- Reusable lesson: a deterministic slice selection can silently drop the very signal a demo needs — add
  an explicit, disclosed selection pass for it rather than assuming the signal survives a default slice.
