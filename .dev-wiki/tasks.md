# Tasks

> Last updated: 2026-06-04T19:15:46 by /dev-init

<!-- phase:phase-02-config-driven-refactor -->
## Phase 2: Config-driven refactor (M1) — ACTIVE

- [ ] Write `config/schema.md` (typology content-model, HANDOFF §5) and validate against existing fentanyl content
- [ ] Extract fentanyl content (`STEPS`/`INDICATORS`/`ADVISORY`/`CANDIDATES`/`LIFT` + stats) into `config/typologies/fentanyl.json`
- [ ] Make the engine render all six acts generically from any valid config (no hardcoded typology copy)
- [ ] Defensive rendering: malformed/partial config degrades gracefully, never blanks the stage
- [ ] Add build step (stdlib) that inlines src + css + active config → `dist/index.html`
- [ ] Verify `dist/index.html` runs from `file://` and is behaviourally equivalent to the baseline (both gates + lift intact)

> Run `/dev-plan` to enrich these with TDD cycle, scope globs, and success criteria before implementing.

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

**Phase 3 · Multi-typology (M2)** — 2nd typology from public paraphrased advisory; selector/switch; arc holds with no engine edits.
**Phase 4 · Presenter polish (M3)** — keyboard nav (←/→/Esc), reset, reduced-motion, speaker notes, cross-browser pass.
**Phase 5 · Live / pre-gen mode (M4, optional)** — `scripts/pregenerate.md` + `data/signals_*.json` loader w/ fallback; optional `backend/relay.py`.
**Phase 6 · Ship (M5)** — README complete, compliance self-check, `dist/index.html` verified offline, smoke checklist, human sign-off.

</details>
