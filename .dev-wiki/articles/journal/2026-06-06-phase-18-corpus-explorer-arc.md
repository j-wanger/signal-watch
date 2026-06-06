---
title: "Phase 18: Corpus explorer arc — human gate + close-the-loop coverage payoff (M7)"
aliases: [corpus-explorer-arc, corpus-human-gate, close-the-loop-coverage, corpus-5-screen-arc, coverage-not-precision]
category: journal
tags: [milestone-m7, corpus-explorer, dramatic-arc, human-gate, close-the-loop, coverage, no-fabricated-numbers, subtraction-test, div-toggle]
parents: [phase-18-corpus-explorer-arc]
created: 2026-06-06
updated: 2026-06-06
source: debrief
duration: ~2-3h (post-compaction estimate)
---

# Phase 18: Corpus explorer arc — human gate + close-the-loop coverage payoff (M7)

## What Happened

Gave the corpus explorer (`dist/corpus/`, from `corpus.html`) the dramatic arc the six-act showcase
already has, at the END of the completed M0–M7 roadmap. The explorer went from a flat 4-screen
analytical flow (Select → Coverage → Build recs → Signal, ending on a spec card) to a 5-screen ARC:
**Select → Coverage → Build recs/GATE → Signal → Close the loop** — mirroring the showcase's Act 3
(human gate) + Act 6 (the loop closes), grounded ENTIRELY in existing data with NO fabricated numbers.

A UX-research-report detour preceded the plan: Jake brought an agentic-UX best-practice report, which
turned out to be a VALIDATION PASS, not a backlog — its recommendations were mostly already shipped
(streaming, progress trace, reduced-motion, CP gate named, provenance via highlights + the corpus
explorer) or don't transfer to a presenter-driven projector demo (collapsible accordions, popovers,
skeletons); the confidence-interval rec was rejected as a false-precision/compliance hazard. That
review confirmed the agentic spine was already sound and drove choosing the corpus arc over
call-it-done / engineering-hygiene / showcase-true-up / deepening-the-showcase-gate.

