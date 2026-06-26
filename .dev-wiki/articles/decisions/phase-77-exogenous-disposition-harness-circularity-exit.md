---
title: "DEFER the exogenous-disposition validation harness — substrate's emit_* fns (P29/P30) are CLI-UNWIRED"
aliases: ["exogenous-disposition harness deferred", "emit_true_entities cli-unwired", "emit_intended_disposition cli-unwired", "circularity exit deferred"]
category: decisions
tags: [phase-77, exogenous-disposition, validation-harness, determination-engine, evidence-requirements, discovery, consume, deferred]
parents: [phase-77-consume-sibling-emissions]
created: 2026-06-26
updated: 2026-06-26
source: debrief
confidence: high
---

## Context

Signal-watch's determination engine (`evidence_requirements.evaluate_sufficiency`) decides file vs
clear from the evidence atoms, but every prior measurement of it has been against its own logic or a
synthetic case it produced — no independent oracle. Substrate's Phase-30 emission was expected to write
`eval/intended_disposition.json` (a disposition label authored BLIND to the casework sufficiency rule,
eval-only, firewalled), giving signal-watch the chance to validate the engine against an oracle it did
not make: the "circularity exit". At T1, verifying substrate @f2da3e4 by code (not by the brief),
both `emit_true_entities` and `emit_intended_disposition` were found to be tested-but-UNWIRED into the
substrate CLI — they run only inside substrate's own tests; the documented emit produces NEITHER
`identity/true_entities.json` NOR `eval/intended_disposition.json`. Only `identity/true_entities.parquet`
(via `--identity`) is CLI-reachable.

## Decision

DEFER the validation harness (DISCOVERY → Option 1) and author the substrate-CLI-wiring brief. There is
no tool-use-boundary path to the exogenous-disposition oracle, so there is nothing to validate against
without library-importing substrate's internals — which would violate the consume boundary (build the
artifact against an emission, not a sibling import). Authored
`docs/substrate-emit-cli-wiring-PLAN-BRIEF.md` (pins f2da3e4) naming both unwired `emit_*` functions,
the CLI-wiring ask (a flag), the firewall contract, and — the deeper gap surfaced at T4 — that wiring
the emit alone is insufficient for real merge scoring because substrate's clusters are content-addressed
`ENT-<entity_ref>` (a relabel of the spine key); a genuine identity layer is needed.

Alternatives rejected: build the harness against an unreachable emission (nothing to read); library-
import substrate's emit_* to call them directly (breaks the consume-via-emission boundary; couples
signal-watch to substrate internals).

## Consequences

The circularity exit is deferred to a sibling follow-on; the determination engine
(`evidence_requirements.py`) stays BYTE-UNCHANGED (it was never an A2 risk — the harness was always
read-only, but it is now simply not built). The harness consumes once substrate wires the emit JSON to
its CLI. The deferral is routed to a named brief, not left open. When the emit lands, the harness is a
clean companion-only consume (the engine output compared to a blind label, label never an engine input).
