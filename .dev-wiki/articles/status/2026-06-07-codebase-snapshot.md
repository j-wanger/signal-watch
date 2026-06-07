---
title: "Codebase Snapshot — 2026-06-07 (Phase 24 cross-corpus synthesis)"
aliases: []
category: status
tags: [snapshot, corpus, synthesis, typology, multi-source]
created: 2026-06-07
updated: 2026-06-07
source: debrief
---

# Codebase Snapshot — 2026-06-07

Taken at the close of **Phase 24 (cross-corpus synthesis)** — READY FOR COMPLETION pending commit.

## Corpus
- **42 derived live across 46 publications, 4 sources, 2 jurisdictions.**
  - FinCEN advisories: 14 md / 12 derived (2 FATF non-derivable) — US, 17 U.S.C. §105
  - FinCEN alerts: 19 md / 17 derived (2 non-derivable) — US, 17 U.S.C. §105
  - OFAC: 3 md / 3 derived — US Treasury, 17 U.S.C. §105
  - FINTRAC: 10 md / 10 derived — Canada, Crown-copyright non-commercial licence
- **NEW: `data/typology-map.json`** — cross-corpus typology overlay (22-term closed vocab + 42-entry
  doc-id→typology map; jurisdiction derived from the source registry, not stored). Validated fail-loud
  at the build boundary (`load_typology_map` / `validate_typology`).
- Clusters: **5 cross-jurisdiction** (terrorist-financing 5 docs US+CA, synthetic-opioids,
  human-trafficking, professional-money-laundering, romance-and-investment-fraud) + 2 cross-agency US
  (sanctions-evasion 7, public-benefits-fraud 3) + 11 honest singletons (5 Canada-specific).

## Structure / Module Sizes
- `scripts/build.py` — 596 lines (stdlib; config + corpus boundary validation, CORPUS_SOURCES registry,
  Phase-24 typology gate + jurisdiction merge).
- `scripts/derive_signals.py` — 805 lines (authoring-only, stdlib; the inverted-loop grounding gate —
  BYTE-FROZEN this phase).
- `corpus.html` + `dist/corpus/index.html` — the corpus explorer; built ship file **636,848 B**
  (Phase-24 synthesis view + Documents/Typologies toggle).
- `index.html` + `config/typologies/*.json` — the six-act showcase (3 typologies); BYTE-FROZEN.

## Dependencies
- Ship artifact: zero build/runtime deps (single-file, offline, no fetch). Google Fonts via `<link>`,
  degrades to system fonts.
- Authoring-only: `markitdown[pdf]` (MIT, convert only) in a gitignored uv `.venv`. `anthropic` GONE
  since Phase 17.

## Test / Verification Status
- `python3 scripts/build.py --check all` → 4/4 ZERO DRIFT.
- `node tests/corpus-explorer.test.mjs` → **98 passed, 0 failed** (Phase-24: +24 synthesis assertions).
- `python3 scripts/derive_signals.py --selftest` → PASS (grounding core unchanged).
- All 42 derived records `--check-derived` clean.

## Recent Commits (last 5)
- bfc183e Phase 23 hotfix: stage the FINTRAC corpus-status.json regen (3→10)
- e2507e1 Phase 23: seed FINTRAC product-types + inverted-heading cross-phase fact to working-knowledge
- f13fbaf Phase 23: mark delivery accepted + phase complete (gate)
- b0fcda4 Phase 23: FINTRAC depth — source #4 grown 3→10 (OAs + real-estate Brief), inverted-anchor widening
- 7f6bc22 Phase 22: mark delivery accepted + phase complete (gate)

(Phase 24 implementation + this debrief are uncommitted at snapshot time — working tree carries
`data/typology-map.json`, `scripts/build.py`, `corpus.html`, `dist/corpus/index.html`,
`tests/corpus-explorer.test.mjs`, `CLAUDE.md`, `README.md` + the dev-wiki refresh.)
