---
title: "Phase 43: Live pipeline robustness + progressive presentation (live news)"
aliases: [phase-43, live-pipeline-robustness]
category: phases
tags: [news-live, llm-transport, streaming, timeout, context-window, progressive-rendering, measure-first]
parents: []
created: 2026-06-10
updated: 2026-06-10
source: plan
status: active
scope: ["scripts/serve_news.py", "news.html", "tests/news_live_test.py", "tests/news-stream.test.mjs", ".dev-wiki/tmp/ph43_stress.py", "docs/news-live.md", "tests/smoke-checklist.md", "CLAUDE.md"]
entry_criteria: "Phase 42 delivered + accepted + committed (ecb2de7 work + 0527fed trim + 2ec4075 gate flip) + pushed to main; 0 open prior tasks; direction = user REFRAME at the dev-plan gate 2026-06-10 (a live test on a REAL investigation note timed out ~200s with no intermediate feedback); assumption gate closed 2026-06-10 (A1/A3/A4 accept, A2 reject-by-reframe→A2' accept)."
exit_criteria: "The ~200s failure class reproduced, named, and fixed or failing HONESTLY in-stream; call_llm streams internally (idle-gap timeout, token-count progress) with the SAME signature — 13/13 replay fixtures green, NO re-capture; stage-completion progressive rendering in the LIVE region only (NO visible token stream); pre-flight n_ctx check refuses honestly; offline dist/news byte-identical (--check all 5/5 zero drift); node news-stream + corpus green; all selftests + news_live_test (+ --live long-note probe) green; docs --ctx-size guidance + staged-rendering walkthrough; news_ground/SYSTEM_PROMPT/EXTRACT_SCHEMA/store-writes untouched; the always-on badge stays; NO non-negotiable change."
---

# Phase 43: Live pipeline robustness + progressive presentation (live news)

> **READY FOR COMPLETION (2026-06-10):** ALL 5 tasks T1–T5 [x]; every exit criterion met (ticked below); reviewer 9/10 ACCEPT (1 HIGH fixed inline); delivery gate pending — flips post-commit via the delivery flow. Journal: [[2026-06-10-phase-43-live-pipeline-robustness]].

## Objective

Make the live news extraction pipeline robust to article/note size + complexity and make its
progress VISIBLE: a live test on a REAL investigation note timed out at ~200s with no intermediate
feedback (the user's reframe at the dev-plan gate, off all five carried candidates).
Measure-first robustness (classify the failure before fixing) + stage-completion progressive
rendering (corpus-demo-style reveal — never a visible token stream).

Full rationale + alternatives: the finalized decision article
`articles/decisions/phase-43-live-pipeline-robustness.md` (do not re-derive).

## Approach

Code facts driving the plan: `call_llm` has a hard timeout=180 + max_tokens=4096 and is
NON-streaming (serve_news.py:197-224); `extract()` emits ONE "extracting" stage then blocks on the
single LLM call; the documented llama-server launch sets NO `--ctx-size` (default context may
silently overflow on long notes).

1. **T1 — Stress harness + failure classification (measure-first, D2)**: a LOCAL driver
   (`.dev-wiki/tmp/ph43_stress.py`, never committed to ship paths) generating SYNTHETIC
   investigation notes at size/complexity tiers (length × entity count × relationship density) +
   long commercial articles from the negative-news wiki (LOCAL-ONLY, Phase-40 D3 precedent), run
   through `extract()` against the live llama-server; per-stage wall-time, prompt/completion
   tokens, finish_reason, failure class; the server's real n_ctx queried via `/props`; the user's
   ~200s failure REPRODUCED + classified (read-timeout vs finish_reason=length truncation vs
   context overflow vs intrinsic model degradation).
2. **T2 — Streaming transport INSIDE call_llm**: stream:true SSE chunk reader; a per-chunk
   IDLE-gap timeout replaces the 180s whole-response deadline; the full text is accumulated and
   returned — SAME signature/return, so the 13 replay fixtures stay green with NO re-capture (the
   fixture seam). Token-count progress events flow through the existing Phase-39 NDJSON stage
   stream + a client elapsed/token counter. finish_reason=length → an honest in-stream error
   naming truncation; max_tokens raised per T1 findings.
3. **T3 — Stage-completion progressive rendering (D3, LIVE region only)**: the grounding-complete
   stream event carries the grounded record; the client reveals converted text → GROUNDED red
   flags + provisional entities corpus-demo-style (the gate has already disposed the flags; the
   verify loop is the measured wall-time majority) → the entity list refines live through
   verify i/N events → the final record swaps in at done. Honest staging labels (red flags
   grounded; entities provisional until verified). NO partial-JSON parsing, NO visible token
   stream.
4. **T4 — Size/complexity handling EARNED by T1**: pre-flight prompt-token estimate vs the
   server's reported n_ctx (honest in-stream refusal/warning instead of silent
   truncation/overflow); T1-earned limit changes; sectioned extraction (chunk → extract → merge →
   ground) ONLY IF measurement shows intrinsic degradation — and even then with NO prompt/schema
   change (section TEXT only). Re-run the T1 stress matrix.
5. **T5 — Full regate + docs**: `--check all` 5/5 zero drift; both node harnesses; all selftests +
   news_live_test (+ `--live` real-model smoke incl. one long-note probe); docs/news-live.md gains
   `--ctx-size` launch guidance + the staged-rendering walkthrough; smoke-checklist + CLAUDE.md
   `## Current state` updated IN PLACE.

