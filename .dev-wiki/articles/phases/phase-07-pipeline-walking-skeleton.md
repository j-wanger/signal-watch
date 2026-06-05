---
title: "Phase 7: Pipeline walking skeleton (M6)"
aliases: [signal-watch-pipeline-slice]
category: phases
tags: [milestone-m6, pipeline, fincen, ingestion, signal-watch]
parents: []
created: 2026-06-04
updated: 2026-06-04
source: plan
status: completed
scope: ["data/fincen/**", "config/typologies/*.json", "index.html", "scripts/**", "config/schema.md", "dist/**"]
entry_criteria: "M5 shipped (single-file per-typology dist runs offline; compliance gate passed). The scripted ship artifact is the demo this slice feeds real data into."
exit_criteria: "FinCEN EFE FIN-2022-A002 acquired as PDF; converted to data/fincen/<id>.md (full verbatim article = source of truth); one schema-valid config/typologies/elder-financial-exploitation.json hand-derived from it; the engine renders the FULL verbatim advisory in Act 1's existing SOURCE DOCUMENT panel (bounded scrollable, attributed 17 USC §105, separated from the illustrative badge); 'Signal Engine'→'Signal Watch' rebrand; all three built dist still run offline from file://, no console errors."
---

# Phase 7: Pipeline walking skeleton (M6)

## Objective

Thin vertical slice of the "Signal Watch" ingestion pipeline on ONE real FinCEN
advisory — **EFE FIN-2022-A002** (Elder Financial Exploitation; 24 enumerated red
flags = the cleanest single-signal derivation surface) — end to end: acquire (PDF) →
convert (PDF→markdown, persisted as the source of truth) → hand-derive ONE schema-valid
frontend signal config → render the FULL verbatim advisory in Act 1's existing SOURCE
DOCUMENT panel. Proves the pipe on ONE item before widening the scraper or automating
derivation (both explicitly later phases). "Signal Engine" → "Signal Watch" rebrand rides along.

This encodes the project identity pivot: from a hand-authored scripted dramatization to a
public-data-seeded ingestion pipeline whose demo output is the existing frontend — designed
to later take real data. Provenance upgrades stakeholder buy-in.

## Scope

- `data/fincen/raw/<id>.pdf` — NEW. The acquired advisory PDF (authoring-only).
- `data/fincen/<id>.md` — NEW. Full advisory as markdown, persisted as source of truth.
- `scripts/**` — a single-fetch acquire step + a PDF→markdown convert step (open-source
  converter, authoring-only). `build.py` validates `advisory_full` at the boundary and
  inlines a larger article; the self-contained guard must still pass.
- `config/typologies/elder-financial-exploitation.json` — NEW. One hand-authored,
  schema-valid signal derived from the full article (human-authored, NOT auto-extracted),
  with a NEW `advisory_full` field carrying the verbatim EFE text.
- `index.html` + `config/schema.md` — NEW top-level `advisory_full` field; Act 1's existing
  SOURCE DOCUMENT panel (`.doc`/`#doctext`, ~lines 337-353) renders it as a BOUNDED
  SCROLLABLE region (max-height + overflow-y; `.stage` has no overflow today); a distinct
  "public domain · verbatim · FinCEN FIN-2022-A002" attribution kept visually separate from
  the always-on "Illustrative data & outputs" badge; `validateConfig()` gets a defensive
  default for `advisory_full`; "Signal Engine" → "Signal Watch" at all default sites.

Explicitly OUT of scope (later phases): widening the scraper to ALL FinCEN advisories;
automating derivation; the CLAUDE.md/HANDOFF doc update for the FinCEN verbatim exception +
fentanyl-config provenance true-up (a separate doc task). This slice is ONE item, end to end.

## Exit Criteria

- [ ] EFE FIN-2022-A002 acquired as PDF into `data/fincen/raw/` (single-fetch / scraper stub; authoring-only, no runtime fetch)
- [ ] `data/fincen/elder-financial-exploitation.md` holds the FULL verbatim article (source of truth), via an open-source PDF→markdown converter; enumerated red-flag list intact on manual inspection
- [ ] `config/typologies/elder-financial-exploitation.json` is schema-valid (`build.py <id>` passes); exactly one indicator + one candidate with `target:true`; the target candidate has a full signal `definition`; the signal traces to an enumerated red flag in the markdown (hand-derived)
- [ ] Act 1's SOURCE DOCUMENT panel renders the FULL verbatim advisory (`advisory_full`) in a bounded scrollable region, attributed (17 USC §105), visually distinct from the illustrative badge
- [ ] "Signal Engine" → "Signal Watch" rebrand applied (header + `<title>` + schema default + `validateConfig` default)
- [ ] All three built `dist/<id>/index.html` (fentanyl, trade-based, elder-financial-exploitation) run offline from `file://`, no console errors; coverage map + both human gates + combination-lift reveal intact

