---
title: "Phase 56 — Chain workbench: the HTML analyst UI (companion-served live consume + verify over a pre-baked case library)"
type: phase
status: active
ceremony: lite
milestone: M9
created: 2026-06-17
updated: 2026-06-17
tags: [cross-pillar, html-ui, companion-server, analyst-workbench, live-neural-sar, pre-baked-library, dev-time, two-beat, frontend-design]
---

# Phase 56 — Chain workbench: the HTML analyst UI

## Objective

An HTML frontend for the substrate→casework→verify chain, **living in signal-watch**. The user's
"detection doesn't need runtime gen" reframes "orchestrator" → an **analyst case-workbench**: in a real
AML system, generation + detection run upstream/batch and the analyst's runtime starts at the *alert*.
So the demo's live surface is the analyst loop over a case, with the **gate as the live proof**.

## Approach (gated 2026-06-17 — workbench over a pre-baked library; live consume + verify)

- **Pre-baked / upstream (vendored):** substrate gen + detection → the evidence **bundles** are the case
  library, committed into signal-watch like the corpus pin (synthetic/illustrative).
- **Live per case (in the UI):** casework **consume** (6 verifiers + a **neural SAR draft**, `ClaudeDrafter`)
  → signal-watch's `e2e_chain_check --real` cross-pillar verify → **CONNECTED** + the flag→corpus audit walk.
- **`scripts/serve_chain.py`** (stdlib companion) — `GET /cases`; `POST /run {case}` → subprocess the
  casework consume CLI → subprocess `e2e_chain_check` → **stage-stream** (NDJSON). Holds
  `ANTHROPIC_API_KEY` server-side; **stub fallback** when absent (keyless = deterministic SAR).
- **`chain.html`** (dossier theme, `frontend-design`) — case list → Run → staged reveal. Dev-time
  companion, **never a ship artifact** (offline dists byte-frozen; `chain.html` is NOT a build target).

Subprocess + file handoff only — **no import** of either sibling (the news/corpus live-mode isolation,
extended to drive a sibling CLI). The one sibling prerequisite: a thin casework consume CLI (T2 brief).

## Scope

- `data/chain-cases/**` (the vendored bundle library) · `scripts/serve_chain.py` · `chain.html` ·
  `tests/{chain.test.mjs, serve_chain selftest}` · `docs/chain-workbench.md` · `tests/smoke-checklist.md`
- `aml-casework/docs/consume-cli-PLAN-BRIEF.md` (authored here, executed in a casework session)
- NOT touched: the 8 build targets / offline dists; `build.py` never imports the companion.

## Exit criteria (the SPINE — this session / signal-watch-local)

1. Vendored case library (≥1 bundle: `CASE-P-0010361`) + a build-time validator (each passes
   `e2e_chain_check` substrate-side; provenance recorded).
2. `serve_chain.py` — `--selftest` green OFFLINE with the casework subprocess STUBBED (cases listed; a
   run stage-streams → CONNECTED on a fixture; key→stub fallback; honest gated/error paths); no sibling
   import; build.py clean of it.
3. `chain.html` — `node tests/chain.test.mjs` green (stage-rendering + badge + XSS-escape + NDJSON
   stage consumption under the DOM shim).
4. Casework consume-CLI brief written (the sibling prerequisite).
5. `docs/chain-workbench.md` + smoke-checklist; `chain.html` NOT a build target; `--check all` 8/8.

## Delivery gate (the live beat — GATED on the casework CLI)

The live run (real neural SAR drafted in the browser, end-to-end CONNECTED) closes when the casework
consume CLI lands (T2, a casework-rooted session) + the companion drives it. Two-beat, like Phase 55:
the signal-watch spine is selftest-proven now; the live demo is gated on the sibling CLI.

## Assumptions (ledger: Phase-56 block, all_accept: false)

- **A0 [HIGH]** detection pre-baked/upstream; the bundles are vendored; the live verify is the proof. ACCEPT.
- **A2 [MED]** the case library = committed synthetic bundles (SAR live-drafted, not vendored). ACCEPT.
- **A4 [HIGH, T0-weakest]** casework can expose a thin per-case consume CLI (the 5 functions exist). ACCEPT.
- **A1' [HIGH]** companion subprocesses the casework CLI + e2e_chain_check, no imports, dev-time, dists
  untouched. ACCEPT.
- **A5 [MED]** server-side key + deterministic-stub fallback (keyless demo runs). ACCEPT.
- A3 (defer live neural) was REJECTED → live drafting pulled into v1 (the casework CLI prerequisite).

## Abort

`chain.html` becomes a build target, or any of the 8 offline dists drift → STOP and surface. The
companion importing sibling code → out of bounds (subprocess + file-contract only). The key reaching the
browser → out of bounds (non-negotiable). Grounding HEADs: aml-substrate@df23bba · aml-casework@85602c1.
