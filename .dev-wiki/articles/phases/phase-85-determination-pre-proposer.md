---
title: "Phase 85: §12 determination pre-proposer — the 6th live loop, oracle-scored (Agentification Stage 2)"
aliases: [phase-85, determination-pre-proposer, agentification-stage-2, sixth-live-loop]
category: phases
tags: [agentification, determination, oracle, live-loop, measurement, companion, firewall]
parents: [phase-83-merge-adjudicator-oracle-scored, phase-78-consume-disposition-validation-control, phase-82-consume-sibling-northstar-evidence-at-scale]
created: 2026-06-29
updated: 2026-06-29
source: plan
status: active
scope: ["scripts/determination_proposer.py", "tests/determination_proposer_quality_harness.py", "scripts/serve_workbench.py", "workbench.html", "tests/workbench.test.mjs", "tests/test_selftests.py", "tests/fixtures/determination-proposer/**", "docs/determination-live.md", "docs/case-workbench.md", "docs/agentification-roadmap.md", "CLAUDE.md", "HANDOFF.md"]
entry_criteria: "Phase 84 DELIVERED + accepted 2026-06-29 (impl a3e669a; all 9 dists byte-frozen, evidence_requirements.py untouched). The consume/render frontier is closed; every substrate-gated path is a verified dead-end at substrate HEAD 3716f77 (code-verified this session, UNCHANGED since Phase 84's pin — last substrate phase still Phase 41, Ask #3 measured-null). The agentification roadmap names Stage 2 (the §12 determination pre-proposer) as the next leverage item after Phase 83's merge adjudicator. The seams are all built: determine_case(named_risk=, mitigation_established=) override kwargs, the Phase-78 non-circular exogenous intended_disposition oracle + assert_no_oracle_leak firewall, the Phase-83 replay-harness + build-stripped-overlay pattern."
exit_criteria: "All 6 tasks [x]. determination_proposer --selftest + serve_workbench --selftest PASS; determination_proposer_quality_harness.py --check green (two-sided counts, abstention separate, synthetic-substrate-qualified). node tests/workbench.test.mjs green (count grows from 195). The live headline recorded honestly (counts-only, two-sided) OR the stub baseline + the one-command --freeze fold-forward note. Companion-only: --check all 9/9 byte-frozen; evidence_requirements.py git-diff empty; build.py imports nothing new (grep clean); the 256/376 signing funnel unchanged. Roadmap Stage 2 marked BUILT (the 6th live loop). CLAUDE.md + HANDOFF trued IN PLACE (no per-phase bullet). Honesty swept (no catch-rate/lift/precision/recall in the new files/docs)."
---

# Phase 85: §12 determination pre-proposer — the 6th live loop, oracle-scored (Agentification Stage 2)

## Objective

Build the agentification roadmap's **Stage 2** — the §12 determination pre-proposer (the 6th companion
live loop, the SECOND oracle-scored agent): a companion agent that PROPOSES each case's determination
(`file` / `cleared` / `needs-more-info` + a rationale) from the assembled §12 bundle evidence ONLY (the
oracle firewall), MEASURED TWO-SIDED against the Phase-78 exogenous `intended_disposition` oracle versus
the deterministic sufficiency-engine baseline, pinned via a replay quality harness. Companion-only — all
9 ship dists byte-frozen, `evidence_requirements.py` BYTE-UNCHANGED (the agent proposes, the engine
licenses, the human decides). The deliverable is the MEASUREMENT; the agent is thin.

## Why now / why this shape

