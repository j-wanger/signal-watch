# `data/casefile/` — the rich investigation case file (schema)

**Phase 73. Companion-only.** `build.py` never reads this; it is loaded + computed by the live
investigator workbench (`scripts/serve_workbench.py`). The 8 ship dists are unaffected.

`case.json` is an **authored, fully-synthetic** north-star case: ONE matched pair that fires the
**identical grounded signal set** and resolves **oppositely** — the network and the source of funds is
the difference. The determination verdict is **computed by the live engine** (`evidence_requirements.py`)
over this evidence; the `determination.expected_*` fields are a **test oracle**, never the served value.

## Top level

```
{ meta{title, badge, synthetic_notice, jurisdiction, predicate_focus, thesis, ...},
  reference{ caution_list[], prior_str_register[] },   // shared across the pair
  cases[ CASE-A (files), CASE-B (clears) ] }
```

## `reference` (shared, top level)

- **`caution_list[]`** — `{id, kind:"address"|"entity", address?{line,city,region,country,normalized}, reason, text, badge}`.
  Address-keyed. An ownership chain reaching a `normalized` address here lights the corroboration leg.
- **`prior_str_register[]`** — `{id, subject_name, identifiers{email?, normalized_email?, phone?}, predicate, prior_str_id, text, badge}`.
  An inbound counterparty whose normalized identifier matches a record here lights corroboration **and**
  supplies the **named predicate risk** (read from `.predicate`). The register entry is itself authored
  synthetic — honesty notes say exactly that (not "never authored").
- **`watchlist[]`** — `{id, name, kind, identifiers, text, badge}`. A name-screening reference. A counterparty
  whose NAME is a near-match but shares NO identifier is the *excluded near-match* (a `resolution_edge` with
  `status:"excluded"`, `candidate_register` → here) — proving resolution is exact-on-identifier, not
  fuzzy-on-name. A name-only collision is never a hit.

## `cases[]`

Each case: `{case_id, display_name, subject{entity_ref, account_ids[]}, alerts[], entities[],
transactions[], related_parties[], ownership_edges[], resolution_edges[], determination{}}`.
CASE-B also carries `evidence_panel_ref:"CASE-A"` — it shares the evidence topology by reference; only
the identity/attribute layer differs.

### `alerts[]` — the grounded signals (identical across the pair)
`{alert_id, capability, detector, account_id, party_ref?, txn_ids[], grounding{signal_id, advisory_id, flag, red_flag}}`.
`flag` is the **verbatim** US-federal (FinCEN, public-domain) indicator; `red_flag` is the plain-language
translation. Both cases carry C3 `fin-2020-alert001:IND-05` + C2 `fin-2023-alert001:IND-03` + C14
`fin-2025-a003:IND-09` — real grounded references (the live exemplar `CASE-P-0028818` carries them too).

### `entities[]` — the one resolved primitive
```
{ entity_id, kind:"person"|"org", display_name, synthetic_label:true (ALWAYS),
  role:"subject"|"counterparty"|"related_party", observed_at?,
  identity{ address?{line,city,region,country,normalized}, email?, phone? },
  identifiers[ {kind:"email"|"phone"|"address", value, normalized, strength:"strong"|"weak"} ],
  kyc?{ risk_rating, cdd_level, nature_of_business, source_of_funds?, expected_monthly{amount,currency,txn_count} }  // SUBJECT only
}
```
- **`strength:"strong"` is FORBIDDEN on `kind:"address"`** — email/phone resolve identity; an address only
  corroborates (the >90 pct-false-positive discipline). The validator rejects a strong address.
- `source_of_funds` is the **clean contrast axis**: CASE-A `null` (unestablished) → ML-A7 lights;
  CASE-B established → ML-A7 is mitigated, not a leg.
- PII is structurally fictional: emails on `.test`/`.example`, phones in `555-01XX`, addresses authored.

### `transactions[]` — rail-aware, named counterparty
```
{ txn_id, account_ref, direction:"CREDIT"|"DEBIT", channel:"WIRE"|"EMT"|"AFT"|"P2P"|"CARD"|"CASH"|"CHEQUE",
  amount{value,currency}, timestamp,
  counterparty{ entity_ref?->entities, name, observed_at?, address?, email?, phone?, country, memo?, role:"originator"|"beneficiary" } }
```
Channel → routing-key **present-check** (not a prohibitive absent-check): WIRE⇒name+address;
EMT⇒email; AFT⇒country; P2P⇒handle/email/phone; CARD/CASH/CHEQUE⇒name-or-null. `counterparty.country`
populated on every leg. The **money-flow network** is derived at render by grouping txns by
`(account_ref, counterparty.entity_ref)` → directed weighted edges.

