---
title: "Phase 42: Anchor dossier view + per-scan network visualizer (live news)"
aliases: [phase-42, anchor-dossier-network-view]
category: phases
tags: [news-live, entity-resolution, anchor-dossier, network-graph, svg, duckdb-read, claude-md-trim]
parents: []
created: 2026-06-10
updated: 2026-06-10
source: plan
status: active
scope: ["scripts/serve_news.py", "news.html", "tests/news_live_test.py", "tests/news-stream.test.mjs", "docs/demo-investigation-note.md", "docs/news-live.md", "tests/smoke-checklist.md", "CLAUDE.md"]
entry_criteria: "Phase 41 delivered + accepted + committed (1f74cb2 work + 62603be gate flip) + pushed to main; 0 open tasks; direction user-picked at the dev-plan gate 2026-06-10; assumption gate closed 2026-06-10 (A1/A3 accept, A2 don't-know→A2' accept, A4 accept-with-condition, A5 scope constraint)."
exit_criteria: "Graph + dossier render in the LIVE region only; GET /anchor serves anchor_summary; conflicts surfaced presentation-only (both kept); synthetic-note demo flow documented + note committed; --check all 5/5 zero drift; node news-stream + corpus green; all selftests + news_live_test green; replay fixtures untouched; the always-on badge stays; NO non-negotiable change; CLAUDE.md ≤~220 lines with non-negotiables intact."
---

# Phase 42: Anchor dossier view + per-scan network visualizer (live news)

## Objective

CONSUME the Phase-41 ER data model instead of extending it: one integrated view where the
per-scan NETWORK GRAPH is the navigation surface at the Disposition step and the ANCHOR DOSSIER
(wrapping the previously-unconsumed `news_store.anchor_summary()` — the named Phase-41 seam) is
the node detail. Plus a committed SYNTHETIC investigation-note demo seed proving anchor
accumulation + conflict surfacing + the investigation-note input in one documented flow, and the
CLAUDE.md trim rider (305 → ~200-220 lines).

Direction user-picked at the dev-plan gate 2026-06-10 — continuing the
live-layer-is-a-real-tool trajectory. Full rationale + alternatives: the finalized decision
article `articles/decisions/phase-42-anchor-dossier-network-view.md` (do not re-derive).

## Approach

1. **Per-scan network visualizer** at Disposition (replaces the Phase-41 text subject-map):
   vanilla SVG, DETERMINISTIC layout (radial initial placement + fixed-iteration relaxation, no
   `Math.random`, no vendored lib — the A4 condition: SVG is the INITIAL implementation for demo
   testing; revisit rendering tech if the live tool grows past demo scale; ≤~35 nodes). Nodes =
   scan entities (main subjects highlighted); edges = `relationships[]` with labels; edge click →
   evidence quote.
2. **Anchor dossier as node detail**: graph-node click or watchlist-row click → a NEW companion
   route `GET /anchor?name=` wrapping `news_store.anchor_summary()` → the accumulated identity:
   scans touched, properties grouped by kind WITH per-scan provenance, same-kind-multi-value
   conflicts flagged "conflicting values — both kept" (presentation-only, NEVER auto-resolved —
   Phase-41 D2 carried), aliases, relationship edges. Honest empty state when no anchor exists;
   honest null/404 from the route; graceful degrade when the store is absent / `--no-persist`.
3. **Demo seeding (A2')**: a committed SYNTHETIC investigation note (clearly labeled synthetic;
   references a fixture entity, e.g. George Rossi/TGR Group; carries a `client_number` + one
   deliberately conflicting property) pasted as `source_type=investigation-note`, plus a
   same-article re-scan — one documented demo flow. Evidence check at the gate: the 7 fixture
   articles are case-DISJOINT (zero cross-article entity overlap), so this REPLACES any
   re-scan-different-articles script. The seeded DuckDB store stays local/gitignored.
