---
title: "Phase 16: Invert extraction — LLM extracts, deterministic groundedness gate disposes + scale to 7/14"
aliases: [invert-extraction, groundedness-gate, quote-traceability, md-normalizer]
category: journal
tags: [milestone-m7, corpus, extractor, derive-signals, groundedness, architecture-inversion, subtraction-test]
parents: [phase-16-invert-extraction]
created: 2026-06-06
updated: 2026-06-06
source: debrief
duration: ~3h (post-compaction estimate; may undercount)
---

# Phase 16: Invert extraction (LLM extracts, deterministic gate disposes) + scale as proof (M7)

## What Happened

Applied the SUBTRACTION TEST to the extraction spine and INVERTED the extraction boundary. The user reframed
the Phase-15 follow-up menu — naming the fear that "in the end we still rely on LLM authoring" — toward making
the deterministic layer a GATE rather than a neural-overridden extractor. So: the LLM (this model session)
EXTRACTS candidate red flags; the deterministic layer became a GROUNDEDNESS GATE that disposes. Traceability
authority moved from `src_line ∈ extract_red_flags(md)` (a structural parse) to QUOTE-GROUNDING
(`normalize(flag) ⊂ normalize(md)`).

The subtraction won decisively at T1: ONE rule — `normalize(text) = re.sub(r'[^a-z0-9]+','',text.lower()).replace('fincenadvisory','')`
— absorbs the ENTIRE closed FinCEN-md artifact set at once (line wraps, word-wrap hyphens, smart quotes,
punctuation, footnote-ref digits, AND the page-break running header → a droppable `fincenadvisory` token incl.
the letter-spaced variant). The header-glued escrow STRESS case (fin-2025-a003 raw L499) grounds WITHOUT
special-casing because the header sits at the line boundary, not mid-flag. `check_record` rewired: deleted the
`flag_lines = {f['line'] for f in extract_red_flags(md)}` src_line∈extractor check → `normalize(flag) in
normalize(md)` (grounding = the authority) + a coarse `rf_region(md)` relevance guard (first `_RF_*` anchor →
first `_RF_REGION_END` terminal; src_line must sit inside). The ~3-line normalizer + ~12-line `rf_region`
REPLACE the src_line traceability that depended on the ~130-line extractor — correctness-path complexity SHRANK.

T2 migration was near-free as predicted: all 5 committed records pass `--check-derived` under the new gate
UNEDITED (their `flag` fields were transcribed verbatim by prior loops → ground by construction). Only edit was
a surgical RAW-text provenance swap across all 5. T4 landed THE PROOF: **ransomware fin-2021-a004** — the
previously-unreachable headline (deterministic extract returned ZERO flags: glued-no-separator) — the LLM read
the source and extracted ALL 12 genuine red flags, every one grounding verbatim, with NO converter + NO
post-hoc splitter. The Phase-15 glued-deferral DISSOLVED. **COVID-EIP fin-2021-a002** consolidated 7 fragmented
(i)/(ii) sub-clause blocks → 3 genuine indicators. Corpus 5/14 → 7/14 live.

Reviewer ACCEPT 9/10; 2 MEDIUM findings fixed inline (see Review Gate). One DISCOVERY refined T1 during T4.

## Decisions Made

- Phase 16 = INVERT the extraction architecture (LLM extracts → deterministic groundedness gate disposes);
  subtraction test on the ~130-line accreted extractor.
- Relevance trade (A) = groundedness + a cheap section-cite region check (`rf_region`), NOT pure groundedness,
  NOT a full parser.
- `extract_red_flags` DEMOTED not deleted (B); `corpus-status.json` SHAPE preserved, semantics shifted
  (derivable = `rf_region` exists, false only for the 2 FATF advisories).
- Breadth (C) = 2 records as PROOF (COVID-EIP + ransomware previously-unreachable); pymupdf4llm converter option
  DISSOLVED.

(Decisions recorded in _CURRENT_STATE Recent Decisions during planning — lite ceremony skips decision articles.)

## Problems Solved

- Header-glued + hyphen-truncated escrow flag (fin-2025-a003 L499) grounding — solved by the single normalize()
  rule (header at line boundary collapses to a droppable token; word-wrap hyphens fold away).
- Ransomware fin-2021-a004 (0 deterministic flags, glued-no-separator) reached — the LLM extracted all 12 flags;
  the gate verified each grounds verbatim. The structure-preserving-converter need dissolved.
