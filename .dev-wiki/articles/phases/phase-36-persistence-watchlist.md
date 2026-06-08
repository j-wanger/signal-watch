---
title: "Phase 36: Persistence (DuckDB→parquet) + feedback watchlist"
aliases: []
category: phases
tags: [m8, news, live-mode, persistence, duckdb, parquet, watchlist, feedback-loop]
parents: []
created: 2026-06-08
updated: 2026-06-08
source: plan
status: active
scope: ["scripts/news_store.py", "scripts/serve_news.py", "news.html", "dist/news/index.html", "tests/news_live_test.py", "tests/news-stream.test.mjs", "docs/news-live.md", "tests/smoke-checklist.md", "CLAUDE.md", ".claude/rules/active-phase.md"]
entry_criteria: "Phase 35 DELIVERED + accepted + committed (4408dd9, pushed to main). The live-extraction backbone works: serve_news.py companion → call_llm → parse_llm_json → build_record → news_ground.ground_record (ungrounded drops). Phase 35 screens vs the STATIC book."
exit_criteria: "A live scan PERSISTS to DuckDB; escalating at the Disposition gate ADDS the entity to the watchlist; a subsequent scan screens against book ∪ escalated (provenance shown); parquet export works; DuckDB is venv-only and NEVER in the ship path; the offline dist/news byte-identical (--check news zero drift, live + store code stripped, zero network/store code, fallback intact); --check all 5/5 zero drift; --selftest PASS; both harnesses green; the frozen set byte-clean; NO non-negotiable change."
---

# Phase 36: Persistence (DuckDB→parquet) + feedback watchlist

## Objective

