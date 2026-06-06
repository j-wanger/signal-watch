---
title: "Phase 17: Complete corpus derivation — delete extract_red_flags (the real subtraction) + scale to 12/14"
aliases: [complete-corpus-derivation, delete-extract-red-flags, real-subtraction, rf-triage-counter, corpus-12-14]
category: journal
tags: [milestone-m7, corpus, extractor, derive-signals, subtraction-test, dead-code-deletion, scale-to-complete, groundedness]
parents: [phase-17-complete-corpus-derivation]
created: 2026-06-06
updated: 2026-06-06
source: debrief
duration: ~3h (post-compaction estimate; may undercount)
---

# Phase 17: Complete corpus derivation + delete extract_red_flags (the real subtraction) (M7)

## What Happened

Did the REAL line-count subtraction Phase 16 deferred, then scaled the corpus explorer to near-completion. Phase 16
INVERTED the boundary (LLM extracts → deterministic gate disposes) and the correctness-path complexity SHRANK, but
`derive_signals.py` had GROWN 1063→1189 because decision B retained the now-demoted `extract_red_flags`. Phase 17 deleted
it — and the deletion went WIDE.

**T1 — the subtraction.** Deleted `extract_red_flags` AND the whole now-dead `--scaffold`/`--draft`/`--scaffold-derived`
authoring stack the inverted loop replaced (`scaffold_config`, `write_scaffold`, `draft_judgment`, `write_draft`,
`_few_shot`, `_apply_judgment`, `_derived_skeleton`) + the `anthropic` dependency + the `os` import. `derive_signals.py`
dropped **1202 → 600 lines (−602, −50%)** — beat the ~700 estimate; def-grep 0; stdlib-only. The extractor's sole
surviving job (triage flag-counts for the not-yet-derived chip) became a ~14-line `_rf_triage(md, region)` counter that
reuses the already-computed `rf_region` span — no section-finding. `--selftest` is now gate-only (hardcoded verbatim EFE
fixtures L507/L509 replacing the deleted extractor; it still pins grounding/paraphrase/degenerate/matrix/shape/dup/
normalizer/escrow). The inverted loop (LLM extracts → `check_record`/`--check-derived` gate disposes by quote-grounding)
is now the SOLE derivation path.

**T2–T4 — scale to completion.** Derived the 5 remaining derivable advisories via the inverted loop: fin-2026-a001
(glued health-care, 24 ind, 6 BUILD_NOW — the LLM reached a glued advisory the deleted extractor sized as ~6 blocks, no
splitter), fin-2021-a001 (COVID health-insurance, 16 ind), fin-2024-a001 (Iran-backed terror finance, 9 ind),
fin-2025-a001 (ISIS, 11 ind), and the EFE corpus record fin-2022-a002 (12 ind). The two "LOW" advisories validated clean
— the LOW triage was the deleted extractor under-counting through interleaved footnotes, NOT unextractable content; no
degrade needed. Corpus **7/14 → 12/14 live**; only the 2 FATF advisories (no enumerated red-flag list) stay
non-derivable.

**T5–T6 — rebuild + docs.** dist/corpus rebuilt 109,948 → 180,119 B; `--check all` 4-artifact ZERO DRIFT; headless
brace-match confirmed the built `__CORPUS__` is valid JSON (14 advisories, 12 derived, render-ready through all 4
screens). README + CLAUDE document the deleted stack + the counter + 12/14. Reviewer ACCEPT 9/10.

## Decisions Made

