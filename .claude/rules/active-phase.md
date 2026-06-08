# Active Phase Context

Phase: 36 — Persistence (DuckDB→parquet) + feedback watchlist (M8). DELIVERED → READY FOR COMPLETION (all 5 tasks [x]; exit criteria MET; `--check all` 5/5 zero drift; corpus 235/0; news 67→76; derive/news_ground/serve_news/news_store selftests PASS; frozen set byte-clean; dist/news byte-identical via the strip). Direction approved 2026-06-08. Delivery gate pending the commit (the delivery flow flips it after the commit verifiably lands). Next: after the commit, /dev-plan for Phase 37.

Objective: wire the Phase-35 M8 live companion to a DuckDB persistence layer + an ESCALATED-ONLY feedback watchlist, companion/venv-side, ZERO ship-path impact. A live scan persists to DuckDB (disposition NULL); Screen scores entities vs book ∪ watchlist(escalated); ESCALATE at the Disposition gate marks `disposition='escalate'` → joins the watchlist; a later article screens the now-larger surface (provenance shown) — making the human gate consequential.

Shipped: `scripts/news_store.py` (NEW — OWNS DuckDB; build.py NEVER imports it) · `scripts/serve_news.py` (`GET /watchlist` + `POST /disposition` + `--export-parquet`/`--no-persist`/`--db` + graceful degradation) · `news.html` live-region overrides (book∪watchlist matchEntities + escalate-any-entity gate + provenance), build-time STRIPPED → dist/news byte-identical · tests (DuckDB-gated HTTP routes + offline book-only strip assertion + live-client block) · docs + smoke-checklist + CLAUDE.md in-place. DuckDB 1.5.3 .venv-only; store + parquet gitignored.

Key constraints: DuckDB venv-only, NEVER on the ship path; all client store/network code inside `/*LIVE_START*/…/*LIVE_END*/`; escalated-only watchlist (not all-scanned); HONESTY invariants carry forward (real scores, synthetic book, always-on badge, nothing ungrounded, escalation provenance). CAVEAT: the real `call_llm` vs a live llama-cpp server is still STUBBED/UNVERIFIED — first-run smoke is the user's; the grounding gate is the backstop.

FROZEN byte-clean: the six-act showcase (index.html + config/** + the 3 typology dists), the ENTIRE corpus (corpus.html + dist/corpus — NEW baseline after the QOL commits 7e31dd8 + 7e7c0b8 — all source dirs + every derived record + both overlays), the grounding core derive_signals.py, and scripts/news_ground.py.

Exit criteria: a live scan persists; escalate adds to the watchlist; a later scan screens book ∪ escalated (provenance); parquet export works; DuckDB venv-only; dist/news byte-identical; `--check all` 5/5; both harnesses + all selftests green; NO non-negotiable change.

Abort rule: if DuckDB can't confine to the `.venv` → stdlib sqlite3 + (DuckDB-CLI or skip) for parquet (re-confirm the one-new-dep choice). If dist/news can't be byte-identical after the strip, surface it. Blocked >3 attempts on a task → mark [blocked] + ask: skip or abort.

Gates:
- [x] Direction confirmed by user (escalated-only feedback watchlist + DuckDB→parquet persistence, served-by-companion; approved 2026-06-08)
- [ ] Delivery accepted (post-implementation; the delivery flow flips this after the commit lands)
