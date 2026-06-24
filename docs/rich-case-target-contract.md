# Rich-case target contract — what the pillars build toward (Phase 73 handoff)

**Status:** the inverted-dependency handoff. signal-watch AUTHORED the north-star investigation case
(`data/casefile/case.json` + `data/casefile/schema.md`, Phase 73); aml-substrate + aml-casework now build
toward it. This doc is the contract — grounded in a code-level verification of the live siblings
(aml-substrate `f15c241`, aml-casework `bf15535`) on 2026-06-23, **not** the spec sketch's assumptions.

**The authoritative target is `data/casefile/case.json`** — the concrete shape to emit toward. The
acceptance test for the whole program: signal-watch's `serve_workbench.casefile_*` path consumes a
**substrate-emitted** bundle (not an authored `case.json`) and the live engine still computes
Northgate→determination/file and Lakeshore→cleared, with the network/identity/ER read from REAL emission.

**The scope boundary (load-bearing — do NOT push these into substrate):** the **caution-list**, the
**prior-STR register**, and the **determination / mitigation / affirmative-clear verdict** stay
signal-watch's authored + computed layer (`reference{}` in case.json + `evidence_requirements.py`). They are
context an INVESTIGATOR brings, not facts a transaction monitor emits. Substrate's job is the
**identity + network** layer; casework's job is to **verify + sign/clear** over it.

---

## Pillar 1 — aml-substrate: emit the identity/network layer (the chosen next phase)

The substrate emits the detection core today (C2/C3/C8/C14 alerts, KYC, ownership edges with pct). The gap
is that the counterparties are **bare codes**, the BO graph carries **no names**, and inbound legs are
**not entity-resolved**. Four items, each with the target shape, the verified current state, and acceptance:

### SUB-1 — channel-aware counterparty IDENTITY on the transaction
- **Target** (`case.json` transactions[].counterparty): `{entity_ref, name, email?, phone?, address?, country, observed_at?, role}` — per rail (WIRE→name+address, EMT→email[+phone], AFT→country).
- **Verified state — PARTIAL:** `counterparty_name`/`counterparty_country` fields EXIST (`schema/transaction.py:36-37`) but `counterparty_name` is **STRIPPED at emission** (`monitor/detectors/views.py` TxnView omits it) and `counterparty_country` is **never populated** (0 assignments in `gen/activity.py`); no email/phone/address fields exist on the txn. **Effort: M.**
- **Acceptance:** an emitted txn carries a named, optionally-contactable counterparty + a populated country; the fields survive TxnView into the evidence bundle.

### SUB-2 — deliberately SEEDED, strength-tagged shared identifiers
- **Target** (`case.json` resolution_edges + identifiers[].strength): two parties share an email/phone (`strength:"strong"`) or an address (`strength:"weak"`), so entity resolution is exact-on-identifier.
- **Verified state — PARTIAL:** SHARES_EMAIL/PHONE edges + an `apply_identity_linkage()` injector EXIST (`gen/identity.py`) but the edges are **untagged** (no strength on `schema/graph.py` RelationshipEdge) and the injector is **flag-off by default**. **Effort: M.**
- **Acceptance:** the emitted population seeds ≥1 strong (email/phone) cross-party identifier collision, strength-tagged; address collisions tagged weak (never strong — the >90 pct-FP discipline).

