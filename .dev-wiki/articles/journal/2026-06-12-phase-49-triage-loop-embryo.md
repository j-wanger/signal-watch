---
title: "Phase 49: Triage-loop embryo made demo-able — §14's continuous adjudication loop as the 5th ship artifact (triage console)"
aliases: []
category: journal
tags: [triage-loop, adjudication, lfcm, ship-artifact, synthetic-history, m9]
parents: [phase-49]
created: 2026-06-12
updated: 2026-06-12
source: debrief
duration: ~1 session (planned AND implemented same day 2026-06-12)
---

# Phase 49 — Triage-loop embryo made demo-able: §14 as the 5th ship artifact (triage console)

## What Happened
- STANDARD ceremony. ALL 5 tasks [x] same-session 2026-06-12 (planned and implemented today; everything UNCOMMITTED in the working tree — the delivery flow commits). Exit criteria 5/5 MET, review-gate-verified empirically. READY FOR COMPLETION — delivery gate pending.
- T1 scenario dataset + curate script: `data/triage/scenarios.json` — 20 scenarios (16 + 4 controls), 4 strata 10/3/3/4; the TM-104 divergent pair shares panel P-HF-104 BY REFERENCE; 6 labeled second-rater seeds; `curate_triage_scenarios.py --selftest` rejects 10 seeded-broken fixtures; regen-twice byte-identical.
- T2 build boundary + `triage` target: errors-list validation (console precedent); 4 tamper classes + 2 bonus drift classes caught unit-level; 6 existing targets zero drift; probe-history appears in build.py comments ONLY (claim-shaped grep proves it).
- T3 triage.html arc RED-first (test skeleton failed on the missing file FIRST): full Queue → Evidence → Disposition (§14 grammar incl. need-more-info → C/D picker + the policy-gap escape; rationale REQUIRED) → Reveal (decisions-not-correctness; second-rater replay; process-inconsistency surfacing) → Discovery ledger; 57 core assertions; provisional dist. Initially dispatched to a subagent which the user KILLED → implemented inline (USER OVERRIDE; no artifacts lost — the agent had only read files).
- T4 harness full coverage 93/93: hand-computed agreement fixture (1/2, incl. the escalated-but-fired exclusion); signal-gap derivation; XSS; keyboard guards incl. SELECT; both motion modes; FINAL dist freeze (dist/triage/index.html 96,686 B).
- T5 docs + FULL REGATE: CLAUDE.md artifact #5 + targets + tests + milestone; HANDOFF §8; smoke-checklist triage section incl. the "read 4 panels, one per stratum" believability row; --check all 7/7 zero drift; all suites green; claim-shaped honesty greps green; derive_signals.py + program-blueprint.md byte-untouched.

## Decisions Made
- D1–D8 pre-captured at plan in [[decisions/phase-49-triage-loop-embryo|the Phase-49 decision article]] (approved, high) — no new decision articles (dedup). Implementation-time (small, journal-only): (a) T2's success grep concretized to `! grep -E '^[^#]*"probe-history"|^[^#]*probe_history'` after the word-shaped form failed on its OWN documentation comments — claim-shape success greps at PLAN time; (b) the CLAUDE.md trim toward ~200 consciously DEFERRED again (~330 after the artifact-#5 additions; rewriting load-bearing live-mode paragraphs at session end failed the cost-of-error test; debt now two phases old, named in the delivery report); (c) T3 subagent → inline (USER OVERRIDE); (d) novel-source validation implemented STRONGER than planned — doc jurisdiction verified via the merged corpus + source registry AND flag/red_flag/C/D drift-checked byte-equal vs the CURRENT committed indicator (plan-reviewer suggestion adopted; the console-cases precedent).

## Problems Solved
- T2's word-shaped probe-history grep failed on its own documentation comments — concretized to the claim-shaped negative grep (the same fix the plan reviewer had prescribed for T5's greps; the lesson generalizes to plan time).

