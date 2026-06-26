# Cross-pillar build order (verified snapshot)

> **A signal-watch-authored coordination snapshot — the program-level "what's next, in what order" view
> across the 3 pillars.** Per-gap detail lives in the `*-PLAN-BRIEF.md` files; this is the sequencing over
> them. **Code-verified 2026-06-26** against these live HEADs — **re-verify before acting; sibling state
> drifts between sessions:**
> - **aml-substrate** `f2da3e4` (Phase 30, `main`) — *advanced from `fc98b09` since the last snapshot*
> - **aml-casework** `b3546d4` (Phase 18, `feat/phase-1a-deterministic-verifiers`) — *advanced from `4a858e6`*
> - **signal-watch** `b18ef71` (Phase 76, `main`)
>
> Synthetic / illustrative; no catch-rate, lift, or precision asserted.

## What changed since the last snapshot

Both siblings executed the prior build order. **Tracks A and B are now largely DONE; the work shifts to
signal-watch consuming the three new emissions, plus a new substrate realism FORK.**

- **substrate Phase 29** — slice-aligned `true_entities` emission (`identity/true_entities.json`, firewalled,
  100% coverage). ✓ CODE EXISTS — **but `emit_true_entities` is UNWIRED into the substrate CLI** (called only in
  substrate tests). *Critical nuance (Phase-77 finding): clusters are content-addressed `ENT-<entity_ref>` — a 1:1
  relabel of `entity_ref`, the SAME field the spine keys on → a CIRCULAR oracle for the real merge cases (agreement
  is true-by-construction, no discriminating signal). Even wired, it can't score the spine's real refusals honestly.*
- **substrate Phase 30** — `exogenous-disposition-label` (`eval/intended_disposition.json`, `file|clear` authored
  blind to the sufficiency rule). ✓ CODE EXISTS — **also UNWIRED into the CLI** (`emit_intended_disposition` is
  test-only). Both gaps → the `substrate-emit-cli-wiring-PLAN-BRIEF.md` handoff.
- **casework Phase 17** — reconciliation tripwires wired to an advisory (warn-never-fail, non-required) CI lane.
  ✓ DONE. *No promotion-to-blocking criterion yet — a named follow-on.*
- **casework Phase 18** — the `cleared` affirmative-dismissal verdict (CW-4). ✓ DONE; file bar byte-unchanged.

## Phase 77 outcome (signal-watch, implemented — the Track-C′ consume)

The three consumes landed with two honest pivots forced by the CLI-unwiring discovery above:

1. **`true_entities` → merge console real 66.** ⛔ **DEFERRED at the abort rule (oracle is CIRCULAR).** The
   attempt: capture the slice's identity ground truth from substrate's `--identity` parquet → score the 66. The
   finding: substrate's emitted clusters are content-addressed **`ENT-<entity_ref>` — a 1:1 relabel of `entity_ref`,
   the SAME field the spine keys its refuse/merge on.** So "66/66 correct-rejection" is true-by-construction (zero
   discriminating signal), not a measurement. Presenting it as scoring would breach A4 / the abort rule. The real-66
   stay **CONSENSUS** (Phase-76 framing, no oracle); `dist/merge` UNCHANGED (byte-frozen). A non-circular real merge
   oracle needs `entity_ref ≠ cluster` — a genuine identity layer (household/fragment merges) or the open-data fork's
   real collisions (Track B′). The synthetic-13 scoring is sound + untouched (genuinely two-sided). *The
   `substrate-emit-cli-wiring` brief is re-scoped: wiring the CLI is necessary but NOT sufficient — substrate must
   emit a true-identity layer, not an entity_ref echo.*
2. **`intended_disposition` → determination validation harness.** ⛔ DEFERRED — the emit is CLI-unwired (can't curate
   the oracle at build time without a substrate CLI run). Re-scoped to the `substrate-emit-cli-wiring-PLAN-BRIEF.md`
   handoff (wire BOTH emissions). The engine-vs-exogenous-label harness builds once substrate emits from its CLI.
