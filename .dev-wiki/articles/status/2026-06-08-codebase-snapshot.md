---
title: "Codebase Snapshot — 2026-06-08 (Phase 30 data-source lens)"
aliases: []
category: status
tags: [snapshot, corpus, data-source-lens, capability-lens, taxonomy, re-projection, multi-source]
created: 2026-06-08
updated: 2026-06-08
source: debrief
---

# Codebase Snapshot — 2026-06-08

Taken at the close of **Phase 30 (data-source lens)** — DELIVERED → READY FOR COMPLETION (delivery gate
pending the user's eyeball-and-accept). The symmetric counterpart to the Phase-29 capability lens, on the
D1–D20 data-source axis; the TIGHTEST phase in the series (a pure `corpus.html` re-projection — build.py,
the taxonomy, and all 42 derived records BYTE-FROZEN). Supersedes the Phase-28 snapshot.

## Corpus
- **42 derived live across 46 publications, 4 sources, 2 jurisdictions; 875 indicators** (unchanged since
  Phase 28; no re-derivation this phase).
  - FinCEN advisories: 14 md / 12 derived (2 FATF non-derivable) — US, 17 U.S.C. §105
  - FinCEN alerts: 19 md / 17 derived (2 non-derivable) — US, 17 U.S.C. §105
  - OFAC: 3 md / 3 derived — US Treasury, 17 U.S.C. §105
  - FINTRAC: 10 md / 10 derived — Canada, Crown-copyright non-commercial licence (attribution in a per-doc
    page FOOTER, not the on-screen label)
- **Per-indicator data model:** every indicator carries `capability` (1 of 28) + `data_source` (1 of 20)
  from the user-approved taxonomy; coverage status/data/build_rec GROUNDED in the user's 28+20 y/n/partial
  interview (258 covered / 191 partial / 454 gap; 220 BUILD_NOW · 147 SOURCE_DATA). Plus the grounded
  verbatim `flag` (evidence) + a register `red_flag` translation (Phase 25/26 two-layer model).
- **Two committed overlays, both validated fail-loud at the build boundary:**
  - `data/typology-map.json` — cross-corpus typology overlay (Phase 24; 22-term vocab + 42-entry map).
  - `data/capability-taxonomy.json` — the C1–C28 capability + D1–D20 data-source taxonomy (Phase 29;
    code → {name, desc, group, posture}; data_sources posture 9 y / 4 partial / 7 n). Surfaces BOTH lenses
    now: Phase 29 the capability (C) axis, Phase 30 the data-source (D) axis.

## Structure / Module Sizes
- `scripts/build.py` — **654 lines** (stdlib; config + corpus boundary validation, CORPUS_SOURCES registry,
  typology + capability-taxonomy gates, `_inline_article`/`_strip_provenance`, attribution/url projection).
  BYTE-FROZEN this phase.
- `scripts/derive_signals.py` — **844 lines** (authoring-only, stdlib; the inverted-loop grounding gate —
  `normalize`/`rf_region`/`check_record`). BYTE-FROZEN.
- `corpus.html` — **1,307 lines** (the corpus explorer; Phase 30 added the 4th Select mode + `dsAgg`/
  `indsForDS`/`dsCard`/`renderDataSource`/`enterDataSource` + `currentDataSource`/`fromDataSource`, +130/−14).
- `dist/corpus/index.html` — the built ship file, **2,457,938 B (~2.46MB)**.
- `index.html` + `config/typologies/*.json` — the six-act showcase (3 typologies); BYTE-FROZEN.

## Dependencies
- Ship artifact: zero build/runtime deps (single-file, offline, no fetch). Google Fonts via `<link>`,
  degrades to system fonts.
- Authoring-only: `markitdown[pdf]` (MIT, convert only) in a gitignored uv `.venv`. `anthropic` GONE since
  Phase 17.

## Test / Verification Status
- `python3 scripts/build.py --check all` → **4/4 ZERO DRIFT** (build verified deterministic — 5 runs +
  seed-0, md5 stable).
- `node tests/corpus-explorer.test.mjs` → **217 passed, 0 failed** (Phase-30: +27 data-source-lens asserts,
  190 → 217).
- `python3 scripts/derive_signals.py --selftest` → PASS (grounding core byte-unchanged).
- All 42 derived records `--check-derived` clean.

## Recent Commits (last 5)
- 029f33c Phase 29: capability lens — surface the C1–C28 / D1–D20 taxonomy as an institution coverage-by-capability view
- cc8948c dev-wiki: Phase 28 debrief — lifecycle capture (delivery accepted)
- 24e4a08 Phase 28: corpus completeness + grounded coverage + streaming read (875 indicators)
- 60737c4 Phase 27: make the corpus demo shippable — assess → presentation fixes → faithfulness-guarded re-extraction
- 20e1601 Phase 26: Elevate the corpus demo to showcase quality — debrief + delivery gate accepted

## Frozen byte-clean this phase
The showcase (index.html + config/** + the 3 typology dists), every source md, every corpus-status.json,
`data/typology-map.json`, **`data/capability-taxonomy.json`**, **`scripts/build.py`**, the grounding core
`scripts/derive_signals.py`, AND all 42 derived `data/*/derived/*.json` records (the data_sources axis was
already inlined/validated in Phase 29 — NO data/build change). HANDOFF.md byte-clean (no compliance/
architecture change). NO non-negotiable change.