## Artifacts Changed
- `triage.html` + `dist/triage/index.html` (NEW, 5th ship artifact, 96,686 B) · `data/triage/scenarios.json` + `scripts/curate_triage_scenarios.py` (NEW; regeneration-only, US_FEDERAL_ALLOWLIST = fin-2022-a002 / ofac-virtual-currency / fin-2023-alert004)
- `scripts/build.py` (TRIAGE_* constants + load/validate/render/build/check_triage + main wiring — all/--check now 7 targets)
- `tests/triage-console.test.mjs` (NEW, 93) · `CLAUDE.md` · `HANDOFF.md` §8 · `tests/smoke-checklist.md` · `specs/phase-49-triage-loop-embryo.md` · `.dev-wiki/*`

## Health Delta
- +1 test harness (triage-console, 93 assertions, NEW) · +1 selftest surface (curate_triage_scenarios --selftest) · --check all 6→7 targets · all existing suites unchanged green (corpus 303+arc, news 150, gate-console 68, derive selftest, news_quality_harness 17 fixtures within baseline).

### Review Gate
- Unified reviewer: 9/10 ACCEPT, zero HIGH. 3 MEDIUMs: (1) the "+ 4 controls" count phrasing in CLAUDE.md/HANDOFF read as 24 total — fixed inline by the orchestrator (now "16 + 4"); (2) CLAUDE.md ~330 vs the ~200 contract — carried, named in the delivery report; (3) phase-49.md exit-criteria checkboxes unchecked — pre-debrief staleness, fixed at this debrief (verified 5/5). 2 suggestions logged as soft observations. Reviewer verified empirically: all suites, regen determinism, --check all 7/7, honesty greps, frozen files byte-untouched, dataset audit.

### Gate Compliance
- Direction gate: approved, present (tasks.md gate-log `direction=approved`; assumption gate closed 2026-06-12, all_accept: false). Delivery gate: PENDING — flips post-commit via the delivery flow (gate-state follows git-state).

### Assumption-Ledger Revisit
- Phase 49: A1 held (demo-first artifact built and presentable; instrument-first noted as the follow-on) · A2 held (console-cases layering implemented exactly — curate script reads probe-history at AUTHORING time only; build.py never reads probe-history, code-grep verified; nothing entered __CORPUS__) · A3 held (structural) — the mitigation built (shared-by-reference panels, template skeletons, 16+4 ceiling); believability itself adjudicated by the user at the delivery gate · A4 held (5th ship artifact with full discipline: build target, --check, 93-assertion harness). Prior phases re-scanned: no open rows, no late bites. `scripts/check-assumption-ledger.sh` ABSENT in this repo — manual fill (0 blank rows for phase-49).

## Related
- [[phase-49|Phase 49]] — parent phase

## Soft Observations / Phase 50 Candidates
- CLAUDE.md trim debt now TWO phases old (~330 vs ~200; bloat centers = the corpus/news live-mode paragraphs; own-commit precedent exists) — candidate: a dedicated hygiene slot next phase. | maintenance
- Claim-shape success greps at PLAN time — word-shaped greps failed on their own documentation twice this phase (T2 live; T5 pre-fixed by the plan reviewer); candidate for the plan-reviewer checklist or /wiki-capture. | T2/T5
- Authored-panel BELIEVABILITY is adjudicated at the delivery gate (smoke-checklist row + verbatim scenario in the report) — the A3 revisit hook; if panels read thin, the pre-drawn split valve (richer fewer panels) is the named remedy. | A3
- §14 names TWO loop failure modes; the artifact dramatizes click-through fatigue (hidden controls) but never names elicited-consensus drift on screen — natural for the instrument-first follow-on phase. | reviewer suggestion
- The dataset embeds 8 of 12 rulebook rules (6 fired + 2 below-line) — stream growth headroom without new curation machinery. | T1
- The triage disposition grammar is a consciously DUPLICATED closed vocab in 3 places (curate script, build.py, triage.html GRADES — the console precedent); a grammar change must move all three together. | T2/T3
- T4's coverage additions all passed first-run (T3's GREEN already implemented every feature) — coverage-pinning value, not fix-driving; the RED→GREEN framing was nominal for T4. | T4
