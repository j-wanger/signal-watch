---
title: "Phase 61 — Blueprint review against what's been implemented (deep true-up + batched re-ground)"
aliases: []
category: journal
tags: [blueprint, cross-pillar, reconciliation, coverage-map, e2e-chain, verify-first, three-tier-status]
parents: [phase-61-blueprint-implementation-review]
created: 2026-06-20
updated: 2026-06-20
source: debrief
duration: ~3-4h (post-compaction estimate)
---

# Phase 61 — Blueprint review against what's been implemented

## What Happened
- `docs/program-blueprint.md` was a Phase-47/48 DESIGN snapshot whose central §3 built-vs-design-stage
  partition had gone materially STALE by the doc's OWN honesty standard: the program split into
  pillars (P50) and built **aml-substrate P1–20** (@34400e2) + **aml-casework P1–12** (@c6d8401) +
  signal-watch's coverage map / e2e chain / C/D control / corpus-redundancy. The four §3
  "(design-stage)" rows (txn monitoring · case investigation · SAR/STR narrative · LFCM assist) now
  carry substantial committed SIBLING code.
- Under ultracode the user chose **C — report + deep blueprint revision**, **batched the cross-pillar
  re-ground** (A1 up-scope over the recommended report-only boundary — the Phase-60 batching
  instinct), and **re-sync blueprint-report.html** (A3). HEADs were verified LIVE via git log this
  session, NOT read from loaded facts (the cross-pillar-review process rule).
- **T1 — the audit (96-agent fan-out)** → NEW `docs/blueprint-implementation-review.md`: per-§ status
  in a THREE-TIER vocabulary (demo-built / pillar-build-synthetic / design-stage), every built/
  pillar-built status NAMES the committed artifact verified at its pinned HEAD, both-direction drift
  enumerated (8 blueprint-stale + 6 impl-diverged), a re-grounded next-frontier ranking. The central
  finding: the §3 binary was OUTGROWN — the blueprint was UNDER-claiming (real fail-closed sibling
  code at synthetic/probe scale, NOT deployed) — and a few items were OVER-stated (composition
  detection-lift, §9 row-2/row-3, §11 /intel/ + REQUOTE-RETRY).
- **T2 — the batched verify-first re-ground**: re-pinned `signal_coverage_map.py` + `e2e_chain_check.py`
  GROUNDING_HEADS substrate 9c75c03 (P18) → 34400e2 (P20); casework unchanged @c6d8401. The diff of
  `git 9c75c03..34400e2` touched NO detector/view (only `validate/composition.py` the stress-bench, a
  51-line `monitor/signal_ref.py` helper, 2 measurement probes) → confirmed genuinely ZERO tier
  movement BEFORE re-freeze. reachable-now held 171.
- **T3 — the verified-gated blueprint deep revision**: three-tier status legend added; §3 markers +
  §7/§8/§11/§13 prose trued-up with cross-repo refs + HEAD pins; `Status: DESIGN` + the §15
  demo-charter non-negotiables PRESERVED.
- **T4 — `blueprint-report.html`** revised sections re-synced + a md↔html consistency note.
- **T5 — exit verification**: `build.py --check all` 8/8; `git diff --stat HEAD -- dist/` = ONLY
  dist/index.html (1 line, the sanctioned launcher grounding_heads cascade); regression green; no
  sibling imports.
- The user accepted delivery and chose to **switch to an aml-substrate session** for the next
  frontier (the honest near-ceiling note below).

## Decisions Made
- **Phase 61 accepted as delivered** — the reconciliation review + the deep verified-gated blueprint
  true-up + the batched re-ground were independently verified at the delivery gate and accepted.
- **Next frontier is sibling-rooted** — chosen over (a) authoring the aml-substrate emergence brief
  from signal-watch or (b) a thin signal-watch-local tidy-up; the user switches to an aml-substrate
  session for the emergence/§14-M-layer phase.

