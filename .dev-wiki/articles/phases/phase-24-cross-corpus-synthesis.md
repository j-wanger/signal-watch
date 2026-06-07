---
title: "Phase 24: Cross-corpus synthesis — a typology lens over the multi-source corpus"
aliases: ["phase-24-cross-corpus-synthesis"]
category: phases
tags: [corpus, multi-source, synthesis, typology, cross-jurisdiction, coverage, honesty, corpus-explorer]
parents: [phase-23-fintrac-depth]
created: 2026-06-07
updated: 2026-06-07
source: plan
status: complete
delivery: accepted
scope: ["data/typology-map.json", "scripts/build.py", "corpus.html", "dist/corpus/index.html", "tests/**", "CLAUDE.md", "README.md"]
entry_criteria: "Phase 23 complete + accepted + committed (b0fcda4); the demo is at Definition of Done — a 4-source / 2-jurisdiction corpus (42 derived across 46 publications: 12 FinCEN advisories + 17 alerts + 3 OFAC + 10 FINTRAC) via the CORPUS_SOURCES registry; the corpus explorer presents docs as a flat per-document arc. No carried scope debt. User invoked /dev-plan for a net-new stakeholder ask and chose cross-corpus synthesis at the goal gate (highest net-new value for the Canadian-bank audience, now that the corpus spans two jurisdictions)."
exit_criteria: "data/typology-map.json overlays a closed-vocab typology onto every live derived doc, validated at the build boundary (closed vocab + referential + full coverage, fail-loud); ≥2 genuine cross-jurisdiction clusters confirmed (or the degrade path taken); corpus.html renders a cross-corpus synthesis view (group-by-typology → cluster → honest COMBINED coverage + per-jurisdiction contribution, drill-through to the per-doc arc) with NO fabricated similarity/overlap/lift metric; the per-doc arc unbroken; --check all zero drift; the 4 source dirs + 42 derived + the grounding core derive_signals.py + the showcase byte-frozen; the harness extended for a cross-jurisdiction cluster; CLAUDE + README updated; NO non-negotiable change."
---

# Phase 24: Cross-corpus synthesis — a typology lens over the multi-source corpus

## Objective

Turn the 4-source / 2-jurisdiction corpus (42 derived across 46 publications) from 46 isolated
documents into an analytical tool. Synthesis groups documents by TYPOLOGY and shows the COMBINED
coverage across the cluster — the genuinely new insight being **no single advisory covers a typology;
the combined corpus does** (uniquely enabled now that the corpus spans FinCEN + OFAC + FINTRAC, US +
Canada). The payoff reuses the existing per-indicator coverage math as honest UNION arithmetic
(already disclosed-illustrative under the always-on badge). The per-document 5-screen arc (Phase 18)
stays the spine; the typology lens is additive.

## Scope

The UNFREEZE (edits allowed):
- `data/typology-map.json` — NEW committed overlay artifact: doc-id → exactly one typology from a
  closed vocabulary (the vocab declared in the file). A SEPARATE overlay, NOT edits to the 42 derived
  records — so the source dirs + derived records stay byte-frozen.
- `scripts/build.py` — (1) validate the typology map at the build boundary (closed vocab + referential
  integrity + total live-doc coverage, fail-loud, mirroring the existing derived-shape validation);
  (2) merge each doc's typology into `__CORPUS__`. First structural `build.py` touch since Phase 20.
- `corpus.html` — the cross-corpus synthesis view: a group-by-typology entry from Select → a typology's
  cross-jurisdiction document cluster + COMBINED coverage + per-jurisdiction contribution, drill-through
  to each doc's existing per-doc arc.
- `dist/corpus/index.html` — rebuilt output.
- `tests/**` — extend the harness for a cross-jurisdiction cluster (honest combined coverage,
  per-source traceability, no fabricated number, per-doc arc regression-clean).
- `CLAUDE.md`, `README.md` — the overlay artifact + the synthesis view + the honesty constraint.

FROZEN byte-untouched: `index.html`, `config/**`, the 3 typology dists, the grounding core
`scripts/derive_signals.py` + the authoring scripts (`acquire_fincen.py`, `pdf_to_md.py`,
`crawl_fincen.py`), ALL 4 source dirs (`data/fincen/**`, `data/fincen-alerts/**`, `data/ofac/**`,
`data/fintrac/**` — mds + derived + corpus-status.json), and the six-act showcase. The typology label
is an OVERLAY, not a migration.

## Exit Criteria

- [ ] `data/typology-map.json` overlays a closed-vocab typology onto every live derived doc, validated
      at the build boundary (closed vocab + referential + full coverage, fail-loud)
- [ ] ≥2 genuine cross-jurisdiction clusters confirmed (≥2 typologies × ≥2 jurisdictions) — or the
      degrade path (same-jurisdiction cross-doc-type clusters) recorded
- [ ] `corpus.html` renders a cross-corpus synthesis view (group-by-typology → cluster → honest
      COMBINED coverage + per-jurisdiction contribution, drill-through to the per-doc arc) with NO
      fabricated similarity/overlap/lift metric
- [ ] the existing per-document 5-screen arc is unbroken (regression-clean)
- [ ] `--check all` zero drift; the 4 source dirs + 42 derived records + the grounding core
      `derive_signals.py` + the showcase byte-frozen
