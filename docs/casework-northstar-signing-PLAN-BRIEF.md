# PLAN-BRIEF — aml-casework: ground the dominant case topologies so north-star FILES SIGN at scale

> **A signal-watch → aml-casework handoff brief** (the Phase-67–79 vendoring pattern: signal-watch authors the
> contract; casework implements the grounding verifiers on its own lifecycle — *no code lands in casework from
> here*). Synthetic / illustrative; **no rate, score, or multiplier is claimed.** **Re-vendored to aml-casework
> HEAD `04cc335` (Phase 21); Ask #2 (C15) LANDED, signal-watch Phase 82 (2026-06-29).** Companion to
> [`northstar-at-scale-build-order.md`](northstar-at-scale-build-order.md) and the substrate half
> [`substrate-northstar-evidence-emission-PLAN-BRIEF.md`](substrate-northstar-evidence-emission-PLAN-BRIEF.md).

## STATUS (signal-watch Phase 82 — Ask #1 done earlier; Ask #2 LANDED via the casework P20 re-vendor)

- **Ask #1 — fan-IN C3 grounding** was DONE at casework Phase 19 (`_c3_fan_in`) and consumed at signal-watch Phase
  79 (the matched-pair Lakeshore co-sign); the original brief's "190/376 C3 fail-close" measurement was STALE
  (pre-Phase-19).
- **Ask #2 — C15 shell / nominee replay** is LANDED: casework **Phase 20** (`a059fc5`) reconciled C15 (shell
  throughput) + C4 (any-channel structuring) to substrate's real `ShellDetector`/`StructuringDetector`
  definitions; signal-watch re-vendored `076fb8e → 04cc335` and re-measured the signing funnel over the 376-case
  slice: **the cases casework SIGNS end-to-end moved from 128/376 to 256/376** (the C15-throughput-conduit + C4
  any-channel cases that previously fail-closed now sign for the right reason — verifier strictness intact: it
  signs the legitimate topology, still refuses what it cannot reproduce). Casework Phase 21 (`7398ddc`, drift
  tripwire) is internal hardening, picked up free by the re-vendor.
- **Ask #3 — the grounded STR-narrative contract** stays a documentation clarification (the DECIDE consume remains
  the live narrative author). The honest sign FRONTIER persists: a txn-bearing C14 shape casework cannot reproduce
  a signable record from still fails-CLOSED (the "refusal IS defensibility" climax) — a named casework follow-on.

## Intent

