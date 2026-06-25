# PLAN BRIEF — aml-casework: CONSUME confidence-graded resolution

> **Status: cross-pillar PLAN BRIEF (Phase 74, signal-watch).** A handoff for the **aml-casework** sibling
> to build on its own lifecycle — *no code lands in aml-casework from here* (the Phase-55–58 / 66 pattern:
> signal-watch authors the contract; the sibling implements + measures it). Synthetic / illustrative; **no
> catch-rate, lift, or precision number is asserted.** This brief EXTENDS the Phase-73
> [rich-case target contract](rich-case-target-contract.md) (**CW-2** entity-resolution verification,
> **CW-4** the live cleared-by-mitigation verdict) and keys its consume shape to the just-authored
> [identity-grade-grammar](identity-grade-grammar.md),
> [resolution-link-schema](resolution-link-schema.md), and
> [confidence-as-provenance-contract](confidence-as-provenance-contract.md).
>
> **Verified sibling pin: `cfd989fe9b1dfeef9fb26988a69867561c22a26c` ("close Phase 15 delivery gate",
> branch `feat/phase-1a-deterministic-verifiers`), code-verified 2026-06-25.**
>
> **DRIFT NOTE (read first).** The Phase-73 contract was grounded against casework `bf15535` and noted CW-4
> as "casework's own current-state names this a Phase-15 candidate." At the verified HEAD casework **is at
> Phase 15** — and the `cleared` path **still does not exist** (the candidate was *named*, not *built*):
> - Disposition vocab at HEAD: `SYSTEM_DISPOSITIONS = ("blocked", "needs_more_info", "signed")` +
>   `HUMAN_DISPOSITIONS = ("file", "both_defensible")` (`signoff.py:32, 38`). **No `cleared`.** Hand it
>   Lakeshore today and it signs `file` (or refuses), never a documented affirmative dismissal. **CW-4
>   remains a GAP.**
> - `party_ref` resolution is still **strictly fail-closed**: a party-leaf alert's `party_ref` must resolve
>   to a declared `parties[].party_id` or the bundle fails (`contract.py:447-461` — "party_ref '…' does not
>   resolve to any parties[].party_id (fail-closed)"). There is **no grade, no confidence, no graded
>   resolution link** anywhere in `contract.py`. The contract-version vocab is
>   `KNOWN_CONTRACT_VERSIONS = ("0.1", "0.2", "0.3")` (`contract.py:53`).
> - The verifier chain is deterministic and fail-closed by design (the Phase-1a branch name). That posture
>   is *correct* — this brief does **not** loosen it; it adds a **graded** accept path *beside* the
>   fail-closed one, the grade riding as provenance.

---

## Objective

Replace the binary "resolved-or-rejected" `party_ref` validation with **confidence-graded resolution**:
casework accepts a resolution link that carries a **grade**, and **propagates the grade as provenance** —
a `weak`-grade link weakens a clear (it never silently merges), a `reject`/unknown link contributes
nothing (fail-closed preserved). Plus the two Phase-73 deferred CW items: **CW-2** entity-resolution
verification and **CW-4** the live **cleared-by-mitigation** verdict.

Three pieces, each additive — the byte-frozen fail-closed core is the floor, the graded path sits beside it.

## 1. Consume the graded resolution link (extends the fail-closed `party_ref`)

Today a `party_ref` either resolves (binary yes) or fails closed. The
[resolution-link schema](resolution-link-schema.md) carries **more than a boolean** — it carries a
**grade** and the **`basis[]`** that earned it. Casework consumes that.

### The link shape casework reads

From the [resolution-link schema](resolution-link-schema.md), the fields casework needs:

```jsonc
{
  "entity_id": "E-000123",
  "grade": "strong",                                  // "strong" | "weak" | "reject"  (ordinal)
  "basis": [{"kind": "email", "normalized_value": "jcaldermgmt@swiftmail.test"}],
  "method": "deterministic-identifier"
}
```

### The graded accept rule (cite [confidence-as-provenance](confidence-as-provenance-contract.md) §Exclude-don't-down-weight)

The filing/clear gate is a **boolean** with a byte-frozen bar (the A1 guard). A boolean **cannot express
"but the link is weak"**, so the rule is **exclude, not down-weight**:

- An evidence atom an investigator **reads** from the file via a resolution link — e.g. **ML-A4**, the
  network / beneficial-ownership leg read from a `resolution_edge` — is **admitted to the determination
  only if its supplying link is graded `strong` or `weak`**. A `reject`/unknown-grade link (empty
  `basis[]`) contributes **nothing**.
- The grade-gated view is computed **before** the sufficiency / signoff evaluation; the verifier chain
  itself is **never modified** and never sees a grade (it stays the byte-frozen fail-closed core).
- A `weak`-graded link is **admitted but flagged weak** — it can corroborate but, per the grammar, never
  resolves a party on its own. **It never silently merges two parties** (the >90%-FP discipline).
- **Multi-hop composes weakest-link:** an ownership/control chain takes the **minimum** grade along it —
  "this chain's weakest resolution is `weak`" — never a multiplied pseudo-probability
  ([confidence-as-provenance](confidence-as-provenance-contract.md) §Graph confidence). *Unknown over wrong.*

### The per-decision manifest (inspectability)

Every signoff emits an **inspectable manifest** listing each candidate evidence atom as **admitted** or
**quarantined-by-low-grade**, with the **link + grade** that supplied it (cite
[confidence-as-provenance](confidence-as-provenance-contract.md) §Manifest). A validator reads *why* a leg
was or was not counted — the file/clear is auditable down to the link behind each leg. This is casework's
defensibility climax: the refusal is *legible*, not an implicit filter.

> **Fail-closed preserved (the firewall).** A missing/unknown grade, or an empty `basis[]`, is treated as
> the weakest (`reject`) and **excluded** — never defaulted to "trusted"
> ([grade grammar](identity-grade-grammar.md) §Fail-closed). The Phase-15 `party_ref` fail-closed posture
> (`contract.py:461`) is **not loosened** — a `reject` link still grounds nothing. The graded path only
> *adds* a `strong`/`weak` accept; it never weakens the floor.

## 2. CW-2 — entity-resolution VERIFICATION (extends Phase-73 CW-2)

Casework's deterministic verifier chain gains an **ER-verification** check: when an evidence atom is
asserted **read** from a resolution edge, the verifier confirms the **link grade ≥ `weak`** and that the
atom's `basis[]` identifier(s) are present on the cited records — i.e. the resolution that supplied the leg
is *itself* grounded (exact-on-identifier), not asserted. A `reject`/empty-basis link supplying a *read*
atom is a **verifier violation** → `blocked`. This is the resolution analogue of the existing txn-leaf /
party-leaf grounding walk: a leg is only as defensible as the resolution behind it.

## 3. CW-4 — the live cleared-by-mitigation verdict (extends Phase-73 CW-4)

Add the **`cleared`** disposition — the documented affirmative dismissal casework cannot currently express.
signal-watch **proved the exact shape** in Phase 73 (`evidence_requirements.py` additive branch):

> **mechanism established + 0 corroborating legs + affirmative mitigation established + no named predicate
> → `cleared`** — a **separate clear path**, the file/determination bar **BYTE-UNCHANGED** (the A1 guard,
> proven by `evidence_requirements.py --selftest`).

Casework adopts that verified design:

- Add `cleared` to the disposition vocab (a new `HUMAN_DISPOSITIONS` member, or a system-computable
  affirmative-clear classification — match signal-watch's branch placement: the clear is evaluated
  **AFTER** the verifier chain, never inside it).
- A `cleared` disposition requires a grounded **`affirmative_clear` block** (the mitigation evidence —
  e.g. an explained source-of-funds, a documented legitimate pattern) on the **clear** stance, the mirror
  of `file`'s grounded inculpatory suspicion. Empty mitigation → no clear (the `file`-side discipline at
  `signoff.py:49-56`, mirrored).
