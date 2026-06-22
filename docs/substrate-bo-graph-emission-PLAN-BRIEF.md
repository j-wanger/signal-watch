# PLAN-BRIEF — aml-substrate: beneficial-owner / ownership-graph EMISSION

> **A signal-watch → aml-substrate handoff brief** (the Phase-55–58 sibling-brief pattern). Authored in
> signal-watch (Phase 66); **executed in an aml-substrate session**. signal-watch defines the *contract* it
> needs; the substrate owns the build. Pinned to **aml-substrate@9d2e65c** (verified live this session).
>
> **Why this is the #1 lever.** A two-repo richness recon (Phase 66) found the substrate is
> *single-signal-separable* (composition is architecturally subsumed by network linkage — substrate P16):
> more cases / typologies / detectors add *visible volume*, **not** detection difficulty. The richness that
> *compounds* — for the demo and for real detection leverage — is the **network**: beneficial owners,
> directors, nominee chains, ownership %. That graph is **already generated** but neither projected to
> detectors nor emitted in the evidence bundle (a recorded gap). Closing it is the highest demo-richness +
> KYC-control value per unit effort (recon estimate ~3–4 days).

## What exists today (code-verified @9d2e65c)

- **The graph IS generated.** `gen/population.py:184-197` draws, per Organization, beneficial owners (≥ a
  threshold, with `ownership_pct`) + a director from existing persons, as `RelationshipEdge`s:
  - `RelationshipEdge(src_id=owner_pid, dst_id=org_id, label=BENEFICIAL_OWNER, attrs={"ownership_pct": pct})`
  - `RelationshipEdge(src_id=owner_pid, dst_id=org_id, label=DIRECTOR_OF, attrs={})`
- **The schema is clean.** `schema/graph.py:16-24` — `RelationshipEdge{src_id, dst_id, label, edge_id?,
  attrs:dict, valid_from?, valid_to?}`; `schema/enums.py` `RelationshipLabel` includes `BENEFICIAL_OWNER`,
  `DIRECTOR_OF`, `OFFICER_OF`, `CONTROLS`, `OWNS`, `ON_BEHALF_OF`, `SHARES_*`, `SAME_AS`.
- **It is NOT exposed.** No `PartyGraphView`; the detectors' `PartyView` (`monitor/detectors/views.py`)
  projects 16 flat KYC fields but **no ownership edges**.
- **It is NOT emitted.** The v0.2 evidence bundle carries `parties[]` = the **subject only** (16-field
  PartyView); no related parties, no ownership edges.
- **C14 is tautological today.** The KYC-integrity detector (substrate P19 finding) fires on EDD accounts,
  but `cdd_level==EDD ⇔ risk_rating==HIGH` by construction and `source_of_funds` is never populated — a
  static construction artifact, not an emergent KYC-integrity signal. A BO-disclosure gap is the *real*,
  non-tautological KYC-integrity signal waiting to be built.

## The ask (three parts)

### 1. EXPOSE — a `PartyGraphView` projection
Add a view that projects, for a subject party, its **declared ownership/control graph** from the existing
`RelationshipEdge`s: the beneficial owners + directors + officers + controllers of the subject (if the
subject is an Org), and — for a Person subject — the Orgs they beneficially own / direct. Shape (one row
per edge), mirroring `RelationshipEdge` so nothing is invented:
```
related_party = { "party_id": str, "label": RelationshipLabel, "ownership_pct": int|null,
                  "is_person": bool, "risk_rating": str, "cdd_level": str, "pep_tier": str,
                  "sanctions_flag": bool, "adverse_media_flag": bool }
```
The KYC fields on each related party reuse the existing `PartyView` projection (no new KYC generation).

### 2. EMIT — `related_parties[]` in the evidence bundle (contract v0.2 → v0.3)
Add a `related_parties[]` block to the evidence bundle alongside `parties[]`: the subject's declared
ownership/control edges (the `PartyGraphView` rows above). Bump the contract version (v0.2 → v0.3); keep
v0.2 readers working (the block is additive / optional). `meta.synthetic` stays true.

