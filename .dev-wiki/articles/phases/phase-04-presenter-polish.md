---
title: "Phase 4: Presenter polish (M3)"
aliases: []
category: phases
tags: [milestone-m3]
parents: []
created: 2026-06-04
updated: 2026-06-04
source: init
status: not-started
scope: ["src/**", "index.html", "dist/index.html"]
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

- [ ] ←/→ navigate acts; Esc resets to Act 0
- [ ] reset control present and wired
- [ ] `prefers-reduced-motion` respected (gauge, lift bars, streaming, build log)
- [ ] cross-browser pass on the actual presentation browser
- [ ] (optional) speaker-notes overlay toggle
- [ ] end-to-end run with keyboard only

## Constraints

- Keyboard nav must respect the gates: Act 3 → can't advance with zero selected;
  Act 4 → confirm still required. Prevents: keys bypassing the wow beats.

## Notes

Reduced-motion must not break the narrative — fall back to instant state, not no state.
