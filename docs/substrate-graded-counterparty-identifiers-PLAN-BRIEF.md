# PLAN BRIEF — aml-substrate: emit GRADED counterparty identifiers

> **Status: cross-pillar PLAN BRIEF (Phase 74, signal-watch).** A handoff for the **aml-substrate**
> sibling to build on its own lifecycle — *no code lands in aml-substrate from here* (the Phase-55–58 / 66
> pattern: signal-watch authors the contract; the sibling implements + measures it). Synthetic /
> illustrative; **no catch-rate, lift, or precision number is asserted.** This brief EXTENDS the Phase-73
> [rich-case target contract](rich-case-target-contract.md) (SUB-2 seeded strength-tagged identifiers,
> SUB-4 named source-party ER) and keys its emission shape to the just-authored
> [identity-grade-grammar](identity-grade-grammar.md), [resolution-link-schema](resolution-link-schema.md),
> and [true-entities-scorer-contract](true-entities-scorer-contract.md).
>
> **Verified sibling pin: `a3fb02b4efe5ffb564c88cf3fd4931ba672ab63a` ("close Phase 27", branch `main`),
> code-verified 2026-06-25.**
>
> **DRIFT NOTE (read first).** The Phase-73 contract was grounded against substrate `f15c241` and assumed
> the identity hooks were *inert* and the SHARES_* injector *flag-off only*. At the verified HEAD the
> substrate is **substantially further along** than that contract assumed — this brief re-grounds to the
> live shape:
> - `gen/identity.py` is a **complete Phase-5 identity-linkage subsystem**, not inert hooks:
>   `apply_identity_linkage()` populates `phone`/`email`/`device_id` on `Person` **and** `Organization`
>   (`schema/party.py:78-80, 108-110`), injects `SHARES_EMAIL` / `SHARES_PHONE` / `SHARES_DEVICE` /
>   `SHARES_ADDRESS` edges, and returns hidden `true_entities` clusters. It is driven by the **`--identity`
>   CLI flag** (`cli.py:109`), which writes `<out>/identity/`.
> - A **ground-truth-blind reference resolver already exists** (`resolve/resolver.py`) — it reads only the
>   observable projection (name/phone/email/device_id, NO cluster id) and resolves on a shared **strong**
>   identifier (phone/email/device), explicitly **not** address (co-residents share an address).
> - A **scorer already exists** (`resolve/measure.py`) — the *sole* reader of `true_entities`, reporting
>   pairwise **and** B-cubed precision/recall/F1 against two baselines (all-singletons,
>   connected-components-on-SHARES). The [scorer contract](true-entities-scorer-contract.md)'s "full scorer
>   over the substrate" is therefore **mostly already built** — this brief's scoring ask is a thin
>   *extension*, not a green-field.
>
> What is genuinely missing is the **counterparty leg** (the identity subsystem lives on the *party*
> graph, not on the *transaction* counterparties the consumer reads) and the **`strength` tag** on the
> shared-identifier edges. That gap is this brief.

---

## Objective

Make a counterparty an **identity**, not a code, and tag every shared identifier with the grade vocabulary
the consumer's deterministic linkage runs on — so signal-watch's entity spine resolves cross-record
counterparties **record-sourced**, never by re-inferring strength from a bare string.

Concretely: emit, per transaction counterparty leg, the **observable identifiers** (email / phone /
address / account / client number) the rail carries, each tagged with a `strength` drawn from the
[grade grammar](identity-grade-grammar.md)'s closed vocabulary; populate the already-built identity hooks
**onto the counterparty surface** (not only the subject-party graph); and tag the existing `SHARES_*` /
beneficial-ownership edges with `strength`. The consumer then links exact-on-identifier and grades the
link deterministically — never fuzzy-on-name.

**Why this fixes the artifact (the generator dial).** Today counterparties on a transaction leg carry
**name-only** (`counterparty_ref`, `counterparty_name`, `counterparty_country`; `TxnView` strips even the
name — `views.py:34-46`). Name-only means **every** cross-record counterparty link would be a fuzzy
name match — on the grade grammar that is grade `reject`, *excluded*, so ~85% of would-be links never
resolve and the entity spine looks empty. Seeding strength-tagged identifiers turns the **strong / fuzzy
ratio into a generation parameter**: the share of links that resolve `strong` (exact identifier) vs sit at
`weak` (address-only) vs `reject` (name-only) becomes a dial the generator sets honestly, instead of an
artifact of which fields happen to be populated.

## The exact emission shape (keyed to the grade vocabulary)

The closed vocabulary the consumer grades against (verbatim from
[identity-grade-grammar](identity-grade-grammar.md) §Vocabulary):

