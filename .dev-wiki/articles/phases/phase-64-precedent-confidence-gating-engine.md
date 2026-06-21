---
title: "Phase 64: Precedent-confidence gating engine + the elicitation loop (live)"
aliases: [gating engine, precedent-confidence gating, elicitation loop, LFCM elicitation-loop]
category: phases
tags: [m9, lfcm, gating, elicitation-loop, control, workbench, live, measuring-to-controlling]
parents: []
created: 2026-06-21
updated: 2026-06-21
source: plan
status: active
scope:
  - "workbench.html"
  - "scripts/serve_workbench.py"
  - "scripts/curate_workbench_cases.py"
  - "tests/workbench.test.mjs"
  - "tests/test_selftests.py"
  - "docs/case-workbench.md"
  - "tests/smoke-checklist.md"
  - "scripts/build.py (NO substrate/casework import — companion-only, no build target)"
entry_criteria: "Phase 63 delivered + accepted (committed a3fde1e); the workbench (workbench.html + serve_workbench.py, companion-only, NOT a build target) serves the 200-case slice + the live finale; curate_workbench_cases.py's `_confidence(combo, n_precedent)` is a STATIC bucketer (thresholds 500/50 + cleared-% 88/62/28 hardcoded; the 129/52/19 funnel a static count baked into data/workbench/cases.json); serve_workbench does NO live routing. The confidence model is purely sample-size (verified firsthand this session) → the §12-routing / §14-illustrative-disposition separation is clean."
exit_criteria: "The static bucketer becomes a LIVE, parameterized gating CONTROL with a feedback loop: an explicit `gating_policy` object + a pure `route(confidence, sample_size, policy) → {auto-decide|review|human-gate}` (reproducing the committed 129/52/19 funnel from policy defaults + a monotonicity invariant); the decision APPLIED (auto-clear → illustrative disposition applied; human-gate → escalate); the session-only ELICITATION LOOP (/adjudicate → grow the combo's session precedent → recompute confidence → re-route; persists nothing); the gating panel UI (visible knobs, per-case live routing, the adjudication action + the loop visualization, the funnel re-derived live, always-on badge); the engine EXECUTED ONCE live over the 200-case slice (the funnel re-derived + the loop shifting one decision). The §12-routing / §14-illustrative-disposition seam holds (route on real firing frequency; dispositions illustrative; NO §14 re-grounding from probe-history). `serve_workbench.py --selftest` + `node tests/workbench.test.mjs` + `uv run pytest` green; `build.py --check all` 8/8 ZERO dist drift; no substrate/casework import; companion-only (NOT a 9th build target)."
---

# Phase 64: Precedent-confidence gating engine + the elicitation loop (live)

## Objective

Turn the Phase-63 workbench's STATIC precedent-confidence bucketer into a LIVE, parameterized gating
CONTROL with a feedback loop — the Phase-63 follow-on #3, "the LFCM elicitation-loop path", and the
measuring→controlling pivot (Phase 63 DISPLAYED the confidence + the 129/52/19 funnel; Phase 64 makes
the routing a LIVE control). Companion-only (a `serve_workbench.py` extension, NOT a 9th ship target);
the loop is session-only and persists nothing; `--check all` stays 8/8 with ZERO dist drift.

**The starting point (verified firsthand this session):** `_confidence(combo, n_precedent)` in
`scripts/curate_workbench_cases.py` is a static bucketer baked at curate time — `n_precedent >= 500`
→ high/auto-clear/88, `>= 50` → medium/review/62, else low/human-gate/28; the gate vocab
`{auto-clear, review, human-gate}` is frozen into `data/workbench/cases.json`; the 129/52/19 funnel is
a static count. `serve_workbench.py` serves cases + the live finale but does NO live routing. The
confidence model is PURELY sample-size → the §12-routing / §14-disposition separation is clean.

## The delta (four moves)

1. **EXPLICIT routing policy.** Lift the hardcoded 500/50 + cleared-% into a visible `gating_policy`
   object ("chosen, not measured" knobs) + a pure `route(confidence, sample_size, policy) →
   {auto-decide|review|human-gate}`.
