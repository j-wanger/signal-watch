# PLAN-BRIEF — aml-substrate: the determination-signal SIGN-PATH remainder (kyc → C14 emission)

> **A signal-watch → aml-substrate handoff brief** (the Phase-55–58 sibling-brief pattern). Authored in
> signal-watch; **executed in an aml-substrate session** (tightly coordinated with an aml-casework reconcile —
> see Sequencing). signal-watch defines the *contract* it consumes; the substrate owns the build/emit.
> Pinned to **aml-substrate@443e4a6** (Phase 25 close; feature code `ab7b34a` — verified live this session,
> clean tree).
>
> **The coherence anchor is the substrate CODE @443e4a6, NOT any brief's prose.** The GROUND companion is
> [`casework-c14-kyc-grounding-PLAN-BRIEF.md`](./casework-c14-kyc-grounding-PLAN-BRIEF.md) (it grounds this
> emission — the C14 predicate is verbatim-identical there by design); the spine tying both together is
> [`cross-pillar-sign-path-COHERENCE.md`](./cross-pillar-sign-path-COHERENCE.md). The PREDECESSOR
> `docs/substrate-determination-signals-PLAN-BRIEF.md` (this brief is its live-remainder successor) is pinned
> to an OLDER substrate commit (`b53855c`, Phase 24) and its body still describes C14 as the OLD EDD tautology
> — execute the C14 predicate off `kyc_integrity.py:50-58` @443e4a6 (reproduced verbatim below), never off
> that brief's stale text. This
> brief is the LIVE-REMAINDER SUCCESSOR to it: that brief's parts 1–3 (the BO graph `related_parties[]`, the
> generated `source_of_funds` field, the C14 re-key) + the ML two-leg path **LANDED** — substrate Phase 25
> emitted them and signal-watch Phase 71 consumed them (a per-customer merge reaches the **≥2-leg ML
> determination bar from real signals**: C8 ML-A3 + C15 ML-A4). What that brief left **OPEN is the SIGN path
> for a kyc case**: the substrate emits **zero C14** to bundles, so `kyc_integrity` (KYC-A1) never lights from
> a real signal and no kyc case can DETERMINE — let alone SIGN. This brief is that remainder: **emit C14**,
> dispose **C1** (measured null) and broaden **C7** honestly, and mint a **kyc (and later TF) case slice** so
> a kyc case reaches signal-watch's consume path AND grounds in casework.

## Why this is the handoff (the kyc half of §12)

The §12 sufficiency loop has two independent gates a case must clear end-to-end:
**DETERMINE** (signal-watch, pure: does the bundle carry the licensing atoms?) and **SIGN** (aml-casework, the
six Class-G verifiers re-derive every cited alert from the bundle). The **ML half closed** (Phase 25 + 71); the
**kyc half is blocked at the substrate-emission boundary**. All 342 committed cases classify
`money_laundering` — **zero carry a C14 alert** (verified: committed bundle capabilities are C2/C3/C4/C5/C8/C15
only — no C14, no C7), so the authored-but-unexercised `kyc_integrity` profile never fires and the
determination control is exercised on only half its profile surface.

The blocker is **producer-side and singular**: the substrate has *re-keyed* C14 onto a real, label-independent
KYC state (`source_of_funds` is generated; the detector fires a faithful minority) **but holds C14 out of the
emission set** — `SCREENING_EMISSION_DETECTORS` is C8-only — *precisely because* a txn-less party-leaf alert
needed casework's reference-by-path grounding, which now **exists**. So the emission is safe to flip — **IFF the
one casework coherence break is reconciled first** (below). Closing the kyc half is what proves the *whole*
sufficiency loop runs end-to-end on a non-ML offence, not just ML.

## What exists today (code-verified @443e4a6; sibling paths under `src/aml_substrate/`)

