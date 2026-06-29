---
title: "Phase 86 — Agentification Stage 3: the STR drafter behind the verifiers, consistency-measured (the gate-bounded 4/4 tie is the finding)"
aliases: [phase-86-journal, str-drafter, agentification-stage-3, drafter-consistency-measure, gate-bounded-tie]
category: journal
tags: [agentification, stage-3, str-drafter, consistency-not-correctness, no-oracle, gate-bounded, companion, honesty, drafter-quality-harness]
parents: [phase-86-str-drafter-consistency-measure]
created: 2026-06-29
updated: 2026-06-29
source: debrief
duration: ~1 session (plan+deliver same session, post-compaction estimate)
---

# Phase 86 — Agentification Stage 3: the STR drafter behind the verifiers, consistency-measured

## What Happened

Built the agentification roadmap's **Stage 3** — turning the already-built deterministic stub STR
drafter into a CONSISTENCY-MEASURED drafting agent. The state-loader surfaced PRE-GATE that Stage 3
is NOT new infra: the STR drafter + its six Class-G verifiers ALREADY SHIPPED in Phase 57 (the Drafter
Protocol, the `--drafter {stub,claude,openai,opencode}` switch, the live-draft reveal), a live model
was up on `127.0.0.1:8080`, and the drafter has NO correctness oracle (free-text drafting). So the
deliverable was reshaped to the **MEASUREMENT FRAME** — `tests/drafter_quality_harness.py`, the GATHER
consistency-not-correctness pattern (a pure dep-free `score_drafts()` scorer: counts-only stub-vs-live
SIGN/REFUSE + fabrication-guard CATCH + grounding CONSISTENCY; `--check` replays a pinned subprocess-
result capture through the scorer; `--freeze` runs the real `serve_chain.casework_consume` stub+openai
per bundle). NO oracle firewall needed (no truth to hide — simpler than Stages 1/2).

