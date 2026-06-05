# Dev Wiki Log

[2026-06-04T19:15:46] INIT -- dev wiki bootstrapped, 6 phase articles (retrofit from HANDOFF.md M0-M5), M0 completed / M1 active, ceremony: lite, git: yes
[2026-06-04T19:15:46] PLAN -- Phase 2 (M1) planned, 6 tasks, 3 decisions (minimal structure: engine template + JSON config + stdlib build inliner)
[2026-06-04T19:15:46] IMPL -- Phase 2 (M1) all 6 tasks done; dist/index.html verified byte-identical to baseline; awaiting delivery acceptance + /dev-debrief
[2026-06-04T19:15:46] DEBRIEF -- Phase 2 (M1) completed + accepted; journal 2026-06-04-m1-config-driven-refactor; next: /dev-plan M2
[2026-06-04T19:15:46] PLAN -- Phase 3 (M2) planned, 4 tasks, 3 decisions (TBML typology, build-time switch, build-boundary validation)
[2026-06-04T19:15:46] IMPL -- Phase 3 (M2) all 4 tasks done; TBML added as config-only, engine untouched (zero index.html diff); fentanyl regression byte-identical
[2026-06-04T19:15:46] DEBRIEF -- Phase 3 (M2) completed + accepted; journal 2026-06-04-m2-multi-typology; next: /dev-plan M3
[2026-06-04] PLAN -- Phase 4 (M3) planned, 3 tasks (pure-engine: nav+reset+keys, prefers-reduced-motion, rebuild+Chrome pass); speaker notes deferred; engine edits intentional
[2026-06-04] IMPL -- Phase 4 (M3) all 3 tasks done; engine-only (config/+build.py byte-identical); both dist rebuilt + self-contained; gates verified on both dist x both motion modes; real Chrome 149 renders
[2026-06-04] DEBRIEF -- Phase 4 (M3) completed + accepted; journal 2026-06-04-m3-presenter-polish; next: /dev-plan M5 ship
[2026-06-04] PLAN -- Phase 6 (M5 ship) planned, 3 tasks, 4 decisions; M4 (live/pre-gen) skipped (inert under file://); doc/verify only — parameterize smoke-checklist + refresh README + compliance/offline hard gate; ask-slide/rename/Playwright deferred
[2026-06-04] IMPL -- Phase 6 (M5 ship) all 3 tasks done; doc/verify only (index.html+config/+scripts/ byte-identical); compliance + offline file:// HARD GATE PASS (zero drift, badge both dist, self-contained, advisories paraphrased+attributed, no secrets/PII)
[2026-06-04] DEBRIEF -- Phase 6 (M5 ship) completed + accepted; journal 2026-06-04-m5-ship; project meets HANDOFF §1.2 definition of shipped; M4 + ask-slide + new typologies are optional config-driven follow-ups
[2026-06-04T20:56:40] PLAN -- Phase 7 (M6 pipeline walking skeleton) planned, 5 tasks, 8 decisions; thin vertical slice on FinCEN EFE FIN-2022-A002 (acquire PDF → convert PDF→MD persist → hand-derive one schema-valid signal → render verbatim in Act 1's SOURCE DOCUMENT panel); authoring-time vs ship-artifact split (converter authoring-only, ship stays single-file/offline/no-fetch); FinCEN-only verbatim exception (17 USC §105); Signal Engine→Signal Watch rebrand; T2 converter quality is the de-risk gate
[2026-06-04T01:45:00] DEBRIEF -- Phase 7 (M6 pipeline walking skeleton) all 5 tasks done (not yet committed); 0 decisions captured (lite ceremony skips decision articles), 12 in substance; journal 2026-06-04-m6-pipeline-walking-skeleton; codebase snapshot created; _ARCHITECTURE.md refreshed (realized authoring pipeline: acquire_fincen.py + pdf_to_md.py/markitdown + advisory_full text_file→inline); 3 follow-up phases discovered (doc true-up + provenance fix, FinCEN corpus crawler, automate derivation); retro check ran (5 completed phases) — no systemic issues; delivery gate UNCHECKED (commit handled interactively)
