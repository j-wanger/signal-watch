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
status: corrected-at-impl
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

## CORRECTED at impl (the live measurement contradicted the optimistic half)

The two-sided FRAME held, the FIREWALL held, and the file-miss NULL held — but the predicted SHAPE of
the agent's win was WRONG. The live capture (a local Qwen MoE over the full 6935-case capture via 46
cap-signatures; counts only, synthetic substrate slice) showed:

- The agent DID correct the structural KYC over-flag — it abstains on all **727** KYC-pure file-ready
  cases (the predicted over-flag win HELD on the KYC class).
- The agent recovers MORE oracle-file cases — committed `file` on **74** vs the engine's **50** (higher
  file sensitivity, the opposite of a recall NULL — though the misses it does not recover are still the
  substrate-Ask-#3 data gap).
- BUT the agent OVER-files on the volume ML class — committed-wrong **4482** vs the engine's **593**. It
  files the dominant `C2|C3|C8` signature (4040 cases, 4029 benign) because it reasons from per-case
  red-flag CO-OCCURRENCE; the benign-ness is a POPULATION base-rate property invisible in a single case,
  which the calibrated deterministic rule encodes and the per-case agent cannot infer.

So the prediction "clean precision-recovery on the over-flag" was INCOMPLETE: the agent TRADES the
engine's conservatism for sensitivity (recovers files + fixes the KYC over-flag, over-files on ML) —
it does not strictly dominate. The A1 DISCIPLINE held (reported two-sided + honestly; the miss-side
null held; surfaced-not-silent; re-measured ONCE with population base-rate context at the user's call,
NOT iterated-to-fit against the oracle); only the predicted shape was replaced. The honest finding
VINDICATES propose→gate→decide — a sensitivity-rich PROPOSER, the deterministic engine + the human gate
supplying the population-calibrated discipline. See [[phase-85-base-rate-remeasure-not-overfit]] for the
mid-build remeasure call.
