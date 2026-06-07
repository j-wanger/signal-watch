# Active Phase Context

Phase: 25 - Corpus output quality — extract → translate (natural AML red flags) + the article-processing screen (M7) — DELIVERED 2026-06-07; all 5 tasks [x]; exit criteria GREEN; reviewer 9/10 ACCEPT, two LOW FIXED INLINE; committed d3fdadf (impl) + cd0e1e5 (review LOW fixes); delivery gate ACCEPTED.

Objective (DELIVERED): bring the corpus explorer to the showcase's TWO-LAYER red-flag model — keep step 1 = the grounded verbatim `flag` extraction (the evidence), ADD step 2 = a natural-AML `red_flag` TRANSLATION beside it on every derived indicator (re-derived across all 42 live docs via the inverted loop), plus a per-doc "Read advisory" screen (`renderArticle`) rendering the FULL source article (verbatim phrases highlighted → translated). The per-doc arc is now Select → Read advisory → Coverage → Build recs → Signal → Close. OUTCOME: 42/42 records carry a faithful `red_flag`; the 6-screen arc + the article beat ship; honest show-both held; NO non-negotiable change.

Tasks (all DELIVERED): T1 (M) the gate `red_flag` SHAPE check + build.py full-article inline (`_inline_article`/`_strip_provenance`) + the EFE proof/checkpoint (PASS) · T2 (L) re-derive the remaining 41 docs · T3 (M) the article-processing screen + thread `red_flag` through the arc · T4 (S) rebuild + drift guard + harness 98→108 · T5 (S) docs.

Scope (the UNFREEZE, all consumed): `scripts/derive_signals.py` (ADDITIVE `red_flag` SHAPE check — grounding normalize/rf_region/flag⊂md BYTE-UNCHANGED), `scripts/build.py` (full-article inline + the `red_flag` boundary check in `validate_corpus_data`), all 4 sources' `derived/*.json` (the re-derive), `corpus.html` (the new screen + threading), `dist/corpus/index.html`, `tests/**`, `config/schema.md`, `CLAUDE.md`, `README.md`. FROZEN byte-untouched (verified): every source MD + every `corpus-status.json`, `index.html`, `config/typologies/**`, the 3 typology dists, `data/typology-map.json`, the six-act showcase, the authoring scripts (`acquire_fincen.py`/`crawl_fincen.py`/`pdf_to_md.py`).

Key constraints (all HELD):
- HONESTY MODEL: the verbatim `flag` stays the GROUNDED authority shown BESIDE the translation (never replaced); the grounding gate logic is BYTE-UNCHANGED; the `red_flag` check is SHAPE-only (present/non-empty/distinct/12–240 chars) in BOTH `check_record` and `validate_corpus_data`; translation faithfulness is the one accepted neural step, mitigated by show-both + the always-on badge + per-doc re-check; paraphrase is the compliance DEFAULT → NO non-negotiable change.
- BUILD-BOUNDARY INLINE: the full article is inlined at build time (new build.py helpers), keeping `render_one` + the 3 typology dists byte-frozen.
- PER-DOC ARC + SYNTHESIS preserved: the new screen is ADDITIVE; the Phase-24 synthesis view + drill-through stay regression-clean. NO non-negotiable change (the always-on badge + the verbatim US-federal-public-domain + FINTRAC-Crown-copyright bases stay).

Exit criteria (all MET): `--check all` 4/4 ZERO DRIFT · `--selftest` PASS (grounding core byte-unchanged) · harness 98→108 · 42/42 derived records `--check-derived` clean (red_flag present/distinct/bounded; verbatim still grounds) · frozen set byte-clean · reviewer 9/10 ACCEPT (two LOW fixed inline) · dist/corpus 2.19MB (under the 2.5MB watch line).

Abort (NOT needed): if T1's EFE proof couldn't yield honest translations → degrade to presentation-only before T2; if 42 inlined mds pushed dist past ~2.5MB → reconsider (rf_region-only / note). Blocked >3 attempts → ask the user: skip or abort.

Gates:
- [x] Direction confirmed by user (corpus extract→translate + full article; full re-derive; the `red_flag`-beside-verbatim honesty model; 2026-06-07)
- [x] Delivery accepted (post-implementation report 2026-06-07; reviewer 9/10 ACCEPT, two LOW fixed inline; impl d3fdadf + review cd0e1e5)

Demo at Definition of Done; run /dev-plan only for a net-new ask.
