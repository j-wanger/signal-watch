---
title: "Consume casework cleared via a casework-replayable C5 PROXY bundle, not Lakeshore (which fails-closed)"
aliases: ["casework cleared via C5 proxy", "Lakeshore fails-closed on fan-in C3", "casework cleared affirmative dismissal", "cleared-demo bundle"]
category: decisions
tags: [phase-77, casework, cleared, lakeshore, decide, re-vendor, file-bar, consume, fan-in-c3]
parents: [phase-77-consume-sibling-emissions]
created: 2026-06-26
updated: 2026-06-26
source: debrief
confidence: high
---

## Context

The Lakeshore case (CASE-B in `data/casefile/case.json`) clears in signal-watch's own live workbench
engine, but the DECIDE finale (the casework subprocess) could never SIGN a documented dismissal —
casework only had `{blocked, needs_more_info, signed}` + `{file, both_defensible}` until casework's
Phase 18 added the `cleared` affirmative-dismissal disposition (verified @b3546d4). The Phase-77 plan
was: re-vendor casework `bf15535→b3546d4`, then translate Lakeshore into a casework-contract bundle so
the DECIDE subprocess signs `cleared`. At T3 the translation surfaced a cross-pillar blocker: casework's
`grounding_replay` C3 detector is fan-OUT (≥5 cited outflows), but Lakeshore's C3 signal is fan-IN
(multiple originators → one beneficiary), so a Lakeshore bundle cites 0 outflows and casework refuses
it before the cleared branch is reached. Re-vendoring (T2) was verified to not regress any existing
DECIDE signings (gate funnel identical: 202/111/63).

## Decision

Consume casework `cleared` end-to-end, but on a casework-REPLAYABLE C5 PROXY bundle rather than
Lakeshore (USER OVERRIDE, option b). Authored `data/casefile/cleared-demo.bundle.json` — a C5
cash-placement case (an `exculpatory:true` transaction + a grounded exculpatory claim, NO
crime_type/inculpatory evidence, grounded on the vendored `fin-2023-alert001:IND-08`) — and wired
`serve_workbench.cleared_demo_consume`; casework SIGNS `cleared` (signed==true, disposition==`cleared`,
blocking_violations==[]). An adversarial review confirmed the bundle is HONEST (no fabricated
exculpatory evidence; the clear is grounded). The north-star Lakeshore CASE-B is documented as
fail-closed and the gap is parked as `docs/casework-c3-fan-in-PLAN-BRIEF.md`.

Alternatives rejected: fabricate fan-OUT outflows to force Lakeshore through casework's C3 detector
(the A3 abort — never weaken the file bar or fabricate evidence to force a sign); weaken casework's
grounding_replay here (it is the sibling's verifier, not signal-watch's to loosen; the casework file
bar stays byte-unchanged).

## Consequences

The DECIDE finale now signs `cleared` end-to-end through the real casework verifier — the affirmative-
clear arc is proven cross-pillar — on a replayable C5 proxy; the casework file/determination bar stays
BYTE-UNCHANGED (`cleared` is a separate branch). Casework is re-vendored at b3546d4 (`VENDORED_AT`); the
DECIDE subprocess now passes `--disposition file|cleared`; build.py still imports no casework; the 9 ship
dists stay byte-frozen (the workbench is companion-only). Lakeshore co-signing awaits casework fan-IN C3
support (`docs/casework-c3-fan-in-PLAN-BRIEF.md`, pin b3546d4). Vendoring stays
distribution-not-coupling (the subprocess file-handoff is unchanged).
