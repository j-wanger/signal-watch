# C/D-Tag Control — the measured-not-gated control, made real

> **Illustrative data & outputs.** NON-SHIP design + control artifact (the `cd-correctness-report.md` /
> `blueprint-report.html` / `probe-history.md` class). Read-only over the committed corpus; the ship
> corpus (`corpus.html`, `dist/corpus`, every `data/*/derived/*.json`, the overlays) is byte-frozen and
> **untouched**. Every number is **consensus / self-consistency, never validated correctness or ground
> truth**, and carries its measurement definition. Executable: `python3 scripts/cd_correctness.py
> --control-check` (PASS/BREACH) and `--control-freeze` (conscious re-baseline). Phase 54, 2026-06-16.

## What this is, and why it exists

The corpus's inverted extraction boundary gates **three different things and conflates none of them**:
*"a grounding gate ≠ a completeness gate ≠ a correctness gate."* The grounding gate proves each
verbatim `flag` is faithful to its source; it does **not** check that the per-indicator **C
(capability)** and **D (data-source)** codes are *correct*. Those codes are **load-bearing** — they
drive every downstream coverage field (status / data / build_rec / build_logic via the cover×data
matrix) and the Capability + Data-source lenses — yet the C/D dimension is **unguarded**: a mis-assigned
code silently shows a wrong posture corpus-wide, and no deterministic gate can catch it, because a
judgmental tag has **no ground truth** to gate against.

The program blueprint (§4–§5) anticipates exactly this: not every workload yields a deterministic
pass/fail, so its gate taxonomy carries a **"measured-not-gated"** class — dimensions you cannot gate
but **must** monitor, via blind inter-rater agreement + regression-against-a-baseline. Phases 51–53
built the **instrument** and a **standing baseline** for the C/D dimension (below). This document is the
thing those measurements were *for*: the **production-grade control** — scope, risk-tiering, baseline,
cadence, trip-wires, the independent effectiveness challenge, ownership, escalation, and re-baseline —
that turns three one-off numbers into an ongoing monitoring discipline. It closes the Phase-47 T2/T3
"control story" gap (named, never written).

## Regulatory frame (grounded, not asserted)

This is a model-risk **ongoing-monitoring** control. Under **SR 11-7** (Fed/OCC 2011; the 2021
interagency statement confirms AML monitoring/screening/AI tools are in scope), **Pillar 2 — model
validation** requires three independent activities: conceptual soundness, outcomes analysis, and
**ongoing monitoring**. AML models hit a **ground-truth problem** the OCC's 2021 Handbook names
directly — *"unlike credit models where default outcomes provide clear ground truth, there is no
definitive dataset of all money laundering that occurred"* — so it endorses **alternative outcomes
analysis** over naïve back-testing. A judgmental **tag** has the same problem one level down: there is
no ground-truth C/D code. The honest alternative-outcomes instrument is therefore **blind inter-rater
consensus** (consensus, never "proven correct").

The Canadian counterpart, **OSFI Guideline E-23** (effective 2027-05-01; the demo audience is a
Canadian bank), defines a model **lifecycle** whose **Model monitoring** stage maps to SR 11-7 Pillar 2
ongoing monitoring, and a **model risk rating** (categorical tier on quantitative + qualitative
dimensions) that drives *review frequency, documentation depth, approval authority, and monitoring
scope* — the proportionality this control's **risk-tiering** uses. E-23's own framing of "deterministic
gate baselines as ongoing monitoring" is precisely the `--control-check` regression baseline below.

> **Scope honesty.** This control governs the **C/D tag** — one judgmental component of the corpus
> derivation pipeline (itself plausibly a "model" under E-23/SR 11-7). The grounded `flag` is gated
> elsewhere (`derive_signals.py --check-derived`); completeness is a third thing again. This is the
> *measured-not-gated* control for the *one* unguarded dimension, not a whole-pipeline MRM program.

## The standing baseline (Phases 51–54, committed)

