---
title: "Phase 41: Entity-resolution schema enrichment (live news) — implemented, ready for completion"
aliases: []
category: journal
tags: [news-live, entity-resolution, schema, grounding-gate, duckdb, privacy, prompt-engineering]
parents: [phase-41-entity-resolution-schema]
created: 2026-06-10
updated: 2026-06-10
source: debrief
duration: unknown
---

# Phase 41: Entity-resolution schema enrichment (live news)

## What Happened
- ALL 6 lite tasks T1–T6 [x] (no scope growth; spec `specs/phase-41-entity-resolution-schema.md` nana:approved 2026-06-09 satisfied the enforce-hook prerequisite). READY FOR COMPLETION — delivery gate pending.
- T1 extraction schema+prompt: closed vocabs SINGLE-AUTHORITY in news_ground; EXTRACT_SCHEMA/SYSTEM_PROMPT construct from the constants; new fields emit only-when-nonempty (legacy-capture compat); goltsev-derived exemplars.
- T2 shared-gate extensions: aliases RAW-ground, properties NORMALIZE-ground (canonical-form rejection proven), relationship evidence RAW-ground + referential integrity + self-edge drop; alias-fold INVERSION (DROP→FOLD w/ folded_into audit + structural `_adjacent_parent`); `reconcile_refs` remaps post-fold/post-verify. The 4 committed records passed CLEAN (checkpoint — no adjudication needed).
- T3 store anchor redesign: anchors / monolithic entity_properties / entity_relationships tables + scans.source_type; additive legacy migration proven; both-kept conflict rule; confidence asserted NULL; `anchor_summary` read.
- T4 watchlist/screen alias-awareness: escalated rows carry anchor aliases + source_type provenance; live matcher scores name ∪ aliases MAX-pair with CLASS-AWARE rules (single-token/@-handle EXACT-only, never fuzzy; `via` reported).
- T5 live UI (strip intact): source-type selector, SUBJECT MAP panel (evidence-quoted edges, honest none/multiple mains), identity cards (a.k.a. + property chips).
- T6 regate + 3 `.ph41` US-federal fixtures + FIXTURE_META privacy-allowlist assert + docs (news-live.md `## Entity resolution`, smoke-checklist Phase-41 walk, CLAUDE.md in-place). The PROMPT-REGRESSION gate fired and was cleared (see Decisions/Problems).
- Architectural: the DuckDB store is now the live layer's first real ER data model (identity spine + monolithic property-edge table + relationship edges — designed for private investigation notes as future input). EXTRACT_SCHEMA property ORDER is now load-bearing (strict-grammar generation order = schema order).
- Escape hatches (DEPENDENCY ×2, annotated in tasks.md): T1 placed vocab constants in news_ground.py (T2-scope file — the spec's single-authority rule required it); T2 added reconcile_refs consumer glue in serve_news.py (referential integrity had to survive the fold in the same change).

## Decisions Made
- D5 (Phase 41 r2 PROMPT-REGRESSION FIX, user-ruled): the enriched ONE-CALL prompt with red_flags generated LAST cost ~12.5% kept flags (24→21 over the 3 .ph40-paired federal articles; sanctions-evasion family lost on tgr-group). User ruling at the mid-T6 checkpoint: prompt-iteration-first (two-pass extraction held as fallback, rollback rejected). r2 = red_flags FIRST in EXTRACT_SCHEMA property order (llama-cpp strict grammar generates in schema order — flags get full attention before enrichment spends budget) + enrichment bullets BELOW the checklist + an explicit never-reduce-flag-coverage guard. Result: regression CLEARED — 24→25 kept flags (tgr 10→10 overlap 9/10; cmlo 5→8 incl. +3 families) with enrichment intact (tgr: 8 alias-bearing entities, 10 evidence-grounded edges, honest 7-subject set). Recorded as a Recent Decisions row in _CURRENT_STATE (lite — no decision article).

## Problems Solved
- Enrichment-vs-flags budget competition under strict grammar — solved by schema-order reordering + prompt restructure (D5), measured against the .ph40-paired fixtures, not vibes.
- Legacy-capture compatibility — new fields default-empty for old qwen.json captures; pinned pre-41 captures byte-clean (`git diff --exit-code`); goldens regenerated deterministically, no re-capture.

## Open Questions
- None blocking. Named seams: anchor-view UI/route (anchor_summary has no consumer) · fuzzy cross-scan merge adjudication · confidence-column population basis · per-property subtable split criteria · offline-demo enrichment · carried corpus candidates (FINTRAC /intel/, AUSTRAC/UK) · CLAUDE.md trim (305 lines, increasingly due).

## Artifacts Changed
- `scripts/serve_news.py` (schema/prompt from vocab constants, source_type plumbing, reconcile glue) · `scripts/news_ground.py` (vocab authorities, grounding extensions, alias-fold, reconcile_refs) · `scripts/news_store.py` (anchor redesign) · `scripts/build.py` (shared-gate consequence) · `news.html` (LIVE region only) · `tests/news_live_test.py` + `tests/news-stream.test.mjs` (+13 → 103) · `tests/fixtures/news-live/` (10→13: 3 `.ph41` pairs) · `docs/news-live.md` · `tests/smoke-checklist.md` · `CLAUDE.md` (T6 in-place) · `specs/phase-41-entity-resolution-schema.md`.

### Review Gate
- Unified reviewer dispatched (6 tasks ≥ 4 trigger). Score 9/10, Verdict ACCEPT, zero HIGH+. 4 MEDIUMs: decision-article vocab record stale (FIXED inline pre-commit: frozen 9-term vocab + DRQ3 13-edge distribution recorded) · anchor_summary unconsumed (FIXED: named as next-phase seam in the decision article) · pre-debrief staleness (resolved by this debrief) · CLAUDE.md 305 lines (carried as candidate). 3 Suggestions noted as cosmetic residuals. Reviewer independently re-verified: pinned captures byte-clean, replay 13/13, selftests, node 103, --check news, build-import discipline, privacy allowlist, NULL confidence.

## Health Delta
- node news-stream 90→103 (+13: alias-class matcher both-directions, subject-map/identity-card render, Phase-41 strip assertions); corpus 239 unchanged · news_ground selftest +Phase-41 grounding block (≥3 identifier cases incl. punctuation-varied/line-wrapped/canonical-rejection, ≥2 alias-folds, relationship/main-subject disposal, reconcile_refs) · news_store selftest +anchor block (4-scan accumulation, both-kept dob conflict, NULL confidence, legacy migration) · news_live_test +canned41 loop + FIXTURE_META allowlist · replay fixtures 10→13 · `--check all` 5/5 zero drift · pinned pre-41 captures byte-clean · `--live` real-Qwen smoke RAN green.

## Related
- [[phase-41-entity-resolution-schema|Phase 41: Entity-resolution schema enrichment (live news)]] — parent phase
- [[decisions/phase-41-entity-resolution-schema|Phase 41 direction decision]] — D1–D4 (plan-time)

## Soft Observations / Phase N+1 Candidates
- Anchor view built but UNCONSUMED: `news_store.anchor_summary` (accumulated identity w/ kept conflicts) has no route/UI | candidate: "anchor dossier view + conflict surfacing" | evidence: reviewer MEDIUM finding; decision article Consequences seam note.
- Schema property ORDER is a measured, load-bearing prompt lever under strict-grammar local models (flags-last −12.5%, flags-first restored +1) — reusable insight, /wiki-capture candidate | evidence: tasks.md T6 annotation, .ph41 vs .ph40 fixture comparison.
- kind↔value semantic fit is the new unguarded neural dimension (observed: dob="born in Russia" grounded but mis-kinded) | candidate: measurement pass before any gate rule | evidence: docs/news-live.md honest-residual note.
- The model's own aliases[] extraction outperformed the structural fold on TGR (@monalisa7→Zhdanova attached where `_adjacent_parent` could not) — the prompt does ER work the deterministic layer can't; keep prompt-first posture | evidence: ofac-tgr-group.ph41.golden.json.
- CLAUDE.md at 305 lines (reviewer flag) | candidate: hygiene half-task in next /dev-plan.
- reconcile_refs doesn't dedup edges that become identical post-fold; degraded-fold drop reason can mislabel a lowercase multi-token name | two cosmetic residuals, fix opportunistically | evidence: reviewer Suggestions.
