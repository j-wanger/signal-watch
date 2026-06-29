---
title: "Phase 86 — Companion-only: measure the casework drafter + verifiers, do not modify them (no re-vendor; all 9 dists byte-frozen)"
aliases: [phase-86-companion-only, casework-unchanged, measure-dont-modify, a1-frozen-drafter]
category: decisions
tags: [agentification, stage-3, str-drafter, companion-only, casework, byte-frozen, a1-frozen, planning]
parents: [phase-86-str-drafter-consistency-measure]
created: 2026-06-29
updated: 2026-06-29
source: plan
confidence: medium
---

## Context

The drafter (Drafter Protocol) and its six grounding verifiers live in vendored aml-casework
(`vendor/aml-casework/`, `VENDORED_AT = 04cc335`, which equals the sibling HEAD `04cc335`, Phase 21 —
no newer drafter work landed). The phase MEASURES that built machinery; the temptation in a "make it
better" framing is to tune the drafter or the verifiers, which would be a code change to a vendored
dependency + a re-vendor + a possible dist or §12-funnel ripple. The propose→gate→decide invariant
(the agent drafts, the verifiers gate, the human signs) must hold exactly as in Stages 1/2.

## Decision

Companion-only invariants, all enforced as exit criteria + the abort rule:
- all 9 ship dists byte-frozen (`--check all` 9/9 — the workbench/chain are companion-only, touch no
  dist);
- build.py imports nothing new (a grep guard: `drafter_quality_harness` NOT imported by build.py);
- the vendored casework Drafter Protocol + the six grounding verifiers are UNCHANGED — we MEASURE
  them, do not modify (no re-vendor; pin stays `04cc335` == sibling HEAD; `git diff --quiet
  vendor/aml-casework` empty);
- `evidence_requirements.py` + the 256/376 §12 signing funnel UNTOUCHED (the drafter is the
  downstream DECIDE beat; `git diff --quiet scripts/evidence_requirements.py` empty).

The agent drafts, the six verifiers gate, the human signs — propose→gate→decide held.

## Consequences

Unlike Stages 1/2 (which added a firewall to hide a truth field), Stage 3 needs NO oracle firewall —
there is no truth to hide; the drafter sees the bundle evidence by design (it must, to draft). So the
harness is structurally simpler than the Stage-1/2 harnesses. Any casework src edit, a re-vendor, a
build.py companion import, a non-byte-identical dist, or an `evidence_requirements.py` / §12-funnel
change is an abort-and-surface event. The cost accepted: the phase cannot improve drafting quality —
it can only measure the existing machinery. That is the correct scope for a measurement-frame phase
(the deliverable is the measure, per [[phase-86-direction-str-drafter-measurement]]).
