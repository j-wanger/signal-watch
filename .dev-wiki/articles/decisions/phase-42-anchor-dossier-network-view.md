---
title: "Phase 42: Anchor dossier + per-scan network visualizer (live news)"
type: decision
confidence: high
source: plan
created: 2026-06-10
updated: 2026-06-10
tags: [news-live, entity-resolution, anchors, visualization, duckdb]
---

# Phase 42 — Anchor dossier view + network visualizer

> Gate closed 2026-06-10: A1/A3 accept · A2 don't-know → evidence check refuted the
> cross-article-overlap seeding claim → A2' (synthetic investigation note + same-article
> re-scan) accepted · A4 accept-with-condition (SVG = initial implementation for demo
> testing; revisit rendering tech if the live tool grows) · A5 recorded as a scope
> constraint (pure consumption, agent-verified infrastructure). Ledger block appended.

## Direction (user-set at the dev-plan gate, 2026-06-10)

User picked, off the offered candidates: **anchor dossier view PLUS a network visualizer
for the extracted article**, with the CLAUDE.md trim (305 → ~200) bundled as a hygiene
half-task. This continues the live-layer-is-becoming-a-real-tool trajectory (Phase 41
reveal): consume the Phase-41 data model (anchors / properties / relationship edges)
instead of extending it.

## Proposed approach (draft — pending assumption gate)

**One integrated view, graph as the navigation surface:**

1. **Per-scan network visualizer** (LIVE region of news.html): nodes = the scan's
   entities (main subjects highlighted), edges = `relationships[]` with labels;
   edge click → evidence quote. Vanilla SVG, deterministic layout (radial initial
   placement + fixed-iteration relaxation — no Math.random, no vendored lib).
   Replaces/upgrades the Phase-41 text subject-map panel at Disposition.
2. **Anchor dossier** as node detail: clicking a graph node (or a watchlist row)
   fetches `GET /anchor?name=` — a NEW companion route wrapping the UNCONSUMED
   `news_store.anchor_summary()` — and renders the accumulated identity: scans
   touched, properties grouped by kind WITH per-scan provenance, **conflicts
   surfaced presentation-only** (same kind, >1 distinct value → flagged, both kept,
   never auto-resolved — Phase-41 D2), relationship edges.
3. **Pure consumption phase:** no change to news_ground (the shared gate),
   EXTRACT_SCHEMA, SYSTEM_PROMPT, build.py, or the replay fixtures. Read-side +
   UI only. Offline dist/news stays byte-frozen (all new code inside
   /*LIVE_START*/…/*LIVE_END*/).
4. **Demo seeding:** the dossier's payoff (accumulation, conflicts) needs
   overlapping scans — documented demo script (scan the 3 .ph41 fixture articles,
   which share entities); no committed seed data (privacy boundary unchanged).
5. **CLAUDE.md trim:** replace-in-place to ~200 lines, narrative → journal/HANDOFF,
   non-negotiables verbatim.

## Assumptions (to be positioned at the gate)

- A1 (weakest): demo payoff requires a seeded multi-scan store; a demo script is
  enough (vs committing seed data or auto-seeding).
- A2: visualization is LIVE-region-only; offline dist/news + the 4 committed
  records stay byte-frozen (no offline network view this phase).
- A3: graph-as-navigation integrated shape (node click → dossier) over two
  disjoint panels.
- A4: vanilla SVG + deterministic layout, no vendored graph library.
- A5: pure consumption — no gate/schema/prompt/store-write changes; fixtures
  untouched, no re-capture.
