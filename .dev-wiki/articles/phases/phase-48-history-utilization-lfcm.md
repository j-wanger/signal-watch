---
title: "Phase 48: Brownfield history + LFCM — blueprint extension, triage-elicitation loop, synthetic-history probe"
aliases: [phase-48, history-utilization, large-financial-crime-model, lfcm, triage-elicitation-loop]
category: phases
tags: [program-design, blueprint, lfcm, history, transaction-monitoring, sar-feedback, signal-library, model-risk, judgment-elicitation]
parents: [phase-47-agentic-aml-program-design]
created: 2026-06-12
updated: 2026-06-12
source: plan
status: active
ceremony: standard
scope: ["docs/program-blueprint.md", "docs/probe-history.md", "docs/blueprint-report.html", "data/probe-history/**", "scripts/probe_history_stats.py", "specs/phase-48-*.md", "CLAUDE.md", "HANDOFF.md", ".dev-wiki/*"]
entry_criteria: "Phase 47 closed (delivered + accepted + committed f8a674e, gate flip 810b965, 2026-06-12); assumption gate closed 2026-06-12 (all_accept: false — A1 accept-with-condition, A2–A4 accept)"
exit_criteria: "(1) blueprint extended + internally coherent (history + LFCM + continuous-adjudication-loop sections, 6th §3 workload row, count fixes); (2) probe gate-green through the UNCHANGED gate + measurement-defined stats + shape-caveat writeup; (3) honesty greps green; (4) full regate green with all 4 dists byte-identical; (5) docs/blueprint-report.html — single self-contained offline, DESIGN-labeled, system-flow + grounding-chain SVG centerpieces, outside build.py"
---

# Phase 48: Brownfield history + LFCM — blueprint extension, triage-elicitation loop, synthetic-history probe

## Objective

Additive extension of `docs/program-blueprint.md` answering the user's two planning inputs (the
blueprint's greenfield gap; the LFCM idea) plus the mini-triage elicitation loop raised at the
Step-9 questions — and a fully SYNTHETIC history probe that turns the history-as-substrate claim
into a measurement instead of hand-waving:

1. **History-utilization section** — history as THREE named roles, each with substrate + verifier
   (derivation substrate via the inverted extraction boundary / §6 probe baseline — legacy TM as
   the A/B comparator / outcome-feedback embryo — filings as biased Class-M material); doctrine
   "history is evidence, never ground truth"; §8 deferred rows re-dispositioned in place
   (vision-lab-deferred vs adopter-available-with-caveats).
