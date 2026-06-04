---
title: "Phase 2: Config-driven refactor (M1)"
aliases: []
category: phases
tags: [milestone-m1]
parents: []
created: 2026-06-04
updated: 2026-06-04
source: init
status: completed
scope: ["config/**", "src/**", "scripts/build.*", "index.html", "dist/index.html"]
entry_criteria: "M0 complete — baseline demo runs from the repo."
exit_criteria: "Fentanyl demo is behaviourally equivalent but driven by config; dist/index.html runs from file://."
---

# Phase 2: Config-driven refactor (M1)

## Objective

Make the engine generic against a typology config. Extract the fentanyl content
(`STEPS`/`INDICATORS`/`ADVISORY`/`CANDIDATES`/`LIFT`) into a config object validated
by a schema, and add a trivial build step that inlines everything into a single
self-contained `dist/index.html`.

## Scope

- `config/schema.md` — the typology content-model spec (HANDOFF §5)
- `config/typologies/fentanyl.json` — fentanyl content extracted from the baseline
- `src/` — engine + acts + css (dev-time modular split, optional)
- `scripts/build.*` — inline src + css + active config → `dist/index.html`
- `dist/index.html` — ship target

## Exit Criteria

- [x] `config/schema.md` written and validated against existing fentanyl content
- [x] fentanyl content extracted to `config/typologies/fentanyl.json`
- [x] engine renders all six acts generically from any valid config (no hardcoded copy)
- [x] defensive rendering: malformed/partial config degrades gracefully, never blanks the stage
- [x] build step inlines config → `dist/index.html`; verified opening from `file://` (structural; visual via smoke-checklist)
- [x] behaviour is equivalent to the baseline — byte-identical act HTML across all 7 acts

## Constraints (HANDOFF §3.2, §4)

- NO ES modules / `fetch()`-loaded config in the ship target — `file://` breaks. The
  build must inline everything. Prevents: dead demo off a USB stick.
- Keep the six-act arc, both human gates, the combination-lift reveal, and the
  always-visible "Illustrative data & outputs" badge. Prevents: losing the persuasion.
- Engine stays generic — no typology copy in engine code. Prevents: forked-per-typology.

## Checkpoints

- After the schema + fentanyl.json exist: diff the rendered output against the baseline
  before deleting the inline arrays. Prevents silent content drift.

## Notes

A dev-time `python3 -m http.server` is fine for iteration but must never be required
to present. The build script should be stdlib-only (no new dependencies).
