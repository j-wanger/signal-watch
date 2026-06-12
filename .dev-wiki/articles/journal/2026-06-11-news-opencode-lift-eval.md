---
title: "News-side opencode lift eval (post-phase segment, after Phase 46 close)"
aliases: []
category: journal
tags: [opencode, news, live-mode, harness-probe, grounding, agent-loop, eval]
parents: [phase-46-corpus-live-derivation]
created: 2026-06-11
updated: 2026-06-11
source: debrief
duration: unknown
---

# News-side opencode lift eval — post-Phase-46 segment (user-directed)

POST-PHASE session segment (the booth.html 2026-06-10 one-off precedent): Phase 46 was already
closed (delivered + accepted + committed 5981b41 + gate-flip 4cf6cbb, pushed). This segment ran
the previously-staged SEPARATE eval the Phase-46 checkpoint deferred, plus one wiki capture.
ZERO repo-file changes — all artifacts in gitignored `.dev-wiki/tmp/ph46/` + the aml-wiki inbox.

## What Happened

- Ran the staged A/B: **opencode 1.17.3 agent loop vs the direct single-shot baseline** on
  ofac-sinaloa-fentanyl (the hardest committed fixture: 11.5K chars, 25 entities); committed news
  prompt/schema BOTH sides; current Qwen3.6-35B; `ph46_news_gate.py` (build_record + ground_record
  imported untouched) as backpressure.
- MEASURED — the iterate-on-gate-failure loop ENGAGED here (unlike the corpus probe) and delivered
  real lift exactly where the corpus probe's corollary predicted:
  - red flags **12/12 grounded vs 4/5** (3× grounded count; all 5 iteration drops recovered by requoting)
  - relationships **22/23 vs 4/25** (5.5×; 18 dropped evidences recovered by exact-byte requoting,
    2 ungroundable honestly pruned)
  - entities 23/25 vs 24/25 (par)
  - aliases **0 vs 22 — SILENT REGRESSION**: the agent optimized what the gate report surfaced and
    neglected what it didn't
  - wall: quality plateaued ~20 min, did NOT self-terminate, externally KILLED at ~25 min
    (12 gate runs / 27 tool calls / 0 tool-call failures) vs **129.5s** single shot.
- CONCLUSION RECORDED (a finding, NOT an adoption decision — no phase commitment): the corpus-probe
  corollary HELD — the loop earns its keep only where the baseline measurably leaves recoveries
  (news YES, corpus NO). Production use would mandate a max-iteration cap. The FOLD-IT-IN pattern
  applies again: a deterministic REQUOTE-RETRY pass for the news pipeline (post-grounding, ONE
  re-prompt with dropped relationship evidences + drop reasons, asking only for exact-byte requotes)
  is the named next-phase candidate — composes with the Phase-44 wrap-tolerant locate_span.
- WIKI CAPTURE (user-approved): the agent-runtime-adoption-probe pattern → aml-wiki
  `inbox/2026-06-11-agent-runtime-adoption-probe.md` (reviewer 9/10 accept; 2 new tag proposals
  llm-extraction/validation-gates flagged for absorb). Its predicted corollary (the 21/25 dropped
  relationships as the lift site) is now MEASURED FACT — add a one-line confirmation at absorb.

## Open Questions

- Whether/when to build the news requote-retry pass (future /dev-plan candidate, joins the DEFERRED
  list; evidence: the measured 5.5× relationship recovery).
- The alias-regression lesson: agent loops optimize the surfaced gate dimensions and silently
  neglect unsurfaced ones — any future loop's backpressure report must surface EVERY quality
  dimension (alias counts included).

## Artifacts Changed

- `.dev-wiki/tmp/ph46/ph46_probe.md` (ADDENDUM appended — gitignored, LOCAL-ONLY)
- `.dev-wiki/tmp/ph46/{oc-news-final-verdict.json, news-direct-verdict.json, oc-news-run.jsonl}` (107 events; pinned, gitignored)
- aml-wiki `inbox/2026-06-11-agent-runtime-adoption-probe.md` (external wiki, not this repo)
- NO repo file changed; all suites were green at the Phase-46 close earlier this session.

## Related

- [[phase-46-corpus-live-derivation|Phase 46: Corpus live derivation mode]] — parent phase (closed; this eval was its explicitly-SEPARATE staged follow-up)
- [[2026-06-11-phase-46-corpus-live-derivation]] — the phase journal (untouched)

## Soft Observations / Phase N+1 Candidates

- News REQUOTE-RETRY pass | deterministic ONE-re-prompt fold-in post-grounding | measured: 18/21 dropped relationship evidences + all 5 dropped flags recoverable by requoting — most of the 5.5× at single-call cost, without the alias regression or the termination problem (ph46_probe.md ADDENDUM).
- Backpressure-report COMPLETENESS | the agent maximized exactly the printed dimensions (flags, relationships) and produced ZERO aliases | any loop's stop/maximize criteria must enumerate every quality dimension explicitly.
- Agent NON-TERMINATION | spun ~5 min past its quality plateau, required an external kill | opencode's per-agent `max` iteration cap (user's practitioner report) is mandatory equipment for unattended use.
- aml-wiki inbox entry gains the news-confirmation line at absorb (predicted corollary → measured fact).
