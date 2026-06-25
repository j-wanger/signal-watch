---
title: "Phase 74: The persistent entity intelligence spine — consumer slice + standards/schemas + sibling handoff briefs"
aliases: ["entity spine debrief", "the memory demo session"]
category: journal
tags: [companion, entity-spine, entity-resolution, persistence, duckdb, standards, schemas, cross-pillar, sibling-briefs, confidence-grade, bitemporal, file-bar, standard]
parents: [phase-74-entity-intelligence-spine]
created: 2026-06-25
updated: 2026-06-25
source: debrief
duration: ~4-6h (post-compaction estimate; may undercount)
---

# Phase 74: The persistent entity intelligence spine — consumer slice + standards/schemas + sibling handoff briefs

## What Happened

- Stood up a companion-only **persistent entity intelligence spine** — the LFCM "memory" lever that
  separates two cases firing the SAME grounded signals but deserving OPPOSITE outcomes (Northgate-files
  / Lakeshore-clears). STANDARDS-FIRST: authored the cross-repo contract HERE, then the consumer slice
  that PROVES it, then 3 sibling emission briefs.
- T1 — 4 standards docs (`resolution-link-schema`, `identity-grade-grammar`,
  `confidence-as-provenance-contract`, `true-entities-scorer-contract`), one shared strong/weak/reject
  grade vocabulary across all 4 + the spec. CHECKPOINT cleared before building the spine.
- T2 (the one L) — `scripts/entity_spine.py`, a NEW pillar-neutral module: 3 layers (observations /
  append-only bitemporal `resolution_links` / `persistent_entities`); deterministic strong/weak/REJECT
  linkage (name-only REJECTED; 2+ distinct strong matches → refuse-as-ambiguous → new entity);
  append-only supersede; reversible `retract_link` bumps `resolution_version` + cascade-marks
  dispositions grounded across the edge "re-decision required" (audit row preserved); conflicting-
  values-both-kept; event-driven stale-prior; fail-closed-to-weakest. The DIRECTIONAL FIREWALL holds —
  `news_store.py` byte-untouched, no news import, the --selftest asserts news disposition vocab is
  core-absent + news not in `sys.modules`.
- T3 — `scripts/resolution_scorer.py` + `data/entity-spine/true_entities.json` (8 synthetic
  observations / 5 latent clusters). The resolver-input firewall is a schema-boundary ALLOW-LIST
  (`assert_no_cluster_leak` rejects a 1:1 `cluster_ref` surrogate — renaming the field does NOT pass).
  Pairwise P=1.00/R=0.67, B-cubed P=1.00/R=0.875; every number carries the synthetic-only qualifier.
- T4 — serve_workbench's SEPARATE grade-gated read path (`_cf_read_manifest`): strong/weak ADMITS,
  reject/empty QUARANTINES (excluded, never down-weighted); a per-decision `read_manifest`. The matched
  pair re-derives against the LIVE spine matching `expected_*` (Northgate ML-A4 admitted×2 strong → file;
  Lakeshore excluded edge → empty manifest → cleared). The file bar stayed BYTE-IDENTICAL.
- T5 — a GENUINE gitignored DuckDB write seam + the re-surfacing memory case (CASE-C Vesna Maric,
  shared strong email to independent prior-STR PSR-0001). The short-circuit is a MEASURED drop:
  cold_targets [ML-A4, ML-A5] → memory_targets [ML-A4] = **targets_shrink 1** + predicate
  pre-named "human trafficking". Write-then-read-back across a store REOPEN; the stale-prior guard
  fires "re-decision required" after a split bumps the version.
- T6 — the 3 sibling briefs, VERIFY-HEAD-FIRST. **Both siblings had drifted** (see Problems Solved).
- T7 — full verification + CLAUDE.md true-up.

## Decisions Made

- [[phase-74-new-module-spine-not-promote-news-store|New-module spine, not promote-news_store]] — the
  spine is `scripts/entity_spine.py`; `news_store` byte-untouched; M8 inherently safe; convergence
  deferred. Drops the A1 separability don't-know.
- [[phase-74-confidence-is-a-deterministic-ordinal-grade|Confidence is a deterministic ordinal grade]] —
  strong/weak/reject from the identifier grammar, never a fabricated score; probabilistic only if
  measured vs true_entities; fail-closed-to-weakest.
- [[phase-74-priors-are-provenance-not-a-signal-file-bar-byte-identical|Priors are provenance, not a signal; the file bar stays byte-identical]] —
  the self-confirming-loop guard; exclude-not-downweight on a separate grade-gated path; mirrors the
  Phase-73 affirmative-clear separate-path discipline.
- [[phase-74-genuine-persistent-store-and-prove-the-scorer-here|Genuine persistent store + prove the scorer here]] —
  a gitignored DuckDB write seam (the news_store precedent) + a minimal scorer behind a resolver-input
  firewall. Both the user's Step-9 picks.
- *(The A5 sibling-drift resolution is captured below in Problems Solved + memory, not as a 5th decision
  article — it is a discovery/lesson, not a design choice with alternatives.)*

## Problems Solved

