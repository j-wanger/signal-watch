# Spec: Phase 48 — Brownfield history + LFCM: blueprint extension, triage-elicitation loop, synthetic-history probe

> status: nana:approved (derived from the gate-approved decision article) · created: 2026-06-12
> Source of truth for rationale:
> `.dev-wiki/articles/decisions/phase-48-history-lfcm-blueprint-extension.md` (D1–D5 + the A1
> condition). Direction = the user's OWN planning input: the Phase-47 blueprint reads GREENFIELD
> (TM alert / investigation / SAR-STR filing history unaddressed) + the LFCM idea + the
> mini-triage elicitation loop raised at the Step-9 questions.

## Objective

Extend `docs/program-blueprint.md` ADDITIVELY so it stops being greenfield and carries the LFCM
architecture honestly, and back the history-as-substrate claim with a measured synthetic probe.
Four deliverables: (1) a HISTORY-UTILIZATION section — history as THREE named roles each with
substrate + verifier (derivation substrate via the inverted extraction boundary / §6 probe
baseline — legacy TM as the A/B comparator / outcome-feedback embryo — filings as biased Class-M
material), the doctrine "history is evidence, never ground truth", §8 deferred rows
re-dispositioned (vision-lab-deferred vs adopter-available-with-caveats); (2) an LFCM section —
6th §3 workload row (entity/event risk decisioning), library-not-monolith (the signal library IS
the model inventory; LFCM = the program-level name), dossier-now/score-deferred-with-owner, 5
named failure modes (correlated double-counting, volume inversion → composition-before-escalation,
coverage illusion, monolith trap, drift at scale), §11 chain-1 re-point, editorial count fixes;
(3) a CONTINUOUS ADJUDICATION LOOP section (the user's mini-triage idea under the A1 condition);
(4) a fully SYNTHETIC advisory-shaped legacy rulebook derived through the EXISTING FROZEN gate +
a stdlib stats script whose every number carries its measurement definition; (5) an HTML
BLUEPRINT REPORT (user addition at plan close, 2026-06-12) — `docs/blueprint-report.html`, a
single self-contained offline NON-ship artifact (booth.html precedent) covering the extended
blueprint in its entirety, centerpiece inline-SVG SYSTEM-FLOW (six workloads + triage-loop
feedback) and GROUNDING-CHAIN (audit walk, verifier per hop) diagrams, labeled DESIGN.

## Scope

- `docs/program-blueprint.md`: the three new sections, the 6th §3 row, §3 "five workloads"→six,
  §12 "three ship artifacts"→four, §11 chain-1 re-point, probe-measurement citation (T1–T3, T6).
- `data/probe-history/**` (NEW): `legacy-rulebook.md` (SYNTHETIC, advisory-shaped, ~10–15 legacy
  TM rules under an existing rf_region anchor form), `alert-history.json` (synthetic, seeded
  disposition inconsistencies + re-review patterns), `derived/legacy-rulebook.json` (T4, T5).
- `scripts/probe_history_stats.py` (NEW, stdlib-only) + `docs/probe-history.md` (NEW) (T5a/T5b).
- `docs/blueprint-report.html` (NEW, single self-contained offline, NON-ship — no build.py
  target) (T6, the phase's single L; T5 split into T5a/T5b to hold the one-L budget).
- `CLAUDE.md`, `HANDOFF.md` (§8 one line), `.dev-wiki/*` (T7).

## Non-goals

- NO re-centered blueprint v2 and NO separate docs/lfcm.md (D1 rejected both — additive only).
- NO LFCM score build — dossier now; score DEFERRED with a named owner (D3); the loop section is
  DESIGN, not an artifact build (the gate console is the named embryo, not extended this phase).
- NO gate change of any kind: derive_signals.py byte-frozen; no rf_region anchor extension.
- NO probe data in any build.py-read path; NO real customer/transaction/alert data anywhere.
- NO new lift/precision/similarity number; no design parameter presented as measured.
- The HTML report is NOT a ship artifact: no build.py target, no dist, no validator — the
  booth.html precedent (promote via a future phase only if presented beyond design review); it
  renders the DESIGN and claims nothing beyond the blueprint's own text + the probe's defined
  numbers.

## Constraints (safety rails)

- All 4 ship artifacts + dists BYTE-IDENTICAL through the phase (`--check all` green; drift →
  STOP and surface). Prevents: silently breaking the presented demo or the new console.
- derive_signals.py FROZEN — the probe goes through the EXISTING gate with ZERO edits; the
  rulebook is AUTHORED advisory-shaped (synthetic — shape is free) so the gate never widens.
  Prevents: loosening the grounding core to pass a probe.
- Probe outputs OUTSIDE every build.py-read path (`data/probe-history/` is not a CORPUS_SOURCES
  dir; `! grep -q "probe-history" scripts/build.py`). Prevents: synthetic legacy rules bleeding
  into `__CORPUS__`/the demos.
- Every probe stat carries "definition:" (the measurement-defined-number rule); loop design
  parameters (e.g. ~30 min/day, strata, thresholds) labeled "chosen, not measured" with an
  adversarial grep (the §10 pattern). Prevents: the fabricated-figure class.
- The history doctrine is grep-pinned: "history is evidence, never ground truth"; the writeup
  states the SHAPE CAVEAT (the probe demonstrates "history CAN be a derivation surface", not
  "any real rulebook parses unchanged" — real rulebooks may need the regression-gated
  anchor-extension path). Prevents: over-claiming the probe result.

## Assumptions (gate-closed 2026-06-12, all_accept: false; ledger block in assumption-ledger.md)

- A1 [HIGH — the T0 weakest assumption]: the triage-elicitation loop's value does NOT depend on
  analyst-judgment convergence — gap discovery (need-more-info wired to the C/D coverage model)
  is the value floor, calibration stats the upside, agreement itself a first-class measured
  dimension (divergence routes to adjudication — the console pattern). ACCEPT WITH CONDITION:
  scenarios are SOURCED FROM REAL INSTITUTIONAL HISTORY (alerts/cases/filings replayed as
  mini-triage scenarios) — historical decisioning is ground truth about DECISIONS, never about
  correctness; and the loop's discovery outputs explicitly include PROCESS INCONSISTENCIES and
  POLICY GAPS alongside signal/data gaps.
- A2 [HIGH]: LFCM's regulatorily survivable architecture = a grounded signal LIBRARY + a small
  composition layer — the library IS the model inventory (per-signal lifecycle, tiered
  validation); "LFCM" stays the program-level name, never a single Tier-1 mega-model as the
  validation unit.
- A3 [MED]: history enters as THREE distinct roles (derivation substrate / §6 probe baseline /
  outcome-feedback embryo) under "history is evidence, never ground truth"; §8's deferred rows
  RE-DISPOSITIONED in place, not duplicated.
- A4 [MED]: the probe executes as a fully SYNTHETIC advisory-shaped legacy rulebook through the
  EXISTING FROZEN gate (zero gate changes; honest shape caveat) + a stdlib stats script over
  synthetic alert/disposition history; outputs committed OUTSIDE every build.py-read path; all 4
  dists byte-frozen; the two stale blueprint counts fixed in scope.

## Checkpoints

- Post-T3 coherence read: the three new sections against §2/§3/§4-J/§5/§8/§11 before probe work
  begins — the blueprint is the load-bearing deliverable.
- T5 gate-frozen valve: if the synthetic rulebook fails `check_record` under the existing
  anchors, re-author the rulebook SHAPE — never touch the gate; after 3 shape attempts, surface.

## Exit criteria

1. Blueprint extended + internally coherent: history-utilization + LFCM + continuous-adjudication-
   loop sections present; 6th §3 workload row; §3/§12 count fixes; §11 chain-1 re-pointed.
2. Probe gate-green through the UNCHANGED gate (git diff --quiet scripts/derive_signals.py) +
   measurement-defined stats (≥4 "definition:" lines) + the shape-caveat writeup
   docs/probe-history.md.
3. Honesty greps green: the doctrine line; "chosen, not measured"; no unmeasured number; the
   adversarial score-claim grep clean.
4. Full regate green; all 4 ship dists byte-identical.
5. `docs/blueprint-report.html` present: single self-contained offline (no external src/href
   asset, renders from file://), DESIGN-labeled, full-blueprint coverage, system-flow +
   grounding-chain inline-SVG centerpieces, never referenced by scripts/build.py.

## Verification

- T1: doctrine + adopter greps; the history-as-ground-truth count equals the "never ground truth"
  count (every mention is a negation).
- T2: state-flag awk pins the §3 table at 6 data rows; "five workloads"/"three ship artifacts"
  absent; adversarial "score is built/live/deployed/measured" grep clean.
- T3: "process inconsisten" + "policy gap" + "chosen, not measured" present; any "30 min" line
  carries "chosen".
- T4: rulebook exists + SYNTHETIC label; alert-history.json parses; build.py never references
  probe-history; `derive_signals.py --selftest` green (gate untouched).
- T5a: `git diff --quiet scripts/derive_signals.py` && derived record exists + gate-green via the
  existing check machinery; T5b: stats script runs with ≥4 "definition:" lines &&
  "advisory-shaped" in docs/probe-history.md.
- T6: report exists && "grounding chain" + "DESIGN" present && no external `(src|href)=http`
  asset && build.py never references blueprint-report.
- T7: full regate — `--check all`, the 3 node suites (corpus-explorer, news-stream, gate-console),
  `derive_signals.py --selftest`, `news_quality_harness.py --check`, no build.py probe reference.

## Rollback / descope

- Probe descope valve: if the rulebook cannot be authored gate-green in shape (3 attempts), the
  blueprint sections ship alone and the probe is surfaced as a recorded descope — never a
  silently widened gate.
- Any existing-dist drift: STOP, surface, revert the offending change — never re-baseline.
- If a blueprint edit collides with a frozen Phase-47 claim (e.g. §10's ratio refusal), the
  refusal wins — re-word the new section, never weaken the honesty posture.
