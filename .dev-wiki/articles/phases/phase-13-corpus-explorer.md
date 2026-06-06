---
title: "Phase 13: Corpus explorer (advisory-selection front-end + per-indicator build-rec render)"
aliases: [corpus-explorer, advisory-selection, build-rec-render, corpus-demo]
category: phases
tags: [milestone-m7, frontend, ship-artifact, build-recommendation, staged-flow, corpus]
parents: []
created: 2026-06-05
updated: 2026-06-05
source: plan
status: active
ceremony: lite
scope: ["corpus.html", "scripts/build.py", "scripts/derive_signals.py", "data/fincen/corpus-status.json", "dist/corpus/index.html", "README.md", "CLAUDE.md"]
entry_criteria: "Phase 12 complete + accepted (M7 foundation): the deterministic spine is validated across all 14 FinCEN advisories (7 CLEAN / 3 LOW / 4 NEEDS), and the LLM backend (no key) derived 2 proof-slice records (fin-2022-a001 kleptocracy 5-ind/2-BUILD_NOW + fin-2024-a002 PRC precursors 14-ind/4-BUILD_NOW), each passing --check-derived. The derived-record shape (per-indicator status/data/build_rec/rationale + build_logic on BUILD_NOW gaps) is stable. User wants the PAYOFF: render the corpus-backed demo so a stakeholder picks an advisory and watches coverage → build recommendations → signal."
exit_criteria: "(1) dist/corpus/index.html is a NEW self-contained offline ship artifact (no fetch / ES module / external script) rendering a STAGED 4-screen corpus explorer: SELECT (14 advisories with honest status chips — DERIVED live, CLEAN/LOW/NEEDS 'not yet derived', FATF non-derivable; the 2 derived advisories clickable) → COVERAGE (coverage gauge covered=1/partial=0.5/gap=0 + indicator list) → BUILD RECOMMENDATIONS (per-indicator cover×data→build_rec matrix, BUILD_NOW-first, each row src_line-traceable to its red flag) → SIGNAL SPEC (BUILD_NOW signal card(s) from build_logic). (2) derive_signals.py --corpus-status emits committed data/fincen/corpus-status.json (14 entries: id, advisory_no, title, source, status, flag_count, derivable; deterministic, stdlib-only, anthropic lazy). (3) build.py gains render_corpus/build_corpus/check_corpus + special 'corpus' target resolution + a corpus-data boundary validator (build_rec ∈ enum; BUILD_NOW ⇒ full build_logic shape), assembling __CORPUS__ from corpus-status.json + derived/*.json; build.py does NOT import derive_signals.py. (4) the always-on 'Illustrative data & outputs' badge + reduced-motion + keyboard parity present. (5) git diff index.html empty; config/** + the 3 typology dists byte-untouched; build.py --check all (typologies) zero drift. (6) documented in README + CLAUDE."
---

# Phase 13: Corpus explorer (advisory-selection front-end + per-indicator build-rec render)

## Objective

The payoff for the M7 corpus-backed demo: render the Phase-12 derived records as a NEW standalone ship
artifact — a FinCEN CORPUS EXPLORER where a stakeholder picks one of 14 advisories and watches the loop
derive its coverage → per-indicator build recommendations → signal spec. The new centerpiece is the
per-indicator cover×data → build_rec render (the analytical artifact Phase 12 produced as data).

## Approach

A NEW standalone artifact `dist/corpus/index.html` (built from `corpus.html` via build.py) — NOT folded
into the six-act `index.html` engine. corpus.html owns its own copy of the dossier theme CSS (no shared
include) so the 3-typology showcase stays byte-frozen. The view is a STAGED 4-screen flow (user chose
staged theatre over a dense analyst dashboard — this is a pitch artifact):

1. **SELECT** — all 14 FinCEN advisories, each with an honest status chip: DERIVED (live, clickable) ·
   CLEAN/LOW/NEEDS (the --corpus extraction status, "not yet derived") · FATF shown non-derivable.
2. **COVERAGE** — chosen advisory's coverage gauge (covered=1, partial=0.5, gap=0) + indicator list.
   Reuses the Act-0 gauge/map component (re-implemented in corpus.html, not imported).
3. **BUILD RECOMMENDATIONS** (the NEW centerpiece) — per-indicator matrix: status × data → build_rec
   (BUILD_NOW / ENHANCE / BUILD_ENRICH / MONITOR / SOURCE_DATA / COVERED) + rationale, sorted
   BUILD_NOW-first, each row traceable to its red-flag + src_line.
4. **SIGNAL SPEC** — the BUILD_NOW signal card(s) from build_logic.

