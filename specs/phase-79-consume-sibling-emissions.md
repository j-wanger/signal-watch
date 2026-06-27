---
phase: 79
slug: phase-79-consume-sibling-emissions
title: "Consume sibling emissions — Lakeshore `cleared` co-sign (floor) + merge real-data oracle (gated upside)"
ceremony: standard
status: active
created: 2026-06-27
grounded_against:
  signal-watch: 92ac6d0 (Phase 78 committed)
  aml-substrate: c099259 (Phase 33; Phase 32 31cb439 = anchored-fork-fragments)
  aml-casework: 076fb8e (Phase 19 ed93a0d = C3 fan-in re-derivation, feat/phase-1a-deterministic-verifiers)
---

# Phase 79 — Consume sibling emissions

## 1. Objective

Consume the two sibling emissions that Phase 77 deferred to NAMED briefs, both now code-verified
RESOLVED sibling-side this session:

1. **Lakeshore `cleared` co-sign (the FLOOR — committed).** casework Phase 19 (`ed93a0d`,
   "Closes signal-watch's casework-c3-fan-in-PLAN-BRIEF.md") built `_c3_fan_in`. Re-vendor the stale
   vendored copy (`b3546d4`, fan-out only) → `076fb8e`, shape Lakeshore CASE-B into a fan-in-C3
   casework bundle, `--disposition cleared` → casework SIGNS the dismissal end-to-end. Completes the
   north-star rich-case loop (Northgate FILES / Lakeshore CLEARS, both via casework, not just
   signal-watch's own engine). Companion-only, no dist touch.
2. **Merge real-data oracle (the GATED UPSIDE).** substrate Phase 32 (`31cb439`) mints genuine
   same-person fragments under `--anchored`: cluster ids are opaque `GT-<sha1>` keyed on the latent
   gen entity, DISJOINT from every resolver input (`entity_ref ≠ cluster`) — structurally curing the
   Phase-77 circular oracle (`ENT-<entity_ref>` echo). Score the merge console's real cases against
   this non-circular oracle — but MEASURE-FIRST companion-only before any `dist/merge` re-freeze.

## 2. The verified blocks are now resolved (re-verify before acting — sibling state drifts)

- **casework** advanced `b3546d4` → **`076fb8e`** (Phase 19). `_c3_fan_in` added to
  `grounding_replay.py` (≥N distinct inbound CREDIT originators via `counterparty_name`,
  single-originator refused, window-checked); fan-out byte-unchanged, no contract bump; ships a
  Lakeshore-shaped fixture `case-cleared-c3-fanin-06.json` that signs `cleared`. **The vendored copy
  signal-watch subprocesses is still `b3546d4` (fan-out only) — the consume REQUIRES a re-vendor.**
- **substrate** advanced `9677a37` → **`c099259`** (Phase 33). Phase 32 (`31cb439`)
  `derive_slice_clusters` keys each ref on its latent gen entity (`linkage.get(ref, ref)`) → opaque
  `GT-<sha1>` cluster id; `tests/test_anchored_fork_fragments.py` asserts `len(refs) > len(set(clusters))`
  and ≥1 cluster spanning ≥2 distinct `entity_ref`s (a `P-FRAG-*` fragment merged with a real owner).
  Phase 33 (`f9e63e7`) added open-data Stage-1 realism (Census/SSA/GLEIF names) behind the same flag.
- **CAVEATS (load-bearing):** (a) the genuine fragments exist ONLY under the opt-in `--anchored`; the
  default build is the unscorable echo (the substrate A1 guard). (b) The verifier's live
  `--anchored --emit-eval-oracles` run **CRASHED** (substrate `ReplayError fin-2023-alert003:IND-05`
  at n=400/seed0) before the emit step — the property is proven only by tests that drive
  `build_dataset` directly, bypassing the full CLI replay. **The emit reproducing end-to-end on a
  pinnable param set is the phase's weakest assumption (A1) — T3 is its measure-first gate.**

## 3. Scope (in)

- **Floor:** `vendor/aml-casework/**` (re-vendor via `scripts/vendor_casework.sh`),
  `data/casefile/**` (Lakeshore CASE-B fan-in-C3 bundle), `scripts/serve_workbench.py`,
  `scripts/serve_chain.py` (the `--disposition cleared` path).
- **Gated upside:** `scripts/resolution_scorer.py`, `scripts/curate_merge_cases.py`,
  `tests/fixtures/merge-anchored-oracle/**` (the no-substrate-replayable confusion capture +
  baseline), then (gated) `data/merge/cases.json`, `scripts/build.py` (`validate_merge_cases`),
  `merge.html`, `dist/merge/**`, `tests/merge-console.test.mjs`.
- **Docs:** the three now-resolved `docs/*-PLAN-BRIEF.md`, `docs/cross-pillar-build-order.md`,
  `CLAUDE.md`.

## 4. Scope (out / DEFERRED, named)

- ANY change to `evidence_requirements.evaluate_sufficiency` / the determination + file bar (the A1
  guard — `git diff --quiet`).
- The 8 non-merge ship dists (showcase ×3, corpus, news, console, triage, launcher) — BYTE-FROZEN.
  `dist/merge` is the ONE sanctioned re-freeze, GATED on the T3 measure-first result.
- substrate open-data Stage-2/3 (sanctions anchors / paid landmines — not yet built); a separate
  consume if/when emitted.
- Probabilistic/Splink ER, graph/Kuzu, medallion/DuckLake (named-deferred since Phase 76).

## 5. The honesty frame (LOAD-BEARING)

- **The Phase-77 abort rule governs the merge track.** A "scored" claim is permitted ONLY if the
  oracle is provably independent of the spine's `entity_ref` decision key (the `GT-<sha1>` hash is —
  verified) AND the scored population is genuinely two-sided (correct-rejections AND should-merge
  fragments). Tautological-or-one-sided → STOP to CONSENSUS, never a fabricated score.
