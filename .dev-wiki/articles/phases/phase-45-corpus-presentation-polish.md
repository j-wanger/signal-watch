---
title: "Phase 45: Corpus demo presentation polish (pre-presentation day)"
aliases: [phase-45]
category: phases
tags: [corpus-explorer, presentation, polish, honesty, combination-lift, story-coherence]
parents: []
created: 2026-06-10
updated: 2026-06-10
source: plan
status: active
scope: ["corpus.html", "dist/corpus/**", "tests/corpus-explorer.test.mjs", "tests/smoke-checklist.md", "CLAUDE.md"]
entry_criteria: "Phase 44 delivered + accepted + committed (5c8c014/0835bff) + pushed; 0 open prior tasks."
exit_criteria: "Three story HIGH live-risk fixes in; NO fabricated lift number remains in corpus.html/dist/corpus (LIFT const + bars + 'pending calibration' tag deleted; the beat carries honest R2 composition-search-space inventory counts computed client-side, or the R1 zero-numbers copy fallback) + CLAUDE.md honesty paragraph rewritten in place; FINTRAC footer attribution fires on FINTRAC-bearing lens drills, empty on US-only; ranked copy MEDIUMs done; user walkthrough run with feedback dispositioned (no open HIGH) + presenter/demo-path notes in tests/smoke-checklist.md; dist/corpus rebuilt (frozen baseline moves) with --check all 5/5 + both node suites green; showcase + news artifacts byte-identical; always-on badge stays; presentation-ready by 2026-06-11."
---

# Phase 45: Corpus demo presentation polish (pre-presentation day)

## Objective

The corpus explorer (dist/corpus) is presented to stakeholders TOMORROW (2026-06-11). Polish phase:
(1) clean up any inconsistencies across the corpus demo; (2) remove the fake/illustrative
combination-lift numbers (the generic 18→64→83 template behind the "Illustrative · pending
calibration" tag) and refocus that beat on the CONCEPT of combination lift instead of fabricated
figures; (3) story coherence + delivery review of the demo arc. The user will likely add more
feedback; the phase must absorb it.

## Scope

Files and modules affected:
- `corpus.html` — the lift beat (`renderLift`, corpus.html:1132–1173, the `LIFT` const at 1148–1152,
  the `.lift*`/`.illus` CSS) + arc copy edits for coherence
- `dist/corpus/index.html` — rebuilt (the frozen-dist baseline moves; other dists stay byte-identical)
- `tests/corpus-explorer.test.mjs` — the P26-5 lift assertions (lines ~723–741: 3 bars,
  weak/mid/strong, the 18/83 count-up values) must follow the redesign
- `tests/smoke-checklist.md` — pre-present walkthrough updates
- `CLAUDE.md` — the "ONE approved fabrication-shaped reversal" honesty-constraint paragraph
  describes the 18→64→83 template; update in place when it's removed

## Exit Criteria

- [x] Inconsistency inventory across the corpus demo arc (measure-first) + fixes applied
- [x] No fabricated lift percentages anywhere in dist/corpus; the lift beat carries the composition
      CONCEPT (atoms-over-monolithic-scenarios) without invented figures — R2 real inventory counts
- [x] Story coherence + delivery review of the 7-step arc (landing → Select lenses → per-doc arc)
- [x] User feedback absorbed (T5 walkthrough 2026-06-10: 2 items fixed, 2 refinement rounds, FREEZE)
- [x] corpus-explorer harness green (239→273, lift assertions replaced); other dists `--check` byte-identical
- [x] Always-on "Illustrative data & outputs" badge stays; no non-negotiable change

## Constraints (optional)

- Honesty model holds: removing the fake numbers must not introduce any NEW number (no
  similarity/overlap/lift metric — the Phase-18/24 rejections stand). Prevents: trading one
  fabrication for another.
- The showcase (`index.html`) stays byte-frozen unless the user explicitly extends scope — its Act-5
  lift reveal is a non-negotiable wow beat. Prevents: silent showcase regression the day before
  presentation.
- news/showcase dists stay byte-identical (`--check` on untouched targets). Prevents: cross-artifact
  drift from a corpus-only phase.

## Checkpoints (optional)

- After the inconsistency inventory: report findings before fixing (user may reprioritize).
- After the lift-beat redesign renders: user walkthrough — presentation is tomorrow; the user's
  delivery feedback gates the freeze.

## Notes

Stub created 2026-06-10 by the dev-plan state loader; activated 2026-06-10 at the plan (lite,
6 tasks T1–T6 in tasks.md). Presentation date 2026-06-11 — one-day horizon. The user's
feedback-absorption expectation suggests small, reviewable increments over one big edit.

STATUS (debrief 2026-06-10): 6/6 tasks [x] same-session → READY FOR COMPLETION; delivery gate
pending (gate-log direction=approved delivery=pending; two-commit convention — the frozen
dist/corpus baseline MOVED by design). NOT auto-completed: the delivery flow flips status after
the commit verifiably lands. Assumption revisit: A1–A5 ALL held (A4 with the multi-doc
attribution upside). T5 walkthrough FROZEN (2 feedback items fixed — display-only fixEncoding +
landing hook; deferred items named in tasks.md T5 notes).

Assumption gate closed 2026-06-10 (all_accept: false): A1 [HIGH] lift = R2 real inventory counts
(don't-know round 1 → defended with worked real-value examples → accepted; no performance claim,
disclaimer removed, R1 zero-numbers fallback copy-only) · A2 [HIGH] showcase Act-5 untouched,
deliberate cross-artifact divergence accepted · A3 [MED] human gate = copy reframe + presenter
stagecraft, no interaction redesign · A4 [MED] FINTRAC attribution extends the Phase-28 footer
mechanism to the two lens views · A5 [MED] global polish + curated demo-path notes (route
recommendation lands at T5). Review findings + gate record:
[[phase-45-corpus-presentation-polish]] (articles/decisions/, approved); ledger block in
assumption-ledger.md.
