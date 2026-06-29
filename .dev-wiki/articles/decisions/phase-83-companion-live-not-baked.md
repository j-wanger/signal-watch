---
title: "Phase 83: the served surface is a companion live mode, NOT a baked static replay"
aliases: [phase-83-companion-live, merge-adjudicator-served-surface, 5th-live-loop]
category: decisions
tags: [agentification, merge, dist-boundary, live-mode, build-strip, firewall]
parents: [phase-83-merge-adjudicator-oracle-scored]
created: 2026-06-29
updated: 2026-06-29
source: implementation
confidence: high
---

## Context

The merge adjudicator needs a served surface so the agent's proposal sits beside the human gate and
the post-disposition oracle. Two designs: (A) a companion live mode — a new `scripts/serve_merge.py`
plus a build-stripped `/*LIVE_START*/.../*LIVE_END*/` overlay in `merge.html` (the corpus/news live
pattern); or (B) bake a static pinned agent replay into the offline `dist/merge` ship file. The
non-negotiable: all 9 ship dists stay BYTE-FROZEN, and the offline file makes NO model call (§4.5).

## Decision

Design (A) — the companion live mode. `serve_merge.py` (stdlib, 127.0.0.1, the `serve_corpus.py`
pattern) serves `merge.html` and proxies the adjudicator (StubAdjudicator offline / LiveAdjudicator on
:8080); the LIVE overlay is wrapped in `/*LIVE_START*/.../*LIVE_END*/` and build-stripped, so
`dist/merge` is byte-identical via `--check merge` after the strip. This matches the agentification
roadmap's companion-only mandate and the 4 existing live loops, keeps all 9 dists byte-frozen, is
§4.5-clean, and is demoable both offline (stub) and live (agent).

Rejected: design (B) baking a static replay — it re-freezes `dist/merge` (a sanctioned dist change we
do not need), and a static second-rater replay is NOT a live agent loop (it cannot show the agent
proposing under a live model, which is the whole point of "the 5th live loop").

## Consequences

- `build.py` strip coverage extends to the `merge` target; `--check merge` is the byte-identity guard.
- `build.py` imports NO `serve_merge` / `merge_adjudicator` / scorer / spine / curate / casework (grep
  guard) — the companion layer never crosses into the build.
- The oracle firewall is enforced on the served path: `/adjudicate` carries no oracle pre-disposition;
  the overlay sends the oracle to the client only post-disposition (same as the static page).
- Offline `dist/merge` is unchanged — the static console keeps screening the committed book; live mode
  is the dev/authoring-time companion only.
- **OUTCOME (implemented 2026-06-29):** `serve_merge.py` (port 8040) + the build-stripped `/*LIVE_*/`
  overlay landed; `dist/merge` byte-identical via `--check merge` (a +1-newline drift caught + fixed —
  see [[phase-83-live-region-newline-discipline]]); the overlay installs by wrapping `render()`
  in-region ([[phase-83-live-overlay-via-render-wrap]]); build.py imports nothing new; all 9 dists
  byte-frozen. Design (A) held in full; confidence → high.
