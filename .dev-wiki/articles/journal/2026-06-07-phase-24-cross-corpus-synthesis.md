---
title: "Phase 24: Cross-corpus synthesis — a typology lens over the multi-source corpus (M7)"
aliases: []
category: journal
tags: [corpus, multi-source, synthesis, typology, cross-jurisdiction, coverage, honesty, corpus-explorer]
parents: [phase-24-cross-corpus-synthesis]
created: 2026-06-07
updated: 2026-06-07
source: debrief
duration: ~1 session (post-compaction estimate)
---

# Phase 24: Cross-corpus synthesis — a typology lens over the multi-source corpus

## What Happened
- Turned the 4-source / 2-jurisdiction corpus (42 derived across 46 publications) from 46 isolated
  documents into an analytical tool: a group-by-TYPOLOGY view that shows COMBINED coverage across a
  cross-jurisdiction cluster — **no single regulator enumerates a typology; the combined corpus does**.
  The per-document 5-screen arc (Phase 18) stays the spine; the typology lens is additive. User chose
  cross-corpus synthesis at the goal gate over navigability-at-scale / durability-CI / more-scale —
  highest net-new value for the Canadian-bank audience, uniquely enabled now that the corpus spans two
  jurisdictions.
- **PRECONDITION (DISCOVERY)** before T1: `main` failed its OWN drift guard — `data/fintrac/corpus-status.json`
  was committed at 3 entries in Phase 22 while Phase 23 added 7 more derived FINTRAC records (the committed
  dist had all 10; the manifest didn't — a partial commit into b0fcda4). Regenerated via the documented
  command (`derive_signals.py --corpus-status data/fintrac`); dist byte-identical, `--check all` back to
  4/4. Committed STANDALONE as Phase-23 hotfix **bfc183e** (user-approved) BEFORE starting T1.
- **T1 (the load-bearing checkpoint)** authored `data/typology-map.json` — a 22-term closed vocabulary +
  a 42-entry map (every live derived doc → exactly one typology; jurisdiction NOT stored, derived from the
  source registry). build.py: added `jurisdiction` to each CORPUS_SOURCES entry (US=FinCEN/OFAC,
  Canada=FINTRAC) + projected into each merged entry; added `load_typology_map` (shape gate) +
  `validate_typology` (the BUILD-BOUNDARY gate: closed vocab + referential integrity + total live-doc
  coverage, fail-loud) wired into render_corpus. Gate VERIFIED fail-loud end-to-end (a corrupted map →
  `build.py corpus` dies "typology 'bogus-typology' not in the declared vocabulary"). CLUSTER-VERIFY
  CHECKPOINT **PASS**: **5 cross-jurisdiction** typologies (terrorist-financing 5 docs US+CA,
  synthetic-opioids 2, human-trafficking 2, professional-money-laundering 2, romance-and-investment-fraud 2)
  + 2 cross-AGENCY US clusters (sanctions-evasion 7, public-benefits-fraud 3) + 11 honest singletons
  (5 Canada-specific). The build.py merge landed here alongside the gate (validation needs the merged corpus).
- **T2 (L, the synthesis view)** corpus.html +~120 lines, additive: a Documents/Typologies TOGGLE on Select
  (`selMode`, default 'doc' → doc-mode byte-identical, harness stays 74/74 at that point); `clusters()`
  builds the typology index from `__CORPUS__`; `typoCard` cluster cards (cross-jurisdiction / cross-agency
  chip); `renderSynthesis(t)` = the NEW screen (pooled `coverageIndex` over the UNION of every regulator's
  enumerated flags = COMBINED coverage on the reused gauge; per-jurisdiction contribution counts; each
  cluster doc a clickable `.synthrow` with jurisdiction + doc_type chips); navigation: `view='synthesis'`,
  `currentTypology`/`fromTypology` state, `enterSynthesis`, `pick(id,from)` so Back from per-doc Coverage
  returns to the cluster. HONESTY HELD: combined coverage is honest UNION arithmetic (NO dedup/matching
  across regulators), per-jurisdiction is an honest count, a framenote states "NOT de-duplicated or matched
  across regulators (no similarity or overlap is computed or claimed)" — NO similarity/overlap/lift number
  anywhere (ties to the Phase-18 precision-lift rejection).
- **T3** rebuilt dist/corpus (635KB; __CORPUS__ now carries typology per derived doc + jurisdiction per doc
  + the typology vocab); `--check all` 4/4 ZERO DRIFT. Extended the harness 74→**98** (+24 synthesis
  assertions, same zero-dep vm+DOM-shim): typology picker, a cross-jurisdiction cluster's synthesis (the
  honesty-critical assertion: COMBINED coverage == coverageIndex over the UNION of every cluster doc's
  indicators), the HONESTY GATE (disclaimer present; NO `\d+% (similar|overlap|match)`, NO `lift`),
  per-row source traceability, drill-through + Back-returns-to-origin-cluster, a singleton renders honestly,
  state-clear on toSelect. FROZEN byte-clean (git): the grounding core derive_signals.py + all 4 source dirs.
- **T4** CLAUDE.md + README.md: a Phase-24 cross-corpus-synthesis bullet/paragraph (the overlay artifact +
  build-boundary gate, the typology-mode → cluster → combined-coverage → drill-through shape, the 5
  cross-jurisdiction + 2 cross-agency clusters, the honesty constraint, harness 74→98). NO non-negotiable
  change — the verbatim 17 U.S.C. §105 + FINTRAC Crown-copyright wording byte-unchanged; HANDOFF.md needed
  no edit (no compliance/architecture change; corpus counts 42/46 unchanged this phase).

