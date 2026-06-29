---
title: "Phase 83 — Agentification Stage 1: the merge adjudicator agent, oracle-scored (the 5th companion live loop; agent 54/66 vs spine 33) (standard, planned+delivered same session)"
aliases: [phase-83-journal, merge-adjudicator-stage1]
category: journal
tags: [agentification, merge, oracle, live-loop, measured-agent, firewall, companion, build-strip]
parents: [phase-83-merge-adjudicator-oracle-scored]
created: 2026-06-29
updated: 2026-06-29
source: debrief
duration: ~3h (post-compaction estimate)
---

# Phase 83 — Agentification Stage 1: the merge adjudicator agent, oracle-scored

## What Happened

Built the agentification roadmap's Stage 1 — the FIRST measurable agent + the 5th companion LIVE loop.
A companion-only **merge adjudicator** (`scripts/merge_adjudicator.py`: `StubAdjudicator` +
`LiveAdjudicator`) proposes one of `{uphold_merge, reject_as_shares, both_defensible, escalate}` +
rationale per merge case, MEASURED against the committed non-circular `GT-<hash>` oracle in
`data/merge/cases.json` (the ONE gate with a correctness oracle). The split mirrors the proven GATHER
StubPlanner/LivePlanner: the deterministic `StubAdjudicator` (echo `spine_verdict`→uphold/reject — the
dep-free offline default + the two-sided 33/66 baseline) + a `LiveAdjudicator` over
`osint_tools.call_openai`→`127.0.0.1:8080` (`parse_llm_json` fail-closed).

**The firewall** — `adjudicator_input()` strips to the evidence surface; `assert_no_oracle_leak()`
raises on any `_TRUTH_LEAK_KEYS` field (mirroring `resolution_scorer.assert_no_cluster_leak`); the
served `/adjudicate` carries no oracle pre-disposition. Surfaced as `scripts/serve_merge.py` (port
8040, stub-offline / agent-on-:8080 / degrade-to-stub) + a build-stripped `/*LIVE_*/` overlay in
`merge.html` → `dist/merge` BYTE-IDENTICAL via `--check merge`; build.py imports nothing new (grep
clean); `evidence_requirements.py` untouched (this is merge, not §12); all 9 dists byte-frozen.

**T7 EXECUTE ONCE landed for real** — a model WAS on :8080, so the live capture landed at T2's
`--freeze` (folding T7 forward). **The measured headline:** the live agent matched the oracle on
**54 of 66** scored cases vs the StubAdjudicator baseline's **33**, recovering 21 of the 33 the spine
got wrong (18 of 30 fragmentation-gaps + all 3 over-merge-traps); **0 deferrals**; counts-only, by
quadrant + provenance, synthetic-substrate-qualified, no catch-rate/lift/precision/recall.

Two build-strip traps surfaced + resolved at T4 (the live-overlay byte-identity guards): the overlay
installs by WRAPPING the reassignable `render()` declaration in-region (static live CSS/HTML survives
the strip; `CASE_SCREENS` holds stale references → wrap the call site, not the array); and the LIVE
region must carry NO trailing blank line (`LIVE_REGION_RE` eats the leading newline → a trailing blank
is a +1-newline drift, caught by `--check merge`).

## Decisions Made

- [[phase-83-merge-adjudicator-stage1-frame|Build agentification Stage 1 — the merge adjudicator]] — bumped plan→implementation, medium→high
- [[phase-83-companion-live-not-baked|Companion live mode, not a baked static replay]] — bumped →high
- [[phase-83-4way-vocab-count-deferrals|Keep the 4-way vocab; count deferrals separate]] — bumped →high
- [[phase-83-measure-by-quadrant-two-sided-baseline|Report agreement by quadrant vs a two-sided baseline]] — bumped →high
- [[phase-83-live-overlay-via-render-wrap|The LIVE overlay wraps render() inside the stripped region]] — NEW (impl)
- [[phase-83-live-region-newline-discipline|A build-stripped LIVE region carries no trailing blank line]] — NEW (impl)

## Problems Solved

- `dist/merge` drift after the strip — a +1-newline diff from a trailing blank in the LIVE region;
  fixed by inserting the region flush against the next statement (the strip already eats the leading
  newline). Caught by `--check merge` at T4.
- Live overlay bytes leaking outside the stripped region — solved by wrapping `render()` in-region +
  injecting `<style>` via JS (not static markup, not monkeypatching the reference-captured screens).

## Open Questions

- None unresolved. The forward frontier (Stage 2 §12 determination pre-proposer, etc.) lives in
  `docs/agentification-roadmap.md`, not tasks.md.

## Artifacts Changed

- `scripts/merge_adjudicator.py` (NEW — StubAdjudicator + LiveAdjudicator + the oracle firewall + counts-by-quadrant scoring; `--selftest` dep-free)
- `tests/merge_adjudicator_quality_harness.py` (NEW — `--check` dep-free stub baseline + live replay, `--freeze`; wired into `tests/test_selftests.py`)
- `scripts/serve_merge.py` (NEW — companion server port 8040; stub-offline / agent-on-:8080 / degrade-to-stub; the on-the-wire firewall)
- `merge.html` + `scripts/build.py` (the build-stripped `/*LIVE_*/` overlay + `render_merge` LIVE-strip; `dist/merge` byte-identical)
- `tests/merge-console.test.mjs` (offline-strip + live-branch tests; ~76→100 assertions)
- `tests/fixtures/merge-adjudicator/adjudicator.replay.json` (NEW — the pinned live capture; `live_expected.calls = {reject_as_shares:45, uphold_merge:21}`, deferred 0)
- `docs/merge-live.md` (NEW) · `docs/agentification-roadmap.md` (Stage 1 → BUILT) · `CLAUDE.md` (current-state trued in place) · `HANDOFF.md` §8

## Related

- [[phase-83-merge-adjudicator-oracle-scored|Phase 83 — Agentification Stage 1: the merge adjudicator agent, oracle-scored]] — parent phase

## Soft Observations / Phase N+1 Candidates

- The live agent used **0 deferrals** (committed a binary call on every case) — the 4-way vocab's defer
  option went unexercised live | a deferral/anchoring ablation (prompt the agent to defer on genuine
  ambiguity, or HIDE `spine_verdict` from the evidence and re-measure to test spine-anchoring) | evidence: `tests/fixtures/merge-adjudicator/adjudicator.replay.json`
- Stage 2 of the agentification roadmap — a §12 determination pre-proposer (the `determine_case` seam
  is built; light dependency; no correctness oracle → a consistency-not-correctness measure) — is the
  next leg | `docs/agentification-roadmap.md`
- The deferred (B) option — baking the agent's measured beat into the OFFLINE `dist/merge` as a static
  pinned second-rater replay (no model) — remains a possible follow-on if a stakeholder wants the
  headline by opening the file without a server
- The by-quadrant measurement is small-N on two quadrants (over-merge-trap=3, real-co-reference=3); a
  richer substrate slice would strengthen those cells
