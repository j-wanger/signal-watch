# PLAN BRIEF — aml-substrate: emit slice-aligned `true_entities` (the merge console's real-data oracle)

> **Status: cross-pillar PLAN BRIEF (Phase 76, signal-watch).** A handoff for the **aml-substrate**
> sibling to build on its own lifecycle — *no code lands in aml-substrate from here* (the Phase-55–58 / 66 /
> 74–75 pattern: signal-watch authors the contract; the sibling implements + measures it). Synthetic /
> illustrative; **no catch-rate, lift, or precision number is asserted.** This brief keys its emission shape
> to the [true-entities-scorer-contract](true-entities-scorer-contract.md), the
> [identity-grade-grammar](identity-grade-grammar.md), and the
> [resolution-link-schema](resolution-link-schema.md), and is the sibling-side unblocker for the
> **merge-adjudication Class-J console** (`dist/merge/`, Phase 76) — the deferred ER piece named in the
> [graded-counterparty-identifiers brief](substrate-graded-counterparty-identifiers-PLAN-BRIEF.md).
>
> **Verified sibling pin: `fc98b09` ("close Phase 28 — entity-resolution emission", branch `main`),
> code-verified live 2026-06-25** (same HEAD Phase 75 consumed; no drift this session).

---

## Why this brief exists

Phase 76 stood up the **merge-adjudication console** — the human gate over entity-resolution candidate
links. It has TWO case populations:

1. **REAL candidate SHARES (66)** — distinct `entity_ref`s the substrate v0.5 slice asserts `resolved` that
   the spine REFUSED (the controller-cluster / noise-floor over-merge, Phase-75 finding). These are
   **consensus-not-ground-truth**: the console can show the spine's refusal and the human's call, but it
   **cannot show whether the call matched truth** — substrate emits no `true_entities` *with the slice*.
2. **SYNTHETIC scored cases (13)** — from `data/entity-spine/true_entities.json`, where the latent cluster
   is known, so the Reveal SHOWS whether the adjudication matched truth (synthetic-only, qualified).

The console's architectural novelty is that the merge gate is the **one gate with a measurable correctness
oracle**. Today that oracle exists only on the synthetic 13. This brief is the sibling work that extends it
to the real 66 — **without ever letting the resolver see the truth.**

## The seam (what already exists at `fc98b09`)

- `gen/identity.py::apply_identity_linkage()` **already returns hidden `true_entities` clusters** and, under
  the `--identity` CLI flag (`cli.py`), writes `<out>/identity/`. The ground truth is *computed* — it is not
  *exported alongside the curated case slice* the consumer reads.
- A **ground-truth-blind resolver** (`resolve/resolver.py`) and a **B-cubed / pairwise scorer**
  (`resolve/measure.py`, the sole reader of `true_entities`) already exist — the
  [scorer contract](true-entities-scorer-contract.md)'s "full scorer over the substrate" is largely built.
- The consumer reads the per-case **bundles** (`data/workbench/bundles/*.json`: `parties[]`,
  `related_parties[]`, `resolution_edges[]`) curated by `curate_workbench_cases.py`. These carry
  `entity_ref` (the reliable declared identity) but **no `true_entities`** — so the merge console's real
  cases are oracle-less.

**The gap:** the latent clusters exist but are not emitted in a slice-aligned, consumer-readable,
firewall-respecting form keyed on `entity_ref`. **Status: NOT BUILT.**

## EMIT

Emit, alongside the case-slice projection, a SEPARATE **eval-only** `true_entities` artifact mapping each
emitted `entity_ref` to its latent cluster id:

```
identity/true_entities.json   (or .parquet — the consumer reads either)
{
  "contract_version": "0.5",
  "note": "EVAL-ONLY ground-truth identity clusters. NEVER an input to any resolver.",
  "entities": [
    { "entity_ref": "P-0008383", "cluster": "GT-00417" },
    { "entity_ref": "P-0010571", "cluster": "GT-00417" },   // same cluster => genuinely the same person
    { "entity_ref": "P-0018178", "cluster": "GT-00982" },   // distinct cluster => a SHARES collision, not identity
    ...
  ]
}
```

