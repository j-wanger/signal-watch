# Cross-pillar build order (verified snapshot)

> **A signal-watch-authored coordination snapshot — the program-level "what's next, in what order" view
> across the 3 pillars.** Per-gap detail lives in the `*-PLAN-BRIEF.md` files; this is the sequencing over
> them. **Code-verified 2026-06-26** against these live HEADs — **re-verify before acting; sibling state
> drifts between sessions:**
> - **aml-substrate** `f2da3e4` (Phase 30, `main`) — *advanced from `fc98b09` since the last snapshot*
> - **aml-casework** `b3546d4` (Phase 18, `feat/phase-1a-deterministic-verifiers`) — *advanced from `4a858e6`*
> - **signal-watch** `b18ef71` (Phase 76, `main`)
>
> Synthetic / illustrative; no catch-rate, lift, or precision asserted.
>
> **UPDATE 2026-06-26 (Phase 78):** aml-substrate advanced **`f2da3e4` → `9677a37` (Phase 31 — emit-cli-wiring)**,
> which CLI-wired `--emit-eval-oracles`. signal-watch **Phase 78 CONSUMED** the now-reachable
> `eval/intended_disposition.json` → the **determination-validation harness** (the "circularity exit", Track-C′
> item 2 below) + a **§12 discovery feed** in the workbench (companion-only; `evidence_requirements.py` +
> all 9 dists byte-frozen). The merge real-66 stays CONSENSUS (substrate Phase 31's own commit re-confirms the
> slice is all-singleton — still circular). Doc: `docs/determination-validation.md`.
>
> **UPDATE 2026-06-27 (Phase 79 — the consumes LANDED):** both Phase-77-deferred blocks resolved sibling-side
> + consumed. aml-casework advanced **`b3546d4` → `076fb8e` (Phase 19, `ed93a0d`)** — `_c3_fan_in` built; aml-substrate
> advanced **`9677a37` → `c099259` (Phase 32/33)** — the `--anchored` fork mints NON-circular `GT-<hash>` identity
> clusters (`entity_ref ≠ cluster`). signal-watch **Phase 79 CONSUMED both**: (1) **Track-C′ item 3** — re-vendored
> casework + the north-star **Lakeshore CASE-B SIGNS `cleared`** end-to-end via fan-in C3 (the matched pair closes,
> both via casework). (2) **Track-C′ item 1** — the merge console's real population **SUPERSEDED** the consensus-66
> with **29 substrate-anchored SCORED cases** (genuinely two-sided: 13 uphold / 16 reject, scored against the
> non-circular `GT-` oracle; the Phase-77 circular-oracle abort CURED). `dist/merge` re-frozen; the other 8 dists +
> `evidence_requirements.py` byte-frozen. The three handoff briefs are now CLOSED/RESOLVED (see their banners).
> Substrate open-data **Stage 2/3** + casework's CI-promotion criterion remain the open sibling frontiers.
>
> **UPDATE 2026-06-27 (Phase 80 — the Phase-34 sanctions-screening consume LANDED):** aml-substrate advanced
> **`c099259` → `1f5901e` (Phase 34 — seam-5 sanctions screening)** — `sanctions_flag` made LIVE under `--anchored`
> via a label-blind OFAC-watchlist name collision + a revived non-tautological C14 (the escalation-gap branch).
> signal-watch **Phase 80 CONSUMED both halves**: (a) the **merge console** gained an **OFAC name-collision case
> class** — a third SCORED population (24 cases, two-sided 11 uphold / 13 reject) where the merge question is
> entity resolution under sanctions screening (a flagged record + its same-person fragment that evaded screening
> = uphold; two strangers sharing a watchlisted name = the common-name false positive = reject); `dist/merge`
> re-frozen (the ONE sanctioned dist touch; the 8 non-merge dists + `evidence_requirements.py` byte-frozen). (b) the
> **workbench §12** gained a **non-tautological sanctions-driven C14 leg** (companion-only): a C14-PURE party leaf
> (`data/casefile/sanctions-c14-demo.bundle.json`) lights the **KYC-A1** determination atom from a real sanctions
> signal — and casework's **Phase-19 party-leaf C14 grounding** (re-vendored @076fb8e) **SIGNS** it end-to-end
> (disposition `file`), the txn-less party-leaf C14 that used to fail-closed at casework's no-transactions contract.
> The measure-first gate cleared GREEN (the two-sidedness is genuine, from the Phase-32 fragment overlay running
> alongside sanctions; no one-sided abort). The remaining frontier is **substrate P35+** (TF slice / broader C7 /
> org-name sanctions / open-data Stage 2/3 — `docs/substrate-p35-determination-signals-PLAN-BRIEF.md`) +
> casework's CI-promotion criterion. **C1/ML-A6 is a documented measured null, not an ask.**
>
> **UPDATE 2026-06-28 (Phase 81 — the sanctions ARC consume; two measure-first NON-RESULTS, one observable):**
> aml-substrate advanced **`1f5901e` → `f7fbdb0` (Phases 35/36/37)** — P35 org-name OFAC screening (`4f49e53`),
> P36 exposure-via-ownership C17 (`1651b1e`), P37 geo enrichment (`5b5cf32`). aml-casework UNCHANGED at `076fb8e`
> (does NOT ground C17). signal-watch **Phase 81** consumed the arc HONESTLY — both planned consumes hit their
> measure-first abort/degenerate branches; the value landed in observable + briefs:
> - **(merge org-name collision) → ABORTED (structurally one-sided).** substrate fragments PERSONS but NOT orgs
>   (0 org fragment clusters), so every org-name collision is between distinct orgs → all-reject. `dist/merge`
>   BYTE-FROZEN (no touch); → **[`substrate-org-fragment-emit-PLAN-BRIEF.md`](substrate-org-fragment-emit-PLAN-BRIEF.md)**.
> - **(C17 exposure-via-ownership) → DEGENERATE as a determination leg; shipped OBSERVABLE-ONLY.** 13 customers
>   carry a sanctioned BO; ALL oracle-clear (label-blind, corr≈0); a C17 leg moves 0 to the bar (the cohort lacks
>   a laundering mechanism). The workbench surfaces the exposure as a screening OBSERVABLE (a `/sanctions-c17-exposure`
>   route + panel + `data/casefile/sanctions-c17-exposure-demo.bundle.json`) and the live engine SHOWS it does NOT
>   reach the bar — `evidence_requirements.py` + the profile BYTE-UNCHANGED (no atom that never fires). Determination-leg
>   follow-on → **[`substrate-exposure-signal-PLAN-BRIEF.md`](substrate-exposure-signal-PLAN-BRIEF.md)**.
> - **(P37 geo) → CONSUMED as an observable** (`counterparty_country` beyond US/CA; no leg). A C20 high-risk-jurisdiction
>   determination leg is a named future item (MUST control for txn-volume — substrate's caveat).
> - **(open sanctions datasets, non-commercial)** — the SHIP-compliance license matrix authored:
>   **[`open-sanctions-data-fork-PLAN-BRIEF.md`](open-sanctions-data-fork-PLAN-BRIEF.md)** (OFAC PD / UK OGL → ship;
>   OpenSanctions CC-BY-NC → no-ship; the demo's buy-in purpose is plausibly commercial). The P35 brief is RECONCILED:
>   TF + broader-C7 were substrate-CUT (already-null / tell-unavoidable); org-name built-but-one-sided.
> - **casework C17-SIGN gap (NEW, named):** casework does NOT ground C17, so a sanctioned-exposure case would DETERMINE
>   (signal-watch engine) but not SIGN through casework — a named handoff, moot this phase (the C17 consume is
>   observable-only, no determination to sign). The remaining open frontiers: substrate org-fragment emit + the
>   discriminating-exposure-signal + open-data Stage 2/3 + a C20 jurisdiction leg; casework's CI-promotion criterion
>   + C17 grounding.
>
> **UPDATE 2026-06-29 (Phase 82 — the north-star DECISION-EVIDENCE consume + casework re-vendor; one measure-first abort):**
> aml-substrate advanced **`f7fbdb0` → `294d3e5` (Phases 38/39/40)**; aml-casework **`076fb8e` → `04cc335` (Phases 20/21)**.
> signal-watch **Phase 82** consumed three of four READY emissions; the fourth aborted measure-first:
> - **(P39 predicate + P40 mitigation → the §12 loop closes from GROUNDED evidence at scale)** — CONSUMED into the
>   workbench (`serve_workbench.determine_case` READS the prior-STR predicate + reconciled mitigation from each
>   bundle; `evidence_requirements.py` BYTE-UNCHANGED, the A1 guard). On the 376-case slice: **1 KYC-integrity
>   determination** (grounded prior-STR predicate; 31 over the full 23,651-customer population) + **17 affirmative
>   `cleared`** (reconciled source-of-funds — the Lakeshore thesis at scale). HONEST BOUND: the predicate does NOT
>   advance the **ML** file loop (0 slice ML cases have mechanism + 2 legs lacking only the predicate) → substrate
>   Ask #3 (the second leg) stays the dominant ML blocker. The 8 non-merge dists + `dist/merge` byte-frozen
>   (companion-only). → [`substrate-northstar-evidence-emission-PLAN-BRIEF.md`](substrate-northstar-evidence-emission-PLAN-BRIEF.md) #1/#2 CONSUMED.
> - **(casework P20 C15/C4 reconcile → north-star FILES SIGN at scale)** — re-vendored `04cc335`; the slice's
>   end-to-end SIGNED coverage moved from **128/376 to 256/376** (the C15-throughput + C4 any-channel cases that
>   fail-closed now sign; verifier strictness intact). → [`casework-northstar-signing-PLAN-BRIEF.md`](casework-northstar-signing-PLAN-BRIEF.md) #2 LANDED.
> - **(P38 org-fragment → the merge ORG-collision class) → ABORTED measure-first (still one-sided).** substrate
>   BUILT the org fork (364 `O-FRAG` records, 16 flag-intersected), but on signal-watch's OWN distill/scorer path
>   the fragments share NO resolution handle (perturbed name + fresh corp#/address — no shared identifier), so
>   they never become merge CANDIDATES → 0 uphold, all-reject. `dist/merge` BYTE-FROZEN (untouched); the SHARPENED
>   ask (retain a shared incorporation_number/address handle) → [`substrate-org-fragment-emit-PLAN-BRIEF.md`](substrate-org-fragment-emit-PLAN-BRIEF.md).
> - **Still OPEN:** substrate Ask #3 (second corroborating leg — the ML file-loop blocker) + Ask #4 (ownership
>   edges) + the org-fragment resolution handle + a C20 jurisdiction leg + open-data Stage 2/3; casework's
>   CI-promotion criterion + C17 grounding + the txn-bearing-C14 sign frontier.

## What changed since the last snapshot

Both siblings executed the prior build order. **Tracks A and B are now largely DONE; the work shifts to
signal-watch consuming the three new emissions, plus a new substrate realism FORK.**

- **substrate Phase 29** — slice-aligned `true_entities` emission (`identity/true_entities.json`, firewalled,
  100% coverage). ✓ CODE EXISTS — **but `emit_true_entities` is UNWIRED into the substrate CLI** (called only in
  substrate tests). *Critical nuance (Phase-77 finding): clusters are content-addressed `ENT-<entity_ref>` — a 1:1
  relabel of `entity_ref`, the SAME field the spine keys on → a CIRCULAR oracle for the real merge cases (agreement
  is true-by-construction, no discriminating signal). Even wired, it can't score the spine's real refusals honestly.*
- **substrate Phase 30** — `exogenous-disposition-label` (`eval/intended_disposition.json`, `file|clear` authored
  blind to the sufficiency rule). ✓ CODE EXISTS — **also UNWIRED into the CLI** (`emit_intended_disposition` is
  test-only). Both gaps → the `substrate-emit-cli-wiring-PLAN-BRIEF.md` handoff.
- **casework Phase 17** — reconciliation tripwires wired to an advisory (warn-never-fail, non-required) CI lane.
  ✓ DONE. *No promotion-to-blocking criterion yet — a named follow-on.*
- **casework Phase 18** — the `cleared` affirmative-dismissal verdict (CW-4). ✓ DONE; file bar byte-unchanged.

## Phase 77 outcome (signal-watch, implemented — the Track-C′ consume)

The three consumes landed with two honest pivots forced by the CLI-unwiring discovery above:

1. **`true_entities` → merge console real 66.** ⛔ **DEFERRED at the abort rule (oracle is CIRCULAR).** The
   attempt: capture the slice's identity ground truth from substrate's `--identity` parquet → score the 66. The
   finding: substrate's emitted clusters are content-addressed **`ENT-<entity_ref>` — a 1:1 relabel of `entity_ref`,
   the SAME field the spine keys its refuse/merge on.** So "66/66 correct-rejection" is true-by-construction (zero
   discriminating signal), not a measurement. Presenting it as scoring would breach A4 / the abort rule. The real-66
   stay **CONSENSUS** (Phase-76 framing, no oracle); `dist/merge` UNCHANGED (byte-frozen). A non-circular real merge
   oracle needs `entity_ref ≠ cluster` — a genuine identity layer (household/fragment merges) or the open-data fork's
   real collisions (Track B′). The synthetic-13 scoring is sound + untouched (genuinely two-sided). *The
   `substrate-emit-cli-wiring` brief is re-scoped: wiring the CLI is necessary but NOT sufficient — substrate must
   emit a true-identity layer, not an entity_ref echo.*
2. **`intended_disposition` → determination validation harness.** ⛔ DEFERRED — the emit is CLI-unwired (can't curate
   the oracle at build time without a substrate CLI run). Re-scoped to the `substrate-emit-cli-wiring-PLAN-BRIEF.md`
   handoff (wire BOTH emissions). The engine-vs-exogenous-label harness builds once substrate emits from its CLI.
3. **`cleared` → DECIDE signs a documented dismissal.** ✓ CONSUMED via a C5-replayable proxy: re-vendored casework
   `→b3546d4`, authored `data/casefile/cleared-demo.bundle.json` (C5 cash-placement, `exculpatory:true`), passes
   `--disposition cleared` → **casework SIGNS `cleared` end-to-end**. The north-star **Lakeshore CASE-B still
   fails-closed** (casework's C3 is fan-OUT-only; Lakeshore's is fan-IN) → the `casework-c3-fan-in-PLAN-BRIEF.md`
   handoff. The A3 abort held — no fan-out pattern fabricated to force the sign.

## Build order — now

### Track C′ — signal-watch CONSUME (the active next phase; Phase 77 candidate)
The bottleneck moved here. Three consumes, in rough value order:
1. **Consume Phase 29 `true_entities` → score the merge console's real 66.** `curate_merge_cases.py` reads
   `identity/true_entities.json`, looks up each SHARES pair's clusters → flips the 66 from consensus to scored.
   Honest result: **66/66 correct-rejection** (the spine's refusals confirmed against substrate's declared-identity
   truth). Frame the one-sidedness explicitly (no should-merge in the real slice). Rebuilds `dist/merge`.
2. **Consume Phase 30/31 `intended_disposition` → a determination-engine validation harness** (the circularity exit):
   pass bundles (no label) through `evaluate_sufficiency` → compare to the exogenous `file|clear`. Companion-only,
   synthetic-only-qualified. The highest *strategic* consume (validates the engine against an oracle it didn't make).
   ✓ **DONE — signal-watch Phase 78** (`scripts/determination_validation_harness.py`; unblocked once substrate
   Phase 31 CLI-wired `--emit-eval-oracles`). Bundle-only frame (mechanism + ≥legs; human-gate inputs held out =
   non-circular); 6935-case slice → the ML signal layer discriminates (file-ready on far more oracle-file than
   oracle-clear) but misses most file cases (§12 gap), and the KYC bar is a structural over-flag (a source-of-funds
   gap alone is not laundering). Surfaced as the workbench §12 discovery feed. Doc: `docs/determination-validation.md`.
3. **Consume casework Phase 18 `cleared` → the Lakeshore DECIDE signs a documented dismissal.** Re-vendor
   `bf15535→b3546d4` (`scripts/vendor_casework.sh`); shape the Lakeshore case into a **casework-contract bundle**
   (v0.1, an `exculpatory:true` txn + neutral/exculpatory claims) and pass `--disposition cleared`. Completes the
   rich-case loop (Lakeshore signs `cleared` via casework, not just signal-watch's own engine).

### Track B′ — aml-substrate, next (the realism FORK; parallel, contract-neutral)
- **The open-reference-data fork** — anchor the synthetic universe to open data (GLEIF CC0 ownership + Census/SSA
  names + OSM/GeoNames addresses + government sanctions/FATF anchors), routing around the 4 NC/ND/SA/paid traps.
  Brief: [`substrate-open-reference-data-fork-PLAN-BRIEF.md`](substrate-open-reference-data-fork-PLAN-BRIEF.md)
  (`f2da3e4`). It's realism of *values*, not *contract* — consumers read the same shape. Direct payoff: makes the
  merge console's real cases real-shaped collisions (not the artificial noise floor) and gives `true_entities` a
  non-trivial, two-sided oracle. **Sequence after the Track C′ consume settles** unless the artificial collision
  floor is judged the demo's current weak point.
- *(optional)* a `true_entities` refinement: emit clusters from substrate's genuine identity LAYER (the
  `--identity` household/fragment merges) rather than content-addressed-from-`entity_ref`, so the real-data oracle
  becomes two-sided. Folds naturally into the fork.

### Track A′ — aml-casework, next
- **Promotion criterion for the advisory CI lane** (N clean cycles, zero false positives → blocking) — the named
  follow-on from Phase 17.
- The speculative C15/C3/C4 widening stays **dropped** (not data-reachable; documented audit trail only).

### Track D′ — AGENTIFICATION (signal-watch-run, cross-cutting; parallel, blocks no one)
- signal-watch RUNS the agents; substrate + casework are the deterministic producers/verifiers. The 4 live
  loops (news/corpus extraction · GATHER · DECIDE drafting) are built; the next loops sequence by leverage:
  a merge adjudicator scored vs the GT-`<hash>` oracle (the measured-quality headline) → a §12 determination
  pre-proposer → a real STR drafter → a §14 triage second-rater. Each is companion-only, under the
  propose→gate→decide discipline (no ship dist / frozen gate touched). Detail:
  [`agentification-roadmap.md`](agentification-roadmap.md); contract = `program-blueprint.md` §2/§4/§6/§11.

## Critical path

The prior bottleneck (`substrate true_entities`) is **resolved** — it's emitted. The only remaining serial
dependency is **signal-watch's Track C′ consume** of what already exists; nothing blocks it. The substrate
realism fork (Track B′) and casework's promotion criterion (Track A′) run in parallel and block no one.
