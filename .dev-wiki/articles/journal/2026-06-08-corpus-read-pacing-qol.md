---
title: "QOL: 3-tier progressive-read pacing on the corpus Read screen"
aliases: []
category: journal
tags: [qol, corpus, presentation, progressive-render, streaming-read, pacing, post-phase-33]
parents: [phase-33-corpus-completeness-resegmentation]
created: 2026-06-08
updated: 2026-06-08
source: debrief
duration: unknown
---

Post-Phase-33 QOL polish (no phase change). The corpus Read-screen "agent reading" stream
(`renderArticle`) now scales render speed by **three tiers** off the existing highlight `spans`
instead of a uniform char/frame budget: **cat1** general text in the active zone reads fast
(`MS1=0.45ms/char`, ~2× faster), **cat2** each red-flag phrase reveals whole then **DWELLS**
(`dwellMs = min(750, 220+len*6)` — a 0.2–0.75s processing pause while the caret holds + the
translation writes; was an instant pop), **cat3** general text past the LAST phrase blasts
(`MS3=0.12ms/char`, fastest — "after the wow, don't drag the demo"). The whole timeline still
scales to the ~45s cap on dense docs (SCALE compresses; relative tier speeds preserved).

**Why the phrase DWELLS rather than types out char-by-char:** `.hl` carries `padding:0 2px` +
`border-radius:3px`, so splitting a phrase into adjacent highlight spans would render as separate
pills; and the string-DOM harness tracks `insertAdjacentHTML` output (not live-element growth), so
a single growing span isn't observable in tests. A whole-reveal-then-dwell keeps one clean span,
is harness-safe, and reads as "stopped to process this one."

Committed `b7d942c` + pushed to main (follow-up to the Phase-33 commit `823c0c2`). Scope:
`corpus.html` + `dist/corpus` only. `--check all` 5/5 zero drift; corpus harness 235; news 65;
frozen set untouched. The pacing knobs (`MS1`/`MS3`/`dwellMs`) are tunable for the demo feel.

## Soft Observations / Phase N+1 Candidates
- The pacing knobs (`MS1`/`MS3`/`dwellMs`) are illustrative defaults — worth a presenter eyeball
  on the dense docs (financial-entities = 153 phrases × ~218ms dwell ≈ 33s of the 45s cap) to
  confirm the dwell cadence doesn't feel choppy at high phrase counts. Evidence: numeric pacing
  sim across small/dense docs this session.
