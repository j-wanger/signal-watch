# Resolution-Link Schema — the append-only, bitemporal identity layer

> **Status: DESIGN / contract (Phase 74).** Companion-only — governs `scripts/entity_spine.py`; `build.py`
> imports none of it; the 8 ship dists stay byte-frozen. Siblings implement against the
> [handoff briefs](substrate-graded-counterparty-identifiers-PLAN-BRIEF.md). Synthetic/illustrative; no
> catch-rate / lift number. Companion docs: [identity-grade-grammar](identity-grade-grammar.md) ·
> [confidence-as-provenance-contract](confidence-as-provenance-contract.md) ·
> [true-entities-scorer-contract](true-entities-scorer-contract.md).

The persistent entity intelligence spine exists because the decisioning lever — separating two cases that
fire the **same** grounded signals but deserve **opposite** outcomes (the committed Northgate-files /
Lakeshore-clears pair) — rests on evidence that lives in a *resolved, persisted* entity (its network and
source of funds), not the transaction stream. The spine is where that evidence accumulates so an
investigation is *memoryful*, not re-gathered cold each alert (FATF R.10 ongoing CDD; FINTRAC ongoing
monitoring; "perpetual / event-driven KYC" is the industry name for the model).

## The three-layer model (resolution is its own layer)

Identity is **not** a join key you discover once. It is a *derived, revisable, graded* assertion. The spine
separates three things that are usually smeared together — and keeping them separate is the whole contract:

1. **Observations** — raw presented attributes, immutable, provenance-linked. "These bytes (name, email,
   phone, address, account, identifier) appeared in this record, at this time." An observation never asserts
   who anyone *is*.
2. **Resolution links** — the append-only, bitemporal mapping from observations to a stable internal
   `persistent_entity_id`. "Observation o1 and observation o57 resolve to entity E-000123, at grade `strong`,
   by this method, recorded at this decision-time, believed to hold over this valid-time."
3. **The persistent entity** — keyed by the stable `persistent_entity_id`: the resolved best-view plus all
   entity-resident facts (KYC, source-of-funds, adverse media, beneficial ownership) **and the decision
   history** (prior dispositions + their grounding chains). This is the spine.

"Do these two records share a counterparty?" is answered by **observation → resolution-link →
`persistent_entity_id`**: they share a counterparty *iff* their observations resolve to the same entity id at
the current resolution version. The indirection is not overhead — it *is* the entity intelligence (the
difference between "same name string" and "we decided, defensibly and revisably, these are the same party").

Exact-normalized **name** is demoted from "the entity key" to **one deterministic linkage rule** (a
`reject`-grade one — see the [grade grammar](identity-grade-grammar.md)) feeding the link layer. This is the
key departure from the news-pillar anchor store (`news_store.py`), which keys identity on the normalized name
itself; the spine is a **new module**, leaving `news_store` byte-untouched.

## The link schema

| field | meaning |
|---|---|
| `link_id` | unique id of this link assertion |
| `entity_id` | the stable internal `persistent_entity_id` the observation resolves to |
| `observation_ref` | the observation (record + presented attribute) this link binds |
| `method` | `deterministic-identifier` \| `deterministic-name` \| (deferred: `probabilistic`, `human-adjudicated`) |
| `grade` | the ordinal identity grade: `strong` \| `weak` \| `reject` (see the grade grammar) |
| `basis[]` | the identifier(s) that drove the grade — `[{kind, normalized_value}]`; empty ⇒ name-only |
| `valid_time_start` / `valid_time_end` | the period we believe the link held (NULL end = open) |
| `decision_time` | when we *recorded* this assertion (advances on every new row) |
| `resolution_version` | a monotonic counter on the entity, bumped on any merge/split touching it |
| `supersedes` | the `link_id` this row replaces (NULL for a first assertion) |
| `status` | `active` \| `superseded` \| `retracted` |

**Append-only, supersede-not-overwrite.** A correction is a new row that supersedes the old; the old row is
never mutated or deleted (the audit trail is the point). A **merge** is an `active` link; an **un-merge /
split** is a `retracted` row superseding the merge.

**Reversible split with cascade-invalidation (load-bearing).** When a link is retracted (a wrong merge
discovered), every disposition whose grounding chain crossed the retracted edge is cascade-marked
`re-decision required` — *not* deleted (audit preserved). A disposition must never be reachable through a
retracted edge. This is what stops a wrong merge from silently leaving its filings/clearings standing.

**Conflicting values are both kept.** When two records credibly tied to one entity disagree (two DOBs, two
addresses), the spine keeps both as separate observation rows with provenance — never last-write-wins, never
silent reconciliation (the `news_store` "both-kept" discipline carried forward).

Bitemporality (the two clocks), the stale-prior guard, and the deferred probabilistic/graph layers are
specified in the [confidence-as-provenance contract](confidence-as-provenance-contract.md) §Bitemporality.
