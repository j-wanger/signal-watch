# Active Phase Context

**Phase 68 — *Re-vendor the FINTRAC-STR-rich casework + render the structured STR in the workbench*** (signal-watch-local, LITE) — direction gate accepted 2026-06-22 (coordinated with aml-casework Phase 13; A0/A1 resolved casework-side, A2 the boundary by Phase-67 precedent). After aml-casework Phase 13 ships the FINTRAC-STR-rich drafter, signal-watch re-vendors casework's NEW commit + renders the structured FINTRAC STR record in the workbench DECIDE view.

## Status
**ACTIVE — implementing (aml-casework Phase 13 committed 021fb80, re-vendored).** The blocker is cleared: casework Phase 13 shipped the FINTRAC-STR-rich drafter + committed (021fb80); `scripts/vendor_casework.sh` re-vendored it (VENDORED_AT → 021fb80) + rebuilt the venv. VERIFIED end-to-end: the chain workbench (serve_chain, CASE-P-0010361) now signs a SIGNED STR carrying ALL 5 structured blocks + crime_type + the rich Details-of-suspicion narrative (LCTR, RGS grounds, forward-intent tipping-off, honest-gap). NOTE: the CASE workbench (serve_workbench) cases ALL fail-closed (composed mules, the documented defensibility climax) → the live signed STR appears in the CHAIN workbench. Remaining: render the structured blocks in chain.html + SAR→STR vocab + verify --check all 8/8 (chain.html/workbench.html are companion-only, NOT ship targets → dists unaffected).

## Objective
After aml-casework Phase 13 ships the FINTRAC-STR-rich drafter, RE-VENDOR it into signal-watch (re-run `scripts/vendor_casework.sh` + re-pin `VENDORED_AT`), RENDER the structured FINTRAC STR record + the rich grounded Details-of-suspicion narrative in the workbench DECIDE view (currently a thin narrative blob; empty FINTRAC fields shown as HONEST NULL), and TRUE UP SAR->STR vocab across the workbench UI + docs — with the Phase-67 distribution boundary held and the 8 offline dists byte-frozen. The companion still SUBPROCESSES the vendored casework CLI over the existing file-handoff; build.py NEVER imports casework.

## Scope
`vendor/aml-casework/**` (the re-vendored copy) · `scripts/vendor_casework.sh` (RUN to re-sync) · `vendor/aml-casework/VENDORED_AT` (re-pin to the new commit + date) · `scripts/serve_workbench.py` (the LIVE DECIDE display surface) · `workbench.html` (LIVE display surfaces — structured blocks + rich narrative) · `docs/case-workbench.md` · `CLAUDE.md` · `README.md` · `tests/workbench.test.mjs` · `tests/smoke-checklist.md`.

## Key constraints
- Boundary held (Phase-67 precedent): build.py imports no casework; the companion subprocesses the vendored CLI over the file-handoff; `vendor/` is outside build.py's world; the 8 offline dists stay BYTE-FROZEN (`--check all` 8/8).
- The structured STR render is COMPANION-ONLY (`workbench.html` / `serve_workbench.py` — NOT a ship target; no 9th dist).
- Empty FINTRAC fields (the no-PII bundle lacks aliases / beneficial owner / IP / names) surfaced as HONEST NULL — grounded-or-empty honesty, never faked.
- STR-primary vocab (the Canadian-bank demo files an STR; the `str_record` model is already STR — this trues up the filer-facing prose).

## Exit criteria
Re-vendored casework reflects casework Phase 13 (`VENDORED_AT` pins the new commit + date); the workbench DECIDE view renders the structured FINTRAC STR record + the rich grounded Details-of-suspicion narrative; SAR->STR trued up across the workbench UI / docs/case-workbench.md / CLAUDE.md / README; `node tests/workbench.test.mjs` green; `serve_workbench --selftest` green; `python3 scripts/build.py --check all` 8/8 ZERO dist drift; build.py imports no casework.

## Abort
Any dist drift / a vendored import sneaking into build.py / the subprocess boundary broken → STOP-and-surface.

## Blocked-on
**aml-casework Phase 13** — the FINTRAC-STR-rich drafter (the structured `str_record` shape + the rich grounded Details-of-suspicion narrative) must SHIP + COMMIT in aml-casework before signal-watch re-vendors and renders.

Gates:
- [x] spec — waived under LITE ceremony (the assumption-ledger gate IS the direction gate, Phase-67 precedent)
- [x] Direction confirmed (coordinated with aml-casework Phase 13; ledger Phase 68 A0–A2, by Phase-67 boundary precedent)
- [x] Delivery accepted (post-implementation report 2026-06-22; re-vendored casework@021fb80 + venv rebuilt; chain.html renders the structured FINTRAC STR record [offence + structured aggregate + honest-NULL]; SAR→STR vocab trued up across chain/workbench UIs + docs; build.py --check all 8/8 byte-frozen + imports no casework; all 7 .mjs arcs + both selftests green. REFRAME captured: the CASE workbench fails-closed [defensibility climax] → the live signed STR is the CHAIN workbench, where the render landed.)

Plan [[phases/phase-68-restr-vendor-render]]; ledger Phase-68.