Wire the Phase-35 M8 news-stream live companion to a DuckDB persistence layer + a feedback
WATCHLIST, all companion/venv-side with ZERO ship-path impact. The loop is ESCALATED-ONLY (the
user's choice at the gate, REFINING D4's "book ∪ all prior-scanned"): a live scan → grounded record
→ the companion PERSISTS the scan to DuckDB (disposition NULL); the Screen step scores each extracted
entity against book ∪ watchlist(escalated); at the Disposition gate, ESCALATE posts back → DuckDB
marks `disposition='escalate'` → that entity joins the watchlist; a later article screens against the
now-larger surface (a re-mentioned escalated entity hits with provenance "escalated from <prior
article>, <date>"). This makes the existing human Disposition gate CONSEQUENTIAL — closing the
"working instance of the loop, not a dramatization" arc Phase 35 named.

## Scope

Files and modules affected:
- `scripts/news_store.py` (NEW) — OWNS DuckDB: schema scans / entities(+disposition) / red_flags;
  `append_scan` / `set_disposition` / `watchlist_rows()` (escalated-only, reconciled) /
  `export_parquet` (native `COPY … (FORMAT parquet)`). build.py NEVER imports it.
- `scripts/serve_news.py` — the companion: persist each grounded `/extract` record (store OPTIONAL);
  `GET /watchlist` (book ∪ escalated + provenance); `POST /disposition`; a `--export-parquet` flag
- `news.html` — the live branch (`/*LIVE_START*/…/*LIVE_END*/`): refetch the watchlist, screen
  against book ∪ escalated, escalate posts back, provenance shown; the offline build STRIPS the region
- `dist/news/index.html` — rebuilt, byte-identical via the strip
- `tests/news_live_test.py`, `tests/news-stream.test.mjs` — store/union/parquet coverage + an offline
  book-only assertion
- `docs/news-live.md`, `tests/smoke-checklist.md`, `CLAUDE.md` (in-place `## Current state` edit),
  `.claude/rules/active-phase.md`

## Exit Criteria

- [ ] A live scan PERSISTS to DuckDB via row-append (the scan + entities[+disposition] + red_flags),
      survives restart
- [ ] Escalating at the Disposition gate marks `disposition='escalate'` → the entity JOINS the
      watchlist; a subsequent scan screens against book ∪ escalated and a re-mentioned escalated entity
      surfaces WITH provenance ("escalated from <article>, <date>")
- [ ] A parquet export is produced via native DuckDB `COPY … (FORMAT parquet)`
- [ ] DuckDB is venv-only and NEVER in the ship path (build.py doesn't import news_store; no store dep
      inlined); offline `dist/news/index.html` byte-identical (`--check news` zero drift, live + store
      code stripped, zero network/store code, fallback intact; static offline screening book-only)
- [ ] `--check all` 5/5 zero drift; `--selftest` PASS; both harnesses green; frozen set byte-clean;
      NO non-negotiable change

## Constraints

- DuckDB is the ONE new pip dep this phase — into the existing gitignored uv `.venv` (where
  markitdown lives), NEVER imported by build.py or inlined into any dist (prevents the ship artifact
  gaining a runtime/store dep — violates the self-contained, offline, no-fetch non-negotiable).
- `scripts/news_store.py` OWNS the store; build.py STILL never imports the authoring/LLM/store layer
  (the no-authoring/no-store-layer build-boundary invariant holds).
- All client store/network code lives inside the stripped `/*LIVE_START*/…/*LIVE_END*/` region →
  dist/news byte-identical, the self-contained `die("fetch(")` guard holds.
- ESCALATED-ONLY watchlist (not all-scanned) — a curated screen surface, not a dump of incidental
  names (prevents compounding noise that degrades screening precision).
- HONESTY: real client-side fuzzy scores; the book stays synthetic; prior-scanned watchlist entries
  are REAL grounded extractions; the always-on "Illustrative data & outputs" badge stays; escalation
  provenance shown in the screen/exposure view; escalation can target ANY extracted entity (proactive
  watchlisting), not only book-matches.
- Serialize writes (a lock / single-writer connection) — ThreadingHTTPServer `/extract` appends are
  concurrent against a single DuckDB file.

## Checkpoints

- After the store schema + append path (T1): the row shape + restart-survival + the watchlist-union
  reconciliation are exercised by `news_store.py --selftest` before the companion + UI wire to them.
- If DuckDB can't be confined to the `.venv` / leaks toward the ship path, or the offline dist can't
  stay byte-identical after the strip: STOP and surface it.

## Assumptions

- DuckDB installs cleanly into the existing gitignored uv `.venv` (py3.12). If false: fall back to
  stdlib `sqlite3` for the row-store + (DuckDB-CLI or skip) for parquet export — grounding/honesty
  unaffected; re-confirm the one-new-dep choice with the user.
- The Phase-35 `build_record` output shape is a stable row schema for the store. If false: add a thin
  row-projection rather than reshaping the grounded record.

## Notes

- Watchlist reconciliation: book rows `{role,country,segment}` and scanned entities
  `{location,age,profession,context}` both COLLAPSE to a uniform screening row
  `{name,type,kind:'book'|'scanned',provenance}` — `name` is what the 0.85 Jaro-Winkler matcher
  scores; `provenance` keeps the exposure view honest about WHY a hit fired.
- The store file + parquet exports are gitignored (the `data/*/raw/` convention).
- The companion DEGRADES gracefully if duckdb is missing (still serves the page + `/extract`;
  persistence disabled with a warning).
- KNOWLEDGE GAPS to verify at impl: DuckDB append + parquet-export idioms (check the DuckDB docs);
  ThreadingHTTPServer + a single DuckDB file under threaded `/extract` appends (serialize writes).
- Phase 35 hook points (verified): `serve_news.py` `do_POST /extract` → `extract()` →
  `build_record()` → `news_ground.ground_record()`; the grounded `record` (entities[] carrying
  `id/name/type/location/age/profession/context` + red_flags[]) is what gets appended.
- The screen surface today: `news.html` `matchEntities(a)` reads `NEWS.book.rows` (synthetic rows);
  the union watchlist is fetched LIVE (`GET /watchlist`) and merged in the live branch so the offline
  `news_payload`/`render_news` stays static-book-only and the strip keeps dist/news byte-identical.
