---
title: "Phase 16: Invert extraction (LLM extracts, deterministic gate disposes) + scale as proof"
aliases: [invert-extraction, groundedness-gate, quote-traceability, md-normalizer, subtraction-test]
category: phases
tags: [milestone-m7, corpus, extractor, derive-signals, groundedness, architecture-inversion, spine-robustness]
parents: []
created: 2026-06-06
updated: 2026-06-06
source: plan
status: completed
ceremony: lite
scope: ["scripts/derive_signals.py", "data/fincen/derived/*.json", "data/fincen/corpus-status.json", "dist/corpus/index.html", "README.md", "CLAUDE.md"]
entry_criteria: "Phase 15 complete + accepted (impl commit 62f7c1d): corpus explorer at 5/14 live; extract_red_flags hardened (footnote-resume + 2 citation signatures). But the spine has accreted ~130 lines of _SECTION_STOP/_FOOTNOTE_STOP/_CITATION format special-casing across Phases 11–15 and still only cleanly parses 7/14; the project already concedes the spine ASSISTS, it does not AUTOMATE — complete records need LLM authoring (it stitches the page-broken/hyphen-truncated/header-glued flags the regex cannot, e.g. fin-2025-a003 raw L499). User chose to INVERT the architecture (LLM extracts, deterministic groundedness gate disposes) + scale as proof, over pure breadth-scaling or a structure-preserving converter."
exit_criteria: "(1) Groundedness gate + md normalizer land: a pure normalize(text) handles the closed FinCEN-md artifact set; check_record traceability is rewired to normalized `flag` ∈ normalized md (quote = the new authority, src_line a hint) + a section-cite relevance guard; the escrow STRESS case grounds AND a fabricated flag is rejected (both asserted in --selftest); --selftest still EFE 12+12. (2) The 5 committed records migrate + pass --check-derived under the new gate. (3) extract_red_flags DEMOTED (selftest-anchor + scaffold hint only, no longer the traceability authority); --corpus-status regenerated keeping the SAME SHAPE (build.py + corpus.html byte-untouched), derivable false only for the 2 FATF advisories, live keys on a gate-passing record. (4) 2 new records via the inverted loop (incl. ≥1 previously-LOW/glued advisory) gate-pass → 7/14 live. (5) dist/corpus rebuilt, --check all zero drift, showcase byte-frozen; README + CLAUDE document the inverted architecture + the honesty shift (the spine GATES, no longer claims to ASSIST extraction; the converter option dissolved)."
---

# Phase 16: Invert extraction (LLM extracts, deterministic gate disposes) + scale as proof

## Objective

