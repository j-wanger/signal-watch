---
title: "Phase 8: Doc true-up + provenance fix"
aliases: [signal-watch-doc-true-up, m6-doc-debt]
category: phases
tags: [milestone-m6, docs, provenance, signal-watch, compliance]
parents: []
created: 2026-06-04
updated: 2026-06-04
source: plan
status: completed
ceremony: lite
scope: ["CLAUDE.md", "HANDOFF.md", "README.md", "tests/smoke-checklist.md", "config/typologies/fentanyl.json", "dist/**", "scripts/build.py"]
entry_criteria: "Phase 7 (M6 pipeline slice) delivered + accepted; the rebrand and the FinCEN-verbatim render live in the engine + dist, but the docs still describe the pre-M6 world. Three doc/provenance debts were explicitly deferred from Phase 7."
exit_criteria: "No branded 'Signal Engine' left in CLAUDE.md/HANDOFF.md/README.md/tests/smoke-checklist.md; the paraphrase non-negotiable carries the FinCEN-only verbatim public-domain exception (17 USC §105, attributed, NOT FINTRAC); the unverifiable FIN-2019-A006/FIN-2024-A002 fentanyl cites are removed (FINTRAC Jan-2025 alert is the sole attribution) across config + docs; fentanyl dist rebuilt clean (self-contained guard 0 tokens, node --check PASS); index.html engine diff empty; only dist/fentanyl changed."
---

# Phase 8: Doc true-up + provenance fix

## Objective

Close the three doc/provenance debts deferred from Phase 7 (M6). The unifying thread:
**the docs must tell the truth about what the shipped artifact now is and cites.** Phase 7
landed the "Signal Watch" rebrand and the verbatim-FinCEN render in the engine + dist; the
always-loaded docs (CLAUDE.md / HANDOFF.md / README.md) still describe the pre-M6 world.

Doc/config-string only. The engine (`index.html`) is NOT touched — `git diff index.html`
must stay empty.

## Scope (three defects)

1. **Brand drift.** `Signal Engine` survives in doc H1s + one verify line: `CLAUDE.md:1`,
   `HANDOFF.md:1` & `:180` (the CLAUDE skeleton block), `README.md:1`,
   `tests/smoke-checklist.md:31`. The engine self-brands as **"Signal Watch — AML Vision
   Prototype"** (`index.html:6,221,253`). `smoke-checklist.md:31` asserts the header shows
   "Signal Engine" → that check now FAILS against the shipped artifact (verification defect,
   not cosmetics). Doc H1 → `Signal Watch — AML Vision Demo`. Replace only the *branded* name;
   preserve lowercase technical "engine" ("generic engine", "engine-only").
2. **Stale non-negotiable.** `CLAUDE.md:20-21` and `HANDOFF.md §4.4 (:100)` say advisory text
   "must be PARAPHRASED", full stop. Act 1 now renders a verbatim FinCEN advisory. Amend with
   the FinCEN-only public-domain exception: federal advisories are public domain (17 USC §105),
   may be reproduced verbatim WITH attribution, kept visually separate from the illustrative
   badge; does NOT extend to FINTRAC (Canadian Crown copyright → still paraphrase).
3. **False fentanyl provenance.** `FIN-2019-A006` / `FIN-2024-A002` = 0 hits in aml-wiki; the
   demo's indicators trace to the FINTRAC Jan-2025 Operational Alert (its own ~5,000-STR
   2020–2023 figures are in `advisory_stream`). The FinCEN IDs were never the derivation
   surface. Remove them; attribute fentanyl solely to FINTRAC. Bad cites: `fentanyl.json:15`
   (`anchor.source`), `CLAUDE.md:21`, `HANDOFF.md:100` & `:120`, `README.md:64-65`.

Out of scope (later phases): FinCEN corpus crawler; automated article→signal derivation.

## Exit Criteria

- [ ] `! grep -rIn 'Signal Engine'` across CLAUDE.md, HANDOFF.md, README.md, tests/smoke-checklist.md
- [ ] smoke-checklist header check matches the shipped "Signal Watch" brand
- [ ] CLAUDE.md + HANDOFF.md state the FinCEN-only verbatim public-domain exception (17 USC §105) + the FINTRAC paraphrase carve-out
- [ ] `! grep -rIn 'FIN-2019-A006|FIN-2024-A002'` across config/ + CLAUDE.md + HANDOFF.md + README.md
- [ ] fentanyl attributed to the FINTRAC Jan-2025 Operational Alert (config + docs)
- [ ] `build.py all` clean; self-contained guard 0 tokens; `node --check` PASS; `git diff --stat index.html` empty; `git diff dist/` shows only dist/fentanyl changed

## Constraints (load-bearing)

- **Engine untouched.** This is doc/config-string only. `index.html` diff must be empty; no
  schema, no new acts, six-act arc + two wow beats + always-on badge unchanged.
- **Branded-name-only replace.** Swap the product name `Signal Engine` → `Signal Watch`; never
  the lowercase technical "engine". No `sed` blind replace — reviewed edits.
- **Honest provenance.** Attribute only to sources actually used + verifiable (FINTRAC alert).
  This is the project's "provenance upgrades buy-in" thesis applied to its own docs.
- **Config change forces a rebuild.** `fentanyl.json` content changed → `dist/fentanyl` must be
  rebuilt and stay self-contained; the other two dist must remain byte-identical.

## Notes

Verified during planning: `grep` for `FIN-2019-A006|FIN-2024-A002` over aml-wiki = 0 hits;
`FIN-2022-A002` (elder) IS present (so the EFE pipeline cite is sound). Engine brand strings:
`<title>Signal Watch — AML Vision Prototype`, `brandTitle = "Signal Watch"`,
`BRAND` JS default `{title:'Signal Watch', subtitle:'AML Detection · Vision Prototype'}`.
Direction confirmed by user 2026-06-04 (provenance fix = remove + attribute to FINTRAC).
