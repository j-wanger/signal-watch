# Active Phase Context

**Phase 63 — *Investigator Case Workbench (capstone sales-pitch demo)*** (signal-watch-local, LITE) — direction gate closed 2026-06-21 (all_accept:true), **RE-SCOPED post-gate to option (B): feed the REAL (synthetic) substrate alert POPULATION** (over the curated-4 hybrid). A companion-served investigator case workbench extending the existing `serve_chain.py` companion (a SERVED page, NOT a build/dist target — the chain.html/Phase-56 precedent).

## Objective

Walk a bank stakeholder through THREE beats over a REAL (synthetic) substrate alert POPULATION — a deterministic BOUNDED SLICE (~100–300 cases) vendored from aml-substrate@f90bd39 as TOOL-USE (file-contract; verified feasible this session — the contract v0.2 PartyView emits the rich label-leak-proof investigator clutter at population scale, NO precursor phase needed). **Beat 1 (clutter)** — a QUEUE of the real population + a per-case dense investigator page (real PartyView KYC: risk_rating/cdd_level/pep_tier/sanctions+adverse-media/occupation/source_of_funds+wealth/nationality/residency/NAICS/expected_monthly_volume+count; cross-account aggregation over subject.account_ids; txn summaries/details; REAL counterparty edges), offline/model-free; a clearly-SYNTHETIC display identity laid over the real KYC (substrate omits name/DOB by privacy design). **Beat 2 (signals on)** — a presenter toggle overlays the case's GROUNDED signals + composes the risk picture (grounding/clarity/corroboration; ZERO catch-rate/precision number — the detection-lift triple-null governs). **Beat 3 (live finale)** — the "decide" action wires the EXISTING serve_chain → casework consume on a SELECTED real case, default Claude (configurable openai/opencode/stub), stub fallback, NDJSON stage reveal; plus an HONEST COVERAGE STATISTIC ("N of M cases ground end-to-end now; the rest is the visible frontier", REAL/measured). The 4 named exemplars (textbook mule / false-positive trap / thin single-signal / ambiguous-medium) are tagged WITHIN the real population. Each case shows an illustrative precedent-confidence badge (anchored to REAL probe-history firing frequency; DISPOSITIONS stay label-blind illustrative — the Phase-62 split). DEFERRED to follow-ons: agentic tool-calling (OSINT/counterparty/network-ER), the precedent-confidence GATING engine, the substrate ownership-graph emission.

## Scope

`workbench.html` · `scripts/serve_chain.py` · `scripts/curate_workbench_cases.py` · `data/workbench/**` · `tests/workbench.test.mjs` · `docs/case-workbench.md` · `tests/smoke-checklist.md` · `.claude/rules/active-phase.md` · `HANDOFF.md` · `CLAUDE.md`. Cross-pillar consume: aml-substrate@f90bd39 emit (TOOL-USE, file-contract, NO import).

## Key constraints

- **Companion-served, off by default, scripted fallback** — a serve_chain-served page, NOT a 9th build target (Phase-49 new-ship→standard does NOT fire). NO keys in the frontend (creds server-side, browser sends a backend NAME only — Phase-57 §4.5).
- **NO catch-rate / detection-lift / precision number on the clarity beat** — clutter→clarity = grounding/defensibility/corroboration (combo-strength = richer converging defensible evidence), never a higher catch rate. The always-on "Illustrative data & outputs" badge stays.
- **REAL (synthetic) substrate population, nothing real leaves.** A deterministic bounded slice (~100–300 cases) vendored from aml-substrate@f90bd39, pinned, `meta.synthetic:true`. 3 emission gaps handled in signal-watch (NOT a substrate change): synthetic display identity over real KYC; cross-account display aggregation; the txn-edge network. REAL txn counterparty edges only (ownership-graph emission deferred).
- **build.py NEVER imports aml_substrate / aml_casework** — subprocess + file-contract only (the Phase-62 probe-history pattern); `--check all` stays 8/8 with ZERO dist drift (companion-only).
- **Coverage statistic is REAL/measured; confidence is DISPLAY-ONLY** — precedent-confidence anchored to real firing frequency but dispositions label-blind illustrative ("chosen, not measured"); the auto-gating engine is deferred.
- **Live finale = wiring + checkpoint** — wire the existing Phase-57 Claude backend, run it live ONCE early (T4); real debugging beyond creds is a SURFACED FINDING, not silently absorbed.

## Exit criteria

Companion workbench renders the real-population queue + per-case cluttered view + the signals-on reveal over the vendored slice; the 4 exemplars are tagged; each case shows an illustrative confidence badge; an honest coverage statistic is computed/displayed; the live finale runs serve_chain → casework consume on a selected real case (default Claude, stub fallback) with the Phase-57-backend checkpoint resolved; `node tests/workbench.test.mjs` green (full arc, both motion modes, XSS-escape); `build.py --check all` 8/8 with ZERO dist drift; build.py imports NO sibling; the vendored slice is deterministic + pinned aml-substrate@f90bd39 + `meta.synthetic`; `docs/case-workbench.md` written.

## Abort

Any dist drifts / build.py imports a sibling → STOP-and-surface. The substrate emit isn't as rich/deterministic as verified → STOP at the T1 emit-checkpoint, fall back to a bounded curated set (do NOT hand-fabricate at population scale). The Phase-57 live backend needs real debugging beyond creds → surface as a finding. A key/token reaches the browser → out of bounds.

## Gates

- [x] spec (LITE ceremony — spec step skipped by design; the dev-debrief self-check is the quality gate)
- [x] Direction confirmed by user (assumption positions taken 2026-06-21; all_accept:true — then RE-SCOPED post-gate to option B: A0 flipped → substrate-grounded real population VERIFIED feasible @f90bd39 [NO precursor phase]; A1' real txn edges only; A2' bounded vendored slice ~100–300; A3' coverage REAL / dispositions illustrative)
- [ ] Delivery accepted

Plan [[phases/phase-63-investigator-case-workbench]]; ledger Phase-63.
