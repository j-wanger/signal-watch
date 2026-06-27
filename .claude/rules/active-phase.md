# Active Phase Context

**Phase 78 — *Consume the disposition oracle*: the determination-validation harness (the circularity exit) + the §12 discovery-feed control** (signal-watch-local, STANDARD) — DELIVERED + accepted 2026-06-26. Net: harness + §12 feed landed; the exogenous oracle revealed ML-discriminates-but-misses (§12 gap) + the KYC structural over-flag; companion-only, 9 dists byte-frozen, A1 held. Adversarial review 0 must-fix / 3 fixed / 3 refuted / 10 praise.

## Objective
Consume substrate Phase 31's now-CLI-reachable `eval/intended_disposition.json` (`--emit-eval-oracles`)
to build the determination-validation harness Phase-77 A2 deferred — the FIRST validation of
`evaluate_sufficiency` against an oracle it did not author — then pivot it into a control: a §12
discovery feed over the engine-vs-oracle disagreement cases in the investigator workbench.
Companion-only; the engine + all 9 dists stay byte-frozen.

## Scope
- `scripts/determination_validation_harness.py` (NEW; `--freeze`/`--check`/`--selftest`)
- `tests/fixtures/determination-validation/{capture,baseline}.json`
- `scripts/serve_workbench.py`, `workbench.html` (the §12 discovery feed)
- `docs/determination-validation.md`, CLAUDE.md, `docs/cross-pillar-build-order.md`

## Key constraints (LOAD-BEARING)
- **Bundle-only, non-circular frame:** score the bundle-derived structure (mechanism + ≥2 legs); HOLD
  OUT the human-gate inputs (named_predicate_risk, mitigation) and NAME them as the boundary — NEVER
  derive them from the oracle basis. The oracle is authored blind to the sufficiency rule.
- **The firewall:** the oracle label never enters an engine input (`assert_no_oracle_leak`). The
  discovery feed is presentation-only (the Phase-74 priors-are-provenance precedent).
- **A1 guard:** `evidence_requirements.py` BYTE-UNCHANGED (`git diff --quiet`).
- **Boundary:** build.py imports no harness/serve_workbench/substrate; all 9 dists byte-frozen.
- **Honesty governor:** no catch-rate/precision/lift/recall; synthetic-only qualified; badge always-on.
- Substrate pin **9677a37** (Phase 31); `--check` replays the committed capture with NO substrate run.

## Exit criteria
`--check` → the per-class confusion structure vs a committed baseline (no substrate run); the §12
discovery feed renders the *missed* / *over-flag* cells annotated by the engine's `missing[]`;
`--check all` 9/9 byte-frozen; `uv run pytest` green; `evidence_requirements.py` byte-unchanged.

## Abort rule
Any dist drift / a build.py companion-or-substrate import / an engine change / an oracle-label leak
into the engine / a confusion number presented as a catch-rate / a dist requiring a live substrate
read → STOP-and-surface. **Measure-first (T2):** if the matrix is degenerate (signal-file-ready ≈ 0
or non-discriminating across oracle classes) → STOP+REPORT, down-scope T3 to an honest-degeneracy
report; never fabricate a discovery feed over a non-result.

## Gates
- [x] spec (`specs/phase-78-consume-disposition-validation-control.md`)
- [x] Direction confirmed by user (assumption positions taken 2026-06-26; bundle-only frame +
      measure→control deliverable; no unresolved reject/don't-know)
- [x] Delivery accepted (post-implementation report 2026-06-26)

Spec `specs/phase-78-consume-disposition-validation-control.md`; plan
[[phases/phase-78-consume-disposition-validation-control]]; ledger Phase-78.
**Next after delivery:** the open-data fork (substrate) unblocks the two-sided real merge oracle;
casework C3 fan-in unblocks the Lakeshore co-sign — both sibling-rooted (see
`docs/cross-pillar-build-order.md`).
