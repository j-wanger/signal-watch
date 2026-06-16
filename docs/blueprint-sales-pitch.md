# Blueprint Sales Pitch — v2 (post adversarial review)

> Revised 2026-06-16 after a four-angle adversarial critique (signal-scale governance, regulatory
> scoping, buyer objections, technical feasibility). v1 overclaimed maturity ("built, not slideware"),
> asserted "sustainable" without arithmetic, overreached on E-23 and Project Protect, and left the
> signal-count objection unaddressed. This version fixes all four and makes the program's honesty
> *offensive*, not defensive. Backed by `docs/governance-throughput-model.md`. Honest-attribution
> caveats (vendor-sourced stats flagged; Cullen vs. Maloney figures separated) hold.

## The thesis (the spine)

AML programs decay because their failures are *architectural*, not operational — which is exactly why
budget and headcount never fix them. The blueprint replaces the decaying rules estate with an
architecture whose first principle, *universal grounding*, makes every detection and every dismissal
examinable by construction. That is precisely the standard — defensibility, then effectiveness — that
FATF, OSFI E-23, and live FINTRAC enforcement are all converging on. We are not selling a cheaper way
to do the same noisy thing; we are selling the architecture that makes the **TD outcome structurally
unreachable** (you can prove what you monitor) and the **E-23 finding structurally unreachable** (you
can defend every decision).

## The business case in one number

This is not a cost-takeout pitch; it is a **risk-adjusted-value** pitch. The fundable number is
**expected-loss-avoided**. TD paid ~US$3.09B — and the fine is the *small* part: the consent order
brought an asset cap, product-approval restrictions, a multi-year DOJ monitor + four-year FinCEN
monitorship, a lookback/remediation program, and the Fed *relocating AML functions to the U.S.* The
operational and strategic cost dwarfs the penalty. RBC ($7.475M) and CIBC ($1.33M) prove FINTRAC now
prices the same failures into the Canadian Big Six. Defensibility-by-construction is the control that
takes that tail risk off the board's table — that is the value that funds the transformation, and it is
denominated in fines-and-monitorships avoided, not reviewer-hours saved.

## The opening move: coverage first, then the economics

Open with the question TD couldn't answer, then connect it to the board's exposure:

1. **"Can you prove what you are *not* monitoring?"** — TD couldn't (92% / $18.3T unmonitored). The
   blueprint makes coverage **honest union arithmetic over named grounds** (§13 "coverage illusion":
   count is not coverage); the dangerous miss — the typology in no advisory and no history — is *named*.
2. **"Can you defend the logic of every alert — fired *and dismissed* — to an examiner?"** — under
   E-23 a program that can't is a *control deficiency, not a resourcing problem.* The answer is the
   **audit walk down the grounding chain** (§2): from any output, an examiner reaches the regulatory
   text, the policy, and the data, in finitely many *replayable* hops.
3. **"What is that gap worth?"** — the second beat is the economics above, not cost. Coverage risk is
   the opener *because it is fine-risk*; efficiency is the closer. Leading with cost is the "flat cost
   paradigm" that *caused* TD's failure.

## The core argument: structural disease → architectural cure

