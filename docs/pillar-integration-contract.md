# Pillar 1 → Pillar 2 Integration Contract (v0.1 — DRAFT)

> **Status: ARCHITECTURE (design).** Cross-pillar data contract authored from the signal-watch
> program-architecture home. References `docs/program-blueprint.md` (the FROZEN design
> source-of-truth, §2 grounding chain · §3 rows 4–6 · §13 LFCM) — this is a NEW artifact, not a
> blueprint edit. Grounded by code-verifying aml-substrate at HEAD `bafc67d` (Phase 13 — the
> triple-null) on 2026-06-17; re-stamped from the original `0daa3cc` (Phase 11) grounding after
> confirming the §1/§2 evidence dataclasses (`Alert`/`Dossier`/`STRRecord`/`LCTR`/`EFTR`/
> `GroundingSnapshot`, `STR_REQUIRED_ELEMENTS`) are UNCHANGED P11→P13 — only `validate/*` moved
> (the triple-null measurement, absorbed in §3 below). **The serialized §2 schema + id-mint rule are
> RATIFIED (Phase 55, 2026-06-17)** — derived from the current in-memory dataclasses + the consumer's
> `validate_bundle` gate; what remains is EMISSION, not schema: aml-substrate does NOT yet persist the
> bundle (the §5a join has never executed). Fully ratified-and-wired when the Pillar-1 enabling
> increments (§5a persist + ids; §5b the network signal) land and `e2e_chain_check --real` passes.

## 0. Why this contract exists

Pillar 1 (`/Users/jwang/aml-substrate`) is the data substrate + its monitoring layer: it generates
synthetic Canadian retail-banking data where laundering EMERGES, runs label-blind detectors over
it, and assembles grounded alerts → dossiers → an STR/LCTR/EFTR scaffold. Pillar 2 (a new repo, to
be built) is the **case-investigation → composition → SAR/STR-narrative** workload (blueprint §3
rows 4–6; the agentic capstone DESIGN.md already names "pillar #6"). The two are developed in
PARALLEL; this contract is the only coupling — it lets Pillar 2 bootstrap on a few synthetic
investigations from Pillar 1's REAL output without the repos depending on each other's code.

**Doctrine inherited:** grounded-or-dropped; deterministic verifier per substrate; history/labels
are evidence, never ground truth; nothing presented as a measured number without its measurement
definition.

## 1. The grounding spine Pillar 2 inherits (reference-by-path — REAL, already verified)

Pillar 1's monitoring layer is built on a reference-by-path chain that is Class-G replay-verified
today (`aml_substrate/monitor/verify.py:verify_alert()` re-runs the cited detector over only the
cited transactions and asserts byte-identical reproduction). The audit walk Pillar 2 stands on:

```
Dossier(account_id)
  └─ Alert(detector, capability C-code, account_id, txn_ids[], rule)
       ├─ txn_ids[] ───────────► Transaction.txn_id            (substrate data rows, committed parquet)
       ├─ account_id ──────────► Account.account_id            (committed parquet)
       └─ grounding: GroundingSnapshot
            ├─ signal_id = "<advisory_id>:<indicator_id>"  ──► signal-watch corpus data/<src>/derived/*.json
            ├─ capability (C-code) · data_source (D-code)
            └─ flag = verbatim advisory quote                 (self-contained: copied at firing time)
```

The `GroundingSnapshot` is a COPY of corpus data taken when the alert fired, so the audit walk is
self-contained (no live corpus access needed to replay). **Pillar 2 adopts this chain unchanged**
as the evidence substrate; its citation verifier (below) extends it upward to narrative statements.

## 2. What Pillar 1 emits — the evidence substrate (RATIFIED serialized schema — Phase 55, 2026-06-17)

The records below exist as clean in-memory dataclasses today but are **NOT YET persisted** (the CLI
prints a text summary and discards them; the generic `io/serialize.py` handles every one of these
dataclasses, but nothing writes them out and there are no stable `alert_id`/`dossier_id`). The §5a
enabling increment (an aml-substrate-rooted session) adds the serialization + id-minting step below.

