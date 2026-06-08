---
date: 2026-06-08
phase: 35
title: News live local-model backend (M8) + CLAUDE.md trim
tags: [m8, news, live-mode, llama-cpp, companion, grounding, claude-md, hygiene]
mode: full
ceremony: lite
---

# Phase 35 — News live local-model backend (M8)

## What shipped
Hooked the M8 adverse-media news stream to a REAL local llama-cpp backend for real-time, on-demand
extraction — the "live mode" the non-negotiable already sanctioned (optional, isolated, off by default,
scripted fallback). Built as a **same-origin companion**, so the offline `dist/news` is untouched.

- **T1** `scripts/serve_news.py` — stdlib `ThreadingHTTPServer` companion: serves `news.html` over
  http://localhost (seed NEWS + a `live` config) + `/health` + `/extract`. Reuses `build.load_news`.
- **T2** `scripts/news_ground.py` — the news grounding gate factored out (stdlib: `news_normalize`,
  `article_body`, `ground_record` in DROP mode). `build.py`'s news gate now imports it → live grounding
  == build grounding by construction. dist/news byte-identical (behavior-preserving refactor).
- **T3** (L) live `/extract` — model output JSON-schema-constrained → `parse_llm_json` (strips `<think>`/
  fences) → `build_record` (assemble + assign E#/R# ids) → `news_ground.ground_record` DROPS ungrounded.
  `call_llm` (llama-cpp via urllib) is isolated so the pipeline tests with no model.
- **T4** `news.html` live branch in a `/*LIVE_START*/…/*LIVE_END*/` region + `render_news` STRIPS it for
  the offline build → **dist/news byte-identical** (zero network code offline; the self-contained guard
  holds). The companion serves the region whole (74.5KB vs 70KB offline).
- **T5** `docs/news-live.md` + smoke-checklist live section + CLAUDE.md `## Current state` refreshed
  **in place** (no per-phase bullet — per the new maintenance contract).

## Architecture decisions (the 3 direction-gate choices)
1. Served-by-companion (same-origin, no CORS) over a file://→localhost toggle.
2. DuckDB→parquet store + feedback watchlist — DEFERRED to Phase 36.
3. Feedback watchlist (book ∪ prior-scanned) — Phase 36.
Plus a mid-flight REVISION: grounding stays in **Python server-side** (shared `news_ground.py`), NOT
re-ported to JS — the companion choice made server-side grounding the clean, DRY answer.

## Honesty
The "LLM proposes, the deterministic gate disposes" spine, moved to runtime. Schema-constrained →
server-side grounded (ungrounded entities/attributes/flags drop); if nothing grounds, `/extract` returns
an honest error, never an empty/fabricated record. Real client-side fuzzy scores; synthetic book;
always-on badge stays. Zero new pip deps (stdlib + urllib).

## Side task — CLAUDE.md trim (pre-phase)
CLAUDE.md had bloated to **689 lines / 74KB** — an append-only per-phase changelog in `## Current state`
(459 lines) + `## Milestones` (100). Root cause: **no automated writer** (no AGENTS.md/sync hook here; and
`/dev-debrief`'s refresh only ever rewrites four MACHINE sections this file doesn't have) — the bloat was
the implementing agent appending a phase bullet by hand each phase, a snapshot-section maintained as a log.
Fix: distilled to **208 lines** of durable architecture + added a **maintenance contract** at the top of
`## Current state` (snapshot/replace-in-place, never append; per-phase narrative → git/.dev-wiki/HANDOFF).
Non-negotiables / Knowledge-wiki / Aesthetic / Definition-of-done kept byte-identical.

## Verification
`--check all` 5/5 ZERO DRIFT (all dists byte-identical incl. dist/news) · `derive_signals --selftest` PASS ·
corpus harness 235/0 · news harness 67/0 (65 + 2 strip-invariant asserts) · `tests/news_live_test.py`
(build_record + grounding + the `/extract` route over HTTP with a stubbed model) PASS · gate + companion
selftests PASS. Frozen set byte-clean (git-confirmed): showcase (index.html + config/** + 3 typology dists),
the ENTIRE corpus (corpus.html + dist/corpus + all source dirs + every derived record + the 2 overlays),
`derive_signals.py`, and `dist/news/index.html`. NO non-negotiable change.

## Open / caveats
- The REAL model integration (`call_llm` against an actual llama-cpp server) is **unverified** — exercised
  only with a stubbed model. First-run smoke is the user's. The grounding gate is the backstop regardless.

## Soft Observations / Phase N+1 Candidates
- **Phase 36 (queued):** persistence — companion → DuckDB row-append → parquet export — + the feedback
  watchlist (book ∪ all prior-scanned entities; the screen surface compounds). DuckDB is the one new dep.
- A "reading…" affordance during the (blocking) model call, or SSE streaming of `/extract`, would make the
  live wait feel like the scripted streaming Read.
- The CLAUDE.md maintenance contract now guards re-bloat — future debriefs must honor snapshot-not-log.
- Extending live mode to the corpus/showcase is possible but out of scope (news was the clean seam).