- **The C14 detector already fires on a REAL, non-tautological KYC state.** `monitor/detectors/kyc_integrity.py`
  `_kyc_defect` (lines 50-58) was Phase-25 re-keyed off the dead EDD tautology onto the generated
  `source_of_funds`. The primary branch (lines 50-57) fires when **`elevated_obligation AND
  party.source_of_funds is None`**, where:

  ```
  elevated_obligation = (risk_rating != LOW)
                        OR (cdd_level == EDD)
                        OR (pep_tier not in {None, NONE})
                        OR sanctions_flag
                        OR adverse_media_flag
  ```

  Two fall-through branches (lines 59-62): (b) HIGH risk not escalated to EDD, (c) sanctions/adverse flag
  without EDD. **Honesty: the substrate is internally inconsistent on the lift figure** — the detector
  docstring (`kyc_integrity.py:19-20, 49`) says "lift ~ 1"; `DESIGN.md:576` says "lift ≈ 0.8". Both express
  the SAME governor: **lift < 1, label-independent — a faithful KYC STATE (the ML-A7 / KYC-A1 leg), not a
  detection tell.** Use the qualitative form ("<1, label-independent") and, if a number is cited, cite
  `DESIGN.md:576` (not the detector file, which says ~1) — and reconcile the substrate to one figure as a
  cleanup. NOTE: the `sanctions_flag` / `adverse_media_flag` escalation branches are **dead on the current
  substrate** (never set True per `kyc_integrity.py` docstring) — they ground nothing today; only the
  `risk != LOW` / `cdd == EDD` / `pep_tier` legs of `elevated_obligation` can actually fire.
- **`source_of_funds` is already GENERATED** (gen-unfreeze #7). `gen/population.py:201`
  `_source_of_funds(_sof_rng(seed, pid), affluent=…)` via an **isolated per-party sub-rng** (lines 130-138 —
  the P21 minimal-blast pattern; only the `persons.source_of_funds` column is new); ~12% return `None` (the gap
  C14 screens), keyed never on the label. **This corrects the companion brief's stale "no `gen/` assignment"
  claim** (its part 1 is DONE).
- **C14 is NOT emitted to bundles.** `monitor/detectors/__init__.py:71`
  `SCREENING_EMISSION_DETECTORS = (IncomeMismatchDetector(),)` — **C8-only**; the comment (lines 64-71) names
  C14 a *deliberate* non-emission because a txn-less party-leaf alert "needs the casework-side
  reference-by-path grounding extension before an emitted C14 bundle has a consumer." `kyc_integrity.py:90`
  emits `txn_ids=()`. **The blocker the comment names is now resolved consumer-side** (casework `_resolve_party`
  via `party_ref`). The Detection a fired C14 carries account/party lineage but **NOT a `party_ref`** — task #1
  is the emit path that composes the `party_ref`-bearing party-leaf alert (see The ask; this is work-to-do, not
  already-wired state).
- **The BO graph already projects to `related_parties[]`.** `gen/population.py:263-281` mints
  `BENEFICIAL_OWNER` + `DIRECTOR_OF` `RelationshipEdge`s with `ownership_pct`; `monitor/evidence.py:49`
  `CONTRACT_VERSION = "0.3"` emits the additive `related_parties[]` block (verified on the wire: every
  committed bundle is `contract_version=0.3` with a top-level `related_parties[]` list — the ML-A4 leg /
  optional KYC-A2 ownership leg).
- **C7 is sparse; C1 has no detector.** `monitor/detectors/business_activity.py:28-31` cuts on a robust
  `product_type` cohort outlier (`PEER_ROBUST_Z=8.0`, `$25k` floor, `MIN_COHORT=30`); finer occupation/NAICS
  cohorts await a richer PartyView join (`DESIGN.md:578` — *C7-broaden deferred, C8 covers ML-A3*). **No C1
  detector exists** — `grep capability=='C1'` over `detectors/*.py` is empty; Phase 25 measured the illicit
  cohort's anticipated-vs-actual deviation **suppressed** by the P21 dormant-then-burst architecture (volume-C1
  re-expresses C8, timing re-expresses C6 → an honesty-governor double-count; `DESIGN.md:577` names the C8
  double-count, the C6 extension is consistent). `ExpectedActivity` itself **is** generated
  (`population.py:202-204`) — the null is a **DETECTOR null, not a data gap**.
