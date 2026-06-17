# End-to-End Acceptance — the 3-pillar chain "connected" (Phase 55)

> **Illustrative data & outputs.** This defines, deterministically, what it means for the 3-pillar
> demo to be *connected end to end*. It is the contract `scripts/e2e_chain_check.py` implements and
> the acceptance criterion both sibling PLAN-BRIEFs (`§5a` persist, casework consume-real-bundle)
> are written against. NON-ship; signal-watch reads only committed/regenerated sibling **outputs**
> (the file-contract — no `import aml_substrate` / `aml_casework`). Grounding HEADs:
> aml-substrate@`bafc67d` · aml-casework@`0316580` · the contract = `docs/pillar-integration-contract.md` §2.

## The vertical slice (what gets connected)

The first wired case is a **C4-structuring** case — the one path verified reachable on the *existing*
grounding pin without any widening:

- **Pillar 1 (aml-substrate)** `StructuringDetector` (capability **C4**) fires on a sub-$10K cash
  structuring pattern and emits an evidence bundle whose alert grounds to `fin-2026-alert001:IND-11`
  (the detector's own docstring grounds it there).
- **Corpus (signal-watch, FROZEN)** `data/fincen-alerts/derived/fin-2026-alert001.json` carries
  `IND-11` → capability **C4**; its verbatim `flag` is the grounding evidence.
- **Pillar 2 (aml-casework)** `grounding_replay.py` registers `"C4"` (`_assert_c4_structuring`),
  consumes the bundle, runs its 6 Class-G verifiers, drafts + grounds the SAR narrative, and reaches
  the Class-A sign-off seam.

Three-way alignment — substrate C4 → `IND-11` → casework C4 — so the slice flows with no
corpus-pin widening and no new capability registration.

## "Connected" = these deterministic checks pass

`e2e_chain_check.py` asserts the join over two artifacts: the **substrate-emitted bundle** (Pillar-1
output, the §2 evidence-bundle json) and the **casework signed SAR** (Pillar-2 output, the same
bundle after `record_signoff`: narrative filled, seam flipped, a signoff verdict). The checks, in
chain order:

### A. Substrate side — the emitted evidence is real-grounded
1. **Bundle shape (the join-critical subset of §2 / `validate_bundle`):** `contract_version` present;
   `illustrative === true`; `case_id` present; `subject.customer_id` + non-empty `subject.account_ids`;
   ≥1 transaction each with `txn_id`+`account_id`; ≥1 alert.
2. **Alert grounding chain (per alert):** `alert_id, detector, capability, account_id, rule` present;
   `txn_ids` non-empty and ⊆ the bundle's `transactions`; `account_id ∈ subject.account_ids`;
   `grounding{signal_id, advisory_id, indicator_id, capability, data_source, flag}` complete;
   `signal_id === "<advisory_id>:<indicator_id>"`; `grounding.capability === alert.capability`.
3. **Deterministic id-mint (§2 rule):** `alert_id === "AL-" + sha1(detector|account_id|sorted(txn_ids)|signal_id)[:12]`;
   if a `dossier` is present, `dossier_id === "DS-" + sha1(account_id|sorted(alert_ids))[:12]` and
   `dossier.alert_ids ⊆ {alert_id}`. (Re-runs reproduce ids byte-for-byte.)
4. **Corpus grounding (against the FROZEN signal-watch corpus — signal-watch's OWN data, not a
   sibling):** for each alert, `normalize(grounding.flag)` is a substring of `normalize(flag)` of the
   record `data/<source>/derived/<advisory_id>.json` at `indicator_id`. For the C4 slice:
   `fin-2026-alert001` / `IND-11`. `normalize` is signal-watch's `derive_signals.normalize` (the
   stable grounding core — single source of truth, reused not reimplemented).

### B. Casework side — the SAR is verified + signed
5. **Seam flipped:** `str_record.narrative` non-empty AND
   `str_record.completeness.grounds_for_suspicion_narrative === true` (both, the seam invariant).
6. **Completeness:** every `STR_REQUIRED_ELEMENTS` key present in `str_record.completeness`.
7. **Citations resolve:** every `str_record.narrative_claims[].cites` entry resolves to either a
   `signal_id` grounded by some alert OR a `txn_id` in `transactions` (dangling-reference check); each
   claim has non-empty `text`.
8. **Signed:** the SAR carries a `signoff` block with `signoff.signed === true` and
   `signoff.blocking_violations === []` (REQUIRED — the chain's terminal Class-A artifact; an unsigned
   SAR is not a connected chain).

### C. Cross-pillar identity
9. **Same case:** the substrate bundle and the casework signed SAR share `case_id`, and the SAR's
   `cited_signal_ids ⊆` the signal_ids grounded by the bundle's alerts (Pillar 2 cited what Pillar 1
   grounded — the audit walk is continuous end to end).

**Connected ⟺ A∧B∧C all pass.** Any failure names the exact seam (which check, which id/flag) — a
green run is the deterministic proof that a substrate-detected C4 case became a verified, signed SAR
whose every statement walks back through the evidence to the frozen regulator corpus.

## Two beats (what is proven, when)

- **Beat 1 — SPINE, now (`--selftest`):** the checks run against a committed **synthetic** C4 fixture
  pair (`data/e2e/*.json`) authored to the §2 schema — NOT sibling output. Proves the assertion logic
  + a negative fixture (a broken join) is caught. This is the deliverable this session.
- **Beat 2 — REAL, the delivery gate (`--real --substrate <bundle> --casework <signed>`):** the same
  checks run against the actual sibling outputs once `§5a` (aml-substrate persist+ids) and the
  casework consume-real-bundle bridges land in their own sessions. Absent pins → honest
  `GATED: sibling output absent` + nonzero exit. `data/pillar-status.json` flips to all-green only
  here.
  - **Bridge #1 alone (substrate-side):** `--real --substrate <bundle>` with NO `--casework` runs the
    A-checks only — the bridge-#1 acceptance. It flips `bridge_1_persist` → done **without** claiming the
    full chain (`e2e_real` stays pending until the casework SAR lands). `--selftest` preserves real
    bridge progress — only a `--real` run moves a bridge state. (Bridge #1 VERIFIED 2026-06-17 against
    aml-substrate@`df23bba` `CASE-P-0010361`: schema + id-mint + corpus grounding all matched.)

## Honesty boundary

The synthetic fixtures are LABELED synthetic (`illustrative: true`) and are NEVER presented as real
substrate output. `--real` **refuses any path under `data/e2e/`** (the synthetic fixtures) — so a
verification run cannot flip the committed `pillar-status.json` to a false "connected" / green launcher;
only genuine sibling outputs (`evidence/<run_id>/…`) update the bridge state. The harness proves *the
chain connects*, not that any number is real — every output carries the always-on Illustrative posture.
No sibling code is imported; the seam is files only.
