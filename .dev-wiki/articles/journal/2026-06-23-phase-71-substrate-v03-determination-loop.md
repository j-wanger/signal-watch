---
title: "Phase 71: Adopt the substrate v0.3 slice; close the §12 determination loop"
aliases: []
category: journal
tags: [companion, cross-pillar, substrate-v0.3, determination-loop, vendor, lfcm]
parents: [phase-71-substrate-v03-slice-determination-loop]
created: 2026-06-23
updated: 2026-06-23
source: debrief
duration: ~half-day (single session, post-compaction estimate)
---

# Phase 71: Adopt the substrate v0.3 slice; close the §12 determination loop

## What Happened
- Adopted aml-substrate's just-shipped Phase-25 **v0.3** evidence-bundle slice (`related_parties[]` — the real BO graph) and CLOSED the §12 determination loop in the investigator workbench: **0→81 cases now reach the ≥2-leg ML determination bar from REAL signals** (not gathered corroboration), via `evidence_requirements.determine` over the fired capabilities — pure signal-watch, NOT routed through casework.
- **The T1 measure-first PROBE was the keystone** and it bent the plan productively. Two surprises drove the rest of the phase: (1) the substrate DELIBERATELY non-emits C14 (`cli.py` "C8-ONLY (C26/C14 deliberate non-emission)") → `kyc_integrity` is unreachable by the consume path → **kyc DEFERRED** at the user gate (it becomes a §12 substrate-emission brief item, not a deliverable). (2) ZERO cases reach ≥2-leg from the EMITTED+DEDUPED bundles because `_read_population`'s dedup-keep-richer DROPS the C8 screening leg whenever a monitoring mechanism co-exists — but a **per-customer MERGE** recovers it (366 capability legs / 667 with related_parties→ML-A4). The closure leg pair is **C8 (ML-A3) + C15/related_parties (ML-A4)**, NOT the brief's internal C1/C7/C14 (C1 nulled, C7 deferred, C14 non-emitted).
- T1 STOP+REPORT surfaced the merge + kyc-defer scope changes; the user confirmed (merge YES, kyc DEFER) before T2 committed anything.
- Full E2E: the casework v0.3 **acceptance bump** (KNOWN_CONTRACT_VERSIONS += "0.3") + a one-file corpus extension (`fin-2025-a003`) + re-vendor (VENDORED_AT 021fb80→157554b); casework sibling 289 tests green. A late nuance: the casework corpus gap was SOURCE-COVERAGE (the snapshot only covered `fincen-alerts/`, never the fincen advisory series), NOT pin-staleness — the pin held honest.
- `boGraphHTML` renders the bundle's real `related_parties[]` as a labelled ownership-weighted SVG network (reused `liveGraphLayout` + a 1-line fix to carry `ownership_pct`); owner KYC posture on edge rows; "N pct" never "%"; declared-not-gathered framing; XSS-escaped.
- T4: no `present_atoms` change needed — related_parties stays the ML-A4 EVIDENCE/render, C15 stays the leg TRIGGER (lighting ML-A4 from mere ownership-presence would over-fire dishonestly).

## Decisions Made
- **§12 closure = the DETERMINATION beat** (`evidence_requirements.determine`, ≥2-leg from real signals), NOT the signed STR finale — pure signal-watch, does NOT route through casework.
- **Include the minimal casework v0.3 acceptance bump** (version whitelist + re-vendor) as an in-scope cross-pillar DEPENDENCY; defer the deeper C14-grounding verifier (so v0.3 cases SIGN, not just determine) to a casework-pillar phase (the C3/C15 pattern).
- **Per-customer MERGE** (a case = a customer): curate unions a customer's monitoring (C2-C5/C15) + C8-screening bundles — the ONLY mechanism for the §12 closure (C8 and C15 never co-occur in a single emitted bundle; the prior dedup-keep-richer dropped the C8 leg → 0 cases). User gate at the T1 STOP+REPORT.
- **Defer kyc_integrity** — the substrate's deliberate C14 non-emission makes kyc end-to-end not signal-watch-local.
- **related_parties[] stays the ML-A4 network EVIDENCE/render; C15 stays the leg TRIGGER** (no `present_atoms` change at T4).
- (Lite ceremony — no decision articles; positions captured in the ledger Phase-71 block + the _CURRENT_STATE decisions table.)