The cluster id is opaque and carries no other information (no 1:1 surrogate of any observable). Coverage:
every `entity_ref` that appears in the emitted slice (parties + related_parties + every `resolution_edges`
endpoint) MUST have a `cluster` entry, so the consumer can score every candidate SHARES pair.

## GROUND — the resolver-input firewall (load-bearing)

The `cluster` field is the latent truth. It must ride a channel **physically separate** from anything a
resolver consumes:

- The cluster id MUST NOT appear in any `parties[]` / `related_parties[]` / `identifiers[]` /
  `resolution_edges[]` field (the resolver-input surface), NOR as any field 1:1-correlated with it
  (renaming `cluster` to a per-cluster `*_ref` does **not** satisfy this — the firewall is a schema
  boundary, not a field name; see [scorer contract](true-entities-scorer-contract.md) §"resolver-input
  firewall" and signal-watch's `resolution_scorer.assert_no_cluster_leak`).
- The truth lives ONLY in `identity/true_entities.json`. The bundles stay byte-shape-compatible — the
  consumer that ignores the eval-only file behaves exactly as today.
- This mirrors signal-watch's own `data/entity-spine/true_entities.json`: the `cluster` is eval-only; the
  resolver runs on `resolver_input()` (name / kind / role / identifiers) and never reads it.

## CONSUME (signal-watch side, when this lands)

`scripts/curate_merge_cases.py` gains an eval-only read of `identity/true_entities.json`:

- For each REAL candidate SHARES pair `(entity_ref_a, entity_ref_b)`, look up both clusters; the latent
  truth is `same_entity = (cluster_a == cluster_b)`.
- Attach an `oracle` block — IDENTICAL in shape to the synthetic cases:
  `{ same_entity, correct_adjudication: same_entity ? "uphold_merge" : "reject_as_shares", qualifier }` —
  flip the real case from `source:"substrate-v0.5-slice", scored:false, oracle:null` to a **scored** case.
- The firewall holds end-to-end: the `cluster` is read ONLY to compute `same_entity` for the post-disposition
  Reveal; it NEVER enters the evidence (`a`/`b`) the human sees, and `validate_merge_cases`'s
  `MERGE_TRUTH_LEAK_KEYS` check stays the build-boundary guard.
- The qualifier softens from "synthetic clusters" to **"substrate-generated synthetic population; ground
  truth from the substrate's identity generator"** — still synthetic, still not production ground truth, but
  now the console scores the REAL 66 too. The honesty split in the Reveal/ledger (consensus vs scored)
  collapses for these cases as they move into the scored set.

Until then, the real 66 stay **consensus-only** and the merge console's scored dimension is the synthetic 13
(the committed state — the honest fallback, never faked).

## Acceptance (sibling-side)

1. `identity/true_entities.json` emitted for the slice population; every emitted `entity_ref` has a `cluster`.
2. The resolver-input firewall holds: no bundle field carries `cluster` or a 1:1 surrogate; the existing
   `resolve/resolver.py` is byte-unchanged (it already never reads it).
3. `resolve/measure.py` scores the slice resolver against the emitted clusters (B-cubed + pairwise; the
   synthetic-only qualifier mandatory on every number) — the in-family precedent already exists.
4. The emission is **additive** — bundles that ignore `identity/` behave exactly as at `fc98b09`.

**Pin: `fc98b09`** · **Unblocks:** scoring the merge console's real candidate SHARES against ground truth
(today synthetic-only). **Out of scope here:** probabilistic / Splink ER, the merge console UI (built,
Phase 76), graph/Kuzu — named in the [confidence-as-provenance contract](confidence-as-provenance-contract.md).
