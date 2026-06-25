---
title: "Phase 74: The persistent entity intelligence spine — consumer slice + standards/schemas + sibling handoff briefs"
aliases: ["entity intelligence spine", "persistent entity spine", "entity_spine", "the memory demo", "resolution-link standards"]
category: phases
tags: [companion, entity-spine, entity-resolution, persistence, duckdb, standards, schemas, cross-pillar, sibling-briefs, confidence-grade, bitemporal, standard]
parents: []
created: 2026-06-25
updated: 2026-06-25
source: plan
status: active
scope: ["scripts/entity_spine.py", "scripts/resolution_scorer.py", "scripts/serve_workbench.py", "scripts/evidence_requirements.py", "data/entity-spine/**", "data/casefile/**", "docs/resolution-link-schema.md", "docs/identity-grade-grammar.md", "docs/confidence-as-provenance-contract.md", "docs/true-entities-scorer-contract.md", "docs/substrate-graded-counterparty-identifiers-PLAN-BRIEF.md", "docs/substrate-exogenous-disposition-label-PLAN-BRIEF.md", "docs/casework-confidence-graded-resolution-PLAN-BRIEF.md", "tests/workbench.test.mjs", "tests/**", "CLAUDE.md", "HANDOFF.md"]
entry_criteria: "Phase 73 DELIVERED + accepted + committed (f804722); the live companion workbench runs (serve_workbench + evidence_requirements + workbench.html) over the matched Northgate/Lakeshore casefile pair (data/casefile/case.json); evidence_requirements.py's file/determination bar is byte-frozen (the A1 guard, asserted by --selftest); news_store.py is the M8 DuckDB store (anchor + provenance + conflict-both-kept + reversible prune); the spec is approved (specs/phase-74-entity-intelligence-spine.md, STANDARD); the direction gate is CLOSED (assumption-ledger Phase-74 — A2/A3/A4 accept, A1/A5 don't-know→DOWN-SCOPED, never all-accept)."
exit_criteria: "The 4 standards + 3 sibling briefs exist with one shared grade vocabulary (strong/weak/reject); scripts/entity_spine.py --selftest passes (observation→bitemporal link→persistent_entity; deterministic strong/weak/REJECT linkage [name-only rejected]; append-only supersede-not-overwrite; reversible split WITH cascade-invalidation; conflicting-values-both-kept; confidence=grade) with the directional no-news-import firewall; the minimal scorer --selftest passes over a tiny synthetic true_entities with the resolver-input firewall (no cluster-id field, no 1:1 surrogate); serve_workbench's grade-gated read path + per-decision admitted/quarantined manifest re-derives the matched pair against the LIVE spine matching expected_*; the self-confirming-loop guard proves injecting a prior cleared yields a byte-identical file/clear verdict; the genuine gitignored DuckDB write seam + the re-surfacing memory case shrink the gather targets-to-close measurably + the stale-prior re-examine path fires; evidence_requirements.py --selftest passes UNCHANGED (the file bar byte-identical); python3 scripts/build.py --check all 8/8 byte-frozen + build.py imports no spine/scorer; node tests/workbench.test.mjs + node tests/news-stream.test.mjs + python3 tests/news_live_test.py + uv run pytest all green; CLAUDE.md trued up."
---

# Phase 74: The persistent entity intelligence spine — consumer slice + standards/schemas + sibling handoff briefs

## Objective

Stand up a companion-only **persistent entity intelligence spine** that ties records to the same
counterparty over time, presents each entity's resolved context (network, source of funds, prior
dispositions) consistently on every surfacing, and accumulates prior decisions on the entity — proven
by a thin deterministic slice in the live investigator workbench. The decisioning lever this program
chases — separating two cases that fire the SAME grounded signals but deserve OPPOSITE outcomes
(Northgate-files / Lakeshore-clears) — rests on evidence that lives in the entity's network and
source of funds; that evidence must PERSIST on a resolved entity or every alert re-gathers it cold.
Author the cross-repo **standards/schemas** (resolution-link, identity-grade grammar, confidence-as-
provenance, the true_entities scorer contract) HERE — the contract everything depends on — then a
thin deterministic consumer slice that PROVES them, then **three emission briefs** handed off to the
sibling repos. STANDARDS-FIRST, then the consumer, then the briefs.

## Scope

Companion-only — NO ship target; the 8 offline dists stay byte-frozen; `build.py` imports neither the
spine nor its schema/scorer. Files and modules affected:
- `scripts/entity_spine.py` (NEW) — the pillar-neutral spine: observation → bitemporal resolution
  link → `persistent_entity`; deterministic strong/weak/REJECT linkage; append-only supersede;
  reversible split with cascade-invalidation; conflicting-values-both-kept; confidence=grade.
  `news_store.py` stays BYTE-UNTOUCHED (the directional firewall — no news import).
