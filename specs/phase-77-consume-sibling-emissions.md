# Phase 77 — Consume the three sibling emissions

**Ceremony:** STANDARD (cross-pillar consume; one shipped-dist touch; honesty subtleties — same class as 73/74/75).
**Status:** active (planned 2026-06-26).

## 1. Objective

Consume the NEW work both siblings shipped this session (code-verified live): bring substrate's Phase-29
`true_entities` + Phase-30 `exogenous-disposition-label` and casework's Phase-18 `cleared` verdict into
signal-watch — completing three loops the prior phases set up. The open-source **data fork** is PARKED as a
substrate handoff brief (`docs/substrate-open-reference-data-fork-PLAN-BRIEF.md`), not signal-watch work.

## 2. The consume seam (verified sibling state)

- **aml-substrate `f2da3e4`** (fc98b09→): Phase 29 emits `identity/true_entities.json`
  (`{entity_ref→cluster}`, default path, firewalled, 100% slice coverage); Phase 30 emits
  `eval/intended_disposition.json` (`{case_id, intended_disposition(file|clear), intended_basis}`, eval-only,
  authored BLIND to the sufficiency rule). Both additive — bundles byte-identical.
- **aml-casework `b3546d4`** (4a858e6→): Phase 18 adds `cleared` to `HUMAN_DISPOSITIONS` — licensed by a
  grounded exculpatory mitigation + no grounded inculpatory predicate; never system-computed; a SEPARATE
  post-verifier human-claim branch (file bar byte-unchanged). Needs a casework-contract bundle (v0.1).

## 3. Scope (in / out)

**In (ordered by strategic depth):** (T1) a determination-engine validation harness consuming
`intended_disposition` — the circularity exit; (T2/T3) re-vendor casework + the Lakeshore DECIDE signs a
`cleared` documented dismissal; (T4/T5) `true_entities` → score the merge console's real 66 (one-sided);
(T6) verification + true-up.

**Out (deferred/parked):** the open-source data fork (substrate brief, contract-neutral); the two-sided real
merge oracle (awaits the fork's real fragmentation); probabilistic/Splink ER; graph/Kuzu.

## 4. Constraints (safety rails)

- **A1 (one-sided framing):** substrate's `true_entities` clusters are content-addressed from `entity_ref`
  (`GT-sha1(ref)`) → every real SHARES truth is 'distinct'/reject. The consume scores the **human
  adjudicator** (catches over-merges), NOT the spine (tautological). The merge Verdict/ledger must STATE the
  one-sidedness + name the fork for the two-sided version; a substrate-population synthetic-only qualifier.
- **A2 (circularity exit):** the validation harness reads `evaluate_sufficiency`'s OUTPUT vs the independent
  label; the label NEVER feeds the engine; `evidence_requirements.py` BYTE-UNCHANGED.
- **A3 (cleared):** casework's file/determination bar stays byte-unchanged; the Lakeshore exculpatory evidence
  is GROUNDED in the case's affirmative mitigation, never fabricated; re-vendor must not regress signings.
- **A4 (boundary/honesty):** the ONLY dist touch is `dist/merge` re-freeze; build.py imports no
  spine/scorer/sibling/curate; synthetic-only qualifiers; no catch-rate/lift/precision; always-on badge; the
  resolver-input firewall holds (the real-66 oracle rides the revealed `oracle` block).
- **A5 (authoring-time):** the substrate emissions re-emit from a pinned slice at curate time (pin substrate
  `f2da3e4`, like `curate_workbench_cases`); the dist reads only committed data.

## 5. Checkpoints

- **After T1:** confirm the harness scores the engine against the independent label with the engine
  byte-unchanged (the circularity genuinely exited). If the harness can't run without changing the engine → STOP.
- **After T4:** confirm the real-66 oracle scores the HUMAN (not just the spine). If it can only ever score
  the spine (purely tautological) → defer consume #3 to post-fork (the A1 abort).

## 6. Assumptions (stop if violated)

A1 the one-sided oracle scores the human meaningfully; A2 the harness leaves the engine byte-unchanged; A3
the cleared consume needs no file-bar weakening / no fabricated evidence; A4 boundary/honesty hold; A5
authoring-time curation. (Full positions: `assumption-ledger.md` Phase 77.)

## 7. Exit criteria

1. `scripts/validate_determination.py --selftest` green; `evidence_requirements.py` byte-unchanged; the label proven never an engine input.
2. Casework re-vendored to `b3546d4`; the Lakeshore DECIDE signs `cleared` (grounded exculpatory, file bar byte-unchanged); existing signings unregressed.
3. The real 66 carry a one-sided substrate-sourced oracle (firewall held); `validate_merge_cases` updated in exact parity with curate; `merge.html` renders the one-sided framing; `dist/merge` re-frozen.
4. `--check all` 9 targets (only `dist/merge` re-frozen; the other 8 byte-frozen); build.py imports no spine/scorer/sibling/curate; all arcs + the harness selftest + `uv run pytest` green; CLAUDE.md + the build-order + the three briefs trued up (CONSUMED).

## 8. Abort rule

Any non-merge dist drift / a sibling-or-spine import in build.py / a loosened validator / a scored number
presented as a real catch-rate / the resolver-input firewall leaking / the casework file bar weakened or
exculpatory evidence fabricated / the exogenous label fed into the determination engine → STOP-and-surface.
If consume #3 can only score the spine (never the human) → defer it to post-fork. The open-data fork stays a
NAMED substrate handoff, never built here.
