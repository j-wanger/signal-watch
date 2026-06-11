# Tasks

> ACTIVE PHASE ONLY. Closed phase blocks live VERBATIM in [articles/tasks-archive-pre-phase-44.md](articles/tasks-archive-pre-phase-44.md) (split out 2026-06-10 by the Phase-44 T6 hygiene trim; per-phase narrative also in the journal + articles/decisions/*). Archived blocks:
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

<!-- phase:phase-46-corpus-live-derivation -->
<!-- gate-log:phase-46 direction=approved delivery=accepted -->

## Phase 46 — Corpus live derivation mode: local-model agentic derivation through the frozen gate (M7×M8 convergence)

Direction = the user's REFRAME at the dev-plan gate 2026-06-10 (the 5th reframe in 6 gates, off all five carried DEFERRED candidates): "live mode with local model for the corpus demo as well, ideally with a better harness integration like opencode" + a pasted opencode/local-model practitioner research report. Phase 46 brings a LIVE mode to the corpus demo, mirroring the news-live architecture: a companion-served, dev/authoring-time live mode where a local model derives a NEW advisory document (pasted md / URL → red-flag indicators + C/D tags + coverage) through the EXISTING frozen gate (derive_signals.py check_record — quote-grounding, cover×data matrix, red_flag shape); only gate-green output renders into the corpus 6-screen arc. The harness question (hand-rolled serve_news-pattern pipeline vs opencode as the local-model agent runtime driving a derive-until-gate-green loop) is PROBE-GATED at T1, not pre-decided: opencode must beat the direct pipeline on measured gate pass rate / iteration count / wall time / tool-call reliability, else the phase ships on the proven pattern; USER CHECKPOINT on the harness verdict before T2. Probe model = the EXISTING running llama-server Qwen (127.0.0.1:8080, news-proven; swap only on measured tool-call-class failure); held-out material = a FINTRAC /intel/ frontier doc (LOCAL-ONLY, gitignored, NOT committed — composes with the deferred C1 candidate; its licence/heading-form sub-questions travel with it). Boundaries: offline dist/corpus stays BYTE-IDENTICAL via the news-style /*LIVE_START*/…/*LIVE_END*/ build strip (live mode optional/isolated/off-by-default, scripted fallback — the non-negotiable); live-derived records are DISPLAY/PROPOSE-only (committing a new derived record to data/ remains a separate human-reviewed act under existing licence rules); the 2026-06-11 presentation OUTRANKS the phase — nothing presentation-touching moves before it, --check all 5/5 enforced before any commit. Assumption gate closed 2026-06-10, all_accept: TRUE (A1–A4 accept; ledger block in assumption-ledger.md; decision article articles/decisions/phase-46-corpus-live-derivation.md).

- [x] T1 Harness probe (measure-first): install opencode + configure the local llama-server provider (verify --jinja serving + ctx vs /props n_ctx); acquire ONE held-out FINTRAC /intel/ frontier doc as probe material (LOCAL-ONLY, gitignored, not committed); run (a) the opencode agent derive-until-gate-green loop and (b) a direct serve_news-pattern pipeline baseline on the SAME doc with derive_signals.py --check-derived as backpressure; measure gate pass rate / iterations / wall time / tool-call failures. CHECKPOINT taken 2026-06-11: DIRECT+RETRY accepted (opencode matched quality at 3.1x wall, loop never engaged; news-lift eval = separate, staged in tmp). | scope: .dev-wiki/tmp/** | success: probe report .dev-wiki/tmp/ph46/ph46_probe.md with measured numbers for BOTH harnesses on the same doc; user checkpoint taken
- [x] T2 Corpus live companion: the T1-chosen harness wired as scripts/serve_corpus.py (serve_news pattern: localhost page serving + NDJSON staged /derive + single-flight 409 + failures NAMED in-stream + disconnect-persists-nothing); the existing check_record gate disposes — only gate-green indicators emitted; --selftest included | scope: scripts/serve_corpus.py | success: python3 scripts/serve_corpus.py --selftest green; live derivation of the held-out doc end-to-end emits gate-green indicators via staged NDJSON
- [x] T3 corpus.html LIVE region UI: live-derive entry (paste; URL mode consciously omitted — the /intel/ frontier is PDF-shaped, outside news_fetch's HTML ladder; the converted-md paste IS the authoring surface) + Phase-44-pattern stage-completion processing view (never token streams) + the gate-green derived doc renders through the existing 6-screen arc; ALL live client code in /*LIVE_START*/…/*LIVE_END*/; extend the build.py strip to the corpus target — dist/corpus BYTE-IDENTICAL | scope: corpus.html, scripts/build.py, tests/corpus-explorer.test.mjs | success: node tests/corpus-explorer.test.mjs green incl. a live-strip assertion; python3 scripts/build.py --check all 5/5 (dist/corpus byte-identical)
- [x] T4 Regate + docs: docs/corpus-live.md (news-live.md sibling: architecture + walkthrough + flags); tests/smoke-checklist.md live-corpus notes; CLAUDE.md current-state updated IN PLACE (maintenance contract — replace facts, never append per-phase bullets); full regate | scope: docs/corpus-live.md, tests/smoke-checklist.md, CLAUDE.md | success: python3 scripts/build.py --check all 5/5 && node tests/corpus-explorer.test.mjs && node tests/news-stream.test.mjs && python3 scripts/derive_signals.py --selftest all green

> Exit (phase-46): T1 probe report (.dev-wiki/tmp/ph46/ph46_probe.md) carries measured numbers for BOTH harnesses (gate pass rate / iterations / wall time / tool-call failures) on the SAME held-out doc + the user checkpoint taken on the harness verdict; scripts/serve_corpus.py --selftest green + a live end-to-end derivation of the held-out doc emits ONLY gate-green indicators via staged NDJSON; corpus.html live entry + stage-completion processing view land in the /*LIVE_*/ region with the strip extended to the corpus target — node tests/corpus-explorer.test.mjs green incl. a live-strip assertion + dist/corpus BYTE-IDENTICAL (--check all 5/5); docs/corpus-live.md + smoke-checklist notes + CLAUDE.md in place; full regate green (both node suites + all selftests); live-derived output DISPLAY/PROPOSE-only — no new record committed to data/; the always-on badge stays; NO non-negotiable change; nothing presentation-touching moved before 2026-06-11.
> Abort: blocked >3 attempts on a task → mark [blocked: …] + ask the user skip or abort. The 2026-06-11 presentation OUTRANKS the phase — anything presentation-touching waits. opencode can't drive a reliable tool-calling loop with the existing Qwen (or loses the T1 measurement) → ship the phase on the direct serve_news-pattern pipeline (the designed fallback), never adopt unearned complexity; model swap ONLY on measured tool-call-class failure. The held-out FINTRAC doc fails the existing rf_region anchors → anchor extension is REGRESSION-GATED (every existing md's region byte-unchanged + --selftest fixtures) or pick a different frontier doc — never loosen the gate. dist/corpus can't stay byte-identical after the strip → STOP and surface it. A live-derived record wants committing → that is a SEPARATE human-reviewed act under licence rules, out of phase scope.

<!-- phase:phase-45-corpus-presentation-polish -->
<!-- gate-log:phase-45 direction=approved delivery=accepted -->

<!-- phase:phase-44-live-extraction-quality -->
<!-- gate-log:phase-44 direction=approved delivery=accepted -->

<!-- phase:phase-43-live-pipeline-robustness -->
<!-- gate-log:phase-43 direction=approved delivery=accepted -->
