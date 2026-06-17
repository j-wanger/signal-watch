---
title: "Phase 55 — Cross-pillar end-to-end bridge: aggregation + verification (the 3-pillar full demo connected)"
type: phase
status: active
ceremony: lite
milestone: M9
created: 2026-06-17
updated: 2026-06-17
tags: [cross-pillar, integration, e2e, verification-harness, launcher, non-ship-mostly, file-contract, aml-substrate, aml-casework, c4-structuring, two-beat-delivery]
---

# Phase 55 — Cross-pillar end-to-end bridge: aggregation + verification (the 3-pillar full demo connected)

## Objective

Connect the 3-pillar full demo. The review (this session) verified the program is **aligned in
direction but the cross-pillar interface has never executed as a wire**: aml-substrate persists no
evidence (`cli.py` prints + discards; no `evidence/` dir, no id-mint), so aml-casework's chain runs on
hand-authored synthetic bundles — the substrate→casework join is a designed seam, not a wire. The
actual wiring must execute in SIBLING sessions (their dev-* hooks bind there); **the aggregation +
final delivery sit in signal-watch.** This phase delivers the signal-watch SPINE that makes the
connected demo *provable* and *presentable*, and routes the wiring to the siblings via briefs.

## Approach (gated 2026-06-17 — "verifier harness + walkthrough" + the launcher re-scope)

Shape question answered **A — verifier harness + walkthrough** (PROVE the join with a re-runnable
cross-repo check, not narrate it). A3 reject of pure-non-ship → re-scoped to **launcher + live
pillar-status** (one new ship-surface file). signal-watch delivers, this session:

1. **Ratify the serialization format** (`docs/pillar-integration-contract.md` §2/§5a PROPOSED→RATIFIED;
   close §7) — the concrete `evidence/` layout + per-record json + the deterministic `alert_id`/
   `dossier_id` mint rule. This is the spec sibling brief #1 implements.
2. **`docs/e2e-acceptance.md`** — the deterministic definition of "the chain connects": a
   substrate-emitted **C4-structuring** bundle → casework's 6 Class-G verifiers green → `record_signoff`
   signed=True → grounding resolves to `fin-2026-alert001:IND-11` in the frozen corpus.
3. **`scripts/e2e_chain_check.py`** (NON-ship, stdlib, **no sibling import**) — reads committed/vendored
   sibling outputs (the file-contract / vendored-pin pattern) and asserts the join: schema-match,
   id referential integrity, SAR-citation→evidence→corpus resolution. Ships fixture-proven (`--selftest`
   on a synthetic C4 bundle matching the ratified schema); `--real` gated honestly until the siblings
   land. Emits `data/pillar-status.json` (the three bridge states).
4. **The launcher** — `launcher.html`→`dist/index.html` (8th build target): the single front door
   linking the 5 existing artifacts in arc order + a cross-pillar panel rendering `data/pillar-status.json`
   (inlined at build, like every artifact's config). The 5 existing artifacts stay byte-frozen;
   `--check all`→8/8.
5. **Two sibling PLAN-BRIEFs** (the established hand-off pattern) — aml-substrate §5a persist+mint-ids;
   aml-casework consume-real-bundle. Shared external acceptance = `e2e_chain_check --real` green.
6. **`docs/e2e-walkthrough.md`** — the presenter script + the two-beat delivery framing.

The C4 slice is **code-verified reachable on the existing pin**: substrate `StructuringDetector`
(capability=C4) is grounded in `fin-2026-alert001:IND-11`; that pinned record (casework vendors it) has
`IND-11`→C4; casework `grounding_replay.py` registers `"C4"`. Three-way alignment, no pin-widening.

## Scope

- `docs/pillar-integration-contract.md` · `docs/e2e-acceptance.md` · `docs/e2e-walkthrough.md`
- `scripts/e2e_chain_check.py` · `data/e2e/**` · `data/pillar-status.json`
- `launcher.html` · `scripts/build.py` (launcher target) · `dist/index.html` · `tests/launcher.test.mjs`
- `tests/smoke-checklist.md`
- `aml-substrate/docs/persist-evidence-seam-PLAN-BRIEF.md` · `aml-casework/docs/consume-real-bundle-PLAN-BRIEF.md` (authored here, executed in sibling sessions)

## Exit criteria (the SPINE — this session)

1. Contract §2/§5a RATIFIED (no PROPOSED on the schema rows); §7 serialization Q struck.
2. `docs/e2e-acceptance.md` names the C4 slice + the exact assertions e2e_chain_check makes.
3. `scripts/e2e_chain_check.py --selftest` green on the synthetic fixture; `--real` honestly gated;
   `! grep -nE "import aml_substrate|aml_casework"` clean; regenerates `data/pillar-status.json`.
4. `dist/index.html` builds (8th target); `node tests/launcher.test.mjs` green; `--check all` 8/8 with
   the 5 existing dists byte-identical.
5. Both sibling PLAN-BRIEFs written with the shared `--real` acceptance criterion.
6. `docs/e2e-walkthrough.md` + smoke-checklist pointer.

## Delivery gate (the second beat — GATED on siblings)

The end-to-end `--real` verification (and `data/pillar-status.json` flipping to all-green) closes when
the sibling sessions land bridge #1 (substrate persist+ids) + #2 (casework consume-real-bundle) and
`e2e_chain_check --real` passes. The delivery report distinguishes **spine-delivered / fixture-proven**
(now) from **real-chain-verified** (gated).

## Assumptions (ledger: Phase-55 block, all_accept: false)

- **A0 [HIGH, T0-weakest]** §5a schema ratifiable NOW → fixture-harness matches real emission. ACCEPT —
  the harness IS the divergence detector; brief #1's acceptance is `--real` green.
- **A1 [HIGH]** verify by reading committed sibling outputs, no code import (file-contract / vendored-pin).
  ACCEPT — casework's corpus pin precedent proves it.
- **A2 [MED]** the C4-structuring slice grounds on the existing pin, no widening. ACCEPT — don't-know
  round 1 → DEFENDED by code (three-way C4↔IND-11↔C4 alignment).
- **A3 [MED]** the launcher (dist/index.html, 8th target) + pillar-status is the ONE ship-surface
  addition; the 5 existing artifacts byte-frozen; console/triage NOT re-opened. ACCEPT — reject round 1
  (pure-non-ship) → re-scoped.

## Abort

Any of the 5 EXISTING dists drift, or console/triage touched → STOP and surface (never re-baseline). The
harness importing sibling code → out of bounds (file-contract only). Any synthetic fixture presented as
real substrate output → out of bounds (Illustrative). Grounding HEADs: aml-substrate@bafc67d ·
aml-casework@0316580 — re-verify before consuming a sibling fact (the re-ground-before-consume rule).
