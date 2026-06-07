---
title: "Phase 25: Corpus output quality — extract → translate (natural AML red flags) + the article-processing screen (M7)"
aliases: []
category: journal
tags: [corpus, red-flag, translation, article-processing, extract-translate, honesty, corpus-explorer, inverted-loop]
parents: [phase-25-corpus-translation]
created: 2026-06-07
updated: 2026-06-07
source: debrief
duration: ~1 session (post-compaction estimate)
---

# Phase 25: Corpus output quality — extract → translate (natural AML red flags) + the article-processing screen

## What Happened
- Brought the corpus explorer to the six-act showcase's TWO-LAYER red-flag model. The corpus demo
  surfaced the grounded VERBATIM `flag` substring as "the red flag" — which reads like an article
  EXTRACTION, not how an AML program writes a red flag — and it lacked the showcase's article-processing
  beat (full advisory rendered, red-flag phrases highlighted, then extracted/translated). This phase keeps
  step 1 = the grounded verbatim extraction (the EVIDENCE) and ADDS step 2 = a natural-AML `red_flag`
  TRANSLATION beside it on every derived indicator, plus a per-doc "Read advisory" screen that renders
  the FULL source article, highlights the grounded phrases, then reveals the translation. The per-doc arc
  grew Select → **Read advisory** → Coverage → Build recs → Signal → Close. The user REFRAMED here — away
  from the three offered N+1 options (grow-Canada-singletons / a 3rd jurisdiction / durability-CI) — to a
  QUALITY gap he saw in the built artifact.
- **T1 (the load-bearing checkpoint)** extended `derive_signals.py check_record` with an ADDITIVE
  `red_flag` SHAPE check (present / non-empty / distinct-from-verbatim / 12–240 chars), `--selftest` +3
  fixtures (missing / identical / over-long); the grounding logic (normalize / rf_region / flag⊂md) stays
  BYTE-UNCHANGED. `build.py` gained `_inline_article` + `_strip_provenance` — each LIVE derived doc's
  `source_md` body (provenance-header-stripped) inlines into `__CORPUS__` as `article_text` (the EFE body
  ~47KB), reusing the `advisory_full` text_file→text pattern; `render_one` + the 3 typology dists stay
  byte-frozen. A re-declared `red_flag` boundary check in `validate_corpus_data` fails loud (wiring
  proven). EFE (fin-2022-a002) re-derived with `red_flag` on all 12 indicators, `--check-derived` clean.
  CHECKPOINT **PASS**: the 12 translations resemble the showcase elder labels by MEANING (IND-11
  verbatim-identical "Uncharacteristic large-sum wire-transfer attempts"), faithful + grounded, no
  over-interpretation — the quality/honesty oracle held, so the full re-derive proceeded.
- **T2 (L, the re-derive)** re-derived the remaining 41 live derived docs (11 advisories + 17 alerts +
  3 OFAC + 10 FINTRAC) via the inverted loop — one subagent per doc, each adding a faithful natural
  `red_flag` per indicator + self-gating to `--check-derived` clean, then INDEPENDENTLY re-checked.
  FULL SWEEP: 42/42 records clean (red_flag present/distinct/12–240, verbatim still grounds,
  matrix-consistent). FAITHFULNESS re-checked across sources — every red_flag is a register-only change,
  NO over-interpretation: truncated verbatims (human-trafficking IND-23/35, terrorist-financing IND-02/04)
  rephrase only as far as the quote goes; OFAC maritime drops example commodities rather than narrowing;
  the verbatim flag stays beside each translation as the grounded authority.
- **T3 (the article-processing screen)** corpus.html +~45 lines, additive: a new per-doc `renderArticle`
  screen (the full source article in a scrollable `.doc` panel with each verbatim flag highlighted via a
  best-effort whitespace-flexible `highlightArticle`, then the extract→translate `.xrow` list: verbatim
  phrase → red_flag) inserted at DETAIL[0]; STEPS 5→6, updateControls back/next/hint arrays extended.
  `red_flag` threaded as the indicator LABEL through Coverage / Build-recs / Signal-spec / Close with the
  verbatim kept as the traceable `.csub`/`.bsrc` subline + a new "Red flag" spec row. Keyboard-nav-safe
  (no `<input>`); reduced-motion one-shot. The Phase-24 synthesis view + drill-through stay intact (Back
  from a cluster now returns to the cluster after the Read-advisory screen).
