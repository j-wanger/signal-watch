# Tasks

> Last updated: 2026-06-04T19:15:46 by /dev-plan

<!-- phase:phase-03-multi-typology -->
## Phase 3: Multi-typology (M2) — all tasks done (awaiting delivery acceptance + /dev-debrief)

Second typology = **Trade-based ML (TBML)**; switch = **build-time** (`dist/<id>/index.html`). Engine untouched.

- [x] T1 · `config/typologies/trade-based.json` authored — TBML from paraphrased public advisories (FinCEN Apr-2025, FATF 2024); within schema; price-anomaly target (gap+available); 2%/42% asymmetry as advisory highlight
- [x] T2 · `scripts/build.py` — per-typology `dist/<id>/index.html` + boundary validation (fails loud; caught a schema-doc bug: hints length); `all` mode; stale single-file removed
- [x] T3 · TBML verified — 7 acts render, target-derived signal `S-PRICE-ANOMALY-TRADE`, self-contained, inlined CONFIG deep-equals config
- [x] T4 · Regression + no-engine-edits proof — `git diff index.html` EMPTY (engine untouched); fentanyl dist byte-identical to baseline; both typologies pass validation

> M2 exit criteria met: 2 typologies, build-time switchable, **zero engine edits**. The schema generalized cleanly (one doc fix, no engine change).
> DISCOVERY: schema doc said `hints[7]`; baseline carries 8 (trailing unused). Fixed validator to steps==7 / next_labels,hints ≥7.

<!-- phase:phase-02-config-driven-refactor -->
<details>
<summary>Phase 2: Config-driven refactor (M1) — COMPLETED (commit 99899ad)</summary>

- [x] T1 schema · T2 fentanyl.json · T3 generic engine · T4 defensive · T5 build.py · T6 verified (byte-identical to baseline)

</details>

<!-- phase:phase-01-bootstrap -->
<details>
<summary>Phase 1: Bootstrap (M0) — COMPLETED (commit c56b82e)</summary>

- [x] git init · project docs · baseline imported + verified · committed

</details>

<!-- phase:future -->
<details>
<summary>Future phases (plan when active)</summary>

**Phase 4 · Presenter polish (M3)** — keyboard nav (←/→/Esc), reset, reduced-motion, speaker notes, cross-browser pass.
**Phase 5 · Live / pre-gen mode (M4, optional)** — `scripts/pregenerate.md` + `data/signals_*.json` loader w/ fallback; optional `backend/relay.py`.
**Phase 6 · Ship (M5)** — README complete, compliance self-check, dist verified offline, smoke checklist, human sign-off.

</details>