- `scripts/resolution_scorer.py` (NEW) + `data/entity-spine/true_entities.*` — a minimal scorer over
  a tiny synthetic `true_entities` (pairwise P/R or cluster-F1/B-cubed) behind the resolver-input
  firewall (no cluster-id field, no 1:1 surrogate); synthetic-only qualifier mandatory.
- `scripts/serve_workbench.py` — the grade-gated read path (unknown/missing grade + null `basis[]` →
  weakest → EXCLUDED from filing inputs); the per-decision admitted/quarantined manifest; the genuine
  gitignored DuckDB write seam (write a disposition, read it back); the re-surfacing memory case +
  the stale-prior (event-driven supersession) guard; the matched pair re-derives against the live
  spine (the fixture-drift bridge).
- `scripts/evidence_requirements.py` — `--selftest` ONLY (the file bar is byte-untouched) + the new
  inject-a-prior-`cleared`→byte-identical assertion.
- `data/casefile/**` — possibly the authored re-surfacing case (or a new re-surfacing data file).
- `docs/{resolution-link-schema, identity-grade-grammar, confidence-as-provenance-contract,
  true-entities-scorer-contract}.md` — the 4 standards. `docs/{substrate-graded-counterparty-
  identifiers, substrate-exogenous-disposition-label, casework-confidence-graded-resolution}-PLAN-
  BRIEF.md` — the 3 sibling briefs (each pins a code-verified sibling commit).
- `tests/**`, `CLAUDE.md`, `HANDOFF.md`.

## Exit Criteria

- [ ] T1: the 4 standards exist (`test -f`) and the grade vocabulary (strong/weak/reject) is used
      consistently across all 4 docs + the spec (a grep consistency check). CHECKPOINT: report the
      resolution-link schema + grade vocabulary before building the spine.
- [ ] T2: `python3 scripts/entity_spine.py --selftest` passes (observation → bitemporal link →
      persistent_entity; deterministic strong/weak/REJECT linkage [name-only rejected]; append-only
      supersede-not-overwrite; reversible split WITH cascade-invalidation [a disposition grounded
      across an edge flips to "re-decision required", audit row preserved]; conflicting-values-both-
      kept; confidence=grade); `grep -nE "^(import|from) " scripts/entity_spine.py` shows no
      news_store/serve_news import; the --selftest asserts news disposition vocab is NOT in the core.
- [ ] T3: `python3 scripts/resolution_scorer.py --selftest` passes over a tiny synthetic
      `true_entities` AND a contract test asserts no resolver-input field is the cluster id NOR
      1:1-correlated with cluster identity (renaming the cluster field does NOT pass).
- [ ] T4: a SEPARATE grade-gated read path (unknown/missing grade AND null `basis[]` → weakest →
      EXCLUDED) + a per-decision admitted/quarantined manifest; the matched pair re-derives against
      the live spine matching `expected_*`; `python3 scripts/evidence_requirements.py --selftest`
      passes UNCHANGED AND a new assertion proves injecting a prior `cleared` yields a byte-identical
      file/clear verdict; `serve_workbench --selftest` re-derives the pair against the live spine.
- [ ] T5: the genuine gitignored DuckDB write seam (write a disposition, read it back); a re-surfacing
      case (an entity surfaces in a 2nd case after an INDEPENDENT-provenance prior) whose second
      surfacing attaches the prior + grounding chain so the gather targets-to-close MEASURABLY shrink
      (the short-circuit is the measured drop, not a status flag); the stale-prior guard (event-driven
      supersession; the prior carries the resolution-version decided under) — `serve_workbench
      --selftest` asserts both.
- [ ] T6: the 3 sibling briefs exist (`test -f`) and each contains a pinned sibling commit hash;
      BOTH siblings' live HEAD code-verified BEFORE writing (the A5 precondition).
- [ ] T7: `python3 scripts/build.py --check all` 8/8 byte-identical AND `grep -n import scripts/build.py`
      shows no spine/scorer import; `node tests/workbench.test.mjs` + `node tests/news-stream.test.mjs`
      + `python3 tests/news_live_test.py` + `uv run pytest` all green; CLAUDE.md trued up
      (replace-in-place, no per-phase bullet).

## Constraints

