# Active Phase Context

**Phase 83 — *Agentification Stage 1: the merge adjudicator agent, oracle-scored* (the 5th companion live loop)** (signal-watch-local, STANDARD, agentic) — PLANNED 2026-06-29 → READY FOR IMPLEMENTATION (begin at T1). Siblings stalled at the Phase-82 pins (substrate `294d3e5` / casework `04cc335`, code-verified LIVE) — no consume; the agentification roadmap is the forward path.

## Objective
Build the agentification roadmap's Stage 1 — the FIRST measurable agent: a companion-only merge adjudicator (StubAdjudicator + LiveAdjudicator) that PROPOSES one of {uphold_merge, reject_as_shares, both_defensible, escalate} + a rationale per merge case, MEASURED against the committed non-circular `GT-<hash>` oracle in `data/merge/cases.json` (the ONE gate with a correctness oracle). Surface it as the 5th companion LIVE loop (`serve_merge.py` + a build-stripped `/*LIVE_*/` overlay in `merge.html`); run it live once, pin the capture, record the agreement counts. The deliverable is the MEASUREMENT; the agent is deliberately thin; the human still adjudicates (propose→gate→decide).

## Scope (file globs)
`scripts/merge_adjudicator.py` · `tests/merge_adjudicator_quality_harness.py` · `tests/test_selftests.py` · `scripts/serve_merge.py` · `merge.html` · `scripts/build.py` (merge-target strip) · `tests/merge-console.test.mjs` · `tests/fixtures/merge-adjudicator/**` · `docs/merge-live.md` · `docs/agentification-roadmap.md` · `CLAUDE.md` · `HANDOFF.md`

## Key constraints
- §4.5 / dist boundary: ALL 9 ship dists BYTE-FROZEN; the LIVE overlay build-stripped → `dist/merge` byte-identical (`--check merge`); the offline file makes NO model call.
- The oracle firewall: the agent provably NEVER sees the `oracle` (`adjudicator_input()` strip + `assert_no_oracle_leak()`); `/adjudicate` carries no oracle pre-disposition.
- build.py imports NO merge_adjudicator/serve_merge/scorer/spine/curate/casework (grep guard); `evidence_requirements.py` UNTOUCHED (this is merge, not §12).
- Honesty: counts-only; the synthetic-substrate qualifier on every number; the word-ban (no catch-rate/lift/precision/recall) extends to the LIVE markers + the docs.
- Execute-once: NO model on :8080 → ship the StubAdjudicator baseline (33/66) + flag the live capture a named follow-on; NEVER fabricate a live agent number.

## Exit criteria
`merge_adjudicator.py --selftest` 0 (firewall + 33-right/33-wrong + counts-by-quadrant + deferrals + qualifier, no banned words); `merge_adjudicator_quality_harness.py --check` 0 + in `uv run pytest`; `serve_merge.py --selftest` 0; `--check merge` byte-identical + `--check all` 9/9; `merge-console.test.mjs` green (existing + live-branch + offline-strip); the agreement counts recorded (stub unconditionally; live pinned OR pending-with-note); docs + CLAUDE.md trued in place; honesty swept.

## Abort rule
Any unsanctioned dist drift (esp. `dist/merge` not byte-identical after strip) / a build.py companion import / an oracle leak to the client pre-disposition / an `evidence_requirements.py` change / any agreement count presented as a catch-rate/lift/precision/recall → STOP-and-surface. If blocked >3 attempts: ask user — skip or abort.

## Gates
- [x] spec (`specs/phase-83-merge-adjudicator-oracle-scored.md`)
- [x] Direction confirmed by user (2026-06-29, AskUserQuestion two rounds — Frontier "Agentification S1: merge adjudicator" · Q1 "Accept — measure, report by quadrant" · Q2 "4-way + count deferrals" · Q3 "Add a served surface now" · Q3b "(A) companion live mode"; all_accept, NOT silent; ledger Phase-83)
- [x] Delivery accepted (post-implementation report 2026-06-29; impl commit db7e3ae; agent 54/66 vs spine 33; all 9 dists byte-frozen; committed + pushed to main)

Decisions [[decisions/phase-83-merge-adjudicator-stage1-frame]] · [[decisions/phase-83-companion-live-not-baked]] · [[decisions/phase-83-4way-vocab-count-deferrals]] · [[decisions/phase-83-measure-by-quadrant-two-sided-baseline]]; plan [[phases/phase-83-merge-adjudicator-oracle-scored]]; ledger Phase-83.