2. **The decision APPLIED, not displayed.** Auto-clear cases get an illustrative disposition applied
   automatically; human-gate cases escalate (the control EXECUTES — the measuring→controlling pivot).
3. **The ELICITATION LOOP (the LFCM core).** A human adjudicates a gated case → that disposition
   becomes session precedent → the combo's sample grows → confidence recomputes → the next similar
   case may re-route toward auto. Session-only, persists nothing. Blueprint §14's continuous
   adjudication loop made live.
4. **EXECUTE ONCE.** Run the engine live over the real 200-case slice: re-derive the funnel + demonstrate
   the loop shifting one routing decision.

## The honesty seam (LOAD-BEARING)

The loop shifts ROUTING via REAL sample-growth (the §12-grounded firing frequency — genuine); the
recorded/auto-applied DISPOSITION stays labeled illustrative. It demonstrates WHERE human judgment gets
spent and how precedent concentrates it — NEVER that the auto-dispositions are correct. This holds the
Phase-62 §12/§14 boundary: route on §12 measurement, do NOT re-ground §14 from probe-history (the
Phase-62 stand-down holds — see [[substrate-probe-history-12-not-14]]).

**Decisions (direction gate 2026-06-21, all_accept:true — lite skips decision articles):**
1. **Phase 64 direction = the precedent-confidence gating engine** — chosen at the Step-9 gate over
   agentic tool-calling (local) and the sibling-rooted C3/C15 alignment; the LFCM elicitation-loop path
   + the measuring→controlling pivot.
2. **The §12-routing / §14-illustrative-disposition honesty seam is the load-bearing design invariant** —
   routing keys on real firing frequency; dispositions stay illustrative; no §14 re-grounding from
   probe-history (the Phase-62 stand-down holds).
3. **Companion-only / LITE holds** — a `serve_workbench` extension, NOT a 9th ship target; the loop is
   session-only / persists-nothing.

## Scope

Files and modules affected (companion-only — NOT a build target):
- `scripts/serve_workbench.py` — the `gating_policy` object + the pure `route()`; the live per-case
  routing decision served; the session-only `/adjudicate` loop path (grow precedent → recompute →
  re-route; in-memory only).
