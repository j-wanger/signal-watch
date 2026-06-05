---
title: "Codebase Snapshot 2026-06-05"
category: status
tags: [snapshot, phase-09, build-drift-guard]
created: 2026-06-05
updated: 2026-06-05
source: debrief
---

# Codebase Snapshot — 2026-06-05 (Phase 9: build-drift guard)

## Metrics

- Engine: `index.html` 646 lines (untouched this phase — `git diff index.html` empty).
- Build: `scripts/build.py` 307 lines (Phase 9: `render_one`/`check_one`/`resolve_targets`
  refactor + `--check` drift-guard mode; pure-stdlib).
- Typology configs: 3 (`fentanyl`, `trade-based`, `elder-financial-exploitation`).
- Source corpus: `data/fincen/fin-2022-a002.md` (verbatim EFE advisory, source of truth).
- Built ship files: 3 × `dist/<typology>/index.html` (self-contained, offline).

## Module Structure

Generic engine template + `__CONFIG__` injection point (index.html); build/validate/inline +
drift guard (scripts/build.py); authoring-only ingestion (acquire_fincen.py, pdf_to_md.py).
See `_ARCHITECTURE.md` for the full layout + the M6 authoring pipeline (acquire→convert→derive→build).

## Dependencies

- Ship artifact: zero build/runtime deps (Google Fonts via `<link>`, degrades offline).
- Authoring-only: markitdown[pdf] (MIT) in a gitignored uv-managed py3.12 `.venv`.

## Verification Status

- No automated test framework (demo project; `tests/smoke-checklist.md` is the rehearsal gate).
- New capability: `python3 scripts/build.py --check all` — drift guard, exit 0 on clean HEAD
  (verified this session; all 3 typologies report zero drift), non-zero naming the typology on
  un-rebuilt drift.
- Build byte-DETERMINISTIC (built twice → identical sha); `node --check` (v22.22.2) PASS ×3 on
  freshly built dist; `git diff index.html` empty; all 3 `dist/` byte-identical (no config edits).

## Recent Commits

- a4594bd Phase 8 debrief: capture session + mark phase complete
- 042d732 Phase 8: Doc true-up + provenance fix (M6 debt)
- 8459dd9 Phase 7: Pipeline walking skeleton (M6)
- 93afeaf Phase 6: Ship (M5)
- b3b3971 M3: presenter polish

(Phase 9 not yet committed — READY FOR COMPLETION, awaiting delivery gate.)