### 3. DETECT — a **non-tautological** C14 BO-disclosure detector
Author a KYC-integrity screening detector over the ownership graph that fires on a **real disclosure gap**,
NOT the `cdd_level↔risk_rating` tautology. Candidates (pick the one that genuinely *emerges*, measurement-
first per substrate doctrine — do **not** stamp it):
- a beneficial owner who is **high-risk / PEP / sanctions-or-adverse-flagged** but the *org's* `cdd_level`
  is below EDD (an under-classified entity given its ownership);
- an org with a **missing/incomplete BO disclosure** (no `BENEFICIAL_OWNER` edge ≥ the disclosure
  threshold while the org transacts at scale);
- a **nominee chain** (a director/BO who is BO/director of many orgs — a structural fan-out).
Bind it to a corpus indicator via aml-casework's `grounding_replay` (the cross-pillar grounding contract);
report it as `needs-behavior` until emergence is *verified*, never stamped (substrate P19 discipline).

## The contract signal-watch consumes (and already renders)

The emitted `related_parties[]` maps **1:1** onto the network view signal-watch already ships. Phase 66's
GATHER OSINT corpus (`data/osint/corpus.json`) was authored to **mirror this exact shape** — its ownership
records carry `{src, dst, label∈RelationshipLabel, ownership_pct}` edges, and `osint_tools.build_graph` +
`workbench.html` already render them as labeled, ownership-weighted graph edges. So:

| substrate emits | signal-watch renders (today, over the synthetic OSINT stand-in) |
|---|---|
| `related_parties[].label` (BENEFICIAL_OWNER / DIRECTOR_OF / …) | the network edge label |
| `related_parties[].ownership_pct` | the edge weight / annotation |
| `related_parties[].party_id` + KYC fields | the node + its risk chips |

**When the real BO graph lands, the workbench network view needs no rework** — the synthetic OSINT corpus is
its rendering prototype. That coherence is the point of bundling this brief into Phase 66.

## Acceptance (the cross-pillar seam)

- The substrate evidence bundle for an Org subject (and a Person who owns/directs an Org) carries a
  non-empty `related_parties[]` with `BENEFICIAL_OWNER`/`DIRECTOR_OF` edges + `ownership_pct`.
- The contract version is bumped (v0.2 → v0.3); v0.2 consumers still parse the bundle.
- The C14 BO-disclosure detector fires on a *measured* disclosure gap (not the EDD tautology), grounded via
  aml-casework `grounding_replay` to a corpus indicator.
- signal-watch can vendor a related-parties-bearing bundle into `data/workbench/` and the workbench network
  view renders the emitted edges with **no consume-side code change** (the Phase-66 OSINT shape holds).

## Honesty governor

This brief adds **network richness** — the dimension that compounds — **not** detection difficulty. The
substrate is single-signal-separable; the BO graph does not change that, and nothing here should be framed
as a catch-rate / detection-lift improvement. The value is **defensibility + KYC-control depth + a richer,
auditable investigator network**, all of it synthetic and badge-labeled.

## Pins / provenance
- aml-substrate @ **9d2e65c** (src/ byte-identical to the f90bd39 gen pin signal-watch vendors).
- Generated-but-unprojected: `gen/population.py:184-197`, `schema/graph.py:16-24`, `schema/enums.py`
  (`RelationshipLabel`). The PartyView gap: `monitor/detectors/views.py`. The tautological-C14 finding:
  substrate P19 / `docs/corpus-coverage-build-PLAN-BRIEF.md`.
- Consume-side mirror: signal-watch `data/osint/corpus.json` (ownership records) + `scripts/osint_tools.py`
  (`build_graph`) + `workbench.html` (`gatherGraphHTML`), Phase 66.
