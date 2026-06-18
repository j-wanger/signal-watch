---
title: "Phase 56 — Chain workbench SPINE (beat 1) delivered"
date: 2026-06-17
phase: 56
tags: [chain-workbench, cross-pillar, companion, beat-1, lite]
status: active
---

# Phase 56 — Chain workbench: the SPINE (beat 1) delivered + accepted

The analyst case-workbench for the substrate→casework→verify chain. Reframed at plan time (the user's
"detection doesn't need runtime gen") from an orchestrator to an **analyst workbench**: detection is
pre-baked upstream (substrate evidence bundles vendored like the corpus pin); per case the downstream —
casework consume (6 verifiers + a live/stub SAR draft) + signal-watch's cross-pillar verify — runs LIVE,
stage-streamed → CONNECTED + a flag→corpus audit walk. Two-beat, like Phase 55.

## What shipped (T1–T5, all [x])

- **T1** `data/chain-cases/` — `CASE-P-0010361` vendored byte-identical from aml-substrate@df23bba
  (sha1 `bac574d…`; 5 alerts C4/C3/C2/C5/C15, 71 txns, illustrative:true) + a manifest; a new
  `scripts/validate_chain_cases.py` reuses `e2e_chain_check.check_substrate` (schema + §2 id-mint +
  grounding to the frozen corpus) and enforces manifest↔bundle referential integrity. `--selftest` catches
  id-mint tamper + capability drift.
- **T2** `aml-casework/docs/consume-cli-PLAN-BRIEF.md` (sibling hand-off, untracked there). Code-verified
  @85602c1: reference flow = `load_real_bundle → generate_narrative(drafter) → record_signoff →
  emit_signed_sar`. **Surfaced the load-bearing wrinkle:** the test `FixedDraftStub` is in `tests/` and is
  fixed-content → the CLI's `--drafter stub` needs a src-resident bundle-derived stub; the open risk moved
  to brief-A0 (can a generated narrative satisfy `narrative_grounding`).
- **T3** `scripts/serve_chain.py` (stdlib companion) — `GET /cases`, `POST /run` NDJSON stage stream
  (evidence → consume → verify → connected), single-flight 409. casework consume = subprocess of
  `python -m aml_casework.ingest` (injectable; honest "bridge gated" until the CLI lands); e2e verify =
  subprocess `--real` with **pillar-status.json snapshot+restore** (a run never drifts the launcher).
  `--selftest` green offline (casework stubbed) → CONNECTED on the real vendored bundle.
- **T4** `chain.html` (dossier theme; signature = a typed 4-node chain ledger that lights as the join
  connects) + the flag→corpus audit walk; line-buffered NDJSON reader = stage rendering, never a token
  stream; `esc()` the sole escaper. `tests/chain.test.mjs` 31/31 (vm + DOM/fetch shim).
- **T5** `docs/chain-workbench.md` (run recipe + the subprocess/snapshot boundary + two-beat framing) +
  a smoke-checklist section.

## Invariants held

`--check all` 8/8 zero drift; `dist/` + `data/pillar-status.json` byte-untouched; no `import
aml_substrate`/`aml_casework` anywhere (subprocess + file-handoff only); chain.html not a build target /
not in dist/; nothing persisted; key server-side only. No CLAUDE.md edit (non-ship, matching the 51–54
precedent + the bloat guard).

## Design choices worth remembering

- **pillar-status snapshot/restore** around the verify subprocess: e2e_chain_check always writes
  `data/pillar-status.json`, which the launcher inlines at build time — so a workbench run had to preserve
  it byte-for-byte or `--check all` would drift. serve_chain snapshots + restores it.
- **serve_chain reads the signed-SAR FILE, not the CLI stdout** — de-risks the casework CLI's output
  contract (the file is the §2 artifact); only the file shape must match, not a print format.
- **config injection via an HTML-comment marker** (`<!--__CHAIN_CONFIG__-->` → a `window.__CHAIN_CONFIG__`
  script) keeps raw chain.html valid JS, so the test loads the template directly (chain.html has no dist).

## Two-beat status