- **TF has no live path anywhere.** `schema/enums.py:116-126` `CrimeType` is "Reserved; unused in P1" with no
  `TERRORIST_FINANCING` member; `gen/audit.py:32` `TYPOLOGIES` is 7 ML patterns only.

## The ask (one queue — kyc first; measurement-first per substrate doctrine; do NOT stamp emergence)

> **Sequencing keystone (read first):** aml-casework must reconcile its **copied** C14 grounding branch BEFORE
> (or in the same coordinated handoff as) the substrate flips the emission — else every emitted C14 alert on a
> non-EDD elevated-obligation party fails-closed and **no kyc case can sign**. That casework edit is *its* brief;
> this brief is the substrate producer half. Do not flip emission ahead of the reconcile landing/agreed.

### 1. FLIP C14 into the emission set (the singular producer move)
Add `KycIntegrityDetector()` to `SCREENING_EMISSION_DETECTORS` (`monitor/detectors/__init__.py:71`). The fired
`Detection` already carries `capability='C14'`, `txn_ids=()`, and the owning-party lineage; the emit path must
**compose** a **party-leaf alert** whose `party_ref` references a `parties[]` `PartyView` (reference-by-path, no
transaction) and whose `grounding.signal_id='fin-2025-a003:IND-09'` + `advisory_id` are cited in the bundle's
`str_record.cited_signal_ids`. The Detection today carries account/party lineage but **no `party_ref`** — the
`party_ref`-bearing alert is what this task builds; it is not present in the current C8-only emission set.
**This likely needs NO `gen/` touch** — the alert composes from existing PartyView state — so probably **no
freeze re-baseline**; if any `gen/` byte moves, make it a conscious `--write` in its own bisectable commit
(one-commit-per-gen-touching-task).

### 2. MINT a kyc_integrity case slice (the population to vendor)
The committed 342-case slice has **zero C14 and zero C7 alerts** (all `money_laundering`). Emit a slice whose
cases fire C14 on a PartyView satisfying the `elevated_obligation AND source_of_funds is None` predicate, so a
kyc case lands in the re-vendored population and exercises the `evidence-requirements.json` `kyc_integrity`
profile end-to-end.

> **CRITICAL — C14 is DUAL-MAPPED in signal-watch's consume side; the minted case MUST fire C14 ALONE.**
> In `data/workbench/evidence-requirements.json`, C14 is cited by **two** atoms across **two** crime_types:
> `kyc_integrity` KYC-A1 (line 100) **AND** `money_laundering` ML-A7 "Source of funds not established"
> (line 71). `crime_type_for_capabilities` (`evidence_requirements.py:217`) tie-breaks **toward
> money_laundering** on equal counts (`max(..., key=lambda k: (counts[k], k != "kyc_integrity"))` — for a 1-1
> tie, `k != "kyc_integrity"` ranks ML above kyc). **Verified empirically @59a7417:** `[C14] → kyc_integrity`,
> but `[C14, C15] → money_laundering` and `[C14, C8] → money_laundering`. So a C14 alert co-firing with ANY
> ML-mapped capability (C2/C3/C4/C5/C7/C8, **and C15** — C15 maps to ML, evidence-requirements.json:45) makes
> the case classify `money_laundering`; the C14 alert then lights **ML-A7 (a single leg)**, NOT KYC-A1, and an
> ML case needs mechanism + 2 legs → it will **not determine**. **The minted kyc case must fire ONLY C14**
> (no ML-mapped capability on the same subject), so it classifies `kyc_integrity` and C14 lights KYC-A1.
>
> A consequence for KYC-A2 (the ownership leg): KYC-A2's `evidence` is `["C15"]`, but a real C15 *alert*
> co-firing would flip the case to ML. KYC-A2 is `additional_legs_required=0` (**not required** for the kyc
> determination — a single C14 + a human-named predicate risk determines), so the kyc slice does **not** need
> it. If KYC-A2 is ever exercised, it must come via the **GATHER `gather_signal: "ownership"` path** (record-
> sourced), not a co-firing C15 alert.

