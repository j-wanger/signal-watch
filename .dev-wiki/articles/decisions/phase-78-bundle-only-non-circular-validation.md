---
type: decision
slug: phase-78-bundle-only-non-circular-validation
title: "Score the bundle-only signal structure, not the human-gated verdict — the non-circular validation frame"
phase: 78
status: accepted
confidence: high
source: plan
created: 2026-06-26
tags: [cross-pillar, determination-engine, firewall, circularity, validation-harness, honesty]
---

# Decision — bundle-only, non-circular validation

**Context.** Substrate Phase 31 wired `eval/intended_disposition.json` (`file`|`clear`, authored blind
to the sufficiency rule). The Phase-77 merge-66 consume died at the abort rule because its oracle was a
relabel of the system-under-test's own decision key (circular). The disposition oracle must NOT repeat
that.

**Decision.** The harness scores the **bundle-derived** part of the determination — mechanism present +
≥2 corroborating legs (the §12 signal layer) — against the oracle. The **human-gate inputs**
(`named_predicate_risk`, mitigation) are **held out and named as the boundary the harness does not
cross**; they are NEVER derived from the oracle `intended_basis` (that would re-introduce circularity
via the detector↔basis correlation). The oracle label never enters any engine input
(`assert_no_oracle_leak`, mirroring `resolution_scorer.assert_no_cluster_leak`).

**Why non-circular (unlike merge-66).** The oracle is authored from the latent laundering process,
blind to `evaluate_sufficiency`; the engine reads only bundle signals. Neither reads the other →
disagreement is meaningful. This is the genuine "circularity exit."

**Why not the full gated verdict.** Rejected at the direction gate: feeding the human-gate inputs from
a deterministic policy correlated with the oracle basis would make the agreement true-by-construction.
The bundle-only frame measures the honest thing — whether the signal-assembly pre-positions the file
decision — and reports the held-out gate as the boundary.

**Consequence.** The deliverable is a per-class **confusion structure** (signal-file-ready × oracle
file/clear), not an accuracy (the oracle is overwhelmingly clear — 6814 of 6935 — so accuracy is trivially gamed). Synthetic-only
qualified; no catch-rate/precision/lift wording.

Related: [[decisions/phase-78-measure-then-control-discovery-feed]] · the Phase-74 priors-are-provenance
guard · the Phase-77 circular-oracle abort.
