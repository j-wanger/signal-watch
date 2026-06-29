---
title: "Phase 82 — the §12 loop closes from GROUNDED bundle evidence (P39 predicate + P40 mitigation as DATA, rule frozen)"
aliases: [phase-82-grounded-evidence-consume, phase-82-predicate-mitigation-data]
category: decisions
tags: [cross-pillar, consume, substrate, predicate-reference, mitigation-evidence, determination, a1-guard, evidence-as-data, scale]
parents: [phase-82-consume-sibling-northstar-evidence-at-scale]
created: 2026-06-29
updated: 2026-06-29
source: debrief
confidence: high
---

## Context

The GENERATED 376-case slice carried mechanism signals but no decision-layer evidence — Phase 78
measured a **0-of-376** named-predicate gap, so no slice case could reach the FILE bar and no case
could affirmatively CLEAR (only clear-by-absence). substrate Phases 39/40 emit exactly that missing
evidence: `reference.named_predicate_risk` + `prior_str_register[]` (a `flagged` resolution edge) and
`mitigation_evidence{established, basis, corroborants[]}`. The question was HOW to consume it without
violating the A1 guard (`evidence_requirements.py` BYTE-UNCHANGED — the sufficiency rule must not be
silently weakened). A code check confirmed the engine ALREADY exposes the `named_predicate_risk` +
`mitigation_established` params (`evidence_requirements.py` line 310-312) — the params exist; only the
DATA was missing.

## Decision

Consume P39 predicate + P40 mitigation as **bundle DATA read by `serve_workbench.determine_case`** (a
new `_bundle_evidence` reader that lifts the predicate from the `flagged` edge + the mitigation block
from each case's substrate bundle), NOT as a rule edit. The engine derives legs from capabilities and
never sees provenance; the read-from-a-record evidence flows in as the params the frozen engine already
consumes. The human still adjudicates the disposition — the predicate/mitigation are grounded, not
analyst-typed. Proven non-degenerate by a rigorous with/without-`determine()` regression (the Phase-81
C17 lesson: measure on the real engine, never a coverage proxy).

Rejected: **editing the engine rule** to admit the new evidence (an A1 violation — the params already
existed, so no edit was warranted). Rejected: **re-attempting the C17 leg** (degenerate, label-blind,
corr≈0 — Phase 81 established it is structurally an observable, not a determination leg).

## Consequences

- On the 376-case slice the §12 loop closes from read-from-a-record evidence at scale: **1 KYC-integrity
  determination** (grounded prior-STR predicate; 31 over the full 23,651-customer population) + **17 ML
  affirmative `cleared`** (reconciled source-of-funds — the Lakeshore "source of funds is the difference"
  thesis at scale), up from 0/0.
- `evidence_requirements.py` BYTE-UNCHANGED (`git diff --quiet`) — the A1 guard holds by construction;
  the predicate/mitigation are DATA the frozen engine reads. A case carrying BOTH a predicate and a
  mitigation is NOT cleared (the prior-STR predicate blocks the affirmative clear — the rule already
  encodes this).
- `workbench.html` `paintDet` gained the grounded-evidence panel + the `cleared` verdict branch
  (`.detv.clear`); slice cases that affirmatively clear now render a documented-dismissal (was
  mis-rendered as needs-more-info).
- The ML FILE loop stays blocked — 0 slice ML cases reach the bar because they lack a SECOND
  corroborating leg as a fired signal (substrate Ask #3, the dominant blocker, named as the next
  highest-leverage substrate emission).
