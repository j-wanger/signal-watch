---
title: "Phase 82 — Consume sibling emissions: north-star evidence AT SCALE (substrate P39 predicate + P40 mitigation §12 loops) + merge org-collision class (P38) + casework P20 signing re-vendor"
aliases: [phase-82]
category: phases
tags: [cross-pillar, consume, substrate, casework, predicate-reference, mitigation-evidence, org-name-collision, merge-oracle, casework-funnel, north-star, scale, measure-first, firewall, a1-guard]
parents: []
created: 2026-06-29
updated: 2026-06-29
source: plan
status: delivered
ceremony: standard
scope: ["scripts/curate_merge_cases.py", "scripts/distill_sanctions_slice.py", "scripts/resolution_scorer.py", "data/merge/cases.json", "merge.html", "dist/merge/**", "scripts/build.py", "tests/merge-console.test.mjs", "tests/fixtures/merge-sanctions-org-oracle/**", "data/entity-spine/**", "scripts/curate_workbench_cases.py", "scripts/serve_workbench.py", "data/workbench/**", "data/casefile/**", "workbench.html", "tests/workbench.test.mjs", "vendor/aml-casework/**", "docs/*-PLAN-BRIEF.md", "docs/cross-pillar-build-order.md", "CLAUDE.md", ".dev-wiki/tasks.md"]
entry_criteria: "substrate advanced f7fbdb0→294d3e5 (Phase 40 close; feat P38 a9a088a org-fragment / P39 1483c84 predicate-reference / P40 978c8fe affirmative-mitigation); casework advanced 076fb8e→04cc335 (Phase 21 close; feat P20 a059fc5 C15/C4 reconcile / P21 7398ddc drift-hardening). All four code-verified READY this session (3 background investigators, file:line — CLI-wired, non-circular/label-blind, two-sided where needed; none the Phase-77 unwired-or-circular trap). A1 verified: evidence_requirements.py already exposes named_predicate_risk + mitigation_established (line 310-312) — P39/P40 are DATA. Direction gate closed 2026-06-29 (AskUserQuestion): scope = Both clusters (full batch); §12 = measure-first-with-fallback, rule frozen; merge = measure two-sidedness on our path, one-sided → abort; casework = re-vendor + funnel re-measure."
exit_criteria: "T1 emit reproduces (bundles carry predicate + mitigation; true_entities ≥1 O-FRAG org cluster, entity_ref≠cluster; param set + SHA recorded) OR emit-stability abort documented; no-substrate replay captures committed. T2 the four rigorous deltas recorded as non-ship numbers + each gate decision (build/degrade/abort). IF T2a two-sided: merge-org class curated (validate↔curate EXACT parity) + dist/merge re-frozen + tests green; ELSE dist/merge BYTE-FROZEN + an org brief. IF T2b/c non-degenerate: the predicate/mitigation lights ≥1 slice case to the FILE/CLEAR bar (with/without regression proves the RULE frozen); ELSE the consume ships a rendered observable + a brief. casework re-vendored to 04cc335; funnel re-measured + counts recorded; selftests green; build.py imports no casework; 8 non-merge dists byte-frozen. Briefs re-pinned + banners updated + open frontier named; honesty governor swept. --check all 9/9; node tests/*.test.mjs green; uv run pytest green; evidence_requirements.py byte-unchanged (A1); CLAUDE.md current-state trued in place."
grounded_against:
  signal-watch: HEAD (Phase 81 committed, 52c5d10)
  aml-substrate: 294d3e5 (Phase 40 — P38 a9a088a org-fragment / P39 1483c84 predicate-reference / P40 978c8fe affirmative-mitigation)
  aml-casework: 04cc335 (Phase 21 — P20 a059fc5 C15/C4 reconcile / P21 7398ddc drift-hardening; vendored pin moving 076fb8e→04cc335)
---

# Phase 82 — Consume sibling emissions: north-star evidence AT SCALE

## Objective

Consume four sibling emissions so the GENERATED 376-case slice carries north-star-quality
determinations AT SCALE — the same engine that decides the 2 hand-authored cases (Northgate FILES /
Lakeshore CLEARS, Phase 73) now decides the slice end-to-end, because the slice finally carries the
decision-layer evidence it was missing:

- **substrate P39** (`1483c84`, predicate-reference) — Ask #1 of the northstar-evidence brief, the
  *keystone*: closes the measured **0-of-376** named-predicate gap. Predicate → reach the FILE bar.
- **substrate P40** (`978c8fe`, affirmative-mitigation) — Ask #2, the CLEAR-side mirror: mitigation →
  affirmatively CLEAR (not only clear-by-absence).
- **casework P20** (`a059fc5`, C15/C4 reconcile) — re-vendor; ~55 previously fail-closed cases SIGN.
- **substrate P38** (`a9a088a`, org-fragment) — un-aborts Phase 81's merge-org track as a 4th SCORED
  merge population (the org sibling of the Phase-80 person class).

The decisive A1 fact: `evidence_requirements.py` already exposes the predicate + mitigation params
(line 310-312), so P39/P40 enter as bundle DATA the FROZEN engine reads — NOT a rule edit.

## Scope

- Merge: `scripts/{curate_merge_cases,distill_sanctions_slice,resolution_scorer}.py`,
  `data/merge/cases.json`, `merge.html`, `dist/merge/**`, `scripts/build.py` (validate_merge_cases),
  `tests/merge-console.test.mjs`, `tests/fixtures/merge-sanctions-org-oracle/**`, `data/entity-spine/**`.
- §12 workbench: `scripts/{curate_workbench_cases,serve_workbench}.py`, `data/workbench/**`,
  `data/casefile/**`, `workbench.html`, `tests/workbench.test.mjs`.
