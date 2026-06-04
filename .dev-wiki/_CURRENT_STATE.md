# Project: AML Signal Engine — Vision Demo

> Last updated: 2026-06-04T19:15:46 by /dev-init

## Recommended Next Action

M2 complete (TBML added, engine untouched, both typologies build + validate). Next: `/dev-plan` for
M3 (presenter polish) — keyboard nav (←/→/Esc-reset), reset control, `prefers-reduced-motion`,
optional speaker notes, cross-browser pass. Note: keyboard nav must preserve both gates.

## Active Phase

**[[phase-03-multi-typology|Phase 3: Multi-typology (M2)]]** (status: completed)

Entry criteria: MET (M1 complete — engine generic against config, commit `99899ad`)
Exit criteria: MET — 2 typologies (fentanyl, trade-based), build-time switchable, ZERO engine edits

Progress: 100% — delivery accepted, milestone committed. Next active phase: M3 (run `/dev-plan`).

## Active Phase Contract

Phase: 3 - Multi-typology (M2)
Tasks: 4 (see tasks.md) — author trade-based.json → build.py per-id + validation → verify TBML → regression
Transition: continue
Abort: if blocked >3 attempts, ask user: skip or abort

## Recent Decisions

| Decision | Confidence | Date |
|----------|------------|------|
| M2 typology = Trade-based ML (richest aml-wiki coverage, dated public advisories, data-mappable signals, flows from fentanyl) | high | 2026-06-04 |
| M2 switch = build-time (`dist/<id>/index.html`); no runtime selector (scripted-first reliability + minimal) | high | 2026-06-04 |
| Validate config at the build boundary (build.py fails loud on schema violation) — deterministic validator at boundary | high | 2026-06-04 |
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
| index.html | Generic engine template (`__CONFIG__` injection point) — unchanged since M1 | 2026-06-04 |
| config/schema.md | Content-model contract | 2026-06-04 |
| config/typologies/{fentanyl,trade-based}.json | Typology content (single source of truth per typology) | 2026-06-04 |
| scripts/build.py | Validates config at boundary + inlines → dist/<id>/index.html | 2026-06-04 |
| dist/{fentanyl,trade-based}/index.html | Built self-contained ship files (per typology) | 2026-06-04 |
| archive/aml_vision_demo_fentanyl.baseline.html | Original baseline (equivalence reference) | 2026-06-04 |

## Session Journal (last 5)

- [2026-06-04] M2 multi-typology: added trade-based.json (TBML) from aml-wiki survey, paraphrased; build.py gained per-typology dist + build-boundary validation. TBML verified; engine untouched (zero index.html diff); fentanyl regression byte-identical.
- [2026-06-04] M1 config-driven refactor: schema + fentanyl.json extracted; engine genericized (`__CONFIG__` injection, literals promoted); defensive rendering; stdlib build. Verified byte-identical act HTML to baseline; baseline archived.
- [2026-06-04] M0 bootstrap: git init, project docs, baseline imported + verified, committed `c56b82e`; dev-wiki initialized.

## Cross-References

- HANDOFF.md · CLAUDE.md · README.md
- Knowledge wiki: **aml-wiki** (registered central store) — domain reference for typologies,
  indicators, FINTRAC/FinCEN/E-23. Linked via gitignored `wiki/` symlink; query with `/wiki-query`.
