---
title: "Phase 22: FINTRAC as corpus source #4 (first cross-jurisdiction source; gate widened for FINTRAC 'indicators' vocab; Crown-copyright non-commercial reproduction) (M7)"
aliases: ["2026-06-06-phase-22-fintrac-corpus-source"]
category: journal
tags: ["M7", "fintrac", "cross-jurisdiction", "multi-source", "corpus", "non-negotiable", "crown-copyright", "gate", "regression-gated", "lite"]
parents: ["phase-22-fintrac-corpus-source"]
created: 2026-06-06
updated: 2026-06-06
source: debrief
duration: long
---

# Phase 22: FINTRAC as corpus source #4 (first cross-jurisdiction source) (M7)

## What Happened

Added FINTRAC (Canada's FIU) as the FOURTH corpus source — the demo's FIRST move beyond US-federal
(US Treasury FinCEN + OFAC → +Canada FINTRAC), and its first cross-jurisdiction source. This reused
the Phase-20 CORPUS_SOURCES registry, the inverted-loop derivation, and the quote-grounding gate; the
grounding core (`normalize`/`check_record`) stayed BYTE-UNTOUCHED. Chosen at the gate over
paraphrase-corpus / paraphrase-showcase ("this demo is for a Canadian bank after all").

T1 (the L task) widened the rf_region anchors for FINTRAC's "indicators" heading vocab —
`_RF_HEADER_FINTRAC` (a standalone "Money laundering / Terrorist (activity) financing / ML&TF
indicators" line) + `_RF_INTRO_FINTRAC` (the matching intro), ML/TF-QUALIFIED so a bare "indicators"
never anchors. Deliberately NARROW (NOT a broad "<cat> indicators") because fin-2020-a008 uses
"Financial Indicators"/"Behavioral Indicators" headings — a broad anchor would shift it. The
ML/TF-qualified phrasing has 0 occurrences ANYWHERE across all 36 existing FinCEN+OFAC mds (stronger
than OFAC's Phase-21 inertness — not even mid-prose), so the regression gate held perfectly: rf_region
dump diffed new-vs-HEAD = 0 shifted, all 32 existing records `--check-derived` clean, `--selftest` PASS
with 3 new bidirectional FINTRAC fixtures. The `corpus_status_records` issuer was parameterized
(FINTRAC iff "fintrac" in dir) AND gained a per-source `licence` suffix — FINTRAC carries the
Crown-copyright basis, never "public domain (17 U.S.C. 105)"; FinCEN/OFAC output stays BYTE-IDENTICAL.

An in-flight CHECKPOINT-driven refinement (regression-safe) handled the synthetic-opioids OA, which
heads its list "Money laundering indicators OF synthetic opioid activity" (a section-title trailing
clause the strict `:?$` header missed) — widened `_RF_HEADER_FINTRAC` to allow an optional trailing
`of/related to/for…` clause (mirrors FinCEN's strict-vs-LOOSE header split), STILL 0-collision since
the ML/TF base phrase occurs 0×. Acquisition was hand-curated; `acquire_fincen.py` `_to_pdf_url` needed
NO tweak (FINTRAC serves a `<page>.pdf` absolute URL the existing direct-download branch already
handled — the planned tweak was a no-op). DISCOVERY: `pdf_to_md.py`'s provenance header hardcoded
"FinCEN … public domain, 17 U.S.C. 105" → made source-aware (a FINTRAC branch records the Crown-copyright
basis; FinCEN/OFAC branch byte-identical so frozen mds reproduce exactly).

3 OAs acquired + converted + derived via the inverted loop (one extraction subagent per OA on the FI
lens of a mid-size Canadian PCMLTFA reporting entity, each independently re-checked): underground-banking
(14 ind / 4 BUILD_NOW), terrorist-financing (13 / 3 — honestly SOURCE_DATA-heavy: 4/13 hinge on external
attribution a bank can't observe), synthetic-opioids (15 / 4 — the Canadian fentanyl counterpart). 42
indicators, 11 BUILD_NOW; all 3 `--check-derived` clean. build.py registered `fintrac-advisories` as
source #4; corpus.html got a 4-type menu AND — compliance-critical — three blanket "public domain
(17 U.S.C. §105)" claims (footer/lead/framenote) that became FALSE with FINTRAC added were corrected to
the multi-jurisdiction reality (US-federal public domain + FINTRAC Crown-copyright non-commercial
licence). The per-doc source attribution is data-driven → FINTRAC renders its own Crown-copyright basis,
never "public domain". Harness grew 49→61; the verbatim non-negotiable was extended identically in
CLAUDE.md + HANDOFF.md from "ONE exception" (US-federal) to "TWO verbatim bases" (US-federal public
domain + FINTRAC non-commercial licence). The corpus now ships 35 derived across 39 publications, 4
sources, 2 jurisdictions.

## Decisions Made

- Phase 22 = FINTRAC as corpus source #4, the FIRST cross-jurisdiction source — user chose the
  verbatim-corpus path over paraphrase-corpus / paraphrase-showcase. Reused the registry + inverted
  loop + gate; grounding core byte-untouched. (Lite — `_CURRENT_STATE.md`.)
- Gate vocab widening — NARROW ML/TF-qualified FINTRAC "indicators" anchors, regression-gated to 0
  FinCEN/OFAC shift (0× collision across all 36 mds). A checkpoint refinement added an optional
  section-title trailing clause for the synthetic-opioids OA — still 0-collision. (Lite.)
- Compliance: FINTRAC reproducible VERBATIM for NON-COMMERCIAL use WITH attribution under a
  Crown-copyright LICENCE (per FINTRAC's Terms & Conditions, verified live) — explicitly NOT public
  domain (distinct from US 17 USC §105). Non-negotiable extended FinCEN/US-federal-only → TWO verbatim
  bases, identically in CLAUDE.md + HANDOFF.md; every other non-US/non-FINTRAC source still paraphrases.
  (Lite.)
- Source-aware attribution in corpus.html + a source-aware `pdf_to_md.py` provenance header — FINTRAC
  renders its Crown-copyright basis, never the US-federal "public domain" string. (Lite.)

## Problems Solved

- FINTRAC "indicators" vocab vs the byte-frozen gate — solved by ADDING narrow ML/TF-qualified anchors
  (grounding core untouched), regression-gated to 0 FinCEN/OFAC rf_region shift + all 32 records clean.
- The synthetic-opioids section-title trailing clause ("…indicators OF synthetic opioid activity") that
  the strict header missed — widened the FINTRAC header to allow an optional connector-prefixed trailing
  clause; mirrors FinCEN's strict-vs-LOOSE split, still 0-collision (re-verified).
- Mislabeling risk — a FINTRAC md/source must not claim US public domain. Solved by making BOTH the
  `pdf_to_md.py` provenance header and the corpus.html source panel source-aware; corrected three blanket
  "public domain" claims in corpus.html that became false with a second jurisdiction.
- TF SOURCE_DATA honesty — 4/13 terrorist-financing indicators hinge on external attribution
  (listed-entity / jurisdiction / propaganda-payee) a bank can't observe → SOURCE_DATA, never a
  fabricated signal.
- Review-gate MEDIUM — `config/schema.md:75` carried a stale "verbatim exception is FinCEN-only … does
  NOT extend to FINTRAC" claim that became false this phase → fixed inline (one-line doc-prose
  correction; `config/` was frozen but schema.md is the advisory_full contract prose, not a typology
  config or the engine; `--check all` stayed zero drift, the typology JSONs + engine byte-frozen).

## Open Questions

- None unresolved.

## Artifacts Changed

- `scripts/derive_signals.py` (rf_region anchors WIDENED: `_RF_HEADER_FINTRAC` [ML/TF-qualified, optional
  trailing clause] + `_RF_INTRO_FINTRAC`, ORed in; `corpus_status_records` issuer + per-source `licence`
  parameterized [FINTRAC = Crown-copyright non-commercial, FinCEN/OFAC byte-identical]; 3 new bidirectional
  FINTRAC `--selftest` fixtures. Grounding core `normalize`/`check_record` byte-untouched — regression-gated
  to 0 FinCEN/OFAC rf_region shift)
- `scripts/pdf_to_md.py` (provenance header made SOURCE-AWARE — FINTRAC records the Crown-copyright basis;
  FinCEN/OFAC branch byte-identical. DISCOVERY, folded into T2)
- `scripts/build.py` (CORPUS_SOURCES gained `fintrac-advisories` source #4, doc_type "FINTRAC")
- `data/fintrac/**` (NEW source #4: index.json + 3 md + 3 derived + corpus-status.json; raw/ gitignored)
- `corpus.html` (4-type menu — +fintracN bucket + count line; eyebrow "FinCEN + OFAC + FINTRAC corpus";
  three blanket "public domain" claims corrected to the multi-jurisdiction basis; per-doc attribution
  data-driven → FINTRAC Crown-copyright, never "public domain")
- `dist/corpus/index.html` (rebuilt — 39 publications: 14 Advisory + 19 Alert + 3 OFAC + 3 FINTRAC; 35
  derived/live)
- `tests/corpus-explorer.test.mjs` (49→61: 4-type doc_type-chip count, ≥1 FINTRAC live, a FINTRAC-OA
  full-arc walk, a Crown-copyright-not-public-domain attribution assertion)
- `CLAUDE.md`, `HANDOFF.md` (verbatim non-negotiable extended "ONE exception" → "TWO verbatim bases"
  [US-federal public domain + FINTRAC Crown-copyright non-commercial licence], identically; CLAUDE gained
  a Phase-22 source-#4 bullet; counts → 35/39/4)
- `config/schema.md` (review-gate fix: the stale FinCEN-only verbatim claim corrected to the
  multi-jurisdiction reality — doc-prose only, no behavioral change, `--check all` zero drift)
- `README.md` (corpus counts → 39/35; a FINTRAC source-#4 multi-source paragraph replacing the now-false
  "cross-jurisdiction out of scope" sentence; per-basis verbatim note)
- `.gitignore` (`data/fintrac/raw/`)

## Related

- [[phase-22-fintrac-corpus-source|Phase 22: FINTRAC as corpus source #4]] — parent phase
- [[2026-06-06-phase-21-ofac-corpus-source|Phase 21: OFAC as corpus source #3]] — the registry source #4
  reuses; the anchor-widening pattern Phase 22 narrows to ML/TF-specific vocab
- [[2026-06-06-phase-20-multi-source-spine|Phase 20: Multi-source spine]] — the CORPUS_SOURCES registry

## Review Gate

Unified reviewer (one Agent, adversarial, ran the checks itself) — Score 9/10, Verdict ACCEPT, no
CRITICAL/HIGH. Independently confirmed: 0 of 36 existing rf_regions shift under the FINTRAC anchors
(monkeypatch diff + per-line scan + grep), grounding core byte-untouched, all 42 flags re-grounded (0
ungrounded), no fabricated BUILD_NOW, both non-negotiable wordings present/consistent/accurate, counts
reconcile (39/35/4), frozen set byte-clean. One MEDIUM (`config/schema.md` stale FinCEN-only claim) →
FIXED inline + re-verified (zero drift). One LOW (`data/ofac/*.md` provenance headers say "FinCEN
advisory OFAC-…" — wrong issuer noun; the public-domain licence claim is correct) → pre-existing /
frozen / out of Phase-22 scope → noted, not fixed.

## Soft Observations / Phase N+1 Candidates

- FINTRAC's anchorable OA set extends beyond the 3 derived (real-estate, casinos, armoured-cars, etc.) —
  a cheap no-gate-change follow-on if more FINTRAC depth is ever wanted; but the cross-jurisdiction +
  dual-licence-basis proof is now MADE, so diminishing returns. | next: a no-gate-change FINTRAC-depth
  phase only on a fresh stakeholder ask. | evidence: T3 verify note.
- FINTRAC's running header ("OPERATIONAL ALERT" + variable page numbers) glues into page-break flags
  (same shape as OFAC's Phase-21 obs); handled per-flag via contiguous-span extraction. A future
  `normalize()` hardening could strip it if FINTRAC scales — anti-subtraction today (would reintroduce
  parser-like special-casing), harmless now. | evidence: T3 task line + the OFAC Phase-21 soft-obs.
- Pre-existing LOW (reviewer-noted): `data/ofac/*.md` provenance headers say "FinCEN advisory OFAC-…"
  (wrong issuer noun; the public-domain claim is correct). Frozen Phase-21 artifact, out of Phase-22
  scope; a future un-freeze could correct it for regen-consistency (low value). | evidence: Review Gate.
- The demo is now at Definition of Done with a 4-source, 2-jurisdiction corpus. Run /dev-plan only for a
  net-new stakeholder ask.

### Activation Quality

No `active-knowledge.md` present this session (lite ceremony, no knowledge-wiki activation file) —
activation quality not measured.
