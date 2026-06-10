---
title: "Phase 42: Anchor dossier view + per-scan network visualizer (live news) — implemented, ready for completion"
aliases: [phase-42-journal]
category: journal
tags: [news-live, entity-resolution, anchor-dossier, network-graph, svg, duckdb-read, claude-md-trim]
parents: [phase-42-anchor-dossier-network-view]
created: 2026-06-10
updated: 2026-06-10
source: debrief
duration: unknown
---

# Phase 42: Anchor dossier view + per-scan network visualizer — implemented, READY FOR COMPLETION

## What Happened
- PURE CONSUMPTION of the Phase-41 ER model, all 6 lite tasks T1–T6 [x]; delivery gate pending (handled by the delivery flow after commit).
- T1 `GET /anchor` companion route (read-only, name-keyed) wrapping the previously-unconsumed `news_store.anchor_summary()`: 400 missing name · 503 store-off (mirrors /disposition) · 404 unknown/empty-normalizing · 200 JSON; `anchor_route_test` proves 2 same-article scans → ONE anchor with per-scan alias provenance.
- T2 SVG network visualizer at Disposition: `liveGraphLayout` (PURE deterministic data→positions — radial init + 24-iteration relaxation, self-edge skip, missing-endpoint synthesis) + string-built SVG with `esc()` everywhere; edge evidence quote CLOSED until clicked (spec-pinned, replaces the Phase-41 always-visible rows; harness asserts closed-then-revealed).
- T3 anchor dossier panel: `liveOpenDossier`/`liveDossierBody` — scans w/ source-type provenance, properties by kind, same-kind-multi-value conflicts flagged "conflicting values — both kept" (presentation-only), honest 404/store-off/empty states, watchlist `wdoss` affordance.
- T4 committed SYNTHETIC note `docs/demo-investigation-note.md` + `docs/news-live.md` "## Demo: anchor accumulation". SPEC CHECKPOINT ran LIVE (real Qwen, verify on): article 72.1s/14 entities + note 19.5s/4 entities → dossier showed 2 scans w/ source-type provenance, client_number C-2024-0117, phone conflict flagged both-kept, article alias+edges accumulated — the A2' payoff confirmed.
- T5 full regate GREEN + docs/smoke-checklist/CLAUDE.md in place; T6 CLAUDE.md trim 319(post-T5)→220 lines, non-negotiables/honesty/conventions DIFF-CLEAN (scripted section diff), the 73-line news-stream phase-changelog rewritten as a durable snapshot.
- No scope growth, no escape hatches; build.py/news_ground.py/store writes/fixtures untouched (reviewer-verified via git diff).

## Decisions Made (in-session, lite — no decision articles; planning D1–D5 already recorded)
- Evidence-on-click: the SVG edge's grounded evidence quote is CLOSED until clicked (spec-pinned; Phase-41 always-visible rows replaced).
- In-note conflict: the TGR article extraction yields NO properties[] (verified against the .ph41 golden) — an article-vs-note same-kind conflict was not honest; the synthetic note carries TWO phone values (an investigation-note reality) making the conflict deterministic, plus a location claim for a possible cross-scan conflict.
- /anchor route semantics: store-off = 503 (the /disposition convention); unknown/empty-normalizing name = honest 404; missing name = 400; name-keyed route (server-side name→anchor resolution is the merge-robust seam; payload carries anchor_id).
- CLAUDE.md two-commit plan: phase work commits with the post-T5 content (`.dev-wiki/tmp/ph42-claude-post-t5.md`), the trim commits separately from `.dev-wiki/tmp/ph42-claude-trimmed.md` (same-file changes can't be staged apart; snapshots are TEMP — never commit, delete after the trim commit).

## Health Delta
- node news-stream 103→130 (+27: strip, layout determinism/centrality/bounds/degenerates, XSS-escape, evidence click-reveal, dossier conflict/empty/404, wdoss); news_live_test +anchor_route_test +persist-off /anchor 503; all selftests green; `--check all` 5/5 ZERO DRIFT; `--live` real-Qwen smoke RAN.

## Assumption Revisit
- A1/A3/A5 held; A4 held with the condition recorded (SVG-initial; reviewer noted the min-gap wrap-around for the rendering revisit). A2 BIT in round 1 then held as A2' — the don't-know was the right position: the evidence check REFUTED the cross-article-overlap claim PRE-implementation; the revised synthetic-note seed CONFIRMED live. The bite was caught at planning, so the decision article's confidence needs no downgrade — flagged for the maintainer regardless.

## Open Questions
- None new. Carried: kind↔value semantic fit unguarded (Phase-41 residual); _CURRENT_STATE.md (158) + _ARCHITECTURE.md (161) over the 100-line cap (standing).

## Artifacts Changed
- `scripts/serve_news.py` (GET /anchor route + live_config "anchor" endpoint)
- `news.html` (LIVE region only: graph + dossier panel; offline strip intact)
- `docs/demo-investigation-note.md` (NEW, SYNTHETIC-labeled), `docs/news-live.md`, `tests/smoke-checklist.md`
- `tests/news_live_test.py`, `tests/news-stream.test.mjs` (103→130)
- `CLAUDE.md` (T5 in-place snapshot + T6 trim → 220 lines)

### Review Gate
- Unified reviewer 9/10 ACCEPT, zero HIGH+. 3 MEDIUMs: 2 pre-debrief staleness items resolved by this debrief; 1 stale `data/news/**` scope ref fixed inline by the orchestrator. Suggestions recorded.

### Gate Compliance
- gate-log:phase-42 `direction=approved delivery=pending` — compliant for pre-commit (delivery flips post-commit-verify, per gate-state-follows-git-state).

## Soft Observations / Phase 43 Candidates
- The live note scan emitted an `other`-label edge (George Rossi→TGR Group) alongside the article's owner-or-controller-of edge on the SAME pair — dossier-level edge display-dedup (same pair, multiple labels) is future polish; the store keeps all (correct).
- `liveGraphLayout`'s min-gap pass walks sorted angles forward-only: on a dense outer ring the last node can wrap past the first (reviewer note). Harmless ≤35 nodes; fold into the A4 rendering-tech revisit if the tool grows.
- Fuzzy-merge adjudication remains the named successor; the sanctions-screening wiki insight (identifier-layered matching) is now actionable via properties[].
- Negative-news bulk scan (2,313 articles) remains a candidate (wall-time design needed).
- FINTRAC /intel/ depth + AUSTRAC/UK third jurisdiction remain the corpus-scale candidates.
- Living-doc hygiene: _CURRENT_STATE.md (158) + _ARCHITECTURE.md (161) over the 100-line cap — a structural condensation pass is increasingly due.
- anchor_summary payload is now consumed — prior "unconsumed seam" notes are stale (already seeded to working-knowledge).

## Related
- [[phase-42-anchor-dossier-network-view|Phase 42: Anchor dossier view + per-scan network visualizer (live news)]] — parent phase
