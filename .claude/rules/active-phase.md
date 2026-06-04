# Active Phase Context

Phase: 6 - Ship (M5) — ACTIVE
Objective: Finalize for stage — true-up two stale + fentanyl-only docs to post-M3/per-typology reality,
then run the compliance + offline `file://` hard gate on BOTH built dist. Doc/verify only.
Scope: README.md, tests/smoke-checklist.md, dist/** (verification). NO engine/config edits expected.

Tasks (in order):
- T1 · Parameterize `tests/smoke-checklist.md` per typology — fix stale `dist/index.html` → `dist/<id>/`;
  move M3 controls (←/→/Space/Esc/↺, reduced-motion) from "deferred" into active verify items;
  per-typology fill table (signal id, figures, coverage delta) sourced from config/typologies/*.json.
- T2 · Refresh `README.md` — status M2→shipping; document shipped M3 controls (drop "planned for M3");
  Compliance section covers BOTH fentanyl (FINTRAC Jan-2025, FinCEN FIN-2019/2024) AND trade-based.
- T3 · Compliance self-check + offline `file://` verification (HARD GATE) — badge present every act both
  dist; advisories paraphrased+attributed; no secrets/keys; no real-data; both open offline no console
  errors; record pass/fail. First full re-verification of post-M3 dist — NOT a formality.

Key constraints (load-bearing):
- M4 (live/pre-gen) skipped by decision — scripted single-file IS the ship path.
- Ship artifacts are per-typology `dist/<id>/index.html`; the old single `dist/index.html` is retired.
- Compliance is a hard gate, not a formality (HANDOFF §4): no real data, advisories paraphrased+public,
  "Illustrative data & outputs" badge always visible, no secrets in repo.
- Deferred (do NOT add in M5): closing "ask" slide, rename, Playwright.

Exit criteria (HANDOFF §1.2): README run/present/add-typology · compliance self-check passes · both
`dist/<id>/index.html` run offline from `file://` · smoke-checklist parameterized · human sign-off (Jake).

Abort: if T3 surfaces a defect needing an engine/config change beyond doc scope, PAUSE and report —
M5 is doc/verify; an engine fix is a scope change, not a silent in-phase edit.

Gates:
- [x] Direction confirmed by user (M5 ship, M4 skipped; 3 lite doc/verify tasks; ask-slide/rename/Playwright deferred — approved 2026-06-04)
- [x] Delivery accepted (post-implementation report 2026-06-04 — accepted, committed to main)
