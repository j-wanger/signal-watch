# Cross-pillar sign-path COHERENCE — the C14/kyc seam (the single source of truth)

> **What this is.** The one doc that ties the two §12 sibling handoff briefs together so they
> cannot drift apart. The C14/kyc seam touches all three pillars; each brief owns its own pillar's
> ask, but the *firing condition* and the *bundle shape* are SHARED — and the shared parts have
> already bitten once (see "The ONE shared C14 condition" below). When the two briefs disagree, the
> arbiter is the **substrate CODE @443e4a6**, never either brief's prose.
>
> **STATUS (2026-06-23 — EMIT · GROUND · CONSUME all DONE).** **EMIT** — aml-substrate Phase 26
> @**f15c241** (C14 in `SCREENING_EMISSION_DETECTORS`; txn-less party-leaf via `Alert.party_ref`).
> **GROUND** — aml-casework Phase 14 @**bf15535** (`_screen_c14_kyc_integrity` broadened to the full
> `elevated_obligation` predicate; C14 cases SIGN). **CONSUME** — signal-watch Phase 72 (re-pin +
> re-vendor; the §12 KYC loop closes from a real signal — KYC-A1 = C14 alone). **DISCOVERED CROSS-PILLAR
> FRONTIER (the named follow-on):** casework's foundational no-transactions contract blocks a *purely*
> txn-LESS C14 party-leaf bundle from SIGNING — the determination closes, the signature is
> contract-blocked (fails-CLOSED with the honest `bundle: no transactions` reason; txn-BEARING C14
> cases sign). The fix is a casework follow-on: relax the contract for a `kyc_integrity` filing, OR drop
> `transaction_details` from the kyc STR profile.
>
> **Pins (current as of Phase 72).** aml-substrate **@f15c241** (Phase 26) · aml-casework **@bf15535**
> (Phase 14; vendored into signal-watch at this commit) · signal-watch **Phase 72**.
>
> **The two briefs this consolidates (both authored in `signal-watch/docs/` this session):**
> - SUBSTRATE / EMIT ask → [`substrate-determination-signals-kyc-c14-PLAN-BRIEF.md`](./substrate-determination-signals-kyc-c14-PLAN-BRIEF.md)
>   (emit C14 + mint a kyc case slice; the live-remainder successor to the consolidated
>   [`substrate-determination-signals-PLAN-BRIEF.md`](./substrate-determination-signals-PLAN-BRIEF.md))
> - CASEWORK / GROUND ask → [`casework-c14-kyc-grounding-PLAN-BRIEF.md`](./casework-c14-kyc-grounding-PLAN-BRIEF.md)
>   (broaden the copied `_kyc_defect` branch (a) to the live `elevated_obligation` predicate so kyc cases SIGN)

---

## §12 sign-path state — what "close the kyc loop" means

The §12 determination loop is **EMIT → GROUND → DETERMINE → SIGN**. For kyc:

- **DETERMINE — closed by signal-watch Phase 71.** The `kyc_integrity` profile is built, unit-tested,
  and reachable: a single fired C14 alert lights `KYC-A1` (mechanism), and with a human-named
  predicate risk the sufficiency rule (`mechanism_required=1, additional_legs_required=0,
  named_predicate_risk_required=true`) licenses the determination. **No consume-side code remains.**
- **SIGN — DONE (Phase 72), with one residual frontier.** casework Phase 14 @bf15535 broadened
  branch (a) to the live `elevated_obligation` predicate AND the substrate Phase 26 @f15c241 emitted
  C14 + minted a kyc slice — vendored TOGETHER (re-vendor preserved the ML signings; 0 regressions).
  **txn-BEARING C14 cases now SIGN.** The RESIDUAL: a *purely* txn-LESS C14 party-leaf bundle still
  fails-CLOSED at casework's foundational no-transactions contract (`bundle: no transactions`, fires
  before the C14 verifier) — surfaced via the honest e2e_note, never loosened. In the slice 2 of 6
  kyc cases sign. The named follow-on (casework): relax the contract for a `kyc_integrity` filing, OR
  drop `transaction_details` from the kyc STR profile.

