---
title: "Phase 43: Live pipeline robustness + progressive presentation (live news) — implemented, ready for completion"
aliases: [phase-43-journal]
category: journal
tags: [news-live, llm-transport, streaming, timeout, context-window, progressive-rendering, measure-first]
parents: [phase-43-live-pipeline-robustness]
created: 2026-06-10
updated: 2026-06-10
source: debrief
duration: ~3.5 hours (plan + spec + implement + regate, same session)
---

# Phase 43: Live pipeline robustness + progressive presentation — implemented, ready for completion

## What Happened
- ALL 5 lite tasks T1–T5 [x] same-session (planned + implemented 2026-06-10) under the approved spec `specs/phase-43-live-pipeline-robustness.md` (nana:approved, internal mode, 8 adversarial constraints incorporated, Tier-1 reviewer 8/10→revised). Direction = the user's REFRAME at the dev-plan gate: a live test on a REAL investigation note timed out ~200s with NO intermediate feedback.
- T1 (measure-first): `.dev-wiki/tmp/ph43_stress.py` — deterministic tiered synthetic notes with HEAD/TAIL planted entities (the truncation-vs-degradation discriminator) + `ph43-stress-results.md`. VERDICT: primary failure = OUTPUT-BUDGET (extraction JSON ≈400–450 tokens/entity; 4096 truncates at ~10+ entities; finish_reason DISCARDED → opaque parse error ~103s — the user's failure class); secondary = READ-TIMEOUT (budget raised → XL 191s / XXL 321s exceed the 180s deadline); context overflow unreachable (n_ctx=262144, 4 slots); INTRINSIC DEGRADATION REFUTED (planted recall perfect at every tier). Probes: stream×json_schema composes; /tokenize available.
- T2 (streaming transport): call_llm STREAMS (SSE; `_consume_sse` socketless-testable); idle-gap 120s replaces the 180s deadline; MAX_GEN_TOKENS 4096→16384; finish_reason=length → named ExtractError; mid-stream TimeoutError → "model stalled" named; SAME signature → 13/13 replay fixtures green, ZERO re-capture; live XL probe completed at 193s with 116 token events.
- T3 (stage-completion rendering, LIVE region): "grounded" slim-record event (article_text excluded) + per-entity "verified" verdicts + "persisting" probe; `livePreviewBody` pure renderer (flags FINAL badge; provisional chips → checking/kept/dropped); token-counter label; verify projection (~Ns left est.); verified live — grounded reveal at 18s on the demo note.
- T4 (T1-earned size handling): `preflight_size` (assembled prompt vs /props n_ctx; ExtractError names the overage + the `--ctx-size` remedy; FAIL-OPEN); `/extract` single-flight (honest 409 — probe finding: slots=4 means ghost jobs run in PARALLEL splitting throughput, the likely contributor to the user's 200s profile); disconnect-before-done persists NOTHING (probe emit precedes append_scan; .venv test proves store row-count 0). Production-path re-run: ALL 5 tiers PASS, recall perfect (S 4/4 … XXL 35/35), zero UNHANDLED. Sectioned extraction NOT earned — skipped with measured reason.
- T5 (regate + docs): `--check all` 5/5 zero drift; corpus 239 + news-stream 140; all selftests; news_live_test system + .venv + --live; docs/news-live.md (`--ctx-size` guidance + "## Size robustness + staged rendering"); smoke-checklist Phase-43 item; CLAUDE.md in place (225 lines — +5 over the 220 soft target, durable facts not phase logs).

## Decisions Made
- D1–D5 recorded at planning ([[phase-43-live-pipeline-robustness|decision article]] + ledger): D1 direction (robustness + staged presentation); D2 measure-first; D3 stage-completion rendering (A2' reject-by-reframe round); D4 pure-transport scope; D5 privacy (synthetic stress notes; the real note never committed).
- Implementation-level: the "persisting" probe emit closes the disconnect-persist window STRUCTURALLY; idle-gap default 120s (measured first-chunk latency ≤~20s at XXL); preflight fail-OPEN; single-flight 409; named stall message (reviewer suggestion adopted).

## Problems Solved
- The opaque ~200s failure REPRODUCED + NAMED: discarded finish_reason turned output-budget truncation into a silent parse error that would have PASSED the gate — now failures travel in-stream with names (output-budget · pre-flight over-context w/ remedy · model stalled).
- Review gate: unified reviewer 9/10 ACCEPT. 1 HIGH (extract_lock leaked if the header write raises → header writes moved inside try/finally) + 3 MEDIUM (2 pre-debrief staleness — resolved by this debrief; dead except clause removed; test stub restore moved into finally) + 2 suggestions (named stall message ADOPTED; lock-release selftest assertion carried). All code findings fixed + re-verified green same session.

## Open Questions
- None new. Carried: living-doc hygiene debt compounding (tasks.md 415KB; _CURRENT_STATE 111/100; _ARCHITECTURE 163/100) — the deferred candidate, now also a self-check finding.

## Artifacts Changed
- `scripts/serve_news.py` (call_llm streaming transport, preflight_size, /extract single-flight, staged events) · `news.html` (LIVE preview panel only) · `tests/news_live_test.py` (+streaming_transport_test, +size_and_concurrency_test) · `tests/news-stream.test.mjs` (130→140) · `docs/news-live.md` · `tests/smoke-checklist.md` · `CLAUDE.md` · `specs/phase-43-live-pipeline-robustness.md` · `.dev-wiki/tmp/ph43_stress.py` + `ph43-stress-results.md` (LOCAL scratch, never committed to ship paths)

## Health Delta
- news-stream harness 130→140 (+10: strip pair, staged labels, preview n=0/1/large, XSS); news_live_test +2 functions (SSE reassembly, ExtractError length+stall, privacy sentinel, busy 409, disconnect-store, preflight fail-open); serve_news --selftest extended (transport invariants + token-counter label + MAX_GEN_TOKENS guard). All green. No escape hatches; no scope growth; gate/prompt/schema/store-writes/fixtures/news_fetch/build.py untouched (reviewer git-diff-verified); offline dist/news byte-identical.

## Assumption Revisit (ledger filled)
- A1 held (both limits-class causes reproduced; intrinsic degradation refuted) · A2' held (stage-completion rendering shipped exactly as revised, verified live) · A3 held (flags post-gate; entities provisional; "persisting" probe guarantees disconnect persists nothing) · A4 held (pure transport git-diff-verified; 13/13 zero re-capture; sectioned extraction not earned, not built). No late bites in prior-phase blocks (Phase 39 A3 "verify latency deferred" remains held — a soft observation, not a bite).

## Related
- [[phase-43-live-pipeline-robustness|Phase 43: Live pipeline robustness + progressive presentation (live news)]] — parent phase

### Retro Check (Phases 39–43, completed count 30)
| Dimension | Findings | Signal |
|-----------|----------|--------|
| 1. Recurring Blockers | 2 — living-doc hygiene debt named in 3+ debriefs (tasks.md 415KB chokes Read tooling); check-assumption-ledger.sh absent on this machine (2nd debrief running the manual fallback) | high |
| 2. Decision Reversals | 2 — measured rollbacks, not drift (Phase 40 r3 calibration rolled back on regression; Phase 38 denylist→context-shaping pivot); both evidence-driven by design | low |
| 3. User Corrections | 3+ — user REFRAMES at the dev-plan gate in Phases 41/42/43 (off offered candidates, toward real-tool quality gaps); Phase 41 T6 prompt-iteration-first ruling; Phase 43 A2 token-stream reject | high |

Recommendations: schedule the living-doc hygiene phase (strongest Phase-44 candidate — the debt now degrades tooling); at dev-plan gates, lead with an inspect-the-built-artifact assessment before offering candidates (the reframe pattern is consistent and already in memory).

## Soft Observations / Phase 44 Candidates
- The per-entity verify loop is again the wall-time MAJORITY for entity-rich docs now extraction streams (44 entities ≈ 40+ sequential calls); batched verify remains the named deferred candidate (Phase 39 A3 lineage). Evidence: the XL probe.
- The stress harness + tier generator could graduate to a committed perf/registry-scoring harness (Phase 40 residue adjacency) — currently local scratch.
- llama-server slot count silently DIVIDES context (n_ctx/slots per slot) — the preflight reads the reported per-slot value; docs could quantify the slots interaction further if multi-user use emerges.
- Hygiene debt (tasks.md 415KB chokes Read tooling) — a strong Phase-44 rider/standalone candidate.