- **Consensus-vs-scored split (Phase-76 decision) holds:** if the real cases become scored, the
  Verdict + ledger keep the consensus/scored split visible; synthetic-substrate-anchored qualified
  ("measured on synthetic clusters; production has no ground truth"), never presented as production
  catch-rate / lift / precision / recall.
- **The honest Lakeshore consume:** the CASE-B bundle is shaped to casework's ACTUAL fan-in C3
  contract from Lakeshore's real network (multi-originator → one beneficiary); no fan pattern is
  fabricated to force the sign (the Phase-77 A3 discipline — the sign must be earned by the evidence).
- **The firewall:** build.py imports no spine/scorer/sibling/curate; `validate_merge_cases` stays in
  EXACT parity with the curate firewall (Phase-76); the oracle truth rides only the post-disposition
  `oracle` block (`MERGE_TRUTH_LEAK_KEYS`), never pre-adjudication evidence.

## 6. Exit criteria

1. **Floor:** `scripts/serve_workbench.py --selftest` shows Lakeshore CASE-B signs `cleared`
   end-to-end via fan-in C3 AND the Northgate FILE half still files (the matched pair holds), the
   live-engine verdict matching the authored `expected_*` (fixture-drift bridge). Vendored
   `grounding_replay.py` exposes `_c3_fan_in`; the gate funnel (202/111/63) holds.
2. **Gated upside (T3):** `tests/fixtures/merge-anchored-oracle/` capture replays a non-tautological
   two-sided real-data confusion structure with NO substrate run (the Phase-78 harness pattern);
   `assert_no_cluster_leak` / the resolver-input firewall holds. **OR** the documented abort: emit
   won't reproduce / result tautological-or-one-sided → the honest non-result + a substrate
   emit-stability brief; T4 does not run.
3. **Gated upside (T4, only if T3 clean):** `dist/merge` re-frozen with the real cases scored
   (consensus→scored), `node tests/merge-console.test.mjs` green, validate↔curate parity,
   the honesty-governor word-ban holds.
4. **Invariants:** `git diff --quiet scripts/evidence_requirements.py` (A1). build.py imports no
   spine/scorer/sibling/curate (grep-clean). `python3 scripts/build.py --check all` → the 8
   non-merge dists byte-frozen (dist/merge re-frozen iff T4 ran, else byte-frozen too).
   `uv run pytest` green.
5. **Docs:** the three briefs annotated closed with their resolving sibling commits;
   `cross-pillar-build-order.md` trued-up to the live HEADs (substrate c099259 / casework 076fb8e).

## 7. The measure-first gate (the falsifiable assumption)

**Weakest assumption (T0 / A1):** that substrate's `--anchored --emit-eval-oracles` can be made to
reproduce a clean, scorable oracle this phase (it crashed today). **T3 is the gate:** pin a known-good
param set (route around the `ReplayError`; substrate's tests drive `build_dataset` directly), drive
the emit, score the spine's real refusals + fragment should-merges, capture the confusion structure.
If the emit won't reproduce after bounded attempts → the crash is a substrate bug, not a param issue
→ STOP the merge track, author a substrate emit-stability brief, deliver the Lakeshore floor. **A2
guard:** even if it reproduces, if the scored result is effectively one-sided / tautological → STOP to
consensus. A weak-but-real two-sided result is a legitimate honest outcome.

## 8. Abort rules

STOP-and-surface on any of: an UNSANCTIONED ship-dist drift (the 8 non-merge dists, or `dist/merge`
before its T3 gate passes) · a build.py spine/scorer/sibling/curate import · an
`evidence_requirements.py` change · a fabricated fan-in pattern to force the Lakeshore sign · a
tautological-or-one-sided merge result presented as "scored" · a confusion number presented as a
catch-rate/precision/lift · a funnel regression (202/111/63) at re-vendor. **Measure-first (T3):**
emit won't reproduce OR oracle scores tautological/one-sided → STOP the merge track to consensus + a
substrate emit-stability brief; deliver the Lakeshore floor + the honest non-result; T4 does not run.

## 9. Assumptions ledger

See `.dev-wiki/assumption-ledger.md` Phase 79. Direction gate closed 2026-06-27 (one Step-13 pick via
AskUserQuestion — "Bundle, gated upside"; A1 accepted-as-falsifiable [the T3 measure-first gate], A2
the Phase-77 abort guard, A3 the measure-first reframe, A4 re-vendor-with-checkpoint, A5 the
contract-constraint boundary; all_accept warned-not-silent).
