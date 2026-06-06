---
title: "Phase 15: Harden extraction faithfulness + fix shipped defects (M7)"
date: 2026-06-05
category: journal
tags: [milestone-m7, corpus, extractor, derive-signals, correctness, spine-robustness]
phase: phase-15-harden-extraction-faithfulness
ceremony: lite
---

# Phase 15: Harden extraction faithfulness + fix shipped defects (M7)

Lite, 5 tasks, DELIVERED + accepted. Fixed the 2 concrete defects Phase 14 surfaced, scoped by
MEASUREMENT not assumption — and deliberately did NOT build a brittle glued-list splitter.

## The reframe (what made this phase small + correct)

The Phase-14 follow-up list framed it as "fix the extractor to parse more (the L499 miss + the 3 LOW +
2 glued NEEDS)." Measurement (inspecting each LOW/NEEDS advisory) showed they fail for THREE distinct
reasons: (a) **footnote-interruption** — a real, well-formed list hard-stopped mid-list by a page-boundary
footnote run (fin-2025-a003 L499 escrow flag; fin-2025-a001 ISIS); (b) **glued-no-separator** — markitdown
dropped both bullets AND blank lines, fusing flags + the intro caveat into one block (fin-2021-a004
ransomware, fin-2026-a001 health-care) with no safe deterministic split; (c) partial/noise. The extractor's
contract is **extract-or-honestly-flag** and it already honors (b)/(c). So the only TRUE defect is the
**silent miss in a CLEAN advisory** (fin-2025-a003 reads CLEAN but drops L499 — a faithfulness lie) plus the
shipped fin-2022-a001 esc() bug. Fixing only those kept the phase small and honest.

## What shipped

- **T1 footnote-resume fix** (`extract_red_flags`) — 3 measured iterations. Split the stop logic into
  `_SECTION_STOP` (true terminals — reminder/SAR/numbered-section — always break) + a new `_FOOTNOTE_STOP`
  handled CONDITIONALLY: a mid-list footnote run is TRANSIENT when another red-flag section follows
  (`next_boundary` set) → skip it and resume up to the next anchor (captures L499); TERMINAL when it's the
  last section → break (no over-run). The first attempt (remove footnote-stop entirely) was too blunt —
  regressed last-section advisories (a008 11→28, a021a002 7→22, a022a001 5→11); the bounded `next_boundary`
  rule fixed that. Two footnote-TAIL leaks remained (a003 L445, PRC L578 — footnote continuations wrapped
  past an internal blank, no leading "N." marker, NOT structurally separable since the genuine escrow L499
  also sits post-footnote-pre-anchor), so hardened `_CITATION` with 2 targeted signatures: a federal case
  docket (`\d:\d{2}-[a-z]{2,3}-\d+`, kills L445 "2:23-cr-258") + a no-day "(Mon YYYY)" paren-date end (kills
  L578 "(Nov. 2006)."). FINAL: **surgical — 1 genuine flag recovered (a003 17→18), 0 collateral** (all 13
  other advisories byte-identical, EFE 12+12, summary still 7C/3L/4N).
- **T2 entity sweep** — `html.unescape` over the 2 Phase-12 records (fin-2022-a001 2×, fin-2024-a002 5×
  `&gt;=`/`&lt;=`) → raw text; both re-check clean. esc() bug fixed end-to-end (verified in the built file:
  data now holds raw `>= 2`, old `&gt;=` gone → renders `>=`).
- **T3 escrow IND-18** — added the recovered flag to fin-2025-a003 (BUILD_ENRICH; shell classification needs
  registry enrichment). 18 indicators, check-clean. Extraction ↔ derivation now consistent.
- **T4 rebuild** — manifest regenerated (a003 17→18), dist/corpus rebuilt, `--check all` zero drift.
- **T5 docs** — footnote-resume + glued-deferral + the RAW-text/esc() convention in README/CLAUDE/docstring.

## Decisions

- **Harden faithfulness + fix defects, scoped by measurement** — a footnote-resume fix + an esc() entity
  sweep. NOT a glued-list splitter. (User chose this over scaling further / showcase debt / a wow beat.)
- **Glued-no-separator splitting DEFERRED** (re-confirms the Phase-12 flag-don't-force decision): no safe
  deterministic split exists; structure-preserving parsing would need a better converter, not a post-hoc
  splitter. (User approved deferring it at the direction gate.)

## Problems & solutions

- The footnote-resume hit the ABORT condition (first attempt captured footnote prose) but didn't need to
  abort — the bounded `next_boundary` rule + 2 targeted citation-tail filters got it surgical. 3 measured
  iterations beat one guess: capture before-state → change → measure full corpus → narrow.
- The 2 footnote-tail leaks couldn't be separated structurally (the genuine escrow flag also sits after a
  footnote run before the next anchor), so the content-based `_CITATION` filter (the existing footnote
  filter) was the right tool, hardened to exactly 2 corpus-specific signatures + measured for zero collateral.

## Health Delta

`extract_red_flags` logic refined (no new modules/deps; stdlib-only; anthropic stays lazy; not imported by
engine/build). `--selftest` EFE 12+12 unchanged. `--check all` 4-artifact zero drift. `index.html`/
`corpus.html`/`config/**` + the 3 typology dists byte-untouched.

## Soft Observations / Phase 16 Candidates

- **Glued-no-separator needs a better converter, not a splitter** — if fin-2021-a004 / fin-2026-a001 flags
  are ever wanted, the fix is a structure-preserving PDF→md step (pymupdf4llm was the noted AGPL
  authoring-only fallback), since markitdown drops bullets + blank lines. A post-hoc splitter can't safely
  reconstruct list boundaries. Evidence: fin-2021-a004 L283+, fin-2026-a001.
- **Scale the live menu to 6–7/14** — the remaining CLEAN advisories (EFE corpus record, COVID-EIP
  fin-2021-a002) are derivable now; same authoring loop as Phase 14.
- **ISIS (fin-2025-a001) stays LOW** — single-section, footnotes terminal (no next anchor to bound a
  resume); correctly flagged, not a regression. A different heuristic (terminal-stop detection for a
  last-section footnote→resume) could recover it but adds fragility for one advisory — deferred.
- Carried: FATF non-derivable labeling · corpus combination-lift wow beat · elder presentation-values
  true-up · fentanyl verbatim re-point · manifest `--fetch` cadence.

## Gate Compliance

Direction gate approved 2026-06-05 (harden spine + fix defects; glued-splitting deferred). Delivery gate
accepted 2026-06-05 (this debrief). Both gates present.

## Review Gate

Lite phase (5 tasks). Self-check (categories 1–2) was the quality gate: scope clean (byte-frozen confirmed),
correctness verified (surgical extraction diff, EFE 12+12, 3× `--check-derived`, `--check all` zero drift,
esc() fix confirmed in the built artifact, `node --check`). No reviewer dispatch.
