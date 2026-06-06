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
- [[phase-10-fincen-corpus-crawler|Phase 10: FinCEN corpus crawler (SCALE)]] — completed + accepted (discovery manifest `data/fincen/index.json`; authoring-only `crawl_fincen.py`, pure parser + `--selftest`; bounded batch, not mass-download; commit 0c87c47)
- [[phase-11-automated-derivation|Phase 11: Automated derivation (LLM-drafted signal config)]] — completed + accepted (AUTOMATE; authoring-only `derive_signals.py`, deterministic `--selftest`/`--scaffold` + neural `--draft`; LLM proposes a `.draft.json`, build.py + schema + human gates dispose; variant B over A; review 9/10; commit c37dc39)
- [[phase-12-fincen-corpus-derivation|Phase 12: FinCEN corpus derivation foundation (M7)]] — completed + accepted (backend-only; deterministic spine validated on ALL 14 → 7 CLEAN/3 LOW/4 NEEDS; LLM-backend (this session, no key) derived 2 records; boundary = cover×data matrix + traceability + shape; spine assists-not-automates; review 8/10→fixed; commit 90939b4; demo expansion = Phase 13)
- [[phase-13-corpus-explorer|Phase 13: Corpus explorer (advisory-selection front-end + per-indicator build-rec render) (M7)]] — completed + accepted (the PAYOFF — a NEW standalone ship artifact `dist/corpus/index.html` via `corpus.html`, staged 4-screen flow SELECT→COVERAGE→BUILD RECOMMENDATIONS→SIGNAL SPEC, all 14 advisories with honest status, 2 derived live; showcase byte-frozen; build.py decoupled from derive_signals.py; review 9/10; impl commit 54516d4)
- [[phase-14-scale-corpus-derivation|Phase 14: Scale corpus derivation (3 more CLEAN advisories → 5/14 live) (M7)]] — completed + accepted (PURE AUTHORING — derived fin-2020-a008 trafficking [10 ind/2 BUILD_NOW] + fin-2025-a003 Chinese MLN [17 ind/5 BUILD_NOW] + fin-2025-a002 Iran [16 ind/4 BUILD_NOW·7 ENRICH] via the proven --scaffold-derived→author→--check-derived loop, rebuilt dist/corpus to 5/14 live; zero engine/spine/front-end edits, all byte-frozen; --check all zero drift; findings → Phase-15 extractor footnote-resume fix + fin-2022-a001 esc() bug; 5 lite tasks; impl ce0de90 + gate 410241f)
- [[phase-15-harden-extraction-faithfulness|Phase 15: Harden extraction faithfulness + fix shipped defects (M7)]] — completed + accepted (footnote-resume fix in extract_red_flags [_SECTION_STOP terminals + conditional _FOOTNOTE_STOP + 2 targeted _CITATION signatures] — SURGICAL: fin-2025-a003 recovered its silently-dropped L499 escrow flag 17→18, 0 collateral, EFE 12+12, 7C/3L/4N held; esc() entity sweep [fin-2022-a001 + fin-2024-a002 → raw text, verified in built file]; escrow IND-18 added; regen+rebuild, --check all zero drift. Glued-no-separator DEFERRED — no safe split, stays FLAGGED [re-confirms Phase-12]. byte-frozen held; 5 lite tasks)

### Decisions
- None yet

### Journal
- [[2026-06-05-phase-12-fincen-corpus-derivation|2026-06-05 · Phase 12 FinCEN corpus derivation foundation (M7)]]
- [[2026-06-05-phase-11-automated-derivation|2026-06-05 · Phase 11 Automated derivation (LLM-drafted signal config)]]
- [[2026-06-05-phase-10-fincen-corpus-crawler|2026-06-05 · Phase 10 FinCEN corpus crawler (SCALE)]]
- [[2026-06-05-phase-09-build-drift-guard|2026-06-05 · Phase 9 build-drift guard]]
- [[2026-06-04-phase-08-doc-true-up|2026-06-04 · Phase 8 doc true-up + provenance fix]]
- [[2026-06-04-m6-pipeline-walking-skeleton|2026-06-04 · M6 pipeline walking skeleton]]
- [[2026-06-04-m5-ship|2026-06-04 · M5 ship]]
- [[2026-06-04-m3-presenter-polish|2026-06-04 · M3 presenter polish]]
- [[2026-06-04-m2-multi-typology|2026-06-04 · M2 multi-typology (TBML)]]
- [[2026-06-04-m1-config-driven-refactor|2026-06-04 · M1 config-driven refactor]]

## By Hierarchy

