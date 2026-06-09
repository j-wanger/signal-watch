---
title: "Phase 39: Live news QOL — streamed extraction progress + one-shot URL acquisition"
aliases: [phase-39]
category: phases
tags: [news, live-mode, companion, qol, ux, url-input, markitdown, streaming, ndjson]
parents: [phase-38-consolidate-live-news]
created: 2026-06-09
updated: 2026-06-09
source: plan
status: active
scope: ["news.html", "scripts/serve_news.py", "scripts/news_fetch.py", "tests/news_live_test.py", "tests/news-stream.test.mjs", "tests/fixtures/news-fetch/**", "docs/news-live.md", "dist/news/index.html", "tests/smoke-checklist.md", "CLAUDE.md"]
entry_criteria: "Phase 38 delivered + accepted + committed 7df3ce4/f27f99b + pushed; the live companion (serve_news.py) + the strip invariant + the recorded-fixture replay harness exist."
exit_criteria: "Streamed stage-level progress live in the companion (or documented job-id+polling fallback); one-shot URL acquisition through the news_fetch ladder + standardizer + verifier with honest failure → paste fallback; offline dist/news byte-identical; --check all zero drift; all harnesses + selftests green (incl. the new news_fetch --selftest); replay fixtures green without re-capture; build.py never imports the live layer; NO non-negotiable change."
---

# Phase 39: Live news QOL — streamed extraction progress + one-shot URL acquisition

## Objective

QOL upgrade for the LIVE news subsystem (companion-served, dev/authoring-time only). Two halves
(approach approved at the assumption gate 2026-06-09; ledger row appended):

1. **PROGRESS** — `POST /extract` becomes a chunked NDJSON stream of stage events
   (received → [fetching → converting] → extracting → grounding → verifying i/N → done {payload}).
   `serve_news.extract()` gains an optional `on_progress=None` callback so the Phase-38
   replay-fixture seam (call_llm stubbing, deterministic `build_record`) is untouched. The client
   reads via fetch+ReadableStream and renders stage label + verify i/N + elapsed timer in the live
   region. NO token streaming (raw JSON isn't user-meaningful + misses the per-entity verify loop,
   the wall-time majority). Fallback if stdlib chunked flush misbehaves under ThreadingHTTPServer:
   job-id + polling (verify at impl; record it if taken).
2. **URL ACQUISITION (ONE-SHOT** — the user rejected preview-then-run) — `/extract` accepts
   `{url}` OR `{text}`. A NEW companion-only module `scripts/news_fetch.py` owns acquisition: a
   multi-method fetch LADDER (urllib with browser-like headers → curl subprocess → markitdown
   `convert(url)`; bot guards expected) + a deterministic format STANDARDIZER (strip
   nav/link-list/image boilerplate from converted markdown, collapse whitespace) + a VERIFIER gate
   (article-shape checks: min prose length/ratio, bot-guard/captcha/paywall/JS-wall detection →
   honest structured failure suggesting paste). markitdown stays `.venv`-only via lazy import +
   graceful degrade (the news_store/DuckDB pattern). The converted text is streamed back in an
   early event and fills the textarea as extraction runs — passive recovery: the user can trim +
   re-run. Acquisition PROPOSES, the scripted gate DISPOSES (the project spine, applied to fetch).

## Scope

Files and modules affected:
- `scripts/serve_news.py` — NDJSON stage streaming + `extract(on_progress=None)` + the {url} route path
- `scripts/news_fetch.py` — NEW companion-only acquisition module (ladder + standardizer + verifier + `--selftest`)
- `news.html` — live region ONLY (`/*LIVE_START*/…/*LIVE_END*/`): progress UI + URL input
- `tests/news_live_test.py`, `tests/news-stream.test.mjs`, `tests/fixtures/news-fetch/**` — harness coverage (committed HTML fixtures, no network)
- `docs/news-live.md`, `tests/smoke-checklist.md`, `CLAUDE.md` (in-place `## Current state`) — docs
- `dist/news/index.html` — rebuilt, byte-identical via the strip

## Tasks

5 lite tasks T1–T5 (no L) — see `tasks.md`: T1 streamed stage-level progress · T2 news_fetch.py
ladder/standardizer/verifier + selftest · T3 wire {url} into /extract · T4 news.html URL input +
progress UI integration · T5 regate + docs (incl. the URL-mode compliance posture note).

## Exit Criteria

- [ ] Streamed stage-level progress live in the companion (chunked NDJSON over `POST /extract`,
      fetch+ReadableStream client) — OR the documented job-id+polling fallback
- [ ] One-shot URL acquisition through the news_fetch ladder + standardizer + verifier; honest
      structured failure → paste fallback; early converted-text event fills the textarea
- [ ] Replay fixtures green WITHOUT re-capture (`extract(on_progress=None)` preserves the seam)
- [ ] Offline `dist/news` byte-identical (`--check news` / `--check all` zero drift)
- [ ] `node tests/news-stream.test.mjs` + `node tests/corpus-explorer.test.mjs` +
      `python3 tests/news_live_test.py` + news_fetch/news_ground/serve_news/news_store `--selftest` green
- [ ] build.py never imports the live layer (news_fetch companion-only); markitdown stays off the ship path
- [ ] NO non-negotiable change; the always-on badge stays

## Constraints

- All new client code inside `/*LIVE_START*/…/*LIVE_END*/` — prevents offline dist/news drift
  (the strip + the `die("fetch(")` self-contained guard must hold).
- markitdown is `.venv`-only — the news_store graceful-degrade precedent (lazy import, feature
  disabled with an honest warning when absent); never a build.py/ship dependency.
- The grounding spine is untouched: whatever converted text becomes `article_text` is BOTH the
  model input and the grounding surface; the gate still disposes.
- Compliance (T5 docs note): URL fetch is local/dev-only; fetched text is never committed or
  redistributed; public/US-federal posture for anything promoted to fixtures — not a
  non-negotiable change.
- Abort rule: chunked streaming unworkable even after the polling fallback → surface it; a fetch
  ladder that can't pass the verifier on real targets is an HONEST FAILURE (paste fallback), NOT a
  reason to loosen the verifier; blocked >3 attempts → mark [blocked: …] + ask skip/abort.

## Notes

Decisions D1–D4 (2026-06-09, recorded in `_CURRENT_STATE.md → Recent Decisions`): D1 user-set
direction (fix no-feedback UX + URL input, live subsystem only) · D2 progress architecture
(stage-level chunked NDJSON; token streaming + client-only spinner rejected; polling fallback;
`on_progress=None` seam) · D3 one-shot acquisition (ladder + standardizer + verifier; converted
text fills textarea; markitdown lazy degrade) · D4 invariants carry forward (strip/byte-identical,
build.py never imports live, fixture seam, badge).

Knowledge gaps to verify at impl: exact markitdown 0.1.6 in-memory HTML API (`convert_stream` vs
`convert(url)`) under `.venv`; BaseHTTPRequestHandler chunked-flush behavior under
ThreadingHTTPServer (T1 carries the polling fallback). Wiki pointers: SSE/chunked HTTP is the
standard fit for unidirectional progress (EventSource is GET-only → fetch+ReadableStream for
POST); the negative-news wiki holds 2,313 raw article files with `source_url` frontmatter —
ready-made URL-mode test material.
