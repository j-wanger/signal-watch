---
title: "Phase 61 — Blueprint review against what's been implemented"
status: completed
ceremony: lite
created: 2026-06-20
updated: 2026-06-20
grounding_heads:
  aml-substrate: 34400e2   # Phase 20
  aml-casework: c6d8401    # Phase 12
  signal-watch-corpus: 472b44e
---

# Phase 61 — Blueprint review against what's been implemented (+ batched cross-pillar re-ground; deep blueprint true-up)

## Why

`docs/program-blueprint.md` is a **Phase-47/48 DESIGN snapshot**. Its own standard:
*"nothing claims to be built unless it names a committed artifact"* / *"Workloads marked
(design-stage) do not exist."* Since it was written, the program **split into pillars** (P50) and
built an enormous amount: **aml-substrate P1–20** (@34400e2 — detectors C2–C15 + screening
C7/C8/C14 + composition stress-bench + the C14 emergence honest-null) · **aml-casework P1–12**
(@c6d8401 — 6 Class-G verifiers + the real neural narrator + grounding_replay C7/C8/C14 + signed
SAR) · signal-watch's **coverage map / e2e chain / C/D control / corpus-redundancy / chain
workbench**. The four §3 **"(design-stage)"** rows (txn monitoring · case investigation · SAR/STR
narrative · LFCM assist) now carry substantial committed **sibling** implementation — so the
blueprint's central built-vs-design partition is **materially stale, by the doc's own honesty
standard**.

## Objective

AUDIT §1–§15 against committed artifacts across all three repos (file-contract, NO sibling import)
→ adversarially **verify** every "now built" claim at its pinned HEAD → write the committed
reconciliation report → apply the **verified-gated** blueprint deep revision → re-sync the report
HTML. The cross-pillar re-ground (coverage map + e2e pins, stale at P18) is **batched in**
(verify-first, no-op expected — substrate P19/P20 added no screening detector).

## Direction (gate 2026-06-20, all_accept: true)

The user (under ultracode) chose **C — report + deep blueprint revision**; **batched the
cross-pillar re-ground** (A1 up-scope over the recommended report-only review boundary — the
Phase-60 batching instinct); **re-sync blueprint-report.html** (A3).

- **A0 [HIGH — T0 weakest] ACCEPT** — verify-first gates every blueprint edit; where the binary
  built/design-stage would overclaim a synthetic, pillar/probe-scale build, the marker becomes an
  honest **third status** ("pillar-build / synthetic-scale"). The spine: prevents the revision
  laundering "synthetic pillar build" into "built workload".
- **A1 [HIGH] ACCEPT (batched)** — the coverage-map + e2e re-ground to substrate@34400e2 /
  casework@c6d8401 is a verify-first **no-op-EXPECTED** consume; non-zero tier movement / an e2e
  GAP → STOP-and-surface, never a silent re-freeze.
- **A2 [HIGH] ACCEPT (USER OVERRIDE)** — re-opening the FROZEN-set blueprint is sanctioned; "Status:
  DESIGN" + §15 non-negotiables preserved; cross-repo refs + HEAD pins enter the blueprint.
- **A3 [MED] ACCEPT** — re-sync the report HTML's revised sections + a md↔html consistency check.
- **A4 [MED] ACCEPT** — non-ship EXCEPT the sanctioned launcher re-ground (the e2e cascade via
  data/pillar-status.json — the Phase-60 Option-A pattern); 7/8 dists byte-identical; --check all 8/8.

## Scope

`docs/blueprint-implementation-review.md` (NEW) · `docs/program-blueprint.md` (verified-gated
revision) · `docs/blueprint-report.html` (revised-section re-sync) · `data/coverage-map/**` ·
`scripts/signal_coverage_map.py` (read-only verify + selftest goldens) · `scripts/e2e_chain_check.py`
+ `scripts/e2e/**`. NOT touched: the 7 non-launcher dists; committed corpus records/overlays
(read-only); build.py never imports the two scripts; NO sibling import.

## Tasks

T1 audit → report (L) · T2 batched verify-first re-ground (M) · T3 verified-gated blueprint deep
revision (M) · T4 blueprint-report.html re-sync (S) · T5 exit verification (S). See `tasks.md`.

## Exit criteria

1. `docs/blueprint-implementation-review.md` — per-§ three-tier status (every built/pillar-built
   status names a verified artifact + HEAD), both-direction drift, re-grounded next-frontier; HEADs
   pinned.
2. `docs/program-blueprint.md` revised — every change traces to a verified finding; three-tier
   legend; §3 markers + §8/§11/§13 prose trued-up; no overclaim; "Status: DESIGN" + §15 preserved.
   `blueprint-report.html` revised sections synced.
3. `signal_coverage_map.py --check` byte-identical (re-frozen, reachable-now 171, zero movement
   confirmed) · `--selftest` green · `e2e_chain_check.py` re-pinned, `--selftest` green, `--real`
   recorded (CONNECTED/GAP) · no sibling import; build.py never imports either.
4. `build.py --check all` → 8/8; `git diff --stat HEAD -- dist/` shows ONLY dist/index.html.

## Abort

Any OTHER dist drifts / a non-launcher ship artifact touched / the blueprint becomes a build target
→ STOP. The re-ground diff ≠ zero tier movement → STOP, do NOT re-freeze (surface as a finding). A
blueprint edit that OVERCLAIMS → out of bounds. Sibling import → out of bounds.
