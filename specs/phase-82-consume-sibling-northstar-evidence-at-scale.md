# Spec — Phase 82: Consume sibling emissions — north-star evidence AT SCALE (substrate P39 predicate + P40 mitigation §12 loops) + merge org-collision class (P38) + casework P20 signing re-vendor

> STANDARD ceremony. Cross-pillar consume (3 substrate phases + 1 casework re-vendor) + a conditional
> ship-dist touch (`dist/merge`). Direction gate closed 2026-06-29 (AskUserQuestion): scope = **"Both
> clusters (full batch)"** — all four tracks; §12 frame = **"measure-first-with-fallback, rule frozen"**;
> merge-org = **"measure two-sidedness on our own path; one-sided → abort, dist/merge byte-frozen"**;
> casework = **"re-vendor + funnel re-measure, honest counts"**. Sibling HEADs code-verified LIVE this
> session (3 background investigators, file:line — not loaded facts): aml-substrate @**294d3e5** (Phase 40
> close; feat SHAs P38 `a9a088a` / P39 `1483c84` / P40 `978c8fe`); aml-casework @**04cc335** (Phase 21 close;
> feat P20 `a059fc5` / P21 `7398ddc`). Re-verify both HEADs at T1 — sibling state drifts.

## 1. Objective

Consume the sibling emissions that landed since signal-watch's last pins (substrate `f7fbdb0`→`294d3e5`,
casework vendored `076fb8e`→`04cc335`). All four were code-verified **READY** (CLI-wired, non-circular /
label-blind, two-sided where needed — none the Phase-77 unwired-or-circular trap). Notably **three of the
four directly answer handoff briefs signal-watch itself authored**:

