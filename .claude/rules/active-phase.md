# Active Phase Context

Phase: 13 - Corpus explorer (advisory-selection front-end + per-indicator build-rec render) — M7 — DELIVERED, READY FOR COMPLETION
(all 5 tasks [x], exit criteria MET; impl commit 54516d4, 2026-06-05; post-review esc() fix uncommitted in tree). No next phase planned — run /dev-plan.
Objective: render the Phase-12 derived records as a NEW standalone ship artifact dist/corpus/index.html (from corpus.html) — a FinCEN CORPUS
EXPLORER, staged 4-screen flow: SELECT (14, honest status, 2 derived live) → COVERAGE (gauge) → BUILD RECOMMENDATIONS (cover×data→build_rec matrix, BUILD_NOW-first, src_line-traceable) → SIGNAL SPEC (BUILD_NOW cards).

Scope: corpus.html (NEW), scripts/build.py, scripts/derive_signals.py, data/fincen/corpus-status.json (NEW), dist/corpus/index.html (NEW), README.md, CLAUDE.md.
UNTOUCHED (byte-frozen): index.html, config/**, dist/{fentanyl,trade-based,elder-financial-exploitation}/.

Delivered (verified in tree): corpus.html (own theme CSS + __CORPUS__ + staged render JS, reduced-motion/keyboard parity, illustrative badge, defensive render);
--corpus-status → committed corpus-status.json (14 + 7c/3l/4n summary, stdlib-only, anthropic lazy); build.py render/build/check_corpus + validate_corpus_data
(build_rec ∈ enum; BUILD_NOW ⇒ full build_logic) + "corpus" target, folded into all/--check all (4 artifacts), NOT importing derive_signals.py; dist/corpus built + verified
(17 headless assertions + 3 screenshots). index.html + config/** + 3 typology dists byte-untouched; --check all zero drift; --selftest 12+12. Review 9/10 ACCEPT (1 MEDIUM esc() fix folded in).

Follow-ups (Phase 14): scale derivation to ~5 remaining CLEAN advisories; glued-list splitting for 3 LOW; exclude/label 2 FATF advisories; (carried) elder true-up · fentanyl re-point · --fetch cadence. Abort (if reopened): if the derived shape needs an engine edit to render — re-implement standalone in corpus.html, don't touch index.html.

Gates:
- [x] Direction confirmed by user (standalone artifact + staged 4-screen flow + all-14 honest status — 2026-06-05)
- [x] Delivery accepted (post-implementation report 2026-06-05; impl commit 54516d4, review 9/10 ACCEPT)
