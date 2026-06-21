---
title: "Phase 62 — Grounded probe-history consume (§12) + §14-frozen boundary + P22 pin re-ground (lite, planned 2026-06-20, delivered+accepted 2026-06-21)"
aliases: []
category: journal
tags: [probe-history, grounded-consume, triage-console, cross-pillar, substrate-pin, honesty-split, scope-checkpoint]
parents: [phase-62-grounded-probe-history-consume]
created: 2026-06-21
updated: 2026-06-21
source: debrief
duration: ~1 session
---

# Phase 62 — Grounded probe-history consume (§12) + §14-frozen boundary + P22 pin re-ground

## What Happened

- The phase was PLANNED (2026-06-20, all_accept:false) as a two-pronged END-TO-END consume of aml-substrate's
  P22 "grounded probe-history" projector: (1) the §12 non-ship measurement layer (`probe_history_stats.py`)
  AND (2) a **sanctioned USER-OVERRIDE unfreeze of `dist/triage`** (the §14 triage console), re-curating
  `scenarios.json` off the grounded `alert-history.json` instead of the SYNTHETIC Phase-48 fixture.
- **REDIRECT from the loaded planning frame:** the consume target was the §12 MEASUREMENT layer, NOT a
  coverage-map re-ground — the coverage re-ground is a known zero-movement no-op (P21/P22 added no
  detector/view). That redirect was correct: T6's pin move to substrate@ae98924 produced ZERO tier movement
  (reachable-now held 171), exactly as anticipated.
- **A0 (verify-first the substrate committed HEAD) DID REAL WORK.** The loaded planning facts pinned
  2e5d0f0/P21; code-verify (`git -C /Users/jwang/aml-substrate`) found P22 committed at **ae98924** — the
  planning facts were stale, exactly the failure A0 exists to catch (the cross-pillar re-ground rule
  vindicated again). Ran the COMMITTED `--probe-history` projector (sanctioned tool-use, file-contract
  output) → `data/probe-history/grounded/alert-history.json`: **4,966 real label-blind firings** (C2 2433 /
  C3 2269 / C5 210 / C15 54; C4/C6 absent), 618 entities, deterministic (sha256 `d9d1110e`, byte-identical
  re-run), HEAD pinned in `provenance.json`.
