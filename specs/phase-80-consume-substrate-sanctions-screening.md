# Spec — Phase 80: Consume substrate Phase 34 (OFAC name-collision merge case class + non-tautological C14 §12 leg)

> STANDARD ceremony. Cross-pillar consume + a conditional ship-dist touch. Direction gate closed
> 2026-06-27 (AskUserQuestion — "Consume P34: merge + workbench" + the one-sided fallback = "Abort
> merge → companion + brief"). Both sibling HEADs code-verified LIVE this session (file:line, not
> loaded facts): aml-substrate @**1f5901e** (Phase 34), aml-casework @**076fb8e** (Phase 19).

## 1. Objective

Consume aml-substrate's one genuinely-unconsumed emission — **Phase 34 "seam-5 sanctions screening
realism"** (`1f5901e`): the dead `sanctions_flag` made LIVE under `--anchored` via a label-blind
real-OFAC-watchlist NAME COLLISION, plus the revived non-tautological C14 KYC-integrity branch that
fires on sanctions-flagged parties. Two consumes:

1. **Merge console** — add an **OFAC watchlist name-collision** case class: a synthetic party whose
   (real-frequency) name collides with a real public-domain OFAC entry — *same latent entity (uphold
   the link) or common-name false positive (reject)?* The single most recognizable entity-resolution
   decision in AML sanctions screening, landing in the one gate with a measurable oracle.
2. **Workbench §12** — feed the revived sanctions-driven **C14** into the determination loop so the
   KYC leg lights from a REAL signal, not the EDD≔HIGH tautology (the C14→kyc path already exists,
   Phase 72; this only supplies a non-tautological signal).

Plus: author the substrate **P35 handoff brief** (the now-confirmed remaining frontier) and true up
the cross-pillar docs + two drift items.

## 2. Context

- Phases 32–33 (`--anchored` same-person fragments + real-frequency names) are ALREADY consumed —
  the Phase-79 merge slice carries them (verified: "Anna Vega"/"Anna eVga" fragment pairs in
  `data/merge/cases.json`). Phase 34's sanctions layer is the delta; the slice has no
  sanctions/watchlist/OFAC/C14 content.
- substrate's remaining emissions (TF slice, C1 anticipated-activity [a *documented measured null*,
  not a gap], broader C7, org-name sanctions, Stage-2/3 open data) are **P35+ and not yet built** →
  this is likely signal-watch's last substantial local consume for a while; queue the P35 brief.
- casework (`076fb8e`) sits exactly at the Phase-79 vendor pin — nothing new to consume; one drift
  correction worth banking: its txn-less C14 party-leaf is **no longer fails-closed** (it completes
  via the resolving party leaf; test fixture reaches `signed`) — CLAUDE.md's Phase-72
  "kyc signing is the txn-contract frontier" note is now partially stale.

## 3. Constraints (LOAD-BEARING)

- **A1 guard:** `scripts/evidence_requirements.py` BYTE-UNCHANGED (`git diff --quiet`).
- **Firewall:** `build.py` imports no spine/scorer/sibling/curate (grep guard); the **8 non-merge
  ship dists byte-frozen** (`--check all`); `dist/merge` the ONE sanctioned re-freeze, GATED on T1.
- **validate↔curate parity:** build.py `validate_merge_cases` mirrors `curate_merge_cases` EXACTLY
  (the Phase-76 lesson); the post-disposition `oracle` block never leaks into pre-adjudication
  evidence (`assert_no_*_leak`).
- **Compliance:** real OFAC names ship clean under 17 USC §105 (US-federal public domain — the
  existing exception explicitly covers OFAC). Framed STRICTLY as the **false-positive trap** — the
  synthetic party is NEVER the sanctioned entity; never "we caught a sanctioned party." Badge
  always-on; synthetic-substrate-anchored qualifier governs any scored claim.
- **Honesty governor:** no catch-rate / lift / precision / recall / multiplier wording; a confusion
  count is never a catch-rate.
- **Measure-first:** T1 is the abort gate. The merge track (T2/T3) runs ONLY on a clean, two-sided,
  non-circular T1; the workbench track (T4) + the P35 brief (T5) run regardless.

## 4. Approach

Three tracks + true-ups, measure-first gated (the Phase-79 pattern):

- **T1 (the gate)** — run substrate @1f5901e `--anchored --emit-eval-oracles` (the GT-`<hash>`
  merge oracle path) AND `--anchored` evidence/screening bundles (the C14-from-sanctions case
  material) as TOOL-USE (subprocess, the curate pattern; build.py never imports it); distill a
  no-substrate-replayable capture. **Assess two-sidedness:** are the watchlist-name collisions
  two-sided (some TRUE latent-entity matches + some common-name false positives), distinguished
  non-circularly by the GT-`<hash>` oracle? Record the count; document the gate decision.
