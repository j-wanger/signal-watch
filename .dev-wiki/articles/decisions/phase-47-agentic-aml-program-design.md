---
title: "Phase 47: Demo-to-program design — the regulatorily defensible agentic AML program"
aliases: [phase-47-direction, agentic-aml-program-blueprint, gate-console]
category: decisions
tags: [program-design, model-risk, sr-11-7, osfi-e-23, gate-taxonomy, human-in-the-loop, agentic-operating-model]
parents: [phase-47-agentic-aml-program-design]
created: 2026-06-12
updated: 2026-06-12
source: plan
confidence: high
---

## Context

The 2026-06-11 bank-stakeholder presentation was a huge success. At the Phase-47 dev-plan gate the
user reframed (6th reframe at a gate) off the DEFERRED list to a direction-setting objective: turn
the vision demo into the design of a REAL program — "efficient, effective, and regulatorily
defensible" — built on the demo's pipeline patterns, with a target operating model of ~95% agentic
work + 5% human work where the human 5% is the important, interesting layer: pipeline
conceptualization, judgment calls on decisions, and non-binary ("art-like") gate decisions.

User direction at the Step-9 gate questions: deliverable = engineering blueprint PLUS an interactive
artifact in the project's own idiom; regulatory anchoring = SR 11-7 (held in the aml-wiki) layered
with OSFI E-23 (audience's regulator; currently a wiki GAP — research first); ceremony = STANDARD
(escalated from lite for this direction-setting phase).

## Decision

**D1 (DIRECTION):** Phase 47 = a program-design phase, not a code-feature phase. Deliverables:
(a) an engineering **program blueprint** (docs/), (b) a **gate console** interactive vision artifact
dramatizing the non-binary human judgment gate, (c) the OSFI E-23 knowledge gap closed in the
aml-wiki before the design hardens.

**D2 (DESIGN SPINE — the 5% first; A1 REJECTED-BY-REFRAME → A1′ at the gate):** The blueprint's
spine is a **universal grounding principle + gate taxonomy + human-work charter**, not a
breadth-first target-operating-model essay. The user's reframe (gate, 2026-06-12): grounding is
UNIVERSAL — what varies per workload is the grounding SUBSTRATE, and therefore the deterministic
verifier implementation. Derivation grounds to advisory text (substring verifier); transaction
monitoring grounds to the committed SIGNALS + the transactional/non-transactional data supporting
them (referential/lineage verifiers); SAR/STR narratives ground to guidance, policies, signals, and
data (citation verifiers). The "quote" generalizes from text-substring to traceable-reference-into-
the-substrate; grounding CHAINS (monitoring grounds to signals that were themselves grounded to
advisories) and defensibility is the audit walk down the chain. Nothing ungrounded survives a gate.
On top of the grounding layer the taxonomy keeps: measured dimensions (blind inter-rater,
regression-vs-baseline), human-judgment gates (non-binary, graded dispositions with captured
rationale), and mandated-accountability review. The original T0 risk survives as a design check:
each workload's substrate + verifier must be NAMED, never assumed (the substring verifier itself
does not transfer; the principle does).

**D3 (AGENTIFICATION CRITERION):** The freshly-captured agent-runtime-adoption-probe rule becomes the
program-wide criterion: a component is agentified only where a direct deterministic/single-shot
baseline measurably leaves recoveries on the table (A/B probe first); otherwise the loop's one good
idea is folded into the deterministic pipeline. Constraints inherited from the news-lift FINDING:
every agentic loop carries a max-iteration cap, and gates must surface ALL scored dimensions
(an agent optimizes only what the gate report shows — unsurfaced dimensions silently regress).

**D4 (REGULATORY ANCHOR):** Layered — SR 11-7 / 2021 interagency statement as the structural
backbone (model inventory, three pillars, alternative validation under no-ground-truth), OSFI E-23
as the audience-jurisdiction anchor (researched via /wiki-bootstrap focus topic before the design
hardens). FINTRAC obligations stay the content-domain layer.

**D5 (HONESTY TRANSITION):** The demo's honesty constraints are explicitly dispositioned in the
blueprint — which survive verbatim into the program (no fabricated numbers; provenance-per-decision;
illustrative-vs-real labeling), and which transform (the "Illustrative data & outputs" badge becomes
an outcomes-analysis / ongoing-monitoring obligation when outputs become real). Applied to the
phase's OWN headline: "95/5" is a design DIRECTION (automate-by-default, judgment-by-design), never
a stated target ratio; if a ratio ever appears it carries its future measurement definition
(decision-volume share per gate class) — the Phase-45 fake-lift deletion pattern applied forward.

### Approach-review revisions (Step 12, score 7/10 revise — incorporated)

- **Sequencing:** E-23 research is strictly first (bar: E-23 lifecycle stages mapped against
  SR 11-7's pillars — "good enough to harden the spine"); the blueprint core next; the gate console
  LAST behind a mid-phase checkpoint with an MVP of ONE gate class (C/D tag adjudication) and a
  named descope path (Phase 47b) if the blueprint consumes the budget.
- **Charter breadth (4th class):** the gate taxonomy gains a MANDATED-ACCOUNTABILITY human class
  (SAR sign-off, board/model-governance attestations — compulsory under SR 11-7 Pillar 3 / three
  lines of defense, regardless of judgment-need). The 5% charter designs BOTH the art-like judgment
  work and the compulsory accountability work; an interesting-only charter under-counts the human
  layer and leaves an examiner-visible hole.
- **Validation story NAMED:** the blueprint carries a drift / ongoing-monitoring section with an
  explicit disposition (designed-now vs deferred-with-owner) for the no-ground-truth problem; the
  committed quality-harness baseline (--check / --freeze) is the embryo of exactly this control.
- **Gate console data provenance:** the console runs on a COMMITTED, licence-clean, curated
  divergence dataset (promoted or deterministically regenerated — never a `.dev-wiki/tmp/`
  dependency); it inherits the always-on illustrative badge + the Phase-28 FINTRAC footer-attribution
  mechanism; graded dispositions come from the PRESENTER, never a synthesized judgment score (real
  measured agreement numbers are safe to show; a fabricated graded scale is not).
- **D3 caveat preserved:** the program-wide criterion is the PROBE itself, not the Phase-46 outcome
  (n=1, conditional verdict) — blueprint text keeps the inbox entry's own caveat.
- **HANDOFF charter:** the blueprint dispositions HANDOFF's "ships a demo, not a system" mandate in
  one explicit line (transcended under user override at this gate) so future sessions don't read a
  silent contradiction.

Alternatives considered: stakeholder-facing proposal first (rejected — engineering blueprint is the
source of truth; a digest derives later); SR 11-7-only anchoring (rejected — wrong jurisdiction for
a Canadian-bank audience); pure design doc without artifact (rejected by the user — the project
communicates through vision artifacts); breadth-first whole-program architecture (rejected per T0
alternative framing — the gate taxonomy is the load-bearing part).

## Consequences

- The repo gains its first design-phase deliverable class (blueprint doc + spec contract under
  standard ceremony); ship artifacts and all committed data/dist remain FROZEN.
- The gate console becomes the FOURTH vision artifact (same single-file offline idiom), dramatizing
  graded human dispositions over real pipeline output (e.g. C/D tag adjudication, alias-ownership
  calls, inter-rater divergences — the measured-not-gated dimensions).
- The DEFERRED candidate list is re-sequenced in the blueprint as program-capability roadmap input
  rather than demo residue.
- Open at the assumption gate: whether a live bank engagement shapes the deliverable's register;
  whether this repo is the program seed or remains the vision lab.
