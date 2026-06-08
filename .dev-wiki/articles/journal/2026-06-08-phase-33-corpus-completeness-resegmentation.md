---
title: "Phase 33: Corpus completeness + full typology re-segmentation"
aliases: []
category: journal
tags: [m7, corpus, completeness, source-set, fincen, fintrac, guidance-directives, typology, re-segmentation, trade-based-money-laundering, workflow, multi-source, html-acquisition]
parents: [phase-33-corpus-completeness-resegmentation]
created: 2026-06-08
updated: 2026-06-08
source: debrief
duration: unknown
---

# Phase 33: Corpus completeness + full typology re-segmentation

## What Happened

The corpus is the primary demo (Phase 27). The user reviewed the BUILT corpus and found the SOURCE SET incomplete — a DIFFERENT defect from Phase-28's within-doc extraction completeness (there each doc shipped too few of its OWN flags; here the corpus was missing whole DOCUMENTS): missing FinCEN advisories "especially the latest" + FINTRAC "way way off — so much in the Obligations/Guidance section we didn't pull". At the goal gate the user chose MAXIMAL on BOTH axes — corpus completeness = ALL 11 FINTRAC `/guidance-directives/` per-sector ML/TF indicator pages + the latest & 2018-19 FinCEN back-catalog; typology = a FULL vocabulary review — consistent with the prioritizes-scale-over-showcase-polish posture, and called for a "dedicated dynamic workflow".

Delivered the full six-task arc:
- **T1** — acquired + converted 16 new docs (5 FinCEN advisories + 11 FINTRAC guidance pages) via a NEW HTML→md authoring path (guidance is HTML, not the Phase-22 `<page>.pdf` sibling): `acquire_fincen.py` gained `--html` (BOM-tolerant raw fetch), `pdf_to_md.py convert()` accepts an `.html` raw source + an "indicators guidance" FINTRAC provenance kind (existing PDF branches byte-identical). The `derive_signals.py` anchor work (T2-scoped) was done HERE as a prerequisite to verify the acquired guidance grounds — surfaced + handled inline (DEPENDENCY escape hatch), all regression-gated.
- **T2** — the dedicated derivation Workflow (28 agents) → 1,376 new indicators, deterministic apply + the grounding gate; 3 regression-gated rf_region anchor additions in the grounding core.
- **T3** — capability-posture grounding COLLAPSED TO A NO-OP: 0 of 1,376 new indicators needed flagging — every one mapped to the existing 28-capability/20-data-source taxonomy. `ph33_apply.py` reported 0 flagged. This validated the Phase-28 interview's comprehensiveness; no targeted re-interview was needed.
- **T4** — full typology re-segmentation: vocab 22→27 (+trade-based-money-laundering, virtual-currency, unlawful-employment, casino-gaming, fintrac-sector-baselines), 42→56 mapped docs; TBML re-segmented onto ofac-sham-transactions.
- **T5** — a 5th CORPUS_SOURCES registry entry (`fintrac-guidance`, doc_type "FINTRAC Guidance", jurisdiction Canada) + corpus.html SRC_ORDER 4→5 source groups + a guidance stat count; dist rebuilt; drift guard green.
- **T6** — corpus harness +16 (217→233), news harness byte-frozen at 65/65; docs + regate.

The corpus roughly TRIPLED: 875→2,251 indicators (+1,376, 2.6×), 42→56 derived records, dist/corpus 2.46→4.87MB.

## Decisions Made

