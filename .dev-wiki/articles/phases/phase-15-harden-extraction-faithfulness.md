---
title: "Phase 15: Harden extraction faithfulness + fix shipped defects"
aliases: [extractor-faithfulness, footnote-resume, esc-fix, spine-robustness]
category: phases
tags: [milestone-m7, corpus, extractor, derive-signals, correctness, spine-robustness]
parents: []
created: 2026-06-05
updated: 2026-06-05
source: plan
status: completed
ceremony: lite
scope: ["scripts/derive_signals.py", "data/fincen/derived/fin-2022-a001.json", "data/fincen/derived/fin-2025-a003.json", "data/fincen/corpus-status.json", "dist/corpus/index.html", "README.md", "CLAUDE.md"]
entry_criteria: "Phase 14 complete + accepted: corpus explorer at 5/14 live. Phase 14 surfaced 2 concrete defects — (1) the extractor missed a real flag at fin-2025-a003 md L499 (orphaned by a page-boundary footnote run; the advisory still reports CLEAN — a silent faithfulness miss), and (2) the Phase-12 fin-2022-a001 record stores `&gt;= 2` which double-escapes under corpus.html's esc() on a currently-shipped record. User chose to harden the spine + fix defects over scaling further / showcase debt / a wow beat."
exit_criteria: "(1) extract_red_flags footnote-resume fix: a mid-list footnote/citation run no longer permanently ends a section — fin-2025-a003 extracts the L499 escrow flag (17→18), --selftest EFE 12+12 unchanged, newly-captured flags spot-checked genuine. (2) No derived record stores HTML-pre-escaped entities in build_logic (fin-2022-a001's `&gt;=` → raw text). (3) fin-2025-a003 derived record carries the recovered escrow flag as an 18th --check-derived-clean indicator. (4) --corpus-status regenerated + dist/corpus rebuilt; --check all zero drift; index.html/corpus.html/config/** + 3 typology dists byte-untouched. (5) glued-no-separator deferral documented (stays FLAGGED — no safe deterministic split)."
---

# Phase 15: Harden extraction faithfulness + fix shipped defects

## Objective

Fix the two concrete defects Phase 14 surfaced, scoped by MEASUREMENT not assumption: the extractor's silent
miss of a real red flag in a CLEAN advisory (fin-2025-a003 L499, orphaned by a page-boundary footnote run),
and the fin-2022-a001 esc() double-escape render bug on a shipped record. Do NOT build a brittle glued-list
splitter — measurement shows the glued LOW/NEEDS advisories have no safe deterministic split signal.

## Approach

