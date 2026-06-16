---
title: Phase 51 — Corpus redundancy measurement (the §13 fm-1 frontier, measured honestly)
phase: 51
status: active
ceremony: standard
created: 2026-06-16
updated: 2026-06-16
tags: [measurement-workstream, corpus, redundancy, composition, lfcm, fm-1, measure-first, non-ship]
---

# Phase 51 — Corpus redundancy measurement

The first deliverable of the **measurement workstream** stood up by the 2026-06-16 measure-first
direction: convert a chosen-not-measured headline into a MEASURED result. The composition value-prop
pivoted (post-triple-null) to **redundancy-management** as one of its three surviving legs — and the
blueprint §13 failure-mode-1 (correlated double-counting) is REAL on committed data: the corpus pools
2,251 indicators across 5 regulators that it deliberately **refuses to de-duplicate on honesty
grounds**. This phase measures that redundancy EXPOSURE honestly, as a non-ship analysis artifact —
the composition-as-redundancy-management demonstration on real grounded data the triple-null does not
touch.

## Objective

Produce a **non-ship measurement artifact** (the `blueprint-report.html` / `probe-history.md` class —
read-only over the committed corpus) that quantifies the cross-regulator redundancy exposure of the
committed signal library, WITHOUT touching the frozen ship corpus and WITHOUT violating the
no-similarity/no-dedup non-negotiable.

## Approach — the HYBRID (user gate, 2026-06-16)

1. **Deterministic co-occurrence (the in-constraint UPPER BOUND).** Cross-tab the 2,251 indicators by
   (typology × capability) × regulator. Typology resolved via the overlay maps (per-indicator override
   in `data/indicator-typology-map.json` else doc-level inherit from `data/typology-map.json`),
   capability = the C-code on the derived record, regulator = the `CORPUS_SOURCES` id. Report the
   UPPER BOUND: % of indicators that co-occur with another regulator's indicator in the same
   (typology, capability) cell. This is honest UNION/CO-OCCURRENCE arithmetic over EXISTING committed
   labels — the class `CLAUDE.md:204` explicitly allows — framed as **candidate co-occurrence**, never
   as dedup/overlap/lift.
2. **Sampled consensus-class semantic-equivalence (the measure-not-claim REFINEMENT).** Take a blind
   sample of cross-regulator co-occurring pairs; a blind rater judges semantic equivalence; report the
   equivalence RATE (consensus, never ground truth, illustrative — the Phase-34 inter-rater doctrine).
   The honest redundancy ESTIMATE = upper bound × sampled equivalence rate, each number carrying its
   measurement definition.

Output framing: *"candidate cross-regulator redundancy ≤ X% (deterministic label co-occurrence,
in-constraint); a blind sample estimates ~Z% of co-occurring pairs are semantically equivalent
(consensus, not ground truth) → estimated real redundancy ~Y%."* Never "the corpus is X% redundant."

## Constraints (LOAD-BEARING — abort if violated)

- The SHIP corpus (`corpus.html`, `dist/corpus`, every `data/*/derived/*.json`, the 3 overlays) stays
  BYTE-FROZEN and read-only. The signal-watch abort rule applies: dist/derived drift → STOP.
- The artifact is NON-SHIP (a `scripts/` measurement + a report; NOT a `build.py` dist target). It
  carries the always-on "Illustrative data & outputs" badge.
- NO de-duplication of the corpus; NO similarity number ON the ship artifact. The semantic-equivalence
  number is sampled + blind + consensus-class + illustrative — never a validated dedup or a lift/precision figure.
- Every number carries its measurement definition (§10 discipline; the "chosen, not measured"
  honesty applied to the sampling params).

## Exit criteria

A committed non-ship artifact (script + report) reporting the deterministic upper-bound co-occurrence
fraction + the sampled consensus-class equivalence estimate, both with measurement definitions and the
always-on badge; `python3 scripts/build.py --check all` still byte-identical (ship corpus untouched);
a `--selftest` on the measurement script.

## Abort rule

Ship corpus / dists drift → STOP and surface (never re-baseline). If the typology overlay proves too
sparse to make (typology × capability) a meaningful cell (A1), fall back to (capability × regulator)
and report the coarser axis honestly rather than forcing the finer one.
