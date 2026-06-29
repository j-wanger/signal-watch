---
title: "Phase 85 — Agentification Stage 2: the §12 determination pre-proposer, oracle-scored (the 6th companion live loop; the A1 over-flag prediction was contradicted + re-measured honestly)"
aliases: [phase-85-journal, determination-pre-proposer, agentification-stage-2, sixth-live-loop]
category: journal
tags: [agentification, determination, oracle, live-loop, measured-agent, firewall, companion, base-rate, honesty]
parents: [phase-85-determination-pre-proposer]
created: 2026-06-29
updated: 2026-06-29
source: debrief
duration: ~3h (post-compaction estimate)
---

# Phase 85 — Agentification Stage 2: the §12 determination pre-proposer, oracle-scored

## What Happened

Built the agentification roadmap's **Stage 2** — the 6th companion LIVE loop + the SECOND oracle-scored
agent, mirroring Phase 83's merge adjudicator exactly. A companion-only **determination pre-proposer**
(`scripts/determination_proposer.py`: `StubProposer` + `LiveProposer`) proposes one of
`{file, cleared, needs-more-info}` + rationale per §12 case from the assembled bundle evidence ONLY (the
oracle firewall), MEASURED TWO-SIDED against the Phase-78 exogenous `intended_disposition` oracle
(file|clear) vs the deterministic sufficiency-engine baseline. The agent is THIN by design — it is a
THIN layer ON TOP of the Phase-78 `determination_validation_harness`, REUSING its `proposer_input` /
`assert_no_oracle_leak` / `classify` / CAPTURE. It proposes per cap-signature, so **46 signatures cover
all 6935 capture cases** (full population, no sampling).

**The firewall** — `proposer_input()` strips to the evidence surface; `assert_no_oracle_leak()` raises
on any leaked `intended_disposition` (the reused Phase-78 allow-list); the served
`/propose-determination` carries no oracle on the wire (single-flight, 409 on concurrent,
stub/live/degrade). `evidence_requirements.py` BYTE-UNCHANGED (the agent proposes, the engine licenses,
the human decides — propose→gate→decide); build.py imports nothing new (grep clean); all 9 ship dists
byte-frozen; the 256/376 signing funnel unchanged.

**T5 EXECUTE ONCE landed for real** — a model WAS on :8080, so the live capture landed (folding the
execute-once forward). **And the measurement CONTRADICTED the A1 prediction.** The A1 row said the
agent's headroom was clean precision-recovery on the engine's structural over-flag, with the file-misses
honestly NULL. The live capture (a local Qwen MoE, base-rate-informed prompt, counts only, synthetic
substrate slice) showed instead a **sensitivity TRADE**:

- the agent DID correct the structural KYC over-flag — abstains on all **727** KYC-pure file-ready cases
  (the predicted over-flag win HELD on the KYC class);
- it recovers MORE oracle-file cases — committed `file` on **74** vs the engine's **50**;
- BUT it OVER-files on the volume ML class — committed-wrong **4482** vs the engine's **593**, because it
  files the dominant `C2|C3|C8` signature (4040 cases, 4029 benign) reasoning from per-case red-flag
  CO-OCCURRENCE — the benign-ness is a POPULATION base-rate property invisible in a single case.

The orchestrator SURFACED the contradiction mid-build (not silent — the honesty governor). The user's
call: add the public TM false-positive / population base-rate context to the prompt and RE-MEASURE ONCE
(one principled, publicly-grounded revision — NOT iterated-to-fit against the oracle). The over-file
persisted even with base-rate context. The honest two-sided finding stands as the deliverable, and it
VINDICATES propose→gate→decide: a sensitivity-rich PROPOSER, the deterministic engine + the human gate
supplying the population-calibrated discipline.

## Decisions Made

- [[phase-85-direction-determination-pre-proposer|Direction = the §12 determination pre-proposer (Stage 2)]] (medium) — confirmed at impl
- [[phase-85-oracle-firewall-non-circular|The agent never sees the oracle — non-circular by construction]] (medium) — held, verified by the pre-push firewall review
- [[phase-85-propose-gate-decide-a1-frozen|propose→gate→decide — evidence_requirements.py byte-frozen]] (medium) — held, git-diff empty
- [[phase-85-over-flag-headroom-not-miss-recovery|The headroom shape — CORRECTED at impl]] (medium, status: corrected-at-impl) — the prediction was INCOMPLETE; replaced by the honest sensitivity-trade finding
- [[phase-85-base-rate-remeasure-not-overfit|Add base-rate context + re-measure ONCE, not iterate-to-fit]] (high) — NEW (impl); the mid-build USER OVERRIDE call

