# Spec: Phase 47 — Demo-to-program design: the regulatorily defensible agentic AML program

> status: nana:approved (derived from the gate-approved decision article) · created: 2026-06-12
> NOTE: generated POST-GATE because ceremony escalated lite → STANDARD mid-flow (first design
> phase; cost-of-error is direction-setting). Source of truth for rationale:
> `.dev-wiki/articles/decisions/phase-47-agentic-aml-program-design.md` (D1–D5 + A1′ reframe).

## Objective

Translate the successful vision demo (presented to bank stakeholders 2026-06-11) into the design
of a REAL efficient / effective / regulatorily defensible agentic AML program. Three deliverables:
(a) the engineering program blueprint `docs/program-blueprint.md`; (b) the GATE CONSOLE — a 4th
single-file offline vision artifact dramatizing the non-binary human judgment gate (MVP: ONE gate
class — C/D tag adjudication — over a committed licence-clean divergence dataset); (c) the OSFI
E-23 knowledge gap closed in the aml-wiki FIRST (before the design hardens).

## Scope

- `wiki/concepts/*.md` (aml-wiki via symlink): NEW E-23 article + cross-link from
  aml-model-risk-management.md (T1).
- `docs/program-blueprint.md` (NEW): spine + assembly (T2, T3).
- `data/console/cases.json` (NEW) + `scripts/curate_console_cases.py` (NEW, regeneration-only) +
  `scripts/build.py` (validator + console target ONLY) (T4, T5).
- `console.html` (NEW) → `dist/console/` + `tests/gate-console.test.mjs` (NEW) (T5).
- `CLAUDE.md`, `tests/smoke-checklist.md`, `HANDOFF.md` (§8 disposition line only), `.dev-wiki/*` (T3, T6).

## Non-goals

- NO real program build — this repo stays the vision lab + design source-of-truth (A2).
- NO stakeholder-facing digest (derives in a later phase, A3); no live bank clock.
- NO change to the existing 3 ship artifacts, their dists, committed derived data, overlays, or
  the grounding core. NO new lift/precision/similarity number anywhere.
- Console MVP = ONE gate class; multi-gate-class console, persistence, and live mode are OUT.

## Constraints (safety rails)

- Existing 3 ship artifacts + dists BYTE-IDENTICAL through the phase (`--check all` green on the
  pre-phase baselines; drift → STOP and surface). Prevents: silently breaking the presented demo.
- The gate console is a single self-contained offline file, NO LLM/fetch call, session-only
  dispositions (export = copy-out). Prevents: violating the offline non-negotiable.
- Console dataset committed + licence-clean: quotes ground against CURRENT committed derived
  records (build-boundary validator, fail-loud); FINTRAC rows carry Crown-copyright attribution
  metadata (Phase-28 footer mechanism in the artifact). Prevents: an ungrounded or
  licence-violating demo dataset.
- "95/5" appears ONLY as a design direction (automate-by-default, judgment-by-design); any ratio
  carries its measurement definition (A4 — the Phase-45 fake-lift deletion pattern forward).
- Always-on "Illustrative data & outputs" badge on the console; graded dispositions come from the
  PRESENTER, never a synthesized judgment score.
- E-23 article written from the PRIMARY OSFI source (WebFetch), never from memory.

## Assumptions (gate-closed 2026-06-12; ledger block in assumption-ledger.md)

- A1′ [HIGH, reject-by-reframe → accepted]: grounding is UNIVERSAL; the grounding SUBSTRATE varies
  per workload (advisory text → substring verifier; monitoring → signals + transactional/
  non-transactional data, referential/lineage verifiers; SAR/STR narratives → guidance/policies/
  signals/data, citation verifiers); grounding CHAINS — defensibility = the audit walk down the
  chain; each workload's substrate + verifier NAMED, never assumed.
- A2 [HIGH]: this repo = vision lab + design source-of-truth; the real build is future/elsewhere.
- A3 [MED]: no live bank engagement dictates register or deadline; blueprint is engineering-first.
- A4 [MED]: "95/5" = design direction, never a stated target ratio.
- A5 [MED]: the 5% human charter includes a MANDATED-ACCOUNTABILITY class (SAR sign-off,
  governance attestations — compulsory under SR 11-7 Pillar 3) alongside art-like judgment work.

## Checkpoints

- Post-T1 spine-hardening: E-23 lifecycle stages mapped against SR 11-7 pillars — "good enough to
  harden the spine" before T2 writes the blueprint core.
- T5-CHECKPOINT (MID-PHASE, pre-T5): budget + blueprint-state review with the user-visible record;
  decide proceed-to-T5 or descope console to Phase 47b (the blueprint is the load-bearing
  deliverable). Decision line recorded in tasks.md.

## Exit criteria

1. E-23 article in the aml-wiki with the per-stage SR 11-7 mapping table.
2. `docs/program-blueprint.md` complete with named sections: per-workload substrate/verifier table
   all-cells-filled; 4-class gate taxonomy; dual-class human charter; probe-rule agentification
   criterion w/ max-iteration caps + surface-all-dimensions; SR-11-7+E-23 control mapping; drift /
   ongoing-monitoring disposition (designed-now vs deferred-with-owner); honesty-constraint
   disposition table (survive vs transform); HANDOFF "ships a demo, not a system" one-line
   disposition; DEFERRED list re-sequenced as capability roadmap; 95/5-as-direction.
3. Gate console MVP (one gate class, graded session-only dispositions + rationale capture,
   committed licence-clean dataset, badge + attribution) OR a recorded conscious descope to 47b at
   T5-CHECKPOINT.
4. Full regate green; existing 3 ship artifacts byte-identical.

## Verification

- T1: `test -f` new article && mapping-table check (every E-23 lifecycle stage row names an
  SR 11-7 pillar) && `grep -q 'e-23' wiki/concepts/aml-model-risk-management.md`.
- T2/T3: deterministic section/table presence checks per task `success:` fields, incl. the
  adversarial no-95%-target grep.
- T4: build-boundary validator green; zero `.dev-wiki/tmp` / uncommitted references; FINTRAC
  attribution metadata present.
- T5: `node tests/gate-console.test.mjs` && `python3 scripts/build.py --check all` for ALL 4
  targets && `git diff --quiet` on the 5 pre-existing dists.
- T6: full regate — `--check all`, all node suites, all python selftests,
  `tests/news_quality_harness.py --check`.

## Rollback / descope

- Console descope valve: Phase 47b at T5-CHECKPOINT (blueprint ships alone; T6 runs on the
  no-console branch — CLAUDE.md gets the blueprint pointer only, no 4th-artifact lines).
- Any existing-dist drift: STOP, surface, revert the offending change — never re-baseline.
- E-23 primary source unreachable: surface honestly; do NOT write the article from memory.
