---
title: "Phase 79: Lakeshore co-signs cleared via window-compression + an IND-02-grounded bundle"
aliases: [lakeshore-cosign, window-compression, case-b-bundle]
category: decisions
tags: [cross-pillar, casework, fan-in-c3, lakeshore, cleared, matched-pair, faithfulness, honesty]
parents: [phase-79-consume-sibling-emissions]
created: 2026-06-27
updated: 2026-06-27
source: plan
confidence: high
---

# Decision — Lakeshore's honest co-sign: compress the window, ground the bundle on IND-02

## Context

The north-star matched pair (CASE-A Northgate files / CASE-B Lakeshore clears) only had Northgate
going through casework; Lakeshore's `cleared` was shown via the separate Phase-77 C5 proxy because
casework's C3 was fan-OUT-only. Phase 19 (vendored 076fb8e) built `_c3_fan_in`, but two residual
blockers remained: casework's `_FANOUT_WINDOW=7` (Lakeshore's 8 credits spanned 14 days) and no real
CASE-B casework bundle. The honest-fix constraint (the A3 abort rule): NEVER fabricate the fan-in
pattern.

## Decision

Make Lakeshore co-sign the HONEST way:

- **Window-compression (user-confirmed "compress to ≤7d"):** re-time CASE-B's 8 catering credits
  into a 6d2h window (04-02..04-08) — the SAME 8 distinct clients / amounts / memos, only the dates
  tighten. The multi-originator fan-in is REAL; nothing about the pattern is invented, so the A3 abort
  (no fabricated fan-out/fan-in) holds. Verdict unchanged (still clears).
- **The bundle grounds C3 on the FAITHFUL `fin-2023-alert001:IND-02`** (multi-originator-deposit),
  while `case.json`'s AL-LS-C3 keeps `fin-2020-alert001:IND-05` (social-media-solicitation) for
  matched-pair signal SYMMETRY with CASE-A. The divergence is DISCLOSED in the bundle provenance.

`data/casefile/case-b.bundle.json` (real casework bundle: cited_txns CREDIT/DEBIT + amount_cents +
counterparty_name, an exculpatory:true documented-settlement leg, NO crime_type/inculpatory) +
`serve_workbench.lakeshore_cosign_consume` (selftest-proven, mirrors `cleared_demo_consume`, not
UI-coupled) → `signed:true, disposition:cleared, blocking:[]`.

## Consequences

The matched pair now BOTH route through casework (the stronger demo). The IND-05/IND-02 grounding
divergence is a known, disclosed seam — a candidate future faithfulness fix re-grounds BOTH CASE-A +
CASE-B's C3 to IND-02, deferred because it touches the FILE case and the matched-pair "same signals"
invariant. `evidence_requirements.py` BYTE-UNCHANGED (A1); companion-only (no dist touched by this
track — Northgate still files, the pair holds).

Related: [[decisions/phase-77-casework-cleared-lakeshore-translation]] ·
`docs/casework-c3-fan-in-PLAN-BRIEF.md` · the matched-pair `data/casefile/case.json`.
