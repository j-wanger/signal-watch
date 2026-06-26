# Phase 76 — The merge-adjudication Class-J console

**Ceremony:** STANDARD (a new ship-class artifact, like Phase 47/49 consoles).
**Status:** active (planned 2026-06-25).

## 1. Objective

Dramatize the program blueprint's **Class-J merge-adjudication gate** — the human gate over entity-resolution candidate links — as a **6th ship artifact** `merge.html` → `dist/merge/index.html` (offline, self-contained, sibling to the gate + triage consoles; those byte-frozen). Consume Phase 75's over-merge finding: the deterministic spine resolves what it can (entity_ref) and refuses the ambiguous; the human adjudicates the refused residual (the candidate SHARES). **The architectural novelty:** unlike the consensus-only gate console and the label-blind §14 triage, the merge gate is the ONE gate with a measurable correctness **oracle** (`true_entities`) — so the Reveal SHOWS, where the oracle exists, whether the adjudication matched truth (synthetic-only, qualified).

## 2. The consume seam (Phase 75 output)

The committed v0.5 slice carries **66 candidate SHARES** (distinct entity_refs sharing a strong identifier — genuinely ambiguous: same UBO vs household/coincidence) + the spine's `2+-distinct-strong → refuse-as-ambiguous` path (`entity_spine.py:207-211`). `resolution_scorer.py` scores a clustering vs the synthetic `data/entity-spine/true_entities.json` (pairwise/B-cubed) behind the resolver-input firewall — the scored-oracle machinery already exists.

## 3. Scope (in / out)

**In:** expand the synthetic `true_entities` oracle (T1); `curate_merge_cases.py` → committed `data/merge/cases.json` (T2); `merge.html` + the `merge` build target + `validate_merge_cases` at the build boundary (T3, the one L); `tests/merge-console.test.mjs` (T4); the substrate-emit handoff brief (T5); verification + true-up (T6).

**Out (DEFERRED, NAMED):** scoring-over-REAL-substrate (needs substrate to emit `true_entities` for the slice — the resolver-input firewall keeps it hidden today → the T5 handoff brief); a live/companion re-adjudication mode (the ship artifact curates at build time); probabilistic/Splink ER; graph/Kuzu.

## 4. Constraints (safety rails)

- **Honesty (A4):** consensus-not-ground-truth for the REAL substrate cases (no oracle without substrate-emit); the scored dimension SYNTHETIC-ONLY + qualified ("measured on synthetic clusters; production has no ground truth"); the Reveal visibly SPLITS real-consensus from synthetic-scored; NO catch-rate/lift; the always-on badge.
- **Resolver-input firewall:** the scorer never leaks cluster ids into the resolver (`assert_no_cluster_leak`); the curate keeps the oracle on the eval-only channel.
- **Companion/ship boundary:** build.py validates the merge cases at the boundary but imports no spine/scorer/sibling; the deterministic verdict + scored oracle curate at BUILD time (no live spine in the dist — A5).
- **Dists byte-frozen (A3):** the existing 8 dists stay byte-identical EXCEPT the sanctioned launcher cascade (it lists the new artifact — Phase-60 Option-A). `--check all` becomes 9 targets.

## 5. Checkpoints

- **After T1:** confirm the expanded synthetic oracle yields genuinely-ambiguous scored cases (same-person-fragmented / household-share / coincidence) without fabricating the truth. If it can't → fall back to consensus + defer scoring (the A1 abort).

## 6. Assumptions (stop if violated)

A1 the synthetic oracle is expandable to a non-toy scored gate; A2 the 66 real candidate SHARES are genuinely ambiguous; A3 dist/merge additive + build-boundary validated; A4 honesty (consensus-real / synthetic-scored split); A5 build-time curation, no live spine in the dist. (Full positions: `assumption-ledger.md` Phase 76.)

## 7. Exit criteria

1. The synthetic `true_entities` oracle expanded with deliberate ambiguous merge cases; `resolution_scorer --selftest` green + the ambiguous-case count is meaningful.
2. `curate_merge_cases.py` → committed `data/merge/cases.json` (real candidate SHARES [consensus] + synthetic scored cases); deterministic regen; the resolver-input firewall + closed adjudication vocab validated.
3. `merge.html` renders the Class-J arc (Queue → Evidence → Adjudication [rationale required] → Reveal [real-consensus / synthetic-scored split] → Ledger); the `merge` build target + `validate_merge_cases` at the boundary; `dist/merge` byte-frozen on `--check merge`.
4. `tests/merge-console.test.mjs` green (the arc, the graded gate, reveal-locked-pre-adjudication, the scored-vs-consensus split + synthetic-only label, ledger, badge, XSS, keyboard guards, both motion modes).
5. The substrate-emit handoff brief (substrate emits `true_entities` for the slice, firewall preserved) — re-grounded to fc98b09.
6. `--check all` (9 targets; the 8 existing byte-frozen except the launcher cascade); build.py imports no spine/scorer/sibling; the gate + triage + workbench arcs green (not regressed); `uv run pytest` green; CLAUDE.md trued up (the 6th ship artifact).

## 8. Abort rule

Any non-launcher dist drift / a sibling-or-spine import in build.py / a loosened validator / a scored number presented as a real catch-rate / the resolver-input firewall leaking → STOP-and-surface. The scored-over-real-substrate path stays a NAMED sibling handoff, never faked here.
