---
title: "Phase 20: Multi-source spine, proven with FinCEN Alerts"
aliases: ["phase-20-multi-source-spine"]
category: phases
tags: ["M7", "multi-source", "fincen-alerts", "scale", "lite"]
parents: ["phase-19-durability-closeout"]
created: 2026-06-06
updated: 2026-06-06
source: plan
status: completed
scope: ["scripts/build.py", "scripts/derive_signals.py", "scripts/crawl_fincen.py", "scripts/acquire_fincen.py", "data/fincen-alerts/**", "corpus.html", "dist/corpus/index.html", "tests/**", "README.md", "CLAUDE.md"]
entry_criteria: "Phase 19 complete + accepted (impl ab0739a — corpus-explorer test harness committed, _rf_triage pinned); M0–M7 roadmap + arc + durability complete, demo at Definition of Done."
exit_criteria: "Thin SOURCES registry merges per-source corpus-status.json + derived/*.json into one __CORPUS__ with data/fincen/ byte-frozen · acquisition retargets to the FinCEN alerts hub → ≥5 committed alert mds · ≥4 alert records --check-derived clean via the inverted loop · corpus.html unified advisories+alerts menu with honest type chips · --check all zero drift, harness extended, showcase + data/fincen/ byte-frozen · README/CLAUDE document the registry + Alerts as source #2 + OFAC as the next-source candidate."
---

# Phase 20: Multi-source spine, proven with FinCEN Alerts

## Objective

Scale the corpus beyond FinCEN *advisories* to other FinCEN *publication types* (Alerts first) via a THIN multi-source pipeline registry, staying entirely inside the verbatim public-domain regime so NO non-negotiable changes — still FinCEN, still 17 USC §105, still verbatim. The quote-grounding gate (`check_record`/`rf_region`/`normalize`) is reused UNCHANGED because it is already source-agnostic; the multi-source generalization is proven via a MERGE, not a migration.

## Scope

The UNFREEZE (edits allowed):
- `scripts/build.py`, `scripts/derive_signals.py` — the SOURCES registry + per-source `--corpus-status`
- `scripts/crawl_fincen.py`, `scripts/acquire_fincen.py` — retarget acquisition to the FinCEN alerts hub
- `data/fincen-alerts/**` — the NEW source #2 (index.json, mds, derived records, corpus-status.json)
- `corpus.html`, `dist/corpus/index.html` — unified menu + honest type chips + rebuild
- `tests/**` — extend the harness for the multi-source menu
- `README.md`, `CLAUDE.md` — document the spine

FROZEN byte-untouched: `index.html`, `config/**`, the 3 typology dists, AND `data/fincen/**` (the `fincen-advisories` source — corpus-status.json + the 14 mds + 12 derived stay byte-identical; prove multi-source via the MERGE, not a migration).

## Exit Criteria

- [ ] A thin SOURCES registry merges per-source `corpus-status.json` + `derived/*.json` into one `__CORPUS__`; `build.py corpus` rebuilds dist/corpus with `data/fincen/` byte-frozen (`git diff data/fincen/corpus-status.json data/fincen/derived` empty)
- [ ] Acquisition retargets to the FinCEN alerts hub → `data/fincen-alerts/index.json` + ≥5 committed alert mds (checkpoint: convert one first, confirm a groundable `rf_region`)
- [ ] ≥4 alert records `--check-derived` clean via the inverted loop (LLM extracts, gate disposes); any un-groundable alert honestly skipped + documented
- [ ] `corpus.html` shows a unified advisories+alerts menu with honest Advisory/Alert type chips; the 5-screen arc unchanged per record
- [ ] `--check all` zero drift; the harness extended for the multi-source menu + an alert walking the arc; the showcase + `data/fincen/` byte-frozen
- [ ] README + CLAUDE document the registry, Alerts as source #2, the unchanged gate, the no-non-negotiable-change rationale, and OFAC as the next-source candidate

## Constraints

- NO non-negotiable change (prevents touching the "FinCEN-only verbatim" rail — still FinCEN, still 17 USC §105, still verbatim; the gate is reused unchanged).
- `data/fincen/` stays the `fincen-advisories` source BYTE-FROZEN (prevents migration churn — the subtraction test rejects renaming 14 mds + 12 derived + corpus-status; prove multi-source via the MERGE).
- The registry is ready for `{fincen-advisories, fincen-alerts, …ofac}` and no more (prevents over-engineering — NOT a plugin framework).
- NEVER fabricate (prevents synthetic numbers — the always-on "Illustrative data & outputs" badge + the verbatim public-domain attribution stay; un-groundable alerts are honestly skipped, like the 2 FATF advisories).

## Checkpoints

- T2 CHECKPOINT: convert ONE alert and confirm `rf_region(md)` is not None (a groundable red-flag region) BEFORE acquiring/converting the full batch. If un-groundable: pivot.

## Assumptions

- FinCEN Alert PDFs are direct zero-hop `/system/files/...FinCEN Alert*.pdf` links off the alerts hub (https://www.fincen.gov/resources/advisoriesbulletinsfact-sheets) — simpler than advisories' detail-page resolution. Network egress + markitdown both confirmed working in-session. If false (alerts convert mostly un-groundable): DEGRADE — pivot the source to FinCEN Financial Trend Analyses (indicator-heavy) or derive fewer-but-deeper. If the registry can't merge without growing as complex as a per-source migration (subtraction MOVES not shrinks): narrow to advisories-only + a documented registry stub.

## Notes

Direction approved by user 2026-06-06: the user reframed at the gate ("try FinCEN articles first, other than advisories") — scale via OTHER FinCEN publication types (Alerts first) over other agencies (OFAC) / a new showcase typology. This stays inside the verbatim public-domain regime so the gate is reused unchanged and the multi-source generalization is still exercised by genuinely heterogeneous content. OFAC (US-federal, also 17 USC §105) remains the documented next-source candidate if/when this proves out. FinCEN Alerts share the advisory structure (typology overview → enumerated red-flag indicators → SAR filing instructions), so the same derivation surface + gate apply. The long tail of remaining alerts is cheap follow-on, not this phase. Lite ceremony — decisions recorded in `_CURRENT_STATE.md` (no decision articles).
