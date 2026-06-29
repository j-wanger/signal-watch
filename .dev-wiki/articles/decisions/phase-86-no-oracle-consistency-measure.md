---
title: "Phase 86 — The STR drafter has NO correctness oracle; the measure is counts-only consistency, never an accuracy"
aliases: [phase-86-no-oracle, consistency-not-correctness, drafter-measure, no-gold-narrative]
category: decisions
tags: [agentification, stage-3, str-drafter, consistency-not-correctness, honesty, no-oracle, planning]
parents: [phase-86-str-drafter-consistency-measure]
created: 2026-06-29
updated: 2026-06-29
source: plan
confidence: medium
---

## Context

Stages 1 (merge adjudicator) and 2 (§12 pre-proposer) were each oracle-scored — they had a
measurable correctness ground truth (the merge `GT-<hash>` cluster oracle; the §12 exogenous
`intended_disposition` oracle). The STR drafter is the decisive break: it produces free-text prose,
and there is NO committed narrative reference to score that prose against. Its "gate" is the six
deterministic Class-G verifiers, which produce a binary signed/refused + `blocking_violations`
(citation grounding, corpus grounding, the fabrication guard) — faithfulness, NOT narrative quality.
A measure must replace the absent oracle without dressing a non-accuracy up as one.

## Decision

The measure is **counts-only consistency**, the roadmap's consistency-not-correctness class (the
GATHER harness is the model):
- **stub-vs-live SIGN/REFUSE** — does the live agent draft something the deterministic verifiers
  will sign, where the stub did/did not?
- **fabrication-guard CATCH count** — does the guard catch a hallucinated/ungrounded block
  (`blocking_violations`)?
- **grounding CONSISTENCY** — are claims grounded identically across stub and live?

It is NEVER reported as an accuracy / catch-rate / precision / recall — the verifier IS the
measurable gate, not a truth label. A hand-authored "gold narrative" oracle was REJECTED: a synthetic
gold is authorship judgment, not truth, and scoring prose against it carries overfit + authorship
bias + an honesty risk (presenting a synthetic gold as a correctness standard). User-positioned at
the gate (Q2 = Accept).

## Consequences

The drafter becomes the SECOND consistency-not-correctness harness (GATHER first), keeping the
program's evaluation discipline coherent: oracle-scored where truth exists, consistency where it does
not. No `--freeze` produces a fabricated correctness number — the worst honest outcome is a stub-only
baseline + a named live-capture follow-on. The honesty governor's word-ban
(catch-rate/lift/precision/recall) extends to the new markers + docs; every number carries the
synthetic-substrate qualifier. The trade accepted: the drafter headline cannot be a Stage-1/2-shaped
"agent matched N of M vs truth" — it is a consistency statement, which is the honest ceiling for
free-text drafting without a reference corpus.
