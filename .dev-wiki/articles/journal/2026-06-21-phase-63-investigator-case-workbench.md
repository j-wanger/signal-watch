---
title: "Phase 63 — Investigator Case Workbench (capstone sales-pitch demo) (lite, planned 2026-06-21, re-scoped to option B, delivered 2026-06-21)"
aliases: []
category: journal
tags: [m9, demo, capstone, sales-pitch, workbench, live-finale, fail-closed, cross-pillar, substrate-population, pytest-wrapper]
parents: [phase-63-investigator-case-workbench]
created: 2026-06-21
updated: 2026-06-21
source: debrief
duration: ~1 session
---

# Phase 63 — Investigator Case Workbench (capstone sales-pitch demo)

## What Happened

- Built the capstone sales-pitch demo: a COMPANION-SERVED investigator case workbench that walks a bank
  stakeholder through clutter → clarity → live decisioning over a REAL (synthetic) aml-substrate alert
  POPULATION. All 5 tasks (T1–T5) landed; exit criteria met → READY FOR COMPLETION (this is the delivery gate).
- **Post-gate RE-SCOPE to option (B) — USER OVERRIDE.** The direction gate had closed all-accept on a
  CURATED-4 / local-synthetic / self-contained set; the user reviewed the built artifact and re-scoped to
  feed the REAL substrate population. **A0 FLIPPED → VERIFIED feasible:** aml-substrate@f90bd39's contract-v0.2
  PartyView already emits the rich investigator clutter (risk_rating / cdd_level / pep_tier / sanctions+
  adverse-media / occupation / source_of_funds+wealth / nationality / residency / NAICS / expected volumes,
  label-leak-proof) at population scale → NO precursor phase needed. Recorded in the ledger as the A0 flip →
  verified-revised-accept (all_accept now false).
- **The clutter source is REAL/measured.** Ran the substrate emit as TOOL-USE (file-contract; build.py NEVER
  imports the siblings — the Phase-62 pattern), vendored a deterministic bounded slice of **200 cases** into
  `data/workbench/` (pinned aml-substrate@f90bd39, `meta.synthetic:true`). The 4 named exemplars (textbook
  mule CASE-P-0002174 / false-positive trap CASE-P-0018660 / thin single-signal CASE-P-0008468 / ambiguous-
  medium CASE-O-000008) are tagged WITHIN the real population, not hand-authored variants. A clearly-synthetic
  display identity is laid over the real KYC (substrate omits name/DOB by privacy design).
- **The T4 cross-pillar finding → FAIL-CLOSED as the demo's defensibility climax.** Coverage is MEASURED, not a
  capability-membership proxy: curate runs aml-casework's stub over all 200 vendored bundles and records
  grounds_e2e per case. Only **57/200 sign end-to-end** — composed cases (≥2 capabilities) fail on a real
  substrate↔casework **C3/C15 replay divergence** (casework's independent re-derivation can't reproduce the
  cited C3/C15 from the evidence). Rather than loosen the verifier, the demo EMBRACES the refusal: deciding a
  composed mule shows the gate refusing → escalate-to-human, never loosening. The user accepted this framing
  as the defensibility climax. **The verifier was never loosened (abort rule held).**
- **Precedent-confidence funnel, anchored to REAL firing frequency.** Each case carries a precedent-confidence
  badge keyed to its fired-signal-combo frequency over the emitted population (REAL): common combo (e.g. C2+C3,
  16,856 precedents) = large precedent → auto-clear; rare composition = small precedent → human-gate. Gate
  funnel: **129 auto-clear / 52 review / 19 human-gate.** The DISPOSITION direction stays ILLUSTRATIVE (the
  Phase-62 grounded-detection / illustrative-disposition split — "chosen, not measured").
- **Mid-phase USER OVERRIDE — a thin PYTEST WRAPPER (not full py-init).** The user asked for proper Python
  tooling. Resolved as a thin wrapper, NOT a src/+pytest+packaging restructure (signal-watch ships HTML — no
  Python ships — so the restructure is the wrong fit): `pyproject.toml` ([tool.uv] package=false; pytest as a
  dev dep) + `tests/test_selftests.py` that shells out to each `scripts/*.py --selftest` + `node tests/*.test.mjs`.
  Now `uv run pytest` runs the whole suite (17 parametrized cases — 11 python selftests + 6 .mjs), giving parity
  with the sibling pillars while the dep-free paths stay the source of truth. pytest is dev-only (gitignored .venv);
  no new runtime deps.

## Problems Solved

- **The curated-4 hybrid was thinner than the real thing** — re-scoped to the substrate population (option B);
  verified @f90bd39 emits the rich clutter at scale → no precursor phase, no hand-fabrication.
- **The composed-case grounding gap (the T4 finding)** — only ~28% of composed cases sign (the C3/C15 fan-in
  vs fan-out divergence). Instead of papering over it by loosening the gate, turned the refusal into the demo's
  defensibility climax + an honest MEASURED coverage statistic (57/200 ground now; the rest is the visible frontier).
