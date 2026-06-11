# Tasks

> ACTIVE PHASE ONLY. Closed phase blocks live VERBATIM in [articles/tasks-archive-pre-phase-44.md](articles/tasks-archive-pre-phase-44.md) (split out 2026-06-10 by the Phase-44 T6 hygiene trim; per-phase narrative also in the journal + articles/decisions/*). Archived blocks:
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

<!-- phase:phase-45-corpus-presentation-polish -->
<!-- gate-log:phase-45 direction=approved delivery=pending -->

## Phase 45 — Corpus demo presentation polish (pre-presentation day) — M7

dist/corpus presents to bank stakeholders TOMORROW 2026-06-11 (one-day horizon, lite). Phase 45 = presentation polish driven by two independent review agents (story coherence + inconsistency sweep; findings recorded in articles/decisions/phase-45-corpus-presentation-polish.md). Baseline green at planning: --check all 5/5 zero drift, corpus harness 239/239, no stale counts. Work: (1) three story HIGH live-risk fixes (.brecrow stagger cap · human-gate pre-decided copy · zero-build-now lift dead-end); (2) lift-beat refocus to R2 "real composition search space" — DELETE the fake 18→64→83 LIFT template + the "Illustrative · pending calibration" tag, render honest INVENTORY counts (covered indicators in the committed signal's typology × contributing regulators, computed client-side from __CORPUS__, the same honesty class as the lenses; R1 zero-numbers ladder is the copy-only fallback) — this completes the Phase-18 honesty arc (the figures were comment-documented as never-measured at corpus.html:1145–47; tests :723–741 pin them and move in the SAME commit); (3) FINTRAC footer attribution EXTENDED to the Capabilities/Data-sources lens views (the Phase-28 relocated-footer mechanism, the user's compliance call — not suppression); (4) ranked copy-coherence pass (MEDIUMs first, LOWs time-permitting); (5) user walkthrough + feedback-intake FREEZE checkpoint with presenter/demo-path notes into smoke-checklist; (6) full regate — the frozen dist/corpus baseline MOVES (two-commit delivery convention). FROZEN: grounding core, derived data, build pipeline, showcase index.html BYTE-IDENTICAL (its Act-5 lift template STAYS — cross-artifact divergence accepted at the gate) + news artifacts byte-identical; the always-on badge stays; NO new fabricated/similarity/overlap/lift number (the Phase-18/24 rejections + honesty-over-demo-drama stand). Assumption gate closed 2026-06-10 (all_accept: false — A1 don't-know round 1 → defended with worked real-value examples → accepted): A1 [HIGH] lift = R2 real inventory counts, no performance claim, disclaimer removed, honest small-N/single-regulator degradation, R1 fallback copy-only · A2 [HIGH] showcase Act-5 untouched (byte-frozen, non-negotiable-protected); deliberate divergence accepted · A3 [MED] human gate = copy reframe ("the agent has PROPOSED all N — deselect to dispose") + presenter stagecraft, NO interaction redesign · A4 [MED] FINTRAC attribution extends the Phase-28 footer mechanism to the two lens views · A5 [MED] GLOBAL polish + curated demo-path notes in smoke-checklist (the user hasn't named demo docs — route recommendation lands at T5).

- [x] T1 Live-risk fixes: cap .brecrow stagger (Math.min(k*90,1500), corpus.html~:1018); human-gate lead copy reframe (~:999/1001, "the agent has PROPOSED all N pre-committed — deselect to dispose"); zero-build-now lift empty state ports the renderSignal two-message split (~:1140); "Backtest on population" → "Queue backtest on population" (~:1051) | scope: corpus.html, tests/corpus-explorer.test.mjs | success: node tests/corpus-explorer.test.mjs green incl. updated assertions && grep -c "Queue backtest" corpus.html = 1
- [x] T2 Lift beat R2 refocus: delete the LIFT const (~:1148–52), % bars/counters (~:1159–63, anim ~:1172, CSS .liftbar/.fill weak/mid/strong ~:183–93), the .illus tag (~:1158); render real composition-search-space counts from __CORPUS__ (covered indicators in the committed signal's typology across contributing regulators; honest single-regulator/small-N copy); promotion-gate sentence promoted into the side panel; framenote ~:1170 rewritten keeping "promotion gate"; hint ~:1293 drops "— illustrative"; replace the tests P26-5 lift block (test:~723–741); CLAUDE.md "Honesty constraints" rewritten IN PLACE (the approved-fabrication-reversal paragraph replaced by the R2 honest-inventory description) | scope: corpus.html, tests/corpus-explorer.test.mjs, CLAUDE.md | success: ! grep -qE "pending calibration|liftbar" corpus.html && node tests/corpus-explorer.test.mjs green
- [x] T3 FINTRAC attribution on lens views: updateAttribution (~:1214) fires on capability/data-source drill screens whenever FINTRAC verbatim excerpts are on screen (~:692/:747); stays empty for US-only screens | scope: corpus.html, tests/corpus-explorer.test.mjs | success: new harness assertions (attribution non-empty on a FINTRAC-bearing capability drill, empty on a US-only one) && suite green
- [x] T4 Ranked copy-coherence pass (MEDIUMs first, LOWs time-permitting): seed atom vocabulary on the landing (~:497–99); landing lead names all 5 source families (~:498); the "5 regulators/sources" tile honest split (~:503); "Advisories" chrome → "Documents" (~:290, :1291, footer); step-1 "Read advisory" vs "Read the source" reconciled; close-screen "gap → covered" pill → UI vocabulary (~:1107); typoLabel title-cased human labels incl. "Cross-cutting indicators" (~:361); FINTRAC pseudo reference codes display-only fix (real refs where they exist, doc-type label otherwise); LOWs: stepper numbering from 1, source-heading capitalization (~:559), FINTRAC date format | scope: corpus.html, tests/corpus-explorer.test.mjs | success: suite green && ! grep -q "↺ Advisories" corpus.html
- [x] T5 User walkthrough + feedback intake (FREEZE checkpoint): rebuild dist/corpus; the user walks the dist; feedback items dispositioned ranked + time-boxed, overflow explicitly deferred; presenter/demo-path notes into tests/smoke-checklist.md (recommended route, the deselect stagecraft at the gate, second-gate narration via the E-23/Model-Validation route, zero-build-now docs to avoid [fin-2021-a004, fin-2023-alert003], Google-Fonts cache warm on the presentation machine) | scope: corpus.html, tests/smoke-checklist.md, dist/corpus/** | success: user dispositions recorded in tasks.md notes && smoke-checklist updated && no open HIGH feedback
  > T5 DISPOSITIONS (walkthrough 2026-06-10, "ok looks pretty good" + 2 items, then 2 refinements, then FREEZE):
  > (1) FIXED — non-ASCII cleanup ("verify all page contents"): classified into (a) mojibake in the fincen-alerts derived records' AUTHORED coverage fields (Â· / â-em-dash / â-arrow, ~2.2K occurrences) and (b) PDF symbol-font PUA bullets in 9 FINTRAC/OFAC article mds (tofu). Fix = LOAD-TIME DISPLAY-ONLY encoding repair in corpus.html (MOJI map, \u-escaped; fixEncoding walk at validateCorpus) — committed records + md BYTE-FROZEN per the phase contract. Harness now sweeps ALL 56 live docs × 6 screens + every cap/DS/typology drill mojibake/tofu-free (the permanent verify-all-contents gate). Legit non-ASCII (dossier typography, FINTRAC French, ©/§/glyphs) kept.
  > (2) FIXED — landing hook reshaped onto "effective and regulatorily defensible financial-crime program" (round 2: hero dash removed — one clean line, italics carry the beat; the "hard part was never access: extensive human review" body beat RESTORED; examiner/cited-verbatim payoff moved to the loop paragraph).
  > DEFERRED (named): byte-surgical mojibake repair of the fincen-alerts derived records (the permanent fix; display repair then becomes the safety net) · FINTRAC month-only date display · publications/documents naming unification · interactive second gate · R3 composition graph.
- [x] T6 Full regate + docs: python3 scripts/build.py corpus (frozen baseline MOVES) then python3 scripts/build.py --check all → 5/5; node tests/corpus-explorer.test.mjs + node tests/news-stream.test.mjs green; CLAUDE.md current-state lines true in place | scope: dist/corpus/**, CLAUDE.md, .dev-wiki/** | success: --check all 5/5 && both node suites green

> Exit (phase-45): the three story HIGH live-risk fixes in; NO fabricated lift number remains in corpus.html/dist/corpus (LIFT const + bars + "pending calibration" tag deleted; the beat carries honest R2 inventory counts computed client-side, or the R1 zero-numbers copy if counts degrade) and CLAUDE.md's honesty-constraints paragraph rewritten in place; FINTRAC footer attribution fires on FINTRAC-bearing lens drill screens, empty on US-only; ranked copy-coherence MEDIUMs done; the user walkthrough run with feedback dispositioned (no open HIGH) + presenter/demo-path notes in tests/smoke-checklist.md; dist/corpus rebuilt (the frozen baseline moves) with --check all 5/5 and both node suites green; showcase index.html + news artifacts byte-identical; the always-on badge stays; NO non-negotiable change; presentation-ready by 2026-06-11.
> Abort: blocked >3 attempts on a task → mark [blocked: …] + ask the user skip or abort (one-day horizon: prefer ASK EARLY over burning attempts); the R2 inventory counts can't be computed honestly client-side or would imply a performance claim → fall back to the R1 zero-numbers ladder (A1's designed fallback), never invent a number; showcase or news dist drifts → STOP and surface it; user feedback exceeding the day → disposition ranked + time-boxed at T5, overflow explicitly deferred — never silently absorbed.

<!-- phase:phase-44-live-extraction-quality -->
<!-- gate-log:phase-44 direction=approved delivery=accepted -->

<!-- phase:phase-43-live-pipeline-robustness -->
<!-- gate-log:phase-43 direction=approved delivery=accepted -->