The decisive honesty call: the payoff is **COVERAGE close-the-loop, NOT precision combination-lift**.
Precision-lift (the showcase's "alone 22% → together 81%" beat) was EXPLICITLY REJECTED — the derived
records carry no precision/lift numbers, so porting it would FABRICATE ~12 per-advisory illustrative
stats, violating the "never present synthetic numbers as real" non-negotiable. Coverage is computed
from existing statuses (`coverageIndex()`) and already disclosed illustrative → zero-new-fabrication.

Clean phase: the abort/degrade path (close-the-loop-only) was never needed, no blocked tasks. The
div-toggle gate proved keyboard-safe; the close-the-loop coverage math is honest by construction
(picked gaps flip gap→covered via the existing `coverageIndex()`, same model as Act 6).

T1 the gate (selectable BUILD_NOW div-toggles + a per-advisory `selected` Set, default all-selected,
reset on `pick()`) · T2 Signal reflects the picks (selected ∩ BUILD_NOW with `build_logic`; two honest
empty states — nothing-buildable vs deselected-all) · T3 the new `renderClose` 5th screen (STEPS 4→5,
DETAIL 3→4; coverage gauge animates before→after via `coverageIndex` with picked gaps flipped covered;
reduced-motion branch; honest flat-hold for 0-picked/0-BUILD_NOW) · T4 rebuild dist/corpus + 15/15
headless DOM-shim assertions + drift guard · T5 docs (no stale "4-screen").

## Decisions Made
- Phase 18 = give the corpus explorer a dramatic arc (human gate + close-the-loop coverage payoff) —
  chosen over call-it-done / engineering-hygiene / showcase-true-up / deepening-the-showcase-gate. The
  corpus explorer is where the project's earned identity lives (real provenance, 12/14 derived) and was
  the one artifact missing the dramatic arc the showcase has.
- The payoff is COVERAGE close-the-loop, NOT precision combination-lift (precision-lift rejected to
  avoid fabricating ~12 per-advisory illustrative stats).
- Scope contained to `corpus.html` (+ dist rebuild + docs); the arc reuses existing data fields
  (status→coverage, build_rec→BUILD_NOW, build_logic→spec) → NO schema/data/build.py change. Human gate
  uses div-toggles (NOT `<input>`) to preserve Space/arrow keyboard nav + determinism.
- The gate FOLDS into the existing Build-recs screen (BUILD_NOW rows become selectable) rather than a
  separate gate screen — subtraction test.
- (Meta, pre-phase) The agentic-UX research report is a VALIDATION PASS, not a backlog.
- (Recorded in `_CURRENT_STATE` `## Recent Decisions` by the planner — not duplicated as articles, lite.)

## Problems Solved
- Keyboard-nav collision risk — resolved by div-toggles (the showcase `.selrow` pattern) instead of
  `<input>` elements, which would steal focus / intercept Space/arrows.
- Honest before/after for the close-the-loop screen — resolved by reusing `coverageIndex()` on a
  COPY of the indicators (`Object.assign`, never mutating `a.indicators`) with picked gaps flipped
  covered; 0-picked/0-BUILD_NOW shows an honest flat-hold (no fake rise).

## Artifacts Changed
- `corpus.html` — the only source unfreeze: `selected` Set state, selectable div-toggle BUILD_NOW rows,
  `renderSignal` filtered to the picks (two empty states), new `renderClose` 5th screen,
  STEPS/DETAIL/stepper/nav/keyboard updated for 5 screens.
- `dist/corpus/index.html` — rebuilt 109,948→180,119 B-class artifact via `build.py corpus` (109k→ now
  larger with the arc).
- `README.md`, `CLAUDE.md` — document the 5-screen arc + the coverage-not-precision honesty stance.

## Related
- [[phase-18-corpus-explorer-arc|Phase 18: Corpus explorer arc — human gate + close-the-loop coverage payoff]] — parent phase
- [[2026-06-06-phase-17-complete-corpus-derivation|Phase 17]] — predecessor (12/14 derived; the real subtraction)

## Soft Observations / Phase 19 Candidates
- The 0-BUILD_NOW-advisory close-the-loop path is NOT exercised by any of the 12 live advisories (all
  have ≥1 BUILD_NOW); the identical "coverage holds" flat-hold branch is verified via the deselect-all
  path. Re-verify directly if a future not-yet-derived 0-BUILD_NOW advisory is ever derived. | evidence:
  /tmp/test_corpus.js note "all 12 live advisories have ≥1 BUILD_NOW".
- The non-reduced (animated) close-the-loop path was not headless-tested (the DOM-shim ran
  reduced-motion); it reuses the proven `animVal`/coverage-gauge animation from `renderCoverage`. Low risk.
- The headless DOM-shim test (`/tmp/test_corpus.js`) is ad-hoc and uncommitted. The corpus explorer is
  now a 5-screen interactive artifact — consider committing a small `tests/` harness if it keeps growing
  (Phase-19 candidate).
- Reusable testing insight: `vm.runInNewContext` only auto-exposes `var`/`function` declarations as
  sandbox globals, NOT `const`/`let` — append an epilogue assigning the needed `const`/`let` bindings to
  `globalThis` to drive them from the test harness.
- Carried Phase-19 candidates: tighten the coarse `_rf_triage` counter (Phase-17 reviewer MEDIUM) · drop
  the stale `anthropic` pin from `requirements-authoring.txt` · FATF non-derivable labeling polish · the
  recurring showcase-debt true-up (elder presentation-values + fentanyl verbatim re-point — deferred
  Ph10/11/15/16) · an honest corpus combination-lift wow beat (ONLY with a non-fabricated lift source) ·
  manifest `--fetch` cadence. The M0–M7 roadmap + this arc are complete; the demo is at Definition of Done.

## Review Gate (lite + 5 tasks; size gate ≥4 → reviewer may apply)
Lightweight post-hoc review (phase already committed/accepted, non-blocking). Findings:
- corpus.html diff is clean, matches the planned contract, reuses existing helpers (`coverageIndex`,
  `animVal`, `.covrow`, `srcCap`, the `.selrow`/div-toggle pattern) — no duplication, no new dependency.
- No fabricated numbers: coverage is the only quantity, already disclosed illustrative; close-the-loop
  copies indicators (`Object.assign`) so `a.indicators` is never mutated on revisit.
- Frozen set held: impl commit 6d654a4 touched only corpus.html + dist/corpus (+ docs + dev-wiki);
  `--check all` 4-artifact zero drift; `git show --stat` shows index.html/build.py/config/data/3-typology
  dists byte-untouched.
- 1 LOW (already in soft obs): the animated close path is headless-untested (reuses proven animation).
- No MEDIUM/HIGH findings; nothing blocking. ACCEPT.

### Retro Check
Not triggered this debrief (17 completed phases; 17 % 5 ≠ 0).
