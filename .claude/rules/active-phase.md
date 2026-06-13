# Active Phase Context

Phase: 50 — AML program build: the demo became the program. A major user REFRAME at the dev-plan gate (2026-06-12): build the blueprint's §3 design-stage workloads as REAL systems, **one real-system-class repo per pillar**. signal-watch is now the program-ARCHITECTURE home (blueprint + this lifecycle record only); the build lives in sibling repos.

Pillar 1 = the **data substrate** → **`/Users/jwang/aml-substrate`** (Python; ultra-realistic synthetic Canadian retail-banking data where ML typologies EMERGE from modeled behavior). Its DESIGN.md holds the architecture, schema + distribution spec, gate, and cited sources. **aml-substrate Phases 1 (Foundation) + 2 (Emergence) DELIVERED 2026-06-13** — commits 44ad9b1→5632816, 83 tests green: population/KYC graph + 6-channel background engine + net-new EMT detail (P1); criminal/mule/shell designation + fresh-Python laundering engine + transitive labeling + coverage checklist + the A1 permutation-null separability gate + emergence realism (P2). ~161s/1M scale; 1:21,657 imbalance calibration; structuring breaks Benford. **Active: aml-substrate Phase 3** — FINTRAC reporting + alert/case monitoring layer (signals fire over the labelled substrate → grounded alerts, the §3 monitoring workload).

Doctrine (aml-substrate): data-first/emergent (typologies emerge, NEVER injected/stamped); deterministically SCRIPTED generation, no runtime LLM (small statistical models OK; LLM only authors scripts); grounded in researched REAL schemas + distributions; everything SYNTHETIC, no real customer data, ever.

Note: the `/dev-*` skills anchor to this session's root (signal-watch) and don't operate cross-repo. aml-substrate tracks its own phases in DESIGN.md + docs/; lifecycle bookkeeping for it is hand-authored (or run the dev-* skills from a session rooted there).

FROZEN (signal-watch — no further demo work this track unless re-opened): the 5 ship artifacts + dists byte-identical (index.html + config + 3 typology dists; corpus.html + dist/corpus; news.html + dist/news; console.html + dist/console; triage.html + dist/triage); derive_signals.py; news pipeline; all committed derived data + the 3 overlays; docs/program-blueprint.md + blueprint-report.html.

Abort rule: existing signal-watch dists drift → STOP and surface (never re-baseline).

Gates (Phase 50, program-kickoff direction gate — closed 2026-06-12, all_accept: false):
- [x] Direction confirmed by user (A1 foundation-first/emergence-ready accept · A2 build-on-research [user override of review-first] · A3 1M-scale reject→small-first · A4 hybrid eyes-open→deferred to phase 2; ledger Phase-50 block, revisit-status recorded at Phase-1 delivery)
- [x] aml-substrate Phase 1 (Foundation) delivered 2026-06-13 (54 tests; A1 proven, A3 validated, A2 held, A4 deferred)
- [x] aml-substrate Phase 2 (Emergence) delivered 2026-06-13 (83 tests; A1 measured-not-assumed via the separability gate, A2 bounded, A3 fresh works, A4 1:21k validated at scale, A5 no migration)

Per-pillar/per-phase gates for aml-substrate are tracked in that repo (DESIGN.md §8 + docs/).
