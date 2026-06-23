# PLAN-BRIEF — aml-substrate: determination-signal emission (the §12 build queue)

> **A signal-watch → aml-substrate handoff brief** (the Phase-55–58 sibling-brief pattern). Authored in
> signal-watch (Phase 70); **executed in an aml-substrate session**. signal-watch defines the *contract* it
> needs; the substrate owns the build. Pinned to **aml-substrate@b53855c** (verified live this session).
>
> **This brief SUPERSEDES & ABSORBS `docs/substrate-bo-graph-emission-PLAN-BRIEF.md`** (Phase 66). That brief
> covered ONE determination leg (network/UBO); Phase 69–70 measured the *full* determination-evidence gap and
> consolidates the asks into a single handoff so the sibling session has one queue, not a brief-per-gap.

## Why this is the handoff (the §12 measurement)

Phase 69 built the evidence-**sufficiency** filing control: a determination is licensed by mechanism + **≥2
corroborating legs** + a named predicate risk + no unrebutted mitigation — never by combo-frequency. Measured
over the committed 294-case workbench population, **zero cases reach the ≥2-leg bar from fired signals alone**
(182 carry a mechanism + 0 legs, 104 a mechanism + 1 leg, and 8 carry no mechanism at all — a single leg
only). That gap *is* the "defensive filing" exposure.

Phase 70 then made the **GATHER** loop close the **external** legs at full coverage (network/UBO via the
registry, corroboration via sanctions/adverse — `finding_coverage` 0.5 → 1.0, ML-A5 closed; see
`docs/evidence-driven-filing.md`). What GATHER **cannot** close are the **internal** legs — they have no
external record to fetch; they are evidence the *program* must produce. Those are this brief.

The §12 non-gatherable gap, **derived** by `signal_brief()` over the committed population
(`scripts/evidence_requirements.py`; reproduce: union `signal_brief(crime_type, present_atoms(caps), profile)`
across `serve_workbench.load_index()["cases"]`):

| determination atom | capability needed | data needed | cases needing it |
|---|---|---|---|
| **ML-A6** anticipated-activity inconsistency | **C1** customer-profile / out-of-pattern monitoring | D8 KYC/CDD, D10 customer-reference | **294 / 294** |
| **ML-A7** source of funds not established | **C14** KYC integrity & customer-cooperation | D8 KYC/CDD, D20 external/lifestyle reference | **294 / 294** |
| **ML-A3** profile inconsistency | **C7** peer/business-activity anomaly · **C8** income/occupation-vs-activity | D8 KYC/CDD, D20 external reference | **287 / 294** |
| **ML-A4** network / UBO linkage | **C15** beneficial-ownership / nominee network | D8 KYC/CDD | gather-closeable now, but **synthetic** OSINT stand-in (real edges = the BO-graph emission below) |

Closing these is what moves the population from "always needs-more-info" to "a defensible determination is
*reachable*" — the whole point of the sufficiency control.

## What exists today (code-verified @b53855c; sibling paths are under `src/aml_substrate/`)

- **The contract is still v0.2 / subject-only.** `monitor/evidence.py:38` `CONTRACT_VERSION = "0.2"`; the
  bundle's `parties[]` is the subject's 16-field `PartyView`. **No `related_parties[]`, no `PartyGraphView`.**
- **The BO graph is generated but unprojected.** `gen/population.py` draws `RelationshipEdge`s
  (`BENEFICIAL_OWNER` + `DIRECTOR_OF`, with `ownership_pct`) — never projected to a view nor emitted.
- **The anticipated-activity baseline + a peer/income basis ALREADY EXIST.** `gen/population.py:135` sets
  `ExpectedActivity(monthly_volume_cents=…)` on every person, projected onto
  `PartyView.expected_monthly_volume_cents` + an occupation / business-activity basis; the **C8** detector
  even fires on them (7 of the 294 vendored cases). So ML-A3's data is present — what's missing is broader
  **C7** coverage and, for ML-A6, a **C1** anticipated-vs-actual *detector* over the existing baseline (not data).
- **`source_of_funds` is the one genuinely-missing field.** No `gen/` assignment (verified) — so ML-A7 lacks
  both the SoF data AND a non-tautological detector.
- **C14 is tautological.** A `kyc_integrity` detector exists (`monitor/detectors/kyc_integrity.py`) but fires
  on `cdd_level==EDD ⇔ risk_rating==HIGH` by construction with `source_of_funds` never populated — a static
  artifact, not an emergent KYC-integrity signal (substrate P19 finding).
- **Detectors emit C2–C8, C14, C15, C26 codes**, but the **C1** anticipated-vs-actual detector is absent and
  C14 is the tautology above — so the vendored slice is all `money_laundering`, ML-A6/A7 never light, and the
  determination legs stay short.

## The ask (one queue, four parts — measurement-first per substrate doctrine; do NOT stamp emergence)

### 1. GENERATE the one missing data field (the SoF root gap)
At population generation, populate per customer (synthetic, badge-labeled, distribution-grounded):
- **`source_of_funds`** (a stated SoF + a verifiable/unverifiable flag) — backs C14 / ML-A7; today it has
  **no `gen/` assignment**, so C14 can only fire the EDD tautology.
