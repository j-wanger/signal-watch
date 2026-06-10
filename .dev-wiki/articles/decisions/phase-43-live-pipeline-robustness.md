---
title: "Phase 43: Live pipeline robustness + progressive presentation"
aliases: [phase-43-direction, live-extract-streaming]
category: decisions
tags: [live-news, serve-news, streaming, robustness, ux, measure-first]
parents: [phase-43-live-pipeline-robustness]
created: 2026-06-10
updated: 2026-06-10
source: plan
confidence: low
---

## Context

User REFRAME at the Phase-43 dev-plan gate (off the offered candidates: fuzzy-merge, bulk scan,
FINTRAC /intel/, AUSTRAC/UK, hygiene). A live test of the news pipeline on a REAL investigation
note failed: the Qwen backend timed out (~200s, "local agent extracting" the whole time, then the
failure message). Two reported weaknesses: (1) robustness — extraction must work regardless of
article size/complexity; (2) presentation — no intermediate feedback during the long monolithic
extract call; rendering should begin after the red-flags or entities pass.

Code facts established at planning: `call_llm` has a hard `timeout=180` + `max_tokens=4096`,
non-streaming (`serve_news.py:197-224`); `extract()` emits ONE "extracting" stage event then blocks
on the single LLM call (`serve_news.py:392-406`); the per-entity progress only exists in the verify
loop; the documented llama-server launch command (`docs/news-live.md`) sets NO `--ctx-size` —
llama-server's default context is small, so a long note + the large SYSTEM_PROMPT may silently
overflow context.

## Decision

Phase 43 = live pipeline robustness + progressive presentation, MEASURE-FIRST:

1. Stress harness over synthetic investigation notes at size/complexity tiers (+ long commercial
   articles, local-only) — classify the failure: read-timeout vs max_tokens truncation
   (finish_reason=length) vs context overflow (llama-cpp /props n_ctx) vs intrinsic model
   degradation. Reproduce the user's failure class before fixing.
2. Streaming transport inside `call_llm` (llama-cpp `stream:true`): per-chunk idle timeout replaces
   the whole-response 180s deadline; token-count progress events feed the existing Phase-39 NDJSON
   stage stream. Signature/return preserved (full text) → replay fixtures green, NO re-capture.
3. Progressive rendering: strict-grammar generation order = schema order (red_flags FIRST, Phase-41
   D5) → incremental partial-JSON parse emits red flags, then entities, as their arrays close;
   client renders them as an HONESTLY-LABELED ungrounded preview ("preview — pending grounding");
   the grounded record remains the only final/persisted output.
4. Size/complexity handling EARNED by measurement: pre-flight token estimate vs the server's
   reported n_ctx (honest refusal/warning instead of silent truncation); finish_reason=length
   detection with an honest in-stream error; sectioned extraction (chunk→extract→merge→ground) only
   IF measurement shows intrinsic degradation (the Phase-40 deferred trigger; Phase-41 D5's
   designed fallback).
5. Full regate + docs (incl. the `--ctx-size` launch guidance in docs/news-live.md).

Alternatives considered: staged two-pass extraction as the DEFAULT (rejected unless earned — regates
prompt/fixtures, Phase-41 D5 ruled prompt-iteration-first); client-only spinner polish (rejected —
no stage truth, the Phase-39 reasoning).

## Consequences

- news_ground / SYSTEM_PROMPT / EXTRACT_SCHEMA / store writes stay FROZEN; all client changes in
  the LIVE region; offline dist/news byte-identical; fixtures US-federal-only; the user's real note
  never committed (stress notes SYNTHETIC).
- If measurement contradicts the limits-class hypothesis, T4's sectioned-extraction path activates
  as a surfaced finding (prompt/schema unfreeze would be a NEW gate, not silent drift).
- Hygiene (tasks.md 415KB, _CURRENT_STATE/_ARCHITECTURE over cap) carries again — debt noted.
