---
title: "Phase 63: Investigator Case Workbench (capstone sales-pitch demo)"
aliases: [case workbench, clutter-to-clarity demo, investigator workbench]
category: phases
tags: [m9, demo, capstone, sales-pitch, workbench, live-finale]
parents: []
created: 2026-06-21
updated: 2026-06-21
source: plan
status: active
scope:
  - "workbench.html"
  - "scripts/serve_chain.py"
  - "scripts/curate_workbench_cases.py"
  - "data/workbench/**"
  - "tests/workbench.test.mjs"
  - "docs/case-workbench.md"
  - "tests/smoke-checklist.md"
  - "scripts/build.py (NO substrate/casework import — companion-only, no build target)"
entry_criteria: "Phase 62 delivered + accepted; the chain workbench (chain.html + serve_chain.py, companion-only, NOT a build target) is the live finale to wire; aml-substrate@f90bd39 emits the rich v0.2-PartyView investigator clutter at population scale (VERIFIED this session — NO precursor phase needed); a deterministic bounded slice (~100-300 cases) is vendored as TOOL-USE (file-contract, no import)."
exit_criteria: "A presenter-driven companion workbench over a REAL (synthetic) substrate alert POPULATION: real-population queue → per-case cluttered investigator view → signals-on reveal → live decisioning over a vendored bounded slice (~100-300 cases, pinned aml-substrate@f90bd39, meta.synthetic), the 4 named exemplars tagged within the population, each with an illustrative precedent-confidence badge, an honest REAL coverage statistic computed/displayed; companion-served (serve_chain) with a deterministic-stub offline fallback; the live finale runs the existing serve_chain → casework consume on a selected real case (default Claude, stub fallback) with the Phase-57-backend checkpoint resolved; workbench.test.mjs green (full arc, both motion modes, XSS); --check all 8/8 with ZERO dist drift (companion-only, no new build target); no substrate/casework import in build.py; docs/case-workbench.md written."
---

# Phase 63: Investigator Case Workbench (capstone sales-pitch demo)

> **RE-SCOPED 2026-06-21 (post direction-gate).** The gate originally closed all-accept on a
> CURATED-4 / local-synthetic / self-contained set. The user then chose option **(B): feed the REAL
> (synthetic) substrate alert POPULATION.** This was VERIFIED feasible this session —
> aml-substrate@f90bd39 ALREADY emits the rich investigator clutter (contract v0.2 PartyView:
> risk_rating / cdd_level / pep_tier / sanctions+adverse-media flags / occupation / source_of_funds /
> source_of_wealth / nationality / residency / NAICS / expected_monthly_volume+count, label-leak-proof)
> at POPULATION scale (`--emergence --monitor --emit-evidence --emit-screening`, ~500–2,000
> deterministic synthetic bundles per 50k-client run) → **NO substrate precursor phase is needed.**
> Two build parameters chosen: a BOUNDED slice (~100–300 cases), and REAL txn counterparty edges only
> (the formal ownership/beneficial-owner graph is a substrate follow-on). The revised objective +
> decisions below are the durable description; the original curated-4 shape is superseded.

## Objective

