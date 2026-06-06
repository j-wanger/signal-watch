# Active Phase Context

Phase: 13 - Corpus explorer (advisory-selection front-end + per-indicator build-rec render) — M7 — ACTIVE (planned 2026-06-05)
Objective: The PAYOFF — render the Phase-12 derived records as a NEW standalone ship artifact `dist/corpus/index.html` (built from corpus.html): a FinCEN CORPUS EXPLORER, staged 4-screen flow SELECT (14, honest status, 2 derived live) → COVERAGE (gauge) → BUILD RECOMMENDATIONS (cover×data→build_rec matrix, BUILD_NOW-first, src_line-traceable) → SIGNAL SPEC (BUILD_NOW cards from build_logic).

Scope: corpus.html (NEW), scripts/build.py, scripts/derive_signals.py, data/fincen/corpus-status.json (NEW), dist/corpus/index.html (NEW), README.md, CLAUDE.md. UNTOUCHED: index.html, config/**, dist/{fentanyl,trade-based,elder-financial-exploitation}/.

Key constraints:
- NEW standalone artifact; showcase stays BYTE-FROZEN. corpus.html owns its own theme CSS (no shared include).
- Single self-contained file, offline — no fetch / ES module / external script. Honest data, no fabricated lift/stats; "Illustrative data & outputs" badge + reduced-motion + keyboard parity stay.
- build.py reads committed data (corpus-status.json + derived/*.json); MUST NOT import derive_signals.py.

Exit: dist/corpus self-contained offline 4-screen explorer · --corpus-status emits the 14-entry manifest · build.py corpus/--check corpus work + decoupled · git diff index.html empty + --check all zero drift · README+CLAUDE updated.
Abort: if the derived shape needs an engine edit to render — re-implement standalone in corpus.html, don't touch index.html.

Gates:
- [x] Direction confirmed by user (standalone corpus artifact + staged 4-screen flow + all-14 honest status — approved 2026-06-05)
- [ ] Delivery accepted (post-implementation report)