- **substrate Phase 38** (`a9a088a`, org-fragment-emit) — answers `substrate-org-fragment-emit-PLAN-BRIEF.md`
  (the exact contract Phase 81's merge-org track aborted to): `apply_anchored_org_fork` mints `O-FRAG-`
  same-org fragment records sharing the base's `ENT-` cluster with a distinct `entity_ref` (the UPHOLD face),
  alongside distinct-org name collisions (the REJECT face). Emitted via `--anchored --emit-eval-oracles` →
  `identity/true_entities.json`. Substrate self-reports two-sided (seed 0: 16 uphold / 35 reject).
- **substrate Phase 39** (`1483c84`, predicate-reference-layer, "north-star evidence S#1") — Ask **#1** of
  `substrate-northstar-evidence-emission-PLAN-BRIEF.md`, the *keystone*: emits observable
  `reference.prior_str_register[]` + `named_predicate_risk` + `flagged` resolution edges the gate READS.
  Always-on via `--emit-evidence`/`--emit-screening`. Closes the measured **0-of-376** predicate gap (every
  slice case stalls at `needs_more_info` today). Label-blind (corr ≈ −0.006/+0.004).
- **substrate Phase 40** (`978c8fe`, affirmative-mitigation-evidence) — Ask **#2** of the same brief, the
  CLEAR-side mirror: emits `mitigation_evidence{established,basis,corroborants[]}` + `exculpatory:true` txn
  legs the gate reads to earn `mitigation_established`. ≥2-corroborant (non-echo, corr ≈ 0.02). Always-on.
- **casework Phase 20** (`a059fc5`, C15/C4 reconcile) — answers `casework-northstar-signing-PLAN-BRIEF.md`:
  reconciles C15 (shell throughput) + C4 (any-channel structuring) to substrate's real
  `ShellDetector`/`StructuringDetector` definitions; ~55 previously fail-closed cases (49 C15 + 6 C4) now
  SIGN. Phase 21 (`7398ddc`) is internal drift-hardening — a no-op the re-vendor picks up for free.

**The unifying frame — north-star at scale.** The same engine that decides the 2 hand-authored cases
(Northgate FILES / Lakeshore CLEARS, Phase 73) now decides the **generated 376-case slice** end-to-end,
because the slice finally carries the decision-layer evidence it was missing: predicate → reach the FILE
bar; mitigation → affirmatively CLEAR; casework grounding → SIGN. Plus the merge console gains its
org-collision completeness (the corporate-screening false-positive — the dominant sanctions-screening pain).

Four consumes + true-ups:

1. **§12 file-at-scale** (substrate P39) — consume the predicate-reference so slice cases with a
   mechanism + 2 legs that currently stall reach the FILE bar from a *grounded* register, not analyst-typed.
2. **§12 clear-at-scale** (substrate P40) — consume the affirmative-mitigation so generated cases CLEAR by
   explained source-of-funds, not only clear-by-absence.
3. **Casework signing** (casework P20) — re-vendor; the §12 FILE cases (and the C15/C4 topologies) SIGN.
4. **Merge-org class** (substrate P38) — add an OFAC org-name collision SCORED population to the merge
   console (the org sibling of the Phase-80 person class), scored against the non-circular `GT-<hash>` oracle.

Plus: re-pin substrate; close/reconcile the consumed briefs; true up `cross-pillar-build-order.md`.

## 2. Context

- The local consume frontier was declared EXHAUSTED at Phase 81 ("the next phase AWAITS a substrate
  emission") — these are exactly the awaited emissions. The frontier re-opens as designed.
- **A1 verified (line 310-312)**: `scripts/evidence_requirements.py` ALREADY exposes the
  `named_predicate_risk` + `mitigation_established` params. So consuming P39/P40 is pure **bundle DATA** the
  FROZEN engine reads — NOT a rule edit. The A1 guard (`evidence_requirements.py` byte-unchanged) holds by
  construction; the consume work is in the curate/serve layer (`curate_workbench_cases.py`/`serve_workbench.py`).
- **The Phase-81 C17 degeneracy lesson is LOAD-BEARING**: a measure-first gate must run the RIGOROUS engine
  (`determine()` with/without the evidence), NEVER a coverage proxy. The brief measured 40% predicate / 6%
  mitigation *coverage* — coverage ≠ cases-reaching-the-bar. The §12 advance must be proven by a with/without
  determination-bar regression. (Unlike C17, the predicate is a *required-and-currently-missing* rule
  component, so cases that already carry mechanism+2legs should move — but the count is measured, not assumed.)
- **The substrate emit-path risk (the claim most likely to break)**: P39/P40 ride the always-on
  `--emit-evidence`/`--emit-screening` bundle path — the SAME path the Phase-81 planning run hit a substrate
  `ReplayError` on (diagnosed there as orthogonal to the `--emit-eval-oracles` oracle path, which reproduced
  clean). The committed 376-case slice predates P39/P40 (@`fc98b09`); getting predicate/mitigation requires a
  re-emit at the new HEAD, which may re-hit the crash. T1 routes around it with a known-good param set; if it
  won't reproduce after bounded attempts → the §12 tracks (T4/T5) degrade and route to a substrate
  emit-stability brief. The merge-org oracle (T3) uses the clean `--emit-eval-oracles` path.
- Merge `data/merge/cases.json` is currently **66 scored cases** (29 real-substrate + 24 OFAC person +
  13 synthetic). The org class ADDS a population (the additive demonstrative-consume pattern — no
  population-count ripple).

## 3. Scope (file globs)

`scripts/curate_merge_cases.py` · `scripts/distill_sanctions_slice.py` · `scripts/resolution_scorer.py` ·
`data/merge/cases.json` · `merge.html` · `dist/merge/**` (the ONE conditional re-freeze) · `scripts/build.py`
(validate_merge_cases) · `tests/merge-console.test.mjs` · `tests/fixtures/merge-sanctions-org-oracle/**` ·
`data/entity-spine/**` · `scripts/curate_workbench_cases.py` · `scripts/serve_workbench.py` ·
`data/workbench/**` · `data/casefile/**` · `workbench.html` · `tests/workbench.test.mjs` ·
`vendor/aml-casework/**` + `VENDORED_AT` · `docs/*-PLAN-BRIEF.md` · `docs/cross-pillar-build-order.md` ·
`CLAUDE.md` · `.dev-wiki/tasks.md`. **NO change to `scripts/evidence_requirements.py`.**

## 4. Key constraints (LOAD-BEARING)

- **A1 guard:** `scripts/evidence_requirements.py` BYTE-UNCHANGED (`git diff --quiet`). The sufficiency RULE
  is frozen; P39/P40 enter as bundle DATA the engine already reads.
- **Evidence-advance, rule frozen** (user Q1): a §12 advance is PROVEN by a with/without-`determine()`
  regression on the RIGOROUS engine (case reaches the bar WITH the evidence, WITHHELD without). Any
  same-evidence double-count dedup lives in the consume layer, never the engine. If a consume forces an
  `evidence_requirements.py` change → STOP-and-surface (do not silently touch).
- **Merge measure-first (user Q2):** the org class is gated on two-sidedness REPLAYED through signal-watch's
  OWN distill/scorer path. One-sided → ABORT to a brief, `dist/merge` BYTE-FROZEN. No fabrication to force
  two-sidedness. The 4th-consecutive `dist/merge` re-freeze happens ONLY on a clean two-sided result.
- **Firewall:** `build.py` imports no spine/scorer/sibling/curate/casework (grep guard — VERIFIED CLEAN);
  the **8 non-merge dists byte-frozen**; `dist/merge` is the ONE sanctioned re-freeze, GATED on T2a two-sided.
- **validate↔curate EXACT parity** (Phase-76); the post-disposition merge `oracle` block never leaks
  pre-adjudication (`assert_no_*_leak`).
- **Casework boundary:** companion-only SUBPROCESS file-handoff; re-vendor touches no dist; contract stays
  v0.3-compatible (curate hands the v0.3 view).
- **Honesty governor:** no catch-rate / lift / precision / recall / multiplier wording — the measured
  magnitudes (predicate cases-to-bar, mitigation clears, sign funnel) are honest COUNTS with their
  definitions; sweep DOCS too (the Phase-78 lesson). Badge always-on; synthetic-substrate qualifier.
- **Compliance:** real OFAC ORG names ship clean under 17 USC §105 (US-federal public domain — covers OFAC),
  framed STRICTLY as the FALSE-POSITIVE trap — the synthetic org is NEVER the sanctioned entity. No CC-BY-NC
  bytes in the repo.

## 5. Tasks (dependency-ordered; measure-first BEFORE every gated build)

1. **T1 — Foundation: re-verify HEADs + emit the enriched slice + re-pin** (M, DEPENDENCY).
2. **T2 — Measure-first gate (the rigorous, non-ship deltas that gate every build)** (M).
3. **T3 — Merge-org class build** (L; conditional on T2a two-sided; else abort + dist/merge byte-frozen).
4. **T4 — §12 predicate file-at-scale consume** (M; conditional on T2b non-degenerate; A1-frozen; else observable).
5. **T5 — §12 mitigation clear-at-scale consume** (M; conditional on T2c non-degenerate; A1-frozen; else observable).
6. **T6 — Casework re-vendor + funnel land** (M).
7. **T7 — Brief true-ups + cross-pillar + re-pin** (S).
8. **T8 — Verify + CLAUDE.md + close** (M).

(Full TDD cycle / scope / success per task in `.dev-wiki/tasks.md`.)

## 6. Exit criteria

- T1: substrate HEAD re-verified (contains P38/39/40); the enriched-slice emit reproduces (predicate +
  mitigation in bundles; org fragments in true_entities) OR the §12 tracks degrade per the emit-path abort;
  no-substrate replay captures committed.
- T2: all four deltas recorded as non-ship numbers; each gate decision (build / degrade / abort) documented.
- **IF T2a two-sided** (merge-org): `--check all` 9/9 (8 byte-frozen + `dist/merge` re-frozen with the org
  class); `node tests/merge-console.test.mjs` green incl. the org basis; validate↔curate parity; the
  oracle-leak firewall held; honesty word-ban held. **IF one-sided:** `dist/merge` BYTE-FROZEN + a substrate
  org-emit-stability/realism brief.
- **IF T2b/c non-degenerate** (§12): the predicate/mitigation lights ≥1 slice case to the FILE/CLEAR bar via
  the with/without regression; `git diff --quiet scripts/evidence_requirements.py`; `node
  tests/workbench.test.mjs` green. **IF degenerate:** the consume ships as a rendered observable (the
  grounding present, the bar not reached) + a handoff brief (route to substrate asks #3/#4 — the second leg /
  ownership edges).
- T6: casework re-vendored to `04cc335`; the signing funnel re-measured + the new counts recorded; selftests
  green under the vendored copy; 8 non-merge dists byte-frozen; build.py imports no casework.
- T7: substrate re-pinned in the briefs + build-order; consumed-brief banners updated (org-fragment-emit,
  northstar-evidence #1/#2, casework-northstar-signing P20); the still-open frontier named (substrate asks
  #3/#4, the C20 jurisdiction leg, the casework C17-sign gap); honesty governor swept.
- T8: `--check all` 9/9; `node tests/*.test.mjs` green; `uv run pytest` green; smoke-checklist walked;
  CLAUDE.md `## Current state` trued IN PLACE (≤~200 lines, no per-phase bullet).

## 7. Abort rule

Any UNSANCTIONED ship-dist drift (the 8 non-merge dists, or `dist/merge` before its T2a gate passes) / a
build.py spine-scorer-sibling-curate-casework import / an `evidence_requirements.py` change (incl. one forced
by a §12 dedup — surface it, don't silently touch) / a real OFAC org name framed as a real sanctions catch
(not the false-positive trap) / any CC-BY-NC dataset committed / a cohort or confusion count presented as a
catch-rate/precision/lift/recall → STOP-and-surface. Measure-first: T2a one-sided/tautological → STOP the
merge org track (T3 does NOT run) to a brief; T2b/c degenerate (DELTA≈0) → the §12 consume degrades to a
rendered observable + a brief; the substrate `--emit-evidence` re-emit won't reproduce after bounded
attempts → STOP the §12 tracks (T4/T5), route to a substrate emit-stability brief, keep the §12 loop at the
current committed slice.

## 8. Risks (the claims I'd most expect to be wrong)

1. **[HIGH] The §12 re-emit (`--emit-evidence`) won't reproduce** — the Phase-81 `ReplayError` path. Mitigated
   by T1's known-good param search + the emit-stability abort. *Most likely to break.*
2. **[MED] The predicate/mitigation cohort doesn't reach the bar** (C17 redux) — coverage ≠ cases-to-bar.
   Mitigated by the rigorous with/without measure + the observable fallback (accepted at the gate).
3. **[MED] The org-fragment overlay replays one-sided through OUR distill** (substrate's 16/35 self-report ≠
   our scorer's read — the Phase-77/81 trap). Mitigated by T2a measuring on our own path + the abort.
4. **[LOW] The casework re-vendor regresses a currently-signing case** (a stricter reconciled detector drops
   a case that used to sign). Mitigated by the funnel two-sided check (moves should be fail-close→sign, not
   sign→fail-close) + casework selftests.