- **"Proper Python tooling" vs HTML-ships-not-Python** — resolved with a thin pytest umbrella over the existing
  dep-free suite, not a packaging restructure.

## Open Questions

- The **C3/C15 cross-pillar contract divergence** (substrate fan-IN C3 vs casework fan-OUT C3 replay; C15
  shell-threshold divergence) is a real sibling-repo engineering frontier — the composed-case grounding gap.
  A future substrate/casework sibling phase aligns the C3/C15 semantics.
- The **agentic tool-calling phase** (OSINT / counterparty gathering / network-ER; tool-evidence extending the
  grounding chain) is the clear next demo-ambition step (the original P63 follow-on).
- The **precedent-confidence GATING engine** (confidence + sample-size → auto-decide-vs-human-gate as a LIVE
  mechanism, not the current display) — the LFCM elicitation-loop path.
- The **substrate ownership/beneficial-owner graph emission** would unlock a richer network view than the
  emitted txn-counterparty edges.

## Artifacts Changed

- `workbench.html` (NEW — the companion-served investigator workbench: real-population queue → per-case
  cluttered KYC/txn/counterparty view → signals-on reveal → live-finale decisioning + the precedent-confidence
  badge + the fail-closed coverage framing; dossier theme; NOT a build/dist target)
- `scripts/serve_workbench.py` (NEW — the localhost companion serving the page + cases + the live finale;
  reuses serve_chain's consume/verify/audit primitives; `--selftest`)
- `scripts/curate_workbench_cases.py` (NEW — deterministic curate: validates the vendored bundles, tags the 4
  exemplars, computes the precedent-confidence badge over real firing frequency, runs casework's stub over all
  200 bundles to MEASURE grounds_e2e → the coverage statistic; lays the synthetic display identity; `--selftest`)
- `data/workbench/` (NEW — 200 real synthetic bundles + the measured `cases.json` index, pinned
  aml-substrate@f90bd39 / aml-casework@c6d8401; coverage 57/200 measured; gate funnel 129/52/19)
- `tests/workbench.test.mjs` (NEW — the workbench arc test, 61 assertions; both motion modes, XSS)
- `pyproject.toml` (NEW — [tool.uv] package=false; pytest dev dep) + `uv.lock` (NEW) + `tests/test_selftests.py`
  (NEW — the pytest umbrella, 17 parametrized cases shelling out to the dep-free suite)
- `docs/case-workbench.md` (NEW — companion walkthrough + honesty framing + the deferred follow-ons incl. the
  ownership-graph emission)
- `tests/smoke-checklist.md` (a workbench presenter entry)

## Related

- [[phase-63-investigator-case-workbench|Phase 63 — Investigator Case Workbench (capstone sales-pitch demo)]] — parent phase

## Soft Observations / Phase N+1 Candidates

- The **C3/C15 cross-pillar contract divergence** (substrate fan-in vs casework fan-out; C15 shell threshold)
  is a real sibling-repo engineering frontier — the composed-case grounding gap (only ~28% of composed cases
  sign). | a substrate/casework C3/C15 contract-alignment phase (the composed-case grounding frontier) | this
  journal "Open Questions" + `data/workbench/cases.json` e2e_note refusals
- The **agentic tool-calling phase** (OSINT / counterparty / network-ER; tool-evidence extending the grounding
  chain) is the clear next demo-ambition step. | an agentic-investigation phase | the P63 plan "Follow-on phases" (a)
- The **precedent-confidence GATING engine** (confidence + sample-size → auto-decide-vs-human-gate as a live
  mechanism, not the display) — the LFCM elicitation-loop path. | a precedent-confidence-gating phase | the P63
  plan "Follow-on phases" (b) + MEMORY.md lfcm-is-jakes-target-vision
- The **substrate ownership/beneficial-owner graph emission** would unlock a richer network view than the
  emitted txn-counterparty edges. | an aml-substrate ownership-graph-emission phase | the P63 plan "Follow-on phases" (c)

## Health Delta

- +1 .mjs arc test (`tests/workbench.test.mjs`, 61 assertions); +2 dep-free `--selftest` entrypoints
  (`serve_workbench`, `curate_workbench_cases`); +1 pytest umbrella (`tests/test_selftests.py`, 17 parametrized
  cases — 11 python selftests + 6 .mjs).
- Full suite GREEN: `uv run pytest` 17 passed; `build.py --check all` 8/8 with ZERO dist drift; build.py imports
  no sibling. No new RUNTIME deps (pytest dev-only, gitignored .venv).
- The T4 checkpoint surfaced + MEASURED a real cross-pillar finding (casework signs 57/200; composed cases fail
  on the C3/C15 divergence) — the verifier was never loosened (abort rule held).
