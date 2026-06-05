---
title: "Codebase Snapshot 2026-06-05 (Phase 12)"
category: status
tags: [snapshot, phase-12, corpus-derivation, m7]
created: 2026-06-05
updated: 2026-06-05
source: debrief
---

# Codebase Snapshot — 2026-06-05 (Phase 12: FinCEN corpus derivation)

## Metrics

- Engine: `index.html` 646 lines (untouched this phase — `git diff index.html` empty).
- Build: `scripts/build.py` 307 lines + `config/schema.md` (untouched — backend-only phase).
- Authoring tools (stdlib, build-time only): `crawl_fincen.py`, `acquire_fincen.py`, `pdf_to_md.py`,
  **`derive_signals.py` 949 lines** (Phase 12: corpus-wide section-FINDER + `--corpus` + deterministic
  checks + derived-record scaffold/check; grew from 551).
- Typology configs: 3 ship typologies (`fentanyl`, `trade-based`, `elder-financial-exploitation`).
- FinCEN corpus: **14 advisory md committed** (`data/fincen/*.md`) + `index.json` manifest +
  **2 derived records** (`data/fincen/derived/fin-2022-a001.json`, `fin-2024-a002.json`).
- Built ship files: 3 × `dist/<typology>/index.html` (self-contained, offline).

## Module Structure

Generic engine + `__CONFIG__` injection (index.html); build/validate/inline + drift guard (build.py);
M6 authoring pipeline (crawl→acquire→convert→derive→build). Phase 12 added the **corpus-derivation
backend** in `derive_signals.py`: a DETERMINISTIC spine (`extract_red_flags` section-FINDER + `--corpus`
classification + `build_rec_category`/`check_record`) and an LLM-backend authoring path (`--scaffold-derived`
+ a model session OR `--draft` proposes; `--check-derived` disposes). The spine ASSISTS but does not
AUTOMATE — a complete derived record needs LLM-backend authoring; the two human gates dispose. Engine,
build.py, and config/schema.md untouched. See `_ARCHITECTURE.md`.

## Dependencies

- Ship artifact: zero build/runtime deps (Google Fonts via `<link>`, degrades offline).
- Authoring-only (gitignored uv `.venv`): markitdown[pdf] (convert); anthropic (SDK, `--draft` only,
  LAZY). The Phase-12 LLM-backend proof slice used a model SESSION (no key, no SDK call).

## Verification Status

- No automated test framework (demo project; `tests/smoke-checklist.md` is the rehearsal gate).
- `derive_signals.py --selftest` — EFE extraction 12+12 AND the deterministic checks (build-rec matrix,
  traceability, build_logic shape, dup-id) all asserted; exit 0 offline.
- `--corpus` across all 14: **7 CLEAN · 3 LOW · 4 NEEDS** (2 NEEDS = FATF jurisdiction advisories, correct).
- Both derived records pass `--check-derived`; boundary holds (a tampered record is rejected).
- `git diff index.html`/`build.py`/`schema.md` empty; `build.py --check all` zero drift; anthropic LAZY.
- Review gate 8/10 → revise; 1 HIGH + 2 MEDIUM disposer gaps fixed pre-commit.

## Recent Commits

- (Phase 12 commit pending — this snapshot is written at the delivery gate, pre-commit.)
- 7c76971 Phase 11: mark delivery accepted + phase complete (gate)
- c37dc39 Phase 11: Automated derivation (LLM-drafted signal config)
- 059792f gitignore the FinCEN corpus markdown mirror (keep derived md committed)