## Decisions Made
- Phase 24 = cross-corpus synthesis at the goal gate over navigability-at-scale / durability-CI /
  more-scale; integration shape = group-by-typology from Select → cluster + combined coverage →
  drill-through to the per-doc arc (additive lens; the per-doc arc is the spine) | high
- HONESTY GATE (ties to the Phase-18 precision-lift rejection): combined coverage = honest UNION
  arithmetic; per-jurisdiction = honest counts; every clustered indicator traceable to source + jurisdiction.
  NO similarity/overlap/lift metric; indicators NOT de-duplicated/matched across regulators | high
- SUBTRACTION + GATE LOCATION: the typology label is a SEPARATE committed overlay `data/typology-map.json`
  (doc-id → one closed-vocab typology, 22-term vocab; jurisdiction from the source registry, not stored),
  NOT 42 derived-record edits → all 4 source dirs + the grounding core stay byte-frozen. Validated at the
  BUILD BOUNDARY in build.py (a refinement from the originally-proposed derive_signals.py gate — keeps the
  grounding core frozen) | high
(Lite ceremony — decisions recorded in `_CURRENT_STATE` Recent Decisions, not as separate articles.)

## Problems Solved
- `main` failed its own drift guard (Phase-23 partial commit: corpus-status.json at 3 while dist had 10)
  → regenerated the manifest + committed standalone hotfix bfc183e before T1. (DISCOVERY escape hatch.)
- The build.py merge needed the typology fields attached before validate_typology could run → landed the
  merge in T1 alongside the gate, leaving T2 purely the corpus.html view (scope refinement, not a hatch).
- Reviewer LOW #1: `validate_typology` annotated `vocab: set` but receives a dict → corrected to `dict`.
- Reviewer LOW #2: jchip styled any non-Canada jurisdiction as "us" (latent) → added an `xx` neutral
  class for a future 3rd jurisdiction. Both FIXED INLINE before commit; re-verified clean.

## Open Questions
- None — all resolved this session.

## Artifacts Changed
- `data/typology-map.json` (NEW — the cross-corpus typology overlay: 22-term vocab + 42-entry map)
- `scripts/build.py` (`jurisdiction` per CORPUS_SOURCES entry + per merged entry; `load_typology_map` +
  `validate_typology` build-boundary gate; typology + vocab merged into `__CORPUS__`. First structural
  touch since Phase 20)
- `corpus.html` (the synthesis view — Documents/Typologies toggle, clusters/typoCard/renderSynthesis,
  view='synthesis' + navigation branches; additive — the per-doc arc unchanged)
- `dist/corpus/index.html` (rebuilt, 635KB)
- `tests/corpus-explorer.test.mjs` (74→98; +24 synthesis assertions)
- `CLAUDE.md`, `README.md` (the overlay artifact + the synthesis view + the honesty constraint)

## Related
- [[phase-24-cross-corpus-synthesis|Phase 24: Cross-corpus synthesis]] — parent phase
- [[2026-06-06-phase-23-fintrac-depth|Phase 23 FINTRAC depth]] — built the 2-jurisdiction corpus this lens needs
- [[2026-06-06-phase-18-corpus-explorer-arc|Phase 18 corpus-explorer arc]] — the per-doc spine + the precision-lift rejection this honors

### Review Gate
Unified reviewer (size-gated — L-task phase, 4 tasks): VERDICT ACCEPT, SCORE 9/10, no CRITICAL/HIGH.
Two LOW findings, both FIXED INLINE before commit: (1) `validate_typology` annotated `vocab: set` but
receives a dict → corrected to `dict`; (2) `jchip` styled any non-Canada jurisdiction as "us" (latent for
a future 3rd jurisdiction) → added an `xx` neutral class. Re-verified after the fixes: `--check all` 4/4,
harness 98/98, `--selftest` PASS, frozen set byte-clean.

### Health Delta
- Harness 74→98 (+24 synthesis assertions; same zero-dep vm+DOM-shim).
- `--check all` 4/4 ZERO DRIFT. `--selftest` PASS (grounding core derive_signals.py byte-unchanged).
- dist/corpus 621KB→635KB (typology + jurisdiction + the typology vocab in `__CORPUS__`).
- No new runtime deps; the ship artifact stays single-file/offline/no-fetch.

## Soft Observations / Phase N+1 Candidates
- The corpus now has 22 typologies, 11 of them singletons (5 Canada-specific: cannabis,
  illegal-wildlife-trade, child-sexual-exploitation, real-estate, underground-banking) — a future source
  could grow a singleton into a cross-jurisdiction cluster; the synthesis view scales to it data-drivenly.
  | Phase N+1: add a source to grow a singleton into a cross-jurisdiction cluster. | data/typology-map.json
- The Phase-23 partial-commit defect (committed dist passed but committed INPUTS didn't → drift guard red
  on main) is the SECOND time durability/CI enforcement would have caught a real issue earlier —
  strengthens the deferred Phase-9 "pre-commit/CI --check enforcement" item. | Phase N+1: a pre-commit/CI
  gate running --check all + --selftest + the harness. | log.md Phase-9 deferred item
- Lesson: run `--check all` against the COMMITTED tree / a clean checkout, not just the working tree — a
  working-tree verify can pass while a commit is partial. | pre-commit discipline. | this journal precondition
- The demo is at Definition of Done again (Phase 24 adds analytical depth on the 4-source/2-jurisdiction
  corpus). | /dev-plan only for a net-new stakeholder ask. | _CURRENT_STATE Recommended Next Action
