# Phase 73 — Rich investigation case in the LIVE workbench: the matched FILE/DISMISS pair, rail-aware counterparty network, entity resolution, and the affirmative-clear verdict

**Project:** signal-watch (presenter-driven offline AML vision prototype + the companion investigator workbench served by `scripts/serve_workbench.py`)
**Ceremony:** STANDARD (user override of the design-pass LITE recommendation)
**Date:** 2026-06-23
**Plan:** `[[phases/phase-73-rich-investigation-case-live-workbench]]` · **Ledger:** Phase-73

---

## 0. Provenance & the two user overrides

This spec is the contract for the 15-agent design-pass output (ground → 6 design perspectives → synthesize → 3 adversarial critics → revise). It is FAITHFUL to that output's concrete data model, the two cases' synthetic data, the investigation flow, the honesty guardrails, and the deferred cross-pillar contract — **except where the user explicitly overrode the workflow's recommendation.** Those overrides are load-bearing and govern this spec:

1. **Ship target = EXTEND THE COMPANION WORKBENCH, NOT a new offline dist.** The design pass recommended a 6th offline dist (`casefile.html` → `dist/casefile/`) rendering *authored-frozen* verdicts mapped to the engine vocab. The user **inverted** this: the rich case lives in the **live companion workbench** (`scripts/serve_workbench.py` + `workbench.html`), and the verdicts are **live-engine OUTPUT** computed by `evidence_requirements.py` over the rich authored evidence — **never authored-frozen strings.** No new dist, no `casefile.html`, no `build.py` `casefile` target, no launcher card. The 8 committed dists stay byte-frozen.
2. **Ceremony = STANDARD; ALL THREE graphs wired THIS phase.** The design pass scoped to one money-flow graph in a LITE phase, deferring the entity-resolution + named-BO graphs to a follow-on. The user **escalated to STANDARD** and pulled all three graphs (money-flow + entity-resolution + named-BO) into this phase, accepting two L tasks.

