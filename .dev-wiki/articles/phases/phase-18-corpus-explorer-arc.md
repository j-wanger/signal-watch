---
title: "Phase 18: Corpus explorer arc — human gate + close-the-loop coverage payoff"
aliases: [corpus-explorer-arc, corpus-human-gate, close-the-loop-coverage, corpus-5-screen-arc, coverage-not-precision]
category: phases
tags: [milestone-m7, corpus-explorer, dramatic-arc, human-gate, close-the-loop, coverage, no-fabricated-numbers, subtraction-test, div-toggle]
parents: []
created: 2026-06-06
updated: 2026-06-06
source: plan
status: active
ceremony: lite
scope: ["corpus.html", "dist/corpus/index.html", "README.md", "CLAUDE.md"]
entry_criteria: "Phase 17 complete + accepted (impl commit 572cd3b; reviewer ACCEPT 9/10): the corpus is 12/14 derived live and the real subtraction landed (extract_red_flags + the scaffold/draft stack deleted, derive_signals.py 1202→600, the inverted loop the SOLE derivation path). The M0–M7 roadmap is complete; a UX-research review (agentic-UX best-practice report) confirmed the demo's agentic spine was already sound and most recommendations were already shipped or didn't transfer to a presenter-driven projector demo. The one remaining net-new buy-in lever: the corpus explorer (dist/corpus/, from corpus.html) is a flat 4-screen analytical flow (Select → Coverage → Build recs → Signal) that ends on a spec card — it lacks the dramatic arc the six-act showcase has (no human-decision beat, no payoff). User chose the corpus-explorer arc over call-it-done / engineering-hygiene / showcase-true-up / deepening-the-showcase-gate."
exit_criteria: "(1) The corpus explorer ships a 5-screen arc: Select → Coverage → Build recs/GATE → Signal → Close the loop. (2) BUILD_NOW recommendation rows are SELECTABLE on the Build-recs screen — div-toggles (NOT <input>, so Space/arrow keyboard nav + determinism survive), per-advisory selection Set, default all-BUILD_NOW-selected, reset on pick(), non-BUILD_NOW rows read-only. (3) Signal reflects the picks — spec cards for selected ∩ BUILD_NOW with build_logic; deselect → honest labeled empty state. (4) The NEW close-the-loop screen animates the coverage index BEFORE → AFTER using the existing coverageIndex() with the picked gap indicators flipped to covered (identical model to showcase Act 6); reduced-motion jumps to the after value; 0 BUILD_NOW / 0 picked → an honest flat-hold + note (never a fake rise). (5) dist/corpus rebuilt; python3 scripts/build.py --check all shows index.html/build.py/config/**/data/fincen/** + the 3 typology dists byte-frozen (only dist/corpus changed); node --check valid self-contained JS; README + CLAUDE document the 5-screen arc + the human gate + the coverage-not-precision honesty stance (precision-lift explicitly rejected to avoid fabricated per-advisory stats)."
---

# Phase 18: Corpus explorer arc — human gate + close-the-loop coverage payoff

## Objective

Give the corpus explorer (`dist/corpus/`, built from `corpus.html`) the dramatic arc the six-act showcase
already has — grounded ENTIRELY in existing data, with NO fabricated numbers. Today the explorer is a flat
4-screen analytical flow (Select → Coverage → Build recs → Signal) that ends on a spec card with no
human-decision beat and no payoff. Add the two beats it lacks, mirroring the showcase's Act 3 (human gate) +
Act 6 (loop closes), honestly (coverage), as net-new stakeholder buy-in value.

## Approach

