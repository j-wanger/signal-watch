---
title: "Phase 79: Consume sibling emissions — Lakeshore fan-in floor + the merge real-data oracle (gated)"
aliases: [phase-79]
category: phases
tags: [cross-pillar, consume, casework, substrate, fan-in-c3, merge-oracle, floor-gated-upside, measure-first, firewall]
parents: []
created: 2026-06-27
updated: 2026-06-27
source: plan
status: completed
ceremony: standard
scope: ["vendor/aml-casework/**", "scripts/vendor_casework.sh", "scripts/serve_chain.py", "scripts/serve_workbench.py", "data/casefile/**", "scripts/resolution_scorer.py", "scripts/curate_merge_cases.py", "tests/fixtures/merge-anchored-oracle/**", "data/merge/cases.json", "scripts/build.py", "merge.html", "dist/merge/**", "tests/merge-console.test.mjs", "docs/*-PLAN-BRIEF.md", "docs/cross-pillar-build-order.md", "CLAUDE.md"]
entry_criteria: "Both Phase-77-deferred consumes code-verified RESOLVED sibling-side (casework Phase 19 @076fb8e built _c3_fan_in; substrate Phase 32 @c099259 mints entity_ref≠cluster anchored fragments). Direction gate closed (Bundle, gated upside)."
exit_criteria: "Lakeshore CASE-B signs cleared via fan-in C3; the merge oracle scored two-sided (or aborted to consensus + a brief); --check all → the 8 non-merge dists byte-frozen + dist/merge re-frozen-or-untouched; evidence_requirements.py byte-unchanged; uv run pytest green; the three resolved briefs + cross-pillar-build-order trued up."
grounded_against:
  signal-watch: HEAD (Phase 78 committed, 92ac6d0)
  aml-substrate: c099259 (Phase 33; Phase 32 anchored fork @31cb439)
  aml-casework: 076fb8e (Phase 19 _c3_fan_in)
---

# Phase 79 — Consume sibling emissions

## Objective

Consume the two Phase-77-deferred sibling emissions, now code-verified RESOLVED sibling-side, as a
**floor + gated-upside** bundle: (FLOOR) Lakeshore CASE-B signs `cleared` end-to-end via casework's
new fan-in C3, completing the north-star matched pair; (GATED UPSIDE) the merge real-data oracle —
measure-first companion-only, then gate the `dist/merge` re-freeze on a clean two-sided result.

## Why now (the verified unblock)

Both blocks named in `docs/cross-pillar-build-order.md` resolved sibling-side this session
(file:line, not from the loaded snapshot): **casework Phase 19** (`ed93a0d`, on
`feat/phase-1a-deterministic-verifiers @076fb8e`) built `_c3_fan_in` in `grounding_replay` — the
Lakeshore fan-in-C3 path; **substrate Phase 32** (`31cb439`, main @`c099259`/Phase 33) mints
`entity_ref ≠ cluster` anchored fragments under `--anchored` (opaque `GT-<sha1>` cluster ids disjoint
from every resolver input; 17 multi-ref clusters / refs 255 > clusters 231 at n=400/seed0) — curing
the Phase-77 circular merge oracle.

## The two tracks

**FLOOR (committed):** re-vendor casework `b3546d4→076fb8e` (no-regression checkpoint — funnel
202/111/63, `evidence_requirements.py` byte-unchanged), shape CASE-B from its REAL multi-originator
network (no fabricated pattern), `--disposition cleared` → casework signs. Companion-only, no dist
touch.

**GATED UPSIDE (measure-first):** the live `--anchored --emit-eval-oracles` run CRASHED today
(substrate `ReplayError` `fin-2023-alert003:IND-05` at n=400/seed0); the non-circular property is
proven only by substrate tests that bypass the full CLI replay. So: pin a known-good param set, drive
the emit, score the spine's real refusals + fragment should-merges against the `GT-` oracle, commit a
no-substrate-replayable confusion capture + baseline, THEN gate the `dist/merge` re-freeze on a clean,
two-sided, non-tautological result. ABORT (the Phase-77 rule): emit won't reproduce / tautological /
one-sided → STOP to consensus + a substrate emit-stability brief; the dist re-freeze does not run.

## Scope

`vendor/aml-casework/**` + `scripts/vendor_casework.sh` + `scripts/serve_chain.py` (re-vendor) ·
`data/casefile/**` + `scripts/serve_workbench.py` (Lakeshore fan-in) · `scripts/resolution_scorer.py`
+ `scripts/curate_merge_cases.py` + `tests/fixtures/merge-anchored-oracle/**` (the measure-first
oracle) · `data/merge/cases.json` + `scripts/build.py` + `merge.html` + `dist/merge/**` +
`tests/merge-console.test.mjs` (the gated re-freeze) · `docs/*-PLAN-BRIEF.md` +
`docs/cross-pillar-build-order.md` + `CLAUDE.md` (docs true-up).

## Exit Criteria — ALL MET (DELIVERED 2026-06-27)

- [x] Lakeshore CASE-B signs `cleared` end-to-end via fan-in C3; Northgate still files; the matched pair holds
- [x] the merge oracle scored two-sided + replays with NO substrate (the gate cleared GREEN, NOT aborted — 29 substrate-scored + 13 synthetic-scored)
- [x] `--check all` 9/9 → the 8 non-merge dists byte-frozen + `dist/merge` re-frozen
- [x] `evidence_requirements.py` BYTE-UNCHANGED (the A1 guard); build.py imports no spine/scorer/sibling/curate
- [x] the three resolved briefs (casework-c3-fan-in CLOSED, substrate-emit-cli-wiring RESOLVED, substrate-open-reference-data-fork Stage-1 PARTLY-LANDED) + cross-pillar-build-order trued up to the live HEADs
- [x] `uv run pytest` 26 green; validate↔curate parity; honesty governor (no rate/score/multiplier wording); synthetic-substrate-anchored qualifier; badge always-on

**Delivery:** all 5 tasks [x]; adversarial review (3 dims) 1 must-fix (mid-flight stale `cases.json`) RESOLVED / 2 should-fix addressed / 1 self-refuted. Pending the delivery-flow commit.

## Constraints

- `evidence_requirements.py` BYTE-UNCHANGED (prevents the file-bar A1 regression).
- build.py imports no spine/scorer/sibling/curate (prevents the companion-into-build firewall breach).
- The 8 non-merge dists byte-frozen; `dist/merge` the ONE sanctioned re-freeze (prevents unsanctioned dist drift) — gated on the T3 measure-first result.
- validate↔curate parity (Phase-76) (prevents a weaker build-boundary validator than the authoring curator).

## Abort

Any non-merge dist drift / a build.py spine/scorer/sibling/curate import / an `evidence_requirements.py`
change → STOP. Merge track: emit won't reproduce after bounded attempts / tautological / one-sided →
STOP to consensus + a substrate emit-stability brief; T4 does NOT run.

## Decisions

[[decisions/phase-79-floor-plus-gated-upside-bundle]] · [[decisions/phase-79-merge-measure-first-before-dist]]

Spec `specs/phase-79-consume-sibling-emissions.md`; ledger Phase-79.
