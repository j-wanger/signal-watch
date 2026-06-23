# PLAN-BRIEF — aml-casework: the C14 KYC-integrity grounding verifier (so v0.3 kyc cases SIGN)

> **A signal-watch → aml-casework handoff brief** (the sibling-brief pattern; cf.
> `docs/substrate-determination-signals-PLAN-BRIEF.md`). Authored in signal-watch; **executed in an
> aml-casework session**. signal-watch defines the *contract* it consumes; casework owns the grounding.
> Pinned to **aml-casework@157554b** (`feat/phase-1a-deterministic-verifiers`; HEAD "feat: adopt evidence
> contract v0.3 + cover the fincen advisory series" — verified live this session).
>
> **The core ask (one code change):** `_screen_c14_kyc_integrity` branch (a) must GROUND the substrate's
> NEW SoF-based C14 condition. Today it copies the OLD `_kyc_defect` (`cdd==EDD AND not source_of_funds`,
> `grounding_replay.py:340`) → any non-EDD elevated-obligation C14 alert fails closed → **kyc cases can't
> sign, only determine.** Broaden branch (a) to the substrate's `elevated_obligation` predicate; everything
> else (the six Class-G verifiers, C14 registration, party_ref resolution) is already in place.
>
> **Coherence anchor — read this carefully.** The EMIT companion is the substrate sign-path brief
> [`substrate-determination-signals-kyc-c14-PLAN-BRIEF.md`](./substrate-determination-signals-kyc-c14-PLAN-BRIEF.md)
> (pinned @443e4a6 — it carries the elevated_obligation predicate verbatim, identical to this brief by design);
> the spine is [`cross-pillar-sign-path-COHERENCE.md`](./cross-pillar-sign-path-COHERENCE.md). The OLDER
> consolidated `docs/substrate-determination-signals-PLAN-BRIEF.md` (pinned **aml-substrate@b53855c**, Phase 24,
> BEFORE the SoF re-key) is historical context only — its body still describes C14 as *tautological*
> (`cdd_level==EDD ⇔ risk_rating==HIGH`, lines 61–63); its STATUS block records Phase 25 @443e4a6 as executed,
> but its predicate text predates the re-key. **The authoritative coherence source is therefore the substrate
> CODE — `aml-substrate@443e4a6 kyc_integrity.py:50–58` — NOT any brief's prose.** The predicate block and
> bundle shape in THIS brief are made identical to that code (and to the EMIT companion's §3 `related_parties[]`
> contract). Execute off the code.

## Why this is the handoff (the coherence break, code-confirmed latent)

The substrate re-keyed C14 in Phase 25 onto a **broad** `elevated_obligation` predicate
(`aml-substrate@443e4a6 kyc_integrity.py:50-58`). casework's grounder still copies the **old narrow** one
(`grounding_replay.py:340`). The drift is **inert today** because the substrate emits zero C14 (its
`SCREENING_EMISSION_DETECTORS` is C8-only — `__init__.py:71`). **The instant C14 is flipped into the
emission set**, every C14 alert on a non-LOW-risk **OR** PEP **OR** sanctioned/adverse party that *isn't*
EDD will fail all three casework branches → a false violation → fail-closed → **every such kyc case cannot
sign.**

signal-watch already *determines* a kyc case on a single C14 alert + a named predicate risk (the kyc profile
is unit-tested in isolation — `evidence_requirements.py:427`), but it cannot *file* one: `run_case`
subprocesses casework, reads `consume_res['signed']`, and a fail-closed grounding refusal escalates instead
of files. **The kyc half of the §12 loop closes only when casework grounds the same predicate the substrate
fires.** This is the casework half — and it is the named "NEXT for this pillar" in casework's own uncommitted
`docs/capability-assertions-PLAN-BRIEF.md` Phase-60 status block ("reconcile the copied `_kyc_defect`
against the real detector").

## What exists today (code-verified @157554b; paths under `src/aml_casework/`)

- **Branch (a) is the OLD narrow predicate.** `grounding_replay.py:340`:
  `if cdd == _CDD_EDD and not party.get("source_of_funds"): return []` — i.e. `cdd_level==EDD AND no
  source_of_funds`. Constants `_CDD_EDD = "EDD"` / `_RISK_HIGH = "HIGH"` at `:139-140`.
- **Branches (b)/(c) ALREADY MATCH the substrate.** `grounding_replay.py:342` (HIGH risk not escalated:
  `risk == _RISK_HIGH and cdd != _CDD_EDD`) and `:344` (flagged without EDD:
  `flagged and cdd != _CDD_EDD`, where `flagged = sanctions_flag OR adverse_media_flag`, `:338`). These
  mirror the substrate's two fall-through branches (`kyc_integrity.py:59-62`) verbatim-in-spirit. **Only the
  SoF branch (a) diverged.** (NOTE: on the *current* substrate the sanctions/adverse-media flags are dead —
  never set True, `kyc_integrity.py:21-22` — so branch (c) grounds nothing today; it is kept for
  completeness and stays byte-unchanged.)
- **C14 is REGISTERED and party resolution is reference-by-path.** `_SCREENING = {"C7":…, "C8":…,
  "C14": _screen_c14_kyc_integrity}` (`grounding_replay.py:367-371`); dispatch resolves the party via
  `_resolve_party` (`:404-419` — a non-empty `party_ref` resolves ONLY by reference-by-path, no fallback to
  the account join → fail-closed on a non-resolving ref), then calls the screen (`replay_alert :442-445`,
  the resolve+call at `:444-445`). A capability in neither table is a violation (`:446-449`,
  grounded-or-dropped).
- **The screen reads the right pivots, fails closed correctly.** `_screen_c14_kyc_integrity`
  (`grounding_replay.py:319-349`): `party is None` → violation (`:332-333`); `cdd_level is None` →
  violation (`:335-336`); reads `risk_rating` (`:337`) and `sanctions_flag`/`adverse_media_flag` (`:338`);
  `cited_txns` unread (`:330` — C14 is txn-less). The defect-branch block is `:340-345`. The only logic edit
  is branch (a) at `:340`.
- **The screen's docstring (only) describes the OLD predicate.** `grounding_replay.py:324-325` documents
  branch (a) verbatim as "(a) an EDD-classified party with no documented source_of_funds." This is the ONE
  location carrying the old branch-(a) predicate text — and it re-derives the wrong rule for the next reader.
  Two OTHER C14 references are stale in *different* ways (see ask #3): `:27` is a generic "re-derives the
  screened DEFECT (substrate `kyc_integrity._kyc_defect`, copied)" reference (no predicate text), and `:136`
  is the module-constant comment carrying the OLD **signal id** `fin-2026-alert001:IND-04` (`:137`), not the
  branch-(a) predicate.
- **Signal-id divergence (a real reconciliation, cause identified).** casework's C14 comment cites
  `fin-2026-alert001:IND-04` (`grounding_replay.py:137`); the live substrate detector cites
  `fin-2025-a003:IND-09` (`aml-substrate@443e4a6 kyc_integrity.py:70`). The substrate's own docstring
  (`kyc_integrity.py:5-6`) records this as a **Phase-24 RE-GROUND** (public-benefits-fraud →
  professional-money-laundering); casework copied the pre-P24 id. **Canonical = `fin-2025-a003:IND-09`**
  (the substrate is the emit-side source of the cited grounding). The grounder logic never reads the
  signal_id (it re-derives party state), so this is documentation-only — but fix it in the same commit.
- **v0.3 is already accepted; the BO graph is read by no verifier yet.** `KNOWN_CONTRACT_VERSIONS =
  ("0.1", "0.2", "0.3")` (`contract.py:53`); an unvalidated version is a violation (`:396-397`). The
  `related_parties[]` block validates to the v0.2 PartyView bar — "the determination/network consume is
  signal-watch-side" (`contract.py:44-52`). So KYC-A2 (the optional ownership leg, `additional_legs_required=0`)
  needs no casework grounding work.
- **`pep_tier` AND `source_of_funds` are BOTH in the PartyView allow-list.** `PARTY_VIEW_FIELDS`
  (`contract.py:61-78`) is the 16-field allow-list; it includes `pep_tier` (`:66`) and `source_of_funds`
  (`:70`). So the broadened predicate can read `pep_tier` off the resolved party directly — **no hedge,
  no absence-handling needed** (the DRAFT's "treat a missing pep_tier as not-elevated" was wrong: the field
  is on the wire — verified present on the committed v0.3 bundles, e.g. a related-party row `pep_tier:'NONE'`).
- **TF has NO live path.** `CRIME_TYPES = ("money_laundering", "terrorist_financing", "kyc_integrity")`
  (`contract.py:103`) but `CRIME_BY_CAPABILITY` (`:108-117`) maps C2/C3/C4/C5/C7/C8/C15→money_laundering and
  C14→kyc_integrity ONLY — **no capability implies terrorist_financing.** A declared
  `crime_type='terrorist_financing'` is flagged by `validate_bundle`'s agree-with-cited-capabilities arm
  (`contract.py:526-534`, within the crime_type block `:515-535`) since no cited cap implies it.

## The ask (numbered, measurement-first, do NOT loosen the verifier)

### 1. VERIFIER-FIRST keystone: re-derive the predicate from the substrate CODE, never a loaded copy or the companion brief
Open `aml-substrate@443e4a6 kyc_integrity.py:50-58` and read the live `_kyc_defect` SoF branch directly.
Confirm the predicate below matches the live detector @HEAD (sibling pins drift, and the companion
*substrate brief* still documents the OLD tautology — code-verify, never trust a loaded fact or a sister
brief). STOP+REPORT if the live substrate predicate differs from this brief's; do not edit casework off a
stale copy. This is the casework instance of the briefs' shared "code-verify the sibling" discipline.

### 2. BROADEN branch (a) to the substrate's `elevated_obligation` predicate (the ONLY logic change)
Replace `grounding_replay.py:340` (`if cdd == _CDD_EDD and not party.get("source_of_funds")`) with the
full elevated-obligation predicate. The grounder re-derives the IDENTICAL party-state defect the substrate
fired (this block is **verbatim-coherent with `aml-substrate@443e4a6 kyc_integrity.py:50-57`**):

```
elevated_obligation = (risk_rating != "LOW") OR (cdd_level == "EDD")
                      OR (pep_tier not in {None, "NONE"}) OR sanctions_flag OR adverse_media_flag
# grounds (returns []) when:  elevated_obligation AND source_of_funds is None
```

- Add `_RISK_LOW = "LOW"` (mirror the `_CDD_EDD`/`_RISK_HIGH` copied-constant convention at `:139-140`) and
  read `pep_tier` off the resolved party — it IS in the v0.2/v0.3 PartyView allow-list (`contract.py:66`),
  so read it unconditionally; the existing `cdd_level is None` fail-closed guard (`:335-336`) is the only
  missing-pivot gate. Compare `pep_tier not in {None, "NONE"}` (`PEPTier.NONE` serializes to the string
  `"NONE"` — `aml-substrate enums.py:84`). COPY the substrate constants; **never** import `aml_substrate`
  (DESIGN forbids it — `grounding_replay.py:3-7`).
- Branches (b)/(c) at `:342`/`:344` stay byte-unchanged (they already match). This is **additive/broadening
  and regression-gated — the verifier is never loosened**: `cdd==EDD` is a strict SUBSET of
  `elevated_obligation`, so every old-branch-(a) ground still grounds; a clean party state still grounds
  NOTHING (`:346-349`), a non-resolving party / missing `cdd_level` still fails closed (`:332-336`). The
  change admits MORE faithful defects, it does not relax the gate (the rare case where broadening =
  faithfulness restoration).

### 3. UPDATE the stale C14 references in the SAME commit (re-scoped — three locations, three distinct edits)
- **`grounding_replay.py:324-325`** (the `_screen_c14_kyc_integrity` docstring) is the ONLY location with
  the old branch-(a) predicate text — rewrite "(a) an EDD-classified party with no documented
  source_of_funds" to the elevated-obligation predicate so the next reader re-derives the new rule.
- **`grounding_replay.py:27`** (the module docstring) references "the screened DEFECT (substrate
  `kyc_integrity._kyc_defect`, copied)" generically — add a one-line note that the copied condition is the
  SoF/elevated-obligation predicate (re-keyed Phase 25), NOT a predicate rewrite (there is no predicate text
  there to replace).
- **`grounding_replay.py:136-137`** (the `_CDD_EDD`/`_RISK_HIGH` constant comment) carries the OLD signal id
  `fin-2026-alert001:IND-04` — update it to the canonical `fin-2025-a003:IND-09` (the Phase-24 re-ground;
  cause noted in "What exists today"). This is the signal-id reconciliation, done — not a predicate rewrite.

  (Same-commit so docstrings can never trail the logic — the exact failure mode that produced this drift.)

### 4. DO NOT stamp; the predicate is label-independent by construction
The substrate sets `risk_rating`, `pep_tier`, and `source_of_funds` BLIND to the laundering label
(measured **lift < 1**, label-independent — a faithful KYC STATE, not a detection tell). The grounder
re-derives this OBSERVABLE state; it never reads or infers a label. A clean record that does not show the
defect the alert claims is a violation, not a pass (the never-loosen doctrine, `drafter_stub.py:21`).
(Provenance note: the precise figure "lift ≈ 0.8" lives in the substrate's
`docs/phase-25-determination-signal-emission.md:60,86`, not in the detector — whose docstring says
"lift ~ 1" at `kyc_integrity.py:19-20,49`; the substrate is internally inconsistent on the number. Cite
the Phase-25 doc for 0.8, or — preferred — say only "< 1, label-independent," which both sources support.
Do NOT attribute "0.8" to `kyc_integrity.py`.)

### 5. DEFER TF (do kyc only first; see TF path below)
TF is structurally deeper and shares ZERO live machinery. Do not touch `CRIME_BY_CAPABILITY` for TF in this
phase. kyc is the near-term close that proves the loop.

## The contract signal-watch consumes (no consume-side rework)

signal-watch's consume side is already in place and needs no change for the kyc close (verified
signal-watch@59a7417): `GROUNDABLE_CAPS ∋ C14` (`curate_workbench_cases.py:65`); `C14→kyc_integrity`
(`evidence_requirements.py:57`); `determine_case` lights KYC-A1 on a single C14 + a named risk
(pure sufficiency, never touches casework — selftest `evidence_requirements.py:427`); `run_case`
subprocesses casework over a file-handoff and reads `consume_res['signed']`. The cross-pillar agreement
contract:

| substrate EMITS (Phase 25 producer move) | casework GROUNDS (this brief) | signal-watch CONSUMES (already built) |
|---|---|---|
| a C14 party-leaf alert: `capability='C14'`, `txn_ids=()`, a `party_ref` → a `parties[]` PartyView; `grounding.signal_id` cited in `str_record.cited_signal_ids` | `replay_alert` resolves the party via `party_ref` (`:444`), re-derives the **identical** elevated_obligation+SoF predicate, returns `[]` (grounds) or a fail-closed violation | maps `C14 → KYC-A1` via the kyc profile — **iff the case is C14-pure** (see the dual-mapping caveat below); never re-checks the predicate |
| the PartyView pivots: `cdd_level`, `risk_rating`, `pep_tier`, `sanctions_flag`, `adverse_media_flag`, `source_of_funds` (label-stripped, all in `PARTY_VIEW_FIELDS`) | reads exactly these off the resolved party (`grounding_replay.py:334-340` after the broaden) | — |
| `related_parties[]` BO-graph, v0.3, optional — `{party_id, label∈RelationshipLabel, ownership_pct, is_person, risk_rating, cdd_level, pep_tier, sanctions_flag, adverse_media_flag}` (the substrate brief §3 shape, verbatim) | validated to the v0.2 PartyView bar, read by no verifier (`contract.py:44-52`) | optionally lights KYC-A2 via C15 (`additional_legs_required=0` → not required) |
| `crime_type` derives from the cited C14 cap | `CRIME_BY_CAPABILITY` C14→kyc_integrity (`contract.py:116`); a contradicting declared offence is a fail-closed violation (`contract.py:526-534`) | `_CRIME_BY_CAPABILITY` C14→kyc_integrity (`evidence_requirements.py:57`), identical |

**C14 is DUAL-MAPPED in signal-watch's profile — the minted kyc slice must be C14-pure.** `C14` is cited by
TWO atoms across TWO crime_types: `kyc_integrity` **KYC-A1** (`evidence-requirements.json:100`) AND
`money_laundering` **ML-A7** "Source of funds not established" (`:71`). The tie-break
`crime_type_for_capabilities` (`evidence_requirements.py:217`,
`max(..., key=lambda k: (counts[k], k != "kyc_integrity"))`) resolves toward `money_laundering` on a tie.
So a case firing C14 **alongside ANY ML-mapped capability** (C2/C3/C4/C5/C7/C8, or C15-as-ML) classifies
`money_laundering`, and the C14 alert lights **ML-A7 (a single leg)** — NOT KYC-A1 — and the case will NOT
determine (ML needs mechanism + ≥2 legs). **The clean `C14 → KYC-A1` contract holds ONLY for a C14-pure
kyc case** (optionally C14 + C15: `crime_type_for_capabilities(["C14","C15"])` returns `kyc_integrity` —
the 1-1 cap-count tie breaks toward kyc — so a C14+C15 case is still kyc and KYC-A2 lights). **The
substrate's minted kyc slice (substrate brief task #4 / Acceptance) must therefore fire ONLY C14
(optionally C15), with NO ML-mapped capability co-firing** — this constraint belongs in the substrate
brief; restated here because it gates whether casework's grounded C14 ever reaches KYC-A1.

**SIGN** = `replay_bundle` returns zero blocking violations for every cited alert; `record_signoff` classifies
`signed` iff clean AND complete. The six Class-G verifiers (`signoff.py:64-71`: contract → grounding_replay →
completeness → citation → corpus_grounding → narrative_grounding) run unchanged — only branch (a)'s
re-derivation changes.

## A TF grounding path (scoped — pursue ONLY after kyc proves the loop)

TF is closed-vocab-reachable but has NO live path anywhere: no substrate TF detector, no TF generation
(`CrimeType` "Reserved; unused in P1" with no `TERRORIST_FINANCING` member — `aml-substrate enums.py:116-126`;
7 ML typologies only — `gen/audit.py:32`); casework `CRIME_TYPES` carries `terrorist_financing`
(`contract.py:103`) but `CRIME_BY_CAPABILITY` maps no capability to it (`:108-117`); signal-watch
`_CRIME_BY_CAPABILITY` likewise leaves TF unmapped (which is *why* the TF slot is dropped at
`crime_type_for_capabilities`). The minimal TF slice = **3 coordinated edits, one per pillar, all keyed on
ONE new capability code** (name it e.g. `C-TF`):

- **SUBSTRATE:** a TF detector (`capability='C-TF'`) reading observable TxnView/PartyView features
  (label-blind, never-stamp) + TF generation so it has a cohort to fire on. Ships as a documented
  needs-behavior NULL if no label-independent separation emerges (the honesty-governor landing).
- **CASEWORK (this pillar's TF half):** add `C-TF → terrorist_financing` to `CRIME_BY_CAPABILITY`
  (`contract.py:108-117`) + a matching grounding assertion registered fail-closed — a **`ScreeningAssertion`**
  `(alert, cited_txns, party|None) -> list[str]` in `_SCREENING` if the TF signal is party/context-relative,
  or a plain **`Assertion`** `(alert, cited_txns) -> list[str]` in `_ASSERTIONS` if it is a txn-pattern
  (signatures at `grounding_replay.py:146-147`; empty list == grounds). COPY (never import) any substrate
  constant. A declared `crime_type='terrorist_financing'` without a cited cap that implies it is a contract
  violation in BOTH validators (honest NULL, never fabricated).
- **SIGNAL-WATCH:** add `C-TF → terrorist_financing` to `_CRIME_BY_CAPABILITY` + a `terrorist_financing`
  profile (≥1 mechanism atom citing `C-TF`) keeping the no-ghost invariant; inherits the synthetic +
  always-on badge constraints.

Propose TF only after kyc proves the loop.

## C3/C15 alignment (a separate frontier — NOTE only, not this brief)

Out of scope here, recorded for coherence. casework grounds the WEAKER re-derivation on two signals:
- **C3** `_assert_c3_funnel_fan` re-derives a COUNT of ≥5 outflows in 7d (`_MIN_FANOUT_COUNT = 5`,
  `grounding_replay.py:83`; honesty-gap comment `:78-84`); distinct-counterparty is NOT re-derivable because
  the real bundle carries `counterparty_ref=null` on cited outflows (documented honesty gap). The substrate
  `FunnelDetector` fires on BOTH fan-IN and fan-OUT across DISTINCT counterparties. Tightening needs
  Pillar-1 emission to carry counterparty refs — a cross-pillar follow-up, NOT a casework loosening.
- **C15** `_assert_c15_shell` grounds via a generic-trading-company NAME match OR low-net-retention
  throughput (`_MAX_NET_RETENTION_RATIO = 0.05`, `grounding_replay.py:106`); the throughput path is the
  WEAKER sub-signal, backing up the name match (`:98-106`).

This C3/C15 divergence is why composed fan-in mules fail closed (the defensibility climax — never loosen the
verifier to make them sign). It is reconciled in a sibling Pillar-1-emission session, independent of the C14
kyc close.

## Acceptance (the cross-pillar seam)

- The kyc-grounding selftest passes: a C14 party-leaf alert whose resolved party is `risk_rating != LOW` (or
  PEP, or sanctioned/adverse) AND `source_of_funds is None`, NOT necessarily EDD, **grounds** (returns `[]`)
  — and a clean elevated-obligation party (SoF present) still produces a violation. Run the casework
  `grounding_replay`/`signoff` selftests + `validate_bundle` on the vendored slice; the six Class-G verifiers
  pass unchanged on the existing committed fixtures (regression: no previously-grounding C14 case regresses —
  guaranteed because `cdd==EDD ⊂ elevated_obligation`).
- The three C14 references are reconciled in the same commit: `:324-325` describes the elevated-obligation
  predicate, `:27` notes the SoF re-key, `:136-137` cites `fin-2025-a003:IND-09`.
- **(work-to-do, not already-wired)** Once the substrate flips C14 into `SCREENING_EMISSION_DETECTORS` and
  the emit path composes a **party-leaf** alert (`txn_ids=()` + a resolving `party_ref` → a `parties[]`
  PartyView) — neither exists today; `SCREENING_EMISSION_DETECTORS` is C8-only — a substrate **C14-pure**
  kyc bundle **signs**: `replay_bundle` returns zero blocking violations, `record_signoff` → `signed`.
- signal-watch re-vendors casework's reconciled commit + the substrate's C14 slice; `run_case` reads
  `consume_res['signed']=True` → `disposition='file'`; the kyc half of §12 closes (DETERMINE is already
  reachable on the unit-tested profile; SIGN unlocks here). When re-vendoring, update
  `curate_workbench_cases.py:57 SUBSTRATE_HEAD` to the post-emission substrate commit (currently pinned
  `443e4a6`, the pre-emission Phase-25-close) so the slice doesn't carry a stale "C8-only emission" implied pin.

## Honesty governor

- **Never loosen the verifier** (`drafter_stub.py:21`): broadening branch (a) admits MORE faithful defects —
  it does not relax the gate (`cdd==EDD ⊂ elevated_obligation`). A clean record still grounds nothing; a
  non-resolving party / missing pivot still fails closed. The composed-mule fail-closed refusal stays the
  defensibility climax.
- **Grounds the OBSERVABLE, never a stamp:** the grounder re-derives the party-state predicate (risk/PEP/SoF/
  flags), all assigned BLIND to the laundering label upstream (lift < 1, label-independent). It reads no
  label and infers none. A faithful KYC STATE, not a detection tell.
- **No-import / copied-constant discipline:** every substrate constant is COPIED, not imported
  (`grounding_replay.py:3-7`) — which is a manual reconciliation obligation. This brief's existence IS that
  obligation discharged once; add a reconciliation-checklist line ("re-verify the copied SoF predicate
  against the live detector @HEAD whenever the substrate re-keys C14") so the same drift can't recur
  silently. The six Class-G verifiers ground ATOMS against their source; they do NOT verify the copied
  predicate against the live detector — that coherence is UNGUARDED by construction (`check_corpus_drift`
  covers only the verbatim corpus flag).
- **No catch-rate / precision / lift / % claim** anywhere; the substrate is single-signal-separable, this is
  determination-BREADTH (a kyc case can sign), not detection difficulty.

## Pins / provenance

- aml-casework @ **157554b** (`feat/phase-1a-deterministic-verifiers`; HEAD "feat: adopt evidence contract
  v0.3 + cover the fincen advisory series"). Working tree was dirty this session (3 `.claude/hooks/*.sh` +
  `docs/capability-assertions-PLAN-BRIEF.md` uncommitted; no git remote — local-only). Re-verify HEAD before
  executing.
- Coherence anchor = **aml-substrate CODE @443e4a6** (Phase 25; the SoF-keyed `elevated_obligation` C14
  predicate at `kyc_integrity.py:50-58`, `signal_id="fin-2025-a003:IND-09"` at `:70`). The companion
  **`docs/substrate-determination-signals-PLAN-BRIEF.md`** is pinned to the OLDER **@b53855c** and its
  "What exists today" body still describes C14 as tautological — do NOT execute off it for the predicate;
  it carries its own predecessor-correction note to re-key that body to 443e4a6.
- signal-watch consume side @ **59a7417**: `curate_workbench_cases.py:65` (GROUNDABLE_CAPS ∋ C14),
  `:57` (SUBSTRATE_HEAD pinned 443e4a6), `evidence_requirements.py:57` (C14→kyc_integrity), `:217`
  (the kyc-disfavoring tie-break), `evidence-requirements.json:71` (C14→ML-A7) / `:100` (C14→KYC-A1) /
  `:108` (KYC-A2→C15), `serve_workbench.py` `determine_case`/`run_case` (subprocess file-handoff, no
  import; dists byte-frozen); vendored casework @ `vendor/aml-casework/VENDORED_AT` commit 157554b.
- Load-bearing casework file:lines (this session): `grounding_replay.py:340` (branch a, the edit),
  `:342`/`:344` (branches b/c, unchanged), `:139-140` (constants), `:146-147` (the two assertion
  signatures), `:319-349` (`_screen_c14_kyc_integrity`), `:354-360`/`:367-371` (the two registries),
  `:404-419` (`_resolve_party`), `:422-449` (`replay_alert` dispatch + fail-closed), `:324-325` (the EDD
  branch-(a) docstring — the predicate rewrite), `:27` (generic copied-ref note), `:136-137` (the OLD
  signal id), `:78-84`/`:98-106` (C3/C15 honesty gaps); `contract.py:44-52` (related_parties to v0.2 bar),
  `:53` (KNOWN_CONTRACT_VERSIONS), `:61-78` (PARTY_VIEW_FIELDS incl. pep_tier `:66`, source_of_funds `:70`),
  `:103` (CRIME_TYPES incl. TF), `:108-117` (CRIME_BY_CAPABILITY, no TF cap), `:396-397` (unknown-version
  violation), `:515-535` (crime_type block; `:526-534` the agree arm); `signoff.py:64-71` (the six Class-G
  verifiers); `drafter_stub.py:21` (never-loosen doctrine).
- Substrate-side provenance: `kyc_integrity.py:50-58` (the predicate), `:59-62` (branches b/c), `:70`
  (canonical signal_id), `:19-20,49` (detector says "lift ~ 1"), `:21-22` (sanctions/adverse flags dead),
  `__init__.py:71` (SCREENING_EMISSION_DETECTORS C8-only); `docs/phase-25-determination-signal-emission.md:60,86`
  (the "lift ≈ 0.8" figure — the substrate-internal inconsistency vs the detector docstring);
  `enums.py:84` (`PEPTier.NONE="NONE"`), `:116-126` (CrimeType, no TF member); `gen/audit.py:32` (7 ML
  typologies).
- **Signal-id reconciliation (resolved):** canonical = `fin-2025-a003:IND-09` (substrate `kyc_integrity.py:70`,
  the Phase-24 re-ground per `:5-6`); casework `:137` carries the pre-P24 `fin-2026-alert001:IND-04` →
  update to canonical in ask #3. Non-blocking for grounding (the grounder never reads the signal_id) but
  fixed in the same commit.
