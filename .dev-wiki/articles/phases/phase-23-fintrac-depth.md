---
title: "Phase 23: FINTRAC depth — Operational Alerts + Operational Briefs"
aliases: ["phase-23-fintrac-depth"]
category: phases
tags: [corpus, multi-source, fintrac, depth, scale, gate, crown-copyright, operational-brief]
parents: [phase-22-fintrac-corpus-source]
created: 2026-06-06
updated: 2026-06-06
source: plan
status: active
scope: ["scripts/acquire_fincen.py", "data/fintrac/**", "scripts/derive_signals.py", "data/fintrac/corpus-status.json", "dist/corpus/index.html", "tests/**", "CLAUDE.md", "README.md"]
entry_criteria: "Phase 22 complete + accepted + committed (6765d26 + 7f6bc22); the corpus ships 35 derived across 39 publications via the CORPUS_SOURCES registry across 4 sources (FinCEN advisories + alerts + OFAC + FINTRAC); FINTRAC is registered as source #4 with 3 derived Operational Alerts; the quote-grounding gate normalize/check_record is source-agnostic + byte-frozen; the FINTRAC 'indicators' anchor add (Phase 22) + the OFAC widening (Phase 21) proved the narrow-global-anchor widening pattern holds with 0 regression; the FINTRAC Crown-copyright non-commercial reproduction basis is already established (NO non-negotiable change this phase). User chose FINTRAC depth at the goal gate (audience = a Canadian bank) + OAs + Briefs WITH the regression-gated widening at the scope gate."
exit_criteria: "≥5 new FINTRAC strategic-intel products (OAs + the real-estate Operational Brief) acquired (hand-curated index.json) → converted → derived via the inverted loop, each --check-derived clean, FINTRAC source 3 → ~8-11; the rf_region anchors widened for the new FINTRAC heading forms (narrow, specific, 0-collision — e.g. 'TABLE OF INDICATORS' for the briefs) with ZERO FinCEN/OFAC/existing-FINTRAC regression (all 35 prior records --check-derived clean, --selftest passes incl. new bidirectional FINTRAC fixtures, every prior md's rf_region byte-unchanged); --check all zero drift, the 3 other sources + the showcase byte-frozen; the harness counts updated (FINTRAC bucket 3→N, total/derived) + a FINTRAC Brief walks the arc; README + CLAUDE counts updated; NO non-negotiable change."
---

# Phase 23: FINTRAC depth — Operational Alerts + Operational Briefs

## Objective

Grow the existing FINTRAC corpus source #4 (`data/fintrac/`, doc_type "FINTRAC") from 3 derived
Operational Alerts to the full anchorable set of FINTRAC strategic-intelligence products carrying
enumerated ML/TF indicators — Operational Alerts AND Operational Briefs (incl. the real-estate brief).
This is "Canadian depth" for the demo's audience (a Canadian bank): the FINTRAC source goes 3 → ~8-11,
becoming the second-deepest source. Reuse the Phase-20 CORPUS_SOURCES registry, the inverted-loop
derivation, and the quote-grounding gate; the grounding core (normalize/check_record) stays
BYTE-UNTOUCHED — only the rf_region relevance anchors widen for new FINTRAC heading forms.

## Scope

The UNFREEZE (edits allowed):
- `scripts/acquire_fincen.py` — reuse `--source data/fintrac`; the FINTRAC `<slug>.pdf` URL form is
  already handled by the `_to_pdf_url` direct-download branch (Phase 22 confirmed; likely no edit).
- `data/fintrac/**` — GROW the source: NEW hand-curated index.json additions + NEW md + NEW derived
  records + a regenerated corpus-status.json (raw/ gitignored). The 3 EXISTING FINTRAC records stay
  byte-untouched.
- `scripts/derive_signals.py` — add a NARROW, SPECIFIC, 0-collision anchor per new FINTRAC heading form
  to `_RF_HEADER_FINTRAC`/`_RF_INTRO_FINTRAC` + new bidirectional fixtures. Anchors + fixtures ONLY —
  the grounding core (normalize/check_record) stays byte-untouched.
