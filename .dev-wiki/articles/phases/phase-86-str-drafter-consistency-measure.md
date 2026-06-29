---
title: "Phase 86: STR drafter behind the verifiers — the consistency-measured drafting agent (Agentification Stage 3)"
aliases: [phase-86, str-drafter, agentification-stage-3, drafter-consistency-measure, sixth-live-loop-measured, drafter-quality-harness]
category: phases
tags: [agentification, stage-3, str-drafter, drafter-protocol, narrative, consistency-not-correctness, no-oracle, companion, measurement, byte-frozen]
parents: [phase-85-determination-pre-proposer, phase-83-merge-adjudicator-oracle-scored]
created: 2026-06-29
updated: 2026-06-29
source: plan
status: active
ceremony: standard
scope: ["tests/drafter_quality_harness.py", "tests/fixtures/drafter-quality/**", "tests/test_selftests.py", "tests/workbench.test.mjs", "tests/chain.test.mjs", "workbench.html", "chain.html", "docs/drafter-live.md", "docs/agentification-roadmap.md", "CLAUDE.md", "HANDOFF.md"]
entry_criteria: "Phase 85 DELIVERED + accepted 2026-06-29 (impl 2008692; all 6 tasks [x]; all 9 dists byte-frozen, evidence_requirements.py untouched). The agentification roadmap names Stage 3 (the STR drafter) as the next leg. STATE-LOADER FINDING (code-verified, surfaced pre-gate): the STR drafter + its verifier gate ALREADY SHIPPED in Phase 57 — the Drafter Protocol, the --drafter {stub,claude,openai,opencode} switch, the backend mapping serve_chain.py:188, the live-draft staged reveal. A live model is up on 127.0.0.1:8080. serve_chain.casework_consume returns {signed, blocking_violations, narrative_present, completeness, drafter_effective} (serve_chain.py:262-308). The drafter has NO correctness oracle (free-text drafting)."
exit_criteria: "All 5 tasks [x]. python3 tests/drafter_quality_harness.py --check PASS + in the uv-run-pytest umbrella; the live (or stub-only, honestly) counts-only headline recorded; node tests/workbench.test.mjs green (count grows); python3 scripts/build.py --check all 9/9 byte-frozen; git diff --quiet vendor/aml-casework + git diff --quiet scripts/evidence_requirements.py both empty; build.py companion-import grep clean (no drafter_quality_harness); the 256/376 §12 funnel unchanged; docs/agentification-roadmap.md Stage 3 marked BUILT + docs/drafter-live.md written; CLAUDE.md + HANDOFF trued IN PLACE; honesty swept (no catch-rate/lift/precision/recall)."
---

# Phase 86: STR drafter behind the verifiers — the consistency-measured drafting agent (Agentification Stage 3)

## Objective

Turn the already-built deterministic stub STR drafter into a CONSISTENCY-MEASURED drafting agent —
a drafter quality harness (`tests/drafter_quality_harness.py`, the `gather_quality_harness.py`
pattern) that measures the live (local) drafter vs the deterministic stub over the committed casefile
bundles, counts-only (stub-vs-live SIGN/REFUSE + fabrication-guard CATCH + grounding CONSISTENCY),
pinned as a `--check`/`--freeze` regression gate, with an honest counts-only headline. The deliverable
is the MEASUREMENT FRAME + marking roadmap Stage 3 BUILT. Companion-only — all 9 ship dists
byte-frozen; the vendored casework Drafter Protocol + the six grounding verifiers UNCHANGED (measure,
don't modify); `evidence_requirements.py` + the 256/376 §12 funnel UNTOUCHED.

## Why now / the state-loader finding that reshaped the frame

The agentification roadmap names Stage 3 (the STR drafter) after Stage 2 (Phase 85, the §12
determination pre-proposer). The state-loader surfaced — BEFORE the gate — that Stage 3 is NOT new
infrastructure: the STR drafter + its verifier gate ALREADY SHIPPED in Phase 57.

- The Drafter Protocol = casework's pluggable `Drafter` boundary
  (`vendor/aml-casework/src/aml_casework/narrative_generator.py`).
- The `--drafter {stub,claude,openai,opencode}` switch + all four backend adapters were BUILT Phase 57,
  wired through `serve_chain.py:188` + `serve_workbench.py` via a server-side-env name pass-through.
- The live-draft staged reveal already exists in chain.html/workbench.html.
- A live model is up on `127.0.0.1:8080`; the openai drafter defaults to it
  (`serve_chain.DEFAULT_OPENAI_BASE`, no env).

So the roadmap's "near-zero new code" is literally true. The genuine deliverable is therefore the
MEASUREMENT FRAME, not infra. See [[phase-86-direction-str-drafter-measurement]].

## The decisive difference from Stages 1 & 2 (the no-oracle break)

Stages 1 (merge adjudicator) and 2 (§12 pre-proposer) were each oracle-scored — a measurable
correctness ground truth (the merge `GT-<hash>` cluster oracle; the §12 exogenous
`intended_disposition` oracle). **The STR drafter has NO correctness oracle** — it produces free-text
prose, and there is NO committed narrative reference to score it against. Its "gate" is the six
deterministic Class-G verifiers → a BINARY signed/refused + `blocking_violations` (citation grounding,
corpus grounding, the fabrication guard; faithfulness, NOT narrative quality). This puts Stage 3 in
the roadmap's **consistency-not-correctness** class (the GATHER `tests/gather_quality_harness.py` is
the model), NOT the oracle-scored class. The measure is counts-only stub-vs-live SIGN/REFUSE +
fabrication-guard CATCH count + grounding CONSISTENCY — NEVER an accuracy/catch-rate/precision/recall;
a hand-authored "gold narrative" oracle is REJECTED (synthetic gold is judgment, not truth). See
[[phase-86-no-oracle-consistency-measure]]. A consequence: NO oracle firewall is needed (no truth to
hide — the drafter sees the bundle evidence by design), so the harness is SIMPLER than the Stage-1/2
harnesses. See [[phase-86-companion-only-casework-unchanged]].