- Milestones M0 → M5 map 1:1 to Phases 1 → 6 (see HANDOFF.md §8); M6 spans Phase 7 (pipeline slice) + Phase 8 (doc/provenance true-up) + Phase 9 (build-drift guard, HARDEN) + Phase 10 (corpus crawler, SCALE) + Phase 11 (automated derivation, AUTOMATE)
- M0–M3 done; M5 (ship) done + accepted; **M4 (live/pre-gen) skipped** by decision. **M6 (Signal Watch ingestion pipeline) — Phases 7–11 ALL completed + accepted** — the vision arc is complete: Phase 11 (AUTOMATE) automated the manual article→signal derivation, boundary-preserving (LLM proposes, build.py + schema + 2 human gates dispose). **M7 (corpus-backed demo)** — Phase 12 (completed + accepted): deterministic spine validated across all 14 FinCEN advisories (7 CLEAN/3 LOW/4 NEEDS) + LLM-backend derivation (no key) proven on a 2-advisory slice; spine assists-not-automates. **Phase 13 (completed + accepted) — the PAYOFF**: a NEW standalone corpus-explorer ship artifact (`dist/corpus/index.html` via `corpus.html`) renders the derived records as a staged 4-screen flow (select an advisory → coverage → build recommendations → signal spec); showcase byte-frozen, build.py decoupled from the authoring layer; shipped 2/14 derived live. **Phase 14 (completed + accepted) — SCALE**: pure authoring filled the explorer's live menu 2/14 → 5/14 by deriving 3 more CLEAN advisories (trafficking · Chinese MLN · Iran) via the proven --scaffold-derived→author→--check-derived loop + a dist rebuild; zero engine/spine/front-end edits (all byte-frozen). **Phase 15 (completed + accepted) — HARDEN**: fixed the 2 defects Phase 14 surfaced (extractor footnote-resume — a CLEAN advisory stops silently dropping a flag, surgical fin-2025-a003 17→18 with 0 collateral; the fin-2022-a001 esc() double-escape sweep) scoped by measurement; glued-no-separator splitting deferred (no safe split, stays FLAGGED). M7 (Phases 12–15) complete.

## Living Documents

- `_CURRENT_STATE.md` — project state, active phase, next action
- `_ARCHITECTURE.md` — structural snapshot
- `tasks.md` — task tracking
- `schema.md` — wiki schema · `config.md` — ceremony (lite)

## Knowledge Wiki

- **aml-wiki** (registered central store, `/Users/jwang/private-knowledge/aml-wiki`) — AML
  domain reference. Linked via gitignored `wiki/` symlink; auto-scoped by CWD. Query: `/wiki-query`.

## Recent