**Measurement first.** Inspecting the LOW/NEEDS advisories showed they fail for 3 distinct reasons:
- **(a) Footnote-interruption** — a real, well-formed list hard-stopped mid-list by a page-boundary footnote
  run, orphaning everything after (fin-2025-a003's L499 escrow flag; fin-2025-a001 ISIS). The current
  `_SECTION_STOP` treats a footnote-number line (`\d+\.`) as a hard section-end. **Safely fixable.**
- **(b) Glued-no-separator** — markitdown dropped both bullets and blank lines, fusing flags + the intro
  caveat into one block (fin-2021-a004 ransomware, fin-2026-a001 health-care). No blank/bullet/marker signal;
  sentence-splitting would over-split genuine multi-sentence flags (the `_MAX_FLAG_CHARS` calibration target).
  **No safe deterministic signal.**
- **(c) Partial/noise** (fin-2021-a001, fin-2024-a001).

The extractor's contract is **extract-or-honestly-flag**, and it already honors (b)/(c) — those aren't
defects, they're correctly flagged as not-cleanly-extractable. The only TRUE defect is the silent miss in a
CLEAN advisory (a faithfulness lie) plus the esc() bug. So:

1. **Footnote-resume fix** in `extract_red_flags` — a mid-list footnote/citation run no longer *permanently*
   ends a section; the span skips it (the `_CITATION` filter already drops footnote blocks) and resumes
   capturing real flag blocks up to the next anchor or a TRUE terminal stop ("Reminder of Relevant BSA
   Obligations", SAR-filing, a numbered major section header). Guarded by `--selftest` (EFE 12+12).
2. **Pre-escaped-entity sweep** across all `derived/*.json` `build_logic` — replace stored `&gt;`/`&lt;`/
   `&amp;` with raw text. Convention: derived records store RAW text; `corpus.html`'s `esc()` is the sole
   escaper.
3. **Add the recovered escrow flag** as fin-2025-a003's 18th indicator (extraction ↔ derivation consistent).
4. **Regenerate `--corpus-status` + rebuild `dist/corpus`**; `--check all` zero drift.
5. **Docs** — the faithfulness fix + the glued-no-separator deferral rationale.

**Deferred (investigated, not punted):** glued-no-separator splitting for ransomware / health-care-fraud.
No safe signal → they stay correctly FLAGGED (re-confirms the Phase-12 flag-don't-force decision).

## Scope

- `scripts/derive_signals.py` — the footnote-resume span fix + docstring note.
- `data/fincen/derived/fin-2022-a001.json` — esc() entity → raw text (and any other affected record).
- `data/fincen/derived/fin-2025-a003.json` — add the 18th (escrow) indicator.
- `data/fincen/corpus-status.json` — regenerated.
- `dist/corpus/index.html` — rebuilt.
- `README.md`, `CLAUDE.md` — document the fix + the glued deferral.

UNTOUCHED (byte-frozen): `index.html`, `corpus.html`, `config/**`, `dist/{fentanyl,trade-based,elder-financial-exploitation}/`.

## Exit Criteria

- [x] Footnote-resume fix: fin-2025-a003 extracts the L499 flag (17→18); `--selftest` EFE 12+12 unchanged; surgical — 0 collateral, all 13 other advisories byte-identical, spot-checked genuine.
- [x] No derived record stores HTML-pre-escaped entities in build_logic (fin-2022-a001 + fin-2024-a002 swept to raw text); touched records still `--check-derived`-clean.
- [x] fin-2025-a003 derived record = 18 `--check-derived`-clean indicators (the recovered escrow flag IND-18 traces to L499).
- [x] `--corpus-status` regenerated; `dist/corpus` rebuilt; `build.py --check all` zero drift; `git diff index.html corpus.html` empty; config/** + 3 typology dists byte-untouched.
- [x] Glued-no-separator deferral documented (stays FLAGGED — no safe deterministic split; README/CLAUDE/docstring).

## Constraints (load-bearing)

- **Faithfulness over count** — the fix exists to stop a CLEAN advisory silently dropping a real flag, NOT to inflate counts. Newly-captured blocks must be genuine red flags (the `_CITATION`/`_RF_HEADER_LOOSE`/min-length filters still apply); spot-check.
- **EFE 12+12 is the guard rail** — `--selftest` must stay green; the footnote-resume change must not over-extend EFE's financial section into footnote prose.
- **No brittle splitter** — glued-no-separator advisories stay FLAGGED; do not ship a sentence-split heuristic that risks over-splitting genuine multi-sentence flags.
- **Deterministic, stdlib-only, authoring-only** — `extract_red_flags` stays pure + stdlib; `anthropic` lazy; `derive_signals.py` never imported by `index.html`/`build.py`.
- **Showcase byte-frozen** — `index.html`/`corpus.html`/`config/**` + the 3 typology dists untouched.

## Checkpoints

- T1: if the footnote-resume fix can't capture L499 without regressing EFE 12+12 or swallowing footnote prose as flags — revert it, keep the silent miss FLAGGED as a documented known limitation, don't ship a fragile span heuristic (the abort rule).
- T4: confirm `git diff index.html corpus.html` empty + `--check all` zero drift before declaring done.
- Blocked >3 attempts on a task → ask the user: skip or abort.

## Assumptions

- The footnote-resume cases (fin-2025-a003, fin-2025-a001) have a clean separation between the footnote run (caught by `_CITATION`) and the resumed list, so resuming is safe. Verified per-advisory at T1.
- Adding the 18th indicator to fin-2025-a003 doesn't disturb the existing 17 (their src_lines still trace); the record stays `--check-derived`-clean.

## Notes

Direction approved by user 2026-06-05: harden the spine + fix defects, defer glued-no-separator splitting.
The key reframe vs the Phase-14 follow-up list: "fix the extractor to parse more" → "the extractor already
extracts-or-flags; fix only the SILENT MISS (a CLEAN advisory dropping a real flag) + the esc() bug." This is
the subtraction-tested scope — measurement showed the glued cases have no safe split, so chasing them would
add fragility for little gain. Follow-ups not in scope (later): if glued-no-separator splitting is ever
wanted, it needs a different ingestion (a converter that preserves list structure), not a post-hoc splitter ·
remaining CLEAN derivations (EFE corpus record, COVID EIP) · FATF non-derivable labeling · corpus
combination-lift wow beat · elder true-up · fentanyl re-point · manifest --fetch cadence.