- **A1 file-bar guard (load-bearing) — confidence routes AROUND the frozen filing engine, never
  through it.** A low-confidence link must not flip a frozen-threshold decision: any atom inherited
  across a link below a declared grade is EXCLUDED (not down-weighted); `evidence_requirements.py`
  stays BYTE-IDENTICAL (its `--selftest` passes unchanged). If wiring requires ANY change to
  `evaluate_sufficiency()` or the determination bar → STOP-and-surface.
  *Prevents: a weak identity link silently flipping a file/clear a boolean engine can't qualify.*
- **The self-confirming-loop guard** — accumulated dispositions must NOT become a signal. Priors
  enter only as analyst-visible provenance; a regression test asserts injecting a prior `cleared`
  yields ZERO change in the file/clear output for a fixed evidence set.
  *Prevents: "previously cleared → clears again" — the store laundering its own past decisions.*
- **New-module firewall** — the spine is `scripts/entity_spine.py`; `news_store.py` byte-untouched;
  `entity_spine.py` imports no `news_store`/`serve_news` (directional, not a token blocklist); the
  --selftest asserts news disposition vocab is core-absent. `node tests/news-stream.test.mjs` +
  `python3 tests/news_live_test.py` stay green (M8 not regressed).
  *Prevents: rewriting the M8 anchor table out from under the live news pillar.*
- **The synthetic ground-truth cluster id must never reach the resolver** — the resolver-input schema
  physically omits any cluster field; a contract test fails on a 1:1-correlated surrogate (renaming
  the cluster field does not pass); the cluster id lives only in the scorer's evaluation-only channel.
  Every resolver-quality number carries the "measured on synthetic clusters; production has no ground
  truth" qualifier. *Prevents: a leaked cluster id making the resolver trivially "accurate".*
- **Companion-only boundary (A4)** — a genuine gitignored DuckDB write seam crosses "persists nothing"
  DELIBERATELY + only in the companion (the `news_store` precedent: a 127.0.0.1 gitignored DuckDB
  store is §4.5-clean); `build.py` imports neither spine nor scorer; `--check all` 8/8 byte-identical.
  *Prevents: a companion persistence seam leaking into a ship artifact or build.py.*
- **Confidence must not collapse to a bare float across repos** — the standard defines an ordinal
  grade with named criteria + `basis[]`; the gate keys on the grade; a missing/unrecognized grade
  fails closed to weakest. *Prevents: a fabricated-shaped match score crossing the cross-pillar
  contract.*

## Checkpoints

- After T1 (the standards/schemas, BEFORE building the spine): STOP and report the resolution-link
  schema + the ordinal grade vocabulary — these are the contract everything else depends on; a wrong
  grade vocabulary propagates into the gate and the briefs.
- After the spine `--selftest` is green and the workbench reads from it but BEFORE the memory demo
  (T4→T5): report that the matched pair still derives the same verdicts against the live spine (the
  fixture-drift oracle held).
- If wiring the spine requires ANY change to `evaluate_sufficiency()` or the determination bar → STOP
  and surface (the file bar is byte-frozen; route confidence/priors around it).
- If deterministic linkage cannot separate the matched pair without name-only matching (which the
  grammar rejects) → STOP: the casefile may lack a strong identifier the grammar needs — a data-
  authoring finding, never a license to loosen the grammar.
- If the re-surfacing prior must be hand-set to steer the verdict (the A2 circularity trap) → STOP.
- If a sibling brief would target stale state (A5) → re-verify the sibling's live HEAD before writing.

## Assumptions

