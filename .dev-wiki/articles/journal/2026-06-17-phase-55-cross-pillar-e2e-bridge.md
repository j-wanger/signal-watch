---
title: "Phase 55 — Cross-pillar end-to-end bridge: the spine (aggregation + verification)"
type: journal
date: 2026-06-17
phase: 55
tags: [cross-pillar, integration, e2e, verification-harness, launcher, two-beat-delivery, review-gate]
---

# Phase 55 — Cross-pillar end-to-end bridge: the spine

## What happened

Planned + delivered (the signal-watch SPINE) + committed in one session. The cross-pillar review
earlier this session found the program aligned in direction but the substrate→casework interface
**never executed as a wire** (aml-substrate persists no evidence → aml-casework runs on hand-authored
fixtures). Phase 55 builds the signal-watch half that makes the connected demo *provable*; the wiring
routes to sibling sessions via briefs. Shape (user gate): **verifier harness + walkthrough** (PROVE the
join, don't narrate) + an A3 re-scope to a **launcher** (the one ship-surface change).

## Delivered (T1–T6, the spine)

- **T1** `docs/pillar-integration-contract.md` §2/§5a RATIFIED — bundle-per-case json at
  `evidence/<run_id>/<case_id>.json` conforming to `aml_casework.contract.validate_bundle`, + the
  deterministic `alert_id`/`dossier_id` sha1 mint rule. Grounded in casework's actual `validate_bundle`.
- **T2** `docs/e2e-acceptance.md` — the deterministic "connected" definition (C4 slice; checks A/B/C).
- **T3** `scripts/e2e_chain_check.py` (NON-ship, stdlib, NO sibling import — only `derive_signals.normalize`).
  `--selftest` green on a synthetic C4 fixture pair (`data/e2e/*`); `--real` honestly gated; emits
  `data/pillar-status.json`. Adversarially confirmed the grounding + dangling-cite + id-mint checks catch.
- **T4** the launcher `launcher.html` → `dist/index.html` (8th build target). Single offline front door:
  links the 5 artifacts + renders the 3 bridge states from inlined `pillar-status.json`. `tests/launcher.test.mjs`
  (23 assertions). **Removed the obsolete M1 stale-`dist/index.html` deletion in `build.py`** (it would
  have deleted the launcher — DISCOVERY escape hatch, noted in code + commit).
- **T5** two sibling PLAN-BRIEFs (in the sibling repos, uncommitted there for their sessions):
  `aml-substrate/docs/persist-evidence-seam-PLAN-BRIEF.md` (§5a) + `aml-casework/docs/consume-real-bundle-PLAN-BRIEF.md`.
- **T6** `docs/e2e-walkthrough.md` (two-beat presenter script) + smoke-checklist section.

## Health delta

New: `tests/launcher.test.mjs` (23 assertions, green); `e2e_chain_check.py --selftest`. `--check all`
7→8 targets, zero drift. No regressions (`gate-console.test.mjs` PASS; the 5 existing dists byte-identical).

### Review Gate (4+ tasks + a ship artifact → dispatched a reviewer over b37d7a0)

Reviewer **confirmed the id-mint rule is byte-identical** across the contract, the harness, and both
sibling briefs (ran all three as code — identical hashes; the headline cross-pillar risk, clean). Four
findings fixed in `e95df82`:
- **HIGH** — `--real` on the synthetic `data/e2e/*` fixtures flipped the committed `pillar-status.json`
  to a false "connected"/green launcher (+ dist drift). Fix: `--real` REFUSES paths under `data/e2e/`.
- **MED** — `signoff` was optional; the "signed SAR" claim now requires it (hard violation if absent).
- **LOW×2** — enforce `illustrative:true` on the signed SAR too; sort the corpus glob for determinism.

### Gate Compliance

`<!-- gate-log:phase-55 direction=approved delivery=pending -->` — direction gate present (all_accept:
false, A0–A3 positioned). Delivery: the spine is delivered + committed (beat 1); the gate stays
`pending` because the full delivery (the `--real` chain green) is the two-beat gate, gated on the
sibling sessions. The phase stays ACTIVE.

## Two-beat delivery state

- **Beat 1 (spine): DELIVERED + committed** (`b37d7a0` + `e95df82`). `dist/index.html` opens offline;
  the chain panel honestly shows all bridges **pending**.
- **Beat 2 (the real chain): GATED on the sibling sessions.** When bridge #1 (substrate persist) + #2
  (casework consume) land in their own repos, `e2e_chain_check --real` flips the panel green. The phase
  cannot fully close from signal-watch.

## Soft Observations / Phase N+1 Candidates

- **The two sibling bridges are the next work** — bridge #1 (`aml-substrate` §5a persist+mint-ids) then
  bridge #2 (`aml-casework` consume-real-bundle), each in its OWN rooted session (the briefs are the
  hand-off). Beat 2 of this phase's delivery gate depends on them. The casework brief names A0 (the real
  emission conforms to `validate_bundle` as-is) as the load-bearing risk — the first real ingest is where
  any hand-mirror schema drift surfaces.
- **`docs/pillar-integration-contract.md` §6** still says "compose the ≥2 grounded axes" — mildly stale
  vs §3's ratified "≥1 axis suffices" (the triple-null). A future contract-consistency tidy; left out of
  Phase-55 scope (T1 was the serialization §2/§5a, not §6).
- **The grounding HEAD pins** (`GROUNDING_HEADS` in `e2e_chain_check.py` + `pillar-status.json`) are
  hardcoded constants — the honest re-ground-before-consume artifact. A future could derive them, but
  that would couple to the sibling repos; the hardcode is deliberate.
- **Once beat 2 lands**, consider whether the launcher should fold into the demo-(A) presentation flow,
  and whether the 3 showcase typologies should collapse into one card.
