---
title: "Phase 74: priors are provenance, not a signal — confidence on a separate path, the file bar stays byte-identical"
aliases: ["priors are provenance not signal", "self-confirming loop guard", "file bar byte-identical", "grade-gated read path", "exclude not downweight"]
category: decisions
tags: [phase-74, entity-spine, file-bar, a1-guard, self-confirming-loop, evidence-requirements, honesty-governor]
parents: [phase-74-entity-intelligence-spine]
created: 2026-06-25
updated: 2026-06-25
source: plan
confidence: medium
---

## Context

The spine accumulates prior dispositions and a graded confidence on each entity. Two failure modes
threaten the frozen filing engine. (1) The self-confirming loop: if `evaluate_sufficiency()` reads a
prior `cleared`, "previously cleared" clears again — the store becomes a feedback loop that launders
its own past decisions. (2) The frozen-boolean problem: `evidence_requirements.py`'s file/determination
bar is byte-frozen (the Phase-73 A1 guard, asserted by its `--selftest`) and is pure-boolean — it
literally cannot express "but the identity link is weak", so a low-grade inherited atom that reaches
the decision inputs would silently over- or under-fire.

## Decision

Priors and accumulated history are **analyst-visible provenance ONLY** — the filing engine never
reads them. Confidence rides a **SEPARATE grade-gated read path**: the engine consumes a grade-gated
VIEW where any atom inherited across a link below a declared grade is EXCLUDED (not down-weighted),
and each decision emits an inspectable manifest of atoms admitted vs quarantined-by-low-grade. The
file/determination bar in `evidence_requirements.py` stays BYTE-IDENTICAL — confidence routes AROUND
it, never through it (if wiring requires ANY change to `evaluate_sufficiency()` → STOP-and-surface).
A regression assertion proves injecting a prior `cleared` disposition yields a byte-identical
file/clear verdict for a fixed evidence set. This mirrors the Phase-73 affirmative-clear
separate-path discipline (a new path that never loosens the bar). Alternatives rejected: feed priors
as a sufficiency leg (the self-confirming loop); down-weight low-grade atoms inside the engine (the
boolean engine can't carry a weight, and it would mutate the frozen bar).

## Consequences

- The A1 file-bar guard from Phase 73 is RE-ASSERTED and extended: `evidence_requirements.py
  --selftest` passes unchanged PLUS the new inject-a-prior-`cleared`→byte-identical assertion.
- The grade gate is fail-closed + inspectable: unknown/missing grade → weakest → excluded → listed
  in the manifest as quarantined-by-low-grade (the auditor can walk file/clear down to the link that
  supplied each admitted atom).
- The memory demo's short-circuit must therefore be a MEASURED drop in gather targets-to-close
  (prior-attached atoms make `present_before` already sufficient), NOT a status flag or a prior fed
  to the bar — the persistence proves itself without steering the verdict.
- The honesty seam holds: a richer accumulated history changes what the analyst SEES, never what the
  engine DECIDES — "the file bar is provably the same bar".
</content>
</invoke>
