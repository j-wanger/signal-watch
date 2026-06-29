---
title: "Phase 85: build the §12 determination pre-proposer (Agentification Stage 2) — the only high-value LOCAL move"
aliases: [phase-85-direction, determination-pre-proposer, agentification-stage-2, sixth-live-loop]
category: decisions
tags: [agentification, determination, oracle, live-loop, measurement, companion, direction]
parents: [phase-85-determination-pre-proposer]
created: 2026-06-29
updated: 2026-06-29
source: plan
confidence: medium
---

## Context

Phase 84 closed the workbench render frontier; Phases 80–82 closed the local consume frontier. Every
remaining substrate-gated path is a VERIFIED dead-end at substrate HEAD `3716f77` (code-verified this
session, unchanged since Phase 84's pin): Ask #3 (a 2nd corroborating FILE-side leg) is a Phase-41
measured-null, Ask #4 (`ownership_edges`) is CLI-null, the merge org-collision class is one-sided
(P38 fragments share no resolution handle), and the open-reference-data fork's Stage 2 is unshipped.
So there is no new emission to consume and no new render to fix. The question: what is the
highest-leverage move that is LOCAL (does not wait on a sibling)?

## Decision

Build the agentification roadmap's **Stage 2 — the §12 determination pre-proposer** (the 6th live
loop): a companion agent that PROPOSES each case's determination (file / cleared / needs-more-info +
rationale) from the assembled §12 bundle evidence ONLY, MEASURED against the Phase-78 exogenous
`intended_disposition` oracle vs the deterministic sufficiency-engine baseline. It mirrors Phase 83
(the merge adjudicator, Stage 1) exactly — and every seam it needs already exists (the
`determine_case(named_risk=, mitigation_established=)` override, the non-circular oracle, the
`assert_no_oracle_leak` firewall, the replay-harness + build-stripped-overlay pattern).

Rejected: (a) an honest-determination-panel render — lower leverage, and a framing risk (≈358/376
slice cases resolve to needs-more-info, so a bulk-determination panel screams "the engine can't
decide"); the agent measurement is the more honest frame for the same surface. (b) Stage 3 (a real
STR drafter) — roadmap-sequenced AFTER Stage 2. (c) hold-for-substrate — there is no new emit, so it
is a zero-movement no-op (the documented "a pin re-ground alone is a no-op" lesson).

## Consequences

- The 6th live loop joins the five (news/corpus extraction · GATHER · DECIDE · the merge adjudicator),
  and the second oracle-SCORED agent (after Stage 1) — the agentification roadmap's next credibility
  data point.
- Companion-only: the workbench is never built into `dist/`, so all 9 ship dists are trivially
  byte-frozen; `evidence_requirements.py` stays byte-unchanged (the agent proposes, the engine
  licenses, the human decides). See [[phase-85-propose-gate-decide-a1-frozen]].
- The measured story is NOT a Phase-83-shaped "54-vs-33" recall-recovery — the headroom is on the
  over-flag (clear) side; the file-misses are honestly NULL (a DATA gap). See
  [[phase-85-over-flag-headroom-not-miss-recovery]].
- The local frontier after this is genuinely thin — the next legs (a real STR drafter, a §14 triage
  second-rater) and any miss-side gain are sibling-rooted or a later roadmap stage.