A north-star FILE is only complete when the case-investigation pillar (casework) **SIGNS** it — re-deriving the
fired capabilities from the raw transactions and producing the signed STR. **Signing IS the defensibility
climax:** casework refuses to sign what its own deterministic replay cannot reproduce, and that refusal is the
audit-grade guarantee. A Phase-81-post assessment measured signing across the generated 376-case slice:
**128 SIGN end-to-end; 248 FAIL-CLOSED.** The refusals are honest and grounded (each carries an `e2e_note` naming
the capability casework couldn't reproduce) — but their DISTRIBUTION is the problem: **190 of the 248 fail-close on
C3 fan-IN, and 49 on C15** — and the C3 fan-in funnel-to-one-beneficiary shape **IS the north-star's FILE topology**
(the mule). So at scale, the very cases that should file the way Northgate files are the ones casework won't sign.
This brief asks casework to ground those two topologies so generated north-star FILES sign at population scale —
not only via the hand-authored `case-b.bundle.json` translation.

**The load-bearing distinction:** this is NOT a request to make casework sign MORE (a looser verifier is a worse
verifier). It is a request to ground two *specific, legitimate* topologies casework's current replay doesn't cover,
so that REAL fan-in / shell-ownership cases sign for the right reason. The refusal of genuinely-ungroundable cases
must stay.

## What already signs (do NOT regress)

casework's Phase-19 `_c3_fan_in` (≥N distinct inbound CREDIT originators within a window) grounds the *specific*
Lakeshore shape — the matched-pair CLEAR co-signs end-to-end. The cash-placement C5 `cleared` proxy signs. The
party-leaf C14 (the Phase-80 sanctions-driven kyc) signs. **Keep all of these byte-stable.** The funnel itself
(128 sign / 248 fail-closed) is a *measured, two-sided* property of the committed slice — the goal is to move the
legitimate-topology refusals into the sign column, not to flatten the funnel.

## The asks (with the design choice + why)

### 1. Fan-IN C3 grounding at POPULATION scale (the dominant blocker)

- **The gap (measured):** **190 of 376** slice cases fail-close on a C3 fan-in vs fan-out replay divergence.
  casework's `_c3_fan_in` was built (Phase 19) for the single Lakeshore shape; the slice's broader fan-in population
  — multi-originator funnel-IN to one beneficiary, the canonical mule — does not reproduce under the current replay
  (the parameters / the window / the originator-distinctness test fit Lakeshore, not the generated distribution).
- **The ask:** generalize the fan-in C3 grounding to the population's funnel-in distribution — the same audit logic
  (count distinct inbound CREDIT originators into one beneficiary account within a window), parameterized to the
  generated topology rather than one hand-tuned case.
- **KEY DESIGN CHOICE — ground the TOPOLOGY, never widen by relaxing the verifier. WHY:** the temptation is to make
  C3 pass more by loosening the threshold — that destroys the verifier's value (it would sign noise). The correct
  move is to make casework's replay RECOGNIZE the legitimate fan-in pattern it currently mis-reads as a fan-out
  miss: same strictness, broader topology coverage. A north-star FILE that doesn't sign on the real mule shape is
  not a north-star FILE — and the fix must keep the refusal of genuinely-ungroundable cases intact.

### 2. C15 shell / nominee-ownership replay

- **The gap (measured):** **49 of 376** fail-close on C15 (shell / beneficial-ownership) — casework can't
  independently reproduce the network/ownership leg from the raw bundle.
- **The ask:** a C15 grounding verifier that re-derives the shell/nominee ownership signal from the bundle's
  `related_parties[]` / (forthcoming) `ownership_edges[]` — so the network leg that corroborates the file signs.
- **KEY DESIGN CHOICE — C15 grounding consumes the SAME ownership evidence the determination engine reads. WHY:**
  the substrate half (`substrate-northstar-evidence-emission` #4) emits multi-hop `ownership_edges`; casework's C15
  verifier should re-derive over that exact structure, so the determination leg and the sign-time replay agree on
  one ownership representation — no second, divergent ownership model. This couples the two pillars on a shared
  evidence shape, which is the whole point of the cross-pillar contract.

### 3. (Lower priority) a grounded STR-narrative contract

- **The gap:** the slice's `str_record` carries `narrative: null` / `crime_type: null`; the signed-STR prose is
  produced LIVE by the DECIDE consume, not as a committed layer — so a generated case has no frozen narrative.
- **The ask:** a deterministic, grounded narrative template (per crime_type, citing the fired signals) OR a
  documented contract that the DECIDE consume is the sole narrative author and runs per case at sign time.
- **KEY DESIGN CHOICE — narrative is GROUNDED-or-live, never pre-fabricated prose. WHY:** an authored narrative
  string in committed data would be ungrounded fiction; the program's discipline is that every claim cites its
  evidence. So the narrative is either a template that cites the bundle's own signals, or it stays a live DECIDE
  product — never a hand-written paragraph baked into the slice.

## Constraints + sequencing

- **Verifier-strictness is sacred:** every ask GROUNDS a real topology; none LOOSENS the refusal of ungroundable
  cases. The 128/248 funnel is honest — the win is moving legitimate-topology refusals to signs, with the funnel
  staying two-sided.
- **Re-vendor on landing:** signal-watch consumes casework via the vendored copy (`vendor/aml-casework/` +
  `VENDORED_AT`); a new grounding verifier lands by re-vendoring + re-measuring `_measure_grounding` over the slice
  (the funnel recomputes deterministically). build.py never imports casework — the boundary stays
  distribution-not-coupling.
- **Sequence:** #1 (fan-in C3) is the dominant blocker — it alone moves the largest refusal class (190) and unblocks
  the north-star FILE topology; #2 (C15) couples to the substrate ownership-edges emission (land them together);
  #3 is a documentation/contract clarification.
- **Pin `076fb8e` (Phase 19).** Status: NOT BUILT. Re-verify the live HEAD before acting (sibling state drifts).
  Out of scope: any verifier relaxation; any signal-watch dist change (the workbench is companion-only).
