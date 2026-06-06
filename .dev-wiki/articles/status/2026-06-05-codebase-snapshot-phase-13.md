---
title: "Codebase Snapshot 2026-06-05 (Phase 13)"
category: status
tags: [snapshot, phase-13, corpus-explorer, ship-artifact, m7]
created: 2026-06-05
updated: 2026-06-05
source: debrief
---

# Codebase Snapshot — 2026-06-05 (Phase 13: Corpus explorer)

## Metrics

- Engine: `index.html` (BYTE-FROZEN this phase — `git diff index.html` empty).
- **NEW standalone artifact:** `corpus.html` **470 lines** — own copy of the dossier theme CSS +
  `__CORPUS__` injection + staged 4-screen render JS (SELECT → COVERAGE → BUILD RECOMMENDATIONS → SIGNAL SPEC).
- Build: `scripts/build.py` **487 lines** (Phase 13: + render_corpus/build_corpus/check_corpus +
  validate_corpus_data boundary validator + "corpus" target; folded into all / --check all → 4 artifacts;
  does NOT import derive_signals.py).
- Authoring tools (stdlib, build-time only): `crawl_fincen.py`, `acquire_fincen.py`, `pdf_to_md.py`,
  **`derive_signals.py` 1040 lines** (Phase 13: + `--corpus-status` manifest emitter + shared
  `_section_counts` / `_load_index` helpers; grew from 949).
- Typology configs: 3 ship typologies (`fentanyl`, `trade-based`, `elder-financial-exploitation`) — byte-frozen.
- FinCEN corpus: 14 advisory md committed + `index.json` manifest + **`corpus-status.json`** (NEW, 14
  entries + 7-clean/3-low/4-needs summary) + **2 derived records** (`derived/fin-2022-a001.json`,
  `fin-2024-a002.json`).
- Built ship files: **4** — 3 × `dist/<typology>/index.html` (byte-frozen) + **`dist/corpus/index.html`** (NEW).

## Module Structure

Two independent single-file ship artifacts now: the six-act SHOWCASE engine (`index.html` + 3 typology
configs, byte-frozen) and the NEW CORPUS EXPLORER (`corpus.html` → `dist/corpus/index.html`). build.py gained
a decoupled corpus path that assembles `__CORPUS__` from committed data (`corpus-status.json` +
`derived/*.json`) and validates the renderable shape at its boundary — it never imports the authoring layer
(`derive_signals.py`). The corpus-status manifest is emitted by `derive_signals.py --corpus-status`. See
`_ARCHITECTURE.md`.

## Dependencies

- Ship artifacts: zero build/runtime deps (Google Fonts via `<link>`, degrades offline). Both `index.html`
  and `corpus.html` are self-contained, offline, no fetch / ES module.
- Authoring-only (gitignored uv `.venv`): markitdown[pdf] (convert); anthropic (SDK, `--draft` only, LAZY).

## Verification Status

- No automated test framework (demo project; `tests/smoke-checklist.md` is the rehearsal gate). New
  uncommitted /tmp harness: a headless DOM-shim render smoke test for corpus.html (17 assertions) + 3 browser screenshots.
- `derive_signals.py --selftest` — EFE 12+12 + deterministic checks all pass; exit 0 offline.
- `--corpus` across all 14: 7 CLEAN · 3 LOW · 4 NEEDS (matches corpus-status.json summary).
- Both derived records pass `--check-derived`.
- `build.py --check all` — **4 artifacts zero drift** (3 typologies + corpus); `git diff index.html` empty;
  `config/**` + the 3 typology dists byte-untouched; build.py does NOT import derive_signals.py.
- Review gate **9/10 ACCEPT** — one MEDIUM (esc() quote-escaping) fixed inline, rebuilt, re-verified.

## Recent Commits

- 54516d4 Phase 13: Corpus explorer — advisory selection + build-rec render (M7)  *(post-review esc() fix
  to corpus.html + dist/corpus uncommitted in the tree at snapshot time)*
- 348ba81 Phase 12: mark delivery accepted + phase complete (gate)
- 90939b4 Phase 12: FinCEN corpus derivation foundation (M7)
- 7c76971 Phase 11: mark delivery accepted + phase complete (gate)
- c37dc39 Phase 11: Automated derivation (LLM-drafted signal config)