**EXECUTE ONCE landed for real** (a model WAS on :8080) — and the measure is the **gate-bounded 4/4
tie**: over 4 designed casefile bundles the live agent drafter matched the deterministic stub 4/4 —
signed the SAME 3 (narratives the verifiers accepted), fail-closed on the SAME 1 (the narrative-seam
case `CASE-P-0025128` → casework's `needs_more_info`; no narrative the verifiers would sign), with
**0 fabrications caught + 0 recoveries**. The agent did NOT hallucinate a narrative to force a file.
THE FINDING: the drafter measure is consistency-BOUNDED by the gate — because the six verifiers refuse
anything ungrounded, a competent agent drafter and the deterministic stub CONVERGE at the gate, so the
GATE (not the drafter) determines defensibility. A tie is a real result; it vindicates
propose→gate→decide from the DRAFTING side, mirroring Stage 2's vindication from the determination
side. We deliberately did NOT contrive a deliberately-ungrounded adversarial case to force `caught>0`
(honesty over drama — the fabrication-guard-fires demo already lives in the scripted fail-closed beat;
that case is a named follow-on).

## Decisions Made

- [[phase-86-gate-bounded-drafter-tie|The drafter measure is gate-bounded; the 4/4 tie is the finding]] (high) — NEW (debrief)
- [[phase-86-no-oracle-consistency-measure|No correctness oracle — counts-only consistency, never an accuracy]] (medium) — held
- [[phase-86-stub-vs-live-narrative-seam-contrast|Non-degenerate via the stub's narrative-seam fail-close]] (medium) — held (population WAS non-degenerate at the population level; the live contrast resolved to a tie)
- [[phase-86-companion-only-casework-unchanged|Companion-only; casework + the six verifiers unchanged]] (medium) — held
- [[phase-86-direction-str-drafter-measurement|Direction = Stage 3, deliverable = the measurement frame]] (medium) — held

## Problems Solved

- The free-text drafting honesty trap — no correctness oracle exists, so the measure is counts-only
  consistency (the GATHER class), never an accuracy/catch-rate/precision/recall; a hand-authored "gold
  narrative" oracle was rejected (synthetic gold is judgment, not truth).
- The pre-delivery adversarial review's 2 MINORs (an over-attributed seam-case refusal cause) fixed
  inline — the docs now state only what the capture proves (the bundle has 36 txns; "lacks
  transaction_details" misread casework's OUTPUT completeness flag as missing INPUT data).
- The casework subprocess boundary in `--check` — `--check` replays PINNED consume results through the
  pure scorer (dep-free, no subprocess, no model), `--freeze` runs the real subprocess; the gather-
  harness shape.

## Open Questions

- None unresolved. The forward frontier (Stage 4 §14 triage second-rater, the adversarial drafter
  case, the fixture-disposition enrichment, a unified agent-eval synthesis) lives in
  `docs/agentification-roadmap.md`, not tasks.md. The signal-watch-LOCAL consume frontier stays
  substrate-gated (Ask #3 = the 2nd corroborating leg, a measured-null at substrate HEAD `3716f77`).

## Artifacts Changed

- `tests/drafter_quality_harness.py` (NEW — the pure dep-free `score_drafts()` scorer + `--check`/`--freeze`/`--selftest`, the GATHER pattern)
- `tests/fixtures/drafter-quality/drafter.replay.json` (NEW — the pinned stub+live capture + the frozen baseline)
- `tests/test_selftests.py` (registered the harness `--check`/`--selftest`; uv run pytest 32→34)
- `tests/workbench.test.mjs` (the consistency-not-correctness framing assertion; 205→206)
- `docs/drafter-live.md` (NEW — the companion walkthrough; the defensibility climax = the verifiers refuse what the agent can't ground)
- `docs/agentification-roadmap.md` (Stage 3 → BUILT/MEASURED; now two consistency-not-correctness harnesses)
- `CLAUDE.md` + `HANDOFF.md` (trued IN PLACE — no per-phase bullet)
- `vendor/aml-casework` + `scripts/evidence_requirements.py` UNCHANGED (git-diff empty); all 9 ship dists byte-frozen (`--check all` 9/9); the 256/376 §12 funnel untouched

## Related

- [[phase-86-str-drafter-consistency-measure|Phase 86 — STR drafter behind the verifiers (Agentification Stage 3)]] — parent phase
- [[phase-85-determination-pre-proposer|Phase 85 — Stage 2: the §12 determination pre-proposer]] — the mirror (vindication from the determination side)
- [[phase-83-merge-adjudicator-oracle-scored|Phase 83 — Stage 1: the merge adjudicator]] — the first oracle-scored agent

## Soft Observations / Phase N+1 Candidates

- Stage 4 — the §14 triage second-rater (the roadmap's named next leg): the §14 second-rater field is already plumbed end-to-end (curate→build→html→test) + an agreement metric; swap an agent into the slot (a live model constrained to the §14 disposition vocabulary), NO new gate code — the highest-leverage next agentification phase | `docs/agentification-roadmap.md` Stage 4
- A deliberately-ungrounded adversarial bundle to demonstrate the fabrication-guard FIRING on a live hallucination (`caught>0`) — the named follow-on this phase deliberately did NOT contrive (honesty over drama) | `docs/drafter-live.md` limitation section
- Enrich the drafter fixture with `disposition` (+ completeness) so the doc's `needs_more_info` claim is backed by the committed artifact (the review's MINOR-1 root: `_slim` drops disposition, so the fixture proves signed/narrative/violations but not the refusal TYPE) | `tests/drafter_quality_harness.py` `_slim`
- After Stage 4 the agentification track is "done" (4 stages on the loops) — a unified agent-evaluation SYNTHESIS report (all loop measures in one examinable artifact) is a candidate future phase | `docs/agentification-roadmap.md` cross-cutting section
- The signal-watch-LOCAL consume frontier stays substrate-gated (Ask #3 = the 2nd corroborating leg, a measured-null at substrate HEAD `3716f77`/Phase 41); the buildable frontier remains the agentification track (Stage 4)