Apply the subtraction test to the extraction spine: relocate complexity from brittle section-PARSING (an open
problem — every advisory's structure differs) to md NORMALIZATION (a closed problem — a finite artifact set).
The LLM (this model session as backend) EXTRACTS candidate red flags; the deterministic layer becomes a
GROUNDEDNESS GATE that DISPOSES on whether each `flag` is verbatim-real in the source md AND falls within its
cited section. Net complexity goes down and lands somewhere testable. Then scale as PROOF (not count) — 2 new
records incl. ≥1 advisory the old regex could not reach → corpus explorer 5/14 → 7/14 live.

## Approach

**The subtraction test applied.** `extract_red_flags` has grown ~130 lines of `_SECTION_STOP` /
`_FOOTNOTE_STOP` / `_CITATION` machinery across Phases 11–15 (two-tier anchors → footnote-resume → citation
signatures → glued-handling) and STILL only cleanly parses 7/14 advisories. We already concede in CLAUDE.md
that "the spine ASSISTS, it does not AUTOMATE — complete records need LLM authoring." The evidence the user
surfaced: the extractor's raw output is noise the LLM already cleans. `fin-2025-a003` raw `src_line` 499 =
`"FINCEN ADVISORY A customer that is a U.S.-based escrow company receives funds from an unaffiliated,
foreign-"` — a running-header glued on the front, hyphen-truncated mid-sentence; the clean `flag` text that
shipped in the record was **LLM-authored by stitching across the page break**. The regex is doing the hard
(open) problem badly; the LLM is already doing it well.

**So invert.** "Deterministic validators at boundaries over neural judges at the end" — put the LLM at the
START (extraction, a generative task it is good at) and the deterministic validator at the BOUNDARY (the gate):

1. **md normalizer (`normalize(text)`, pure, stdlib)** — folds the closed FinCEN-md artifact set: running
   headers (`FINCEN ADVISORY` + letter-spaced `F I N C E N` variants), form-feed page breaks, hyphenated
   line-breaks rejoined, smart/curly quotes folded, whitespace collapsed. A finite, known, testable set —
   unlike section structure, which is open-ended.
2. **Groundedness gate (rewire `check_record` traceability)** — each indicator's normalized `flag` must be a
   substring of the normalized source md. **Quote-grounding becomes the traceability authority**, replacing
   `src_line ∈ extractor-output`; `src_line` survives only as an optional hint. Quote-based traceability is
   simpler AND stronger: it checks the actual text, format-agnostic.
3. **Section-cite relevance guard (decision A)** — the indicator's `section` must be locatable in the md AND
   the quote must fall within that section's span. Buys back section-level relevance cheaply, without
   reintroducing a brittle structural parser.
4. **Unchanged dispose-logic** — matrix-consistency (`build_rec_category` cover×data), BUILD_NOW⇒full
   `build_logic`, and shape checks stay deterministic. Only the traceability check inverts.

**Migration is nearly free** — each existing derived-record indicator ALREADY carries its verbatim span in
`flag`, so the 5 committed records migrate by re-validating (adjust only any over-cleaned paraphrase back to a
grounded verbatim span; text stays RAW per the esc()-sole-escaper convention).

**Demote, don't delete (decision B).** `extract_red_flags` + its machinery is kept ONLY as the EFE
`--selftest` regression anchor (proves the parser still reads the canonical clean doc) + an optional scaffold
hint. It stops being the correctness/traceability authority and stops growing. `corpus-status.json` keeps its
SHAPE EXACTLY (so `build.py` + `corpus.html` stay byte-untouched) but its semantics shift: `live` = has a
gate-passing committed record; `derivable: false` = the 2 FATF advisories (`fin-2020-a009`, `fin-2021-a003` —
no enumerated red-flag list); else not-yet-derived. CLEAN/LOW/NEEDS survives only as an informational triage
hint.

**Scale as proof (decision C).** 2 new records — COVID-EIP `fin-2021-a002` (clean, easy) + ONE
previously-unreachable advisory the old extractor flagged LOW/glued (ISIS `fin-2025-a001` OR ransomware
`fin-2021-a004`) — demonstrating the inverted loop reaches advisories the regex could not. This **dissolves
the pymupdf4llm converter option entirely**: the LLM reads the glued md like a human; the gate verifies the
quote is real. Corpus explorer goes 5/14 → 7/14 live.

## Scope

- `scripts/derive_signals.py` — `normalize()` + rewired `check_record` groundedness/section-cite gate;
  `extract_red_flags` demoted to selftest-anchor + scaffold hint (docstring/comment records the demotion);
  `--corpus-status` semantics shift (shape preserved).
- `data/fincen/derived/*.json` — migrate the 5 existing records + author 2 new ones via the inverted loop.
- `data/fincen/corpus-status.json` — regenerated, SAME SHAPE, derivable false only for the 2 FATF advisories.
- `dist/corpus/index.html` — rebuilt (7/14 live).
- `README.md`, `CLAUDE.md` — document the inverted architecture + the honesty shift.

UNTOUCHED (byte-frozen): `index.html`, `corpus.html`, `config/**`,
`dist/{fentanyl,trade-based,elder-financial-exploitation}/`. `corpus.html` is byte-frozen because the
`corpus-status.json` shape is preserved.

## Exit Criteria

- [ ] Groundedness gate + md normalizer land: `normalize()` handles the closed artifact set; `check_record`
      traceability rewired to normalized `flag` ∈ normalized md + a section-cite guard; the escrow STRESS case
      grounds AND a fabricated non-substring flag is rejected (both asserted in `--selftest`); `--selftest`
      still EFE 12+12; stdlib-only, `anthropic` lazy, not imported by index.html/build.py.
- [ ] All 5 committed records (fin-2020-a008, fin-2022-a001, fin-2024-a002, fin-2025-a002, fin-2025-a003) pass
      `--check-derived` under the new gate; any over-cleaned paraphrase adjusted to a grounded verbatim span;
      provenance wording updated where it referenced src_line traceability.
- [ ] `extract_red_flags` demoted to selftest-anchor + scaffold hint (docstring records the demotion);
      `--corpus-status` regenerated keeping the SAME SHAPE (14 entries, same fields); `derivable` false only
      for the 2 FATF advisories; `build.py corpus` + `corpus.html` need NO edit; CLEAN/LOW/NEEDS is an
      informational hint only.
- [ ] 2 new records via the inverted loop (incl. ≥1 previously-LOW/glued advisory whose record notes the
      bypassed failure mode) gate-pass → 7/14 live; each has ≥1 BUILD_NOW with full build_logic; provenance
      marks them LLM-EXTRACTED + gate-checked.
- [ ] `dist/corpus` rebuilt (7/14 live), `--check corpus` ok, `--check all` 4-artifact zero drift;
      `git diff index.html corpus.html config` empty; the 7 derived advisories render through all 4 screens;
      README + CLAUDE document the inverted architecture + the honesty shift + the dissolved converter option.

## Constraints (load-bearing)

- **Complexity must SHRINK, not MOVE** — the whole point is the subtraction test. If the normalizer grows as
  complex as the extractor it replaces, the trade has failed (see Abort).
- **Groundedness ≠ relevance** — the gate proves a quote is REAL TEXT, not that it is a GENUINE red flag. The
  section-cite check buys back section-level relevance cheaply; the two human gates dispose on residual
  relevance. Do NOT reintroduce a full structural parser to chase relevance.
- **EFE 12+12 is the guard rail** — `extract_red_flags` stays the `--selftest` anchor; demoting it must not
  break its canonical clean-doc parse.
- **LLM proposes, deterministic checks dispose (strengthened)** — the LLM now proposes extraction TOO; the
  gate disposes on groundedness. This extends, not violates, the standing principle.
- **Showcase byte-frozen** — `index.html`/`corpus.html`/`config/**` + the 3 typology dists untouched.
  `corpus.html` is frozen because `corpus-status.json` keeps its shape.
- **Deterministic, stdlib-only, authoring-only** — `normalize` + the gate are pure + stdlib; `anthropic`
  lazy; `derive_signals.py` never imported by `index.html`/`build.py`.

## Checkpoints

- T1: if `normalize()` cannot ground the escrow STRESS case (header-glued + hyphen-truncated at raw L499)
  without becoming as complex as `extract_red_flags`, the subtraction test is failing — pause and report
  (the Abort path).
- T4: confirm the previously-LOW/glued advisory genuinely grounds under the gate before committing it as proof.
- T5: confirm `git diff index.html corpus.html config` empty + `--check all` zero drift before declaring done.
- Blocked >3 attempts on a task → ask the user: skip or abort.

## Assumptions

- The FinCEN-md artifact set is genuinely CLOSED (running headers, form-feeds, hyphen-line-breaks, smart
  quotes, whitespace) — a finite normalizer suffices. If a new artifact class appears that the normalizer
  can't fold without parser-like complexity, that is the Abort signal (narrow to the clean records + COVID-EIP).
- The 5 existing records' `flag` fields are close enough to verbatim that migration is re-validation, not
  re-authoring. Verified per-record at T2; over-cleaned paraphrases adjusted to grounded spans.
- A previously-LOW/glued advisory (ISIS fin-2025-a001 or ransomware fin-2021-a004) is readable by the LLM and
  its flags ground verbatim under the gate. If neither grounds cleanly, narrow breadth to COVID-EIP only (the
  Abort path) — do not ship filler.

## Notes

Direction approved by user 2026-06-06: invert the extraction architecture + scale as proof; the structure-
preserving converter (pymupdf4llm) option is DISSOLVED. The reframe vs the Phase-15 follow-up menu: the user
named the fear that "in the end we still rely on LLM authoring" — so rather than keep growing a regex that
the LLM has to clean up after anyway, make the deterministic layer a GATE (it disposes on groundedness), not
a neural-overridden extractor. The honesty revision to record in docs: the spine no longer claims to ASSIST
extraction — it GATES; the LLM extracts + authors; the two human gates dispose. The named trade (recorded in
the Constraints + Abort): groundedness proves a quote is REAL TEXT, not that it is a GENUINE red flag — the
section-cite check (decision A) buys back section-level relevance cheaply, and the two human gates remain the
final dispose. Follow-ups not in scope (later): scale beyond 7/14 (the remaining clean advisories) ·
corpus combination-lift wow beat · FATF non-derivable labeling polish · (carried) elder presentation-values
true-up · fentanyl verbatim re-point · manifest `--fetch` cadence.
