# PLAN-BRIEF — aml-substrate: the decision-layer evidence emission for north-star cases AT SCALE

> **A signal-watch → aml-substrate handoff brief** (the Phase-55–79 pattern: signal-watch authors the contract;
> the sibling implements + measures it on its own lifecycle — *no code lands in substrate from here*). Synthetic /
> illustrative; **no rate, score, or multiplier is claimed.** **Pinned to verified substrate HEAD `f7fbdb0`
> (Phase 37), code-verified 2026-06-28.** Companion to
> [`northstar-at-scale-build-order.md`](northstar-at-scale-build-order.md) (the coordination overview) and
> [`casework-northstar-signing-PLAN-BRIEF.md`](casework-northstar-signing-PLAN-BRIEF.md) (the sibling half).

## Intent

The north-star investigation pair (`data/casefile/case.json` — Northgate FILES / Lakeshore CLEARS on the SAME
signals) is the program's **authored quality bar**: a rich, grounded, network-and-source-of-funds case carrying a
**defensible determination**. It was authored FIRST as the cross-pillar SPEC (Phase 73 inverted the pillars).
A Phase-81-post assessment measured how far the GENERATED 376-case substrate slice has come toward that bar. The
finding: **the case MATERIAL is generated at scale (grounded signals over a real-shaped transaction network — in
fact RICHER than the north-star: dozens-to-hundreds of rail-aware txns/case vs ~15 — plus named identity, a BO
graph, source-of-funds), and the determination ENGINE runs identically over all of it.** What is NOT generated is
the **decision-layer EVIDENCE** — the layers that make the north-star *decisive*. This brief names exactly that
evidence, so a generated case can carry a north-star-quality determination at scale instead of being hand-authored.

**The load-bearing distinction (read this first):** the goal is NOT for substrate to GENERATE determinations
(deciding is a human gate by program doctrine — Class-J / §12). The goal is for substrate to emit the **grounded,
auditable EVIDENCE** a human gate reads to decide — replacing today's *analyst-typed-ungrounded* inputs with
*read-from-a-record* inputs. Every ask below is evidence the gate consumes, never a verdict.

## What is already generated at scale (do NOT re-emit)

Verified across the committed 376-case slice + the 6935-case `--emit-eval-oracles` population: grounded `alerts[]`
(verbatim flags + signal_id + grounded txn_ids; C2 323 / C3 313 / C8 142 / C14 107 / C15 88 / C5 63 / C4 34),
rail-aware `transactions[]`, `display_name` identity, `resolution_edges` (status `resolved`, 67 across 41 bundles),
`related_parties[]` BO (56 of 376), a `source_of_funds` LABEL (217 of 376). The §12 ML loop closes from real
signals (mechanism + ≥2 legs) on the cases that have them. **This brief is ONLY the missing decision evidence.**

## The asks (decision-layer evidence — each with the design choice + why)

### 1. A PREDICATE-bearing reference layer (`prior_str_register` + `caution_list`) — the keystone

- **The gap (measured):** the file bar REQUIRES `named_predicate_risk` (for money_laundering AND kyc_integrity);
  **no determination completes without it.** **0 of 376** slice cases carry one — it is typed by the analyst at the
  gate, or read from a prior-STR register that exists ONLY in the 2 hand-authored casefile cases. Unattended, every
  slice case stalls at `needs_more_info`. The north-star's predicate comes from a `flagged` resolution edge
  (Vesna Maric → `PSR-0001`, carrying `predicate: "human trafficking"`).
