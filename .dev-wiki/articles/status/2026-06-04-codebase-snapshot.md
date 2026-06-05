---
title: "2026-06-04 · Codebase snapshot"
aliases: []
category: status
tags: [snapshot, m6, signal-watch]
parents: [phase-07-pipeline-walking-skeleton]
created: 2026-06-04
updated: 2026-06-04
source: dev-debrief
---

# 2026-06-04 · Codebase snapshot (post-M6, pre-commit)

Taken at the M6 debrief, before the delivery commit. Reflects the "Signal Watch" ingestion-pipeline
slice in the working tree (uncommitted).

## Metrics

| Metric | Value |
|--------|-------|
| Typology configs | 3 (`fentanyl`, `trade-based`, `elder-financial-exploitation`) |
| Built dist | 3 (`dist/<typology>/index.html`, self-contained) |
| Authoring scripts | 3 (`build.py`, `acquire_fincen.py`, `pdf_to_md.py`) |
| Corpus | 1 advisory: `data/fincen/fin-2022-a002.md` (48KB verbatim) + `raw/*.pdf` (824KB) |
| Ship runtime deps | 0 (single-file, offline, no fetch) |
| Authoring deps | markitdown[pdf] (MIT) in gitignored uv `.venv` |
| Tests | none (deliberate project decision — verification = build validator + manual smoke-checklist) |

## Module Structure

Generic engine `index.html` (`__CONFIG__` injection) ← per-typology `config/typologies/*.json`
(validated against `config/schema.md`) → `scripts/build.py` inlines + resolves `text_file` →
`dist/<id>/index.html`. Authoring-only ingestion (`acquire_fincen.py` → `pdf_to_md.py`) persists
`data/fincen/<advisory-id>.md` as the verbatim source of truth. See `_ARCHITECTURE.md`.

## Build / Verify Status

- All 3 dist build clean; self-contained guard 0 tokens on all 3; `node --check` on inlined engine PASS.
- Compliance separation verified: "Illustrative data & outputs" badge distinct from the "public domain ·
  verbatim · FinCEN FIN-2022-A002" attribution.
- Live `file://` render = human sign-off at the delivery gate (Playwright deliberately skipped per
  M3/M5 precedent).

## Recent Commits (last 5)

- `93afeaf` Phase 6: Ship (M5) — parameterize smoke-checklist, refresh README, compliance/offline gate PASS
- `b3b3971` M3: presenter polish — keyboard nav, reset, prefers-reduced-motion (engine-only)
- `61a9cca` M2: add trade-based ML typology (config-only, zero engine edits)
- `99899ad` M1: config-driven refactor — generic engine + typology config + build
- `ae2c595` Wire project to registered aml-wiki knowledge base

(M6 work is uncommitted at snapshot time — delivery commit handled interactively by the orchestrator.)

## Related

- [[phase-07-pipeline-walking-skeleton|Phase 7: Pipeline walking skeleton (M6)]]
- [[2026-06-04-m6-pipeline-walking-skeleton|M6 journal]]