| Stratum | What it measures | Result | Definition / caveat |
|---|---|---|---|
| **Self-consistency** (random, n=96) | a same-family blind re-rate vs committed, per axis | C/D **0.677**, **κ ≈ 0.65 ≈ raw** | REPRODUCIBILITY (shared-bias) — lower-bounds reliability; κ ⇒ genuine, not chance |
| **Independent reliability** (n=96) | a **context-matched, cross-family** (local Qwen) rater vs committed, per axis | C **0.604** (58/96), D **0.646** (62/96) (κ C **0.583**, D **0.599**) | the Phase-52/53 deferred follow-up, executed — removes the context confound AND the same-family bias; still consensus |
| **Cross-rater** (n=96) | Opus-blind-flag-only vs Qwen-context-matched | C **0.677** (65/96), D **0.646** (62/96) | a genuine cross-family number (neither is committed) |
| **Panel consensus** | Krippendorff's α over {committed, Opus-blind, Qwen-context-matched} | C α **0.634**, D α **0.618** | chance-corrected 3-rater consensus; the panel is 2 model families + committed, **not yet a human** |
| **Divergence uphold** (hard subset, n=24) | a blind rater upholds the Phase-34 correction | **0.708** (17/24, 0 neither) | adjudicable on the hard cases; a forced binary scores mechanically higher |
| **Redundancy context** (Phase 51) | cross-regulator co-occurrence ceiling | **≤ 0.325** | context for tiering, not a trip-wire |

**The finding the independent stratum delivers.** A context-matched cross-family rater agrees with the
committed C/D at **0.604 (C) / 0.646 (D)** — *statistically indistinguishable* from the same-family
self-consistency (0.677; the Wilson intervals overlap), with Krippendorff's **α ≈ 0.62** over the
3-rater panel. Two reads follow: **(1) the reliability is genuine** — it survives a change of model
family and is chance-corrected (α ≈ raw), so it is not a same-model echo; and **(2) context-matching
matters** — given the document context the committed code had, an independent rater lands *near*
committed (≈0.6), not far below it, so the Phase-53 flag-only comparison **overstated** apparent
disagreement (its "committed-questionable ≤61%" upper bound was inflated by the context asymmetry this
stratum removes). The honest reliability of the unguarded dimension is therefore **~0.6 per axis: soft,
genuine, adjudicable — and never to be presented as validated-correct.** (What this stratum does *not*
do: re-run the forced-pairwise decomposition with the Qwen rater — so it bounds the confound's
direction without re-measuring its exact share; a human-rater panel remains the deferred upgrade.)

## Risk-tiering (proportionality — E-23 model risk rating / SR 11-7 Tier 1–4)

Monitoring intensity scales with how load-bearing a code is. The C/D codes are tiered by downstream
materiality:

- **Tier-A (tightest):** codes that drive a **BUILD_NOW** disposition (cover×data ⇒ a full
  `build_logic` + a committed signal candidate). A mis-tag here changes what the institution is told to
  *build* — highest blast radius. Sampled every cycle; every breach adjudicated.
- **Tier-B:** codes driving PARTIAL / SOURCE_DATA coverage (a posture claim, no build). Sampled on a
  rotating basis.
- **Tier-C:** display-only lens membership. Spot-checked.

(The tier of a code is derived from the committed cover×data matrix at monitoring time — no new stored
field; the corpus stays byte-frozen.)

## The control loop (cadence · sampling · trip-wires)