## Scope

Files and modules affected:
- `scripts/serve_news.py` — call_llm transport + stage events + pre-flight check ONLY (SYSTEM_PROMPT/EXTRACT_SCHEMA frozen)
- `news.html` — the LIVE region only (staged reveal + elapsed/token counter); offline strip intact
- `tests/news_live_test.py`, `tests/news-stream.test.mjs`
- `.dev-wiki/tmp/ph43_stress.py` + `.dev-wiki/tmp/ph43-stress-results.md` — LOCAL scratch (never ship paths)
- `docs/news-live.md`, `tests/smoke-checklist.md`, `CLAUDE.md` (T5 in-place snapshot)

## Exit Criteria

- [x] The user's ~200s failure class reproduced, named (classification matrix in `.dev-wiki/tmp/ph43-stress-results.md`), and fixed or failing HONESTLY with an in-stream reason
- [x] call_llm streams internally (idle-gap timeout replaces the 180s deadline; token-count progress) with the SAME signature — 13/13 replay fixtures green, NO re-capture
- [x] A live long-generation probe survives >180s
- [x] Stage-completion progressive rendering in the LIVE region only (grounded red flags + provisional entities at grounding-complete, refined through verify, final at done; NO visible token stream); honest staging labels
- [x] Pre-flight token-vs-n_ctx check refuses/warns honestly; every T1 failing tier passes or fails HONESTLY with a named in-stream reason (re-run matrix recorded)
- [x] `python3 scripts/build.py --check all` 5/5 zero drift (offline dist/news byte-identical)
- [x] node news-stream (w/ new staged-reveal assertions) + corpus harnesses green; all selftests + news_live_test (+ `--live` long-note probe) green
- [x] docs/news-live.md `--ctx-size` launch guidance + staged-rendering walkthrough; smoke-checklist + CLAUDE.md in place
- [x] news_ground / SYSTEM_PROMPT / EXTRACT_SCHEMA / store writes / replay fixtures untouched; the always-on badge stays; NO non-negotiable change

## Constraints

- MEASURE-FIRST (D2): no fix lands before the failure is classified and the ~200s case
  reproduced — prevents fixing the wrong layer (timeout vs truncation vs overflow vs degradation).
- PURE TRANSPORT (D4): news_ground / SYSTEM_PROMPT / EXTRACT_SCHEMA / store writes FROZEN;
  call_llm signature preserved — prevents a regate cascade + replay-fixture re-capture; any
  prompt unfreeze is a surfaced FINDING, not drift.
- Stage-completion rendering only (D3): NO partial-JSON parsing, NO visible token stream —
  prevents showing ungrounded model output (the gate disposes before anything renders as a flag).
- LIVE-region-only client code: prevents offline `dist/news` drift (the strip invariant).
- PRIVACY (D5): the user's real note NEVER committed; stress notes SYNTHETIC; commercial captures
  LOCAL-ONLY; fixtures US-federal-only — prevents private/commercial data entering the repo.

## Checkpoints

- After T1: the failure-classification matrix is the earned basis for T4 — report it before
  building size/complexity handling.
- If stream:true proves incompatible with the json_schema strict grammar in the user's llama-cpp
  build: surface at T2 with the T1 evidence — don't hack around it.
- If offline `dist/news` cannot stay byte-identical after the live-region edits: STOP and surface.
- Blocked >3 attempts on a task: mark `[blocked: …]` + ask the user (skip or abort).

## Assumptions (gate summary, closed 2026-06-10)

- A1 ACCEPT — measure-first: classify before fixing; the ~200s failure must be reproduced.
- A2 REJECT-BY-REFRAME → A2' ACCEPT — round 1 (token-stream-flavored rendering) rejected; A2' =
  STAGE-COMPLETION-driven progressive rendering, corpus-demo-style; internal stream:true serves
  ONLY the timeout fix + an elapsed/token counter.
- A3 ACCEPT — streaming transport inside call_llm with the signature preserved (the fixture seam).
- A4 ACCEPT — pure-transport scope; sectioned extraction only if T1-earned, with no prompt/schema
  change. Unresolved assumptions: none.

## Notes

- PRECONDITION per the global enforce hooks (Phase 40/42 precedent): an approved spec via
  `/spec --internal` BEFORE any implementation edit — `specs/phase-43-live-pipeline-robustness.md`
  does NOT exist yet; creating + approving it is the first implementation step.
- Wiki knowledge carried in: Phase-39 established the NDJSON stage stream + that the per-entity
  verify loop is the wall-time majority (why grounding-complete is the right first reveal);
  Phase-41 D5 made red_flags-first schema order load-bearing (do not disturb generation order);
  Phase-40 D3 = the commercial-captures-local-only precedent.
- KNOWLEDGE GAPS (resolved at impl): the server's actual n_ctx (T1, via `/props`); whether
  stream:true composes with the json_schema strict grammar in the user's llama-cpp build (T2);
  the actual failure class (T1's whole job).
- Decisions D1–D5 (lite) recorded in `_CURRENT_STATE.md` Recent Decisions; the finalized decision
  article is `articles/decisions/phase-43-live-pipeline-robustness.md` (written at the gate).
- Ledger row appended to `assumption-ledger.md` at the gate (revisit at debrief).
