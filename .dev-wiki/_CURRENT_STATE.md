# Project: AML Signal Engine — Vision Demo

> Last updated: 2026-06-04 by /dev-debrief

## Recommended Next Action

M3 complete (presenter polish — keyboard nav, reset, reduced-motion; engine-only, both dist rebuilt,
delivery accepted + committed). Next: `/dev-plan` for **M5 ship** (README, compliance self-check,
offline smoke checklist, human sign-off) — M4 (live/pre-gen) is optional and can be skipped unless a
live data demo is wanted. Carry-over: parameterize `tests/smoke-checklist.md` per typology;
speaker-notes overlay is pre-scoped if presenters want on-screen prompts.

## Active Phase

**[[phase-04-presenter-polish|Phase 4: Presenter polish (M3)]]** (status: completed)

Entry criteria: MET (M2 complete — multi-typology build-time switchable, commit `61a9cca`)
Exit criteria: MET — ←/→/Space/Esc nav + ↺ reset; `prefers-reduced-motion` final-state; both dist
rebuilt + self-contained; gates hold under keyboard (verified on both dist × both motion modes).

Progress: 100% — delivery accepted, milestone committed. Engine-only (`config/`+`build.py` untouched).
Next active phase: M5 ship (run `/dev-plan`).

## Active Phase Contract

Phase: 4 - Presenter polish (M3) — COMPLETED
Tasks: 3/3 done — centralize nav + reset + keys → prefers-reduced-motion → rebuild both dist + verify
Transition: continue
Abort: n/a (phase complete)

## Recent Decisions

| Decision | Confidence | Date |
|----------|------------|------|
| M3 is pure-engine: edit index.html for nav/reset/reduced-motion, rebuild both dist. M2 zero-diff rule was phase-specific, does not carry over | high | 2026-06-04 |
| Keyboard nav reuses centralized advance()/back()/reset(); keys check `nextBtn.disabled` so both gates hold (programmatic .onclick() ignores the disabled attr) | high | 2026-06-04 |
| Reduced-motion = instant FINAL state (not no-state): CSS @media query + a `reduced` guard in the JS reveal fns | high | 2026-06-04 |
| Speaker notes DEFERRED out of M3 (would need config-driven copy + schema + both JSONs; keeps M3 a clean engine-only diff) | high | 2026-06-04 |
| Cross-browser target = Chrome (macOS); keys-only end-to-end pass on both typologies | medium | 2026-06-04 |
| reset() = clean Act 0 (selected→default, confirmed=false, maxReached=0), applied to both Esc and Act6 "Run again" (refines run-again, which left maxReached) | high | 2026-06-04 |
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
- [OPEN] Closing "what it takes to build this / the ask" slide? (HANDOFF §10)
- [RESOLVED 2026-06-04] 2nd typology → Trade-based ML (M2 shipped)

## Key Artifacts

| Path | Purpose | Last Modified |
|------|---------|---------------|
| index.html | Generic engine template (`__CONFIG__` injection point); M3 added keyboard nav + reset + reduced-motion | 2026-06-04 |
| config/schema.md | Content-model contract | 2026-06-04 |
| config/typologies/{fentanyl,trade-based}.json | Typology content (single source of truth per typology) | 2026-06-04 |
| scripts/build.py | Validates config at boundary + inlines → dist/<id>/index.html | 2026-06-04 |
| dist/{fentanyl,trade-based}/index.html | Built self-contained ship files (per typology) | 2026-06-04 |
| archive/aml_vision_demo_fentanyl.baseline.html | Original baseline (equivalence reference) | 2026-06-04 |

## Session Journal (last 5)

- [2026-06-04] M3 presenter polish: engine-only — centralized nav (advance/back/reset) + keys (←/→/Space/Esc) reusing the gate logic via the `nextBtn.disabled` guard; ↺ reset control; `prefers-reduced-motion` final-state (CSS @media + synchronous `T()`/`animVal`). Verified both shipped dist × both motion modes (gates hold, no Act 5 without confirm, 0 pending timers reduced); real Chrome 149 renders. `config/`+`build.py` byte-identical. Speaker notes deferred.
- [2026-06-04] M2 multi-typology: added trade-based.json (TBML) from aml-wiki survey, paraphrased; build.py gained per-typology dist + build-boundary validation. TBML verified; engine untouched (zero index.html diff); fentanyl regression byte-identical.
- [2026-06-04] M1 config-driven refactor: schema + fentanyl.json extracted; engine genericized (`__CONFIG__` injection, literals promoted); defensive rendering; stdlib build. Verified byte-identical act HTML to baseline; baseline archived.
- [2026-06-04] M0 bootstrap: git init, project docs, baseline imported + verified, committed `c56b82e`; dev-wiki initialized.

## Cross-References

- HANDOFF.md · CLAUDE.md · README.md
- Knowledge wiki: **aml-wiki** (registered central store) — domain reference for typologies,
  indicators, FINTRAC/FinCEN/E-23. Linked via gitignored `wiki/` symlink; query with `/wiki-query`.
