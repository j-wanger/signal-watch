# Active Phase Context

Phase: 19 - Durability closeout — commit corpus-explorer test harness + pin _rf_triage (M7) — DELIVERED + accepted (2026-06-06); all 3 lite tasks [x]; impl commit ab0739a; exit criteria GREEN (harness 28/28, --selftest PASS, --check all 4-artifact zero drift, frozen set git-diff-empty). M0–M7 + the corpus-explorer arc + durability are all complete and the demo is at Definition of Done — run /dev-plan only for a net-new stakeholder ask (no remaining internal work without fabrication risk).
Objective: T1 (M) commit a ZERO-DEP Node DOM-shim harness that reads the committed `dist/corpus/index.html`, drives the 5-screen arc, and asserts the ~15 Ph18 invariants · T2 (S) PIN + DISCLOSE `_rf_triage` (a glued-fixture `--selftest` assertion + a one-line comment, NO output change) · T3 (S) wire the harness command into README + CLAUDE + smoke-checklist.

Scope (the ONLY unfreeze): `tests/**`, `scripts/derive_signals.py` (comment + selftest fixture ONLY — no output change), `README.md`, `CLAUDE.md`, `tests/smoke-checklist.md`. FROZEN byte-untouched: `index.html`, `corpus.html`, `scripts/build.py`, `config/**`, `data/fincen/**` (incl. corpus-status.json + derived/*.json), ALL of `dist/**` (the harness only READS dist/corpus/index.html).

Key constraints:
- ZERO runtime deps — hand-rolled Node DOM-shim, NEVER jsdom (file:// offline ethos + the dep-free `--selftest`/`--check` idiom). The harness loads the COMMITTED dist so it doubles as a build-output smoke test.
- The `_rf_triage` item is PIN + DISCLOSE, NOT a counting rewrite — an accurate glued counter would reintroduce the Phase-17-deleted parser (anti-subtraction); harmless today (12 live render from records; build.py ignores flag_count for live; the 2 FATF show count 0).
- NO behavioral change to any shipped artifact — corpus-status.json + dist/** stay byte-identical; `--check all` must still show zero drift + the frozen set git-diff-empty.

Exit criteria (all MET): `node tests/corpus-explorer.test.mjs` exits 0 (28 arc assertions, zero npm deps, no jsdom) · `derive_signals.py --selftest` gained the bidirectional glued `_rf_triage` pin + the "coarse hint, not authoritative for glued" docstring and passes · `build.py --check all` zero drift across 4 artifacts + frozen set git-diff-empty (corpus-status.json + dist/** byte-identical) · README + CLAUDE + smoke-checklist each name the harness command.
Abort: DEGRADE to a leaner assertion set (boot + each screen renders without throwing + the coverage-math unit, skipping event-driven toggles) if the DOM-shim can't drive the arc without a real DOM lib — NEVER pull jsdom into a file:// offline demo. Blocked >3 attempts on a task → ask the user: skip or abort.

Gates:
- [x] Direction confirmed by user (durability closeout over call-it-done / showcase-debt-true-up / new-stakeholder-ask; zero-dep Node DOM-shim; _rf_triage pin-not-rewrite — 2026-06-06)
- [x] Delivery accepted (post-implementation report 2026-06-06; impl commit ab0739a; 28/28 harness, --selftest PASS, --check all 4-artifact zero drift, frozen set git-diff-empty)
