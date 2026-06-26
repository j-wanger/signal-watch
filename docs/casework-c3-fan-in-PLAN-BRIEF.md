# PLAN-BRIEF — aml-casework: support C3 fan-IN in grounding_replay (the Lakeshore co-sign gap)

> **A signal-watch → aml-casework handoff brief** (the Phase-55–58 / 74–76 pattern: signal-watch authors the
> contract; the sibling implements on its own lifecycle — *no code lands in casework from here*). Synthetic /
> illustrative; no catch-rate, lift, or precision asserted. **Pinned to verified casework HEAD `b3546d4`
> (Phase 18), code-verified live 2026-06-26.** Companion to [`cross-pillar-build-order.md`](cross-pillar-build-order.md).

## The gap (verified, the Phase-77 T3 finding)

casework's CW-4 `cleared` verdict (Phase 18) is built + consumable — signal-watch Phase 77 SIGNS it end-to-end
on a casework-replayable C5 cash-placement case (`data/casefile/cleared-demo.bundle.json`, grounded on the
vendored `fin-2023-alert001:IND-08`; `serve_workbench.cleared_demo_consume`). **But the north-star Lakeshore
case (`data/casefile/case.json` CASE-B) cannot co-sign** — it FAILS-CLOSED at casework's `grounding_replay`:

```
grounding_replay: alerts[AL-LS-C3].replay(C3): only 0 cited outflow(s); the fan-out pattern needs >=5
```

casework's C3 assertion (`grounding_replay._assert_c3_funnel_fan`) is **fan-OUT** — `>=N outflow transactions
within a window` (the layering fan-out). Lakeshore's C3 is **fan-IN** — `multi_originator_funnel_in` (≥N distinct
ORIGINATORS crediting one account; the catering business's many client receipts). Same capability code (C3),
**opposite direction**. Lakeshore has 8 inbound credits + 2 outbound debits → 0 cited outflows → casework's
fan-out replay correctly refuses. casework's other replayable detectors don't fit either (C2 needs outflow≥80%
inflow within 72h — Lakeshore's flow spans weeks; C4/C5 need cash deposits — Lakeshore's are AFT/EMT transfers).

This is the documented Phase-16/63 substrate↔casework C3 divergence (the workbench-fail-closed finding) surfacing
on the rich case. **signal-watch's engine computes Lakeshore → `cleared`** (Phase 73, affirmative mitigation), but
casework refuses to CO-SIGN because it cannot independently re-derive the mechanism — the verifier's defensibility,
NEVER loosened, NEVER faked (signal-watch did not fabricate a fan-out pattern to force a sign — the A3 abort held).

## EMIT (the ask)

Extend casework's `grounding_replay` C3 assertion to ALSO re-derive **fan-IN** (keep fan-out): a C3 alert grounds
if EITHER `>=N distinct outflow counterparties (fan-out)` OR `>=N distinct inbound ORIGINATORS into one account
within the window (fan-in)`. Direction is read from the cited transactions (CREDIT vs DEBIT) + counterparty refs;
the assertion stays a pure per-capability PATTERN re-derivation over the cited txns (no `aml_substrate` import).
The honesty caveat already noted for fan-out (`counterparty_ref=null` ⇒ distinct-counterparty not re-derivable,
count-proxy only) applies symmetrically to fan-in.

## GROUND / CONSUME

- Once casework re-derives fan-in C3, signal-watch's Lakeshore DECIDE co-signs `cleared` end-to-end (the
  `cleared_demo_consume` path already passes `--disposition cleared`; only the Lakeshore bundle's C3 replay is
  blocked today). The cleared rule is unchanged (a grounded exculpatory claim + no grounded inculpatory).
- No file/determination-bar change; additive to the C3 assertion only; the existing fan-out cases stay green.

## Acceptance (sibling-side)

1. `grounding_replay` re-derives a fan-in C3 (≥N distinct inbound originators) as well as fan-out; existing
   fan-out replays unchanged. 2. A Lakeshore-shaped bundle (8 inbound credits from distinct originators, an
   `exculpatory:true` documented-receipt leg) SIGNS `cleared` via `--disposition cleared`. 3. The file bar +
   the other verifiers are byte-unchanged.

**Pin: `b3546d4`** · executed in an aml-casework session · the motivating case is signal-watch's Lakeshore
CASE-B. **Out of scope:** any file-bar / verifier-vocab change; the C3 distinct-counterparty `counterparty_ref`
enrichment (a substrate-side gap, named separately in [`cross-pillar-build-order.md`](cross-pillar-build-order.md)).
