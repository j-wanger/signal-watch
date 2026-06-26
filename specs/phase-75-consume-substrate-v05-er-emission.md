# Phase 75 — Consume the substrate v0.5 entity-resolution emission

**Ceremony:** STANDARD (user override of the project LITE default — cross-pillar contract adoption, real coupling surface).
**Status:** active (planned 2026-06-25).

## 1. Objective

Adopt aml-substrate's Phase 27/28 ADDITIVE emission — named-identity **v0.4** (`display_name`, `counterparty_name`) and entity-resolution **v0.5** (party-level `identifiers[]` `{kind,value,normalized,strength}`, `RelationshipEdge.strength`, top-level `resolution_edges[]`) — into the **companion-only** consume path (`curate_workbench_cases` → `entity_spine` → `workbench` render), grounding the Phase-74 memory short-circuit in **real substrate-emitted graded identifiers** instead of the hand-authored synthetic note (`data/casefile` PSR-0001). The depth of the memory-lever payoff is **sized by a measure-first cross-case-overlap gate** (T1).

## 2. Context — the check (code-verified 2026-06-25)

Two Explore agents over the live siblings:

| Sibling | Pin@brief | Live HEAD | Consumable? |
|---|---|---|---|
| aml-substrate | `a3fb02b` (P27) | `fc98b09` (P28) | **YES** — named-identity v0.4 + entity-resolution v0.5, both additive |
| aml-casework | `cfd989f` (P15) | `4a858e6` (P16) | **NO** — P15/P16 internal harnesses; `cleared` + graded-resolution UNBUILT; still v0.3 |

The seam is **pre-cut**: `entity_spine.observe()` (Phase 74) already takes `party.identifiers[]` filtered on `strength=="strong"` — byte-aligned to substrate v0.5. `curate_workbench_cases.py` pins `SUBSTRATE_HEAD="f15c241"` (v0.3) and reads only `related_parties[]`. The consume is: bump the pin, re-curate at fc98b09, read the v0.5 fields, feed graded identifiers + resolution_edges into the spine, render real names + edges.

## 3. Scope (in / out)

**In:** the measurement (T1); `curate_workbench_cases` v0.5 bump + additive validation (T2); the spine ingestion of real graded identifiers + resolution_edges + cross-case accumulation (T3); the workbench render of real names + resolution edges (T4); re-grounding the 3 sibling briefs to live HEADs (T5); full verification + true-up (T6).

**Out (DEFERRED, NAMED not built):** the casework re-vendor (no-op — A6); executing the still-open sibling briefs (exogenous-disposition-label, C1/C7/TF determination-signals, casework `cleared` + graded-resolution); probabilistic/Splink ER; the merge-adjudication Class-J console; graph/Kuzu projection; the medallion/DuckLake stack; `news_store` convergence onto the shared spine core (the Phase-74 deferred A1 question).

## 4. Constraints (safety rails)

- **A1 file-bar guard (load-bearing):** wiring real ER into the spine MUST NOT touch `evidence_requirements.py` `evaluate_sufficiency()` / the determination bar. Confidence/priors ride the SAME grade-gated PROVENANCE path (EXCLUDES low-grade atoms, never down-weights). The byte-identical-verdict regression assertion (inject a prior `cleared` → byte-identical verdict) stays green.
- **Companion-only:** build.py imports nothing new; the 8 dists stay BYTE-FROZEN (`--check all` 8/8 + the no-import grep guard).
- **Measure, don't fabricate (A1):** if T1 measures ZERO cross-case overlap, the memory lever DOWN-SCOPES to labeled-synthetic — never assert/fabricate a real-data number.
- **Additive-only (A2):** the v0.3 curate path + the `--measure-casework` v0.3 stub consume must stay green after the bump.
- **M8 not regressed:** `news-stream.test.mjs` + `news_live_test.py` green (`news_store.py` byte-untouched).

## 5. Checkpoints

- **After T1:** STOP and report the cross-case-overlap number. It gates T3's memory-lever framing (real-data vs labeled-synthetic). If zero, confirm the down-scope before proceeding.

## 6. Assumptions (stop if violated)

A1 cross-case overlap exists (measure-first gate); A2 contract bump additive; A3 party-level identifier shape consumable by the spine as-is; A4 companion-only / dists byte-frozen; A5 the determination bar stays byte-unchanged; A6 casework has nothing consumable. (Full positions: `assumption-ledger.md` Phase 75.)

## 7. Exit criteria

1. T1 cross-case-overlap measurement recorded (a committed number); the memory-lever framing chosen from it.
2. `curate_workbench_cases` re-curated at `fc98b09` (v0.5), additive-validated; the v0.3 path + casework stub green.
3. The spine ingests real substrate graded identifiers + resolution_edges; cross-case accumulation runs on real data; `entity_spine --selftest` extended + green.
4. The workbench renders real `display_name`/`counterparty_name` + resolution edges; `workbench.test.mjs` extended + green.
5. The 3 sibling briefs re-grounded to live HEADs with BUILT/PARTIAL/NOT-BUILT status.
6. `--check all` 8/8 byte-frozen; build.py imports nothing new; news + news_live + gather + pytest green; `evidence_requirements.py` byte-unchanged; CLAUDE.md / HANDOFF.md §8 trued up.

## 8. Abort rule

Any new ship target / dist drift / a sibling-or-companion import in build.py / a validator loosened to force a fit → STOP-and-surface. Determination-bar touched (A5), breaking contract change (A2), or fabricated cross-case number (A1) → STOP.