## Problems Solved
- A binary built/design-stage partition that would have either UNDER-claimed or OVERCLAIMED the
  committed sibling pillar builds — resolved with the A0 third honest status
  ("pillar-build/synthetic-scale", caveated); partials stayed "partial/pillar-scale", never "(built)".
- The stale coverage-map / e2e pins (held at P18) — re-grounded to the current sibling HEADs with a
  verify-first NO-OP-EXPECTED diff (ZERO tier movement confirmed before re-freeze; the Phase-59/60
  abort discipline never had to fire).

## Artifacts Changed
- `docs/blueprint-implementation-review.md` (NEW — the blueprint↔implementation reconciliation review)
- `docs/program-blueprint.md` (three-tier legend + §3 markers + §7/§8/§11/§13 prose, verified-gated)
- `docs/blueprint-report.html` (revised §3/§8/§11/§13 sections re-synced + md↔html consistency note)
- `data/coverage-map/{substrate-pin.json, coverage.json}` (re-pinned 9c75c03→34400e2, re-frozen)
- `scripts/signal_coverage_map.py` (`--selftest` goldens re-grounded as regression anchor only)
- `scripts/e2e_chain_check.py` + `scripts/e2e/**` (GROUNDING_HEADS re-pinned; `--real` recorded)
- `data/pillar-status.json` + `dist/index.html` (the sanctioned launcher re-ground, 1 line)

## Related
- [[phase-61-blueprint-implementation-review|Phase 61 — Blueprint review against what's been implemented]] — parent phase

## Retro Check (Phases 52-61)

| Dimension | Findings | Signal |
|-----------|----------|--------|
| 1. Recurring Blockers | 0 | none |
| 2. Decision Reversals | 1 (composition detection-lift retired at P51-prep — already a SHIPPED honesty asset, not a regression) | low |
| 3. User Corrections | 3 (P60 A3 launcher-cascade Option-A; P57 Q1 opencode-agent-loop reframe; P58 corpus-first detection-layer reframe) | low |

Recommendations:
- The recurring shape across 52-61 is the USER REFRAME / UP-SCOPE at the dev-plan gate (P57 agent-loop, P58 corpus-first, P60 combined scope, P61 batched re-ground) — this is a HEALTHY collaboration mode, not a reliability gap: each reframe carried clear intent and landed all_accept. Keep surfacing falsifiable assumptions (not direction menus) and let the user up-scope.
- The launcher-cascade (e2e re-ground → pillar-status.json → dist/index.html) is now a STABLE, named pattern (Phase-55/57/60/61 Option-A) — no longer a surprise; the abort rule correctly fires + the user picks Option-A each time. No systemic issue.
- No recurring blockers, no permission/subagent failures across the window. No dedicated improvement phase warranted.

## Soft Observations / Phase N+1 Candidates
- The next real reachable-now movement is **SIBLING-rooted** (aml-substrate emergence/§14-M-layer
  phase) and **undrivable from a signal-watch session** — the coverage-map lever is near-ceiling here
  (needs-detector=0). | Phase N+1 framing: run the re-grounded substrate emergence brief in an
  aml-substrate-rooted session. | evidence: `docs/blueprint-implementation-review.md` §7 (ranked #1);
  substrate diff 9c75c03..34400e2 touched no detector/view.
- Thin signal-watch-local residue remains as low-value candidates: §9-row-2 "human-confirmed"
  output-status third stratum (honest-labeling); the `e2e_chain_check --selftest` pillar-status.json
  clobber guard (it silently overwrites the committed `--real` state); the news REQUOTE-RETRY fold
  (§11.2 deferred half). | Phase N+1 framing: a small durability/honest-labeling tidy-up if no scale
  frontier is taken. | evidence: review §7 items #4/#5; Phase-60 soft obs.
- `docs/blueprint-implementation-review.md` is a NEW blueprint companion — like blueprint-report.html
  it is hand-synced with the blueprint md; future blueprint revisions should re-ground BOTH + the
  review against current sibling HEADs (a consistency-check candidate alongside `--check`). | evidence:
  review §6 edit list ↔ blueprint diff.