### `related_parties[]` + `ownership_edges[]` — the named BO graph
`related_parties[]` carry `{party_id, entity_ref, display_name, label, ownership_pct?, is_person}`.
`ownership_edges[] {src, dst, label, ownership_pct?}` — `src` is the owner; label vocab
`BENEFICIAL_OWNER / DIRECTOR_OF / OFFICER_OF / CONTROLS / OWNS`. **Multi-hop** so the
Northgate ← 1187442 Ontario Inc. ← 44-Holloway-caution-listed-address chain renders as a chain.
`ownership_pct` renders **"N pct", never "%"**.

### `resolution_edges[]` — the entity-resolution layer
`{between[entity_id…], status:"resolved"|"flagged"|"excluded", shared[{kind,value,normalized,strength}], reading, matched_register?, candidate_name?, cross_institution?}`.
- `resolved` — 2 entities + a shared identifier present on **both** (validator self-grounds on the matched
  field, normalized). Northgate's R1: the structured-drain beneficiary == the director, cross-institution.
- `flagged` — 1 entity + `matched_register` (a prior-STR hit). Northgate's R2: the inbound source Vesna
  Maric matches PSR-0001.
- `excluded` — the considered-and-rejected near-match (`shared:[]`). Lakeshore's John-Calderon-vs-James-Calder
  collision — proving resolution is exact-on-identifier, not fuzzy-on-name.

### `determination{}` — the test oracle, mapped to the live engine
```
{ crime_type,
  mechanism{atom,name,present,via:"fired",evidence[]},
  legs[ {atom,name,present,via:"fired"|"read"|"gathered",evidence[]} ],
  named_predicate_risk{named,value,source},
  mitigation{established:bool, basis},
  expected_verdict:"determination"|"needs_more_info"|"cleared",   // ORACLE only
  expected_disposition:"escalated"|"cleared",
  presentation_label:"file"|"documented_dismissal",               // DISPLAY label, mapped from atoms
  sufficiency_line,
  str_record{} | clearance_record{} }
```
The **`via`** tag distinguishes how an atom became present and is referentially grounded:
`fired`→an alert in `alerts[]`; `read`→a present entity/edge in the file; `gathered`→a present
`caution_list`/`prior_str` record. Throughput-vs-profile **reinforces the mechanism** — it is NOT a
counted leg.

## How the live engine computes the verdict (the T2 contract)

Over this evidence, the extended `evidence_requirements` engine derives atom presence:
- **mechanism ML-A1** from fired C2/C3.
- **ML-A7** (`via:fired` — C14 is a fired alert) present iff C14 fired **AND** the subject's
  `kyc.source_of_funds` is **not** established. Established source ⇒ ML-A7 absent (mitigated away) **and**
  `mitigation_established=true`.
- **ML-A4** (`via:read`) from a resolved network / ownership linkage present in the file.
- **ML-A5** (`via:gathered`) from a caution-list address hit on the ownership chain and/or a prior-STR
  match on an inbound source.
- **named predicate** read from the matched `prior_str_register.predicate`.

Then the **file bar is unchanged**: `mechanism + ≥2 independent legs + named predicate + no unrebutted
mitigation → determination` (Northgate). The **new affirmative-clear branch** fires only on the
not-sufficient path: `mechanism + legs absent + affirmative mitigation established + no named predicate
→ cleared` (Lakeshore). The clear is earned by **positive** evidence (established source + reconciled
flows + historical fit), never the absence of a hit, and never a loosened determination.

## Honesty (load-bearing)

Fully synthetic, badge always-on, a per-panel synthetic marker on the prior-STR panel. The contrast is
**qualitative** ("the network is the difference") — **no** catch-rate / precision / lift / Nx-as-performance
claim. Structured facts (ownership pct, country, predicate) are read from **this record**, never authored
by a model at render. "N pct", never "%". The dismissal is documented **by substance**, never branded a
"defensive filing".
