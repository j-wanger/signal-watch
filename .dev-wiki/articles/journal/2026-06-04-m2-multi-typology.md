---
title: "2026-06-04 · M2 multi-typology (TBML)"
category: journal
date: 2026-06-04
phase: phase-03-multi-typology
tags: [milestone-m2, typology, tbml]
---

# M2 — multi-typology

## What shipped
Added a second typology (Trade-based ML) as config only, proving the engine is typology-agnostic.
- `config/typologies/trade-based.json` — TBML content authored from a read-only aml-wiki survey;
  paraphrased public advisories (FinCEN Apr-2025 fentanyl↔TBML, FATF 2024); price-anomaly target
  signal `S-PRICE-ANOMALY-TRADE`; lift = price × related-party × high-risk-corridor (22→81%).
- `scripts/build.py` — now outputs `dist/<id>/index.html` (coexisting typologies), validates each
  config against the schema at the build boundary (fails loud), adds an `all` mode, removes the
  stale single-file layout.
- `config/schema.md`, `README.md`, `CLAUDE.md` refreshed.
- `index.html` **unchanged**.

## Decisions
- **Typology = TBML** (not pig-butchering): richest aml-wiki coverage, dated paraphrasable
  advisories, signals that map to bank data, and it flows narratively from the fentanyl anchor.
- **Switch = build-time** (`dist/<id>/`), not a runtime selector — aligns scripted-first reliability
  and the minimal ethos.
- **Validate at the build boundary** (deterministic validator in build.py) over runtime-only checks.

## Verification
- TBML: 7 acts render, both gates, lift; target-derived signal; self-contained; CONFIG deep-equals.
- **Engine untouched**: `git diff index.html` empty since the M1 commit — "add a typology = 1 JSON file" proven.
- Fentanyl regression: dist byte-identical to the archived baseline.
- Validator rejects malformed configs (missing/duplicate/non-buildable target, bad enums, lengths).

## Escape hatches
- **DISCOVERY** — schema *doc* claimed `hints[7]`; the baseline carries 8 (trailing unused). The new
  build-boundary validator caught it. Fixed the constraint (`steps==7`, `next_labels`/`hints ≥7`)
  and the doc; configs/engine unchanged.

## Health delta
New file: `config/typologies/trade-based.json`. build.py gained a `validate_config` boundary check.
dist layout changed to per-typology. No deps added.

## Soft Observations / Phase N+1 Candidates
- `tests/smoke-checklist.md` is fentanyl-specific (hardcoded 45%, signal name). M3/M5 should make it
  typology-parameterized (or generate per-typology from config).
- The schema generalized with zero engine edits across a structurally different typology — strong
  evidence the M1 content model is sound. A 3rd typology (pig-butchering) would be cheap if wanted.
- M3 keyboard nav must keep both gates intact (can't advance Act 3 with zero selected; Act 4 confirm).
