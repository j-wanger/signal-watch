---
title: "Phase 83: keep the 4-way agent vocab; count both-defensible/escalate as deferred (not scored)"
aliases: [phase-83-4way-vocab, merge-adjudicator-deferrals, defer-is-a-feature]
category: decisions
tags: [agentification, merge, vocab, oracle, human-gate, honesty]
parents: [phase-83-merge-adjudicator-oracle-scored]
created: 2026-06-29
updated: 2026-06-29
source: implementation
confidence: high
---

## Context

The merge console's human-gate vocab is 4-way: `uphold_merge`, `reject_as_shares`, `both_defensible`,
`escalate`. The committed oracle, however, is BINARY — `uphold_merge` / `reject_as_shares` (33/33 over
the 66 scored cases); `both_defensible` and `escalate` carry NO oracle label. The question: should the
agent be forced to a binary call (cleaner single agreement number) or keep the full 4-way vocab?

## Decision

Keep the agent's full 4-way vocab and count `both_defensible` + `escalate` as **"deferred to human"** —
a SEPARATE count, NOT scored against the binary oracle. Agreement is computed only over the agent's
binary commitments. This matches the human-gate doctrine: an agent that recognizes ambiguity and
defers is a feature, not a miss — `propose → gate → decide`, never relaxed.

Rejected: forcing a binary call to get a cleaner single number — it loses the defer signal (an agent
deferring on the genuinely-ambiguous cases is exactly the behavior the human-gate doctrine wants to
surface), and it would conflate "wrong" with "honestly uncertain."

## Consequences

- The harness reports three buckets: matched (binary call == oracle), mismatched (binary call !=
  oracle), deferred (both_defensible/escalate) — counts-only, with the synthetic qualifier.
- The deferred count is itself a measured signal (does the agent defer where the cases are
  genuinely-ambiguous, i.e. the over-merge-trap + fragmentation-gap quadrants?).
- No agreement count is presented as a catch-rate / lift / precision / recall (the honesty word-ban).
- A lazy agent that echoes `spine_verdict` is detectable: its agreement equals the stub's, with zero
  deferrals — the by-quadrant breakout exposes it.
- **OUTCOME (implemented 2026-06-29):** the 4-way vocab + deferral-counting path is implemented and
  tested (junk→escalate in the selftest), but the LIVE agent used **0 deferrals** — it committed a
  binary call on every case (and beat the spine, 54/66 vs 33, so it was not the lazy-echo case). The
  defer path is structurally correct but UNEXERCISED live; a deferral/anchoring ablation (prompt-to-
  defer on ambiguity, or hide `spine_verdict` to test anchoring) is a Phase-N+1 candidate. The
  decision held; confidence → high.
