---
title: "Phase 53 — C/D disagreement decomposition (error vs defensible-neighbor, measured honestly)"
type: phase
status: active
ceremony: lite
milestone: M9
created: 2026-06-16
updated: 2026-06-16
tags: [measure-first, corpus, honesty, c-d-tags, non-ship, consensus, decomposition]
---

# Phase 53 — C/D disagreement decomposition (error vs defensible-neighbor, measured honestly)

## Objective

Finish the Phase-52 finding. Phase 52 measured the unguarded C/D dimension and found it
**soft but adjudicable**, but its own report names the open gap: the ~⅓ of random-stratum
mismatches "whose error-vs-defensible composition was **not** adjudicated," and that "a clean
decomposition would require running the forced-pairwise adjudication on the **same** random-stratum
mismatches." This phase **is** that decomposition — it turns "the share of the disagreement that is
defensible-neighbour vs genuine-error is *unmeasured*" into a measured (bounded) split, and adds the
chance-corrected statistic (kappa) the report flagged as missing. The measure-first workstream's
THIRD deliverable, the sibling of Phases 51–52; a NON-SHIP analysis over the FROZEN corpus.

## Approach (gated 2026-06-16 — decompose-by-reuse, same-family adjudicator as a BOUND)

Pure reuse of the Phase-52 `cd_correctness.py` machinery — no new rater infrastructure:

- **Enlarge the random stratum** (n≈72–96, seed-fixed, corpus-proportional from the 2,251) — a blind
  same-model rater re-assigns one C + one D from `flag` + `red_flag` + the closed vocab, never seeing
  the committed code (the Phase-52 random stratum, larger N). Add **Cohen's kappa** (blind vs
  committed, per axis) alongside raw agreement.
- **Decompose its mismatches** — for every item where blind ≠ committed (on C, D, or either), present
  the two codes **neutrally** (the existing `divergence_options` forced-pairwise, seed-fixed order),
  and a blind rater picks: committed-better / both-defensible / blind-better / neither-escalate. Score
  the mismatch population into **genuine-error** (committed-better) / **defensible-neighbour**
  (both-defensible) / **committed-questionable** (blind-better) / **un-adjudicable** (neither).
