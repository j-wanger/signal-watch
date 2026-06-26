---
title: "The build-boundary validator must be in EXACT parity with curate's firewall"
aliases: ["validator parity", "build validator mirrors curate firewall", "MERGE_TRUTH_LEAK_KEYS parity"]
category: decisions
tags: [phase-76, merge-console, validator-parity, build-boundary, adversarial-review, honesty]
parents: [phase-76-merge-adjudication-console]
created: 2026-06-25
updated: 2026-06-25
source: debrief
confidence: high
---

## Context

Two validators enforce the merge console's honesty contract: `curate_merge_cases.py`'s firewall
(companion-side, at authoring time) and `build.py`'s `validate_merge_cases` (at the build boundary,
standalone). The STANDARD adversarial review found they had drifted: the shipping
(`validate_merge_cases`) validator was WEAKER than curate's — it omitted the `note` leak-key from
`MERGE_TRUTH_LEAK_KEYS` and did not enforce that REAL cases are `basis=strong` /
`spine_verdict=kept_distinct`. A weaker shipping validator is a silent honesty hole: a malformed or
truth-leaking case could pass the boundary even though curate would have rejected it.

## Decision

Bring the two validators into EXACT parity. Both were fixed: the build validator now includes the
`note` leak-key and enforces the real-case invariants (basis=strong / spine_verdict=kept_distinct).
The contract is: when an authoring tool and a build-boundary validator both enforce the same
firewall/closed-vocab contract, they must mirror each other exactly — the build boundary is the last
line of defense and must be no weaker than the authoring check.

## Consequences

The resolver-input firewall (no truth field in pre-adjudication evidence; the latent truth confined
to each scored case's revealed `oracle` block) is now enforced identically at both layers. This was
a should-fix from the adversarial review, resolved inline. General lesson recorded to memory: a
weaker shipping validator silently undermines an authoring-time firewall — keep paired validators in
exact parity. Confirms the ledger's A3/A5 assumptions (dist additive + boundary-validated;
build-time curation, no live spine) held, with this parity gap as the one found-and-fixed defect.
