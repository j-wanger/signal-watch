---
title: "2026-06-04 · M1 config-driven refactor"
category: journal
date: 2026-06-04
phase: phase-02-config-driven-refactor
tags: [milestone-m1, refactor]
---

# M1 — config-driven refactor

## What shipped
Refactored the single-file demo into a generic engine + per-typology config + a stdlib build.
- `config/schema.md` — content-model contract (HANDOFF §5, tightened).
- `config/typologies/fentanyl.json` — fentanyl content, single source of truth.
- `index.html` — generic engine; all six acts render from a `CONFIG` object via a single
  `__CONFIG__` injection point. Entangled literals promoted to config (target candidate &
  indicator via `target:true`, proposal `signal_name`, `stats`, anchor copy, `coverage_noun`).
- `scripts/build.py` — inlines the chosen config → `dist/index.html` (self-contained, file://-safe).
- `tests/smoke-checklist.md`; baseline moved to `archive/`.

## Decisions
- **Minimal structure** over the §3.3 modular split (one engine template + JSON + stdlib inliner).
  Subtraction test; split src/ later only if the engine grows.
- **Single source of truth = config JSON**; `index.html` holds a placeholder, not a duplicate.
- **Promote entangled literals to config** (derive target via `target:true`) so M2 needs zero engine edits.

## Verification
- Equivalence: `dist` renders **byte-identical act HTML to the baseline** across all 7 acts.
- Generic: zero typology literals in the engine (grep-clean).
- Defensive: no-lift / no-coverage / empty-`{}` configs degrade to labeled placeholders, no blank stage.
- Self-contained: no fetch/module/external script; only Google Fonts refs; build fails loud on bad config.

## Escape hatches
- **DISCOVERY** — added `anchor.coverage_noun` mid-refactor (the Act 0/6 gauge captions named
  "fentanyl typologies"; promoted to config + schema).

## Health delta
New: `config/`, `scripts/build.py`, `dist/`, `tests/`, generic `index.html`. No deps added (stdlib + vanilla JS).
Verification harnesses were throwaway (/tmp), not committed.

## Soft Observations / Phase N+1 Candidates
- M2 schema readiness: the contract carries `target`/`signal_name`/`coverage_noun` so a 2nd typology
  should need no engine edits — M2 is the real test of the "add one JSON file" claim.
- The DOM-stub equivalence harness could become a committed `tests/` Playwright check in M3/M5
  (evidence: /tmp harness proved per-act HTML equality cheaply).
- `hl:1` (baseline) → `hl:true` (config) normalization is intentional; documented in schema.
