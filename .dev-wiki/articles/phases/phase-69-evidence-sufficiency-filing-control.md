---
title: "Phase 69: Evidence-sufficiency filing control — requirement profile → complete-or-honestly-gapped assembly → differentiated determination"
aliases: []
category: phases
tags: [evidence-sufficiency, requirement-profile, completeness, gather, differentiated-determination, companion, all-typology, lite]
parents: [dev-wiki]
created: 2026-06-22
updated: 2026-06-22
source: plan
status: complete
scope: ["data/workbench/evidence-requirements.json", "scripts/serve_workbench.py", "scripts/curate_workbench_cases.py", "scripts/osint_tools.py", "data/osint/corpus.json", "chain.html", "workbench.html", "docs/evidence-driven-filing.md", "docs/case-workbench.md", "docs/chain-workbench.md", "CLAUDE.md", "tests/workbench.test.mjs", "tests/smoke-checklist.md"]
entry_criteria: "Phase 68 delivered + accepted (re-vendored casework@021fb80; chain.html renders the structured FINTRAC STR record; SAR->STR vocab trued up; --check all 8/8). The case→STR pipeline carries two product-coherence defects the user named at the gate: (1) lazy/incomplete filing (drops most of the casework-emitted subject block — chain.html render gap), (2) defensive filing keyed on combo-FREQUENCY rather than evidence-sufficiency. Cases already carry a synthetic display.name keying the committed OSINT corpus (serve_workbench.py:320); UBO is record-sourced from data/osint/corpus.json — local IS enough for the demo."
exit_criteria: "A per-typology evidence-requirement profile (all 3 crime_types) authored + validated; per-case completeness (required/have/gathered/gap) computed + rendered vs the profile with honest-NULL for the previously-dropped subject/relationship fields; the gather loop targets the unmet required entity (record-sourced from the OSINT corpus); the disposition is licensed by evidence-sufficiency-vs-profile (sufficient→determination; insufficient→needs-more-info NAMING the gap), with precedent/frequency kept as CONTEXT only, applied across cases spanning all 3 crime_types; the unmet-requirement gap emitted as a substrate-signal brief + docs/evidence-driven-filing.md written; the control run LIVE once (structured facts record-sourced — the Phase-66 lesson); build.py --check all 8/8 ZERO dist drift; build.py imports no casework/substrate/osint_tools; node tests/workbench.test.mjs + serve_workbench/osint_tools/news_ground selftests green."
---

# Phase 69: Evidence-sufficiency filing control — requirement profile → complete-or-honestly-gapped assembly → differentiated determination

## Objective

Fold the two product-coherence defects the user named at the gate into ONE companion-only control — **evidence-sufficiency** — over a shared per-typology **evidence-requirement profile**. Completeness is the MEASUREMENT (required vs have vs gathered vs gap, vs the profile); the decision is the SUFFICIENCY VERDICT (sufficient → a differentiated determination; insufficient → needs-more-info that NAMES a data/signal gap to build in aml-substrate — the §12 discovery loop). This supersedes the Phase-64 combo-frequency route (precedent/frequency kept as CONTEXT, not the auto-decide trigger), respects the substrate label-blind wall (the profile is deterministic / chosen-not-measured), and runs across the multi-typology 294-case population covering all 3 crime_types (ML / TF / kyc_integrity).

## Scope

Files and modules affected:
- `data/workbench/evidence-requirements.json` — the per-crime_type requirement profile (NEW, authored this phase)
- `scripts/serve_workbench.py` — the profile loader/validator; per-case completeness assessment; sufficiency-vs-frequency routing; the named-gap → substrate-signal brief
- `scripts/curate_workbench_cases.py` — crime_type derivation via casework `CRIME_BY_CAPABILITY` (the all-typology spread)
- `scripts/osint_tools.py` — requirement-targeted GATHER (target the unmet required entity, record-sourced)
- `data/osint/corpus.json` — OSINT entries covering the demonstrated cases' subjects (UBO exemplar)
- `chain.html` — render the previously-dropped STR subject/relationship fields (honest-NULL) + the required/have/gathered/gap completeness panel
- `workbench.html` — the differentiated-determination disposition surface (sufficiency licenses the decision; precedent/frequency as context)
- `docs/evidence-driven-filing.md` — the design doc (the spine + the Phase-70+ sequence)
- `docs/case-workbench.md` · `docs/chain-workbench.md` · `CLAUDE.md` — the new-control true-up (T6)
- `tests/workbench.test.mjs` · `tests/smoke-checklist.md` — the arc coverage + smoke row

