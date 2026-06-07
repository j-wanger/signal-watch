---
title: "Phase 22: FINTRAC as corpus source #4"
aliases: ["phase-22-fintrac-corpus-source"]
category: phases
tags: [corpus, multi-source, fintrac, cross-jurisdiction, verbatim, non-negotiable, gate, crown-copyright]
parents: [phase-21-ofac-corpus-source]
created: 2026-06-06
updated: 2026-06-06
source: plan
status: completed
scope: ["scripts/derive_signals.py", "scripts/acquire_fincen.py", "scripts/pdf_to_md.py", "scripts/build.py", "data/fintrac/**", "corpus.html", "dist/corpus/index.html", "tests/**", "CLAUDE.md", "README.md", "HANDOFF.md", ".gitignore"]
entry_criteria: "Phase 21 complete + accepted + committed (68ee1dc + f61f92c); the corpus ships 32 derived across 36 publications via the CORPUS_SOURCES registry across 3 sources (FinCEN advisories + alerts + OFAC); the quote-grounding gate normalize/check_record is source-agnostic + byte-frozen; the OFAC source-#3 add proved the add-an-anchor-set widening pattern holds with 0 regression. User chose FINTRAC as source #4 (the demo's first cross-jurisdiction source — 'this demo is for a Canadian bank after all') + the verbatim-corpus path over paraphrase-corpus/paraphrase-showcase, and signed off (2026-06-06 'proceed') on extending the verbatim non-negotiable with FINTRAC as a Crown-copyright non-commercial reproduction LICENCE (NOT public domain)."
exit_criteria: "FINTRAC registered as source #4 in CORPUS_SOURCES (data/fintrac/, doc_type FINTRAC); ≥3 OAs acquired (hand-curated index.json) → converted → derived via the inverted loop, each --check-derived clean; the rf_region anchors widened for FINTRAC 'indicators' vocab (narrow, ML/TF-specific) + the issuer parameterized, with ZERO FinCEN/OFAC regression (all 32 records --check-derived clean, --selftest passes incl. new bidirectional FINTRAC fixtures, every FinCEN+OFAC md's rf_region byte-unchanged); --check all zero drift; the 3 existing sources + the showcase byte-frozen; corpus.html shows FINTRAC docs with an honest FINTRAC chip + a 4-type count line + SOURCE-AWARE attribution (never 'public domain' for FINTRAC); the harness extended for a FINTRAC record walking the arc; the verbatim non-negotiable extended to add FINTRAC (Crown-copyright non-commercial reproduction licence, NOT public domain; FINTRAC attribution required; not commercial redistribution; other non-US/non-FINTRAC still paraphrase) in CLAUDE.md + HANDOFF; README + CLAUDE document source #4."
---

# Phase 22: FINTRAC as corpus source #4

## Objective

Add FINTRAC (Canada's FIU, Financial Transactions and Reports Analysis Centre of Canada) as the
FOURTH corpus source in the multi-source explorer — the demo's FIRST move beyond US-federal (US
Treasury FinCEN + OFAC → +Canada FINTRAC). Reuse the Phase-20 CORPUS_SOURCES registry, the inverted-loop
derivation, and the quote-grounding gate; the grounding core (normalize/check_record) stays
BYTE-UNTOUCHED. Acquire FINTRAC Operational Alerts (OAs) hand-curated (their PDF-version URLs),
convert to md, derive via the existing inverted loop + a NARROW widening of the gate's relevance
anchors for FINTRAC's "indicators" heading vocab, and render source-aware FINTRAC attribution (never
the US-federal "public domain" string). Extend the verbatim non-negotiable to add FINTRAC as a
Crown-copyright NON-COMMERCIAL reproduction LICENCE (NOT public domain — distinct from US-federal
17 USC §105).

## Scope

