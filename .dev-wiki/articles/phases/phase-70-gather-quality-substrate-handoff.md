---
title: "Phase 70: Gather extraction quality (measured) + the consolidated §12 substrate handoff"
aliases: []
category: phases
tags: [companion, gather-quality, measure-first, substrate-handoff, lfcm]
parents: []
created: 2026-06-22
updated: 2026-06-22
source: plan
status: complete
scope: ["scripts/osint_tools.py", "scripts/serve_workbench.py", "scripts/serve_chain.py", "scripts/evidence_requirements.py", "tests/workbench.test.mjs", "tests/fixtures/**", "docs/substrate-*-PLAN-BRIEF.md", "docs/evidence-driven-filing.md", "docs/case-workbench.md", "CLAUDE.md", "tests/smoke-checklist.md"]
entry_criteria: "Phase 69 DELIVERED + accepted; the live GATHER under-extracts corroboration findings (the named Phase-69 follow-on); the substrate handoff briefs are sibling-rooted and proliferating."
exit_criteria: "Gather coverage measured live before/after vs the stub reference (pinned + regression-asserted); the consolidated substrate handoff brief written + pinned; --check all 8/8 zero dist drift; build.py imports no sibling/companion; uv run pytest + all .mjs arcs + selftests green."
---

# Phase 70: Gather extraction quality (measured) + the consolidated §12 substrate handoff

## Objective

Measure the live GATHER's extraction recall against the deterministic StubPlanner reference
(consistency-not-correctness, the Phase-65 honesty class) and fix the diagnosed under-extraction
surface — then consolidate the proliferating sibling-substrate asks into ONE pinned §12 handoff
brief. Companion-only; the 8 offline dists stay byte-frozen.

## Scope

Files and modules affected:
- `scripts/osint_tools.py` — the gather coverage metric + the diagnosed under-extraction fix (the
  `findings()` payload-enrich + exhaustive-per-record prompt + ownership/direct-hit disambiguation)
- `scripts/serve_workbench.py` — the coverage metric in the gather result + NDJSON stream; the
  stub-reference selftest assertion
- `scripts/serve_chain.py` — only if the coverage metric rides a shared payload helper
- `scripts/evidence_requirements.py` — the deterministic non-gatherable-atom aggregation for the brief
- `tests/workbench.test.mjs` — the coverage-render arc + the pinned replay/regression assertion
- `tests/fixtures/**` — ONE pinned live capture (deterministic, replayable with no model)
- `docs/substrate-*-PLAN-BRIEF.md` — the consolidated brief (absorbs/supersedes the BO-graph brief)
- `docs/evidence-driven-filing.md`, `docs/case-workbench.md`, `CLAUDE.md`, `tests/smoke-checklist.md`
  — the true-up

## Exit Criteria

- [ ] Gather coverage metric present in the result + NDJSON stream; the StubPlanner achieves full
      targeted-atom closure on the demo case in `serve_workbench --selftest`
- [ ] The live baseline coverage + the diagnosed under-extraction surface recorded in
      `docs/evidence-driven-filing.md` (A1 down-scope: measurement gates the fix)
- [ ] The diagnosed surface fixed; `osint_tools --selftest` green (every gate-DROP case + the
      record-sourced ownership assertion still hold)
- [ ] ONE pinned live capture replays deterministically (no model) + a coverage-regression assertion
      green vs the stub reference; live before/after coverage recorded
- [ ] ONE consolidated aml-substrate handoff brief pinned to a code-verified substrate commit;
      the BO-graph brief folded/superseded; the gap inventory derived-not-hand-listed
- [ ] `--check all` 8/8 ZERO dist drift; build.py imports no casework/substrate/osint_tools;
      `uv run pytest` + all `.mjs` arcs + selftests green

## Constraints

- Companion-only — NOT a ship target; build.py imports no casework/substrate/osint_tools; the 8
  offline dists stay BYTE-FROZEN (`--check all` 8/8); the agent runs server-side (browser sends a
  backend NAME only — §4.5). *Prevents: a companion edit leaking into a ship artifact / a sibling
  import into build.py.*
- Measure-first — the StubPlanner is the deterministic reference (it grounds exhaustively, one
  finding per gatherable record, so it IS the reference); gather quality = live recall vs the stub
  (consistency-not-correctness); ZERO catch-rate/precision/lift number (the single-signal-separable
  governor). *Prevents: claiming an unmeasured quality improvement; a detection-difficulty framing.*
