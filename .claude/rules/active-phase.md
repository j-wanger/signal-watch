# Active Phase Context

**Phase 81 — *Consume substrate Phases 35–37: the sanctions arc* — OFAC org name-collision merge class + the C17 exposure-via-ownership §12 leg + geo + open-sanctions data-fork brief** (signal-watch-local, STANDARD) — PLANNED 2026-06-28. Consume aml-substrate's three unconsumed emissions beyond the Phase-34 pin (`1f5901e` → HEAD @**f7fbdb0**, Phase 37): P35 org-name OFAC screening (`4f49e53`), P36 exposure-via-ownership C17 leg (`1651b1e`), P37 geo enrichment (`5b5cf32`). casework unchanged @**076fb8e** (does NOT ground C17 — a named SIGN-gap handoff). Both sibling states code-verified LIVE this session (file:line, not loaded facts).

## Objective
Three consumes + a plan: (1) **merge console** — an OFAC ORG-name collision case class (synthetic org's real-frequency legal name collides with a real public-domain OFAC SDN entity → *same latent entity [uphold] vs common-name false positive [reject]*; the Phase-80 person-class's sibling), MEASURE-FIRST gated; (2) **workbench §12** — the C17 exposure-via-ownership leg consumed as a NEW EVIDENCE atom (a customer with a sanctioned beneficial owner + a DISTINCT ML mechanism reaches the determination bar via ≥2 INDEPENDENT legs), MEASURE-FIRST gated; + render P37's geo observable (no leg); (3) **PLAN-ONLY** `docs/open-sanctions-data-fork-PLAN-BRIEF.md` (per-source license matrix + the non-commercial boundary). + reconcile the stale substrate-P35 brief + cross-pillar true-ups + re-pin substrate `f7fbdb0`.

## Scope
`scripts/curate_merge_cases.py` · `data/merge/cases.json` · `scripts/build.py` (validate_merge_cases) ·
`merge.html` · `dist/merge/**` · `tests/merge-console.test.mjs` · `tests/fixtures/merge-sanctions-org-oracle/**` ·
`data/entity-spine/**` · `scripts/resolution_scorer.py` · `scripts/distill_sanctions_slice.py` ·
`scripts/curate_workbench_cases.py` · `scripts/serve_workbench.py` · `data/workbench/**` (incl. `evidence-requirements.json`) ·
`workbench.html` · `tests/workbench.test.mjs` · `docs/*-PLAN-BRIEF.md` · `docs/cross-pillar-build-order.md` ·
`CLAUDE.md` · `.dev-wiki/tasks.md`. **NO change to `scripts/evidence_requirements.py`.**

## Key constraints (LOAD-BEARING)
- **A1 guard:** `evidence_requirements.py` BYTE-UNCHANGED (`git diff --quiet`). The sufficiency RULE byte-frozen.
- **Evidence-advance, rule frozen** (user-positioned): the C17 leg is a profile-DATA atom (`evidence-requirements.json`) + companion assembly — the engine derives legs from capabilities, never sees provenance. New determinations rest on genuinely ≥2 INDEPENDENT legs; the same-OFAC-hit double-count dedup lives in the consume layer. Proven by a determination-bar regression (case reaches the bar WITH the leg, WITHHELD without it).
- **Firewall:** build.py imports no spine/scorer/sibling/curate (grep guard); the **8 non-merge dists byte-frozen**; `dist/merge` the ONE sanctioned re-freeze, GATED on T1a two-sided.
- **validate↔curate EXACT parity** (Phase-76); the post-disposition `oracle` never leaks pre-adjudication (`assert_no_*_leak`).
- **Compliance:** real OFAC ORG names ship clean under 17 USC §105 (US-federal public domain — covers OFAC), framed STRICTLY as the **false-positive trap** — the synthetic org is NEVER the sanctioned entity. **OpenSanctions CC-BY-NC = PLAN-ONLY — NO CC-BY-NC bytes in the repo (ship or companion).** Badge always-on; synthetic-substrate-anchored qualifier.
- **Honesty governor:** no catch-rate/lift/precision/recall/multiplier wording (sweep DOCS too — the Phase-78 lesson).
- **Measure-first:** T1 is the dual abort gate; the merge org track (T2/T3) runs ONLY on a clean two-sided non-circular T1a; the exposure leg ships as a §12 advance ONLY on a non-degenerate T1b; the brief (T5) + P37 geo + verification (T6) run regardless.

## Exit criteria
T1a + T1b captures committed + no-substrate replayable + both gate decisions documented. IF T1a two-sided: `--check all` 9/9 (8 byte-frozen + `dist/merge` re-frozen with the org class); `node tests/merge-console.test.mjs` green incl. the org basis; validate↔curate parity; honesty word-ban held. IF one-sided: `dist/merge` BYTE-FROZEN + a substrate org-emit brief. IF T1b non-degenerate: the C17 leg lights ≥1 case to the bar via ≥2 INDEPENDENT legs; the determination-bar regression proves the RULE frozen; `git diff --quiet scripts/evidence_requirements.py`; `node tests/workbench.test.mjs` green. IF degenerate: the leg ships as a rendered observable + a brief (honest null). The open-sanctions data-fork brief exists with the license matrix + non-commercial boundary; the stale substrate-P35 brief reconciled (TF/C7 cut, org-name done); cross-pillar-build-order trued up to f7fbdb0; the casework-C17-SIGN gap noted; `uv run pytest` green.

## Abort rule
Any UNSANCTIONED ship dist drift (the 8 non-merge dists, or `dist/merge` before its T1a gate passes) / a build.py spine-scorer-sibling-curate import / an `evidence_requirements.py` change (incl. one forced by the C17 dedup — surface it, don't silently touch) / a real OFAC name framed as a real sanctions catch (not the false-positive trap) / any CC-BY-NC dataset committed to the repo / a cohort or confusion count presented as a catch-rate/precision/lift/recall → STOP-and-surface. Measure-first: T1a one-sided/tautological → STOP the merge org track (T2/T3 do NOT run) to a brief; T1b degenerate → the C17 leg degrades to a rendered observable + a brief.

## Gates
- [x] spec (`specs/phase-81-consume-substrate-sanctions-arc.md`)
- [x] Direction confirmed by user (2026-06-28, AskUserQuestion — Q1 "All three (+ P37 geo)" · Q2 "Plan-only brief + license matrix" · Q3 "Evidence-advance, rule frozen" · Q4 "Accept both abort fallbacks"; assumption positions taken, no unresolved reject/don't-know; ledger Phase-81)
- [ ] Delivery accepted (post-implementation report)

Spec `specs/phase-81-consume-substrate-sanctions-arc.md`; plan
[[phases/phase-81-consume-substrate-sanctions-arc]]; ledger Phase-81.
