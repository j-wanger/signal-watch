---
title: "Phase 60 — Consume the landed sibling halves (substrate P16-18 + casework P10-12): the C7 reachable-now rise + the real e2e chain"
type: phase
status: completed
ceremony: lite
milestone: M9
created: 2026-06-19
updated: 2026-06-19
tags: [cross-pillar, signal-coverage-map, e2e-chain, consume, re-ground, reachable-now, c7, emergence-doctrine, behavior-emergence, sibling-briefs, non-ship]
---

# Phase 60 — Consume the landed sibling halves: the C7 reachable-now rise + the real e2e chain

## Objective

A cross-pillar review (code-verified this session) found **both siblings moved 3 phases past the Phase-59
pins**:

- **aml-substrate@9c75c03** (Phase 18): §13 fourth-null closure (P16) · party-bearing bundle + `--screen`
  (P17) · **emits the real C8 party-bearing v0.2 evidence bundle**, sample `CASE-P-0000251.json` (P18).
- **aml-casework@c6d8401** (Phase 12): **C7** grounding_replay assertion (P10) · **C8** (P11) · **C14**
  party-leaf reference-by-path (P12); **C26** deliberately UNREGISTERED — the honest null.

Phase 59 A2 said reachable-now rises only when a party-bearing emission (substrate) + the paired
grounding_replay assertions (casework) BOTH land. They now have. Consume them: re-ground the coverage map,
**verify-first then re-freeze**, and run the **real** e2e chain on substrate's C8 bundle → a casework SAR.

## The verified consequence — only C7 moves

Reachability is a strict 3-way AND: `has_detector ∧ has_casework_assertion ∧ behavior_emergence == "emerges"`.
Reading the code-verified pin facts against the now-landed sibling work:

| Cap | has_detector | casework assertion (was→now) | behavior_emergence | re-ground effect |
|-----|--------------|------------------------------|--------------------|------------------|
| **C7** | ✓ (P15) | false → **true** (P10) | **emerges** | **all 78 buildable C7 signals → `reachable-now`** |
| C8 | ✓ | false → true (P11) | `data-only` | no move (3rd leg fails) |
| C14 | ✓ | false → true (P12) | `data-only` | no move (3rd leg fails) |
| C26 | ✓ | (unregistered, honest null) | `absent` | no move (3rd leg fails) |

C7 has **78** buildable signals: 62 `needs-detector` + 15 `needs-behavior` + 1 `needs-view-exposure` (verified).
`is_reachable` is evaluated FIRST in `classify()`, *before* the data_source_class fall-through — so once C7's
assertion lands, **all 78** become `reachable-now` (62 direct on exposed-active data + 16 via transaction-proxy
grounding, the existing 91/93-proxy convention), not just the 62 in `needs-detector`. Re-grounding flips C7's
missing third condition → **reachable-now: 93 → 171 (+78)** — the first *real* rise (matches the 2026-06-18
transient review + the banked memory), the C7 win banked for a combined consume. Residual tiers:
needs-detector 62→0 (the cheapest tier exhausted), needs-view-exposure 70→69, needs-behavior 296→281.

> **Plan-stage correction:** the first verification undercounted this as +62 (counting only `needs-detector`
> C7). Re-reading `classify()` — `is_reachable` precedes the sclass branch — gives the true +78. Caught at
> planning, which is exactly why the user chose verify-first.

**The honest finding (A1):** C8/C14/C26 stay put despite the now-landed casework assertions *and* substrate's
party-bearing emission, because the binding gap is the 3rd leg — `behavior_emergence` (data-only / absent),
which is **neither emission work nor assertion work**. Further reachable-now rises need EMERGENT BEHAVIOR
(substrate emergence-engine work, bottom-up) or are a permanent null (C26). Phase 59's "both halves must
land" sharpens to **"only the capability whose behavior genuinely emerges reaches reachable-now."** The
cross-pillar wiring is provably *not* the screening-capability bottleneck.

