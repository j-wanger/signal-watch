---
title: "Phase 79: floor + gated-upside bundle for the two unblocked sibling consumes"
aliases: [phase-79-bundle, lakeshore-floor-merge-upside]
category: decisions
tags: [cross-pillar, consume, casework, substrate, floor-gated-upside, ceremony, merge-oracle]
parents: [phase-79-consume-sibling-emissions]
created: 2026-06-27
updated: 2026-06-27
source: plan
confidence: high
---

# Decision — floor + gated-upside bundle

## Context

Both Phase-77-deferred consumes were **code-verified RESOLVED sibling-side this session**
(file:line, not from the loaded snapshot): casework Phase 19 (`ed93a0d`, on
`feat/phase-1a-deterministic-verifiers @076fb8e`) built `_c3_fan_in` — closing the
Lakeshore CASE-B fan-in-C3 co-sign blocker; substrate Phase 32 (`31cb439`, main
@`c099259`/Phase 33) mints `entity_ref ≠ cluster` anchored fragments under `--anchored`
(opaque `GT-<sha1>` cluster ids disjoint from every resolver input; 17 multi-ref clusters /
refs 255 > clusters 231 at n=400/seed0) — structurally curing the Phase-77 circular merge
oracle. Both blocks named in `docs/cross-pillar-build-order.md` are now live. Jake invoked
"consume sibling repos" (plural).

## Decision

Bundle both consumes in ONE STANDARD phase as a **floor + gated-upside** structure:

- **FLOOR (committed):** Lakeshore CASE-B signs `cleared` end-to-end via fan-in C3 —
  re-vendor casework `b3546d4→076fb8e`, shape CASE-B from its REAL multi-originator network
  (no fabricated pattern), `--disposition cleared` → casework signs. Completes the north-star
  matched pair (Northgate files / Lakeshore clears, both via casework). Companion-only.
- **GATED UPSIDE:** the merge real-data oracle — measure-first companion-only first, then gate
  the `dist/merge` re-freeze on a clean two-sided non-tautological result.

Rationale: the Phase-77 precedent (bundle independent modest consumes under one STANDARD phase)
holds; the Lakeshore floor guarantees phase value even if the merge track aborts. Direction gate:
the user picked "Bundle, gated upside" via AskUserQuestion 2026-06-27.

**Alternatives rejected.** (a) Lakeshore-only this phase, deferring merge to its own phase —
under-uses the now-available substrate emission given Jake's plural "consume sibling repos".
(b) Bundle + commit to the `dist/merge` re-freeze up front — removes the de-risking buffer given
the live emit crash (see [[decisions/phase-79-merge-measure-first-before-dist]]).

## Consequences

The floor lands phase value unconditionally; the upside is genuinely optional and its abort path
is pre-specified (consensus + a substrate emit-stability brief, the dist re-freeze does not run).
The phase carries one L task (T3, the measure-first merge oracle). STANDARD ceremony stands
(cross-pillar + a conditional ship-dist touch). A1 guard holds across both tracks
(`evidence_requirements.py` byte-unchanged); the firewall (build.py imports no
spine/scorer/sibling/curate) and the 8 non-merge dists stay frozen.

Related: [[decisions/phase-79-merge-measure-first-before-dist]] ·
[[decisions/phase-77-three-consumes-one-phase-fork-parked]] · `docs/cross-pillar-build-order.md`.
