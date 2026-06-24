---
title: "Phase 73 ship target: extend the companion workbench (live engine) — NOT a new offline dist"
aliases: ["extend the companion workbench", "live engine over a precomputed dist", "no 9th dist this phase"]
category: decisions
tags: [phase-73, ship-target, companion, live-engine, workbench, boundary]
parents: [phase-73-rich-investigation-case-live-workbench]
created: 2026-06-23
updated: 2026-06-23
source: plan→delivered
confidence: high
---

## Context

The design fan-out's lead recommendation was a NEW offline-shippable dist (`casefile.html` →
`dist/casefile/`) — the matched pair rendered as AUTHORED-FROZEN outcomes mapped to the engine's
verdict vocab, the same way `dist/console` and `dist/triage` already ship precomputed adjudication
outcomes offline. That keeps the lead demo open-one-file-offline (the Canadian-bank stakeholder
audience the ship contract exists for) but renders frozen strings, not a running engine: the verdicts
are known at author time, the dist never calls `evaluate_sufficiency`.

## Decision

The user OVERRODE the dist recommendation: **extend the COMPANION workbench so the live sufficiency
engine actually RUNS over the rich data.** The rendered `determination` (Northgate) and the new
affirmative-`cleared` (Lakeshore) are engine OUTPUT computed over the authored evidence (A2), not a
precomputed dist. Reason: "the workbench is terrible" is the defect being fixed — a frozen dist would
render a better story but leave the live engine (the thing a technical buyer interrogates) unchanged.
The companion (`workbench.html` + `serve_workbench.py` + `evidence_requirements.py`) is the right home
because the live engine is there. Alternative rejected: the new offline dist (renders frozen strings;
inverts the "make the live engine good" goal, even though it would be the stronger pure-stakeholder
beat).

## Consequences

- Companion-only (A0): NOT a 9th ship target; build.py imports no companion/sibling layer; the 8
  offline dists stay BYTE-FROZEN (`--check all` 8/8). The rich case is served + computed live, never
  inlined by build.py.
- The named renderers (`liveGraphLayout`/`boGraphHTML`/`determinePanel`/`dispositionHTML`) already
  live in the companion `workbench.html` — this is in-place extension, not the extract-and-re-home a
  new dist would have required.
- The live tier's setup cost (server + vendored casework for the DECIDE finale) is accepted; the
  determination/clear verdicts compute from the authored evidence with no model.
- Trade-off: the lead stakeholder demo stays gated behind the companion setup, not open-one-file — a
  conscious cost the user chose to keep the engine honest-and-running.
