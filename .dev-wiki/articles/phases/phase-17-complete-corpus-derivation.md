---
title: "Phase 17: Complete corpus derivation + delete extract_red_flags (the real subtraction)"
aliases: [complete-corpus-derivation, delete-extract-red-flags, real-subtraction, rf-region-counter, corpus-12-14, inverted-loop-sole-path]
category: phases
tags: [milestone-m7, corpus, extractor, derive-signals, subtraction-test, groundedness, scale-to-complete, dead-code-deletion]
parents: []
created: 2026-06-06
updated: 2026-06-06
source: plan
status: active
ceremony: lite
scope: ["scripts/derive_signals.py", "data/fincen/derived/*.json", "data/fincen/corpus-status.json", "dist/corpus/index.html", "README.md", "CLAUDE.md"]
entry_criteria: "Phase 16 complete + accepted (impl commit bca3612; reviewer ACCEPT 9/10): the extraction boundary INVERTED — the LLM extracts, the deterministic layer GATES (normalize(flag) ⊂ normalize(md) is the traceability authority; rf_region() the section-cite relevance guard). Correctness-path complexity SHRANK but the FILE GREW 1063→1189: decision B retained the now-demoted extract_red_flags alongside the new gate + heavy inversion docstrings. The debrief named 'delete extract_red_flags' as the top Phase-17 candidate but had the dependency backwards — extract_red_flags is off the correctness path yet is the SOLE producer of the extraction/flag_count triage the byte-frozen corpus.html renders for every not-yet-derived advisory. User chose scale-to-complete (7/14 → 12/14) + the real subtraction (delete the dead extractor + the dead --scaffold/--draft/--scaffold-derived authoring stack), unblocked by a cheap rf_region-bounded triage counter, over scale-only / lean-freeze-and-delete."
exit_criteria: "(1) extract_red_flags + the --scaffold/--draft/--scaffold-derived authoring stack (scaffold_config, write_scaffold, draft_judgment, write_draft, _few_shot, _apply_judgment, _derived_skeleton) DELETED; derive_signals.py drops ~1202 → ~700, leaving normalize + rf_region + check_record + the counter + --corpus-status + --selftest (gate-only). (2) A ~12-line rf_region-bounded triage counter lands; --corpus-status regenerates the SAME SHAPE (14 entries, each with derivable/extraction/flag_count), so corpus.html + build.py stay byte-untouched. (3) --selftest passes gate-only (check_record good/bad/para/tiny/shape_bad/dup with a non-extractor EFE fixture; the EFE 12+12 extract_red_flags assertion dropped). (4) Corpus scaled to 12/14 live via the inverted loop (only the 2 FATF advisories fin-2020-a009 + fin-2021-a003 stay non-derivable), or scale-what-passed documented; each new record --check-derived clean + grounded. (5) dist/corpus rebuilt; --check all 4-artifact zero drift; index.html/corpus.html/config/**/build.py + 3 typology dists byte-frozen; README + CLAUDE document the deleted authoring stack (the inverted loop is the sole derivation path), the rf_region-bounded counter, and the 12/14 corpus."
---

# Phase 17: Complete corpus derivation + delete extract_red_flags (the real subtraction)

## Objective

Finish the Phase-16 inversion thesis with the REAL line-count subtraction, and scale the corpus explorer toward
completion. Two halves, sequenced subtraction-first: (A) delete `extract_red_flags` AND the now-dead
deterministic-scaffold + neural-draft authoring stack it feeds — unblocked by a cheap `rf_region`-bounded triage
counter — so `derive_signals.py` drops ~1202 → ~700, leaving a spine that is purely "LLM extracts, deterministic
gate disposes"; (B) on the stripped spine, derive the 5 remaining derivable advisories via the inverted loop →
corpus explorer 7/14 → 12/14 live (only the 2 FATF advisories stay non-derivable).

## Approach

**(A) The subtraction — do first (riskiest, highest-value, the abort rule keys off it).** The Phase-16 debrief
named "delete extract_red_flags" as the top candidate but had the dependency backwards. `extract_red_flags` is
off the correctness path (the LLM extracts, the gate disposes) — but it is the SOLE producer of the
extraction/`flag_count` triage that the **byte-frozen** `corpus.html` renders for every
"derivable-but-not-yet-derived" advisory (the "clean · N flags · not yet derived" chip; `corpus.html:281-284`,
`build.py:373`). A naive delete would force reimplementing a flag-counter — complexity MOVES, not shrinks (the
Phase-16 abort-rule failure mode).

