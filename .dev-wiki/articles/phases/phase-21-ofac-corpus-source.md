---
title: "Phase 21: OFAC as corpus source #3"
aliases: ["phase-21-ofac-corpus-source"]
category: phases
tags: [corpus, multi-source, ofac, verbatim, non-negotiable, gate]
parents: [phase-20-multi-source-spine]
created: 2026-06-06
updated: 2026-06-06
source: plan
status: active
scope: ["scripts/derive_signals.py", "scripts/acquire_fincen.py", "scripts/pdf_to_md.py", "scripts/build.py", "data/ofac/**", "corpus.html", "dist/corpus/index.html", "tests/**", "CLAUDE.md", "README.md", "HANDOFF.md", ".gitignore"]
entry_criteria: "Phase 20 complete + the 11-alert follow-on committed; FinCEN corpus 29/33 derived via the CORPUS_SOURCES registry; the quote-grounding gate is source-agnostic and byte-frozen. User signed off (2026-06-06) on extending the verbatim public-domain non-negotiable from FinCEN-only to US-federal (17 USC §105) AND chose to WIDEN the rf_region gate for OFAC vocab (over a small-clean-source / holding OFAC)."
exit_criteria: "OFAC registered as source #3 in CORPUS_SOURCES (data/ofac/, doc_type OFAC); ≥3 OFAC docs acquired (hand-curated index.json) → converted → derived via the inverted loop, each --check-derived clean (honest 0-BUILD_NOW allowed); the rf_region anchors widened for Risk Indicators/Deceptive Practices/Risk Factors + the issuer parameterized, with ZERO FinCEN regression (all 29 FinCEN records --check-derived clean, --selftest passing incl. a new bidirectional OFAC-heading fixture, every FinCEN md's rf_region byte-unchanged); --check all zero drift; FinCEN sources (data/fincen/, data/fincen-alerts/) + the showcase byte-frozen; corpus.html shows OFAC docs with an honest OFAC chip + a 3-type-aware count line; harness extended for an OFAC record walking the arc; the verbatim non-negotiable extended FinCEN-only→US-federal in CLAUDE.md + HANDOFF (FINTRAC still excluded)."
---

# Phase 21: OFAC as corpus source #3

## Objective

