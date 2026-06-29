---
title: "Phase 84: slice cases will LOOK like northstar after names but NOT RESOLVE like northstar — decisiveness is substrate-gated"
aliases: ["decisiveness-substrate-gated", "look-not-resolve", "ask-3-ask-4-gated"]
category: decisions
tags: ["workbench", "northstar", "cross-pillar", "substrate-handoff", "out-of-scope", "render-vs-decide"]
parents: ["phase-84-workbench-rich-case-render-at-scale"]
created: 2026-06-29
updated: 2026-06-29
source: plan
confidence: high
---

## Context

After surfacing emitted names the slice cases will VISUALLY resemble the authored Northgate/Lakeshore
pair (named ledger, money-flow + resolution graphs). The tempting next step is to make them also
RESOLVE like northstar — FILE/CLEAR with a decisive verdict. The user was positioned on this and chose
"also re-sharpen the substrate brief" (scope = render-parity; decisiveness = re-sharpen-the-handoff,
not build it here).

## Decision

**Decisiveness is explicitly OUT OF SCOPE for this phase — it is substrate-gated.** Slice cases will
LOOK like northstar but will NOT RESOLVE like northstar:

- **Ask #3 (the 2nd corroborating FILE-side leg) is a Phase-41 MEASURED-NULL** — "no faithful,
  non-vacuous, launderer-flipping second leg exists on the current substrate." The ML FILE loop stays
  at DELTA=0 (Phase-82 finding: 0 slice ML cases reach the file bar; they lack a second corroborating
  fired signal).
- **Ask #4 (`ownership_edges`, multi-hop BO) is confirmed CLI-NULL** — absent from
  `src/aml_substrate/`, probe/test-only — the exact blocker the multi-hop BO render just hit (0/376
  ownership_edges). Verified at substrate HEAD `3716f77`.

Instead of building decisiveness, this phase **re-sharpens the handoff**:
re-ground `docs/substrate-northstar-evidence-emission-PLAN-BRIEF.md` against verified HEAD `3716f77`
(Ask #3 = Phase-41 measured-null; Ask #4 = CLI-null).

## Consequences

- This is a RENDER phase, not a §12/determination phase — `evidence_requirements.py` byte-unchanged,
  the 256/376 casework signing funnel byte-unchanged (the A1 guard + dist boundary).
- The named handoff (re-sharpened brief) is the deliverable for the decisive half — substrate's work,
  not signal-watch's. The render gives the visual parity; substrate gives the resolution parity.
- High confidence: both Asks were code-verified at substrate HEAD; the gap is real and named, not
  speculative.
- Avoids the Phase-81/82 trap of forcing a degenerate decision advance on label-blind data (corr≈0) —
  decisiveness on the current slice has no faithful mechanism; surfacing it as a FILE/CLEAR verdict
  would fabricate a resolution the data does not support.