Boundaries held: build.py reads committed data artifacts (corpus-status.json + derived/*.json) and never
imports derive_signals.py (the standing "no authoring tool imported by engine or build.py"
non-negotiable). The deterministic status manifest is emitted by `derive_signals.py --corpus-status`. No
fabricated lift/stats — the derived data drives everything; the always-on "Illustrative data & outputs"
badge stays.

Build-rec matrix (cover×data → category, from derive_signals.py `_REC_MATRIX`): (covered,*)→COVERED;
(gap,available)→BUILD_NOW; (gap,partial)→BUILD_ENRICH; (gap,insufficient)→SOURCE_DATA;
(partial,available|partial)→ENHANCE; (partial,insufficient)→MONITOR.

## Scope

Files and modules affected:
- `corpus.html` (NEW) — standalone explorer template (own theme CSS + corpus render JS + `__CORPUS__`).
- `scripts/derive_signals.py` — add `--corpus-status` emitting `data/fincen/corpus-status.json`.
- `scripts/build.py` — add render_corpus / build_corpus / check_corpus + special "corpus" target + a
  corpus-data boundary validator; assemble `__CORPUS__` from committed data. Does NOT import derive_signals.py.
- `data/fincen/corpus-status.json` (NEW) — committed per-advisory status manifest (14 entries).
- `dist/corpus/index.html` (NEW) — the built artifact, committed (commit-dist convention).
- `README.md`, `CLAUDE.md` — document the corpus explorer.

UNTOUCHED: `index.html`, `config/**` (typologies + schema.md), `dist/{fentanyl,trade-based,elder-financial-exploitation}/`.

## Exit Criteria

- [ ] `dist/corpus/index.html` is a NEW self-contained offline ship artifact (no fetch / ES module / external script) rendering the staged 4-screen explorer (SELECT → COVERAGE → BUILD RECOMMENDATIONS → SIGNAL SPEC).
- [ ] SELECT lists all 14 advisories with honest status chips (DERIVED live/clickable · CLEAN/LOW/NEEDS "not yet derived" · FATF non-derivable); the 2 derived advisories explorable through all 4 screens.
- [ ] BUILD RECOMMENDATIONS renders the per-indicator cover×data → build_rec matrix, BUILD_NOW-first, each row src_line-traceable; SIGNAL SPEC renders ≥1 BUILD_NOW card from build_logic.
- [ ] `derive_signals.py --corpus-status` emits committed `data/fincen/corpus-status.json` (14 entries); deterministic, stdlib-only, anthropic lazy.
- [ ] `build.py corpus` / `--check corpus` work; build.py does NOT import derive_signals.py; the corpus-data boundary validator fails loud (build_rec ∈ enum; BUILD_NOW ⇒ full build_logic shape).
- [ ] Always-on "Illustrative data & outputs" badge + reduced-motion + keyboard parity present.
- [ ] `git diff index.html` empty; `config/**` + the 3 typology dists byte-untouched; `build.py --check all` (typologies) zero drift.
- [ ] Documented in README + CLAUDE.

## Constraints (load-bearing)

- **Standalone artifact, showcase byte-frozen** — `index.html` + `config/**` + the 3 typology dists stay byte-untouched. corpus.html duplicates the theme CSS rather than sharing an include. `git diff index.html` stays empty.
- **Single self-contained file, offline** — `dist/corpus/index.html` runs by opening one file, no server, no fetch, no ES module (same non-negotiable as the showcase; file:// breaks fetch/modules).
- **build.py stays decoupled from the authoring layer** — it reads committed data artifacts (corpus-status.json + derived/*.json), never imports derive_signals.py; it re-implements only a light renderable-shape check at its boundary.
- **Honest data only** — all 14 shown with their true status; only the 2 derived are live; no fabricated lift/stats; the "Illustrative data & outputs" badge stays always visible.
- **Derived records drive the render** — the per-indicator status/data/build_rec/rationale + build_logic from data/fincen/derived/*.json is the data model; the cover×data matrix is the same one the deterministic spine enforces.

## Checkpoints

- After T2/T3: if the derived-record shape can't drive the coverage gauge / build-rec matrix / spec card without an engine edit — keep corpus.html fully standalone (re-implement the renderable component in its own CSS/JS), don't reach into index.html.
- If reusing the Act-component markup would force an index.html change — re-implement it in corpus.html instead; the showcase stays byte-frozen.
- Blocked >3 attempts on a task → ask the user: skip or abort.

## Assumptions

- The 2 derived records (fin-2022-a001, fin-2024-a002) are check-passing and shape-stable (verified Phase 12). The other 12 advisories render as selectable-but-not-yet-derived with their --corpus status.
- The Act-0 gauge, Act-2 matrix, and Act-4 spec-card markup are re-implementable in corpus.html from the existing index.html patterns without an engine edit (the render components are simple DOM + CSS).

## Notes

Direction approved by user 2026-06-05: a NEW standalone corpus-explorer artifact + a STAGED 4-screen flow
+ all-14-with-honest-status. User chose standalone over fold-into-index.html (honors the "keep the six-act
arc + two wow beats" non-negotiable literally, protects the showcase from pre-demo regression); staged
flow over a dense dashboard (pitch artifact, not analyst dashboard); all-14-honest over only-2-derived or
derive-5-more-first (tells the corpus story without faking content). This is the PAYOFF for M7 — the
render of the Phase-12 derived build-rec concept. Follow-ups not in scope: scaling LLM-backend derivation
to the 5 remaining CLEAN advisories; glued-list splitting for the 2 NEEDS advisories; excluding the 2 FATF
advisories from the derivable corpus.
