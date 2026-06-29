---
title: "Phase 85: the agent provably never sees intended_disposition — non-circular by construction (the Phase-77 trap avoided)"
aliases: [phase-85-oracle-firewall, non-circular-determination, proposer-input-strip, no-oracle-on-the-wire]
category: decisions
tags: [agentification, determination, firewall, oracle, non-circular, measurement, honesty]
parents: [phase-85-determination-pre-proposer]
created: 2026-06-29
updated: 2026-06-29
source: plan
confidence: medium
---

## Context

A measurement against a truth label is only meaningful if the system under test never saw that label.
Phase 77 learned this the hard way: the merge oracle was content-addressed `ENT-<entity_ref>` (1:1 with
the spine's own key) → any score was circular, true-by-construction. Phase 78 then established the
NON-CIRCULAR exogenous `intended_disposition` oracle (authored blind to the sufficiency rule) plus the
`assert_no_oracle_leak()` allow-list firewall, and Phase 83 carried the same firewall onto a served
agent path. The §12 determination pre-proposer must hold the same property: the agent that proposes
file/cleared/needs-more-info must provably NOT have read `intended_disposition`.

## Decision

Hold the oracle firewall as a NON-NEGOTIABLE constraint, asserted at three layers:
1. `proposer_input()` strips the bundle to the evidence surface (grounded predicate + mitigation +
   legs + KYC) and excludes `intended_disposition` (and any sibling truth field).
2. `assert_no_oracle_leak()` RAISES on any truth field in the proposer input, reusing the Phase-78
   allow-list (do not re-implement the strip).
3. The served `/propose-determination` response carries NO oracle field on the wire — the oracle
   reaches the client only post-decision, exactly as the static page already does.

Asserted in `determination_proposer --selftest`, `serve_workbench --selftest`, and
`workbench.test.mjs`. The measurement is non-circular BY CONSTRUCTION — the score cannot be a tautology
because the label is unreachable from the proposer's input.

Rejected: trusting that the agent "wouldn't use" a present truth field (the Phase-77 trap dressed up);
a post-hoc audit instead of a structural strip (catches a leak after the fact, not by construction).

## Consequences

- The Phase-85 measured number is defensible as a real measurement (the agent earned the agreement, it
  did not echo the label).
- The firewall is the A4 ledger row, in the abort rule: any oracle leak into the proposer input or onto
  the wire pre-decision → STOP-and-surface.
- The reuse of the Phase-78 allow-list + the Phase-83 served-firewall pattern means the firewall is
  proven machinery, not new — lower implementation risk.
