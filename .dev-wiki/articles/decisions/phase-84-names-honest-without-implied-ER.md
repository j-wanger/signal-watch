---
title: "Phase 84: surface counterparty names honestly — money-flow groups within-account/by-ref, never imply cross-account ER"
aliases: ["names-honest-without-implied-ER", "no-cross-account-ER-badge", "per-account-local-names"]
category: decisions
tags: ["workbench", "render", "honesty", "entity-resolution", "money-flow", "synthetic-qualifier"]
parents: ["phase-84-workbench-rich-case-render-at-scale"]
created: 2026-06-29
updated: 2026-06-29
source: plan
confidence: high
---

## Context

Surfacing the emitted `counterparty_name` makes the money-flow graph tempting to draw as a
cross-account entity network — node "Lucas Ahmed" linking every account that transacts with a
counterparty of that name. But substrate's counterparty names are per-account-LOCAL synthetic names:
there is NO cross-account entity resolution behind them. Drawing them as a resolved network would
imply an ER capability the data does not have — and loosened name matching WITHOUT identifier layering
explodes false positives >90% (the wiki ER discipline, [[wiki:entity-resolution-and-network-analytics]];
the Phase-82 merge-org-abort applied the same caveat).

## Decision

**Surface the names, but the money-flow graph groups WITHIN-ACCOUNT / by-`counterparty_ref` with an
explicit honesty badge** — never imply cross-account entity resolution. The badge names the limit:
counterparty names are per-account-local synthetic names; no cross-account ER is performed.

The multi-hop BO CHAIN degrades honestly to flat named BO with a "single-hop; multi-hop ownership
chain pending substrate emission (Ask #4)" marker (see [[phase-84-decisiveness-substrate-gated]]).

No fuzzy name-matching is added in any new render — the >90%-FP discipline holds.

## Consequences

- The names are honest evidence (real emitted data), not a fabricated network claim. The badge keeps
  the render compliance-clean alongside the always-on "Illustrative data & outputs" badge and the
  synthetic-substrate qualifier.
- The resolution graph renders from substrate's OWN emitted `resolution_edges` (a measured edge set,
  not a render-side inference) — that IS honest cross-reference; the money-flow grouping is the part
  that must not over-claim.
- The honesty governor extends to the new render markers: counts-only, synthetic-substrate-qualified,
  the word-ban (no catch-rate/lift/precision/recall).
- High confidence: this mirrors the established merge/ER discipline already enforced across Phases
  76-82; it is the project's standing rule applied to a new surface, not a new judgment call.
