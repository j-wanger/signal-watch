# Active Phase Context

Phase: 25 - Corpus output quality — extract → translate (natural AML red flags) + the article-processing page (M7) — PLANNED 2026-06-07; direction approved; 5 tasks; implementation starting at T1.

Objective: Turn the corpus explorer's red flags from bare VERBATIM article extractions into natural AML-term red flags, and give the corpus demo the showcase's missing article-processing beat. Each live derived indicator gains a `red_flag` (natural AML phrasing) BESIDE its grounded verbatim `flag` (the evidence). A new per-doc screen renders the FULL source article, highlights the grounded phrases (free — exact substrings by the gate), then reveals the translation. Per-doc arc becomes: Select → Read advisory [process] → Coverage → Build recs → Signal → Close.

Tasks (lite, riskiest-first):
- T1 (M) extend the gate (`red_flag` SHAPE check; grounding byte-unchanged) + build.py full-article inline (md → __CORPUS__, provenance-header-stripped) + re-derive EFE (fin-2022-a002) as the design PROOF. CHECKPOINT: the EFE translations resemble the showcase elder labels + ground clean, else STOP/degrade.
- T2 (L) re-derive the remaining 41 derived docs with `red_flag` (inverted loop, batched subagents, each gated + independently re-checked).
- T3 (M) corpus.html article-processing screen + thread `red_flag` through the arc (verbatim kept as the traceable subline).
- T4 (S) rebuild dist/corpus + drift guard + extend the harness.
- T5 (S) docs (schema/derivation + the honesty model, CLAUDE, README).

Scope (UNFREEZE): `scripts/derive_signals.py` (ADDITIVE `red_flag` shape check ONLY — normalize/rf_region/flag⊂md grounding BYTE-UNCHANGED), `scripts/build.py` (full-article inline + `red_flag` merge/validate), all 4 sources' `derived/*.json` (the re-derive), `corpus.html` (the new screen + threading), `dist/corpus/index.html`, `tests/**`, `config/schema.md`, `CLAUDE.md`, `README.md`.
FROZEN byte-untouched: every source MD (`data/{fincen,fincen-alerts,ofac,fintrac}/*.md`), every `corpus-status.json`, `index.html`, `config/typologies/**`, the 3 typology dists, `data/typology-map.json`, the six-act showcase, the authoring scripts (`acquire_fincen.py`/`crawl_fincen.py`/`pdf_to_md.py`).

Key constraints:
- HONESTY (load-bearing): the verbatim `flag` stays the grounded authority, shown BESIDE the `red_flag` (never replaced). The grounding gate logic is byte-unchanged; the new gate check is SHAPE only (present / non-empty / distinct-from-verbatim / length-bounded) — translation faithfulness is the one NEURAL step, mitigated by show-both + the always-on illustrative badge + the EFE oracle + per-doc re-check. Paraphrase is the compliance DEFAULT, so the translation ALIGNS with the non-negotiables. NO non-negotiable change.
- PER-DOC ARC + SYNTHESIS preserved: the new screen is ADDITIVE; the Phase-24 synthesis view + the 98-assertion harness stay regression-clean.
- The full source article renders verbatim under each source's existing basis (US-federal public-domain 17 U.S.C. §105 / FINTRAC Crown-copyright non-commercial licence), kept visually distinct from the always-on illustrative badge.

Exit criteria: every live derived indicator carries a natural `red_flag` beside its grounded verbatim `flag` (gate-shape-validated, grounding byte-unchanged); the explorer renders a full-article processing screen (highlight → translate) ahead of Coverage with `red_flag` threaded + the verbatim traceable; `--check all` zero drift; the harness extended; source mds + corpus-status.json + the six-act showcase byte-frozen; docs updated; NO non-negotiable change.

Abort/degrade: if T1's EFE proof can't yield honest translations (don't resemble the showcase oracle / over-interpret), DEGRADE to presentation-only (verbatim-in-context + existing signal logic for buildable gaps) and report BEFORE T2. If inlining 42 mds pushes dist past ~2.5MB, reconsider (rf_region-only / note it). Blocked >3 attempts on a task → ask the user: skip or abort.

Gates:
- [x] Direction confirmed by user (full re-derive now + corpus extract→translate + full article; the `red_flag`-beside-verbatim honesty model + the build-boundary full-article inline + the 5-task shape signed off; 2026-06-07)
- [ ] Delivery accepted (post-implementation report)
