---
title: "Phase 19: Durability closeout — commit corpus-explorer test harness + pin _rf_triage"
aliases: []
category: journal
tags: ["M7", "durability", "testing", "lite"]
parents: [phase-19-durability-closeout]
created: 2026-06-06
updated: 2026-06-06
source: debrief
duration: ~30-45min (post-compaction estimate; may undercount)
---

# Phase 19: Durability closeout — commit corpus-explorer test harness + pin _rf_triage

## What Happened

A durability closeout at the END of the completed M0–M7 roadmap (demo at Definition of Done). With no
net-new feature value left that doesn't risk fabrication (combination-lift needs a precision source the
records don't carry — rejected Ph18) and no FinCEN scale frontier (12/14 derived; the 2 FATF advisories
have no red-flag list), the one remaining real-value move was DURABILITY — committing the corpus-explorer
test harness that had been ad-hoc/uncommitted across Ph17/Ph18 and flagged as a soft observation three
phases running.

**T1 — the harness (the centerpiece).** Committed `tests/corpus-explorer.test.mjs`: a ZERO-DEP Node
`vm`+DOM-shim runner (hand-rolled document/getElementById/querySelectorAll/window/requestAnimationFrame/
matchMedia/setTimeout — NEVER jsdom, per the file:// offline ethos + the project's dep-free
`--selftest`/`--check` idiom). It loads the COMMITTED `dist/corpus/index.html` (the real inlined
`__CORPUS__`), so it doubles as a build-output smoke test. The shim drives the actual div-toggle onclick
wiring — resolving the phase's one open sub-question (can interactive selection be driven keyboard-safe +
deterministic without a real DOM lib?) YES. 28 assertions pass (the plan estimated ~15): each of the 5
screens renders; the gate defaults all-BUILD_NOW-selected and a div-toggle onclick really flips `selected`;
Signal = selected∩buildable with both honest empty states; close-the-loop before→after coverage math + the
`Object.assign` no-mutation invariant; reduced-motion single-paint AND the animated path landing final
after a rAF/timer flush (this closes the Ph18 "animated close path is headless-untested" soft-obs);
0-picked flat-hold (no fake rise).

**T2 — pin `_rf_triage` (the honest non-fix).** The Ph17 reviewer MEDIUM (glued-no-separator overcount)
was reframed as PIN + DISCLOSE, NOT rewrite: an accurate glued counter would REINTRODUCE exactly the
deterministic parser Phase 17 deleted (anti-subtraction), and it's harmless today (live records render from
their indicators; build.py ignores flag_count for live ones). Added a bidirectional `--selftest` assertion
(the same 3 flags read `('low', 1)` when glued vs `('clean', 3)` when separated) + a docstring disclosure.
NO output/logic change — `--selftest` PASS, `corpus-status.json` + `dist/corpus` byte-identical.

**T3 — wire it into the ritual.** README.md (new `## Test` section), CLAUDE.md ("How to run" Test bullet),
and `tests/smoke-checklist.md` (intro framing + a "Corpus explorer" section) all name
`node tests/corpus-explorer.test.mjs` as the structural pre-present check.

Two carried Phase-19 candidates resolved during planning: the `anthropic` pin is DEAD
(`requirements-authoring.txt` does not exist — Ph17's deletion already took it; no task needed), and the
`tests/` gap was confirmed REAL. Clean phase — no escape hatches, no blocked tasks, abort/degrade path
(leaner assertion set) never needed.

## Decisions Made

(Lite ceremony — recorded in `_CURRENT_STATE.md` ## Recent Decisions during planning; no decision articles.)
- Phase 19 = durability closeout, over call-it-done / showcase-debt-true-up / new-stakeholder-ask.
- Zero-dep hand-rolled Node `vm`+DOM-shim, NEVER a third-party DOM library; the harness loads the committed
  dist so it doubles as a build-output smoke test.
- The `_rf_triage` footgun is PINNED + DISCLOSED, not rewritten (an accurate glued count reintroduces the
  Phase-17-deleted parser — anti-subtraction; harmless today).

## Problems Solved

- The Ph18 "animated (non-reduced) close path is headless-untested" soft-obs — now covered by a test that
  flushes the rAF/timer queue and asserts the animated path lands the final after-value.
- The "ad-hoc/uncommitted DOM-shim" soft-obs (three phases running) — the shim is now committed,
  documented, and wired into the pre-present ritual.

## Artifacts Changed

- `tests/corpus-explorer.test.mjs` (NEW — zero-dep `vm`+DOM-shim harness; 28 assertions; the project's
  first automated test for a browser ship artifact)
- `scripts/derive_signals.py` (`--selftest` bidirectional `_rf_triage` glued/separated pin + docstring
  disclosure; NO output/logic change)
- `README.md` (new `## Test` section), `CLAUDE.md` ("How to run" Test bullet), `tests/smoke-checklist.md`
  (intro framing + "Corpus explorer" section)

Frozen byte-untouched + verified git-diff-empty: `index.html`, `corpus.html`, `scripts/build.py`,
`config/**`, `data/fincen/**` (corpus-status.json + derived/*.json), `dist/**`.

## Related

- [[phase-19-durability-closeout|Phase 19: Durability closeout]] — parent phase
- [[2026-06-06-phase-18-corpus-explorer-arc|Phase 18]] — the arc this harness locks in

## Health Delta

+28 harness assertions (new committed harness) + 2 new `--selftest` pins. New dep-free test command added to
the toolchain (`node tests/corpus-explorer.test.mjs`). No type/lint toolchain delta (project uses
deterministic build/derive validators). All gates green at debrief: harness 28/28, `--selftest` PASS,
`--check all` zero drift across 4 artifacts, frozen set byte-untouched.

## Soft Observations / Phase N+1 Candidates

- The harness tests the COMMITTED dist, so editing `corpus.html` without rebuilding would test stale bytes —
  mitigated by the documented pre-present sequence (`--check all` drift guard → harness → smoke-checklist);
  a future hygiene pass could add a build-then-test wrapper. | evidence: `tests/corpus-explorer.test.mjs`
  reads `dist/corpus/index.html`
- The 0-BUILD_NOW close path (an advisory with literally zero BUILD_NOW indicators) is still unexercised by
  real data (all 12 live advisories have ≥1 BUILD_NOW), though the 0-PICKED branch — the SAME flat-hold code
  — is now covered via deselect-all. | improves on the Ph18 soft-obs
- The showcase six-act `index.html` has no equivalent automated harness (verified at M3 on real Chrome + the
  manual smoke-checklist); a future durability pass could extend the same `vm`+shim to it.
- `_CURRENT_STATE.md` is at ~104 lines (over the 100 soft cap) — a periodic trim is due (planner already
  adjudicated leaving it this phase to preserve load-bearing Ph18 context).
- The recurring showcase-debt true-up (elder presentation-values + fentanyl verbatim re-point) remains
  deferred — consistent with the documented scale/durability-over-showcase-polish pattern.

Retro check: not triggered (17 completed phases; 17 % 5 ≠ 0).
