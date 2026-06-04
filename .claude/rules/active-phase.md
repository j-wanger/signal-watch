# Active Phase Context

Phase: 2 - Config-driven refactor (M1)
Objective: Make the engine generic against a typology config; extract fentanyl content to JSON; add a build step that inlines everything into a single self-contained dist/index.html.
Scope: config/**, src/**, scripts/build.*, index.html, dist/index.html
Key constraints:
- NO ES modules / fetch()-loaded config in the SHIP target — file:// breaks. Build inlines everything.
- Keep six-act arc, both human gates, combination-lift reveal, and the "Illustrative data & outputs" badge.
- Engine stays generic — no typology copy in engine code. No real data; advisories paraphrased + public.
Exit criteria:
- config/schema.md written + validated; fentanyl content extracted to config/typologies/fentanyl.json
- engine renders all six acts from any valid config; malformed config degrades gracefully
- build inlines config → dist/index.html, verified from file://; behaviour equivalent to baseline
Abort: if blocked >3 attempts on any task, run /dev adjust
