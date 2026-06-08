---
title: "Phase 30: Data-source lens — surface the D1–D20 data-source axis as an institution coverage-by-data-source view (M7)"
aliases: []
category: journal
tags: [m7, corpus-explorer, data-source-lens, taxonomy, re-projection, lite]
parents: [phase-30-data-source-lens]
created: 2026-06-08
updated: 2026-06-08
source: debrief
duration: ~90 minutes
---

# Phase 30: Data-source lens — institution coverage-by-data-source view over the corpus

## What Happened

The Phase-28 interview tagged every one of the 875 indicators with a `data_source` (D1–D20) code, and
Phase 29 ALREADY committed the `data_sources` block in `data/capability-taxonomy.json`, had `build.py`
referential-integrity-validate it, and inlined it + the per-indicator codes into `__CORPUS__`. So only the
capability (C) axis had a UI — the data (D) axis shipped INERT. Phase 30 surfaces it as a FOURTH Select mode
(Documents / Typologies / Capabilities / **Data sources**), the symmetric counterpart to the Phase-29
capability lens, ENTIRELY in `corpus.html` — the TIGHTEST phase in the series (`build.py`, the taxonomy, and
all 42 derived records BYTE-FROZEN; +130/−14 corpus.html).

The DISTINCT story (why it isn't "the same lens twice"): a capability is a BUILD problem ("do we have the
detection logic"); a data source is an ACCESS problem ("do we even have the feed"). The payoff the abort
rule demanded: **7 of 20 data sources have posture "not yet"** — exactly the SOURCE_DATA indicators the bank
can't action until it acquires e.g. blockchain analytics / beneficial-ownership data, previously buried
per-doc, now legible corpus-wide.

Honesty = the Phase-24/29 re-projection precedent: per-data-source DEMAND = honest count of indicators
carrying the code; POSTURE = the interview answers re-grouped; covered/partial/gap = honest counts over
existing status. NO similarity/overlap/lift number; the always-on badge stays. A clean mirror — change set ==
declared scope, no scope creep, no escape hatches, no tasks discovered. The OSFI-as-a-source reframe was
disposed at the goal gate BEFORE implementation, so D-lens-only carried through with no mid-phase surprises.

## Decisions Made

- **Phase 30 = the data-source lens (D1–D20) ONLY** (recorded inline in _CURRENT_STATE Recent Decisions;
  lite skips decision articles). The user first reframed to "+OSFI as a new corpus source"; a read-only
  in-session feasibility check DISPOSED OSFI — Guideline B-8 is principles-based supervisory guidance that
  DEFERS to FINTRAC/FATF and publishes NO enumerated red-flag list (deriving from it would reproduce
  FINTRAC's indicators or fabricate; its Crown-copyright basis is fine, the CONTENT isn't a red-flag corpus).
  A landscape check found NO clean second Canadian indicator-source exists — FINTRAC is Canada's SOLE
  enumerated-indicator publisher (OSFI/CIRO/AMF defer to it). "Complete the multi-jurisdiction setup" honestly
  points to a THIRD jurisdiction (AUSTRAC [CC BY] / UK [OGL]) — offered, but the user chose the certain,
  nearly-free D-lens-only win.
- **NO new committed artifact and NO build.py change** — Phase 29 already committed + validates + inlines the
  `data_sources` axis; `corpus.html` already had `DS_BY`/`DSRC`/`dsNum`. So the frozen set GREW to include
  `scripts/build.py` + `data/capability-taxonomy.json` + all 42 derived records. The whole feature is
  `corpus.html` + harness + docs.

## Problems Solved

- **The D-axis shipped inert after Phase 29** — mirrored the capability mode onto the D-axis: `dsAgg`/
  `indsForDS`, `renderDataSource` with the INVERSE "Implements capabilities" panel, and `enterDataSource`/
  `currentDataSource`/`fromDataSource` threaded through render/back/advance/updateControls/stepIndex/
  toSelect/toLanding/pick — Back returns to the data source.

## Open Questions

- None unresolved this session.

## Artifacts Changed

- `corpus.html` (4th Select mode `selMode='datasource'`; `view='datasource'`; `currentDataSource`/
  `fromDataSource` state; `dsAgg`/`indsForDS`/`dsCard`/`renderDataSource`/`enterDataSource`; four-way toggle;
  data-access copy variants; D-cards omit the group line)
- `dist/corpus/index.html` (rebuilt; ~2.43MB → ~2.46MB / 2,457,938 B)
- `tests/corpus-explorer.test.mjs` (+27 data-source-lens asserts, 190 → 217)
- `CLAUDE.md` (Phase-30 state bullet + Milestones + test count + dist size — added by the orchestrator),
  `README.md` (a combined capability+data-source lenses paragraph; ALSO fixed the stale "Documents/Typologies"
  two-mode claim never updated for the Phase-29 Capabilities mode), `tests/smoke-checklist.md` (a Data-sources
  human-eye check)
- HANDOFF.md intentionally left BYTE-CLEAN (no compliance/architecture change — consistent with Phase 29).

## Related

- [[phase-30-data-source-lens|Phase 30: Data-source lens]] — parent phase
- [[2026-06-07-phase-29-capability-lens|Phase 29]] — the capability lens this mirrors on the D-axis
- [[2026-06-07-phase-28-corpus-completeness|Phase 28]] — produced the `data_source` codes this lens surfaces
- [[2026-06-07-phase-24-cross-corpus-synthesis|Phase 24]] — the overlay + re-projection-honesty precedent

## Soft Observations / Phase N+1 Candidates

- **Overlap/near-dup guard at the extraction gate is STILL UNGUARDED** — `derive_signals.py check_record`
  dedups only EXACT normalized-flag equality within a record (the Ph28 dupes were exact double-extractions,
  removed by hand); near-dup/substring-overlap has no guard. | Phase-31: a within-record overlap/substring
  dedup guard. | evidence: `check_record` (the norms/dups exact-match block).
- **The Canadian source path is EXHAUSTED** — FINTRAC is Canada's sole enumerated-indicator publisher
  (OSFI/CIRO/AMF defer, confirmed in-session). To genuinely complete the multi-jurisdiction setup the move is
  a THIRD JURISDICTION: AUSTRAC (CC BY) or the UK (FCA/NCA/JMLSG, OGL). Verify derivability + licence
  in-session first. | Phase-31: a third-jurisdiction source add. | evidence: this session's research.
- **The always-on "Illustrative" badge wording** could be revisited now coverage is interview-GROUNDED. LOW
  priority — touches a non-negotiable, needs explicit approval. | evidence: the Ph28 grounded-coverage interview.
- **A non-reproducible build byte-count transient** was observed once (`build.py corpus` printed 2,440,824,
  then settled deterministically at 2,457,938 across 5+ runs + seed-0; md5 stable, `--check` zero drift) —
  likely a filesystem/flush artifact, not a build bug. | Phase-31: note only; re-investigate only on spurious
  drift. | evidence: the determinism characterization run.