### 3. C1 — dispose the measured null honestly (no detector)
**Do NOT build a volume-C1** — it re-expresses C8 (burst magnitude) and C6 (dormancy) and would double-count an
existing tell (an honesty-governor breach). Keep C1/ML-A6 a **documented measured null** under the P21 dormancy
architecture (the Phase-25 landing). The `ExpectedActivity` data exists; only a faithful *distinct* channel-mix
facet would be new, and that is speculative/low-priority. Action here = **document, not detect**.

### 4. C7 — broaden only if a label-independent finer cohort emerges (deferred)
C8 already covers ML-A3; broadening C7 to occupation/NAICS cohorts awaits a richer PartyView join and is a
candidate follow-on, not on the near-term kyc path. Report `needs-behavior` if pursued; never tune to labels.

### 5. TF — DEFER (a strictly later, fully serial follow-on)
TF is structurally deeper than kyc and shares **zero** live machinery (no substrate TF detector, no TF
generation; casework `CRIME_TYPES` lists `terrorist_financing` but no capability maps to it; signal-watch
`_CRIME_BY_CAPABILITY` leaves TF unmapped). When pursued **after kyc proves the loop**, it is 3 coordinated
edits, all keyed on **one new capability code** (e.g. `C-TF`): a SUBSTRATE TF detector reading observable
TxnView/PartyView features (label-blind, never-stamp) + TF generation so it has a cohort to fire on (ship as a
documented needs-behavior NULL if no label-independent separation emerges — never author a TF leg that
re-expresses an existing ML tell); CASEWORK adds `C-TF→terrorist_financing` + a matching fail-closed grounding
assertion (copied, never imported); signal-watch adds `C-TF→terrorist_financing` + a `terrorist_financing`
profile with ≥1 mechanism atom citing `C-TF`. A declared crime_type with no cited capability that implies it is
a contract violation in both validators (honest NULL). **Propose TF only after kyc.**

## The contract signal-watch consumes (no consume-side rework)