## Non-degeneracy (the two-sided contrast)

A stub-vs-live consistency measure is only meaningful if the population spans both gate outcomes. It
does: the deterministic STUB drafter fail-closes on the narrative-seam case (Phase-82's
`CASE-P-0025128`, a txn-bearing C14 where casework's stub drafter fails narrative verification — "seam
left open"). So the committed casefile bundles (`data/casefile/*.bundle.json`) span SIGN and REFUSE,
and that case is the two-sided contrast: does the live agent sign where the stub couldn't, or does the
fabrication guard catch it? T1 measure-first CLASSIFIES the population first; an honest NULL is
surfaced if it proves degenerate (a deliberately-ungrounded case is the named fallback). See
[[phase-86-stub-vs-live-narrative-seam-contrast]].

## Formal Spec

> Standard-ceremony spec captured in-article (no separate `/spec` round; the contract is fully
> determined — the drafter + gate are built, the measurement frame is fixed by the GATHER pattern).

**Objective.** Build the drafter quality harness (`tests/drafter_quality_harness.py`, the
`gather_quality_harness.py` pattern) — a pure dep-free `score_drafts()` scorer (counts-only:
stub-vs-live sign/refuse, fabrication-guard catch from `blocking_violations`, grounding consistency)
+ `--check` (replay a pinned live capture vs a frozen baseline; dep-free; in uv-run-pytest) +
`--freeze` (run `serve_chain.casework_consume` stub+openai per bundle; refuse to freeze a regression)
— measuring the live drafter vs the stub over the committed casefile bundles, with an honest
counts-only headline; companion-only, all 9 dists byte-frozen, casework + `evidence_requirements.py`
unchanged.

**In scope.** `tests/drafter_quality_harness.py` · `tests/fixtures/drafter-quality/**` ·
`tests/test_selftests.py` (the uv-run-pytest umbrella) · the live-draft sign/refuse regression
assertion in `tests/workbench.test.mjs` (+ `tests/chain.test.mjs` if present; minimal new surfacing
in `workbench.html`/`chain.html` only-if-needed) · `docs/drafter-live.md` ·
`docs/agentification-roadmap.md` (Stage 3 → BUILT) · CLAUDE.md + HANDOFF.

**Out of scope.** Any casework src edit / a re-vendor · any drafter or verifier behavior change · any
`evidence_requirements.py` / §12-funnel change · any new ship-dist artifact · an oracle firewall
(none needed — no truth to hide) · a gold-narrative correctness oracle (rejected).

**Constraints (load-bearing).**
1. No-oracle / consistency-only — counts-only stub-vs-live SIGN/REFUSE + fabrication-guard CATCH +
   grounding CONSISTENCY; NEVER an accuracy/catch-rate/precision/recall. See
   [[phase-86-no-oracle-consistency-measure]].
2. Non-degenerate two-sided contrast — the stub fail-closes on the narrative-seam case; T1 classifies
   the population first; honest NULL if degenerate. See
   [[phase-86-stub-vs-live-narrative-seam-contrast]].
3. Companion-only / casework-unchanged — all 9 dists byte-frozen; the Drafter Protocol + the six
   verifiers UNCHANGED (no re-vendor; pin `04cc335` == sibling HEAD); `evidence_requirements.py` + the
   256/376 §12 funnel UNTOUCHED; build.py imports nothing new. The agent drafts, the six verifiers
   gate, the human signs. See [[phase-86-companion-only-casework-unchanged]].
4. Honesty governor — counts-only; the synthetic-substrate qualifier on every number; the word-ban
   (no catch-rate/lift/precision/recall) extends to the new markers + docs; the always-on badge stays.
5. Execute-once honestly — no model on :8080 → ship the stub-only baseline + the named `--freeze`
   follow-on; NEVER fabricate a live number.

**Checkpoints.** After T1 (the dep-free `--check` harness — the stub-vs-stub / replay floor is the
always-checkable measured floor); at T2 (EXECUTE ONCE — if no model is reachable, STOP fabricating:
ship the stub baseline + the named follow-on; if the population is degenerate, surface the honest
NULL).

**Exit criteria.** See `## Exit Criteria` below (bidirectional with tasks T1–T5).

**Assumptions.** See `## Assumptions` below; each has a stop-if-violated fallback (assumption-ledger
Phase-86).

**Abort rule.** Any casework src edit / a re-vendor / a build.py companion import / a non-byte-identical
dist / an `evidence_requirements.py` or §12-funnel change / a fabricated live drafter number / a
degenerate measure presented as a contrast (or any accuracy/catch-rate/precision/recall framing) →
STOP-and-surface. If blocked >3 attempts: ask user — skip or abort.

## Scope

Files and modules affected (companion-only — NO ship/dist target; build.py imports none of it):
- `tests/drafter_quality_harness.py` — the pure dep-free `score_drafts()` scorer (counts-only) +
  `--check` (replay a pinned capture vs a frozen baseline; no casework subprocess, no model) +
  `--freeze` (run `serve_chain.casework_consume` stub+openai per casefile bundle; needs the casework
  venv + the local model; refuse to freeze a regression)
- `tests/fixtures/drafter-quality/**` — the pinned stub+live capture + the frozen `expected` baseline
- `tests/test_selftests.py` — register the harness `--check` in the uv-run-pytest umbrella
- `tests/workbench.test.mjs` (+ `tests/chain.test.mjs` if present) — assert the EXISTING live-draft
  surface shows SIGN/REFUSE (+ fabrication-catch / `blocking_violations` if surfaced)
- `workbench.html` / `chain.html` — MINIMAL new surfacing ONLY if the sign/refuse + fabrication-catch
  climax is not already visible (companion HTML only — touches no dist)
- `docs/drafter-live.md` (NEW) + `docs/agentification-roadmap.md` (Stage 3 → BUILT) + CLAUDE.md +
  HANDOFF — current-state true-up (replace in place; no per-phase bullet)

## Exit Criteria

- [ ] `python3 tests/drafter_quality_harness.py --check` PASS (or the honest "run --freeze (needs the
      casework venv + a live model)" message when no fixture); registered in the uv-run-pytest umbrella
- [ ] The live (or stub-only, honestly) counts-only headline recorded (stub vs live sign/refuse, the
      fabrication-guard catches, the narrative-seam contrast outcome; synthetic-substrate-qualified;
      no rate words; the fixture committed + replaying through `--check`)
- [ ] `node tests/workbench.test.mjs` green (assertion count grows); the live-draft sign/refuse
      assertion passes
- [ ] `docs/agentification-roadmap.md` Stage 3 marked BUILT (now TWO consistency-not-correctness
      harnesses — GATHER + the drafter); `docs/drafter-live.md` written + cross-linked from the roadmap
- [ ] Companion-only: `python3 scripts/build.py --check all` 9/9 byte-frozen; `git diff --quiet
      vendor/aml-casework` AND `git diff --quiet scripts/evidence_requirements.py` both empty; build.py
      imports nothing new (grep: no `drafter_quality_harness`); the 256/376 §12 funnel unchanged
- [ ] CLAUDE.md `## Current state` + Milestones + How-to-run + Test list + HANDOFF §8 trued IN PLACE
      (no per-phase bullet)
- [ ] Honesty swept (no catch-rate/lift/precision/recall in the new files/docs; the synthetic
      qualifier on every recorded number; a degenerate population surfaced as an honest NULL, never a
      manufactured contrast)

## Constraints

- No-oracle / consistency-only — prevents a non-accuracy dressed as an accuracy (the
  free-text-drafting honesty trap). See [[phase-86-no-oracle-consistency-measure]].
- Non-degenerate two-sided contrast — prevents a vacuous "live == stub" headline; the narrative-seam
  fail-close is the fulcrum. See [[phase-86-stub-vs-live-narrative-seam-contrast]].
- Companion-only / casework-unchanged — `vendor/aml-casework` + `evidence_requirements.py` BYTE-FROZEN;
  prevents a vendored-dependency edit / re-vendor / dist or §12-funnel ripple. See
  [[phase-86-companion-only-casework-unchanged]].
- Honesty governor — counts-only, synthetic-qualified, the word-ban; prevents an overclaim the
  no-oracle data cannot support.

## Checkpoints

- After T1 (the dep-free `--check` harness): the replay floor is the always-checkable measured floor —
  it ships regardless of model availability.
- At T2 (EXECUTE ONCE): if no model is reachable on :8080, STOP fabricating — ship the stub-only
  baseline + the named `--freeze` follow-on. If the population is one-sided (the stub signs every
  bundle), surface the honest NULL + the deliberately-ungrounded fallback case; never invent a contrast.

## Assumptions

(assumption-ledger Phase-86 — all ACCEPTED, all_accept: true NOT silent.)

- A1 [the T0 weakest, non-degeneracy] The measure is two-sided because the deterministic STUB drafter
  fail-closes on the narrative-seam case (Phase-82 CASE-P-0025128) — the committed
  `data/casefile/*.bundle.json` population spans SIGN and REFUSE. If false (the stub signs every
  bundle → degenerate): T1 measure-first surfaces the honest NULL + the deliberately-ungrounded
  fallback case; never a manufactured contrast.
- A2 [no oracle / consistency-only] The measure is counts-only (stub-vs-live SIGN/REFUSE +
  fabrication-guard CATCH + grounding CONSISTENCY), never an accuracy. If a "gold narrative" oracle is
  tempting: REJECT it (synthetic gold is judgment, not truth) — the abort rule's rate-word ban governs.
- A3 [measure/execute-once] The stub baseline is ALWAYS available; the live capture is best-effort. If
  no model this session: the stub-only baseline + the harness ship as the measured deliverable; the
  live freeze is a named follow-on; NEVER fabricate.
- A4 [companion-only / casework-unchanged — NON-NEGOTIABLE] All 9 dists byte-frozen; the Drafter
  Protocol + the six verifiers + `evidence_requirements.py` + the 256/376 §12 funnel UNCHANGED; no
  re-vendor. If a fix would need a casework edit: STOP-and-surface (the abort rule).

## Notes

- Mirrors the GATHER quality harness (`tests/gather_quality_harness.py`) — the consistency-not-
  correctness pattern: `--check` replays a pinned live capture with NO model against a frozen baseline
  + asserts consistency vs the deterministic stub; `--freeze` re-captures + refuses to lock a
  regression. The DIFFERENCE: the drafter runs through a casework SUBPROCESS (needs the casework venv),
  so `--check` replays PINNED consume results through a pure scorer (dep-free) rather than re-running
  the gate; `--freeze` runs the real subprocess.
- `serve_chain.casework_consume(bundle, out, drafter, disposition)` returns {drafter, drafter_effective,
  signed, disposition, blocking_violations, narrative_present, completeness} (`serve_chain.py:262-308`).
  BACKENDS = (stub, claude, openai, opencode); `resolve_backend` falls back honestly to stub.
- Vendored casework pin: `vendor/aml-casework/VENDORED_AT = 04cc335` == sibling HEAD `04cc335`
  (Phase 21). No newer drafter work landed; no re-vendor.
- The 6 live loops the program now has: news/corpus extraction · GATHER tool-calling · DECIDE drafting ·
  the merge adjudicator (Stage 1, oracle-scored) · the §12 determination pre-proposer (Stage 2,
  oracle-scored) · this drafter (Stage 3, consistency-measured). This phase MEASURES the existing
  drafter loop; it does not add a loop. The next leg in leverage order: a §14 triage second-rater.
- The roadmap's cross-cutting evaluation discipline: oracle-scored where truth exists (Stages 1/2),
  consistency-not-correctness where it doesn't (GATHER is the model). The drafter is the SECOND
  consistency-not-correctness harness.
