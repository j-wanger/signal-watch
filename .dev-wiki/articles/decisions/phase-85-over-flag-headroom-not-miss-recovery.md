---
title: "Phase 85: the agent's headroom is OVER-FLAG precision-recovery, not file-MISS recall — a null on the miss side IS the finding"
aliases: [phase-85-over-flag-headroom, miss-side-null, two-sided-determination-measurement, abstention-as-coverage]
category: decisions
tags: [agentification, determination, measurement, honesty, oracle, two-sided, abstention]
parents: [phase-85-determination-pre-proposer]
created: 2026-06-29
updated: 2026-06-29
source: plan
confidence: medium
---

## Context

Phase 83 had a clean two-sided headline (agent 54/66 vs spine 33) because the merge spine got 33 of 66
WRONG in both directions — there was symmetric headroom to recover. The §12 determination engine is
NOT symmetric. The Phase-78 pre-measurement shows the engine's error mass is structural OVER-FLAG: all
727 KYC-pure cases are file-ready-but-oracle-clear, plus 593/6087 file-ready-but-clear. The file-MISS
side is different — the 71 of 121 missed oracle-file cases miss because the 2nd corroborating leg is
NOT in the bundle (substrate Ask #3 measured-null). An agent reasoning over the same bundle the engine
sees CANNOT recover what isn't there. The risk: presenting a Phase-83-shaped "the agent beats the
engine" story that the data does not support.

## Decision

Frame the measurement as TWO-SIDED (agent-vs-oracle AND engine-vs-oracle, on file AND clear), and
state the headline as **precision-recovery on the engine's structural over-flag** (the clear side),
with the **file-misses HONESTLY NULL**. The null is itself the finding: it demonstrates the misses are
substrate-gated (a DATA gap), not reasoning-gated — which is exactly the Phase-84 decisiveness handoff,
now measured. Do NOT promise a "54-vs-33"-shaped recall-recovery; do NOT present a one-sided number.

**Abstention semantics (the measurement-semantics note):** the proposer's three-way output (file /
cleared / needs-more-info) is scored against the BINARY oracle (file|clear) as two SEPARATE numbers —
`committed-accuracy` (of the agent's committed file|clear proposals, how many matched) and
`abstention-coverage` (the needs-more-info fraction). needs-more-info is NEVER counted as a wrong-file
(it would understate the agent) NOR as correct (it would overstate). The deterministic engine baseline
shares the same three-way output space and is scored identically. This is the honest second-rater
pattern carried from the news/triage gates.

Rejected: a single conflated accuracy number (hides the over-flag vs miss asymmetry — the whole point);
counting abstentions as misses or as hits (both dishonest); a recall-recovery headline (the file-misses
are a data gap, not the agent's to recover).

## Consequences

- The harness emits {committed-accuracy, abstention-coverage} as two figures, plus the two-sided
  confusion (agent-vs-oracle, engine-vs-oracle, on file AND clear), every number counts-only and
  synthetic-substrate-qualified, no catch-rate/lift/precision/recall words.
- The honest credible claim is "of the over-flag cells the engine files-but-the-oracle-clears, the
  agent committed clear on N" — a measured, two-sided, counts-only statement. The file-miss row reads a
  documented NULL with the substrate-Ask-#3 reason.
- If the over-flag mass were absent (it is not — Phase-78 pre-measured it), the fallback reframe is the
  §12-discovery-feed queue-prioritizer — still honest, still local.
- This is the A1 (T0-weakest) row of the assumption ledger; its revisit-status confirms or falsifies
  the over-flag-headroom shape at debrief.