- **The emission:** a population-scale reference layer — a `prior_str_register[]` (prior-STR records keyed on
  counterparty/party identifiers, each carrying a typed `predicate`) and a `caution_list[]` (addresses / entities of
  concern) — plus the `resolution_edges` (ask #4) that hit them.
- **KEY DESIGN CHOICE — emit a REFERENCE LAYER the gate READS, not a per-case generated predicate. WHY:** a
  generated predicate would be substrate *auto-deciding* the offence, collapsing the human gate and (worse) planting
  a `flag↔label` tell the program forbids (the Phase-81 / broader-C7 discipline). A reference register keyed on
  identifiers is HONEST: the analyst (or the memory/resurfacing path) READS the predicate from a grounded record,
  with the audit walk intact. It scales the *grounding* of the predicate, not the *decision*.

### 2. AFFIRMATIVE-mitigation evidence as OBSERVABLE bundle fields — the rich DISMISS half

- **The gap (measured):** at scale we generate FILES and CLEAR-BY-ABSENCE, never the north-star's *affirmatively
  explained* dismissal. The clear engine branch is correct but reachable ONLY on the 2 authored bundles. **0 of
  376** slice bundles carry an `exculpatory` or reconciliation field. Substrate KNOWS the affirmative basis —
  `explained_source_of_funds` is **4485 of the 6935** oracle cases — but that knowledge rides the EXOGENOUS oracle.
- **The emission:** per case, derive and emit OBSERVABLE exculpatory evidence — an `exculpatory: true` txn leg, and
  a reconciliation flag (inbound legs tie to `nature_of_business`; volume fits `expected_monthly`; a recurring,
  identifiable supplier) — the structured analog of the north-star's authored `clearance_record`.
- **KEY DESIGN CHOICE — emit it as OBSERVABLE EVIDENCE, NOT through the disposition oracle. WHY (the firewall):**
  the engine is structurally FORBIDDEN from reading the oracle (`assert_no_oracle_leak` / `assert_engine_blind_to_oracle`
  — the Phase-78 non-circularity guard: if the engine consumed the answer key, the determination would be circular,
  true-by-construction, worthless). So the affirmative explanation must arrive as evidence the engine earns
  `mitigation_established` from — auditable bank-observable facts (the flows, the supplier) — distinct from the
  held-out oracle label. This is the ONLY firewall-respecting way to make affirmative dismissals generable. Without
  it, "clear" at scale is forever clear-by-absence, and the north-star's whole thesis ("the source of funds is the
  difference") has no generated analogue.

### 3. The SECOND corroborating leg as a FIRED signal (close the §12 gap)

- **The gap (measured):** of **121** oracle-file cases the signal layer assembles file-ready for **50** and MISSES
  **71**. The missing piece is the second corroborating leg — ML-A5 (external corroboration) has `evidence: []`, so
  it is closeable ONLY by the per-case GATHER agentic loop, which does not run at batch scale; the §12 signal layer
  pre-positions under half of files unattended.
- **The emission:** a fired detector for the second leg — a network/source-of-funds corroboration signal (the
  counterparty-network edge / the SoF inconsistency) that assembles ML-A4/ML-A5 from EMITTED signals, not only from
  a gather pass.
- **KEY DESIGN CHOICE — keep it LABEL-BLIND and MEASURE-FIRST. WHY:** the Phase-81 lesson (and substrate's own
  broader-C7 cut) — a corroboration signal that correlates with the latent label is a forbidden tell; emit it
  label-blind and report `needs-behavior` until the lift is *measured*, never stamped. The value is determination
  BREADTH (more files pre-position from internal signals), not detection lift.

### 4. MULTI-HOP `ownership_edges` + `flagged`/`excluded` resolution edges keyed to the reference layer

- **The gap (measured):** **0 of 376** bundles carry an `ownership_edges` block (BO is flat single-hop
  `BENEFICIAL_OWNER` only); **0 flagged / 0 excluded** resolution edges across the slice (67 `resolved` only). The
  north-star's load-bearing corroboration is the MULTI-HOP chain (Northgate ← `1187442 Ontario Inc.` ← a
  caution-listed address) and its two decisive ER edges — the `flagged` edge that SUPPLIES the predicate (#1) and
  the `excluded` near-match that PROVES exact-on-identifier (the false-positive discipline).
- **The emission:** `ownership_edges[]` with intermediary nodes terminating against the `caution_list` (#1); and
  `resolution_edges` with `status: flagged` (hit a `prior_str_register` entry) and `status: excluded` (a name
  near-match that does NOT share an identifier).
- **KEY DESIGN CHOICE — the chain TERMINATES against the reference layer, and `excluded` is a first-class status.
  WHY:** the chain's investigative value is *reaching* a known-bad node (predicate corroboration); without a
  reference layer to terminate against, a chain is just topology. And `excluded` is the north-star's
  honesty-keystone (the Lakeshore near-match cleared BECAUSE no identifier was shared) — it is what proves the
  program does not over-merge on a name; it must be a generated status, not only an authored one.

## Firewall + honesty constraints (LOAD-BEARING)

- **Contract-neutral where possible:** prefer ADDITIVE bundle fields so existing consumers (casework's v0.3 view,
  the determination engine) read the same shape; a new field defaults-absent on old captures.
- **The oracle stays firewalled:** affirmative-mitigation + predicate evidence are OBSERVABLE bundle fields, NEVER
  the `intended_disposition` / `intended_basis` oracle (that remains the eval-only measurement channel —
  `assert_no_oracle_leak`).
- **Label-blind + measure-first:** no `flag↔label` correlation on any new signal (the predicate reference and the
  second leg); report measured behavior, never a stamped lift. Synthetic / illustrative throughout.

## Pin / status / sequencing

- **Pin `f7fbdb0` (Phase 37).** Status: NOT BUILT (the named handoff). Re-verify the live HEAD before acting
  (sibling state drifts — [[cross-pillar-review-verify-sibling-repo]]).
- **Sequence:** #1 (predicate reference) + #2 (affirmative evidence) are the highest-leverage (they unblock the
  determination AND the dismissal); #4 (ownership chain + flagged/excluded) feeds #1; #3 (second leg) widens file
  coverage. Each is independently consumable by signal-watch (additive read), so they can land in any order.
- **Relation to existing briefs:** this supersedes the open §12-signal asks of
  `substrate-determination-signals-PLAN-BRIEF.md` for the north-star-evidence subset; the open-reference-data fork
  ([`substrate-open-reference-data-fork-PLAN-BRIEF.md`](substrate-open-reference-data-fork-PLAN-BRIEF.md)) is where
  the reference layers (#1, #4) get real-shaped anchors. Out of scope: any determination/verdict generation; any
  oracle leak; the matched-pair *device* (an authoring flourish, not a quality requirement — see the build-order doc).