- A1 [HIGH — T0 weakest, DON'T-KNOW → DOWN-SCOPED] news_store's machinery may not be cleanly
  separable from its name-anchor + serve_news coupling. RESOLUTION: drop the dependency — the spine
  is a NEW module `entity_spine.py`; `news_store` byte-untouched → the M8 arc is inherently safe.
  Convergence is a DEFERRED Phase-75+ question.
- A2 [HIGH, ACCEPT] an honest re-surfacing scenario can be authored — an entity surfaces in a SECOND
  case after a prior disposition from INDEPENDENT provenance (a prior STR/case record), not hand-set
  to steer the verdict. If the only re-surfacing that works requires hand-setting the prior → STOP.
- A3 [MED, ACCEPT-with-EVIDENCE — census-verified] the casefile pair carries strong identifiers
  (email/phone 'strong') sufficient for DETERMINISTIC in-pair linkage without name-only matching
  (census: shared email strong on E-CALDER↔E-CALDER-EXT and E-MARIC↔prior-STR; phone strong on
  E-OKONKWO; address weak; E-CALDERON name-only EXCLUDED). If a needed link rests on name-only → STOP
  (a casefile finding, never relax name-only rejection).
- A4 [MED, ACCEPT] a genuine gitignored DuckDB write seam in serve_workbench stays §4.5-clean +
  companion-firewalled (the news_store precedent). If the seam leaks into build.py or a dist drifts →
  STOP.
- A5 [MED — cross-pillar drift, DON'T-KNOW → DOWN-SCOPED] the siblings' live state may not match the
  briefs' assumptions. RESOLUTION: code-verify BOTH siblings' live HEAD BEFORE writing any brief; pin
  the verified commit in each (the standing verify-the-sibling rule made a hard precondition).

## Notes

STANDARD phase (user override of the project LITE default — cross-pillar contract/schema work, high
blast radius). The four planning decisions (confidence medium, source plan):

1. **New-module spine, not promote-news_store** — build `scripts/entity_spine.py`; `news_store`
   byte-untouched; the M8 arc inherently safe; convergence deferred. Resolves the A1 don't-know by
   dropping the separability dependency. ([[decisions/phase-74-new-module-spine-not-promote-news-store]])
2. **Confidence is a deterministic ordinal grade, never a fabricated score** — strong/weak/reject
   from the identifier grammar; probabilistic only when measured vs true_entities; fail-closed-to-
   weakest. ([[decisions/phase-74-confidence-is-a-deterministic-ordinal-grade]])
3. **Priors are provenance, not a signal; confidence on a separate path; the file bar stays
   byte-identical** — the self-confirming-loop guard + the frozen-boolean problem → exclude-not-
   downweight; a regression assertion proves injecting a prior `cleared` is byte-identical. Mirrors
   the Phase-73 affirmative-clear separate-path discipline.
   ([[decisions/phase-74-priors-are-provenance-not-a-signal-file-bar-byte-identical]])
4. **Genuine persistent store + prove the scorer here** — a gitignored DuckDB write seam (the
   news_store precedent) + a minimal scorer over synthetic true_entities behind a resolver-input
   firewall (no cluster field, no 1:1 surrogate). Both the user's Step-9 picks.
   ([[decisions/phase-74-genuine-persistent-store-and-prove-the-scorer-here]])

Wiki knowledge folded in: loosening ER match rules WITHOUT identifier layering pushes false positives
>90% — the strong/weak/reject grammar IS the textbook fix (name is a weak observation). pKYC is
EVENT-DRIVEN, not interval-driven (a material change / new disposition triggers a review) — the exact
frame for the re-surfacing memory demo AND the stale-prior guard (staleness = event-superseded, not
clock-old). FINTRAC (the Canadian-bank audience): BO traced through all layers to natural persons,
confirmed at onboarding AND ongoing monitoring — regulatory backing for the multi-hop BO + the
bitemporal ongoing-monitoring model. The honesty governor: news_store keeps confidence RESERVED
because a model confidence is a fabricated-shaped number; the spine's grade is deterministic linkage-
strength, probabilistic only if measured vs true_entities.

Knowledge GAPS (authored fresh, chosen-not-measured, named in the briefs/standards): bitemporal data
modeling (valid-time + decision-time, supersede-not-overwrite, reversible merge/un-merge — 1D lenses
only, production = decision-time frozen / analytics = current-resolution recompute, NO 2D
cross-product; stale-prior = event-driven supersession; the pKYC event-driven model is the basis) —
nothing in the wiki. Resolution-correctness scorer metrics (pairwise P/R, cluster-F1 / B-cubed) — no
wiki article; aml-substrate's own `test_resolution_lift.py` is the in-family reference.

Out of scope (DEFERRED as governed enhancements, NAMED in the standards not built): probabilistic /
Splink ER, the merge-adjudication Class-J console, graph/Kuzu analytics, and the full
medallion/DuckLake stack; any 2D (resolution-version × data-snapshot) time-travel; any change to the
8 dists or the filing/determination threshold; EXECUTING the sibling briefs (emitted here,
implemented in their own repos).

Direction gate 2026-06-25 — NOT all-accept (two don't-knows DOWN-SCOPED, never a silent pass): A1
→ new-module (drop separability), A5 → verify-both-siblings'-HEAD-first. Spec
`specs/phase-74-entity-intelligence-spine.md` (STANDARD; adversarial constraints + two-tier review,
revise→fixed). Ledger Phase-74. The claim most likely to be wrong (named at planning): that the
matched pair separates on DETERMINISTIC strong-identifier linkage alone (A3) — defended by the
casefile census + the STOP-if-name-only rule (a data finding, never a grammar relaxation).
</content>
</invoke>
