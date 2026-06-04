---
title: "Phase 4: Presenter polish (M3)"
aliases: []
category: phases
tags: [milestone-m3]
parents: []
created: 2026-06-04
updated: 2026-06-04
source: plan
status: completed
scope: ["index.html", "dist/**"]
entry_criteria: "M2 complete — multi-typology switchable."
exit_criteria: "A presenter can run it end-to-end on the target laptop with keys only."
---

# Phase 4: Presenter polish (M3)

## Objective

Make it stage-ready: keyboard navigation, reset, optional speaker notes, reduced-motion
support, and a cross-browser pass on the presentation browser.

## Scope

- keyboard handlers (←/→ nav, Esc reset), reset control
- `prefers-reduced-motion` handling for all animations
- optional speaker-notes / teleprompter overlay (toggle)
- timing/pacing review

## Exit Criteria

- [x] ←/→/Space navigate acts; Esc resets to clean Act 0 (verified: real keydown listener, both gates hold)
- [x] reset control present and wired (↺ Reset in controls bar; rendered in real Chrome)
- [x] `prefers-reduced-motion` respected (gauge, lift bars, streaming, build log) — final state in one paint
- [~] cross-browser pass — Chrome (macOS) target: headless Chrome 149 renders both dist; full live pass = delivery gate
- [deferred] (optional) speaker-notes overlay toggle — out of M3 (needs config-driven copy; later phase)
- [~] end-to-end run with keyboard only — automated behavioral pass on both dist; human visual run = delivery gate

## Constraints

- Keyboard nav must respect the gates: Act 3 → can't advance with zero selected;
  Act 4 → confirm still required. Prevents: keys bypassing the wow beats.

## Notes

Reduced-motion must not break the narrative — fall back to instant state, not no state.

## Plan (2026-06-04, lite — pure-engine)

Speaker notes DEFERRED (would need config-driven copy + schema + both JSONs; out of this phase).
Cross-browser target = **Chrome (macOS)**. This phase intentionally edits the engine — the M2
byte-identical/zero-diff rule does not carry over.

- **T1 · Centralize nav + reset + keys.** Extract `advance()`/`back()`/`reset()` from the
  next/back handlers; bind keys (→/Space=advance, ←=back, Esc=reset) with an
  `if(nextBtn.disabled)return` guard so gate #1 (Act 3, 0 selected) and gate #2 (Act 4 confirm)
  hold under keyboard. Visible Reset control + subtle ←/→·Esc legend. `reset()` → clean Act 0
  (selected→default, confirmed=false, maxReached=0), applied to both Esc and Act 6 "Run again".
- **T2 · `prefers-reduced-motion`.** CSS `@media` neutralizes keyframes/transitions; a `reduced`
  guard in the JS reveal fns (streamAdvisory, build log, act5 lift, animVal, gauge fills) jumps to
  FINAL state — full advisory + all signals, completed build log, bars/gauge at final width+number.
- **T3 · Rebuild + verify.** `build.py all` → both dist self-contained; Chrome (macOS) keys-only
  end-to-end pass on both typologies; both gates hold.
