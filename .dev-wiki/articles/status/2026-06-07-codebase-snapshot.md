---
title: "Codebase Snapshot — 2026-06-07 (Phase 28 corpus completeness + grounded coverage)"
aliases: []
category: status
tags: [snapshot, corpus, completeness, grounded-coverage, taxonomy, streaming-render, multi-source]
created: 2026-06-07
updated: 2026-06-07
source: debrief
---

# Codebase Snapshot — 2026-06-07

Taken at the close of **Phase 28 (corpus completeness + grounded-coverage interview + streaming render)** —
COMPLETE + accepted + committed `24e4a08`. (Supersedes the same-day Phase-24 snapshot; Phases 25–28 of corpus
output-quality work landed since.)

## Corpus
- **42 derived live across 46 publications, 4 sources, 2 jurisdictions; 875 indicators** (Phase 28
  re-extracted 634→903 for completeness, then deduped →875).
  - FinCEN advisories: 14 md / 12 derived (2 FATF non-derivable) — US, 17 U.S.C. §105
  - FinCEN alerts: 19 md / 17 derived (2 non-derivable) — US, 17 U.S.C. §105
  - OFAC: 3 md / 3 derived — US Treasury, 17 U.S.C. §105
  - FINTRAC: 10 md / 10 derived — Canada, Crown-copyright non-commercial licence (attribution now in a
    per-doc page FOOTER, not the on-screen label)
- **Per-indicator data model (Phase 28 NEW fields):** every indicator carries `capability` (1 of 28) +
  `data_source` (1 of 20) from the user-approved taxonomy; coverage status/data/build_rec are GROUNDED in
  the user's 28+20 y/n/partial interview (NOT fabricated) — 258 covered / 191 partial / 454 gap; 220
  BUILD_NOW · 147 SOURCE_DATA. BUILD_NOW carry `build_logic` from 28 capability spec-templates.
- Each indicator also carries the grounded verbatim `flag` (the evidence) + a register `red_flag`
  translation (Phase 25/26 two-layer model).
- `data/typology-map.json` — cross-corpus typology overlay (22-term closed vocab + 42-entry
  doc-id→typology map; jurisdiction derived from the source registry). Validated fail-loud at the build
  boundary (`load_typology_map` / `validate_typology`).

## Structure / Module Sizes
- `scripts/build.py` — **654 lines** (stdlib; config + corpus boundary validation, CORPUS_SOURCES registry,
  typology gate + jurisdiction merge, `_inline_article`/`_strip_provenance`, Phase-28 `attribution`/`url`
  projection + `import re` + "AML Corpus Explorer" brand subtitle).
- `scripts/derive_signals.py` — **844 lines** (authoring-only, stdlib; the inverted-loop grounding gate —
  `normalize`/`rf_region`/`check_record` BYTE-FROZEN since before Phase 25; all 903→875 flags re-ground
  through it unchanged).
- `corpus.html` + `dist/corpus/index.html` — the corpus explorer; built ship file **2,416,194 B (~2.40MB)**
  (Phase-28 streaming `renderArticle` + char-position `highlightArticle` + `cleanArticle` de-pipe +
  `#attribution` per-doc footer + branding).
- `index.html` + `config/typologies/*.json` — the six-act showcase (3 typologies); BYTE-FROZEN.

## Dependencies
- Ship artifact: zero build/runtime deps (single-file, offline, no fetch). Google Fonts via `<link>`,
  degrades to system fonts.
- Authoring-only: `markitdown[pdf]` (MIT, convert only) in a gitignored uv `.venv`. `anthropic` GONE since
  Phase 17.

## Test / Verification Status
- `python3 scripts/build.py --check all` → **4/4 ZERO DRIFT**.
- `node tests/corpus-explorer.test.mjs` → **165 passed, 0 failed** (Phase-28: +17 incl. the first
  full-motion streaming coverage via `__drain` + enriched dynEl).
- `python3 scripts/derive_signals.py --selftest` → PASS (grounding core byte-unchanged).
- All 42 derived records `--check-derived` clean.

## Recent Commits (last 5)
- 24e4a08 Phase 28: corpus completeness + grounded coverage + streaming read (875 indicators)
- 60737c4 Phase 27: make the corpus demo shippable — assess → presentation fixes → faithfulness-guarded re-extraction
- 20e1601 Phase 26: Elevate the corpus demo to showcase quality — debrief + delivery gate accepted
- 337b8aa Phase 26 T4–T6: combination-lift + build-log wow beats, story landing, harness + docs
- 83be590 Phase 26 T3: progressive article render + Select source-grouping + red-flag section-grouping

## Frozen byte-clean this phase
The showcase (index.html + config/** + the 3 typology dists), every source md, every corpus-status.json,
`data/typology-map.json`, and the grounding core `scripts/derive_signals.py` (gate logic UNCHANGED — the
re-extraction only changed flag/field VALUES). NO non-negotiable change (the FINTRAC attribution was
RELOCATED to a per-doc footer, not removed — the verbatim+attribution rail HELD).
