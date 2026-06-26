---
title: "Phase 77: Consume the three sibling emissions — exogenous-disposition validation harness · casework cleared → Lakeshore DECIDE · true_entities → merge real-scoring"
aliases: ["phase 77", "three sibling consumes", "circularity exit + cleared + merge real-scoring"]
category: phases
tags: [consume, cross-pillar, exogenous-disposition, casework-cleared, true-entities, merge-console, validation-harness]
parents: []
created: 2026-06-26
updated: 2026-06-26
source: plan
status: completed
scope: ["scripts/validate_determination.py", "data/determination-eval/**", "vendor/aml-casework/**", "scripts/vendor_casework.sh", "scripts/serve_workbench.py", "scripts/serve_chain.py", "data/casefile/**", "scripts/curate_merge_cases.py", "scripts/build.py", "data/merge/cases.json", "data/entity-spine/**", "merge.html", "tests/merge-console.test.mjs", "dist/merge/**", "docs/**", "CLAUDE.md"]
entry_criteria: "Phase 76 delivered + accepted; the three sibling emissions code-verified live (substrate f2da3e4, casework b3546d4)."
exit_criteria: "All three consumes built + verified; --check all 9 targets (only dist/merge re-frozen); build.py imports no spine/scorer/sibling/curate; all arcs + the harness selftest + pytest green; CLAUDE.md + build-order + the three consumed briefs trued up; the open-data fork parked as a substrate brief."
---

# Phase 77 — Consume the three sibling emissions

## Objective

Consume the NEW sibling work landed this session into the signal-watch demo surface: substrate
advanced fc98b09→f2da3e4 (Phase 29 slice-aligned `true_entities` + Phase 30
`exogenous-disposition-label`, both additive/firewalled/eval-only) and casework advanced
4a858e6→b3546d4 (Phase 17 advisory CI lane + Phase 18 the `cleared` affirmative-dismissal
disposition). Three independent consumes, ordered by strategic depth: (1) the exogenous-disposition
VALIDATION HARNESS — the "circularity exit", validating the determination engine against an
independent oracle it didn't produce; (2) casework `cleared` → the Lakeshore DECIDE signs a documented
dismissal; (3) `true_entities` → score the merge console's REAL 66, one-sided and framed honestly.

## Scope

- `scripts/validate_determination.py`, `data/determination-eval/**` (T1 the harness)
- `vendor/aml-casework/**`, `scripts/vendor_casework.sh` (T2 re-vendor)
- `scripts/serve_workbench.py`, `scripts/serve_chain.py`, `data/casefile/**` (T3 Lakeshore cleared DECIDE)
- `scripts/curate_merge_cases.py`, `scripts/build.py`, `data/merge/cases.json`, `data/entity-spine/**` (T4 the real-66 scored oracle)
- `merge.html`, `tests/merge-console.test.mjs`, `dist/merge/**` (T5 one-sided framing render + re-freeze)
- `CLAUDE.md`, `docs/**`, `tests/**` (T6 verification + true-up)

## Exit Criteria

- [ ] `scripts/validate_determination.py --selftest` green; `evidence_requirements.py` byte-unchanged; the label is never an engine input
- [ ] casework re-vendored to b3546d4; the existing DECIDE signings unchanged (no regression)
- [ ] the Lakeshore DECIDE signs `cleared` (grounded exculpatory, no fabrication; casework file bar byte-unchanged)
- [ ] `curate_merge_cases.py --selftest` green — the real 66 carry a one-sided substrate-sourced oracle; firewall held; `build.py merge` validates the new shape
- [ ] `merge.html` renders the one-sided framing; `merge-console.test.mjs` green; `dist/merge` re-frozen + byte-stable
- [ ] `--check all` 9 targets (only dist/merge changed); build.py imports no spine/scorer/sibling/curate; all arcs + harness selftest + `uv run pytest` green; CLAUDE.md + build-order + the three consumed briefs trued up

## Constraints

