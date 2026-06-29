# Active Phase Context

**Phase 86 — *STR drafter behind the verifiers: the consistency-measured drafting agent (Agentification Stage 3)*** (signal-watch-local, STANDARD, companion-only) — DELIVERED 2026-06-29, READY FOR COMPLETION (all 5 tasks [x], exit criteria met, impl committed `c8f32b8` + pushed to main). The roadmap's Stage 3. STATE-LOADER FINDING (surfaced pre-gate): the STR drafter + its six Class-G verifiers ALREADY SHIPPED in Phase 57; the drafter has NO correctness oracle → the deliverable was the MEASUREMENT FRAME (the GATHER consistency-not-correctness class), NOT new infra.

## Objective
Turn the already-built stub STR drafter into a CONSISTENCY-MEASURED drafting agent — `tests/drafter_quality_harness.py` (the `gather_quality_harness.py` pattern) measuring the live (local) drafter vs the deterministic stub over the committed casefile bundles, counts-only (stub-vs-live SIGN/REFUSE + fabrication-guard CATCH + grounding CONSISTENCY), pinned as a `--check`/`--freeze` regression gate, with an honest counts-only headline. The deliverable is the MEASUREMENT.

## Measured result (the gate-bounded tie)
A model WAS on :8080 (counts-only, small-synthetic-qualified): over 4 designed bundles the live agent matched the deterministic stub **4/4** — signed the same 3, fail-closed on the same narrative-seam case `CASE-P-0025128`, 0 caught, 0 recovered; it did NOT hallucinate a narrative to force a file. THE FINDING: the drafter measure is consistency-BOUNDED by the gate (the verifiers refuse anything ungrounded → a competent agent and the stub converge at the gate → the GATE determines defensibility) — vindicates propose→gate→decide from the DRAFTING side. A tie is a real result; limitation (recovered=0/caught=0) stated plainly.

## Scope (file globs)
`tests/drafter_quality_harness.py` · `tests/fixtures/drafter-quality/**` · `tests/test_selftests.py` · `tests/workbench.test.mjs` · `docs/drafter-live.md` · `docs/agentification-roadmap.md` · `CLAUDE.md` · `HANDOFF.md`

## Key constraints (all HELD)
- No oracle (free-text drafting) → counts-only consistency; NEVER accuracy/catch-rate/precision/recall. A gold-narrative oracle REJECTED. NO oracle firewall needed (simpler than Stages 1/2).
- Companion-only / casework-UNCHANGED: all 9 dists byte-frozen (`--check all` 9/9); `git diff --quiet vendor/aml-casework` + `git diff --quiet scripts/evidence_requirements.py` both empty; build.py imports nothing new; the 256/376 §12 funnel untouched — the agent drafts, the six verifiers gate, the human signs.
- HONESTY over drama: the tie reported straight; the deliberately-ungrounded adversarial case (to fire the guard live) deliberately NOT contrived (a named follow-on).

## Exit criteria (MET)
`drafter_quality_harness.py --check` PASS + in the uv-run-pytest umbrella; the counts-only headline recorded; `node tests/workbench.test.mjs` green (205→206); `--check all` 9/9; vendor/aml-casework + evidence_requirements.py git-diff empty; build.py companion-import grep clean; the 256/376 funnel unchanged; roadmap Stage 3 marked BUILT + `docs/drafter-live.md` written; CLAUDE.md + HANDOFF trued IN PLACE; honesty swept.

## Abort rule
Any casework src edit / a re-vendor / a build.py companion import / any of the 9 dists not byte-identical / an `evidence_requirements.py` or §12-funnel change / a fabricated live drafter number / a degenerate measure presented as a contrast → STOP-and-surface. If blocked >3 attempts: ask user — skip or abort.

## Gates
- [x] spec (`## Formal Spec` embedded in [[phases/phase-86-str-drafter-consistency-measure]] — standard ceremony, no separate /spec round)
- [x] Direction confirmed by user (2026-06-29, AskUserQuestion — direction = Stage 3 STR drafter, deliverable = the measurement frame; 3 assumptions ACCEPTED, all_accept tracked NOT silent; ledger Phase-86)
- [x] Delivery accepted (2026-06-29 — user accepted "OK"; impl `c8f32b8` pushed to main; the gate-bounded 4/4 tie recorded; all 9 dists byte-frozen, `evidence_requirements.py` + vendor unchanged, `uv run pytest` 34, pre-delivery review 0 blockers/0 majors/2 minors fixed)

Decisions [[decisions/phase-86-gate-bounded-drafter-tie]] (debrief) · [[decisions/phase-86-direction-str-drafter-measurement]] · [[decisions/phase-86-no-oracle-consistency-measure]] · [[decisions/phase-86-stub-vs-live-narrative-seam-contrast]] · [[decisions/phase-86-companion-only-casework-unchanged]]; plan [[phases/phase-86-str-drafter-consistency-measure]]; ledger Phase-86 (all 5 rows HELD).
