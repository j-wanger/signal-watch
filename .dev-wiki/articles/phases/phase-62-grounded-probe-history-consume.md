---
title: "Phase 62 — Grounded probe-history consume (§12) + §14-frozen boundary + P22 pin re-ground"
aliases: []
category: phases
tags: []
parents: []
created: 2026-06-20
updated: 2026-06-21
source: plan
status: completed
ceremony: lite
scope: ["data/probe-history/**", "data/triage/**", "data/capability-taxonomy.json", "scripts/curate_triage_scenarios.py", "scripts/probe_history_stats.py", "scripts/signal_coverage_map.py", "scripts/e2e_chain_check.py", "scripts/build.py", "dist/triage/**", "docs/**", ".claude/rules/active-phase.md", "HANDOFF.md", "CLAUDE.md"]
entry_criteria: "aml-substrate P22 'grounded probe-history' projector COMMITTED (T1 verifies + pins the HEAD; pause+ask if uncommitted)."
exit_criteria: "grounded alert-history.json committed + deterministic + schema-valid; C-code→TM-### map committed + selftested; probe_history_stats.py prints all 6 Role-2 metrics over the grounded file; data/triage/scenarios.json re-curated (history-derived strata re-grounded, novel+random byte-stable, §14 grammar intact); dist/triage rebuilt + re-frozen, the OTHER 7 dists byte-unchanged, build.py --check all 8/8, triage-console.test.mjs green, no substrate import; cross-pillar pins moved to substrate@<P22>, signal_coverage_map.py --check byte-identical (reachable-now 171), e2e_chain_check.py --selftest green; honesty framing checked at the delivery gate."
grounding_heads:
  aml-substrate: ae98924    # P22 loop-closure (verified committed at T1; the loaded 2e5d0f0/P21 facts were stale)
  aml-casework: c6d8401    # Phase 12 (unchanged)
  signal-watch-corpus: 472b44e
---

# Phase 62 — Grounded probe-history consume (§12) + §14-frozen boundary + P22 pin re-ground

> **Status: COMPLETED — delivered + accepted 2026-06-21.** The phase was PLANNED as a two-pronged
> end-to-end consume (§12 measurement + a sanctioned USER-OVERRIDE unfreeze of `dist/triage`). At the
> **T4 pause-checkpoint the §14 unfreeze was STOOD DOWN on evidence** — the substrate's label-blind
> probe-history is the RIGHT source for §12 (firing/disposition MEASUREMENT) but the WRONG source for §14
> (the triage console needs adjudicable FACT PATTERNS the substrate doesn't emit: `curate_triage_scenarios.py`
> couples to alert-history via only 5 metadata fields on 7/20 scenarios, and the marquee TM-104 pair is C20
> — no substrate detector). The user **accepted the boundary** → `dist/triage` stays **BYTE-FROZEN**, NO
> re-curation, NO redesign-to-force. The phase delivered the **§12 measurement consume only**; the ONLY
> dist change is the launcher pin cascade (`dist/index.html`, 1 line — Phase-60 Option-A). The
> Objective/Scope below are PRESERVED AS-PLANNED for context — read them against this Resolution.

## Why

aml-substrate **Phase 22 (loop-closure)** landed a CONFORMANT **grounded probe-history projector** — it
projects `monitor/compose.Dossier` into a grounded `alert-history.json`, **conformance-validated against a
VENDORED copy of signal-watch's OWN `probe_history_stats.py` @58925a8** (real n=1000 build). signal-watch's
§12 non-ship measurement layer (`probe_history_stats.py`) and §14 triage console
(`data/triage/scenarios.json`) today both run on the **SYNTHETIC Phase-48 probe-history fixture**. The
substrate's grounded output is a drop-in replacement curate source: the alert / entity / cited-evidence side
becomes **grounded in real substrate detection output**, while dispositions stay **label-blind illustrative**
(never ground truth). Substrate output is itself synthetic (`meta.synthetic:true`) → the "no real data,
ever" non-negotiable holds. The Phase-61 §7 frontier ranking did NOT anticipate this (P22 landed after).

## Objective

Consume the grounded probe-history **end-to-end**: (1) the §12 non-ship measurement layer
(`probe_history_stats.py`), AND (2) the §14 triage console — a **sanctioned USER-OVERRIDE ship-artifact
unfreeze** of `dist/triage` (the same class as the Phase-60 launcher + Phase-61 blueprint true-up). Only the
**history-derived strata** (fired-signal + below-the-line) re-ground; novel + random stay as-authored.
`dist/triage` rebuilds + re-freezes at a NEW grounded baseline; the OTHER 7 dists stay byte-frozen; build.py
NEVER imports the substrate (tool-use produces the file, build reads committed `data/` only).

## Direction (gate 2026-06-20, all_accept: false)

The user invoked `/dev-plan` to consume substrate P22's grounded probe-history end-to-end into signal-watch.

