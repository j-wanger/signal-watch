---
title: "Phase 23: FINTRAC depth — Operational Alerts + Operational Briefs (3→10) (M7)"
aliases: []
category: journal
tags: [corpus, multi-source, fintrac, depth, scale, gate, crown-copyright, operational-brief, inverted-anchor]
parents: [phase-23-fintrac-depth]
created: 2026-06-06
updated: 2026-06-06
source: debrief
duration: ~1 session (post-compaction estimate)
---

# Phase 23: FINTRAC depth — Operational Alerts + Operational Briefs (3→10)

## What Happened
- Grew FINTRAC corpus source #4 from 3 derived Operational Alerts to **10** strategic-intel products
  (9 OAs + 1 real-estate Operational BRIEF) — "Canadian depth" for the demo's audience (a Canadian bank).
  Reused the Phase-20 CORPUS_SOURCES registry + the inverted-loop derivation + the quote-grounding gate;
  the grounding core (`normalize`/`check_record`) stayed **byte-UNTOUCHED** — only the rf_region relevance
  anchors widened. NO new source, NO non-negotiable change, NO `build.py`/`corpus.html` structural edit.
- **T1** acquired + markitdown-converted 7 NEW FINTRAC docs via `--source data/fintrac`
  (`acquire_fincen.py` `_to_pdf_url` + `pdf_to_md.py` provenance both needed NO edit — confirmed the
  Phase-22 finding); `index.json` 3→10. Per-doc triage: 4 anchor AS-IS under the forward FINTRAC anchors,
  3 use an INVERTED "Indicators of <X>" heading. Captured the 39-md FinCEN+OFAC+existing-FINTRAC
  rf_region BASELINE — the regression reference for T2.
- **T2 (L, the gate change)** the PLANNED literal "TABLE OF INDICATORS" anchor was a MISREAD — the
  real-estate Brief's section heading is markitdown-FRAGMENTED ("4. INDICATORS OF MONEY" / "LAUNDERING
  IN REAL ESTATE"); the actual derivation surface is the inverted form. Added `_RF_HEADER_FINTRAC_INV`
  (two narrow branches: (a) "of <ML/TF>" with a CONNECTOR-gated trailing clause + `:?$` that EXCLUDES the
  boilerplate sentence "Indicators of <ML/TF> can be thought of as red flags …" opening the 3 existing
  OAs; (b) "relating to | associated with <topic>" — connectors the boilerplate never uses → 0 collision).
  REGRESSION CLEAN: **0 of 39** existing rf_regions shifted; all 35 prior records `--check-derived` clean;
  `--selftest` +4 bidirectional fixtures (3 positive headings + 1 negative boilerplate).
- **T3 (the derivation)** 7 docs via the inverted loop (one extraction subagent per doc, self-gated then
  independently re-checked): **225 indicators / 50 BUILD_NOW**. FAITHFULNESS FIX: dropped
  human-trafficking's 2016 Appendix (39 indicators — md L554 reproduces a SEPARATE 2016 OA → cross-doc
  double-count), kept the 57 genuine 2021 primary. KEPT the honest full lists, NO per-doc caps (user
  "keep it"). FINTRAC OAs are far denser than FinCEN advisories (house norm ≤24; new range 16-57).
- **T4** regen corpus-status (issuer=FINTRAC, 10 clean) + rebuilt `dist/corpus` (432KB→621KB; 46
  publications, 42 derived); `build.py`/`corpus.html` UNCHANGED (4-type menu/chips/count are data-driven,
  count assertions relationship-based). Harness 61→74 incl. a dedicated real-estate Brief full-arc walk.
- **T5** CLAUDE.md + README.md counts 39→46 publications / 35→42 derived / 3→10 FINTRAC + a Phase-23
  bullet/paragraph; NO non-negotiable change (depth within the Phase-22 Crown-copyright basis).

## Decisions Made
- Phase 23 = FINTRAC depth (3→10) at the goal gate over cross-corpus synthesis / presentation (audience =
  a Canadian bank → weight Canadian-relevant typologies) | high
- Scope = OAs + Operational Briefs WITH a regression-gated narrow-anchor widening, over OAs-only-no-gate
  and over a source-scoped rf_region refactor (DEFERRED — a future option if heading forms proliferate) | high
- The widening = an INVERTED "Indicators of <X>" anchor `_RF_HEADER_FINTRAC_INV` (two narrow branches +
  boilerplate exclusion via the connector gate), 0/39 shift, grounding core byte-untouched | high
- KEEP the honest full indicator lists, NO per-doc caps; drop ONLY human-trafficking's 2016 Appendix as a
  faithfulness fix (cross-doc double-count) | high
(Lite ceremony — decisions recorded in `_CURRENT_STATE` Recent Decisions, not as separate articles.)

## Problems Solved
- The real-estate Brief did NOT carry the planned "TABLE OF INDICATORS" heading (markitdown fragmented it)
  → handled via the inverted "Indicators of <X>" anchor, regression-gated 0/39. (DISCOVERY escape hatch.)
- Boilerplate collision risk: "Indicators of <ML/TF> can be thought of as red flags" opens the 3 existing
  OAs BEFORE their forward heading → the connector gate + `:?$` excludes it ("can" is not a connector).
