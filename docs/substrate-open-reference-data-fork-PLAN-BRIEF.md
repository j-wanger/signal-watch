# PLAN-BRIEF — aml-substrate: the open-reference-data fork (anchor the synthetic universe to open data)

> **A signal-watch → aml-substrate handoff brief** (the Phase-55–58 / 74–76 pattern: signal-watch authors the
> contract; the sibling implements + measures it on its own lifecycle — *no code lands in substrate from here*).
> Synthetic / illustrative; **no catch-rate, lift, or precision asserted.** **Pinned to verified substrate HEAD
> `f2da3e4` (Phase 30), code-verified 2026-06-26.** Source: the open/openly-licensed reference-dataset survey
> (permissive core + two NC/ND landmines). Companion to [`cross-pillar-build-order.md`](cross-pillar-build-order.md).

## Why a FORK, not a trunk change

Substrate today is **purely procedural** (verified `@f2da3e4`): synthetic name pools (`gen/names.py`
`GIVEN_NAMES`/`SURNAMES`), synthetic business names + a 12-item `NAICS` list, synthetic emails/phones with a
**calibrated collision noise floor** (`gen/identity.py`, 0.04/0.06/0.10 + the deliberate controller-cluster
SHARES), an 18-city hardcoded geo distribution. **No real-reference ingestion** (grep-confirmed: `sanctions_flag`
is dead, no GLEIF/OFAC/Census/OSM). This is the **license-safe default and should stay the trunk.**

The **fork** is an open-reference-**anchored** variant where a synthetic entity's name / address / jurisdiction /
ownership / sanctions-exposure all cohere AND trace to real open data — **without ingesting any real PII** (the
"synthetic-but-anchored" pattern: generate synthetic, *attach* real reference attributes; real company/sanctions
names are public reference data, never customer data).

A fork (not a trunk edit) because: (1) it's additive realism on a **different axis** than the emission contract —
the trunk's `gen/` is frozen + manifest-guarded, and the seams plug in at the *pools/config*, not the engine;
(2) it carries **licensing constraints** the pure-synthetic trunk doesn't; (3) **consumers read the same emission
shape** (v0.5 bundles + `true_entities` + `intended_disposition`) whether values are procedural or anchored — so
the fork **does not touch the cross-pillar contract** (orthogonal to the Phase-29/30 consume).

## The license-safe core (build on these — all free, on-prem, commercial-OK)

- **Ownership backbone:** GLEIF LEI Golden Copy (**CC0**) — L1 real names/addresses/jurisdictions, **L2
  who-owns-whom edges**. + Corporations Canada (OGL-Canada), Companies House (open), SEC EDGAR (PD).
- **Names:** US Census surnames + SSA given names (PD), frequency-weighted; Faker `en_CA`/`fr_CA` (MIT);
  Wikidata (CC0).
- **Geo/address:** OpenStreetMap (ODbL), OpenAddresses (per-source — check each), GeoNames (CC-BY), Natural
  Earth (PD); parse/normalize with libpostal (MIT).
- **Red-flag anchors (government, free):** OFAC (PD), EU/UN (free), **FCDO UK Sanctions List** (free — repoint
  off the now-closed OFSI list), **Consolidated Canadian Autonomous Sanctions List** (free), FATF black/grey
  (live), FINTRAC operational alerts (OGL), FinCEN advisories (PD).
- **Financial reference:** ISO 4217/3166, MCC via `python-iso18245` (MIT), ISO 20022 external code sets (free),
  Payments Canada institution numbers (real 3-digit + synthetic transits), GLEIF BIC-to-LEI mapping.

## The four traps (route AROUND — the bank-commercial landmines)

- **OpenSanctions bulk = CC-BY-NC** → a bank's internal AML screening **counts as commercial use** (no
  exemption). Use the government source lists above for the anchor + **Wikidata (CC0) for PEPs**; only license
  OpenSanctions if you specifically want the consolidated FtM/yente graph.
- **TI CPI = CC-BY-ND** → internal country-risk lookup OK; do NOT blend into a redistributed derived dataset.
- **ICIJ Offshore Leaks = ODbL + CC-BY-SA** (share-alike) → fine internally; caution if redistributing a blend.
- **OpenCorporates = paid** + ~half its sources offline + no UBO → prefer GLEIF + national registries.

## The five anchoring seams (verified `@f2da3e4` — plug in here; the `gen/` engine stays frozen)

1. **`gen/names.py` person pools** (`GIVEN_NAMES`/`SURNAMES`, 40-item lists) → Census/SSA frequency-weighted
   real-name pools (load from a file; scale to n without overfitting).
2. **`gen/names.py` org name + `NAICS`** (12-item) → GLEIF / Corporations-Canada real legal names + sector
   (filter by jurisdiction; sample real LEI+legal_name; keep address/BO assignment procedural).
3. **`gen/identity.py` contact collision rates** (0.04/0.06/0.10) → calibrate against real sharing rates
   (household / recycled-number); **keep the deliberate controller-cluster SHARES** (the ER signal).
4. **`gen/population.py` geo** (18-city hardcoded weights) → Census metro distribution; OSM/OpenAddresses for
   real street-level addresses (where the source license permits).
5. **The red-flag anchor (the dead `sanctions_flag` made live):** wire a deterministic SUBSET of synthetic
   entities to MATCH a real listed name/alias/jurisdiction (OFAC / Canada / FATF) so a sanctions screen
   genuinely hits — and tag jurisdictional risk from the live FATF grey/black + EU non-cooperative lists.

## The payoff for the program (why this serves the north star)

- The **merge console's REAL cases** today are substrate's *artificial* collision noise floor. Anchoring →
  **real-shaped collisions** (real shared addresses, real corporate-registration overlaps, Census-frequency name
  clashes) → the merge gate adjudicates *realistic* ER ambiguity, and substrate's `true_entities` oracle stops
  being the trivial `entity_ref`-restatement it is today (it could express a genuine same-person-across-refs case).
- **GLEIF L2 ownership** → the real ownership-graph layer the decisioning lever (network + source of funds)
  traverses — the Northgate/Lakeshore separation made real-data-grounded.
- **Real sanctions/PEP anchors** → genuine watchlist-exposure red flags (the dead `sanctions_flag` made live).

## Boundary + staging

- **Contract-neutral:** the emission shape (v0.5 bundles + `true_entities` + `intended_disposition`) is
  UNCHANGED — consumers behave identically. This fork is realism of *values*, not *contract*.
- **Synthetic-but-anchored, internal-only:** NO real PII ever; always-on illustrative posture. Internal-only use
  keeps it license-simple — **re-examine every NC/ND/SA source IF the platform is ever redistributed or sold.**
- **Stage 1 — the permissive core** behind seams 1–4 (GLEIF + Census + OSM + GeoNames); measure the realism
  delta vs the procedural trunk.
- **Stage 2 — the red-flag anchor** (seam 5: deterministic real-list matches + FATF/EU jurisdiction tags).
- **Stage 3 — the paid-landmine decisions** (OpenSanctions consolidated graph / SWIFT Ref / Payments Canada FIF /
  provincial registries) — only if redistribution or the consolidated-graph need actually materializes.

**Pin: `f2da3e4`** · executed in an **aml-substrate fork session** · contract-neutral (signal-watch/casework
consume the same shape). **Out of scope:** any change to the v0.5 emission contract, the determination engine, or
the 8+1 signal-watch dists.
