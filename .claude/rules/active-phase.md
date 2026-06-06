# Active Phase Context

Phase: 18 - Corpus explorer arc — human gate + close-the-loop coverage payoff (M7) — DELIVERED + accepted (2026-06-06); all 5 tasks [x]; impl commit 6d654a4. Roadmap M0–M7 + this arc complete — run /dev-plan for Phase 19 (or the demo is at Definition of Done).
Objective: give the corpus explorer (`dist/corpus/`, from `corpus.html`) the dramatic arc the six-act showcase has — a 5-screen arc (Select → Coverage → Build recs/GATE → Signal → Close the loop), mirroring the showcase's Act 3 (human gate) + Act 6 (loop closes), grounded ENTIRELY in existing data with NO fabricated numbers.

Scope (the ONLY unfreeze): `corpus.html` + `dist/corpus/index.html` (rebuild) + `README.md` + `CLAUDE.md`. Byte-frozen: `index.html`, `scripts/build.py`, `config/**`, `data/fincen/**` (corpus-status.json + derived/*.json), `dist/{fentanyl,trade-based,elder-financial-exploitation}/`.

Key constraints:
- NO fabricated precision/lift numbers — the payoff is COVERAGE close-the-loop (existing `coverageIndex()`, already disclosed illustrative). Precision-lift EXPLICITLY REJECTED (records carry no precision/lift numbers).
- The human gate uses div-toggles, NOT `<input>` (preserves Space/arrow keyboard nav + determinism — the showcase `.selrow` pattern).
- The gate FOLDS into the existing Build-recs screen (subtraction test — no separate gate screen); default all-BUILD_NOW-selected, non-BUILD_NOW read-only, reset on `pick()`.
- The arc reuses existing data fields (status→coverage, build_rec→BUILD_NOW, build_logic→spec card) → NO schema/data/build.py change.
- Defensive 0-BUILD_NOW / 0-picked → honest flat-hold + note (never a fake rise); reduced-motion reaches the same final state.

Exit criteria: 5-screen arc ships · BUILD_NOW recs selectable (div-toggle gate, default all-selected, keyboard-safe, non-BUILD_NOW read-only) · Signal reflects the picks (honest empty state) · close-the-loop animates coverage before→after from the picks with a reduced-motion branch + honest 0-BUILD_NOW flat-hold · dist/corpus rebuilt · `--check all` shows index.html/build.py/config/data/3-typology-dists byte-frozen · `node --check` valid · README + CLAUDE document the arc + the coverage-not-precision honesty stance.
Abort: DEGRADE to close-the-loop-only (no gate; coverage close over ALL BUILD_NOW) if interactive selection can't be made keyboard-safe/deterministic without growing complex; keep the close screen informational if the math can't be honest; NEVER fabricate precision/lift. Blocked >3 attempts → ask user: skip or abort.

Gates:
- [x] Direction confirmed by user (corpus-explorer arc over call-it-done / hygiene / showcase-true-up / deepen-the-gate; coverage payoff over precision-lift; corpus.html-only scope; div-toggle gate folded into Build-recs — 2026-06-06)
- [x] Delivery accepted (post-implementation report 2026-06-06; impl commit 6d654a4; 15/15 headless assertions, --check all 4-artifact zero drift, frozen set intact)
