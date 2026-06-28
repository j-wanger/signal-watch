# PLAN-BRIEF — aml-substrate P35+: the remaining determination-signal frontier (TF · broader C7 · org-name sanctions · open-data Stage 2/3)

> **◼ RECONCILED 2026-06-28 (Phase 81) — most of this frontier is now RESOLVED; substrate advanced
> `1f5901e` → `f7fbdb0` (Phases 35/36/37), code-verified + measured this session.** Per-ask status (supersedes
> the "still-unbuilt frontier" section below, kept historical):
> - **(1) TF slice → substrate-CUT** (NOT an open ask). substrate measured it `already-null` this session (no TF
>   crime type; `{US,CA}`-only jurisdiction; the disposition basis needs a high-blast crime-mix edit the consumer's
>   brief forbids) and retains it as an honest-null artifact. signal-watch's TF `evidence-requirements.json` profile
>   stays authored-but-unexercised by design.
> - **(2) broader C7 → substrate-CUT** (NOT an open ask). substrate measured it `tell-unavoidable` this session (at
>   m=1 a pure magnitude screen; mules are the magnitude outliers, `corr` 0.172/0.187 over the 0.10 label-blind
>   gate) and kept the `broaden_c7_probe.py` cut-record. A broadened C7 would re-introduce the forbidden flag↔label tell.
> - **(3) org-name sanctions → BUILT (substrate Phase 35 `4f49e53`) but the merge consume is BLOCKED, one-sided.**
>   signal-watch Phase 81 T1a MEASURED it STRUCTURALLY ONE-SIDED: substrate's anchored fragment overlay is
>   person-only (0 org fragment clusters), so an org-name collision can never be a same-org UPHOLD → all-reject →
>   the merge org case can't ship two-sided. → **[`substrate-org-fragment-emit-PLAN-BRIEF.md`](substrate-org-fragment-emit-PLAN-BRIEF.md)**
>   (the new ask: fragment orgs like persons). The org-name screening ALSO feeds the workbench: a sanctioned org BO
>   is one source of the Phase-36 C17 exposure leg (consumed below).
> - **(NEW) Phase 36 — exposure-via-ownership C17 leg → CONSUMED (Phase 81 T4)** as a DEFENSIVE-EXPOSURE
>   determination leg. Measured: it fires on 13 customers with a sanctioned beneficial owner but all are oracle-CLEAR
>   (the `sanctions_flag` is label-blind, `corr≈0`) → a defensible precautionary basis, NOT a latent-laundering
>   discriminator (the Phase-78 §12 discovery feed classifies it as over-flag). NOT a detection lift.
> - **(NEW) Phase 37 — geo/jurisdiction enrichment → CONSUMED (Phase 81 T4)** as a rendered OBSERVABLE (22-country
>   `counterparty_country` + FATF tail, no leg). A C20 high-risk-jurisdiction determination leg is the named FUTURE
>   item — it MUST control for txn-volume (substrate's caveat: mules transact more, a naive "any high-risk exposure"
>   flag inherits txn-count mediation).
> - **(4) open-data Stage 2/3 → still deferred** (substrate-side); the signal-watch SHIP-compliance angle is now
>   mapped in **[`open-sanctions-data-fork-PLAN-BRIEF.md`](open-sanctions-data-fork-PLAN-BRIEF.md)** (the per-source
>   license matrix + the non-commercial boundary); the substrate-anchoring angle stays in
>   [`substrate-open-reference-data-fork-PLAN-BRIEF.md`](substrate-open-reference-data-fork-PLAN-BRIEF.md).
>
> Net: of the four original asks, two are substrate-CUT (TF, C7), one is built-but-blocked-on-a-new-ask (org-name →
> org-fragment brief), one stays deferred (open-data → two licensing briefs); the two unanticipated Phase-36/37
> emissions are consumed. The historical brief follows.

> **A signal-watch → aml-substrate handoff brief** (the Phase-55–58 sibling-brief pattern). Authored in
> signal-watch (Phase 80); **executed in an aml-substrate session**. signal-watch defines the *contract* it
> needs; the substrate owns the build. **Code-verified live this session at aml-substrate @`1f5901e`
> (Phase 34, `main`)** — re-verify before acting; sibling state drifts between sessions.
>
> **This brief supersedes the absorbed `docs/substrate-determination-signals-PLAN-BRIEF.md`** for the parts that
> LANDED (Phase 71/72 consumed the BO-graph + the C14 kyc emission; Phase 80 consumed the Phase-34 sanctions
> screening). It carries forward ONLY the still-unbuilt determination-signal asks, re-grounded to the live HEAD.

## What LANDED since the prior brief (verified @1f5901e — do NOT re-ask)

- **Phase 25–28** — `related_parties[]` BO graph (v0.3) + `source_of_funds` + the re-keyed C14 + the v0.4
  named-identity + v0.5 entity-resolution emission. ✓ CONSUMED (signal-watch Phase 71/72/74/75).
- **Phase 29–31** — slice-aligned `true_entities` + the exogenous `intended_disposition` oracle, CLI-wired
  via `--emit-eval-oracles`. ✓ CONSUMED (signal-watch Phase 78 — the determination-validation harness).
- **Phase 32–33** — the `--anchored` same-person fragment overlay (`GT-<hash>` latent clusters, `entity_ref ≠
  cluster` → non-circular) + real-frequency name pools. ✓ CONSUMED (signal-watch Phase 79 — the merge console's
  scored real population).
