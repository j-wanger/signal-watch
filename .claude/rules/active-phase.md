# Active Phase Context

Phase: 22 - FINTRAC as corpus source #4 (first cross-jurisdiction source; gate widened for FINTRAC "indicators" vocab; Crown-copyright non-commercial reproduction) — M7 — DELIVERED 2026-06-06; all 6 tasks [x]; exit criteria GREEN (--selftest PASS incl. 3 FINTRAC fixtures, --check all 4-artifact zero drift, all 35 derived --check-derived clean, harness 61/61, 0 FinCEN/OFAC rf_region shift, frozen set byte-clean); reviewer 9/10 ACCEPT, one MEDIUM (config/schema.md stale claim) FIXED inline, one LOW (OFAC provenance noun, pre-existing/frozen) noted. DELIVERED + accepted (committed 6765d26). The demo is at Definition of Done with a 4-source, 2-jurisdiction corpus (FinCEN advisories + alerts + OFAC + FINTRAC); run /dev-plan only for a net-new stakeholder ask.
Objective (all DELIVERED): T1 (L) WIDEN rf_region anchors with NARROW ML/TF-qualified FINTRAC "indicators" anchors (_RF_HEADER_FINTRAC/_RF_INTRO_FINTRAC) + parameterize issuer + per-source licence, regression-gated to 0 FinCEN/OFAC shift (0× collision across 36 mds; checkpoint refinement added an optional section-title trailing clause for synthetic-opioids, still 0-collision) · T2 hand-curated acquisition (acquire _to_pdf_url needed NO tweak; pdf_to_md provenance made source-aware) · T3 3 OAs via the inverted loop (42 ind / 11 BUILD_NOW; TF SOURCE_DATA-heavy) · T4 build.py source #4 + corpus.html 4-type menu + source-aware attribution (3 blanket "public domain" claims corrected) · T5 regen + rebuild + harness 49→61 · T6 docs + non-negotiable extension.

Scope (the UNFREEZE, all consumed): `scripts/derive_signals.py`, `scripts/pdf_to_md.py` (source-aware provenance — DISCOVERY), `data/fintrac/**` (NEW source #4), `scripts/build.py`, `corpus.html` + `dist/corpus/index.html`, `tests/**`, `CLAUDE.md`, `README.md`, `HANDOFF.md`, `.gitignore`, `config/schema.md` (review-gate stale-claim fix — justified frozen-set deviation, doc-prose only). `scripts/acquire_fincen.py` was in scope but needed no edit. FROZEN byte-untouched (verified): `index.html`, `config/typologies/**`, the 3 typology dists, `data/fincen/**` + `data/fincen-alerts/**` + `data/ofac/**`.

Key constraints (all HELD):
- GATE REGRESSION: the widening kept all 32 prior records `--check-derived` clean + `--selftest` passing AND every FinCEN+OFAC md's rf_region BYTE-UNCHANGED (reviewer independently confirmed 0 of 36 shift). The grounding core normalize/check_record byte-untouched — only the rf_region relevance anchors widened.
- COMPLIANCE: the verbatim non-negotiable now has TWO bases — US-federal public domain (17 USC §105) + FINTRAC Crown-copyright NON-COMMERCIAL reproduction LICENCE (NOT public domain), with FINTRAC's required attribution, non-commercial-only, every other non-US/non-FINTRAC source still paraphrases. Updated identically in CLAUDE.md + HANDOFF.md; source-aware attribution (FINTRAC never shows "public domain").
- NEVER fabricate a BUILD_NOW — honest 42-ind/11-BUILD_NOW yield, TF honestly SOURCE_DATA-heavy.

Exit criteria (all MET): see the READY FOR COMPLETION line above.
Abort (NOT needed): if the widening had shifted ANY FinCEN/OFAC rf_region, REVERT + narrow the anchor. Blocked >3 attempts → ask the user: skip or abort.

Gates:
- [x] Direction confirmed by user (FINTRAC over the 3 documented directions; verbatim-corpus over paraphrase-corpus/paraphrase-showcase; non-negotiable extension signed off 2026-06-06 "proceed")
- [x] Delivery accepted (post-implementation report 2026-06-06; reviewer 9/10 ACCEPT, one MEDIUM fixed; impl commit 6765d26)
