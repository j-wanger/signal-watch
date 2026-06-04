---
title: "Phase 6: Ship (M5)"
aliases: []
category: phases
tags: [milestone-m5]
parents: []
created: 2026-06-04
updated: 2026-06-04
source: plan
status: completed
scope: ["README.md", "dist/**", "tests/**"]
entry_criteria: "M3 complete; M4 (live/pre-gen) skipped by decision. Demo is presenter-ready and multi-typology."
exit_criteria: "HANDOFF §1.2 definition of shipped fully satisfied; human sign-off."
---

# Phase 6: Ship (M5)

## Objective

Finalize: README run/present instructions, a compliance self-check, and a single-file
`dist/index.html` verified offline. Get human sign-off.

## Scope

- `README.md` — run, present, add-a-typology (live mode skipped — M4 not built)
- `dist/<id>/index.html` (fentanyl, trade-based) — verified offline ship artifacts
- `tests/smoke-checklist.md` — manual stage-rehearsal checklist, parameterized per typology

Doc/verify only — **zero engine/config edits expected**. M4 (live/pre-gen) skipped by decision.

## Plan (2026-06-04, lite)

- T1 · parameterize `tests/smoke-checklist.md` per typology (fix stale single-file `dist/index.html`
  path → `dist/<id>/`; M3 controls become active verify items; fill table covers both typologies)
- T2 · refresh `README.md` (M3 shipped controls; compliance covers fentanyl AND trade-based advisories)
- T3 · compliance self-check + offline `file://` verification — HARD GATE on both dist
- Human sign-off → delivery gate at `/dev-debrief`

## Exit Criteria

- [ ] README covers run / present / add-a-typology (live mode N/A — skipped)
- [ ] compliance self-check passes: no real data, advisories paraphrased + public, badge present, no secrets
- [ ] both `dist/<id>/index.html` open and run end-to-end from `file://`, offline
- [ ] `tests/smoke-checklist.md` parameterized per typology (Playwright skipped — dependency-light)
- [ ] human sign-off (Jake)

## Constraints

- The compliance self-check is a hard gate, not a formality. Prevents: synthetic
  figures read as real, copyrighted advisory text, leaked secrets.

## Notes

Definition of shipped — HANDOFF §1.2: reliable on stage · multi-typology from config ·
config-driven & maintainable · presenter-ready · compliance-clean · documented.
