---
title: "Phase 33: Corpus completeness + full typology re-segmentation"
aliases: ["phase-33-corpus-completeness-resegmentation"]
category: phases
tags: [m7, corpus, completeness, source-set, fincen, fintrac, guidance-directives, typology, re-segmentation, trade-based-money-laundering, workflow, multi-source]
parents: []
created: 2026-06-08
updated: 2026-06-08
source: plan
status: ready-for-completion
scope: ["scripts/crawl_fincen.py", "scripts/acquire_fincen.py", "scripts/pdf_to_md.py", "data/fincen/*.md", "data/fincen/index.json", "data/fincen/derived/*.json", "data/fincen/corpus-status.json", "data/fintrac-guidance/**", "scripts/derive_signals.py", "data/capability-taxonomy.json", "data/typology-map.json", "scripts/build.py", "corpus.html", "dist/corpus/index.html", "tests/corpus-explorer.test.mjs", "CLAUDE.md", "HANDOFF.md", "README.md", "tests/smoke-checklist.md"]
entry_criteria: "Phase 32 (news real-source + presentation elevation) DELIVERED + accepted + committed afb24f4 + pushed to main; the corpus is the primary demo (Phase 27). The user reviewed the BUILT corpus and found the SOURCE SET incomplete (a DIFFERENT defect from Phase-28's within-doc extraction completeness): missing FinCEN advisories 'especially the latest' + FINTRAC 'way way off — so much in the Obligations/Guidance section we didn't pull'. Said 'do both' at the Phase-32 gate → split by frozen set into Phase 32 = news + Phase 33 = corpus; called for 'a dedicated dynamic workflow'. Direction approved at the goal gate 2026-06-08: corpus completeness MAXIMAL on both axes (all 11 FINTRAC /guidance-directives/ sector pages; a full typology vocab review)."
exit_criteria: "The corpus completeness gap closed (5 new FinCEN advisories + 11 FINTRAC guidance sector pages, ~16 docs, roughly DOUBLING the corpus toward ~1500+ indicators) + the typology axis re-segmented (full 22-term vocab review; trade-based-money-laundering added; the sector-page handling resolved). Every new record --check-derived clean + all 42 existing records still clean; new-indicator coverage posture INHERITED-or-INTERVIEWED (zero fabricated); the FINTRAC shared-spine overlap DISCLOSED, never cross-source de-duped; a new fintrac-guidance CORPUS_SOURCES entry + an HTML→md acquisition path; derive_signals.py touched only if needed (regression-gated, every existing rf_region byte-unchanged). build.py --check all ZERO DRIFT (the 3 typology dists + dist/news byte-identical); --selftest PASS; validate_typology + validate_capability_taxonomy clean; node tests/corpus-explorer.test.mjs + node tests/news-stream.test.mjs green; the frozen set byte-clean; NO non-negotiable change."
---

# Phase 33: Corpus completeness + full typology re-segmentation

## Objective

Close the corpus SOURCE-completeness gap and re-segment the typology axis across the expanded corpus, via a dedicated derivation Workflow. Add ~16 new documents (5 FinCEN advisories + all 11 FINTRAC /guidance-directives/ sector "ML/TF indicators" pages), roughly DOUBLING the corpus (~875 → ~1500+ indicators), then review the full 22-term typology vocabulary across the doubled corpus (add `trade-based-money-laundering`; resolve the sector-page handling). All new derivation is ADDITIVE and gated at the build boundary.

## Why now (the defect)

- The corpus is the primary demo (Phase 27). The user reviewed the BUILT corpus and found the SOURCE SET incomplete — a DIFFERENT defect from Phase-28's within-doc extraction completeness: there each doc shipped too few of its OWN flags; here the corpus is missing whole DOCUMENTS.
- FinCEN = a discovery-WINDOW miss (research-confirmed): the crawler floor is 2020 with no re-crawl since 2026-03, so the LATEST advisory (FIN-2026-A002, 18 red flags) + the 2018-19 back-catalog (FIN-2019-A006 the original US fentanyl advisory / A005 BEC / A003 CVC / FIN-2018-A003 PEP, 14 red flags) are absent. Skip the superseded 2020 COVID cluster.
- FINTRAC = a source-AREA miss: all 10 current FINTRAC docs are /intel/ strategic intelligence; ZERO come from /guidance-directives/, the 11 sector "ML/TF indicators" pages (Financial entities master + MSB + real estate + securities + life insurance + DPMS + casinos + accountants + BC notaries + Crown agents + virtual currency), 50-100+ indicators each, HEAVY cross-page shared-spine duplication, HTML not PDF.
- The user chose MAXIMAL on both axes at the goal gate (FINTRAC all 11 pages; a full typology vocab review) — consistent with the prioritizes-scale-over-showcase-polish posture. The audience is a Canadian bank, so deepening FINTRAC weighs Canadian-relevant.

## Scope