The UNFREEZE (edits allowed):
- `scripts/derive_signals.py` — WIDEN the rf_region anchor set with NARROW FINTRAC "indicators"
  heading anchors (`_RF_HEADER_FINTRAC` / `_RF_INTRO_FINTRAC` for "Money laundering / Terrorist
  (activity) financing / ML&TF indicators") + parameterize the `corpus_status_records` issuer
  (FINTRAC). Constrained: ZERO FinCEN/OFAC regression. Deliberately NARROW (NOT a broad
  "<cat> indicators") to avoid shifting fin-2020-a008's "Financial/Behavioral Indicators" region.
- `scripts/{acquire_fincen,pdf_to_md}.py` — `--source data/fintrac` reuse + reuse/extend the OFAC
  `_to_pdf_url` direct-download handling for the FINTRAC PDF-version URL form. `crawl_fincen.py`
  stays FinCEN-only (no FINTRAC crawler).
- `data/fintrac/**` — new source dir (hand-curated index.json + md committed; raw/ gitignored).
- `scripts/build.py` — register `fintrac` (doc_type "FINTRAC") in `CORPUS_SOURCES` (one entry).
- `corpus.html` + `dist/corpus/index.html` — make the menu count line 4-type-aware; render FINTRAC's
  required attribution in the source panel SOURCE-AWARE (never the "public domain" string for FINTRAC).
- `tests/**`, `CLAUDE.md`, `README.md`, `HANDOFF.md`, `.gitignore` — harness + docs + the
  non-negotiable extension + the raw-ignore.

FROZEN byte-untouched: `index.html`, `config/**`, the 3 typology dists, AND the THREE existing
sources `data/fincen/**` + `data/fincen-alerts/**` + `data/ofac/**` (mds + derived +
corpus-status.json) — prove source #4 via the MERGE, not a migration.

## Exit Criteria

> READY FOR COMPLETION 2026-06-06 — all 6 tasks [x], all exit criteria MET, reviewer 9/10 ACCEPT (no
> CRITICAL/HIGH; one MEDIUM `config/schema.md` stale claim FIXED inline; one LOW OFAC provenance noun
> pre-existing/frozen, noted). Status stays `active` until the commit lands + the delivery gate flips
> (delivery-flow Step D3). Implemented 35 derived across 39 publications, 4 sources, 2 jurisdictions.

- [x] FINTRAC registered as source #4 in `CORPUS_SOURCES` (`data/fintrac/`, doc_type "FINTRAC")
- [x] ≥3 OAs acquired (hand-curated index.json) → converted → derived via the inverted loop, each
      `--check-derived` clean (3 OAs / 42 ind / 11 BUILD_NOW; TF honestly SOURCE_DATA-heavy)
- [x] rf_region anchors widened for FINTRAC "indicators" vocab (narrow, ML/TF-specific) + the issuer
      parameterized, with ZERO FinCEN/OFAC regression: all 32 prior records `--check-derived` clean,
      `--selftest` passing incl. 3 new bidirectional FINTRAC fixtures, every FinCEN+OFAC md's rf_region
      byte-unchanged
- [x] `--check all` zero drift; the 3 existing sources (`data/fincen/`, `data/fincen-alerts/`,
      `data/ofac/`) + the showcase byte-frozen
- [x] corpus.html shows FINTRAC docs with an honest FINTRAC chip + a 4-type count line + SOURCE-AWARE
      attribution (never "public domain" for FINTRAC); harness extended 49→61 (a FINTRAC OA walks the arc)
- [x] the verbatim non-negotiable extended to add FINTRAC (Crown-copyright non-commercial reproduction
      licence, NOT public domain; FINTRAC attribution required; not commercial redistribution; other
      non-US/non-FINTRAC still paraphrase) in CLAUDE.md + HANDOFF; README + CLAUDE document source #4

## Constraints

- GATE REGRESSION (the load-bearing constraint): the rf_region anchor widening MUST keep all 32
  existing records (12 advisory + 17 alert + 3 OFAC) `--check-derived` clean + `--selftest` passing
  AND every FinCEN + OFAC md's rf_region BYTE-UNCHANGED. `check_record` treats `rf_region==None` as a
  HARD violation — the tightest coupling. The FINTRAC anchor is deliberately NARROW (ML/TF-specific)
  because fin-2020-a008 uses "Financial Indicators"/"Behavioral Indicators" headings; a broad
  "<cat> indicators" anchor would shift it. Verified: the FINTRAC-specific forms have 0 collisions
  across all 36 existing mds. (Prevents a permissive "indicators" anchor from shifting an existing
  region — esp. fin-2020-a008's.)
- COMPLIANCE / NON-NEGOTIABLE EXTENSION: FINTRAC publications are reproducible VERBATIM for
  NON-COMMERCIAL use WITH attribution under a Crown-copyright reproduction LICENCE (FINTRAC's Terms &
  Conditions) — explicitly NOT public domain (the US-federal 17 USC §105 basis is no-copyright-at-all).
  Required FINTRAC attribution: © His Majesty the King in Right of Canada + complete title + author +
  "a copy of the version available at <URL>". NOT commercial redistribution (needs FINTRAC written
  permission). All other non-US / non-FINTRAC sources still paraphrase. Keep the "Illustrative data &
  outputs" badge always-on; keep the verbatim attribution visually distinct from it; render it
  SOURCE-AWARE (FINTRAC never shows the US-federal "public domain" string). (Prevents mislabeling
  FINTRAC's Crown-copyright licence as public domain.)
- BYTE-FROZEN: `index.html`, `config/**`, the 3 typology dists, AND the THREE existing sources
  (`data/fincen/**`, `data/fincen-alerts/**`, `data/ofac/**` incl. corpus-status.json + derived/*.json).
  Prove source #4 via the MERGE, not a migration. (Prevents churn on what works.)
- NEVER fabricate a BUILD_NOW; NEVER reproduce a FINTRAC doc without its required attribution. Honestly
  skip any OA with no groundable region (non-derivable, labeled like the 2 FATF advisories / 2
  non-derivable alerts).

## Checkpoints

- CONVERT-ONE-FIRST (T2, mirrors Phase 20/21): acquire + convert ONE FINTRAC OA, run `rf_region(md)`
  AFTER the widening, confirm not None AND confirm the FinCEN/OFAC rf_region baseline shows 0 shift
  before the batch.
- BEFORE COMMITTING the gate edit (T1): confirm all 32 existing records + `--selftest` still pass AND
  every FinCEN + OFAC md's rf_region is byte-unchanged. If ANY shifts → REVERT the widening + narrow
  the anchor.

## Assumptions

- The narrow FINTRAC "indicators" anchor is inert for the 36 existing mds (verified: 0 collisions, and
  the broad-anchor risk on fin-2020-a008 is explicitly avoided), so the existing rf_regions stay
  byte-identical. If false (the widening shifts any FinCEN/OFAC region or fails any of the 32 records —
  complexity contaminates the core, subtraction test fails): REVERT the widening + NARROW the anchor.
- FINTRAC OAs convert to groundable md via the same markitdown path. EVIDENCE (planning probe): FINTRAC
  OAs carry ~30–35 enumerated bulleted ML/TF indicators (a clean derivation surface, same as the FinCEN
  red-flag list / OFAC risk-indicator list); the OAs are HTML pages WITH a PDF version (the PDF keeps
  the md-from-PDF path uniform). If an OA does not anchor/ground → honestly skipped, not forced.

## Notes

- The CORPUS_SOURCES registry (Phase 20) + the Phase-21 OFAC source-#3 add proved the pattern: source
  #4 = a registry entry + a new data dir + (for non-FinCEN heading vocab) a narrow regression-gated
  anchor add. The gate (check_record / rf_region / normalize) is source-agnostic; `--corpus-status
  <source-dir>` already takes any source path.
- What's genuinely NEW vs OFAC (source #3): (1) FIRST cross-jurisdiction source — a DIFFERENT
  compliance basis (Crown-copyright non-commercial reproduction LICENCE, NOT public domain); (2) the
  gate vocab is FINTRAC's "indicators" heading (vs FinCEN "red flags" / OFAC "risk indicators"),
  deliberately NARROW (ML/TF-specific); (3) SOURCE-AWARE attribution rendering (FINTRAC must NEVER show
  the "public domain" string).
- Acquisition: FINTRAC OAs are HTML pages WITH a PDF version → `data/fintrac/index.json` is
  HAND-CURATED ({id,title,date,type,url=the OA PDF-version URL}); `acquire_fincen.py`/`pdf_to_md.py`
  reused via `--source data/fintrac` + the OFAC `_to_pdf_url` direct-download handling (reused/extended
  for the FINTRAC PDF URL form). No FINTRAC crawler (`crawl_fincen.py` stays FinCEN-only).
- The `corpus_status_records` issuer is parameterized (FinCEN / OFAC / FINTRAC). corpus.html's doc_type
  chip is DATA-DRIVEN → a fourth type flows through the chip; the menu COUNT line becomes 4-type-aware,
  and the source panel attribution becomes SOURCE-AWARE.
- gitignore is per-source (`data/fincen/raw/`, `data/fincen-alerts/raw/`, `data/ofac/raw/`) → add
  `data/fintrac/raw/`.
- Proof batch ~3–4 OAs spanning ML+TF vocab (e.g. underground banking, synthetic-opioids/fentanyl
  [cross-links the existing showcase], a TF Operational Alert to exercise "Terrorist financing
  indicators"); the exact set is finalized at T3 by what anchors + grounds. Honest BUILD_NOW where
  FI-observable; never fabricate a BUILD_NOW to hit a count.
- WIKI: the FinCEN advisory structure / red-flag→signal derivation pattern (working-knowledge.md,
  uses:2) generalizes to FINTRAC OAs — the enumerated ML/TF indicator list IS the derivation surface
  (same as the FinCEN red-flag list / OFAC risk-indicator list). NEW cross-phase fact: FINTRAC
  publications are reproducible VERBATIM for NON-COMMERCIAL use WITH attribution (Crown copyright + an
  explicit reproduction LICENCE), distinct from the US-federal 17 USC §105 public-domain basis. Source:
  https://fintrac-canafe.canada.ca/help-aide/no-av-eng
