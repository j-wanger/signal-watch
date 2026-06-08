---
title: "Phase 36: Persistence (DuckDB→parquet) + feedback watchlist (M8)"
aliases: []
category: journal
tags: [m8, news, live-mode, persistence, duckdb, parquet, watchlist, feedback-loop]
parents: [phase-36-persistence-watchlist]
created: 2026-06-08
updated: 2026-06-08
source: debrief
duration: long
---

# Phase 36: Persistence (DuckDB→parquet) + feedback watchlist (M8)

## What Happened
- Planned (dev-plan) then implemented Phase 36 in one session (lite, 5 tasks incl. one L = T3),
  DELIVERED → READY FOR COMPLETION (delivery gate handled by the delivery flow after commit). Wired
  the Phase-35 M8 news-stream live companion to a DuckDB persistence layer + an ESCALATED-ONLY
  feedback watchlist, all companion/venv-side with ZERO ship-path impact.
- The loop (escalated-only, REFINING D4's "book ∪ all prior-scanned"): a live scan → grounded record
  → the companion PERSISTS to DuckDB (disposition NULL); the Screen step scores each extracted entity
  against book ∪ watchlist(escalated); ESCALATE at the Disposition gate posts back → DuckDB marks
  `disposition='escalate'` → that entity joins the watchlist; a later article screens against the
  now-larger surface, a re-mentioned escalated entity hitting WITH provenance. This makes the existing
  human Disposition gate CONSEQUENTIAL — closing the "working instance of the loop, not a
  dramatization" arc Phase 35 named.
- **T1** `scripts/news_store.py` (NEW) — OWNS DuckDB: schema scans / entities(+disposition) /
  red_flags; `append_scan` / `set_disposition` / `watchlist_rows()` (escalated-only, reconciled to
  `{name,type,kind,provenance}`, book ∪ escalated) / `export_parquet` (native `COPY … (FORMAT
  parquet)`) / `reconcile_book`. DuckDB 1.5.3 installed into the existing gitignored uv `.venv`.
  build.py NEVER imports it (asserted in the success criteria). Writes serialized.
- **T2** `scripts/serve_news.py` wiring — persist each grounded record on `/extract` (store OPTIONAL:
  warn + disable if duckdb missing, still serve + `/extract`); `GET /watchlist` (book ∪ escalated +
  provenance); `POST /disposition {scan_id,entity_id,decision}`; a `--export-parquet <dir>` flag
  (+ `--no-persist` / `--db`); store lifecycle with graceful degradation.
- **T3 (L)** `news.html` live region — client overrides inside `/*LIVE_START*/…/*LIVE_END*/` only:
  `matchEntities` screens book ∪ watchlist, the Disposition gate gains an ESCALATE-any-entity action
  posting back + refetch, provenance shown. `render_news` STRIPS the region → dist/news byte-identical.
- **T4** tests — `tests/news_live_test.py` gained `/watchlist` + `/disposition` HTTP routes over a
  temp DuckDB store (DuckDB-gated, skips under system python); `tests/news-stream.test.mjs` gained an
  offline book-only strip assertion + an 8-assertion live-client behavioral block proving the
  book∪watchlist union-screen compounds and the escalate gate renders.
- **T5** docs + full regate + state refresh — `docs/news-live.md` (persistence + escalated-only
  watchlist + parquet + the venv duckdb install) + `tests/smoke-checklist.md` (live-persistence
  walkthrough) + CLAUDE.md `## Current state` edited IN PLACE per the maintenance contract (no
  per-phase bullet).
- ALSO this session, two between-phases corpus QOL polishes (committed separately, USER OVERRIDE on
  the otherwise-frozen corpus): `7e31dd8` (phrase-read pacing: 45s cap → 22s + dwell halved) and
  `7e7c0b8` (phrase reveal → ~1.5× the plain-text per-char rate, replacing the fixed dwell).
  corpus.html + dist/corpus only; corpus harness 235/0. The corpus FROZEN baseline moved twice.

## Decisions Made
- D1 (Phase 36 DIRECTION/SCOPE) — ESCALATED-ONLY feedback watchlist, REFINING D4's "book ∪ all
  prior-scanned" → book ∪ entities the analyst ESCALATES at the Disposition gate. A domain-honest
  CURATED watchlist (not noise); makes the human gate consequential. (Recorded in _CURRENT_STATE
  Recent Decisions at plan time; lite skips decision articles.)
- D2 (Phase 36 ARCHITECTURE) — new `scripts/news_store.py` OWNS DuckDB; build.py NEVER imports it.
  Companion-only `GET /watchlist` + `POST /disposition` + `--export-parquet`. All client wiring inside
  `/*LIVE_START*/…/*LIVE_END*/` → stripped → dist/news byte-identical. DuckDB .venv-only.
- D3 (Phase 36 HONESTY) — real fuzzy scores / synthetic book / always-on badge / nothing ungrounded
  carry forward; escalation provenance shown; escalation may target ANY extracted entity (proactive
  watchlisting), not only book-matches — load-bearing for the compounding loop.

## Problems Solved
- Byte-identical offline dist after a feature add — same strip discipline as Phase 35: all store/
  network client code confined to the `/*LIVE_START*/…/*LIVE_END*/` region, `render_news` removes it,
  `--check news` zero drift held.
- DuckDB confined to the venv (1.5.3) without touching the ship path — build.py import-guarded.

## Open Questions
- None unresolved.

## Artifacts Changed
- `scripts/news_store.py` (NEW — DuckDB store + escalated-only watchlist; companion-only)
- `scripts/serve_news.py` (GET /watchlist, POST /disposition, --export-parquet/--no-persist/--db, store lifecycle)
- `news.html` (live-region client overrides; build-time stripped → dist/news byte-identical)
- `dist/news/index.html` (rebuilt — byte-identical via the strip)
- `tests/news_live_test.py` (/watchlist + /disposition HTTP routes, DuckDB-gated)
- `tests/news-stream.test.mjs` (offline book-only strip assertion + live-client behavioral block)
- `docs/news-live.md`, `tests/smoke-checklist.md`, `CLAUDE.md` (in-place Current state), `.claude/rules/active-phase.md`
- `.gitignore` (data/news/.live/ + *.duckdb + *.parquet)
- `corpus.html` + `dist/corpus/index.html` (two QOL pacing commits 7e31dd8, 7e7c0b8)

## Related
- [[phase-36-persistence-watchlist|Phase 36: Persistence (DuckDB→parquet) + feedback watchlist]]
- [[2026-06-08-phase-35-news-live-backend|Phase 35: News live local-model backend]] — parent backbone

## Soft Observations / Phase 37 Candidates
- The real model call (`serve_news.call_llm` vs a live llama-cpp server) is still STUBBED/UNVERIFIED —
  client+server logic, grounding, and persistence are all tested, but first-run-against-a-real-model
  smoke is the user's (carried from Phase 35; the grounding gate is the backstop). | Phase 37: a
  real-model smoke harness or a recorded-fixture integration test. | evidence: this journal + Phase-35.
- No UI to VIEW / manage / PRUNE the accumulated watchlist (it only grows). | Phase 37: a
  watchlist-management view.
- Committed (seed) articles aren't persisted or escalatable — only live scans are. | Persisting/
  seeding the committed articles could demonstrate the compounding loop without a live model running.
- The corpus phrase-render pacing has now been tuned by feel three times (45s → 22s → 1.5×-rate). |
  A presenter-facing speed control (slider) could remove the guess-and-tune loop. (Soft.)

## Health Delta
- News harness 67 → 76 (+9: an offline book-only strip assertion + an 8-assertion live-client
  behavioral block). New test surface: `.venv/bin/python scripts/news_store.py --selftest`
  (append → escalate → watchlist union → parquet roundtrip) and news_live_test.py /watchlist +
  /disposition HTTP routes over a temp DuckDB store (DuckDB-gated, skips under system python).
  DuckDB 1.5.3 venv dep added.
- Regate green: `--check all` 5/5 zero drift; corpus 235/0; news 76/0; derive `--selftest` PASS;
  serve_news / news_ground / news_store selftests PASS.
- No type-checker/linter section in _ARCHITECTURE (node/python dep-free harnesses + python build);
  no lint/type deltas.
