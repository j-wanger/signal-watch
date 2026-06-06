---
title: "Phase 13 Corpus explorer (advisory-selection front-end + per-indicator build-rec render) — M7 — THE PAYOFF"
aliases: [corpus-explorer-session, build-rec-render]
category: journal
tags: [milestone-m7, frontend, ship-artifact, build-recommendation, staged-flow, corpus]
parents: [phase-13-corpus-explorer]
created: 2026-06-05
updated: 2026-06-05
source: debrief
duration: ~1 session
---

# Phase 13 Corpus explorer — THE PAYOFF for M7

## What Happened
- The M7 payoff: rendered the Phase-12 derived records as a NEW standalone ship artifact
  `dist/corpus/index.html` (from `corpus.html`) — a FinCEN CORPUS EXPLORER where a stakeholder picks 1 of
  14 advisories and watches coverage → per-indicator build recommendations → signal spec, in a STAGED
  4-screen flow (SELECT → COVERAGE → BUILD RECOMMENDATIONS → SIGNAL SPEC), not a dense dashboard.
- T1: `derive_signals.py --corpus-status` → committed `corpus-status.json` (14 advisories + summary 7
  CLEAN/3 LOW/4 NEEDS); shared `_section_counts` + best-effort `_load_index`; stdlib-only, anthropic lazy.
- T2 (the L): `corpus.html` — standalone, own copy of the dossier theme CSS (~200 lines, deliberate:
  showcase byte-frozen), `__CORPUS__` injection, staged render JS, reduced-motion + keyboard parity,
  always-on illustrative badge, defensive rendering (malformed → labeled placeholder, never blank).
- T3: build.py `render_corpus`/`build_corpus`/`check_corpus`/`validate_corpus_data` (fail-loud: build_rec ∈
  enum; BUILD_NOW ⇒ full build_logic) + special "corpus" target, folded into `all`/`--check all` (now 4
  artifacts); reads committed data, NEVER imports derive_signals.py (only comment/hint mentions).
- T4: built + verified — 17 headless DOM-shim assertions (uncommitted /tmp harness) + 3 browser
  screenshots; both derived advisories render all 4 screens; non-derived show honest status.
- T5: README + CLAUDE document the new ship target + decoupled boundary; milestone bumped to M7.
- Review ACCEPT 9/10. One MEDIUM — esc() didn't escape quotes though used in double-quoted attribute
  positions — FIXED inline (now escapes `"`/`'`), rebuilt, re-verified.

## Decisions Made
- Phase 13 deliverable = a NEW standalone corpus-explorer artifact (NOT folded into six-act `index.html`).
  Honors the six-act non-negotiable; protects the showcase; the derived-record shape fits a
  coverage→build-rec→signal view, not the theatrical arc. (Standalone over fold-in.)
- Corpus scope = all 14 shown with HONEST status (2 derived live; 12 show --corpus CLEAN/LOW/NEEDS as "not
  yet derived"). (Over "only 2 derived" / "derive ~5 more first".)
- Corpus view = a STAGED 4-screen flow, not a dense dashboard. (Pitch artifact; reuses act-staging muscle.)
- build.py stays DECOUPLED — reads committed data, never imports derive_signals.py; the manifest is
  emitted by `derive_signals.py --corpus-status`.

## Problems Solved
- esc() quote-escaping gap (review MEDIUM): used in double-quoted attribute positions but only escaped
  `<`/`>`/`&`. Fixed to also escape `"`/`'`, rebuilt corpus.html → dist, re-verified.

## Open Questions
- Scale derivation to the ~5 remaining CLEAN advisories (fuller live menu) — only 2/14 derived.
- Glued-list splitting in `extract_red_flags` for the 3 LOW advisories (no blank separators).
- Explicitly exclude/label the 2 FATF advisories (now lumped under "no red-flag list").
- (Carried) elder presentation-values true-up · fentanyl verbatim re-point · manifest --fetch cadence.

## Artifacts Changed
- `corpus.html` (NEW), `data/fincen/corpus-status.json` (NEW), `dist/corpus/index.html` (NEW)
- `scripts/derive_signals.py` (+`--corpus-status`, shared helpers), `scripts/build.py` (+corpus path)
- `README.md`, `CLAUDE.md` (document the explorer; milestone → M7)

## Related
- [[phase-13-corpus-explorer|Phase 13: Corpus explorer]] — parent phase
- [[2026-06-05-phase-12-fincen-corpus-derivation|Phase 12]] — produced the derived records this renders

## Soft Observations / Phase 14 Candidates
- Only 2/14 derived; live menu thin for a stage demo. → scale derivation to ~5 CLEAN. Evidence: corpus-status.json (7 clean).
- `extract_red_flags` can't split the 3 LOW advisories. → glued-list splitting. Evidence: `--corpus` report.
- 2 FATF advisories correctly non-derivable but lumped with 2 extractor-miss advisories. → explicit FATF labeling. Evidence: corpus-status.json (4 × extraction=none).
- The explorer is analytical; it has no Act-5 combination-lift "wow" beat. → optional per-advisory lift/composition reveal (needs derived lift data). Evidence: 4-screen flow vs the 7-act arc.
- corpus.html duplicates ~200 lines of theme CSS (deliberate — showcase byte-frozen). → if the showcase ever unfreezes, factor a shared-theme partial. Evidence: corpus.html `<style>`.

### Health Delta
No unit-test framework (vanilla HTML/Python). Gates green at session end: `--selftest` 12+12; both derived
records pass `--check-derived`; `build.py --check all` = 4 artifacts zero drift; `index.html` + `config/**`
byte-untouched. New uncommitted /tmp harness: headless DOM-shim render smoke test (17 assertions). Review
9/10 ACCEPT — one MEDIUM (esc() quote-escaping) fixed inline, rebuilt, re-verified.