- Phase 33 scope MAXIMAL on both axes (the user's goal-gate choice) — all 11 FINTRAC guidance pages + the FinCEN back-catalog; a FULL typology vocab review.
- Sector-page typology mapping = "closest crime typology each" (user's goal-gate choice): the 10 derivable FINTRAC guidance pages are per-SECTOR baselines spanning all crime typologies → real-estate→real-estate, virtual-currency→virtual-currency, casinos→casino-gaming (new), the rest→fintrac-sector-baselines (new). TBML re-segmented onto ofac-sham-transactions.
- New FINTRAC guidance → a NEW `data/fintrac-guidance/` dir + a 5th CORPUS_SOURCES entry (keeps `data/fintrac/` OAs byte-frozen) + a new HTML→md acquisition path.
- Grounding core got the anticipated CONDITIONAL regression-gated touch — 3 rf_region anchor additions (markdown-ATX-prefix tolerance, FINTRAC topic-leading "<topic> ML/TF indicators", FinCEN "Red Flag Indicators for <topic>"); the grounding LOGIC (normalize/check_record/matrix) byte-UNCHANGED; 3 new --selftest fixtures pin them.
- New-indicator coverage INHERITED-or-INTERVIEWED, never fabricated: 0 of 1,376 flagged (T3 a no-op).
- 2 docs honestly NON-DERIVABLE: BEC fin-2019-a005 (defers to the 2016 BEC advisory, no own enumerated list); FINTRAC Agents-of-the-Crown guidance (defers to general indicators).

## Problems Solved

- FINTRAC guidance grounding — the guidance heading forms didn't match the existing `_RF_HEADER_FINTRAC` anchors; resolved with 3 narrow regression-gated rf_region anchor additions (`_RF_MD_HEADER_PREFIX` strip, `_RF_HEADER_FINTRAC_LEAD`, `_RF_HEADER_RFI_FOR`), each 0-shift across the 46 frozen mds, pinned by 3 new selftest fixtures. The grounding logic itself stayed byte-unchanged.
- One ALLOWED frozen-region deviation: the "Red Flag Indicators for" anchor CORRECTS fin-2024-alert005's rf_region (27→444); it stays `--check-derived` clean (its flags src_line 456-532 fall inside the corrected region).
- HTML acquisition — DOJ/gov-site fetching hits bot-protection; routed authoring-only (the ship stays offline). The new `--html` path handles the FINTRAC guidance HTML pages.

## Artifacts Changed

- `scripts/acquire_fincen.py` (NEW `--html` fetch path, BOM-tolerant)
- `scripts/pdf_to_md.py` (`convert()` accepts `.html` raw source + "indicators guidance" FINTRAC provenance; existing PDF branches byte-identical)
- `scripts/derive_signals.py` (3 new rf_region anchors + 3 selftest fixtures; grounding logic byte-unchanged)
- `scripts/build.py` (ADDITIVE: 5th `fintrac-guidance` CORPUS_SOURCES entry)
- `data/fincen/{fin-2026-a002,fin-2019-a006,fin-2019-a005,fin-2019-a003,fin-2018-a003}.md` + `index.json` + 4 new `derived/*.json` + `corpus-status.json`
- `data/fintrac-guidance/**` (NEW dir: 11 mds, 10 derived, index.json, corpus-status.json)
- `data/typology-map.json` (vocab 22→27, 42→56 mapped docs)
- `corpus.html` (SRC_ORDER 4→5 source groups + a guidance stat count)
- `dist/corpus/index.html` (rebuilt, 2.46→4.87MB)
- `tests/corpus-explorer.test.mjs` (+16 → 233), `tests/smoke-checklist.md`
- `CLAUDE.md`, `HANDOFF.md`, `README.md`

## Related

- [[phase-33-corpus-completeness-resegmentation|Phase 33: Corpus completeness + full typology re-segmentation]] — parent phase

## Health Delta

- corpus harness 217→233 (+16 Phase-33 assertions); news harness 65/65 (byte-frozen)
- corpus 875→2,251 indicators (+1,376, 2.6×); 42→56 derived records; dist/corpus 2.46→4.87MB
- `--check all` 5/5 ZERO DRIFT; `--selftest` PASS; all 56 `--check-derived` clean
- typology vocab 22→27; CORPUS_SOURCES 4→5

## Soft Observations / Phase 34 Candidates

- The capability/data-source ASSIGNMENT for the 1,376 new indicators was the neural step (agent-assigned), gated only by VALIDITY (in-vocab), not correctness; at this scale some mis-assignments are likely. Coverage is disclosed illustrative, but a future phase could spot-check/verify the C/D assignments (ties to the ground-judgments-in-a-user-interview memory). | Phase 34: a C/D-assignment verification pass over the 1,376 new indicators | Evidence: `ph33_apply.py` reported 0 flagged across 1,376 (validity-only gate).
- The 7-doc `fintrac-sector-baselines` cluster is a SECTOR bucket inside a CRIME-typology map (the one-typology-per-doc invariant forced it). A future phase could add a proper SECTOR axis if the demo wants sector-level navigation. | Phase 34: a sector axis (4th lens) | Evidence: the sector pages span all crime typologies.
- TBML is thin (1 doc — ofac-sham-transactions). Future trade-based-ML-specific source content would strengthen the cluster. | Phase 34: a TBML-specific source (e.g. FATF/Egmont TBML indicators) | Evidence: no doc in the corpus is purely TBML.
- The 10 FINTRAC guidance pages share a heavy common spine (~116-175 indicators each, large overlap); ingested per-doc (honest, no cross-source dedup per the Phase-24 gate). A future phase could surface the shared-spine as a coverage-density signal IF cross-source matching is done honestly. | Phase 34: a shared-spine coverage-density signal (honest matching only) | Evidence: the 10 sector pages overlap heavily.
