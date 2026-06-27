# Determination-validation harness + the §12 discovery feed (Phase 78)

> Companion-only (dev/authoring-time). `build.py` NEVER imports the harness; no ship dist is touched; the
> determination engine (`evidence_requirements.py`) is BYTE-UNCHANGED. Synthetic; counts only — no
> rate, score, or multiplier is claimed.

## What it is — the "circularity exit"

The FIRST validation of signal-watch's determination engine against an oracle it did **not** author.
aml-substrate (Phase 31 `--emit-eval-oracles`) emits `eval/intended_disposition.json` — a `file`|`clear`
label per slice case, authored **BLIND to the sufficiency rule**. Because the oracle is independent of
`evaluate_sufficiency`, comparing the engine's signal-assembly to it is a genuine measurement — unlike the
Phase-77 merge-66 `true_entities` oracle, which was a content-addressed relabel of the spine's own key
(circular, correctly deferred; substrate Phase 31's own commit re-confirms it is all-singleton).

## The non-circular frame (load-bearing)

The `file` bar = **mechanism + ≥N corroborating legs** (bundle-derived — the §12 signal layer) **+ a NAMED
predicate risk + no unrebutted mitigation** (human-gate inputs, NOT in a raw bundle). The harness scores the
**bundle-only signal structure** — `mechanism present AND ≥ the required legs`, computed from the fired
capabilities alone via `evidence_requirements.present_atoms` / `evaluate_sufficiency` with the human-gate
inputs **HELD OUT** (`named_predicate_risk=False`, no `gathered`/`read`, no mitigation). The human gate is
named as the boundary the harness does not cross; it is **never** derived from the oracle basis (that
detector↔basis correlation would re-introduce circularity).

**The firewall.** The oracle label never enters an engine input — `assert_no_oracle_leak` (a positive
allow-list: a renamed surrogate still raises) + the signature guard (`assert_engine_blind_to_oracle`). The
§12 discovery feed surfaces the oracle-vs-engine divergence to the analyst (presentation), but
`determine`/`evaluate_sufficiency` read none of it — the Phase-74 priors-are-provenance precedent.

## The population — a case = a customer (the per-customer merge)

The oracle covers the substrate **screening-slice** flagged customers (keyed `case_id = CASE-<customer>`,
fired caps C8/C14). A customer may also carry a **monitoring** bundle (C2/C3/C5/C15) under the same
`case_id`. The harness merges per-customer (screening ∪ monitoring fired capabilities) — the Phase-71 "a
case = a customer" frame the workbench engine actually decides over — so the engine sees its mechanism
(C2/C3/C5) + leg (C8/C15/...) capabilities. Scoring screening-only would make the ML side degenerate (no
mechanism cap in the screening slice) — an artifact, not a finding.

## The measure-first result (the T2 gate — PASSED, non-degenerate)

A 40000-client, seed-0 slice (substrate `9677a37`): **6935 cases, 121 file / 6814 clear.**

| | oracle = file | oracle = clear |
|---|---|---|
| **signal-file-ready** | 50 | **1320 (over-flag)** |
| **not file-ready** | **71 (missed)** | 5494 |

- **The ML signal layer discriminates** (non-degenerate): file-ready on **50 of 121** oracle-file ML cases
  vs **593 of 6087** oracle-clear ML cases — the file-ready cell is proportionally larger among oracle-file
  (the two classes separate; counts, not a rate). But it does NOT assemble to file-ready on **71 of 121**
  oracle-file cases — the §12 signal gap (the file bar needs the held-out human predicate + more signals than
  the slice assembles); each missed case names its absent mechanism/leg.
- **The KYC bar is a pure over-flag**: all **727** C14-pure kyc cases are oracle-clear, yet all **727** score
  "file-ready" (C14 mechanism alone, `additional_legs_required=0`). A source-of-funds *gap alone*
  pre-positions every one of them to file when none are laundering — a structural defensive-filing exposure.
- **Over-flag total 1320** (727 kyc + 593 ML); **missed total 71** (all ML).

These are illustrative on synthetic data — counts, never a rate.

## The §12 discovery feed (measure → control)

`serve_workbench` `GET /discovery` + the workbench panel surface the two disagreement cells as a live
analyst queue: **missed** (the §12 build queue — each row carries the engine's own `missing[]` gap to
build/gather) and **over-flag** (the defensive-filing exposure, incl. the KYC structural over-flag).
Read-only, persists nothing; the bounded sample discloses the full count (no silent cap).

## How to run

```
# the substrate emit (authoring-time only; pin 9677a37):
PYTHONPATH=<substrate>/src <substrate>/.venv/bin/python -m aml_substrate.cli \
  --clients 40000 --months 2 --seed 0 --emergence --monitor \
  --emit-evidence --emit-screening --emit-eval-oracles --out <out>

python3 scripts/determination_validation_harness.py --freeze --emit-dir <out>   # re-capture (writes capture.json + baseline.json)
python3 scripts/determination_validation_harness.py --check                      # replay, NO substrate (the regression gate)
python3 scripts/determination_validation_harness.py --selftest                   # dep-free (firewall + recompute)
```

`--check` is in the `uv run pytest` umbrella. The committed fixtures live under
`tests/fixtures/determination-validation/` (`capture.json` = the per-case caps + oracle; `baseline.json` =
the frozen confusion structure the served feed also reads).

## Deferred (named sibling handoffs)

- **merge real-66 scoring** — still circular (`true_entities` = `ENT-<entity_ref>` echo); needs `entity_ref
  ≠ cluster` (the open-data fork). `docs/substrate-open-reference-data-fork-PLAN-BRIEF.md`.
- **Lakeshore `cleared` co-sign** — needs casework C3 fan-in. `docs/casework-c3-fan-in-PLAN-BRIEF.md`.