So: Phase-71 closed "determine"; Phase-72 closed "sign" for txn-bearing C14 (the residual txn-less
signing path is the one open frontier). **TF is deferred** — closed-vocab-reachable but no live path in any pillar (no
substrate detector, no casework cap-map, signal-watch `_CRIME_BY_CAPABILITY` leaves it unmapped). Do
kyc first; TF is a strictly later, fully serial 3-pillar follow-on.

---

## The 3-column contract: substrate EMITS | casework GROUNDS | signal-watch CONSUMES

| capability | substrate EMITS | casework GROUNDS | signal-watch CONSUMES |
|---|---|---|---|
| **C14 / kyc** | a **txn-less party-leaf alert** (`txn_ids=()`, `party_ref` → a `parties[]` PartyView, `signal_id='fin-2025-a003:IND-09'`) when the elevated_obligation predicate is true. **Not emitted yet** — held out of `SCREENING_EMISSION_DETECTORS` (C8-only today); the ENABLING change is the flip + minting a C14-bearing kyc slice (the committed 342 carry ZERO C14). | re-derives the **IDENTICAL** predicate over the resolved party (`_screen_c14_kyc_integrity` → `_resolve_party` by `party_ref`, no account-join fallback). Returns `[]` (grounds) or a fail-closed violation. **Reconcile required:** branch (a) must broaden (see below). C14 is registered in `_SCREENING`; the six Class-G verifiers run unchanged. | maps `C14 → kyc_integrity` (`_CRIME_BY_CAPABILITY`) → lights `KYC-A1`. `GROUNDABLE_CAPS` already contains C14; `determine_case` is pure sufficiency. **CAVEAT (dual-map):** C14 also cites the money_laundering atom **ML-A7**, and `crime_type_for_capabilities` tie-breaks toward `money_laundering`. So the minted kyc slice MUST fire **only** C14 (optionally C15→KYC-A2) with **no** ML-mapped cap co-firing — else it classifies ML and C14 lights ML-A7 (a single leg), not KYC-A1, and the case will NOT determine. |
| **C1** (ML-A6, anticipated-vs-actual) | **measured NULL — no detector.** `ExpectedActivity` IS generated per party (`population.py`), but C1 is documented as suppressed by the P21 dormancy and would double-count C8 — the gap is a **DETECTOR**, not data. | nothing to ground until a C1 detector emits. | `_CRIME_BY_CAPABILITY` maps `C1`? **No** — C1 is not in the offence map; ML-A6 (`evidence=['C1']`) is an internal mitigation atom, lit only by a fired C1 signal. Unreachable until substrate ships a non-tautological C1 detector. |
| **C7** (ML-A3, peer/business-activity anomaly) | a detector EXISTS (`BusinessActivityAnomalyDetector`, screening class) but is **not emitted** — and parametrically narrow (`PEER_ROBUST_Z=8.0`, `MIN_COHORT=30`, product_type cohort sparse; C7-broaden deferred, C8 covers ML-A3). | `_screen_c7_peer_anomaly` registered in `_SCREENING`; grounds the re-derivable $25k inflow floor, names the peer-cohort core as screening-lineage (never faked as a replay). | maps `C7 → money_laundering` → lights ML-A3. Reachable the moment a broadened C7 emits; today ML-A3 is carried by **C8** (which IS emitted). |
| **TF** (terrorist_financing) | **NO live path.** `CrimeType` enum "unused in P1"; the 7 generated typologies are all ML; no TF detector, no TF cohort. | `CRIME_TYPES` lists `terrorist_financing` but **no capability maps to it** (`CRIME_BY_CAPABILITY` has C14→kyc only). | `_CRIME_BY_CAPABILITY` leaves TF **unmapped** — which is WHY the TF slot is dropped at `crime_type_for_capabilities`. No TF profile exists. |
| | TF needs ONE new cap (e.g. **C-TF**) coordinated across all three: a label-blind substrate detector + TF generation (ship a documented needs-behavior NULL if no label-independent separation emerges — never re-express an ML tell) | + `C-TF → terrorist_financing` in `CRIME_BY_CAPABILITY` + a fail-closed assertion (copied, never imported) | + `C-TF → terrorist_financing` + a `terrorist_financing` profile with ≥1 mechanism atom citing C-TF (keep the no-ghost invariant) |

