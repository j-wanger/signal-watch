# Active Phase Context

**Phase 70 — *Gather extraction quality (measured) + the consolidated §12 substrate handoff*** (signal-watch-local, LITE) — DELIVERED + accepted 2026-06-22. **No active signal-watch-local phase now — run `/dev-plan` for the next.**

## Status
**COMPLETE — T1–T5 ALL [x]; delivery accepted by the user 2026-06-22 (LITE).** The orchestrator flips the delivery gate after the commit verifies. The named Phase-69 follow-on RESOLVED: measured the live GATHER's recall vs the deterministic StubPlanner reference (consistency-not-correctness, NOT model-tuning), diagnosed the surface (the `LivePlanner.findings()` prompt — A1 down-scope), fixed both LivePlanner prompts → **coverage 0.5→1.0, ML-A5 closes, the determination becomes reachable.** Pinned a deterministic replay fixture + a coverage-regression gate (`tests/gather_quality_harness.py`) + an honest-truncation backstop. The consolidated `docs/substrate-determination-signals-PLAN-BRIEF.md` absorbs/supersedes the BO-graph brief (now a redirect stub), pinned aml-substrate@b53855c. Two adversarial review workflows ran (3 metric issues + 2 brief factual errors + 4 harness/honesty refinements fixed). Companion-only; `--check all` 8/8 ZERO dist drift; build.py imports none of it; `uv run pytest` 19→20.

## Phase 71+ candidates
The substrate determination-signal build queue (the consolidated brief: SoF data + C1/C7/C14 detectors + BO-graph emission + a kyc/TF case slice — sibling aml-substrate) · roll the sufficiency model across the triage + gate consoles (still disposition-only) · the MAX_ITERS=4 / live-vs-stub order divergence is a latent gather-robustness follow-on (the honest-truncation backstop handles it; a deeper-chain corpus would want the cap scaled).

## Gates
- [x] spec — waived under LITE ceremony (the assumption-ledger gate IS the direction gate, Phase-67/68/69 precedent)
- [x] Direction confirmed by user (assumption positions taken 2026-06-22; A0 accept, A1 don't-know→down-scope, A2/A3 accept, A4 reject→consolidate)
- [x] Delivery accepted (post-implementation report 2026-06-22; user ran /dev-debrief accept)

Plan [[phases/phase-70-gather-quality-substrate-handoff]]; ledger Phase-70.