- `scripts/{crawl_fincen,acquire_fincen,pdf_to_md}.py` — re-crawl FinCEN (widened window) + a NEW HTML→md acquisition path for the FINTRAC guidance pages (authoring-only).
- `data/fincen/*.md` + `data/fincen/index.json` + `data/fincen/derived/*.json` (NEW only) + `corpus-status.json` — the 5 new FinCEN advisories land in the EXISTING source.
- `data/fintrac-guidance/**` (NEW dir) — the 5th corpus source: the 11 FINTRAC guidance sector pages + derived records + corpus-status.json.
- `scripts/derive_signals.py` — CONDITIONAL, regression-gated only: an rf_region anchor add IFF the guidance heading doesn't ground under `_RF_HEADER_FINTRAC`.
- `data/capability-taxonomy.json` — extended only for flagged non-mapping new indicators (grounded posture).
- `data/typology-map.json` — full vocab review + re-map (add `trade-based-money-laundering`).
- `scripts/build.py` (ADDITIVE: a new `fintrac-guidance` CORPUS_SOURCES entry), `corpus.html`, `dist/corpus/index.html`, `tests/corpus-explorer.test.mjs`, `CLAUDE.md`, `HANDOFF.md`, `README.md`, `tests/smoke-checklist.md`.

## Exit Criteria

- [x] 5 new FinCEN advisories + 11 FINTRAC guidance sector pages acquired with correct provenance headers; the 14 existing FinCEN mds + all 10 FINTRAC OA mds byte-identical.
- [x] Every new derived record `--check-derived` clean; all 42 existing records still `--check-derived` clean; `--selftest` PASS. (56/56 clean.)
- [x] `derive_signals.py` was touched (3 regression-gated anchor adds + 3 selftest fixtures); the grounding LOGIC byte-unchanged, 0-shift across the 46 frozen mds, ONE allowed correction (fin-2024-alert005 region 27→444, stays clean).
- [x] New-indicator coverage posture INHERITED (zero fabricated; 0 of 1,376 flagged — T3 a no-op); `validate_capability_taxonomy` referential integrity holds (taxonomy unchanged).
- [x] The typology axis re-segmented: `validate_typology` passes; `trade-based-money-laundering` present + assigned (ofac-sham-transactions); the sector-page handling resolved ("closest crime typology each", fintrac-sector-baselines bucket); every live doc maps to exactly one term. Vocab 22→27, 42→56 docs.
- [x] A new `fintrac-guidance` CORPUS_SOURCES entry; `dist/corpus` reflects the expanded corpus with the new docs in the SELECT menu (corpus.html SRC_ORDER 4→5).
- [x] `build.py --check all` ZERO DRIFT (5/5; the 3 typology dists + dist/news byte-identical); `node tests/corpus-explorer.test.mjs` (233) + `node tests/news-stream.test.mjs` (65) green; the frozen set byte-clean; NO non-negotiable change.

## Constraints

- ADDITIVE only — the showcase (index.html + config/** + 3 typology dists), the news stream (news.html, dist/news, data/news/**), and all 42 EXISTING derived records + their source mds stay BYTE-FROZEN. Prevents: collateral churn on shipped, accepted artifacts.
- The grounding core `derive_signals.py` is touched ONLY as a regression-gated anchor ADD (never a logic change). Prevents: reintroducing the Phase-17-deleted parser / shifting an existing rf_region.
- New-indicator posture is INHERITED (from the C/D code via the Phase-28 interview + the cover×data matrix) or INTERVIEWED (a short targeted y/n/partial extends the taxonomy with GROUNDED posture). Prevents: fabricated coverage (honesty-over-demo-drama).
- The 11 sector pages share a common spine → ingested as DISTINCT per-doc publications, the overlap DISCLOSED, NEVER cross-source de-duped. Prevents: a fabricated cross-source matching/de-dup number (the Phase-24 gate).

## Checkpoints

- After T2 (the derivation workflow): report the new-indicator count, the per-doc `--check-derived` verdict, whether `derive_signals.py` was touched (and the 0-collision proof if so), and the flagged non-mapping-indicator count — before T3's interview.

## Assumptions

- The FINTRAC /guidance-directives/ heading form grounds under the existing `_RF_HEADER_FINTRAC` anchors. If false: a regression-gated anchor add (narrow, 0-collision verified across all existing mds), resolved during T2. (KNOWLEDGE GAP carried from planning.)
- DOJ/gov-site fetching may hit bot-protection (the Phase-32 experience). If a static crawl/fetch fails: route via the Wayback Machine (authoring-only), as in Phase 32; the ship artifact stays offline. The SearXNG-backed authoring search/fetch (a future candidate, Blockers) could harden this path.

## Notes

- New FINTRAC guidance lives in a NEW `data/fintrac-guidance/` dir + a NEW CORPUS_SOURCES registry entry (the Phase-20 multi-source pattern keeps `data/fintrac/` + its 10 records byte-frozen — multi-source via the merge, not a migration).
- Both compliance bases are already established (FinCEN US-federal 17 U.S.C. §105 public-domain + FINTRAC Crown-copyright non-commercial-with-attribution) → NO non-negotiable change. The FINTRAC guidance docs carry the Crown-copyright provenance/attribution (Phase-22 discipline; the per-doc footer attribution is Phase-28's mechanism).
- The sector-page question (T4): the 11 guidance pages are SECTOR-organized, not single-typology, but the typology-map invariant is one-typology-per-doc — resolve a 'general/sector' handling within that invariant.
- Workflow-driven (the user's call): the acquire→convert→derive→ground fan-out over ~16 docs + the typology re-segmentation is exactly a Workflow. The LLM proposes (extraction + the typology map + the posture); the deterministic gate + the two human gates dispose.
