---
title: "Phase 9: Build-drift guard"
aliases: [signal-watch-drift-guard, zero-drift-invariant, build-check]
category: phases
tags: [milestone-m6, build, invariant, drift-guard, smoke-checklist]
parents: []
created: 2026-06-05
updated: 2026-06-05
source: plan
status: completed
ceremony: lite
scope: ["scripts/build.py", "tests/smoke-checklist.md", "README.md"]
entry_criteria: "Phase 8 (M6 doc true-up) delivered + accepted (commit 042d732). That phase's rebuild DISCOVERED the M5 zero-drift invariant (committed dist == fresh build) had silently broken in Phase 7 — caught only by accident. The invariant has no runnable guard; the smoke-checklist's zero-drift item is manual prose and undercounts typologies (says 'both dist', i.e. 2, against the shipped 3)."
exit_criteria: "`python3 scripts/build.py --check all` exits 0 on clean HEAD and non-zero (naming the typology) on an un-rebuilt config drift; `build.py all && git diff --exit-code dist/` clean (refactor is output-neutral); smoke-checklist carries the runnable `--check all` guard with no stale 'both dist'/2-typology count (all 3 typologies referenced) + the `git status --porcelain dist/` complement; `--check` documented in build.py docstring + README; `git diff index.html` empty."
---

# Phase 9: Build-drift guard

## Objective

Turn the M5 **zero-drift invariant** (committed `dist/<id>/index.html` == a fresh build of
its config) — which silently broke in Phase 7 and was caught only by accident during Phase 8's
rebuild — into a **runnable, non-mutating guard**, and wire it into the smoke-checklist.

Doc + build-script-glue only. The engine (`index.html`) is NOT touched and there are no config
changes, so all 3 `dist/` files stay byte-identical (`git status --porcelain dist/` clean at
phase end).

## Approach

Mechanism = an in-process `python3 scripts/build.py --check [all|<id>]` mode, NOT a
`build.py all && git diff` one-liner. Refactor `build_one` into:

- `render_one(typ, template) -> str` — validate + inline + self-contained guard, **returns**
  the output string;
- a thin writer that writes the string to `dist/<id>/index.html`.

The `--check` path renders each config and byte-compares against the committed
`dist/<id>/index.html`, prints a per-typology drift report, and exits non-zero on any mismatch
or a missing built file (0 when clean). It stays **pure-stdlib and git-agnostic** — it does NOT
shell out to git. The `git status --porcelain dist/` one-liner is documented in the
smoke-checklist as the belt-and-suspenders complement that also catches stray *untracked* dist
files `--check` won't see. The refactor must be **output-neutral**: `build.py all` stays
byte-identical to the committed dist.

## Scope

Files affected:
- `scripts/build.py` — extract `render_one`; add `--check` mode + per-typology drift report; docstring Usage.
- `tests/smoke-checklist.md` — replace the manual zero-drift prose (≈L72) with the runnable command; fix the stale 2-typology count; note the `git status --porcelain` complement.
- `README.md` — one-line drift-guard command under "How to run".

## Exit Criteria

- [ ] `python3 scripts/build.py --check all` exits 0 on clean HEAD; exits non-zero and names the typology on an un-rebuilt config drift
- [ ] `python3 scripts/build.py all && git diff --exit-code dist/` clean (refactor output-neutral)
- [ ] smoke-checklist carries the runnable `--check all` guard; no stale "both dist"/2-typology count; all 3 typologies referenced; `git status --porcelain dist/` complement noted
- [ ] `--check` documented in build.py docstring + README "How to run"
- [ ] `git diff index.html` empty

## Constraints (load-bearing)

- **Engine untouched** — prevents a "drift guard" PR from sneaking an engine change in. `git diff index.html` must be empty.
- **Zero config changes → all 3 dist byte-identical** — prevents the guard work from itself becoming a source of drift. `git status --porcelain dist/` clean at phase end.
- **Pure-stdlib + git-agnostic** — prevents coupling the build to a git checkout; `--check` is an in-process byte-compare, no `git` subprocess.
- **Output-neutral refactor** — prevents the `render_one` extraction from silently changing dist bytes; `build.py all` must reproduce the committed dist exactly.
- **Self-contained guard 0 tokens + `node --check` PASS** preserved on built dist.

## Checkpoints

- If making the guard non-flaky requires the **build to become deterministic in a way that changes dist bytes** (i.e. the build turns out to be non-deterministic): STOP and report — that's a different fix outside this doc/script-glue slice.
- If blocked >3 attempts on a task: ask the user — skip or abort.

## Notes

Rationale for HARDEN-before-SCALE: the M6 pipeline thesis is already proven by the Phase-7
walking skeleton (one real advisory, end-to-end, verbatim render). A corpus crawler / automated
derivation don't earn their complexity for a ~3-typology demo, and automated derivation risks
pulling a neural judge toward the build boundary (against deterministic-validators-at-boundaries).
The guard closes a real Phase-7 invariant breach and is cheap. Committing built `dist/` is kept
(the single file IS the deliverable — opens straight from the repo, offline, no Python), so the
invariant is guarded rather than dissolved. Pre-commit hook / CI enforcement explicitly DEFERRED
(lite ceremony; HANDOFF "don't over-engineer") — a clean follow-up if wanted later. Refactor
target verified during planning: `build_one(typ, template)` at `scripts/build.py:176`, `main()`
at `:222`; stale prose at `tests/smoke-checklist.md:72`. Direction confirmed by user 2026-06-05.