- **Phase 34 (seam-5)** — `sanctions_flag` made LIVE under `--anchored` via a **label-blind OFAC-watchlist
  name collision** + the **revived non-tautological C14** (the escalation-gap branch: `(sanctions_flag or
  adverse_media_flag) and cdd_level != EDD`). ✓ CONSUMED (signal-watch **Phase 80**): the merge console's
  OFAC name-collision case class (two-sided 11 uphold / 13 reject) + the workbench's §12 sanctions-driven C14
  leg (KYC-A1 lights; casework's Phase-19 party-leaf grounding SIGNS it).

## The still-unbuilt frontier (the P35+ queue, in rough value order)

### 1. A TF (terrorist-financing) case slice — the unexercised crime_type
**Code-verified absent (@1f5901e):** no dedicated TF detector; `terrorist`/`terror_financing` appear only in
docstrings + the FATF validation typologies, not in `gen/` or `monitor/detectors/`. The disposition basis
`sanctioned_or_designated_nexus` stays deferred (it needs a crime-mix edit). **The ask:** emit a small TF case
slice — a crime_type whose fired capabilities map to a TF determination atom — so signal-watch's
`evidence-requirements.json` TF profile (authored-but-unexercised) fires end-to-end. Measurement-first per
substrate doctrine: report `needs-behavior` until emergence is *measured*, never stamped.

### 2. Broader C7 (peer/business-activity anomaly) coverage
**Code-verified built but SPARSE (@1f5901e):** `monitor/detectors/business_activity.py:43` `capability="C7"`
fires, but on few cases (9 of 2000 in a probe emit). **The ask:** broaden C7 so the **ML-A3 profile-inconsistency**
leg (C7 · C8) reaches more cases from peer/income-anomaly signals — widening the population that can reach the
≥2-leg determination bar from *internal* signals (not gathered corroboration). Not a detection-quality change; a
determination-evidence breadth change.

### 3. Org-name sanctions screening (the entity-level OFAC collision)
**Code-verified deferred (@1f5901e):** Phase 34's `apply_anchored_sanctions` screens PERSON surnames against the
OFAC token index; organizations are not screened. **The ask:** extend the label-blind collision to org names
(an under-classified org with a sanctioned-name-colliding beneficial owner) — feeds a C14/C15 cross-pillar
determination leg signal-watch already renders (`related_parties[]`). Same label-blind discipline: no entity IS
a designated party; the collision is the screening false-positive surface.

### 4. Open-data realism Stage 2/3 (carried from Phase 33)
**Code-verified deferred (@1f5901e):** Phase 33 landed Stage-1 realism (US-Census/GLEIF-CA name pools + NAICS +
geo via `--anchored`). Stage 2/3 (paid sources, OSM street geo, full NAICS hierarchy, government sanctions/FATF
anchors) stay deferred. **The ask:** Stage 2 anchors the synthetic universe to more open reference data, making
the merge console's collisions *real-shaped* (not the artificial frequency floor) and giving `true_entities` a
richer two-sided oracle. Realism of *values*, not *contract* — consumers read the same shape, no consume-side rework.

## NOT an ask (a principled measured null — do NOT build)

- **C1 anticipated-vs-actual deviation (ML-A6).** Code-verified a **documented measured null** at @1f5901e
  (`docs/phase-25-determination-signal-emission.md`: "C1 / ML-A6 remains a measured null — the dormancy
  architecture suppresses it; C1 would double-count C8"). signal-watch treats ML-A6 as an honest gap, not a
  missing detector. Re-deriving a C1 detector would stamp an emergence the substrate measured does not occur.

## The contract signal-watch consumes (no consume-side rework)

signal-watch reads fired capabilities off the case bundle (`entry.capabilities` → the determination atoms via
`evidence-requirements.json`) and renders `related_parties[]` as the network view. So:

| substrate emits | signal-watch consumes (already built) |
|---|---|
| a TF case (fired caps → a TF atom) | the unexercised `evidence-requirements.json` TF profile fires |
| broader C7 on real data | ML-A3 lights on more cases → the ≥2-leg bar reachable from internal signals |
| an org-name OFAC collision | the merge console's name-collision class + the network view |
| Stage-2/3 open-data anchors | real-shaped merge collisions + a richer `true_entities` oracle (no rework) |

## Honesty governor

The substrate is **single-signal-separable** (composition is architecturally subsumed by network linkage —
substrate P16): this brief adds **determination-evidence breadth + value-realism**, NOT detection difficulty.
Nothing here is a detection-quality improvement; the value is **defensibility + KYC-control depth + collision
realism**, all synthetic and badge-labeled. No rate, score, or multiplier is claimed. If a framing reads as
"harder to detect / better catch," re-word.

## Pins / provenance

- aml-substrate @ **`1f5901e`** (Phase 34, verified live this session: TF absent, C7 sparse, org-name sanctions
  deferred, Stage 2/3 deferred, C1 a documented measured null).
- Consume-side (all already built): `data/merge/cases.json` + `scripts/curate_merge_cases.py`
  (`enumerate_substrate_sanctions`) + `scripts/distill_sanctions_slice.py`; `scripts/serve_workbench.py`
  (`sanctions_c14_consume`) + `data/casefile/sanctions-c14-demo.bundle.json`; `scripts/evidence_requirements.py`
  (the atoms ← capabilities map, BYTE-UNCHANGED).
- Supersedes the landed parts of `docs/substrate-determination-signals-PLAN-BRIEF.md` (Phase 70/71, pinned @b53855c).
