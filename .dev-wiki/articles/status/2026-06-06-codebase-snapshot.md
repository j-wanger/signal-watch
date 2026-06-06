---
title: "Codebase Snapshot — 2026-06-06 (Phase 16: inverted extraction)"
aliases: [snapshot-phase-16]
category: status
tags: [snapshot, milestone-m7, derive-signals, corpus]
parents: [phase-16-invert-extraction]
created: 2026-06-06
updated: 2026-06-06
source: debrief
---

# Codebase Snapshot — 2026-06-06 (Phase 16)

Captured at the close of Phase 16 (invert extraction — LLM extracts, deterministic groundedness gate disposes;
DELIVERED, awaiting commit at the delivery gate).

## File Metrics

| Metric | Value |
|--------|-------|
| `scripts/derive_signals.py` | 1202 lines (Phase 15: 1063 → Phase 16: ~1189–1202; +the gate + normalizer + inversion docstrings, demoted extractor retained) |
| Derived records (`data/fincen/derived/*.json`) | 7 (fin-2020-a008, fin-2021-a002 NEW, fin-2021-a004 NEW, fin-2022-a001, fin-2024-a002, fin-2025-a002, fin-2025-a003) |
| FinCEN corpus md (`data/fincen/*.md`) | 14 (committed source of truth) |
| Corpus explorer live | 7/14 (was 5/14) |
| `dist/corpus/index.html` | ~110 KB (was ~95 KB) |
| Showcase artifacts | `index.html`, `corpus.html`, `config/**`, 3 typology dists — BYTE-FROZEN |

## Module Structure

Unchanged module set — Phase 16 is an authority shift WITHIN `scripts/derive_signals.py` (authoring layer);
no new modules, no new deps. See `_ARCHITECTURE.md` for the full layout. Key change: the extraction boundary
INVERTED — traceability authority moved from `src_line ∈ extract_red_flags(md)` (a structural parse) to
QUOTE-GROUNDING (`normalize(flag) ⊂ normalize(md)`) + a coarse `rf_region()` relevance guard + a
`_MIN_FLAG_NCHARS=24` floor. `extract_red_flags` DEMOTED to the EFE `--selftest` anchor + a triage hint.
`build.py` / `index.html` / `corpus.html` unchanged (`corpus-status.json` shape preserved).

## Dependencies

- Ship artifact: zero build/runtime deps (Google Fonts via `<link>`, degrades offline).
- Authoring-only (gitignored uv `.venv`, py3.12): `markitdown[pdf]` (MIT, convert), `anthropic` (SDK,
  `--draft` only, LAZY-imported). NEVER a ship dep; never imported by `index.html`/`build.py`.
- Deterministic layer stdlib-only. System python: 3.14.4 (authoring tools run on the uv py3.12 venv).

## Verification State

- `python3 scripts/derive_signals.py --selftest` → EFE 12+12 + grounding/normalizer/escrow/paraphrase/degenerate
  assertions PASS.
- All 7 derived records pass `--check-derived` under the new groundedness gate.
- `python3 scripts/build.py --check all` → 4-artifact ZERO DRIFT.
- Reviewer ACCEPT 9/10 (2 MEDIUM findings fixed inline).

## Recent Commits (pre-gate)

```
2a62903 Phase 15: mark delivery accepted + phase complete (gate)
62f7c1d Phase 15: Harden extraction faithfulness — footnote-resume + esc() sweep (M7)
410241f Phase 14: mark delivery accepted + phase complete (gate)
ce0de90 Phase 14: Scale corpus derivation — 3 more advisories → 5/14 live (M7)
39f672e Phase 13: mark delivery accepted + phase complete (gate)
```

(Phase 16 impl commit lands at the delivery gate.)
