---
title: "Phase 39: Live news QOL — streamed extraction progress + one-shot URL acquisition"
aliases: []
category: journal
tags: [news, live-mode, companion, streaming, ndjson, url-acquisition, fetch-ladder, qol]
parents: [phase-39-live-news-qol]
created: 2026-06-09
updated: 2026-06-09
source: debrief
duration: unknown
---

# Phase 39: Live news QOL — streamed progress + one-shot URL acquisition (M8)

## What Happened
- HEADLINE: one-shot URL acquisition + streamed stage-level extraction progress are LIVE against the real Qwen — measured end-to-end on treasury.gov jy2735: URL → fetch 0.4s → convert 14.4K chars → extract 34s → verify 16 entities (~0.5s each) → DONE 42.7s, 16 entities + 8 flags grounded, 0 dropped.
- T1: `/extract` is now ALWAYS an NDJSON stage stream (received → [fetching → converting] → extracting → grounding → verifying i/N → done). `extract()` gained `on_progress=None` — the Phase-38 replay fixtures pinned the same core with ZERO re-capture. Client = fetch+ReadableStream (`liveReadStream`/`liveStageLabel` + elapsed ticker).
- T2: NEW companion-only `scripts/news_fetch.py` — fetch ladder (urllib→curl→markitdown) + deterministic standardizer + article-shape verifier + `--selftest` over committed fixtures (`tests/fixtures/news-fetch/`). markitdown lazy/.venv-only with graceful degrade; build.py never imports it.
- T3/T4: `/extract` accepts {url} OR {text}; an early `converted` event fills the textarea (trim + re-run = the recovery path, honoring the gate's A1 accept-with-condition); news.html got a live-region URL field — dist/news BYTE-IDENTICAL (all inside the strip).
- T5: regate + docs/news-live.md (progress stream, URL mode + ladder + compliance posture: URL fetch local/dev-only, fetched text never committed/redistributed) + smoke-checklist + CLAUDE.md in place.

## Decisions Made (impl, recorded here per lite ceremony)
- D5 THE LADDER RULE — a rung wins ONLY by passing the article verifier; a "successful" fetch returning a guard page advances the ladder like a connection error. Pinned in `news_fetch --selftest`.
- D6 INTERSTITIAL TWO-STEP — urllib + curl rungs carry a cookie jar and follow at most ONE same-host meta-refresh (Akamai ak_bmsc dance); never cross-host; pages > 16KB never treated as interstitials.
- D7 STREAMING MECHANICS — BaseHTTPRequestHandler speaks HTTP/1.0 (body-until-close) so per-line write+flush streams with NO chunked framing; the planned job-id+polling fallback was NOT needed. 200 commits early → later failures travel IN-stream as {"error": …}; request-shape errors stay 400s; mid-stream BrokenPipe caught quietly.
- D8 PASTED TEXT WINS OVER URL when both are present — combined with the early `converted` event, this IS the one-shot flow's recovery path.

## Problems Solved
- justice.gov ladder pivot: the live run hit a 2.5KB Akamai interstitial that urllib "fetched" successfully but converted to 0 chars — the initial fetch-error-only ladder stopped there and failed. Fix = D5 (verifier advances the ladder) + D6 (cookie + one same-host meta-refresh: 2.5KB guard → 102KB real article, verified live).

## Artifacts Changed
- `scripts/serve_news.py` (NDJSON stage stream + on_progress + {url} path), `scripts/news_fetch.py` (NEW), `news.html` + `dist/news/index.html` (live region only — offline byte-identical), `tests/news_live_test.py` (read_extract_stream, url_route_test, in-stream errors, verify progress), `tests/news-stream.test.mjs` (81→90), `tests/fixtures/news-fetch/` (NEW, 5 committed fixtures), `docs/news-live.md`, `tests/smoke-checklist.md`, `CLAUDE.md`.

## Health Delta
- node news-stream 81→90 / corpus green; `news_fetch --selftest` NEW PASS (dep-free; +real markitdown under .venv); `--check all` 5/5 ZERO DRIFT; news_live_test PASS under system python3 + .venv + `--live` (real Qwen smoke: 2 entities, 4 flags grounded); news_ground/serve_news/news_store/derive_signals selftests PASS.
- Self-check (lite cat 1-2): cross-refs resolve; ONE finding — CLAUDE.md 269 lines (target ~200; was 255), the queued trim pass stands.

## Soft Observations / Phase N+1 Candidates
- **Red-flag extraction quality (USER-RAISED at the delivery gate — the LEAD Phase 40 candidate):** live red flags pass the faithfulness gate (verbatim flag quote-grounds; red_flag shape-checked distinct/12–240) but have NO structured prompt guidance (one dense sentence vs the entities' full subjects-only ruleset) and NO second-pass verify — completeness, span granularity, translation quality, and consistency are unguarded, and the user observes inconsistent/lower-quality flags in real tests. Accepted framing: measure-first — URL-mode stress corpus (now cheap) → characterize the failure modes → context-shape with few-shot flag→red_flag exemplars from the committed gate-passing news records + mechanism vocabulary (the corpus's transferable contribution; rf_region does NOT transfer — news has no enumerated list) → a keep-biased per-flag verify only if residue remains (Phase 38: keep-bias calibration is load-bearing).
- CLAUDE.md at 269 lines (target ~200) — the deferred trim pass is now more pressing | a Phase-N hygiene half-task, not a full phase | self-check finding above.
- The .gov header banner ("An official website…") survives standardization into the model input + grounding surface — harmless today (subjects-only prompt + grounding hold); Phase 38 warns an enumerated denylist overfits, but ONE structural rule (drop pre-H1 head matter?) might generalize | evidence: the live treasury.gov/justice.gov acquisitions this session.
- Verify-latency unchanged by design (A3): progress made the 42.7s wait LEGIBLE, not shorter | per-entity verify batching stays the deferred candidate.
- Replay-fixture corpus growth + a recorded fixture for the second-pass verify | carried from Phase 38, untouched.
- The negative-news wiki holds 2,313 raw articles with source_url frontmatter | ready-made batch material for URL-mode exercising or a bulk-scan/feed phase (the M8 "compose" north-star adjacency).

### Gate Compliance
- Direction gate: approved via the assumption-approval gate 2026-06-09 (ledger: A1 reject→revised→accept-with-condition; A2–A4 accept; all_accept: false).
- Delivery gate: PENDING at debrief time — flips post-commit per delivery-flow D3.
- Assumption revisit: A1 BIT (the accept-with-condition standardizer/verifier proved load-bearing — justice.gov interstitial + the 0-char conversion); A2 held (chunked flush worked, fallback unused); A3 held; A4 held (fixtures green w/o re-capture, dist byte-identical, zero drift). Suggest reviewing D3 (Phase 39 ACQUISITION) confidence in light of A1's bite — the condition VALIDATED the design (no downgrade indicated); maintainer decides.

## Related
- [[phase-39-live-news-qol|Phase 39: Live news QOL]] — parent phase
