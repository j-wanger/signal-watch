---
title: "Phase 60 — Consume the landed sibling halves: the C7 reachable-now rise + the real e2e chain"
date: 2026-06-19
type: journal
phase: 60
tags: [cross-pillar, signal-coverage-map, e2e-chain, consume, reachable-now, c7, emergence-doctrine, verify-first, launcher, non-ship]
---

# Phase 60 — Consume the landed sibling halves (2026-06-19)

## What happened

A cross-pillar review (code-verified, not from loaded facts) found **both siblings moved 3 phases** past the
Phase-59 pins: aml-substrate@`9c75c03` (P18 — emits the real C8 party-bearing v0.2 bundle) + aml-casework@`c6d8401`
(P12 — C7/C8/C14 grounding_replay assertions; C26 honest null). Phase 59 A2 said reachable-now rises only when both
halves land — they had. The user up-scoped to the **combined scope** (coverage-map consume + the real e2e chain) and
chose **verify-first then freeze**. All 5 tasks delivered + accepted via /dev-debrief.

## The result

- **First real reachable-now rise: 93 → 171 (+78).** needs-detector exhausted 62→0; needs-view-exposure 70→69;
  needs-behavior 296→281. coverage.json re-frozen, `--check` byte-identical, `--selftest` green.
- **The honest headline: all +78 is C7.** Only C7 has `behavior_emergence=="emerges"`; once its assertion landed,
  `is_reachable(C7)` is true → ALL 78 C7 buildable signals flip (62 direct + 16 proxy, because `is_reachable` is
  evaluated *before* the data_source_class branch). **C8/C14/C26 moved 0** — data-only/absent is the binding 3rd
  conjunct, NEITHER emission nor assertion work. Phase 59's "both halves must land" sharpened to *"only the cap whose
  behavior genuinely emerges reaches reachable-now."*
- **The real cross-pillar chain CONNECTS.** First real contact: casework consumed substrate's C8 v0.2 bundle
  (`CASE-P-0000251`) → signed SAR, zero blocking violations (all 6 verifiers passed, no contract-version gap);
  `e2e_chain_check --real` CONNECTED (C4 too).

## Decisions

- **Direction (all_accept:true):** combined scope (coverage map + e2e chain) over the recommended coverage-only;
  verify-first then freeze on the C7 number. Ledger Phase-60.
- **Option A (mid-impl, A3 bit):** accept the sanctioned launcher re-ground (the Phase-55/57 pattern — the launcher
  IS the cross-pillar status front door) over verification-only / defer. 7/8 dists byte-identical, only `dist/index.html`
  moved (grounding_heads).

## What bit

- **The +62→+78 correction (A0 held-with-correction).** The first verification undercounted the rise as +62 by
  counting only the 62 `needs-detector` C7 signals. Re-reading `classify()` — `is_reachable` precedes the
  data_source_class branch — revealed all 78 C7 flip (the 16 in needs-behavior/needs-view-exposure become
  proxy-reachable). Caught at planning, confirmed empirically before the freeze. **This is verify-first paying off.**
- **A3 bit (the launcher cascade).** "Zero ship artifacts" was correct for the coverage-map-only scope but wrong for
  the combined scope: `e2e_chain_check` regenerates `pillar-status.json` (grounding_heads), which the launcher dist
  embeds → re-grounding the e2e artifact inherently re-grounds the launcher. STOP-and-surfaced per the abort rule;
  resolved by the user's Option-A.

## Health Delta

- coverage map `--selftest`: 2 goldens re-grounded to the verified C7-live reality (live set + C7/D1→reachable-now)
  as **regression anchors for the landing**, NOT a loosening; `C8/D1→needs-behavior` retained and now proves an
  assertion alone doesn't move a data-only cap. e2e `--selftest` PASS. `build.py --check all` 8/8.

## Soft Observations / Phase 61 candidates

- **The coverage-map reachable-now lever is near its honest CEILING from signal-watch's side.** needs-detector is
  exhausted (0); the remaining tiers are either sibling-rooted substrate work (needs-view-exposure 69 + the genuine
  emergence gaps in needs-behavior) or honest ceilings (C8/C14 may be permanently `data-only` — substrate's own basis
  calls C8 "burst-magnitude re-expressed" and C14 "correctly uncorrelated with laundering"; C26 absent; 2 out-of-reach).
  The next REAL reachable-now movement is a **sibling-rooted aml-substrate phase** (emergence-engine + view-exposure;
  briefs re-grounded + ready) — not drivable from a signal-watch session. Evidence: `data/coverage-map/coverage.json`
  summary + `docs/corpus-substrate-coverage.md` §3b.
- **e2e `--selftest` silently clobbers the committed `pillar-status.json`** (writes "bridges pending" → would drift the
  launcher). A guard (don't write the committed status file on selftest, or restore-after) is a small hygiene candidate.
  Evidence: T5 — the selftest overwrote the --real CONNECTED state; restored via `--real`.
- **The e2e chain is now PROVEN on real C8** — a signal-watch-local candidate is elevating the launcher / chain
  workbench to showcase the real C8 party-bearing chain (vs the synthetic C4). Lower priority (showcase-polish).
- **Sibling brief edits sit dirty in the sibling trees** (aml-substrate + aml-casework) — a sibling-rooted session
  commits them; signal-watch can't drive their dev-lifecycle.