The consume and render frontiers are closed (Phases 80–84); every substrate-gated path is a verified
dead-end at substrate HEAD `3716f77` (unchanged since Phase 84's pin — code-verified this session, the
last substrate phase is still Phase 41, Ask #3 a measured-null). The agentification roadmap is the
signal-watch-internal forward path, and Stage 2 (the §12 determination pre-proposer) is the next
leverage item after Stage 1 (the merge adjudicator). It mirrors Phase 83 exactly, and every seam it
needs already exists:

- the `determine_case(named_risk=, mitigation_established=)` override kwargs (the engine reads evidence
  as DATA — the §12 bundle assembler `_bundle_evidence`);
- the Phase-78 NON-CIRCULAR exogenous `intended_disposition` oracle (authored blind to the sufficiency
  rule) + `assert_no_oracle_leak()` (the allow-list firewall) + the
  `determination_validation_harness` (re-runs the engine per case, bundle-only, oracle held out);
- the Phase-83 replay-harness (`--check`/`--freeze`) + the build-stripped `/*LIVE_*/` overlay pattern.

The agent sees the same bundle evidence `_bundle_evidence` assembles (grounded predicate + mitigation +
legs + KYC — all record-sourced) and proposes one of file/cleared/needs-more-info.

## The asymmetry (load-bearing — read before reading the measurement)

Unlike Phase 83's symmetric two-sided headroom (the merge spine got 33 of 66 wrong in BOTH directions),
the §12 engine's error mass is structural OVER-FLAG: Phase-78 pre-measured all 727 KYC-pure cases as
file-ready-but-oracle-clear + 593/6087 file-ready-but-clear. The file-MISS side is a DATA gap — the 71
of 121 missed oracle-file cases miss because the 2nd corroborating leg is not in the bundle (substrate
Ask #3 measured-null). An agent reasoning over the SAME bundle the engine sees cannot recover what is
not there. So the agent's measurable HEADROOM is over-flag CORRECTION on the CLEAR side; the
file-misses are HONESTLY NULL — and that null is itself the finding (it demonstrates the misses are
substrate-gated, not reasoning-gated; the Phase-84 decisiveness handoff, now measured). This phase does
NOT promise a Phase-83 "54-vs-33"-shaped recall-recovery story. See
[[phase-85-over-flag-headroom-not-miss-recovery]].

## Measured result (the prediction above was INCOMPLETE — the honest two-sided outcome)

The live measurement (a local Qwen MoE, base-rate-informed prompt, the full 6935-case capture via 46
cap-signatures; counts only, synthetic substrate slice) CONTRADICTED the optimistic half of the
asymmetry prediction and was surfaced to the user mid-implementation. The user's call: add base-rate
context to the prompt and re-measure (ONE principled revision, not iterated-to-fit against the oracle).

- The agent DID correct the structural KYC over-flag: it abstains on all **727** KYC-pure cases the rigid
  rule marks file-ready (the predicted over-flag win HELD on the KYC class).
- The agent recovers MORE oracle-file cases: it commits `file` on **74** (vs the engine's **50**) — higher
  file sensitivity.
- BUT the agent OVER-files on the volume ML class: committed-wrong **4482** vs the engine's **593**. Even
  given the public base-rate context, it files the dominant `C2|C3|C8` signature (4040 cases, 4029 benign)
  because it reasons from per-case red-flag CO-OCCURRENCE — the benign-ness is a POPULATION property
  invisible in a single case, which the calibrated deterministic rule encodes and the per-case agent
  cannot infer.

So the agent did NOT cleanly "recover precision on the over-flag" as predicted — it TRADES the engine's
conservatism for sensitivity (recovers files + fixes the KYC over-flag, over-files on ML). The honest
finding VINDICATES propose→gate→decide: the agent is a sensitivity-rich PROPOSER; the deterministic
engine + the human gate supply the population-calibrated discipline. The measurement is the deliverable,
not a target. Full headline + walkthrough: `docs/determination-live.md`; roadmap Stage 2 marked BUILT.

## Formal Spec

> Standard-ceremony spec captured in-article (no separate `/spec` round; the contract is fully
> determined — every seam is built, the measurement frame is fixed by Phase 78).

**Objective.** Build the §12 determination pre-proposer — the 6th live loop, Agentification Stage 2 — a
companion agent that proposes `file` / `cleared` / `needs-more-info` (+ rationale) from the §12 bundle
evidence ONLY (oracle firewall), measured TWO-SIDED against the exogenous `intended_disposition` oracle
vs the deterministic engine baseline; companion-only, all 9 dists byte-frozen,
`evidence_requirements.py` untouched.

**In scope.** `scripts/determination_proposer.py` ·
`tests/determination_proposer_quality_harness.py` · the `/propose-determination` route in
`serve_workbench.py` · the proposal UI in `workbench.html` + `tests/workbench.test.mjs` · the pinned
baseline/capture under `tests/fixtures/determination-proposer/` · docs (`docs/determination-live.md`
or `docs/case-workbench.md` extension) + `docs/agentification-roadmap.md` (Stage 2 → BUILT) +
CLAUDE.md + HANDOFF.

**Out of scope (substrate-gated).** Decisiveness on the slice (FILE/CLEAR at scale — Ask #3
measured-null) · miss-side recall recovery · any `evidence_requirements.py` change · any new ship-dist
artifact.

**Constraints (load-bearing).**
1. The oracle firewall — the agent NEVER sees `intended_disposition`; the served response carries no
   oracle field on the wire (`proposer_input()` strip + `assert_no_oracle_leak()` reusing the Phase-78
   allow-list). Non-circular by construction. See [[phase-85-oracle-firewall-non-circular]].
2. propose→gate→decide — the agent proposes, the deterministic engine LICENSES, the human DECIDES;
   `evidence_requirements.py` BYTE-FROZEN; the proposal is presentation/measurement-only. See
   [[phase-85-propose-gate-decide-a1-frozen]].
3. Two-sided HONEST measurement — agent-vs-oracle AND engine-vs-oracle, on file AND clear; counts-only;
   the synthetic-substrate qualifier on every number; the word-ban (no catch-rate/lift/precision/recall)
   extends to the new render markers + docs.
4. Abstention = coverage SEPARATE from accuracy — needs-more-info is reported as a coverage figure,
   never scored as a wrong-file nor as a correct call; {committed-accuracy, abstention-coverage} are
   two numbers.
5. Companion-only — build.py imports nothing new (grep guard); all 9 dists byte-frozen; the workbench
   touches no dist.

**Checkpoints.** After T1 (the firewall + the stub baseline green — the dep-free measured floor); after
T4 (the UI + the served firewall, PRE-measurement); after T5 (the live headline OR the stub baseline +
the fold-forward note).

**Exit criteria.** See `## Exit Criteria` below (bidirectional with tasks T1–T6).

**Assumptions.** See `## Assumptions` below; each has a stop-if-violated fallback (assumption-ledger
Phase-85).

**Abort rule.** Any oracle leak (into the proposer input or onto the wire pre-decision) / an
`evidence_requirements.py` change / a build.py companion import / any of the 9 dists not byte-identical
/ a miss-side recovery story / any number framed as catch-rate/lift/precision/recall / a fabricated
live agent number → STOP-and-surface. If blocked >3 attempts: ask user — skip or abort.

## Scope

Files and modules affected (companion-only — NO ship/dist target; build.py imports none of it):
- `scripts/determination_proposer.py` — `StubProposer` (echo the engine verdict = offline default +
  reference) + `LiveProposer` (openai-compatible model on `127.0.0.1:8080`) + `proposer_input()` strip
  + `assert_no_oracle_leak()` + the two-sided + abstention scorer
- `tests/determination_proposer_quality_harness.py` — `--check` (dep-free replay + stub baseline) /
  `--freeze` (one live capture); wired into `tests/test_selftests.py`
- `scripts/serve_workbench.py` — the single-flight `/propose-determination` route (no oracle on the
  wire; 409 on concurrent; stub/live/degrade)
- `workbench.html` + `tests/workbench.test.mjs` — the proposal panel beside the DETERMINATION beat
  ("proposed, not decided" + the synthetic qualifier + the two-sided framing); the human gate licensing
  path byte-unchanged
- `tests/fixtures/determination-proposer/**` — the pinned live capture (or pending)
- `docs/determination-live.md` (or `docs/case-workbench.md` extension) + `docs/agentification-roadmap.md`
  (Stage 2 → BUILT) + CLAUDE.md + HANDOFF — current-state true-up (replace in place; no per-phase bullet)

## Exit Criteria

- [ ] `python3 scripts/determination_proposer.py --selftest` PASS (firewall rejects an oracle leak +
      `proposer_input` strips it; StubProposer echoes the engine verdict; the stub baseline reproduces
      the engine-vs-oracle two-sided confusion; no banned words)
- [ ] `python3 tests/determination_proposer_quality_harness.py --check` green; the two-sided confusion
      counts (agent-vs-oracle, engine-vs-oracle, on file AND clear) + the abstention-coverage figure
      match the committed baseline; in `uv run pytest`
- [ ] `python3 scripts/serve_workbench.py --selftest` PASS incl. the `/propose-determination` route +
      the on-the-wire oracle firewall + single-flight + stub/live/degrade
- [ ] `node tests/workbench.test.mjs` green (count grows from 195): the proposal panel renders;
      "proposed, not decided" + the synthetic qualifier present; `intended_disposition`/oracle NEVER
      appears pre-decision; the human gate licensing unchanged; a firewall-clean `/propose-determination`
      request fires
- [ ] The live headline recorded HONESTLY (counts-only, two-sided, synthetic-qualified — over-flag
      precision-recovery + the file-miss NULL) if a model was reachable on :8080; ELSE the stub baseline
      + the one-command `--freeze` fold-forward note
- [ ] Companion-only: `python3 scripts/build.py --check all` 9/9 byte-frozen; `git diff --quiet
      scripts/evidence_requirements.py`; build.py imports nothing new (grep:
      determination_proposer|serve_workbench|curate_workbench|casework|entity_spine); the 256/376 funnel
      unchanged
- [ ] `docs/agentification-roadmap.md` Stage 2 marked BUILT (the 6th live loop); CLAUDE.md `## Current
      state` + Milestones + How-to-run + Test list + HANDOFF §8 trued IN PLACE
- [ ] Honesty swept (no catch-rate/lift/precision/recall in the new files/docs; the synthetic qualifier
      on every recorded number; abstention reported as coverage separate from accuracy)

## Constraints

- The oracle firewall — non-circular by construction; prevents a tautology dressed as a measurement
  (the Phase-77 trap). See [[phase-85-oracle-firewall-non-circular]].
- propose→gate→decide / A1-frozen — `evidence_requirements.py` BYTE-UNCHANGED; prevents the proposal
  influencing the decision (and prevents the circular self-score). See
  [[phase-85-propose-gate-decide-a1-frozen]].
- Two-sided counts-only honesty + the over-flag-not-miss framing — prevents a one-sided number / a
  Phase-83-shaped recall-recovery overclaim the data does not support. See
  [[phase-85-over-flag-headroom-not-miss-recovery]].
- Abstention = coverage separate from accuracy — prevents needs-more-info being scored as a wrong-file
  (understates) or as correct (overstates).
- Companion-only / dist boundary — all 9 dists byte-frozen; build.py imports nothing new; prevents a
  ship/dist drift or the companion layer crossing into the build.

## Checkpoints

- After T1 (the dep-free `--check` harness): the StubProposer baseline (the engine-vs-oracle two-sided
  confusion) is the always-checkable measured floor — it ships regardless of model availability.
- At T5 (EXECUTE ONCE): if no model is reachable on :8080, STOP fabricating — ship the stub baseline +
  flag the live agent capture as a named follow-on (the Phase-83 contract). Never invent a live number.

## Assumptions

(assumption-ledger Phase-85 — all 5 ACCEPTED, all_accept: true NOT silent; A1's substrate-recency rider
DISCHARGED — HEAD `3716f77` unchanged.)

- A1 [the T0 weakest, the headroom shape] The agent's measurable headroom is the OVER-FLAG / CLEAR side
  (the engine's 727 KYC-pure + 593/6087 file-ready-but-clear over-flags), NOT the file-MISS side (a DATA
  gap — substrate Ask #3 measured-null). If false (the over-flag mass were absent — Phase-78 says it is
  not): reframe to the §12-discovery-feed queue-prioritizer fallback.
- A2 [measure/execute-once] The StubProposer measurement (echo the engine verdict) is ALWAYS available;
  the live agent capture is best-effort. If no model this session: the stub baseline + firewall +
  harness + UI ship as the measured deliverable; the live freeze is a named follow-on; NEVER fabricate.
- A3 [abstention semantics] needs-more-info is scored as a SEPARATE coverage figure, never as a
  wrong-file nor as correct; {committed-accuracy, abstention-coverage} are two numbers. The deterministic
  engine baseline is scored identically.
- A4 [the oracle firewall — NON-NEGOTIABLE] The agent provably never sees `intended_disposition`; the
  served response carries no oracle on the wire. If a leak: STOP-and-surface (the abort rule).
- A5 [propose→gate→decide / A1-frozen — NON-NEGOTIABLE] The agent proposes, the engine licenses, the
  human decides; `evidence_requirements.py` byte-unchanged, the 256/376 funnel unchanged, all 9 dists
  byte-frozen. If the proposal would feed the bar: STOP-and-surface (the abort rule).

## Notes

- Mirrors Phase 83 (the merge adjudicator, the 5th live loop) — the StubProposer/LiveProposer split,
  the firewall, the replay harness, the build-stripped overlay, the counts-only honesty. The difference
  is the asymmetric headroom (over-flag, not symmetric) and the binary-oracle-vs-three-way-output
  abstention semantics.
- The seam `determine_case(named_risk=, mitigation_established=)` and the Phase-78 oracle/firewall/harness
  are code-verified built this session — no new substrate or casework dependency.
- The 6 live loops after this phase: news/corpus extraction · GATHER tool-calling · DECIDE drafting · the
  merge adjudicator (Stage 1, oracle-scored) · this §12 determination pre-proposer (Stage 2,
  oracle-scored). The next legs in leverage order: a real STR drafter (Stage 3 — the Drafter Protocol
  exists) → a §14 triage second-rater.
- Substrate HEAD `3716f77` is the same pin Phase 84 verified; Ask #3 (the 2nd corroborating FILE-side
  leg) is the Phase-41 measured-null that makes the file-miss row honestly NULL. The decisive half stays
  substrate-gated — this phase MEASURES that boundary, it does not move it.
