# Active Phase Context

Phase: 49 — Triage-loop embryo made demo-able: blueprint §14's continuous adjudication loop as the 5th ship artifact (triage console). STANDARD ceremony. 5 tasks, planned 2026-06-12, next: T1.

Objective: triage.html → dist/triage/index.html (single self-contained offline; gate console BYTE-FROZEN). Committed SYNTHETIC data/triage/scenarios.json deterministically curated (curate script reads data/probe-history at AUTHORING time only; rule text embedded; build.py never reads probe-history) — ~16 scenarios × 4 §14 strata + ~4 controls, panels shared BY REFERENCE across divergent-disposition pairs, fired-rule state universal, labeled second-rater seeds. Arc: Queue → Evidence → Disposition (§14 grammar incl. need-more-info→C/D picker + the policy-gap escape; rationale REQUIRED) → Reveal (decisions-not-correctness; second-rater replay; process-inconsistency surfacing) → Discovery ledger (JSON export, persists nothing).

Scope: scripts/curate_triage_scenarios.py · data/triage/** · scripts/build.py · triage.html · tests/triage-console.test.mjs · dist/triage/** · specs/phase-49-*.md · CLAUDE.md · HANDOFF.md §8 · tests/smoke-checklist.md · .dev-wiki/*

Key constraints: 4 existing dists byte-identical; derive_signals.py + news pipeline + overlays + blueprint FROZEN (no docs/program-blueprint.md edit); everything synthetic, badge always-on, NO LLM/fetch; no fake instrumentation — render-computed numbers w/ measurement definitions only, params "chosen, not measured"; US-federal-only novel stratum.

Exit criteria: (1) scenarios.json committed — ≤20 scenarios, 4 strata populated, ≥3 controls, deterministic regen byte-identical, panel-sharing by reference, ≥4 labeled second-rater seeds, synthetic meta flag; (2) build.py triage target in all/--check, 4-class tamper validation fails loud, no probe-history in build.py; (3) dist/triage single-file offline full arc; (4) tests/triage-console.test.mjs fully green ~50+; (5) honesty greps + FULL REGATE — --check all zero drift (7 targets), derive_signals.py + program-blueprint.md untouched, all existing suites green.

Abort rule: existing dists drift → STOP and surface (never re-baseline); >3 attempts on a task → mark [blocked] + ask.

Gates:
- [x] Direction confirmed by user (assumption gate closed 2026-06-12: A1 demo-first accept · A2 don't-know→defended→accept · A3 accept · A4 5th-ship-artifact accept; all_accept: false)
- [x] Delivery accepted (post-implementation report 2026-06-12)
