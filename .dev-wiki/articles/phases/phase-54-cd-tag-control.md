---
title: "Phase 54 — C/D tag control: the measured-not-gated control made real (SR-11-7 ongoing monitoring)"
type: phase
status: active
ceremony: lite
milestone: M9
created: 2026-06-16
updated: 2026-06-16
tags: [measure-first, corpus, honesty, c-d-tags, non-ship, control, sr-11-7, ongoing-monitoring, independent-rater, krippendorff, consensus]
---

# Phase 54 — C/D tag control: the measured-not-gated control made real (SR-11-7 ongoing monitoring)

## Objective

Stop point-measuring; build the **control**. Phases 51/52/53 measured the unguarded C/D dimension
three times — the C/D tags are *soft but adjudicable* (self-consistency 0.677, κ≈0.65; the
disagreement is sharp, not scatter; committed-error bounded ≥37% / ≤61%, the upper bound confounded by
context asymmetry). Those phases built the **instrument + a standing baseline**. This phase makes the
blueprint's §4–§5 **"measured-not-gated" control class** CONCRETE + EXECUTABLE for the C/D tag — the
canonical unguarded/judgmental dimension ("a grounding gate ≠ a completeness gate ≠ a correctness
gate") — closing the **named-OPEN Phase-47 T2/T3 blocker**: *"the production-grade SR-11-7-class
control DESIGN at scale (cadence, sampling, ownership, where it sits in the 5% charter) is not yet
written."* It also **executes the Phase-52/53 deferred follow-up once** (the user's rigor escalation at
the gate): a context-matched, genuinely-independent (local Qwen) rater → the clean cross-family
reliability number + Krippendorff's α that 52/53 left deferred — the control's "independent
effectiveness challenge," demonstrated for real, not merely scheduled.

## Approach (gated 2026-06-16 — control made real, independent challenge executed once, probe-gated)

Two parts, on existing machinery, with the model dependency isolated at the build boundary:

1. **The control DESIGN** — `docs/cd-tag-control.md` (NON-ship, Illustrative badge): the SR-11-7
   measured-not-gated control for the C/D dimension — scope + **risk-tiering** (BUILD_NOW-driving codes
   monitored tighter), the committed **baseline** (the Phase 51-53 numbers + the new independent one),
   ongoing-monitoring **sampling cadence** + seed discipline, **trip-wires** (self-consistency below the
   baseline Wilson lower bound; independent-challenge agreement below threshold; a new-source regate
   failure), the **independent effectiveness challenge** (executed once this phase, scheduled +
   owner-assigned thereafter), **ownership / escalation / re-baseline**, where it sits in the human 5%
   charter, and the **audit-walk** defensibility. Cites blueprint §4–§5 + SR-11-7 Pillar-2 + OSFI E-23
   (wiki) — does NOT edit `program-blueprint.md` (the cd-correctness-report-cites-§13 pattern; dodges
   the blueprint-report.html hand-sync drift).

2. **The control made EXECUTABLE** — extend `cd_correctness.py` (the PURE stdlib replay core) with
   **Krippendorff's α** (the chance-corrected inter-rater consensus stat 52/53 named as missing) +
   `--control-check` (draw the monitoring sample, compare vs a committed `cd-control-baseline.json`,
   emit **PASS / BREACH per trip-wire**) + `--control-freeze` (conscious re-baseline — the
   `news_quality_harness --freeze` idiom). Demonstrate **PASS on the current corpus + BREACH on injected
   drift** (the separability-gate "fires on an injected artifact" pattern). *A control that can't run is
   just prose.*

**The independent effectiveness challenge (executed once):** a SEPARATE dev-time companion
`scripts/cd_rate_independent.py` calls the local Qwen (127.0.0.1:8080), **context-matched** (the
source-doc region for the gid + the 28+20 interview posture + the closed vocab, grammar/json-schema
constrained C+D) over the **same** committed n=96 enlarged-random sample → `independent-sample.json`,
replayed deterministically thereafter. **Probe-gated** (Phase-46 pattern): T1 `--probe` verifies
competence on a few items; pass → full run; fail → fall back to an Opus-context-matched rater (removes
the context confound, not the family one) + the independence leg reverts to scheduled-with-owner,
surfaced at the checkpoint. The new math: Qwen-context-matched-vs-committed agreement (the clean
apples-to-apples reliability number) + cross-rater (Opus-blind-flag-only vs Qwen-context-matched) +
Krippendorff-α over the rater set.