The clean fix, also REQUIRED by the user's "corpus may grow later" answer: add a ~12-line `rf_region`-bounded
triage counter that reuses the already-existing `rf_region(md)` span and counts candidate lines inside it.
`rf_region` already solved "where is the red-flag region"; counting inside it is trivial vs the 130-line
section-finder. The counter (a) replaces `extract_red_flags`' triage role so the deletion is clean, (b) keeps
`--corpus-status` fully REGENERABLE for a future new advisory (honors "may grow later"), (c) is genuinely
smaller.

With the counter as the bridge, the subtraction goes WIDE: delete `extract_red_flags` AND the now-dead
deterministic-scaffold + neural-draft authoring stack it feeds — `--scaffold` / `--draft` / `--scaffold-derived`
(`scaffold_config`, `write_scaffold`, `draft_judgment`, `write_draft`, `_few_shot`, `_apply_judgment`,
`_derived_skeleton`). The inverted loop (LLM extracts → `--check-derived` gate disposes) already replaced all of
it. `derive_signals.py` drops ~1202 → ~700, leaving exactly `normalize` + `rf_region` + `check_record` + the
counter + `--corpus-status` + `--selftest` (gate-only). The spine becomes purely "LLM extracts, deterministic
gate disposes."

**(B) Scale to completion (on the stripped spine).** Derive the 5 remaining derivable advisories via the
inverted loop → 7/14 → 12/14 live (only the 2 FATF advisories `fin-2020-a009` + `fin-2021-a003` stay
non-derivable). Targets: `fin-2026-a001` (health-care, glued-no-separator — the inverted loop's easiest new
target), `fin-2021-a001`, `fin-2024-a001` (Iran-terror, LOW), `fin-2025-a001` (ISIS, LOW), `fin-2022-a002` (EFE
— already the showcase elder typology, duplicative but cheap; completes 12/14). Per-advisory validate-first
against the md; degrade gracefully (skip + leave not-yet-derived; the counter handles its chip) if a LOW/glued
advisory won't pass the gate faithfully.

## Scope

- `scripts/derive_signals.py` — delete `extract_red_flags` + the `--scaffold`/`--draft`/`--scaffold-derived`
  authoring stack; add the `rf_region`-bounded triage counter; rewire `corpus_status_records`; fix `--selftest`
  to gate-only.
- `data/fincen/derived/*.json` — 5 new records via the inverted loop (fin-2026-a001, fin-2021-a001,
  fin-2024-a001, fin-2025-a001, fin-2022-a002).
- `data/fincen/corpus-status.json` — regenerated, SAME SHAPE (14 entries, derivable/extraction/flag_count).
- `dist/corpus/index.html` — rebuilt (12/14 live, or scale-what-passed).
- `README.md`, `CLAUDE.md` — document the deleted authoring stack + the counter + 12/14.

UNTOUCHED (byte-frozen): `index.html`, `corpus.html`, `config/**`, `scripts/build.py`,
`dist/{fentanyl,trade-based,elder-financial-exploitation}/`. `corpus.html` + `build.py` are byte-frozen because
the counter preserves `corpus-status.json`'s SHAPE — no front-end / build edit.

## Exit Criteria

- [ ] `extract_red_flags` + the `--scaffold`/`--draft`/`--scaffold-derived` authoring stack DELETED
      (`grep -cE "def extract_red_flags|def write_scaffold|def write_draft|def draft_judgment|def scaffold_config"`
      == 0); `derive_signals.py` materially smaller (~1202 → ~700), leaving normalize + rf_region + check_record
      + counter + --corpus-status + --selftest.
- [ ] `rf_region`-bounded triage counter lands; `--corpus-status` regenerates a SAME-SHAPE corpus-status.json
      (14 entries, each with derivable/extraction/flag_count); `corpus.html` + `build.py` need NO edit.
- [ ] `--selftest` passes gate-only (check_record good/bad/para/tiny/shape_bad/dup with a non-extractor EFE
      fixture; the EFE 12+12 extract_red_flags assertion dropped).
- [ ] Corpus scaled to 12/14 live via the inverted loop (only the 2 FATF advisories non-derivable), or
      scale-what-passed documented; each new record `--check-derived` clean + every flag grounds
      (normalize(flag) ⊂ normalize(md)).
