---
type: phase-note
phase: 27
slug: phase-27-assessment-findings
created: 2026-06-07
---

# Phase 27 — Corpus output-quality assessment (READ-ONLY findings)

> Produced by the `ph27-corpus-quality-assessment` dynamic workflow (44 agents: 42 per-doc audits + 1 build-animation gap analysis + 1 synthesis) over the committed corpus, plus a deterministic metrics pass (highlight hit-rate via corpus.html's exact match logic, markitdown-artifact density, flag-fragment signals, red_flag shape). NO ship/data/dist mutation. Tier tally: **PRESENTATION_ONLY 39 · RE_TRANSLATE 1 · RE_EXTRACT 2** (synthesis promotes fintrac-professional-ml → RE_EXTRACT, so effectively 3 RE_EXTRACT).

## Synthesis report

This is a synthesis task — I have all the inputs I need (per-doc assessments, tier tally, build-animation gap analysis). No file reads required; the diagnosis is established. Writing the findings report directly.

## Verdict — is it shippable, and what's the real problem

**Not shippable as-is, but the fix is shallow and almost entirely presentation — not data or gate.** The engineer's "brutally bad" Read-advisory beat is real, but the brutality lives in `corpus.html`'s render layer, not in the corpus. The grounding system works: across 42 docs the verbatim flags are real whole single-indicator quotes, register scores are excellent (39/42 at 4-5), and the translations mostly hit the showcase oracle bar. What you're seeing on screen is **raw markitdown displayed unprocessed** — glued running headers (`FINCEN ADVISORYFinancial Indicators`), trailing footnote digits (`.33`, `NPO84`), tab-between-every-word soup, page-number lines, and hyphen-wrap newlines — plus a **highlight matcher too literal to survive those same artifacts** (the verbatim flag grounds against `normalize()`'d md but is matched against the raw displayed text, so it misses). The build animation is genuinely incomplete (no run spinner, no gate hold, no proposal grid, no lift panel). Fix the article render, fix the highlighter, finish the build beat, re-extract 3 docs — and it ships. **Keep the grounding gate untouched; it is the compliance firewall.**

## Systemic problems, ranked

1. **Raw-markitdown article render (hits ~all 42 docs — the dominant defect).** The displayed source article is unprocessed markitdown. Every doc carries some mix of: glued running headers (`FINCEN ADVISORY…`, `FINCEN ALERT…`, `F I N C E N A D V I S O R Y`, `OPERATIONAL ALERT 7/8`, `OPERATIONAL BRIEFTHEME`), trailing footnote digits glued to sentence ends (`.33`, `variants,35`, `practices.83`, `NPO84`), bare page-number lines, footnote runs interleaved between red-flag bullets, hyphen-wrap newlines (`health\ncare`), and in the worst cases **tab-between-every-word soup** (`Transactions\trelated\tto\tpayments…` — fin-2023-alert004, fin-2024-alert004, fin-2024-alert005). This is the single highest-leverage fix: a display-time markitdown cleaner in `corpus.html` lifts the perceived quality of every doc at once. **No data change.**

