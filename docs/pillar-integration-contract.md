# Pillar 1 → Pillar 2 Integration Contract (v0.1 — DRAFT)

> **Status: ARCHITECTURE (design).** Cross-pillar data contract authored from the signal-watch
> program-architecture home. References `docs/program-blueprint.md` (the FROZEN design
> source-of-truth, §2 grounding chain · §3 rows 4–6 · §13 LFCM) — this is a NEW artifact, not a
> blueprint edit. Grounded by code-verifying aml-substrate at HEAD `bafc67d` (Phase 13 — the
> triple-null) on 2026-06-17; re-stamped from the original `0daa3cc` (Phase 11) grounding after
> confirming the §1/§2 evidence dataclasses (`Alert`/`Dossier`/`STRRecord`/`LCTR`/`EFTR`/
> `GroundingSnapshot`, `STR_REQUIRED_ELEMENTS`) are UNCHANGED P11→P13 — only `validate/*` moved
> (the triple-null measurement, absorbed in §3 below). Ratified when the Pillar-1 enabling
> increments (persist + ids; the network signal) land — until then the serialized schemas below
> are PROPOSED, derived from the current in-memory dataclasses (which aml-substrate does NOT yet
> persist — the §5a join has never executed).

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

## 2. What Pillar 1 emits — the evidence substrate (PROPOSED serialized schema)

The records below exist as clean in-memory dataclasses today but are **NOT persisted** (the CLI
prints a text summary and discards them; nothing is written to disk; there are no stable
`alert_id`/`dossier_id`). The contract requires Pillar 1 to add a serialization + id-minting step
(enabling increment §5a). The generic `io/serialize.py` already handles every one of these
dataclasses, and DESIGN.md §8 lists "persist STR/LCTR/EFTR + verify" as deferred-but-planned.

Serialized form (proposed, parquet/json under a committed-or-regenerated `evidence/` output dir):

| Record | Key | Fields (current, real) | Minted id to ADD |
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
- **§5a — persist + mint ids:** serialize Alert/Dossier/STRRecord/LCTR/EFTR + the overlays to
  `evidence/`; mint deterministic `alert_id`/`dossier_id`. Re-baseline under the gen/ freeze guard
  if it touches frozen `gen/` (it shouldn't — monitoring is downstream of `gen/`).
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

- The exact `evidence/` serialization format + directory layout (parquet vs json per record class).
- Whether the network-structure signal grounds to an existing committed FINTRAC/FinCEN network
  advisory or needs a new corpus indicator (corpus is FROZEN — likely an existing indicator).
- The stratified bootstrap set: how many cases, drawn how (the §14 strata over the observable
  grouping), and which are the known-disposition controls.
- Pillar 2 repo name + its own dev-wiki bootstrap.