- [ ] `dist/corpus` rebuilt (12/14 or scale-what-passed); `--check all` 4-artifact zero drift;
      `git diff index.html corpus.html config scripts/build.py` empty + the 3 typology dists byte-untouched;
      headless DOM assertions pass for the new records; README + CLAUDE document the subtraction + the counter +
      12/14.

## Constraints (load-bearing)

- **The counter must SHRINK, not MOVE complexity** — it reuses the existing `rf_region` span; if it grows as
  complex as the `extract_red_flags` it replaces, the subtraction test FAILS (see Abort).
- **corpus-status.json SHAPE is the contract** — 14 entries, each with `derivable`/`extraction`/`flag_count`.
  Preserving it byte-frozens `corpus.html` (`corpus.html:281-284`) + `build.py` (`build.py:373`). Any shape
  change breaks the frozen front-end.
- **The inverted loop is the SOLE derivation path** — quote-grounding (`normalize(flag) ⊂ normalize(md)` via
  `check_record`) is the traceability authority, NOT `src_line ∈ extractor`. The deleted scaffold/draft stack is
  fully replaced by it.
- **Quality over count** — degrade gracefully on a LOW/glued advisory that won't ground faithfully (skip + leave
  not-yet-derived; the counter handles the chip). Never ship filler.
- **Showcase byte-frozen** — `index.html`/`corpus.html`/`config/**`/`build.py` + the 3 typology dists untouched.
- **Deterministic, stdlib-only, authoring-only** — `normalize` + `rf_region` + the counter + the gate are pure +
  stdlib; `derive_signals.py` never imported by `index.html`/`build.py`; the ship artifact never calls an LLM.

## Checkpoints

- T1 (the subtraction): if the `rf_region`-bounded counter can't preserve corpus-status.json's SHAPE / pass
  build.py validation without growing as complex as the `extract_red_flags` it replaces, the subtraction test is
  failing — STOP, keep `extract_red_flags`, narrow to scale-only (the Abort path).
- T3 (LOW advisories): validate faithfulness per advisory BEFORE authoring; degrade to skip if one won't pass
  the gate at acceptable quality (the deletion still lands clean — it's counter-gated, not scale-gated).
- T5: confirm `git diff index.html corpus.html config scripts/build.py` empty + `--check all` zero drift before
  declaring done.
- Blocked >3 attempts on a task → ask the user: skip or abort.

## Assumptions

- The `rf_region` span already located by Phase 16 is a good-enough region to count candidate red-flag lines for
  triage. If counting inside it needs parser-like logic to be honest, that is the Abort signal (narrow to
  scale-only).
- The 5 remaining derivable advisories are readable by the LLM and their flags ground verbatim under the gate.
  If a LOW/glued advisory won't ground cleanly, degrade to scale-what-passes — do not ship filler.
- The EFE (`fin-2022-a002`) corpus record is duplicative of the showcase elder typology but cheap; it completes
  12/14. Degrade-first candidate if size bites; the counter handles it gracefully if left not-derived.

## Notes

Direction approved by user 2026-06-06: scale-to-complete (7/14 → 12/14) + the real subtraction (delete
`extract_red_flags` + the dead `--scaffold`/`--draft`/`--scaffold-derived` authoring stack), unblocked by a
cheap `rf_region`-bounded triage counter — over scale-only, and over lean-freeze-and-delete (which the
"corpus may grow later" answer took off the table: freezing triage into a committed corpus-status.json + deleting
the generator would leave un-regenerable stale triage). The debrief's "real subtraction" was real but had the
dependency backwards: the deletion is UNBLOCKED by the cheap counter, NOT by full scaling — `extract_red_flags`
is off the correctness path but is the sole producer of the triage the byte-frozen `corpus.html` renders. The
counter (reuses the existing `rf_region` span, counts candidate lines) replaces that triage role, keeps
`--corpus-status` regenerable, and is materially smaller than the 130-line section-finder. This is the genuine
line-count shrink decision B deferred from Phase 16 (the file GREW 1063→1189 then; this drops it ~1202 → ~700).
Follow-ups not in scope (later): tighten the coarse `rf_region` if scaling widely · FATF non-derivable labeling
polish · corpus combination-lift wow beat · (carried) elder presentation-values true-up · fentanyl verbatim
re-point · manifest `--fetch` cadence.
