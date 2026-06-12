---
title: "Phase 47: Demo-to-program design — blueprint + gate console + E-23 (the first design phase)"
aliases: []
category: journal
tags: [design, program-architecture, model-risk, sr-11-7, osfi-e-23, gate-console, m9]
parents: [phase-47-agentic-aml-program-design]
created: 2026-06-12
updated: 2026-06-12
source: debrief
duration: ~4h (single session: plan + full implementation + regate)
---

# Phase 47 — Demo-to-program design: the regulatorily defensible agentic AML program

## What Happened
- STANDARD ceremony (first design phase; first standard — escalated from lite at the gate). ALL 7 tasks [x] same-session 2026-06-12. READY FOR COMPLETION — delivery gate pending. Direction gate closed at plan time (A1 reject-by-reframe → A1′; A2–A5 accept). Post-implementation self-check CLEAN; exit criteria 4/4 MET (reviewer-verified against artifacts).
- T1 aml-wiki E-23 gap closed: `wiki/articles/concepts/osfi-e-23-model-risk-management.md` from the PRIMARY osfi-bsif.gc.ca fetch (published 2025-09-11, effective 2027-05-01); lifecycle Design(rationale/data/development)→Review→Approval→Deployment→Monitoring→Decommission; 8/8 mapping rows name an SR 11-7 pillar; cross-link added. DESIGN INPUT: E-23's model definition explicitly includes "judgmental assumptions" → the human-judgment gate layer is itself in-scope; rationale capture = lifecycle evidence.
- T2 blueprint spine `docs/program-blueprint.md` §1–§6: universal grounding principle (the user's A1′ reframe AS the spine), 5-workload × 4-cell substrate/verifier table (RED 5/0 → GREEN 5/5), G/M/J/A gate taxonomy, dual-stream human-work charter (judgment + mandated-accountability, 4 invariants), agentification criterion (probe rule, n=1 caveat, caps, surface-all-dimensions).
- T3 blueprint assembly §7–§12: E-23-lifecycle × SR-11-7-pillar control mapping (built controls name committed artifacts); validation story Designed-now vs Deferred—with-owner (owner = the adopting institution's model-risk function); 6-row honesty disposition table; §10 refuses a 95% ratio target on DESIGN grounds; §11 re-sequences the DEFERRED list into 4 capability chains; §12 + HANDOFF §8 M9 line (demo charter transcended for DESIGN artifacts only).
- T4 `data/console/cases.json`: 213 REAL C/D adjudication cases (C-only 83 / D-only 96 / both 34) deterministically curated from the Phase-34 correction (git show 83a79c3^ vs current; byte-identity claim VERIFIED zero exceptions) via `scripts/curate_console_cases.py` (regeneration-only, stdlib); build.py +94/-0 additive (load/validate_console_cases); 212 FINTRAC rows manifest-byte-matched attribution, 1 US row null.
- T5-CHECKPOINT: PROCEED recorded (no 47b descope — blueprint complete + verified, budget healthy, console was the user's explicit gate choice). T5 console.html → dist/console/index.html (305,180 bytes; the 4th ship artifact): Queue (213 grouped by axis; consensus-not-ground-truth framing) → Evidence (verbatim flag + red_flag; NEUTRAL Assessment A/B) → Disposition (graded uphold-A/uphold-B/both-defensible/neither-escalate; rationale REQUIRED) → Record reveal (adjudicated=B DERIVED per case vs current committed codes, 213/213 verified at build — drift fails the build) → session-only Ledger (JSON copy-out; persists nothing). tests/gate-console.test.mjs 68/68 (RED-first); badge + FINTRAC footer/US-empty; XSS; keyboard guards; both motion modes.
- T6 CLAUDE.md updated in place (Three→Four ship artifacts, console target, tests, M9 milestone); smoke-checklist 6-item console section; FULL REGATE GREEN: --check all 6/6 zero drift · gate-console 68 · corpus 303 · news-stream 150 · all python selftests · news_quality_harness 17-within-baseline · news_live_test · news_store.

## Decisions Made
- All phase decisions captured at plan time in [[decisions/phase-47-agentic-aml-program-design|the Phase-47 decision article]] (D1–D5, confidence high) — no new decision articles (dedup). Implementation-time decision: T5-CHECKPOINT = PROCEED (recorded in tasks.md).

## Problems Solved
- T1 scope-glob deviation: the real aml-wiki path is `wiki/articles/concepts/`, not `wiki/concepts/` — DISCOVERY-class path correction, phase article scope list fixed at this debrief.
- T4 provenance finding: the Phase-34 commit-message split "114 C + 129 D" vs measured 117/130 — the deterministic diff is the authority, not the prose.

## Open Questions
- None new-blocking. The blueprint's Deferred—with-owner validation items (outcome feedback, population drift monitoring, ATL/BTL sampling) are owned by a future adopting institution — recorded in blueprint §8, not dev-wiki blockers.

## Artifacts Changed
- `wiki/articles/concepts/osfi-e-23-model-risk-management.md` (NEW, aml-wiki) + cross-link in aml-model-risk-management.md
- `docs/program-blueprint.md` (NEW, M9 design deliverable) · `specs/phase-47-agentic-aml-program-design.md` · `HANDOFF.md` §8 M9 line
- `data/console/cases.json` (NEW) + `scripts/curate_console_cases.py` (NEW) + `scripts/build.py` (console target + validator, additive)
- `console.html` → `dist/console/index.html` (NEW 4th ship artifact) + `tests/gate-console.test.mjs` (NEW, 68) + `tests/smoke-checklist.md` + `CLAUDE.md`

## Health Delta
- Tests +68 (NEW gate-console suite); build drift guard 5→6 artifacts; all 11 suites green at close; build.py +~200 lines additive; ZERO changes to frozen surfaces (grounding core, derived data, overlays, news pipeline; existing dists byte-identical — reviewer re-verified).

### Review Gate
- Unified reviewer: 9/10 ACCEPT, zero HIGH. MEDIUMs: (1) validate_console_cases provenance grep covers ".dev-wiki" but not bare "tmp/" — narrower than the stated invariant, 1-line widening candidate; (2) test stub omits the `adjudicated` key → only the ADJ='b' reveal branch exercised; (3) ledger "Clear session" lacks confirm/undo; (4) blueprint §1 pointer could name §9–§10 explicitly. T1 scope-glob MEDIUM fixed at this debrief.

### Gate Compliance
- Direction gate: approved, present (tasks.md gate-log `direction=approved`). Delivery gate: PENDING — flips post-commit via the delivery flow (gate-state follows git-state).

### Assumption-Ledger Revisit
- Phase 47: A1′ held (the spine shipped as reframed — table 5/5, chains written, no substrate-less workload) · A2 held (vision lab; design artifacts only, no program build) · A3 held (no external clock) · A4 held (§10 direction-not-ratio + adversarial grep green) · A5 held (dual-stream charter §5 + Class A in the taxonomy + the SAR row). Prior phases re-scanned: no late bites, 0 open rows. `scripts/check-assumption-ledger.sh` ABSENT — manual check: 0 blank revisit rows.

## Related
- [[phase-47-agentic-aml-program-design|Phase 47]] — parent phase

## Soft Observations / Phase 48 Candidates
- validate_console_cases provenance grep narrower than the invariant (no bare "tmp/" check) — 1-line widening, low practical risk. | reviewer MEDIUM
- gate-console stub: one boot with adjudicated:'a' would pin the reveal labeling both ways. | reviewer suggestion
- Ledger "Clear session" destroys the session record the artifact is about, one click, no confirm/undo. | reviewer suggestion
- Blueprint §1 honesty pointer could name §9–§10 explicitly. | reviewer suggestion
- CLAUDE.md 286 lines vs the ~200 contract target (263 pre-phase; +23 durable, not a leak — but the trend runs against the contract; trim residual now two phases old). | maintenance
- _ARCHITECTURE.md was 113 vs the 100 budget + missing the 4th artifact — updated + trimmed at this debrief. | staleness
- E-23 article frontmatter `source: web-research` vs the 136 existing `source: synthesize` — wiki-lint may flag; conscious new value (primary-source-fetched). | T1
- Console subset/curated-queue toggle consciously omitted (test pins the all-cases queue) — revisit only if the console is presented and 213 rows read as noise. | T5
- The blueprint's design-stage workload rows (transaction monitoring, case investigation, SAR/STR narrative) are Phase-48+/future-engagement candidates: each begins as conceptualization (name substrate + verifier, probe before agentifying) — suggested framing for the next /dev-plan gate alongside the §11 roadmap chains. | T2/T3
- Wiki-capture candidate: "OSFI E-23's model definition explicitly includes judgmental assumptions — a human-judgment gate layer is itself an in-scope model component; captured disposition rationale = lifecycle evidence" (pairs with the agent-runtime-adoption-probe entry already in the aml-wiki inbox). | T1
