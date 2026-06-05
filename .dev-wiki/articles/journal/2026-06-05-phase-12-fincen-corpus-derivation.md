---
title: "Phase 12: FinCEN corpus derivation foundation (deterministic spine all-14 + LLM proof slice)"
aliases: []
category: journal
tags: [milestone-m7, authoring-pipeline, derivation, corpus, build-recommendation, llm-backend, deterministic-spine]
parents: [phase-12-fincen-corpus-derivation]
created: 2026-06-05
updated: 2026-06-05
source: debrief
duration: ~120min
---

# Phase 12: FinCEN corpus derivation foundation

Built the backend for an EXPANDED, singular FinCEN demo (eventual: the user picks one of 14 advisories and
watches the loop derive its coverage → build recommendations → signal). This phase = the **deterministic
spine validated across all 14 advisories** + the **LLM-backend derivation proven on a 2-advisory slice**,
where the LLM backend is THIS session (no API key — the Phase-11 T4 recorded-run substitution). Boundary
preserved + extended: the LLM PROPOSES status/data + build recommendation + build logic; the deterministic
spine DISPOSES (schema/shape · build-rec consistency vs the cover×data matrix · traceability to a red-flag md
line). Backend-only — `index.html` + `build.py` + `config/schema.md` untouched. Lite, all 5 tasks complete +
two user-requested post-completion refinement passes. READY FOR COMPLETION. Opens **M7 (corpus-backed demo)**.

## What Happened

- **T1 — commit the corpus (S).** The 14 advisory md were already converted on disk (gitignored) + network
  blocked in-session → no acquisition. Un-gitignored `data/fincen/*.md` (dropped the `*.md` ignore + the
  EFE `!`-exception; `raw/` stays local), staged all 14. Reverses Phase-10's no-bulk-md call (justified —
  the corpus now backs the demo). public-domain FinCEN (17 USC §105).
- **T2 — generalize `extract_red_flags` + `--corpus` (L).** Rewrote the EFE-only anchor logic as a
  corpus-wide section-FINDER: anchors on INTRO sentences (forward "red flags … may include/as follows/
  listed below/described below" + reverse "the following … red flag") AND short HEADERS (Title-case +
  connectors, no "of <topic>" clause = a title), coalesces a same-label header+intro pair (≤15 lines), spans
  to the next anchor/footnote/stop. `--corpus` 3-way report — CLEAN/LOW-CONFIDENCE/NEEDS-ATTENTION via
  `extraction_quality`. EFE held at 12+12 throughout (the regression guard). DISCOVERY: the corpus is
  markedly heterogeneous (no-blank-separator lists, letter-spaced "F I N C E N A D V I S O R Y" page headers,
  footnotes glued to lists) — the abort-rule section-FINDER-that-FLAGS is the right call vs a brittle
  universal regex.
- **T3 — deterministic checks (M).** Pure `build_rec_category(status, data)` = the 3×3 matrix (covered→COVERED ·
  gap+available→BUILD_NOW · gap+partial→BUILD_ENRICH · gap+insufficient→SOURCE_DATA · partial+available/
  partial→ENHANCE · partial+insufficient→MONITOR). `check_build_rec` rejects any contradiction; `check_record`
  disposes a derived record on 3 axes (build-rec consistency, src_line traceability to an extracted red-flag
  line, BUILD_NOW⇒full build_logic / COVERED·SOURCE_DATA⇒none). `_checks_selftest` folded into `--selftest`.
- **T4 — LLM-backend derivation, 2-advisory proof slice (M).** `--scaffold-derived` emits a skeleton (one
  indicator per extracted red flag, src_line traceable, empty judgment) → `data/fincen/derived/<id>.json`;
  I (THIS session, no key) filled the judgment; `--check-derived` disposed. **fin-2022-a001** (kleptocracy,
  "the following" format, 5 ind, 2 BUILD_NOW) + **fin-2024-a002** (PRC precursor chemicals, header format,
  14 ind, 4 BUILD_NOW; full spread BUILD_ENRICH=2·BUILD_NOW=4·COVERED=1·ENHANCE=4·MONITOR=1·SOURCE_DATA=2).
  BOUNDARY proven: tampering IND-12 covered→BUILD_NOW is REJECTED. DISCOVERY (refines T2): added an
  intro-noise filter dropping the standard FinCEN caveat boilerplate that bled into the first block.
- **T5 — docs + verify (S).** Docstring + README + CLAUDE document `--corpus`/`--scaffold-derived`/
  `--check-derived`, the spine, the checks, and the LLM-proposes/checks-dispose boundary.
