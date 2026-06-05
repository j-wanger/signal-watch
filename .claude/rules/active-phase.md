# Active Phase Context

Phase: 7 - Pipeline walking skeleton (M6) — COMPLETED + accepted (committed to main 2026-06-04)
Objective: Proved the "Signal Watch" ingestion pipe end to end on ONE FinCEN advisory (EFE FIN-2022-A002):
acquire PDF → markitdown PDF→MD (data/fincen/ = source of truth) → hand-derive one schema-valid config →
render the FULL verbatim advisory in Act 1's SOURCE DOCUMENT panel. "Signal Engine"→"Signal Watch" rebrand
rode along (engine + dist; docs deferred). Target signal S-DORMANT-DRAIN-ELDER.
Scope: data/fincen/**, scripts/**, config/typologies/*.json, config/schema.md, index.html, dist/**.

Key constraints (load-bearing):
- Authoring-time vs ship split: acquire/convert/derive are BUILD-TIME; output persisted + INLINED. Ship
  artifact stays single-file, offline, zero runtime deps, NO fetch (HANDOFF §4 / §4.5).
- FinCEN advisory text = verbatim public domain (17 USC §105), attributed, NOT paraphrased; FinCEN-ONLY
  (NOT FINTRAC); kept visually SEPARATE from the "Illustrative data & outputs" badge.

Done: committed to main (raw PDF gitignored per decision — regenerable via acquire_fincen.py; .md committed as source of truth).
Deferred → Phase 8 doc true-up (rebrand docs + amend the "paraphrased" non-negotiable + fix fentanyl FINTRAC-vs-FinCEN provenance).

Exit (MET in working tree, pending acceptance): EFE PDF → data/fincen/<id>.md → schema-valid
elder-financial-exploitation.json → Act 1 verbatim render (scrollable, attributed, separated) → rebrand →
all 3 dist self-contained + node --check PASS.

Abort: if delivery review surfaces a defect needing an engine/config change beyond the slice — PAUSE and report.

Gates:
- [x] Direction confirmed by user (M6 pipeline slice; EFE FIN-2022-A002; Act 1 verbatim render; rebrand; 5 lite tasks — 2026-06-04)
- [x] Delivery accepted (post-implementation report 2026-06-04 — accepted, committed to main)
