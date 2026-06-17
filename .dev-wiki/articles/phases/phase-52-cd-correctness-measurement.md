---
title: "Phase 52 — C/D-tag reliability measurement (the unguarded dimension, measured honestly)"
type: phase
status: completed
ceremony: lite
milestone: M9
created: 2026-06-16
updated: 2026-06-16
tags: [measure-first, corpus, honesty, c-d-tags, non-ship, consensus]
---

# Phase 52 — C/D-tag reliability measurement (the unguarded dimension, measured honestly)

## Objective

Measure the reliability of the corpus's per-indicator **C (capability) / D (data-source)**
tags — the ONE dimension the grounding gate explicitly never checks ("a grounding gate ≠ a
completeness gate ≠ a correctness gate"; the C/D dimension is *unguarded*, working-knowledge).
The measure-first workstream's second deliverable, the sibling of Phase 51 (corpus redundancy):
convert an asserted-but-unmeasured headline ("the C/D tags are correct") into an honest measured
number, as a NON-SHIP analysis over the FROZEN corpus.

## Approach (gated 2026-06-16 — stratified, blind-rater, measure-not-claim)

One blind same-model rater, two deterministic strata (same instrument as Phase 51 T2):

- **Random stratum** (n=24, seed 0, from the 2,251 committed indicators) — the rater assigns one
  C + one D from `flag` + `red_flag` + the C1–C28 / D1–D20 vocab, **never seeing the committed
  code**. Agreement = blind == committed, per axis. Honestly labeled **self-consistency /
  reproducibility** (a same-model class redoing the original extraction task), NOT validated
  correctness.
- **Divergence stratum** (n=24, seed 0, from the 213 Phase-34 console cases) — the rater sees
  `flag` + `red_flag` + the two candidate codes presented **neutrally** (order fixed by seed),
  picks option-1 / option-2 / both-defensible / neither, **never told which is the Phase-34
  correction**. Reported as uphold-correction / uphold-original / both / neither. The 213 are a
  real two-pass disagreement → the closer-to-independent number.

Deliverables (mirror Phase 51): `scripts/cd_correctness.py` (stdlib, deterministic, read-only) ·
`data/cd-correctness/{random-sample.json, divergence-sample.json}` (committed blind-rater fixtures,
judged once + replayed) · `docs/cd-correctness-report.md` (always-on Illustrative badge).

## Scope

- `scripts/cd_correctness.py` (NEW)
- `data/cd-correctness/*.json` (NEW — non-corpus; build.py never reads it)
- `docs/cd-correctness-report.md` (NEW)
- `.dev-wiki/*` (lifecycle)

## Key constraints

- **NON-SHIP, read-only.** The ship corpus (`corpus.html`, `dist/corpus`, every
  `data/*/derived/*.json`, the overlays) stays **byte-frozen**; `build.py` NEVER imports
  `cd_correctness.py`; `data/cd-correctness/` is non-corpus.
- **Measure-not-claim (A0).** The random number is **self-consistency / reproducibility, not
  validated correctness** — a same-model rater shares the original extractor's biases. Independence
  (different model family / human) + larger N **deferred-with-owner**. Never headline "X% correct".
- **Blind by construction (A1).** The rater (a subagent) never sees the committed code / which
  option is the correction; the script dumps blind, the orchestrator does NOT hand-rate.
- **Every number carries its measurement definition** (the §10 honesty grep); consensus, never
  ground truth; n=24 / seed 0 **chosen, not derived**.

## Exit criteria

- `python3 scripts/cd_correctness.py --selftest` GREEN; samples deterministic (byte-identical on
  re-run).
- `--verify-fixtures` GREEN (committed judgments match the seeded samples).
- `--report` emits both strata, every number definition-carrying, with the honesty boundary.
- `docs/cd-correctness-report.md` written (badge + both strata + finding + honesty boundary +
  reproduce).
- `python3 scripts/build.py --check all` → ZERO drift (7/7, ship corpus + all dists byte-identical).

## Abort rule

Any ship-corpus / dist drift → STOP and surface (the standing abort rule); never re-baseline.

## Assumptions

Direction-gate ledger: `.dev-wiki/assumption-ledger.md` Phase-52 block — A0 self-consistency-not-
correctness (the load-bearing honesty assumption, T0 weakest) · A1 blindness-by-construction · A2
n=24/seed-0 illustrative · A3 non-ship byte-frozen abort rule. all_accept: true.

## Deferred residual (named, not built)

The deterministic alternative to a neural rater: a **section-heading → capability** map (the
Phase-37 "how much is deterministic" thread) — replace the model rater with a deterministic one on
the subset where the heading determines C. More build than measure; covers only a subset. Carried
as a candidate, not this phase.
