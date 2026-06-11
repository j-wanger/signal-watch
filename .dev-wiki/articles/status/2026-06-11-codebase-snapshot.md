---
title: "Codebase snapshot 2026-06-11 (Phase 46 ready for completion — pre-delivery, presentation day)"
aliases: []
category: status
tags: [snapshot, phase-46, corpus, live-mode]
parents: [phase-46-corpus-live-derivation]
created: 2026-06-11
updated: 2026-06-11
source: debrief
---

# Codebase Snapshot — 2026-06-11

Taken at the Phase-46 debrief (4/4 [x], READY FOR COMPLETION; delivery gate pending; phase work
UNCOMMITTED in the working tree). Presentation day: dist/corpus byte-identical, presentation-safe.

## File Metrics
- Ship templates: corpus.html 1,660 lines (Phase-46 /*LIVE_*/ region added) · news.html 1,234 · index.html 646 (byte-frozen)
- scripts/build.py 1,042 (render_corpus strip extension, one line) · scripts/serve_corpus.py 685 (NEW, stdlib companion, port 8010) · scripts/serve_news.py 872
- CLAUDE.md 263 lines (vs ~200 target — carried trim candidate)
- Corpus: 60 derived records on disk (56 corpus + 4 news) · 2,251 indicators · 62 publications · 5 sources · 3 overlays

## Test Status (full regate at T4 — all green)
- `--check all` 5/5 zero drift (dist/corpus byte-identical THROUGH the live-region addition)
- corpus-explorer 303 (273→303, +30 live-strip/injection/processing-page) · news-stream 150
- derive_signals / serve_corpus (NEW) / serve_news / news_ground --selftest · news_quality_harness --check (17 fixtures within baseline) · news_live_test (system)

## Module Structure
- Unchanged from `_ARCHITECTURE.md` (refreshed this debrief) except: NEW `scripts/serve_corpus.py`
  (the SECOND live companion — imports the frozen derive_signals gate + build payload loaders;
  build.py does NOT import it), corpus.html live region (build-stripped), NEW `docs/corpus-live.md`.

## Recent Commits (pre-delivery — Phase 46 not yet committed)
- 5da6ec5 Booth draw-in loop (post-phase one-off)
- 7e9fa23 Phase 45: flip delivery gate to accepted (post-commit verify)
- 324734e Phase 45: corpus presentation polish (pre-presentation)
- 5c8c014 Phase 44: flip delivery gate to accepted (post-commit verify)
- 0835bff Phase 44: live extraction quality

## Dependencies
- Ship: none (offline single-file). Authoring/companion: markitdown[pdf] + duckdb in gitignored .venv; serve_corpus stdlib-only.