## Problems Solved
- §12 loop wouldn't close from emitted bundles (0 cases) — resolved by the per-customer MERGE replacing dedup-keep-richer in `curate_workbench_cases` (`_merge_bundles`).
- 11 finale signing regressions on the v0.3 slice — diagnosed as ALL corpus-pin drift (`fin-2025-a003` missing from casework's vendored corpus snapshot), 0 from contract/SoF/C14 — fixed by re-vendoring the casework corpus.
- kyc_integrity unreachable — diagnosed as deliberate substrate C14 non-emission (a §12 brief item), deferred at the user gate.

## Open Questions
- None unresolved. A1/A2 resolved by the T1 probe; kyc/C14/C1/C7/TF are deferred-by-design, named in the §12 brief.

## Artifacts Changed
- `scripts/curate_workbench_cases.py` (per-customer MERGE — `_merge_bundles`, replaced dedup-keep-richer)
- `data/workbench/**` (re-vendored + merged v0.3 population: 294→342 cases, coverage 99/294→107/342, funnel 189/66/39→181/79/82)
- `vendor/aml-casework/**` (021fb80→157554b — accepts v0.3 + carries `fin-2025-a003`)
- `scripts/vendor_casework.sh`, `vendor/aml-casework/VENDORED_AT` (re-vendor + pin)
- `workbench.html` (new `boGraphHTML` BO-network render; `liveGraphLayout` now carries `ownership_pct`)
- `scripts/serve_workbench.py`, `scripts/evidence_requirements.py` (§12-closure selftest; determination wiring)
- `docs/case-workbench.md`, `docs/evidence-driven-filing.md`, `docs/substrate-determination-signals-PLAN-BRIEF.md` (STATUS header), `tests/smoke-checklist.md`, `CLAUDE.md` (Current-state, replace-in-place)
- `tests/workbench.test.mjs` (117→124, +7 BO-graph tests)

## Related
- [[phases/phase-71-substrate-v03-slice-determination-loop|Phase 71]] — parent phase
- [[phases/phase-70-gather-quality-substrate-handoff|Phase 70]] — the gather-quality predecessor; this consumes its §12 brief

## Health Delta
- `workbench.test.mjs` 117→124 (+7 BO-graph); `serve_workbench`/`curate`/`evidence_requirements` selftests extended + green; `gather_quality_harness` green; news/gate/triage/corpus arcs green; `uv run pytest` 20 (count unchanged — extended existing entries).
- `build.py --check all` 8/8 ZERO dist drift; build.py imports no casework/substrate (grep clean). casework sibling 289 tests green.
- Committed slice: 294→342 cases, coverage 99/294→107/342, funnel 189/66/39→181/79/82. **§12: 0→81 cases reach the ≥2-leg ML determination bar from real signals.**
- Honesty: rendered output carries no %/catch-rate/lift token.

## Soft Observations / Phase N+1 Candidates
- The casework C14-grounding verifier + the substrate C14/C1/C7/TF emission → make v0.3 cases SIGN (not just determine) + exercise kyc/TF end-to-end (the §12 brief's open remainder). Sibling (substrate + casework) phase. | Evidence: `docs/substrate-determination-signals-PLAN-BRIEF.md` STATUS header + `docs/case-workbench.md` deferred section.
- Roll the determination/sufficiency model across the triage + gate consoles (still disposition-only). | Evidence: `docs/case-workbench.md`.
- Gather robustness (MAX_ITERS / live-vs-stub order; a deeper-chain corpus for the cap) — carried from Phase 70. | Evidence: Phase-70 journal.
