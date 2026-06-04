# Project: AML Signal Engine — Vision Demo

> Last updated: 2026-06-04T19:15:46 by /dev-init

## Recommended Next Action

Start M1: run `/dev-plan` to break Phase 2 (config-driven refactor) into tasks — write
`config/schema.md`, extract fentanyl content to `config/typologies/fentanyl.json`, make
the engine generic, and add the single-file build.

## Active Phase

**[[phase-02-config-driven-refactor|Phase 2: Config-driven refactor (M1)]]** (status: active)

Entry criteria: MET (M0 complete — baseline demo runs from the repo, committed `c56b82e`)
Exit criteria: fentanyl demo behaviourally equivalent but config-driven; `dist/index.html` runs from `file://`

Progress: ~0% (just planned; M0 bootstrap done)

## Active Phase Contract

Phase: 2 - Config-driven refactor (M1)
Tasks: see tasks.md (none enumerated yet — run /dev-plan)
Transition: continue
Abort: if blocked >3 attempts, ask user: skip or abort

## Recent Decisions

| Decision | Confidence | Date |
|----------|------------|------|
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
| aml_vision_demo_fentanyl.html | Baseline six-act demo (the thing being shipped) | 2026-06-04 |
| HANDOFF.md | Full context, content model, milestone plan | 2026-06-04 |
| CLAUDE.md | Always-loaded non-negotiables | 2026-06-04 |

## Session Journal (last 5)

- [2026-06-04] M0 bootstrap: git init, project docs, baseline imported + verified, committed `c56b82e`; dev-wiki initialized.

## Cross-References

- HANDOFF.md · CLAUDE.md · README.md
