---
title: "Phase 48: Brownfield history + LFCM — blueprint extension, triage-elicitation loop, synthetic-history probe"
aliases: [phase-48-direction, lfcm-framing, history-utilization]
category: decisions
tags: [program-design, blueprint, lfcm, history, transaction-monitoring, validation, model-risk]
parents: [phase-48-history-utilization-lfcm]
created: 2026-06-12
updated: 2026-06-12
source: plan
confidence: high
---

## Context

The user reviewed docs/program-blueprint.md (Phase 47) and surfaced two planning inputs:
(1) the blueprint is GREENFIELD — no §3 substrate row, §8 disposition, or §11 chain names the
institution's real history (TM alert history, investigation history, SAR/STR filing history);
(2) the LFCM idea — a "Large Financial Crime Model": thousands–tens of thousands of grounded
signals assisting financial-crime risk judgment for any event/entity. At the Step-9 questions the
user added a third element: a **continuous mini-triage elicitation loop** — curated scenarios
analysts work ~30 min/day, accumulating signal/risk-driven judgment stats and surfacing
inconsistencies + signal/data gaps via options like "I need more information (e.g. KYC)" —
motivated by the federated-learning caution (one bank's confirmed-event history is too thin for
statistical alignment; align to elicited judgment on underlying risk instead).

State-loader evidence: the greenfield gap is structurally real; wiki quantifies history's
leverage (70% of rule alerts re-review already-discounted behavior; FP 90–98%; alert-to-SAR ~2%);
historical SAR/case text is an established extraction substrate; SR 11-7 tiered inventory makes
a 10^4-signal monolith infeasible as a validation unit; OCC endorses alternative (incl.
expert-judgment) validation for BSA/AML.

## Decision

(assumption gate CLOSED 2026-06-12, all_accept: false — A1 [HIGH] ACCEPT WITH CONDITION,
A2–A4 accept; ledger block in assumption-ledger.md) Phase 48 = an ADDITIVE blueprint extension
(user's Q1 choice)
plus a synthetic-history probe (Q2), with LFCM's decisioning form = dossier-now / score-deferred-
with-owner (Q3):

1. **History-utilization section**: history as THREE distinct roles, each with a named
   substrate/verifier per the A1′ doctrine — (i) substrate for derivation (legacy rules,
   investigations, filings decompose via the inverted extraction boundary), (ii) baseline for
   §6 probes (legacy TM = the A/B comparator; below/above-the-line shape), (iii) outcome-feedback
   embryo (filings: biased, Class-M, consensus-never-ground-truth). §8 deferred rows
   RE-DISPOSITIONED (available-with-caveats for an adopting institution), not duplicated. New
   honesty line: "history is evidence, never ground truth."
2. **LFCM section**: a 6th §3 workload row — entity/event risk decisioning (substrate = fired
   signals + their grounding chains + entity anchors; verifier = referential replay of every
   contributing signal + the no-unmeasured-number rule; gates G+M+J); inventory stance =
   grounded signal LIBRARY + small composition layer, never one Tier-1 mega-model (the library IS
   the model inventory; LFCM stays the program-level name); named failure modes (correlated
   double-counting, volume inversion → composition-before-escalation, coverage illusion,
   monolith trap, drift at scale); §11 chain 1 re-pointed as the LFCM build-out path with
   internal history as the sixth source class.
3. **Continuous adjudication loop section** (the user's triage idea): a designed daily
   judgment-elicitation stream — stratified scenario sampling (signal-fired / below-threshold /
   synthetic-novel / random) against selection bias; graded disposition options including
   "need more information (which)" wired to the C/D coverage model as MEASURED data-gap stats;
   interleaved known-case controls + agreement monitoring against fatigue/gaming; regulatory
   framing = expert-judgment alternative validation (OCC) + E-23 Monitoring evidence; the gate
   console named as the embryo artifact. Value floor = gap discovery (works even if consensus
   never converges); calibration stats = the compounding upside, always consensus-class.
   **A1 CONDITION (binding on this section):** triage scenarios are SOURCED FROM REAL
   INSTITUTIONAL HISTORY — alerts/cases/filings replayed as mini-triage scenarios; historical
   decisioning is ground truth about DECISIONS, never about correctness; and the loop's
   discovery outputs explicitly include PROCESS INCONSISTENCIES and POLICY GAPS alongside
   signal/data gaps.
4. **Synthetic-history probe**: a small fully-SYNTHETIC legacy rulebook (md) + alert/disposition
   history; the rulebook derives through the EXISTING FROZEN gate (the md is just another
   derivation surface — zero gate changes, the Phase-46 pattern), landing legacy rules in the
   C/D coverage model; a stdlib stats script aggregates the synthetic disposition history into
   baseline/gap measurements, every number carrying its measurement definition (D5).
5. **HTML blueprint report** (D6 — USER ADDITION at plan close, 2026-06-12, post-gate pre-
   implementation): docs/blueprint-report.html, a single self-contained offline NON-ship
   artifact (booth.html precedent — no build.py target; promote only if presented beyond design
   review) covering the extended blueprint in its entirety, centerpiece inline-SVG SYSTEM-FLOW
   (six workloads + triage-loop feedback) and GROUNDING-CHAIN (audit walk, verifier per hop)
   diagrams, labeled DESIGN. The phase's single L — T5 split into T5a/T5b to hold the budget.

Alternatives rejected: re-centered blueprint v2 (cross-reference churn, bigger statement than
the evidence supports); separate docs/lfcm.md (two documents to keep coherent); design-only
without probe (history-as-substrate claim stays hand-waving); score-as-target (collides with
the no-ground-truth doctrine at maximum strength).

Reviewer refinements (Step 12, 9/10 accept, incorporated): the synthetic rulebook is authored
ADVISORY-SHAPED against existing rf_region anchors and the probe writeup states this shape
caveat (the probe demonstrates "history can be a derivation surface", not "any real rulebook
parses unchanged" — real rulebooks may need the regression-gated anchor-extension path); probe
outputs live OUTSIDE every build.py-read path (never merged into __CORPUS__); in-scope editorial
fixes for stale counts (§3 "five workloads" → six, §12 "three ship artifacts" → four);
elicited-consensus drift named as the triage loop's own Class-M failure mode; loop design
parameters (~30 min/day, strata, thresholds) labeled chosen-not-measured with an
adversarial-grep honesty check (the §10 pattern).

## Consequences

- The blueprint stops being greenfield: an adopting institution sees its existing assets named
  as substrates with verifiers, and §8's deferral honestly splits vision-lab-deferred vs
  adopter-available-with-caveats.
- LFCM gets a regulatorily survivable architecture (library + composition, per-signal lifecycle)
  and an honest decisioning claim (dossier now; score only with a designed calibration program).
- The triage loop gives the score-deferred path its named embryo WITHOUT depending on
  convergence (gap-discovery floor) — and turns §4-J precedent accumulation into a daily
  practice with measurable agreement.
- All 4 ship artifacts + dists stay byte-frozen; the probe is additive material + scripts only;
  no live-bank dependency (A2 vision-lab clock holds); all probe material synthetic
  (non-negotiable #4 generalized).
