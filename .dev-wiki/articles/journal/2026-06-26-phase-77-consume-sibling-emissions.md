---
title: "Phase 77 — Consume the three sibling emissions: harness deferred · casework cleared via C5 proxy · real-66 merge scoring reverted to consensus (circular oracle)"
aliases: ["phase 77 debrief", "three sibling consumes delivered", "circular oracle revert + cleared C5 proxy"]
category: journal
tags: [phase-77, consume, cross-pillar, true-entities, casework-cleared, exogenous-disposition, merge-console, circular-oracle, abort-rule, deferred]
parents: [phase-77-consume-sibling-emissions]
created: 2026-06-26
updated: 2026-06-26
source: debrief
duration: unknown
---

# Phase 77 — Consume the three sibling emissions

## What Happened

Phase 77 set out to consume three sibling emissions code-verified live this session (substrate
fc98b09→f2da3e4 = Phase 29 `true_entities` + Phase 30 `exogenous-disposition-label`; casework
bf15535→b3546d4 = Phase 17 advisory CI lane + Phase 18 `cleared`). As delivered, ONE consume landed
as planned and TWO deferred against discovered sibling state — each routed to a named sibling brief,
NOT left open. The phase is companion-only: all 9 ship dists stayed byte-frozen, build.py imports no
spine/scorer/sibling/curate.

- **T1 (the circularity exit) → DEFERRED (DISCOVERY).** Verified @f2da3e4 by code that substrate's
  `emit_true_entities`/`emit_intended_disposition` are tested-but-UNWIRED into the CLI (they run only
  in substrate's own tests; produce neither `identity/true_entities.json` nor
  `eval/intended_disposition.json` — only `identity/true_entities.parquet` via `--identity` is
  CLI-reachable). No tool-boundary path to the oracle → deferred; authored
  `docs/substrate-emit-cli-wiring-PLAN-BRIEF.md`.
- **T2 (re-vendor) → DONE.** Re-vendored casework `bf15535→b3546d4` (`VENDORED_AT`);
  serve_workbench/serve_chain selftests green; the gate funnel is IDENTICAL (auto-clear 202 /
  human-gate 111 / review 63) — no signing regression.
- **T3 (Lakeshore cleared) → DONE via a C5 PROXY (USER OVERRIDE option b).** The north-star Lakeshore
  CASE-B fails-closed at casework's `grounding_replay` (casework C3 = fan-OUT ≥5 outflows; Lakeshore's
  C3 is fan-IN multi-originator → 0 cited outflows → correctly refused; A3 abort held — no fan-out
  fabricated). So casework's `cleared` is consumed end-to-end on a casework-REPLAYABLE C5
  cash-placement proxy (`data/casefile/cleared-demo.bundle.json`, exculpatory:true txn + grounded
  exculpatory claim, NO crime_type/inculpatory, grounded on vendored `fin-2023-alert001:IND-08`).
  `serve_workbench.cleared_demo_consume` → signed + disposition==`cleared` + blocking_violations==[];
  an adversarial review confirmed the bundle is HONEST. The Lakeshore gap →
  `docs/casework-c3-fan-in-PLAN-BRIEF.md`.
- **T4 (real-66 scoring) → ATTEMPTED → DEFERRED at the abort rule.** Re-emitted the slice population
  with `--identity` (pin f2da3e4) and mapped the committed 66 real SHARES. The CHECKPOINT fired worse
  than "all distinct": every emitted cluster is content-addressed `ENT-<entity_ref>` — a 1:1 relabel
  of the SAME field the spine keys its merge/refuse on (all 441 slice persons; ZERO cross-entity_ref
  merges; 66/66 DISTINCT). Scoring against it is CIRCULAR (true-by-construction). Per the abort rule +
  the user's call ("revert real to consensus, defer"), reverted curate/build/cases/test to the
  Phase-76 CONSENSUS state. The circular parquet capture was NOT committed.
- **T5 → N/A (voided by T4).** The real 66 stay consensus; `merge.html`/`cases.json`/test reverted to
  Phase-76; `node tests/merge-console.test.mjs` 73/0; `build.py --check merge` byte-stable. dist/merge
  is byte-identical to its Phase-76 ship.
