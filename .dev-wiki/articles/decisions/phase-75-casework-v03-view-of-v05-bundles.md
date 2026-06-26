---
title: "casework gets the v0.3 VIEW of additive v0.5 bundles"
aliases: ["v0.3 view", "casework contract-version view", "relabeled contract_version"]
category: decisions
tags: [phase-75, cross-pillar, casework, contract-version, curate, additive-contract]
parents: [phase-75-consume-substrate-v05-er-emission]
created: 2026-06-25
updated: 2026-06-25
source: plan
confidence: high
---

## Context

Phase 75 bumps the curated bundles to substrate's contract v0.5 (additive: `display_name`,
`counterparty_name`, party `identifiers[]`, `RelationshipEdge.strength`, `resolution_edges[]`). But the
vendored aml-casework (HEAD `4a858e6`) still has `KNOWN_CONTRACT_VERSIONS=("0.1","0.2","0.3")` — it REJECTS
an unknown `contract_version` of `"0.5"` at its grounding boundary, even though it TOLERATES the additive
unknown fields ("validate the 16 known keys, tolerate unknown extra fields"). The `--measure-casework`
consume must stay green after the bump.

## Decision

curate hands the casework-facing copy a RELABELED `contract_version` of `"0.3"` — a v0.3 VIEW of the v0.5
bundle. The committed bundle stays v0.5 (it carries the real version for the spine/render path); only the
copy handed to the casework subprocess is relabeled. Casework grounds the identical v0.3 subset it already
knows; the additive v0.5 fields ride along untouched. Casework adding `"0.4"`/`"0.5"` to its
`KNOWN_CONTRACT_VERSIONS` is its NOT-BUILT side (named in the confidence-graded-resolution brief).

Alternative rejected: bump casework's `KNOWN_CONTRACT_VERSIONS` here — that's a sibling-repo change, out of
the companion-only scope; the consume must not depend on an unbuilt casework change.

## Consequences

- The `--measure-casework` consume stays green after the v0.5 bump with no sibling change.
- The relabel is a thin, named cross-pillar seam, not a contract fork — casework grounds the identical
  subset; the committed bundle remains the single source of the real version.
- The casework-side bump is a documented sibling follow-on (the confidence-graded-resolution brief, still
  NOT-BUILT at `4a858e6`).
