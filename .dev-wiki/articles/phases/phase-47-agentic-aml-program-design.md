---
title: "Phase 47: Demo-to-program design — the regulatorily defensible agentic AML program"
aliases: [phase-47, program-design, demo-to-real, gate-console]
category: phases
tags: [design, program-architecture, model-risk, sr-11-7, osfi-e-23, gate-taxonomy, human-in-the-loop, m9-candidate]
parents: []
created: 2026-06-12
updated: 2026-06-12
source: plan
status: completed
scope: ["docs/program-blueprint.md", "specs/phase-47-agentic-aml-program-design.md", "console.html", "dist/console/**", "data/console/**", "scripts/curate_console_cases.py", "scripts/build.py", "tests/gate-console.test.mjs", "tests/smoke-checklist.md", "CLAUDE.md", "HANDOFF.md", "wiki/articles/concepts/*.md", ".dev-wiki/*"]
entry_criteria: "Phase 46 closed (committed 5981b41 + 4cf6cbb, pushed); presentation 2026-06-11 delivered, user verdict: huge success; direction = the user's 6th gate reframe; assumption gate closed 2026-06-12 (A1 reject-by-reframe → A1′; A2–A5 accept)."
exit_criteria: "E-23 article w/ per-stage SR 11-7 mapping table; docs/program-blueprint.md complete w/ named sections; gate console MVP OR recorded descope to 47b at T5-CHECKPOINT; full regate green, existing 3 ship artifacts byte-identical."
---

# Phase 47: Demo-to-program design — the regulatorily defensible agentic AML program

## Objective

Translate the successful vision demo (presented 2026-06-11) into the DESIGN of a real, efficient,
effective, regulatorily defensible agentic AML program — the first DESIGN phase (STANDARD ceremony).
Deliverables: (a) the engineering program blueprint `docs/program-blueprint.md`; (b) the GATE
CONSOLE, a 4th single-file offline vision artifact dramatizing the non-binary human judgment gate
(MVP: ONE gate class — C/D tag adjudication — over a committed licence-clean divergence dataset);
(c) the OSFI E-23 knowledge gap closed in the aml-wiki FIRST.

## The A1′ design spine (the user's reframe at the gate)

Grounding is UNIVERSAL — what varies per workload is the grounding SUBSTRATE, and therefore the
deterministic verifier: advisory text → substring verifier; transaction monitoring → the committed
signals + the transactional/non-transactional data supporting them → referential/lineage verifiers;
SAR/STR narratives → guidance/policies/signals/data → citation verifiers. Grounding CHAINS
(monitoring grounds to signals themselves grounded to advisories); defensibility = the audit walk
down the chain; nothing ungrounded survives a gate; each workload's substrate + verifier is NAMED
in the blueprint, never assumed. On top: measured dimensions (blind inter-rater,
regression-vs-baseline), human-judgment gates (non-binary graded dispositions + captured rationale),
and a MANDATED-ACCOUNTABILITY class (SAR sign-off, governance attestations — SR 11-7 Pillar 3). The
5% human charter designs both judgment AND accountability work. Agentification criterion = the
agent-runtime-adoption-probe rule (A/B probe first; n=1 caveat; max-iteration caps; gates surface
ALL scored dimensions). Regulatory anchor layered: SR 11-7 backbone + OSFI E-23 (audience
jurisdiction) + FINTRAC content layer.

## Scope

`wiki/articles/concepts/*.md` (E-23 article, T1 — scope glob corrected at debrief: the aml-wiki's real concepts path is `articles/concepts/`) · `docs/program-blueprint.md` (T2/T3) · `HANDOFF.md` §8
(T3, one line) · `data/console/cases.json` + `scripts/curate_console_cases.py` + `scripts/build.py`
validator (T4) · `console.html` → `dist/console/` + `tests/gate-console.test.mjs` + build.py
console target (T5) · `CLAUDE.md` + `tests/smoke-checklist.md` + docs (T6).

## Exit Criteria

- [x] E-23 article in the aml-wiki with the per-stage SR 11-7 mapping table (T1 — 8/8 rows name an
      SR 11-7 pillar; primary osfi-bsif.gc.ca source)
- [x] docs/program-blueprint.md complete with named sections: per-workload substrate/verifier table
      all-cells-filled; 4-class gate taxonomy; dual-class human charter; probe-rule criterion w/
      caps + surface-all-dimensions; SR-11-7+E-23 control mapping; drift disposition
      (designed-now vs deferred-with-owner); honesty disposition table (survive vs transform);
      HANDOFF one-line disposition; DEFERRED list as capability roadmap; 95/5-as-direction (T2/T3)
- [x] Gate console MVP shipped (T5-CHECKPOINT = PROCEED, no 47b descope): one gate class (C/D
      adjudication, 213 committed licence-clean cases), graded session-only dispositions +
      required rationale, always-on badge + FINTRAC attribution; gate-console 68/68 (T4/T5)
- [x] Full regate green (--check all 6/6, 11 suites); existing 3 ship artifacts + dists
      byte-identical (T6; reviewer re-verified)

## Constraints

- Existing 3 ship artifacts + dists BYTE-IDENTICAL through the phase — prevents breaking the
  just-presented demo; drift → STOP, never re-baseline.
- Gate console = offline single file, NO LLM/fetch, session-only dispositions — prevents violating
  the offline non-negotiable.
- Console dataset committed + licence-clean (quotes ground against CURRENT committed records;
  FINTRAC rows carry attribution) — prevents an ungrounded/licence-violating demo dataset.
- "95/5" only as design direction — prevents a fabricated target ratio (Phase-45 pattern forward).
- E-23 from the PRIMARY OSFI source — prevents writing regulation from memory.

## Checkpoints

- Post-T1: spine-hardening check (E-23 lifecycle stages mapped against SR 11-7 pillars) before T2.
- T5-CHECKPOINT (pre-T5): budget + blueprint-state review → proceed or descope console to 47b.

## Assumptions

- A1′ universal-grounding spine (substrate varies, verifiers named). If a workload genuinely has no
  nameable substrate: surface it as a blueprint FINDING, never assume one.
- A2 repo = vision lab + design source-of-truth. If a real build is requested: new phase, new plan.
- A3 no live bank clock. If an engagement lands: surface at a checkpoint, re-gate register.
- A4 95/5 = direction only. If a ratio is demanded: it carries its measurement definition.
- A5 charter includes mandated-accountability. If it crowds the judgment story: both stay — the
  examiner-visible hole is worse.

## Notes

- Progress 7/7 tasks [x] (2026-06-12, same-session): READY FOR COMPLETION — delivery gate pending
  (status stays `active` until the delivery flow commits + flips the gate). Review gate 9/10
  ACCEPT, zero HIGH; A1′–A5 all held (ledger revisit filled). Journal:
  [[2026-06-12-phase-47-agentic-aml-program-design]].
- Decision article: [[decisions/phase-47-agentic-aml-program-design]] (D1–D5 + approach-review
  revisions; confidence high). Spec: `specs/phase-47-agentic-aml-program-design.md` (generated
  post-gate — ceremony escalated lite → standard mid-flow).
- Direction quote (user, at the gate): "demo was a huge success, now we are ready to plan for how
  to turn this into a real thing… ~95% agentic work + 5% human work, but make the 5% human work
  important and interesting — pipeline conceptualization, judgmental calls on decisions, gate
  decisions (non-binary, more art-like)." 6th user reframe at a gate; this one reframes ALTITUDE.
