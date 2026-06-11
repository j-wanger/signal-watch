---
title: "Phase 45 — Corpus demo presentation polish (pre-presentation day)"
status: approved
confidence: medium
source: plan
created: 2026-06-10
updated: 2026-06-10
tags: [corpus, presentation, polish, lift, honesty]
---

# Phase 45 — Corpus demo presentation polish

## Context

dist/corpus presents to bank stakeholders 2026-06-11 (tomorrow). User direction: clean up
inconsistencies, REMOVE the fake combination-lift numbers (the generic 18→64→83 illustrative
template) and refocus that beat on the CONCEPT, plus an independent story-coherence/delivery
review (delivered by two review agents 2026-06-10). More user feedback expected mid-phase.

Baseline at planning: `--check all` 5/5 zero drift; corpus harness 239/239 green; NO stale
counts (all on-screen numbers computed from injected data at render).

## Review findings driving the plan (ranked)

STORY HIGHs: (1) `.brecrow` stagger uncapped — up to ~15s blank on FINTRAC guidance docs
(corpus.html:1018); (2) human gate reads PRE-DECIDED — all BUILD_NOW pre-checked under "You
decide what we build" (corpus.html:999/1230); (3) two zero-build-now docs (fin-2021-a004,
fin-2023-alert003) dead-end with impossible advice on the lift empty state (corpus.html:1140).

COMPLIANCE HIGH: FINTRAC verbatim excerpts render on the Capabilities + Data-sources lens
screens (corpus.html:692/747) with EMPTY footer attribution — `updateAttribution()` fires only
on `view==='detail'` (corpus.html:1214). Gap in the project's own Phase-28 relocated-attribution
mechanism.

LIFT MAP: `LIFT` const corpus.html:1148–1152; bars/markup 1159–1163; `.illus` tag 1158 (becomes
REMOVABLE once no number shows — one fewer disclaimer); framenote 1170 holds the artifact's only
"promotion gate" mention; tests/corpus-explorer.test.mjs:723–741 PIN the fake values (must move
in the same commit). Showcase index.html Act-5 carries the SAME template but is byte-frozen +
non-negotiable-protected.

MEDIUMs (copy): atoms/composition vocabulary unintroduced before the final beat (seed on
landing); landing names 4 of 5 source families + "5 regulators/sources" vs 3 regulators;
"Backtest on population" ✓ claims a backtest that never ran; "Advisories" chrome residue;
`typoLabel` renders "cross cutting indicators" (746 ind, 33%) as a de-hyphenated lowercase slug;
"gap → covered" pill exposes the internal token; FINTRAC pseudo reference codes
(FINTRAC-UNDERGROUND-BANKING) where FinCEN shows real ones — display-level handling only.

## Approved approach (gate closed 2026-06-10)

T1 live-risk fixes (3 story HIGHs) · T2 lift concept refocus — R2 "real composition search
space" (honest client-side counts, same honesty class as the lenses; R1 qualitative ladder as
the no-numbers fallback; R3 graph deferred post-demo) + tests + CLAUDE.md honesty-section
rewrite · T3 FINTRAC attribution on lens views · T4 ranked copy-coherence pass (MEDIUMs, then
LOWs time-permitting) · T5 user walkthrough + feedback intake (the freeze checkpoint; demo-path
notes into smoke-checklist) · T6 regate + rebuild (frozen corpus baseline MOVES; two-commit
delivery convention).

FROZEN: grounding core, derived data, build pipeline, showcase + news artifacts (byte-identical
in --check), always-on badge stays.

## Assumptions surfaced at the gate

A1 lift = R2 real-counts (vs R1 zero-numbers) — the T0 weakest assumption. A2 showcase Act-5
stays untouched; cross-artifact divergence accepted. A3 gate fix = copy + presenter stagecraft,
no interaction redesign. A4 attribution gap fixed by EXTENDING the footer mechanism to lens
views. A5 global polish + curated demo-path notes (vs single hardened route).

## Gate positions (closed 2026-06-10, all_accept: false)

- A1 [HIGH] — don't-know round 1 → DEFENDED with worked real-value examples → ACCEPTED. Lift =
  R2 real composition-search-space inventory counts (covered indicators in the committed signal's
  typology × contributing regulators, computed client-side from __CORPUS__ — the same honesty
  class as the lenses); NO performance claim; the "Illustrative · pending calibration" disclaimer
  REMOVED (no number left to disclaim); honest small-N/single-regulator degradation copy; R1
  zero-numbers ladder is the copy-only FALLBACK if the counts can't render honestly.
- A2 [HIGH] — ACCEPTED. Showcase index.html Act-5 untouched (byte-frozen,
  non-negotiable-protected); the corpus-vs-showcase lift divergence is DELIBERATE and accepted.
- A3 [MED] — ACCEPTED. Human gate = copy reframe ("the agent has PROPOSED all N — deselect to
  dispose") + presenter stagecraft; NO interaction redesign the day before presentation.
- A4 [MED] — ACCEPTED. FINTRAC attribution: EXTEND the Phase-28 relocated-footer mechanism to
  the Capabilities/Data-sources lens views (the user's compliance call; extension, not
  suppression).
- A5 [MED] — ACCEPTED. GLOBAL polish + curated demo-path notes in tests/smoke-checklist.md; the
  user hasn't named demo docs → the route recommendation lands at T5 (walkthrough/freeze).

Ledger block appended to .dev-wiki/assumption-ledger.md at the gate (by the orchestrator).
Plan landed as 6 lite tasks in tasks.md (T1 live-risk HIGHs · T2 lift R2 refocus · T3 FINTRAC
lens attribution · T4 ranked copy pass · T5 walkthrough/FREEZE · T6 full regate — the frozen
dist/corpus baseline MOVES, two-commit delivery convention).