- `scripts/curate_workbench_cases.py` — `_confidence`'s hardcoded knobs lifted into `gating_policy`
  (the static bucketer's logic preserved; the committed funnel reproduced from policy defaults).
- `workbench.html` — the gating panel (visible knobs, per-case live routing, the human-gate
  adjudication action + the loop visualization, the funnel re-derived live, always-on badge).
- `tests/workbench.test.mjs` — the gating arc (routing render + adjudication loop + the live funnel +
  badge + both motion modes + XSS-escape).
- `tests/test_selftests.py` — the gating selftests added to the pytest wrapper.
- `docs/case-workbench.md` — the gating-engine section + the §12/§14 boundary statement.
- `tests/smoke-checklist.md` — a gating presenter entry.
- `scripts/build.py` — NEVER imports aml_substrate / aml_casework; companion-only, no build target.

## Exit Criteria

- [ ] T1: an explicit `gating_policy` + a pure `route(confidence, sample_size, policy)`;
      `serve_workbench.py --selftest` reproduces the committed 129/52/19 funnel from policy defaults +
      the monotonicity invariant (a larger sample never yields a STRICTER gate); no sibling import.
- [ ] T2: the session-only `/adjudicate` loop — a human-gate case re-routes toward auto after
      adjudications of its combo; a persists-nothing assertion (no disk write across an /adjudicate cycle).
- [ ] T3: the gating panel UI renders (visible knobs, per-case live routing, the adjudication action +
      the loop visualization, the funnel re-derived live, always-on badge); `node tests/workbench.test.mjs`
      gating arc green (both motion modes, XSS-escape).
- [ ] T4: the engine EXECUTED ONCE live over the 200-case slice (the funnel re-derived + the loop
      shifting one decision, captured as evidence); `uv run pytest` + `node tests/workbench.test.mjs`
      green; `build.py --check all` 8/8 ZERO dist drift; no substrate/casework import in build.py.
- [ ] T5: `docs/case-workbench.md` has the gating section + the §12/§14 boundary statement;
      `tests/smoke-checklist.md` has the gating entry.

## Constraints

- Companion-only — a `serve_workbench` extension, NOT a 9th build/dist target — prevents the Phase-49
  new-ship→standard ceremony escalation + the launcher cascade.
- The loop is session-only and persists NOTHING (in-memory) — prevents a stateful artifact masquerading
  as a learned model + keeps "committing is a human-reviewed act".
- Recompute from data already in `cases.json` (n_precedent stored) — records BYTE-FROZEN; no substrate
  re-emit, no sibling import — prevents a substrate dependency creeping into a routing phase.
- Route on §12 firing frequency; dispositions stay §14 illustrative; NO §14 re-grounding from
  probe-history — prevents the loop reading as "learns the correct answers" (the Phase-62 stand-down).
- ZERO catch-rate / detection-lift / precision number; the always-on "Illustrative data & outputs"
  badge stays — prevents resurrecting the retired triple-null claim.
- build.py NEVER imports aml_substrate / aml_casework — file-contract / vendored-pin only.

## Checkpoints

- **Build-time honesty checkpoint (A0, T0 weakest):** if the live loop can't be kept honest over
  illustrative dispositions (it reads as "the engine learns the correct answers") → scope to
  display-only batch routing, report don't force (the named fallback). The routing re-derivation via
  real sample-growth is genuine; the disposition stays labeled illustrative + no learns-correct claim.
- If `route()` does NOT reproduce the committed 129/52/19 funnel from the policy defaults → the lift
  changed behavior; STOP and reconcile (the bucketer's logic must be preserved exactly).

## Assumptions (gate-resolved — the live loop carries the weakest, T0)

- **A0 [T0 weakest] the live elicitation loop is the TARGET, with a BUILD-TIME honesty checkpoint.**
  The loop shifts ROUTING via real sample-growth (§12-grounded firing frequency) while the
  recorded/auto-applied DISPOSITION stays labeled illustrative + no learns-correct claim. If it can't
  be kept honest at build → scope to display-only batch routing, report don't force.
- **A1 companion-only.** The loop is inherently live-stateful → a serve_workbench extension, NOT a 9th
  ship target (Phase-49 new-ship→standard does NOT fire); `--check all` stays 8/8.
- **A2 recompute from cases.json.** n_precedent is already stored → records byte-frozen, no substrate
  re-emit, no sibling import.
- **A3 the Phase-62 §12/§14 boundary.** Route on §12 confidence; dispositions §14 illustrative; NO §14
  re-grounding from probe-history.
- **A4 EXECUTE ONCE.** The key activity is EXECUTED live over the 200-case slice (the funnel re-derived
  + the loop shifting one decision), not just designed (the measuring→controlling pivot).

## Notes

- **The measuring→controlling pivot.** Phase 63 measured + DISPLAYED the precedent-confidence and the
  129/52/19 gate funnel; Phase 64 builds the CONTROL the measurement was for (route + apply + the
  elicitation loop) and EXECUTES it once — the pattern in [[measuring-to-controlling-pivot]].
- **Blueprint §14 + §13 LFCM.** This is §14's continuous adjudication loop made live (adjudication →
  precedent → confidence → re-route) and the §13 LFCM elicitation-loop path (library-not-monolith,
  dossier-now/score-deferred, the history-sourced mini-triage elicitation loop) — see
  [[lfcm-is-jakes-target-vision]].
- **The Phase-62 source boundary holds.** The substrate's label-blind probe-history is the right source
  for §12 measurement (firing frequency) but the wrong source for §14 adjudicable fact patterns — so
  routing keys on §12, dispositions stay §14 illustrative, and the loop does NOT re-ground §14 from
  probe-history. See [[substrate-probe-history-12-not-14]] + the Phase-63 grounded-detection /
  illustrative-disposition split ([[workbench-fail-closed-cross-pillar]]).
- **Knowledge gaps:** none unfilled — the existing curate/serve/html code was read firsthand this
  session; the confidence model is purely sample-size (verified) so the §12-routing/§14-disposition
  separation is clean.
- **Follow-on (still sequenced OUT):** agentic tool-calling (OSINT / counterparty / network-ER); the
  C3/C15 cross-pillar contract alignment (a sibling-repo phase); the substrate ownership/beneficial-owner
  graph emission.
