# Active Phase Context

Phase: 29 — Capability lens: surface the Phase-28 C1–C28 capability / D1–D20 data-source taxonomy as an institution coverage-BY-CAPABILITY view in the corpus explorer (M7). DELIVERED — all 4 tasks T1–T4 [x]; READY FOR COMPLETION (delivery gate pending the user's eyeball-and-accept).

Why: the per-indicator `capability`/`data_source` codes the Phase-28 interview produced (on all 875 indicators) shipped UNUSED. The lens answers coverage PER DETECTION CAPABILITY across the whole corpus (vs PER DOCUMENT) — the executive buy-in view + the realized payoff of the 28+20 interview.

What shipped: a committed, build-validated `data/capability-taxonomy.json` overlay (code → {name, desc, group, posture}, 28 caps + 20 data sources; the Phase-24 pattern) validated fail-loud at the build boundary (`load_capability_taxonomy`/`validate_capability_taxonomy`: shape + posture {y,n,partial} + closed-vocab referential integrity against all 875 codes); a THIRD Select mode (Documents/Typologies/Capabilities) with a per-capability card (posture chip + demand count + covered/partial/gap micro-bar, gap-sorted) + drill-through into the per-doc arc + Back (`fromCapability`). A pure RE-PROJECTION of grounded data — honest counts, NO fabricated/overlap number. Harness 165→190; `--check all` 4/4 ZERO DRIFT; `--selftest` PASS; 42/42 `--check-derived` clean; dist/corpus ~2.43MB.

Constraints held: FROZEN byte-clean — the showcase (index.html + config/** + 3 typology dists), every source md, every corpus-status.json, data/typology-map.json, the grounding core derive_signals.py, AND all 42 derived records (NO re-derivation). HANDOFF.md byte-clean (no compliance/architecture change). NO non-negotiable change. NO fabricated numbers.

Phase-30 candidates (evidence-backed): an OVERLAP/near-dup guard at the extraction gate (exact-equality dedup exists at derive_signals.py:353-361; the overlap case is unguarded); a parallel DATA-SOURCE lens (the D1–D20 axis); revisit the always-on "Illustrative" badge wording now coverage is interview-grounded.

Gates:
- [x] Direction confirmed by user (capability lens chosen at the goal gate; promote the taxonomy to a committed data artifact; 2026-06-07)
- [x] Delivery accepted (post-implementation report 2026-06-07; review 9/10 accept; committed + pushed to main)
