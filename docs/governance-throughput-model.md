# Governance Throughput Model — is per-signal lifecycle governance sustainable at 10³–10⁴ signals?

> **Status: MODEL (design artifact).** Built 2026-06-16 in response to adversarial review of the
> LFCM design (`docs/program-blueprint.md` §13). It answers the sharpest objection to the
> library-not-monolith architecture: *if every signal is a model with its own E-23 lifecycle, does
> the maintenance burden become as unsustainable as the rule-sprawl it replaces?*
>
> This is a **parameterized model with stated assumptions, not a measured result.** Every load-bearing
> number is **chosen, not measured** (the §14 / §10 discipline) and labeled as such. Its value is to
> (a) replace an unmeasured "sustainable" claim with explicit arithmetic, (b) identify the load-bearing
> parameters, and (c) state precisely what must be *measured* on a built library to validate it.
> Where the model's conditions are not yet established, it says so.

## 1. The question, framed correctly

The objection is usually posed as *initial* cost ("validate 10,000 models"). That is the wrong frame.
Initial validation is a **one-time, amortizable** cost. The binding constraint is **steady-state
governance throughput**: the rate at which the governance function must re-validate, monitor, and
decommission signals *in perpetuity* as advisories are superseded, typologies drift, and new signals
arrive. This is a **queueing problem** (Little's Law): governance work arrives at rate **λ**, is
processed at rate **μ**; the system is sustainable iff **μ > λ**. When λ > μ you accumulate a backlog
of un-revalidated, silently-drifting signals — which is **program decay relocated** from
rule-sprawl-and-change-paralysis to validation-debt. So the real question is whether λ and μ can be
held in the stable regime at 10⁴ signals, and at what FTE cost.

## 2. The cost decomposition is the gate taxonomy (§4)

The key structural fact: **the G/M/J/A gate taxonomy already partitions per-signal governance work by
who does it** — which makes it the cost model.

| Gate class | Per-signal work | Who | Marginal cost at scale |
|---|---|---|---|
| **G** — deterministic verifiers (grounding, referential/lineage, schema/vocab) | Replay-verify each signal's grounding chain; re-runs on every change | **Machine** | **≈ 0** (compute only) — runs on *every* signal on *every* change, far exceeding any human review cadence |
| **M** — measured neural dimensions (C/D-tag correctness) | Blind inter-rater agreement, **sampled** | Human (sampled) | sampling-rate × adjudication-time |
| **J** — graded human judgment | Adjudicate divergences/escalations only | Human (on divergence) | divergence-rate × adjudication-time |
| **A** — mandated accountability (approval sign-off) | Non-automatable approval at design + decommission | Human (irreducible) | 1 batchable sign-off per lifecycle transition, **tier-gated** |

**The whole sustainability argument reduces to one claim:** Class G — the *bulk* of per-signal
evidence — is automatable and runs at machine cadence, so the human residue (M/J/A) is what must be
bounded. Tiering bounds it. The model below tests whether the bound holds.

## 3. The tiering rubric (the relief valve, made concrete)

Per SR 11-7 / E-23 model-risk rating, each signal is rated at design time into one of three tiers; the
rating drives validation depth, re-validation frequency, and approval authority. The tiering decision
is itself a governance act — **one act per signal, at design, batchable, re-evaluated only on material
change** — and is counted below.

| Tier | What | Validation depth | Re-val cadence | Human minutes/signal/yr (steady state) |
|---|---|---|---|---|
| **T1** (high materiality) | Drives high-volume escalation; novel/frontier typology; no peer redundancy | Full independent conceptual-soundness review + human approval | Quarterly | **480** (8 hr) |
| **T2** (medium) | Standard signal, some peer overlap | Automated G + sampled M + light approval | Annual | **60** (1 hr) |
| **T3** (low / commodity) | Well-established, redundant-with-peers, stable advisory | Automated G only + batch attestation | Biennial / on-change | **10** |

These minutes are the **non-automatable (M/J/A) residue only** — Class-G runs by machine and is not in
the human total. They are **illustrative, chosen-not-measured** (see §6 for what to measure).

## 4. The arithmetic (worked, with a parameter table)

**Reference library: N = 5,000 signals**, tier distribution **T1 5% / T2 25% / T3 70%**:

| Tier | Count | min/signal/yr | Annual hours |
|---|---|---|---|
| T1 | 250 | 480 | 2,000 |
| T2 | 1,250 | 60 | 1,250 |
| T3 | 3,500 | 10 | 583 |
| **Total** | **5,000** | — | **≈ 3,833 hr/yr** |

At ~1,800 productive hr/FTE: **≈ 2.1 FTE/yr** steady-state human governance.

| Library size N (same distribution) | Steady-state FTE/yr |
|---|---|
| 1,000 | ≈ 0.4 |
| 5,000 | ≈ 2.1 |
| 10,000 | ≈ 4.3 |

**One-time stand-up** (initial validation, amortized over the build): dominated by T1 initial
conceptual-soundness review. At 16 hr/T1 + 2 hr/T2 + 0.25 hr/T3 for N=5,000 ≈ 7,400 hr ≈ **~4
FTE-years one-time**, spread over the build period — absorbable and non-recurring.

**Verdict from the arithmetic:** the steady-state cost is **bounded and roughly linear in N**, and at
10⁴ signals lands around **4–5 FTE/yr** — a *team*, not an army, and not unbounded. **But that number
is hostage to three parameters**, examined next.

## 5. Sensitivity — the three parameters the whole claim rests on

The 4–5 FTE figure is only as good as its assumptions. The model is acutely sensitive to:

1. **The T1 fraction (the dominant lever).** At 5% T1 → 2.1 FTE (N=5k). At **20% T1 → ~6.7 FTE**; at
   40% → ~12 FTE. **Tier inflation is the failure mode.** Sustainability depends entirely on most
   signals being *defensibly* low-tier — and "defensibly" is a **regulatory-acceptance** question, not
   an internal one (a signal grounded to a current operational alert on an active typology is not
   obviously low-materiality). *If the regulator rejects aggressive tiering, the cost balloons.*
2. **T1 per-signal hours.** 8 hr/yr ongoing re-validation is defensible; **real independent validation
   of a genuinely material model can be days.** At 40 hr/T1/yr, T1 alone is ~5.5 FTE at N=5k. The model
   assumes ongoing re-validation is light because the *initial* validation is amortized — true only if
   the signal is stable.
3. **Whether Class-G evidence genuinely discharges the bulk of per-signal validation.** This is the
   critic's deepest point: *a grounding gate ≠ a correctness gate.* If a regulator demands per-signal
   *conceptual-soundness* review (E-23 Principle 3.4) that the automatable grounding evidence does NOT
   satisfy, the automatable fraction shrinks and the human residue (and FTE) grows. **This is why the
   C/D-correctness control gap (a measured error rate, not just inter-rater consensus) is load-bearing
   for the cost model, not only for defensibility.**

A fourth parameter governs the *queue* rather than the per-signal cost:

4. **The re-validation arrival rate λ vs. processing rate μ.** New signals (agentic ingestion, "days
   not quarters") + drift-triggered re-validations + advisory supersession set λ. **Faster agentic
   ingestion raises λ** — so ingestion speed, sold as a strength, *widens the queue* unless μ keeps
   pace. μ is raised cheaply by automating Class-G (every signal, every change) but the M/J/A residue
   is human-paced. **The contested lever is agentic refresh/decommission with sampled human oversight**
   (§13 fm-5): if the re-validation *stream* can be largely agentic, μ scales and the queue stays
   stable; if refresh must be human-paced, the re-validation stream dominates λ and the backlog grows.
   **This lever has no documented regulatory prior art** (the blueprint admits it) and depends on the
   production-drift substrate that §8 defers — so it is the single biggest *unproven* assumption in the
   sustainability story.

## 6. What is PROVEN vs. what must be MEASURED

**Proven / structural (survives scrutiny):**
- Class-G evidence is genuinely automatable and runs at machine cadence (demo-proven: deterministic
  replay over the committed corpus, every quote gate-checked).
- The cost is **bounded and linear** in N, not unbounded — categorically unlike a rule estate, whose
  governance cost *looks* lower only because the work isn't being done (that *is* the decay). Visible-
  and-bounded beats hidden-and-unbounded.
- Decomposition makes each unit examinable; a 10⁴-monolith is unvalidatable by construction.

**Unproven / must be measured on a built library before "sustainable" is a claim, not a model:**
1. **The real tier distribution.** The 5/25/70 split is chosen. Measure it on a built library; the T1
   fraction is the dominant cost driver.
2. **The agentic-derivation error rate** (on held-out, not calibration, advisories — *perfect-on-
   calibration = overfit*). This sets the Class-M sampling rate needed to bound accumulated C/D error,
   which feeds back into parameter 3 above.
3. **The drift-triggered re-validation rate** (advisory supersession + typology drift) — sets λ.
4. **Whether agentic refresh/decommission with sampled oversight is regulator-acceptable** — the
   contested lever; without it the re-validation stream is human-paced and the queue math tightens.
5. **The per-tier minimum validation floor a regulator accepts** — does automatable Class-G discharge
   T3/T2, or does conceptual-soundness review (3.4) reassert a human floor?

## 7. Bottom line

At **10³ signals, sustainable under any reasonable assumption** (sub-1 FTE). At **10⁴ signals,
sustainable at a team scale (~4–5 FTE/yr) IFF three conditions hold**: (1) the T1 fraction stays
low *and that tiering is regulator-defensible*; (2) automatable Class-G genuinely discharges the bulk
of per-signal validation — which requires closing the C/D-correctness control gap so "grounded" carries
real validation weight; (3) the re-validation stream is largely agentic-with-sampling — the lever with
no regulatory prior art. **The arithmetic is favorable and bounded; the risk is entirely in those three
conditions, all of which are measurable and none of which is yet measured.** That is the honest
sustainability position: not "it scales," but "here is the model, here are the three parameters it
rests on, and here is exactly what we would measure to prove it" — which is itself the discipline
(no unmeasured performance claim) that makes the rest of the program defensible.
