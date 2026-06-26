---
title: "All three consumes in one STANDARD phase; two deferred to named sibling briefs, the open-data fork parked"
aliases: ["three consumes one phase", "open-data fork parked", "phase-77 scope", "consume-readiness gated on siblings"]
category: decisions
tags: [phase-77, scope, ceremony, open-data-fork, sibling-handoff, consume, deferred]
parents: [phase-77-consume-sibling-emissions]
created: 2026-06-26
updated: 2026-06-26
source: debrief
confidence: high
---

## Context

Three independent sibling emissions were expected this session — substrate Phase 29 (`true_entities`
for the slice) + Phase 30 (`exogenous-disposition-label`), casework Phase 18 (`cleared`). Each is
consumable on the signal-watch side and each is roughly M-to-L in effort. The open question for the
two-sided real merge oracle (a should-merge truth substrate's content-addressed clusters can't provide)
points at an OPEN-DATA fork of the synthetic generator — substrate-side, contract-neutral.

## Decision

Run all three consumes in ONE phase under STANDARD ceremony (independent, each modest; bundling keeps
cross-repo coherence and amortizes the verification regate), ordered by strategic depth. As delivered,
only ONE consume landed as planned and TWO deferred against discovered sibling state — but each deferral
was routed to a NAMED sibling brief, not left open:

- **(1) exogenous-disposition harness → DEFERRED** (substrate's `emit_*` are CLI-unwired) →
  `docs/substrate-emit-cli-wiring-PLAN-BRIEF.md`.
- **(2) casework `cleared` → DELIVERED via a C5 proxy** (re-vendored b3546d4; Lakeshore itself
  fails-closed on fan-in C3) → the Lakeshore co-sign gap is `docs/casework-c3-fan-in-PLAN-BRIEF.md`.
- **(3) `true_entities` → real scoring DEFERRED** (the captured oracle is circular) → real-66 stays
  consensus; the unblocking work is `docs/substrate-open-reference-data-fork-PLAN-BRIEF.md`.

The open-data fork is PARKED as a substrate handoff brief (substrate-side, contract-neutral), NOT a
signal-watch task. Alternatives rejected: three separate phases (ceremony overhead for independent
modest consumes); build the open-data fork here (sibling-rooted, not a signal-watch deliverable).

## Consequences

One STANDARD phase delivers one sibling consume (casework `cleared` end-to-end) + four named handoff
briefs (`substrate-emit-cli-wiring`, `casework-c3-fan-in`, `substrate-open-reference-data-fork`,
`cross-pillar-build-order`). NO dist changed — Phase 77 is companion-only, all 9 dists byte-frozen;
build.py imports no spine/scorer/sibling/curate. The honesty governor + resolver-input firewall held.
The phase surfaced the CONSUME-READINESS pattern: a signal-watch-local frontier can be thin until a
sibling phase lands — three planned advances were gated on sibling emissions that don't exist yet
(verify the sibling live before committing to a consume). The two-sided real merge oracle stays a named
substrate handoff, never faked here.