```
GRADES        = ("strong", "weak", "reject")      # ordinal, weakest-first: reject < weak < strong
STRONG_KINDS  = ("email", "phone", "account_number", "client_number", "id_registration", "wallet", "domain")
WEAK_KINDS    = ("address",)
```

### 1. Identifiers on the counterparty leg (extends SUB-1 / SUB-4)

Per transaction, the counterparty carries an `identifiers[]` list, each entry:

```jsonc
{
  "kind":  "email",                       // one of STRONG_KINDS ∪ WEAK_KINDS
  "value": "jcaldermgmt@swiftmail.test",  // the RAW presented value (consumer normalizes)
  "strength": "strong"                    // == "strong" iff kind ∈ STRONG_KINDS; "weak" iff kind ∈ WEAK_KINDS
}
```

- `strength` is a **deterministic function of `kind`** against the grammar's STRONG_KINDS / WEAK_KINDS —
  the generator must not author it independently (an `email` is always `strong`; an `address` is always
  `weak`). Emit it anyway so the consumer is record-sourced and a contract test can assert
  `strength == grade_of(kind)`.
- **Name is never an identifier.** `counterparty_name` stays a separate field; it is an *observation that
  triggers a candidate link*, graded `reject` until an identifier corroborates (grammar §"name is
  neither"). Do **not** put name in `identifiers[]`.
- **Rail-aware population** (extends SUB-1): WIRE → name + address (weak) [+ account_number, strong];
  EMT → email (strong) [+ phone, strong]; AFT → country + account_number (strong). The rail decides which
  identifiers are observable — that *is* the realistic noise model.
- **Surface fix (load-bearing):** the counterparty identity must **survive the view layer** into the
  evidence bundle. `TxnView` (`views.py:34-46`) currently strips `counterparty_name` and carries no
  identifiers; the projection must carry `counterparty_name` + `identifiers[]` (label-blind — these are
  observable presented attributes, never a ground-truth field).

### 2. Populate the identity hooks onto the counterparty surface

`gen/identity.py` already mints `phone`/`email`/`device_id` and the `SHARES_*` graph **on the party
population**. The gap is that a *transaction counterparty* on a fan-in leg is not yet one of those resolved
parties (SUB-4: counterparties are drawn from a per-account local pool, no cross-account resolution). Close
it so an inbound credit's originator carries an `entity_ref` to a party record that *has* identifiers — the
same `email`/`phone`/`device_id` the identity layer already populates — so two records crediting the same
source resolve to one entity exact-on-identifier.

### 3. `strength` on the SHARES_* and beneficial-ownership edges

The existing `SHARES_EMAIL` / `SHARES_PHONE` / `SHARES_DEVICE` / `SHARES_ADDRESS` edges (and the
`BENEFICIAL_OWNER` / `DIRECTOR_OF` ownership edges) must carry the grade so a multi-hop chain composes
**weakest-link** (confidence-as-provenance §"Graph confidence composes weakest-link"):

```jsonc
{ "label": "SHARES_EMAIL",   "strength": "strong" }   // email/phone/device share → strong
{ "label": "SHARES_ADDRESS", "strength": "weak" }     // address share → weak (NEVER strong)
```

> **Schema note for the implementer:** `RelationshipEdge.attrs` is typed `dict[str, int]`
> (`schema/graph.py:22`). Carrying a string `strength` needs the attrs type widened to
> `dict[str, int | str]` (or a dedicated `strength: str | None` field). A small, additive schema move —
> flag it in the substrate phase plan.

**The >90%-FP discipline (do not violate):** address collisions are tagged `weak`, **never** `strong`.
Co-residents share an address; an address match corroborates but never resolves on its own. The reference
resolver already encodes exactly this (`resolver.py:70` — "a shared STRONG identifier (phone/email/device)
— NOT address"). The `strength` tag must mirror that boundary.

### 4. Deliberately seed ≥1 strong cross-party collision (SUB-2 acceptance)

The emitted population must seed at least one **strong** (email/phone) cross-party identifier collision,
strength-tagged, plus address collisions tagged `weak` — so the consumer's resolution has a real `strong`
link to recover and a real `weak`-only pair to flag-but-not-merge. The identity subsystem's two-flavor
injection (household co-residents share address+device; synthetic-identity fragments share one observable
attribute) already produces these — this ask is to (a) **strength-tag** them and (b) **surface them on the
counterparty leg**, not only the party graph.

## The firewall — never leak the cluster id onto the resolver-input surface

Hard constraint, cite the [scorer contract](true-entities-scorer-contract.md) §Firewall: the synthetic
ground-truth cluster id (`true_entities[].cluster_id`, `gen/identity.py:155`) is the perfect cheat and
**must never appear on the resolver-input surface**. The substrate already enforces this structurally — the
reference resolver reads only the observable projection (`resolver.py:36` — "no cluster id, no ground
truth") and `measure.py` is the *sole* reader of `true_entities`. The emission this brief adds must hold
the same line:

- `identifiers[]`, `counterparty_name`, the `strength` tags, and the `entity_ref` (SUB-4) are
  **observable** presented attributes — emit them freely.
- `cluster_id` / `true_entity_id` / **any field 1:1-correlated with the latent partition** (a per-cluster
  synthetic ref) stays on the **evaluation-only `true_entities` channel** the consumer's resolver never
  reads. A contract test must fail the build if any resolver-input field correlates with the cluster
  partition (the test checks **correlation, not field name** — renaming does not pass).

## Sibling-executed framing

Built in **aml-substrate**, on its own lifecycle, **measure-first** (the sibling's own discipline): emit a
slice, run it through signal-watch's `serve_workbench.casefile_*` consume, and measure how much of the rich
render (named counterparties, a resolving `strong` link, a `weak`-flagged pair) survives on REAL emitted
data before scaling. The scorer is already present (`resolve/measure.py`) — extend it to score the
**counterparty-leg** resolution against `true_entities`, reporting only the
[scorer contract](true-entities-scorer-contract.md)'s production-reportable signals: the **confidence-grade
distribution** (strong / weak / reject share) and the **human-adjudication rate** — never an accuracy
number presented as production-trustworthy.

## Why this matters to the consumer (the entity spine tie-back)

signal-watch's [resolution-link schema](resolution-link-schema.md) answers "do these two records share a
counterparty?" through **observation → resolution-link → `persistent_entity_id`**, and the link's `grade`
is the grade of the **strongest shared identifier in its `basis[]`**. With name-only counterparties the
`basis[]` is always empty → every link is `reject` → the spine resolves nothing and the
Northgate-files / Lakeshore-clears decisioning lever (which rests on a *resolved, persisted* network +
source-of-funds, not the transaction stream) has no spine to stand on. Strength-tagged identifiers on the
counterparty leg are the record-sourced `basis[]` that lets the consumer's deterministic linkage grade a
link **auditable, not asserted** — and turns the rich case from *authored* into *emitted, resolved,
verifier-defensible end-to-end*.

---

## /dev-plan kickoff (paste into the aml-substrate session's `/dev-plan`)

**Round 1** (no cross-pillar dependency — the standards are authored) · **Size: medium** (counterparty
identifiers + populate hooks are medium; the `attrs` widen is small; tightly coupled — one phase) ·
**Pin: `a3fb02b`** · **Unblocks:** the casework graded-resolution consume (Round 2) + the consumer's
real counterparty resolution.

> **Objective.** Make a transaction counterparty an *identity*: emit `identifiers[]` (email/phone/address/
> account + `strength`) on the counterparty leg, propagate the already-built `gen/identity.py` hooks +
> `SHARES_*` graph onto the counterparty surface, and tag `SHARES_*` / beneficial-ownership edges with
> `strength` — so signal-watch's spine resolves counterparties record-sourced, exact-on-identifier.
>
> **Scope (this repo):** `schema/transaction.py` (counterparty `identifiers[]`) · `schema/graph.py`
> (`RelationshipEdge.attrs` → `dict[str,int|str]`, additive) · `gen/activity.py` + `gen/flows.py`
> (rail-aware identifier population) · `gen/identity.py` (propagate hooks onto counterparties) ·
> `monitor/views.py` (`TxnView` carries `counterparty_name` + `identifiers[]`, label-blind) ·
> `resolve/measure.py` (extend to score counterparty-leg resolution) · tests.
> **Out of scope:** probabilistic ER; the consumer wiring (signal-watch re-vendors after).
>
> **Load-bearing assumptions (surface at the direction gate):** (A) the counterparty leg can carry
> `identifiers[]` through `TxnView` **without leaking a label** field; (B) widening `attrs` to
> `dict[str,int|str]` is additive — no downstream type break; (C) `strength == grade_of(kind)`
> deterministically (the generator never authors strength independently); (D) the cluster-id firewall
> holds on the new counterparty surface.
>
> **Exit criteria (testable):** ≥1 **strong** cross-party identifier collision seeded, strength-tagged,
> **surfaced on a counterparty leg** + address collisions tagged `weak`; a contract test asserts
> `strength == grade_of(kind)` AND **no resolver-input field correlates with the cluster partition**
> (correlation, not field name); `resolve/measure.py` scores counterparty-leg resolution and reports only
> the grade-distribution + human-adjudication rate, qualified "synthetic clusters; production has no
> ground truth."
>
> **The guard that must not break:** **name is never an identifier** (stays a separate field, grade
> `reject`); **address is never `strong`** (co-residents share an address); the **cluster id never reaches
> the resolver-input surface**.
