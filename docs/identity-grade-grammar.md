# Identity-Grade Grammar — ordinal, fails closed

> **Status: DESIGN / contract (Phase 74).** Companion-only. The shared identity-grade vocabulary used by
> `scripts/entity_spine.py`, the [resolution-link schema](resolution-link-schema.md), the
> [confidence-as-provenance contract](confidence-as-provenance-contract.md), and the sibling briefs.

Confidence in a resolution link is an **ordinal grade**, not a float. Loosening match rules *without*
identifier layering pushes false positives over 90% (the analyst-fatigue tsunami); the grammar is the
deterministic fix — name similarity is a *weak observation that triggers review*, never a resolving link.

## The grades

| grade | criterion | example (from the committed casefile) | admitted to a filing decision? |
|---|---|---|---|
| `strong` | exact match on a normalized **strong identifier** — email, phone, government id, account number, client number | shared `jcaldermgmt@swiftmail.test` (James Calder across institutions) | **yes** |
| `weak` | match on a **weak identifier only** (address, partial) — corroborating, never resolving on its own | shared address `44hollowaycourtbramptononca` | yes, **flagged weak** |
| `reject` | **name-only** (no shared identifier) — *not a link* | "John Calderon" vs watchlisted "Jon A. Calderón" | **no — excluded** |

## Strong vs weak identifier kinds

- **strong:** `email`, `phone`, `account_number`, `client_number`, government/tax id, registration number,
  `wallet`, `domain` — any identifier that, matched exactly on its normalized value, identifies a party.
- **weak:** `address` and other shared-context attributes — many parties share an address; a match
  corroborates but does not resolve.
- **name** is neither: it is an observation that may *trigger* a candidate link, graded `reject` until a
  strong/weak identifier corroborates it.

## Rules

- `basis[]` records exactly which identifier(s) drove the grade (`[{kind, normalized_value}]`), so a grade is
  **auditable, not asserted**.
- **Fail-closed.** A missing/unknown grade, or a link with an **empty `basis[]`** (the proxy for "unknown"),
  is treated as the **weakest** (`reject`) and its inherited evidence is **excluded** from any filing
  decision. Unknown never defaults to "trusted."
- **Resolution is exact-on-identifier, never fuzzy-on-name.** The casefile encodes this directly: the
  cross-institution James Calder link resolves on a shared `strong` email; the common-name John Calderon /
  Jon A. Calderón pair is `excluded` on the absence of any shared identifier (a different full name and a
  different email).
- A link's grade is the grade of the **strongest** shared identifier in its `basis[]` (one strong identifier
  resolves; weak-only stays `weak`; none stays `reject`).
- Confidence is **deterministic linkage-strength** derived from this grammar — never a model-emitted or
  probabilistic match score (a model confidence is a fabricated-shaped number; `news_store` keeps its
  `confidence` column RESERVED for this reason). A probabilistic score is admissible *only* when measured
  against ground truth — see the [scorer contract](true-entities-scorer-contract.md).

## Vocabulary (the closed set siblings emit against)

```
GRADES        = ("strong", "weak", "reject")      # ordinal, weakest-first: reject < weak < strong
STRONG_KINDS  = ("email", "phone", "account_number", "client_number", "id_registration", "wallet", "domain")
WEAK_KINDS    = ("address",)
```

A sibling emitting identifiers (see the
[graded-counterparty-identifiers brief](substrate-graded-counterparty-identifiers-PLAN-BRIEF.md)) tags each
with a `strength` drawn from this vocabulary so the consumer's deterministic linkage is record-sourced, not
inferred.