- **A5 verify-HEAD-first caught REAL sibling drift** — both siblings had moved off the assumed pins,
  and reasoning from loaded facts would have produced wrong briefs. aml-substrate was at **a3fb02b**
  (close Phase 27), NOT f15c241: its `gen/identity.py` is already a FULL identity subsystem
  (email/phone/device_id + SHARES_* edges, `--identity` flag), and a ground-truth-blind
  `resolve/resolver.py` + a B-cubed/pairwise `resolve/measure.py` scorer ALREADY EXIST → the real gap
  is the counterparty LEG + a `strength` tag on `RelationshipEdge` (`attrs` is `dict[str,int]`, needs
  widening), NOT greenfield ER. aml-casework was at **cfd989f** (close Phase 15), NOT bf15535: the
  `cleared` path is still NOT built → CW-4 remains a GAP. All 3 briefs re-grounded to live HEADs with a
  drift note each.
- **The file-bar guard held under wiring pressure** — confidence/priors route AROUND `evaluate_sufficiency`
  (which structurally has no prior/disposition/history param). Proven: injecting a prior `cleared` yields
  a byte-identical (json sort_keys) verdict; `evidence_requirements.py` is byte-unchanged (empty
  `git diff --stat`).
- **The memory short-circuit is a number, not a status flag** (the A2 circularity STOP respected) — the
  re-surfacing prior is INDEPENDENT-provenance (the prior-STR register), never hand-set to steer; the
  measured drop in gather targets-to-close is the proof.
- **Diff hygiene** — the regenerated casefile render fixtures were re-emitted at the Phase-73 indent=1
  format so the diff stays surgical (only the new `read_manifest` field moves).

## Open Questions

- **Convergence** — `news_store` adopting the shared pillar-neutral spine core (the deferred A1
  separability question) is a Phase-75+ candidate, not closed here.
- **The memory beat is proven by a measured number but not yet RENDERED in `workbench.html`** — a
  visible-render polish follow-on (T5 scope was serve_workbench/data/tests).

## Artifacts Changed

- `scripts/entity_spine.py` (NEW — the pillar-neutral spine module + --selftest)
- `scripts/resolution_scorer.py` (NEW — the synthetic-validated resolution scorer + firewall + --selftest)
- `data/entity-spine/true_entities.json` (NEW committed; `data/entity-spine/store/` gitignored)
- `scripts/serve_workbench.py` (grade-gated read path + per-decision manifest + `casefile_memory` +
  the genuine gitignored DuckDB write seam + the stale-prior guard)
- `data/casefile/case.json` (the `resurfacing` block — CASE-C, kept OUT of `cases[]`)
- `scripts/evidence_requirements.py` (--selftest ONLY: the inject-a-prior-`cleared`→byte-identical
  assertion; the file bar byte-unchanged)
- `docs/{resolution-link-schema, identity-grade-grammar, confidence-as-provenance-contract,
  true-entities-scorer-contract}.md` (NEW — the 4 standards)
- `docs/{substrate-graded-counterparty-identifiers, substrate-exogenous-disposition-label,
  casework-confidence-graded-resolution}-PLAN-BRIEF.md` (NEW — the 3 sibling briefs, pinned to verified HEADs)
- `tests/test_selftests.py` (entity_spine + resolution_scorer added to PY_SELFTESTS)
- `CLAUDE.md` (`## Current state` trued up — replace-in-place)

### Review Gate (STANDARD — ran this session, 2-reviewer adversarial workflow)

Verdict: **ship / ship.** All findings PRAISE, zero bugs.

- **Correctness reviewer** verified: ambiguity refuses merge; append-only links; cascade-invalidation
  marks only grounded dispositions; stale-prior on version bump; `edge_grade` pure + fail-closed;
  pairwise/B-cubed sound; the firewall catches renamed surrogates; grade-gating excludes low-grade;
  the persistence round-trip is genuine; targets-shrink is measured.
- **Discipline reviewer** verified all 8 invariants HELD: file-bar byte-unchanged; news byte-untouched
  + M8 unregressed; build.py isolation; metrics honesty (synthetic-only qualifier); memory-demo
  independent-provenance; E-CALDERON name-only rejection; exclude-not-down-weight; standards/briefs
  coherence.
- **Self-review:** 5 pass + 1 firewall-justified `_norm()` duplication note (entity_spine must NOT
  import news_store → the small duplication is the correct trade for the directional firewall).

## Related

- [[phase-74-entity-intelligence-spine|Phase 74 — The persistent entity intelligence spine]] — parent phase

## Soft Observations / Phase N+1 Candidates

- The memory short-circuit is proven by a measured number (cold 2 → memory 1 targets) but NOT yet
  rendered in `workbench.html` | Phase-75: render the memory beat in the workbench surface | this journal T5
- Convergence: `news_store` could adopt the shared pillar-neutral spine core | Phase-75+: spine convergence (the deferred A1 question) | [[phase-74-new-module-spine-not-promote-news-store]]
- Probabilistic/Splink ER + the merge-adjudication Class-J console | a governed-enhancement phase, named in the standards | `docs/confidence-as-provenance-contract.md`
- The 3 sibling emission briefs are ready for SIBLING execution (substrate counterparty leg + strength tag; substrate exogenous disposition label; casework cleared-path + graded-resolution consume) | sibling aml-substrate / aml-casework phases | the 3 PLAN-BRIEFs
- Graph/Kuzu projection over the spine | a governed-enhancement phase | `docs/resolution-link-schema.md`
