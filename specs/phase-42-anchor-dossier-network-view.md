<!-- nana:approved 2026-06-10 -->
# Spec: Phase 42 — Anchor dossier view + per-scan network visualizer (live news)

## Objective

The LIVE news subsystem renders its entity-resolution data: a per-scan entity NETWORK
VISUALIZER (the navigation surface) and an ANCHOR DOSSIER (the accumulated-identity
detail view) — consuming the Phase-41 data model that is currently write-only. Bundled
rider: trim CLAUDE.md from 305 to ≤220 lines (the maintenance contract's ~200 target
plus tolerance; 220 is the single number every check in this spec uses).

## Context

Phase 41 enriched the live scan into a resolution-grade identity record (aliases,
closed-vocab properties, grounded relationship edges, main subjects) and normalized the
local DuckDB store to an ANCHOR design with cross-scan accumulation — but nothing reads
it back: `news_store.anchor_summary()` has zero consumers, and the Disposition step
shows a text-only subject map. The user's direction (dev-plan gate, 2026-06-10) is to
consume that model: graph + dossier, continuing the live-layer-is-a-real-tool
trajectory (private investigation notes are a first-class future input). The
assumption gate closed 2026-06-10: A1/A3 accept, A2 don't-know → evidence-refuted →
A2' accept (the 7 committed fixture articles are case-disjoint — zero cross-article
entity overlap, so the demo seed is a committed SYNTHETIC investigation note + a
same-article re-scan), A4 accept-with-condition (SVG is the INITIAL implementation for
demo testing), A5 recorded as a scope constraint. Ledger: `.dev-wiki/assumption-ledger.md`
Phase-42 block; decision article: `.dev-wiki/articles/decisions/phase-42-anchor-dossier-network-view.md`.

## Scope

### In scope
- `scripts/serve_news.py`: a read-only companion `GET /anchor?name=<n>` route wrapping
  `news_store.anchor_summary()`; the "anchor" endpoint added to the inlined live config.
- `news.html` LIVE region ONLY: the per-scan SVG network visualizer at Disposition
  (replacing the Phase-41 text subject map) + the anchor dossier panel (opened from a
  graph node or a watchlist row).
- A committed, clearly-labeled SYNTHETIC investigation note at
  `docs/demo-investigation-note.md` (fixture entity + client_number + one deliberately
  conflicting property) + the documented demo flow. The note must NOT live under
  `data/news/` or any `CORPUS_SOURCES` directory — those are build-consumed paths and
  would break the byte-frozen offline dist or enter the validation gate.
- `tests/news_live_test.py`, `tests/news-stream.test.mjs` extensions; `docs/news-live.md`;
  `tests/smoke-checklist.md`; CLAUDE.md (`## Current state` in place + the trim rider).

### Out of scope
- Any change to `news_ground.py` (the shared gate), `EXTRACT_SCHEMA`, `SYSTEM_PROMPT`,
  store WRITE paths, or replay fixtures (no model re-capture) — pure consumption phase.
- Fuzzy cross-scan merge adjudication (the named deferred successor).
- Offline `dist/news` enrichment (the 4 committed records carry no relationships[];
  an offline graph is a different phase) — offline artifacts stay byte-frozen.
- Vendored/CDN graph libraries; pan/zoom/drag physics (A4: SVG-initial, revisit if the
  live tool grows).
- `derive_signals.py`, the corpus, the showcase — untouched.

## Approach

One integrated view, graph as navigation: the per-scan graph renders the extraction's
entities (main subjects highlighted) and relationship edges (labels visible; CLICKING
an edge reveals its evidence quote in a detail area — click, not hover, so the
DOM-shim harness can assert it structurally); clicking a node — or a watchlist row —
fetches `GET /anchor`
and renders the accumulated identity: scans touched, properties grouped by kind with
per-scan provenance, conflicts surfaced presentation-only, aliases, relationship edges.
Layout is hand-rolled and DETERMINISTIC (no randomness), implemented as a pure
data→positions function so the dep-free node harness can assert it directly. All new
markup/CSS/JS is injected from inside the existing `/*LIVE_START*/…/*LIVE_END*/` region.
The CANONICAL documented demo flow (one referent for docs + the checkpoint): paste a
fixture article → scan → paste `docs/demo-investigation-note.md` as
source_type=investigation-note → scan → open the shared entity's dossier (accumulation
across both scans + the conflict flag visible). The same-article re-scan is the
documented OPTIONAL no-note variant showing pure accumulation.

### Domain Research Questions
1. What does an investigator actually scan first on an i2/Maltego-style chart —
   and does the layout privilege main-subject centrality or edge-label readability?
2. Which property kinds most often conflict across real adverse-media re-reports
   (age, location, spelling?) — does the conflict flag need kind-specific wording?
3. How should provenance be summarized when one anchor accumulates many scans —
   per-row source-type chips vs a scan timeline?

## Constraints (CRITICAL)