- **The `file` bar is byte-unchanged.** `cleared` is **additive** — adding it must produce a
  byte-identical `file` / `both_defensible` / `blocked` / `needs_more_info` verdict for every existing
  bundle (the regression invariant — mirror signal-watch's `--selftest` proof). Hand casework Lakeshore →
  it clears *with a documented basis*; hand it Northgate → it still signs `file`.

> **CW-4 is independent and the smallest cross-pillar win.** It needs no substrate change — it can be
> exercised **today** through the existing subprocess file-handoff (signal-watch hands casework the
> authored Lakeshore bundle; casework returns `cleared`). CW-1 (counterparty-identity grounding) and the
> *graded-resolution* consume (§1) depend on the substrate's
> [graded-counterparty-identifiers emission](substrate-graded-counterparty-identifiers-PLAN-BRIEF.md)
> landing first — you cannot verify a grade that is not emitted. Sequence CW-4 first.

## Contract-version note

The graded resolution link is **additive** to the bundle shape — it rides as an optional block, exactly as
the v0.2 `parties` and v0.3 `related_parties` blocks did (`evidence.py:51-53`). A bundle carrying graded
links advances the contract version (a new entry in `KNOWN_CONTRACT_VERSIONS`, currently
`("0.1","0.2","0.3")`); an old bundle without the block stays valid and resolves on the existing
fail-closed `party_ref` path. **No existing bundle's verdict moves** — the additive discipline the whole
contract layer is built on.

## Sibling-executed framing

Built in **aml-casework**, on its own lifecycle. The boundary stays **distribution-not-coupling** (the
Phase-67 vendoring lesson): signal-watch invokes casework over the **subprocess file-handoff**; `build.py`
never imports casework; the 8 ship dists stay byte-frozen. Casework adds the graded accept path, the
ER-verification check, and the `cleared` verdict behind its **own** verifier chain and **own** tests —
including the regression invariant that the `file` bar is byte-unchanged.

## Why this matters to the consumer (the entity spine tie-back)

signal-watch's determination engine reads the **network / beneficial-ownership leg (ML-A4)** off the
[entity spine](resolution-link-schema.md) — and that leg is exactly what separates Northgate (files) from
Lakeshore (clears): same grounded signals, opposite outcomes, because one resolves to a network with a
named predicate and the other to an explained source-of-funds. If casework verifies and signs that
decision but treats every resolution link as a binary boolean, it **cannot express** that a clear standing
on a `weak`-graded network leg is *less defensible* than one standing on a `strong` leg — it would either
over-trust a name-only merge (the >90%-FP tsunami) or fail-close a legitimately `weak` corroboration.
Graded consume is what lets casework **propagate the grade as provenance** all the way to the analyst-
visible disposition, so the file/clear is auditable down to the identity link behind each leg — the LFCM
grounding chain, made defensible end-to-end.
