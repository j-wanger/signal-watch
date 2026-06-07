---
type: phase
phase: 25
slug: phase-25-corpus-translation
status: complete
ceremony: lite
created: 2026-06-07
updated: 2026-06-07
milestone: M7
---

# Phase 25: Corpus output quality — extract → translate (natural AML red flags) + the article-processing page

> Delivered + accepted 2026-06-07 (reviewer 9/10 ACCEPT, two LOW fixed inline; committed d3fdadf + cd0e1e5).

## Objective
Bring the corpus explorer to the six-act showcase's two-layer red-flag model. The corpus demo currently surfaces the grounded VERBATIM `flag` substring as "the red flag" — which reads like an article extraction, not how an AML program writes red flags — and it lacks the showcase's article-processing beat (full advisory rendered, red-flag phrases highlighted, then extracted/translated). Keep step 1 = the grounded verbatim extraction (the evidence); ADD step 2 = a natural-AML `red_flag` TRANSLATION beside it. Add a per-doc screen that renders the FULL source article, highlights the grounded phrases (free — exact substrings by the Phase-16 grounding invariant), then reveals the translation.

## Scope
UNFREEZE: `scripts/derive_signals.py` (additive `red_flag` shape check — grounding byte-unchanged), `scripts/build.py` (full-article inline + `red_flag` merge/validate), all 4 sources' `derived/*.json` (the re-derive), `corpus.html`, `dist/corpus/index.html`, `tests/**`, `config/schema.md`, `CLAUDE.md`, `README.md`.
FROZEN byte-untouched: every source MD, every `corpus-status.json`, `index.html`, `config/typologies/**`, the 3 typology dists, `data/typology-map.json`, the six-act showcase, the authoring scripts.

## Honesty model (load-bearing)
The verbatim `flag` stays the grounded authority, shown BESIDE the `red_flag` (never replaced). The grounding gate logic stays byte-unchanged; the new gate check is SHAPE only (present / non-empty / distinct-from-verbatim / length-bounded). Translation faithfulness is the one neural step — accepted explicitly, mitigated by show-both + the always-on illustrative badge + the EFE oracle (T1 vs the showcase's hand-written labels) + per-doc re-check. Paraphrase is the compliance DEFAULT, so the translation aligns with the non-negotiables. NO non-negotiable change.

## Exit criteria
- Every live derived indicator carries a natural `red_flag` beside its grounded verbatim `flag` (gate-shape-validated; grounding logic byte-unchanged).
- The corpus explorer renders a full-source-article processing screen (verbatim phrases highlighted → translated) ahead of Coverage, with `red_flag` threaded through the arc and the verbatim kept traceable.
- `python3 scripts/build.py --check all` zero drift; the harness extended.
- Source mds + every `corpus-status.json` + the six-act showcase byte-frozen.
- CLAUDE + README + schema updated; NO non-negotiable change.

## Tasks
See tasks.md (phase-25 block): T1 gate+build+EFE proof (M, checkpoint) · T2 re-derive 41 (L) · T3 article-processing screen + thread red_flag (M) · T4 rebuild+drift+harness (S) · T5 docs (S).

## Decisions
See _CURRENT_STATE.md `## Recent Decisions` (the three Phase-25 rows). Direction approved by user 2026-06-07 (full re-derive now; corpus extract→translate + full article; the red_flag-beside-verbatim honesty model + the build-boundary full-article inline).

## Abort / degrade
If T1's EFE proof can't yield honest translations (don't resemble the showcase oracle / over-interpret), DEGRADE to presentation-only (verbatim-in-context + existing signal logic for buildable gaps) and report before T2. If inlining 42 mds pushes dist past ~2.5MB, reconsider (rf_region-only / note it).
