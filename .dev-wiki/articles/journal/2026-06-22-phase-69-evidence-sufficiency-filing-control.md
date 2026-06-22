---
title: "Phase 69: Evidence-sufficiency filing control"
aliases: []
category: journal
tags: [evidence-sufficiency, requirement-profile, completeness, differentiated-determination, gather, companion, lite]
parents: [phase-69-evidence-sufficiency-filing-control]
created: 2026-06-22
updated: 2026-06-22
source: debrief
duration: ~1 session
---

# Phase 69: Evidence-sufficiency filing control

## What Happened
- Folded the user's two product-coherence defects of the case→STR pipeline into ONE companion-only control — **evidence-sufficiency** — over a shared per-typology **evidence-requirement profile**: (1) lazy/incomplete filing (chain.html dropped most of the casework subject block), (2) defensive filing keyed on combo-FREQUENCY rather than evidence-sufficiency.
- **Supersedes the Phase-64 frequency-route:** the decision is licensed by evidence-SUFFICIENCY vs the profile; n_precedent demoted to `frequency_context` (the contrast, never the trigger). Fulfils Phase-64's flagged "governed/chosen-not-measured next step" without breaking the §12/§14 seam (sufficiency = evidence-presence, not disposition-direction).
- The ML determination bar (the user's domain calls at the gate): a mechanism atom AND ≥2 corroborating legs AND a NAMED predicate risk AND no unrebutted mitigation; atoms enriched with A6 anticipated-activity + A7 source-of-funds + A4 network. **TF dropped** this phase (no capability maps to it).
- Completeness is the MEASUREMENT (required STR elements + determination atoms vs honest gaps); the decision is the SUFFICIENCY VERDICT (sufficient → differentiated determination; insufficient → needs-more-info that NAMES the gap). The §12 discovery loop: unmet, NON-gatherable atoms (no gather_signal) become a substrate-signal brief naming the capability/data to build.
- LIVE-once executed (local Qwen at 127.0.0.1:8080, 2 runs): **ZERO structured-fact fabrications** (the Phase-66 ownership-pct guard held); when the live model under-extracted the corroboration finding, the determination WITHHELD honestly (needs_more_info — never fabricates sufficiency). The deterministic stub is the reliable model-free demo path.
- Adversarial review (6-dimension, 19 agents): 1/13 confirmed — C5 was a GHOST capability (mapped to ML in the offence map, cited by no atom) → FIXED (C5 → ML-A1 "Placement/layering mechanism") + a no-ghost regression guard. 12/13 refuted (honesty seam / boundary / faithfulness / XSS / cross-field consistency all HELD).
- REALITY NOTE carried from the plan: the structured STR render lives in the CHAIN workbench (chain.html / serve_chain), NOT serve_workbench — the 294 case-workbench cases fail-closed by design (the defensibility climax); the one signed-STR case is CASE-P-0010361.

## Decisions Made
- Fold the two defects into ONE evidence-sufficiency control over a shared per-typology requirement profile (completeness = the measurement; the decision = the sufficiency verdict). — extracted this session
- Supersede the Phase-64 frequency-route: license on evidence-SUFFICIENCY; n_precedent → context only. — extracted this session
- The ML determination bar = mechanism + ≥2 legs + named predicate risk + no unrebutted mitigation (A6/A7 mitigation atoms + A4 network); TF dropped (no capability maps to it). — extracted this session
- The §12 feedback: unmet, NON-gatherable atoms become a substrate-signal brief naming the capability/data to build. — extracted this session
- The no-ghost invariant: a capability mapped to a crime_type in the offence map MUST be cited by an atom (the adversarial C5 fix + a selftest guard). — extracted this session

## Problems Solved
- The model under-extracting the corroboration finding live — the determination WITHHELD honestly (needs_more_info), proving the control never fabricates sufficiency; the stub stays the reliable demo path.
- The C5 ghost capability (mapped to ML, cited by no atom) — FIXED by adding C5 to ML-A1 + a no-ghost regression guard, closing the offence-map↔atom consistency gap.

## Open Questions
- A4 partially revised: the 294-case population is ALL money_laundering (C14/C7 absent), so the kyc_integrity + TF profiles are authored but UNEXERCISED — "all typologies" landed at the profile+control level, single-typology at the case level. A kyc/TF case needs a sibling aml-substrate slice emitting C14/TF detectors.

## Artifacts Changed
- `scripts/evidence_requirements.py` (NEW — the determination control: loader/validator + determine/assess_completeness/present_atoms/gather_targets/gathered_signals/evaluate_sufficiency/signal_brief; stdlib + the shared osint_tools._BANNED honesty sweep; casework STR-vocab MIRRORED, not imported)
- `data/workbench/evidence-requirements.json` (NEW — the per-crime_type requirement profile, companion-only; build.py never reads it)
- `docs/evidence-driven-filing.md` (NEW — the design spine + the Phase-70+ sequence)
- `chain.html` (the previously-dropped STR fields render honest-NULL + a new completeness panel)
- `workbench.html` (the DETERMINATION beat between GATHER and DECIDE — frequency contrast + atom assessment + named-risk/mitigation elicitation + verdict + the §12 brief)
- `scripts/serve_chain.py` (completeness rides the run_case payload)
- `scripts/serve_workbench.py` (run_gather requirement targets/closure; determine_case + POST /determine; wired into --selftest)
- `tests/workbench.test.mjs` (106→116), `tests/chain.test.mjs` (48→55), `tests/test_selftests.py` (registers evidence_requirements → uv run pytest 18→19), `tests/smoke-checklist.md`
- `CLAUDE.md`, `docs/case-workbench.md`, `docs/chain-workbench.md` (the new-control true-up)

## Related
- [[phases/phase-69-evidence-sufficiency-filing-control|Phase 69]] — parent phase

## Soft Observations / Phase N+1 Candidates
- The population is all-ML; kyc/TF profiles are profile-ready but unexercised | a sibling aml-substrate slice emitting C14/TF detectors is the unblock | evidence: crime_type distribution {money_laundering: 294}
- Roll the evidence-sufficiency model across the triage + gate consoles (still disposition-only) | Phase 70+ console rollout | evidence: docs/evidence-driven-filing.md "Deferred"
- The §12 briefs consistently name SoF / anticipated-activity / income capabilities to build in substrate | the discovery loop pointing at sibling work | evidence: source_of_funds / expected_monthly_* null in the population
- The live gather (local Qwen) under-extracts corroboration findings (calls the right tools, doesn't always ground the finding) | a Phase-65/66 gather-quality follow-on | evidence: the live-once run; the deterministic stub is the reliable demo path
