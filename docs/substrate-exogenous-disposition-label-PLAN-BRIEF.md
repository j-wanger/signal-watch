# PLAN BRIEF — aml-substrate: emit an EXOGENOUS disposition label

> **Status: cross-pillar PLAN BRIEF (Phase 74, signal-watch).** A handoff for the **aml-substrate**
> sibling to build on its own lifecycle — *no code lands in aml-substrate from here* (the Phase-55–58 / 66
> pattern: signal-watch authors the contract; the sibling implements + measures it). Synthetic /
> illustrative; **no catch-rate, lift, or precision number is asserted.** Companions:
> [true-entities-scorer-contract](true-entities-scorer-contract.md) (the evaluation-only-channel pattern
> this brief reuses) and [confidence-as-provenance-contract](confidence-as-provenance-contract.md) (the
> "priors are provenance, never a signal" / self-confirming-loop guard).
>
> **Verified sibling pin: `a3fb02b4efe5ffb564c88cf3fd4931ba672ab63a` ("close Phase 27", branch `main`),
> code-verified 2026-06-25.**
>
> **DRIFT / verified-state NOTE.** This brief's premise holds at HEAD — and is *cleaner* than assumed:
> - `compose.py` is **explicitly score-deferred** (`monitor/compose.py:4-6`, decision D3): "no risk
>   score, numeric rating, or priority is emitted … presenting it as a real risk score is the
>   fabricated-figure class." An alert/dossier is a plain dataclass with **no disposition and no label**
>   (`alert.py:8` — "No risk score and no label is ever attached"). So **there is no disposition label to
>   validate against today** — confirmed gap, this brief's whole reason.
> - The **latent generating process already exists and is label-bearing**: `Transaction.illicit_flow` /
>   `Transaction.laundering_label` (`schema/transaction.py:40-41`) and `Party.latent_role` /
>   `illicit_income` / `illicit_income_type` (`schema/party.py`) are the ground-truth fields the generator
>   sets. `monitor/measure.py` is the **deliberate sole reader** of these label fields ("the ONLY Phase-3
>   module that reads the synthetic label fields — a deliberate boundary … to MEASURE detection, never to
>   tune a threshold"). The exogenous *disposition* label this brief asks for is a **consequence of that
>   same latent process**, ridden out on the **same evaluation-only channel** the existing labels use —
>   the architecture is already in place; this adds one derived field to it.

---

## Objective

Emit an **exogenous disposition label** — the intended **file** / **clear** outcome a case *should*
receive — that is **decoupled from casework's sufficiency rule**, so signal-watch's determination engine
(`evidence_requirements.evaluate_sufficiency`) can be validated against a label it **did not itself
author**.

This is the **circularity exit.** Today, in the signal-watch determination loop, the *features* (the legs,
the network, the source-of-funds atoms) and the *outcome the engine derives* both flow from one
author-generator (signal-watch's own authored `case.json` + its own sufficiency profile). An engine that
authors both the inputs and the answer cannot be *validated* — only *replayed*. The substrate, which owns
the **latent generating process** that decided who is actually laundering, is the one author positioned to
emit the intended outcome **blind** to the engine that will be measured against it.

## The exact emission shape

Per emitted case/entity, a single exogenous label on the **evaluation-only channel** (alongside
`illicit_flow` / `latent_role`, **never** on the evidence bundle the engine reads):

```jsonc
{
  "intended_disposition": "file",          // closed vocab: "file" | "clear"
  "intended_basis": "predicate_established" // closed vocab; the latent REASON, not the engine's rule
}
```

- `intended_disposition` is a **two-value closed vocab**: `file` (the latent process placed a real
  predicate behind this flow) | `clear` (the flow is a generated legitimate / explained pattern — the
  affirmative-clear analogue, e.g. a household co-resident pattern or an explained source-of-funds).
- `intended_basis` names the **latent cause** drawn from the generating process's own vocabulary
  (`predicate_established`, `legitimate_pattern`, `explained_source_of_funds`, `coincidental_collision`,
  …) — it is the *why* the generator knows, **not** a restatement of the engine's sufficiency atoms
  (mechanism / ≥2 legs / named predicate). The two must be **independently authored** so agreement is
  *evidence*, not a tautology.

### Two hard constraints (these are what make it a valid oracle)

1. **Authored BLIND to the sufficiency profile.** The label is a **consequence of the latent generating
   process** (the same machinery behind `illicit_flow` / `latent_role` / `laundering_label`) — emitted by
   the generator's truth, **not** by running anything resembling
   [`evidence_requirements.py`](evidence-driven-filing.md)'s rule (mechanism + ≥2 corroborating legs +
   named predicate + no unrebutted mitigation). If the substrate were to compute the label *from* the
   sufficiency rule, the engine would again be graded against its own logic — the exact circularity this
   exits. The generator already knows the truth (it minted the predicate); read it from there.

2. **Evaluation-only channel — never on the engine-input surface.** The label rides the **same
   firewalled channel as `true_entities` and `illicit_flow`** (the
   [scorer contract](true-entities-scorer-contract.md) §Firewall pattern): the resolver / determination
   engine **never reads it**; only an evaluation harness does. This mirrors the existing discipline — the
   evidence bundle (`monitor/evidence.py`) is built from label-stripped `TxnView`s precisely so "no label
   field can leak into the evidence" (`evidence.py:10, 135`). The disposition label inherits that firewall
   verbatim. A contract test must fail the build if `intended_disposition` / `intended_basis` appears on
   any field the engine consumes.

## How the consumer uses it (validation, not coupling)

signal-watch runs its determination engine over the **observable** emitted bundle (no label), derives
file-vs-clear from the sufficiency rule, then an **evaluation harness** (the only reader of
`intended_disposition`) compares the two — **agreement, not training.** The engine is never tuned toward
the label (the same A2/A3 discipline `measure.py` already enforces for detection: "never fixed by tuning
toward the ground truth"). Disagreements are the honest finding — a case the engine *files* that the latent
process intended to *clear* is a **false-file** the artifact can now *see*, where today it is invisible
because the engine grades its own homework.

The label also closes the loop with the **affirmative-clear** path: a `clear`-intended case that the engine
clears (mechanism + 0 legs + affirmative mitigation established — the Phase-73 additive branch, file bar
byte-unchanged) is a validated clear; a `clear`-intended case the engine *files* exposes an over-filing
edge the determination profile would otherwise hide.

> **Self-confirming-loop guard (cite [confidence-as-provenance](confidence-as-provenance-contract.md)
> §Priors).** The exogenous label is an **evaluation oracle**, never an engine input — exactly as a prior
> disposition is "provenance, never a signal." It must never become a feature: the invariant is that
> `evaluate_sufficiency` produces a **byte-identical** verdict whether or not the label exists. The label
> grades the engine; the engine never reads the label.

## Sibling-executed framing

Built in **aml-substrate**, on its own lifecycle, **measure-first**: emit `intended_disposition` on a
slice through the existing label channel, run signal-watch's `serve_workbench.casefile_*` consume +
evaluation harness over it, and report only an **agreement-rate framing qualified "measured on synthetic
clusters; production has no ground truth"** (the [scorer contract](true-entities-scorer-contract.md)
honesty rule) — **never** a precision / catch-rate / lift number presented as production-trustworthy. This
is the determination analogue of the resolution scorer: synthetic is the one place the latent answer
exists, so it is where the *mechanism* is validated before the abstain-discipline is trusted on real data.

## Why this matters to the consumer (the entity spine + the decisioning lever)

The whole program rests on separating two cases that fire the **same** grounded signals but deserve
**opposite** outcomes (Northgate-files / Lakeshore-clears). That separation is only *defensible* if the
engine that makes it can be shown to agree with a truth it did not author. Without an exogenous label the
determination engine is unfalsifiable — it can only replay its author's intent. With it, the engine becomes
**measurable against the latent generating process**, the resolved entity spine becomes the substrate the
measured decision stands on, and the rich case stops being *authored-and-self-graded* and becomes
*emitted, resolved, and validated end-to-end* against an independent oracle.