- The Phase-66 honesty guard — structured facts (ownership label/pct/direction) stay RECORD-SOURCED,
  never model-authored; the `_BANNED`-token honesty sweep + the grounding gate unchanged. *Prevents:
  the live model fabricating a structured fact (the Phase-66 ownership-pct lesson).*
- A1 don't-know — the live baseline DIAGNOSES the under-extraction surface BEFORE T2 commits a fix
  (root cause is code-verified at osint_tools.py:430-447: `findings()` passes the model only
  `{id, text}`, not the record's DECLARED entity/officers/relationship names it must copy exactly,
  with an open-ended "if nothing relevant return []" prompt conflating an ownership-tie with a
  direct sanctions hit). *Prevents: optimizing what wasn't measured.*

## Checkpoints

- After T1 (the live baseline): the diagnosed surface (prompt vs payload vs leg-mapping) is RECORDED
  before T2 commits the fix — if the surface can't be diagnosed honestly, STOP-and-surface.
- If the live execute-once shows a fabricated structured fact → record-source / sweep / fail-closed,
  never render the fabrication (the Phase-66 lesson).
- If gather coverage can't be measured honestly vs the stub reference → STOP-and-surface; do not
  claim an unmeasured improvement.

## Assumptions

- A0 [boundary, accept] companion-only / build.py imports nothing / 8 dists byte-frozen / §4.5.
  If false: STOP-and-surface.
- A1 [T0 weakest, don't-know → down-scope] the live baseline is a measurement-FIRST task that
  diagnoses the under-extraction surface before any fix is committed. If the surface is undiagnosable:
  report the measurement, do not force a fix.
- A2 [accept] the StubPlanner-as-reference frame is honest (consistency-not-correctness). If it reads
  as a correctness/catch-rate claim: re-word, never claim detection-lift.
- A3 [accept] re-measure live once + pin ONE capture as a deterministic replay fixture + a
  coverage-regression assertion vs the stub (the news_quality_harness pattern). If the live fix can't
  be pinned deterministically: STOP-and-surface.
- A4 [reject one-brief-per-gap → consolidate] ONE consolidated substrate handoff brief that
  absorbs/supersedes `docs/substrate-bo-graph-emission-PLAN-BRIEF.md`. If the BO-graph brief can't
  fold cleanly: the consolidated brief documents the delta.

## Notes

LITE phase — no decision articles. The five planning decisions (recorded here per the lite ceremony):

1. **Measure-first via the stub-as-reference.** Gather quality = live recall vs the deterministic
   StubPlanner (consistency-not-correctness), NOT model-tuning. The StubPlanner grounds exhaustively
   (one finding per gatherable record) so it IS the reference.
2. **A1 down-scoped.** The live baseline is a measurement-FIRST task that diagnoses the
   under-extraction surface before any fix is committed.
3. **A4 consolidate.** ONE consolidated substrate handoff brief (absorbs/supersedes the BO-graph
   brief), not a brief-per-gap.
4. The diagnosed-surface fix is EXPECTED to be: `findings()` payload-enrich (surface the record's
   declared entity/officers/relationship names) + an exhaustive-per-record prompt +
   ownership/direct-hit disambiguation — but T1's measurement is what licenses it.
5. The consolidated brief adds the determination-signal detector asks the §12 briefs already name
   (C1/C7/C8/C14 + SoF/anticipated-activity/income + party/UBO-at-source + a kyc/TF case slice),
   pinned to a code-verified substrate commit.

Grounding (no wiki articles — the knowledge wiki is empty): the Phase-65/66 tool-evidence honesty
pattern (consistency-not-correctness; record-sourced structured facts; run live once to surface
fabrication/under-extraction); the `news_quality_harness` deterministic-replay regression-gate
pattern; the §12 `signal_brief` mechanism (`evidence_requirements.py`); the PLAN-BRIEF handoff
pattern (`docs/substrate-bo-graph-emission-PLAN-BRIEF.md`).

Knowledge gaps carried to impl: the live model's actual gather coverage (T1 measures); the
aml-substrate current state (must be code-verified at T4 for an honest pin); which exact surface
under-extracts (T1 diagnoses — A1 down-scope).

Direction gate 2026-06-22 (NOT all-accept): A0 accept · A1 don't-know→down-scope · A2 accept · A3
accept · A4 reject→consolidate. Ledger Phase-70 block. Grounded against signal-watch HEAD fbd2291 /
the Phase-69 workbench.
