---
title: "Phase 57 — Live neural SAR/STR draft + pluggable drafter backends (claude · OpenAI /v1 · opencode)"
type: phase
status: completed
ceremony: lite
milestone: M9
created: 2026-06-18
updated: 2026-06-18
tags: [cross-pillar, chain-workbench, live-neural-sar, drafter-backends, openai-compatible, opencode, local-model, two-beat, companion-server, dev-time]
---

# Phase 57 — Live neural SAR/STR draft + pluggable drafter backends

## Objective

Make the Phase-56 chain workbench's headline promise — a **LIVE neural SAR/STR draft** — actually true
end-to-end from signal-watch (today it only ever runs the *stub*; the neural path was deferred to
"@integration"), AND open the neural drafter to **multiple backends**: Anthropic (claude, OAuth
subscription) · an **OpenAI-standard `/v1` endpoint** (local models direct) · **opencode** (drive
drafting *through* opencode's agent loop). The drafter is casework's pluggable `Drafter` Protocol
boundary; the **gate stays the oracle** — whatever any backend emits, casework's 6 Class-G verifiers +
`narrative_grounding` dispose.

## Direction (gated 2026-06-18)

The user picked the **live neural draft** frontier and reframed to add **OpenAI-standard backend
endpoint support** (enabling local models + opencode). On the follow-up, "opencode support" = **drive
drafting through opencode** (its agent loop), NOT merely a model behind a /v1 endpoint. So beat 2 carries
**two** casework adapters: a thin `/v1` adapter and the meatier opencode-agent-loop adapter.

Sibling state code-verified this session: **aml-casework@2381d71** (two commits past the held pin
`f0542b7`) — Phase 7 = the consume CLI (`python -m aml_casework.ingest <bundle> --out <signed>
--drafter stub|claude`); **Phase 8 = `ClaudeDrafter` wired for OAuth** (`ANTHROPIC_AUTH_TOKEN` + the
`oauth-2025-04-20` beta header). The drafter is a pluggable Protocol (`narrative_generator.generate_narrative(bundle,
drafter)`); two adapters exist (`drafter_claude.ClaudeDrafter`, `drafter_stub.DeterministicDrafter`); **no**
OpenAI/opencode adapter exists.

## Approach (two-beat, two-repo — the P55/P56 rhythm)

**Beat 1 — signal-watch spine (drivable now):**
- `serve_chain.py` drafter selection becomes a **backend-name pass-through** `{stub, claude, openai,
  opencode}` — each backend's creds/endpoint resolved from **server-side env** (anthropic OAuth /
  `OPENAI_BASE_URL`+key+model / opencode serve URL+model); the browser sends a backend **name only**;
  serve_chain passes `--drafter <name>` + the matched env to the casework subprocess; honest
  requested-vs-effective (fail-soft). The selftest **stubs every backend** offline — so the spine is
  provable regardless of which sibling adapters exist yet.
- `chain.html` gains a **backend picker** + renders the live neural SAR/STR draft as a staged reveal +
  the **verifier/grounding verdict on the generated narrative** + `drafter_effective` honesty +
  a stub-vs-neural comparison.
- **Run the live `--drafter claude` (OAuth) draft end-to-end** (it's drivable now — casework already has
  it), or document the honest fail-soft if OAuth isn't headless-available.

**Beat 2 — gated on casework (briefs authored here):**
- `drafter_openai.py` + `--drafter openai` — a thin `/v1/chat/completions` adapter (local models direct),
  mirroring `drafter_claude.py`.
- `drafter_opencode.py` + `--drafter opencode` — drives `opencode serve` (OpenAPI 3.1 + SSE, async
  POST→poll; local model via opencode's `@ai-sdk/openai-compatible` provider, model key == llama-server
  `--alias`; avoid the bare-`opencode run` headless-permission bug). Output funnels into casework's
  grounding-aware generate loop. **This is the load-bearing leg.**

serve_chain's `openai`/`opencode` *selection* + the picker + the selftest-stub are all built in beat 1
(the spine is backend-agnostic); only the **real local/opencode runs** are gated on the sibling adapters.

