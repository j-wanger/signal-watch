---
title: "Phase 53 — C/D disagreement decomposition (the named follow-up, delivered)"
date: 2026-06-16
type: journal
phase: 53
tags: [measure-first, corpus, honesty, c-d-tags, non-ship, decomposition, kappa, confound]
---

# Phase 53 — C/D disagreement decomposition

Planned + delivered same session (lite, 4 tasks). The measure-first workstream's THIRD number, and
the direct completion of Phase 52: its report named the open gap (the ~⅓ random-stratum mismatch's
"error-vs-defensible composition was NOT adjudicated"; "a clean decomposition would require the
forced-pairwise adjudication on the SAME random-stratum mismatches"). Phase 53 ran exactly that, over
an enlarged sample, + added the chance-corrected statistic (Cohen's κ) the report flagged as missing.

## What shipped (NON-ship analysis; ship corpus byte-frozen, `--check all` 7/7 zero drift)

- `scripts/cd_correctness.py` extended (pure reuse): decomposition sampler (reads the enlarged random
  fixture, selects its per-axis mismatches, presents each forced-pairwise via the existing
  `divergence_options` pattern), decomposition scorer (committed-better=error / both=defensible /
  blind-better=committed-questionable / neither=escalate), Cohen's κ + Wilson CIs. selftest extended.
- `data/cd-correctness/random-sample-large.json` (n=96 blind re-rate) + `decomposition-sample.json`
  (62 mismatch adjudications). Both blind raters ran `tool_uses: 0` (blindness by construction).
- `docs/cd-correctness-report.md` — a Phase-53 section completing the report's own named follow-up.

## Measured

- **Enlarged random (n=96):** self-consistency C/D **0.677** (65/96), **κ ≈ 0.65 ≈ raw** → the
  agreement is GENUINE, not chance-inflated (the 28/20-way vocab makes chance agreement small); closes
  the "not chance-corrected" gap. Reproduces the Phase-52 n=24 0.625 (Wilson CIs overlap).
- **Decomposition (62 mismatches = 31 C + 31 D):** both-defensible **1/62 (1.6%)**, neither **0/62** →
  the Phase-52 "plausibly scatter, not error" guess is **REFUTED**: disagreements are SHARP, not a fog
  of equally-good neighbours. Direction: committed-better **23/62 (37%)** / blind-better **38/62 (61%)**.

## The honest finding (it diverged from the plan)

The decomposition did NOT yield a clean "committed codes are X% wrong." Two results:
1. Disagreements are adjudicable/sharp (refutes scatter).
2. The DIRECTION is **confounded**: committed codes were assigned with FULL document context; both blind
   raters saw only flag+red_flag. A flag-only adjudicator naturally sides with the flag-only re-rate. So
   committed-better 37% = clean LOWER bound on committed-upheld; blind-better 61% = UPPER bound on
   committed-questionable, an UNMEASURED mix of genuine error + the context-asymmetry confound (NOT a
   committed-error rate). The "share unmeasured" caution one level down — the same trap Phase 52's
   correction caught; did not assert the confound dominates.

## A0 surprise (the planned bound mechanism was wrong)

The gate's A0 predicted the same-family adjudicator would inflate *both-defensible* (rate its own scatter
generously), making error a lower bound *because* scatter was over-counted. That mechanism **did not
fire** (both-defensible ≈ 0). The actual confound is **context asymmetry** — the two flag-only raters
side with each other against the full-context committed code. The bound still holds, for a different
reason. Recorded honestly rather than retrofitted (assumption-ledger A0 revisit-status = bit).

## Process notes

- Inline artifact writing (not the dev-plan/debrief background-executor dispatch) — judgment call: the
  living docs (`_CURRENT_STATE.md` 75KB, `active-phase.md` = the cross-pillar program record) are
  hand-maintained and surgical edits are lower-risk than a full-section rewrite agent. Anti-theatre.
- The first blind rater dropped 1 of 96 items (a duplicate-flag entry, `fintrac-guid-casinos/IND-17`);
  a fresh single-item blind rater filled it (SendMessage unavailable to continue the original). Integrity
  preserved — the rebuilt fixture's gids == the seeded sample.

## Soft Observations / Phase N+1 Candidates

- **Context-matched reliability rater (the sharpened follow-up).** The Phase-53 confound shows a
  flag-only re-rate is NOT a fair test of full-context committed codes. The deferred independent rater
  (different model family / human) must be **context-matched** — given the source-doc context the
  committed code had, OR run flag-only on BOTH poles — else it re-measures the context gap, not
  reliability. This converts the bound into a clean number. Evidence: decomposition blind-better 61%
  confounded; committed-better 37% (clean lower bound) survives even the disadvantaged test.
- **Reusable measurement lesson (wiki-capture candidate, cross-project).** When measuring a neural
  judgment's reliability via blind inter-rater agreement, the raters MUST share the same context as the
  reference assignment — otherwise the measurement collapses to a context-asymmetry artifact. The
  cheapest honest design matches context on both poles. Generalizes beyond C/D tags to any
  blind-re-rate-vs-committed reliability probe.
- **κ-beside-raw should be standard.** At a 28/20-way vocab, κ ≈ raw confirmed the self-consistency is
  genuine — the chance-correction lever is one function and cheap; fold it into any future tag-reliability
  measure.
- **Heading→capability determinism probe** (the Phase-37 thread) — the still-unmeasured deterministic
  alternative to a neural C rater on the subset where a section heading constrains C. Carried, not this phase.
- **Routes to sibling repos** (un-drivable from a signal-watch-rooted session): casework
  audit-walk-to-source; the structure-detector reachability probe (aml-substrate).
