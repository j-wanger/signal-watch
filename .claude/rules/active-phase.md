# Active Phase Context

**Phase 85 — *§12 determination pre-proposer: the 6th live loop, oracle-scored (Agentification Stage 2)*** (signal-watch-local, STANDARD, companion-only) — DELIVERED 2026-06-29, READY FOR COMPLETION (all 6 tasks [x], exit criteria met, impl committed `2008692`). The roadmap's Stage 2, the SECOND oracle-scored agent. THE MEASURED RESULT CONTRADICTED THE A1 PREDICTION (surfaced + re-measured honestly, not iterated-to-fit): the agent is a sensitivity-rich PROPOSER, not a clean precision-recoverer — vindicating propose→gate→decide.

## Objective
Build the §12 determination PRE-PROPOSER (the 6th companion LIVE loop): a thin companion agent that PROPOSES each case's determination (`file` / `cleared` / `needs-more-info` + rationale) from the §12 bundle evidence ONLY (the oracle firewall), MEASURED TWO-SIDED against the Phase-78 exogenous `intended_disposition` oracle vs the deterministic sufficiency-engine baseline, pinned via a replay quality harness (per cap-signature — 46 signatures cover all 6935 cases). Companion-only; all 9 ship dists byte-frozen; `evidence_requirements.py` BYTE-UNCHANGED (propose→gate→decide). The deliverable is the MEASUREMENT.

## Measured result (the honest two-sided headline)
A model WAS on :8080 (base-rate-informed prompt; counts-only, synthetic substrate slice): the agent eliminated all **727** KYC structural over-flags + committed `file` on **74** oracle-file cases (engine **50**), but OVER-files the volume ML class **4482** vs the engine's **593** (it files the dominant `C2|C3|C8` signature reasoning from per-case co-occurrence, blind to the population base rate). A sensitivity TRADE, not clean over-flag precision-recovery — the A1 prediction was INCOMPLETE.

## Scope (file globs)
`scripts/determination_proposer.py` · `tests/determination_proposer_quality_harness.py` · `scripts/serve_workbench.py` · `workbench.html` · `tests/workbench.test.mjs` · `tests/test_selftests.py` · `tests/fixtures/determination-proposer/**` · `docs/determination-live.md` · `docs/agentification-roadmap.md` · `CLAUDE.md` · `HANDOFF.md`

## Key constraints (all HELD)
- The ORACLE FIREWALL: the agent provably NEVER sees `intended_disposition` (`proposer_input()` strip + `assert_no_oracle_leak()` REUSED from the Phase-78 harness); the served `/propose-determination` carries no oracle on the wire — non-circular by construction (verified by the pre-push firewall review).
- propose→gate→decide / A1-frozen: the agent PROPOSES, the engine LICENSES, the human DECIDES. `evidence_requirements.py` BYTE-UNCHANGED (git-diff empty); the 256/376 funnel unchanged; build.py imports nothing new; all 9 dists byte-frozen (companion-only).
- TWO-SIDED HONEST measurement, counts-only, synthetic-substrate-qualified, word-ban (no catch-rate/lift/precision/recall). Abstention = coverage separate from accuracy.
- USER OVERRIDE (logged): the live measurement contradicted the A1 over-flag prediction → surfaced mid-build → ONE publicly-grounded base-rate-context revision + re-measure, reported honestly (NOT iterated-to-fit).

## Exit criteria (MET)
`determination_proposer --selftest` + `serve_workbench --selftest` PASS; `determination_proposer_quality_harness.py --check` green (two-sided, abstention separate, synthetic-qualified) + in `uv run pytest`; `node tests/workbench.test.mjs` green (195→205); the live headline recorded HONESTLY (counts-only, two-sided); `--check all` 9/9 byte-frozen; `evidence_requirements.py` git-diff empty; build.py companion-import grep clean; 256/376 funnel unchanged; roadmap Stage 2 marked BUILT; CLAUDE.md + HANDOFF trued IN PLACE; honesty swept.

## Abort rule
Any oracle leak / an `evidence_requirements.py` change / a build.py companion import / any of the 9 dists not byte-identical / a change to the 256/376 funnel / a fabricated live agent number → STOP-and-surface. If blocked >3 attempts: ask user — skip or abort.

## Gates
- [x] spec (`## Formal Spec` embedded in [[phases/phase-85-determination-pre-proposer]] — standard ceremony, no separate /spec round; the contract is fully determined)
- [x] Direction confirmed by user (2026-06-29, AskUserQuestion — direction = §12 determination pre-proposer; 3 assumptions ACCEPTED, all_accept tracked NOT silent; A1 substrate-recency rider DISCHARGED [HEAD 3716f77 unchanged]; ledger Phase-85)
- [x] Delivery accepted (2026-06-29 — delivery report accepted by user "OK"; impl committed 2008692 + pushed to main; all 9 dists byte-frozen, evidence_requirements.py unchanged, workbench tests 195→205; pre-push adversarial review 0 blockers/0 majors/1 nit fixed)

Decisions [[decisions/phase-85-direction-determination-pre-proposer]] · [[decisions/phase-85-oracle-firewall-non-circular]] · [[decisions/phase-85-propose-gate-decide-a1-frozen]] · [[decisions/phase-85-over-flag-headroom-not-miss-recovery]] (corrected-at-impl) · [[decisions/phase-85-base-rate-remeasure-not-overfit]] (NEW); plan [[phases/phase-85-determination-pre-proposer]]; ledger Phase-85 (revisited — A1 held-in-spirit/prediction-corrected, A2–A5 HELD).