A COMPANION-SERVED presenter demo (extending the existing `serve_chain.py` companion — a SERVED page,
NOT a build/dist target; the chain.html / Phase-56 precedent) over a REAL (synthetic) substrate alert
POPULATION, walking a bank stakeholder through clutter → clarity → live decisioning. The substrate emit
is run as TOOL-USE (file-contract; build.py NEVER imports aml_substrate/aml_casework — the Phase-62
probe-history-consume pattern); a deterministic BOUNDED SLICE (~100–300 cases) is vendored into
`data/workbench/` pinned to aml-substrate@f90bd39 (`meta.synthetic:true` → "no real data" holds). The 4
named exemplars (textbook mule / false-positive trap / thin single-signal / ambiguous-medium) are tagged
WITHIN the real population. An HONEST COVERAGE STATISTIC ("N of M cases ground end-to-end now; the rest
is the visible frontier") is computed over the slice — REAL/measured. The agentic tool-calling, the
precedent-confidence-GATING engine, and the substrate ownership-graph emission are sequenced as
FOLLOW-ON phases.

**Decisions (direction gate 2026-06-21 all_accept:true, RE-SCOPED post-gate to option B):**
1. **(B) substrate-grounded real population (A0 flipped):** over the curated-4 hybrid; VERIFIED
   feasible @f90bd39 this session → NO precursor phase. The vendored slice is the demo's clutter source.
2. **Bounded vendored slice ~100–300 cases (A2'):** the 4 named shapes are exemplars TAGGED within the
   real population (not hand-authored variants).
3. **Real txn counterparty edges only for the network view (A1'):** the formal ownership/beneficial-
   owner graph emission is deferred to a substrate follow-on.
4. **3 emission gaps handled in signal-watch (NOT a substrate change):** a clearly-SYNTHETIC display
   identity over the real KYC (substrate omits name/DOB by privacy design); cross-account display
   aggregation over `subject.account_ids`; the txn-edge network.
5. **Coverage statistic REAL/measured; precedent-confidence anchored to real firing frequency, but
   DISPOSITIONS label-blind illustrative (A3', the Phase-62 grounded-detection / illustrative-disposition
   split).**
6. **Companion-only / LITE holds (A3):** a serve_chain-served page, NOT a 9th build target; the Phase-49
   new-ship→standard precedent does NOT fire. Live finale = wiring + checkpoint (wire the existing
   Phase-57 Claude backend; run it live once early; real debugging beyond creds is a SURFACED finding).
   Honest value framing: clutter→clarity = grounding/defensibility/corroboration, NOT a higher catch
   rate (the substrate detection-lift triple-null; combo-strength = richer converging evidence).

## The three beats (over the REAL substrate population; Phase 63 = beats 1+2 + wiring beat 3)

- **Beat 1 — clutter.** A QUEUE of the real population + a per-case dense investigator page: the real
  PartyView KYC profile (risk_rating / cdd_level / pep_tier / sanctions+adverse-media / occupation /
  source_of_funds+wealth / nationality / residency / NAICS / expected_monthly_volume+count) +
  cross-account aggregation over `subject.account_ids` + txn summaries/details + REAL counterparty
  edges — the information-overload pain, over REAL (synthetic) substrate data, offline/model-free. A
  clearly-SYNTHETIC display identity is laid over the real grounded KYC (the substrate omits name/DOB
  by privacy design).
- **Beat 2 — clarity.** "Turn on signals" reveal: risk-grounded signals surface relevant activity
  + compose a risk picture (clutter→clarity). Value = grounding / clarity / defensibility /
  corroboration, NOT a higher catch rate (detection-lift is a MEASURED triple-null — composition is
  never required to detect laundering on synthetic data; see [[composition-detection-lift-retired]]).
- **Beat 3 — live decisioning + narrative + coverage statistic.** The "decide" action wires the
  EXISTING serve_chain → casework consume on a SELECTED real case; real backends (default Claude SDK,
  configurable openai / opencode / stub; stub fallback; NDJSON stage reveal). Plus an HONEST COVERAGE
  STATISTIC ("N of M cases ground end-to-end now; the rest is the visible frontier", REAL/measured over
  the slice). Each case carries an ILLUSTRATIVE precedent-confidence badge anchored to REAL probe-history
  firing frequency (the 4,966-firing history), but DISPOSITIONS stay label-blind illustrative (the
  Phase-62 split); larger precedent sample → higher confidence → fewer human gates [the gating mechanism
  itself is a follow-on; Phase 63 displays the level only].

## Scope

Files and modules affected (companion-only — NOT a build target; artifact-shape RESOLVED at the gate):
- `workbench.html` — the new companion-served workbench template (dossier theme; the dense beat-1
  clutter view + the beat-2 signals-on reveal + the beat-3 live-finale wiring), NOT a build target
- `scripts/serve_chain.py` (the localhost companion: a new workbench route serving cases + the page;
  NDJSON stage stream, subprocess to casework consume, N-backend drafter pass-through — Phase-57 spine)
- `scripts/curate_workbench_cases.py` (NEW — deterministic curate validating the vendored real slice
  + emitting committed `data/workbench/cases.json`; tags the 4 exemplars, computes the illustrative
  precedent-confidence badge + the REAL coverage statistic, lays a synthetic display identity over the
  real KYC; the Phase-62 tool-use / file-contract pattern)
- `data/workbench/**` (the VENDORED real (synthetic) substrate population slice: a deterministic
  bounded slice ~100–300 cases pinned to aml-substrate@f90bd39, `meta.synthetic:true`; each case carries
  the real PartyView KYC + cross-account aggregation over `subject.account_ids` + txn summaries/details +
  REAL counterparty edges; the 4 named exemplars tagged within the population; each badged with an
  illustrative precedent-confidence value)
- `tests/workbench.test.mjs` (NEW — the workbench arc test, the chain.test.mjs pattern)
- `docs/case-workbench.md` (NEW — companion walkthrough + honesty framing + the deferred follow-ons)
- `tests/smoke-checklist.md` (a workbench presenter entry)
- `scripts/build.py` (NEVER imports substrate/casework — file-contract/vendored-pin only; NO build target)

## Exit Criteria

- [ ] T1: a deterministic bounded slice (~100–300 cases) vendored from aml-substrate@f90bd39 (pinned,
      `meta.synthetic`) into `data/workbench/`; the curate `--selftest` green; the 4 exemplars tagged +
      the REAL coverage statistic computed
- [ ] Beat 1: a QUEUE of the real population + a per-case cluttered investigator view (real PartyView
      KYC + cross-account aggregation + txn summaries/details + real counterparty edges) renders
- [ ] Beat 2: a signals-on reveal surfaces the grounded signals + composes a risk picture, honest
      framing (clutter→clarity, NO catch-rate/lift claim; always-on "Illustrative data & outputs" badge)
- [ ] Beat 3: live decisioning on a selected real case via the existing N-backend drafter (default
      Claude, stub fallback) + the honest coverage statistic displayed; the Phase-57-backend checkpoint
      resolved
- [ ] each case shows an illustrative precedent-confidence badge (real firing frequency; dispositions
      label-blind illustrative)
- [ ] `build.py --check all` 8/8 with ZERO dist drift; no substrate/casework import in build.py
- [ ] companion-served (serve_chain pattern); the view path makes no LLM/fetch call; docs/case-workbench.md written

## Constraints

- The offline ship artifact (if a new build target) MUST run by opening one file, offline, no server;
  all live code in `/*LIVE_*/` regions, build-stripped — prevents breaking the file:// non-negotiable.
  (P63 is companion-only — NO new build target.)
- NO real customer/transaction data — the clutter source is the VENDORED REAL (synthetic) substrate
  population (`meta.synthetic:true`, pinned aml-substrate@f90bd39) — prevents the no-real-data violation.
- build.py NEVER imports aml_substrate / aml_casework — subprocess + vendored-pin file-contract only
  (the Phase-62 probe-history tool-use pattern) — prevents the one-repo-per-pillar boundary breach.
- NO catch-rate / detection-lift / precision number on the clarity beat — composition's measured value
  is assembly/grounding/defensibility, not lift — prevents resurrecting the retired triple-null claim.
- The COVERAGE statistic is REAL/measured; CONFIDENCE is precedent-derived + "chosen, not measured" /
  illustrative, with DISPOSITIONS label-blind illustrative — prevents presenting a synthetic disposition
  as a validated rate (the Phase-62 grounded-detection / illustrative-disposition split).
- 3 emission gaps handled in signal-watch (NOT a substrate change): synthetic display identity over the
  real KYC; cross-account display aggregation over `subject.account_ids`; the REAL-txn-edge network. The
  formal ownership/beneficial-owner graph emission is DEFERRED to a substrate follow-on.

## Checkpoints

- **T1 emit-checkpoint:** if the substrate emit isn't as rich/deterministic as VERIFIED this session
  (@f90bd39 v0.2 PartyView at population scale) — STOP at T1, fall back to a bounded curated set; do
  NOT hand-fabricate customer data at population scale.
- **T4 live-finale checkpoint (A0, T0 weakest):** run the live finale once early; if the Phase-57 Claude
  path needs real debugging (not just creds) → STOP-and-surface, do not silently absorb.
- If the confidence/precedent mechanism can't be derived honestly from the slice: scope it to a displayed
  illustrative level (follow-on phase does the real gating) — report, don't force.

## Assumptions (gate-resolved + RE-SCOPED to option B — see Decisions; the live finale carries the weakest, T0)

- **A0 [T0 weakest] verify-first the live finale.** Wire the existing Phase-57 `claude` backend
  (serve_chain → casework consume) + run it live ONCE early (T4 checkpoint); real debugging beyond
  creds is a SURFACED FINDING, not silently absorbed. If the Phase-57 Claude path needs real
  debugging → STOP-and-surface before expanding scope. (The case-data A0 — "verify the substrate
  emit feasible" — RESOLVED this session: aml-substrate@f90bd39 emits the rich v0.2 PartyView at
  population scale → option B chosen, NO precursor phase.)
- **A1' real txn counterparty edges only** for the network view — the formal ownership/beneficial-owner
  graph emission is deferred to a substrate follow-on. If the user wants the ownership graph in P63 →
  re-scope (out of bounds).
- **A2' bounded vendored slice ~100–300 cases** — the 4 named shapes are exemplars TAGGED within the
  real population (not hand-authored variants). Live finale = wiring + checkpoint (the EXISTING
  serve_chain `claude` backend, casework's pluggable Drafter Protocol, server-side creds — NOT a new
  direct SDK integration).
- **A3' coverage REAL / dispositions illustrative + companion-only / LITE** — the coverage statistic is
  REAL/measured; precedent-confidence is anchored to real firing frequency but DISPOSITIONS stay
  label-blind illustrative (the Phase-62 split). A serve_chain-served page, NOT a 9th build target
  (Phase-49 new-ship→standard does NOT fire). If the auto-GATING engine is wanted in P63 → re-scope.
- **Substrate-grounded real population (the option-B case data):** the clutter source is the VENDORED
  bounded slice from aml-substrate@f90bd39 (real PartyView KYC + cross-account aggregation + txn
  detail + real counterparty edges + grounded signals), TOOL-USE / file-contract — NOT hand-fabricated.
  A clearly-SYNTHETIC display identity is laid over the real KYC (substrate omits name/DOB by design).

## Notes

- **The chain workbench is the existing live finale.** `chain.html` (475 lines, companion-only, NOT a
  build target) + `scripts/serve_chain.py` (localhost:8020, NDJSON stage stream, subprocess to the
  casework consume CLI) already do: case-library select → live casework consume (stub/claude/openai/
  opencode drafter, N-backend pass-through, creds server-side §4.5) → e2e_chain_check re-verify →
  CONNECTED + flag→corpus audit walk. Beat 3 is largely WIRING this, not building it.
- **The clutter source is rich — VERIFIED at population scale (the option-B basis).** aml-substrate@f90bd39
  ALREADY emits the rich investigator clutter (contract v0.2 PartyView: risk_rating / cdd_level / pep_tier /
  sanctions+adverse-media flags / occupation / source_of_funds / source_of_wealth / nationality / residency /
  NAICS / expected_monthly_volume+count, label-leak-proof) at POPULATION scale (`--emergence --monitor
  --emit-evidence --emit-screening`, ~500–2,000 deterministic synthetic bundles per 50k-client run). So NO
  precursor phase is needed — P63 vendors a deterministic bounded slice (~100–300 cases) directly. Substrate
  omits name/DOB by privacy design → signal-watch lays a clearly-SYNTHETIC display identity over the real KYC.
  Real txn counterparty edges only (the formal ownership/beneficial-owner graph is a substrate follow-on).
- **Existing pitch asset:** `docs/blueprint-sales-pitch.md` is the program sales narrative; align beats.
- **Honesty posture (load-bearing across the program):** composition detection-lift is RETIRED
  (substrate measured a triple-null); the value is assembly/redundancy/grounding/defensibility. The
  always-on "Illustrative data & outputs" badge stays. Confidence is illustrative/precedent-derived.
- **Wiki knowledge folded in:** SAR narrative gen is a high-cost manual bottleneck (25–315 min/SAR;
  AI ~70% time reduction) — human-in-the-loop review is mandatory; automated SAR systems are SR-11-7
  models (`ai-automated-sar-generation`, `suspicious-activity-reporting`). The clutter→clarity pain is
  the ~98%-false-positive / alert-fatigue problem; the value pivot is "volume → crystallized risk"
  with adjudication-feedback loops (`false-positive-management-in-transaction-monitoring`). Precedent
  confidence echoes dynamic customer-risk-scoring (past alert history + behavioral params;
  `customer-risk-scoring`). Tiered DD (Low/Med/High → fewer/more gates) is the analog for
  confidence→fewer-human-gates.
- **Follow-on phases (sequenced OUT of 63):** (a) agentic tool-calls during investigation/narrative
  composition (OSINT / counterparty gathering / network-ER verification) — tool-gathered evidence
  extends the grounding chain; (b) precedent-confidence-GATING (the real mechanism, not just display);
  (c) the substrate ownership/beneficial-owner graph emission (a richer network view than the P63
  real-txn-edge graph) — a substrate-rooted follow-on.