- `dist/corpus/index.html` — rebuilt output (data-driven; no template edit).
- `tests/**` — update the harness's hardcoded counts + add the real-estate Operational Brief walking
  the arc.
- `CLAUDE.md`, `README.md` — counts + the Operational-Brief inclusion + the heading-form widening.

NO structural `build.py` / `corpus.html` edit — the SELECT menu, doc_type chips, and count line are
already data-driven, so adding docs to the source flows through the merge automatically.

FROZEN byte-untouched: `index.html`, `config/**`, the 3 typology dists, `scripts/build.py` +
`corpus.html` (no structural edit), AND the THREE OTHER sources `data/fincen/**` +
`data/fincen-alerts/**` + `data/ofac/**` (mds + derived + corpus-status.json), AND the 3 EXISTING
`data/fintrac/` records (grow, don't modify).

## Exit Criteria

- [ ] ≥5 new FINTRAC strategic-intel products (OAs + the real-estate Operational Brief) acquired
      (hand-curated index.json) → converted → derived via the inverted loop, each `--check-derived`
      clean; FINTRAC source 3 → ~8-11
- [ ] rf_region anchors widened for the new FINTRAC heading forms (narrow, specific, 0-collision — e.g.
      "TABLE OF INDICATORS" for the briefs) with ZERO FinCEN/OFAC/existing-FINTRAC regression: all 35
      prior records `--check-derived` clean, `--selftest` passing incl. new bidirectional FINTRAC
      fixtures, every prior md's rf_region byte-unchanged (NO-OP if every new doc anchors as-is)
- [ ] `--check all` zero drift; the 3 other sources (`data/fincen/`, `data/fincen-alerts/`,
      `data/ofac/`) + the showcase byte-frozen
- [ ] the harness counts updated (FINTRAC bucket 3→N, total publications + derived) + a FINTRAC Brief
      walks the arc (Select→Coverage→Build-recs/gate→Signal→Close)
- [ ] README + CLAUDE counts updated (publications 39→39+N, derived 35→35+M, FINTRAC 3→N) + the
      Operational-Brief inclusion + the heading-form widening; NO non-negotiable change (the FINTRAC
      Crown-copyright basis is already documented)

## Constraints

- GATE REGRESSION (the load-bearing constraint): each new FINTRAC heading-form anchor MUST be NARROW +
  SPECIFIC + verified 0-collision across ALL 36 FinCEN+OFAC mds, keep all 35 existing records
  (12 advisory + 17 alert + 3 OFAC + 3 existing-FINTRAC) `--check-derived` clean + `--selftest` passing,
  AND every prior md's rf_region BYTE-UNCHANGED. (Prevents a permissive anchor from shifting an existing
  region — `check_record` treats `rf_region==None` as a HARD violation, the tightest coupling.)
- SUBTRACTION / ABORT: if a new heading form shifts ANY existing rf_region or fails ANY of the 35
  records, SKIP that doc (honest non-derivable) — do NOT broaden a shifting anchor. The narrow-global
  anchor was chosen OVER a source-scoped rf_region refactor (deferred); never let depth complexity
  contaminate the grounding core. (Prevents anti-subtraction anchor sprawl.)