- **A0 [HIGH — T0 weakest] ACCEPT** — T1 verifies the substrate P22 projector is COMMITTED
  (`git -C /Users/jwang/aml-substrate`) + pins that HEAD inline; if still uncommitted → PAUSE + ask the user
  to commit it before proceeding. Running `--probe-history` is sanctioned tool-use (file-contract output),
  NOT lifecycle-driving.
- **A1 [HIGH] REJECT → REVISED ACCEPT** — the consume flows end-to-end into `dist/triage` (a sanctioned
  unfreeze), WITH a built-in CHECKPOINT: if the grounded history doesn't map cleanly into the §14 strata OR
  breaks build-boundary validation, PAUSE + report; do NOT redesign the console to force the fit.
- **A2 [HIGH] ACCEPT** — the C-code→TM-### namespace map is SHIP-LOAD-BEARING + grounded (curate source +
  the silent_rules metric); every C-code resolves to a TM id or an explicit honest-null.
- **A3 [MED — DON'T-KNOW → DELIVERY-GATE checkpoint] ACCEPT** — the honesty framing ("grounded detection,
  illustrative dispositions") is drafted explicitly in T3/T4; the user checks it at the delivery gate before
  anything is called "grounded".

## Scope

`data/probe-history/**` (the grounded `alert-history.json` + the C-code→TM-### map) ·
`data/capability-taxonomy.json` (read-only grounding for the map) · `scripts/curate_triage_scenarios.py` ·
`scripts/probe_history_stats.py` · `data/triage/**` (re-curated scenarios) · `dist/triage/**` (the
SANCTIONED unfreeze) · `scripts/build.py` (NO substrate import) · `scripts/signal_coverage_map.py` +
`scripts/e2e_chain_check.py` (pin re-ground only) · `docs/**` · `.claude/rules/active-phase.md` · `HANDOFF.md`
· `CLAUDE.md`. **NOT touched:** the 7 non-triage dists (byte-frozen); the novel + random triage strata
(byte-stable); build.py NEVER imports the substrate.

## Tasks

T1 produce + pin the grounded probe-history (S) · T2 the C-code→TM-### namespace map (S) · T3 the §12
non-ship measurement consume (M) · T4 the §14 triage re-curation — the unfreeze, history-derived strata only,
with the A1 checkpoint (M) · T5 rebuild + re-freeze `dist/triage` at the grounded baseline (S) · T6 re-ground
the cross-pillar pins + document (S). See `tasks.md`.

## Exit Criteria

- [x] grounded `alert-history.json` committed under `data/probe-history/grounded/`, deterministic (re-run
  byte-identical, sha256 `d9d1110e`), schema-valid; substrate P22 HEAD pinned inline (ae98924).
- [x] C-code→TM-### map committed (`capability-tm-map.json`), closed-vocab validated; every C-code resolves
  to a TM id or explicit honest-null (C15→∅); `--selftest` covers it (inversion-faithful).
- [x] `probe_history_stats.py --grounded` prints all 6 Role-2 metrics over the grounded file; the honesty
  framing explicit (every disposition-derived metric tagged "[over illustrative dispositions]"); no overclaim
  language (adversarial overclaim audit found none).
- [x] §14 re-curation **STOOD DOWN at the T4 checkpoint** (the A1 fallback): `data/triage/scenarios.json`
  byte-stable (NOT re-curated) — the substrate's label-blind history is the wrong source for §14; the user
  accepted the boundary. `triage-console.test.mjs` green (§14 unchanged).
- [x] §14 unfreeze NOT executed → `dist/triage` BYTE-FROZEN (the OTHER 7 dists too); `build.py --check all`
  8/8; `git diff --stat HEAD -- dist/` shows ONLY `dist/index.html` (1 line — the launcher pin cascade, NOT
  triage); build.py has no substrate import.
- [x] cross-pillar pins moved to substrate@ae98924; `signal_coverage_map.py --check` byte-identical
  (VERIFIED ZERO tier movement, reachable-now 171) + `--selftest` green; `e2e_chain_check.py --selftest`
  green; provenance + the §14-frozen boundary rationale documented in-place (docs/probe-history.md, CLAUDE.md,
  substrate-pin.json).

## Checkpoints

- **T1 (A0):** substrate P22 projector still uncommitted → STOP, ask the user to commit it before consuming.
- **T4 (A1):** the grounded history doesn't map cleanly into the §14 strata OR breaks build-boundary
  validation → PAUSE + report; do NOT redesign the console to force the fit. Fall back to the §12 non-ship
  consume only (triage stays byte-frozen).
- **Delivery (A3):** the user checks the "grounded detection / illustrative dispositions" framing before
  anything is called "grounded"; re-word if it reads as claiming grounded dispositions.

## Abort

Any of the OTHER 7 dists drift / a build.py substrate import → STOP and surface (only `dist/triage` may move —
the sanctioned unfreeze). A C-code resolves to nothing AND the null isn't surfaced → out of bounds (A2). A
validator looks like it needs loosening → fix the data/design, never the check.
