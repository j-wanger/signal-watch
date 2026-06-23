---
title: "Phase 70: Gather extraction quality (measured) + the consolidated §12 substrate handoff"
aliases: []
category: journal
tags: [gather-quality, measure-first, substrate-handoff, companion, lfcm, lite]
parents: [phase-70-gather-quality-substrate-handoff]
created: 2026-06-22
updated: 2026-06-22
source: debrief
duration: ~1 session
---

# Phase 70: Gather extraction quality (measured) + the consolidated §12 substrate handoff

## What Happened
- Two halves over one spine (the §12 discovery loop): (A) measure + fix the live GATHER's under-extraction; (B) consolidate the proliferating sibling-substrate asks into ONE pinned §12 handoff brief.
- **Measure-first via the stub-as-reference:** gather quality = live recall vs the deterministic StubPlanner (consistency-not-correctness, ZERO catch-rate), NOT model-tuning. The stub grounds a finding per surfaced record → it IS the reference. Added a `coverage` measuring stick (grounded findings vs records returned; targeted-atom closure) to the gather loop + NDJSON stream.
- **A1 (T0 weakest) DON'T-KNOW → defended down-scope:** the live BASELINE diagnosed the under-extraction surface BEFORE any fix. It confirmed the surface = the live `LivePlanner.findings()` prompt (NOT tool-surface / corpus / leg-mapping — the code-verified root cause held).
- **The fix** (T2) = both LivePlanner prompts: `findings()` now sees each record's declared_entities + extracts a finding per record + ownership/direct-hit disambiguation; `action()` screens the SUBJECT for adverse media. Structured facts stay record-sourced (the Phase-66 guard).
- **Re-measured live (T3):** coverage 0.5→1.0, ML-A5 closes, the determination becomes reachable. Pinned ONE live-capture replay + a coverage-regression gate (`tests/gather_quality_harness.py`, the `news_quality_harness` pattern) + an honest-truncation backstop (a cap-truncated run reports `complete:false`).
- **The consolidated brief (T4):** `docs/substrate-determination-signals-PLAN-BRIEF.md` absorbs/supersedes the BO-graph brief (now a redirect stub), pinned aml-substrate@b53855c. The gap inventory is derived (signal_brief across cases → ML-A3/A6/A7) + the all-ML-population finding.
- **TWO adversarial review workflows ran this session** (the size-gated review gate's quality purpose served, no redundant third reviewer): the T1 metric review fixed 3 issues (the `complete` flag, the all-cases reference guard, validator `news_normalize`-empty checks); the final Phase-70 pass fixed 2 brief factual errors + 4 harness/honesty refinements.

## Decisions Made
- Measure-first via the stub-as-reference (gather quality = live recall vs the deterministic StubPlanner; consistency-not-correctness, ZERO catch-rate). — extracted this session
- A1 don't-know → defended down-scope: the live baseline DIAGNOSES the surface before any fix (measurement gates the optimization). — extracted this session
- The fix targets both LivePlanner prompts (findings() payload-enrich + per-record exhaustive + ownership/direct-hit disambiguation; action() subject-screen); structured facts stay record-sourced. — extracted this session
- A4 reject(sibling) → consolidate: ONE aml-substrate handoff brief absorbs/supersedes the BO-graph brief (now a redirect stub). — extracted this session
- A3 accept: a pinned live-capture replay + coverage-regression gate (`gather_quality_harness.py`) + an honest-truncation backstop. — extracted this session

## Problems Solved
- The live GATHER under-extracting corroboration findings (the named Phase-69 follow-on) — RESOLVED: coverage 0.5→1.0, ML-A5 closes, the determination becomes reachable. Don't re-propose.
- Two factual errors caught by the post-build adversarial pass (it earned its keep): (1) the brief wrongly claimed anticipated-activity data is absent (it EXISTS via `ExpectedActivity`; only `source_of_funds` is null) — a grep methodology error; (2) a Phase-69 leg-split stat (181/103) was wrong, actually 182/104 + 8 no-mechanism — both fixed + code-verified.

## Open Questions
- `MAX_ITERS=4` / live-vs-stub order divergence is a latent limitation (the honest-truncation backstop handles it; a future deeper-chain corpus would want the cap scaled) — a gather-robustness follow-on.

## Artifacts Changed
- `tests/gather_quality_harness.py` (NEW — the GATHER extraction-coverage regression gate, the `news_quality_harness` pattern; `--check` replays a pinned live capture with no model, `--freeze` re-baselines; wired into the pytest umbrella)
- `scripts/osint_tools.py` (the `coverage` measuring stick in the gather loop; the LivePlanner `findings()` + `action()` prompt fix; new selftest assertions — the coverage block, the all-cases complete-reference guard, the honest-truncation backstop on a 4-affiliate fixture, a `news_normalize`-empty entity tamper)
- `scripts/serve_workbench.py` (the coverage metric rides the gather result + NDJSON stream; stub-reference coverage/closure selftest)
- `docs/substrate-determination-signals-PLAN-BRIEF.md` (NEW — the consolidated §12 handoff brief; pinned aml-substrate@b53855c)
- `docs/substrate-bo-graph-emission-PLAN-BRIEF.md` (folded to a SUPERSEDED redirect stub → the consolidated brief)
- `docs/evidence-driven-filing.md` (live before/after coverage + the diagnosed surface recorded)
- `tests/test_selftests.py` (registers `gather_quality_harness` → `uv run pytest` 19→20), `tests/workbench.test.mjs` (116→117), `tests/smoke-checklist.md`
- `CLAUDE.md`, `docs/case-workbench.md` (the Phase-70 true-up)

## Related
- [[phases/phase-70-gather-quality-substrate-handoff|Phase 70]] — parent phase

## Soft Observations / Phase N+1 Candidates
- The §12 build queue is now sibling-rooted (the consolidated brief, pinned aml-substrate@b53855c): SoF data is the one genuinely-missing field; the anticipated-activity baseline (`ExpectedActivity`) already exists, so ML-A6 needs a C1 DETECTOR not data | the substrate determination-signal build queue (SoF data + C1/C7/C14 detectors + BO-graph emission + a kyc/TF case slice) | evidence: docs/substrate-determination-signals-PLAN-BRIEF.md
- Roll the sufficiency model across the triage + gate consoles (still disposition-only) | Phase 71+ console rollout | evidence: docs/evidence-driven-filing.md "Deferred"
- `MAX_ITERS=4` / live-vs-stub order divergence is a latent gather limitation (the honest-truncation backstop handles it; a deeper-chain corpus would want the cap scaled) | a gather-robustness follow-on | evidence: the honest-truncation backstop on the 4-affiliate fixture
- Code-verify sibling claims (and even your own grep) before asserting — the post-build adversarial pass caught two factual errors copied into the brief | a process note, not a phase | evidence: the anticipated-activity grep error + the 181/103→182/104 leg-split correction
