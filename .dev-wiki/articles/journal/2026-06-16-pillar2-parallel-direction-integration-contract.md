---
title: Pillar 2 greenlit in parallel — full-chain case-investigation/SAR pillar + the integration contract
date: 2026-06-16
type: journal
phase: phase-50-aml-program-build
tags: [pillar-2, parallel-pillars, integration-contract, lfcm, sar-narrative, composition, cross-pillar]
mode: quick-debrief
---

# Pillar 2 greenlit in parallel — full-chain case-investigation/SAR pillar + the integration contract

Same-session continuation of the 2026-06-16 pillar-1 review. The user reframed the program structure
from SERIAL (finish substrate, then build downstream) to PARALLEL pillars, and set Pillar 2's first
increment. No signal-watch ship artifacts touched; the blueprint stays FROZEN. New artifact:
`docs/pillar-integration-contract.md`.

## What happened

- **The user's reframe:** "what comes after aml-substrate — can we not start it in parallel? even
  using a few synthetic example investigations we should be able to develop the demonstration of
  the concept." Correct instinct, and sharper than it looks: the two tracks DECOUPLE because the
  judgment/composition/narrative end (blueprint §3 rows 4–6) doesn't wait on transaction-detection
  realism — single-feature dominance is a MONITORING concern, not a composition one.
- **What comes after = Pillar 2:** the case-investigation → composition → SAR/STR-narrative
  workload (the Class-J/Class-A end; aml-substrate's DESIGN already names "pillar #6 — the agentic
  capstone"). signal-watch's gate + triage consoles are its DEMO embryos; Pillar 2 is their
  production-class successor with REAL deterministic verifiers.
- **First-increment scope (user chose the bigger bite): the FULL chain** — composition + judgment +
  SAR/STR narrative + completeness checklist + Class-A sign-off seam (§3 rows 4–6 end-to-end).
  De-risked by two constraints I held: build DEPTH-FIRST (one case → signed SAR, then widen to a
  stratified set), and Class-A sign-off is a human-accountability SEAM (arrives evidence-complete),
  not automation.
- **The schema verification (agent, code-verified at HEAD 0daa3cc) resolved two caveats:**
  - VALIDATING — the reference-by-path grounding chain is REAL and Class-G replay-verified
    (`verify_alert` re-runs the cited detector over cited txns, byte-identical); `STRRecord.narrative
    = None` + the one hard-coded-`False` completeness element is a PRE-ANTICIPATED seam. Pillar 2's
    narrative is literally that slot.
  - CORRECTING (my earlier overclaim) — composition does NOT span axes today: all 6 detectors fire
    on the transaction-flow axis only; KYC/sanctions/network are data/structure, NOT fired grounded
    signals. Composing them = correlated signals (the §13 double-counting failure) → hollow.
- **The composition fix (user chose): a grounded NETWORK-STRUCTURE signal** over the existing P7/P8
  reconstructed network. Dual-purpose — a non-redundant composition ground AND a real second
  DETECTION axis (structure, not magnitude) that also serves P12's multivariate goal. The one place
  the two tracks converge. (KYC/sanctions = composition-only, deferred; no-KYC-leak forbids them as
  strong detectors.)
- **The seam:** nothing is persisted today (in-memory dataclasses, no ids). Pillar 1 OWNS a small
  persist + mint-ids step (the generic serializer exists; DESIGN lists it deferred-planned) — cleaner
  than Pillar 2 importing `run_pipeline` (code-coupling, against the one-repo-per-pillar doctrine).
- **Deliverable:** `docs/pillar-integration-contract.md` v0.1 DRAFT — the grounding spine, the
  proposed serialized record schemas, the network-signal fix, the honesty caveats (case-grouping
  oracle-only; derived cluster/component ids; regenerate-don't-reuse), the persist seam, what
  Pillar 2 owns, and open ratification questions.

## Plan of record — three concurrent tracks, one cheap coupling

- **Pillar 1 (aml-substrate):** continues P12 (multivariate subtlety); plus two contract-enabling
  increments — (5a) persist monitoring output + mint ids, (5b) the grounded network-structure
  signal. Planned/built in an aml-substrate-rooted session.
- **Pillar 2 (NEW repo, TBD name):** the full chain, depth-first thin slice → stratified set, real
  verifiers (citation + completeness + grounding-replay), bootstrapped from the persisted contract.
  Its own dev-wiki + lifecycle.
- **signal-watch (architecture home):** owns the integration contract + tracks both pillars.

## Soft Observations / open items

- The contract is v0.1 DRAFT, grounded at HEAD 0daa3cc; ratify when the persist + network-signal
  increments land. Open questions live in §7.
- Sequencing dependency (soft, not a blocker): Pillar 2's NON-redundant composition story needs the
  network signal (5b) + persistence (5a) from Pillar 1 — small, well-scoped increments, not the
  whole of P12. The full-chain machinery (verifiers, STR seam, narrative) is buildable against the
  transaction-flow signals meanwhile.
- This journal + the contract + the record sync are uncommitted.
