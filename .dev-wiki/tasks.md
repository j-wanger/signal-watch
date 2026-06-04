# Tasks

> Last updated: 2026-06-04 by /dev-plan

<!-- phase:phase-06-ship -->
<!-- gate-log:phase-06 direction=approved delivery=accepted -->
<details>
<summary>Phase 6: Ship (M5) — COMPLETED + accepted (doc/verify only, zero engine edits)</summary>

Finalize for stage: true-up two stale + fentanyl-only docs to post-M3 / per-typology reality, then run the compliance + offline `file://` hard gate against BOTH built dist. M4 (live/pre-gen) skipped by decision. Closing "ask" slide + rename + Playwright deferred. Human sign-off = delivery gate.

- [x] T1 · Parameterize `tests/smoke-checklist.md` per typology | scope: tests/smoke-checklist.md | success: `! grep -q 'dist/index.html' tests/smoke-checklist.md && grep -qi 'reduced-motion' tests/smoke-checklist.md && grep -qi 'trade-based' tests/smoke-checklist.md` — stale single-file path gone, M3 controls now active verify items, per-typology fill table covers both typologies ✓ PASS
- [x] T2 · Refresh `README.md` (M3 shipped, both typologies) | scope: README.md | success: `! grep -qi 'planned for M3\|Next: M3\|Next.*M3' README.md && grep -qi 'Esc' README.md && grep -qi 'trade-based' README.md` — status reflects shipped M3 controls (←/→/Space/Esc/↺/reduced-motion); compliance names both fentanyl AND trade-based advisory sources ✓ PASS
- [x] T3 · Compliance self-check + offline `file://` verification (HARD GATE) | scope: dist/**, tests/smoke-checklist.md | success: `for f in dist/fentanyl/index.html dist/trade-based/index.html; do grep -q 'Illustrative data' "$f" || exit 1; done && ! grep -riE 'api[_-]?key|secret|token|password|sk-' dist/` — badge present every act both dist, advisories paraphrased+attributed, no secrets, no real-data patterns; both open from file:// offline, no console errors; pass/fail recorded in checklist. ✓ PASS (zero drift; runtime render carries from M3 on byte-identical dist; record in smoke-checklist.md)

> Exit (HANDOFF §1.2): README run/present/add-typology · compliance self-check passes · both dist run offline from file:// · smoke-checklist parameterized · human sign-off (Jake, at delivery gate).

</details>

<!-- phase:phase-04-presenter-polish -->
<!-- gate-log:phase-04 direction=approved delivery=accepted -->
<details>
<summary>Phase 4: Presenter polish (M3) — COMPLETED + accepted (engine-only)</summary>

Pure-engine M3: keyboard nav + reset + reduced-motion. NO config/schema edits. Speaker notes deferred. Chrome (macOS) target.

- [x] T1 · Centralize nav + reset + keys — `advance()`/`back()`/`reset()`; keys (→/Space/←/Esc) honor both gates via the `nextBtn.disabled` guard; ↺ Reset control + key legend; `reset()`→clean Act 0 (`maxReached=0`), shared by Esc + Act 6 "Run again"
- [x] T2 · prefers-reduced-motion — CSS `@media` (duration:0s, keeps `.sig` forwards-fill) + `REDUCED` flag (synchronous `T()`, `animVal` short-circuit); every reveal lands final in one paint
- [x] T3 · Rebuild both dist + verify — `build.py all`; both self-contained; behavioral harness on both dist × both motion modes (gates hold, no Act 5 without confirm, Esc resets, 0 pending timers under reduced-motion); real Chrome 149 renders Act 0

> M3 exit MET: keys-only nav, both gates intact, reduced-motion final-state, both dist self-contained. Engine intentionally edited (M2 zero-diff rule did not carry over); `config/` + `build.py` byte-identical.

</details>

<!-- phase:phase-03-multi-typology -->
<details>
<summary>Phase 3: Multi-typology (M2) — COMPLETED + accepted (commit 61a9cca)</summary>

Second typology = **Trade-based ML (TBML)**; switch = **build-time** (`dist/<id>/index.html`). Engine untouched.

- [x] T1 · `config/typologies/trade-based.json` authored — TBML from paraphrased public advisories (FinCEN Apr-2025, FATF 2024); within schema; price-anomaly target (gap+available); 2%/42% asymmetry as advisory highlight
- [x] T2 · `scripts/build.py` — per-typology `dist/<id>/index.html` + boundary validation (fails loud; caught a schema-doc bug: hints length); `all` mode; stale single-file removed
- [x] T3 · TBML verified — 7 acts render, target-derived signal `S-PRICE-ANOMALY-TRADE`, self-contained, inlined CONFIG deep-equals config
- [x] T4 · Regression + no-engine-edits proof — `git diff index.html` EMPTY (engine untouched); fentanyl dist byte-identical to baseline; both typologies pass validation

> M2 exit criteria met: 2 typologies, build-time switchable, **zero engine edits**. The schema generalized cleanly (one doc fix, no engine change).
> DISCOVERY: schema doc said `hints[7]`; baseline carries 8 (trailing unused). Fixed validator to steps==7 / next_labels,hints ≥7.

</details>

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

**Phase 5 · Live / pre-gen mode (M4, optional)** — `scripts/pregenerate.md` + `data/signals_*.json` loader w/ fallback; optional `backend/relay.py`.
**Phase 6 · Ship (M5)** — README complete, compliance self-check, dist verified offline, smoke checklist, human sign-off.

</details>