## Scope

- `scripts/serve_chain.py` · `chain.html` · `tests/{chain.test.mjs, serve_chain selftest}` ·
  `docs/chain-workbench.md` · `tests/smoke-checklist.md` · `data/chain-cases/**` (manifest pin re-ground only)
- `aml-casework/docs/{openai-drafter,opencode-drafter}-PLAN-BRIEF.md` (authored here, executed in casework sessions)
- NOT touched: the 8 build targets / offline dists; `build.py` never imports the companion; no sibling import.

## Exit criteria (the SPINE — beat 1 / signal-watch-local)

1. `serve_chain.py` — `--selftest` green OFFLINE with every backend STUBBED (name→server-side-env mapping;
   browser sends name only; fail-soft requested-vs-effective; NO creds in the rendered config payload;
   unknown/unavailable backend → honest gated/stub); no sibling import; build.py clean of it.
2. `chain.html` — `node tests/chain.test.mjs` green (backend picker; live-draft staged reveal; the gate
   verdict on the generated narrative; `drafter_effective` honesty; stub-vs-neural comparison; badge;
   XSS-escape; NDJSON line-split).
3. The casework pin re-grounded to the current HEAD; the **live `--drafter claude` (OAuth) draft** rendered
   + gated (or the honest documented fail-soft — selftest-proven either way).
4. Both sibling briefs written (`drafter_openai`, `drafter_opencode`) with code-verified facts + the shared
   acceptance.
5. `docs/chain-workbench.md` + smoke-checklist updated; `chain.html` NOT a build target; `--check all` 8/8.

## Delivery gate (the live local/opencode beat — GATED on casework)

The live local-model + opencode drafts close when the casework `drafter_openai.py` / `drafter_opencode.py`
adapters land (casework-rooted sessions) + serve_chain drives them. Two-beat, like P55/P56: the spine +
live-claude are provable now; the live local/opencode demos are gated on the sibling adapters.

## Assumptions (ledger: Phase-57 block, all_accept: true — A2 reframed)

- **A0 [HIGH, T0 weakest]** Driving drafting THROUGH opencode is feasible + boundable from casework (headless
  `opencode serve` + SSE async POST→poll; local model via the openai-compatible provider; the agent loop
  reliably emits a verifier-groundable narrative). ACCEPT. Defended by the working-knowledge Phase-46
  practitioner notes (the exact pattern is documented); mitigated by the backend-agnostic spine (selftest
  stubs it) + the `/v1` adapter as the simpler local-model fallback. If false → the opencode leg blocks; the
  /v1 adapter still delivers "local model support."
- **A1 [HIGH]** The `/v1` OpenAI-standard adapter is cheap — a thin adapter mirroring `ClaudeDrafter` (the
  Drafter Protocol is the explicit pluggable seam; `drafter_stub` proves a 2nd adapter slots in). ACCEPT.
- **A2 [HIGH]** The live claude draft is drivable now from signal-watch, no sibling change (casework@2381d71
  has `--drafter claude` + OAuth-aware `ClaudeDrafter`). ACCEPT (code-verified). If false (OAuth not
  headless / rate-limited) → beat-1 live run degrades to the documented fail-soft stub.
- **A3 [HIGH]** Boundary held — serve_chain selects backend by NAME + passes creds/endpoints via SERVER-SIDE
  env to the casework subprocess (no creds in chain.html); subprocess + file handoff only (no sibling
  import); chain.html stays a non-build-target dev companion; dists byte-frozen, `--check all` 8/8. ACCEPT.
- **A4 [MED]** Two-beat — the spine + live-claude now; the live openai/opencode runs gated on casework. ACCEPT.

## Abort

`chain.html` becomes a build target, or any of the 8 offline dists drift → STOP and surface. The companion
importing sibling code → out of bounds (subprocess + file-contract only). Any backend's key/token/base_url
reaching the browser → out of bounds (non-negotiable §4.5). A validator/selftest looks like it needs
loosening → fix the data/design, never the check. Grounding HEADs: aml-substrate@df23bba ·
aml-casework@2381d71 (re-grounded this phase).