---

## The ONE shared C14 condition (verbatim — the anti-drift guard)

All three pillars MUST key C14 on the SAME firing condition — stated as the **observable party-state
defect, never a stamped label**. This is the substrate's Phase-25 re-keyed `_kyc_defect` SoF branch
(verified live `kyc_integrity.py:50-58`):

```
elevated_obligation AND party.source_of_funds is None
  where elevated_obligation = (risk_rating != LOW)
                           OR (cdd_level == EDD)
                           OR (pep_tier not in {None, NONE})
                           OR sanctions_flag
                           OR adverse_media_flag
```

plus the two unchanged fall-through branches both repos already agree on:

```
(b) risk_rating == HIGH        AND cdd_level != EDD
(c) (sanctions OR adverse)     AND cdd_level != EDD
```

The predicate is **label-INDEPENDENT by construction** — risk tier, PEP tier, and the SoF draw are all
assigned BLIND to the laundering label, so this is a faithful KYC STATE (a determination leg), NOT a
detection tell. The detector docstring records the honesty governor as **lift ~ 1** (`kyc_integrity.py`);
`DESIGN.md` carries the precise measurement **≈ 0.8** — both say `< 1`, never-stamp held. (These two
numbers are a substrate-INTERNAL inconsistency to reconcile substrate-side; cite `DESIGN.md` for the
figure, or simply say "< 1, label-independent.")

**THIS EXACT MISMATCH BIT IN PHASE 71 — and is the seam's anti-drift guard.** Casework's COPIED branch
(a) is still the OLD narrow predicate (verified live `grounding_replay.py:340`):

```
if cdd == _CDD_EDD and not party.get("source_of_funds"): return []   # NARROW — EDD-only
```

`cdd == EDD` is a strict SUBSET of `elevated_obligation`. Branches (b)/(c) already match verbatim-in-spirit
across both repos — **only the SoF branch diverged.** Today the drift is INERT (substrate emits zero
C14 — C8-only emission set), so nothing fails yet. **The instant C14 flips into
`SCREENING_EMISSION_DETECTORS`, every C14 alert on a non-LOW-risk / PEP / sanctioned party that ISN'T
EDD fails branches (a)/(b)/(c) → false-violation → fail-closed → that kyc case CANNOT sign.**

> **Why this is unguarded (the structural root cause).** Casework COPIES the substrate predicate (DESIGN
> forbids importing `aml_substrate`); the six Class-G verifiers ground ATOMS against their source, NOT
> casework's copied logic against the live detector. `check_corpus_drift` covers only the verbatim corpus
> flag, not the copied `_kyc_defect`. **This drift can recur silently on any future substrate re-key.**
> GUARD (carry in BOTH briefs): *"re-verify the copied `_kyc_defect` against the live detector @HEAD
> whenever the substrate re-keys C14"* — and the casework reconcile task must re-derive the predicate
> from substrate code @pinned-HEAD, never from the loaded copy. Broadening branch (a) is **faithfulness
> restoration, not verifier loosening** (a clean party state still returns the violation).

---

## Dependency sequencing

**CASEWORK reconcile FIRST (the keystone, gates the substrate emission), then SUBSTRATE emit, then
SIGNAL-WATCH re-vendor.** The producer/adopter split holds throughout: substrate owns build/emit,
casework owns the grounding contract, signal-watch owns the determination contract it consumes — the
file-handoff boundary (no cross-pillar imports; dists byte-frozen) is never crossed.

