# Active Phase Context

Phase: 9 - Build-drift guard (zero-drift invariant) — READY FOR COMPLETION (all 3 tasks [x],
exit criteria met in the working tree; awaiting delivery gate + commit).
Objective: Turn the M5 zero-drift invariant (committed `dist/<id>/index.html` == a fresh build of
its config) — silently broken in Phase 7, caught by accident in Phase 8 — into a runnable,
non-mutating guard wired into the smoke-checklist. Doc + build-script-glue only.
Scope: scripts/build.py, tests/smoke-checklist.md, README.md.

What shipped: T1 `build.py` refactored (`render_one`=single source of truth for dist bytes + thin
writer; `check_one` git-agnostic byte-compare; `resolve_targets`; `--check [all|<id>]` mode). T2
smoke-checklist runnable `--check all` + de-staled 2→3 typologies + `git status --porcelain dist/`
complement. T3 `--check` documented in docstring + README. (Detail: journal 2026-06-05.)

Constraints held: engine untouched (`git diff index.html` empty); zero config edits → all 3 `dist/`
byte-identical; build output-neutral + byte-DETERMINISTIC; pure-stdlib + git-agnostic; `node --check`
PASS ×3; guard 0 tokens. Abort: a non-flaky guard needing dist bytes to change → PAUSE (did not).

Gates:
- [x] Direction confirmed by user (HARDEN-before-SCALE; in-process `--check`; keep committing dist; defer pre-commit/CI — 2026-06-05)
- [x] Delivery accepted (post-implementation report 2026-06-05; committed 33db22a)
