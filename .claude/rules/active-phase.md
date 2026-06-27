# Active Phase Context

**Phase 80 — *Consume substrate Phase 34*: OFAC name-collision merge case class + non-tautological C14 §12 leg** (signal-watch-local, STANDARD) — PLANNED 2026-06-27. Consume aml-substrate's one unconsumed emission (Phase 34 @**1f5901e** — seam-5 sanctions-screening realism: the dead `sanctions_flag` made LIVE under `--anchored` via a label-blind real-OFAC-watchlist NAME COLLISION + the revived non-tautological C14 KYC-integrity branch). Phases 32/33 (`--anchored` fragments + real-frequency names) were already consumed in the Phase-79 merge slice; Phase 34's sanctions layer is the delta. casework @**076fb8e** (Phase 19) sits at the Phase-79 vendor pin — nothing new. Both sibling HEADs code-verified LIVE this session (file:line, not loaded facts).

## Objective
Two consumes + a queue: (1) **merge console** — an OFAC watchlist NAME-COLLISION case class (synthetic party's real-frequency name collides with a real public-domain OFAC entry → *same latent entity [uphold the link] vs common-name false positive [reject]*), MEASURE-FIRST gated; (2) **workbench §12** — a non-tautological sanctions-driven C14 leg lights the kyc determination (additive to the v0.5 slice, the C14→kyc path already exists from Phase 72); (3) author the substrate **P35 handoff brief** (the confirmed remaining frontier) + cross-pillar true-ups.

## Scope
`scripts/curate_merge_cases.py` · `data/merge/cases.json` · `scripts/build.py` (validate_merge_cases) ·
`merge.html` · `dist/merge/**` · `tests/merge-console.test.mjs` · `tests/fixtures/merge-sanctions-oracle/**` ·
`data/entity-spine/**` · `scripts/resolution_scorer.py` · `scripts/curate_workbench_cases.py` ·
`scripts/serve_workbench.py` · `data/workbench/**` · `tests/workbench.test.mjs` · `docs/*-PLAN-BRIEF.md` ·
`docs/cross-pillar-build-order.md` · `CLAUDE.md` · `.dev-wiki/tasks.md`. NO change to `evidence_requirements.py`.

## Key constraints (LOAD-BEARING)
- **A1 guard:** `evidence_requirements.py` BYTE-UNCHANGED (`git diff --quiet`).
- **Firewall:** build.py imports no spine/scorer/sibling/curate (grep guard); the **8 non-merge dists byte-frozen**; `dist/merge` the ONE sanctioned re-freeze, GATED on T1 two-sided.
- **validate↔curate EXACT parity** (Phase-76); the post-disposition `oracle` never leaks pre-adjudication (`assert_no_*_leak`).
- **Compliance:** real OFAC names ship clean under 17 USC §105 (US-federal public domain — covers OFAC), framed STRICTLY as the **false-positive trap** — the synthetic party is NEVER the sanctioned entity; never "we caught a sanctioned party." Badge always-on; synthetic-substrate-anchored qualifier.
- **Honesty governor:** no catch-rate/lift/precision/recall/multiplier wording.
- **Measure-first:** T1 is the abort gate; the merge track (T2/T3) runs ONLY on a clean two-sided non-circular T1; the workbench (T4) + the P35 brief (T5) run regardless.

## Exit criteria
T1 capture committed + no-substrate replayable + the two-sidedness decision documented. IF two-sided: `--check all` 9/9 (8 byte-frozen + `dist/merge` re-frozen); `node tests/merge-console.test.mjs` green incl. the new basis; validate↔curate parity; honesty word-ban held. IF one-sided/flaky: `dist/merge` BYTE-FROZEN + a substrate emit-two-sidedness brief. A sanctions-driven C14 case in the workbench; the §12 kyc leg lights; `node tests/workbench.test.mjs` green; gather/workbench harnesses pass; `git diff --quiet scripts/evidence_requirements.py`. The substrate P35 brief exists; cross-pillar-build-order trued up; the casework C14-fails-closed drift corrected; FOLLOW-ON markers reconciled; `uv run pytest` green.

## Abort rule
Any UNSANCTIONED ship dist drift (the 8 non-merge dists, or `dist/merge` before its T1/T2 gate passes) / a build.py spine-scorer-sibling-curate import / an `evidence_requirements.py` change / a real OFAC name framed as a real sanctions catch (not the false-positive trap) / a confusion number presented as a catch-rate/precision/lift/recall → STOP-and-surface. Measure-first (T1): the anchored sanctions emit won't reproduce after bounded attempts / the oracle is one-sided or tautological → STOP the merge track (T2/T3 do NOT run) to workbench-only + a substrate emit-two-sidedness brief; deliver T4 + T5 + the honest non-result.

## Gates
- [x] spec (`specs/phase-80-consume-substrate-sanctions-screening.md`)
- [x] Direction confirmed by user (2026-06-27, AskUserQuestion — "Consume P34: merge + workbench" + the one-sided fallback "Abort merge → companion + brief"; assumption positions taken, no unresolved reject/don't-know; ledger Phase-80)
- [x] Delivery accepted (post-implementation report 2026-06-27; adversarial review 3-dim ZERO findings; "Accept — commit + push to main")

Spec `specs/phase-80-consume-substrate-sanctions-screening.md`; plan
[[phases/phase-80-consume-substrate-sanctions-screening]]; ledger Phase-80.
