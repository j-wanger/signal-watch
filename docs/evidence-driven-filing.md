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
- **Zero cases reach the ≥2-leg bar from signals alone** — 182 carry a mechanism + 0
  legs, 104 a mechanism + 1 leg, and 8 carry no mechanism at all. The frequency gate
  would auto-clear 189; the determination withholds them pending corroboration. That
  gap *is* the "defensive filing" exposure, made concrete.
- **`source_of_funds` is null and no C1 anticipated-activity detector exists** (the
  expected-activity baseline IS generated in the substrate — `ExpectedActivity` — but
  nothing fires C1 over it), so A6 / A7 are honest gaps for every case → the §12 brief
  names a SoF field + a C1 detector + broader C7 coverage to build.

## Gather extraction quality (Phase 70 — measured)

The §12 loop's value depends on GATHER actually *closing* the gaps it targets. Phase
69's live-once found the opposite — the model fetched the sanctions record but extracted
**no** finding from it, so corroboration (ML-A5) stayed open and the determination
withheld. Phase 70 measures, fixes, and regression-guards that.

**The measuring stick (consistency, not a catch-rate).** The deterministic `StubPlanner`
grounds a finding from *every* record it surfaces, so it is the **reference**: live
gather quality = how much of that reference the live model recovers. The gather result
now carries a `coverage` block — `finding_coverage` (grounded ÷ records surfaced),
per-tool `grounded`, and `target_closure` (closeable atoms closed ÷ targeted) — emitted
in-stream and rendered as counts ("evidence extracted from N of M surfaced records").
`osint_tools --selftest` asserts the stub reaches `finding_coverage == 1.0` for *every*
corpus subject (the reference is a checked property, not an emergent one); an aborted /
no-record run is marked `complete: false` and shows no figure (a transport failure is
not an extraction miss).

**Diagnosis → fix (local Qwen at 127.0.0.1:8080).** The baseline confirmed the surface
was the live `findings()` prompt, not the tool surface / corpus / leg-mapping: the record
was reachable and returned; the stub proves a sanctions finding closes ML-A5. The fix
(both `LivePlanner` prompts): `findings()` now sees each record's **declared entities**
and is told to extract a finding from *every* record — a sanctions/adverse hit is itself
a finding, no ownership tie required; `action()` screens the **subject** for adverse media
plus each affiliate for sanctions (the efficient path within the step cap). Structured
facts stay record-sourced (the Phase-66 guard: the model never authors an ownership
label / percent / direction).

| metric (mule case) | baseline | after fix | stub reference |
|---|---|---|---|
| `finding_coverage` | 0.5 | **1.0** | 1.0 |
| `target_closure` (ML-A5) | 0.0 — open | **1.0 — closed** | 1.0 |
| grounded records | rg-zz-01 | rg-zz-01 · am-zz-01 · sx-cd-01 | same 3 |
| fabricated structured facts | — | 0 | — |

With ML-A5 closed (corroboration), the case clears the ≥2-leg bar and — with a named
predicate risk + rebutted mitigation — reaches a **determination** (the payoff the §12
loop needs). The capture is pinned in `tests/gather_quality_harness.py` (the
`news_quality_harness` pattern): `--check` replays the model's responses with **no
model** and asserts the outcome still matches the baseline *and* the stub reference;
`--freeze` re-captures from a live model (synthetic corpus → no compliance gate) and
refuses to baseline a capture that falls under the reference.

## Deferred — Phase 71+

- **Roll the sufficiency model across the triage + gate consoles** (`triage.html`,
  `console.html`) — the determination grammar there is still disposition-only.
- **The substrate determination-signal build queue.** The demo resolves a *synthetic*
  display identity and gathers a *synthetic* OSINT corpus; the **internal** determination
  legs (anticipated-activity, source-of-funds, profile inconsistency), the **real**
  ownership graph at source, and a **kyc_integrity / TF case slice** must be built in
  aml-substrate. Phase 70 consolidated every §12 ask — derived from the population's
  non-gatherable gap — into ONE handoff:
  **`docs/substrate-determination-signals-PLAN-BRIEF.md`** (it supersedes the Phase-66
  BO-graph brief). Sibling-executed; build.py untouched.

See also `docs/case-workbench.md`, `docs/chain-workbench.md`, and the program
blueprint §12 (history-as-evidence) / §14 (the continuous adjudication loop).
