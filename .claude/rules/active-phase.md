# Active Phase Context

Phase: 30 — Data-source lens: surface the D1–D20 data-source axis as an institution coverage-BY-DATA-SOURCE view in the corpus explorer (M7) — the symmetric counterpart to the Phase-29 capability lens. DELIVERED → READY FOR COMPLETION (all 3 tasks T1–T3 done; exit criteria met); delivery gate pending the user's accept + commit/push to main.

Objective: answer coverage PER DATA SOURCE across the whole corpus — "do we even have the DATA FEED?" (an access/vendor problem) vs the capability lens's "do we have the detection CAPABILITY?" (a build problem). Distinct payoff: 7 of 20 data sources have posture "not yet" — exactly the SOURCE_DATA indicators buried per-doc, now corpus-wide legible.

What shipped: (T1) a 4th co-equal Select mode (Documents / Typologies / Capabilities / Data sources) with `dsAgg`/`indsForDS` → a per-source card (posture + demand count + covered/partial/gap, gap-sorted, group line omitted). (T2) `renderDataSource` drill-through (indicators grouped by source doc + a coverage gauge + the inverse "Implements capabilities" panel) + Back via `fromDataSource`. (T3) harness +27 (190→217); rebuilt dist/corpus; docs (CLAUDE.md, README.md, smoke-checklist.md). BACKEND already built in Phase 29 — ZERO build/data change.

Constraints held: FROZEN byte-clean — the showcase (index.html + config/** + 3 typology dists), every source md, every corpus-status.json, data/typology-map.json, data/capability-taxonomy.json, scripts/build.py, the grounding core derive_signals.py, all 42 derived records, AND HANDOFF.md. Honest re-projection only (per-data-source demand counts + interview posture), NO fabricated/overlap/lift number, the always-on badge stays. NO non-negotiable change.

Exit criteria: MET — Data-sources Select mode + drill-through + Back; honest counts only; frozen set byte-clean; `--check all` 4/4 ZERO DRIFT; `--selftest` PASS; all 42 `--check-derived` clean; harness 217 green.

Abort: n/a (delivered, no deviations). Blocked >3 attempts → ask the user: skip or abort.

Gates:
- [x] Direction confirmed by user (D-lens only chosen at the goal gate; OSFI disposed as non-derivable; no second Canadian source exists; 2026-06-08)
- [ ] Delivery accepted (post-implementation report)