- [2026-06-05] Phase 15 (Harden extraction faithfulness + fix shipped defects, M7) DELIVERED + accepted — scoped by MEASUREMENT (the LOW/NEEDS advisories fail for 3 distinct reasons, not one). Footnote-resume fix in extract_red_flags (3 iterations): _SECTION_STOP terminals always break + a conditional _FOOTNOTE_STOP (mid-list page-boundary footnote run transient when another section follows → skip+resume to the next anchor; terminal for a last section → break) + 2 targeted _CITATION signatures (case-docket + no-day paren-date) to kill 2 footnote-tail leaks. SURGICAL: fin-2025-a003 recovered its silently-dropped L499 escrow flag (17→18), 0 collateral — all 13 other advisories byte-identical, EFE 12+12, 7C/3L/4N held. esc() entity sweep (fin-2022-a001 + fin-2024-a002 `&gt;=`/`&lt;=` → raw text, verified in the built file); escrow IND-18 added; manifest regen + dist/corpus rebuild + --check all zero drift. GLUED-NO-SEPARATOR SPLITTING DEFERRED — no safe deterministic split (re-confirms Phase-12); needs a better converter, not a splitter. The abort rule was hit (first attempt over-captured) but resolved by the bounded next_boundary rule, not aborted. 5 lite tasks; byte-frozen held. User chose harden-spine over scaling / showcase debt / wow beat
- [2026-06-05] Phase 14 (Scale corpus derivation — 3 more CLEAN advisories → 5/14 live, M7) DELIVERED + accepted — PURE AUTHORING (zero engineering): derived 3 more records via the proven --scaffold-derived→author→--check-derived loop, rebuilt dist/corpus → live menu 2/14 → 5/14. fin-2020-a008 human trafficking (10 ind, pruned 1 noise line, 2 BUILD_NOW) · fin-2025-a003 Chinese MLN (17 ind, clean, 5 BUILD_NOW — most buildable) · fin-2025-a002 Iran (16 ind, validate-first passed, 4 BUILD_NOW / 7 BUILD_ENRICH — enrichment-hungry contrast). Matrix-merge authoring (verbatim flags + src_line preserved, build_rec auto-derived). Verified: 3× --check-derived · --check all 4-artifact zero drift · headless render assertions · node --check · --selftest 12+12; index.html/corpus.html/config/**/scripts/** + 3 typology dists byte-untouched. FINDINGS → Phase-15: extractor missed fin-2025-a003 L499 (page-break-glued flag); pre-existing fin-2022-a001 esc() double-escape render bug. User chose scale-derivation over spine-robustness / corpus-wow-beat / showcase-debt
- [2026-06-05] Phase 13 (Corpus explorer — advisory-selection front-end + per-indicator build-rec render, M7) PLANNED, direction approved — the PAYOFF: a NEW standalone ship artifact `dist/corpus/index.html` (built from `corpus.html`), a FinCEN CORPUS EXPLORER where a stakeholder picks 1 of 14 advisories and watches the loop derive coverage → per-indicator build recommendations → signal. STAGED 4-screen flow (SELECT → COVERAGE → BUILD RECOMMENDATIONS → SIGNAL SPEC); all 14 advisories shown with honest status (2 derived live). Showcase (index.html + config/** + 3 typology dists) byte-frozen; corpus.html owns its own theme CSS; build.py reads committed data (corpus-status.json + derived/*.json), never imports derive_signals.py. 5 lite tasks (1 L = corpus.html). User chose standalone over fold-into-index.html, staged over dashboard, all-14-honest over only-2-derived
- [2026-06-05] Phase 12 (FinCEN corpus derivation foundation, M7) DELIVERED — backend for a singular corpus-backed FinCEN demo (user picks 1 of 14 advisories). Committed the 14-advisory corpus md; `extract_red_flags` rewritten as a corpus-wide section-FINDER (Tier-1 + Tier-2 fallback + filters); `--corpus` → 7 CLEAN · 3 LOW · 4 NEEDS (2 NEEDS = FATF advisories, correct). Deterministic checks (cover×data matrix + traceability + build_logic shape). LLM backend = THIS session (no key) derived 2 records (kleptocracy + PRC precursors), boundary holds. Review 8/10→fixed. Spine ASSISTS, doesn't AUTOMATE. EFE 12+12; engine untouched. 5 lite tasks + 2 user refinement passes; demo expansion = Phase 13
- [2026-06-05] Phase 11 (Automated derivation — LLM-drafted signal config, AUTOMATE) completed + accepted — authoring-only `derive_signals.py` automates the manual Phase-7 article→signal derivation (deterministic `--selftest`/`--scaffold` + neural `--draft`, lazy `anthropic`, env-keyed); LLM proposes a gitignored `.draft.json`, build.py + schema + 2 human gates dispose; Anthropic structured-output shape verified vs the claude-api reference; review gate 9/10 accept (2 MEDIUM `--draft` fixes folded in); 5 lite tasks; commit c37dc39. M6 vision arc (7–11) complete
- [2026-06-05] Phase 10 (FinCEN corpus crawler — SCALE) completed + accepted — discovery manifest (`data/fincen/index.json`, 14 advisories) over mass-download; authoring-only `crawl_fincen.py` (pure `parse_index` + `--selftest`); acquire REGISTRY→manifest + `resolve_pdf` detail-page hop; 4 lite tasks; commit 0c87c47 (user chose SCALE over the elder true-up)
- [2026-06-05] Phase 9 (build-drift guard) completed + accepted — in-process `build.py --check` for the M5 zero-drift invariant (broke silently in Phase 7); commit 33db22a
- [2026-06-04] Phase 8 (doc true-up + provenance fix) completed + accepted — rebrand docs to Signal Watch; FinCEN-verbatim non-negotiable; fentanyl provenance → FINTRAC; M6 doc staleness folded in; Phase 7 dist drift corrected; commit 042d732
- [2026-06-04] M6 (pipeline walking skeleton) completed + accepted — FinCEN EFE FIN-2022-A002 slice; Act 1 verbatim render; Signal Watch rebrand; commit 8459dd9
- [2026-06-04] M5 ship — completed + accepted; compliance + offline file:// hard gate PASS; project shipped
- [2026-06-04] M3 presenter polish — engine-only keyboard nav + reset + reduced-motion; both dist rebuilt
- [2026-06-04] dev wiki bootstrapped (retrofit from HANDOFF.md milestone plan); aml-wiki linked
