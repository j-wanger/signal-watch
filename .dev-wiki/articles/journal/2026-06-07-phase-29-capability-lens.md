---
title: "Phase 29: Capability lens — surface the C1–C28 / D1–D20 taxonomy as an institution coverage-by-capability view (M7)"
aliases: []
category: journal
tags: [m7, corpus-explorer, capability-lens, taxonomy, re-projection, lite]
parents: [phase-29-capability-lens]
created: 2026-06-07
updated: 2026-06-07
source: debrief
duration: ~1 session
---

# Phase 29: Capability lens — institution coverage-by-capability view over the corpus

## What Happened

The Phase-28 interview produced per-indicator `capability` (C1–C28) + `data_source` (D1–D20) codes
on every one of the 875 derived indicators — but they shipped INVISIBLE: neither `corpus.html` nor
`build.py` read them. Phase 29 surfaces them as a CAPABILITY LENS — coverage answered PER DETECTION
CAPABILITY across the whole corpus (vs PER DOCUMENT today), cross-referenced against the institution's
interview posture (have/partial/gap). This is the executive buy-in view and the realized payoff of the
28+20 interview.

Honesty model = the Phase-24 cross-corpus-synthesis precedent: a pure RE-PROJECTION of already-grounded
data. Per-capability DEMAND = honest count of corpus indicators mapping to it; institution POSTURE =
the interview answers re-grouped by capability. NO fabricated / similarity / overlap / lift number;
the always-on "Illustrative data & outputs" badge stays. The 42 derived records were BYTE-FROZEN —
they already carried the codes, so there was NO re-derivation.

The change set == the declared scope exactly — no scope creep, no escape hatches, no tasks discovered.
The two engineering-rigor candidates the Phase-28 debrief left behind were disposed at the goal gate by
a read-only grounding inspection (exact-equality dedup already exists at `derive_signals.py:353-361`;
the full-motion streaming harness path already exists at `tests/corpus-explorer.test.mjs:654-685`), so
the lens — the genuinely-unused taxonomy — was the highest-value direction.

## Decisions Made

- **Phase 29 = capability-lens UI** (recorded inline in _CURRENT_STATE Recent Decisions by /dev-plan;
  lite ceremony skips decision articles). The capability/data_source taxonomy from the Ph28 interview
  was the only entirely-unused asset in the ship artifact; the rigor candidates were mostly already done.
- **Commit the taxonomy as `data/capability-taxonomy.json`** (the Phase-24 overlay pattern; build.py
  never reads `.dev-wiki/`). Already in _CURRENT_STATE.
- **HANDOFF.md deliberately left UNCHANGED for Phase 29.** HANDOFF carries compliance/design state +
  the single-file ship-target principle, NOT a per-phase log — only CLAUDE.md + the dev-wiki track
  phases (HANDOFF was touched in Ph22/Ph28 only because those changed COMPLIANCE). Phase 29 adds no
  source, no non-negotiable change, and no change to the ship-target architecture, so a phase-log
  entry in HANDOFF would be a non-tracing edit. The surgical-changes principle says leave it byte-clean.
  (T4's scope listed HANDOFF defensively; the honest call was to leave it untouched.)

## Problems Solved

- **The taxonomy lived in `.dev-wiki/tmp/` (non-ship-grade) and `build.py` must never read `.dev-wiki/`** —
  promoted it to a committed, build-validated `data/capability-taxonomy.json` (code → {name, desc, group,
  posture}), validated fail-loud at the build boundary (`validate_capability_taxonomy`: shape + posture
  vocab {y,n,partial} + closed-vocab referential integrity against all 875 indicator codes across the 42
  records). Referential integrity held first try (pre-verified at planning).

### Review Gate

Dispatched an adversarial diff review (the suite reviewer-prompt targets SKILL.md files, so a focused
code review of the actual Phase-29 diff was the substantive gate). **Score 9/10 · Verdict: accept.**
Verified (not trusted): frozen set genuinely untouched, referential integrity holds against all 875
indicators (zero dangling/unused), honest set arithmetic (each indicator carries exactly one capability
code → sums to 875, no double-count) with no fabricated/similarity/overlap/lift number, keyboard-nav safe
(no `<input>`), every value escaped, real (non-tautological) tests, 190/0 + `--check all` 4/4 zero drift.
Two MEDIUM items, both **inert today**, deferred to Phase-30 candidates (not fixed post-gate):
- `validate_capability_taxonomy` does not warn on a *declared-but-unused* taxonomy code (all 28/20 are
  used today; `capAgg` filters `demand>0` so an unused code wouldn't even render) — "a warn, not a die".
- `fromCapability`/`fromTypology` back-precedence is moot (the 3 `pick()` call sites never set both).

## Open Questions

- None unresolved this session.

## Artifacts Changed

- `data/capability-taxonomy.json` (NEW committed overlay — 28 capabilities + 20 data sources;
  code → {name, desc, group, posture})
- `scripts/build.py` (`load_capability_taxonomy` + `validate_capability_taxonomy` + a `POSTURE={y,n,partial}`
  constant + `CAPABILITY_TAXONOMY` path + a `"taxonomy"` key in `__CORPUS__`; per-indicator codes already
  rode in via `_load_source`)
- `corpus.html` (a THIRD Select mode `selMode='capability'`; `view='capability'`;
  `currentCapability`/`fromCapability` state; `capAgg`/`indsForCap`/`postureChip`/`covSeg` helpers;
  `capCard`; `renderCapability`/`enterCapability`; the three-way Select toggle; dispatch + nav extended)
- `dist/corpus/index.html` (rebuilt; ~2.40MB → ~2.43MB)
- `tests/corpus-explorer.test.mjs` (+25 capability-lens asserts, 165 → 190)
- `CLAUDE.md`, `tests/smoke-checklist.md` (Phase-29 state bullet + Milestones line + test note;
  a Capabilities-mode human-eye check). HANDOFF.md intentionally left unchanged (see Decisions).

## Related

- [[phase-29-capability-lens|Phase 29: Capability lens]] — parent phase
- [[2026-06-07-phase-28-corpus-completeness|Phase 28]] — produced the capability/data_source codes this lens surfaces
- [[2026-06-07-phase-24-cross-corpus-synthesis|Phase 24]] — the overlay + re-projection-honesty precedent reused here

## Soft Observations / Phase N+1 Candidates

- **Overlap/near-dup guard at the extraction gate is STILL OPEN** — exact-equality dedup exists
  (`derive_signals.py:353-361` catches normalize-identical flags within a record) but the OVERLAP/near-dup
  case (what the 28 Phase-28 dupes actually were) is unguarded. | Phase-30: an overlap guard at
  `check_record` + a per-doc distinct-highlight corpus-health canary. | evidence: this journal, Ph28 dedup.
- **A parallel DATA-SOURCE lens (the D1–D20 axis)** — posture is surfaced per-capability, but there's no
  standalone "by data source" view showing which feeds unlock the most indicators. | Phase-30: natural
  extension of the 20-source half of the now-committed taxonomy. | evidence: this phase's taxonomy file.
- **The "Illustrative data & outputs" badge wording** — coverage is now GROUNDED in the interview, yet the
  always-on badge still says "illustrative". | Phase-30: revisit the wording (low priority; touches a
  non-negotiable, handle carefully). | evidence: Ph28 grounded-coverage, this lens re-projecting it.
- **Capability posture is a single interview** — a re-interview / multi-stakeholder refresh flow could
  refine it. | low priority. | evidence: the posture field in capability-taxonomy.json.