The casework consume is TOOL-USE (build.py NEVER imports aml_casework / aml_substrate / osint_tools; the companion subprocesses the vendored CLI over the file-handoff; the agent runs server-side — the browser sends a backend NAME only, §4.5).

## Key constraints

- **Boundary held (Phase-67/68 precedent):** companion-only (serve_workbench / chain.html / osint_tools / data/osint / data/workbench / docs) — NOT a 9th ship target; build.py imports no casework/substrate/osint_tools; the 8 offline dists stay BYTE-FROZEN (`--check all` 8/8); the agent runs server-side (§4.5).
- **Chosen-not-measured profile:** the requirement profile is DETERMINISTIC / chosen-not-measured (wiki/FINTRAC-grounded, the triage-param honesty class), NEVER learned from past dispositions — it respects the substrate LABEL-BLIND wall (no adjudicable ground-truth to learn from locally).
- **Honest-NULL, never faked:** the previously-dropped subject/relationship fields (aliases / BO / IP / DOB / named_relationships) render via `nn()` honest-NULL where the no-PII bundle lacks them; `esc()` stays the SOLE escaper.
- **Sufficiency supersedes frequency:** the disposition is licensed by evidence-sufficiency-vs-profile; precedent/frequency renders as CONTEXT only (the Phase-64 route superseded, not deleted — kept as "how often we've seen the pattern").
- **Single-signal-separable governor (A0):** no detection-lift / catch-rate claim; if a framing reads as "measured/learned catch-rate" → re-word.

## Exit Criteria

- [ ] A per-crime_type evidence-requirement profile (`data/workbench/evidence-requirements.json`) — all 3 crime_types, closed vocab, each required element ∈ casework `STR_REQUIRED_ELEMENTS`, each evidence atom references a real capability/data-source code, the chosen-not-measured disclaimer present — validated by `serve_workbench.py --selftest`.
- [ ] Per-case completeness (required/have/gathered/gap) computed vs the profile + rendered in chain.html, with the previously-dropped subject/relationship fields now rendering (honest-NULL via `nn()`); `esc()` the sole escaper.
- [ ] Requirement-targeted GATHER closes a required gap from the corpus (record-sourced) or honest-gaps it; `news_ground --selftest` green; `validate_osint_corpus` green.
- [ ] The disposition routes DIFFERENTLY for a sufficient vs an insufficient case INDEPENDENT of frequency; the insufficient path NAMES the gap; precedent/frequency renders as context only; applied across cases spanning all 3 crime_types.
- [ ] The unmet-requirement gap emitted as a substrate-signal brief; `docs/evidence-driven-filing.md` written (the spine + the Phase-70+ sequence).
- [ ] The control run LIVE once (grounded/dropped/fabricated counts recorded; structured facts record-sourced — the Phase-66 lesson); `python3 scripts/build.py --check all` 8/8 ZERO dist drift; build.py imports no casework/substrate/osint_tools; all 7 .mjs arcs + serve_workbench/osint_tools/news_ground selftests green.

## Constraints

- Prevents the lazy-filing defect: the completeness panel forces the previously-dropped fields into view (honest-NULL), so the filer-facing STR is complete-or-honestly-gapped, never silently thin.
- Prevents the defensive-filing defect: the determination is licensed by sufficiency-vs-profile, so insufficient-info is a legitimate non-decision (routes to GATHER + the human gate) rather than an auto-file driven by frequency.
- Prevents the label-blind violation: the profile is chosen-not-measured, never learned from dispositions — no catch-rate / detection-lift claim leaks in.

