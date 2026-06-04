# Project: AML Signal Engine — Vision Demo

> Last updated: 2026-06-04T19:15:46 by /dev-init

## Recommended Next Action

M1 implementation complete (all 6 tasks done, dist verified equivalent). Accept the delivery,
then run `/dev-debrief` (capture + commit this milestone) and `/dev-plan` for M2 (multi-typology
— author a 2nd typology from public paraphrased advisory, pulling indicators from aml-wiki).

## Active Phase

**[[phase-02-config-driven-refactor|Phase 2: Config-driven refactor (M1)]]** (status: completed)

Entry criteria: MET (M0 complete — baseline demo runs from the repo, committed `c56b82e`)
Exit criteria: MET — engine generic against config; `dist/index.html` self-contained + byte-identical act HTML to baseline

Progress: 100% — delivery accepted, milestone committed. Next active phase: M2 (run `/dev-plan`).

## Active Phase Contract

Phase: 2 - Config-driven refactor (M1)
Tasks: 6 (see tasks.md) — schema → extract JSON → genericize engine → defensive render → build → verify
Transition: continue
Abort: if blocked >3 attempts, ask user: skip or abort

## Recent Decisions

| Decision | Confidence | Date |
|----------|------------|------|
| M1 dev structure: minimal — one engine template (index.html) + config/typologies/*.json + stdlib build.py inliner; no src/ split (subtraction/YAGNI) | high | 2026-06-04 |
| Single source of truth = config JSON; index.html uses a `__CONFIG__` injection point (no inline duplicate) | high | 2026-06-04 |
| Promote entangled literals (C2 target, proposal name, IND-02 closing id) to config fields so engine is truly generic (unblocks M2) | high | 2026-06-04 |
| Lite ceremony (small single-artifact demo; HANDOFF says don't over-engineer) | high | 2026-06-04 |
| Skip language scaffold (vanilla HTML/JS; py/ts harness would over-engineer) | high | 2026-06-04 |
| Ship target = single self-contained file; no ES modules/fetch (file:// trap) | settled | 2026-06-04 |

## Blockers and Open Questions

- [OPEN] Ship as single file vs hosted page (HANDOFF §10) — presentation/branding call
- [OPEN] Presentation mode: scripted / pre-generated / live (HANDOFF §10)
- [OPEN] Which 2nd typology: pig-butchering and/or trade-based (M2)
- [OPEN] Closing "what it takes to build this / the ask" slide? (HANDOFF §10)

## Key Artifacts

| Path | Purpose | Last Modified |
|------|---------|---------------|
| index.html | Generic engine template (`__CONFIG__` injection point) | 2026-06-04 |
| config/schema.md · config/typologies/fentanyl.json | Content-model contract + fentanyl content (single source of truth) | 2026-06-04 |
| scripts/build.py | Inlines config → dist/index.html (ship target) | 2026-06-04 |
| dist/index.html | Built single self-contained ship file | 2026-06-04 |
| archive/aml_vision_demo_fentanyl.baseline.html | Original baseline (equivalence reference) | 2026-06-04 |

## Session Journal (last 5)

- [2026-06-04] M1 config-driven refactor: schema + fentanyl.json extracted; engine genericized (`__CONFIG__` injection, literals promoted); defensive rendering; stdlib build → dist/index.html. Verified byte-identical act HTML to baseline; baseline archived.
- [2026-06-04] M0 bootstrap: git init, project docs, baseline imported + verified, committed `c56b82e`; dev-wiki initialized.

## Cross-References

- HANDOFF.md · CLAUDE.md · README.md
- Knowledge wiki: **aml-wiki** (registered central store) — domain reference for typologies,
  indicators, FINTRAC/FinCEN/E-23. Linked via gitignored `wiki/` symlink; query with `/wiki-query`.
