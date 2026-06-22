---
title: "Phase 66 — Workbench richness: richer slice + OSINT corpus depth + the substrate BO-graph emission handoff brief"
date: 2026-06-22
phase: phase-66-workbench-richness
ceremony: lite
gates: { direction: accepted (all_accept:true), delivery: accepted }
status: delivered
---

# Phase 66 — Workbench richness + the BO-graph handoff

**What it is.** Two signal-watch-LOCAL richness wins shipped now + the durable network lever authored as a
sibling brief, bundled into one phase for cross-repo coherence. Born from a two-repo richness recon: the
substrate is *single-signal-separable* (composition subsumed by network linkage — P16), so more
cases/typologies/detectors add visible VOLUME, not detection difficulty; the richness that compounds is the
NETWORK (the generated-but-unprojected beneficial-owner graph — the #1 lever).

## What moved

- **T1 — a wider slice.** Re-ran the deterministic substrate emit (`--clients 40000 --seed 0`, tool-use;
  verified `src/` byte-identical between the f90bd39 pin and HEAD → same population, pin honest) + raised the
  curate caps + added a **combo-coverage pass** (≥1 representative of every population combo) →
  `data/workbench/` re-vendored to **294 cases** (was 200), **all 23 population combos** (was 14), 85 4+-cap
  exemplars (was 60), coverage re-MEASURED **99/294**, gate funnel **189/66/39**.
- **T2 — a deeper OSINT corpus mirroring the substrate ownership graph (primary).** `data/osint/corpus.json`
  → 14 subjects; registry records carry `relationships:[{src,dst,label,ownership_pct}]` **mirroring
  aml-substrate's `RelationshipEdge`** (`BENEFICIAL_OWNER`/`DIRECTOR_OF`/`OFFICER_OF`/`CONTROLS`/`OWNS`).
  `osint_tools.py`: REL_LABELS vocab + an ownership-RANGE check in the validator; `build_graph` draws
  direction-aware src→dst ownership edges; jurisdiction threaded; the stub screens EACH discovered affiliate.
  Two ownership→sanctions chains (Zane Zhao→Crescent Dunes; Management Trading Co.→Silk Road Freight),
  cross-subject links (Priya Ueda↔Retail Services). `workbench.html` renders the ownership label +
  `ownership_pct` as **"N pct"** (never "N%" — the no-% rule). 7 subjects yield findings.
- **T3 — the handoff brief.** `docs/substrate-bo-graph-emission-PLAN-BRIEF.md` (the Phase-55–58 pattern): a
  `PartyGraphView` projection · `related_parties[]` bundle emission (v0.2→v0.3) · a non-tautological C14
  BO-disclosure detector · the consume-side mapping (the emitted shape maps 1:1 onto what GATHER already
  renders). Sibling-executed.
- **T4** — live execute-once + suites + docs + the governor.

## The honesty seam — three flaws caught and fixed

The live execute-once and the post-build adversarial pass both earned their keep:

1. **Model-fabricated ownership (live-caught).** Qwen output a fabricated ownership percent (51 vs the
   record's 75) and a flipped direction; the gate was only range-checking it. → Fixed by **record-sourcing**:
   the gate resolves label/percent/DIRECTION from the synthetic record's structured `relationships` (matched
   by the finding's two parties, set-equal), never from the model. The model only grounds the quote + names
   the parties. Re-ran live → correct 75 pct / correct direction, 0 fabricated.
2. **The abbreviation-period bug (live-caught).** The sentence-bridge guard rejected "General Trading Co.
   discloses" ("Co. " read as a boundary), dropping every org-name finding. → Refined to require a *capital*
   after the terminator (a real boundary), so abbreviations pass while the adversary's two-clause stitch
   still drops. **Documented latent limitation:** this relaxed the guard to terminator+ws+CAPITAL — a future
   lowercase-led 2-sentence record could stitch; adversary-verified no committed record is exploitable.
3. **The un-swept synthesis (adversary-caught, MEDIUM).** The model-authored `finding` synthesis was the one
   model free-text that rendered un-swept — a live model could write "owns 51%" beside the (correct)
   record-sourced edge, defeating the no-% rule. → Fixed by **sweeping the synthesis for banned tokens**
   (fail-closed) + a test. The adversary's gate-regression + governor dimensions: zero issues (all Phase-65
   bypasses still closed, persists-nothing holds, the pin honest).

A self-review also closed a failure-path gap (the validator's new `relationships` checks gained a
malformed-relationship test).

## Verification (exit)

`uv run pytest` 18/18 · `node tests/workbench.test.mjs` 103/0 · `osint_tools`/`serve_workbench`/`curate
--selftest` green · `build.py --check all` 8/8 ZERO dist drift · build.py imports no sibling/companion ·
live gather clean (0 fabricated, no % leak).

## Decisions / notes

- Gate all_accept:true (A0 the governor [T0 weakest] · A1 mirror the RelationshipEdge schema [chosen] · A2
  modest ~320 deterministic re-vendor [chosen] · A3 the BO-graph emission as a sibling brief · A4
  companion-only); all HELD at delivery (ledger Phase-66 revisit-status). Grounded against signal-watch HEAD
  761a446 + aml-substrate@9d2e65c / aml-casework@81df91c.
- The OSINT ownership shape was deliberately authored to **mirror the substrate `RelationshipEdge`** so the
  local win doubles as the BO-graph brief's rendering prototype — when the real graph lands, the workbench
  needs no rework. That coherence is why the brief was bundled into this phase.
- The governor (single-signal-separable) governs all richness framing: demo-VISIBLE only, ZERO
  catch-rate/detection-difficulty/% number.
