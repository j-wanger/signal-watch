---
title: "Phase 8: Doc true-up + provenance fix"
date: 2026-06-04
type: journal
phase: phase-08-doc-true-up
tags: [milestone-m6, docs, provenance, signal-watch, compliance, dist-drift]
commit: 042d732
---

# Phase 8: Doc true-up + provenance fix (M6 debt)

Closed the three doc/provenance debts deferred from Phase 7. Doc/config-string only;
engine (`index.html`) untouched (diff empty). Committed to main as `042d732`. Lite ceremony.

## What shipped

- **Rebrand** (T1): branded `Signal Engine` → `Signal Watch` at 4 sites (CLAUDE/HANDOFF×2/README
  H1 → "Signal Watch — AML Vision Demo"; `smoke-checklist:31` header check — which had been
  *failing* against the shipped engine brand). Lowercase technical "engine" preserved (no `sed`).
- **Non-negotiable amended** (T2): CLAUDE.md non-negotiables + HANDOFF §4.4 now state paraphrase
  by default, ONE exception — FinCEN federal advisories are public domain (17 USC §105), verbatim
  + attributed, kept separate from the illustrative badge; does NOT extend to FINTRAC (Crown
  copyright). CLAUDE.md's bad cite cleared in the same rewrite.
- **Fentanyl provenance** (T3): removed unverifiable `FIN-2019-A006`/`FIN-2024-A002` (0 hits in
  aml-wiki, never the derivation surface — the demo's ~5,000-STR figures are FINTRAC's), attributed
  solely to the FINTRAC Jan-2025 Operational Alert. Sites: `fentanyl.json:15`, HANDOFF :100+:120,
  README :64.
- **M6 doc staleness** (user add): CLAUDE "Current state" M2→M6 + authoring-pipeline bullet +
  3-typology list + milestone line; README status M5→M6, elder typology + verbatim-exception in
  Compliance, FinCEN-verbatim authoring note in "Add a typology"; both build-example blocks list elder.

## Decisions

- Provenance fix = **remove** unverifiable cites + attribute to the verified, actually-used source
  (FINTRAC). Honest attribution over chasing unverifiable cites — the project's own provenance
  thesis applied to its docs.
- Doc H1 wording = "Signal Watch — AML Vision Demo" (product-first, matches the engine's ordering).
- Scope correction: defect 3's false cite lives *inside* `fentanyl.json`, so the "doc-only" phase
  necessarily touched one config string + forced a dist rebuild; engine still untouched.

## Escape hatches

- **DISCOVERY (user-approved):** rebuilding for T4 revealed **Phase 7 committed STALE
  `dist/fentanyl` + `dist/trade-based`** — they lacked the engine's highlights feature
  (`esc()`/`.hl`/`docfull` 460px); only `dist/elder` was current. `build.py all` did not reproduce
  committed dist at HEAD, so the M5 "zero-drift" invariant had silently broken (the highlight
  feature landed in `index.html` after fentanyl/trade-based were last built; only elder got rebuilt).
  User chose to stage all fresh dist, restoring the invariant. Engine unchanged.
- **DISCOVERY (reframing sweep):** the T3 success-criterion sweep caught 2 more bad-cite sites in
  `tests/smoke-checklist.md` (62, 75) that the initial T3 file-list missed. Fixed under T3.

## Health Delta

No tests/typecheck in this project (doc-only phase). Build health: `build.py all` clean ×3;
self-contained guard 0 forbidden tokens ×3; `node --check` PASS ×3 (node v22); no external refs
beyond Google Fonts. `git diff index.html` empty (engine untouched). dist drift corrected.

## Review Gate

Lite ceremony, but 4 tasks → above the 4-task gate threshold. Self-check (scope + correctness)
served as the gate: every changed line traces to the 3 defects, the user-approved dist rebuild, or
dev-wiki artifacts; all 6 exit criteria verified by grep/build/node before commit. One deliberate
non-change recorded (README:38/:63 "paraphrased" — true for the typologies README covers).

## Gate Compliance

`gate-log:phase-08 direction=approved delivery=accepted` — both gates present. PASS. Direction
approved via AskUserQuestion (provenance fix); delivery accepted when user said "commit it".

## Soft Observations / Phase N+1 Candidates

- **Build-drift guard (highest value):** wire `python3 scripts/build.py all && git diff --exit-code dist/`
  into `tests/smoke-checklist.md` (or a pre-commit check). This session proved the stale-dist failure
  mode is real and silent — a deterministic guard would have caught the Phase 7 drift at commit time.
  Evidence: this phase's DISCOVERY. → small follow-up.
- **HANDOFF.md may carry residual M2/M5-era staleness** beyond what we swept (e.g. §3.2 single
  `dist/index.html` references, §8 milestone plan). We touched only the brand H1s, §4.4, and the
  content-model example. A full HANDOFF true-up pass could finish it. → optional doc follow-up.
- **Queued vision phases remain** (from M6): FinCEN corpus crawler (widen the scraper from one
  advisory to all); automate the article→signal derivation step (keep the deterministic validator
  at the build boundary). Manual path proven in M6.
- **Elder typology is compliance-mentioned but not in the README walkthrough narrative** — minor;
  fold in if elder becomes a presented typology.

## Activation Quality

No `active-knowledge.md` (lite phase, none generated) — step skipped.