3. **`cleared` → DECIDE signs a documented dismissal.** ✓ CONSUMED via a C5-replayable proxy: re-vendored casework
   `→b3546d4`, authored `data/casefile/cleared-demo.bundle.json` (C5 cash-placement, `exculpatory:true`), passes
   `--disposition cleared` → **casework SIGNS `cleared` end-to-end**. The north-star **Lakeshore CASE-B still
   fails-closed** (casework's C3 is fan-OUT-only; Lakeshore's is fan-IN) → the `casework-c3-fan-in-PLAN-BRIEF.md`
   handoff. The A3 abort held — no fan-out pattern fabricated to force the sign.

## Build order — now

### Track C′ — signal-watch CONSUME (the active next phase; Phase 77 candidate)
The bottleneck moved here. Three consumes, in rough value order:
1. **Consume Phase 29 `true_entities` → score the merge console's real 66.** `curate_merge_cases.py` reads
   `identity/true_entities.json`, looks up each SHARES pair's clusters → flips the 66 from consensus to scored.
   Honest result: **66/66 correct-rejection** (the spine's refusals confirmed against substrate's declared-identity
   truth). Frame the one-sidedness explicitly (no should-merge in the real slice). Rebuilds `dist/merge`.
2. **Consume Phase 30 `intended_disposition` → a determination-engine validation harness** (the circularity exit):
   pass bundles (no label) through `evaluate_sufficiency` → compare to the exogenous `file|clear`. Companion-only,
   synthetic-only-qualified. The highest *strategic* consume (validates the engine against an oracle it didn't make).
3. **Consume casework Phase 18 `cleared` → the Lakeshore DECIDE signs a documented dismissal.** Re-vendor
   `bf15535→b3546d4` (`scripts/vendor_casework.sh`); shape the Lakeshore case into a **casework-contract bundle**
   (v0.1, an `exculpatory:true` txn + neutral/exculpatory claims) and pass `--disposition cleared`. Completes the
   rich-case loop (Lakeshore signs `cleared` via casework, not just signal-watch's own engine).

### Track B′ — aml-substrate, next (the realism FORK; parallel, contract-neutral)
- **The open-reference-data fork** — anchor the synthetic universe to open data (GLEIF CC0 ownership + Census/SSA
  names + OSM/GeoNames addresses + government sanctions/FATF anchors), routing around the 4 NC/ND/SA/paid traps.
  Brief: [`substrate-open-reference-data-fork-PLAN-BRIEF.md`](substrate-open-reference-data-fork-PLAN-BRIEF.md)
  (`f2da3e4`). It's realism of *values*, not *contract* — consumers read the same shape. Direct payoff: makes the
  merge console's real cases real-shaped collisions (not the artificial noise floor) and gives `true_entities` a
  non-trivial, two-sided oracle. **Sequence after the Track C′ consume settles** unless the artificial collision
  floor is judged the demo's current weak point.
- *(optional)* a `true_entities` refinement: emit clusters from substrate's genuine identity LAYER (the
  `--identity` household/fragment merges) rather than content-addressed-from-`entity_ref`, so the real-data oracle
  becomes two-sided. Folds naturally into the fork.

### Track A′ — aml-casework, next
- **Promotion criterion for the advisory CI lane** (N clean cycles, zero false positives → blocking) — the named
  follow-on from Phase 17.
- The speculative C15/C3/C4 widening stays **dropped** (not data-reachable; documented audit trail only).

## Critical path

The prior bottleneck (`substrate true_entities`) is **resolved** — it's emitted. The only remaining serial
dependency is **signal-watch's Track C′ consume** of what already exists; nothing blocks it. The substrate
realism fork (Track B′) and casework's promotion criterion (Track A′) run in parallel and block no one.
