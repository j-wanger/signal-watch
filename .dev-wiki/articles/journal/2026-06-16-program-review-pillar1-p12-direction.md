---
title: Program review of pillar-1 (aml-substrate P7–P11) + P12 direction set
date: 2026-06-16
type: journal
phase: phase-50-aml-program-build
tags: [aml-substrate, program-review, pillar-1, p12-direction, cross-pillar, lfcm-composition]
mode: quick-debrief
---

# Program review of pillar-1 (aml-substrate P7–P11) + P12 direction set

Second cross-pillar review from the signal-watch program-architecture home (no signal-watch code
changed; the build output lands in aml-substrate). Code-verified snapshot of aml-substrate's
delivered state assessed against DESIGN.md + the program blueprint; the user then set pillar-1's
next direction and again handed planning/implementation to an aml-substrate-rooted session.

## What happened

- **The record was 5 phases stale.** This repo's lifecycle said "Phase 7 in planning, handed off."
  Reality (code-verified, working tree clean, 360 tests green, HEAD `0daa3cc`): aml-substrate ran
  **P7→P8→P9→P10→P11, all delivered + accepted**. The 2026-06-15 review predicted exactly this
  drift ("the architecture home will keep drifting because aml-substrate's dev-* run in its own
  repo") — it drifted again within a day. Re-synced this debrief (active-phase.md + _CURRENT_STATE
  Active Phase / Recommended Next Action / Contract).
- **What P7–P11 delivered (the prior brief's premises are now obsolete):** P7 — `counterparty_account_id`
  populated + mirrored credit leg; case-id leak fixed (`flows.py:219` de-cased); a positive freeze
  guard built (`scripts/check-gen-freeze.sh`, hashed manifest, pre-commit-wired) and the
  ruff-corrupts-frozen-gen hazard fixed (`exclude` on the format hook) — **the P6 negative finding
  is closed; the mule network is observable + reconstructable (recall 1.0).** P9 — realism-validated
  + baseline-locked (`measure-baseline.json`, `--validate --check/--freeze`). These + the freeze
  guard + the A1 separability gate **are §8's designed-now controls in miniature** — strong
  blueprint alignment. P10/P11 — two subtlety phases.
- **Blueprint alignment — one proven half, one structural gap.** The substrate is the grounding
  substrate for §3 rows 3–6. *Proven:* observable edges + label-blind detection + the §8 gate
  discipline. *Gap that matters:* laundering is **single-feature-separable 3/3** (`total_amount`
  ROC ≈ 0.95); P10 (diversify method) + P11 (remove cash artifact) BOTH failed to make it
  multivariate → strong evidence the memoryless-Poisson generator (`activity.py:143`; §6
  Hawkes/dormancy still SPEC-ONLY/DEFERRED) is structurally incapable of it. **This directly blocks
  the §13 LFCM north star: composition can't be demonstrated on data a single threshold solves.**
  Second-order: §6 Leg-B legit-fidelity is still 0/3 — there may be no legit high-volume cohort for
  laundering to hide among, which is *why* magnitude separates so cleanly.
- **Direction set (user): P12 = the §6 realism lever** — make laundering genuinely multivariate so
  composition becomes demonstrable, with an EXTERNAL exit bar (detection requires ≥2 composed
  grounded signals; no single feature ROC > ~0.8 alone). Chosen over (b) open Pillar 2 / transaction
  monitoring, (c) a thin chain slice first (decouple), (d) hardening/loop-closure only. The honest
  sub-fork inside it — legit-overlap cohort vs Hawkes/dormancy temporal engine — is left for the
  aml-substrate gate to resolve MEASURE-FIRST (Leg B 0/3 suggests the cohort may be the cheaper
  root-cause fix).
- **The T0 challenge surfaced + dispositioned:** the weakest assumption is that "more substrate
  subtlety" is the highest-leverage move — the real risk is 11 phases with zero downstream consumers
  (the §3 rows 3–6 chain never demonstrated on data). The user took Option 1 anyway, on the
  measured mandate (two cheaper fixes already failed; composition is undemonstrable without it) —
  composition north star over consumer-first. Pillar 2 (monitoring) is the thing P12 unblocks.
- **Handoff:** planning/implementation handed to an aml-substrate-rooted session. Pre-staged brief:
  `aml-substrate/docs/phase-12-multivariate-subtlety-PLAN-BRIEF.md` (code-verified facts, the
  external success bar, the unresolved measure-first sub-fork, five cost-sorted assumptions with
  if-false consequences).

## Soft Observations / standing items

- **The cross-pillar drift is now a confirmed recurring pattern, not a one-off.** Both reviews (06-15,
  06-16) opened by finding the architecture-home record multiple phases stale. The standing fix
  remains a periodic cross-pillar sync; the deeper question is whether signal-watch's record should
  even track aml-substrate's per-phase progress (it can't drive it) or only the pillar-level
  direction + the cross-pillar findings. Candidate: demote the per-phase facts here to a single
  "aml-substrate is at P<n>; see its repo" pointer + keep only direction/findings.
- The P7 brief (`docs/phase-7-observable-network-PLAN-BRIEF.md`) in aml-substrate is consumed +
  superseded; can be removed there.
- Parked aml-substrate optimizations (carry to a future plan): CDD AccountView exposure (verified
  non-label), persist LCTR/EFTR/STR + verify, and aml-substrate's OWN `_CURRENT_STATE.md` prose-lag
  (reads "awaiting Gate 2 / 0%" though all authoritative signals say P11 accepted).
- This debrief + the re-sync are uncommitted in signal-watch; the P12 brief is uncommitted in
  aml-substrate.
