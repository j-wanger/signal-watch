# North-star cases AT SCALE — the cross-pillar build order

> **A signal-watch-authored coordination snapshot** — the program-level "what it takes to GENERATE north-star-quality
> investigation cases at scale (rather than hand-author them), and in what order." Per-pillar detail lives in the two
> handoff briefs this points to. **Grounded in a Phase-81-post assessment (2026-06-28) measured against substrate
> `f7fbdb0` (Phase 37) + casework `076fb8e` (Phase 19) + the committed 376-case workbench slice.** Synthetic /
> illustrative; no rate, score, or multiplier is claimed.

## The intent, stated plainly

The north-star pair (`data/casefile/case.json` — Northgate FILES / Lakeshore CLEARS on the SAME signals) is the
program's **authored quality bar**, and it was authored FIRST as the cross-pillar SPEC (Phase 73 inverted the
pillars: signal-watch authors the rich case; substrate + casework implement what it takes to reach it). This
document answers a single question — *do we now have enough to recreate that quality at scale?* — with a measured
**no, not yet**, and turns the gap into an ordered, sibling-consumable build plan.

## The decomposition (what "north-star quality" actually is)

A north-star case = **rich evidence × a defensible determination × a reliable sign + render.**

| Factor | At scale today (measured) |
|---|---|
| **Case MATERIAL** (grounded signals over a real transaction network, identity, BO graph, source-of-funds) | **GENERATED — and richer than the north-star** (376 cases, dozens-to-hundreds of rail-aware txns each; capability mix C2/C3/C5/C8/C14/C15). |
| **The determination ENGINE** (the sufficiency rule, run identically over every case) | **GENERATED** — the same `evaluate_sufficiency` runs over all 6935 cases; the north-star verdict is engine output, not a special path. |
| **The determination EVIDENCE** (named predicate, affirmative mitigation, the 2nd corroborating leg, the multi-hop ownership chain, the flagged/excluded ER edges) | **AUTHORED-ONLY / analyst-supplied** — the decisive layers exist only in the 2 hand-authored cases. |
| **Sign + rich render** (casework signs; names-not-codes + 3 graphs) | **GAPPY / authored-only** — 128 of 376 sign (the mule topology fails-closed); the 3-graph surface renders only the 2 authored cases. |

So the **material and the engine scale; the decision and the signing do not.** The north-star is not blocked on
"more cases" — it is blocked on the specific **decision-layer evidence** and the **sign-time grounding** the siblings
must emit.

## The reframe that governs the whole plan

Two of the gaps are **by design, not deficiencies.** The named predicate and the mitigation judgment are the
**human gate** (the program's Class-J / §12 charter — a determination is a human act). So "north-star quality at
scale" is NOT "auto-decide cases unattended" — that contradicts the doctrine. It is: **generate EVIDENCE rich and
grounded enough that a human gate produces north-star determinations at scale, with every input READ from an
auditable record rather than typed ungrounded.** Every ask in the two briefs is *evidence the gate consumes*, never
a verdict — and every new signal stays **label-blind + measure-first** (the Phase-81 discipline: a corroboration or
predicate signal that correlates with the latent label is a forbidden tell).

## The build order (prioritized; → the handoff briefs)

### Track S — aml-substrate: emit the decision-layer EVIDENCE
→ [`substrate-northstar-evidence-emission-PLAN-BRIEF.md`](substrate-northstar-evidence-emission-PLAN-BRIEF.md)

1. **A predicate-bearing reference layer** (`prior_str_register` + `caution_list`) — *the keystone.* Measured: the
   file bar REQUIRES a named predicate and **0 of 376** slice cases carry one → every case stalls unattended.
   Emit a reference register the gate READS the predicate from (not a generated label — that would auto-decide /
   plant a tell).
2. **Affirmative-mitigation evidence as OBSERVABLE bundle fields** — *the rich DISMISS half.* Measured: substrate
   knows **4485 of 6935** cases are "explained source of funds" but FIREWALLS it onto the eval-only oracle → the
   engine (blind to the oracle by the non-circularity guard) can only ever clear-by-absence. Emit the explanation as
   auditable evidence (an exculpatory leg, a flow-reconciliation flag) so the engine earns `mitigation_established`
   honestly.
3. **The 2nd corroborating leg as a FIRED signal** — close the §12 gap (the engine assembles file-ready for **50 of
   121** oracle-file cases; the 2nd leg has no fired detector, only GATHER). Label-blind, measure-first.
4. **Multi-hop `ownership_edges` + `flagged`/`excluded` resolution edges** keyed to the reference layer (#1). The
   chain that REACHES a caution-listed node is the corroboration; `excluded` is the over-merge-honesty keystone.

### Track C — aml-casework: ground the topologies so north-star FILES SIGN
→ [`casework-northstar-signing-PLAN-BRIEF.md`](casework-northstar-signing-PLAN-BRIEF.md)

1. **Fan-IN C3 grounding at population scale** — *the dominant signing blocker.* Measured: **190 of 376** fail-close
   on the fan-in mule shape that IS the north-star FILE topology. Ground the topology; never loosen the verifier.
2. **C15 shell/nominee-ownership replay** (**49** fail-close) — re-derive over the SAME `ownership_edges` substrate
   emits (Track S #4), so the determination leg and the sign-time replay share one ownership model.
3. (Lower) a grounded STR-narrative contract (template-cites-evidence OR live-DECIDE-only — never pre-fabricated prose).

### Track W — signal-watch (local, small): render a GENERATED case at north-star richness

- A `showcaseSurface` adapter so a generated slice case renders **names-not-codes + the 3 graphs**
  (money-flow / resolution / BO) — today hard-gated to the 2 authored cases. **Gated on** the slice carrying the
  resolution + multi-hop-BO + reconciliation density the surface assumes — i.e. it lands AFTER Track S #2/#4. This
  is the only signal-watch-local piece; everything decisive is sibling-rooted.

## Dependency order + what unblocks what

- **S#1 (predicate reference)** unblocks *every* unattended determination — do it first; it is the single highest-leverage emission.
- **S#2 (affirmative evidence)** unblocks the entire rich-DISMISS half — without it, "clear at scale" is forever clear-by-absence.
- **S#4 (ownership chain + flagged/excluded)** feeds S#1 (the flagged edge supplies the predicate) AND C#2 (the shared ownership model) — land it alongside.
- **C#1 (fan-in C3)** is independent and unblocks the largest signing class — it can land in parallel with the substrate track.
- **W (render adapter)** is last — it presents what the other tracks make real.

The matched-pair *device* (same signals, opposite outcome) is deliberately OUT of scope as a generation target: it
is an authoring flourish for the demo, not a quality requirement; the value is rich, decided, signed individual
cases at scale, which the four tracks above deliver.

## Honest qualifier

Every number here is measured on **synthetic substrate** ("chosen-not-measured" params; counts, not rates); real-world
quality is a further question the always-on illustrative badge governs. This plan scales the *grounding* of north-star
evidence and the *signing* of north-star topologies — it does not, and by program doctrine should not, automate the
human determination itself.
