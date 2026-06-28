---
title: "Phase 81: The C17 exposure leg is consumed A1-preserving as an EVIDENCE atom — the sufficiency rule stays byte-frozen, verdict drift is intended §12 breadth"
aliases: [phase-81-exposure-evidence-advance, c17-leg-rule-frozen]
category: decisions
tags: [cross-pillar, consume, substrate, c17-exposure, exposure-via-ownership, a1-guard, evidence-requirements, determination-bar, sufficiency, double-count]
parents: [phase-81-consume-substrate-sanctions-arc]
created: 2026-06-28
updated: 2026-06-28
source: plan
confidence: medium
---

# Decision — the C17 exposure leg is an evidence-advance with the sufficiency rule frozen

## Context

substrate Phase 36 (`1651b1e`) adds the C17 exposure-via-ownership leg: a corroborating determination leg
that fires when a customer's beneficial owner / controlled entity carries a `sanctions_flag`, walked over
the BO `RelationshipEdge` graph. Consuming it touches the §12 determination loop — the most A1-sensitive
surface in signal-watch. The risk: a new leg that lets cases reach the determination bar could be a silent
bar-weakening dressed as breadth. Two structural facts shape the consume. **First,** substrate's emission
boundary is `SCREENING_EMISSION_DETECTORS` = C8 + C14 only; the C17 detector is NOT in the emitted bundle
(it READS, never generates), so signal-watch COMPUTES the exposure leg itself from the rendered
`related_parties[]` + `sanctions_flag`. **Second,** the engine derives legs from capabilities via profile
DATA: `evidence_requirements.determine` → `present_atoms()` reads `data/workbench/evidence-requirements.json`
and counts `kind=="leg"` atoms; the engine never sees provenance. Substrate also warns explicitly about a
double-count: the C17 exposure leg and a C14 escalation leg tracing to the SAME OFAC hit are NOT two
independent legs.

## Decision

Consume the C17 exposure leg **A1-PRESERVING, as a new EVIDENCE atom** — the sufficiency RULE stays
byte-frozen, the new evidence advances cases that genuinely present ≥2 independent legs:

- The leg is **profile DATA** (a new `kind=="leg"` atom in `data/workbench/evidence-requirements.json`) +
  **companion-side assembly** in `serve_workbench` (it computes the exposure leg from `related_parties[]` +
  `sanctions_flag`) + the **same-OFAC-hit double-count dedup** in the consume layer (where provenance
  exists). Because the engine derives legs from capabilities via `present_atoms()` and never sees
  provenance, `scripts/evidence_requirements.py` stays **byte-frozen** (the A1 guard, `git diff --quiet`).
- The sufficiency RULE (mechanism + ≥2 independent legs + named predicate + no unrebutted mitigation) is
  **byte-unchanged**. Cases that NEWLY reach the bar do so by genuinely presenting ≥2 INDEPENDENT legs.
- **Verdict drift on sanctioned-BO cases is the intended §12 BREADTH, NOT a bar weakening.** This is proven
  by a **determination-bar regression**: the case reaches the bar WITH the leg and is WITHHELD without it;
  the exposure leg + a same-hit C14 escalation count as ONE leg (the dedup enforces independence).
- The advance is reported measure-first as COUNTS (the honesty governor: never a catch-rate / lift /
  precision / recall).

Direction gate: Q3 "Evidence-advance, rule frozen" (AskUserQuestion 2026-06-28).

**Alternatives rejected.** (a) **Strict no-verdict-drift** (the leg fires but never moves a case to the
bar) — the isolated leg would feel contrived and yield less §12 breadth; the program thesis is precisely
that genuinely independent corroborating legs let a case cross the bar. (b) **Engine-owns-it, relax A1**
(let the engine read the exposure provenance directly, accepting an `evidence_requirements.py` change) —
unnecessary: the consume-layer boundary (profile-data atom + companion assembly + same-hit dedup) holds the
independence invariant without touching the frozen file bar.

## Consequences

`scripts/evidence_requirements.py` stays byte-unchanged (the A1 guard); the C17 leg lives entirely in
profile data + the companion assembly layer + the same-hit dedup. The §12-breadth beat is genuine — a
sanctioned-BO case reaches the determination bar via ≥2 INDEPENDENT legs, proven by the determination-bar
regression (WITH the leg reaches the bar; WITHOUT it is withheld; exposure + same-hit C14 = one leg). This
consume is **gated on T1b measure-first**: if the exposure cohort is degenerate (fires on too few /
already-determined cases), the leg ships as a rendered observable + a brief (an honest null) rather than a
false §12-advance claim. casework (`076fb8e`) does NOT ground C17 → a sanctioned-exposure case may
DETERMINE (signal-watch engine) but not SIGN through casework (the Lakeshore-C3 fail-closed class); the
determination is the demo beat, the casework SIGN gap is a NAMED handoff, not a phase blocker. The
double-count independence rule (distinct legs only when they trace to DISTINCT sanctioned parties) is a
durable constraint for any future exposure-style leg.

## OUTCOME — overtaken by the T1b measurement (2026-06-28)

This direction decision (ship the C17 leg as an evidence atom, A1-preserving) was **overtaken by the T1b
measure-first result.** The rigorous engine-based measurement (the T4 surface-map workflow caught a planning-stage
loose-proxy error in my T1b estimate) showed the C17 leg moves **0** sanctioned-BO cases to the determination bar —
the 13-case cohort carries only C8/C14 (a leg / kyc), **no money-laundering mechanism** (C2/C3/C5/C4), so a *leg*
can never satisfy `mechanism + 2 legs`. **DEGENERATE.** Per the user's "accept both abort fallbacks" + a re-asked
disposition (AskUserQuestion 2026-06-28), the C17 consume shipped **OBSERVABLE-ONLY** instead — a
`/sanctions-c17-exposure` route + panel surface the exposure and the live engine SHOWS the case does NOT reach the
bar; **no profile atom is added** (so A1-preservation is now trivial — `evidence_requirements.py` AND
`data/workbench/evidence-requirements.json` both byte-unchanged). The determination-leg consume is DEFERRED to a
discriminating exposure signal (`docs/substrate-exposure-signal-PLAN-BRIEF.md`). The bar-invariant reasoning below
remains the correct *design* (had the leg fired, it would be an evidence atom on the frozen rule) — it simply never
fired on label-blind data (`corr(flag, illicit) ≈ 0`).

Related: [[phase-81-consume-substrate-sanctions-arc]] ·
[[decisions/phase-81-consume-sanctions-arc-all-three]] ·
[[decisions/phase-74-priors-are-provenance-not-a-signal-file-bar-byte-identical]] ·
[[decisions/phase-73-affirmative-clear-verdict-file-bar-unchanged]].