- All new markup, styles, and behavior injected from JS INSIDE the existing LIVE region
  (no static containers/CSS outside the markers): prevents live UI leaking into — or
  breaking the byte-frozen — offline `dist/news`. `--check all` must stay 5/5; the
  strip assertion extends to dossier/graph tokens absent from the built dist.
- Every store-derived string (names, aliases, property values, evidence) renders via
  `esc()`/`textContent`/`createElementNS` — never concatenated HTML/SVG markup:
  prevents stored-XSS from LLM-extracted commercial article text persisted in DuckDB.
- The dossier read path performs NO store mutation (no UPDATE/DELETE) and renders
  same-kind conflicting values as SEPARATE provenance'd rows: prevents silently
  resolving what Phase-41 D2 deliberately keeps both of.
- No vendored or CDN graph library; no new `<script src=`/external reference in
  news.html: prevents dependency creep + ship-file bloat (A4 condition: SVG-initial).
- `GET /anchor` is read-only, name-keyed (server-side name→anchor resolution — the
  merge-robust seam), 404-honest on unknown/empty-normalizing names, and gracefully
  degraded when the store is absent/--no-persist: prevents 500s and a
  name-vs-identity coupling that fuzzy merge would break.
- The graph builder tolerates degenerate topologies — 0 relationships (isolated
  nodes), edge endpoints not in the entity list (render the node, keep the edge),
  defensive from==to skip, long names: prevents crashes on the common press-release
  case and post-fold artifacts.
- Replay fixtures untouched; any new server test stubs the model and guards
  DuckDB-backed assertions behind the existing `.venv` gate: keeps dep-free runs green
  and avoids re-capture.
- The synthetic note is explicitly labeled SYNTHETIC (book.json precedent) and
  references only US-federal-fixture entities; the resulting store stays
  local/gitignored: holds the privacy boundary + the no-real-customer-data
  non-negotiable.
- CLAUDE.md trim: non-negotiables/honesty/conventions blocks semantically preserved
  (condense, never drop a rule); each removed fact verified present in
  HANDOFF.md/docs/journal; trim isolated in its own commit: prevents deleting
  load-bearing compliance text and keeps the diff reviewable.

## Success Vision

An analyst running the live companion sees the scanned article as a small, legible
network — main subjects visually primary, relationship labels readable, evidence one
interaction away — and can pivot from any entity to its accumulated dossier: which
scans touched it, what is claimed about it with per-scan provenance, and where sources
DISAGREE, shown honestly as coexisting claims rather than a resolved value. A fresh
demo can reach that state in two pastes (article + synthetic investigation note). The
offline ship artifact is bit-for-bit unchanged; the always-on illustrative badge stays;
CLAUDE.md reads as a ≤220-line current-state snapshot with its compliance rules intact.

## Exit Criteria (machine-checkable)

- [ ] `python3 tests/news_live_test.py` (incl. new /anchor tests: known anchor, unknown → 404-shape, empty-normalizing name, no-store degrade)
- [ ] `python3 scripts/serve_news.py --selftest`
- [ ] `node tests/news-stream.test.mjs` (graph: node/edge counts, main-subject marking, XSS-escaped label, degenerate topologies; dossier: conflict rows both render with provenance, honest empty state; strip: graph/dossier tokens absent offline)
- [ ] `node tests/corpus-explorer.test.mjs`
- [ ] `python3 scripts/build.py --check all` (5/5 byte-identical)
- [ ] `python3 scripts/news_ground.py --selftest && python3 scripts/derive_signals.py --selftest`
- [ ] `.venv/bin/python scripts/news_store.py --selftest`
- [ ] `test -f docs/demo-investigation-note.md && grep -qi SYNTHETIC docs/demo-investigation-note.md && grep -q "## Demo: anchor accumulation" docs/news-live.md`
- [ ] `[ $(wc -l < CLAUDE.md) -le 220 ]`

## Checkpoints

- After the /anchor route + the graph visualizer land (before the dossier panel):
  report — confirm the layout-as-pure-function shape held in the DOM-shim harness
  before building the dossier on top.
- After the demo seed lands: run the canonical demo flow live once (article scan +
  note paste) and report what the dossier actually shows — the A2' payoff check.
- If the offline `dist/news` cannot stay byte-identical: STOP and surface (abort rule).
- If a gate/store-write change starts looking necessary: STOP — that violates the A5
  scope constraint; surface instead of widening.

## Assumptions

- `anchor_summary()`'s payload shape (scans/properties/relationships as returned today)
  is sufficient for the dossier. If false (a missing field forces a store READ-path
  addition): extend the read query only — any WRITE-path change stops the phase (A5).
- The live region's JS-injection pattern can carry panel markup + SVG without static
  HTML outside the markers. If false: add a new marker pair to build.py's strip in the
  same change and re-verify `--check news` — never place live markup outside markers.
- Deterministic radial + fixed-iteration relaxation is legible at ≤~35 nodes. If false
  (overlap unreadable on the TGR article): simplify to concentric rings by
  main-subject distance before considering any library (A4 condition).
- The fixture entities give the synthetic note a usable hook (TGR/Rossi). If false:
  use any committed US-federal fixture entity; never a commercial-article entity.
