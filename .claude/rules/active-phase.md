# Active Phase Context

Phase: 4 - Presenter polish (M3) — COMPLETED (engine-only)
Objective: Stage-ready, keyboard-driven run — nav (←/→/Space/Esc), ↺ reset, prefers-reduced-motion — without breaking the six-act arc or the two wow beats.
Scope: index.html, dist/** (config/ + build.py byte-identical — engine-only kept)
Outcome:
- Nav centralized (advance/back/reset); keys reuse the gate logic via the `nextBtn.disabled` guard.
- reset() → clean Act 0 (selected→default, confirmed=false, maxReached=0); shared by Esc + Act 6 "Run again".
- prefers-reduced-motion: CSS @media (duration:0s) + REDUCED flag (synchronous T(), animVal short-circuit) → final state in one paint.
- Verified: both shipped dist × both motion modes (gates hold, no Act 5 without confirm, Esc resets, 0 pending timers reduced); real Chrome 149 renders Act 0.
- Speaker notes DEFERRED (would need config-driven copy — later phase).
Next: /dev-plan for M5 ship (M4 live/pre-gen optional).
Abort: n/a (complete).

Gates:
- [x] Direction confirmed by user (pure-engine M3; Chrome macOS; notes deferred — approved 2026-06-04)
- [x] Delivery accepted (post-implementation report 2026-06-04 — accepted, committed)
