# Active Phase Context

Phase: 21 - OFAC as corpus source #3 (gate widened for OFAC vocab; US-federal public-domain) — M7 — DELIVERED 2026-06-06; all 6 tasks [x]; exit criteria GREEN (--selftest PASS incl. 3 OFAC fixtures, --check all 4-artifact zero drift, all 32 derived --check-derived clean, harness 49/49, 0 FinCEN rf_region shift); reviewer 9/10 ACCEPT, one MEDIUM (comment inaccuracy) FIXED. DELIVERED + accepted (committed 68ee1dc + pushed). The demo is at Definition of Done with a 3-source corpus (FinCEN advisories + alerts + OFAC, US-federal verbatim); run /dev-plan only for a net-new stakeholder ask.
Objective: T1 (L) WIDEN the rf_region anchors for OFAC vocab (_RF_HEADER_OFAC/_RF_INTRO_OFAC) + parameterize the issuer (FinCEN/OFAC), regression-gated to 0 FinCEN rf_region shift; grounding core normalize/check_record byte-untouched · T2 hand-curated OFAC acquisition (_to_pdf_url direct-download tweak, 3 docs) · T3 3 OFAC derivations via the inverted loop (19 ind / 4 BUILD_NOW) · T4 build.py source #3 + corpus.html 3-type menu · T5 regen + rebuild + harness 40→49 · T6 docs + the compliance non-negotiable extension.

Scope (the UNFREEZE, all consumed): `scripts/derive_signals.py` (anchors + issuer + 3 selftest fixtures + comment), `scripts/acquire_fincen.py` (_to_pdf_url), `data/ofac/**` (NEW source #3), `scripts/build.py` (register OFAC), `corpus.html` + `dist/corpus/index.html`, `tests/**`, `CLAUDE.md`, `README.md`, `HANDOFF.md`, `.gitignore`. FROZEN byte-untouched (verified): `index.html`, `config/**`, the 3 typology dists, `data/fincen/**` + `data/fincen-alerts/**` (mds + derived + corpus-status.json).

Key constraints (all HELD):
- GATE REGRESSION: the widening kept all 29 FinCEN records `--check-derived` clean + `--selftest` passing AND every FinCEN md's rf_region BYTE-UNCHANGED (baseline of all 33 captured pre-change → 0 shifted). The grounding/traceability core (normalize/check_record) is byte-untouched — only the rf_region relevance anchors widened.
- COMPLIANCE: the verbatim relaxation extends to US-federal ONLY (17 USC §105 — FinCEN + OFAC + US federal). NOT FINTRAC (Crown copyright → paraphrase) or any non-US/non-government source. Always-on "Illustrative data & outputs" badge + the verbatim attribution kept distinct. Updated identically in CLAUDE.md + HANDOFF.md.
- NEVER fabricate a BUILD_NOW — honest 3-not-4 OFAC yield (small anchorable set), maritime honestly SOURCE_DATA-heavy; non-anchoring OFAC docs honestly skipped.

Exit criteria (all MET): see the DELIVERED line above.
Abort (NOT needed): if the widening had shifted ANY FinCEN rf_region, REVERT + fall back to the small-clean-source. Blocked >3 attempts → ask the user: skip or abort.

Gates:
- [x] Direction confirmed by user ("widen the gate for OFAC" over small-clean-source / hold-OFAC; US-federal public-domain extension signed off — 2026-06-06)
- [x] Delivery accepted (post-implementation report 2026-06-06; reviewer 9/10 ACCEPT, no CRITICAL/HIGH; impl commit 68ee1dc)
