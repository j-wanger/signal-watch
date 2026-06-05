# Dev Wiki Index

## By Category

### Phases
- [[phase-01-bootstrap|Phase 1: Bootstrap (M0)]] — completed
- [[phase-02-config-driven-refactor|Phase 2: Config-driven refactor (M1)]] — completed
- [[phase-03-multi-typology|Phase 3: Multi-typology (M2)]] — completed (TBML, build-time switch)
- [[phase-04-presenter-polish|Phase 4: Presenter polish (M3)]] — completed (engine-only: nav + reset + reduced-motion)
- [[phase-05-live-pregen-mode|Phase 5: Live / pre-gen mode (M4, optional)]] — skipped (inert under file://)
- [[phase-06-ship|Phase 6: Ship (M5)]] — completed + accepted (doc/verify; compliance + offline file:// hard gate PASS)
- [[phase-07-pipeline-walking-skeleton|Phase 7: Pipeline walking skeleton (M6)]] — completed + accepted (FinCEN EFE FIN-2022-A002 slice; Act 1 verbatim render; Signal Watch rebrand)
- [[phase-08-doc-true-up|Phase 8: Doc true-up + provenance fix (M6 debt)]] — completed + accepted (rebrand docs; FinCEN-verbatim non-negotiable; fentanyl provenance → FINTRAC; dist drift corrected)
- [[phase-09-build-drift-guard|Phase 9: Build-drift guard]] — completed + accepted (in-process `build.py --check` for the zero-drift invariant; wired into smoke-checklist; commit 33db22a)
- [[phase-10-fincen-corpus-crawler|Phase 10: FinCEN corpus crawler (SCALE)]] — active (discovery manifest `data/fincen/index.json`; authoring-only `crawl_fincen.py`, pure parser + `--selftest`; bounded batch, not mass-download)

### Decisions
- None yet

### Journal
- [[2026-06-05-phase-10-fincen-corpus-crawler|2026-06-05 · Phase 10 FinCEN corpus crawler (SCALE)]]
- [[2026-06-05-phase-09-build-drift-guard|2026-06-05 · Phase 9 build-drift guard]]
- [[2026-06-04-phase-08-doc-true-up|2026-06-04 · Phase 8 doc true-up + provenance fix]]
- [[2026-06-04-m6-pipeline-walking-skeleton|2026-06-04 · M6 pipeline walking skeleton]]
- [[2026-06-04-m5-ship|2026-06-04 · M5 ship]]
- [[2026-06-04-m3-presenter-polish|2026-06-04 · M3 presenter polish]]
- [[2026-06-04-m2-multi-typology|2026-06-04 · M2 multi-typology (TBML)]]
- [[2026-06-04-m1-config-driven-refactor|2026-06-04 · M1 config-driven refactor]]

## By Hierarchy

- Milestones M0 → M5 map 1:1 to Phases 1 → 6 (see HANDOFF.md §8); M6 = Phase 7 (pipeline slice, post-ship) + Phase 8 (doc/provenance true-up of the M6 debt)
- M0–M3 done; M5 (ship) done + accepted; **M4 (live/pre-gen) skipped** by decision. M6 (Signal Watch ingestion pipeline) **completed + accepted** — project identity pivot to a public-data-seeded ingestion pipeline; docs trued-up to M6 reality in Phase 8.

## Living Documents

- `_CURRENT_STATE.md` — project state, active phase, next action
- `_ARCHITECTURE.md` — structural snapshot
- `tasks.md` — task tracking
- `schema.md` — wiki schema · `config.md` — ceremony (lite)

## Knowledge Wiki

- **aml-wiki** (registered central store, `/Users/jwang/private-knowledge/aml-wiki`) — AML
  domain reference. Linked via gitignored `wiki/` symlink; auto-scoped by CWD. Query: `/wiki-query`.

## Recent

- [2026-06-05] Phase 10 (FinCEN corpus crawler — SCALE) planned + active — discovery manifest (`data/fincen/index.json`) over mass-download; authoring-only `crawl_fincen.py` (pure `parse_index` + `--selftest`); 4 lite tasks; direction approved (user chose SCALE over the elder true-up)
- [2026-06-05] Phase 9 (build-drift guard) completed + accepted — in-process `build.py --check` for the M5 zero-drift invariant (broke silently in Phase 7); commit 33db22a
- [2026-06-04] Phase 8 (doc true-up + provenance fix) completed + accepted — rebrand docs to Signal Watch; FinCEN-verbatim non-negotiable; fentanyl provenance → FINTRAC; M6 doc staleness folded in; Phase 7 dist drift corrected; commit 042d732
- [2026-06-04] M6 (pipeline walking skeleton) completed + accepted — FinCEN EFE FIN-2022-A002 slice; Act 1 verbatim render; Signal Watch rebrand; commit 8459dd9
- [2026-06-04] M5 ship — completed + accepted; compliance + offline file:// hard gate PASS; project shipped
- [2026-06-04] M3 presenter polish — engine-only keyboard nav + reset + reduced-motion; both dist rebuilt
- [2026-06-04] dev wiki bootstrapped (retrofit from HANDOFF.md milestone plan); aml-wiki linked
