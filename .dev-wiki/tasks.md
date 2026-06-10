# Tasks

> ACTIVE PHASE ONLY. Closed phase blocks live VERBATIM in [articles/tasks-archive-pre-phase-44.md](articles/tasks-archive-pre-phase-44.md) (split out 2026-06-10 by the Phase-44 T6 hygiene trim; per-phase narrative also in the journal + articles/decisions/*). Archived blocks:
> - Phase 43: Live pipeline robustness + progressive presentation (live news) — M8
> - Phase 42: Anchor dossier view + per-scan network visualizer (live news) — M8
> - Phase 41: Entity-resolution schema enrichment (live news) — M8
> - Phase 40: Live red-flag extraction quality (measure-first) — M8
> - Phase 39: Live news QOL — streamed extraction progress + one-shot URL acquisition
> - Phase 38: Consolidate the live news subsystem (verify agent backend + watchlist management)
> - Phase 37: Per-indicator typology (corpus Typologies lens)
> - Phase 36: Persistence (DuckDB→parquet) + feedback watchlist — M8
> - Phase 35: News live local-model backend — M8
> - Phase 34: C/D-assignment verification pass — M7
> - Phase 33: Corpus completeness + full typology re-segmentation — M7
> - Phase 32: News stream — real gov-enforcement adverse-media source + presentation elevation — M8
> - Phase 31: M8 walking skeleton — the adverse-media / negative-news stream (a second atom stream) — M8
> - Phase 30: Data-source lens — surface the D1–D20 data-source axis as an institution coverage-by-data-source view — M7
> - Phase 29: Capability lens — surface the C1–C28 capability / D1–D20 data-source taxonomy as an institution coverage-by-capability view — M7
> - Phase 28: Corpus COMPLETENESS + grounded-coverage interview + methodical render + branding/compliance — M7
> - Phase 27: Make the corpus demo shippable — assess corpus output quality, then replan the fix — M7
> - Phase 26: Elevate the corpus demo to showcase quality — register re-translation + progressive render + build/lift wow + grouping/sort + landing page — M7
> - Phase 25: Corpus output quality — extract → translate (natural AML red flags) + the article-processing page — M7
> - Phase 24: Cross-corpus synthesis — a typology lens over the multi-source corpus — M7
> - Phase 23: FINTRAC depth — grow source #4 with the remaining anchorable strategic-intel products (Operational Alerts + Operational Briefs) — M7
> - Phase 22: FINTRAC as corpus source #4 (first cross-jurisdiction source; gate widened for FINTRAC "indicators" vocab; Crown-copyright non-commercial reproduction) — M7
> - Phase 21: OFAC as corpus source #3 (gate widened for OFAC vocab; US-federal public-domain) — M7
> - Phase 20: Multi-source spine, proven with FinCEN Alerts — M7
> - Phase 19: Durability closeout — commit corpus-explorer test harness + pin _rf_triage — M7
> - Phase 18: Corpus explorer arc — human gate + close-the-loop coverage payoff — M7
> - Phase 17: Complete corpus derivation + delete extract_red_flags (the real subtraction) — M7
> - Phase 16: Invert extraction (LLM extracts, deterministic gate disposes) + scale as proof — M7
> - Phase 15: Harden extraction faithfulness + fix shipped defects — M7
> - Phase 14: Scale corpus derivation (3 more CLEAN advisories → 5/14 live) — M7
> - Phase 13: Corpus explorer (advisory-selection front-end + per-indicator build-rec render) — M7 — THE PAYOFF
> - Phase 12: FinCEN corpus derivation foundation (deterministic spine all-14 + LLM proof slice) — COMPLETED + accepted (impl commit 90939b4)
> - Phase 11: Automated derivation (LLM-drafted signal config) — AUTOMATE — COMPLETED + accepted (impl commit c37dc39)
> - Phase 10: FinCEN corpus crawler (SCALE) — COMPLETED + accepted (commit 0c87c47)
> - Phase 9: Build-drift guard (zero-drift invariant) — COMPLETED + accepted
> - Phase 8: Doc true-up + provenance fix (M6 debt) — COMPLETED + accepted
> - Phase 7: Pipeline walking skeleton (M6) — COMPLETED + accepted

<!-- phase:phase-44-live-extraction-quality -->
<!-- gate-log:phase-44 direction=approved delivery=pending -->

## Phase 44 — Live extraction quality: targeted harness, classified fixes, processing page (live news) — M8

The user's REFRAME at the dev-plan gate 2026-06-10 (off the offered candidates — fuzzy-merge, bulk scan, FINTRAC /intel/, AUSTRAC/UK — all deferred again; hygiene BUNDLED as T6): (1) red-flag RECALL — live extraction misses obvious flags around high-risk-country wires in limited real testing; (2) alias PRECISION — entities assigned aliases that are clearly not them; (3) UX — after clicking run extraction, processing should show on a FRESH dedicated page; (4) the user's own hypothesis "do we need a better specific harness?" accepted as the T1 frame; (5) processing SPEED surfaced at the gate — resolved as a QUALITY-GATED optimization task (optimize only where the harness proves quality holds). Measure-first, CLASSIFICATION-first (the Phase-38/40 playbook, now targeted): T1 promotes the gitignored Phase-40 registry-scoring scratch to a COMMITTED harness, extends it with alias-ASSIGNMENT scoring (ownership — currently unmeasured: the gate checks an alias is verbatim, never WHOSE it is), builds targeted material (synthetic high-risk-country wire notes EMBEDDING the user's sample sentences — local gitignored, never committed — plus local-only commercial articles), measures per-stage wall-time, and REPRODUCES + CLASSIFIES both failures: flags = missed-at-generation vs dropped-at-gate (grounding drop / dup-collapse) vs registry blind spot (the SYSTEM_PROMPT registry already names "high-risk-jurisdiction" as a family — serve_news.py:158); aliases = model-generated bad alias vs deterministic fold misparent (token-subset rule or _adjacent_parent moniker fold — news_ground.py:258,293-300). Fixes follow the class (T2 flags, T3 aliases): prompt-iteration-first per the Phase-41 ruling (prompt-regression gate: red_flags FIRST schema order preserved, never-reduce guard, holdout eval); gate/fold changes via the known regate procedure (4 committed records + 13 replay goldens regenerate deterministically, NO re-capture); a structural EXTRACT_SCHEMA change surfaces as a FINDING first. T4 = quality-gated speed optimization at the T1-proven hotspot (likely the verify loop — the batched one-call shape per Phase-40 D5). T5 = fresh processing page, LIVE region only (offline dist/news byte-identical via the strip). T6 = bundled hygiene trim (user-approved, lossless). T7 = full regate + docs. PRIVACY (carried): the user's sample sentences + real failing examples + commercial captures LOCAL-ONLY (gitignored), never committed; fixtures US-federal-only (FIXTURE_META allowlist). The always-on badge stays; NO non-negotiable change. Assumption gate closed 2026-06-10: A1 accept-with-conditions (sample sentences; speed → quality-gated T4), A2 accept, A3 don't-know→defended→accept, A4 accept. PRECONDITION (enforce hooks, Phase 40/42/43 precedent): an approved spec via /spec --internal BEFORE any implementation edit — specs/phase-44-live-extraction-quality.md does NOT exist yet.

- [x] T1 (M) Committed targeted quality harness + reproduce + classify (measure-first): promote the Phase-40 registry-scoring scratch to a committed harness (e.g. tests/news_quality_harness.py or scripts/ — pick the convention-consistent home; committed part runs on committed/fixture material only); EXTEND with alias-ASSIGNMENT scoring (ownership, not verbatim-ness); targeted material = synthetic high-risk-country wire notes embedding the user's sample sentences + local commercial articles (ALL local gitignored, e.g. .dev-wiki/tmp/ph44/ — never committed); per-stage wall-time profile; classify flag misses (missed-at-generation vs dropped-at-gate [grounding drop / dup-collapse] vs registry blind spot) and alias misassignments (model-generated vs token-subset fold misparent vs _adjacent_parent moniker fold) | scope: tests/news_quality_harness.py, .dev-wiki/tmp/ph44*, tests/news_live_test.py | success: both reported failure classes REPRODUCED + classified in a results matrix (.dev-wiki/tmp/ph44-results.md); the committed harness runs deterministically on fixture material; wall-time profile names the hotspot
- [x] T2 (M) Red-flag recall fix per T1 class — prompt-iteration-first (SYSTEM_PROMPT registry/exemplar iteration w/ holdout eval + never-reduce guard) if generation-class; gate diagnostic/fix via the regate procedure if gate-drop-class | scope: scripts/serve_news.py, scripts/news_ground.py, tests/news_live_test.py, tests/fixtures/news-live/** (goldens regenerate deterministically only) | success: harness recall improves on HOLDOUT incl. the wire-flag cases; never-reduce guard green; 13/13 replay fixtures green NO re-capture; the 4 committed records pass the gate
- [x] T3 (M) Alias precision fix per T1 class — fold-logic repair (deterministic, fixture-pinned) and/or prompt rule and/or verify extension (alias-ownership check) | scope: scripts/news_ground.py, scripts/serve_news.py, tests/news_live_test.py, tests/fixtures/news-live/** | success: the reproduced misassignment cases corrected + fixture-pinned; the Phase-41 fold upside cases (e.g. @monalisa7→Zhdanova) unregressed; fixtures green no re-capture
- [x] T4 (M) Quality-gated speed optimization at the T1-proven hotspot (likely batched verify per the Phase-40 D5 one-call shape) | scope: scripts/serve_news.py, tests/news_live_test.py | success: measured wall-time reduction on the stress tiers WITH harness quality scores held (no reduction on any dimension); honest skip-with-reason if no optimization preserves quality
- [x] T5 (M) Fresh processing page — run-extraction navigates to a dedicated processing screen; the Phase-43 staged rendering (grounded flags FINAL, provisional chips, token counter) moves onto it; LIVE region only | scope: news.html (/*LIVE_START*/…/*LIVE_END*/ only), tests/news-stream.test.mjs | success: node news-stream harness covers the navigation + staged reveal on the new screen; offline dist/news byte-identical (--check news zero drift)
- [x] T6 (S) Bundled hygiene trim — archive closed tasks.md phase blocks (move to .dev-wiki/articles/ or an archive file with pointers), bring _CURRENT_STATE.md and _ARCHITECTURE.md under their ~100-line caps (pointers to journals/articles; lossless) | scope: .dev-wiki/tasks.md, .dev-wiki/_CURRENT_STATE.md, .dev-wiki/_ARCHITECTURE.md, .dev-wiki/articles/** | success: tasks.md holds ONLY the active phase + a pointer index; both state files under cap; no information loss (archived blocks reachable via pointers)
- [x] T7 (S) Full regate + docs — --check all 5/5; node news-stream + corpus harnesses; all selftests + news_live_test (system + .venv + --live smoke incl. a wire-note probe); docs/news-live.md quality+speed section; smoke-checklist item; CLAUDE.md updated IN PLACE (snapshot facts, no phase log) | scope: docs/news-live.md, tests/smoke-checklist.md, CLAUDE.md, specs/ | success: full regate green; docs updated in place

> Exit (phase-44): both reported failure classes REPRODUCED + classified + fixed-or-honestly-reported (flags recall on holdout incl. the wire cases; alias misassignments corrected + fixture-pinned, fold upsides unregressed); the targeted quality harness COMMITTED (fixture-material deterministic) w/ alias-ownership scoring; quality-gated speed optimization at the proven hotspot (or an honest skip-with-reason); the fresh processing page live in the LIVE region only; the hygiene trim done losslessly; 13/13 replay fixtures green NO re-capture; the 4 committed records pass the gate; offline dist/news byte-identical (--check all 5/5 zero drift); node news-stream + corpus green; all selftests + news_live_test (system + .venv + --live incl. a wire-note probe) green; docs/news-live.md + smoke-checklist + CLAUDE.md in place; the always-on badge stays; NO non-negotiable change.
> Abort: blocked >3 attempts on a task → mark [blocked: …] + ask the user skip or abort; offline dist/news can't stay byte-identical → STOP and surface it; a structural EXTRACT_SCHEMA need (field add/remove/reorder; red_flags must stay FIRST) → surface as a FINDING, never a silent edit; any optimization that reduces a harness quality score → reject it, report honestly.

<!-- phase:phase-43-live-pipeline-robustness -->
<!-- gate-log:phase-43 direction=approved delivery=accepted -->
