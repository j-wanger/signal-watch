---
title: "Codebase Snapshot — 2026-06-06 (Phase 17: deleted extract_red_flags + scaled to 12/14)"
aliases: [snapshot-phase-17]
category: status
tags: [snapshot, milestone-m7, derive-signals, corpus, dead-code-deletion]
parents: [phase-17-complete-corpus-derivation]
created: 2026-06-06
updated: 2026-06-06
source: debrief
---

# Codebase Snapshot — 2026-06-06 (Phase 17)

Captured at the close of Phase 17 (delete extract_red_flags + the scaffold/draft authoring stack — the real
subtraction — and scale the corpus explorer to 12/14; DELIVERED, reviewer ACCEPT 9/10, awaiting commit at the
delivery gate). Supersedes the Phase-16 same-day snapshot.

## File Metrics

| Metric | Value |
|--------|-------|
| `scripts/derive_signals.py` | 600 lines (Phase 16: 1202 → Phase 17: 600, −602 / −50%; deleted extract_red_flags + the --scaffold/--draft/--scaffold-derived stack + `os` + `anthropic`; stdlib-only) |
| Derived records (`data/fincen/derived/*.json`) | 12 (added Phase 17: fin-2026-a001, fin-2021-a001, fin-2024-a001, fin-2025-a001, fin-2022-a002) |
| FinCEN corpus md (`data/fincen/*.md`) | 14 (committed source of truth) |
| Corpus explorer live | 12/14 (was 7/14; only the 2 FATF advisories non-derivable) |
| `dist/corpus/index.html` | ~181 KB (was ~110 KB) |
| Showcase artifacts | `index.html`, `corpus.html`, `config/**`, `scripts/build.py`, 3 typology dists — BYTE-FROZEN |

## Module Structure

Unchanged module set — Phase 17 is a deletion + scaling WITHIN `scripts/derive_signals.py` (authoring layer); no
new modules, one dep dropped (`anthropic` no longer imported — derive_signals.py is stdlib-only). The inverted
loop (LLM extracts → `check_record`/`--check-derived` gate disposes by quote-grounding) is now the SOLE derivation
path; `extract_red_flags`' sole surviving job (triage flag-counts) is a ~14-line `_rf_triage(md, region)` counter
reusing the `rf_region` span. `--selftest` is gate-only (hardcoded verbatim EFE fixture). See `_ARCHITECTURE.md`.

## Dependencies

- Ship artifact: zero build/runtime deps (Google Fonts via `<link>`, degrades offline).
- Authoring-only (gitignored uv `.venv`, py3.12): `markitdown[pdf]` (MIT, convert only). `anthropic` is now
  UNUSED by `derive_signals.py` (the `--draft` stack was deleted) but still pinned in
  `requirements-authoring.txt` — a stale pin (cleanup candidate).
- Deterministic layer stdlib-only. System python: 3.14.4 (authoring tools run on the uv py3.12 venv).

## Verification State

- `python3 scripts/derive_signals.py --selftest` → gate-only PASS (grounding/paraphrase/degenerate/matrix/shape/
  dup/normalizer/escrow; hardcoded EFE fixture L507/L509 replacing the deleted extractor).
- All 12 derived records pass `--check-derived` under the groundedness gate (verbatim-grounded).
- `python3 scripts/build.py --check all` → 4-artifact ZERO DRIFT.
- Built `__CORPUS__` valid JSON: 14 advisories, 12 derived, render-ready through all 4 screens.
- Reviewer ACCEPT 9/10 (1 MEDIUM = latent triage-overcount footgun for a future not-yet-derived glued advisory;
  harmless in ship, disclosed, NOT fixed inline).

## Recent Commits (pre-gate)

```
2b05c78 Phase 16: mark delivery accepted + phase complete (gate)
bca3612 Phase 16: Invert extraction — LLM extracts, deterministic gate disposes; 5→7/14 (M7)
2a62903 Phase 15: mark delivery accepted + phase complete (gate)
62f7c1d Phase 15: Harden extraction faithfulness — footnote-resume + esc() sweep (M7)
410241f Phase 14: mark delivery accepted + phase complete (gate)
```

(Phase 17 impl commit + gate commit land at the delivery gate.)
