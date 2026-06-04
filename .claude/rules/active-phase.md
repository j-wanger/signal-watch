# Active Phase Context

Phase: 2 - Config-driven refactor (M1)
Objective: Make the engine generic against a typology config; extract fentanyl content to JSON; add a stdlib build that inlines the active config into a single self-contained dist/index.html.
Scope: config/**, index.html, scripts/build.py, dist/index.html, tests/**
Key constraints:
- NO ES modules / fetch()-loaded config in the SHIP target — file:// breaks. build.py inlines `const CONFIG = {…}`.
- Single source of truth = config/typologies/*.json. index.html has a `__CONFIG__` injection point, no inline duplicate.
- Engine truly generic — promote entangled literals (C2 target, proposal signal-name, IND-02 closing id) to config fields. Grep engine clean of typology strings.
- Keep six-act arc, both human gates, combination-lift reveal, "Illustrative data & outputs" badge. No real data; advisories paraphrased + public.
- Defensive: malformed/partial config shows a labeled placeholder, never blanks the stage.
Exit criteria:
- config/schema.md written + validated; fentanyl content extracted to config/typologies/fentanyl.json (diff-equal to baseline)
- engine renders all six acts from any valid CONFIG; build inlines → dist/index.html, verified from file://; behaviour equivalent to baseline
Abort: if blocked >3 attempts on any task, run /dev adjust

Gates:
- [x] Direction confirmed by user (minimal structure approved 2026-06-04)
- [x] Delivery accepted (2026-06-04 — verified byte-identical to baseline; debrief + commit)
