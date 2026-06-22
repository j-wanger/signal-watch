---
title: "Phase 68: Re-vendor the FINTRAC-STR-rich casework + render the structured STR in the workbench"
aliases: []
category: phases
tags: [vendoring, distribution, live-workbench, casework, fintrac-str, render, lite]
parents: [dev-wiki]
created: 2026-06-22
updated: 2026-06-22
source: plan
status: planned
scope: ["vendor/aml-casework/**", "scripts/vendor_casework.sh", "vendor/aml-casework/VENDORED_AT", "scripts/serve_workbench.py", "workbench.html", "docs/case-workbench.md", "CLAUDE.md", "README.md", "tests/workbench.test.mjs", "tests/smoke-checklist.md"]
entry_criteria: "Phase 67 delivered + accepted (the LIVE investigator workbench is shippable from a bare clone — vendored aml-casework@81df91c + make setup; serve_chain resolves vendored>sibling>GATED). BLOCKED on aml-casework Phase 13 shipping the FINTRAC-STR-rich drafter (the structured str_record shape + the rich grounded Details-of-suspicion narrative) — signal-watch re-vendors casework's NEW commit; implementation cannot begin until casework commits Phase 13."
exit_criteria: "Re-vendored casework reflects casework Phase 13 (VENDORED_AT pins the new commit + date); the workbench DECIDE view renders the structured FINTRAC STR record + the rich grounded Details-of-suspicion narrative (currently a thin narrative blob), empty FINTRAC fields shown as HONEST NULL; SAR->STR vocab trued up across the workbench UI / docs/case-workbench.md / CLAUDE.md / README; node tests/workbench.test.mjs green; serve_workbench --selftest green; python3 scripts/build.py --check all 8/8 ZERO dist drift; build.py imports no casework."
---

# Phase 68: Re-vendor the FINTRAC-STR-rich casework + render the structured STR in the workbench

## Objective

After aml-casework Phase 13 ships the FINTRAC-STR-rich drafter, RE-VENDOR it into signal-watch (re-run `scripts/vendor_casework.sh` + re-pin `VENDORED_AT`), RENDER the structured FINTRAC STR record + the rich grounded Details-of-suspicion narrative in the workbench DECIDE view (currently a thin narrative blob), and TRUE UP SAR->STR vocab across the workbench UI + docs — all with the Phase-67 distribution boundary held and the 8 offline dists byte-frozen. The companion still SUBPROCESSES the vendored casework CLI over the existing file-handoff; build.py NEVER imports casework. This is a coordinated cross-pillar follow-on: casework Phase 13 ships first, then signal-watch re-vendors.

## Scope

Files and modules affected:
- `vendor/aml-casework/**` — the re-vendored copy (reflects casework Phase 13)
- `scripts/vendor_casework.sh` — RUN to re-sync (the existing rsync + excludes script)
- `vendor/aml-casework/VENDORED_AT` — re-pin to the new casework commit + date
- `scripts/serve_workbench.py` — the LIVE DECIDE display surface (structured STR record + rich narrative; honest NULL for empty FINTRAC fields)
- `workbench.html` — the LIVE DECIDE render (structured blocks + the rich Details-of-suspicion narrative)
- `docs/case-workbench.md` · `CLAUDE.md` · `README.md` — SAR->STR vocab true-up (the Canadian-bank demo files an STR)
- `tests/workbench.test.mjs` — coverage for the structured-blocks + rich-narrative render + the honest-NULL empty-field path
- `tests/smoke-checklist.md` — the STR-render smoke row

The casework consume is TOOL-USE (build.py NEVER imports aml_casework; the companion subprocesses the vendored CLI over the existing file-handoff — file-contract; `vendor/` is outside build.py's world).

## Key constraints

- **Boundary held (Phase-67 precedent):** vendoring is DISTRIBUTION not import-coupling — the companion subprocesses casework; build.py NEVER imports it; `vendor/` is outside build.py's world; the 8 offline dists stay BYTE-FROZEN (`--check all` 8/8).
- **Companion-only render:** the structured STR render lives in `workbench.html` / `serve_workbench.py` — NOT a ship target (no 9th dist; the offline ship artifacts unchanged).
- **Honest NULL:** empty FINTRAC fields (the no-PII bundle lacks aliases / beneficial owner / IP / names) are surfaced as HONEST NULL, never faked — grounded-or-empty honesty, not fabricated.
- **STR-primary vocab:** the filer-facing prose says STR (Canadian-bank demo); the `str_record` model is already STR — this trues up the surrounding language.

## Exit Criteria

- [ ] Re-vendored casework reflects casework Phase 13; `VENDORED_AT` pins the new commit + date.
- [ ] The workbench DECIDE view renders the structured FINTRAC STR record + the rich grounded Details-of-suspicion narrative (was a thin narrative blob); empty FINTRAC fields shown as HONEST NULL.
- [ ] SAR->STR trued up across the workbench UI / docs/case-workbench.md / CLAUDE.md / README.
- [ ] `node tests/workbench.test.mjs` green.
- [ ] `serve_workbench --selftest` green.
- [ ] `python3 scripts/build.py --check all` 8/8 ZERO dist drift; build.py imports no casework.

## Abort

Any dist drift / a vendored import sneaking into build.py / the subprocess boundary broken → STOP-and-surface.

## Blocked-on

**aml-casework Phase 13** — the FINTRAC-STR-rich drafter (the structured `str_record` shape + the rich grounded Details-of-suspicion narrative) must SHIP + COMMIT in aml-casework before signal-watch can re-vendor and render. Implementation begins CASEWORK-SIDE first; signal-watch re-vendors casework's NEW commit. Until then this phase is PLANNED, not active.

## Gates

- [x] Direction confirmed by user (coordinated with aml-casework Phase 13; ledger Phase-68 A0–A2 — A0/A1 resolved casework-side, A2 the boundary by Phase-67 precedent; 2026-06-22)
- [ ] Delivery accepted (post-implementation report — after casework Phase 13 ships + the re-vendor)

## Notes

- Ceremony: LITE (the assumption-ledger gate IS the direction gate; spec waived).
- Ledger: Phase-68 block in `assumption-ledger.md`.
- Cross-pillar coordination: casework Phase 13 first (ships the FINTRAC-STR-rich drafter), then signal-watch re-vendors — the same vendor-then-render rhythm as Phase 67, here gated on the sibling's new commit.
