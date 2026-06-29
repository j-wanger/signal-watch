# Active Phase Context

**Phase 85 — *§12 determination pre-proposer: the 6th live loop, oracle-scored (Agentification Stage 2)*** (signal-watch-local, STANDARD, companion-only) — PLANNED 2026-06-29. The agentification roadmap's Stage 2 — the SECOND oracle-scored agent. Mirrors Phase 83 (the merge adjudicator) exactly; every seam already exists.

## Objective
Build the §12 determination PRE-PROPOSER (the 6th companion LIVE loop): a companion agent that PROPOSES each case's determination (`file` / `cleared` / `needs-more-info` + rationale) from the assembled §12 bundle evidence ONLY (the oracle firewall), MEASURED TWO-SIDED against the Phase-78 exogenous `intended_disposition` oracle vs the deterministic sufficiency-engine baseline, pinned via a replay quality harness. Companion-only; all 9 ship dists byte-frozen; `evidence_requirements.py` BYTE-UNCHANGED (propose→gate→decide). The deliverable is the MEASUREMENT; the agent is thin.

## Scope (file globs)
`scripts/determination_proposer.py` · `tests/determination_proposer_quality_harness.py` · `scripts/serve_workbench.py` · `workbench.html` · `tests/workbench.test.mjs` · `tests/test_selftests.py` · `tests/fixtures/determination-proposer/**` · `docs/determination-live.md` · `docs/case-workbench.md` · `docs/agentification-roadmap.md` · `CLAUDE.md` · `HANDOFF.md`

## Key constraints
- The ORACLE FIREWALL: the agent provably NEVER sees `intended_disposition` (`proposer_input()` strip + `assert_no_oracle_leak()` reusing the Phase-78 allow-list); the served `/propose-determination` carries no oracle field on the wire — non-circular by construction (the Phase-77 trap avoided).
- propose→gate→decide / A1-frozen: the agent PROPOSES, the deterministic engine LICENSES, the human DECIDES. `evidence_requirements.py` BYTE-UNCHANGED; the 256/376 casework signing funnel unchanged; build.py imports nothing new; all 9 dists byte-frozen (companion-only). The proposal is presentation/measurement-only.
- TWO-SIDED HONEST measurement: agent-vs-oracle AND engine-vs-oracle, on file AND clear; counts-only; the synthetic-substrate qualifier on every number; the word-ban (no catch-rate/lift/precision/recall) on the new markers + docs. The headroom is OVER-FLAG (clear-side) precision-recovery; the file-misses are HONESTLY NULL (a DATA gap — substrate Ask #3 measured-null). NO Phase-83 "54-vs-33"-shaped recall story.
- ABSTENTION = COVERAGE separate from accuracy: {committed-accuracy, abstention-coverage} are two numbers; needs-more-info never scored as a wrong-file nor as correct.
- Companion-only / dist boundary: the workbench touches NO dist; build.py imports nothing new (grep guard: determination_proposer|serve_workbench|curate_workbench|casework|entity_spine).

## Exit criteria
`determination_proposer --selftest` + `serve_workbench --selftest` PASS; `determination_proposer_quality_harness.py --check` green (two-sided counts, abstention separate, synthetic-qualified) + in `uv run pytest`; `node tests/workbench.test.mjs` green (count grows from 195; the proposal panel + "proposed, not decided" + no-oracle-pre-decision + unchanged-licensing); the live headline recorded HONESTLY (counts-only, two-sided) OR the stub baseline + the one-command `--freeze` fold-forward note; `--check all` 9/9 byte-frozen; `evidence_requirements.py` git-diff empty; build.py companion-import grep clean; the 256/376 funnel unchanged; roadmap Stage 2 marked BUILT; CLAUDE.md + HANDOFF trued IN PLACE; honesty swept.

## Abort rule
Any oracle leak (into the proposer input or onto the wire pre-decision) / an `evidence_requirements.py` change / a build.py companion import / any of the 9 dists not byte-identical / a change to the 256/376 funnel / a MISS-SIDE recovery story (the misses are substrate-gated, honestly NULL) / any number framed as catch-rate/lift/precision/recall / a fabricated live agent number → STOP-and-surface. Measure-first / execute-once: NO model on :8080 → ship the StubProposer baseline (the engine-vs-oracle two-sided confusion, the real measured floor) + flag the live capture pending; NEVER fabricate. If blocked >3 attempts: ask user — skip or abort.

## Gates
- [x] spec (`## Formal Spec` embedded in [[phases/phase-85-determination-pre-proposer]] — standard ceremony, no separate /spec round; the contract is fully determined, every seam built)
- [x] Direction confirmed by user (2026-06-29, AskUserQuestion — direction = §12 determination pre-proposer; 3 assumptions ACCEPTED, all_accept tracked NOT silent; A1 substrate-recency rider DISCHARGED [HEAD 3716f77 unchanged]; ledger Phase-85)
- [ ] Delivery accepted (post-implementation report)

Decisions [[decisions/phase-85-direction-determination-pre-proposer]] · [[decisions/phase-85-over-flag-headroom-not-miss-recovery]] · [[decisions/phase-85-oracle-firewall-non-circular]] · [[decisions/phase-85-propose-gate-decide-a1-frozen]]; plan [[phases/phase-85-determination-pre-proposer]]; ledger Phase-85.
