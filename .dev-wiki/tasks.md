# Tasks

> ACTIVE PHASE ONLY. Closed phase blocks live VERBATIM in [articles/tasks-archive-pre-phase-44.md](articles/tasks-archive-pre-phase-44.md) (split out 2026-06-10 by the Phase-44 T6 hygiene trim; per-phase narrative also in the journal + articles/decisions/*). Archived blocks:
> - Phase 48: Brownfield history + LFCM — blueprint extension, triage-elicitation loop, synthetic-history probe + HTML blueprint report — M9
> - Phase 47: Demo-to-program design — the regulatorily defensible agentic AML program (blueprint + gate console) — M9
> - Phase 46: Corpus live derivation mode — local-model agentic derivation through the frozen gate (M7×M8 convergence)
> - Phase 45: Corpus demo presentation polish (pre-presentation day) — M7
> - Phase 44: Live extraction quality: targeted harness, classified fixes, processing page (live news) — M8
> - Phase 43: Live pipeline robustness + progressive presentation (live news) — M8
> - Phase 42: Anchor dossier view + per-scan network visualizer (live news) — M8
> - Phase 41: Entity-resolution schema enrichment (live news) — M8
> - Phase 40: Live red-flag extraction quality (measure-first) — M8
> - Phase 39: Live news QOL — streamed extraction progress + one-shot URL acquisition
> - Phase 38: Consolidate the live news subsystem (verify agent backend + watchlist management)
> - Phase 37: Per-indicator typology (corpus Typologies lens)
> - Phase 36: Persistence (DuckDB→parquet) + feedback watchlist — M8
> - Phase 35: News live local-model backend — M8
> - Phase 34: C/D-assignment verification pass — M7
> - Phase 33: Corpus completeness + full typology re-segmentation — M7
> - Phase 32: News stream — real gov-enforcement adverse-media source + presentation elevation — M8
> - Phase 31: M8 walking skeleton — the adverse-media / negative-news stream (a second atom stream) — M8
> - Phase 30: Data-source lens — surface the D1–D20 data-source axis as an institution coverage-by-data-source view — M7
> - Phase 29: Capability lens — surface the C1–C28 capability / D1–D20 data-source taxonomy as an institution coverage-by-capability view — M7
> - Phase 28: Corpus COMPLETENESS + grounded-coverage interview + methodical render + branding/compliance — M7
> - Phase 27: Make the corpus demo shippable — assess corpus output quality, then replan the fix — M7
> - Phase 26: Elevate the corpus demo to showcase quality — register re-translation + progressive render + build/lift wow + grouping/sort + landing page — M7
> - Phase 25: Corpus output quality — extract → translate (natural AML red flags) + the article-processing page — M7
> - Phase 24: Cross-corpus synthesis — a typology lens over the multi-source corpus — M7
> - Phase 23: FINTRAC depth — grow source #4 with the remaining anchorable strategic-intel products (Operational Alerts + Operational Briefs) — M7
> - Phase 22: FINTRAC as corpus source #4 (first cross-jurisdiction source; gate widened for FINTRAC "indicators" vocab; Crown-copyright non-commercial reproduction) — M7
> - Phase 21: OFAC as corpus source #3 (gate widened for OFAC vocab; US-federal public-domain) — M7
> - Phase 20: Multi-source spine, proven with FinCEN Alerts — M7
> - Phase 19: Durability closeout — commit corpus-explorer test harness + pin _rf_triage — M7
> - Phase 18: Corpus explorer arc — human gate + close-the-loop coverage payoff — M7
> - Phase 17: Complete corpus derivation + delete extract_red_flags (the real subtraction) — M7
> - Phase 16: Invert extraction (LLM extracts, deterministic gate disposes) + scale as proof — M7
> - Phase 15: Harden extraction faithfulness + fix shipped defects — M7
> - Phase 14: Scale corpus derivation (3 more CLEAN advisories → 5/14 live) — M7
> - Phase 13: Corpus explorer (advisory-selection front-end + per-indicator build-rec render) — M7 — THE PAYOFF
> - Phase 12: FinCEN corpus derivation foundation (deterministic spine all-14 + LLM proof slice) — COMPLETED + accepted (impl commit 90939b4)
> - Phase 11: Automated derivation (LLM-drafted signal config) — AUTOMATE — COMPLETED + accepted (impl commit c37dc39)
> - Phase 10: FinCEN corpus crawler (SCALE) — COMPLETED + accepted (commit 0c87c47)
> - Phase 9: Build-drift guard (zero-drift invariant) — COMPLETED + accepted
> - Phase 8: Doc true-up + provenance fix (M6 debt) — COMPLETED + accepted
> - Phase 7: Pipeline walking skeleton (M6) — COMPLETED + accepted

<!-- phase:phase-49-triage-loop-embryo -->
<!-- gate-log:phase-49 direction=approved delivery=pending -->

## Phase 49 — Triage-loop embryo made demo-able: §14's continuous adjudication loop as the 5th ship artifact (triage console)

Direction = the OFFERED recommendation taken as offered at the dev-plan gate 2026-06-12 (first non-reframe in 3 gates; on the user's stated LFCM target path), STANDARD ceremony. Build blueprint §14's continuous adjudication loop as a demo-able FIFTH ship artifact: triage.html → dist/triage/index.html (single self-contained offline file; the gate console BYTE-FROZEN — sibling, not extension). Scenario source = NEW committed SYNTHETIC data/triage/scenarios.json, deterministically curated by scripts/curate_triage_scenarios.py from data/probe-history (rulebook + 44 alert stubs, AUTHORING time only — build.py NEVER reads probe-history; rule text EMBEDDED, dataset self-contained) + US-federal-allowlist-only committed corpus indicators (the synthetic-novel stratum). ~16 scenarios across the 4 §14 strata (history-signal-fired / history-below-the-line / synthetic-novel / random-population) + ~4 known-disposition controls; evidence panels template-derived from rule logic + stub fields w/ a thin authored layer, ONE panel per fact pattern shared BY REFERENCE across divergent-disposition pairs (process-inconsistency beat STRUCTURAL, build-validated); fired-rule state universal; seeded LABELED second-rater dispositions. Arc: Queue (stream w/ stratum chips) → Evidence → Disposition (confirm-risk / confirm-no-risk / both-defensible / escalate / need-more-info naming a C/D code via taxonomy picker + the policy-gap escape "no defensible option — flag for policy review"; rationale REQUIRED) → Reveal (historical disposition, decisions-not-correctness; second-rater replay; process-inconsistency surfacing) → Discovery ledger (signal gaps DERIVED from fired-rule state; data gaps per D-code; process inconsistencies; policy gaps; agreement arithmetic computed at render w/ visible measurement definitions; params "chosen, not measured"; JSON export; persists nothing). Badge always-on; keyboard nav; reduced-motion; NO LLM/fetch. NO edit to docs/program-blueprint.md (avoids the hand-synced blueprint-report drift). Assumption gate closed 2026-06-12, all_accept: false (A1 demo-first ACCEPT · A2 data-path DON'T-KNOW round 1 → defended [Phase-48 A4 verbatim + console-cases curation precedent + §14 purpose] → ACCEPT round 2 · A3 panels ACCEPT · A4 5th-ship-artifact ACCEPT; ledger block in assumption-ledger.md; decision article articles/decisions/phase-49-triage-loop-embryo.md D1–D8 confidence high; spec specs/phase-49-triage-loop-embryo.md). Reviews: approach 7/10→revised (D7 panel verifier, D8 no-fake-instrumentation); plan 7/10→revised→9/10 ACCEPT. FROZEN: all 4 existing ship artifacts + dists BYTE-IDENTICAL; derive_signals.py; news pipeline; derived data + the 3 overlays; docs/program-blueprint.md.

- [x] T1 Scenario dataset + curate script: test scripts/curate_triage_scenarios.py --selftest fixtures first — shared-panel-ref integrity, stratum closed-vocab, US-federal allowlist, determinism, second-rater-seed presence each FAIL on seeded-broken fixtures (RED), write the curate script (reads data/probe-history + allowlisted committed corpus indicators at AUTHORING time; template-derives panel skeletons from rule logic + stub fields, thin authored layer; EMBEDS rule text — dataset self-contained) → data/triage/scenarios.json (~16 scenarios, all 4 strata + ~4 known-disposition controls; seeded LABELED second-rater dispositions; fired-rule state rule_id|none universal; synthetic meta flag) (GREEN), template dedupe; if authoring runs hot, pre-drawn split = curate machinery+fixtures (stays T1) / authored-panel layer (new task) (REFACTOR) | scope: scripts/curate_triage_scenarios.py, data/triage/** | success: python3 scripts/curate_triage_scenarios.py --selftest && regen-twice byte-identical (concretize at VERIFY) && python3 -c sanity gate (all 4 strata populated; ≥3 controls; ≤20 scenarios; every divergent-disposition pair shares its panel BY REFERENCE; fired-rule field universal; novel-stratum doc-ids ∈ allowlist; ≥4 labeled second-rater seeds; synthetic meta flag present) | size: M
- [x] T2 Build boundary + target: test 4 tamper fixtures (broken stratum vocab / dangling panel ref / missing synthetic meta flag / C/D ref outside taxonomy) each make validate_triage_scenarios RAISE, invoked unit-level via python3 -c (template doesn't exist yet — build.py triage greenness deferred to T3) (RED), implement load_triage_scenarios + validate_triage_scenarios in build.py + the `triage` target wired into all/--check (GREEN), reuse existing validation/inline helpers (REFACTOR) | scope: scripts/build.py | success: python3 -c unit checks (valid passes; 4 tampers raise — VERIFIED, errors-list style per the console precedent, render dies on any; +2 bonus drift classes) && per-target --check green on the 6 existing targets (VERIFIED) && ! grep -E '^[^#]*"probe-history"|^[^#]*probe_history' scripts/build.py (concretized at VERIFY: the original word-shaped grep failed on its own documentation comments — the same claim-shape fix the plan reviewer prescribed for T5's greps; probe-history appears in comments/docstrings ONLY, no code reference) | size: S
- [x] T3 triage.html arc: test tests/triage-console.test.mjs skeleton failing, gate-console precedent EXACTLY (load TEMPLATE + inject stub dataset, never parse dist): parse, arc reachability, disposition-gate rules (rationale required; need-more-info requires C/D pick; reveal locked pre-disposition) (RED), implement the full arc → first passing python3 scripts/build.py triage (dist PROVISIONAL — final freeze at T4) (GREEN), dossier-theme copy hygiene, no dead console code (REFACTOR) | scope: triage.html, tests/triage-console.test.mjs, dist/triage/** | success: node tests/triage-console.test.mjs core set green && python3 scripts/build.py triage && python3 scripts/build.py --check triage && offline single-file grep on dist/triage/index.html (concretize at VERIFY) | size: L
- [x] T4 Harness full coverage: test RED→GREEN per feature — need-more-info lands a per-D-code data-gap ledger row; policy-gap escape requires rationale; second-rater replay LABELED; ledger agreement arithmetic equals a hand-computed fixture AND renders its measurement-definition string; signal-gap derivation from fired-rule state; XSS-escape; keyboard guards; both motion modes; badge; export JSON shape (RED), implement each feature to green (GREEN), consolidate shared harness helpers (REFACTOR) | scope: tests/triage-console.test.mjs, triage.html, dist/triage/** | success: node tests/triage-console.test.mjs fully green (~50+) && python3 scripts/build.py triage && python3 scripts/build.py --check triage (T4 owns the FINAL dist freeze) | size: M
- [x] T5 Integration + docs + full regate [deviation noted: the CLAUDE.md trim toward ~200 was consciously DEFERRED again (now ~330 lines after the artifact-#5 additions) — rewriting load-bearing live-mode paragraphs at session end failed the cost-of-error test; the trim debt stays carried, surfaced in the delivery report]: test the pre-edit bar — claim-shaped honesty greps green against T4's triage.html + git diff --quiet docs/program-blueprint.md (RED), write CLAUDE.md replace-in-place (5 ship artifacts; trim toward the ~200-line contract while in there) + HANDOFF.md §8 + tests/smoke-checklist.md row incl. "read 4 evidence panels, one per stratum" (believability adjudicated by the user at the delivery gate; delivery report presents one full scenario verbatim) (GREEN) | scope: CLAUDE.md, HANDOFF.md, tests/smoke-checklist.md | success: python3 scripts/build.py --check all zero drift && git diff --quiet scripts/derive_signals.py && git diff --quiet docs/program-blueprint.md && ! grep -niE "\b(accuracy|precision|recall)\b" triage.html && [ -z "$(grep -iE 'ground truth' triage.html | grep -ivE 'never|not ')" ] && grep -qi "chosen, not measured" triage.html && grep -qi "decisions, not correctness" triage.html && node tests/corpus-explorer.test.mjs && node tests/news-stream.test.mjs && node tests/gate-console.test.mjs && node tests/triage-console.test.mjs && python3 scripts/derive_signals.py --selftest && python3 tests/news_quality_harness.py --check | size: S

> Exit (phase-49): (1) data/triage/scenarios.json committed — ≤20 scenarios, all 4 strata populated, ≥3 controls, deterministic regen byte-identical, US-federal-only novel stratum, divergent pairs share panels by reference, fired-rule state universal, ≥4 labeled second-rater seeds, synthetic meta flag; (2) build.py `triage` target wired into all/--check, boundary validation fails loud on tamper (4 classes), no probe-history reference in build.py; (3) triage.html → dist/triage single-file offline with the full arc, badge always-on; (4) tests/triage-console.test.mjs fully green (~50+ assertions, gate-console precedent); (5) claim-shaped honesty greps green + FULL REGATE — --check all zero drift (7 targets incl. triage), git diff --quiet on derive_signals.py AND program-blueprint.md, all existing suites green.
> Abort: blocked >3 attempts on a task → mark [blocked: …] + ask the user skip or abort. Existing dists drift → STOP and surface (never re-baseline). Believable panels won't fit the ~16+4 ceiling → split per the T1 pre-drawn valve, never pad thin panels to a count. A validator looks like it needs loosening to pass the dataset → fix the DATA, never the validator. Any typed-in agreement/accuracy figure or a parameter presented as measured → out of bounds, honesty constraints govern.

<!-- phase:phase-48-history-utilization-lfcm -->
<!-- gate-log:phase-48 direction=approved delivery=accepted -->

<!-- phase:phase-47-agentic-aml-program-design -->
<!-- gate-log:phase-47 direction=approved delivery=accepted -->

<!-- phase:phase-46-corpus-live-derivation -->
<!-- gate-log:phase-46 direction=approved delivery=accepted -->

<!-- phase:phase-45-corpus-presentation-polish -->
<!-- gate-log:phase-45 direction=approved delivery=accepted -->

<!-- phase:phase-44-live-extraction-quality -->
<!-- gate-log:phase-44 direction=approved delivery=accepted -->

<!-- phase:phase-43-live-pipeline-robustness -->
<!-- gate-log:phase-43 direction=approved delivery=accepted -->
