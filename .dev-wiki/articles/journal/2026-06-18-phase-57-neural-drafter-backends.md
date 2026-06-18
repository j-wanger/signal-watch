---
title: "Phase 57 — Live neural SAR/STR draft + pluggable drafter backends (claude · OpenAI /v1 · opencode)"
type: journal
date: 2026-06-18
phase: 57
tags: [chain-workbench, drafter-backends, openai-compatible, opencode, live-neural-sar, two-beat, cross-pillar, dev-time]
---

# Phase 57 — Live neural SAR/STR draft + pluggable drafter backends

## Summary

Made the Phase-56 chain workbench's "LIVE neural SAR/STR draft" real end-to-end and opened the drafter —
casework's pluggable `Drafter` Protocol — to multiple backends: `claude` (OAuth/key) · `openai` (any
OpenAI-standard `/v1` server, local models direct) · `opencode` (drive drafting **through** opencode's
agent loop) · `stub`. Two-beat, two-repo (the P55/P56 rhythm): **beat 1** (the signal-watch spine + the
re-grounded pin) delivered + verified this session; **beat 2** (the live openai/opencode runs) gated on
two casework adapter briefs authored here. Delivery gate **accepted** by the user.

## Direction (the gate)

The user picked the live-neural frontier and reframed to add **OpenAI-standard backend endpoint support**.
At the clarifying question, "opencode support" = **drive drafting through opencode's agent loop** (not a
model behind a raw `/v1` endpoint) — which **reframed A2** and **displaced the weakest assumption**: the
T0 risk became **A0 = opencode-agent-loop feasibility** (headless `serve` + SSE), not the /v1-adapter
cost. The user accepted all assumptions after seeing the reframe. all_accept: true.

## What changed (beat 1 — signal-watch-local)

- **`scripts/serve_chain.py`** — `drafter_for_env` (binary key→claude/stub) became an N-backend **name
  pass-through**: `BACKENDS`, `_BACKEND_ENV`, `backend_available`/`available_backends`/`default_backend`/
  `resolve_backend`. The browser sends a backend **name**; serve_chain resolves creds/endpoints
  **server-side** and passes `--drafter <name>` to the casework subprocess. Unknown/unavailable → honest
  stub fallback with a named note (never a silent neural→neural switch). `run_case` gained `env`; `_run`
  reads the browser `backend`. `live_config`/`_drafter_config` expose **names + booleans only** — the
  selftest asserts **no secret/endpoint leaks** into the served config/page (§4.5).
- **`chain.html`** — a backend **picker** (only available backends selectable; unavailable show disabled
  "n/a"), the live SAR/STR draft as a staged reveal, the **6-verifier + narrative-grounding verdict on the
  generated draft** ("the gate is the oracle"), honest requested→effective fallback, and a **stub-vs-neural
  comparison** (both narratives cached per case, each gated). `tests/chain.test.mjs` 31 → **46**.
- **Pin re-grounded `f0542b7 → 2381d71`** (`e2e_chain_check.GROUNDING_HEADS` + `data/pillar-status.json`
  regenerated via `--real`; launcher rebuilt — only `dist/index.html` moved, 7 dists byte-identical). The
  REAL chain CONNECTED against casework@2381d71 via the **stub** drafter (casework ingest @2381d71 → signed
  SAR signed:true / 0-blocking → `e2e_chain_check --real` CONNECTED).
- **`docs/chain-workbench.md`** rewritten Phase-56→57 (backend table, server-side-creds recipe, the
  two-beat reframe: consume-CLI + claude landed, openai + opencode gated); **smoke-checklist** Phase-57
  section added.

## What changed (beat 2 — sibling briefs, authored here)

- **`aml-casework/docs/openai-drafter-PLAN-BRIEF.md`** — a thin `/v1/chat/completions` adapter mirroring
  `ClaudeDrafter`; the one refactor = extract `_system_prompt`/`build_user_prompt`/`_DraftSchema` to a
  dep-light `drafter_prompts.py` so the openai adapter reuses the prompt without importing `anthropic`.
- **`aml-casework/docs/opencode-drafter-PLAN-BRIEF.md`** — the load-bearing leg: drive `opencode serve`
  (OpenAPI + SSE, async; provider key == llama-server `--alias`; avoid the bare-`opencode run` headless
  bug), agent output funnels into casework's `generate_narrative` (the 6 verifiers stay the oracle); A0 =
  headless-serve feasibility, with the `/v1` adapter as the named fallback.

Both briefs live in the casework working tree (untracked there); a casework-rooted session commits + builds
the adapters. Neither side imports the other (subprocess + file-handoff).

## The honest caveat

The live **neural** draft was **not run** this session — no anthropic creds in the env. The documented
fail-soft fired; the chain connected via the **stub**. The live `--drafter claude` (OAuth) path is
code-verified present (casework Phase 8) and drivable when a token/key is set; it is also covered by
casework `@integration`. Beat 2 (live openai/opencode) is gated on the casework adapters — the briefs are
specs, not the adapters.

## Health delta

`tests/chain.test.mjs` 31 → 46 (15 new assertions: picker, availability guard, backend POSTed, live-claude
label, requested→effective fallback note, stub-vs-neural comparison, XSS on a compared narrative).
serve_chain `--selftest` extended (N-backend availability + pass-through + no-leak + run-resolution).
`--check all` 8/8 zero drift (only `dist/index.html` moved with the pin). No regressions: gate-console 68,
triage 93, corpus, news 150, launcher 23, e2e/validate selftests green.

## Gate Compliance

Direction gate: approved (all_accept: true, A2 reframed at Q1 → A0 displaced as T0 weakest). Delivery gate:
accepted by the user (beat 1; beat 2 gated). Ledger Phase-57 revisit-status filled (A2 partial-bite: the
live-neural run was not exercised — no creds; A0/A1 deferred to the casework adapter sessions; A3/A4 held).

## Soft Observations / Phase N+1 Candidates

- **The two casework adapters are the natural next sibling work** — `drafter_openai.py` (cheap, the
  documented fallback) then `drafter_opencode.py` (the load-bearing agent-loop leg). Route to
  aml-casework-rooted sessions (the briefs are ready). Evidence: `aml-casework/docs/{openai,opencode}-drafter-PLAN-BRIEF.md`.
- **A live-neural-claude run from signal-watch is one creds-set away** — set `ANTHROPIC_AUTH_TOKEN`, run a
  case with `--drafter claude`, capture the real neural SAR gated by the verifiers; closes A2's untested
  "if false" branch. Evidence: serve_chain `drafter_for_env`/`resolve_backend`; casework Phase-8 OAuth.
- **The prompt-extraction refactor (`drafter_prompts.py`) is a shared casework prerequisite** for both
  adapters — sequence openai first so the refactor lands once. Evidence: both briefs cross-reference it.