## Checkpoints

- If the per-crime_type requirement profile can't be authored honestly as chosen-not-measured (reads as a measured/learned catch-rate) → re-word, never claim detection-lift (the single-signal-separable governor holds); STOP-and-surface if it can't be made honest.
- If the live execute-once shows the model fabricating a structured fact (the Phase-66 ownership-pct lesson) → record-source it / sweep it / fail-closed, never render the fabrication.
- If "all typologies" is read as "a signed STR per typology" → out of scope (needs casework/substrate to draft+sign TF/kyc cases — cross-pillar, Phase 70+); the signed-STR completeness render stays on the one ML chain case (CASE-P-0010361).

## Assumptions

- A1 [T0 weakest] The two defects are ONE control built as a SINGLE vertical slice over the shared profile. If false (separable / decisioning must lead) → reorder around the decision surfaces.
- A2 The profile is deterministic / chosen-not-measured. If false (learn from history) → hits the label-blind wall, needs an adjudicable-data source we don't have locally → re-scope.
- A3 (RESOLVED-LOCAL) Fully signal-watch-local: the subject NAME resolves to the case's synthetic display-identity; UBO is record-sourced from the committed OSINT corpus. If false (need real names/UBO at source) → cross-pillar-coordinated like Phase 68 (the deferred §12 substrate-signal brief).
- A4 (RECONCILED all-typology) The profile covers all 3 crime_types + the control runs across the multi-typology population, WITHOUT a signed STR per typology. If read as "a signed STR per typology" → cross-pillar (Phase 70+).

## Abort

Any new ship target / dist drift / a sibling-or-companion import in build.py / a validator loosened to force a fit → STOP-and-surface. If the requirement profile can't be authored honestly as chosen-not-measured → re-word, never claim detection-lift. If the live execute-once shows a fabricated structured fact → record-source / sweep / fail-closed, never render the fabrication.

## Notes

- Ceremony: LITE (the assumption-ledger gate IS the direction gate; spec waived).
- Ledger: Phase-69 block in `assumption-ledger.md` (A0 boundary · A1 one-slice [T0 weakest] · A2 chosen-not-measured · A3 RESOLVED-LOCAL · A4 RECONCILED all-typology). NOT all-accept — A3/A4 each moved the scope.
- Direction: the user REFRAMED the consolidate-vs-switch question into a product-coherence critique of the case→STR pipeline (lazy/incomplete filing + defensive-not-effective decisioning), folded into one evidence-sufficiency control over a shared requirement profile.
- Grounded against the committed Phase-68 workbench (signal-watch HEAD 268f84b; chain.html render gap, curate_workbench_cases.py frequency-route, osint_tools.py additive gather, serve_workbench.py synthetic display-identity resolution — code-verified via an Explore map this session).
- The Phase-64 frequency-route is SUPERSEDED (precedent/frequency kept as context; the decision keyed on sufficiency); holds the Phase-62 §12/§14 boundary (route on §12, dispositions §14 illustrative).
- WIKI grounding for the profile (T1): `suspicious-activity-reporting` (STR lifecycle / FINTRAC required elements) · `money-mule-networks` (the ML evidence atoms) · `kyc-and-customer-due-diligence` (beneficial ownership: US CTA / Canada FINTRAC — the UBO requirement + kyc_integrity atoms).
- KNOWLEDGE GAP carried to impl: the exact per-typology determination-licensing atom set is net-new authoring (no prior structure exists) — authored honestly as chosen-not-measured, grounded in the wiki articles + FINTRAC STR guidance, reviewed before lock.
- The console rollout (triage/gate) + the substrate party/UBO-at-source coordination are Phase 70+ (the deferred half — captured in `docs/evidence-driven-filing.md`).

## Gates

- [x] Direction confirmed by user (assumption positions taken 2026-06-22; A1/A2 accept, A3 resolved-local, A4 reconciled all-typology)
- [ ] Delivery accepted (post-implementation report)
