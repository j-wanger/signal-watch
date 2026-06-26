---
title: "Phase 76 — The merge-adjudication Class-J console (dist/merge): the scored merge gate"
aliases: []
category: journal
tags: [phase-76, merge-console, class-j, entity-resolution, scored-oracle, ship-artifact, consensus-vs-scored]
parents: [phase-76-merge-adjudication-console]
created: 2026-06-25
updated: 2026-06-25
duration: ~3 hours
source: debrief
---

# Phase 76 — The merge-adjudication Class-J console (dist/merge)

## What Happened

- Built the 6th SHIP artifact `merge.html` → `dist/merge/index.html` — the blueprint's Class-J
  merge-adjudication gate dramatized as an offline single-file console (sibling to the gate + triage
  consoles, those byte-frozen). Consumes Phase 75's over-merge finding: the deterministic spine
  resolves what it can (entity_ref) + refuses the ambiguous; the human adjudicates the 66 candidate
  SHARES residual.
- THE ARCHITECTURAL NOVELTY landed: this is the ONE console with a measurable correctness ORACLE
  (`true_entities`) — unlike the consensus-only gate console + the label-blind §14 triage, the Reveal
  SHOWS (where the oracle exists) whether the adjudication matched truth.
- T1 (the A1 checkpoint) EXPANDED the synthetic oracle 8→25 obs / 5→17 clusters — 13 candidates,
  9 ambiguous, all 4 quadrants / 3 bases (same-person-fragmented / household-share / coincidence).
  CHECKPOINT PASSED: the oracle yields genuine ambiguity without fabricating truth. `resolution_scorer`
  gained `candidate_pairs()` + `KLASS_*` shared vocab.
- T2 wrote `curate_merge_cases.py` → committed `data/merge/cases.json` (66 real consensus + 13
  synthetic scored); deterministic regen; resolver-input firewall + closed vocab; real-domain emails
  domain-masked to `example.test` (local-part token kept — proves the exact-match collision).
- T3 built `merge.html` + the `merge` build target (MERGE_* constants, load/validate/render/build/check,
  main() wiring) + `validate_merge_cases` + the launcher merge card; `dist/merge` byte-frozen on
  `--check merge`; `--check all` now 9 targets.
- T4 wrote `tests/merge-console.test.mjs` (73 assertions). T5 the substrate-emit handoff brief
  (pinned fc98b09). T6 full verification + CLAUDE.md true-up to "Six ship artifacts".
- STANDARD adversarial review ran. Confirmed A3 (dist additive + boundary-validated) and A5
  (build-time curation, no live spine) held; found + fixed a validator-parity gap (the build firewall
  was weaker than curate's — omitted the `note` leak-key; didn't enforce real cases are basis=strong /
  spine_verdict=kept_distinct). Both validators now mirror exactly.

## Decisions Made

- [[phase-76-merge-console-as-sixth-ship-artifact|Merge console is a 6th SHIP artifact, not a workbench beat]]
- [[phase-76-consensus-vs-scored-honesty-split|Consensus-vs-scored split is the load-bearing honesty seam]]
- [[phase-76-build-py-firewall-curation-companion-side|build.py firewall holds; curation is companion-side]]
- [[phase-76-ship-all-66-candidate-shares|Ship all 66 real candidate SHARES (completeness over sampling)]]
- [[phase-76-validator-parity-build-mirrors-curate|The build-boundary validator must mirror curate's firewall exactly]]

## Problems Solved

- How to honestly carry both a scored dimension and real un-scored cases in one console — split the
  populations and make the split visible (real=consensus-no-oracle; synthetic=scored-with-qualifier;
  the Reveal + ledger SPLIT them); real-substrate scoring stays a NAMED sibling handoff.
- Keeping `build.py`'s no-companion-import invariant while the console needs spine verdicts + scored
  oracle — curate at BUILD time (companion-side), `build.py` reads + validates the committed JSON
  standalone (the gate-console pattern).
- A validator-parity gap (build firewall weaker than curate's) — found by the adversarial review,
  fixed inline; the two now mirror exactly.

## Artifacts Changed

- `merge.html` (NEW — the Class-J console; Queue → Evidence → Adjudication → Reveal → Ledger)
- `scripts/curate_merge_cases.py` (NEW — companion authoring tool; reuses entity_spine + resolution_scorer)
- `data/merge/cases.json` (NEW committed — 66 real consensus + 13 synthetic scored)
- `dist/merge/index.html` (NEW byte-frozen ship artifact)
- `scripts/build.py` (the `merge` target: MERGE_* constants, load_merge_cases, validate_merge_cases [standalone], render/build/check_merge, main() wiring; --check all 8→9)
- `scripts/resolution_scorer.py` (oracle 8→25 obs / 5→17 clusters; candidate_pairs() + KLASS_*)
- `data/entity-spine/true_entities.json` (expanded synthetic oracle)
- `launcher.html` + `dist/index.html` (the merge card — the sanctioned launcher cascade; only existing dist changed)
- `tests/merge-console.test.mjs` (NEW — 73 assertions)
- `tests/test_selftests.py` (curate_merge_cases + merge-console arc added to the pytest umbrella)
- `docs/substrate-true-entities-emission-PLAN-BRIEF.md` (NEW sibling handoff, pinned fc98b09)
- `CLAUDE.md` (`## Current state` trued up to "Six ship artifacts"; 413 → 447 lines)

## Related

- [[phases/phase-76-merge-adjudication-console|Phase 76 — The merge-adjudication Class-J console]] — parent phase
- [[phases/phase-75-consume-substrate-v05-er-emission|Phase 75]] — the over-merge finding this consumes

## Soft Observations / Phase N+1 Candidates

- The substrate-true-entities-emission handoff (`docs/substrate-true-entities-emission-PLAN-BRIEF.md`,
  pinned fc98b09) would let the merge console SCORE the real 66 too (today consensus-only) — a sibling
  aml-substrate phase, NOT a signal-watch task. | evidence: T5 brief + ledger A4/T5 deferral
- Refuted-but-recorded known property: the oracle JSON is inlined in `dist/merge` view-source (the
  gate-accepted offline-single-file pattern — triage/console inline their reveal answers too; the
  render layer never surfaces it pre-adjudication; the non-negotiable forbids server-gating). If a
  stricter bar is ever wanted, build-time obfuscation is the only honest fix (net-new vs siblings).
- `CLAUDE.md` is at 447 lines, well over the ~200 maintenance-contract target (pre-existing bloat,
  not Phase-76-introduced) — a hygiene-trim phase is a candidate. | evidence: CLAUDE.md `## Current state`
- Remaining deferred ER pieces stay named in the standards: probabilistic/Splink ER, graph/Kuzu, the
  medallion/DuckLake stack.
