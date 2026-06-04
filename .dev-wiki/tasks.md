# Tasks

> Last updated: 2026-06-04T19:15:46 by /dev-plan

<!-- phase:phase-02-config-driven-refactor -->
## Phase 2: Config-driven refactor (M1) — all tasks done (awaiting delivery acceptance + /dev-debrief)

- [x] T1 · `config/schema.md` written — content-model contract, validated against baseline (every field maps, no orphans)
- [x] T2 · `config/typologies/fentanyl.json` extracted — node diff confirms content-equivalent to baseline (checkpoint passed)
- [x] T3 · Engine genericized in `index.html` — all six acts read from `CONFIG`; literals (target candidate, signal-name, closing indicator, stats) promoted; single `__CONFIG__` injection point; zero typology literals in engine
- [x] T4 · Defensive rendering — `validateConfig()` + `goto()` guard + try/catch; partial/empty configs degrade to labeled placeholders, never blank the stage (verified: no-lift, no-coverage, empty {})
- [x] T5 · `scripts/build.py` (stdlib) — inlines config → `dist/index.html`; self-contained, fail-loud; inlined CONFIG deep-equals fentanyl.json
- [x] T6 · Verified — dist renders **byte-identical act HTML to the baseline** (all 7 acts); self-contained (Google Fonts only); `tests/smoke-checklist.md` written; baseline archived

> M1 exit criteria met. Engine is generic; `dist/index.html` is a single self-contained file.
> Next: present delivery for acceptance, then `/dev-debrief` (capture + commit) → `/dev-plan` M2.

<!-- phase:phase-01-bootstrap -->
<details>
<summary>Phase 1: Bootstrap (M0) — COMPLETED</summary>

- [x] git repo initialized
- [x] CLAUDE.md, README.md, HANDOFF.md, .gitignore written
- [x] baseline demo imported and verified (JS compiles, both gates + lift present, self-contained)
- [x] committed (`c56b82e`)

</details>

<!-- phase:future -->
<details>
<summary>Future phases (plan when active)</summary>

**Phase 3 · Multi-typology (M2)** — 2nd typology from public paraphrased advisory (pull indicators/typologies from aml-wiki); selector/switch; arc holds with no engine edits.
**Phase 4 · Presenter polish (M3)** — keyboard nav (←/→/Esc), reset, reduced-motion, speaker notes, cross-browser pass.
**Phase 5 · Live / pre-gen mode (M4, optional)** — `scripts/pregenerate.md` + `data/signals_*.json` loader w/ fallback; optional `backend/relay.py`.
**Phase 6 · Ship (M5)** — README complete, compliance self-check, `dist/index.html` verified offline, smoke checklist, human sign-off.

</details>
