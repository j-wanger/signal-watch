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

> **Superseded for C14 / source-of-funds (Phase 72).** The substrate now emits C14 (Phase 26), so
> `kyc_integrity` is **exercised** — 727 C14-pure customers, the §12 KYC loop closes from KYC-A1 (see *The
> §12 KYC loop closes — C14 consumed* below). C1 stays a **principled measured null**; broader C7 + a TF
> slice stay gaps. The findings above are the Phase-69 baseline (the 294-case population).

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

## The §12 loop closes — from REAL signals (Phase 71)

Phase 69 measured **zero** cases reaching the ≥2-leg bar from signals alone (the
defensive-filing exposure); Phase 70 made GATHER close the *external* legs. Phase 71
closes the loop from **internal** signals by adopting aml-substrate's **contract v0.3**
slice (substrate Phase 25, pinned `@443e4a6`):

- A case = a **customer**: `curate_workbench_cases` now **merges** the substrate's separate
  monitoring (C2-C5/C15) and C8-screening bundles, so the **profile-inconsistency** leg
  (C8 → ML-A3) co-occurs with the **network** leg (C15 / `related_parties[]` → ML-A4).
- Result (committed merged v0.3 slice, **342 cases**): **81 cases reach the ≥2-leg bar
  from REAL signals** — a mechanism + ML-A3 + ML-A4 — so with a named predicate risk + a
  rebutted mitigation they reach a **determination** *without* GATHER. The §12 ML loop
  closes. (Funnel re-derived **181/79/82**; end-to-end coverage **107/342**.)
- The bundle's **`related_parties[]`** (the real emitted BO graph) renders as the case
  network (`boGraphHTML`; "N pct", never "%").

## The §12 KYC loop closes — C14 consumed (Phase 72)

Phase 72 consumes aml-substrate's **Phase-26 C14 KYC-integrity emission** (re-pinned `@f15c241`; vendored
casework moves to `@bf15535` — its Phase-14 broadened C14 grounding; the casework pin is now READ from
`vendor/aml-casework/VENDORED_AT`, not hardcoded):

- A **C14-PURE** customer (fires C14 with no ML capability co-firing) classifies `kyc_integrity` and reaches a
  determination from **KYC-A1 — the C14 mechanism ALONE** (the kyc profile needs mechanism + **0** legs; the
  human still names the predicate risk). The emitted population holds **727** C14-pure customers; the committed
  slice carries **6** kyc cases (all determine). The §12 KYC loop closes.
- The **dual-map is correct, not a firewall.** A customer with laundering signals **and** a source-of-funds gap
  classifies `money_laundering` (C14 → ML-A7, the SoF leg corroborating the ML case). So the merge folding C14
  into an ML customer is right — the planned curate firewall was a **measured no-op** (727 pure → kyc, 926
  mixed → ML, cleanly).
- **kyc SIGNING is the honest cross-pillar FRONTIER.** A txn-bearing C14 case **signs** end-to-end through the
  re-vendored casework; a purely **txn-less** C14 party-leaf **fails-CLOSED at casework's no-transactions
  CONTRACT** (`bundle: no transactions`, surfaced via the honest `e2e_note`, never loosened). In the slice **2
  of 6** kyc cases sign; the rest fail-closed honestly. The re-vendor preserved the ML signings (**0**
  regressions). Slice **355**, coverage **128/355**, funnel **183/110/62**.

**Still gaps (named in every `signal_brief`).** **C1** anticipated-activity is a **principled measured null**
(the substrate refuses it as a C8/C6 double-count — it will not be built), broader **C7** (screening-only), and
a **TF** case slice (no live path in any pillar). The honesty governor holds: this is determination-evidence
**breadth**, never a catch-rate / detection-lift claim.

## Deferred — Phase 72+

- **Roll the sufficiency model across the triage + gate consoles** (`triage.html`,
  `console.html`) — the determination grammar there is still disposition-only.
- **The substrate determination-signal build queue — further closed.** The BO graph +
  profile-inconsistency/network legs (C8 + C15) close the §12 ML loop (Phase 71); **C14
  source-of-funds / KYC-integrity** closes the §12 KYC loop and signs txn-bearing cases
  (substrate Phase 26 / casework Phase 14 / signal-watch Phase 72). **Still open:** the
  **txn-less C14 party-leaf** signing path (a casework no-transactions-contract follow-on
  — relax the contract for a `kyc_integrity` filing, or drop `transaction_details` from the
  kyc STR profile); **C1** anticipated-activity (a principled measured null); broader
  **C7**; and a **TF** case slice. Consolidated handoff:
  **`docs/substrate-determination-signals-PLAN-BRIEF.md`**. Sibling-rooted; build.py untouched.

See also `docs/case-workbench.md`, `docs/chain-workbench.md`, and the program
blueprint §12 (history-as-evidence) / §14 (the continuous adjudication loop).