- Casework: `vendor/aml-casework/**` + `VENDORED_AT`.
- Docs/dev-wiki: `docs/*-PLAN-BRIEF.md`, `docs/cross-pillar-build-order.md`, `CLAUDE.md`,
  `.dev-wiki/tasks.md`.
- **NO change to `scripts/evidence_requirements.py`.**

## Exit Criteria

- [x] T1: substrate HEAD re-verified (P38/39/40 present @294d3e5); the enriched-slice emit reproduced
      (predicate + mitigation in the 376 bundles); re-pinned. (true_entities O-FRAG existed but shared no
      resolution handle → the merge-org track aborted at T2a, see below.)
- [x] T2: all four rigorous deltas recorded as non-ship numbers; each gate decision documented;
      `git diff --quiet scripts/evidence_requirements.py` (A1 held).
- [x] T2a ONE-SIDED → ELSE branch: `dist/merge` BYTE-FROZEN + the org-fragment-emit brief sharpened
      (P38 fragments share no resolution handle with their base → 0 uphold candidates).
- [x] T2b NON-DEGENERATE: the predicate lights 1 KYC-integrity determination to the FILE bar via the
      with/without regression (31 over the full 23,651-customer population); `git diff --quiet` held.
- [x] T2c NON-DEGENERATE: the mitigation affirmatively CLEARS 17 ML slice cases via the with/without
      regression; `git diff --quiet` held.
- [x] T6: casework re-vendored 076fb8e→04cc335; funnel re-measured (coverage 128→256, the kyc-sign 2→1
      honest relaxation surfaced two-sided); selftests green; build.py imports no casework; 8 non-merge dists byte-frozen.
- [x] T7: substrate re-pinned 294d3e5 in briefs + build-order; consumed-brief banners updated; the open frontier
      named (substrate asks #3/#4, the C20 jurisdiction leg, the casework C17-sign + C14-narrative-seam gaps); honesty swept.
- [x] T8: `--check all` 9/9; `node tests/*.test.mjs` green; `uv run pytest` 27 green; CLAUDE.md
      `## Current state` trued IN PLACE (no per-phase bullet; the 513-line trim flagged as a soft observation).

## Constraints

- **A1 guard** — `scripts/evidence_requirements.py` BYTE-UNCHANGED (`git diff --quiet`); prevents a
  silent rule weakening masquerading as a §12 advance. P39/P40 enter as bundle DATA the engine reads.
- **Evidence-advance, rule frozen** — a §12 advance is PROVEN by a rigorous with/without-`determine()`
  regression; prevents a coverage-proxy overclaim (the Phase-81 C17 error). Same-evidence dedup lives
  in the consume layer; a forced engine edit STOPS-and-surfaces.
- **Merge measure-first** — the org class gates on two-sidedness REPLAYED through our OWN
  distill/scorer path; prevents shipping substrate's self-report as our result (the Phase-77/81 trap).
  One-sided → ABORT, `dist/merge` byte-frozen.
- **Firewall** — `build.py` imports no spine/scorer/sibling/curate/casework (grep guard); prevents the
  companion layer leaking into the build. The 8 non-merge dists byte-frozen; `dist/merge` the ONE
  conditional re-freeze.
- **Honesty governor** — no catch-rate / lift / precision / recall / multiplier; prevents a fabricated
  performance claim; sweep DOCS too (the Phase-78 lesson). Badge always-on; synthetic-substrate qualifier.
- **Compliance** — real OFAC org names ship clean under 17 USC §105, framed STRICTLY as the
  false-positive trap (the synthetic org is NEVER the sanctioned entity); no CC-BY-NC bytes in the repo.

## Checkpoints

- After T2 (the four deltas): report each gate decision (build / degrade / abort) before any ship-dist
  touch — `dist/merge` is the ONE conditional re-freeze.
- If the substrate `--emit-evidence` re-emit won't reproduce after bounded attempts: STOP T4/T5, route
  to a substrate emit-stability brief, keep the §12 loop at the current committed slice.

## Assumptions

- A1 [HIGH, T0 weakest] — P39/P40 MOVE a meaningful number of slice cases to the bar. If false (DELTA≈0,
  C17 redux): the §12 consume degrades to a rendered observable + a handoff brief (route to substrate
  asks #3/#4). The T2b/c rigorous gate decides.
- A2 [HIGH] — the merge-org class replays TWO-SIDED on our own path. If false (one-sided, Phase-81 T1a
  redux): the org track ABORTS to a brief, `dist/merge` byte-frozen. No fabrication to force it.
- A3 [MED] — casework re-vendor lands ~55 fail-close→sign without regressing dists. If false (a stricter
  detector drops a signing case): surface it; the funnel two-sided check catches a sign→fail-close move.
- A4 [LOW] — the substrate `--emit-evidence` re-emit reproduces. If false (the Phase-81 ReplayError
  path): T1's emit-stability abort; keep the §12 loop at the current slice.

## Notes

Direction gate closed 2026-06-29 (AskUserQuestion; all_accept, NOT silent — positions restated in the
ledger Phase-82 row). The local consume frontier re-opens exactly as Phase 81 predicted ("the next phase
AWAITS a substrate emission") — these are the awaited emissions. Decisions:
[[decisions/phase-82-northstar-evidence-at-scale-frame]] · [[decisions/phase-82-measure-first-four-deltas]]
· [[decisions/phase-82-full-batch-four-tracks]]. Spec
`specs/phase-82-consume-sibling-northstar-evidence-at-scale.md`; ledger Phase-82.