Three further user decisions OVERRIDE the workflow where it left a choice open (these were the workflow's own recommendations, now ratified as binding):

3. **DISMISS leads with affirmative business reconciliation + established source of funds** — NOT absence-of-a-negative-hit. (workflow open_decision #2, recommended option)
4. **The prior-Human-Trafficking-STR link sits on an INBOUND funds source (Vesna Maric); the outbound controller (James Calder) is a DIFFERENT identity.** (workflow open_decision #3, recommended option)
5. **The single load-bearing risk (A1):** add an AFFIRMATIVE-CLEAR verdict to the *live* engine WITHOUT moving the file/determination bar. (the workflow named this as CW-4, deferred to casework; the user pulled it into signal-watch's live engine THIS phase.)

Where this spec and the raw workflow output disagree, **this spec governs** (it encodes the overrides). Concrete entity names, money-flow shapes, evidence routing, and honesty machinery are carried verbatim from the workflow.

---

## 1. Objective & success definition

### 1.1 Objective

Author ONE matched pair of investigation cases in the **live companion workbench**:

- **CASE-A "Northgate Hospitality Group Inc."** → the live engine returns **`determination` → `escalated` → "file"**.
- **CASE-B "Lakeshore Catering Group Inc."** → the live engine returns the **new affirmative `cleared`** verdict → "documented dismissal".

Both cases fire the **IDENTICAL grounded signal set** (the same committed indicator ids: C3 funnel fan-in `fin-2020-alert001:IND-05` + C2 rapid pass-through `fin-2023-alert001:IND-03` + C14 source-not-established `fin-2025-a003:IND-09`) yet resolve OPPOSITELY, driven **only** by an authored identity/network layer:

- rail-aware counterparty identity (channel WIRE/EMT/AFT/P2P with named counterparties + populated country);
- a traceable money-flow network with real names;
- shared-identifier entity resolution (strong email/phone vs weak address-corroborate);
- a multi-hop named ownership chain reaching an internal address-keyed caution-list hit;
- a prior-Human-Trafficking-STR linkage on an INBOUND source party.

**THE THESIS:** *same grounded signal, opposite outcome — the network + the source of funds is the difference.*

The determination is **COMPUTED by the live engine** (`evidence_requirements.determine` / `evaluate_sufficiency`) over the authored evidence, surfaced in the live workbench. Names-not-codes everywhere; every value synthetic-by-construction; the always-on "Illustrative data & outputs" badge stays; no fabricated detection metric.

### 1.2 Success definition (the phase is done when ALL hold)

1. The live workbench (`serve_workbench.py` + `workbench.html`) **loads, serves, and computes** the matched pair from `data/casefile/`, surfacing both at the **top of the queue**.
2. The live engine **COMPUTES** `determination`/`escalated`/"file" for Northgate and the **new affirmative `cleared`** for Lakeshore — over the authored evidence, **no frozen verdict strings** (A2).
3. **The file bar is provably unchanged** — the existing `evaluate_sufficiency` rule (mechanism + ≥2 independent legs + named predicate + no unrebutted mitigation) is byte-identical; a RED selftest proves Lakeshore CANNOT reach `determination`, and the affirmative-clear path is a SEPARATE branch, not a loosened gate (A1).
4. **All three graphs render** in `workbench.html` with **real names** (money-flow / entity-resolution incl. the excluded near-match / named-BO via `display_name`, fixing the `:695` `party_id` bug).
5. **Names-not-codes throughout** rendered text (no bare `C#`/`D#`/`ML-A#`/`KYC-A#` in display/name/narrative/reading/text values).
6. `python3 scripts/build.py --check all` → **8/8 dists byte-identical** (companion-only; `build.py` imports none of it).
7. Tests green: the node arc harness + the python selftests (`evidence_requirements --selftest`, `serve_workbench --selftest`, `curate_workbench_cases --selftest`).
8. STANDARD self-check (all 7 categories) + the unified reviewer dispatch pass.

---

## 2. Scope

### 2.1 In scope (companion-only — NO ship target)

| File / dir | Change |
|---|---|
| `data/casefile/case.json` + `data/casefile/schema.md` | **NEW.** The authored matched pair + its schema (T1). |
| `scripts/evidence_requirements.py` + `data/workbench/evidence-requirements.json` | The live engine: read/gathered evidence sources, predicate-from-register, the affirmative-clear verdict; the file bar UNCHANGED (T2). |
| `scripts/serve_workbench.py` (+ `scripts/curate_workbench_cases.py` if the queue-merge belongs there) | Load + serve + COMPUTE the showcase pair via the extended engine; surface at the top of the queue (T3). |
| `workbench.html` | Names-not-codes; rail-aware counterparty panels; all three graphs; caution-list chain; inbound prior-STR panel; the file-vs-dismiss fork; fix `boGraphHTML` `party_id`→`display_name` at `:695` (T4). |
| `tests/casefile.test.mjs` **or** `tests/workbench.test.mjs`, `tests/smoke-checklist.md` | The arc + graph + ER + names-not-codes assertions; smoke row (T5). |
| `docs/case-workbench.md` (and/or `docs/evidence-driven-filing.md`) | Document the rich-case beat + the affirmative-clear verdict, if the existing companion docs need updating to stay true. |

### 2.2 Out of scope (parked / deferred)

- **No new offline dist / `casefile.html` / `build.py` target / launcher card.** (override #1)
- **`build.py` is not touched** for a casefile target. The casefile data is a **companion-only input** read by `serve_workbench.py`; `build.py` imports/reads NONE of it — the 8 dists stay byte-frozen.
- **aml-substrate and aml-casework are PARKED.** The pillar dependency is INVERTED: signal-watch authors the north-star rich case FIRST; the siblings become downstream implementers. No substrate slice, no casework re-vendor, no casework verifier change this phase.
- **The cross-pillar contract doc** (`docs/rich-case-target-contract.md`) is a **DEFERRED follow-on**, NOT phase work — a spec authored before the data model survives implementation is a guess. It is SKETCHED in §9 (what substrate must EMIT, what casework must SIGN) so the data model authors toward it, but it is **not built this phase.**
- **The txn-less party-leaf KYC signing frontier** (the carried Phase-72 casework no-transactions contract) stays a named casework follow-on — Lakeshore/Northgate both carry transactions, so this case pair does not depend on it.

---

## 3. Constraints & non-negotiables

### 3.1 A1 — the load-bearing guard (the determination bar must NOT move)

The new affirmative-clear verdict (mechanism fired + corroborating legs absent + affirmative mitigation **established** → a principled `cleared`) is a **SEPARATE branch** of the engine. It must NEVER loosen the file/determination bar:

> **mechanism + ≥2 independent legs + named predicate risk + no unrebutted mitigation → `determination`**

stays **byte-identical** in `evaluate_sufficiency`'s rule evaluation. Concretely:

- The affirmative-clear branch is reached **only** when the case is NOT sufficient for a determination (it would otherwise be `needs_more_info`) AND affirmative mitigation is established. It is `needs_more_info` strengthened by *positive* evidence into `cleared` — never a weakened determination.
- A RED selftest MUST prove: Lakeshore's atom set + an *un*-established mitigation still returns `needs_more_info` (the old behavior), and only the *established* mitigation flips it to `cleared`. The file bar's five existing selftest assertions (the ML stricter bar, one-leg-short, mechanism-absent, unrebutted-mitigation, named-risk-absent) must all stay GREEN unchanged.

> **HARD STOP (abort rule):** if Lakeshore can ONLY clear by weakening the file bar or by fabricating evidence → **STOP-and-surface.** Do not paper over. (A1 false.)

### 3.2 A2 — verdicts are live-engine OUTPUT

The two verdicts are **computed** by `evidence_requirements.determine`/`evaluate_sufficiency` over the authored evidence at serve time — **never authored-frozen strings** in `case.json`. `case.json` MAY carry the EXPECTED verdict as a **test oracle** (T1), but the served value is the engine's real computation. If the live engine cannot compute the two verdicts over the authored evidence without frozen strings → STOP (A2 false).

### 3.3 A4 — the honesty governor

- **NO catch-rate / detection-lift / precision / recall / f1 / Nx claim** anywhere. The contrast is **QUALITATIVE** ("the network is the difference"), never a performance number. The throughput read is labelled *"gross throughput ~N× the onboarded expected turnover, ~0 net retention"* and **REINFORCES the mechanism — it does NOT count toward the ≥2-leg bar.**
- **"N pct" not "%"** in every rendered ownership/value string. The honesty sweep (`osint_tools._BANNED`, already imported by `evidence_requirements.py`) is the regex authority; extend its reach to the casefile string values.
- **Structured facts (ownership pct/direction, counterparty country) are read from the RECORD, never authored by a model** (Phase-66 governor — the live workbench's GATHER model fabricates structured facts; this case's structured facts are committed-record-sourced by construction).
- **Synthetic-by-construction:** all emails on `.test`/`.example`, all phones in `555-01XX`, addresses from an authored fictional pool, `synthetic_label: true` on every entity. A shared-identifier ER match can ONLY ever resolve two synthetic parties — PII collision is structurally impossible.
- The always-on **"Illustrative data & outputs" badge** stays + **a panel-local synthetic marker on the prior-STR panel** so a cropped screenshot self-identifies.
- **NO real customer/transaction data, ever** (the project non-negotiable).

### 3.4 A0/A6 — companion-only boundary

- Everything is companion-only. **`build.py` imports no sibling/companion module and reads no casefile data.** The 8 committed dists stay byte-frozen (`--check all` 8/8).
- `evidence_requirements.py` stays **stdlib + the shared honesty sweep only** — it NEVER imports `aml_substrate` / `aml_casework` / `serve_chain` / `serve_workbench`; `build.py` NEVER imports it. The casework STR-vocab mirror stays embedded (kept in sync at re-vendor — not re-vendored this phase).

### 3.5 Engine-vocab facts (verified in-repo, do not re-derive)

- `evaluate_sufficiency` verdict vocab today = **`{determination, needs_more_info}`** (`evidence_requirements.py:348`).
- `serve_workbench.DISPOSITION_VOCAB` = **`{cleared, escalated, needs_more_info}`** (`serve_workbench.py:182`) — the workbench adjudication disposition (distinct from the *chain*'s `{file, escalate, needs_more_info}`).
- The casework crime_type vocab = `{money_laundering, terrorist_financing, kyc_integrity}`; the profile covers `{money_laundering, kyc_integrity}`.
- The mapping this phase makes EXPLICIT: `determination → escalated → "file"`; the new `cleared` verdict → `cleared` disposition → "documented dismissal". The presentation labels "file"/"documented dismissal" are workbench DISPLAY strings mapped from the engine atoms, never engine output strings.

---

## 4. The data model (`data/casefile/case.json` + `schema.md`)

A new committed dataset, synthetic, validated at the companion load boundary (not a build input). Top-level:

```
{
  meta: { title, badge: "Illustrative data & outputs", synthetic_notice,
          jurisdiction: "Canada", predicate_focus: "human trafficking" },
  reference: { caution_list[], prior_str_register[] },   // shared across the pair
  cases: [ CASE-A, CASE-B ]
}
```

### 4.1 Entity (`cases[].entities[]`) — the one new resolved primitive

```
{ entity_id,            // case-local slug, e.g. "E-NORTHGATE"
  kind: "person"|"org",
  display_name,
  synthetic_label: true,                 // ALWAYS
  role: "subject"|"counterparty"|"related_party",
  identity: { address?{line,city,region,country,normalized}, email?, phone? },
  identifiers: [ { kind: "email"|"phone"|"address", value, normalized,
                   strength: "strong"|"weak" } ],     // email/phone = strong; address = weak
  kyc?: { risk_rating, cdd_level, source_of_funds?,
          expected_monthly{amount,currency,txn_count} }  // SUBJECT only
}
```

- **`strength:"strong"` is FORBIDDEN on `kind:"address"`** (the >90 pct-FP discipline — address corroborates, never resolves identity). The validator rejects it.
- `source_of_funds` is the **clean contrast axis**: CASE-A null/unestablished, CASE-B established.
- PII structurally fictional (`.test`/`.example` emails, `555-01XX` phones, authored-pool addresses).
- Counterparty `naics_code`/`nature_of_business`/`pep_tier` are **dropped** (subtraction test — no panel renders them; they move to the §9 contract sketch as SUB-5).

### 4.2 Transaction (`cases[].transactions[]`) — mirrors the LIVE shape + a named counterparty

The live txn key is **`channel`** (NOT `rail`); values `WIRE/EMT/AFT/P2P/CARD/CASH/CHEQUE`.

```
{ txn_id, account_ref, direction: "CREDIT"|"DEBIT", channel,
  amount{value,currency}, timestamp,
  counterparty: { entity_ref,            // -> entities[]
                  name, observed_at?, address?, email?, phone?,
                  country,               // POPULATED (the live slice is 0/25,391 null)
                  memo?, role: "originator"|"beneficiary" } }
```

- **Channel → routing-key PRESENT-check** (NOT a prohibitive absent-check — a present-check cannot encode a wrong real-world claim about how a rail works): WIRE requires name+address; EMT requires email; AFT requires country; P2P requires a handle/email/phone; CARD/CASH/CHEQUE require name-or-null.
- `counterparty.country` POPULATED on every leg.
- Amounts rail-consistent: EMT legs sub-limit (< $10k); the drain is **structured** (a series of sub-limit EMTs).

### 4.3 Named-BO graph (`cases[].related_parties[]` + `cases[].ownership_edges[]`)

```
related_parties[]:  party gains display_name + identity + entity_ref
ownership_edges[]:  { src, dst, label, ownership_pct }
                    // label vocab: BENEFICIAL_OWNER / DIRECTOR_OF / OFFICER_OF / CONTROLS / OWNS
                    // MULTI-HOP so the Northgate -> 1187442-Ontario-Inc -> caution-listed-address
                    // chain renders as a visible chain, not a floating assertion.
```

`ownership_pct` renders **"N pct" never "%"**.

### 4.4 Resolution edges (`cases[].resolution_edges[]`) — the ER layer

```
{ between: [entity_id, entity_id],
  shared: [ { kind, value, normalized, strength } ],
  reading }              // the human-readable resolve text
```

- The validator asserts each shared value appears on **BOTH** entities' `identifiers` **on the SAME field** the edge claims to match (normalized for strong email/phone) — self-grounding on the matched field, not the raw value.
- Includes the **excluded near-match** edge (John Calderon vs James Calder — see §5) marked as considered-and-excluded (no shared identifier).

### 4.5 Reference (top-level, shared)

```
caution_list[]:        { id, kind: "address"|"entity", address?{...normalized},
                         reason, text, badge }        // address-keyed
prior_str_register[]:  { id, subject_name, identifiers{email?,phone?},
                         predicate: "human trafficking", prior_str_id, text, badge }
```

- The determination engine **READS the predicate** from the `prior_str_register` record (rather than an analyst typing it at determination time). The register entry is **itself authored synthetic** — `schema.md` / honesty notes state it that way (NOT "never authored", which would overclaim for a fully synthetic artifact).

### 4.6 Determination shape (`cases[].determination`) — the test oracle, MAPPED to the live engine

```
{ crime_type,
  mechanism: { atom, name, present, via: "fired", evidence },
  legs: [ { atom, name, present, via: "fired"|"read"|"gathered", evidence } ],
  named_predicate_risk: { named, value, source },     // source -> the prior_str record
  mitigation: { established: bool, basis },
  expected_verdict: "determination"|"needs_more_info"|"cleared",   // ORACLE only; engine computes the served value
  expected_disposition: "escalated"|"cleared",
  presentation_label: "file"|"documented_dismissal",  // DISPLAY label, mapped from atoms
  sufficiency_line,
  str_record{...} | clearance_record{...} }
```

- The **`via` tag** (fired/read/gathered) renders distinctly and is referentially grounded by the validator: `via:"fired"` MUST cite an alert whose `signal_id` is in `cases[].alerts[]`; `via:"read"` must reference a present entity/edge; `via:"gathered"` must reference a present caution_list/prior_str entry. (This is the only guardrail against an authored slip rendering "a detector fired" with no detector.)
- Throughput-vs-profile is recorded as a **pass-through REINFORCEMENT** of the mechanism — it does NOT count as an independent leg.

---

## 5. The two cases (concrete, parallel, corrected routing)

Both cases carry `cases[].alerts[]` with the **IDENTICAL** signal_ids: `fin-2020-alert001:IND-05` (C3 funnel fan-in), `fin-2023-alert001:IND-03` (C2 rapid pass-through), `fin-2025-a003:IND-09` (C14 source-not-established). CASE-B carries `evidence_panel_ref: "CASE-A"` so the validator PROVES the topology + grounded indicator ids are identical; only the identity/attribute layer differs.

### 5.1 CASE-A "Northgate Hospitality Group Inc." → DETERMINATION / FILE

Synthetic org, short-stay accommodation, Hamilton ON. Risk **HIGH/EDD**; **`source_of_funds` UNESTABLISHED**; expected_monthly $18,000 / 40 txns.

**Network (~14–18 authored txns):**
- ~9 dispersed small inbound EMT/CARD/CASH credits from unrelated originators (e.g. Dragana Petrov `d.petrov88@quickmail.test`, M. Okonkwo `+1-555-0142`, +7) totalling ~$46,200 over ~30 days, near-zero net retention.
- **The drain is rail-honest + structured:** the proceeds forward out as a SERIES of STRUCTURED sub-limit EMTs (~$8,400 × 5; email IS the genuine routing key on an EMT) to controller **James Calder** (`jcalder.mgmt@swiftmail.test`, `observed_at` a receiving institution). Structuring strengthens the trafficking-funnel narrative AND the email resolve is honest to the rail that carried it.

**Evidence routing (CORRECTED — the load-bearing fixes):**
- **R3 resolve (outbound controller):** James Calder is the subject's own listed **director** (related party, SAME email) → "our director == the party receiving the structured drain", asserted from the identifier on OUR rail leg (NOT a lookup into the receiving institution; the cross-institution disclaimer renders adjacent to the edge).
- **Prior-trafficking-STR (INBOUND source — a DIFFERENT person):** inbound originator **Vesna Maric** (`v.maric@quickmail.test`) resolves by email to `prior_str_register` (predicate = human trafficking) → "a SOURCE of the funnel's funds is linked to a prior-trafficking subject" is now literally true (ML-A5 corroboration on the inbound source where it belongs). The controller (Calder) and the STR-source (Maric) are **different identities** — de-concentrated.
- **R4 caution-list (multi-hop ownership chain):** the beneficial owner **1187442 Ontario Inc.** sits at **44 Holloway Court, Brampton** → caution_list address hit, reached through the rendered **Northgate → 1187442-Ontario-Inc → 44-Holloway** ownership chain.
- **Throughput read:** ~$115,500/mo gross throughput, ~0 net retention vs $18,000 onboarded expected turnover — labelled as gross throughput ~N× the onboarded expected turnover, framed as REINFORCING the pass-through mechanism, NOT a separate leg.

**Determination (≥2-leg bar met by INDEPENDENT legs):** mechanism (via:fired, C2/C3) + source-not-established (via:read/fired, C14 — the live exemplar's natural leg) + network (via:read — the resolved txn network + ownership chain) + corroboration (via:gathered — the caution-list address hit + the INBOUND prior-trafficking-STR source) + named_predicate_risk = "human trafficking" (read from the prior_str record, source-cited) + mitigation NOT established → engine computes **`determination` → `escalated` → "file"**.

`str_record`: crime_type = money_laundering; cited_signal_ids + cited_txn_ids; STR completeness (the FINTRAC required elements satisfied); a trafficking-funnel narrative naming the dispersed inbound, the structured forward-out to the director-controller, the shared-identifier cluster, the caution-list ownership chain, the prior-trafficking-STR INBOUND linkage, and human trafficking as the predicate; `narrative_claims[]` each citing evidence by record/txn id. Labelled "ILLUSTRATIVE STR — synthetic case, not a filed report".

### 5.2 CASE-B "Lakeshore Catering Group Inc." → CLEARED / DOCUMENTED DISMISSAL

Synthetic org, event catering, Oakville ON. Risk **MEDIUM/CDD**; **`source_of_funds` = "Catering revenue (event deposits + corporate accounts)" ESTABLISHED** (the MIRROR of A's unestablished source — the clean contrast axis).

**Network (~8 inbound + a recurring forward, parallel funnel-in→forward shape):**
- inbound from recognizable corporate/event clients (Halton Conference Centre Ltd via AFT country=CA, Priya Raman event-deposit EMT `priya.raman@example.test`, +6 clean clients) totalling ~$43,500;
- outbound **WIRE** $39,200 (rail-honest: WIRE carries name+address, NOT email) to **Riverside Linen Supply Ltd**, a recurring monthly supplier.

**The honest NON-MATCH trap (the ER corroborator):** inbound originator **John Calderon** (`jcalderon.events@example.test`) is a common-name collision with A's **James Calder** that does NOT resolve (different given name, different email) — proving ER is **exact-on-identifier, not fuzzy-on-name**; rendered in the ER graph as "considered and excluded — no shared identifier".

**The clear leads with AFFIRMATIVE BUSINESS RECONCILIATION (override #3) — NOT absence-of-a-list-hit:**
- the inbound legs reconcile to the stated catering business (named corporate/event clients matching the profile);
- the forward-out is a recurring identifiable supplier consistent with history;
- source of funds is **established**;
- volume fits the anticipated profile (~$43,500 vs ~$44,000 expected);
- the clean caution-list/prior-STR state + the excluded near-match are **CORROBORATING, not causal.**

**Determination:** mechanism present; mitigation **AFFIRMATIVELY ESTABLISHED** (flows reconcile to a legitimate business + established source of funds + historical consistency — this is what clears it); corroboration HONEST-EMPTY; no nameable predicate → the live engine, via the **new affirmative-clear branch**, computes **`cleared` → "documented dismissal"** (mechanism fired, the ≥2 independent legs absent, mitigation affirmatively established).

> **The honest gap, named not papered (CW-4):** the live engine BEFORE this phase had NO cleared-by-established-mitigation verdict — it returned `needs_more_info` ("go gather"). This phase ADDS that verdict to the live engine (the user's override #5). The new branch is reached only when a determination is NOT licensed AND affirmative mitigation is established — it is `needs_more_info` strengthened by positive evidence, never a weakened file bar (§3.1).

`clearance_record`: outcome = "alert_cleared_with_rationale"; a recorded rationale **BY SUBSTANCE** naming the reconciled business sources + the established source of funds + the historical-consistency basis (clean screen + excluded near-match as corroborators); `retained_for_audit: true`. **NEVER branded "defensive filing".**

---

## 6. The engine-extension contract (`evidence_requirements.py` + `evidence-requirements.json`)

The extensions WIDEN evidence PRESENCE and ADD a distinct verdict — they NEVER loosen the determination rule.

### 6.1 New evidence sources (how an atom becomes present)

Today `present_atoms` marks an atom present iff a fired capability matches OR a `gather_signal` was returned by the live GATHER loop. Extend the presence sources WITHOUT touching the sufficiency rule:

- **`via:"read"` (read-from-file):** an atom is present when the authored evidence in `case.json` references a present entity/edge that grounds it (e.g. ML-A4 network from the resolved txn network + ownership chain; ML-A7 source-not-established from the subject's `kyc.source_of_funds` state). The read source is **referentially checked** against the casefile (the entity/edge must exist).
- **`via:"gathered"` (caution_list / prior_str gather kinds):** extend the gather mapping so a **caution_list address hit** and a **prior_str register hit** each close the corroboration leg (ML-A5) — record-sourced from `reference.caution_list[]` / `reference.prior_str_register[]`, not model-authored.
- **predicate read-from-register:** the `named_predicate_risk` is established by reading the predicate from a matched `prior_str_register` record (the inbound Vesna-Maric resolve), source-cited — rather than an analyst typing it.

### 6.2 The affirmative-clear verdict (the A1-guarded addition)

Add a THIRD verdict to the engine, reachable ONLY on the not-sufficient path:

```
if sufficient_for_determination:   verdict = "determination"      # UNCHANGED bar
elif affirmative_mitigation_established AND no nameable predicate AND legs absent:
                                   verdict = "cleared"            # NEW — a principled dismissal
else:                              verdict = "needs_more_info"    # UNCHANGED default
```

- `cleared` requires **affirmative positive evidence** (established source of funds + reconciled business flows + historical consistency) — it is NOT the absence of a hit and NOT a weakened determination.
- The existing `evaluate_sufficiency` rule (mechanism_required / additional_legs_required / named_predicate_risk_required / no_unrebutted_mitigation_required) is **byte-identical** in how it gates `determination`. The clear branch sits AFTER the sufficiency test fails.
- The profile JSON (`evidence-requirements.json`) MAY gain an affirmative-mitigation expression (e.g. an `affirmative_clear` block naming which mitigation atoms, when AFFIRMATIVELY established with a basis, license a clear) — validated by `validate_requirements` under the existing fail-loud discipline (closed vocab, honesty sweep, no banned token).

### 6.3 The file-bar invariant (the regression gate)

`--selftest` MUST carry RED cases proving:

1. **The new clear path fires** for Lakeshore's atom shape (mechanism present, legs absent, mitigation affirmatively established, no named predicate) → `cleared`.
2. **The same atom shape WITHOUT established mitigation** → still `needs_more_info` (the old behavior — the clear is earned by positive evidence, not the default).
3. **The file bar is unchanged:** the five existing ML-bar assertions (full bar → determination; one-leg-short → needs_more_info; mechanism-absent → needs_more_info; unrebutted-mitigation → needs_more_info; named-risk-absent → needs_more_info) all stay GREEN.
4. **The clear branch cannot manufacture a determination:** no atom set that fails the determination rule can reach `determination` via the clear path (the clear path only ever produces `cleared` or falls through to `needs_more_info`).

---

## 7. Tasks (STANDARD, full TDD)

> Per `dev-wiki-hooks.md`: pick the NEXT uncompleted task, state it, run RED → GREEN → REFACTOR → VERIFY, mark `[x]` before the next. Two L tasks accepted (STANDARD).

### T1 (L) — Author the rich-case dataset + schema (the load-bearing 80 pct)

**Scope:** `data/casefile/case.json`, `data/casefile/schema.md`

**RED:** a test (in `case.json`'s own oracle / a python assertion) that asserts the authored pair's expected verdicts + structural invariants, failing against an absent/partial file.

**GREEN:** author `case.json` (CASE-A determination/file + CASE-B cleared/dismiss; entities, channel-mirrored txns with named counterparties + populated country; resolution_edges + ownership_edges; caution_list; inbound prior-STR on Vesna Maric; structured sub-limit-EMT drain; source-of-funds the clean contrast axis) + `schema.md`.

**Success criterion:**
```
python3 -c "import json; d=json.load(open('data/casefile/case.json')); a,b=d['cases']; \
assert a['determination']['expected_verdict']=='determination' and a['determination']['expected_disposition']=='escalated' and a['determination']['presentation_label']=='file'; \
assert b['determination']['expected_verdict']=='cleared' and b['determination']['expected_disposition']=='cleared' and b['determination']['presentation_label']=='documented_dismissal'; \
sa={x['grounding']['signal_id'] for x in a['alerts']}; sb={x['grounding']['signal_id'] for x in b['alerts']}; \
assert sa==sb and 'fin-2023-alert001:IND-03' in sa and 'fin-2020-alert001:IND-05' in sa and 'fin-2025-a003:IND-09' in sa, (sa,sb); \
assert b.get('evidence_panel_ref')=='CASE-A'; \
assert all(e.get('synthetic_label') for c in d['cases'] for e in c['entities']); \
assert not any(i.get('strength')=='strong' and i.get('kind')=='address' for c in d['cases'] for e in c['entities'] for i in e.get('identifiers',[])); \
print('OK pair+identical-signal_ids+synthetic+no-strong-address')"
```

### T2 (M) — Extend the live determination engine (the A1-guarded core)

**Scope:** `scripts/evidence_requirements.py`, `data/workbench/evidence-requirements.json`

**RED:** add `--selftest` cases that (a) FAIL before the change — the affirmative-clear path does not exist; and (b) prove the file-bar invariant §6.3 (1–4).

**GREEN:** implement the read-from-file evidence source (`via:read`), the caution_list/prior_str gather kinds (`via:gathered`), predicate read-from-register, and the affirmative-clear verdict branch. The determination rule stays byte-identical.

**Success criterion:**
```
python3 scripts/evidence_requirements.py --selftest
# AND a diff/grep proving the determination rule body in evaluate_sufficiency is unchanged
# (the clear branch is additive, after the sufficiency test).
```

### T3 (M) — Wire serve_workbench to load + serve + COMPUTE the showcase pair

**Scope:** `scripts/serve_workbench.py` (+ `scripts/curate_workbench_cases.py` if the queue-merge belongs there)

**RED:** add a `serve_workbench --selftest` (or `curate --selftest`) assertion that the casefile pair loads, computes the two verdicts via the extended engine, and surfaces at the top of the queue — failing before the wiring.

**GREEN:** load `data/casefile/case.json`; map each case's authored evidence into the engine's atom-presence inputs (capabilities/gathered/read + named_predicate_risk + mitigation_established); call the extended engine; surface both cases at the **top of the queue** (the queue payload + per-case display rows). Northgate computes `determination`/`escalated`/file; Lakeshore computes the new `cleared`/documented-dismissal. `build.py` reads none of it.

**Success criterion:**
```
python3 scripts/serve_workbench.py --selftest
# the selftest asserts: casefile pair loads; engine COMPUTES determination->escalated (Northgate)
# and cleared (Lakeshore) over the authored evidence; both at the top of the queue.
```

### T4 (L) — Render in workbench.html (the second L)

**Scope:** `workbench.html`

**RED:** the node arc/render assertions in T5's harness drive this (RED before the render exists).

**GREEN:** render —
- **names-not-codes** (every C/D/ML-A/KYC-A code resolves through the inlined capability-taxonomy `nameOf()`; no bare code in any displayed text; a code survives only in a tooltip/data-attr);
- **rail-aware counterparty panels** (the channel-shaped counterparty identity column: EMT→email, WIRE→address, AFT→country);
- **all three graphs:** money-flow (`txnNetwork` — group txns by (account, counterparty.entity_ref) → directed weighted edges); entity-resolution (shared-identifier edges, strong/weak, **incl. the excluded near-match** John-Calderon vs James-Calder); **named-BO via `display_name`** — fixing the `boGraphHTML` `party_id` bug at `workbench.html:695` (the node names + edge labels use `display_name`, not the raw `party_id`);
- the **caution-list ownership chain** (Northgate → 1187442-Ontario-Inc → 44-Holloway, rendered as a chain);
- the **inbound prior-STR panel** with its OWN inline synthetic marker + the predicate read from the record;
- the **file-vs-dismiss fork** side-by-side (the thesis line: "identical grounded signal, opposite outcome — the network + the source of funds is the difference"; lead with reconciliation/source-of-funds; clean screen/ER as the dramatic corroborator; the dismissal recorded by substance, never "defensive"; a "qualitative network contrast, not a catch-rate" note);
- **"N pct" never "%"**; the persistent badge; the cross-institution disclaimer adjacent to the cross-institution resolve reading.

**Success criterion:**
```
grep -q 'display_name' workbench.html  # the boGraphHTML fix at :695 (party_id -> display_name)
grep -q 'txnNetwork' workbench.html
python3 -c "import re; h=open('workbench.html').read(); \
assert not re.search(r'>[^<]*\b(C[0-9]+|D[0-9]+|ML-A[0-9]+|KYC-A[0-9]+)\b[^<]*<', h) or True"  # backstop; the node harness is authoritative
node tests/<casefile|workbench>.test.mjs    # the authoritative render assertions (T5)
```
(the authoritative R7 names-not-codes + 3-graph assertions live in T5's node harness, run against the live-served render fixture.)

### T5 (M) — Tests + drift guard (the closeout)

**Scope:** `tests/casefile.test.mjs` **or** `tests/workbench.test.mjs`, `tests/smoke-checklist.md`

**RED:** the harness asserts the full beat, failing before T1–T4 land.

**GREEN:** the node harness asserts: the matched-pair fork (Northgate file/escalated vs Lakeshore cleared/documented-dismissal — computed, not frozen); the rail-aware counterparty identity column; **all three graphs render** (money-flow / entity-resolution incl. the strong resolve + excluded near-match / named-BO with display_name); the caution-list ownership chain; the inbound prior-STR panel with its synthetic marker; **names-not-codes** (no bare code in rendered text); "N pct" not "%"; badge always-on; XSS-escape via `esc`; keyboard guards; both motion modes. Add the python selftests + `--check all` to the success command. Add the smoke-checklist row + the pre-present sequence.

**Success criterion:**
```
node tests/<casefile|workbench>.test.mjs \
  && python3 scripts/evidence_requirements.py --selftest \
  && python3 scripts/serve_workbench.py --selftest \
  && python3 scripts/curate_workbench_cases.py --selftest \
  && python3 scripts/build.py --check all   # 8/8 dists byte-identical (companion-only; no drift)
```

---

## 8. Risks & checkpoints

### 8.1 A1 — the load-bearing risk (the affirmative-clear verdict)

**Risk:** adding the `cleared` verdict tempts a loosening of the file bar (e.g. "Lakeshore has a mechanism + 1 leg, just lower the leg requirement") which would silently change Northgate's class and every other ML case in the workbench.

**Checkpoint (T2 VERIFY):** the §6.3 RED selftest is the gate. The clear path MUST be additive and reached only on the not-sufficient branch; the five existing ML-bar assertions stay GREEN; a code-diff proves the determination rule body is byte-identical.

**STOP rule:** if Lakeshore can only clear by weakening the file bar OR by fabricating evidence (e.g. inventing an exculpatory record that isn't authored synthetic) → **STOP and surface to the user.** Do not proceed. (A1 false.)

### 8.2 Three graphs over one phase (the STANDARD-escalation risk)

**Risk:** pulling all three graphs into one phase (vs the design pass's single-graph LITE scope) inflates T4 beyond an L. The named-BO graph also requires the `:695` `party_id`→`display_name` fix, which touches an existing renderer that other cases use.

**Checkpoint (T4):** the `boGraphHTML` fix must keep the existing vendored-population cases rendering (the fix is `party_id`→`display_name` with a fallback to `party_id` when `display_name` is absent, so old bundles without `display_name` don't break). The node harness asserts all three graphs render for the casefile pair; a spot-check confirms an existing population case still renders its BO graph. If T4 cannot land all three within the L budget → surface (do not silently descope a graph; the user pulled them in deliberately).

### 8.3 SME-realism of the file-vs-dismiss contrast

**Risk:** the contrast reads thin or AML-wrong (clearing a funnel alert on "no list hit" is AML-wrong — the design pass's CRITIQUE-1 F2).

**Checkpoint (delivery gate):** the dismissal leads with AFFIRMATIVE business reconciliation + established source of funds (override #3); the prior-STR sits on an inbound source with a DIFFERENT controller (override #4). The delivery report carries the verbatim Lakeshore clearance rationale + the Northgate STR narrative for the user (an SME) to adjudicate realism — believability is a human judgment at the gate, not an automated assertion.

### 8.4 A2 — verdicts must compute, not freeze

**Checkpoint (T3 VERIFY):** the served verdict is the engine's `determine()` output, not `case.json`'s `expected_verdict` string (which is the test oracle only). If the engine cannot reproduce both verdicts over the authored evidence without reading a frozen string → STOP (A2 false).

---

## 9. Honesty & handoff

### 9.1 Honesty spine (every value synthetic-by-construction)

- Every entity carries `synthetic_label: true`; emails on `.test`/`.example`; phones in `555-01XX`; addresses from an authored fictional pool. A shared-identifier ER match can ONLY resolve two synthetic parties — PII collision is structurally impossible. The "no real customer data ever" non-negotiable governs everything committed.
- The always-on badge stays + the prior-STR panel carries its OWN inline synthetic marker (a cropped screenshot self-identifies).
- NO fabricated detection performance — the contrast is QUALITATIVE, never a catch-rate; the throughput read REINFORCES the mechanism, it does NOT count toward the ≥2-leg bar; the fork carries an explicit "qualitative network contrast, not a catch-rate" note (reconciling against the showcase's illustrative-lift template so the two artifacts don't conflict silently).
- names-not-codes (R7) enforced in rendered text (no bare code in display/name/narrative/reading/text values).
- The prior-STR predicate is READ BY THE ENGINE from the register record; the register entry is itself authored synthetic — honesty notes say exactly that, NOT "never authored" (which would overclaim).
- the dismissal is documented-by-substance leading with business reconciliation + established source, never "defensive filing".
- per-`via`-tag referential integrity (fired→present alert; read→present entity/edge; gathered→present caution_list/prior_str) is the only guardrail against inferred-masquerading-as-fired — it is enforced at the load boundary.
- **The claim most likely to be wrong:** that the affirmative-clear verdict can be added to the live engine without moving the file bar. The §6.3 RED selftest is the defense; if it cannot be satisfied, A1 is false and the phase STOPS.

### 9.2 The deferred cross-pillar contract (SKETCHED, not built)

`docs/rich-case-target-contract.md` is a **follow-on deliverable**, authored AFTER the matched pair survives implementation (a spec before the artifact proves the data-model shape is a guess). It will name what the parked siblings must build toward — sketched here so the data model authors toward it:

**aml-substrate must EMIT (the named gaps):**
- **SUB-1** channel-aware counterparty IDENTITY on the txn (per-channel name/address/email/phone/country; populate `counterparty_country`, 0/25,391 today) → makes ML-A4 readable-from-file.
- **SUB-2** deliberately SEEDED shared identifiers (same email/phone across ≥2 parties, strength-tagged) → R3 ER.
- **SUB-3** a NAMED multi-edge BO/control graph (full vocab, multi-hop, named nodes; today only BENEFICIAL_OWNER, bare `party_id`s) → ML-A4 + the caution-list ownership chain.
- **SUB-4** named source-party identity on fan-in legs (not bare `counterparty_ref`) → ML-A5.
- **SUB-5** populated KYC fields incl. `naics_code`/`nature_of_business` (dropped from this phase's model per the subtraction test) → ML-A6/A7 mitigation.
- **SUB-6** cross-border/corridor expressibility — a substrate CAPABILITY gap, NOT a CASE-A requirement (a Canadian trafficking case need not exercise a cross-border leg).
- **SUB-7** an internal address-keyed CAUTION LIST + a prior-STR register carrying the predicate → ML-A5 + named-predicate.
- **SUB-8** a behavioral/historical baseline for the established-mitigation clear.

**aml-casework must SIGN/REFUSE/CLEAR over it:**
- **CW-1** verify the channel counterparty identity grounds.
- **CW-2** verify ER links exact-on-email/phone (strong); refuse address-only as a confirmed identity (weak).
- **CW-3** sign the txn-LESS kyc/caution-list/party-leaf cases — the carried Phase-72/73 no-transactions-contract frontier.
- **CW-4** the affirmative-clear (cleared-by-established-mitigation) verdict — **adopted into signal-watch's LIVE engine THIS phase** (the user's override #5); casework should carry the same verdict so a signed clear is defensible end-to-end. This phase proves it in the live workbench; casework adopts it as the downstream implementer.
- **CW-5** carry the record-sourced predicate into the FINTRAC-quality narrative.

The gate never loosens: every new evidence source widens PRESENCE through the unchanged sufficiency rule (mechanism + ≥2 independent legs + named predicate + no unrebutted mitigation); the affirmative-clear is a NEW verdict requiring affirmative clean evidence, never a weaker gate.

### 9.3 Process honesty

- This is a STANDARD-ceremony phase; this spec is the §38 direction gate's spec deliverable. No "no regressions" claim without a baseline — `--check all` (8/8) is the drift guard, and the file-bar invariant is checked explicitly (§6.3), not asserted.
- `build.py` imports/reads none of the casefile data or the companion engine — the 8 dists are byte-frozen by construction (companion-only).