### SUB-3 — a NAMED multi-hop BO/control graph
- **Target** (`case.json` related_parties[].display_name + ownership_edges multi-hop): nodes carry **real names**; the chain (subject ← owner ← …) is traversable by name.
- **Verified state — PARTIAL:** BENEFICIAL_OWNER/DIRECTOR_OF + `ownership_pct` emitted, multi-hop possible, full vocab slots defined — but **only bare `party_id`s** survive (`PartyGraphView`, `views.py:188-209`); no `display_name`. **Effort: M.**
- **Acceptance:** the emitted BO graph carries display names + the full ownership vocab; a multi-hop chain renders by name (the workbench's `boGraphHTML`/`scBOGraph` reads `display_name`, not `party_id`).

### SUB-4 — named source-party identity on fan-in (inbound) legs
- **Target** (`case.json`: an inbound credit's counterparty resolves to a named party record, e.g. "Vesna Maric, v.maric@…"): the originator on a credit leg is a resolvable entity, not a code.
- **Verified state — GAP:** txns carry only `counterparty_ref` codes; counterparties are drawn from a per-account local pool with **no cross-account party resolution** (`gen/activity.py:253-256`). **Effort: L** (a second-pass entity-resolution layer, or re-draw counterparties from the shared party pool).
- **Acceptance:** an inbound leg's counterparty carries an `entity_ref` to a party record; signal-watch can read a named inbound source (the prior-STR match grounds against a real emitted party, not an authored one).

> **Note (not a substrate item):** SUB-5 (KYC naics/nature_of_business/SoF) is already **HAVE** — no work.
> SUB-6 (cross-border) is a substrate capability gap but **not** a CASE-A requirement (a Canadian
> trafficking case stays domestic). SUB-7 (caution-list / prior-STR register) + SUB-8 (mitigation) are
> **signal-watch authored scope** per the boundary above — do NOT emit them from substrate.

**Substrate phase shape (suggested, measure-first per the sibling's own discipline):** SUB-1 + SUB-3 are
the cheapest, highest-visibility wins (named counterparties + a named BO graph — the demo's two graphs go
from codes to names against REAL emission). SUB-2 + SUB-4 (entity resolution) are the deeper lift and gate
the ER graph. Probe first: emit a slice, run it through signal-watch's `casefile_*` consume, and measure
how much of the rich render survives on REAL data.

---

## Pillar 2 — aml-casework: verify + sign/CLEAR over it (the deferred sibling)

Casework can already **sign** the rich case to a `file` disposition (both cases carry transactions; alerts
ground via txn-leaf or the C14 party-leaf). The load-bearing gap is that it **cannot CLEAR**:

- **CW-4 (the key one) — GAP:** the disposition vocab is `{blocked, needs_more_info, signed}` + `{file, both_defensible}` (`signoff.py:32,38`, immutable since Phase 2) — **no `cleared` path**. Hand it Lakeshore and it signs *file*, not a documented dismissal. signal-watch **proved the exact shape** this phase (`evidence_requirements.py:385` — the additive branch: mechanism + 0 legs + mitigation_established + no predicate → cleared, the file bar byte-unchanged). Casework's own current-state already names this a **Phase-15 candidate**. **Effort: L** (disposition enum + an `affirmative_clear` block + a sufficiency eval in signoff, AFTER the verifier chain). Adopt the verified signal-watch design.
- **CW-2 (entity-resolution verification) — GAP** (L) · **CW-1 (counterparty-identity grounding) — PARTIAL** (M) · **CW-5 (named predicate in the FINTRAC narrative) — PARTIAL** (M) · **CW-3 (sign txn-less) — HAVE** (the Phase-72 no-transactions contract still fails purely txn-less party-leaf bundles; both rich cases carry txns, so unaffected).

CW-1/CW-2 depend on SUB-1/SUB-4 landing first (you can't verify identity/ER that isn't emitted). **CW-4 is
independent** — it can be exercised today via the existing subprocess handoff (signal-watch hands casework
the authored Lakeshore bundle), so it's the smallest defensible cross-pillar win when casework's turn comes.

---

## The end-to-end acceptance (when both pillars land)

substrate emits a bundle with named, resolvable, identity-rich counterparties + a named BO graph →
signal-watch's `casefile_*` path reads it (the authored `reference{}` caution-list/prior-STR stays
signal-watch's) and the live engine computes file vs cleared → casework verifies the identity/ER grounds
and signs *or clears* (CW-4) the result. The rich case stops being authored and becomes **emitted,
resolved, and verifier-defensible end-to-end** — the LFCM grounding chain, made real.