## Constraints (load-bearing)

- **Authoring-time vs ship-artifact split.** Acquire/convert/derive run at authoring; their
  output (markdown + config) is persisted and INLINED by `build.py`, never fetched at runtime.
  The ship artifact stays a single self-contained `dist/<id>/index.html` — NO `fetch()`, no ES
  modules (prevents `file://` breakage). Prevents: a hosted dependency creeping into the
  zero-dep offline ship file (HANDOFF §4 / §4.5 — Copilot is not a web backend).
- **Compliance hard gate still holds.** "Illustrative data & outputs" badge always visible;
  synthetic figures stay synthetic. The ONE new exception is the FinCEN advisory text — genuine
  US federal public-domain material, reproduced verbatim and attributed (17 USC §105), NOT
  paraphrased. Keep the two cleanly separated so real public-domain gov text is never read as
  illustrative. This relaxation is FinCEN-ONLY; it does NOT extend to FINTRAC (Crown copyright).
  Prevents: real government text reading as synthetic, or vice versa.
- **No real customer/transaction data, ever** (HANDOFF §4). FinCEN advisory text is public
  government source, not customer data — permitted.
- **New dependency caution.** The PDF→MD converter is a new dependency confined to authoring
  (`scripts/`), documented, never in the ship artifact. Prevents: a runtime dep in the zero-dep
  single-file demo.
- `validateConfig()` defaults `advisory_full` so existing fentanyl/trade-based configs (which
  lack the field) still render. Prevents: a new required field breaking the two shipped configs.

## Checkpoints

- **T2 (de-risk gate):** after acquire+convert, eyeball `data/fincen/<id>.md` for conversion
  quality before deriving the signal. If the markdown is mangled (column-soup / broken red-flag
  list), SWITCH converter (markitdown ↔ pymupdf4llm) before proceeding to T4. If still too
  garbled after switching: STOP and report — converter choice is the explicit de-risk target.
- **T5:** open all built dist from `file://` and confirm the full advisory renders scrollable in
  Act 1 without breaking the six-act layout or overflowing the stage; badge present AND separated
  from the verbatim-source attribution; both human gates + combination-lift reveal intact.
- **T3 abort:** if a defect surfaces needing an engine/config change beyond the planned slice,
  PAUSE and report rather than expanding scope silently.

## Assumptions

- An open-source PDF→markdown converter can be installed/run here. markitdown (MIT) is tried
  first for license-cleanliness; pymupdf4llm (AGPL — fine for an authoring-only tool that never
  ships) is the quality fallback. If neither installs or both garble output: report the gap.
- Act 1's SOURCE DOCUMENT panel can hold a full advisory once given max-height + overflow-y.
  If the article still breaks the layout: surface it as a design decision, not a silent CSS hack.

## Notes

Knowledge (aml-wiki): aml-wiki carries NO full text / PDF of any FinCEN advisory (only summaries
+ ID references) — the real EFE PDF is acquired externally (T1); converter output quality cannot be
pre-judged and is the explicit T2 de-risk. EFE FIN-2022-A002 specifics: 12 behavioral + 12 financial
red flags; SAR key term "EFE FIN-2022-A002" (SAR Field 2) + checkbox Field 38(d); the discrete
financial red flags map most directly to one clean transaction-level signal.

Derivation pattern (confirmed by the existing fentanyl.json target `S-FLOW-THROUGH-RETAIL`):
advisory red flag → `coverage.indicator` (covered/partial/gap, exactly one `target:true`) →
buildable candidate (cover gap AND data available) → target candidate `definition`
{signal_name, class, features[], logic, window, source, route}. The signal/atom/composition
vocabulary is PROJECT-LOCAL (CLAUDE.md / HANDOFF.md / config/schema.md) — use schema.md as the
contract.

PROVENANCE DEFECT (flagged, out of scope to fix here): `config/typologies/fentanyl.json`
`anchor.source` + CLAUDE.md cite FinCEN FIN-2019-A006 / FIN-2024-A002, neither verifiable in
aml-wiki; the existing fentanyl demo is actually FINTRAC-grounded. True-up is a separate doc task.
