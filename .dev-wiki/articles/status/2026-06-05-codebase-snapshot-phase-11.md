---
title: "Codebase Snapshot 2026-06-05 (Phase 11)"
category: status
tags: [snapshot, phase-11, automated-derivation]
created: 2026-06-05
updated: 2026-06-05
source: debrief
---

# Codebase Snapshot — 2026-06-05 (Phase 11: automated derivation)

## Metrics

- Engine: `index.html` 646 lines (untouched this phase — `git diff index.html` empty).
- Build: `scripts/build.py` 307 lines (untouched this phase — authoring tool never imports it).
- Authoring tools (stdlib, build-time only): `crawl_fincen.py` (discovery → manifest), `acquire_fincen.py`
  (resolve+download), `pdf_to_md.py` (markitdown PDF→md), **`derive_signals.py` 551 lines (NEW —
  Phase 11: deterministic `extract_red_flags`/`scaffold_config` + neural `--draft`)**.
- Typology configs: 3 (`fentanyl`, `trade-based`, `elder-financial-exploitation`).
- Source corpus: `data/fincen/fin-2022-a002.md` (verbatim EFE advisory) + `data/fincen/index.json`
  (14-advisory manifest).
- Built ship files: 3 × `dist/<typology>/index.html` (self-contained, offline).

## Module Structure

Generic engine template + `__CONFIG__` injection (index.html); build/validate/inline + drift guard
(build.py); M6 authoring pipeline (crawl→acquire→convert→**derive**→build), all build-time-only and
never imported by the engine. `derive_signals.py` adds the automated `derive` step: a DETERMINISTIC
layer (stdlib, offline) that extracts the FinCEN red flags + scaffolds a schema-shaped SKELETON, and a
NEURAL layer (`--draft`, env-keyed, lazy `anthropic`) that PROPOSES the judgment fields via the
Anthropic API. The LLM proposes a gitignored `.draft.json`; build.py + schema + 2 human gates DISPOSE.
See `_ARCHITECTURE.md` for the full layout.

## Dependencies

- Ship artifact: zero build/runtime deps (Google Fonts via `<link>`, degrades offline).
- Authoring-only (gitignored uv-managed py3.12 `.venv`): markitdown[pdf] (MIT) for convert;
  **anthropic (SDK) for `derive_signals.py --draft` ONLY, LAZY-imported, `ANTHROPIC_API_KEY` from env.**
  NEVER a ship dep — the ship artifact never calls an LLM.

## Verification Status

- No automated test framework (demo project; `tests/smoke-checklist.md` is the rehearsal gate).
- New capability: `python3 scripts/derive_signals.py --selftest` — deterministic stdlib parser check,
  exit 0 offline (extracts the 24 EFE red flags, 12 behavioral + 12 financial).
- Boundary verified: `build.py <id>.draft` REJECTS the bare skeleton naming the 2 judgment gaps;
  ACCEPTS a filled draft. `build.py --check all` zero drift on all 3 dist; `git diff index.html` empty.
- `--draft` static surface verified (lazy import, env-keyed, no `sk-ant`); the Anthropic
  structured-output shape verified vs the claude-api reference. Live network call unexercised (no key).

## Recent Commits

- (Phase 11 commit pending — this snapshot is written at the delivery gate, pre-commit.)
- 059792f gitignore the FinCEN corpus markdown mirror (keep derived md committed)
- 1b48f42 Phase 10: mark delivery accepted + phase complete (gate)
- 0c87c47 Phase 10: FinCEN corpus crawler (SCALE)
- 3c7895b Phase 9: mark delivery accepted + phase complete (gate)
- 33db22a Phase 9: Build-drift guard (M-hardening)
