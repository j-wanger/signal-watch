---
title: "Phase 14: Scale corpus derivation — 3 more CLEAN advisories → 5/14 live (M7)"
date: 2026-06-05
category: journal
tags: [milestone-m7, corpus, llm-backend-derivation, authoring, build-recommendation]
phase: phase-14-scale-corpus-derivation
ceremony: lite
---

# Phase 14: Scale corpus derivation — 3 more CLEAN advisories → 5/14 live (M7)

Lite, 5 tasks, DELIVERED + accepted. The follow-through on Phase 13: the corpus explorer shipped at 2/14
derived/live (a stakeholder clicking around hit "not yet derived" 12 of 14 times). Phase 14 fills the live
menu to **5/14** — purely by authoring 3 more derived records + rebuilding, with **zero** engine/spine/
front-end edits (the spine tools and `corpus.html` already exist; `build.py` makes an advisory live simply
by the presence of `data/fincen/derived/<id>.json`).

## What shipped

Three new LLM-backend-derived (this session, no API key), `--check-derived`-clean records via the proven
loop (`--scaffold-derived` → author status/data → `build_rec` from the cover×data matrix + rationale +
`build_logic` on BUILD_NOW → prune residual noise → deterministic check disposes):

- **fin-2020-a008 human trafficking** — 10 indicators (pruned 1 intro-tail noise line; advisory states "10
  new financial red flag indicators", extraction got all 10 + 1 noise). Spread: 2 BUILD_NOW
  (victim-maintenance basket · cash-in-no-electronic-out) · 3 ENRICH · 2 ENHANCE · 1 SOURCE · 1 MONITOR · 1
  COVERED (ID/CTR avoidance = structuring).
- **fin-2025-a003 Chinese money-laundering networks** — 17 indicators (clean, no pruning). The most
  buildable typology: **5 BUILD_NOW** (student-mule funnel · cash-layer-to-high-risk dispersal ·
  marketplace-income-no-inventory · inbound-aggregation card mirror · business-pays-third-party-cards) · 4
  ENRICH · 4 ENHANCE · 2 SOURCE · 1 COVERED · 1 MONITOR.
- **fin-2025-a002 Iran illicit finance** — 16 indicators (validate-first gate passed; no swap). The
  enrichment-hungry contrast (maritime DBs, corporate registries, trade/AIS data): 4 BUILD_NOW · **7
  ENRICH** · 2 SOURCE · 1 ENHANCE · 1 MONITOR · 1 COVERED.

Authored each via a matrix-merge script that preserves the verbatim extracted flag text + src_line and
auto-derives `build_rec` from `build_rec_category` (so it can't drift from the matrix). `dist/corpus`
rebuilt → 5/14 live; README + CLAUDE bumped 2/14 → 5/14.

## Decisions

- **Goal = scale derivation** (fuller live menu) over the genuine alternatives: spine robustness
  (glued-list splitting + FATF labeling), a corpus combination-lift wow beat, or showcase debt true-up. The
  demo's biggest pitch weakness was the 12/14 "not yet derived" miss-rate.
- **Picks = 3 strong distinct topical CLEAN** (trafficking · CMLN · Iran); **EFE excluded** (already the
  full showcase elder typology — a duplicate corpus record isn't worth 24 indicators), **COVID EIP
  deferred** (dated). Per-advisory **validate scaffold faithfulness vs the md before authoring** — quality
  over count.

## Problems & solutions

- **esc() double-escape trap** — `corpus.html` applies `esc()` to every rendered field including
  `build_logic.logic`. Storing pre-escaped entities (`&gt;`) would render a literal `&gt;`. Solution: store
  RAW text; phrased thresholds in words ("at least three") to sidestep the character entirely.
- **Extractor missed a real flag** — `fin-2025-a003` has an 18th red flag at md L499 (U.S.-escrow /
  foreign-shell) glued to a page-break `FINCEN ADVISORY` running header right after a footnote block, so it
  fell between sections. Not extracted ⇒ can't trace ⇒ honestly omitted (17 shown, not faked).
- **Faithful bulk authoring** — the matrix-merge script avoided retyping 17/16 verbatim flags by hand and
  guaranteed build_rec ↔ matrix consistency.

## Health Delta

No code added (pure data authoring). `derive_signals.py --selftest` unchanged (EFE 12+12 + deterministic
checks). `build.py --check all` 4-artifact zero drift. `node --check` on the rebuilt inlined script (data +
app, 82 KB) valid. `index.html`/`corpus.html`/`config/`/`scripts/` + the 3 typology dists byte-untouched.

## Soft Observations / Phase 15 Candidates

- **Extractor glued-boundary gap** (spine robustness) — `extract_red_flags` misses red flags glued to a
  page-break running-header immediately after a footnote block (concrete: `fin-2025-a003` L499). The
  section-stop logic ends a section at the footnote and never re-opens for the orphaned flag. Same class as
  the 3 LOW glued-list advisories. Evidence: `data/fincen/fin-2025-a003.md` L494–499.
- **Pre-existing render bug** — the Phase-12 `fin-2022-a001` (kleptocracy) record stores `&gt;= 2` in a
  `build_logic.logic` string; under `corpus.html`'s `esc()` it double-escapes to a literal `&gt;` on the
  SIGNAL screen of a currently-shipped record. One-line fix (store raw text) when that record is next
  touched. Convention worth recording: **derived records store RAW text; the front-end's `esc()` is the
  sole escaper.**
- **Scale the rest** — the remaining CLEAN advisories (EFE corpus record, COVID EIP fin-2021-a002) and the
  2 glued NEEDS (fin-2021-a004, fin-2026-a001, after the extractor fix) extend the live menu further.

## Gate Compliance

Direction gate approved 2026-06-05 (scale derivation; 3 advisories). Delivery gate accepted 2026-06-05
(this debrief; user accepted the post-implementation report). Both gates present.

## Review Gate

Lite phase (5 tasks, pure data authoring) — self-check (categories 1–2) was the quality gate: scope clean
(byte-frozen confirmed), correctness verified (3× `--check-derived`, `--check all` zero drift, headless
render assertions, `node --check`, `--selftest` regression). No reviewer dispatch.