## Direction gate (2026-06-19)

`all_accept: true`. The user **up-scoped Q1 to the COMBINED scope** (coverage-map consume + the real e2e
chain) over the recommended coverage-only focus — a deliberate scale-up batching the full landed sibling
work — and chose **"verify first, then freeze"** on the C7 +78.

- **A0 [HIGH — T0 weakest]** Clean C7-only +78 (casework's C7 assertion is green at c6d8401; substrate P16-18
  didn't shift C7's detector/emission). ACCEPT — **verify-first** (re-ground → run → diff → confirm before
  the freeze); STOP-and-surface on any other delta.
- **A1 [HIGH]** C8/C14/C26 don't move — emergent behavior is the screening-cap bottleneck. ACCEPT (held by
  code-verified pin values: C8/C14 data-only, C26 absent).
- **A2 [HIGH]** The real e2e chain is producible + honest-either-way (CONNECTED or a surfaced contract-drift
  GAP); casework's deterministic pipeline runs as a tool (file-contract, no import). ACCEPT.
- **A3 [MED]** NON-ship — `--check all` stays 8/8; build.py never imports either script; both cross-pillar
  artifacts re-grounded against the sibling current HEADs, pinned inline. ACCEPT.

Ledger: Phase-60 block. Grounded against aml-substrate@9c75c03 + aml-casework@c6d8401 + corpus@472b44e.

## Scope

`data/coverage-map/**` (re-grounded pin + re-frozen coverage.json) · `scripts/signal_coverage_map.py`
(read-only verify; `--selftest` goldens re-grounded to the new reality as a regression anchor only) ·
`scripts/e2e_chain_check.py` + `scripts/e2e/**` (re-ground GROUNDING_HEADS + real run) ·
`docs/corpus-substrate-coverage.md` · `docs/pillar-integration-contract.md` (§8) · the two sibling briefs
(`aml-substrate/docs/corpus-coverage-build-PLAN-BRIEF.md`, `aml-casework/docs/capability-assertions-PLAN-BRIEF.md`).

**Not touched:** the 8 build targets / offline dists; the committed corpus records + overlays (read-only);
build.py never imports `signal_coverage_map.py` or `e2e_chain_check.py`; no sibling import (file-contract /
vendored-pin only).

## Tasks

See `tasks.md` (Phase 60 block): T1 re-ground pin + verify-first the C7 +78 · T2 re-freeze coverage.json +
gate · T3 re-ground + run the real e2e chain (C8 bundle → casework SAR) · T4 document + re-ground both
sibling briefs · T5 exit verification.

## Exit criteria

1. `signal_coverage_map.py --check` byte-identical (reachable-now 171) · `--selftest` green · no sibling
   import · build.py never imports it.
2. `e2e_chain_check.py` GROUNDING_HEADS re-pinned · `--selftest` green · a `--real` run completed with an
   honest recorded outcome (CONNECTED or documented GAP) · no sibling import.
3. `docs/corpus-substrate-coverage.md` + contract §8 carry the measured C7 rise + the C8/C14/C26
   emergence-gap finding + the e2e outcome; HEADs re-pinned. Both sibling briefs re-grounded (substrate
   detector/view + party-bearing-emission half DONE → next = emergence-engine work; casework C7/C8/C14
   assertions DONE [C26 honest null] → next per its roadmap; shared acceptance + doctrine constraint).
4. `python3 scripts/build.py --check all` → 8/8, the 8 ship dists byte-identical; ZERO ship artifacts in the
   change set.

## Abort

Any of the 8 offline dists drift / a ship artifact touched → STOP and surface (never re-baseline). The C7
+78 verify (T1) comes back as anything but a clean C7-only +78 → STOP, do NOT freeze. A brief that stamps
behavior or labels → out of bounds (emergence doctrine). The companion importing sibling code → out of
bounds. A validator/selftest looks like it needs loosening → fix the data/design, never the check.
