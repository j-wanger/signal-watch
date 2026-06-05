---
title: "Phase 9: Build-drift guard"
aliases: []
category: journal
tags: [milestone-m6, build, invariant, drift-guard, smoke-checklist]
parents: [phase-09-build-drift-guard]
created: 2026-06-05
updated: 2026-06-05
source: debrief
duration: ~45min
---

# Phase 9: Build-drift guard (zero-drift invariant)

Turned the M5 zero-drift invariant (committed `dist/<id>/index.html` == a fresh build of its
config) — which silently broke in Phase 7 and was caught only by accident during Phase 8's
rebuild — into a runnable, non-mutating guard, and wired it into the smoke-checklist. Doc +
build-script-glue only; engine untouched, zero config edits → all 3 `dist/` stay byte-identical.
Lite ceremony, one short session, all 3 tasks complete. READY FOR COMPLETION.

## What Happened

- **T1 — `--check` drift guard in build.py.** Refactored `build_one` into `render_one(typ,
  template) -> str` (pure validate + inline + self-contained guard; now the SINGLE source of
  truth for a typology's dist bytes) + a thin writer. Added `check_one(typ, template) -> bool`
  (non-mutating, git-agnostic byte-compare of committed dist vs a fresh in-memory render,
  per-typology verdict; catches an invalid-config `SystemExit` as a per-typology FAIL rather
  than aborting the whole run) and `resolve_targets()` (shared `all`/single-`<id>` logic). `main`
  gained a `--check [all|<id>]` mode. No new module — build script stays pure-stdlib.
- **T2 — wire into smoke-checklist + de-stale.** Runnable `python3 scripts/build.py --check all`
  now lives in "Build & open"; the stale M5 manual drift bullet became a forward-pointer; removed
  the "both dist"/2-typology phrasing (3 shipped typologies); noted `git status --porcelain dist/`
  as the belt-and-suspenders complement (catches stray untracked dist files `--check` won't).
- **T3 — document `--check`.** build.py module docstring Usage block + README "Run it" both
  carry the one-line drift-guard command and a short description.

## Decisions Made

(Captured in `_CURRENT_STATE` ## Recent Decisions at plan time — lite ceremony writes no decision
articles.) Direction = **HARDEN before SCALE/AUTOMATE**; mechanism = in-process `build.py --check`
(not a `git diff` one-liner); keep committing built `dist/`; pre-commit/CI enforcement deferred.

## Problems Solved

- **Silent stale-dist failure mode** (the Phase-7 breach Phase 8 caught by accident) — now has a
  deterministic, runnable guard that names the drifting typology and exits non-zero. The
  invariant is guarded rather than dissolved (committed single file IS the deliverable).

## Artifacts Changed

- `scripts/build.py` (`render_one`/`check_one`/`resolve_targets` extraction; `--check` mode; docstring Usage)
- `tests/smoke-checklist.md` (runnable guard, de-staled prose, `git status --porcelain` complement)
- `README.md` ("Run it" drift-guard command + description)

## Related

- [[phase-09-build-drift-guard|Phase 9: Build-drift guard]] — parent phase

## Health Delta

No automated test framework (demo project; smoke-checklist is the rehearsal gate). New
verification capability added = the `--check` drift guard. Build confirmed byte-DETERMINISTIC
(built twice → identical sha `8107629a…`); baseline clean (HEAD dist == fresh build); `node
--check` PASS ×3 on freshly built dist. Engine untouched (`git diff index.html` empty); zero
config edits → all 3 `dist/` byte-identical (no dist changes in the working tree).

## Soft Observations / Phase N+1 Candidates

- **Elder presentation-values true-up (Phase 10 candidate):** the smoke-checklist per-typology
  expected-values table (≈L15) and compliance attribution (≈L62) still cover only fentanyl +
  trade-based; `elder-financial-exploitation` (shipped Phase 7) has no walk-row. Needs elder's
  derived values (coverage %, signal `S-DORMANT-DRAIN-ELDER`, fire-stats, lift bars, delta chip).
  Doc-slice work, separable from the drift guard. Evidence: `tests/smoke-checklist.md` L15, L62.
- **Pre-commit hook running `--check`** for automatic drift enforcement (deferred this phase) —
  optional follow-up if drift recurs.
- **The two larger M6 vision forks remain open** post-hardening: FinCEN corpus crawler (SCALE)
  and automated article→signal derivation (AUTOMATE). Strategic next-increment choice.

## Activation Quality

No `active-knowledge.md` (lite phase, none generated) — step skipped.