1. **CASEWORK reconcile** — no dependency; do first or in parallel. Broaden `grounding_replay` branch (a)
   from `cdd==EDD AND not source_of_funds` to the full `elevated_obligation AND source_of_funds is None`.
   Additive, regression-gated, verifier never loosened. Also: update the stale docstring at
   **`grounding_replay.py:324-325`** (the only line carrying the EDD-only branch-(a) text), and align the
   stale signal_id at **`grounding_replay.py:137`** (`fin-2026-alert001:IND-04` → the canonical
   **`fin-2025-a003:IND-09`**, a Phase-24 re-ground the casework copy missed). This MUST land before the
   substrate emits C14, else every kyc case fails-closed.
2. **SUBSTRATE emit** — depends on #1 being landed/agreed. Flip C14 into `SCREENING_EMISSION_DETECTORS`
   and mint a kyc case slice whose alerts satisfy the ONE predicate (`txn_ids=()`, `party_ref` set,
   PartyView exposing `cdd_level/risk_rating/pep_tier/sanctions_flag/adverse_media_flag/source_of_funds`).
   **The slice must fire ONLY C14** (optionally C15→KYC-A2) with no ML-mapped cap co-firing, or it
   classifies money_laundering (see the dual-map caveat). The SoF FIELD already exists (@443e4a6, gen-
   unfreeze #7) — emitting C14 composes from existing PartyView state, so likely NO `gen/` touch / no
   freeze re-baseline; if any `gen/` byte moves it is a conscious `--write` + a separate bisectable commit.
3. **SIGNAL-WATCH adopt** — depends on #1 AND #2. Re-vendor casework's reconciled commit + the substrate's
   C14-bearing slice TOGETHER (never the emission alone). Re-curate. **No consume-side code rework**
   (`GROUNDABLE_CAPS` already has C14; `determine_case` already maps it). The kyc half of §12 closes —
   DETERMINE is already reachable; SIGN unlocks. (Update the `SUBSTRATE_HEAD` pin/comment in
   `curate_workbench_cases.py` to the post-emission commit so it doesn't imply the C8-only emission set.)

**TF** is a strictly later, fully serial follow-on (3 coordinated pillar edits keyed on one new cap) —
only after kyc proves the loop. A declared `crime_type` with no cited capability that implies it is a
contract violation in BOTH validators (honest NULL, never fabricated).

---

## Reconciliation checklist (run on any C14 / atom / cap-map edit)

- [ ] **Re-verify the copied `_kyc_defect` against the live substrate detector @HEAD** (the unguarded
      cross-field coherence — the dominant trap). Derive from code, not from any brief's prose.
- [ ] Casework branch (a) broadened to `elevated_obligation` **before/with** the substrate emission flip —
      vendor the two TOGETHER, never the emission alone.
- [ ] Stale docstring `grounding_replay.py:324-325` + signal_id `grounding_replay.py:137` updated in the
      same commit as the branch edit (additive; verifier never loosened).
- [ ] Minted kyc slice fires ONLY C14 (no co-firing ML cap) so it classifies `kyc_integrity`, not ML.
- [ ] `evidence_requirements` selftest (no-ghost-capability + banned-token honesty sweep) + casework
      `validate_bundle` green; every new profile atom `basis='chosen-not-measured'`.
- [ ] Substrate brief's stale "What exists today" / Pins corrected to **443e4a6 / v0.3 / SoF-present**
      (it still reads b53855c / v0.2 / SoF-absent / C14-tautological in places) — state the remainder as
      **emission + slice**, not data.
- [ ] C14 lift number reconciled substrate-internally (detector docstring `~1` vs `DESIGN.md ≈0.8`); the
      coherence anchor for the predicate is the substrate CODE @443e4a6, not either brief.