4. **Pure consumption (A5/A1)**: NO change to `news_ground` (the shared gate), `EXTRACT_SCHEMA`,
   `SYSTEM_PROMPT`, store writes, or replay fixtures (no re-capture). All new client code inside
   news.html's `/*LIVE_START*/…/*LIVE_END*/` region. Offline `dist/news` + the 4 committed
   records stay BYTE-FROZEN (`python3 scripts/build.py --check all` must stay 5/5 zero drift).
5. **CLAUDE.md trim rider**: 305 → ~200-220 lines, replace-in-place per the maintenance
   contract; per-phase narrative → journal/HANDOFF; non-negotiables + honesty constraints
   verbatim.

## Scope

Files and modules affected:
- `scripts/serve_news.py` — the `GET /anchor` READ route only
- `news.html` — the LIVE region only (graph + dossier panel); offline strip intact
- `tests/news_live_test.py`, `tests/news-stream.test.mjs`
- `docs/demo-investigation-note.md` — the NEW committed synthetic note (relocated OUT of build-consumed `data/news/` by the approved spec)
- `docs/news-live.md`, `tests/smoke-checklist.md`, `CLAUDE.md` (T5 snapshot edit + T6 trim)

## Exit Criteria

- [x] Graph + dossier render in the LIVE region only (offline strip intact)
- [x] `GET /anchor` serves `anchor_summary` (honest null/404; graceful degrade without a store)
- [x] Conflicts surfaced presentation-only ("both kept", never auto-resolved)
- [x] Synthetic-note demo flow documented + the note committed (explicit SYNTHETIC label; `docs/demo-investigation-note.md`)
- [x] `python3 scripts/build.py --check all` 5/5 zero drift
- [x] node news-stream (130) + corpus (239) harnesses green; all selftests + news_live_test green (+`--live` real-Qwen smoke)
- [x] Replay fixtures untouched (no re-capture)
- [x] The always-on badge stays; NO non-negotiable change
- [x] CLAUDE.md ≤~220 lines with the non-negotiables intact (319 post-T5 → 220; protected sections diff-clean)

## Constraints

- LIVE-region-only client code: prevents offline `dist/news` drift (the strip invariant).
- Pure consumption — no gate/schema/prompt/store-write/fixture change: prevents a regate
  cascade and replay-fixture churn in a read-side phase.
- Conflicts presentation-only (both kept): prevents silent auto-resolution of identity
  conflicts (Phase-41 D2).
- Privacy: the seeded store stays local/gitignored; the committed note is SYNTHETIC + labeled;
  fixtures stay US-federal-only — prevents private/commercial data entering the repo.
- Deterministic SVG layout (no `Math.random`): keeps the render testable + reproducible.

## Checkpoints

- If offline `dist/news` cannot stay byte-identical after the live-region edits: STOP and surface.
- If `anchor_summary`'s read shape proves insufficient for the dossier render: surface the gap
  (a read-shape finding) — do not reshape store writes mid-phase.
- Blocked >3 attempts on a task: mark `[blocked: …]` + ask the user (skip or abort).

## Notes

- READY FOR COMPLETION (2026-06-10): all 6 tasks [x], full regate GREEN, reviewer 9/10 ACCEPT
  zero HIGH+. NOT auto-completed — the delivery gate is pending (status flips at the delivery
  flow, post-commit-verify). Journal: [[2026-06-10-phase-42-anchor-dossier-network-view]].
- Gate result (assumption gate closed 2026-06-10): A1 accept (offline byte-frozen), A3 accept
  (one integrated view), A2 don't-know → A2' accept (the evidence check refuted the
  re-scan-different-articles script — zero cross-article entity overlap → synthetic-note seed),
  A4 accept-WITH-CONDITION (SVG is the initial implementation for demo testing — revisit
  rendering tech past demo scale), A5 accept as scope constraint (pure consumption).
  Unresolved assumptions: none.
- Decisions D1–D5 (lite) recorded in `_CURRENT_STATE.md` Recent Decisions; the finalized
  decision article is `articles/decisions/phase-42-anchor-dossier-network-view.md`.
- PRECONDITION per the global enforce hooks: an approved spec via `/spec --internal` BEFORE any
  implementation edit.
- Ledger block appended to `assumption-ledger.md` (revisit at debrief).
