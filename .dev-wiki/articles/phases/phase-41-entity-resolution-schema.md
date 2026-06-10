---
title: "Phase 41: Entity-resolution schema enrichment (live news)"
aliases: [phase-41, er-schema-enrichment]
category: phases
tags: [news-live, entity-resolution, schema, grounding-gate, duckdb, privacy]
parents: []
created: 2026-06-09
updated: 2026-06-10
source: plan
status: completed
scope: ["scripts/serve_news.py", "scripts/news_ground.py", "scripts/news_store.py", "scripts/build.py", "news.html", "tests/news_live_test.py", "tests/news-stream.test.mjs", "tests/fixtures/news-live/**", "docs/news-live.md", "tests/smoke-checklist.md", "CLAUDE.md"]
entry_criteria: "Phase 40 delivered + accepted + committed (ea53adc work + 760de35 gate flip) + pushed; 0 open tasks; direction set by user REFRAME at the dev-plan gate; assumption gate closed 2026-06-09 (A1 reject→A1' accept-with-conditions, A3 reject→A3'a/A3'b accept, A2/A4/A5 accept)."
exit_criteria: "Extraction schema + prompt enriched (aliases/properties/relationships/main_subject) and grounded-or-stripped by the shared gate; alias DROPs inverted to FOLDs; DuckDB anchor redesign with exact-name cross-scan accumulation; screen matches name ∪ aliases; live UI renders enrichment in the LIVE region only; offline dist/news + the 4 committed records + book.json byte-frozen; new .ph41 US-federal fixtures; full regate green; privacy boundary held."
---

# Phase 41: Entity-resolution schema enrichment (live news)

> **Progress (2026-06-10): READY FOR COMPLETION** — all 6 tasks T1–T6 [x], full regate GREEN
> (node news-stream 90→103, fixtures 10→13 w/ 3 .ph41 US-federal pairs, --check all 5/5 zero drift,
> --live real-Qwen smoke green), reviewer 9/10 ACCEPT zero HIGH+. Spec nana:approved 2026-06-09.
> Delivery gate PENDING — the delivery flow presents it, commits, then flips the gate.
> Session detail: [[2026-06-10-phase-41-entity-resolution-schema|journal]] (incl. D5, the user-ruled
> r2 prompt-regression fix: red_flags FIRST in EXTRACT_SCHEMA order under strict grammar).

## Objective

Enrich the LIVE news subsystem's entity scan schema for proper ENTITY RESOLUTION: entities gain
verbatim `aliases[]` (kept, not dropped) + `properties[]` `{kind, value}` from a closed kind vocab;
the record gains `relationships[]` `{from, to, label, evidence}` (~8-term closed relation vocab) +
a `main_subject` designation — everything grounded-or-stripped by the shared deterministic gate
(LLM proposes, gate disposes). The DuckDB store normalizes to the ANCHOR design with cross-scan
accumulation; screening becomes alias-aware.

The load-bearing reveal (round-1 A1 reject at the assumption gate): the system will be fed
PRIVATE INVESTIGATION NOTES, not just public articles — attribute slots are designed for that
domain (incl. `client_number` + `account_number`), not census-limited. Direction was a user
REFRAME off the offered candidates (FINTRAC /intel/ depth, flag-quality round 2, AUSTRAC/UK, QOL).

Full rationale + alternatives: the finalized decision article
`articles/decisions/phase-41-entity-resolution-schema.md` (confidence: high — do not re-derive).

## Approach (two-layer data model)