## Problems Solved

- The A1 over-flag-recovery prediction was wrong-shaped — surfaced (not silent), re-measured ONCE with
  publicly-grounded base-rate context, reported honestly. The honest finding (a sensitivity trade) is
  the deliverable; not iterated-to-fit against the single synthetic oracle (no held-out set exists).
- The 6935-case full population covered without sampling — the agent proposes per cap-signature, so 46
  distinct signatures (temperature 0, deterministic) cover every case; the capture replays by signature.
- The live-transport error path on `/propose-determination` returned a dropped connection on a model
  error — caught by the pre-push adversarial review (the served-route dimension); fixed INLINE to return
  a clean named error, mirroring `_gather`'s catch.

## Open Questions

- None unresolved. The forward frontier (Stage 3 STR drafter, etc.) lives in
  `docs/agentification-roadmap.md`, not tasks.md. The signal-watch-LOCAL consume frontier stays
  substrate-gated (Ask #3 = the 2nd corroborating leg, a measured-null at substrate HEAD `3716f77`).

## Artifacts Changed

- `scripts/determination_proposer.py` (NEW — StubProposer + LiveProposer + the reused firewall + the two-sided/abstention scorer + the 46-signature cache; `--selftest` dep-free)
- `tests/determination_proposer_quality_harness.py` (NEW — `--check` dep-free stub baseline + live replay-by-signature, `--freeze`; registered in `tests/test_selftests.py`, +2)
- `scripts/serve_workbench.py` (the single-flight `/propose-determination` route; no oracle on the wire; stub/live/degrade; the inline transport-error fix)
- `workbench.html` + `tests/workbench.test.mjs` (the pre-proposer panel beside the UNCHANGED human gate; "proposed, not decided" + synthetic qualifier + no-oracle-pre-decision; tests 195→205)
- `tests/fixtures/determination-proposer/**` (the pinned base-rate-informed live capture + the stub baseline)
- `docs/determination-live.md` (NEW — the companion walkthrough) · `docs/agentification-roadmap.md` (Stage 2 → BUILT, 6 live loops) · CLAUDE.md + HANDOFF §8 (trued in place)

## Related

- [[phase-85-determination-pre-proposer|Phase 85 — §12 determination pre-proposer: the 6th live loop, oracle-scored (Agentification Stage 2)]] — parent phase
- [[phase-83-merge-adjudicator-oracle-scored|Phase 83 — Agentification Stage 1: the merge adjudicator]] — the mirrored machinery (Stage 1)
- [[phase-78-consume-disposition-validation-control|Phase 78]] — the non-circular oracle + firewall + harness this phase is a thin layer over

## Soft Observations / Phase N+1 Candidates

- Stage 3 (the STR drafter) is the roadmap's next agentification leg — the Drafter Protocol + a `--drafter` switch already exist, near-zero new code; local + buildable | `docs/agentification-roadmap.md`
- The agent's per-cap-signature determinism (46 signatures, temperature 0) is a clean property — a "decision table" render of the agent's policy could be a small follow-on | `scripts/determination_proposer.py`
- The over-file finding (the per-case agent lacks the population base-rate prior) suggests a base-rate-aware tool (a population prior / a held-out calibration set) — but it must avoid overfitting to the single oracle (no held-out set exists); needs careful honest framing | [[phase-85-base-rate-remeasure-not-overfit]]
- A defer/anchoring ablation (does the agent abstain MORE when prompted it may?) — the merge adjudicator had 0 deferrals; here the agent abstained on the KYC class + several signatures; abstention behavior is measurable | `tests/fixtures/determination-proposer/`
- The signal-watch-LOCAL consume frontier stays substrate-gated (Ask #3 = the 2nd corroborating leg, a measured-null at substrate HEAD `3716f77`/Phase 41); the buildable frontier is the agentification track (Stages 3/4), not a consume | `docs/substrate-northstar-evidence-emission-PLAN-BRIEF.md`
