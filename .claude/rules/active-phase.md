# Active Phase Context

**Phase 86 — *STR drafter behind the verifiers: the consistency-measured drafting agent (Agentification Stage 3)*** (signal-watch-local, STANDARD, companion-only) — PLANNED 2026-06-29 (5 tasks [ ], NO L). The roadmap's Stage 3. STATE-LOADER FINDING (surfaced pre-gate): the STR drafter + its verifier gate ALREADY SHIPPED in Phase 57 (the Drafter Protocol, the `--drafter {stub,claude,openai,opencode}` switch, the live-draft reveal); a live model is up on `127.0.0.1:8080`; the drafter has NO correctness oracle → the deliverable is the MEASUREMENT FRAME, the consistency-not-correctness class (the GATHER model), NOT new infra or an oracle headline.

## Objective
Turn the already-built stub STR drafter into a CONSISTENCY-MEASURED drafting agent — `tests/drafter_quality_harness.py` (the `gather_quality_harness.py` pattern) measuring the live (local) drafter vs the deterministic stub over the committed casefile bundles, counts-only (stub-vs-live SIGN/REFUSE + fabrication-guard CATCH + grounding CONSISTENCY), pinned as a `--check`/`--freeze` regression gate, with an honest counts-only headline. Mark roadmap Stage 3 BUILT. Companion-only. The deliverable is the MEASUREMENT.

## Scope (file globs)
`tests/drafter_quality_harness.py` · `tests/fixtures/drafter-quality/**` · `tests/test_selftests.py` · `tests/workbench.test.mjs` · `tests/chain.test.mjs` (if present) · `workbench.html` / `chain.html` (only-if-needed) · `docs/drafter-live.md` · `docs/agentification-roadmap.md` · `CLAUDE.md` · `HANDOFF.md` · `.dev-wiki/**`

## Key constraints (all HELD)
- No oracle (free-text drafting) → counts-only consistency (stub-vs-live SIGN/REFUSE + fabrication-guard CATCH + grounding CONSISTENCY); NEVER accuracy/catch-rate/precision/recall. A gold-narrative oracle REJECTED. NO oracle firewall needed (no truth to hide — simpler than Stages 1/2).
- Non-degenerate: the stub fail-closes on the narrative-seam case (Phase-82 CASE-P-0025128) → the committed `data/casefile/*.bundle.json` population spans SIGN and REFUSE. T1 classifies first; honest NULL if degenerate.
- Companion-only / casework-UNCHANGED: all 9 dists byte-frozen; build.py imports nothing new; the Drafter Protocol + the six grounding verifiers UNCHANGED (no re-vendor, pin `04cc335` == sibling HEAD); `evidence_requirements.py` + the 256/376 §12 funnel UNTOUCHED — the agent drafts, the six verifiers gate, the human signs.
- HONESTY: counts-only, the synthetic-substrate qualifier on every number, the word-ban on the new markers + docs; the always-on badge stays. EXECUTE ONCE; no model on :8080 → stub-only baseline + named `--freeze` follow-on, NEVER fabricate.

## Exit criteria (MET → completion)
`drafter_quality_harness.py --check` PASS + in the uv-run-pytest umbrella; the counts-only headline recorded (live or stub-only, honestly); `node tests/workbench.test.mjs` green (count grows); `--check all` 9/9 byte-frozen; `git diff --quiet vendor/aml-casework` + `git diff --quiet scripts/evidence_requirements.py` both empty; build.py companion-import grep clean (no `drafter_quality_harness`); the 256/376 §12 funnel unchanged; roadmap Stage 3 marked BUILT + `docs/drafter-live.md` written; CLAUDE.md + HANDOFF trued IN PLACE; honesty swept.

## Abort rule
Any casework src edit / a re-vendor / a build.py companion import / any of the 9 dists not byte-identical / an `evidence_requirements.py` or §12-funnel change / a fabricated live drafter number / a degenerate measure presented as a contrast (or any accuracy/catch-rate/precision/recall framing) → STOP-and-surface. If blocked >3 attempts: ask user — skip or abort.

## Gates
- [x] spec (`## Formal Spec` embedded in [[phases/phase-86-str-drafter-consistency-measure]] — standard ceremony, no separate /spec round; the contract is fully determined)
- [x] Direction confirmed by user (2026-06-29, AskUserQuestion — direction = Stage 3 STR drafter, deliverable = the measurement frame; 3 assumptions ACCEPTED, all_accept tracked NOT silent; ledger Phase-86)
- [ ] Delivery accepted

Decisions [[decisions/phase-86-direction-str-drafter-measurement]] · [[decisions/phase-86-no-oracle-consistency-measure]] · [[decisions/phase-86-stub-vs-live-narrative-seam-contrast]] · [[decisions/phase-86-companion-only-casework-unchanged]]; plan [[phases/phase-86-str-drafter-consistency-measure]]; ledger Phase-86.
