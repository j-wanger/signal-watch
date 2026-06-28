# PLAN-BRIEF — aml-substrate: a discriminating exposure signal (the C17 determination-leg frontier)

> **A signal-watch → aml-substrate handoff brief** (the Phase-55–79 pattern: signal-watch authors the contract;
> the sibling implements + measures it on its own lifecycle — *no code lands in substrate from here*). Synthetic /
> illustrative; **no rate, score, or multiplier is claimed.** **Pinned to verified substrate HEAD
> `f7fbdb0` (Phase 37), code-verified + MEASURED 2026-06-28.** Companion to
> [`cross-pillar-build-order.md`](cross-pillar-build-order.md) and the Phase-36 exposure detector.

## The finding (Phase 81 T1b measure-first gate — DEGENERATE for a determination advance)

signal-watch Phase 81 consumed substrate Phase 36's **exposure-via-ownership** detector (capability **C17**: a
customer whose beneficial owner carries a `sanctions_flag`). It shipped as a **screening OBSERVABLE** — the gate
measured it DEGENERATE as a §12 **determination** advance.

Measured on the `f7fbdb0` `--clients 12000 --months 3 --seed 0 --anchored --emit-screening --emit-eval-oracles` emit:

- **13 customers carry a sanctioned beneficial owner.** ALL 13 are oracle-**clear** (zero overlap with the 38
  oracle-`file` cases — substrate's `sanctions_flag` is **label-blind by design**, `corr(flag, illicit) ≈ 0`,
  proven, KEEP IT).
- **A hypothetical C17 determination leg moves 0 of the 13 to the determination bar.** The sanctioned-BO cohort
  carries NO money-laundering MECHANISM (placement/layering/structuring — ML-A1/ML-A2 need C2/C3/C5/C4); they fire
  only C8 (a leg) or C14 (kyc). The sufficiency bar is `mechanism + 2 independent legs` — adding a *leg* (C17) to a
  case with **zero mechanisms** can never satisfy it. (Verified with the live engine: WITH-C17 delta = 0.)
- This is structural: a label-blind exposure (corr≈0) does not co-occur with an independently-detected laundering
  mechanism more than by chance, and the chance overlap on this slice is empty.

So the honest Phase-81 consume is **observable-only**: the workbench surfaces the sanctioned-BO exposure (a
common-name false positive — the BO is NEVER a designated person) and the live engine SHOWS the case does NOT reach
the bar. A label-blind exposure does not, by itself, license a filing.

## What substrate could emit (the ask — measurement-enablement, NOT a planted correlation)

The C17 leg's honest role is **corroboration**: given a case that ALREADY carries an *independently-detected*
laundering mechanism, a sanctioned-BO exposure is a corroborating leg. To exercise that role end-to-end, substrate
would emit the data that lets the **merged "a case = a customer" view** (Phase-71/78) be measured for the overlap:

1. **Emit the MONITORING layer alongside screening for the sanctioned-BO customers** (C2/C3/C5/C15 from
   `--monitor`, merged per-customer with the C17/C8/C14 screening slice — the Phase-78 merge). Then a sanctioned-BO
   customer who *independently* carries a mechanism + another leg reaches the bar, and the C17 exposure leg
   corroborates it. **Measure the overlap honestly** — with `corr≈0` it is a CHANCE overlap (likely small or zero);
   report the count, never inflate it.
2. **DO NOT plant a `flag↔mechanism` (or `flag↔illicit`) correlation.** That is the forbidden label-blind tell —
   it would make the sanctions flag a covert detector. The C17 leg is a corroborating EXPOSURE on a case with an
   independent mechanism, never a detector of laundering. (This is the same discipline that CUT broader-C7 as
   `tell-unavoidable`.)

**The honest expectation:** even with the monitoring layer, the sanctioned-BO-with-mechanism overlap on label-blind
synthetic data is a chance event (small/zero). A genuinely *discriminating* sanctions-exposure signal would require
either a non-label-blind real-data anchor (where sanctions exposure correlates with real risk — outside substrate's
deliberately label-blind synthetic design) or accepting the leg as corroboration-only (its Phase-81 role).

## The payoff (why this is honest, not a dead end)

The Phase-81 observable beat is the *correct* shipped form for a label-blind exposure: it shows the workbench
SURFACES the exposure (the screening reality a bank lives) while the determination engine correctly REFUSES to file
on it alone (the defensibility point — a sanctions hit is not, by itself, a determination). The determination-leg
upgrade is a measurement-enablement follow-on, gated on the merged emit + an honest chance-overlap measurement —
not a correctness claim.

## Boundary + status

- **Contract-neutral:** no change to the v0.5 emission contract, the determination engine, or any signal-watch dist.
- **Consume-ready on landing:** signal-watch already computes the C17 exposure from `related_parties[].sanctions_flag`
  (observable-only this phase); a determination leg would add one profile atom + the same-OFAC-hit dedup once the
  merged emit shows a non-chance overlap to exercise it.
- **Status: NOT BUILT** (the named handoff). **Pin `f7fbdb0` (Phase 37).** Out of scope: any planted
  flag↔label/flag↔mechanism correlation (the forbidden tell); any sanctions DETECTION claim (the flag is
  label-blind by design — this is an entity-exposure realism ask, not a detection ask).