- **Beat 1 (spine):** DELIVERED + user-accepted + committed this session. Phase stays ACTIVE.
- **Beat 2 (the delivery gate):** GATED on the casework consume CLI (T2's brief, an aml-casework session).
  Then a real neural SAR drafts in the browser → `e2e_chain_check --real` CONNECTED, no serve_chain change
  expected (it reads the SAR file). The honest open risk is brief-A0 (bundle-derived stub grounding).

## Soft Observations / Phase 57 Candidates

- **Beat 2 is the immediate next move** (sibling-rooted): land `aml-casework/docs/consume-cli-PLAN-BRIEF.md`
  → a real neural SAR in the browser → close the Phase-56 delivery gate. Evidence: T2 brief; the gated
  `casework_consume` path in serve_chain.py.
- **Grow the case library** beyond CASE-P-0010361 — more vendored substrate bundles (different
  typology mixes) make the workbench a richer analyst surface; the validator + manifest already scale to N.
- **`e2e_chain_check --selftest` prints a stale "bridges pending"** trailing line (a Phase-55 cosmetic
  string) while it actually preserves the committed bridge states — harmless, but a 1-line fix candidate if
  that script is reopened.
- **Multi-case "run all" / a session ledger** in the workbench (the console/triage export precedent) — only
  if the demo needs batch storytelling; YAGNI until asked.

## Post-delivery (same session, after the spine commit 16920d4)

- **Showed the workbench** (user asked): served it at `localhost:8020`, screenshotted the landing (real)
  and the full chain arc. The arc screenshot drove the REAL client (loadCases → select → runCase →
  the NDJSON reader) over the proven stub-consume run — so the ledger/SAR/audit-walk render exactly as the
  page does; only the SAR narrative is the offline stand-in (the "deterministic stub" chip is visible).
  Capture used `serve_chain.run_case(..., consume=_stub_signed_sar)`; pillar-status stayed byte-clean
  (snapshot/restore held). All preview scaffolding lives in `/tmp` — zero repo change.
- **DECISION (foreclosed option):** offered to wire that captured-run path into the LIVE `/run` as a
  clearly-labeled offline preview mode (so a browser Run shows the full arc before beat 2). The user chose
  **leave the live `/run` strictly gated as designed** — honesty over demo convenience: a stub SAR rendered
  through the live server would blur beat 2's whole point (the live run IS the proof). No code change; the
  "bridge gated" behavior stands. Don't re-raise the preview-mode idea.

## Beat 2 verified — phase COMPLETE (both beats; 2026-06-17)

The user reported beat 2 done; code-verified the sibling (per the re-ground-before-consume rule, not on faith):
- **The casework consume CLI landed** — aml-casework@`f0542b7` (Phase 7, "consume CLI + deterministic
  drafter"): `python -m aml_casework.ingest <bundle> --out <signed> --drafter stub|claude` (argparse, `main`,
  `__main__`), `--drafter claude` FAIL-SOFT, + a new SRC-resident `drafter_stub.py` — **exactly the brief-A0
  bundle-derived design** (one inculpatory claim per `signal_id`; prose names only the grounded `account_id`
  + generic lowercase typology phrases → grounds by construction). brief-A0 resolved YES. The consume-cli
  brief is now tracked in casework.
- **The chain CONNECTS from signal-watch** — `serve_chain.run_case("CASE-P-0010361")` drove the REAL CLI
  (drafter fail-soft to stub, no key here) → signed, 0 blocking → real `e2e_chain_check --real` → CONNECTED,
  audit walk 5/5 grounded; pillar-status byte-clean (snapshot/restore held). The neural path is key-gated
  here (no `ANTHROPIC_API_KEY`); its fail-soft is verified and the end-to-end neural run is covered by
  casework's `@integration` test — an honest gap from THIS env, not a defect.
- **Close work:** re-grounded the casework pin `85602c1`→`f0542b7` in `e2e_chain_check.py` (the process
  rule); emitted the real signed SAR via the CLI + ran `--real` → pillar-status all-green with `f0542b7`;
  rebuilt the launcher (`dist/index.html`) → `--check all` 8/8 (7 dists byte-identical, only the launcher
  moved with the pin). e2e_chain_check `--selftest` + launcher.test.mjs + the chain suite all green.
- **Gate:** delivery accepted; `gate-log:phase-56 delivery=accepted`; the active-phase delivery checkbox
  flipped `[x]`. A4 (the T0 weakest) HELD — the CLI was thin + one predicted src stub. Phase functionally
  COMPLETE; active→completed left for the user's explicit call (Phase-55 precedent).