- `_RF_REGION_END` too-loose for ransomware — DISCOVERY (escape-hatch, refines T1): broadened
  `"reminder of relevant"` → `"reminder of\b"` so "Reminder of Regulatory Obligations" terminates the region
  (283,405)→(283,339); selftest + all 7 records re-passed, EFE region unchanged — no regression.

## Open Questions

- None new. The coarse-relevance-region limitation is acknowledged + documented (not open): `rf_region` proves
  "in the red-flag region", not "is a red flag" — grounding + the two human gates are the real guarantees.

## Artifacts Changed

- `scripts/derive_signals.py` (1063→1189 lines: `normalize()` + `rf_region()` + `_MIN_FLAG_NCHARS=24` floor +
  rewired `check_record` groundedness gate; `extract_red_flags` demoted to EFE selftest-anchor + triage hint;
  `--corpus-status` semantics shifted, shape preserved; module/`--check-derived` docstrings rewritten)
- `data/fincen/derived/{fin-2020-a008,fin-2022-a001,fin-2024-a002,fin-2025-a002,fin-2025-a003}.json` (migrated:
  raw-text provenance swap, gate-passing)
- `data/fincen/derived/fin-2021-a002.json` (NEW — COVID-EIP, 3 ind, 2 BUILD_NOW), `fin-2021-a004.json`
  (NEW — ransomware, 12 ind, 3 BUILD_NOW; `extraction_quality="llm-extracted"` sentinel)
- `data/fincen/corpus-status.json` (regenerated: `_note` Phase-16 semantics + 2 glued advisories false→true)
- `dist/corpus/index.html` (rebuilt, 7/14 live; 95,188→109,937 B)
- `README.md`, `CLAUDE.md` (inverted architecture + honesty shift + dissolved converter + 5/14→7/14)

## Related

- [[phase-16-invert-extraction|Phase 16: Invert extraction (LLM extracts, deterministic gate disposes) + scale as proof]] — parent phase
- [[2026-06-05-phase-15-harden-extraction-faithfulness|Phase 15: Harden extraction faithfulness]] — the prior spine-hardening phase whose follow-up menu the user reframed

### Review Gate

Unified reviewer **Score 9/10, Verdict ACCEPT**. All exit criteria verified end-to-end.
- [MEDIUM] no min-length floor on grounded flag (a degenerate too-short span could ground) → **FIXED inline**
  (`_MIN_FLAG_NCHARS=24`).
- [MEDIUM] `rf_region` relevance is coarse / over-inclusive → **ACCEPTED** (documented design tradeoff;
  Phase-17 candidate to tighten).
- Suggestions: regression-pin paraphrase rejection → **DONE inline** (2 selftest cases: paraphrase-rejected +
  degenerate-rejected); note the `"llm-extracted"` sentinel is intentional → noted.

## Soft Observations / Phase 17 Candidates

- The real line-count subtraction is DEFERRED: `extract_red_flags` retained per decision B, so
  `derive_signals.py` GREW (1063→1189 — the gate + normalizer + heavy inversion docstrings added alongside the
  retained demoted extractor). The correctness-path complexity shrank; the raw file did not. Phase 17 could
  DELETE `extract_red_flags` outright (re-home the EFE selftest anchor + `--corpus`/`--scaffold-derived` triage
  hint) for the genuine shrink. | evidence: `wc -l scripts/derive_signals.py` 1063→1189
- The relevance guard is coarse BY DESIGN (`rf_region` over-inclusive; docstring: "over-inclusiveness is safe;
  the strong guarantee is grounding") — proves "in the red-flag region", not "is a red flag". The reviewer
  confirmed an in-region intro/footnote quote could pass relevance; grounding + the human gates dispose.
  Optionally tighten if scaling the live menu widely. | evidence: this journal Review Gate (MEDIUM #2)
- Glued health-care fin-2026-a001 is now `derivable=true` (reachable via the inverted loop) but not yet derived
  — the easiest next scale target. | Phase-17 scale candidate
- The ransomware record uses `extraction_quality="llm-extracted"` (an intentional sentinel for the
  0-deterministic-flags case; informational only, not enum-validated) — honest but ad-hoc. | tidy-up candidate
- Carried: scale the live menu further (LOW advisories ISIS fin-2025-a001, Iran-terror fin-2024-a001 + the EFE
  corpus record) via the same inverted loop · FATF non-derivable labeling polish · corpus combination-lift wow
  beat · showcase debt (elder presentation-values true-up, fentanyl verbatim re-point).
