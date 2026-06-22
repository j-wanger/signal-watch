# Evidence-driven filing — the determination control (Phase 69)

> Companion-only design note. The control lives in the chain + case workbenches
> (`serve_chain.py` / `chain.html`, `serve_workbench.py` / `workbench.html`,
> `evidence_requirements.py`); it is **not** a ship artifact and **not** a build
> target. `build.py` imports none of it; the 8 offline dists stay byte-frozen.
> Illustrative throughout — the always-on "Illustrative data & outputs" badge applies.

## The problem this fixes

The Phase-68 workbench filed an STR off a fired signal and a high precedent count.
Two defects, both raised by the user at the Phase-69 direction gate:

1. **The filing was lazy / incomplete.** The casework drafter emits a rich subject
   block (aliases, beneficial ownership, IP/VC, DOB, named relationships), but the
   render dropped most of it — and the no-PII bundle leaves the rest empty. A filing
   that doesn't even surface what it's missing reads as complete when it isn't.
2. **The decision was defensive, not effective.** The gate keyed on combo
   **frequency** (`n_precedent ≥ 500 → auto-clear`). Seeing a pattern more often is
   not a determination. Effective monitoring asks a different question: *have we
   learned what risk this carries, and do we have the supporting evidence a
   determination requires?*

The two fold into **one control — evidence-sufficiency.** Completeness is the
measurement; the decision is the sufficiency verdict; both read the same spine.

## The spine

```
  evidence-requirement profile        (data/workbench/evidence-requirements.json)
        │  per crime_type: required STR elements + determination-licensing ATOMS
        ▼
  COMPLETENESS measurement            (assess_completeness — chain.html render)
        │  required vs have vs honest gap; the dropped STR fields surfaced honest-NULL
        ▼
  requirement-targeted GATHER         (run_gather → osint_tools; record-sourced)
        │  seek the unmet, closeable atoms (network / corroboration); close or honest-gap
        ▼
  differentiated DETERMINATION        (determine / determine_case — workbench.html)
        │  licensed by SUFFICIENCY, not frequency; frequency demoted to context
        ▼
  §12 DISCOVERY-LOOP feedback         (signal_brief)
           the unmet, non-gatherable atoms name what to BUILD in aml-substrate
```

### The evidence-requirement profile (chosen, not measured)

Per crime_type, the profile names the **determination-licensing atoms** — the
supporting evidence a *determination* needs, beyond a complete filing:

- **money_laundering** — a mechanism atom (A1 placement/layering / A2 evasion-intent) **AND
  ≥2 corroborating legs** from {A3 profile-inconsistency, A4 network/UBO, A5 external
  corroboration, A6 anticipated-activity, A7 source-of-funds} **AND** a *named
  predicate risk* (the specific risk we file for — human trafficking, fentanyl —
  grounded to the cited signals' typology) **AND** *no unrebutted mitigation* (SoF /
  anticipated-activity considered, the benign explanation ruled out).
- **kyc_integrity** — the C14 integrity failure + (optionally) beneficial-ownership
  opacity. The *named risk* still required.
- **terrorist_financing** — dropped this phase: no capability maps to it, so the
  population carries no TF case (honest "profile-ready, no case").

The atoms + thresholds are **authored from public AML guidance + the capability
taxonomy, never learned from past dispositions** — the substrate is label-blind
(the §12/§14 honesty seam). The verdict is illustrative; zero catch-rate / precision
/ lift number appears anywhere.

### The differentiated determination

`determine_case` computes the verdict and keeps the Phase-64 frequency gate as
**context** — it decides *where* to spend judgment, never *that* a determination
holds. The contrast is the demo: a case the frequency gate would auto-clear is, by
the evidence, **needs-more-info**. Insufficiency is a legitimate non-decision; its
`missing` names the gap — gather it, confirm it at the human gate, or build it.

`named_risk` and `mitigation_rebutted` are the **human elicitation** — the gate where
a person fills what the data cannot. That is faithful to real casework: the analyst
states the risk and rules out the benign story; the system doesn't pretend to know.

### The §12 discovery loop

The unmet atoms GATHER *can't* close (no external record to fetch — profile
inconsistency, anticipated-activity, source-of-funds) become a **signal brief**: each
names the capability (C*) + data sources (D*) the determination needs but the program
doesn't yet have. The gap is evidence of what to build next, in `aml-substrate` —
exactly how a real program matures: define the risk clearly, then build the detector.

## What the data showed (honest findings)

Measured over the committed 294-case workbench population:

- **All 294 cases are money_laundering.** C14 / C7 are absent, so `kyc_integrity` is
  profile-ready but unexercised (the same honest "no case" state as TF). "All
  typologies" lands at the profile + control level, single-typology at the case level.
- **Zero cases reach the ≥2-leg bar from signals alone** — 181 carry a mechanism + 0
  legs, 103 carry a mechanism + 1 leg. The frequency gate would auto-clear 189; the
  determination withholds all of them pending corroboration. That gap *is* the
  "defensive filing" exposure, made concrete.
- **`source_of_funds` and `expected_monthly_*` are null in the population**, so A6 /
  A7 are honest gaps for every case → the §12 brief consistently names a SoF /
  anticipated-activity / income-inconsistency capability to build.

## Deferred — Phase 70+

- **Roll the sufficiency model across the triage + gate consoles** (`triage.html`,
  `console.html`) — the determination grammar there is still disposition-only.
- **Substrate names / UBO at source.** The demo resolves a *synthetic* display
  identity and gathers a *synthetic* OSINT corpus. The real names + ownership graph
  come from an aml-substrate party/UBO emission (the brief in
  `docs/substrate-bo-graph-emission-PLAN-BRIEF.md`) + the new SoF / anticipated /
  income capabilities the §12 briefs above name. Sibling-executed; build.py untouched.
- **A kyc_integrity / TF case** needs a substrate slice that emits C14 / TF detectors —
  the profile is already authored and will exercise the moment such a case lands.

See also `docs/case-workbench.md`, `docs/chain-workbench.md`, and the program
blueprint §12 (history-as-evidence) / §14 (the continuous adjudication loop).
