---
title: "Phase 75 — Consume the substrate v0.5 entity-resolution emission: the spine's real-data memory lever"
aliases: []
category: journal
tags: [phase-75, cross-pillar, consume, entity-resolution, entity-spine, contract-v05, companion, measure-first]
parents: [phase-75-consume-substrate-v05-er-emission]
created: 2026-06-25
updated: 2026-06-25
source: debrief
duration: ~3-4 hours
---

# Phase 75 — Consume the substrate v0.5 entity-resolution emission

## What Happened

- Consumed aml-substrate's just-shipped ADDITIVE emission — named-identity v0.4 (`display_name`/
  `counterparty_name`) + entity-resolution v0.5 (party-level `identifiers[]` `{kind,value,normalized,strength}`,
  `RelationshipEdge.strength`, top-level `resolution_edges[]`) — into the companion-only path
  (`curate_workbench_cases` → `entity_spine` → `workbench`), grounding the Phase-74 memory short-circuit in
  REAL substrate data instead of the hand-authored synthetic note. STANDARD ceremony (user override).
- **The T1 measure-first gate was the keystone and bent the plan productively.** It was framed to catch the
  zero-overlap failure mode (down-scope to synthetic). The zero-branch did NOT fire — the signal is real —
  but the gate caught that the planned MECHANISM (strong-merge substrate `identifiers[]`) is WRONG:
  substrate's shared strong ids are a DELIBERATE collision noise floor + controller-cluster SHARES between
  DISTINCT entities (`gen/identity.py`: "the reference resolver must be robust to over-merging on noise"),
  and its own `resolution_edges` (`status:"resolved"`) over-merge distinct people (verified: "Chloe Ali"
  resolved to two distinct people). The reliable same-entity key is `entity_ref` (party_id, 100%
  name-consistent). Two-signal split (3k probe): 229 entity_refs re-surface cross-case (real co-reference);
  99 over-merge traps; 168 same-entity_ref corroborations.
- At the T1 CHECKPOINT the user picked **"Entity_ref memory + SHARES adjudication"** — key cross-case memory
  on `entity_ref`; demote substrate email/phone to weak candidate-SHARES; treat identifiers/resolution_edges
  as candidate SHARES links the spine ADJUDICATES (refuses to merge distinct entity_refs). Richer than
  planned — the 99 traps become a demo beat (the spine is robust where substrate's naive resolution
  over-merges) and it on-ramps the deferred Class-J merge-adjudication console.
- T2 re-curated to a 376-case v0.5 slice, including a disclosed cross-case CO-REFERENCE selection pass
  (`DEFAULT_COREF_ENTITIES_CAP=15`, mirroring combo-coverage) because the default capability-richness
  selection had scattered the population co-reference signal OUT of the slice (committed slice had 0) →
  0→36 real co-references. Two cross-pillar seams surfaced: casework gets a relabeled v0.3 VIEW of the v0.5
  bundle (it rejects `"0.5"` but tolerates additive fields), and a latent venv-path bug (relative
  `--measure-casework` + subprocess cwd-change) was fixed inline (resolve to absolute).
- T3 added `entity_ref` to `STRONG_KINDS` + a pillar-neutral `entities_in_multiple_records` cross-case query
  + a `_observe_substrate_party` adapter; committed slice measures 36 co-references + 66 over-merge-refused.
  The A1 file-bar guard HELD — `evidence_requirements.py` byte-unchanged; injecting a prior `cleared` →
  byte-identical verdict. T4 added a `/memory` route + a "Persistent entity intelligence" panel rendering
  the real numbers; live-verified. T5 re-grounded the 3 sibling briefs to live HEADs (substrate `fc98b09`,
  casework `4a858e6`). T6 full verification + CLAUDE.md true-up.
- Adversarial review (STANDARD gate, 8 agents): 0 must-fix, 2 should-fix + 1 nit ALL FIXED (non-deterministic
  `/memory` examples → stable sort; `validate_v05_bundle` dead on the boundary → wired into `validate()`;
  stale "355-of-23k" comment de-staled), 1 refuted. Honesty/A1/boundary dimensions all praise.

## Decisions Made

- [[phase-75-entity-ref-memory-shares-adjudication|Entity_ref-keyed cross-case memory + SHARES adjudication]]
- [[phase-75-cross-case-coreference-selection-pass|A cross-case co-reference selection pass makes the memory beat demonstrable]]
- [[phase-75-casework-v03-view-of-v05-bundles|casework gets the v0.3 VIEW of additive v0.5 bundles]]
- [[phase-75-skip-casework-re-vendor|Skip the casework re-vendor (no observable change)]]

## Problems Solved

- The planned strong-merge mechanism would over-merge substrate's noise floor — resolved by re-keying on
  `entity_ref` + SHARES adjudication (the measure-first gate caught it before any wrong wiring landed).
- The default slice carried 0 cross-case co-references — resolved with a disclosed co-reference selection pass.
- casework rejects `contract_version "0.5"` — resolved with a relabeled v0.3 view (committed bundle stays v0.5).
- A latent venv-path bug (relative arg + cwd-change → py not found) — fixed inline (absolute resolution).

## Open Questions

- None unresolved this phase.

## Artifacts Changed

- `scripts/measure_xcase_overlap.py` (NEW companion module — the measure-first gate; `--selftest`)
- `scripts/entity_spine.py` (`entity_ref` added to `STRONG_KINDS`; new `entities_in_multiple_records` query, stable sort)
- `scripts/serve_workbench.py` (`_observe_substrate_party` adapter + `substrate_memory` + a `/memory` route)
- `scripts/curate_workbench_cases.py` (SUBSTRATE_HEAD f15c241→fc98b09; v0.5 additive read; `validate_v05_bundle` wired into `validate()`; co-reference selection pass; casework v0.3-view; venv-path fix)
- `workbench.html` (the "Persistent entity intelligence" `/memory` panel — `memoryPanelHTML`/`loadMemory`)
- `tests/workbench.test.mjs` (151→159, +8 memory panel)
- `data/workbench/**` (re-curated v0.5 slice, 376 cases)
- `docs/{substrate-graded-counterparty-identifiers,substrate-exogenous-disposition-label,casework-confidence-graded-resolution}-PLAN-BRIEF.md` (re-grounded to live HEADs)

## Related

- [[phase-75-consume-substrate-v05-er-emission|Phase 75 — Consume the substrate v0.5 ER emission]] — parent phase
- [[phase-74-entity-intelligence-spine|Phase 74 — The persistent entity intelligence spine]] — the spine this phase feeds with real data

## Soft Observations / Phase 76 Candidates

- Render the over-merge-refused EXAMPLES as a SHARES network on the `/memory` panel — the SHARES adjudication
  is a number now; a network view would make the "spine refuses to over-merge" beat visceral. | render the
  SHARES adjudication network | evidence: T4 `/memory` panel renders counts only
- The merge-adjudication Class-J console — the natural next consume of the entity-resolution layer (substrate
  emits the candidate SHARES; the over-merge gap is the unbuilt adjudication console named in the standards). |
  Class-J merge-adjudication console | evidence: ledger Phase-75 T1 resolution
- Execute the still-open sibling briefs (substrate exogenous-disposition-label; casework cleared/graded-resolution)
  — sibling-rooted. | sibling sessions
- Converge `news_store` onto the shared spine core (the deferred Phase-74 A1 question). | Phase 76
- Probabilistic/Splink ER + graph/Kuzu + medallion/DuckLake (named-deferred). | later