- The adjudicator is a *same-Claude-family* fresh blind rater → the split is reported as a **BOUND**:
  error-share = **lower** bound, defensible-scatter-share = **upper** bound (A0). Genuine independence
  (different family / human) + a chance-corrected inter-rater panel (Krippendorff's α) stay
  **deferred-with-owner** (the gate's not-chosen alternative).

Deliverables (mirror Phases 51–52): `scripts/cd_correctness.py` (extended — decomposition sampler +
scorer + kappa) · `data/cd-correctness/{random-sample-large.json, decomposition-sample.json}` (NEW
committed blind-rater fixtures, judged once + replayed) · `docs/cd-correctness-report.md` (EXTENDED —
a decomposition section that completes the report's own named follow-up; always-on Illustrative badge).

## Scope

- `scripts/cd_correctness.py` (EXTEND — stdlib, deterministic, read-only; reuses `corpus_redundancy.load_indicators`)
- `data/cd-correctness/*.json` (NEW fixtures — non-corpus; build.py never reads it)
- `docs/cd-correctness-report.md` (EXTEND — add the decomposition section + kappa; Phase-52 sections intact)
- `.dev-wiki/*` (lifecycle)

## Key constraints

- **NON-SHIP, read-only.** The ship corpus (`corpus.html`, `dist/corpus`, every
  `data/*/derived/*.json`, the overlays) stays **byte-frozen**; `build.py` NEVER imports
  `cd_correctness.py`; `data/cd-correctness/` is non-corpus.
- **Decomposition = a BOUND, not a clean split (A0).** The adjudicator is same-Claude-family →
  error-share is a **lower** bound, defensible-scatter a **upper** bound; never present the split as
  exact or as genuine independence. `neither/escalate` is a first-class outcome (a spike = "un-adjudicable").
- **Blind by construction (A1).** Both raters (subagents) never see the committed code / which option
  is the committed one; the script dumps blind, the orchestrator does NOT hand-rate.
- **Every number carries its measurement definition + a chance-corrected companion** (Cohen's kappa
  beside raw %, Wilson CIs); consensus, never ground truth; n / seed **chosen, not derived**.

## Exit criteria

- `python3 scripts/cd_correctness.py --selftest` GREEN (decomposition sampler selects exactly the
  mismatches; forced-pairwise neutral order deterministic + both orders appear; error/scatter/
  blind-better/neither scoring; kappa math on a hand fixture); samples byte-identical on re-run.
- `--verify-fixtures` GREEN for the enlarged random + the decomposition fixtures (judgments match the
  seeded samples + the seed-fixed option order).
- `--report` emits the enlarged random stratum (raw + kappa + CI) and the decomposition (error /
  defensible / committed-questionable / neither, every number definition-carrying, framed as a bound),
  with the updated honesty boundary.
- `docs/cd-correctness-report.md` extended (decomposition section + kappa + the completed finding);
  honesty grep clean (no "X% correct/error"-as-fact).
- `python3 scripts/build.py --check all` → ZERO drift (7/7, ship corpus + all dists byte-identical).

## Abort rule

Any ship-corpus / dist drift → STOP and surface (the standing abort rule); never re-baseline. If the
decomposition is un-adjudicable (neither/escalate spikes) → report THAT as the honest finding, do not
force a split.

## Assumptions

Direction-gate ledger: `.dev-wiki/assumption-ledger.md` Phase-53 block — A0 same-family-adjudicator-
is-a-bound (the load-bearing honesty assumption, T0 weakest) · A1 decomposition-validity (the report's
named missing measurement) · A2 larger-N feasibility / kappa computable · A3 non-ship byte-frozen
abort rule. all_accept: true.

## Deferred residual (named, not built)

- **Genuine independence** — a different model family (local Qwen) or a human (domain-expert) rater →
  converts self-consistency / same-family-bounded into reliability; the gate's not-chosen alternative.
- **An inter-rater panel + chance-corrected α** (Krippendorff) treating the committed code as one more
  rater — the "proper statistic" the Phase-52 report named; needs ≥2 genuinely independent raters.
- **The heading→capability determinism probe** (the Phase-37 thread) — the deterministic alternative
  to a neural rater on the subset where a section heading constrains C. A new dimension, not this phase.

## Outcome (T1–T4 delivered 2026-06-16 — delivery gate pending acceptance)

All exit criteria met; `--check all` 7/7 zero drift; both blind raters ran `tool_uses: 0`.

- **Enlarged random stratum (n=96):** self-consistency C/D **0.677** (65/96), **Cohen's κ ≈ 0.65 ≈ raw** —
  the agreement is GENUINE, not chance-inflated (closes the report's "not chance-corrected" gap), and
  reproduces the Phase-52 n=24 0.625 (Wilson CIs overlap).
- **Decomposition (62 mismatches):** both-defensible **1/62 (1.6%)**, neither **0/62** → the Phase-52
  "plausibly scatter, not error" guess is **REFUTED** — the disagreements are SHARP. Direction:
  committed-better **23/62 (37%)** = clean LOWER bound on committed-upheld; blind-better **38/62 (61%)** =
  UPPER bound on committed-questionable, **CONFOUNDED** by context asymmetry (flag-only re-rate vs
  full-document committed) — NOT a committed-error rate; the error-vs-confound split is itself unmeasured.
- **A0 surprise (recorded honestly):** the predicted bound mechanism (same-family adjudicator inflates
  *both-defensible*) did NOT fire; the real confound is **context asymmetry** (the two flag-only raters
  side with each other against the full-context committed code). The bound still holds, for a different
  reason than planned. Follow-up reframed: an independent rater must be **context-matched** (or run
  flag-only on both poles), else it re-measures the context gap, not reliability.
- Artifacts: `scripts/cd_correctness.py` (extended) · `data/cd-correctness/{random-sample-large,decomposition-sample}.json` · `docs/cd-correctness-report.md` (Phase-53 section added).
