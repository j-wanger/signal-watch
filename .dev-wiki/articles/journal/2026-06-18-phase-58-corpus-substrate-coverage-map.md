---
title: "Phase 58 — Corpus→substrate signal-coverage map (delivered)"
date: 2026-06-18
type: journal
phase: 58
tags: [cross-pillar, corpus-coverage, signal-coverage-map, detection-layer, emergence-doctrine, measure-first, non-ship]
---

# Phase 58 — Corpus→substrate signal-coverage map

Planned + delivered + debriefed same session (LITE, 3 tasks, all [x]). The user's REFRAME at the
dev-plan gate: the detection layer (Pillar 1) was built bottom-up with no systematic join to the corpus
catalog; design it AGAINST the corpus, targeting 200+ grounded signals. Deliverable = the executable
coverage MAP + the doctrine-safe design + prioritized sibling briefs (signal-watch's architecture role;
the build is sibling-rooted). Direction gate all_accept:true (A0 doctrine-reconcilability the T0 weakest).

## What shipped (NON-ship, --check all 8/8 zero drift)

- `scripts/signal_coverage_map.py` (+ `--selftest`/`--check`/`--freeze`/`--json`) — joins the 523
  buildable corpus indicators (status==gap AND data==available) × a pinned substrate snapshot × the
  vendored CASE-P-0010361 emission → a per-signal tiered reachability. Reuses
  `corpus_redundancy.SOURCES`; no sibling import; build.py never imports it.
- `data/coverage-map/substrate-pin.json` (code-verified facts @ the HEADs) + frozen `coverage.json`
  (523 signals; `--check` byte-identical).
- `docs/corpus-substrate-coverage.md` + integration contract §8.
- Two sibling briefs (in the sibling trees, untracked there): aml-substrate
  `corpus-coverage-build-PLAN-BRIEF.md` (expose a PartyView + author C7) · aml-casework
  `capability-assertions-PLAN-BRIEF.md` (paired grounding_replay assertions).

## The measured findings (corpus@472b44e × substrate@df23bba × casework@2381d71, 523 buildable)

reachable-now **93** · needs-detector **62** · needs-view-exposure **312** · needs-behavior **54** ·
out-of-reach **2**.

1. **Premise confirmed, sharply:** 4 of 5 live detectors (C2/C3/C4/C5) ground ZERO buildable corpus gaps
   (they target already-covered capabilities, so those aren't "gaps"). Only C15 intersects; all 93
   reachable-now are C15, 91 via transaction-proxy. The detection layer wasn't designed from the corpus.
2. **The twist — "design data to support signals" is mostly EXPOSE, not GENERATE:** only 2/523 are truly
   out-of-reach. The dominant gap (60%) is data the substrate ALREADY GENERATES but never exposes to the
   detector views (no Person/Org view exists). The highest-leverage build is wiring views to the schema.
3. **Path to 200+ (capability-scaled):** 155 with detector-work alone (93 live + C7 +62); >200 goes
   through view-exposure (the 312) + entity/KYC detectors. ~15-20 capabilities, not 200 detectors.

## Decisions / problems solved

- Two-dimension model: observable-exposure MEASURED (against the schema pin + the real emission — D17 is
  modeled-inactive because counterparty_country is 0/71 in the emission, not by assertion) × behavioral-
  emergence REASONED (DESIGN.md/gen, flagged behavior_confirmed:false).
- The corpus D-code can differ from the substrate detector's observable (C3/D13 funnel grounded via
  transaction proxy) → capability-gated reachable-now with a `direct`/`proxy` mode, bundle-validated.
- Corrected two over-claims mid-build: `data-only` capabilities map to needs-behavior (not needs-detector
  — a static attribute can't be caught by just writing a detector); `path_to_200plus` does NOT treat
  view-exposure as free (each still needs a detector + maybe behavior).
- Stale loaded context corrected by code-verification: substrate is at Phase 14 (persist seam BUILT), not
  Phase 13; 6 detectors; casework registers 5 assertions (C6 has a detector but no assertion).

## Health Delta

New dep-free `--selftest` (classifier-integrity: emission-tamper flips D17 → proves the classifier reads
the emission; fabricated reachable-now rejected). No ship code touched; no test framework change;
`--check all` 8/8 unchanged. Zero ship artifacts in the change set.

## Gate Compliance

direction=approved (all_accept:true) · delivery=accepted. Assumption-ledger Phase-58 revisit: A0–A4 all
HELD (A2 sharpened, A3 surfaced the one named risk). No late bites on prior phases.

## Soft Observations / Phase N+1 Candidates

- **The behavioral-emergence tier is reasoned, not measured** — confirm it in an aml-substrate-rooted
  session (esp. C7→emerges, the claim most likely to move; if data-only, "155 detector-only" drops to
  93). A cheap measure-only behavioral-reachability probe in aml-substrate would convert the reasoned
  tier to measured. Sibling-rooted.
- **The corpus-driven 200+ build is the natural follow-on** but it is SIBLING-rooted (the two briefs are
  the hand-off): aml-substrate (PartyView + C7) → aml-casework (paired assertions), ranked by the map.
- **Reusable insight (wiki-capture candidate):** the bottleneck between a rich synthetic generator and
  its detection layer is often OBSERVABLE-EXPOSURE, not data — the generator produced KYC/ownership/PEP
  data the detectors literally could not read. And: design detectors against the GAP catalog, not the
  already-covered set (4 of 5 live detectors targeted covered capabilities).
