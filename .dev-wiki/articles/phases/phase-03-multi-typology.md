---
title: "Phase 3: Multi-typology (M2)"
aliases: []
category: phases
tags: [milestone-m2]
parents: []
created: 2026-06-04
updated: 2026-06-04
source: plan
status: completed
scope: ["config/typologies/*.json", "scripts/build.py", "dist/**"]
entry_criteria: "M1 complete — engine is generic against config."
exit_criteria: "≥2 typologies present and switchable (build-time) with no engine edits; arc + both wow beats hold for TBML."
---

# Phase 3: Multi-typology (M2)

## Objective

Author at least one more typology (pig-butchering and/or trade-based) as config from
public, paraphrased advisory material, and add a selector or build-time switch.

## Scope

- `config/typologies/pig-butchering.json` and/or `config/typologies/trade-based.json`
- selector entry or `?typology=` build switch

## Exit Criteria

- [x] second typology authored from public advisory material (paraphrased) — TBML
- [x] build-time switch added (`dist/<id>/index.html`) + build-boundary validation
- [x] six-act arc and both wow beats verified for TBML (and fentanyl regression byte-identical)
- [x] adding the typology required NO engine edits — `git diff index.html` empty (proves the M1 contract)

## Constraints (HANDOFF §4)

- Advisory text public-source and PARAPHRASED. No real customer/transaction data.
  Prevents: copyright + compliance breach.

## Notes

Resolved: second typology = **Trade-based ML (TBML)** (aml-wiki: 27 articles, dated public
advisories — FinCEN Apr-2025 fentanyl↔TBML, FATF 2024; signals map to bank data; flows from
the fentanyl anchor). Switch = **build-time** (`dist/<id>/index.html`), no runtime selector.
Build-time validation added to build.py (deterministic boundary validator).

Buildable target signal (from survey): price-anomaly in multi-invoice shipments (gap +
data-available). Lift composition: related-party trade × high-risk corridor × price anomaly.
Author from PARAPHRASED public sources — no verbatim advisory text.
