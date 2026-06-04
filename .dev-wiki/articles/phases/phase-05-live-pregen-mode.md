---
title: "Phase 5: Live / pre-gen mode (M4, optional)"
aliases: []
category: phases
tags: [milestone-m4, optional]
parents: []
created: 2026-06-04
updated: 2026-06-04
source: init
status: not-started
scope: ["backend/**", "data/**", "scripts/pregenerate.md"]
entry_criteria: "M3 complete — presenter-ready. This phase is OPTIONAL."
exit_criteria: "Pre-generated path works; absence of it changes nothing."
---

# Phase 5: Live / pre-gen mode (M4, optional)

## Objective

Optionally make Act 1 (advisory → candidate signals) genuine model output via a
pre-generated `data/signals_<typology>.json`, with the scripted config as fallback.
Live backend (`backend/relay.py`) is a further optional step.

## Scope

- `scripts/pregenerate.md` — OpenCode/Copilot prompt-spec → `data/signals_*.json`
- `data/signals_<typology>.json` — pre-generated candidates (matches schema)
- `backend/relay.py` — OPTIONAL FastAPI relay → local llama.cpp / approved gateway

## Exit Criteria

- [ ] `scripts/pregenerate.md` prompt-spec written
- [ ] engine loads `data/signals_*.json` when served, else falls back to inline config
- [ ] removing the data file changes nothing (scripted core intact)
- [ ] (optional) `backend/relay.py` with auto-fallback on error/timeout

## Constraints (HANDOFF §4.5, §6) — load-bearing

- Live mode is OFF by default, isolated in `backend/`. The demo must run with it absent.
  Prevents: live failure on stage.
- NEVER put keys/tokens in the frontend or commit them. The browser holds no credential.
- Copilot is NOT a web backend. Live = local llama.cpp or the approved gateway only.
- Any live element auto-falls-back to the scripted path on error/timeout.

## Assumptions

- Pre-generated (OpenCode/Copilot, ahead of time) is preferred over live for the actual
  presentation. If a live call is ever wanted, the fallback must be tested first.
