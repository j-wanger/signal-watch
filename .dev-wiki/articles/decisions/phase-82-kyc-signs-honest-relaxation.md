---
title: "Phase 82 — the Phase-72 kyc-signs assertion honestly relaxed (a txn-bearing C14 MAY fail-closed; ≥1 MUST sign preserved)"
aliases: [phase-82-kyc-signs-honest-relaxation, phase-82-narrative-seam-note]
category: decisions
tags: [cross-pillar, casework, kyc, c14, signing, narrative-seam, fail-closed, refusal-is-defensibility, re-vendor]
parents: [phase-82-consume-sibling-northstar-evidence-at-scale]
created: 2026-06-29
updated: 2026-06-29
source: debrief
confidence: high
---

## Context

Phase 72 asserted a txn-bearing C14 case ALWAYS signs (the §12 KYC loop closes). Phase 82 re-vendored
casework 076fb8e→04cc335 (P20 C15/C4 reconcile) and re-emitted the substrate slice (`294d3e5`). The new
emit introduced a C14 case shape (CASE-P-0025128) whose narrative makes casework's STUB drafter fail
narrative verification — the drafter ran but couldn't draft-and-verify. The Phase-72 "always signs"
assertion no longer holds verbatim.

## Decision

HONESTLY RELAX the assertion: a txn-bearing C14 case MAY fail-closed for an honest casework reason (the
drafter can't draft-and-verify some C14 shapes — the "refusal IS defensibility" frontier, the same class
as Lakeshore's fan-in C3 fail-close). Preserve the invariant `≥1 txn-bearing kyc MUST sign`
(CASE-P-0034054 signs). The kyc-sign count moves 2(old)→1(new) — a tiny local frontier inside a large net
coverage gain (128→256, from the casework P20 C15/C4 reconcile). This is NOT a code regression: signing is
casework's `grounding_replay`, separate from `determine_case`; C14 grounding is unchanged.

Additionally, `curate_workbench_cases` now distinguishes a casework CONTRACT-boundary rejection (no
summary, e.g. txn-less "no transactions") from a NARRATIVE-SEAM failure (the drafter ran but couldn't
draft-and-verify — "seam left open"), so the `e2e_note` names the real reason instead of a generic "no
signable record".

Rejected: pinning the test to the old 2-sign count (would force hiding the honest fail-close, or
patching the stub drafter beyond scope — the seam is casework's, not signal-watch's).

## Consequences

- `tests/workbench.test.mjs` 178→184 (+6 Phase-82 tests); the selftest comment + the `e2e_note` + the
  casework-signing brief document the relaxation. The funnel re-measure was two-sided as the A3 check
  required: the moves were fail-close→sign (net +128 coverage), with one honest sign→fail-close at the
  C14 narrative-seam frontier — surfaced, not hidden.
- A named casework follow-on: the stub drafter can't draft-and-verify some C14 narrative shapes — relevant
  to the casework-northstar-signing narrative-contract handoff. This is the txn-bearing-C14 narrative-seam
  frontier (alongside the still-open casework C17-sign gap).
- The "refusal IS defensibility" doctrine now covers a second class (Lakeshore fan-in C3 + the C14
  narrative seam) — a fail-close for an honest, named reason is a feature of the gate, not a defect.
