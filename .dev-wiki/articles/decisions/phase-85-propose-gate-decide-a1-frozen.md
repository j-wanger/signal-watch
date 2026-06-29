---
title: "Phase 85: propose→gate→decide held — the agent proposes, the deterministic engine licenses, the human decides (A1-frozen, companion-only)"
aliases: [phase-85-propose-gate-decide, a1-frozen-determination, companion-only-proposer, presentation-only-proposal]
category: decisions
tags: [agentification, determination, propose-gate-decide, a1-guard, companion, dist-boundary]
parents: [phase-85-determination-pre-proposer]
created: 2026-06-29
updated: 2026-06-29
source: plan
confidence: medium
---

## Context

The program's load-bearing contract is propose→gate→decide: an agent may PROPOSE, but the deterministic
gate LICENSES and the human DECIDES. The §12 sufficiency engine (`evidence_requirements.py`) is the
licensing gate, and it has been BYTE-FROZEN across every phase since Phase 69 (the A1 guard). Adding an
agent that proposes a determination must not — by accident or by convenience — let that proposal feed
the engine's licensing path or the human's decision, and must not cross the build/dist boundary.

## Decision

Hold propose→gate→decide as a NON-NEGOTIABLE constraint: the agent's proposal is a
presentation/measurement-only companion path that NEVER feeds the engine or the human's licensing. The
deterministic sufficiency engine still licenses the determination; the human still decides.
Concretely:
- `evidence_requirements.py` BYTE-UNCHANGED (git-diff empty).
- the 256/376 casework signing funnel byte-unchanged (the proposal is decoupled from signing).
- build.py imports nothing new (grep guard: determination_proposer / serve_workbench / curate /
  casework / spine).
- all 9 ship dists byte-frozen — the workbench is companion-only, it touches no dist.

Rejected: wiring the proposal into the determination bar (an A1 violation, and it would make the
measurement circular — the agent would be scoring its own input to the engine); shipping the proposer
in any dist (the offline ship file makes no model call, §4.5).

## Consequences

- The phase is companion-only by construction — the dist boundary holds trivially, the A1 guard holds
  by construction (the engine is never touched).
- This is the A5 ledger row, in the abort rule: any `evidence_requirements.py` change / the proposal
  feeding the determination bar / a build.py companion import / any of the 9 dists not byte-identical →
  STOP-and-surface.
- The proposal's value is exactly its measurement (how well a thin agent matches the exogenous oracle
  vs the engine) — not its influence on the decision; the agent stays deliberately thin.
