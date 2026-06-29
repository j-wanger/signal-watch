---
title: "Phase 86 — The drafter measure is gate-bounded; the live-vs-stub 4/4 tie is the finding"
aliases: [phase-86-gate-bounded-tie, drafter-tie, gate-bounded-drafter, consistency-tie-is-a-result]
category: decisions
tags: [agentification, stage-3, str-drafter, consistency-not-correctness, gate-bounded, propose-gate-decide, honesty, debrief]
parents: [phase-86-str-drafter-consistency-measure]
created: 2026-06-29
updated: 2026-06-29
source: debrief
confidence: high
---

## Context

Phase 86 measured the live (local) STR drafter against the deterministic stub drafter over the
designed casefile bundles — the consistency-not-correctness frame (no correctness oracle; free-text
drafting). The gate-time A1 prediction was that the narrative-seam case (`CASE-P-0025128`, the
stub's fail-close) would be the two-sided contrast — would the live agent SIGN where the stub
couldn't, or get CAUGHT by the fabrication guard? The EXECUTE-ONCE live capture had to be read
straight, whatever it showed.

## Decision

Record the honest outcome: over the 4 designed bundles the live agent drafter matched the
deterministic stub **4/4** — signed the SAME 3 (narratives the six Class-G verifiers accepted) and
fail-closed on the SAME 1 (the narrative-seam case → casework's `needs_more_info`; no narrative the
verifiers would sign), with **0 fabrications caught** and **0 recoveries**. The agent did NOT
hallucinate a narrative to force a file.

THE FINDING: the drafter measure is consistency-**bounded by the gate**. Because the six deterministic
verifiers refuse anything ungrounded, a competent agent drafter and the deterministic stub
**converge at the gate** — so the GATE (not the drafter) determines defensibility. A tie is a real
result (as it would have been for Stage 1's merge adjudicator); it vindicates propose→gate→decide
from the DRAFTING side, mirroring Stage 2's vindication from the determination side.

Rejected: contriving a deliberately-ungrounded adversarial case to force `caught>0` — honesty over
drama. The fabrication-guard-fires demonstration already lives in the scripted fail-closed beat; the
adversarial case is a named follow-on, not a manufactured contrast.

## Consequences

- The deliverable IS the measurement (the GATHER-pattern consistency frame), reported counts-only +
  small-synthetic-qualified, no rate words. The tie is recorded as the floor finding, not dressed up.
- Honest limitation stated plainly: this population does not exercise the discriminating behaviors
  (`recovered=0`, `caught=0`) — the tie does not prove the agent can never beat the stub; it shows the
  gate bounds the drafter on these designed scenarios.
- Roadmap Stage 3 is BUILT + MEASURED (now two consistency-not-correctness harnesses — GATHER + the
  drafter). The named follow-ons: the deliberately-ungrounded adversarial bundle (to fire the
  fabrication guard live, `caught>0`), the fixture `disposition` enrichment, and — after Stage 4 — a
  unified agent-evaluation synthesis report.
- A1 held in discipline (the tie reported straight, the "honest NULL if degenerate" clause honored in
  spirit) even though the predicted two-sided live contrast went unexercised.

## Related

- [[phase-86-no-oracle-consistency-measure]] — the counts-only measure shape this finding lives inside
- [[phase-86-stub-vs-live-narrative-seam-contrast]] — the non-degeneracy basis (stub fail-closes on the seam case)
- [[phase-85-determination-pre-proposer|Phase 85]] — Stage 2's vindication from the determination side (the mirror)