- **POST-IMPL WIDENING (user ask).** Asked to push CLEAN past 5: added a two-tier fallback (loose
  "Red Flags <Related to/Potentially Indicative of …>" headers + weak "identified red flags" intro, used
  ONLY when no Tier-1 anchor — so EFE + the clean advisories are untouched), the "described below" lead-in,
  and recalibrated `_MAX_FLAG_CHARS` 500→600 (corpus-wide: genuine single flags top 573, glued blocks ≥630
  — a clean gap; 500 was EFE-only calibration). Corpus 3→8 CLEAN; all new extractions spot-verified genuine.
- **POST-REVIEW FILTERS (user ask).** After inspecting all 103 extracted rows together, the user flagged
  artifact classes. Added: drop blocks that are themselves a red-flag HEADER (killed 3 mis-counted
  "Red Flags Associated with…" sub-headers in fin-2025-a002) + drop FOOTNOTE/CITATION blocks (section-stop now
  catches a bare "81." marker; a `_CITATION` filter drops "(Mon DD, YYYY)"-ending cites — killed the IC3
  citation in fin-2025-a001). Honest consequence: fin-2025-a001 dropped to its 2 real flags → LOW (it had only
  been "clean" because the citation padded the count). **Final: 7 CLEAN · 3 LOW · 4 NEEDS.**

## Decisions Made