**The new arc = 5 screens.** (1) Select [unchanged] — pick a derived advisory. (2) Coverage [unchanged] —
enumerated red flags scored covered/partial/gap, provenance-stamped, coverage gauge. (3) Build recs → **THE
GATE** — the per-indicator BUILD_NOW recommendation rows become SELECTABLE (the human-in-the-loop gate, the
project's thesis "agent proposes, human disposes"). FOLDED into the existing Build-recs screen rather than a
separate screen (subtraction test: don't add a screen when an existing one carries the interaction). Default
all-BUILD_NOW-selected; non-BUILD_NOW rows stay read-only. Selection uses div-based toggles (NOT `<input>`) so
they cannot collide with the Space/arrow keyboard nav and determinism/stage-reliability is preserved — the same
pattern the showcase's `.selrow` uses. (4) Signal — spec cards for WHAT THE HUMAN PICKED (selected ∩ BUILD_NOW
with `build_logic`); honest labeled empty state if none picked / none buildable. (5) **Close the loop** [NEW
screen] — the coverage index animates BEFORE → AFTER, where "after" flips the picked gap indicators to covered
(deterministic client-side recompute via the already-present `coverageIndex()`, identical model to showcase
Act 6). REDUCED-motion branch jumps to the after value. Honest flat-hold + note when an advisory has 0 BUILD_NOW
or 0 picked (never a fake rise).

**The payoff is COVERAGE close-the-loop, NOT precision combination-lift.** Precision-lift (the showcase's
signature "alone it's noise 22% → together 81%" beat) was EXPLICITLY REJECTED: the corpus derived records carry
no precision/lift numbers, so porting it would mean FABRICATING ~12 per-advisory illustrative precision stats —
violating the "never present synthetic numbers as real" non-negotiable and undercutting the corpus side's whole
real-provenance credibility. Coverage is already computed from existing statuses (`coverageIndex()`: covered=1,
partial=0.5, gap=0, averaged) and already disclosed illustrative (the corpus footer says so) → the honest,
zero-new-fabrication payoff.

**Contained scope — the arc consumes only existing data fields.** Indicator status → coverage (via the
already-present `coverageIndex()`); `build_rec` → which rows are BUILD_NOW; `build_logic` → the spec card. So
there is NO schema change, NO derived-record change, NO build.py change. The unfreeze is `corpus.html` ONLY
(+ rebuild `dist/corpus` + docs).

## Scope

Files affected:
- `corpus.html` — the only source unfreeze: per-advisory selection state (a Set of indicator ids), selectable
  div-toggle BUILD_NOW rows on the Build-recs screen, `renderSignal` filtered to the picks, a new `renderClose`
  5th screen, `STEPS`/`DETAIL`/stepper/nav/keyboard updated for 5 screens.
- `dist/corpus/index.html` — rebuilt from the unfrozen `corpus.html` via `python3 scripts/build.py corpus`.
- `README.md`, `CLAUDE.md` — document the 5-screen arc + the human gate + the coverage-not-precision honesty
  stance.

UNTOUCHED (byte-frozen): `index.html`, `scripts/build.py`, `config/**`, `data/fincen/**` (corpus-status.json +
derived/*.json), `dist/{fentanyl,trade-based,elder-financial-exploitation}/`. The arc reuses existing data
fields, so no schema/data/build.py edit is needed.

## Exit Criteria

- [ ] The corpus explorer ships a 5-screen arc: Select → Coverage → Build recs/GATE → Signal → Close the loop
      (`STEPS` has 5 entries, `DETAIL` 4 render fns; all 5 reachable by next/back/stepper/keyboard).
- [ ] BUILD_NOW recommendation rows are SELECTABLE on the Build-recs screen — div-toggles (NOT `<input>`,
      keyboard-safe), a per-advisory selection Set, default all-BUILD_NOW-selected, reset on `pick()`,
      non-BUILD_NOW rows read-only.
- [ ] Signal reflects the picks — spec cards for selected ∩ BUILD_NOW with `build_logic`; deselect-all → the
      honest labeled empty state (no broken/blank card).
- [ ] The new close-the-loop screen animates coverage BEFORE → AFTER from the picks (picked gaps flipped to
      covered via `coverageIndex()`); reduced-motion lands the after value directly; a 0-BUILD_NOW advisory
      shows an honest flat close (coverage holds + note, no fabricated rise).
- [ ] `dist/corpus` rebuilt; `python3 scripts/build.py --check all` shows index.html/build.py/config/**/
      data/fincen/** + the 3 typology dists byte-frozen (only dist/corpus changed); `git diff index.html
      scripts/build.py config data` empty; `node --check dist/corpus/index.html` valid; README + CLAUDE
      document the arc + the coverage-not-precision honesty stance.

## Constraints (load-bearing)

- **NO fabricated precision/lift numbers** — the payoff is COVERAGE only (computed from existing statuses,
  already disclosed illustrative). Precision-lift is rejected because the records carry no such numbers; porting
  it would fabricate ~12 per-advisory stats, violating "never present synthetic numbers as real".
- **The human gate uses div-toggles, NOT `<input>`** — `<input>` elements steal focus and intercept Space/arrow
  keys, breaking the keyboard nav + the deterministic stage-reliability the presenter demo depends on. The
  showcase's `.selrow` proves the div-toggle pattern.
- **The gate FOLDS into the existing Build-recs screen** — subtraction test: don't add a 6th screen when an
  existing one carries the interaction. Arc stays 5 screens; default all-BUILD_NOW-selected so the default
  presenter path still walks a complete arc.
- **Scope contained to `corpus.html` (+ dist rebuild + docs)** — the arc reuses existing data fields, so NO
  schema/data/build.py change. The 3 typology dists + the six-act showcase (`index.html`) stay byte-frozen.
- **Defensive 0-BUILD_NOW handling + reduced-motion parity** — an advisory with 0 BUILD_NOW (or 0 picked) must
  show an honest flat-hold + note, never a fake rise; reduced-motion must reach the same final state without
  animation.

## Checkpoints

- T1 (the gate): if interactive div-toggle selection can't be made keyboard-safe + deterministic without
  growing complex, that is the Abort signal — DEGRADE to close-the-loop-only (no gate; coverage close over ALL
  BUILD_NOW), the payoff still lands.
- T3 (close the loop): if the before/after coverage math can't be made honest for some advisory shape, keep
  that screen informational rather than ship a misleading rise. NEVER fabricate precision/lift.
- T4: confirm `git diff index.html scripts/build.py config data` empty + `--check all` byte-frozen for
  everything except dist/corpus before declaring done.
- Blocked >3 attempts on a task → ask the user: skip or abort.

## Assumptions

- The existing `coverageIndex()` (covered=1, partial=0.5, gap=0, averaged over indicators) is the correct,
  already-shipped model for both the Coverage screen and the close-the-loop "after" recompute. If a picked-gaps
  recompute can't reuse it honestly, keep the close screen informational (the Abort path).
- div-toggle selection (the showcase `.selrow` pattern) does not collide with the corpus explorer's keyboard
  nav. If it does, degrade to close-the-loop-only.
- Every derived advisory with ≥1 BUILD_NOW indicator produces a non-trivial before→after delta; advisories with
  0 BUILD_NOW are the honest flat-hold case (defended, not hidden).

## Notes

Direction approved by user 2026-06-06: the corpus-explorer arc (human gate + close-the-loop coverage payoff)
over call-it-done / engineering-hygiene / showcase-true-up / deepening-the-showcase-gate. Rationale: the corpus
explorer is where the project's earned identity lives (real provenance, 12/14 derived) and is the one artifact
missing the dramatic arc the showcase already has — net-new buy-in value, not polish. This is the net-new-value
direction chosen at the END of the completed M0–M7 roadmap, after a UX-research review (agentic-UX best-practice
report) confirmed the demo's agentic spine was already sound and that most of its recommendations were already
shipped or didn't transfer to a presenter-driven projector demo. The decisive honesty call: COVERAGE
close-the-loop (zero new fabrication — coverage is already computed + disclosed illustrative) over precision
combination-lift (would fabricate ~12 per-advisory stats — the same false-precision hazard flagged earlier on
confidence intervals). Follow-ups not in scope (Phase-19 candidates): tighten the coarse `_rf_triage` counter
(Phase-17 reviewer MEDIUM) · drop the stale `anthropic` pin from requirements-authoring.txt · the recurring
showcase-debt true-up (elder presentation-values + fentanyl verbatim re-point — deferred across
Ph10/11/15/16/17) · manifest `--fetch` cadence.