signal-watch already has every consume-side piece for kyc — verified @59a7417: `GROUNDABLE_CAPS ∋ C14`
(`scripts/curate_workbench_cases.py:65`), `_CRIME_BY_CAPABILITY` maps `C14→kyc_integrity`
(`scripts/evidence_requirements.py:57`), and `determine_case` maps C14 to KYC-A1 via the kyc profile **for a
C14-pure case** (see the dual-mapping caveat in task #2). So:

| substrate emits | signal-watch consumes (already built) | casework grounds (after reconcile) |
|---|---|---|
| a **C14 party-leaf alert** (`capability='C14'`, `txn_ids=()`, a `party_ref` to a `PartyView`, signal cited), **with NO ML-mapped capability co-firing on the subject** | the case classifies `kyc_integrity`; `C14 → KYC-A1` lights; a single C14 + a human-named predicate risk **DETERMINES** the kyc case | `_screen_c14_kyc_integrity` resolves the party via `party_ref`, re-derives the **identical** `elevated_obligation AND source_of_funds is None` predicate → grounds (`[]`) or a fail-closed violation |
| the v0.3 `related_parties[]` BO-graph block (already emitted) | the case network view + the optional KYC-A2 ownership leg via the GATHER `ownership` signal (`additional_legs_required=0`, not required; a co-firing C15 alert would flip the case to ML) | the v0.3 block is validated to the v0.2 bar (read by no verifier — the determination consume is signal-watch's) |
| a `kyc_integrity` case in the slice | the unexercised `kyc_integrity` profile fires; `crime_type` derives from the cited C14 cap (C14-pure) | `crime_type_for` derives `kyc_integrity` from `CRIME_BY_CAPABILITY[C14]`; a contradicting declared offence is a violation |

The cross-pillar contract atom is the **C14 code AND its underlying party-state predicate**: the substrate
**fires** it, casework **re-derives the identical predicate**, signal-watch **maps the code** to KYC-A1 (for a
C14-pure case). signal-watch never re-checks the predicate; casework never imports the detector (it copies it —
the standing reconciliation obligation).

## Acceptance (the cross-pillar seam)

1. **Casework reconcile landed first** (its brief): `grounding_replay.py` branch (a) broadened from the old
   `cdd == _CDD_EDD and not source_of_funds` (line 340) to the full `elevated_obligation` predicate; the stale
   documentation updated in the same commit — the branch-(a) EDD phrasing is at **lines 324-325 ONLY** (rewrite
   to the elevated_obligation predicate), and a divergence/reconciliation note added at lines 27 and 136-137
   (these reference the copied `_kyc_defect` generically — they do NOT carry the predicate text); **line 137's
   stale signal id `fin-2026-alert001:IND-04` is realigned to the canonical `fin-2025-a003:IND-09`** (see The
   canonical signal id, below).
2. `SCREENING_EMISSION_DETECTORS` includes `KycIntegrityDetector()`; emitted C14 alerts carry `txn_ids=()`, a
   resolving `party_ref` to a `parties[]` `PartyView`, and a cited `fin-2025-a003:IND-09` grounding. (This emit
   path is built by task #1 — it does not exist in the current C8-only emission set.)
3. At least one `kyc_integrity` case appears in the slice; its fired C14 alert's PartyView satisfies the
   `elevated_obligation AND source_of_funds is None` predicate (a non-tautological state), **with no ML-mapped
   capability co-firing on that subject** so the case classifies `kyc_integrity` (not `money_laundering` via the
   ML-A7 tie-break). The firing leg must be `risk != LOW` / `cdd == EDD` / `pep_tier` — never the dead
   sanctions/adverse branches.
4. C1 ships as a documented measured null (no detector); C7 unchanged (or `needs-behavior` if broadened).
5. signal-watch re-vendors the casework-reconciled commit **and** the substrate C14-bearing slice **together**
   (never the emission alone); a C14-pure kyc case **DETERMINES** (single C14 + named risk) **and SIGNS**
   (casework replay returns zero blocking violations) → **the kyc half of §12 closes.**
6. The §13 four-null and A1 amount-family separability are **unchanged** (prove by byte-identity if `gen/`
   moved); no catch-rate / lift / pin-rise claim anywhere.

## The canonical signal id (declared, not left open)

The cited C14 grounding signal id is **`fin-2025-a003:IND-09`** — canonical per the live substrate detector
`kyc_integrity.py:70` @443e4a6 (S-KYC-INTEGRITY-SCREEN; the P24 re-ground from public-benefits-fraud →
professional-money-laundering, recorded in the substrate docstring). casework's copied docstring at
`grounding_replay.py:137` still cites the **pre-P24** id `fin-2026-alert001:IND-04` — a documentation drift, not
a grounding break (the grounder re-derives party state, never reads the signal id). The casework reconcile
(Acceptance #1) realigns line 137 to `fin-2025-a003:IND-09`. The substrate (emit side, source of the cited
grounding) is the authority for this value.

## Honesty governor

This brief adds **determination-BREADTH** (a non-ML offence reaches the loop) — **NOT** detection difficulty,
catch-rate, or lift. C14's lift is **<1, label-independent** (the substrate is internally inconsistent on the
exact figure — detector docstring "~1", `DESIGN.md:576` "≈0.8" — reconcile to one as a cleanup; cite
`DESIGN.md:576` if a number is used) — faithful *precisely because* it does not lift detection: a KYC STATE,
not a tell. Hold the **never-stamp firewall** — `source_of_funds` is keyed on observable
segment/per-source documentation, never `latent_role`/`illicit_income`/the label (`population.py:105-113`, made
structural by setting SoF before `emergence.designate`). Any C7/TF leg that can only fire on a stamp ships as a
documented needs-behavior NULL. **Detection-lift is RETIRED and the §13 composition north star is structurally
CLOSED** (P16 four-null) — do not propose chasing lift, composition-required, or P14. Verifier-first: the
keystone task re-verifies these code-claims @HEAD (sibling pins drift — code-verify, never reason from a loaded
fact) and STOP+REPORTs each leg's go/no-go `{additive-no-gen | gen-coupled | NULL}`; the plan does not depend on
any A-row being true — null-tolerant per leg.

## The cross-field coherence risk (the structural root cause — guard explicitly)

casework **COPIES** the substrate predicate (DESIGN forbids importing `aml_substrate`); the six Class-G
verifiers ground **atoms against their source**, NOT casework's copied logic against the live detector.
`check_corpus_drift` covers only the verbatim corpus *flag*, not the copied `_kyc_defect`. So the C14 SoF
divergence (casework branch (a) still `cdd==EDD`-only vs the substrate's broad predicate) is **today INERT** —
substrate emits zero C14 — but the instant emission flips, every C14 alert on a non-LOW-risk-OR-PEP-OR-flagged
party that isn't EDD would fail branches (a)/(b)/(c) → false-violation → fail-closed → **every such kyc case
can't sign**. This exact drift can recur silently on any future substrate re-key. **A second, narrower
manifestation: the PEP branch.** `pep_tier` is IN the v0.3 PartyView (verified in the committed bundles —
`pep_tier` present on parties and `related_parties[]`); the substrate predicate fires on `pep_tier not in
{None, NONE}`. If casework's branch (a) drops or hedges `pep_tier`, a C14 alert on a (`pep_tier != NONE`,
otherwise-clean, non-EDD) party fails-closed. The casework reconcile (its brief) must read `pep_tier` from the
PartyView; **as the producer-side guarantee, this brief's minted kyc-slice fires C14 via `risk != LOW` /
`cdd == EDD` / `pep_tier` and the substrate must confirm each cited party's PartyView carries the field casework
will read** (the slice MUST NOT depend on the dead sanctions/adverse branches). **GUARD:** a reconciliation
checklist line in BOTH briefs — *"re-verify the copied `_kyc_defect` (predicate AND the `pep_tier` read) against
the live detector @pinned-HEAD whenever substrate re-keys C14"* — and the casework verifier-first task
re-derives the predicate from substrate code @HEAD, never from the loaded copy. Run
`evidence_requirements --selftest` (no-ghost + banned-token sweep) and casework `validate_bundle` on any
atom/cap-map edit.

## Sequencing

1. **CASEWORK reconcile** (keystone — no dependency; do first / in parallel): broaden branch (a) to
   `elevated_obligation` (read `pep_tier`); rewrite the branch-(a) docstring at lines 324-325; add a divergence
   note at lines 27 and 136-137 and realign line 137's signal id to `fin-2025-a003:IND-09`. Additive,
   regression-gated, verifier never loosened (broadening branch (a) here is faithfulness RESTORATION — `cdd==EDD`
   is a subset of `elevated_obligation` — not loosening). Must land/agree **before** substrate emits C14, else
   every kyc case fails-closed.
2. **SUBSTRATE emit** (depends on #1): flip C14 into `SCREENING_EMISSION_DETECTORS`; build the `party_ref`-
   bearing party-leaf emit path; mint the C14-pure kyc case slice. Verifier-first task re-verifies this brief's
   code-claims @HEAD and ships each leg null-tolerant. SoF is already generated (#7 done) — emitting C14 likely
   needs **no** `gen/` touch (alerts compose from existing PartyView state), so probably no freeze re-baseline;
   if any `gen/` byte moves, a conscious `--write` in a separate bisectable commit. **Do NOT** `ruff --fix .` /
   `pre-commit run --all-files` (reformats frozen `gen/`); verify scoped + full `uv run pytest`.
3. **SIGNAL-WATCH adopt** (depends on #1 AND #2): re-vendor casework's reconciled commit + the substrate's
   C14-bearing slice; re-curate. `GROUNDABLE_CAPS ∋ C14` and `determine_case` already map it — **no consume-side
   code rework.** DETERMINE is already reachable on the unit-tested profile; SIGN unlocks → the kyc half closes.
   Update `curate_workbench_cases.py:57` `SUBSTRATE_HEAD` to the post-emission substrate commit (currently
   `443e4a6` is the pre-emission Phase-25-close; its narrative implies C8-only emission).

TF is a strictly later, fully serial follow-on (§5). The producer/adopter split holds throughout: substrate
owns the build/emit, casework owns the grounding contract, signal-watch owns the determination contract it
consumes; the file-handoff boundary (no cross-pillar imports, dists byte-frozen) is never crossed.

## Pins / provenance

- aml-substrate @ **443e4a6** (Phase 25 close; feature code `ab7b34a`; clean tree). Verified live this session:
  `kyc_integrity.py:50-58` (broad `elevated_obligation` predicate), `:70` (signal `fin-2025-a003:IND-09`),
  `:19-20/:49` (lift "~1" — inconsistent with DESIGN), `__init__.py:71` (`SCREENING_EMISSION_DETECTORS`
  C8-only), `evidence.py:49` (`CONTRACT_VERSION="0.3"`), `population.py:201` (SoF generated) + `:105-113`
  (never-stamp keying) + `:263-281` (BO edges), `business_activity.py:28-31` (C7 sparse), `enums.py:116-126` +
  `audit.py:32` (no TF), `DESIGN.md:576` (lift "≈0.8").
- aml-casework @ **157554b** (`feat/phase-1a-deterministic-verifiers`): `grounding_replay.py:340` branch (a)
  still `cdd==EDD`-only (the divergence); branch-(a) EDD docstring at **lines 324-325 only** (27 and 136-137 are
  generic copied-`_kyc_defect` references); `:137` stale signal id `fin-2026-alert001:IND-04` (→ realign to
  `fin-2025-a003:IND-09`); `contract.py:103/108-117` (TF in `CRIME_TYPES`, no TF capability);
  `KNOWN_CONTRACT_VERSIONS=('0.1','0.2','0.3')`. (The vendored copy in signal-watch `vendor/aml-casework/`
  is at this same `157554b` — pre-reconcile.)
- signal-watch consume side @ **59a7417** (verified ready, no rework): `scripts/curate_workbench_cases.py:65`
  (`GROUNDABLE_CAPS ∋ C14`) + `:57` (`SUBSTRATE_HEAD="443e4a6"`), `scripts/evidence_requirements.py:57`
  (`C14→kyc_integrity`) + `:217` (tie-break toward money_laundering — the C14 dual-mapping consequence),
  `data/workbench/evidence-requirements.json:68-71` (ML-A7 cites C14) + `:85-122` (the kyc profile, KYC-A1
  evidence `["C14"]`, KYC-A2 evidence `["C15"]`, `additional_legs_required=0`). Committed bundles carry no C14
  and no C7 (capabilities: C2/C3/C4/C5/C8/C15).
- **Companion brief:** `docs/substrate-determination-signals-PLAN-BRIEF.md` (parts 1–3 + ML legs LANDED). NOTE:
  its STATUS header (lines 11-19) is correct, but its "What exists today" (lines 48-66) + Pins (lines 131-134)
  sections are **internally stale** — they still cite `b53855c` / `CONTRACT_VERSION="0.2"` / `source_of_funds`
  absent / "C14 tautological", contradicting the committed `443e4a6` / v0.3 / SoF-present slice. **A reader who
  follows that brief's body would re-derive the OLD tautological C14 — so the coherence anchor is the substrate
  CODE @443e4a6, not that brief.** Correct those two sections of the companion before the next sibling session
  reads it as the queue (state the real gap as C14 *emission* + a kyc *slice*, not SoF *data*).
- gen-freeze: `scripts/check-gen-freeze.sh` + `.dev-wiki/gen-freeze-manifest.txt`; current freeze **#7**
  (Phase 25 — verified `check-gen-freeze.sh` returns OK at HEAD; the freeze NUMBER is narrative, corroborated by
  `population.py:105` "gen-unfreeze #7"), the next is **#8**. An unfreeze is a conscious `--write` greenlit on a
  number the phase produced.
