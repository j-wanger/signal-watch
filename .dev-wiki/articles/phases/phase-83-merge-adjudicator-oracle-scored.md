---
title: "Phase 83: Agentification Stage 1 — the merge adjudicator agent, oracle-scored (the 5th companion live loop)"
aliases: [phase-83, merge-adjudicator, agentification-stage-1]
category: phases
tags: [agentification, merge, oracle, live-loop, measurement, companion, firewall]
parents: []
created: 2026-06-29
updated: 2026-06-29
source: plan
status: active  # IMPLEMENTED 2026-06-29 (all 8 tasks [x], exit criteria met); stays active until the user confirms completion at the delivery gate
scope: ["scripts/merge_adjudicator.py", "tests/merge_adjudicator_quality_harness.py", "scripts/serve_merge.py", "merge.html", "scripts/build.py", "tests/merge-console.test.mjs", "tests/test_selftests.py", "tests/fixtures/merge-adjudicator/**", "docs/merge-live.md", "docs/agentification-roadmap.md", "CLAUDE.md", "HANDOFF.md"]
entry_criteria: "Phase 82 DELIVERED + accepted 2026-06-29 (impl efa7abd; all 9 dists settled, evidence_requirements.py byte-unchanged). Siblings code-verified LIVE this session as STALLED at the Phase-82 pins (substrate 294d3e5 / casework 04cc335) — no new emission to consume; the agentification roadmap is the signal-watch-internal forward path. The seams are code-verified (resolution_scorer.candidate_pairs + KLASS_* + assert_no_cluster_leak; osint_tools.call_openai/parse_llm_json; gather_quality_harness --check/--freeze; serve_corpus + /*LIVE_*/ build-strip)."
exit_criteria: "merge_adjudicator.py --selftest exits 0; merge_adjudicator_quality_harness.py --check exits 0 + in uv run pytest; serve_merge.py --selftest exits 0; build.py --check merge byte-identical + --check all 9/9; merge-console.test.mjs green (existing + live-branch + offline-strip); the measured agreement counts recorded (stub baseline unconditionally; live capture pinned OR flagged pending with a model-absent note); docs written; CLAUDE.md current-state trued in place; honesty sweep clean; build.py imports no merge_adjudicator/serve_merge/scorer/spine/curate/casework."
---

# Phase 83: Agentification Stage 1 — the merge adjudicator agent, oracle-scored

## Objective

Build the agentification roadmap's Stage 1 — the FIRST measurable agent: a companion-only merge
adjudicator that proposes a merge call (`uphold_merge` / `reject_as_shares` / `both_defensible` /
`escalate`) + a rationale per case, MEASURED against the committed non-circular `GT-<hash>` oracle in
`data/merge/cases.json` (the ONE gate with a correctness oracle). Surface it as the 5th companion live
loop, keeping all 9 ship dists byte-frozen. The deliverable is the MEASUREMENT; the agent is thin; the
human still adjudicates (propose→gate→decide).

## Scope

Files and modules affected:
- `scripts/merge_adjudicator.py` — StubAdjudicator + LiveAdjudicator + `adjudicator_input()` firewall +
  `assert_no_oracle_leak()` + `score_adjudications()` (companion-only, dep-free scoring)
- `tests/merge_adjudicator_quality_harness.py` — `--check` (dep-free replay + stub baseline) / `--freeze`
  (one live capture); wired into `tests/test_selftests.py`
- `scripts/serve_merge.py` — the companion server (stdlib, 127.0.0.1, the `serve_corpus.py` pattern)
- `merge.html` + `scripts/build.py` — the build-stripped `/*LIVE_*/` overlay + the `merge`-target strip
- `tests/merge-console.test.mjs` — the offline-strip assertion + the live-branch tests
- `tests/fixtures/merge-adjudicator/**` — the pinned live capture (or pending)
- `docs/merge-live.md`, `docs/agentification-roadmap.md` (Stage 1 → BUILT), `CLAUDE.md`, `HANDOFF.md`