- [ ] the harness extended for a cross-jurisdiction cluster (honest combined coverage + traceability)
- [ ] CLAUDE + README document the overlay + synthesis view + the honesty constraint; NO non-negotiable
      change

## Constraints

- HONESTY GATE (the load-bearing constraint, ties to the Phase-18 precision-lift rejection): NO
  similarity %, NO overlap score, NO correlation/lift number anywhere in the synthesis. Show ONLY
  (a) combined coverage as honest set arithmetic over the existing per-indicator status, disclosed-
  illustrative under the always-on badge; (b) honest per-jurisdiction contribution counts; (c) every
  clustered indicator traceable to its source doc + jurisdiction. If a beat needs a fabricated number
  to land, CUT the beat. (Prevents reintroducing the exact fabrication Phase 18 rejected.)
- SUBTRACTION: the typology overlay is a SEPARATE committed `data/typology-map.json`, NOT 42 derived-
  record edits — so the source dirs + derived records + the grounding core stay byte-frozen. Validate
  at the build boundary (where derived shape is already validated), not in the grounding gate. (Prevents
  churn on what works + keeps the grounding core untouched.)
- BUILD-BOUNDARY GATE: the map is fail-loud-validated at build (closed vocab + referential integrity +
  total coverage). Agent proposes the map; the deterministic gate disposes; the user reviews. (Keeps
  "agent proposes, human disposes" — the typology label is a categorization, fully traceable to the
  doc's stated subject; no fabrication surface.)
- PER-DOC ARC PRESERVED: the synthesis lens is ADDITIVE; the existing 5-screen per-doc arc stays the
  spine and stays regression-clean. (Prevents breaking the proven artifact.)
- NO non-negotiable change: the always-on "Illustrative data & outputs" badge stays; the verbatim
  US-federal-public-domain + FINTRAC-Crown-copyright bases are unchanged; combined coverage is
  illustrative, not real.

## Checkpoints

- CLUSTER-VERIFY-FIRST (T1, the load-bearing checkpoint): build the typology map, tabulate typology →
  {sources, jurisdictions}, and CONFIRM ≥2-3 typologies span ≥2 jurisdictions BEFORE T2 builds any UI.
  If not → DEGRADE to same-jurisdiction cross-doc-type clusters (e.g. a FinCEN advisory + its ransomware
  alerts) or report back. (De-risks the weakest assumption: that compelling cross-jurisdiction clusters
  exist.)
- HONEST-OR-CUT (T2): for each synthesis beat, confirm it lands on honest arithmetic + traceability
  alone. If it needs a fabricated metric → CUT it.

## Assumptions

- The corpus has ≥2-3 typologies that genuinely span ≥2 jurisdictions. STRONG priors: terrorist
  financing (FINTRAC TF OA ↔ FinCEN ISIS fin-2025-a001 + Iran fin-2024-a001) and ransomware (a FinCEN
  advisory + its alerts, cross-doc-type within FinCEN). Breadth (synthetic-opioids, human-trafficking,
  fraud) is UNVERIFIED → T1 verifies. If false → the degrade path.
- A single closed-vocab typology label per live derived doc is enough to cluster meaningfully (doc
  subjects are sharply scoped — an OA/advisory is about one typology). If a doc straddles two typologies,
  pick the primary; per-indicator multi-tagging is explicitly OUT (heavy, LLM-judgment-laden, would
  touch 42 records — rejected by the subtraction test).
- The existing per-indicator coverage status (covered/partial/gap) aggregates honestly across a cluster
  as a union (a typology is "covered" by the cluster if any clustered doc covers that indicator's
  behavior). Combined coverage is set arithmetic, not a model output — no fabrication.

## Notes

- The genuinely new capability vs every prior phase: prior phases SCALED the corpus (more sources, more
  depth); this phase makes the accumulated scale ANALYTICAL — the first cross-document relationship in
  the corpus. The 2-jurisdiction breadth (Phase 22/23 FINTRAC) is the precondition that makes "the
  combined corpus covers what no single regulator does" an honest, demonstrable claim.
- Phase 18 EXPLICITLY REJECTED precision/combination-lift for the corpus (the records carry no
  precision/lift numbers; porting the showcase's lift beat would fabricate ~12 per-advisory stats).
  This phase honors that: the payoff is COMBINED COVERAGE (honest union), NOT combination-lift. The
  honesty gate here is the same non-negotiable ("never present synthetic numbers as real").
- The build.py-boundary gate (vs the originally-proposed derive_signals.py gate) is a refinement made at
  planning: it keeps the grounding core derive_signals.py byte-frozen and puts the overlay validation
  where derived-shape validation already lives. Same direction, tighter frozen set.
- The group-by-typology view incidentally eases the 46-doc flat-SELECT-menu watch-item (a soft
  observation carried from Phase 23) — a side benefit, NOT a goal; scope stays on synthesis.
- WIKI: the FinCEN/FINTRAC advisory structure (typology overview → enumerated ML/TF indicators) is the
  derivation surface (working-knowledge.md, uses:2) — each doc is sharply scoped to one typology, which
  is exactly what makes a single closed-vocab label per doc sufficient for honest clustering. The
  red-flag→signal derivation pattern + the quote-grounding gate are reused UNCHANGED (derive_signals.py
  frozen). No new cross-wiki retrieval this lite session.