(Captured in `_CURRENT_STATE` ## Recent Decisions at plan time — lite ceremony writes no decision articles.)
**Backend-only** foundation (user chose it over folding a minimal selectable demo view in); destination = a
**singular** corpus-backed demo (user picks an advisory), NOT 14 demos; derived records are an analytical
artifact, the 3 hand-curated typologies stay the showcase. **LLM backend = this session, NO key**;
deterministic spine (extract + matrix + traceability) disposes. **Commit the full corpus md** (reverses
Phase-10 no-bulk-md). Implementation decisions: **two-tier anchors** (Tier-2 only when Tier-1 empty — keeps
EFE safe), **threshold recalibrated 500→600** (principled, corpus-wide gap), and the load-bearing framing
the user surfaced — **the spine ASSISTS but does not AUTOMATE**: a complete, demo-quality derived record
still requires LLM-backend authoring (judgment + build logic + pruning residual artifacts); documented.

## Problems Solved

- **Heterogeneous corpus.** A single EFE-anchored regex can't parse 14 differently-structured advisories →
  a section-FINDER with Tier-1/Tier-2 anchors + a CLEAN/LOW/NEEDS report that flags non-conformers honestly.
- **EFE regressions (twice).** Generalizing kept breaking EFE's 12+12 — first the "Behavioral Red Flags"
  header + "may include" intro were >8 lines apart (spurious section); fixed with same-label coalescing in a
  wider window. Then the broad reverse intro caught EFE's topic sentence; fixed by requiring a real list
  lead-in. The two-tier fallback finally isolated EFE (it always has Tier-1) from the loose patterns.
- **Bogus counts vs honest flags.** A glued (no-blank-separator) list yielded one giant block → reported as
  "1 flag." Added `extraction_quality` (max-block-length + count gate) to mark those LOW, not a false count.
- **Artifact pollution.** Inspecting all 103 rows surfaced sub-headers, footnote citations, intro-tail
  boilerplate, and (i)/(ii) over-segmentation counted as flags → header-block + citation + intro-noise filters
  (the fuzzier intro-tail / sub-part cases left to the human gate).

## Artifacts Changed

- `scripts/derive_signals.py` (major: generalized `extract_red_flags` section-FINDER + Tier-2 + filters;
  `extraction_quality` + `--corpus`; `build_rec_category`/`check_build_rec`/`check_record` + `_checks_selftest`;
  `_derived_skeleton`/`--scaffold-derived`/`--check-derived`)
- `data/fincen/*.md` (NEW — 14-advisory corpus committed; un-gitignored)
- `data/fincen/derived/fin-2022-a001.json`, `fin-2024-a002.json` (NEW — LLM-backend-derived + checked records)
- `.gitignore` (un-ignore `data/fincen/*.md`)
- `README.md`, `CLAUDE.md` (corpus-derivation section + the assists-not-automates caveat)

## Related

- [[phase-12-fincen-corpus-derivation|Phase 12: FinCEN corpus derivation foundation]] — parent phase
- [[phase-11-automated-derivation|Phase 11]] — the LLM-proposes/validator-disposes boundary, extended here
- [[phase-10-fincen-corpus-crawler|Phase 10]] — produced the manifest + the corpus this phase commits + derives

## Health Delta

No automated test framework (demo project). New verification capability: `--corpus` (corpus-wide extraction
report) + `--check-derived` (record disposer) + an extended `--selftest` (extraction 12+12 AND the
deterministic checks). Authoring deps unchanged (anthropic still authoring-only + LAZY — the session-as-backend
path needs no SDK). Engine untouched (`git diff index.html` empty); `build.py` + `config/schema.md` untouched;
`build.py --check all` zero drift on all 3 ship typologies; deterministic layer stdlib-only.

### Review Gate

Size-gated reviewer dispatched (5 tasks ≥ 4). **Score 8/10, Verdict: revise → all findings fixed inline.**
Load-bearing confirmations: the **EFE 12+12 guard is ROBUST, not luck** (the reviewer traced the coalescing
margins — header→intro distances 10 and 4 vs the ≤15 window; the failure mode is a LOUD selftest exit, never
a silent miscount), the `_MAX_FLAG_CHARS=600` calibration matches the corpus (largest legit flag 573), both
derived records' AML quality + traceability are coherent, docs accurate, and **no bad record can reach the
ship boundary** (derived records never hit build.py/schema). Three fixable gaps in the disposer itself, all
closed pre-commit: **[HIGH]** `check_record` BUILD_NOW branch validated build_logic key *presence* only — now
validates SHAPE (every field a non-empty string, `features` a non-empty `list[str]`); **[MEDIUM]**
`--check-derived` on malformed JSON threw a raw traceback — now a clean `sys.exit`; **[MEDIUM]** traceability
checked membership not injectivity — now also asserts unique indicator ids + distinct src_lines. `--selftest`
extended to assert the shape-hole + dup-id are caught. Both committed records still pass; corpus 7/3/4,
EFE 12+12, engine/build/schema clean, zero drift — all unchanged after the fixes.

### Retro (triggered — 10 completed phases, 10 % 5 == 0; dims 1–3)

- **Blockers:** none this session.
- **Reversals:** deliberate + justified — committed the corpus md (reverses Phase-10 no-bulk-md, now the corpus
  backs the demo); recalibrated the quality threshold 500→600 (the first value was EFE-only).
- **Corrections:** healthy self-correction throughout — the EFE 12+12 invariant regressed TWICE during
  generalization and was caught + fixed each time (loud selftest), extraction artifacts were surfaced via the
  user's review-the-raw-output ask and filtered, the disposer's shape-hole was caught by the review gate.
- **Meta-lesson:** markitdown-converted real-world corpora need EMPIRICAL calibration (thresholds, anchor
  patterns, artifact filters tuned against the actual 14 docs), not first-guess constants. No systemic issue.

### Gate Compliance

`<!-- gate-log:phase-12 direction=approved delivery=… -->`. Direction gate approved 2026-06-05 (backend-only).
Delivery gate set to `accepted` only after the commit verifiably lands (D3 — gate-state follows git-state).

## Soft Observations / Phase N+1 Candidates

- **Phase 13 — the demo scope expansion (the payoff):** advisory-selection front-end + per-indicator
  build-rec render, driven by the derived corpus. This is the destination the backend now enables.
- **Glued-list splitting:** the 2 genuine NEEDS (`fin-2021-a004` ransomware, `fin-2026-a001` health-care
  fraud) have real lists with NO blank separators (markitdown dropped the bullets). A targeted glued-block
  splitter (or LLM-assisted extraction) would recover them — deliberately deferred (risks the clean cases).
- **Exclude the 2 FATF advisories** (`fin-2020-a009`, `fin-2021-a003`) from the derivable corpus — they're
  jurisdiction lists with no red-flag indicators; NEEDS-ATTENTION is correct, not a gap to fix.
- **Scale the LLM-backend derivation** to the remaining 5 CLEAN advisories (the proof slice was 2) —
  reminder: this requires authoring from the model session, the spine only assists.
- **Residual extraction artifacts:** the intro-tail line in `fin-2020-a008` + the (i)/(ii) over-segmentation
  in `fin-2021-a002` survive the filters; the human gate prunes them, but a tighter intro-tail filter is cheap.
- **EFE-as-derived-record validation:** derive EFE via the corpus path and diff against the hand-authored
  elder ship config — a strong end-to-end check of the LLM-backend derivation quality.

## Activation Quality

No `active-knowledge.md` (lite phase, none generated) — step skipped.