- **T6 → DONE.** Full verification + true-up.

## Decisions Made

- [[phase-77-consume-3-true-entities-one-sided|Revert the real 66 to CONSENSUS, defer real scoring — the captured oracle is CIRCULAR]] (high)
- [[phase-77-casework-cleared-lakeshore-translation|Consume casework cleared via a C5 PROXY bundle, not Lakeshore (which fails-closed on fan-in C3)]] (high)
- [[phase-77-exogenous-disposition-harness-circularity-exit|DEFER the exogenous-disposition harness — substrate's emit_* are CLI-unwired]] (high)
- [[phase-77-three-consumes-one-phase-fork-parked|All three consumes in one STANDARD phase; two deferred to named briefs, the open-data fork parked]] (high)

## Problems Solved

- The named Phase-76 "score the real 66 against true_entities" deferral turned out CIRCULAR (the
  oracle is a relabel of the spine's decision key) — caught by the T4 checkpoint, not shipped as a
  tautological number; reverted cleanly to consensus, the synthetic-13 two-sided oracle untouched.
- Lakeshore couldn't sign `cleared` through casework (fan-in vs fan-out C3 mismatch) — consumed
  `cleared` end-to-end on an honest, casework-replayable C5 proxy instead of fabricating a fan-out
  pattern; the file bar stayed byte-unchanged.

## Open Questions

- None unresolved this phase — both deferrals are routed to named sibling briefs. The unblocking work
  (the two-sided real merge oracle + realistic identifier collisions) lives in the substrate open-data
  fork, a substrate-side phase.

## Artifacts Changed

- `vendor/aml-casework/**` + `vendor/aml-casework/VENDORED_AT` (re-vendored bf15535→b3546d4)
- `scripts/{serve_workbench,serve_chain}.py` (`--disposition` file|cleared plumbing; new
  `cleared_demo_consume` + `CLEARED_DEMO_BUNDLE` + a casework-gated cleared check in `--selftest`)
- `data/casefile/cleared-demo.bundle.json` (NEW — the synthetic C5 cleared proxy bundle)
- `docs/cross-pillar-build-order.md` · `docs/substrate-emit-cli-wiring-PLAN-BRIEF.md` (NEW) ·
  `docs/casework-c3-fan-in-PLAN-BRIEF.md` (NEW) · `docs/substrate-open-reference-data-fork-PLAN-BRIEF.md` (NEW)
- `CLAUDE.md` (trued up — pins substrate f2da3e4 / casework b3546d4; real-66 stay consensus, oracle
  circular, real scoring deferred; cleared signed via C5 proxy; harness deferred)
- NO dist change — all 9 dists byte-frozen. build.py untouched (imports no spine/scorer/sibling/curate).

## Related

- [[phase-77-consume-sibling-emissions|Phase 77 — Consume the three sibling emissions]] — parent phase
- [[2026-06-25-phase-76-merge-adjudication-console|Phase 76 — the merge console]] — the prior phase
  that NAMED this real-66 scoring consume as a deferred handoff (now found circular)

## Soft Observations / Phase 78 Candidates

- The substrate open-data fork is the unblocking move for BOTH the two-sided real merge oracle and
  realistic identifier collisions — the highest-leverage next substrate phase (a substrate realism
  phase, not a signal-watch one). | named: `docs/substrate-open-reference-data-fork-PLAN-BRIEF.md` |
  evidence: T4 outcome note in tasks.md + the consume-3 decision article.
- A signal-watch-local frontier may be thin until a sibling phase lands — three of this phase's
  planned advances were gated on sibling emissions that don't exist yet (the consume-readiness
  pattern). | framing: verify the sibling live before committing to a consume; route blocked consumes
  to named briefs | evidence: T1/T3/T4 outcome notes.
- casework C3 fan-in support unblocks the north-star Lakeshore co-sign through the real casework
  verifier. | named: `docs/casework-c3-fan-in-PLAN-BRIEF.md` | evidence: T3 outcome note.