- **T2/T3 (gated on T1 two-sided)** — curate the `sanctions-name-collision` basis into
  `data/merge/cases.json` (validate↔curate parity); rebuild + re-freeze `dist/merge`; render the
  false-positive-trap framing in `merge.html`; update `tests/merge-console.test.mjs`.
- **T4 (always)** — land ≥1 sanctions-driven C14 case (additive, provenance-tagged) into the
  workbench §12 loop; prove the kyc leg lights from it. evidence_requirements.py byte-unchanged.
- **T5 (always)** — the substrate P35 brief + cross-pillar-build-order true-up + the casework
  C14-fails-closed drift correction + reconcile the stale FOLLOW-ON markers.

## 5. Scope

`scripts/curate_merge_cases.py` · `data/merge/cases.json` · `scripts/build.py` (validate_merge_cases)
· `merge.html` · `dist/merge/**` · `tests/merge-console.test.mjs` · `tests/fixtures/merge-sanctions-oracle/**`
· `data/entity-spine/**` · `scripts/curate_workbench_cases.py` · `scripts/serve_workbench.py` ·
`data/workbench/**` · `tests/workbench.test.mjs` · `docs/*-PLAN-BRIEF.md` · `docs/cross-pillar-build-order.md`
· `CLAUDE.md` · `.dev-wiki/tasks.md` (FOLLOW-ON reconciliation). NO change to `evidence_requirements.py`.

## 6. Exit criteria

- T1 capture committed + replays with NO substrate; the two-sidedness decision documented; firewall holds.
- IF two-sided: `--check all` 9/9 (8 byte-frozen + `dist/merge` re-frozen); `node tests/merge-console.test.mjs`
  green incl. the new basis; validate↔curate parity; honesty word-ban holds.
  IF one-sided/flaky: `dist/merge` BYTE-FROZEN (untouched); a substrate emit-two-sidedness brief authored;
  the merge non-result documented honestly.
- A sanctions-driven C14 case in the workbench; the §12 kyc leg lights from it; `node tests/workbench.test.mjs`
  green; gather/workbench harnesses pass; `git diff --quiet scripts/evidence_requirements.py`.
- The substrate P35 brief exists; cross-pillar-build-order trued up to Phase-34 HEAD; the casework
  C14-fails-closed drift corrected; the stale FOLLOW-ON markers reconciled; `uv run pytest` green.

## 7. Risks / assumptions

- **A1 [HIGH, weakest, measure-first]:** the Phase-34 `--anchored` sanctions emit yields a TWO-SIDED,
  non-circular merge oracle. "Label-blind collision" risks being all-false-positive-by-construction
  (the synthetic party never IS the watchlist entity) → a one-sided oracle (the Phase-77 trap).
  → measure-first T1; one-sided ⇒ ABORT merge to workbench-only + brief (user-positioned 2026-06-27).
- **A2 [HIGH]:** the collision shapes as an entity-LINK merge candidate (party vs watchlist entity)
  fitting the merge arc. → confirmed in T1; if not, route to workbench (screening-disposition frame).
- **A3 [MED]:** `dist/merge` is the ONE sanctioned re-freeze (2nd consecutive); 8 non-merge dists
  byte-frozen; validate↔curate parity held.
- **A4 [MED]:** real OFAC names ship clean (17 USC §105), framed strictly as the false-positive trap.
- **A5 [MED]:** the workbench C14 enrichment is ADDITIVE (provenance-tagged) to the existing v0.5
  slice — NOT a full re-curate — and touches no `evidence_requirements.py` byte.

## 8. Checkpoints

- **T1 ABORT GATE** — after the emit + scoring, STOP and report the two-sidedness count + the
  gate decision before T2 touches any dist. One-sided/flaky → the merge track does not run.
- Post-T3 — adversarial review of the re-freeze (the Phase-79 staleness lesson: verify the committed
  `cases.json` CONTENT + `git status` + `--check merge`, not the "wrote…" log).

## 9. Out of scope

- The substrate P35 build itself (TF/C1/C7/org-sanctions/Stage-2-3) — brief-only this phase.
- A full workbench re-curate to substrate Phase 34 (T4 is additive, not a population swap).
- Any `evidence_requirements.py` change (A1); the naive-resolver over-merge quadrant; casework's
  CI-promotion criterion; the Lakeshore IND-05/IND-02 grounding-faithfulness fix (carried).