| Documented failure mode (regulator-sourced) | The mechanism that structurally prevents it |
|---|---|
| Scenario sprawl + change paralysis (TD static 2014–22) | Library-not-monolith (§13): each signal individually grounded, replayable, own lifecycle; retiring one is governed, not feared |
| False-positive overload / queue saturation (90–95%; HSBC 17k backlog) | Composition before escalation (§13 volume inversion) + the volume knob never points at a human (§5): humans see composed dossiers, not raw threshold-trips |
| Coverage gaps — "can't see" (TD $18.3T; HSBC $670B) | Honest coverage arithmetic over named grounds (§13); what you don't monitor is enumerated |
| Staleness / drift (TD's outdated high-risk list) | Agentic ingestion (§11: advisory→signal in days) + agentic refresh/decommission with sampled oversight (§13 drift-at-scale) |
| Data fragmentation / lineage (Danske's separate platform) | Grounding chains + reference-by-path lineage (§2): an alert cites its signal AND the data records; replayable. E-23 3.2 made structural, not documentary |
| Governance / can't explain the model (E-23/SR 11-7 target) | The G/M/J/A gate taxonomy (§4) + the SR 11-7 × E-23 control map (§7): every fired AND dismissed decision carries graded disposition + rationale as lifecycle evidence |
| Defensive, low-value reporting + wrong threshold (Cullen; RBC RGB-vs-RGS) | Graded non-binary disposition with rationale → precedent (§4-J) + consensus-never-truth (§4-M): "defend the call," not "file to cover yourself" |
| Bad metrics (alert-to-SAR, SAR-volume mislead both ways) | No unmeasured number (§10) + surface every scored dimension (§4-M) |
| Cost spiral / under-resourcing (TD flat-cost mandate) | Efficiency is a consequence, never a justification to weaken a gate (§1); a ratio target is refused on design grounds (§10) |

## Defensible → Effective → Sustainable (in order, §1)

- **Defensible first.** Every output survives the audit walk. An efficient program that can't be
  examined is a finding, not a program. *This is the half we have proven* (see "What's proven").
- **Effective second.** Detection stays current because ingestion is agentic; human attention
  concentrates on composed dossiers, not raw-alert triage. Effectiveness ≠ report volume — Canada's
  defensive-reporting pathology proves volume can *signal dysfunction*.
- **Sustainable third — and we model it, we don't assert it.** Decay is the failure of *static*
  estates. A per-signal-lifecycle library is *non-static by design*, but that only helps if the
  governance of thousands of signals is itself bounded. **We have done the arithmetic**
  (`governance-throughput-model.md`): steady-state human governance is **bounded and roughly linear in
  the signal count** (≈ team-scale, not an army), because the gate taxonomy partitions per-signal work
  into an *automatable bulk* (Class-G grounding/replay, machine cadence) and a *small human residue*
  (M/J/A) that tiering bounds. We also name the three parameters the result rests on, and what we'd
  measure to prove them (next section). That is the §10 discipline — no unmeasured claim — applied to
  our own headline.

## The 10,000-models question (pre-empted head-on)

A sophisticated buyer's first objection: *"You want me to run ten thousand 'models,' each through an
E-23 lifecycle — that's a validation army my model-risk function will never get headcount for."* It is
the right question. Our answer, on its own terms:

- **You don't validate 10⁴ models by hand — the gate taxonomy is the cost model.** Class-G evidence
  (grounding, referential replay) runs **by machine on every signal on every change** — far exceeding
  any human review cadence. Only the M/J/A residue is human-paced.
- **You tier, as your MRM function already does.** Per SR 11-7 / E-23 risk rating, most signals are
  low-materiality commodity signals (automated G + batch attestation); a small high-materiality tier
  gets full independent validation. The throughput model puts steady-state cost at **~2 FTE/yr at 5,000
  signals, ~4–5 at 10,000** — bounded and linear, dominated by the high-tier fraction.
- **The honest boundary, owned.** Signal-library-scale governance has **no documented prior art** — we
  are the first to name it. The result is *conditional* on three measurable parameters: the high-tier
  fraction stays low *and is regulator-defensible*; automatable grounding evidence genuinely discharges
  the bulk of per-signal validation (which requires our planned C/D-correctness sampling control); and
  the re-validation stream is largely agentic-with-sampling. **We tell you these are conditions, not
  certainties, because a vendor who hides them is selling you the next TD finding.**
- **Compared to what?** A rules estate's governance cost only *looks* lower because the work isn't
  being done — that *is* the decay (TD's static-since-2014 estate). Our cost is **visible and bounded**;
  theirs is **hidden and unbounded.** Visible-and-bounded is the sustainable one.

## How this lands in a real bank

- **Migration is parallel-run, not rip-and-replace.** The legacy rule estate *decomposes into* the
  governed library (§12): each legacy rule's logic + thresholds extract into the signal model, every
  rule lands in the coverage map (an honest picture of what the legacy program covered and never did),
  and the alert *history* replays as the A/B baseline (§6). You run parallel, reconcile alert-for-alert,
  and prove to your regulator no coverage dropped at cutover.
- **No silent failure.** Every agentic component has a deterministic fallback or an honest outage state
  (§9) — never a silent quality cliff. When the agentic layer is unsure, it drops *honestly* (named
  reason, visible count); a dropped item is examinable, not invisible.
- **Build-vs-buy — the moat no incumbent can retrofit.** A vendor black-box fails the audit walk *by
  construction*: you cannot ground a closed-model alert to regulatory text, so under E-23 its opacity
  is an *unmitigable* model risk you inherit. Defensibility-by-construction is the one thing a
  proven-but-opaque incumbent cannot bolt on after the fact.

## Why stakeholders should believe it (revised)

1. **The honesty discipline is the credibility proof — and the offensive weapon.** The program refuses
   to fabricate a precision or lift number (it *deleted* its own fake-lift template), labels every
   output illustrative, and reports its own negative findings (its synthetic substrate honestly
   measured that its test laundering is too easy to detect and that composition needs a generator
   redesign before it earns its keep — we publish our nulls). The offensive edge: **any precision/ROI
   number a competitor shows is uncalibrated against the ground truth AML does not have — so it dies in
   *your* model-risk validation.** We sell the only thing that survives your validation, and we prove
   we won't overclaim by showing you we don't overclaim to *ourselves*.
2. **The hard part is proven; the pillars are de-risked engineering, not a research bet.** The
   grounding mechanism is *replayable today*: 2,251 grounded indicators, 56 derived signals across 5
   regulatory sources, every quote gate-checked against its source, deterministically re-runnable by
   you. The two pillars a buyer actually operates — monitoring and the case→SAR chain — are **designed
   to that proven standard and being built against it**, not invented. We will build them *on your
   data, gated the same way.* (We do not claim them as deployed; claiming what isn't built is the
   overclaim our whole thesis forbids.)
3. **It automates the intelligence-led encoding step that Project-Protect-style detection depends on.**
   FINTRAC champions intelligence-led detection — Operational-Alert typology indicators encoded as
   detection logic. Today that encoding is manual; our corpus-derivation pipeline automates and
   *gate-verifies* it. (We do not claim to *be* Project Protect — that is a public-private partnership,
   not an architecture — nor do we borrow its 750% outcome; we claim the narrower, true thing: we make
   intelligence-led detection fast *and examinable.*)
4. **It satisfies the half of E-23 it claims, and names the half it doesn't.** The audit walk delivers
   E-23's lineage/provenance standard (Principle 3.2) structurally and supplies the conceptual-soundness
   half of validation (3.4). Outcome-validation, ongoing monitoring, and decommissioning are **designed
   seams with named owners** (§8), not delivered controls — we say so the way the blueprint does, rather
   than claiming "the audit walk is the whole of E-23." The 2027 effective date is a dateable urgency
   hook a tuning project can't match.
5. **The honest boundary is the final credibility move.** AML has no ground truth; prevented crime is
   invisible. We sell **defensibility-by-construction and effectiveness-readiness**, and we name exactly
   what is deferred-with-owner — because a pitch that names its own limits is the only kind a CAMLO who
   has read the TD consent order will trust, and the limits we name are the ones a regulator will ask
   about anyway.

## What we do not claim yet (named, owned, with a measurement plan)

Stating these is the point — each is a deferred-with-owner item with a defined way to close it:
- **Production effectiveness against outcomes** — deferred (no ground truth). Closed by the §14
  elicited-judgment loop + §12 below-the-line history replay as leading indicators a board can govern by.
- **Sustainability at 10⁴ signals** — modeled, not measured (`governance-throughput-model.md`). Closed
  by measuring the tier distribution, the agentic-derivation error rate, and the drift-driven
  re-validation rate on a built library.
- **C/D-tag correctness** — currently measured by inter-rater consensus (reproducibility), not
  correctness. Closed by an adjudication-against-authority sampling control with a measured error rate.
- **Composition lift** — the composition layer is the design's hardest open problem; on synthetic data
  it isn't yet needed (the substrate's laundering is single-feature-separable). Closed by the substrate
  generator redesign (multivariate-subtle laundering) + a measured case where the composed library
  beats both the single best signal and a legacy-rule baseline.

## The close

Anchor urgency in TD (the catastrophic ceiling + board/personal stakes), RBC/CIBC (FINTRAC pricing the
same failures into the Big Six *now*), and the E-23 2027 clock (transform on a date). The closing line:
the fine is the symptom; the architecture is the disease — and we sell the cure, with receipts you can
replay yourself, and an honest list of what we have not yet proven so that the things we *do* claim
survive your own examiner.
