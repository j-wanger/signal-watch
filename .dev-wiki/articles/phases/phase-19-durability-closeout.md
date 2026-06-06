---
title: "Phase 19: Durability closeout — commit corpus-explorer test harness + pin _rf_triage"
aliases: ["phase-19-durability-closeout"]
category: phases
tags: ["M7", "durability", "testing", "lite"]
parents: ["phase-18-corpus-explorer-arc"]
created: 2026-06-06
updated: 2026-06-06
source: plan
status: active
scope: ["tests/**", "scripts/derive_signals.py", "README.md", "CLAUDE.md", "tests/smoke-checklist.md"]
entry_criteria: "Phase 18 complete + accepted (impl 6d654a4 — corpus explorer 5-screen arc ships); M0–M7 roadmap + the arc complete, demo at Definition of Done."
exit_criteria: "node arc harness exits 0 (~15 assertions, zero deps) · --selftest gains the glued _rf_triage pin · --check all zero drift + frozen set git-diff-empty · README/CLAUDE/smoke-checklist document the harness."
---

# Phase 19: Durability closeout — commit corpus-explorer test harness + pin _rf_triage

## Objective

A durability closeout at the end of the completed M0–M7 roadmap (demo at Definition of Done): lock in the corpus explorer's 5-screen behavior with a committed, dependency-free test harness, and clear the one named code-debt item (`_rf_triage`) honestly by PINNING + DISCLOSING it rather than rewriting. No net-new feature value remains without fabrication risk, so durability is the highest-value remaining move.

## Scope

The UNFREEZE (only edits allowed):
- `tests/**` — the new harness
- `scripts/derive_signals.py` — comment + selftest fixture ONLY (no output change)
- `README.md`, `CLAUDE.md`, `tests/smoke-checklist.md` — document the harness command

FROZEN byte-untouched: `index.html`, `corpus.html`, `scripts/build.py`, `config/**`, `data/fincen/**` (incl. `corpus-status.json` + `derived/*.json`), ALL of `dist/**` (the harness only READS `dist/corpus/index.html`).

## Exit Criteria

- [ ] `node tests/corpus-explorer.test.mjs` exits 0 with ~15 arc assertions passing against the committed dist, ZERO npm deps (no jsdom)
- [ ] `derive_signals.py --selftest` gains the glued `_rf_triage` pin + the one-line "coarse hint, not authoritative for glued" comment and passes
- [ ] `build.py --check all` shows zero drift + the frozen set git-diff-empty (corpus-status.json + dist/** byte-identical)
- [ ] README + CLAUDE + smoke-checklist each document the harness command

## Constraints

- ZERO runtime deps — hand-rolled Node DOM-shim, NEVER jsdom (prevents breaking the file:// offline ethos + the project's dep-free `--selftest`/`--check` idiom).
- The `_rf_triage` item is PIN + DISCLOSE, NOT a counting rewrite (prevents reintroducing the deterministic parser Phase 17 deleted — anti-subtraction; glued advisories can't be reliably counted deterministically, which is why the inverted loop has the LLM read them; harmless today).
- NO behavioral change to any shipped artifact (prevents drift — corpus-status.json + dist/** stay byte-identical; `--check all` must still pass).
- The harness loads the COMMITTED `dist/corpus/index.html` (prevents a test/ship divergence — it doubles as a build-output smoke test; `--check all` guarantees dist equals a fresh build).

## Assumptions

- The corpus explorer's inline `<script>` (corpus.html ~189–537) has a tiny DOM surface (getElementById, querySelectorAll, requestAnimationFrame, matchMedia, setTimeout; no layout reads, no real events) so a hand-rolled shim can drive it. If false (the shim can't drive the arc without a real DOM lib): DEGRADE to a leaner assertion set (boot + each screen renders without throwing + the coverage-math unit, skipping event-driven toggles) — NEVER pull jsdom into a file:// offline demo.

## Notes

Two carried Phase-19 candidates resolved during planning:
- The `anthropic` pin is DEAD — `requirements-authoring.txt` does not exist (Phase 17's deletion already took it). No task needed.
- The `tests/` gap is REAL — `tests/` had only `fixtures/` + a manual `smoke-checklist.md`; the headless DOM-shim that verified the corpus explorer across Ph17/Ph18 was ad-hoc/uncommitted (flagged a soft observation three phases running).

Direction approved by user 2026-06-06: durability closeout over call-it-done / showcase-debt-true-up / new-stakeholder-ask; zero-dep Node DOM-shim; `_rf_triage` pin-not-rewrite. Lite ceremony — decisions recorded in `_CURRENT_STATE.md` (no decision articles).