- COMPLIANCE: NO non-negotiable change — the FINTRAC Crown-copyright NON-COMMERCIAL reproduction basis
  was established in Phase 22. NEVER reproduce a FINTRAC doc without its required attribution
  (© His Majesty the King in Right of Canada + complete title + author + "a copy of the version
  available at <URL>"). Keep the "Illustrative data & outputs" badge always-on; provenance stays
  source-aware (FINTRAC never shows "public domain"). (Prevents mislabeling FINTRAC's licence.)
- CORPUS IDENTITY: EXCLUDE FINTRAC's "Money laundering and terrorist financing indicators—<sector>"
  GUIDANCE pages (compliance guidance, NOT strategic-intelligence products). (Prevents blurring the
  strategic-intel corpus identity.)
- NEVER fabricate a BUILD_NOW — honest BUILD_NOW only where FI-observable; a SOURCE_DATA-heavy doc is
  honest, not a failure.
- BYTE-FROZEN: the 3 OTHER sources + the showcase + the 3 existing FINTRAC records. Grow the source via
  ADDED docs, not a migration. (Prevents churn on what works.)

## Checkpoints

- BASELINE-FIRST (T1): capture the FinCEN+OFAC+existing-FINTRAC rf_region baseline BEFORE any anchor
  change — it is the regression reference for T2.
- BEFORE COMMITTING each gate edit (T2): confirm the new anchor is 0-collision across all 36 FinCEN+OFAC
  mds, all 35 existing records + `--selftest` still pass, AND every prior md's rf_region is
  byte-unchanged. If ANY shifts → REVERT the anchor + SKIP that doc.

## Assumptions

- The candidate batch (human-trafficking/Project Protect oai-hts-2021, OCSE/Project Shadow exploitation,
  romance fraud/Project Chameleon, illegal wildlife trade, casino/Project Athena, the real-estate
  Operational Brief `real`) yields ~5-8 anchorable docs. The final set is finalized at acquisition by
  what anchors + grounds. If a doc has no enumerated ML/TF indicator list → honestly skipped (non-
  derivable, labeled like the 2 FATF advisories / 2 non-derivable alerts).
- FINTRAC serves a PDF at `<page-slug>.pdf` → the existing `acquire_fincen.py` `_to_pdf_url`
  direct-download branch handles it with NO tweak (Phase 22 confirmed); `pdf_to_md.py` provenance is
  already source-aware (FINTRAC = Crown-copyright, never "public domain"). If the URL form differs for a
  Brief → adjust `_to_pdf_url` minimally (acquisition is authoring-only).
- The OAs head their lists "Money laundering indicators" (ML/TF-qualified → anchors under the existing
  `_RF_HEADER_FINTRAC`). The real-estate Operational Brief was CONFIRMED this session to head its
  ~40-indicator list with bare "TABLE OF INDICATORS" → a new narrow anchor is needed. If false (a doc
  uses a form that cannot be anchored without shifting an existing region): SKIP that doc.

## Notes

- The CORPUS_SOURCES registry (Phase 20) + the Phase-21 OFAC + Phase-22 FINTRAC source adds proved the
  pattern: growing a source = ADD docs to its data dir + (for a new heading vocab) a narrow
  regression-gated anchor add. The gate (check_record / rf_region / normalize) is source-agnostic;
  `--corpus-status <source-dir>` already takes any source path.
- What's NEW vs Phase 22 (the FINTRAC source ADD): this is DEPTH within an established source, not a new
  source — NO non-negotiable change, NO architecture change, NO structural build.py/corpus.html edit.
  The genuinely new gate work is the SECOND FINTRAC heading form: bare "TABLE OF INDICATORS" (Operational
  Briefs) vs the OAs' ML/TF-qualified "Money laundering indicators". Each new form = one narrow,
  specific, 0-collision anchor.
- The deferred alternative (a source-scoped rf_region refactor, so anchors apply only to their own
  source) is noted as a future option if FINTRAC heading forms proliferate — chosen NOT to do it now
  (the narrow-global anchor is the proven Phase-21/22 pattern; the refactor earns its complexity only at
  more heading-form variety).
- WIKI: the FinCEN/FINTRAC advisory structure (typology overview → enumerated ML/TF indicators →
  reporting instructions) is the derivation surface (working-knowledge.md, uses:2) — the same surface for
  OAs and Operational Briefs. The red-flag→signal derivation pattern (indicator → coverage status →
  buildable candidate where cover=gap AND data=available → signal definition) and the quote-grounding
  gate (normalize(flag) ⊂ normalize(md) inside rf_region) are reused unchanged. No new cross-wiki
  retrieval this lite session; the Operational Brief is a strategic-intel product (same surface), the
  sector GUIDANCE pages are excluded by identity.