Add OFAC (US Treasury, Office of Foreign Assets Control) as the third corpus source in the
multi-source explorer, WITH a regression-gated widening of the rf_region anchors so OFAC's heading
vocabulary derives. The user chose "widen the gate" over a small-clean-source (red-flag-template OFAC
only, no gate change) or holding OFAC. Extend the verbatim public-domain non-negotiable from
FinCEN-only to US-federal (17 USC §105 — OFAC is a US Treasury component, same statute; user signed
off). Acquire OFAC docs (hand-curated, since the OFAC site is a JS SPA with no static listing),
convert to md, derive via the existing inverted loop + the widened quote-grounding gate, reusing the
CORPUS_SOURCES registry (source #3 = a registry entry, per the Phase-20 design that named OFAC next).

## Scope

The UNFREEZE (edits allowed):
- `scripts/derive_signals.py` — WIDEN the rf_region anchor set ("Risk Indicators"/"Deceptive
  Practices"/"Risk Factors" headings + the risk-indicator intro) + parameterize the
  `corpus_status_records` issuer (FinCEN default / OFAC). Constrained: ZERO FinCEN regression.
- `scripts/{acquire_fincen,pdf_to_md}.py` — `--source data/ofac` reuse + a small `_to_pdf_url` tweak
  to treat an absolute `/media/.../download` (and `/system/files/`) URL as a direct download.
  `crawl_fincen.py` stays FinCEN-only (no OFAC crawler — the SPA has no static listing).
- `data/ofac/**` — new source dir (hand-curated index.json + md committed; raw/ gitignored).
- `scripts/build.py` — register `ofac` (doc_type "OFAC") in `CORPUS_SOURCES` (one entry).
- `corpus.html` + `dist/corpus/index.html` — make the menu count line + the non-Alert→advisory
  bucket (corpus.html:276-277) 3-type-aware; the doc_type chip itself is already data-driven.
- `tests/**`, `CLAUDE.md`, `README.md`, `HANDOFF.md`, `.gitignore` — harness + docs + the
  non-negotiable extension + the raw-ignore.

FROZEN byte-untouched: `index.html`, `config/**`, the 3 typology dists, AND the two existing FinCEN
sources `data/fincen/**` + `data/fincen-alerts/**` (mds + derived + corpus-status.json) — prove
source #3 via the MERGE, not a migration.

## Exit Criteria

- [ ] OFAC registered as source #3 in `CORPUS_SOURCES` (`data/ofac/`, doc_type "OFAC")
- [ ] ≥3 OFAC docs acquired (hand-curated index.json) → converted → derived via the inverted loop,
      each `--check-derived` clean (honest 0-BUILD_NOW allowed where content is non-FI-observable)
- [ ] rf_region anchors widened (Risk Indicators/Deceptive Practices/Risk Factors) + the issuer
      parameterized, with ZERO FinCEN regression: all 29 FinCEN records `--check-derived` clean,
      `--selftest` passing incl. a new bidirectional OFAC-heading fixture, every FinCEN md's
      rf_region byte-unchanged
- [ ] `--check all` zero drift; FinCEN sources (`data/fincen/`, `data/fincen-alerts/`) + the
      showcase byte-frozen
- [ ] corpus.html shows OFAC docs with an honest OFAC chip + a 3-type-aware count line; harness
      extended for an OFAC record walking the arc
- [ ] verbatim non-negotiable extended FinCEN-only → US-federal (17 USC §105) in CLAUDE.md + HANDOFF
      (FINTRAC still excluded); README + CLAUDE document source #3 + the widening + hand-curated acquisition

## Constraints

- GATE REGRESSION (the load-bearing constraint): the rf_region anchor widening MUST keep all 29
  FinCEN records `--check-derived` clean + `--selftest` passing AND every FinCEN md's rf_region
  BYTE-UNCHANGED. `check_record` treats `rf_region==None` as a HARD violation — the tightest
  coupling. Regression risk is verified low (the OFAC heading vocab is ~inert for FinCEN docs:
  "risk indicators" 0 FinCEN mds, "deceptive practic" 0, "risk factors" 1; 0 derived records mention
  them). (Prevents a permissive OFAC anchor from admitting a non-red-flag region in a FinCEN doc.)
- COMPLIANCE / NON-NEGOTIABLE EXTENSION: the verbatim relaxation extends to US-federal ONLY
  (17 USC §105 — FinCEN + OFAC + US Treasury/federal agencies). It does NOT extend to FINTRAC
  (Canadian Crown copyright → still paraphrase) or any non-US/non-government source. Keep the
  "Illustrative data & outputs" badge always-on; keep the verbatim attribution visually distinct
  from it. (Prevents over-broadening the verbatim rail beyond US-federal.)
- BYTE-FROZEN: `index.html`, `config/**`, the 3 typology dists, AND the two existing FinCEN sources
  (`data/fincen/**`, `data/fincen-alerts/**` incl. corpus-status.json + derived/*.json). Prove
  source #3 via the MERGE, not a migration. (Prevents churn on what works — the Phase-20 lesson.)
- NEVER fabricate a BUILD_NOW. OFAC content is sanctions/vessel/compliance-oriented and often
  non-FI-observable → honest 0-BUILD_NOW records are allowed; honestly skip any OFAC doc with no
  groundable region (non-derivable, labeled like the 2 FATF advisories / 2 non-derivable alerts).

## Checkpoints

- CONVERT-ONE-FIRST (T2, mirrors Phase 20): acquire + convert ONE OFAC doc, run `rf_region(md)`
  AFTER the widening, confirm not None before the batch.
- BEFORE COMMITTING the gate edit (T1): confirm all 29 FinCEN records + `--selftest` still pass AND
  every FinCEN md's rf_region is byte-unchanged. If ANY shifts → REVERT the widening.

## Assumptions

- The widening is ~inert for FinCEN docs (verified above), so FinCEN rf_regions stay byte-identical.
  If false (the widening shifts any FinCEN region or fails any of the 29 records — complexity
  contaminates the core, subtraction test fails): REVERT the widening and fall back to the
  small-clean-source (red-flag-template OFAC only, e.g. the Sham Transactions advisory which already
  anchors unchanged — no gate change).
- OFAC PDFs convert to groundable md via the same markitdown path. EVIDENCE (planning probe): the
  Sham Transactions advisory already grounds UNCHANGED (rf_region (82,236), heading "Red Flags:
  Indicia of Sham Transactions"); maritime uses "Deceptive Practices", VC guidance uses "Risk
  Indicators" ("examples of risk indicators may be … who:") — both captured by the widening; the
  ransomware advisory defers red flags to a co-issued FinCEN advisory → no list, honestly skipped.

## Notes

- The CORPUS_SOURCES registry (Phase 20) was built ready for OFAC: build.py:50-56 registers each
  source; the gate (check_record / rf_region / normalize) is source-agnostic; `--corpus-status
  <source-dir>` already takes any source path. The spine is in place — the real Phase-21 work is the
  gate widening + the issuer parameterization + hand-curated acquisition + derivation + the
  compliance extension.
- corpus.html doc_type chip is DATA-DRIVEN (reads `a.doc_type`, defaults "Advisory") → a third type
  flows through the chip with no template edit. The ONLY corpus.html touch is the menu COUNT line
  (corpus.html:276-277 splits only `doc_type === 'Alert'` vs everything-else-as-advisory) — an OFAC
  doc would currently miscount as an "advisory" in the header line. Minor, honest-label fix.
- The hardcoded `f"FinCEN {advisory_no}"` issuer in `derive_signals.py corpus_status_records`
  (line ~529) is parameterized per-source (FinCEN / OFAC).
- gitignore is per-source (`data/fincen/raw/`, `data/fincen-alerts/raw/`) → add `data/ofac/raw/`.
- Acquisition: OFAC's site is a JS SPA with no static advisories listing to crawl, so
  `data/ofac/index.json` is HAND-CURATED from OFAC's public-domain `/media/<id>/download` PDFs
  (no OFAC crawler). `acquire_fincen.py`/`pdf_to_md.py` are reused via `--source data/ofac` + the
  `_to_pdf_url` direct-download tweak (an absolute `/media/.../download` or `/system/files/` URL is
  treated as a zero-hop download).
- OFAC records may be honestly enrichment/source-data-heavy with possibly 0 BUILD_NOW (sanctions/
  vessel content is often non-FI-observable) — that is honest, not a failure; never fabricate a
  BUILD_NOW to hit a count.