2. **LFCM section** — 6th §3 workload row (entity/event risk decisioning); library-not-monolith
   (the signal library IS the model inventory; LFCM = the program-level name);
   dossier-now/score-deferred-with-owner; 5 named failure modes (correlated double-counting,
   volume inversion → composition-before-escalation, coverage illusion, monolith trap, drift at
   scale); §11 chain-1 re-point; editorial fixes (§3 "five workloads"→six, §12 "three ship
   artifacts"→four).
3. **Continuous adjudication loop section** — the user's mini-triage idea under the A1 gate
   CONDITION (scenarios SOURCED FROM REAL HISTORY — alerts/cases/filings replayed; historical
   decisioning is ground truth about DECISIONS, never correctness); stratified sampling strata;
   "need more information (which)" wired to the C/D coverage model; discovery outputs incl.
   PROCESS INCONSISTENCIES + policy gaps; agreement measured first-class + interleaved controls;
   elicited-consensus drift named as the loop's own Class-M failure mode; OCC expert-judgment
   alternative-validation + E-23 Monitoring framing; gate console = the embryo; every design
   parameter labeled "chosen, not measured".
4. **Synthetic-history probe** — a fully SYNTHETIC advisory-shaped legacy rulebook through the
   EXISTING FROZEN gate (zero gate edits; shape caveat stated honestly) + a stdlib stats script
   with measurement-defined numbers; outputs OUTSIDE every build.py-read path.
5. **HTML blueprint report** (USER ADDITION at plan close) — `docs/blueprint-report.html`, a
   single self-contained offline NON-ship artifact (booth.html precedent: no build.py target)
   covering the extended blueprint in its entirety; centerpiece inline-SVG SYSTEM-FLOW (six
   workloads + triage-loop feedback) and GROUNDING-CHAIN (audit walk, verifier per hop)
   diagrams; labeled DESIGN. The phase's single L (T5 split into T5a/T5b to hold the budget).

## Scope

- `docs/program-blueprint.md` (the three new sections + 6th row + count fixes + probe citation)
- `data/probe-history/**` (NEW — synthetic rulebook md + alert/disposition history + derived record)
- `scripts/probe_history_stats.py` (NEW, stdlib-only) · `docs/probe-history.md` (NEW, shape caveat)
- `docs/blueprint-report.html` (NEW — self-contained offline, NON-ship, no build.py target)
- `specs/phase-48-brownfield-history-lfcm.md` · `CLAUDE.md` · `HANDOFF.md` (§8) · `.dev-wiki/*`

## Exit Criteria

> STATUS 2026-06-12: ALL 8 tasks [x] same-session; exit criteria 5/5 MET, reviewer-verified
> (unified reviewer 9/10 ACCEPT; stale-count MEDIUM fixed inline). READY FOR COMPLETION —
> delivery gate pending; the delivery flow commits, verifies, then flips (NOT auto-completed).

- [x] Blueprint extended + internally coherent: history + LFCM + continuous-adjudication-loop
      sections (§12–§15), 6th §3 workload row, §3/§12 count fixes
- [x] Probe gate-green through the UNCHANGED gate (zero derive_signals.py edits; 12/12 first
      shot) + measurement-defined stats (9 "definition:" metric lines) + shape-caveat writeup
- [x] Honesty greps green (doctrine line; "chosen, not measured"; no unmeasured number)
- [x] Full regate green with all 4 ship dists byte-identical (--check all 6/6 zero drift)
- [x] docs/blueprint-report.html: single self-contained offline (no external asset), DESIGN-
      labeled, full-blueprint coverage, system-flow + grounding-chain SVG centerpieces, never
      referenced by scripts/build.py (87.8KB)

## Constraints

- All 4 ship artifacts + dists BYTE-IDENTICAL (`--check all`) — prevents breaking the presented demo.
- `derive_signals.py` grounding core FROZEN, ZERO gate edits — the probe rulebook is authored
  advisory-shaped so the gate stays frozen; prevents silently widening the gate to pass a probe.
- Probe material fully SYNTHETIC + outputs outside every build.py-read path — prevents real-data
  leakage (non-negotiable #4 generalized) and prevents probe records bleeding into `__CORPUS__`.
- No unmeasured number; loop design parameters labeled "chosen, not measured"; score deferred with
  a named owner — prevents the fabricated-figure class the honesty constraints exist for.
- News pipeline + derived data + overlays FROZEN.

## Checkpoints

- After T3 (blueprint sections complete): coherence read across §2/§3/§4-J/§5/§8/§11 before any
  probe work — the blueprint is the load-bearing deliverable.
- If the synthetic rulebook fails `check_record` under the existing anchors: re-author the
  rulebook SHAPE (it is synthetic — shape is free), never touch the gate; 3 failures → surface.

## Assumptions (gate-closed 2026-06-12; ledger block in assumption-ledger.md)

- A1 [HIGH] Triage-loop value does NOT depend on consensus convergence (gap discovery = floor,
  calibration = upside, agreement itself measured). ACCEPT WITH CONDITION: scenarios sourced from
  REAL history (decisions-not-correctness ground truth); discovery outputs include process
  inconsistencies + policy gaps. If the floor fails: the loop's design center moves — surface.
- A2 [HIGH] LFCM = grounded signal LIBRARY + small composition layer; the library IS the model
  inventory; never a Tier-1 mega-model. If false: the LFCM section is wrong — stop and replan.
- A3 [MED] History = THREE roles under "history is evidence, never ground truth"; §8 rows
  re-dispositioned, not duplicated. If a role lacks a nameable substrate/verifier: surface.
- A4 [MED] Probe = synthetic advisory-shaped rulebook through the existing frozen gate + stdlib
  stats, outputs outside build.py paths. If a gate edit looks needed: surface, never extend.

## Notes

Wiki knowledge at plan: TM↔case-outcome feedback gap is a NAMED industry structural gap (70% of
rule alerts re-review already-discounted behavior, FP 90–98%, alert-to-SAR ~2%); single-institution
confirmed-event scarcity motivates judgment-elicitation over outcome-fitting; SR 11-7 tiered
inventory + OCC alternative-validation endorsement; 80% of investigative intelligence sits in
unstructured SAR/case text; FINTRAC STR quality turns on articulable suspicion. KNOWLEDGE GAPS
(T2/T3 cite as open design questions, never settled patterns): no signal-library-scale governance
article; no below-the-line testing methodology article; FIU per-filing-feedback reality
undocumented. Decision article: [[decisions/phase-48-history-lfcm-blueprint-extension]] (D1–D5).