The anticipated-activity baseline (`ExpectedActivity.monthly_volume_cents`) and the peer/income basis
(occupation / business-activity) **already exist** — those legs need DETECTORS (part 2), not new data.

### 2. DETECT the internal legs (non-tautological, emergence-verified)
- **C1** (ML-A6) — anticipated-vs-actual deviation over the **existing** `ExpectedActivity` baseline (the
  detector is absent, the data is not). The dominant gap: 294/294 cases.
- **C7** (ML-A3) — broaden peer/business-activity-anomaly coverage (C8 already fires on 7 cases; C7 is sparse).
- **C14** (ML-A7) — a **non-tautological** source-of-funds / BO-disclosure detector over the new SoF field
  (NOT the EDD≔HIGH tautology): e.g. unverified SoF at scale, or a high-risk/PEP/sanctioned beneficial owner
  under an under-classified org.
Bind each to a corpus indicator via aml-casework `grounding_replay`; report `needs-behavior` until emergence
is *measured*, never stamped (substrate P19 discipline).

### 3. EMIT the beneficial-ownership graph (absorbed from the BO-graph brief — the ML-A4 leg at source)
- **`PartyGraphView`** — project, for a subject, its declared ownership/control graph from the existing
  `RelationshipEdge`s.
- **`related_parties[]`** in the evidence bundle (contract **v0.2 → v0.3**, additive / optional so v0.2
  readers keep working): `{party_id, label∈RelationshipLabel, ownership_pct, is_person, risk_rating,
  cdd_level, pep_tier, sanctions_flag, adverse_media_flag}` (reuse the existing `PartyView` for the KYC
  fields). This maps **1:1** onto the network view signal-watch already renders — Phase 66's OSINT corpus
  (`data/osint/corpus.json`) was authored to mirror this exact shape, so **the consume side needs no rework**.

### 4. EMIT a kyc_integrity / TF case slice (exercise the authored-but-unexercised profiles)
The Phase-69 `evidence-requirements.json` profile already carries `kyc_integrity` (and a TF slot, dropped
this phase — no capability maps to it). It is **unexercised** because the population is all-ML. Emit cases
whose fired capabilities include C14 (and, for TF, the relevant detectors) so a kyc/TF case lands in the
re-vendored slice and the profile + the determination control exercise end-to-end.

## The contract signal-watch consumes (no consume-side rework)

signal-watch reads fired capabilities off the case bundle (`entry.capabilities` → the determination atoms
via `evidence-requirements.json`) and renders `related_parties[]` as the network view. So:

| substrate emits | signal-watch consumes (already built) |
|---|---|
| a case firing C1 / C7 / C8 / C14 on real data | the determination atom lights (ML-A6 / ML-A3 / ML-A7) → the case can reach the ≥2-leg bar |
| `related_parties[]` (label + ownership_pct + KYC fields) | the workbench network view (1:1 with the Phase-66 OSINT shape) |
| a kyc_integrity / TF case | the unexercised `evidence-requirements.json` profile fires |

## Acceptance (the cross-pillar seam)

- The population carries `source_of_funds` / anticipated-activity / peer-income fields (synthetic, badged).
- C1 / C7 / C8 / C14 fire on a **measured** signal (not a construction tautology), grounded via aml-casework
  `grounding_replay` to a corpus indicator; reported `needs-behavior` until emergence is verified.
- The evidence bundle carries `related_parties[]` (contract v0.3; v0.2 readers still parse it).
- At least one kyc_integrity (and ideally one TF) case appears in the slice.
- signal-watch re-vendors the slice and a case reaches the **≥2-leg determination bar from real signals** (not
  just gathered corroboration) — the §12 loop closes.

## Honesty governor

The substrate is **single-signal-separable** (composition is architecturally subsumed by network linkage —
substrate P16): this brief adds **determination-evidence breadth** (the legs a determination needs) +
**network richness**, NOT detection difficulty. Nothing here is a catch-rate / detection-lift improvement; the
value is **defensibility + KYC-control depth**, all synthetic and badge-labeled. If a framing reads as
"harder to detect / better catch," re-word.

## Pins / provenance

- aml-substrate @ **b53855c** (verified this session: `CONTRACT_VERSION="0.2"`, no `PartyGraphView` /
  `related_parties`, `source_of_funds` / anticipated / peer-income absent in `gen/`, C14 tautological).
- §12 gap aggregate **derived** (not asserted) via `scripts/evidence_requirements.py` `signal_brief()` over
  the committed 294-case population (signal-watch HEAD this phase).
- Supersedes `docs/substrate-bo-graph-emission-PLAN-BRIEF.md` (Phase 66, pinned @9d2e65c — its 3-part BO-graph
  ask is part 3 here).
- Consume-side: `data/osint/corpus.json` (the ownership mirror), `scripts/osint_tools.py` (`build_graph`),
  `workbench.html` (`gatherGraphHTML`), `scripts/evidence_requirements.py` (the atoms ← capabilities map).
