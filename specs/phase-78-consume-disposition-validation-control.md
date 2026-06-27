---
phase: 78
slug: phase-78-consume-disposition-validation-control
title: "Consume the disposition oracle — the determination-validation harness (the circularity exit) + the §12 discovery-feed control"
ceremony: standard
status: active
created: 2026-06-26
grounded_against:
  signal-watch: HEAD (Phase 77 committed, 5afdb96)
  aml-substrate: 9677a37 (Phase 31 — emit-cli-wiring; close)
  aml-casework: b3546d4 (unchanged; not touched this phase)
---

# Phase 78 — Consume the disposition oracle

## 1. Objective

Consume aml-substrate's now-CLI-reachable **exogenous disposition oracle**
(`eval/intended_disposition.json`, wired by substrate Phase 31 `--emit-eval-oracles`) to build the
**determination-validation harness** — the "circularity exit" the Phase-77 ledger (A2) deferred for
lack of a tool-use-boundary path. Then pivot the measurement into a **control**: surface the
engine-vs-oracle disagreement cases as a **§12 discovery feed** in the investigator workbench (the
[[measuring-to-controlling-pivot]]).

This is the FIRST validation of signal-watch's determination engine against an oracle it did not
author — substrate's `intended_disposition` (`file`|`clear`) is written BLIND to
`evaluate_sufficiency`. That blindness is what makes it a genuine measurement, unlike the Phase-77
merge-66 oracle (a content-addressed relabel of the spine's own decision key — circular, correctly
left deferred and confirmed circular by substrate Phase 31's own commit).

## 2. The verified gap is now closed

- Substrate advanced **f2da3e4 → 9677a37** (Phase 31, committed 2026-06-26). `--emit-eval-oracles`
  now writes `eval/intended_disposition.json` + `identity/true_entities.json` across the CLI
  boundary. **Verified live this session** (5k-client emit): the disposition oracle emits, keyed
  `CASE-<customer>`, two-sided (`file`|`clear`) with a closed `intended_basis` vocab.
- Distribution probe (5k clients, seed 0): **11 `file` / 807 `clear`** (basis: explained_source_of_funds
  533, coincidental_collision 49, structuring 7, layering 4, null 225). Two-sided but heavily
  clear-skewed → the measurement is a **per-class confusion structure**, NOT an accuracy (a trivial
  always-clear engine would "pass" on the overwhelming clear majority — meaningless).
- The other two Track-C′ consumes stay blocked and are NOT in scope: merge real-66 (oracle still
  circular — substrate Phase 31's commit confirms the slice is all-singleton, `ENT-<entity_ref>`
  echo, stays CONSENSUS until the open-data fork); Lakeshore `cleared` (needs casework C3 fan-in).

## 3. Scope (in)

- `scripts/determination_validation_harness.py` — NEW companion harness (`--freeze` / `--check` /
  `--selftest`), the `gather_quality_harness.py` / `resolution_scorer.py` pattern.
- `tests/fixtures/determination-validation/{capture.json,baseline.json}` — the distilled boundary
  capture + the committed confusion-structure baseline.
- `scripts/serve_workbench.py` + `workbench.html` — the §12 discovery-feed control (a read-only
  `/discovery` route + panel; companion-only, persists nothing).
- `docs/determination-validation.md` — the doc; CLAUDE.md + `docs/cross-pillar-build-order.md` true-up.

## 4. Scope (out / DEFERRED, named)

- Merge real-66 scoring (circular; open-data fork). Lakeshore `cleared` co-sign (casework C3 fan-in).
- ANY change to `evidence_requirements.evaluate_sufficiency` / the determination bar (the A1 guard).
- ANY ship dist change — all 9 dists stay BYTE-FROZEN; build.py imports nothing new.
- A "full gated verdict" frame (rejected at the direction gate as re-introducing circularity via the
  detector↔basis correlation). The harness scores the **bundle-only** structure.

## 5. The honesty frame — bundle-only, non-circular (LOAD-BEARING)

The `file` bar = mechanism + ≥2 corroborating legs + a NAMED predicate risk + no unrebutted
mitigation. Of these, **mechanism + leg count are bundle-derived** (the §12 signal layer);
**named_predicate_risk + mitigation are HUMAN-gate inputs** not present in a raw bundle.

- The harness scores the **bundle-only signal structure** (mechanism present? ≥2 legs?) against the
  oracle — measuring whether the deterministic signal-assembly *pre-positions* the file decision.
- The human-gate inputs are **HELD OUT and named as the boundary the harness does not cross** — they
  are NEVER derived from the oracle basis (that would be the circularity the Phase-77 abort rule
  killed the merge-66 consume for).
- **The firewall (the resolver-input-firewall translated):** the oracle label never enters any
  engine input. `assert_no_oracle_leak` guards it (mirrors `resolution_scorer.assert_no_cluster_leak`).
- The control's discovery feed surfaces oracle-vs-engine divergence to the **analyst** (presentation),
  but `determine`/`evaluate_sufficiency` still read none of it — the Phase-74 **priors-are-provenance-only**
  precedent.

## 6. Exit criteria

1. `scripts/determination_validation_harness.py --check` replays the committed capture with NO
   substrate run and produces the confusion structure vs a committed baseline (the
   news/gather-harness regression pattern). `--freeze` re-captures from substrate @9677a37.
2. The confusion structure is the per-class deliverable (signal-file-ready × oracle file/clear), each
   cell defined at render: *missed* (oracle-file, signals not file-ready = §12 gap), *over-flag*
   (oracle-clear, signals file-ready = defensive exposure), plus the correct cells. Synthetic-only
   qualified; NO catch-rate / precision / lift / recall wording.
3. The §12 discovery feed renders the two disagreement cells in `serve_workbench`, each annotated by
   the engine's own `missing[]` gap-naming; the oracle is presentation-only (absent from the
   determine path).
4. `evidence_requirements.py` BYTE-UNCHANGED (A1 guard, `git diff --quiet`). build.py imports no
   harness / serve_workbench / substrate (grep-clean). `--check all` 9/9 byte-frozen. `uv run pytest`
   green (harness added to the umbrella).

## 7. The measure-first gate (the falsifiable assumption)

**Weakest assumption (T0):** that the bundle-only structure (mechanism + ≥2 legs) discriminates
oracle-`file` from oracle-`clear` at all. The oracle side is verified two-sided; the engine-side
discrimination is UNKNOWN until measured. **T2 is the gate:** compute the matrix; if degenerate
(signal-file-ready ≈ 0, or non-discriminating across the oracle classes), **STOP + REPORT** and
down-scope T3 to an honest-degeneracy report rather than manufacturing a discovery feed over a
non-result. A weak-but-real discrimination is a legitimate, honest outcome (it names the §12 signal
gap) — the phase reports what it measures, whatever that is.

## 8. Abort rules

STOP-and-surface on any of: a ship dist drifts · build.py imports the harness/serve_workbench/substrate ·
`evidence_requirements.py` changes · the oracle label reaches an engine input (the firewall leaks) ·
a confusion number is presented as a catch-rate/precision/lift · the harness requires a live substrate
read from any dist. If the matrix is degenerate → down-scope T3 (§7), don't fabricate a feed.

## 9. Assumptions ledger

See `.dev-wiki/assumption-ledger.md` Phase 78. Direction gate closed 2026-06-26 (both decisions
positioned: bundle-only frame; measure→control deliverable).
