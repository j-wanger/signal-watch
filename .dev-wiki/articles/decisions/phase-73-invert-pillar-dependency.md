---
title: "Phase 73 direction: invert the pillar dependency — signal-watch authors the north-star rich case first, substrate/casework parked"
aliases: ["invert pillar dependency", "north-star rich case first", "artifact is the spec"]
category: decisions
tags: [phase-73, cross-pillar, rich-case, north-star, reframe, casefile, companion]
parents: [phase-73-rich-investigation-case-live-workbench]
created: 2026-06-23
updated: 2026-06-23
source: plan→delivered
confidence: high
---

## Context

The Phase-71/72 workbench cases were a real (synthetic) aml-substrate population, but the user's
reframe at the Phase-73 gate judged them "not it" as a stakeholder-buy-in artifact: all C2/C3 with
synthetic ids, raw C-codes on screen, no counterparty/identity/network layer, and an STR that drafts
without the information a filer would actually have. The cross-pillar program (substrate emits →
casework signs → signal-watch demos) had been running substrate-first: signal-watch consumed what the
siblings happened to emit. That ordering is why the demo data is thin — the rich identity/network
layer the north-star demo needs was never on any sibling's roadmap.

## Decision

INVERT the pillar dependency. Signal-watch AUTHORS the north-star rich investigation case FIRST as a
concrete artifact; aml-substrate + aml-casework are PARKED this phase and become downstream
implementers that build toward the authored shape. **The artifact is the spec** — the cross-pillar
contract (what substrate must EMIT and casework must SIGN to make the case real-not-authored) is a
DEFERRED follow-on doc (`docs/rich-case-target-contract.md`), written only after the data model
survives implementation. Alternatives rejected: keep consuming substrate emissions (the source of the
thin-data problem); spec the pillars first (a guess before the data model is proven — CRITIQUE-3's
"don't write the contract before the artifact").

## Consequences

- The phase touches NO sibling code (A6); substrate/casework stay at their current pins.
- The rich case is authored synthetic data (`data/casefile/**`) shaped to the LIVE engine's real
  verdict vocab — a scripted dramatization, the project's core posture (CLAUDE.md line 1).
- The cross-pillar handoff becomes a named follow-on; the data model authors ALL fields now (the
  follow-on contract is documentation-only, the pillars then build to it).
- The follow-on phase has a proven data-model shape to write the contract against — no re-derivation.