## Exit Criteria

- [x] `python3 scripts/merge_adjudicator.py --selftest` exits 0 (firewall rejects an oracle leak; stub
      baseline reproduces 33-right/33-wrong; scoring emits counts-by-quadrant + deferrals + qualifier; no
      banned words)
- [x] `python3 tests/merge_adjudicator_quality_harness.py --check` exits 0; in `uv run pytest` (27→30)
- [x] `python3 scripts/serve_merge.py --selftest` exits 0 (render + payload parity + stub loop + degrade +
      the no-oracle-pre-disposition firewall)
- [x] `python3 scripts/build.py --check merge` byte-identical (LIVE strip); `--check all` 9/9
- [x] `node tests/merge-console.test.mjs` green (existing + live-branch + offline-strip; ~76→100)
- [x] The measured agreement counts recorded (a model WAS on :8080 → the live capture landed for real
      at T2 `--freeze`: agent 54/66 vs spine 33; pinned to `tests/fixtures/merge-adjudicator/adjudicator.replay.json`)
- [x] Docs written; CLAUDE.md current-state trued in place; honesty sweep clean

## Constraints

- **§4.5 / dist boundary** — all 9 ship dists BYTE-FROZEN; the live overlay is build-stripped → `dist/merge`
  byte-identical. Prevents: shipping a model call in the offline file / an unsanctioned dist drift.
- **The oracle firewall** — `adjudicator_input()` strips to the evidence surface; `assert_no_oracle_leak()`
  RAISES on any truth field; `/adjudicate` carries no oracle pre-disposition. Prevents: the agent scoring
  against truth it was shown (a tautology dressed as a measurement).
- **build.py firewall** — imports NO merge_adjudicator/serve_merge/scorer/spine/curate/casework (grep guard).
  Prevents: the companion layer crossing into the build.
- **`evidence_requirements.py` UNTOUCHED** — this is merge, not §12. Prevents: an A1 violation.
- **Honesty** — counts-only; the synthetic-substrate qualifier on every number; the word-ban (no
  catch-rate/lift/precision/recall) extends to the LIVE markers + the docs. Prevents: a measured count read
  as a real performance claim.

## Checkpoints

- After T2 (the dep-free `--check` harness): the stub baseline (33-right/33-wrong) is the always-checkable
  measured result — the floor that ships regardless of model availability.
- At T7 (EXECUTE ONCE): if no model is reachable on :8080, STOP fabricating — ship the stub baseline + flag
  the live agent capture as a named follow-on (note in the commit). Never invent a live agent number.

## Assumptions

- A1 (T0 weakest): the agreement is a meaningful headline because the stub baseline is TWO-SIDED (right
  33/66, wrong 33). If false (the stub were one-sided): the by-quadrant breakout would show it, and the
  headline reframes to where the agent does/does not beat the spine — still honest.
- A2: the 4-way vocab is scorable against the binary oracle by counting deferrals separate. If false: the
  defer count is reported on its own; nothing is scored against an absent label.
- A3: the companion live mode keeps all 9 dists byte-frozen. If false (the strip drifts `dist/merge`):
  STOP-and-surface — the abort rule.
- A4: a model may not be on :8080 this session. If so: the stub baseline ships; the live capture is a named
  follow-on.

## Notes

- Mirrors the proven GATHER split (`osint_tools.py` StubPlanner/LivePlanner + `gather_quality_harness.py`).
- The stub baseline counts come straight from `resolution_scorer` KLASS_* over `cases.json`: right 33/66,
  wrong 33 (30 fragmentation-gap + 3 over-merge-trap).
- The 4 existing live loops (news/corpus/GATHER/DECIDE) share the one local-model transport at
  `127.0.0.1:8080`; the merge adjudicator joins them as the 5th.
