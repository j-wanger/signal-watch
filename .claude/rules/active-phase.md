# Active Phase Context

Phase: 24 - Cross-corpus synthesis — a typology lens over the 4-source/2-jurisdiction corpus (M7) — DELIVERED 2026-06-07; all 4 tasks [x]; exit criteria GREEN (--check all 4/4 zero drift, --selftest PASS, harness 74→98, frozen set + grounding core derive_signals.py byte-clean); reviewer 9/10 ACCEPT, no CRITICAL/HIGH, two LOW FIXED INLINE (validate_typology set→dict annotation; jchip xx neutral class). READY FOR COMPLETION pending commit. The corpus is now ANALYTICAL: group-by-TYPOLOGY → cross-jurisdiction cluster + honest COMBINED coverage → drill-through to the per-doc arc; 5 cross-jurisdiction + 2 cross-agency clusters + 11 honest singletons. Demo at Definition of Done; run /dev-plan only for a net-new ask.

Objective (all DELIVERED): T1 (M) author data/typology-map.json (22-term vocab + 42-entry doc→typology map; jurisdiction from the source registry) + build-boundary gate in build.py (load_typology_map + validate_typology, fail-loud) + CLUSTER-VERIFY checkpoint PASS (5 cross-jurisdiction) · T2 (L) the synthesis capability — build.py merges typology/jurisdiction into __CORPUS__; corpus.html adds the Documents/Typologies toggle + the synthesis view (cluster + union COMBINED coverage + per-jurisdiction counts + drill-through; NO similarity/overlap/lift) · T3 (S) rebuild dist/corpus 635KB + drift guard + harness 74→98 · T4 (S) docs CLAUDE.md + README.md.

Scope (the UNFREEZE, all consumed): `data/typology-map.json` (NEW overlay), `scripts/build.py` (gate + merge — first structural touch since Phase 20), `corpus.html` (the synthesis view), `dist/corpus/index.html`, `tests/**`, `CLAUDE.md`, `README.md`. FROZEN byte-untouched (verified): `index.html`, `config/**`, the 3 typology dists, the grounding core `scripts/derive_signals.py` + the authoring scripts, ALL 4 source dirs (`data/fincen/**` + `data/fincen-alerts/**` + `data/ofac/**` + `data/fintrac/**` — mds + derived + corpus-status.json), and the six-act showcase. The typology label is an OVERLAY, not a migration.

Key constraints (all HELD):
- HONESTY GATE (ties to the Phase-18 precision-lift rejection): combined coverage = honest UNION arithmetic; per-jurisdiction = honest counts; every clustered indicator traceable to source + jurisdiction. NO similarity/overlap/lift number; NOT de-duplicated/matched across regulators (disclosed in a framenote).
- SUBTRACTION + GATE LOCATION: the overlay is a SEPARATE committed file, NOT 42 derived-record edits → the source dirs + the grounding core stay byte-frozen. Validated at the BUILD BOUNDARY in build.py, NOT in the grounding gate.
- PER-DOC ARC PRESERVED: the synthesis lens is additive; the per-doc 5-screen arc unbroken + regression-clean (doc mode byte-identical, harness held). NO non-negotiable change (the always-on badge + the verbatim US-federal-public-domain + FINTRAC-Crown-copyright bases stay).

Exit criteria (all MET): see the DELIVERED line above.
Abort (NOT needed): if T1 had found no genuine cross-jurisdiction cluster, DEGRADE to same-jurisdiction cross-doc-type clusters; if a beat needed a fabricated number, CUT it. Blocked >3 attempts → ask the user: skip or abort.

Gates:
- [x] Direction confirmed by user (cross-corpus synthesis at the goal gate over navigability/durability/more-scale; the group-by-typology integration shape + the build.py-boundary gate refinement signed off; 2026-06-07)
- [x] Delivery accepted (post-implementation report 2026-06-07; reviewer 9/10 ACCEPT, two LOW fixed inline; impl + debrief commit c07d72c)