- AUTHORING-TIME consume: substrate emissions re-emitted from a pinned slice (pin substrate f2da3e4, the `curate_workbench_cases` pattern); the dist reads only committed data — prevents a live substrate/casework read in any dist.
- Companion-only except the ONE dist touch (`dist/merge` re-freeze for consume #3) — prevents non-merge dist drift.
- build.py imports no spine/scorer/sibling/curate — preserves the byte-frozen-dist boundary.
- Honesty governor: synthetic-only qualifiers on every scored number; NO catch-rate/lift/precision; always-on badge — prevents a scored number reading as a real catch-rate.
- The resolver-input firewall: the real-66 oracle rides the revealed `oracle` block, never the pre-disposition evidence — prevents truth leaking into the gate's input.
- The determination engine + the casework file bar stay BYTE-UNCHANGED (the A1/A2/A3 invariants).

## Checkpoints

- After T2 (re-vendor): confirm the existing DECIDE signings are unchanged before T3 builds the cleared path.

## Assumptions

- A1 (accept-with-shaping): consume #3 scores the HUMAN adjudicator one-sided (catches over-merges), framed honestly. If the oracle can only score the spine / fabricates a should-merge / leaks truth → STOP, defer #3 to post-fork.
- A2–A5 (accept-with-evidence, all code-verified this session). If wiring the harness needs an engine change, or the label enters the engine input → STOP (circularity is back). If the re-vendor regresses signings or `cleared` needs the file bar weakened → STOP.

## Notes

The open-data fork (the two-sided real merge oracle) is PARKED as
`docs/substrate-open-reference-data-fork-PLAN-BRIEF.md` (substrate-side, contract-neutral), NOT a
signal-watch task. Spec `specs/phase-77-consume-sibling-emissions.md` (the orchestrator authors it).
Ledger Phase 77. Decisions: [[decisions/phase-77-exogenous-disposition-harness-circularity-exit]] ·
[[decisions/phase-77-casework-cleared-lakeshore-translation]] ·
[[decisions/phase-77-consume-3-true-entities-one-sided]] ·
[[decisions/phase-77-three-consumes-one-phase-fork-parked]].

## Delivery Outcome (DELIVERED + accepted 2026-06-26)

As delivered, ONE consume landed + TWO deferred against discovered sibling state — each routed to a
NAMED brief, never left open. Companion-only: all 9 ship dists BYTE-FROZEN; build.py imports no
spine/scorer/sibling/curate; `evidence_requirements.py` + the casework file bar BYTE-UNCHANGED.

- **T1 (the circularity exit) → DEFERRED (DISCOVERY).** Verified @f2da3e4 by code that substrate's
  `emit_true_entities`/`emit_intended_disposition` are tested-but-UNWIRED into the CLI (only the
  `--identity` parquet is CLI-reachable) → authored `docs/substrate-emit-cli-wiring-PLAN-BRIEF.md`.
- **T2 (re-vendor) → DONE.** casework bf15535→b3546d4 (`VENDORED_AT`); gate funnel IDENTICAL
  (202/111/63) — no signing regression.
- **T3 (casework `cleared`) → DONE via a C5 PROXY (USER OVERRIDE option b).** Lakeshore CASE-B
  fails-closed at casework's fan-OUT-only C3 (Lakeshore's C3 is fan-IN; A3 abort held — no fan-out
  fabricated) → casework's `cleared` consumed end-to-end on a casework-replayable C5 cash-placement
  proxy (`data/casefile/cleared-demo.bundle.json`, adversarially-reviewed honest) →
  `docs/casework-c3-fan-in-PLAN-BRIEF.md`.
- **T4 (real-66 scoring) → ATTEMPTED → DEFERRED at the abort rule.** The slice-aligned `--identity`
  parquet emits clusters content-addressed `ENT-<entity_ref>` (1:1 relabel of the spine's decision
  key; 66/66 DISTINCT) → scoring is CIRCULAR → reverted the real-66 to the Phase-76 CONSENSUS state
  (the circular capture NOT committed; the two-sided synthetic-13 untouched).
- **T5 → N/A (voided by T4).** merge.html/cases.json/test reverted to Phase-76; dist/merge byte-frozen.
- **T6 → DONE.** `--check all` 9/9 byte-frozen; `uv run pytest` 24/24; arcs green; CLAUDE.md +
  `docs/cross-pillar-build-order.md` + the consumed briefs trued up.

Ledger revisit: A1 **bit** (the planned consume could not honestly score the real 66 — both the JSON
one-sided path and the parquet two-sided reframe failed; the abort fired) · A2 **bit** (the harness
oracle was CLI-unreachable; deferred) · A3/A4/A5 **held**. The open-data fork is the unblocking move
for both the two-sided real merge oracle and realistic identifier collisions.
