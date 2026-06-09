---
title: "Codebase Snapshot 2026-06-09 (Phase 39 delivered)"
aliases: []
category: status
tags: [snapshot, news, live-mode, streaming, url-acquisition]
parents: [phase-39-live-news-qol]
created: 2026-06-09
updated: 2026-06-09
source: debrief
---

# Codebase Snapshot — 2026-06-09 (end of Phase 39, pre-commit)

## Ship artifacts (each single-file, offline)
- `dist/<id>/index.html` ×3 showcases (fentanyl, trade-based, elder-financial-exploitation) — frozen
- `dist/corpus/index.html` (~4.98MB) — 2,251 indicators / 56 derived / 62 publications / 5 sources, 4 lenses
- `dist/news/index.html` — M8 adverse-media stream; BYTE-IDENTICAL this phase (all Phase-39 client code inside the stripped live region)

## Module structure (key sizes)
- `scripts/build.py` 1003 · `derive_signals.py` 902 · `serve_news.py` 574 (NDJSON stage stream + {url}|{text} + verify_entities) · **`news_fetch.py` 345 (NEW — fetch ladder + standardizer + verifier)** · `news_store.py` 298 · `news_ground.py` 233
- Templates: `corpus.html` 1338 · `news.html` 829 (URL input + progress UI in the live region) · `index.html` 646
- Fixtures: `tests/fixtures/news-live/` (7 captured-Qwen replay articles) · **`tests/fixtures/news-fetch/` (NEW, 5: article.html/raw/golden + botguard + linkfarm)**

## Dependencies
- Ship path: zero (stdlib build, vanilla JS artifacts). `.venv` (gitignored, companion/authoring-only): markitdown[pdf] + duckdb 1.5.3. build.py never imports the live layer (serve_news/news_store/news_fetch).

## Test status (Phase-39 regate, all green)
- `node tests/news-stream.test.mjs` 90 (81→90) · `node tests/corpus-explorer.test.mjs` green
- `python3 tests/news_live_test.py` PASS (system + `.venv` + `--live` real-Qwen smoke); `news_fetch --selftest` NEW PASS dep-free
- `news_ground`/`serve_news`/`news_store`/`derive_signals` `--selftest` PASS · `build.py --check all` 5/5 ZERO DRIFT
- Live end-to-end measured: URL → 42.7s, 16 entities + 8 flags grounded, 0 dropped (treasury.gov jy2735)

## Recent commits (Phase-39 work commit pending the delivery gate)
- ae91516 docs: refresh README for live news subsystem; pin model endpoint to 127.0.0.1
- 0598f43 Phase 38 debrief: dev-wiki bookkeeping
- f27f99b Phase 38: flip delivery gate to accepted (post-commit verify)
- 7df3ce4 Phase 38: consolidate live news subsystem
- 5ac37d6 Phase 37: flip delivery gate to accepted (post-commit verify)

## Notes
- CLAUDE.md at 269 lines (> ~200 target; was 255) — the queued trim pass stands.
- Prior scan articles: none this cycle; see `2026-06-08-codebase-snapshot.md` for the Phase-38 baseline.
