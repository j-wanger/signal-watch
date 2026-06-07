# Active Phase Context

Phase: 20 - Multi-source spine, proven with FinCEN Alerts (M7) — DELIVERED + accepted (2026-06-06); all 6 tasks [x]; exit criteria GREEN (harness 40/40, --selftest PASS, --check all 4-artifact zero drift, frozen set git-diff-empty); reviewer 9/10 ACCEPT (no CRITICAL/HIGH). Committed c9de677 + delivery accepted (2026-06-06). M0–M7 + the corpus-explorer arc + durability + the multi-source spine are all complete; the demo is at Definition of Done.
Objective: Scale the corpus beyond FinCEN advisories to a 2nd publication type (Alerts) via a thin `CORPUS_SOURCES` registry decoupling source-id from storage dir — multi-source via the MERGE, not a migration; the quote-grounding gate reused UNCHANGED; still FinCEN, still 17 USC §105 verbatim → NO non-negotiable change.

Scope (delivered): `scripts/build.py` (CORPUS_SOURCES registry + _load_source merge + doc_type stamp), `scripts/{derive_signals,crawl_fincen,acquire_fincen,pdf_to_md}.py` (--alerts/--source/source_dir; gate unchanged), `data/fincen-alerts/**` (NEW source #2: 19 md + 6 derived), `corpus.html` + `dist/corpus/index.html` (unified menu + Advisory/Alert chips), `tests/**` (harness 28→40 + fincen-alerts.html fixture), `README.md`, `CLAUDE.md`, `.gitignore`. FROZEN byte-untouched: `index.html`, `config/**`, the 3 typology dists, AND `data/fincen/**` (the fincen-advisories source — proven via the MERGE, not a migration).

Key constraints:
- NO non-negotiable change (FinCEN-only verbatim rail untouched; the gate is source-agnostic, reused unchanged). `data/fincen/` stays BYTE-FROZEN (subtraction test rejects renaming 14 mds + 12 derived).
- NEVER fabricate; the always-on badge + verbatim public-domain attribution stay; un-groundable alerts honestly skipped ("no enumerated red-flag list"). The registry is ready for {advisories, alerts, …OFAC} and no more — NOT a plugin framework.

Exit criteria (all MET): registry merges per-source corpus-status.json + derived/*.json into one __CORPUS__ · ≥4 alert records --check-derived clean (6 delivered, 72 ind / 19 BUILD_NOW) · unified menu + honest type chips · --check all zero drift + frozen set git-diff-empty · README + CLAUDE document the registry + Alerts source #2 + OFAC-next.

Next: phase complete (committed c9de677 + pushed). Follow-on (cheap, NOT a phase): incremental derivation of the 11 derivable-not-yet-derived alerts. OFAC source #3 needs a verbatim-non-negotiable extension (compliance sign-off, not taken). Run /dev-plan only for a net-new stakeholder ask.
Abort: n/a (phase delivered). Blocked >3 attempts on any follow-on task → ask the user: skip or abort.

Gates:
- [x] Direction confirmed by user (scale via OTHER FinCEN publication types — Alerts first — over OFAC / a new showcase typology; thin registry, data/fincen byte-frozen; convert-one-first checkpoint — 2026-06-06)
- [x] Delivery accepted (post-implementation report 2026-06-06; reviewer 9/10 ACCEPT, no CRITICAL/HIGH; impl commit c9de677)