**RATIFIED on-disk form (the §7 open question, now closed — Phase 55).** Pillar 1 emits, per case,
ONE **evidence-bundle json** at `evidence/<run_id>/<case_id>.json` (`run_id` = the deterministic
monitoring-run stamp; committed-or-regenerated, never a stale snapshot — §4.3). The bundle is the
on-disk UNION of the records below + the bundle-level honesty/identity keys, and **conforms by
construction to the Pillar-2 bundle contract** (`aml_casework.contract.validate_bundle` — the
consumer's authoritative structural gate, so "matches the schema" is a runnable check, not prose).
json (not parquet) is ratified for the bundle: one case, human-auditable, diff-friendly; the bulk
transaction/account substrate stays parquet (referenced by path, not embedded). Top-level keys:
`contract_version` (e.g. "0.1") · `illustrative: true` (the always-on synthetic-output discipline,
§4.4) · `case_id` · `subject{customer_id, account_ids[]}` · `transactions[]` (the cited data rows
`{txn_id, account_id, …}`, optional boolean `exculpatory`) · `alerts[]` · `dossier{}` · the
`str_record{}` SCAFFOLD with `narrative: null` and `completeness.grounds_for_suspicion_narrative:
false` (Pillar 2 flips BOTH when it writes the grounded narrative — the seam invariant). `lctr`/`eftr`
ride along when present.

**RATIFIED deterministic id-mint rule (§5a implements it).** Ids are a stable function of content so a
re-run reproduces them byte-for-byte (the gen-freeze discipline extends to evidence):
- `alert_id` = `"AL-" + sha1( detector + "|" + account_id + "|" + ",".join(sorted(txn_ids)) + "|" + signal_id )[:12]`
- `dossier_id` = `"DS-" + sha1( account_id + "|" + ",".join(sorted(alert_ids)) )[:12]`
- `str_record` keys on `case_id` (the labeled-oracle grouping, §4.1; the OBSERVABLE grouping is `customer_id`).

Serialized record fields (current, real — the columns the bundle carries):

| Record | Key | Fields (current, real) | Minted id (RATIFIED — the §2 sha1 rule) |
|---|---|---|---|
| `Alert` | structural | `detector, capability, account_id, txn_ids[], rule, grounding{signal_id, advisory_id, indicator_id, capability, data_source, flag}` | `alert_id` (deterministic from `(detector, account_id, txn_ids, signal_id)`) |
| `Dossier` | `account_id` | `account_id, alerts[] (→alert_id), capabilities[], signal_ids[], cited_txn_ids[]` | `dossier_id` |
| `STRRecord` | `case_id` | `case_id, crime_type, subject_account_ids[], cited_signal_ids[], cited_txn_ids[], completeness{...}, narrative=None` | — |
| `LCTR` | `party_id` | `party_id, account_ids[], txn_ids[], total_cents, window_start, aggregated` | — |
| `EFTR` | `account_id` | `account_id, txn_id, amount_cents, currency, counterparty_country` | — |

Plus the resolution/network overlays (illustrative, adjudicable — NOT ground truth):
`CustomerEntityDossier(customer_id, account_dossiers[], resolved_cluster_id, cluster_members[],
merge_basis_labels[])`; the P7/P8 network `account_id → component_id` map.

## 3. Composition — evidence-assembly, NOT detection-lift (UPDATED 2026-06-16, post-triple-null)

**What changed:** the original §3 premised a network-structure signal as a "non-redundant second
DETECTION axis" that would let composition demonstrate detection lift. aml-substrate **measured that
premise false** through Phase 13 — a code-verified **triple-null**: composition is *never required*
to detect laundering on amount-ROC (multivariate adds −0.34 over `total_amount`'s 0.95), network-ROC
(composed 0.916 vs best single detector 0.886, below the sealed 0.05 margin), or network-precision
(AP 0.043 vs 0.033, below the sealed 0.083 floor). Root cause is structural: one ring ≈ one mule
doing every typology, so typologies co-occur REDUNDANTLY — any single detector already catches the
case. The generator levers meant to fix it (Hawkes/dormancy, legit-overlap cohort) were
measured/predicted null AND counterproductive. **Detection-lift is therefore measured-not-required
on emergent synthetic data and is RETIRED as a contract claim** (deferred-with-owner; the triple-null
is a published honesty result, not a gap to fix).

**What composition IS, in this contract:** redundancy-aware **evidence assembly** — a Pillar-2
dossier gathers the grounded indicators that fire on a case into one examinable bundle a human judges
(dossier-now/score-deferred, blueprint §13), plus the **volume-inversion** workload claim (N raw
alerts → 1 reviewed dossier) which the triple-null leaves untouched. Neither requires the composite
to OUT-DETECT any single signal. The **redundancy-management** frontier (§13 fm-1) is demonstrated on
the **committed corpus** (the un-deduplicated 2,251 indicators across 5 regulators), not on the
substrate.

**The one un-refuted nuance (deferred-with-owner):** the triple-null was measured over the 6
account-LOCAL flow detectors with a typology-COUNT composed signal — NOT a purpose-built
network-STRUCTURE detector over the P7/P8 graph, which does not yet exist. Before retirement is final,
aml-substrate runs ONE cheap **measure-only structure-detector reachability probe** (no gen-unfreeze;
pre-registered two-baseline, held-out). NULL → retirement is unconditional and the network-structure
signal (§5b) is formally shelved. CLEAR → the claim was reachable via that one unbuilt detector,
which is then built (still NOT the P14 case-construction redesign — that is DEFERRED INDEFINITELY as a
self-engineering tautology that violates the "typologies emerge, never injected" doctrine). Pillar 2
builds its chain on the single flow axis meanwhile; the "≥2 non-redundant detection axes" premise is
replaced by "≥1 grounded axis assembled into a complete, examinable dossier."

## 4. Honesty caveats carried on every consumed record

1. **Case grouping is oracle-only.** `STRRecord` keys on the synthetic ground-truth `case_id`. A
   label-blind Pillar 2 assembles cases from the OBSERVABLE grouping (`customer_id` = the
   `Account.customer_id` FK, plus the dossier/network overlay); `case_id` is available as labeled
   oracle for MEASUREMENT only, never as the discovery grouping.
2. **Resolved-entity ids are derived, not stable anchors.** `cluster_id` (P5) and `component_id`
   (P7) are union-find representatives that can shift with membership; the stable observable unit is
   `customer_id`. The resolved cluster is a cited, adjudicable overlay (the P6 finding: don't assume
   the resolver fuses correctly).
3. **Regenerate; don't reuse stale snapshots.** Any local `out/monitor-check/` is gitignored and may
   be pre-P7 (0% counterparty edge). Pillar 2 consumes freshly-generated evidence.
4. **Illustrative badge survives.** Every Pillar-2 output is illustrative/synthetic, labeled per the
   blueprint §9 output-status discipline.

## 5. The seam — Pillar 1 owns persistence; Pillar 2 consumes files

Pillar 2 does NOT import `aml_substrate` as a library (that would couple the repos at code level,
against the one-repo-per-pillar doctrine). Pillar 1 owns the serialized contract; Pillar 2 reads
the committed/regenerated `evidence/` files. Enabling increments (Pillar-1-rooted session):
- **§5a — persist + mint ids (RATIFIED format, §2):** serialize each case to its evidence-bundle json
  at `evidence/<run_id>/<case_id>.json` (the §2 schema; conforms to
  `aml_casework.contract.validate_bundle`); mint `alert_id`/`dossier_id` by the §2 deterministic sha1
  rule. Re-baseline under the gen/ freeze guard only if it touches frozen `gen/` (it shouldn't —
  monitoring is downstream of `gen/`). **Acceptance:** signal-watch's `scripts/e2e_chain_check.py
  --real` (the cross-repo verifier — file-contract, no import) passes its substrate-side checks on the
  emitted bundle, with the C4-structuring slice grounding to `fin-2026-alert001:IND-11`. Brief:
  `aml-substrate/docs/persist-evidence-seam-PLAN-BRIEF.md` (Phase 55).
- **§5b — the grounded network-structure signal** (§3 above).

## 6. What Pillar 2 owns (the workload, full chain — depth-first thin slice)

Build one case all the way to a signed SAR FIRST (thin vertical slice through all four stages), then
widen to a stratified set (§14 doctrine: a conflicting-evidence case, a need-more-info/data-gap
case, a both-defensible disposition — not the happy path). Stages + the REAL verifiers that make it
a build, not a demo:
- **Investigation** — assemble the case evidence set around the observable `customer_id`/network.
- **Composition** — compose the ≥2 grounded axes into a dossier, each signal carrying its §1 walk.
- **SAR/STR narrative** — agentic-drafted; fills `STRRecord.narrative` and flips
  `completeness["grounds_for_suspicion_narrative"]`. **Citation verifier:** every narrative statement
  resolves to an evidence item (dangling-reference + conflict-both-kept checks). **Completeness
  verifier:** the deterministic checklist vs the filing guidance's required elements
  (`STR_REQUIRED_ELEMENTS`).
- **Class-A sign-off SEAM** — a named human act (blueprint §4 Class-A), NOT automated; the demo
  proves the gate ARRIVES evidence-complete.

Score is DEFERRED-with-owner (blueprint §13): dossier now, no aggregate risk number without a named,
owned calibration measurement.

## 7. Open contract questions (resolve at ratification)

- ~~The exact `evidence/` serialization format + directory layout (parquet vs json per record class).~~
  **RESOLVED (Phase 55, 2026-06-17):** one evidence-bundle **json** per case at
  `evidence/<run_id>/<case_id>.json`, conforming to `validate_bundle`; deterministic sha1 id-mint (§2).
  The bulk substrate stays parquet (referenced by path). See §2 + `docs/e2e-acceptance.md`.
- Whether the network-structure signal grounds to an existing committed FINTRAC/FinCEN network
  advisory or needs a new corpus indicator (corpus is FROZEN — likely an existing indicator).
- The stratified bootstrap set: how many cases, drawn how (the §14 strata over the observable
  grouping), and which are the known-disposition controls.
- Pillar 2 repo name + its own dev-wiki bootstrap.

## 8. Signal-coverage mapping — corpus-driven detector design (Phase 58, 2026-06-18)

The signal SUPPLY this contract carries is not a fixed handful — it is the corpus catalog (2,251
indicators / 523 *buildable* = `status=="gap" AND data=="available"`). **`docs/corpus-substrate-coverage.md`
+ `scripts/signal_coverage_map.py`** map each buildable corpus indicator to its reachability on the
substrate, so the detection layer can be designed AGAINST the corpus (top-down) rather than ad hoc.

**The doctrine boundary (load-bearing):** the corpus drives **detector + observable-exposure** design
(top-down); **data generation + labels stay emergent (bottom-up)**. The map MEASURES the
behavioral-coverage gap; it NEVER stamps it. Build briefs derived from it author detectors and
view-exposure only — stamping a behavior or a label is out of bounds.

Each indicator is classified into one of five tiers by its binding gap (observable-exposure MEASURED
against the schema pin + the real emission; behavioral-emergence REASONED from DESIGN.md, flagged):
`reachable-now` (a live detector + casework assertion + emergent behavior, `direct` or via
transaction-`proxy`) · `needs-detector` · `needs-view-exposure` · `needs-behavior` · `out-of-reach`.

**Measured headline — Phase-58 baseline (corpus@472b44e × aml-substrate@df23bba × aml-casework@2381d71):**
93 reachable-now (all C15, capability-scaled — 4 of 5 live detectors ground ZERO buildable gaps), 62
needs-detector, 312 needs-view-exposure (the dominant gap — data the substrate GENERATES but does not
EXPOSE to detectors), 54 needs-behavior, **2 out-of-reach**. The signal supply is broad and
capability-scaled: one capability detector + one `grounding_replay` assertion grounds many corpus
indicators. Re-derive with `signal_coverage_map.py --check`; re-ground the pin before consuming (the
process rule).

**Phase-15 landing update (re-grounded Phase 59, 2026-06-18 — corpus@472b44e × aml-substrate@5875241 ×
aml-casework@4ac9523).** aml-substrate Phase 15 shipped the **substrate half** of the §5 build briefs (a
label-blind PartyView exposing D8/D12 + the C7/C14/C8/C26 screening detectors). The re-frozen map shows
the movement: needs-view-exposure **312→70**, needs-behavior **54→296** — **and reachable-now UNCHANGED
at 93.** Landing the detectors+views moved 0 signals into reachable-now because reachability is a **3-way
AND** (`has_detector ∧ has_casework_assertion ∧ behavior_emergence=="emerges"`) and the substrate half
satisfied only *exposure*: the 242 D8/D12 signals are exposed but **unmeasurable on the still-vendored
txn-only emission** (no party rows → `modeled-inactive` → needs-behavior, an emission-sample limit not
emergence work), and the 62 C7 stay needs-detector pending the casework assertion. **reachable-now rises
only when BOTH remaining halves land:** a party-bearing emission bundle (aml-substrate) + the 4 paired
`grounding_replay` assertions C7/C8/C14/C26 (aml-casework) — both sibling-rooted, handed off in the §5
briefs. Detail + the composite-tier caveat: `docs/corpus-substrate-coverage.md` §3a.

**Phase-60 landing update (re-grounded Phase 60, 2026-06-19 — corpus@472b44e × aml-substrate@9c75c03 ×
aml-casework@c6d8401).** BOTH remaining halves landed: aml-casework Phase 12 shipped the paired
`grounding_replay` assertions (C7 P10 · C8 P11 · C14 P12; C26 deliberately unregistered — the honest null),
and aml-substrate Phase 18 emits the real C8 party-bearing v0.2 bundle. The re-frozen map shows the **first
real reachable-now rise: 93→171 (+78)** — needs-detector **62→0**, needs-view-exposure **70→69**,
needs-behavior **296→281**. **But only C7 moved**, and that is the honest headline: of the four screening
caps whose assertions landed, only C7 has `behavior_emergence=="emerges"` → all 78 C7 buildable signals
flip (62 direct + 16 proxy; `is_reachable` precedes the data_source_class branch). **C8/C14/C26 did NOT
move** — `behavior_emergence` data-only (C8/C14) / absent (C26) is the binding 3rd conjunct, **neither
emission nor assertion work**. So the "both halves must land" framing sharpens to **"only the cap whose
behavior genuinely emerges reaches reachable-now"**; further rises need emergent-behavior work in the
substrate (bottom-up, never stamped), not more wiring. Separately, the **real cross-pillar chain CONNECTS**:
`e2e_chain_check --real` (re-grounded to the same HEADs) on substrate's C8 bundle (`CASE-P-0000251`) →
casework signed SAR, zero blocking violations → CONNECTED; the launcher was re-grounded (only its
`grounding_heads`, 7/8 dists byte-identical — the Phase-55/57 pattern). Detail: `docs/corpus-substrate-coverage.md` §3b.
