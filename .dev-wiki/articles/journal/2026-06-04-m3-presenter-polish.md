---
title: "2026-06-04 · M3 presenter polish"
category: journal
date: 2026-06-04
phase: phase-04-presenter-polish
tags: [milestone-m3, presenter, accessibility, keyboard-nav, reduced-motion]
---

# M3 — presenter polish

## What shipped
Made the demo stage-ready for a live, keyboard-driven run. **Engine-only** — `config/` and
`scripts/build.py` byte-identical; both `dist/<id>/index.html` rebuilt.
- **Navigation centralized** in `index.html`: extracted `advance()` / `back()` / `reset()`; buttons
  AND keys route through them. `advance()` early-returns on `nextBtn.disabled`, so gate #1 (Act 3,
  0 selected) and the Act 4 build-lock are enforced in exactly one place.
- **Keyboard:** `→`/`Space` advance, `←` back, `Esc` reset. Space defers to a focused button (no
  double-fire); modifier chords + form fields ignored. Visible `↺ Reset` control + footer key legend.
- **`reset()`** = clean Act 0 (`selected`→default, `confirmed=false`, `maxReached=0`), applied to
  both Esc and the Act 6 "Run again" (which previously left `maxReached` at 6).
- **`prefers-reduced-motion`:** CSS `@media` collapses keyframes/transitions to ~0s (duration:0s,
  not `animation:none`, so `.sig`'s forwards keyframe still settles visible); a `REDUCED` flag makes
  `T()` run synchronously and `animVal()` jump to its final number → every staged reveal lands in
  one paint, never blank.

## Decisions
- **Pure-engine M3** — editing `index.html` is correct; the M2 "zero engine diff" rule was
  phase-specific (proving typology-agnosticism), not a permanent freeze. Engine stays generic.
- **Keys reuse the gate logic** rather than re-implementing it — keys call `advance()`, which checks
  `nextBtn.disabled`. (Programmatic `.onclick()` ignores the `disabled` attribute, so the guard must
  live in `advance()`, not rely on the attribute.)
- **Reduced-motion = instant FINAL state, not no-state** — synchronous `T()` + `animVal` short-circuit.
- **Speaker notes DEFERRED** out of M3 (would need config-driven copy + schema + both JSONs; keeps
  M3 a clean engine-only diff). Candidate for a later phase.
- **Cross-browser target = Chrome (macOS)**.

## Verification
- Ran the **real engine** (real `keydown` listener) on **both shipped dist** in **both motion modes**
  via a Node DOM-stub harness: gate #1 key-blocked at Act 3/0-selected; **no Act 5 without confirm**
  (stepper can't jump — `maxReached==4`); `Esc`→clean Act 0; reduced-motion final-state in one paint
  (0 pending timers). All green.
- Self-contained: single inline `<script>`, no fetch/module; fonts degrade offline.
- Real headless **Chrome 149** renders Act 0 + reset control on both typologies (no error placeholder).
- Scope: `config/` + `build.py` byte-identical (engine-only promise kept).

## Escape hatches
- None. (One test-harness self-correction: an early assertion checked "stays on Act 4" — a stub
  artifact of no-op `setTimeout`. The real gate #2 invariant is "no Act 5 without `confirmed`";
  corrected the assertion, engine unchanged.)

## Health delta
No new files, no deps. `index.html` +74 lines (nav primitives, keydown listener, `REDUCED` path,
reduced-motion media query, reset control). Both dist regenerated.

## Soft Observations / Phase N+1 Candidates
- Verification leaned on a hand-rolled Node DOM stub. If presenter/QA coverage grows, a tiny
  Playwright smoke (real key events through all 7 acts) would replace the stub and cover the visual
  layer the stub can't.
- Speaker-notes overlay is deferred but pre-scoped: optional `notes[7]` config field + a toggle.
  Cheap to add in a later phase if presenters want on-screen prompts.
- `tests/smoke-checklist.md` is still fentanyl-specific (carried over from M2) — M5 should
  parameterize it per typology.
- M4 (live/pre-gen) remains optional; M5 ship is the likely next milestone (README, compliance
  self-check, offline smoke, sign-off).
