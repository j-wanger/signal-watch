---
title: "Codebase Snapshot 2026-06-10 (Phase 41 ready for completion)"
aliases: []
category: status
tags: [snapshot, news, live-mode, entity-resolution, duckdb]
parents: [phase-41-entity-resolution-schema]
created: 2026-06-10
updated: 2026-06-10
source: debrief
---

# Codebase Snapshot — 2026-06-10 (end of Phase 41, pre-commit)

## Ship artifacts (each single-file, offline)
- `dist/<id>/index.html` ×3 showcases (fentanyl, trade-based, elder-financial-exploitation) — frozen
- `dist/corpus/index.html` (~4.98MB) — 2,251 indicators / 56 derived / 62 publications / 5 sources, 4 lenses — frozen
- `dist/news/index.html` — M8 adverse-media stream; BYTE-IDENTICAL this phase (all Phase-41 enrichment renders companion-live only, inside the stripped live region)

## Module structure (key sizes)
- `scripts/build.py` 1037 · `serve_news.py` 721 (EXTRACT_SCHEMA/SYSTEM_PROMPT from vocab constants; red_flags FIRST in schema order — load-bearing under strict grammar) · `news_ground.py` 504 (closed-vocab single authorities + alias-fold inversion + reconcile_refs + relationship/property grounding) · `news_store.py` 502 (ANCHOR design: anchors / monolithic entity_properties / entity_relationships + scans.source_type; additive legacy migration) · `news_fetch.py` 345
- Templates: `corpus.html` 1338 · `news.html` 897 (source-type selector + SUBJECT MAP + identity cards in the live region) · `index.html` 646
- Fixtures: `tests/fixtures/news-live/` 29 files — 13 replay pairs (7 original + 3 `.ph40` + **3 NEW `.ph41` US-federal capture/golden pairs**) + 3 promoted stress articles; FIXTURE_META privacy allowlist asserted in replay

## Dependencies
- Ship path: zero (stdlib build, vanilla JS artifacts). `.venv` (gitignored, companion/authoring-only): markitdown[pdf] + duckdb 1.5.3. build.py never imports the live/store layer (it DOES import news_ground by design — the shared gate).

## Test status (Phase-41 regate, all green)
- `node tests/news-stream.test.mjs` **103** (90→103: alias-class matcher both-directions, subject-map/identity-card render, Phase-41 strip assertions) · `node tests/corpus-explorer.test.mjs` 239
- `python3 tests/news_live_test.py` PASS (system + `.venv` watchlist loop + `--live` real-Qwen smoke RAN green; +canned41 loop + FIXTURE_META allowlist)
- `news_ground` (+Phase-41 grounding block) / `serve_news` / `news_store` (+anchor block) / `news_fetch` / `derive_signals` `--selftest` PASS · `build.py --check all` 5/5 ZERO DRIFT · pinned pre-41 captures byte-clean (`git diff --exit-code`)

## Recent commits (Phase-41 work commit pending the delivery gate)
- 760de35 Phase 40: flip delivery gate to accepted (post-commit verify)
- ea53adc Phase 40: live red-flag extraction quality — measure-first prompt checklist + shared-gate dup-collapse
- 3c35902 Phase 39: flip delivery gate to accepted (post-commit verify)
- 3786042 Phase 39: live news QOL — streamed extraction progress + one-shot URL acquisition
- ae91516 docs: refresh README for live news subsystem; pin model endpoint to 127.0.0.1

## Notes
- Phase 41 working tree is UNCOMMITTED at snapshot time (delivery gate pending). New untracked: `specs/phase-41-entity-resolution-schema.md`, `.dev-wiki/articles/decisions/`, 6 `.ph41` fixture files.
- Named seam: `news_store.anchor_summary` (accumulated identity w/ kept conflicts) has no route/UI consumer — Phase-42 candidate.
- CLAUDE.md at 305 lines (maintenance-contract target ~200) — trim increasingly due.
