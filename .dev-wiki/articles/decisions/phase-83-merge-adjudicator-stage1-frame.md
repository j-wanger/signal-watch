---
title: "Phase 83: build agentification Stage 1 — the merge adjudicator (the ONE oracle-scored gate)"
aliases: [phase-83-stage-1-frame, merge-adjudicator-frame, agentification-stage-1]
category: decisions
tags: [agentification, merge, oracle, measurement, sibling-stalled]
parents: [phase-83-merge-adjudicator-oracle-scored]
created: 2026-06-29
updated: 2026-06-29
source: implementation
confidence: high
---

## Context

After Phase 82 the local consume frontier is exhausted: both siblings are stalled at the Phase-82
pins (aml-substrate `294d3e5` / aml-casework `04cc335`, code-verified LIVE this session) with no new
emission to consume. The dominant ML §12 FILE-loop blocker (substrate Ask #3 — a second corroborating
leg as a fired signal) is substrate's work, and its handoff brief is already written. The question:
what is the highest-leverage signal-watch-INTERNAL forward move? The agentification roadmap
(`docs/agentification-roadmap.md`, authored post-Phase-82) sequences the next agentic loops by
leverage; Stage 1 (a merge adjudicator scored against the non-circular `GT-<hash>` oracle) is first.

## Decision

Build the agentification roadmap's **Stage 1**: a companion-only merge adjudicator agent that proposes
a merge call per case and whose judgment is MEASURED against the committed non-circular oracle in
`data/merge/cases.json`. The merge console is the ONE gate with a correctness oracle
(`resolution_scorer.py`, the resolver-input firewall enforced at the schema boundary), so this is the
only stage that can answer "how good is the agent, *really*?" with a measured agreement count. The
agent is deliberately thin (a proposer over the *built* scorer); the MEASUREMENT is the deliverable.
Mirrors the proven GATHER split (StubPlanner/LivePlanner + a `--check` harness).

Rejected: the durability CLAUDE.md hygiene trim (lower leverage — a scale/rigor frontier IS
available, and Jake picks rigor over durability when one exists). Waiting on substrate Ask #3 (that is
substrate's emission to make; our brief is written). Stages 2/3/4 of the roadmap (determination
pre-proposer / STR drafter / triage second-rater) — Stage 1 is highest-leverage AND uniquely
oracle-scored (the others are consistency-not-correctness measures).

## Consequences

- The merge adjudicator becomes the 5th companion live loop, sharing the one local-model transport
  (`127.0.0.1:8080`) with news/corpus/GATHER/DECIDE.
- The deliverable is a measured agreement count (counts-only, by quadrant + provenance, synthetic
  qualifier) — the credibility headline for the whole agentic story.
- The StubAdjudicator baseline (33/66, two-sided) ships unconditionally as a real measured result; the
  live agent capture is best-effort (needs a model) — never fabricated.
- Sets the template (a thin proposer + an oracle/consistency harness) for Stages 2–4.
- **OUTCOME (implemented 2026-06-29):** landed as the 5th companion live loop; a model WAS on :8080 so
  the live capture landed for real — the agent matched the oracle on 54 of 66 vs the spine's 33
  (recovering 21 of the 33 the spine got wrong: 18 of 30 fragmentation-gaps + all 3 over-merge-traps),
  0 deferrals, counts-only/synthetic-qualified. The credibility headline materialized; confidence → high.