- human-trafficking over-extracted to 96 by including the 2016 Appendix → dropped the 39 appendix
  indicators, kept the 57 genuine 2021 primary (re-gated clean). (DISCOVERY/faithfulness escape hatch.)

## Open Questions
- None — all resolved this session.

## Artifacts Changed
- `scripts/derive_signals.py` (`_RF_HEADER_FINTRAC_INV` inverted-form anchor + 4 new fixtures; grounding
  core untouched)
- `data/fintrac/**` (index.json 3→10, +7 md, +7 derived, corpus-status.json regen)
- `dist/corpus/index.html` (rebuilt, 621KB; data-driven — no template edit)
- `tests/corpus-explorer.test.mjs` (61→74; real-estate Brief full-arc walk + Brief-subtype +
  Crown-copyright assertions)
- `CLAUDE.md`, `README.md` (counts 39→46 / 35→42 / 3→10 + Phase-23 bullet/paragraph)

## Related
- [[phase-23-fintrac-depth|Phase 23: FINTRAC depth]] — parent phase
- [[2026-06-06-phase-22-fintrac-corpus-source|Phase 22 FINTRAC source #4]] — established the source + basis

### Review Gate
Unified reviewer (size-gated — L-task phase, 5 tasks): VERDICT ACCEPT, SCORE 9/10, no CRITICAL/HIGH.
Independently reproduced the 0-of-39 rf_region regression check via a HEAD-vs-working-tree diff, verified
boilerplate exclusion, faithfulness across 5 records (every sampled flag verbatim-grounded; no inflated
BUILD_NOW — build_logic concrete + bank-observable), the 57-indicator appendix trim (no primary-list leak,
max src_line 477 < appendix L554), compliance (all 7 provenance = Crown-copyright non-commercial, NOT
public domain; non-negotiable wording unchanged), and scope (zero drift, harness 74/74, frozen set
byte-clean, grounding core untouched). Two LOW findings, both grounding-backstopped + NO ship fix
required: (1) real-estate rf_region opens at the cover title (line 7) → over-inclusive front-matter, but
0/33 flags ground there (all at L375+) — safe-by-design over-inclusion per the rf_region docstring; (2)
the inverted anchor's branches are line-prefix-broad (could match a prose lead-in), 0 regressions on 39 +
0 mis-grounds on 7. Docked 1 point for the real-estate title-anchoring looseness only.

### Health Delta
- Harness 61→74 (+13: real-estate Operational Brief full-arc walk + Brief-subtype + Crown-copyright asserts).
- `--selftest` +4 inverted-form fixtures (3 positive headings + 1 negative boilerplate).
- 42/42 derived records `--check-derived` clean (was 35/35). `--check all` 4-artifact ZERO DRIFT.
- No type/lint tooling (dep-free vanilla JS/Python by design).

### Retro Check (Phases 16-23)

| Dimension | Findings | Signal |
|-----------|----------|--------|
| 1. Recurring Blockers | 0 genuine — abort conditions are designed-in (skip-the-doc if an anchor shifts a region); none hit; no blocked task | none |
| 2. Decision Reversals | 0 true reversals — the planned "TABLE OF INDICATORS" anchor was a pre-impl MISREAD corrected at impl (the inverted form), not a reversal of a committed decision; the source-scoped rf_region refactor stays consistently DEFERRED across Ph21/22/23 | low |
| 3. User Corrections | recurring: user steers toward SCALE/depth over the carried elder/fentanyl true-up (Ph20/21/22/23), and toward HONESTY (keep full indicator volume, no caps; drop the double-counted appendix) | high |

Recommendations:
- The user-correction pattern is now well-modelled in memory (prioritizes-scale-over-showcase-polish,
  honesty-over-demo-drama, canadian-bank-audience) — keep defaulting to honest scale over polish at gates.
- Anchor accretion is the one rising cost: `derive_signals.py` now carries forward + inverted FINTRAC +
  OFAC + FinCEN anchor sets. A 5th heading form should trigger the DEFERRED source-scoped rf_region
  refactor (thread issuer into rf_region; one per-source rule; FinCEN/OFAC untouched by construction).

## Soft Observations / Phase N+1 Candidates
- FINTRAC's anchorable set may extend further (capital markets/securities; casinos/Project Athena had no
  standalone OA slug — likely folded into underground-banking) — but 10 FINTRAC docs is substantial
  Canadian depth; diminishing returns. | Phase N+1 only on a fresh stakeholder ask. | this journal T1/T3
- Corpus scale: 46 publications in a flat SELECT menu — a search/filter/group-by-source UI may help as the
  corpus grows. | Phase N+1: corpus-explorer menu scalability. | `dist/corpus/index.html`
- Anchor accretion → the DEFERRED source-scoped rf_region refactor earns its complexity at a 5th heading
  form. | Phase N+1: gate refactor. | `scripts/derive_signals.py`
- Indicator-count range widened to 16-57 (human-trafficking 57). The harness passed on a dense doc, but a
  human-eye smoke check (`tests/smoke-checklist.md`) on a 57-row build-recs screen is worth doing before
  presenting. | pre-present checklist. | `tests/smoke-checklist.md`
- The real-estate Brief's rf_region over-includes front-matter (reviewer LOW #1) — grounding-backstopped,
  safe; tighten only if the title-on-its-own-line anchor form recurs. | watch-item. | reviewer LOW #1