**Cadence.** A quarterly ongoing-monitoring cycle (SR 11-7 Pillar 3's "quarterly ongoing monitoring
reports on performance metrics and threshold breaches"), plus an **event-triggered** cycle on any of:
a new corpus source, a re-derivation, or a C/D re-tag.

**Sampling.** A seed-fixed corpus-proportional random draw (the committed n=96 enlarged-random sample
is the reference instance; the seed is recorded so a cycle is reproducible and an auditor can replay
it). The **independent effectiveness challenge** — the context-matched cross-family rater — runs at
least annually and on any baseline change.

**Trip-wires** (`--control-check`; a breach is first-class, never silently swallowed):

1. **Integrity** — every committed fixture's snapshot of the C/D code still matches the *current*
   corpus. A re-tag of the unguarded dimension trips this immediately (it is the live drift detector
   while the corpus is frozen).
2. **Self-consistency floor** — the same-family re-rate agreement stays at/above its frozen **Wilson-95
   lower bound** (C/D ≥ **0.578**). A re-sampled cycle that degrades below the floor trips this.
3. **Independent-reliability floor** — the cross-family agreement stays at/above its frozen Wilson-95
   lower bound (C ≥ **0.504**, D ≥ **0.546**).

`--control-check` re-evaluates the committed fixtures against the current corpus and the frozen
`cd-control-baseline.json`, emitting **PASS / BREACH** per wire (exit 1 on any breach). On the frozen
corpus it **PASSES**; the selftest demonstrates a **BREACH** on an injected drift (a re-tag that breaks
integrity and pushes a rate below floor — the separability-gate "fires on an injected artifact"
pattern). `--control-freeze` re-records the baseline — a **deliberate** act, the way a corrected corpus
is adopted (the `news_quality_harness --freeze` idiom).

## Ownership, escalation, remediation (three lines of defense)

- **1st line** — the derivation/build owner: owns C/D performance, runs the monitoring cycle, cannot
  self-validate. Files the cycle report (`--report`) + the `--control-check` verdict.
- **2nd line** — an **independent C/D reviewer/adjudicator** (different model family today; a domain
  expert is the named upgrade): owns the independent effectiveness challenge and **adjudicates
  breaches** — is a flagged code a genuine error, a defensible neighbour (the C8/C14-class scatter the
  measurements surfaced), or a baseline that should move?
- **3rd line** — audit: assesses that the control itself runs (cadence kept, breaches dispositioned,
  baselines re-frozen only deliberately).

**Remediation on a breach:** adjudicate → if a genuine error, **re-tag** via the deterministic
downstream (the ph33 rule: regenerate status/data/build_rec/build_logic from the corrected C/D, never
re-author neurally) → re-run the grounding gate → `--control-freeze` to re-baseline → log the issue +
its resolution (SR 11-7 Pillar 3 issue tracking). A re-tag is a **conscious corpus change** that exits
the byte-frozen envelope — out of scope for this NON-SHIP control, surfaced for human action.

## Where it sits in the human charter (the 5%)

The blueprint's ~95% agentic / ~5% high-judgment-human split is a **direction, never a target ratio**.
This control is squarely the 5%: the deterministic parts (sampling, agreement arithmetic, trip-wire
evaluation, integrity) are automated and run unattended; the **judgment** — adjudicating a breach,
deciding error-vs-defensible, authorizing a re-baseline — is the irreducible human work the charter
reserves. The control's job is to **route** the rare judgmental case to a human with the evidence
assembled, not to automate the judgment away.

## Defensibility — the audit walk

A supervisor's question is *"how do you know your capability tags are right?"* The honest, walkable
answer: we **don't gate** a judgmental tag (there is no ground truth) — we **measure** it as blind
inter-rater consensus, against a committed baseline, on a recorded cadence, with breaches adjudicated by
an independent second line and a deliberate re-baseline trail. Every number in this document is
reproducible (`--report`, `--selftest`, `--control-check`), carries its definition, and is labelled
consensus — never validated correctness. That chain — *unguarded dimension → named control → committed
baseline → executable trip-wire → adjudicated breach → re-baseline trail* — **is** the defensibility.

## Honesty boundary (what this is NOT)

- **Not validated correctness, not ground truth.** Every figure is blind inter-rater agreement /
  self-consistency. The panel is two model families + the committed code; a **human** domain-expert
  rater is the named, deferred-with-owner upgrade.
- **Not a whole-pipeline MRM program.** It governs the one *unguarded* dimension (the C/D tag); the
  grounded `flag` and completeness are gated/measured separately.
- **Parameters are chosen, not derived.** Sample size (n=96), seed (0), cadence (quarterly), and the
  Wilson-lower-bound floors are choices recorded for reproducibility, not optimized values. The
  deliverable is the **reproducible control machinery + an honest first instance**, not a final number.
- **NON-SHIP.** The ship corpus stays byte-frozen; `build.py` never reads `data/cd-correctness/`; no
  C/D number lands on any ship artifact.

## Reproduce

```
python3 scripts/cd_correctness.py --report          # the full baseline (all strata, incl. the independent stratum + α)
python3 scripts/cd_correctness.py --control-check    # PASS/BREACH vs the frozen baseline (the monitoring loop)
python3 scripts/cd_correctness.py --control-freeze    # re-record the baseline (a deliberate re-baseline)
python3 scripts/cd_correctness.py --verify-fixtures   # integrity: every fixture matches its seeded sample + current corpus
python3 scripts/cd_correctness.py --selftest          # agreement / kappa / Krippendorff-alpha / trip-wire logic, on fixtures
python3 scripts/cd_rate_independent.py --selftest      # the dev-time companion (offline): context-matched prompt + parse + schema
```
