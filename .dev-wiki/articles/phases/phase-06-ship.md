---
title: "Phase 6: Ship (M5)"
aliases: []
category: phases
tags: [milestone-m5]
parents: []
created: 2026-06-04
updated: 2026-06-04
source: init
status: not-started
scope: ["README.md", "dist/index.html", "tests/**"]
entry_criteria: "M3 complete (M4 optional). Demo is presenter-ready and multi-typology."
exit_criteria: "HANDOFF §1.2 definition of shipped fully satisfied; human sign-off."
---

# Phase 6: Ship (M5)

## Objective

Finalize: README run/present instructions, a compliance self-check, and a single-file
`dist/index.html` verified offline. Get human sign-off.

## Scope

- `README.md` — run, present, add-a-typology, (optional) live mode
- `dist/index.html` — verified offline ship artifact
- `tests/smoke-checklist.md` — manual stage-rehearsal checklist

## Exit Criteria

- [ ] README covers run / present / add-a-typology / (optional) live mode
- [ ] compliance self-check passes: no real data, advisories paraphrased + public, badge present, no secrets
- [ ] `dist/index.html` opens and runs end-to-end from `file://`, offline
- [ ] `tests/smoke-checklist.md` written; (optional) Playwright click-through
- [ ] human sign-off (Jake)

## Constraints

- The compliance self-check is a hard gate, not a formality. Prevents: synthetic
  figures read as real, copyrighted advisory text, leaked secrets.

## Notes

Definition of shipped — HANDOFF §1.2: reliable on stage · multi-typology from config ·
config-driven & maintainable · presenter-ready · compliance-clean · documented.