- **T4 was the load-bearing checkpoint — the A1 pause-checkpoint FIRED and the §14 unfreeze was STOOD DOWN.**
  Reading `curate_triage_scenarios.py` firsthand surfaced the §12/§14 SOURCE BOUNDARY: the substrate's
  label-blind grounded probe-history is the RIGHT source for §12 (firing/disposition MEASUREMENT) but the
  WRONG source for §14 (the triage console needs adjudicable FACT PATTERNS — customer profiles, activity
  narratives, KYC notes — which the substrate doesn't emit). `curate_triage_scenarios.py` couples to
  alert-history via only **5 metadata fields on 7/20 scenarios**; everything substantive
  (panels/divergent-pair/controls) is hand-authored, and the marquee TM-104 pair is **C20 — no substrate
  detector** (the grounded build fires only C2/C3/C5/C15). So a genuinely grounded §14 needs its own
  fact-pattern-synthesizer phase. PAUSED + reported → **the user accepted the boundary** → §14 stays FROZEN,
  NO re-curation, NO redesign-to-force (the A1 fallback exactly: §12-measurement-consume-only).
- Net result: scope shrank from the planned end-to-end unfreeze to **§12-measurement-only**. **`dist/triage`
  stays BYTE-FROZEN**; the ONLY dist change is the launcher pin cascade (`dist/index.html`, 1 line — the
  Phase-60 Option-A pattern). `--check all` stayed 8/8 throughout.

## Problems Solved

- **Stale sibling pin** — the loaded P21/2e5d0f0 facts vs the real P22/ae98924 committed HEAD — caught by A0's
  verify-first gate before any consume; the projector was run against the verified-committed HEAD.
- **The §12/§14 source mismatch** — surfaced at the T4 checkpoint instead of being papered over by
  redesigning the console to force the fit; resolved by accepting the boundary (the gate-sanctioned A1
  fallback).
- **`silent_rules` definitional gap** — the substrate detects per-CAPABILITY, not per-rule-variant, so the
  legacy per-rule-id silence metric had no clean grounded analogue → redefined `silent_rules` to
  CAPABILITY-level silence (a measured definitional adaptation, surfaced not hidden).

## Open Questions

- A genuinely grounded §14 would need a **fact-pattern synthesizer** pairing substrate alerts with adjudicable
  narratives (customer profiles / activity / KYC) — a future-phase candidate; the substrate would need to
  emit/derive adjudicable fact patterns.
- **C4 (structuring) reads as 0 firings at n=1000/m10** — empirically absent; possibly a scale property
  rather than a detection gap (a substrate-side measurement question; does NOT affect the §14 boundary, since
  C20/C10 are structurally absent regardless).
- The blueprint/review docs (`program-blueprint.md`, `blueprint-implementation-review.md`) still pin P20
  (34400e2) — CORRECT as historical (they re-ground at the next blueprint-revision phase per the cross-pillar
  rule), but a future-phase item to track.

## Artifacts Changed

- `data/probe-history/grounded/` (NEW — `alert-history.json` [4,966 firings, sha256 `d9d1110e`] +
  `provenance.json` pinning substrate@ae98924 + the reproduce command `--clients 1000 --months 10 --seed 42
  --probe-history`)
- `data/probe-history/capability-tm-map.json` (NEW — the C-code→TM-### namespace map; selftested
  inversion-faithful; C15→∅ honest-null, the substrate fires a capability the legacy rulebook never authored)
- `scripts/probe_history_stats.py` (gained `--grounded` + `--selftest`; the synthetic default path stays
  BYTE-IDENTICAL — a regression baseline; every disposition-derived metric tagged "[over illustrative
  dispositions]")
- `docs/probe-history.md` (Phase-62 grounded-consume section + the §14-frozen boundary statement)
- `data/coverage-map/{substrate-pin,coverage}.json` · `scripts/e2e_chain_check.py` · `data/pillar-status.json`
  · `dist/index.html` (cross-pillar pins moved P20[34400e2]→P22[ae98924]; VERIFIED ZERO tier movement,
  reachable-now 171; the launcher re-grounded — 1 line; the other 7 dists incl. dist/triage byte-frozen)
- `CLAUDE.md` (current-state probe-history mention updated in-place: the grounded consume + the
  §12-right/§14-wrong boundary)

## Related

- [[phase-62-grounded-probe-history-consume|Phase 62 — Grounded probe-history consume (§12) + §14-frozen boundary + P22 pin re-ground]] — parent phase

## Soft Observations / Phase N+1 Candidates

- The §14 grounded-scenario pipeline (a fact-pattern synthesizer pairing substrate alerts with adjudicable
  narratives) — the genuinely-grounded §14, its own future phase; the substrate would need to emit/derive
  adjudicable fact patterns. | a §14 grounded-fact-pattern phase | this journal "Open Questions" + ledger
  Phase-62 RESOLUTION
- C4 (structuring) firing-rate at n=1000/m10 = 0 — a candidate substrate-side measurement (scale property vs
  detection gap). | an aml-substrate measurement probe | provenance.json `rule_ids_absent`
- The blueprint/review docs still pin P20 (34400e2) — correct as historical, re-ground at the next
  blueprint-revision phase per the cross-pillar rule. | a blueprint-revision re-ground | the cross-pillar
  re-ground rule (active-phase Standing constraints)
- The scale frontier remains SIBLING-rooted (the substrate emergence / §14-M-layer engine) — re-confirmed
  this session. | an aml-substrate emergence/§14-M-layer phase | MEMORY.md cross-pillar-consume-batch