1. **Per-scan extraction JSON stays NESTED** (A1'): entities w/ `aliases[]` (verbatim) +
   `properties[]` `{kind, value}` — kind vocab: address, phone, email, client_number,
   account_number, dob, id_registration, wallet, domain (+ existing location/age/profession);
   record-level `relationships[]` `{from, to, label, evidence}` — relation vocab: co-conspirator,
   owner-or-controller-of, front-for, family-or-associate, employee-or-agent-of,
   professional-intermediary, counterparty, recipient-of-funds — + `main_subject`.
2. **DuckDB normalizes to ANCHORS** (A3'b): entity anchor table (+ entity SOURCE TYPE:
   gov-enforcement / commercial-news / investigation-note — document types differ in significance)
   + ONE monolithic property association table (anchor_id × kind × value edge, detail JSON column,
   evidence + scan provenance + grounded status; confidence column RESERVED/NULL — never
   model-populated until a measured basis; per-property subtables only on measured divergence)
   + a relationship edge table. Exact-normalized-name cross-scan ACCUMULATION now; fuzzy
   cross-scan MERGE adjudication DEFERRED.
3. **Gate** (D3): alias verbatim-grounding; properties grounded-or-stripped; relationship
   evidence grounded + from/to referential integrity + closed label vocab (label stays a neural
   judgment — vocab-checked, never correctness-checked: the C/D-code split); main subject =
   the enforcement action's target, multi-subject honest. Alias handling INVERTS: today's
   alias-dedup DROP (token-subset names) + moniker DROP become FOLDs onto the fuller entity's
   aliases; screening matches name ∪ aliases (max score).
4. **Privacy boundary** (D4/A5): private/client data is a first-class INPUT confined to the
   local live layer — gitignored DuckDB + live session, local 127.0.0.1 model (notes never leave
   the machine); never committed, never fixture-promoted (fixtures stay US-federal public-domain
   only), never in ship artifacts.

## Scope

Files and modules affected:
- `scripts/serve_news.py` — EXTRACT_SCHEMA + SYSTEM_PROMPT + /watchlist + source-type plumbing
- `scripts/news_ground.py` — gate extensions + alias-fold inversion (shared w/ build.py)
- `scripts/news_store.py` — anchor redesign (anchors / entity_properties / entity_relationships)
- `scripts/build.py` — shared-gate consequence only (validate_news_data)
- `news.html` — LIVE region only (source-type selector, entity cards, relationship view)
- `tests/news_live_test.py`, `tests/news-stream.test.mjs`, `tests/fixtures/news-live/**`
- `docs/news-live.md`, `tests/smoke-checklist.md`, `CLAUDE.md` (T6 in-place snapshot edit)

## Exit Criteria

- [x] Extraction schema + prompt carry aliases[]/properties[]/relationships[]/main_subject with closed vocabs + committed-record exemplars; `serve_news.py --selftest` PASS
- [x] Shared gate grounds-or-strips every new field; alias DROPs → FOLDs; the 4 committed records pass with new fields optional; `news_ground.py --selftest` + `build.py news` + `--check news` PASS
- [x] DuckDB anchor design live: anchors (+source_type) / monolithic entity_properties (confidence NULL-reserved) / entity_relationships; two scans same entity → one anchor w/ accumulated provenance; parquet export updated; store `--selftest` PASS
- [x] `/watchlist` returns aliases + source_type provenance; live Screen matches name ∪ aliases (max score)
- [x] Live UI renders enrichment in the LIVE region only; offline strip intact; offline `dist/news` byte-identical
- [x] NEW `.ph41` US-federal captures; old goldens regenerate deterministically (old qwen.json captures default-empty for new fields); docs + smoke-checklist + CLAUDE.md updated; full regate green (`--check all` 5/5 + all selftests + both node harnesses)

## Constraints

- Offline demo artifacts BYTE-FROZEN this phase (A3'a): `dist/news`, the 4 committed derived news records, `book.json` — enrichment renders in the companion live region only. Prevents: ER complexity leaking into the ship artifact.
- Privacy boundary (D4): nothing private committed / fixture-promoted / shipped. Prevents: violating the "no real customer data, ever" non-negotiable.
- Replay-fixture seam: prompt/schema changes never force re-capture; new fields default-empty for old captures. Prevents: invalidating the 10-fixture replay corpus.
- Confidence column stays RESERVED/NULL. Prevents: an unmeasured neural number presented as real.
- The global enforce hooks require an APPROVED SPEC (`/spec --internal`) BEFORE implementation edits — first implementation step.

## Checkpoints

- A gate extension failing a committed record: STOP — it is a FINDING to adjudicate, never a silent loosening.
- If offline `dist/news` cannot stay byte-identical after the live-region edits: STOP and surface it.

## Assumptions

- A1' (accept-with-conditions): two-layer model — nested per-scan JSON + anchor-normalized store. If the nesting fights the gate: revisit at the T2 boundary, don't flatten silently.
- A3'a/A3'b: offline byte-frozen + exact-name accumulation only. If fuzzy merge proves necessary mid-phase: defer it anyway (it is explicitly out of scope).
- A2/A4/A5: gateability of relationships, alias-fold inversion, privacy confinement — accepted as designed.

## Open Questions / Deferred

None blocking. Deferred: fuzzy cross-scan merge adjudication · confidence-column population basis ·
per-property subtable split criteria · an offline-demo enrichment phase · AUSTRAC/UK + FINTRAC
/intel/ (carried corpus candidates) · CLAUDE.md trim (279 lines, hygiene half-task).

## Notes

Stub `phase-41-direction-open.md` replaced by this article 2026-06-09 (direction chosen).
Active knowledge carried in-phase: aml-wiki money-laundering-red-flags stays the mechanism-vocab
source; committed gate-passing records are the few-shot exemplar source (anchor-style-to-reference);
`news_ground.py` is the SHARED gate — blast radius = 4 committed records + 10 replay goldens;
prompt-shaping-beats-overfit-filter (context-shape before post-hoc filters; test precision rules on
NEW data).
