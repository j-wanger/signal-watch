# Active Phase Context

Phase: 8 - Doc true-up + provenance fix (M6 debt) — ACTIVE (direction approved 2026-06-04)
Objective: Close the three doc/provenance debts deferred from Phase 7. The always-loaded docs
must tell the truth about what the shipped artifact now is and cites. Doc/config-string ONLY —
the engine (index.html) is NOT touched (`git diff index.html` must be empty).
Scope: CLAUDE.md, HANDOFF.md, README.md, tests/smoke-checklist.md, config/typologies/fentanyl.json,
dist/**, scripts/build.py.

Three defects:
1. Brand drift — branded "Signal Engine" → "Signal Watch" in the four docs (H1 → "Signal Watch —
   AML Vision Demo"). Replace only the BRANDED name; preserve lowercase technical "engine".
   smoke-checklist:31 header check currently FAILS against the shipped "Signal Watch" brand.
2. Stale non-negotiable — amend CLAUDE.md non-negotiables + HANDOFF §4.4: paraphrase by default
   EXCEPT FinCEN federal advisories (public domain, 17 USC §105, verbatim WITH attribution, kept
   separate from the illustrative badge); does NOT extend to FINTRAC (Crown copyright).
3. False fentanyl provenance — remove unverifiable FIN-2019-A006 / FIN-2024-A002 (0 hits in
   aml-wiki); attribute fentanyl solely to the FINTRAC Jan-2025 Operational Alert. Edit
   fentanyl.json:15 anchor.source + CLAUDE.md:21 + HANDOFF.md:100 & :120 + README.md:64-65.

Key constraints (load-bearing):
- Engine untouched (index.html diff empty); no schema, no new acts; six-act arc + two wow beats
  + always-on "Illustrative data & outputs" badge unchanged.
- Branded-name-only replace (no `sed` blind replace — reviewed edits).
- Honest provenance: attribute only to sources actually used + verifiable (FINTRAC alert).
- fentanyl.json content change forces a dist/fentanyl rebuild; other two dist stay byte-identical.

Exit: `! grep -rIn 'Signal Engine'` (four docs) · CLAUDE.md+HANDOFF carry the FinCEN-only verbatim
exception · `! grep -rIn 'FIN-2019-A006|FIN-2024-A002'` (config + three docs) · `build.py all` clean,
self-contained guard 0 tokens, `node --check` PASS · `git diff --stat index.html` empty · only
dist/fentanyl changed.

Abort: if a fix surfaces a defect needing an engine/schema/config-structure change beyond the
doc/string slice — PAUSE and report. If blocked >3 attempts on a task, ask user: skip or abort.

Gates:
- [x] Direction confirmed by user (3-defect doc true-up; provenance = remove + attribute to FINTRAC; 4 lite tasks — 2026-06-04)
- [x] Delivery accepted (user accepted + asked to commit + fold in M6 doc staleness — 2026-06-04)
