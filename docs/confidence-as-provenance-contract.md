# Confidence-as-Provenance Contract — link → entity fact → disposition

> **Status: DESIGN / contract (Phase 74).** Companion-only. Governs how the identity grade flows from a
> [resolution link](resolution-link-schema.md) through an entity-resident fact to the analyst-visible
> disposition view — **without ever being laundered into a fact**, and **without ever touching the
> byte-frozen filing engine**. Companion: [identity-grade-grammar](identity-grade-grammar.md).

The grade (see the [grade grammar](identity-grade-grammar.md)) is carried as **provenance** all the way from
the resolution link, through the entity-resident fact, to the analyst-visible disposition view. It is never
collapsed into a bare confident fact.

## The frozen-boolean problem — exclude, don't down-weight

The filing engine (`evidence_requirements.evaluate_sufficiency`) is a **boolean** gate with a byte-frozen
determination/file bar (the "A1 guard"). A boolean threshold **cannot express** "but the identity link is
weak." Therefore low-grade inherited evidence must be **excluded, not down-weighted**:

- An evidence atom an investigator *reads* from the file — e.g. `ML-A4`, the network / beneficial-ownership
  leg, read from a `resolution_edge` — is asserted to the engine (`present_atoms(..., read=[...])`) **only if
  the link that supplies it is graded `strong` or `weak`**. A `reject`/unknown-grade link contributes nothing.
- The grade-gated view is computed **before** `evaluate_sufficiency` is called; the engine itself is never
  modified and never sees a grade.

## The per-decision manifest (inspectability)

Every filing decision emits an **inspectable manifest** listing each candidate evidence atom as **admitted**
or **quarantined-by-low-grade**, with the link and grade that supplied it. The file/clear is auditable down
to the link behind each leg. This is the artifact that makes the contract inspectable rather than an implicit
filter — a validator can read *why* an atom was or was not counted.

## Priors are provenance, never a signal (the self-confirming-loop guard)

Accumulated prior dispositions ("previously cleared", "prior STR") enter the workbench **only** as
analyst-visible context. They are **never** read by the boolean filing engine — otherwise a past clear makes
the next alert more likely to clear, and the store becomes a poison vector (the §12 "history is evidence,
never ground truth" trap with a persistence engine behind it).

**The invariant (regression-tested):** *injecting a prior `cleared` disposition produces a byte-identical
file/clear verdict for a fixed evidence set.* `evaluate_sufficiency` is never passed a prior and is never
modified; confidence and priors ride a **separate read path** around it. This mirrors the Phase-73
affirmative-clear discipline (the clear path is additive; the file bar is byte-unchanged).

## Graph confidence composes weakest-link

A multi-hop chain (e.g. an ownership path) takes the **minimum** grade along it — "this control chain's
weakest resolution is `weak`" — never a multiplied pseudo-probability that invents precision the data does
not carry. *Unknown over wrong.*

---

## Bitemporality, staleness, and what is deferred

**Two clocks, two 1D lenses (subtract the cross-product).** The spine carries both *valid-time* (when we
believe a link held) and *decision-time* (when we recorded it). Consumers pick **one** lens — never the
2D (past-resolution × past-data) cross-product:

- **Production disposition** — *decision-time frozen.* A filed/cleared decision stands on the resolution
  **in force when it was made**; a later merge/split does not silently rewrite yesterday's calls.
- **Analytics / impact** — *current-resolution recompute.* Re-run history under today's resolution to see
  what changed, without having destroyed anything.

**Stale-prior guard (event-driven, not clock-old).** A reused prior disposition carries the
`resolution_version` it was decided under. Staleness is **event-driven** (pKYC): if the entity's identity
changed since (a merge/split bumped its `resolution_version`), the prior is surfaced as **re-decision
required** and not trusted silently — the prior may have been about a party that is now two. A prior is only
validly reusable while the entity identity it was attached to is stable.

**Deferred as governed enhancements (named here, not built this phase):**

- **Probabilistic resolution (Splink-class):** a match *probability* where no strong identifier exists. Design
  rule: above a high threshold auto-links; an **uncertain band routes to human adjudication** (it does not
  silently merge); below the band, nothing. The uncertain band is a Class-J queue — *unknown over wrong.*
- **The merge-adjudication Class-J console:** a human loop over probabilistic merges/splits. A merge is itself
  a Class-J disposition; it arrives *with* probabilistic resolution, not before it (deterministic-only linkage
  has nothing probabilistic to adjudicate). The reversible-edge data model exists from day one; the console
  arrives with the resolution dial.
- **Graph analytics (Kuzu-class):** multi-hop "who ultimately controls this" over the entity layer — a
  *projection* of the resolution layer, never a second source of truth (rebuildable from the spine).
- **The medallion / DuckLake / 2D time-travel:** the target storage architecture for the substrate/program
  pillar, out of scope here.

The thin deterministic slice (this phase) is the spine + the grammar + this contract. Everything above is a
layer *on* it, behind the same link contract.
