---
type: phase
phase: 78
slug: phase-78-consume-disposition-validation-control
title: "Consume the disposition oracle — determination-validation harness + §12 discovery-feed control"
status: active
ceremony: standard
created: 2026-06-26
updated: 2026-06-26
tags: [cross-pillar, consume, substrate, determination-engine, validation-harness, circularity-exit, firewall, measure-then-control, lfcm]
grounded_against:
  signal-watch: HEAD (Phase 77 committed, 5afdb96)
  aml-substrate: 9677a37 (Phase 31 emit-cli-wiring)
  aml-casework: b3546d4
---

# Phase 78 — Consume the disposition oracle

## Objective
Consume substrate Phase 31's now-CLI-reachable `eval/intended_disposition.json` to build the
**determination-validation harness** (the circularity exit deferred as Phase-77 A2) and pivot it into
a **control**: a §12 discovery feed surfacing the engine-vs-oracle disagreement cases in the
investigator workbench. Companion-only; the determination engine + all 9 dists stay byte-frozen.

## Why now (the verified unblock)
Phase-77 A2 deferred this exact harness because substrate's `emit_intended_disposition` was
tested-but-CLI-unwired. **Substrate Phase 31 (`9677a37`, committed 2026-06-26) wired
`--emit-eval-oracles`** — verified live this session (the oracle emits across the boundary, keyed
`CASE-<customer>`, two-sided `file`|`clear`, 11/807 split at 5k clients). Substrate's own Phase-31
commit independently confirms: the disposition harness IS unblocked (two-sided oracle); the merge
true_entities stays CONSENSUS (still circular — all-singleton `ENT-<entity_ref>` echo).

## The honesty frame (bundle-only, non-circular)
The `file` bar's mechanism + leg count are **bundle-derived**; named_predicate_risk + mitigation are
**human-gate inputs** absent from a raw bundle. The harness scores the bundle-only signal structure
(does the §12 signal-assembly pre-position the file decision?) and HOLDS OUT the human gate, naming
it as the boundary — never deriving it from the oracle basis (that is the circularity the merge-66
abort killed). The oracle label never enters an engine input (`assert_no_oracle_leak`). The control's
feed is presentation-only (the Phase-74 priors-are-provenance precedent).

## Measure-first gate (T2)
The weakest assumption: that mechanism + ≥2 legs discriminates oracle-file from oracle-clear. Verified
two-sided on the oracle side; engine-side discrimination is measured at T2. Degenerate ⇒ STOP+REPORT,
down-scope T3 to an honest-degeneracy report.

## Scope
`scripts/determination_validation_harness.py` (NEW; freeze/check/selftest) ·
`tests/fixtures/determination-validation/{capture,baseline}.json` · `scripts/serve_workbench.py` +
`workbench.html` (the §12 discovery feed) · `docs/determination-validation.md` + CLAUDE.md /
`docs/cross-pillar-build-order.md` true-up.

## Exit criteria
`--check` replays the committed capture (no substrate run) → the per-class confusion structure vs a
committed baseline; the discovery feed renders the *missed* / *over-flag* cells annotated by the
engine's `missing[]`; `evidence_requirements.py` byte-unchanged; build.py imports nothing new;
`--check all` 9/9 byte-frozen; `uv run pytest` green; honesty governor (no catch-rate/precision/lift),
synthetic-only qualified.

## Abort
Any dist drift · a build.py companion/substrate import · an engine change · an oracle-label leak into
the engine · a confusion number presented as a catch-rate · a dist requiring a live substrate read →
STOP. Degenerate matrix → down-scope, never fabricate a feed.

## Decisions
[[decisions/phase-78-bundle-only-non-circular-validation]] ·
[[decisions/phase-78-measure-then-control-discovery-feed]]

Spec `specs/phase-78-consume-disposition-validation-control.md`; ledger Phase-78.
