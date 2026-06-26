---
title: "Phase 76 — The merge-adjudication Class-J console: the human gate over candidate SHARES links"
status: active
created: 2026-06-25
updated: 2026-06-25
ceremony: standard
tags: [class-j, merge-adjudication, entity-resolution, console, ship-artifact, scored-oracle, blueprint]
---

# Phase 76 — The merge-adjudication Class-J console

## Objective

A 6th SHIP artifact `merge.html` → `dist/merge/index.html` (offline, self-contained; sibling to the gate + triage consoles, those byte-frozen) dramatizing the blueprint's **Class-J merge-adjudication gate** — the human gate over entity-resolution candidate links. Consumes Phase 75's over-merge finding (the deterministic spine resolves what it can + refuses the ambiguous; the human adjudicates the residual). **The novelty:** unlike the consensus-only gate console + the label-blind §14 triage, the merge gate has a measurable correctness ORACLE (`true_entities`) — the Reveal SHOWS, where the oracle exists, whether the adjudication matched truth (synthetic-only, qualified).

## Direction (user's Step-9 picks + the gate)

- FORM: a 6th SHIP console `dist/merge/` (not a workbench beat) — elevates the Class-J merge gate to a first-class artifact, consistent with the console family.
- SCORED dimension: SHOW the synthetic-scored oracle (the differentiator); real-substrate scoring DEFERRED to a substrate-emit handoff.
- Direction gate: all-accept; A1 accept-with-shaping (T1 expands the oracle honestly); A2–A5 accept-with-evidence. Ledger Phase-76.

## The seam (Phase 75 output)

66 candidate SHARES in the committed v0.5 slice (distinct entity_refs sharing a strong identifier — genuinely ambiguous) + the spine's `2+-distinct-strong → refuse-as-ambiguous` path (`entity_spine.py:207-211`) + `resolution_scorer.py` (scores vs synthetic `true_entities`, resolver-input firewall). The scored-oracle machinery exists; this phase builds the human gate over it.

## Arc (mirroring gate/triage)

Queue (candidate SHARES grouped by basis: strong-shared-id / weak-corroboration / name-only) → Evidence (the two records' identities + the shared identifier + the spine's deterministic verdict + network context) → Adjudication (uphold-merge / reject-as-SHARES-edge / both-defensible / escalate; rationale REQUIRED) → Reveal (deterministic baseline + — where the oracle exists — the scored truth, synthetic-only-qualified; the real-consensus / synthetic-scored SPLIT visible) → Ledger (the adjudication record + agreement/scoring arithmetic; persists nothing).

## Approach (6 tasks)

1. **T1 (M):** expand the synthetic `true_entities` oracle (~20-30 observations: same-person-fragmented / household-share / coincidence ambiguity) — CHECKPOINT: confirm it yields genuinely-ambiguous scored cases without fabricating truth; `resolution_scorer --selftest` green.
2. **T2 (M):** `curate_merge_cases.py` → committed `data/merge/cases.json` (real candidate SHARES from the v0.5 slice [consensus] + the expanded oracle's scored cases); deterministic regen; resolver-input firewall + closed adjudication vocab.
3. **T3 (L):** `merge.html` + the `merge` build target + `validate_merge_cases` at the build boundary; the Class-J arc; `dist/merge` byte-frozen on `--check merge`.
4. **T4 (M):** `tests/merge-console.test.mjs` — the arc, the graded gate (rationale required), reveal-locked-pre-adjudication, the scored-vs-consensus split + synthetic-only label, ledger, badge, XSS, keyboard guards, both motion modes.
5. **T5 (S):** the substrate-emit handoff brief (substrate emits `true_entities` for the slice, firewall preserved → the merge console can score REAL cases) — re-grounded to fc98b09.
6. **T6 (S):** verification + true-up — `--check all` (9 targets; 8 existing byte-frozen except the launcher cascade); build.py imports no spine/scorer/sibling; gate + triage + workbench arcs green; `uv run pytest`; CLAUDE.md (the 6th ship artifact).

## Constraints / abort

Honesty (consensus-real / synthetic-scored split; synthetic-only qualifier; no catch-rate/lift; always-on badge); the resolver-input firewall; build-time curation (no live spine in the dist); the existing 8 dists byte-frozen except the launcher cascade. Abort: non-launcher dist drift / a sibling-or-spine import in build.py / a loosened validator / a scored number presented as a real catch-rate / the firewall leaking → STOP. If the oracle can't yield ambiguous scored cases honestly [A1] → consensus + defer scoring.

## Out of scope (deferred, named)

Scoring-over-real-substrate (the T5 substrate-emit handoff); a live/companion re-adjudication mode; probabilistic/Splink ER; graph/Kuzu.

## Spec

`specs/phase-76-merge-adjudication-console.md` (STANDARD). Ledger: `assumption-ledger.md` Phase 76.
