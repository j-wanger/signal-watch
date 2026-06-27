---
title: "Phase 79 — Consume sibling emissions: Lakeshore fan-in C3 floor + the merge real-data oracle (gated → cleared GREEN, supersede)"
aliases: []
category: journal
tags: [cross-pillar, consume, casework, substrate, fan-in-c3, merge-oracle, anchored-oracle, supersede, measure-first, firewall]
parents: [phase-79-consume-sibling-emissions]
created: 2026-06-27
updated: 2026-06-27
source: debrief
duration: long
---

# Phase 79 — Consume sibling emissions (standard, planned + delivered same session)

## What Happened

Consumed the two Phase-77-deferred sibling emissions — both code-verified RESOLVED sibling-side this
session — as a **floor + gated-upside** bundle. Both tracks LANDED: the Lakeshore floor committed,
and the gated merge upside cleared its measure-first abort gate GREEN (not aborted), so the
`dist/merge` re-freeze ran — and the user called "supersedes," replacing the consensus-66 with
substrate-scored real cases.

- **FLOOR (T1–T2, committed):** re-vendored casework `b3546d4→076fb8e` (Phase 19 `_c3_fan_in`); funnel
  202/111/63 byte-stable, `evidence_requirements.py` byte-unchanged. Lakeshore CASE-B now SIGNS
  `cleared` end-to-end via fan-in C3 — the matched north-star pair (Northgate files / Lakeshore clears)
  BOTH route through casework. The honest fix: re-time CASE-B's 8 catering credits into a 6d2h window
  (casework's `_FANOUT_WINDOW=7`; same 8 distinct clients/amounts/memos, only dates tighten — the fan-in
  pattern is REAL) + author `data/casefile/case-b.bundle.json` grounded on the FAITHFUL
  `fin-2023-alert001:IND-02`.
- **GATED UPSIDE (T3–T4):** the merge real-data oracle. T3 (the abort gate, L) reproduced substrate's
  `--anchored --emit-eval-oracles` emit CLEAN (the ReplayError was `--monitor`/`--emit-evidence`,
  orthogonal to the emit path — caught by a scout). The `GT-<hash>` oracle is NON-circular
  (257 entity_refs → 233 opaque clusters; `entity_ref ≠ cluster`; 17 fragment clusters / 31 latent
  should-merge pairs — Phase-77 had ZERO). Scored the demoted spine → 29 candidate pairs, two-sided
  (13 uphold / 16 reject). Distilled the committed no-substrate capture
  `data/entity-spine/substrate-anchored-slice.json`. THEN (T4) the user's "supersedes" call:
  `enumerate_substrate_scored` replaced `enumerate_real_shares`; BOTH populations now scored, split by
  oracle PROVENANCE; `dist/merge` RE-FROZEN (90,831 B).
- **T5 docs:** the 3 handoff briefs annotated with resolving commits (casework-c3-fan-in CLOSED;
  substrate-emit-cli-wiring RESOLVED; substrate-open-reference-data-fork PARTLY LANDED — Stage-1);
  cross-pillar-build-order + CLAUDE.md trued up.

## Decisions Made

- [[phase-79-merge-supersede-substrate-scored|the merge console SUPERSEDED the consensus-66 with substrate-scored real cases]]
- [[phase-79-lakeshore-honest-cosign|Lakeshore co-signs via window-compression + an IND-02-grounded bundle]]
- [[phase-79-floor-plus-gated-upside-bundle|floor + gated-upside bundle]] (planning, finalized high)
- [[phase-79-merge-measure-first-before-dist|merge consume measure-first before any dist touch]] (planning, finalized high; gate cleared GREEN)

## Problems Solved

- **The mid-flight staleness near-miss (the must-fix the review caught):** `data/merge/cases.json`
  feeds `dist/merge`; mid-phase the committed/working `cases.json` was STALE (old 66) while `dist/merge`
  had advanced (new 29). `--check all` PASSED (the stale file + the dist built from it agreed) but
  `--check merge` FAILED. Caught by 3 independent signals (self-review grep, `--check merge`, the
  adversarial review). FIX: regenerated `cases.json` → 29+13, `--check merge` passes. Lesson: a "wrote …"
  log line is NOT proof a file persisted — verify the committed file's CONTENT + git status + the
  specific `--check <target>` before claiming done; commit the curate INPUT (the untracked slice JSON)
  with the output.
- The substrate emit ReplayError (the planning-stage crash that justified the measure-first gate) was
  diagnosed as orthogonal to the emit path — the gate de-risked it correctly, then cleared it.

## Artifacts Changed

- `data/entity-spine/substrate-anchored-slice.json` (NEW — the no-substrate-replayable merge oracle capture; emails masked, email/phone demoted)
- `scripts/curate_merge_cases.py` (`enumerate_substrate_scored` replaces `enumerate_real_shares`; both populations scored; validate + selftest rewritten; removed `_safe_value` + the `EntitySpine` import)
- `data/merge/cases.json` (29 substrate-scored + 13 synthetic-scored) · `merge.html` · `scripts/build.py` (`validate_merge_cases` in EXACT parity) · `dist/merge/index.html` (RE-FROZEN) · `tests/merge-console.test.mjs` (73→74)
- `vendor/aml-casework/**` (b3546d4→076fb8e, Phase 19 fan-in C3; wheel + VENDORED_AT) · `data/casefile/case-b.bundle.json` (NEW) · `tests/fixtures/casefile/CASE-B.detail.json` · `scripts/serve_workbench.py` (`lakeshore_cosign_consume`)
- `docs/{casework-c3-fan-in,substrate-emit-cli-wiring,substrate-open-reference-data-fork}-PLAN-BRIEF.md` · `docs/cross-pillar-build-order.md` · `CLAUDE.md`

## Related

- [[phase-79-consume-sibling-emissions|Phase 79 — parent phase]]
- [[2026-06-26-phase-77-consume-sibling-emissions|Phase 77]] (the deferral this phase consumed) · [[2026-06-26-phase-78-consume-disposition-validation|Phase 78]] (the measure-first harness pattern reused)

## Soft Observations / Phase N+1 Candidates

- substrate open-data Stage 2/3 (sanctions/FATF anchors + paid-landmine routing) — sibling frontier; would give the merge oracle richer real-shaped collisions. | a substrate realism phase | evidence: `docs/substrate-open-reference-data-fork-PLAN-BRIEF.md` (Stages 2/3 OPEN)
- The demoted-spine substrate population is constant-verdict (refuses all 29) — a future phase could ALSO score a NAIVE (non-demoted) resolver over real-substrate data to exercise the over-merge-trap quadrant (currently only the synthetic-13 spans all four). | scored-naive-resolver phase | evidence: the adversarial review should-fix #1
- The Lakeshore IND-05/IND-02 C3-grounding divergence — a faithfulness fix re-grounds BOTH CASE-A + CASE-B's C3 to the faithful IND-02, deferred because it touches the FILE case + the matched-pair "same signals" invariant. | a casefile faithfulness phase | evidence: `data/casefile/case-b.bundle.json` provenance.grounding_note
- casework CI-promotion criterion (the advisory reconciliation lane → blocking) — casework follow-on. | evidence: `docs/cross-pillar-build-order.md` Track A′
