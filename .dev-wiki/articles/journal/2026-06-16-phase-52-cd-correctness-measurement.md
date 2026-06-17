---
title: "Phase 52 — C/D-tag reliability measurement (the unguarded dimension, measured)"
date: 2026-06-16
type: journal
phase: phase-52-cd-correctness-measurement
tags: [measure-first, corpus, honesty, c-d-tags, non-ship, consensus, delivered]
---

# Phase 52 — C/D-tag reliability measurement

Planned + delivered + accepted in one session (lite ceremony, 4 tasks). The measure-first
workstream's SECOND measured number, the sibling of Phase 51 (corpus redundancy). Measures the ONE
corpus dimension the grounding gate explicitly never checks — the per-indicator C (capability) /
D (data-source) codes ("a grounding gate ≠ a completeness gate ≠ a correctness gate"). NON-ship,
read-only; ship corpus byte-frozen throughout.

## What shipped

- `scripts/cd_correctness.py` — stdlib, deterministic, read-only; **reuses
  `corpus_redundancy.load_indicators`** (one corpus reader for both measurements). One blind rater,
  two deterministic strata; `--sample-random` / `--sample-divergence` (blind dumps), `--verify-fixtures`
  (integrity), `--report`, `--selftest`.
- `data/cd-correctness/{random-sample.json, divergence-sample.json}` — committed blind-rater fixtures
  (judged once, replayed). Non-corpus; build.py never reads them.
- `docs/cd-correctness-report.md` — the non-ship deliverable (always-on Illustrative badge).

## The measured result (n=24/stratum, seed 0, blind claude-opus-4-8 rater)

- **RANDOM stratum (self-consistency):** blind free re-rate agrees with committed **C 0.625 (15/24),
  D 0.625 (15/24), both 0.417 (10/24)** — REPRODUCIBILITY, not validated correctness.
- **DIVERGENCE stratum (closer-to-independent, pairwise over the 213 Phase-34 corrections):** uphold
  the correction (rater-B) **17/24 (0.708)**, original 6, both-defensible 1, **neither 0**.

## The finding

The unguarded C/D dimension is **soft** (a same-model rater reproduces a free assignment only
~62.5%/axis — self-consistency) but **adjudicable on the hard cases** (forced pairwise, the blind
rater upholds the committed correction 17/24). **These are two separate measurements, NOT
subtractable** — different samples (random corpus vs the pre-selected hard divergences), different
tasks (open free assignment vs forced pairwise), not even the same metric; and a forced choice scores
mechanically higher than free assignment regardless of quality. The vocab demonstrably HAS overlapping
neighbours (C8 income-inconsistency vs C14 KYC-cooperation for "unexplained source of funds"; C15
shell vs C17 PEP-proxy for a PEP-owned shell), so defensible adjacent-code scatter is **plausibly** one
driver of the random mismatch — but **its share is unmeasured**. Honest bound: not "X% correct," but
reproducible-enough + adjudicable on the hard subset; ~⅓ of free assignments land on a **different**
code whose error-vs-defensible composition was not adjudicated. (At n=24 the two rates are
statistically indistinguishable — Wilson intervals overlap.) [Tightened post-delivery after the
wiki-capture adversarial review flagged the original "gap = scatter, not error" as an overclaim.]

## Gate / honesty

Direction gate all_accept: true (A0 self-consistency-not-correctness · A1 blindness-by-construction ·
A2 n=24/seed-0 illustrative · A3 non-ship byte-frozen). Both blind raters `tool_uses: 0` (A1 held —
no repo read). `--check all` 7/7 zero drift; build.py no `cd_correctness` reference; honesty grep
clean. The claim I most expected to be challenged — a same-model rater inflating self-consistency via
shared bias — is mitigated by labeling the random number "reproducibility" and leaning the finding on
the divergence stratum (a real two-pass disagreement).

## Soft Observations / Phase N+1 Candidates

- **Genuine independence (named, deferred-with-owner):** wire a DIFFERENT model family (or a human)
  as the rater to convert the random self-consistency number into a real independent-reliability
  number. The current number can only lower-bound. Evidence: A0 + the report honesty boundary.
- **Larger N to de-noise:** the random both-axes 0.417 at n=24 is noisy; a larger sample tightens the
  first instance. Chosen-not-derived params (A2). Evidence: `--report`.
- **Deterministic heading→capability residual (the Phase-37 thread):** replace the neural rater with a
  deterministic section-heading→C map on the subset where the heading determines the capability — more
  build than measure, subset-only; carried, not built.
- **Adjacent-code-scatter → taxonomy signal:** the demonstrated overlapping neighbours suggest the C/D vocab has
  defensible-neighbour clusters; a "defensible-neighbour" set in `capability-taxonomy.json` (or a
  vocab consolidation) could make the dimension more determinate. Measurement input, not a fix yet.
- **The measure-first workstream's remaining named candidates:** the casework audit-walk-to-source
  verifier (aml-casework-rooted) and the structure-detector reachability probe (aml-substrate-rooted)
  — both route to sibling repos, not signal-watch.
