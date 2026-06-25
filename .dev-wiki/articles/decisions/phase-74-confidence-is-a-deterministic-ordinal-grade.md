---
title: "Phase 74: confidence is a deterministic ordinal grade, never a fabricated score"
aliases: ["confidence ordinal grade", "strong weak reject grade", "no fabricated match score", "deterministic linkage strength"]
category: decisions
tags: [phase-74, entity-spine, confidence, entity-resolution, honesty-governor, identifier-grammar]
parents: [phase-74-entity-intelligence-spine]
created: 2026-06-25
updated: 2026-06-25
source: plan
confidence: medium
---

## Context

The spine must carry "confidence" on a resolved entity. The honesty governor (memory
[[honesty-over-demo-drama]]) and a direct precedent — `news_store` keeps `confidence` RESERVED/NULL
by explicit decision because a model-emitted confidence is "a fabricated-shaped number" — forbid
inventing a probabilistic match score on synthetic data with no ground truth. But the casefile pair
already carries an identifier grammar (email/phone marked `strong`, address `weak`, name-only
EXCLUDED — the `E-CALDERON` case) that IS a defensible confidence basis. The wiki ER frame is the
backing: loosening match rules WITHOUT identifier layering pushes false positives >90%; identifiers
resolve, name is a weak observation.

## Decision

Confidence is a **deterministic ordinal GRADE** — `strong` (exact email/phone/identifier match),
`weak` (address), `reject` (name-only) — derived from the identifier grammar, never a
probabilistic/model score. A probabilistic score is admissible ONLY when measured against
`true_entities` (the T3 scorer contract), and even then it is synthetic-only and never reads as
production-trustworthy. The grade **fails closed**: an unknown/missing grade (and a null `basis[]`,
its proxy) is treated as weakest → its inherited evidence is EXCLUDED, not down-weighted (a frozen
boolean filing engine cannot express "but the link is weak"). Alternatives rejected: a probabilistic
match float now (the fabricated-shaped-number trap; no ground truth to calibrate it); down-weighting
low-grade evidence (the boolean engine can't carry a weight — exclude-not-downweight).

## Consequences

- The grade vocabulary `{strong, weak, reject}` is authored ONCE in the standards (T1) and used
  identically across the spine, the gate-gated read path, and the three sibling briefs (a grep
  consistency check is the T1 success criterion).
- A minimal scorer is proven HERE (T3) over a tiny synthetic `true_entities` so the
  probabilistic-only-if-measured rule is demonstrated, not just asserted — with the
  "synthetic-only; production has no ground truth" qualifier mandatory on every number.
- Missing/unknown is the safe default everywhere: fail-closed-to-weakest means a never-seen
  counterparty reads "we know nothing yet", never a falsely-confident empty network.
- News_store's reserved-confidence decision is HONORED, not contradicted — the spine adds a grade
  where it has a deterministic basis; it does not retrofit a score onto news.
</content>
</invoke>