- `corpus_status_records` uses the `_rf_triage` counter UNIFORMLY for all 14 — NOT the planned "flag_count from the
  derived record where live, else the counter". DISCOVERY: corpus.html's advCard reads `flag_count` only for the
  not-yet-derived chip (live cards render from the derived record's indicators), so no live/not-live special-casing is
  needed. A simpler subtraction than the plan specified.
- The EFE corpus record (fin-2022-a002) derives the 12 FINANCIAL red flags only; EFE's 12 BEHAVIORAL red flags are
  observational/teller-witnessed SAR-narrative indicators (not a transaction-data signal surface) → out of scope for
  buildable-signal derivation, documented in provenance; the hand-curated showcase elder typology presents them in full.
- Footnote-interrupted flags (fin-2021-a001 etc.): the LLM extracts a CONTIGUOUS grounded span and DROPS the
  across-page-break continuation rather than bridging it — `normalize(md)` carries the footnote run between the split
  clauses, so a bridged flag would not ground. In-flag footnote markers are kept verbatim where they fall mid-span (e.g.
  "NPO84") so the quote grounds.
- The deletion went WIDE: not just `extract_red_flags` but the whole scaffold/draft authoring stack + the `anthropic`
  dependency + the `os` import — all dead by the inverted loop. `derive_signals.py` is now stdlib-only.

(Decisions recorded in _CURRENT_STATE Recent Decisions during planning — lite ceremony skips decision articles.)

## Problems Solved

- The "complexity moves not shrinks" abort risk — the counter genuinely shrank: `_rf_triage` reuses `rf_region` (already
  solved region-finding), so it is a ~14-line reuse, not a reintroduced 130-line section-parser.
- Reaching the glued health-care fin-2026-a001 (the hardest glued advisory) — the LLM read + extracted all 24 flags, the
  gate grounded each verbatim; no structure-preserving converter and no post-hoc splitter were needed (Phase-15
  glued-deferral fully dissolved).
- The two "LOW" advisories (Iran-terror, ISIS) — validate-first showed the LOW label was the deleted extractor
  under-counting through interleaved footnotes, not unextractable content; both gate-passed clean.

## Open Questions

- None unresolved.

## Artifacts Changed

- `scripts/derive_signals.py` (1202 → 600 lines, −602 / −50%: deleted `extract_red_flags` + the
  `--scaffold`/`--draft`/`--scaffold-derived` stack + `anthropic` + `os`; added `_rf_triage(md, region)`; `--selftest`
  gate-only with a hardcoded EFE fixture; stdlib-only)
- `data/fincen/derived/{fin-2026-a001,fin-2021-a001,fin-2024-a001,fin-2025-a001,fin-2022-a002}.json` (NEW — 5 derived
  records via the inverted loop, each `--check-derived` clean + verbatim-grounded)
- `data/fincen/corpus-status.json` (regenerated at 12/14; same 14-entry shape; counter-sourced flag_counts)
- `dist/corpus/index.html` (rebuilt, 12/14 live; 109,948 → 180,119 B)
- `README.md`, `CLAUDE.md` (deleted authoring stack + the `_rf_triage` counter + 12/14; inverted loop is the sole path)

## Related

- [[phase-17-complete-corpus-derivation|Phase 17: Complete corpus derivation + delete extract_red_flags]] — parent phase
- [[2026-06-06-phase-16-invert-extraction|Phase 16: Invert extraction]] — the inversion this phase completes (it named
  the deletion as the Phase-17 candidate)

### Review Gate

Unified reviewer **Score 9/10, Verdict ACCEPT**. All exit criteria verified end-to-end.
- [MEDIUM] latent triage-overcount footgun — `_rf_triage` mis-counts glued advisories (fin-2021-a001 region → 47 blocks;
  fin-2026-a001 6 vs 24 real). HARMLESS in the shipped 12/14 (no glued advisory is not-yet-derived; live cards render
  from the record) but a latent footgun if a future glued advisory is added but not yet derived. → **NOT fixed inline**
  (not a shipped defect; folded to soft observations, disclosed in provenance/docstrings).
- Suggestions (non-blocking): centralize the two triage thresholds (`_MIN_CLEAN_FLAGS`, `_MIN_FLAG_NCHARS`) if the counter
  is ever tightened; the LOW-advisory provenance anchors to the deleted extractor (the load-bearing "now LLM-extracted"
  clause is already present).
- Rationale: subtraction genuine + clean (no orphaned refs, no `os`/`anthropic`, remaining `extract_red_flags` mentions
  are docstrings documenting the deletion); `_rf_triage` reuses `rf_region` (real shrink, not a reintroduced parser); all
  5 new records gate-pass with verbatim grounding spot-checked incl. the hardest glued fin-2026-a001; BUILD_NOW
  build_logics substantive; EFE financial-only scoping sound + documented; `--selftest` still a meaningful gate; docs
  accurate; `--check all` zero drift; showcase byte-frozen.

### Retro Check (Phases 1-15)

| Dimension | Findings | Signal |
|-----------|----------|--------|
| 1. Recurring Blockers | 0 genuine (abort conditions hit transiently in Ph12/Ph15, both self-resolved without aborting; no blocked task) | low |
| 2. Decision Reversals | 0 true reversals (glued-splitter deferred Ph15 → DISSOLVED Ph16; extractor DEMOTED Ph16 → DELETED Ph17 — staged evolution, not reversal) | low |
| 3. User Corrections | recurring: user overrides the planner toward SCALE/ARCHITECTURE over the elder-true-up + fentanyl-re-point (Ph10, Ph11, Ph15, Ph16) | high |

Recommendations:
- The planner keeps recommending the showcase-debt true-up (elder presentation-values, fentanyl verbatim re-point); the
  user keeps deferring it in favor of corpus/architecture work across 4 phases. Either schedule the showcase true-up as a
  committed phase OR stop surfacing it as the default next-action — the repeated override is a stable preference signal,
  not indecision. No dedicated improvement phase warranted (only 1 high-signal dimension; the pattern is a preference,
  not a systemic failure).

## Soft Observations / Phase 18 Candidates

- Tighten the coarse `_rf_triage` counter (the reviewer's MEDIUM): it over/under-counts glued advisories (fin-2021-a001
  region → 47 blocks; fin-2026-a001 6 vs 24 real). HARMLESS in the shipped 12/14 (no glued advisory is not-yet-derived;
  live cards render from the record), but a LATENT footgun if a future glued advisory is added but not yet derived — its
  chip would badly mis-count. Disclosed in provenance/docstrings. Carries the prior "tighten rf_region" candidate.
  | Phase-18 candidate | evidence: `data/fincen/corpus-status.json` flag_counts
- FATF non-derivable labeling polish (carried) — a clearer "FATF jurisdiction advisory, no enumerated red-flag list"
  label in the explorer's Select screen. | Phase-18 candidate
- Reviewer suggestions (non-blocking): centralize the two triage thresholds (`_MIN_CLEAN_FLAGS`, `_MIN_FLAG_NCHARS`) if
  the counter is ever tightened; LOW-advisory provenance anchors to the deleted extractor (load-bearing clause already
  present). | tidy-up candidate
- STALE DEPENDENCY PIN (debrief discovery): `scripts/requirements-authoring.txt` still lists `anthropic`, but
  `derive_signals.py` no longer imports it (the `--draft` stack was deleted in T1, derive_signals.py is now stdlib-only).
  Harmless (authoring-only, gitignored `.venv`) but inaccurate — drop `anthropic` from the requirements file.
  | tidy-up candidate | evidence: `requirements-authoring.txt` vs `grep anthropic scripts/derive_signals.py` (0)
- Carried from prior phases: corpus combination-lift wow beat; elder presentation-values true-up; fentanyl verbatim
  re-point; manifest `--fetch` cadence. | Phase-18 candidates (the showcase-debt true-ups are the recurring deferral —
  see Retro Dim 3)