2. **Highlight reliability (the second-order victim of #1).** Several docs highlight well below 100% because the matcher is defeated by the *same* artifacts the article render needs to strip: footnote-shredded spans, glued running headers mid-flag, hyphen-wrap/paragraph-reflow newlines, smart quotes, mid-quote double-spaces. Worst cases: **fin-2021-a001 (38%)**, **fin-2024-a001 (56%)**, fin-2021-a002 (67%), fin-2022-a002 (83%), fin-2026-a001 (~83%), fin-2022-alert002 (88%), fintrac-real-estate (94%), fintrac-underground-banking (93%), plus "partial" on fin-2025-a001 / fin-2024-a001 / fintrac-cannabis. The fix is one change applied twice: **normalize both sides before matching** (run the displayed article through the *same* normalization the grounding gate already uses — collapse running headers, footnote digits, smart quotes, hyphen-wraps, whitespace — then substring-match the normalized flag against the normalized display text). This makes the highlighter resilient without touching the grounding authority. **No data change.**

3. **The build animation is unfinished (the engineer's second named complaint).** Medium severity, isolated to the Signal/build beat — see the dedicated section below. Self-contained `corpus.html` work, no data.

4. **3 docs with glued/fragment verbatim flags (the only data-touching defects).** A small, named set where the *verbatim span itself* is wrong — heading-glued-to-body walls or full-paragraph definitions instead of crisp single-clause quotes. These need re-extraction through the inverted loop + gate (data + gate-grounded), not a render fix. They are the only items that unfreeze a `derived/*.json`. Listed explicitly below.

5. **1 doc needs a values-only re-translate (register, not data).** fin-2022-a001 — register_score 3, two red_flags read as compressed restatements of the verbatim quote rather than terse mechanism-named oracle indicators. Cheapest possible data touch: `red_flag` **values only**, grounding/verbatim untouched.

## Tier distribution + the doc lists

**Tally: PRESENTATION_ONLY 39 · RE_TRANSLATE 1 · RE_EXTRACT 2** — *with one correction below.*

### RE_EXTRACT (data + gate — re-extract the verbatim span through the inverted loop, re-ground)
- **fin-2026-alert002** — 13 of 14 verbatim flags are >240-char paragraph walls: each glues the bold label + the entire multi-sentence definition with embedded newlines (e.g. IND-13 ~430 chars, IND-07 full label + 5-line front-company paragraph). Re-extract to a tight span (label + lead clause). Register is clean; extract is the defect.
- **ofac-maritime-shipping** — 2 of 7 flags (IND-04, IND-05) glue the section heading onto the following body paragraph via embedded newlines; IND-04 is a >240-char wall. Re-extract to the heading line only (a tighter grounded span).

### Promote to RE_EXTRACT (the tally undercounts by one — flag for the replanner)
- **fintrac-professional-ml** — tiered `PRESENTATION_ONLY` but `extract_score:2` with worst-examples showing **lowercase-start, double-newline-glued multi-clause fragments** (IND-03 three clauses glued by `\n\n`; IND-22 semicolon fragment). These are genuine span defects, not pure render. **Recommend re-extracting it alongside the other two** — treat RE_EXTRACT as **3 docs**, not 2. (Cross-check the other `extract_score:2` doc, fin-2024-alert005, during replan — its worst-examples read as pure tab-soup render with 100% highlight, so it likely stays PRESENTATION_ONLY, but confirm.)

### RE_TRANSLATE (data — `red_flag` values only, grounding/verbatim untouched)
- **fin-2022-a001** — register_score 3; IND-02 and IND-04 read as verbatim restatements lacking an AML mechanism name. Re-translate values only.

### PRESENTATION_ONLY (39 docs — corpus.html render/highlight only, NO data change)
All remaining: fin-2020-a008, fin-2021-a001, fin-2021-a002, fin-2021-a004, fin-2022-a002, fin-2024-a001, fin-2024-a002, fin-2025-a001, fin-2025-a002, fin-2025-a003, fin-2026-a001, fin-2020-alert001, fin-2022-alert002, fin-2022-alert003, fin-2023-alert001, fin-2023-alert002, fin-2023-alert003, fin-2023-alert004, fin-2023-alert005, fin-2023-alert006, fin-2023-alert007, fin-2024-alert003, fin-2024-alert004, fin-2024-alert005, fin-2025-alert001, fin-2025-alert002, fin-2026-alert001, ofac-sham-transactions, ofac-virtual-currency, fintrac-cannabis, fintrac-human-trafficking, fintrac-illegal-wildlife, fintrac-online-child-exploitation, fintrac-professional-ml *(unless promoted per above)*, fintrac-real-estate, fintrac-romance-fraud, fintrac-synthetic-opioids, fintrac-terrorist-financing, fintrac-underground-banking.

*Note: ofac-sham-transactions has 5/7 full-paragraph walls but was tiered PRESENTATION_ONLY (render truncation/expand-UI, not re-extract). The replanner should sanity-check it against the maritime call — if the team decides paragraph walls are a span defect rather than a display-truncation concern, it joins RE_EXTRACT; the assessment's position is it's a display-truncation fix.*

## Build-animation gap + fix spec

From the gap analysis (severity: **medium**):

| Gap | What's missing |
|---|---|
| **build_log_gap** | No run spinner, no gate hold, and the build-log isn't presented in a proposal grid (unlike the six-act showcase's Act-4 beat) |
| **lift_gap** | No lift-side panel; **firestat correctly omitted** (keep it out) |

**Fix spec (corpus.html only, no data):**
1. **Add a `run` step before `markStep`, and hold the gate** — give the build-log the showcase's run-spinner → gate-hold rhythm instead of jumping straight to the marked steps.
2. **Render the build-log in a proposal grid** — match the Act-4 proposal-grid layout.
3. **Add a lift-side panel** for the combination-lift beat — **keep firestat out** (per analysis; it's correctly omitted today).

This animates the **real `build_logic`** (structural, no numbers). The combination-lift figures stay the **generic illustrative template behind the loud "pending calibration — NOT measured on this document" tag** — no per-doc fabrication.

## Recommended build plan for the Phase-27 replan

Ordered by leverage. **Unfreezes: `corpus.html`, `dist/corpus`, tests, docs** for presentation work; **3-4 `derived/*.json` records** for the data-touching tasks. **Grounding gate (`normalize`/`rf_region`/`check_record`) stays byte-frozen. No fabricated numbers.**

**T1 — Article render cleaner (corpus.html) — highest leverage, hits all 42 docs.**
Add a display-time markitdown sanitizer for the Read-advisory body: strip glued running headers (`FINCEN ADVISORY…`, `FINCEN ALERT…`, `F I N C E N…`, `OPERATIONAL ALERT/BRIEF…`), trailing/inline footnote digits, bare page-number lines, interleaved footnote runs, hyphen-wrap newlines, and **tab-between-every-word soup** (the alert004/005 cases). This is a render transform only — the stored `source_md` and the grounding surface are untouched. *Reuse the existing `normalize()` logic as the spec for what to strip — don't reinvent it.*

**T2 — Highlight resilience (corpus.html) — depends on T1's normalizer.**
Match by **normalizing both sides**: run the flag and the displayed (post-T1) article through the same normalization, then substring-match. This fixes the 38%/56%/67%/83%/88%/94% misses without touching the grounding gate (which already grounds correctly against `normalize()`'d md — the bug is the *display* match, not the gate). Target: ~100% highlight across all docs whose flags ground.

**T3 — Finish the build animation (corpus.html) — the engineer's second named complaint.**
Per the fix spec: add `run` before `markStep` + gate hold; render in a proposal grid; add the lift-side panel; keep firestat out. Animates real `build_logic`; lift stays the generic illustrative template behind the loud pending-calibration tag.

**T4 — Re-extract the 3 span-defect docs (data + gate) — through the inverted loop, re-grounded.**
- fin-2026-alert002 (13/14 paragraph walls → label + lead clause)
- ofac-maritime-shipping (IND-04/IND-05 heading-glued-to-body → heading line only)
- fintrac-professional-ml (lowercase-start / `\n\n`-glued multi-clause fragments → clean single-indicator spans)
Each new verbatim span must re-pass `check_record` quote-grounding (`normalize(flag) ⊂ normalize(md)` inside `rf_region`). The gate logic does not change — only these records' `flag` values. *Confirm fin-2024-alert005 and ofac-sham-transactions during planning; the assessment reads them as render/display-truncation, not span defects.*

**T5 — Re-translate fin-2022-a001 (data, values-only) — cheapest data touch.**
Re-translate IND-02 / IND-04 `red_flag` **values only** to the terse mechanism-named oracle register (reuse the Phase-26 translate→adversarial-verify workflow). Verbatim `flag` + grounding untouched; `red_flag` SHAPE gate still passes.

**T6 — Regate + rebuild + harness.**
`--check all` (zero drift on the frozen set) → re-run `--check-derived` on the 3-4 touched records → `build.py corpus` → extend `tests/corpus-explorer.test.mjs` with article-render-cleanliness + highlight-hit-rate asserts and the finished build-beat asserts → walk `tests/smoke-checklist.md`. Verify the frozen set (showcase, source md, corpus-status.json, typology-map.json, derive_signals.py core) stays byte-clean.

**Sequencing note:** T1→T2 are the unlock (39 of 42 docs ship on presentation alone) and should land first; T3 is parallel-safe (independent corpus.html region); T4/T5 are the only data touches and are small + isolated. **Do T1+T2 first to confirm the "brutally bad" verdict flips on presentation alone before opening any `derived/*.json`** — that validates the diagnosis and keeps the data-touch surface as small as the evidence justifies.

## Per-doc table (data-touch first, then worst highlight)

reg=register_score (red_flag vs oracle), ext=extract_score (verbatim flag readability), hl=highlight, hit%=deterministic highlight hit-rate, n=indicators, long=#flags >240ch, lc=#flags starting lowercase.

| doc | tier | reg | ext | hl | hit% | n | long | lc |
|-----|------|----:|----:|----|-----:|--:|-----:|---:|
| fin-2026-alert002 | RE_EXTRACT | 5 | 2 | ok | 100% | 14 | 13 | 0 |
| ofac-maritime-shipping | RE_EXTRACT | 5 | 3 | ok | 100% | 7 | 1 | 0 |
| fin-2022-a001 | RE_TRANSLATE | 3 | 4 | ok | 100% | 5 | 1 | 0 |
| fin-2021-a001 | PRESENT | 5 | 4 | poor | 37% | 16 | 13 | 0 |
| fin-2024-a001 | PRESENT | 4 | 4 | partial | 55% | 9 | 8 | 0 |
| fin-2021-a002 | PRESENT | 5 | 4 | partial | 66% | 3 | 1 | 0 |
| fin-2025-a001 | PRESENT | 5 | 4 | partial | 81% | 11 | 6 | 0 |
| fin-2022-a002 | PRESENT | 5 | 5 | ok | 83% | 12 | 0 | 0 |
| fin-2026-a001 | PRESENT | 5 | 4 | partial | 83% | 24 | 12 | 0 |
| fin-2022-alert002 | PRESENT | 4 | 4 | partial | 88% | 17 | 7 | 0 |
| fintrac-cannabis | PRESENT | 5 | 4 | partial | 90% | 21 | 2 | 0 |
| fintrac-underground-banking | PRESENT | 5 | 4 | ok | 92% | 14 | 2 | 0 |
| fintrac-real-estate | PRESENT | 5 | 4 | partial | 93% | 33 | 2 | 0 |
| fin-2020-a008 | PRESENT | 5 | 4 | ok | 100% | 10 | 4 | 0 |
| fin-2021-a004 | PRESENT | 5 | 4 | ok | 100% | 12 | 5 | 0 |
| fin-2024-a002 | PRESENT | 5 | 4 | ok | 100% | 14 | 7 | 0 |
| fin-2025-a002 | PRESENT | 5 | 4 | ok | 100% | 16 | 16 | 0 |
| fin-2025-a003 | PRESENT | 5 | 4 | ok | 100% | 18 | 9 | 0 |
| fin-2020-alert001 | PRESENT | 5 | 5 | ok | 100% | 6 | 2 | 0 |
| fin-2022-alert003 | PRESENT | 5 | 4 | ok | 100% | 22 | 5 | 0 |
| fin-2023-alert001 | PRESENT | 5 | 5 | ok | 100% | 8 | 1 | 0 |
| fin-2023-alert002 | PRESENT | 5 | 4 | ok | 100% | 9 | 2 | 0 |
| fin-2023-alert003 | PRESENT | 5 | 5 | ok | 100% | 10 | 0 | 0 |
| fin-2023-alert004 | PRESENT | 5 | 3 | ok | 100% | 9 | 2 | 0 |
| fin-2023-alert005 | PRESENT | 5 | 4 | ok | 100% | 14 | 7 | 0 |
| fin-2023-alert006 | PRESENT | 4 | 4 | ok | 100% | 7 | 4 | 0 |
| fin-2023-alert007 | PRESENT | 4 | 4 | ok | 100% | 10 | 2 | 0 |
| fin-2024-alert003 | PRESENT | 5 | 4 | ok | 100% | 7 | 7 | 0 |
| fin-2024-alert004 | PRESENT | 5 | 3 | ok | 100% | 9 | 3 | 0 |
| fin-2024-alert005 | PRESENT | 5 | 2 | ok | 100% | 19 | 3 | 0 |
| fin-2025-alert001 | PRESENT | 5 | 4 | ok | 100% | 10 | 5 | 0 |
| fin-2025-alert002 | PRESENT | 5 | 4 | ok | 100% | 14 | 9 | 0 |
| fin-2026-alert001 | PRESENT | 5 | 5 | ok | 100% | 13 | 3 | 0 |
| ofac-sham-transactions | PRESENT | 5 | 3 | ok | 100% | 7 | 5 | 0 |
| ofac-virtual-currency | PRESENT | 5 | 5 | ok | 100% | 5 | 0 | 0 |
| fintrac-human-trafficking | PRESENT | 5 | 4 | ok | 100% | 57 | 0 | 0 |
| fintrac-illegal-wildlife | PRESENT | 5 | 4 | ok | 100% | 16 | 1 | 0 |
| fintrac-online-child-exploitation | PRESENT | 5 | 4 | ok | 100% | 44 | 5 | 0 |
| fintrac-professional-ml | PRESENT | 5 | 2 | ok | 100% | 26 | 4 | 19 |
| fintrac-romance-fraud | PRESENT | 5 | 4 | ok | 100% | 28 | 1 | 0 |
| fintrac-synthetic-opioids | PRESENT | 5 | 5 | ok | 100% | 15 | 0 | 0 |
| fintrac-terrorist-financing | PRESENT | 4 | 4 | ok | 100% | 13 | 0 | 0 |

## Build-animation gap (severity: medium)

- **build_log_gap:** No run spinner, no gate hold, buildlog not in a proposal grid
- **lift_gap:** No liftside panel; firestat correctly omitted
- **fix_spec:** add run before markStep and hold the gate; use a proposal grid; add a liftside panel, keep firestat out

## Deterministic aggregate

- corpus highlight hit-rate: 604/634 = 95.3% (misses concentrate in 8 docs; fin-2021-a001 worst at 38%)
- register: 36 docs @5, 5 @4, 1 @3 — Phase-26 translations largely hold; the perceived "subpar" was the presentation dragging the whole beat down
- extract: 7 @5, 28 @4, 4 @3, 3 @2 — the @2 set (fin-2026-alert002, fintrac-professional-ml, fin-2024-alert005) is the re-extract candidate pool