- **T4** rebuilt dist/corpus 635KB→**2.19MB** (the full-article inline adds the 42 source-md bodies; under
  the 2.5MB watch line); `--check all` **4/4 ZERO DRIFT** (all 3 typology dists byte-unchanged + corpus
  fresh); harness 98→**108** (+10 article/red_flag/6-screen assertions); `--selftest` PASS (grounding core
  untouched). FROZEN byte-clean (git): all source mds, every corpus-status.json, index.html, config/**,
  data/typology-map.json, the 3 typology dists, the showcase.
- **T5** docs: CLAUDE.md a Phase-25 RED-FLAG-TRANSLATION + ARTICLE-PROCESSING bullet (the two-layer model,
  the re-derive, the Read-advisory screen + build.py full-article inline, the SHAPE-only gate in both
  check_record + validate_corpus_data, dist 635KB→2.19MB, harness 98→108) + the 5→6-screen arc + the test
  line; README.md the 6-screen arc + a "Read advisory + red-flag translation (Phase 25)" paragraph;
  config/schema.md a corpus-explorer-analogue note. NON-NEGOTIABLE wording byte-unchanged (paraphrase
  default + the verbatim US-federal-public-domain / FINTRAC-Crown-copyright bases); HANDOFF.md needed no
  edit.

## Decisions Made
- Phase 25 = corpus output QUALITY — the corpus explorer's red flags read like bare VERBATIM article
  EXTRACTIONS, not how an AML program writes red flags, and it lacks the showcase's article-processing
  page. User REFRAMED here, away from the three offered N+1 options (grow-Canada-singletons / a 3rd
  jurisdiction / durability-CI), to a quality gap he saw in the BUILT artifact | high
- FULL RE-DERIVE NOW (all 42 live docs) over exemplar-first / presentation-only — every derived indicator
  gains the natural `red_flag` in this phase, via the inverted loop (one subagent per doc, self-gated then
  independently re-checked) | high
- HONESTY MODEL (load-bearing): the verbatim `flag` stays the GROUNDED authority shown BESIDE the
  translation (never replaced); the grounding gate logic (normalize / rf_region / flag⊂md) is
  BYTE-UNCHANGED; the new `red_flag` check is SHAPE-only (present / non-empty / distinct / 12–240 chars),
  enforced in BOTH `derive_signals.py check_record` AND `build.py validate_corpus_data`; translation
  faithfulness is the ONE accepted neural step, mitigated by show-both + the always-on badge + per-doc
  re-check; paraphrase is the compliance DEFAULT so the translation ALIGNS with the non-negotiables (NO
  non-negotiable change) | high
- The FULL ARTICLE is inlined at the BUILD boundary (new build.py `_inline_article`/`_strip_provenance`
  helpers reading each doc's `source_md`), keeping `render_one` + the 3 typology dists byte-frozen | high
(Lite ceremony — decisions recorded in `_CURRENT_STATE` Recent Decisions, not as separate articles.)

## Problems Solved
- A zero-dep test-shim limitation surfaced a real robustness gap in `renderArticle`'s scroll-into-view
  callback (querySelector/offsetTop on a minimal DOM) → guarded inline. (DISCOVERY escape hatch — a real
  fix, not a test workaround.)
- OFAC maritime red_flag faithfulness (reviewer LOW): IND-01/02/06/07 imported the source paragraph's
  gloss beyond their heading-only `flag`, breaking show-both → tightened to be heading-faithful.
- Build-boundary MIN-length parity (reviewer LOW): added `MIN_RED_FLAG_CHARS = 12` to
  `validate_corpus_data` so the two gate sites enforce the same shape. Both FIXED INLINE + committed
  cd0e1e5.

## Open Questions
- None — all resolved this session.

## Artifacts Changed
- `scripts/derive_signals.py` (ADDITIVE `red_flag` SHAPE check in `check_record` + 3 `--selftest`
  fixtures; the grounding core normalize/rf_region/flag⊂md BYTE-UNCHANGED)
- `scripts/build.py` (`_inline_article` + `_strip_provenance` full-article inline into `__CORPUS__` per
  live doc; a re-declared `red_flag` boundary check in `validate_corpus_data`)
- `data/{fincen,fincen-alerts,ofac,fintrac}/derived/*.json` (re-derived — every indicator gains a natural
  `red_flag` beside its grounded verbatim `flag`; 42/42 `--check-derived` clean)
- `corpus.html` (the new per-doc `renderArticle` article-processing screen + `highlightArticle` + the
  extract→translate `.xrow` list; `red_flag` threaded as the indicator label through the arc with the
  verbatim as the traceable subline; 6-screen arc)
- `dist/corpus/index.html` (rebuilt, 635KB→2.19MB)
- `tests/corpus-explorer.test.mjs` (98→108; +10 article/red_flag/6-screen assertions)
- `config/schema.md`, `CLAUDE.md`, `README.md` (the `red_flag` field + the processing screen + the
  honesty model; non-negotiable wording byte-unchanged)

## Related
- [[phase-25-corpus-translation|Phase 25: Corpus output quality — extract → translate]] — parent phase
- [[2026-06-07-phase-24-cross-corpus-synthesis|Phase 24 Cross-corpus synthesis]] — the per-doc + synthesis arcs this beat threads red_flag through
- [[2026-06-06-phase-18-corpus-explorer-arc|Phase 18 corpus-explorer arc]] — the per-doc spine + the precision-lift rejection this honesty model continues
- [[2026-06-06-phase-16-invert-extraction|Phase 16 invert-extraction]] — the grounding invariant that makes the highlight free (flag⊂md)

### Review Gate
Unified reviewer (size-gated — 5 tasks incl. an L): VERDICT ACCEPT, SCORE 9/10, no CRITICAL/HIGH/MEDIUM.
Two LOW findings, both FIXED INLINE + committed cd0e1e5: (a) OFAC maritime red_flag faithfulness —
IND-01/02/06/07 imported the source paragraph's gloss beyond their heading-only `flag`, breaking
show-both → tightened to be heading-faithful; (b) build-boundary MIN-length parity — added
`MIN_RED_FLAG_CHARS = 12` to `validate_corpus_data` so both gate sites enforce the same shape.
Re-verified after the fixes: `--check all` 4/4, harness 108/108, `--selftest` PASS, 42/42 records clean,
frozen set byte-clean.

### Gate Compliance
- Direction = approved (corpus extract→translate + full article; full re-derive now; the
  red_flag-beside-verbatim honesty model; signed off 2026-06-07).
- Delivery = accepted (post-implementation report 2026-06-07; reviewer 9/10 ACCEPT, two LOW fixed inline;
  impl d3fdadf + review cd0e1e5).
- Retro NOT triggered (22nd completed phase; 22 % 5 = 2 ≠ 0).

### Health Delta
- Harness 98→108 (+10 article / red_flag / 6-screen assertions); `--selftest` +3 red_flag-shape fixtures.
- `--check all` 4/4 ZERO DRIFT. `--selftest` PASS (grounding core derive_signals.py byte-unchanged).
- dist/corpus 635KB→2.19MB (the inlined source articles dominate the delta; under the 2.5MB watch line).
- No type/lint tooling for the HTML/data layer; the harness + `--selftest` + `--check all` are the gates.
- No new runtime deps; the ship artifact stays single-file/offline/no-fetch.

## Soft Observations / Phase N+1 Candidates
- Story-driven LANDING PAGES for both demos (the showcase + the corpus explorer) — the user LED with this
  at the reframe; it's the strongest carried roadmap candidate. | Phase N+1: landing pages. | roadmap
- Full-article-for-all in the 3-case SHOWCASE — a per-source COMPLIANCE call: elder renders the full EFE
  advisory today (`advisory_full`), but fentanyl + trade-based were never given one (their sources are
  paraphrased — fentanyl's FINTRAC OA deliberately). | Phase N+1: extend the article beat to the showcase
  where the source permits. | per-source compliance
- Pre-commit/CI `--check all` gate — the partial-commit defect has now bit TWICE (carried from Phase 24).
  | Phase N+1: a pre-commit/CI gate running --check all + --selftest + the harness. | log.md Phase-9
  deferred item
- The article highlight is BEST-EFFORT (literal whitespace-flexible match) — a few verbatim flags
  (hyphen-wrap / footnote-digit / quote-mismatch / heading-only) won't highlight; the translate list
  shows ALL regardless. A normalize-aware highlighter could raise coverage. | low priority |
  corpus.html highlightArticle
- dist/corpus at 2.19MB — the inlined source articles dominate; watch the single-file size if more sources
  are added (the 2.5MB watch line is close). | watch-item | dist/corpus/index.html
- The OFAC maritime record carries heading-only `flag` fields (vs prose elsewhere) — a future re-derive
  could capture heading+paragraph for consistency. | low priority | data/ofac/derived
- The demo is again at Definition of Done (Phase 25 adds output quality + the article beat on the
  4-source/2-jurisdiction corpus). | /dev-plan only for a net-new stakeholder ask. | _CURRENT_STATE
  Recommended Next Action