## Scope

- `scripts/cd_correctness.py` (EXTEND — stdlib, deterministic, read-only; Krippendorff-α + the control modes)
- `scripts/cd_rate_independent.py` (NEW — dev-time companion; urllib → 127.0.0.1 local model; never imported by build.py or cd_correctness.py's replay path)
- `data/cd-correctness/{independent-sample.json, cd-control-baseline.json}` (NEW — non-corpus; build.py never reads it)
- `docs/cd-tag-control.md` (NEW — the SR-11-7 control design, non-ship, Illustrative badge)
- `docs/cd-correctness-report.md` (EXTEND — the named follow-up's "delivered in Phase 54 [executed]" line)
- `.dev-wiki/*`, `HANDOFF.md` (lifecycle / §8); **no CLAUDE.md edit** (non-ship, matches 51-53; trim debt unchanged)

## Key constraints

- **NON-SHIP, read-only.** The ship corpus (`corpus.html`, `dist/corpus`, every `data/*/derived/*.json`,
  the overlays) stays **byte-frozen**; `build.py` NEVER imports `cd_correctness.py` or
  `cd_rate_independent.py`; `data/cd-correctness/` is non-corpus; `--check all` 7/7.
- **The replay core stays PURE (A2).** `cd_correctness.py` is stdlib / no-network / deterministic — the
  ONLY model-calling code is the dev-time companion `cd_rate_independent.py`, which produces the fixture;
  the measurement replays from committed fixtures forever after.
- **Context-matched = the committed assignment's inputs (A1).** Source-doc region + the 28+20 interview
  posture + the closed vocab — NOT flag+red_flag-only. So the number is reliability, not a re-measurement
  of the Phase-53 context gap.
- **Consensus, never ground truth.** The independent number is blind cross-family agreement (≥2
  genuinely independent raters now), context-matched; reported with κ + Krippendorff-α + Wilson CIs,
  each definition-carrying; n / seed **chosen, not derived**; the always-on Illustrative badge on the doc.
- **No blueprint edit (A3).** Standalone doc cites §4–§5; the SR-11-7 / OSFI E-23 vocab is pulled from
  the aml-wiki, not guessed.
- **Privacy.** 127.0.0.1 model only; nothing leaves the machine; the independent fixture stores
  JUDGMENTS over committed indicators (no new external content → no fixture-promotion-allowlist concern).

## Exit criteria

- `python3 scripts/cd_rate_independent.py --selftest` GREEN (offline, stubbed model: context-matched
  prompt assembly carries the source-doc region + interview posture; the closed-vocab parse; never
  imports build.py); `--probe N` returns parseable in-vocab C/D from 127.0.0.1 (or the fallback is taken
  + surfaced at the checkpoint).
- `data/cd-correctness/independent-sample.json` committed; `python3 scripts/cd_correctness.py
  --verify-fixtures` GREEN (independent gids == the seeded enlarged-random sample; committed C/D match
  current).
- `python3 scripts/cd_correctness.py --selftest` GREEN incl. **Krippendorff-α** math (perfect→1,
  chance→~0, a hand fixture) + the control trip-wire logic; `--report` emits the independent stratum
  (agreement + κ + α + Wilson, definition-carrying, framed consensus + context-matched).
- `--control-check` GREEN **PASS** on the current corpus; an injected-drift fixture → **BREACH**
  (selftest); `--control-freeze` re-baselines consciously.
- `docs/cd-tag-control.md` renders the control (scope + risk-tier + baseline + cadence + trip-wires +
  independent challenge + ownership + escalation + re-baseline + 5%-charter + audit-walk), cites
  §4–§5 / SR-11-7 / OSFI E-23, always-on Illustrative badge; the Phase-47 T2/T3 control-story blocker
  marked resolved.
- `python3 scripts/build.py --check all` → ZERO drift (7/7); honesty grep clean (no "X% correct/error"-
  as-fact — consensus + context-matched framing); `build.py` has no cd_correctness / cd_control /
  cd-tag-control / cd_rate_independent reference.

## Abort rule

Any ship-corpus / dist drift → STOP and surface (the standing abort rule); never re-baseline. If the
local model fails the T1 probe (unavailable or incompetent at C/D) → take the named Opus-context-matched
fallback + schedule independence, surface at the checkpoint — do NOT silently degrade or force a
low-confidence number. If a validator looks like it needs loosening to pass → fix the DATA/design, never
the validator.

## Assumptions

Direction-gate ledger: `.dev-wiki/assumption-ledger.md` Phase-54 block — A0 local-model
availability+competence (T0 weakest; probe-gated + named fallback) · A1 context-matched =
committed-inputs (apples-to-apples) · A2 replay core stays pure / model isolated at the boundary · A3
non-ship + no-blueprint-edit. all_accept: true.

## Outcome (T1–T5 delivered 2026-06-16 — delivery gate pending acceptance)

All exit criteria met; `--check all` 7/7 zero drift; the change set contains ZERO ship artifacts (NON-ship confirmed).

- **The independent effectiveness challenge, EXECUTED (the Phase-52/53 deferred follow-up).** A
  context-matched, genuinely CROSS-FAMILY rater — a local **Qwen3.6-35B** (probe-gated; the user
  adjudicated competence at the T1 checkpoint after an 8-item interpretable probe) — re-rated the same
  committed n=96 sample: **C 0.604** (58/96, κ 0.583) / **D 0.646** (62/96, κ 0.599); cross-rater
  (Opus-blind-flag-only vs Qwen-context-matched) C 0.677 / D 0.646; **Krippendorff's α** over
  {committed, Opus-blind, Qwen-cm} **C 0.634 / D 0.618**.
- **The finding.** The context-matched cross-family agreement is *statistically indistinguishable* from
  the same-family self-consistency (0.677; Wilson CIs overlap), α ≈ raw ≈ 0.62 → the unguarded
  dimension's reliability is **genuine** (survives a family change, chance-corrected, ~0.6/axis, never
  validated-correct), and **context-matching resolves the Phase-53 confound** (the flag-only comparison
  overstated apparent disagreement). The probe even surfaced a plausible committed mis-tag and hit the
  named C8/C14 defensible-neighbour — competent, not defaulting.
- **The CONTROL, made real.** `docs/cd-tag-control.md` — the SR-11-7 Pillar-2 + OSFI E-23 grounded
  measured-not-gated control (scope · risk-tier [BUILD_NOW codes tighter] · the Phase 51-54 baseline ·
  quarterly cadence · 3 trip-wire classes · the independent challenge · three-lines-of-defense ownership
  · re-baseline trail · the audit walk). Executable: `cd_correctness.py --control-check` (PASS 7/7 on the
  frozen corpus) / `--control-freeze` (`cd-control-baseline.json`); BREACH demonstrated on injected drift
  (selftest + a live perturb-and-restore, baseline byte-restored).
- **A0 (the weakest assumption) HELD with a positive surprise:** the local Qwen was available AND
  competent — the named Opus-context-matched fallback was not needed. A1–A3 HELD (context-matched =
  committed-inputs; the replay core stayed pure stdlib with the model isolated in the dev-time companion;
  non-ship + no blueprint edit). Closes the Phase-47 T2/T3 control-story blocker.
- Artifacts: `scripts/cd_rate_independent.py` (NEW dev-time companion) · `scripts/cd_correctness.py`
  (extended — Krippendorff-α, cross-rater, independent stratum, control harness) ·
  `data/cd-correctness/{independent-sample,cd-control-baseline}.json` (NEW) · `docs/cd-tag-control.md`
  (NEW) · `docs/cd-correctness-report.md` (extended).

## Deferred residual (named, not built)

- **A human (domain-expert) independent rater** — the gold standard beyond cross-family model
  consensus; the control SCHEDULES it but this phase executes the model leg only.
- **The control extended to the whole measured-not-gated CLASS** (the news red_flag translation + any
  other judgmental dimension program-wide) — the reusable PATTERN, with C/D as the proven instance
  (the gate's not-chosen broader option).
- **The heading→capability determinism probe** (the Phase-37 thread) — the deterministic alternative to
  a neural tag on the subset where a section heading constrains C; a new dimension, not this phase.
