# true_entities Scorer Contract — measure resolution on synthetic ground truth, never on production

> **Status: DESIGN / contract (Phase 74).** Companion-only — governs `scripts/resolution_scorer.py` and the
> sibling's `true_entities` emission. The one place the program's "no ground truth" epistemology gets a
> *clean* validation: on synthetic data the latent identity is known, so resolution correctness is
> measurable; on real data it is not. Companion: [resolution-link-schema](resolution-link-schema.md) ·
> [identity-grade-grammar](identity-grade-grammar.md).

Entity resolution under no ground truth feeds a frozen filing decision: a wrong merge produces a
confident-but-wrong file/clear. "Is observation o1 = o57 the same party at grade `strong`?" is, on real data,
the same unverifiable judgment as the disposition itself. The synthetic substrate is the one environment
where the latent answer exists (it generated the parties), so it is where resolution correctness is validated
before the abstain-discipline is trusted on real data.

## What the scorer measures

The scorer compares the **resolver's output clustering** (which observations the deterministic linkage tied
into the same `persistent_entity_id`) against the **ground-truth clustering** (`true_entities` — the latent
identity the synthetic generator knows). Standard cluster-comparison metrics (the in-family reference is the
substrate's own `test_resolution_lift.py`):

- **Pairwise precision / recall** — over all pairs of observations, did the resolver put same-entity pairs
  together (recall) without putting different-entity pairs together (precision)? In this domain a false merge
  is far costlier than a missed one — precision is the load-bearing number.
- **Cluster F1 / B-cubed** — per-observation precision/recall averaged, robust to cluster-size skew.

Every reported number is qualified: **"measured on synthetic clusters; production has no ground truth."**

## The firewall — the resolver never sees the answer (enforced at the schema boundary)

The synthetic ground-truth cluster id is the perfect join key and the perfect way to cheat. The firewall is
**structural, not by convention**:

- The **resolver-input surface physically omits** any ground-truth cluster field. The resolver sees only
  *observable* presented attributes (name, email, phone, address, identifiers) — never `true_entity_id` or
  any field derived from it.
- The cluster id lives **only** in the scorer's evaluation-only channel (a separate `true_entities` table the
  resolver never reads).
- A **contract test fails the build** if any resolver-input field is the cluster id **or a surrogate
  1:1-correlated with cluster identity** (e.g. a per-cluster synthetic ref). Renaming the cluster field does
  **not** pass — the test checks correlation with the partition, not the field name.

## Tuning honesty

Tuning resolver thresholds against the hidden clusters indirectly consumes the labels. Therefore:

- Resolver-quality numbers are **never** presented as production-trustworthy — they validate the *mechanism*,
  not the production model. Synthetic confusability is confusable *by construction* along the dimensions the
  generator authored; production confusability includes dimensions nobody authored (that is why real
  false-clears happen).
- The only **production-reportable** signals are the **confidence-grade distribution** (how much of the
  linkage is `strong` vs `weak` vs `reject`) and the **human-adjudication rate** — never an accuracy number.
- On real data, where truth is gone, the discipline is **abstain-band → Class-J**: an uncertain link routes
  to human adjudication, never auto-merges (*unknown over wrong* — see the
  [confidence contract](confidence-as-provenance-contract.md) §Deferred).

## The thin proof in this repo

This phase authors a **minimal** scorer over a tiny synthetic `true_entities` for the casefile entities
(`scripts/resolution_scorer.py --selftest`): it confirms the deterministic email/phone linkage recovers the
authored clusters (e.g. the two James Calder observations resolve together; the John Calderon / Jon A.
Calderón name-only pair does **not** merge) and that the resolver-input firewall holds. The full scorer over
the substrate's `true_entities.parquet` is the
[sibling's job](substrate-graded-counterparty-identifiers-PLAN-BRIEF.md) — this proves the contract runs
before handoff.
