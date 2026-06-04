# Project: AML Signal Engine — Vision Demo

> Last updated: 2026-06-04 by /dev-debrief

## Recommended Next Action

**M5 shipped — Phase 6 complete + accepted, committed to main.** The project now meets HANDOFF §1.2
definition of shipped: reliable offline (single-file per-typology `dist/<id>/index.html`),
multi-typology from config, presenter-ready (M3 controls), compliance-clean (hard gate PASS),
documented (README + per-typology smoke-checklist). **No required work remains.** Optional follow-ups
(all config-driven, none block, plan each with `/dev-plan` if wanted): M4 live/pre-gen (unbuilt by
decision — inert under `file://`); a closing "ask" slide (new act → its own phase); additional
typologies (e.g. pig-butchering — one JSON, the smoke-checklist just gains a column).

## Active Phase

**[[phase-06-ship|Phase 6: Ship (M5)]]** (status: completed)

Entry criteria: MET (M3 complete — presenter-ready, multi-typology; M4 optional, skipped by decision)
Exit criteria (HANDOFF §1.2): MET — README run/present/add-typology · compliance self-check PASS (no
real data, advisories paraphrased+public, badge present, no secrets) · both `dist/<id>/index.html` run
offline from `file://` · `tests/smoke-checklist.md` parameterized per typology · human sign-off (Jake,
accepted 2026-06-04).

Progress: 100% — delivery accepted, committed to main. Doc/verify only (`index.html` + `config/` +
`scripts/` byte-identical; dist byte-identical to a fresh rebuild — zero drift).
Next: project shipped; remaining items are optional config-driven follow-ups.

## Active Phase Contract

Phase: 6 - Ship (M5) — COMPLETED + accepted
Tasks: 3/3 done — T1 parameterize smoke-checklist → T2 refresh README → T3 compliance + offline gate (PASS)
Transition: complete
Abort: n/a (phase complete)

## Recent Decisions

| Decision | Confidence | Date |
|----------|------------|------|
| M4 (live/pre-gen) skipped: pre-gen needs `fetch()` (breaks `file://`), so it's inert in the single-file ship artifact — always falls back to inline. Scripted IS the ship path; M5 ship is next | high | 2026-06-04 |
| M5 is doc/verify only, zero engine edits: true-up stale README + smoke-checklist to post-M3/per-typology reality, then run compliance + offline `file://` hard gate on both dist | high | 2026-06-04 |
| Closing "ask" slide deferred from M5 (new act → touches six-act-arc non-negotiable + config/schema; a content effort, not a ship task). Product name kept as "Signal Engine". Playwright skipped (dep against dependency-light agreement for a one-shot demo) | medium | 2026-06-04 |
| Ship target = single self-contained `dist/<id>/index.html` per typology (the old `dist/index.html` single path is retired); hosted-vs-single [OPEN] resolved to single-file per decision-log §10 | high | 2026-06-04 |
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

- [RESOLVED 2026-06-04] Ship as single file vs hosted — **single self-contained file** per typology (decision-log §10 settled; M5 ships this)
- [RESOLVED 2026-06-04] Presentation mode → **scripted** (M4 live/pre-gen skipped by decision)
- [DEFERRED 2026-06-04] Closing "ask" slide — out of M5 (new act touches six-act-arc + needs config/schema); revisit as a config-driven follow-up
- [OPEN] Product/name — kept as "Signal Engine" for M5; rename is a branding call if ever wanted
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

- [2026-06-04] M5 ship: doc/verify only (zero engine/config edits — `index.html`+`config/`+`scripts/` clean). Parameterized `tests/smoke-checklist.md` per typology (removed stale single-file `dist/index.html` path; per-typology fill table for the 6 values that differ; M3 controls moved deferred→active checks). Refreshed README (M2→ship; shipped M3 controls; both-typology compliance). Compliance + offline `file://` **HARD GATE PASS**: zero drift (`build.py all` byte-identical, `git status dist/` clean), badge both, self-contained (no fetch/external script; only Google Fonts), advisories paraphrased+attributed, no secrets/PII. M4 skipped (inert under file://). Runtime render carries from M3 (byte-identical dist; no fresh browser run this session). Committed to main.
- [2026-06-04] M3 presenter polish: engine-only — centralized nav (advance/back/reset) + keys (←/→/Space/Esc) reusing the gate logic via the `nextBtn.disabled` guard; ↺ reset control; `prefers-reduced-motion` final-state (CSS @media + synchronous `T()`/`animVal`). Verified both shipped dist × both motion modes (gates hold, no Act 5 without confirm, 0 pending timers reduced); real Chrome 149 renders. `config/`+`build.py` byte-identical. Speaker notes deferred.
- [2026-06-04] M2 multi-typology: added trade-based.json (TBML) from aml-wiki survey, paraphrased; build.py gained per-typology dist + build-boundary validation. TBML verified; engine untouched (zero index.html diff); fentanyl regression byte-identical.
- [2026-06-04] M1 config-driven refactor: schema + fentanyl.json extracted; engine genericized (`__CONFIG__` injection, literals promoted); defensive rendering; stdlib build. Verified byte-identical act HTML to baseline; baseline archived.
- [2026-06-04] M0 bootstrap: git init, project docs, baseline imported + verified, committed `c56b82e`; dev-wiki initialized.

## Cross-References

- HANDOFF.md · CLAUDE.md · README.md
- Knowledge wiki: **aml-wiki** (registered central store) — domain reference for typologies,
  indicators, FINTRAC/FinCEN/E-23. Linked via gitignored `wiki/` symlink; query with `/wiki-query`.
