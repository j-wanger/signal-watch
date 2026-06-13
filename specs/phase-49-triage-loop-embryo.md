# Spec: Phase 49 — Triage-loop embryo made demo-able: §14's continuous adjudication loop as the 5th ship artifact (triage console)

> status: nana:approved (derived from the gate-approved decision article) · created: 2026-06-12
> Source of truth for rationale:
> `.dev-wiki/articles/decisions/phase-49-triage-loop-embryo.md` (D1–D8 + the gate record).
> Direction = blueprint §14's continuous adjudication loop made DEMO-ABLE — the offered
> recommendation taken as offered (first non-reframe in 3 gates), on the LFCM target path.

## Objective

Build blueprint §14's continuous adjudication loop as a demo-able FIFTH ship artifact,
`triage.html` → `dist/triage/index.html` (single self-contained offline file; the gate console
stays byte-frozen). Scenario source = a NEW committed SYNTHETIC dataset
`data/triage/scenarios.json`, deterministically curated by `scripts/curate_triage_scenarios.py`
from `data/probe-history` (rulebook + 44 alert stubs, read at AUTHORING time only — build.py
never reads probe-history; rule text EMBEDDED so the dataset is self-contained) +
US-federal-allowlist-only committed corpus indicators for the synthetic-novel stratum.
~16 scenarios across the 4 §14 strata (history-signal-fired / history-below-the-line /
synthetic-novel / random-population) + ~4 known-disposition controls; evidence panels
template-derived from rule logic + stub fields with a thin authored layer, ONE panel per fact
pattern shared BY REFERENCE across divergent-disposition pairs (the process-inconsistency beat
is STRUCTURAL, build-validated); fired-rule state universal; seeded LABELED second-rater
dispositions. Page arc: Queue (stream w/ stratum chips) → Evidence → Disposition (confirm-risk /
confirm-no-risk / both-defensible / escalate / need-more-info naming a C/D code via a taxonomy
picker + the policy-gap escape "no defensible option — flag for policy review"; rationale
REQUIRED) → Reveal (historical disposition, decisions-not-correctness; second-rater replay;
process-inconsistency surfacing) → Discovery ledger (signal gaps DERIVED from fired-rule state;
data gaps per D-code; process inconsistencies; policy gaps; agreement arithmetic computed at
render from committed data w/ visible measurement definitions; parameters labeled "chosen, not
measured"; JSON export; persists nothing). Badge always-on; keyboard nav; reduced-motion;
NO LLM/fetch.

## Scope

- `scripts/curate_triage_scenarios.py` (NEW) + `data/triage/scenarios.json` (NEW, committed,
  SYNTHETIC) (T1).
- `scripts/build.py`: `load_triage_scenarios` + `validate_triage_scenarios` + the `triage`
  target wired into `all`/`--check` (T2).
- `triage.html` (NEW) → `dist/triage/index.html` + `tests/triage-console.test.mjs` (NEW)
  (T3, T4).
- `CLAUDE.md` (replace-in-place: 5 ship artifacts; trim toward the ~200-line contract),
  `HANDOFF.md` §8, `tests/smoke-checklist.md` (T5).

## Non-goals

- NO edit to `docs/program-blueprint.md` (avoids the hand-synced blueprint-report drift) and
  NO edit to `docs/blueprint-report.html`.
- NO edit to `console.html`/`dist/console` — the gate console stays byte-frozen (D1); the
  triage console is a SIBLING artifact, not an extension.
- NO LLM call, no fetch, no live mode, no persistence — the ledger is session-only with JSON
  copy-out export.
- NO real customer/transaction/alert data anywhere — everything scenario-side is SYNTHETIC
  (probe-history is itself synthetic), flagged as such in the dataset meta.
- NO fake instrumentation (D8): no typed-in agreement/accuracy figure; any agreement-looking
  number is deterministic arithmetic computed at render from the committed dataset, each with
  a visible measurement definition; second-rater replay is seeded + LABELED, never
  simulated-live.
- NO non-US-federal indicator quotation in the synthetic-novel stratum (D6 — allowlist
  pre-committed in the curate script, the FIXTURE_META pattern).

## Constraints (safety rails)

- All 4 existing ship artifacts + dists BYTE-IDENTICAL through the phase (`--check` green on
  the 6 existing targets; drift → STOP and surface). Prevents: silently breaking a presented
  demo, especially the just-shipped console.
- `derive_signals.py` + the news pipeline + the derived data + the 3 overlays untouched.
- build.py NEVER reads `data/probe-history` (`! grep -q "probe-history" scripts/build.py`) —
  the curate script reads it at AUTHORING time only; the committed scenarios.json is
  self-contained (rule text embedded).
- Build-boundary validation fails loud on tamper (4 classes: broken stratum vocab / dangling
  panel ref / missing synthetic meta flag / C/D ref outside the taxonomy).
- Honesty: badge always-on; reveal framed decisions-not-correctness ("never ground truth"
  phrasing only in negation); parameters labeled "chosen, not measured"; no
  accuracy/precision/recall vocabulary in triage.html.
- The process-inconsistency beat is STRUCTURAL: divergent-disposition pairs share ONE evidence
  panel BY REFERENCE, validated at the build boundary — never an authored coincidence (D7).

## Assumptions (gate-closed 2026-06-12, all_accept: false; ledger block in assumption-ledger.md)

- A1 [HIGH]: the triage-loop embryo is DEMO-FIRST — an artifact to present (bank-audience
  class), not an internal instrument; the loop's defining beat (analyst judgment vs the
  institution's historical decision, decisions-not-correctness) needs replayed history, which
  only the synthetic probe data carries. ACCEPT (instrument-first noted as the natural
  follow-on — sequencing, not dismissal).
- A2 [HIGH — silent infrastructure class]: a NEW committed dataset data/triage/scenarios.json
  may be a build-read input for the NEW triage target — the console-cases layering: curate
  script reads probe-history at AUTHORING time only; build.py reads only the committed,
  build-boundary-validated scenarios.json; probe-history stays outside every build path;
  nothing enters __CORPUS__. DON'T-KNOW round 1 → defended (Phase-48 A4 verbatim +
  console-cases curation precedent + §14's own purpose) → ACCEPT round 2.
- A3 [HIGH — the T0 weakest assumption]: authored synthetic evidence panels can be made
  BELIEVABLE within the ~16-scenario + ~4-control ceiling (the 44 alert stubs carry no
  judgable fact pattern — panel authoring IS the bulk of the phase); mitigated structurally by
  D7. ACCEPT. Believability is adjudicated by the user at the delivery gate (the delivery
  report presents one full scenario verbatim).
- A4 [MED — either/or]: ship-class discipline is the right cost — a FIFTH ship artifact on the
  console precedent (an interactive artifact presented without a harness is the riskier
  alternative); the non-ship docs/ shape surfaced and declined. ACCEPT — 5th ship artifact.

## Checkpoints

- T1 REFACTOR valve: if panel authoring runs hot, the pre-drawn split = curate
  machinery+fixtures (stays T1) / authored-panel layer (new task) — surface, don't silently
  balloon.
- Post-T3 arc read: the full Queue → Evidence → Disposition → Reveal → Ledger arc against §14's
  text before harness completion — the disposition grammar (incl. need-more-info → C/D picker
  + the policy-gap escape) is the load-bearing beat.

## Exit criteria

1. `data/triage/scenarios.json` committed: ≤20 scenarios, all 4 strata populated, ≥3 controls,
   deterministic regen byte-identical, US-federal-only novel stratum, divergent pairs share
   panels by reference, fired-rule state universal, ≥4 labeled second-rater seeds, synthetic
   meta flag present.
2. build.py `triage` target wired into all/--check; boundary validation fails loud on tamper
   (4 classes); `! grep -q "probe-history" scripts/build.py`.
3. `triage.html` → `dist/triage/index.html` single-file offline with the full arc (Queue w/
   stratum chips → Evidence → Disposition [§14 grammar + policy-gap escape, rationale
   REQUIRED] → Reveal [decisions-not-correctness, second-rater replay, process-inconsistency
   surfacing] → Discovery ledger [render-computed agreement arithmetic w/ measurement
   definitions, JSON export, persists nothing]); badge always-on.
4. `tests/triage-console.test.mjs` fully green (~50+ assertions; gate-console precedent: load
   TEMPLATE + inject stub dataset; both motion modes, XSS, keyboard guards,
   reveal-locked-pre-disposition).
5. Claim-shaped honesty greps green + FULL REGATE: `--check all` zero drift (7 targets incl.
   triage), `git diff --quiet` on scripts/derive_signals.py AND docs/program-blueprint.md, all
   existing suites green.

## Verification

- T1: `curate_triage_scenarios.py --selftest` (seeded-broken fixtures each FAIL:
  shared-panel-ref integrity, stratum closed-vocab, US-federal allowlist, determinism,
  second-rater-seed presence) && regen-twice byte-identical && the python3 -c sanity gate
  (strata/controls/ceiling/panel-sharing/fired-rule/allowlist/seeds/meta-flag).
- T2: python3 -c unit checks — valid dataset passes; the 4 tamper fixtures each RAISE; the 6
  existing targets still `--check` green; no probe-history reference in build.py.
- T3: harness core set green (parse, arc reachability, disposition-gate rules: rationale
  required; need-more-info requires a C/D pick; reveal locked pre-disposition) && first
  passing `build.py triage` + `--check triage` && offline single-file grep on the dist.
- T4: harness fully green ~50+ (need-more-info → per-D-code data-gap ledger row; policy-gap
  escape requires rationale; second-rater replay LABELED; agreement arithmetic equals a
  hand-computed fixture AND renders its measurement-definition string; signal-gap derivation
  from fired-rule state; XSS; keyboard guards; both motion modes; badge; export JSON shape);
  T4 owns the FINAL dist freeze.
- T5: `--check all` zero drift && `git diff --quiet` derive_signals.py + program-blueprint.md
  && honesty greps (no accuracy/precision/recall; "ground truth" only negated; "chosen, not
  measured" + "decisions, not correctness" present) && all existing node suites +
  `derive_signals.py --selftest` + `news_quality_harness.py --check` green.

## Rollback / descope

- Panel-authoring valve: if believable panels can't be authored within the ceiling (3
  attempts), split per the T1 pre-drawn split and surface — never pad with thin panels to hit
  a count.
- Any existing-dist drift: STOP, surface, revert the offending change — never re-baseline.
- If a triage copy need collides with an honesty grep, the grep wins — re-word the copy, never
  weaken the honesty posture.
- If the dataset can't satisfy the structural panel-sharing validation, fix the DATA (curate
  script), never loosen the validator.
