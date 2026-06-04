---
title: "Phase 1: Bootstrap (M0)"
aliases: []
category: phases
tags: [milestone-m0]
parents: []
created: 2026-06-04
updated: 2026-06-04
source: init
status: completed
scope: ["CLAUDE.md", "README.md", "HANDOFF.md", ".gitignore", "aml_vision_demo_fentanyl.html"]
entry_criteria: "Baseline single-file demo available to import."
exit_criteria: "The current demo runs from the repo and is committed."
---

# Phase 1: Bootstrap (M0)

## Objective

Stand up the project: init git, add project docs (CLAUDE.md, README.md, HANDOFF.md),
import the baseline single-file demo, and confirm it runs.

## Scope

- `CLAUDE.md`, `README.md`, `HANDOFF.md`, `.gitignore`
- `aml_vision_demo_fentanyl.html` (baseline — unchanged)

## Exit Criteria

- [x] git repo initialized
- [x] CLAUDE.md, README.md, HANDOFF.md written
- [x] baseline demo imported and verified (JS compiles, both gates + lift present, self-contained)
- [x] committed (`c56b82e`)

## Notes

Verification was a static check: embedded JS compiles (compile-only, no DOM exec),
document is complete, the only external refs are Google Fonts (degrade to system
fonts offline). No `<script src>`, no `fetch()` in the core walkthrough.
