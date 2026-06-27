# PLAN-BRIEF — aml-substrate: wire the eval-oracle emissions into the CLI

> **✅ RESOLVED 2026-06-27.** substrate Phase 31 (`9677a37`) wired `--emit-eval-oracles` across the CLI;
> Phase 32/33 (`31cb439`/`f9e63e7`) added the `--anchored` NON-circular identity oracle (opaque `GT-<hash>`
> clusters, `entity_ref ≠ cluster` — curing the Phase-77 circular-echo abort). signal-watch consumed BOTH
> across the tool-use boundary: **Phase 78** (the `intended_disposition` oracle → the determination-validation
> harness) + **Phase 79 T3/T4** (the `--anchored` identity oracle → the merge console's real-data SCORED
> population, superseding the consensus-66). The original handoff follows (historical).

> **A signal-watch → aml-substrate handoff brief** (the Phase-55–58 / 74–76 pattern: signal-watch authors the
> contract; the sibling implements on its own lifecycle — *no code lands in substrate from here*). Synthetic /
> illustrative; no catch-rate, lift, or precision asserted. **Pinned to verified substrate HEAD `f2da3e4`
> (Phase 30), code-verified live 2026-06-26** (a real emit + the call-site grep). Companion to
> [`cross-pillar-build-order.md`](cross-pillar-build-order.md).

## The gap (verified, not assumed)

Substrate Phase 29 + Phase 30 each added an **eval-only oracle emission FUNCTION** — but neither is wired into
the CLI, so no consumer can reach it across the tool-use boundary:

- `monitor/evidence.py::emit_true_entities(records, outdir)` → `<out>/identity/true_entities.json` (Phase 29,
  the slice-aligned `{entity_ref→cluster}` oracle).
- `monitor/evidence.py::emit_intended_disposition(records, outdir)` → `<out>/eval/intended_disposition.json`
  (Phase 30, the exogenous `{case_id, intended_disposition(file|clear), intended_basis}` oracle).

**Both are called ONLY in substrate's tests** (`test_true_entities_emission.py`, `test_disposition_emission.py`,
+ the firewall tests). `cli.py` calls `emit_evidence_bundles` (for `--emit-evidence`/`--emit-screening`) but
**neither `emit_*` oracle**. Verified by a real emit: `--clients … --emergence --monitor --emit-evidence
--emit-screening --identity` produces the bundles + `identity/true_entities.parquet` (the resolver's full
ground truth, via `--identity`) but **NEITHER `identity/true_entities.json` NOR `eval/intended_disposition.json`**.

Consequence for the consumer: signal-watch's **determination-engine validation harness** (the "circularity
exit" — validate `evaluate_sufficiency` against the independent `intended_disposition`) has **no boundary path to
its oracle**. It is DEFERRED (Phase 77 T1) pending this wiring.

**A DEEPER gap than wiring (Phase-77 T4 finding — read before scoping):** signal-watch also tried to score the
merge console's real-66 against true_entities by reading the CLI-reachable `--identity` **parquet** directly. It
STOPPED at the abort rule. The captured parquet emits clusters **1:1 with `entity_ref` (every cluster
`ENT-<entity_ref>` across all 441 slice persons; ZERO clusters merge distinct entity_refs)** — i.e. the oracle is
a relabel of the SAME field the spine keys its merge/refuse on, so any "score" is CIRCULAR (true-by-construction
agreement, no discriminating signal). Whether this is because the synthetic population genuinely has no
same-person fragments, or because the emission is content-addressed rather than read from the gen/identity
linkage, needs substrate-side confirmation. **Either way, wiring the JSON is necessary but NOT sufficient** for a
real merge oracle: the consumer needs `entity_ref ≠ cluster` — clusters that actually merge distinct entity_refs
(genuine household/fragment links, or the open-data fork's real collisions).

## EMIT (the ask)

Wire both oracle emissions into the CLI on the existing emit path (they are additive eval-only siblings — no gen
touch, no contract bump). A single flag is fine, e.g. `--emit-eval-oracles` (or fold into `--emit-evidence`/
`--emit-screening`, since the records are already collected there):

```
... --emit-evidence --emit-screening [--emit-eval-oracles] --out <out>
  → <out>/identity/true_entities.json        (emit_true_entities)
  → <out>/eval/intended_disposition.json     (emit_intended_disposition)
```

Both keyed to the SAME emitted slice population the bundles cover (`emit_evidence_bundles`'s `iter_slice_cases`).

## GROUND — the firewall (unchanged, must hold)

- The cluster id / disposition label are EVAL-ONLY: they appear ONLY in `identity/` and `eval/`, NEVER in the
  evidence bundles (`parties[]` / `identifiers[]` / `resolution_edges[]`) nor as a 1:1 surrogate — the existing
  `test_true_entities_firewall.py` / `test_disposition_firewall.py` guards stay green.
- `resolve/resolver.py` + `evidence_requirements`-equivalent stay byte-unchanged (the sole readers are
  `measure.load_slice_truth` / `measure.load_disposition_truth`).
- Additive: a consumer that ignores `identity/`+`eval/` behaves exactly as at `f2da3e4`.

## CONSUME (signal-watch side, once wired)

- The **determination-validation harness** (Phase-77 T1, deferred): read `eval/intended_disposition.json`; run
  `evaluate_sufficiency` on each bundle (NO label in); compare engine `file|clear` to the exogenous label →
  agreement (+ per-basis), synthetic-only qualified; engine byte-unchanged. The circularity exit.
- The **merge-console true_entities consume** (DEFERRED at the abort rule — see the deeper gap above). It can
  only be un-deferred once an emission (JSON or parquet) carries clusters from the genuine gen/identity LINKAGE
  (`entity_ref ≠ cluster` where real fragments exist), NOT a content-addressed `ENT-<entity_ref>` echo. The
  cleaner CLI-reachable JSON is welcome, but the merge console will keep the real-66 as CONSENSUS until the
  clusters are genuine — a content-addressed echo gives it nothing it can honestly score.

## Acceptance (sibling-side)

1. The documented emit produces `identity/true_entities.json` + `eval/intended_disposition.json` (not only the
   parquet). 2. The firewall tests stay green; bundles byte-identical with/without the flag. 3. The CLI `--help`
   names the flag. 4. *(the deeper ask, separable)* `true_entities` clusters are read from the genuine gen/identity
   linkage so that, where the population HAS same-person fragments, ≥1 cluster merges distinct `entity_ref`s
   (`entity_ref ≠ cluster`) — otherwise the merge-console real consume stays CONSENSUS (a content-addressed echo is
   not a scorable oracle). If the population genuinely has no fragments, say so — that itself is the answer (real
   collisions then come from the open-data fork).

**Pin: `f2da3e4`** · executed in an aml-substrate session · references the [true-entities](substrate-true-entities-emission-PLAN-BRIEF.md)
+ [exogenous-disposition](substrate-exogenous-disposition-label-PLAN-BRIEF.md) briefs (the emission shapes those
specify are BUILT — this brief only makes them CLI-reachable). **Out of scope:** any contract/engine change.
