# Spec — Phase 81: Consume substrate Phases 35–37 (the sanctions arc) + open-sanctions data-fork brief

> STANDARD ceremony. Cross-pillar consume (3 substrate phases) + a conditional ship-dist touch + a
> plan-only brief. Direction gate closed 2026-06-28 (AskUserQuestion — scope = "All three (+ P37
> geo)"; open-sanctions = "Plan-only brief + license matrix"; bar invariant = "Evidence-advance,
> rule frozen"; measure-first = "Accept both abort fallbacks"). Sibling HEAD code-verified LIVE this
> session (file:line, not loaded facts): aml-substrate @**f7fbdb0** (Phase 37); aml-casework
> unchanged at the Phase-79 pin @**076fb8e**.

## 1. Objective

Consume aml-substrate's three unconsumed emissions — the **sanctions arc** beyond signal-watch's
Phase-34 pin (`1f5901e` → HEAD `f7fbdb0`):

- **substrate Phase 35** (`4f49e53`) — *org-name* OFAC sanctions screening: the dead
  `Organization.sanctions_flag` made LIVE under `--anchored` via a label-blind real-OFAC-SDN **entity**
  name collision (the direct sibling of what signal-watch's Phase 80 consumed for *persons*).
- **substrate Phase 36** (`1651b1e`) — exposure-via-ownership leg (capability **C17**): a corroborating
  determination leg fired when a customer's beneficial owner / controlled entity carries a
  `sanctions_flag`, walked over the existing BO `RelationshipEdge` graph.
- **substrate Phase 37** (`5b5cf32`) — geo/jurisdiction enrichment: `counterparty_country` expands
  `{US,CA}` → 22 countries with a FATF high-risk tail (an observable, no leg yet).

Three consumes + a plan + true-ups:

1. **Merge console** — add an **OFAC org-name collision** case class (synthetic org's real-frequency
   legal name collides with a real public-domain OFAC SDN entity — *same latent entity / common-name
   false positive?*), scored against substrate's non-circular `GT-<hash>` oracle. The person-class's
   org sibling.
2. **Workbench §12** — consume the C17 **exposure-via-ownership leg** as a new EVIDENCE atom so a
   customer with a sanctioned beneficial owner + a *distinct* ML mechanism genuinely reaches the
   determination bar — the §12 breadth beat. Plus render P37's richer geo observable (no leg).
3. **Open-sanctions data-fork brief** (PLAN-ONLY) — a per-source license/compliance matrix + the
   non-commercial boundary + what substrate should emit (Stage-2/3 open reference data).

Plus: reconcile the now-stale substrate-P35 brief (TF + broader-C7 were substrate-CUT; org-name is
DONE), true up `cross-pillar-build-order.md`, re-pin substrate → `f7fbdb0`.

## 2. Context

- Substrate is **3 phases ahead** of our pin (we consumed Phase 34; 35/36/37 are the delta). The
  phase numbers in the two repos are independent (substrate-P34 ≠ signal-watch-P80).
- Substrate already ships a **REAL OFAC SDN watchlist** (`data/reference/watchlist_ofac.csv`, 2,500
  primary names, every-7th sample, US-Gov **public domain**); `data/reference/PROVENANCE.md` is
  explicit: *no substrate party IS a real designated person; the collision is coincidental-by-
  construction* — the false-positive-trap framing matches signal-watch's compliance posture exactly.
  The `sanctions_flag` is **label-blind synthetic** (`crc32` draw, `corr(flag, illicit) ≈ 0` proven).
- Substrate **CUT** the old P35-brief asks this session and retains them as honest-null artifacts: TF
  = `already-null` (no TF crime type; `{US,CA}`-only jurisdiction; high-blast gen change forbidden);
  broader-C7 = `tell-unavoidable` (at m=1 a pure magnitude screen, mules are the magnitude outliers,
  `corr` over the gate). So those two brief asks are **dead** — reconcile, don't pursue.
- Substrate's emission boundary: `SCREENING_EMISSION_DETECTORS` is **C8 + C14 only**; the new C17
  exposure detector is NOT in the emitted bundle (it READS, never generates) — so signal-watch
  COMPUTES the exposure leg itself from the rendered `related_parties[]` + `sanctions_flag`, not from
  a bundle firing. The org-sanctions (P35) + geo (P37) overlays ride `--anchored` on the producer side;
  all three phases prove substrate default-build byte-identical.
- **The engine derives legs from capabilities via profile DATA** (`evidence_requirements.determine`
  → `present_atoms()` reads `data/workbench/evidence-requirements.json`, counts `kind=="leg"` atoms).
  The engine never sees provenance → the C17 leg is a *profile-data atom + companion-side assembly*;
  `evidence_requirements.py` stays byte-frozen, and the same-OFAC-hit double-count dedup lives in the
  consume layer where provenance exists.
- casework (`076fb8e`) is unchanged from the Phase-79 pin; the workbench SIGN path is the existing
  one. casework does NOT ground C17 → a sanctioned-exposure case may DETERMINE (signal-watch engine)
  but not SIGN through casework (the Lakeshore-C3 fail-closed class); the determination is the demo
  beat, the casework SIGN gap is a NAMED handoff (not a phase blocker).

## 3. Constraints (LOAD-BEARING)

- **A1 guard:** `scripts/evidence_requirements.py` BYTE-UNCHANGED (`git diff --quiet`). The sufficiency
  RULE (mechanism + ≥2 independent legs + named predicate + no unrebutted mitigation) is byte-frozen.
- **Evidence-advance, rule frozen** (user-positioned): the C17 leg is a new EVIDENCE atom (profile data
  + companion assembly + same-hit dedup). Cases that NEWLY reach the bar do so by genuinely presenting
  ≥2 INDEPENDENT legs — reported measure-first as COUNTS. A determination-bar regression proves the
  RULE is unchanged and no determination rests on fewer-than-rule legs.
- **Double-count independence** (substrate's explicit warning): the C17 exposure leg and a C14
  escalation leg tracing to the SAME OFAC hit are NOT two independent legs (distinct only when they
  trace to DISTINCT sanctioned parties). The consume layer dedups by hit provenance before `determine`.
- **Firewall:** `build.py` imports no spine/scorer/sibling/curate (grep guard); the **8 non-merge
  ship dists byte-frozen** (`--check all`); `dist/merge` the ONE sanctioned re-freeze, GATED on T1a.
- **validate↔curate parity:** build.py `validate_merge_cases` mirrors `curate_merge_cases` EXACTLY
  (the Phase-76 lesson); the post-disposition `oracle` block never leaks into pre-adjudication
  evidence (`assert_no_*_leak`).
- **Compliance:** real OFAC **org** names ship clean under 17 USC §105 (US-federal public domain — the
  existing exception explicitly covers OFAC). Framed STRICTLY as the **false-positive trap** — the
  synthetic org is NEVER the sanctioned entity; never "we caught a sanctioned party." Badge always-on;
  synthetic-substrate-anchored qualifier governs any scored claim. **No CC-BY-NC data enters the repo
  (ship or companion) this phase** — OpenSanctions is plan-only.
- **Honesty governor:** no catch-rate / lift / precision / recall / multiplier wording (sweep DOCS too
  — the Phase-78 doc-gap lesson); a confusion or cohort count is never a catch-rate.
- **Measure-first:** T1 is the abort gate. The merge org track (T2/T4) runs ONLY on a clean two-sided
  non-circular T1a. The exposure leg (T3) ships as a determination advance ONLY on a non-degenerate
  T1b (fires + moves ≥1 case to the bar); else it ships as a rendered observable + a brief (honest
  null). The brief (T5) + P37 geo render run regardless.

## 4. Approach

Six tasks, measure-first gated (the Phase-79/80 pattern):

- **T1 (the dual gate)** — run substrate @f7fbdb0 `--anchored --emit-eval-oracles` + the screening
  bundles as TOOL-USE (subprocess, the curate pattern; build.py never imports it). **T1a:** distill the
  org-collision slice; assess two-sidedness (some collisions TRUE latent-entity matches [uphold] + some
  common-name false positives [reject], split non-circularly by `GT-<hash>`). **T1b:** measure the C17
  exposure cohort — does it fire non-degenerately, and (with the same-hit dedup) does ≥1 case reach the
  bar BECAUSE of the exposure leg? Commit no-substrate-replayable captures; document both gate decisions.
- **T2 (gated T1a)** — curate the `sanctions-org-collision` basis into `data/merge/cases.json`
  (validate↔curate parity; firewall held; org emails domain-masked).
- **T3 (gated T1a)** — render the org false-positive-trap framing in `merge.html`; rebuild + re-freeze
  `dist/merge`; extend `tests/merge-console.test.mjs`.
- **T4 (L; the exposure leg gated T1b)** — add the C17 leg atom to the profile (`evidence-requirements.json`);
  assemble it + the same-hit dedup in `serve_workbench`; render the §12 sanctioned-BO-exposure beat in
  `workbench.html`; render P37's geo observable (no leg). `evidence_requirements.py` byte-unchanged;
  determination-bar regression proves the rule frozen + ≥2-independent-leg determinations.
- **T5 (always)** — `docs/open-sanctions-data-fork-PLAN-BRIEF.md` (per-source license matrix +
  non-commercial boundary + substrate emit asks) + reconcile the stale substrate-P35 brief +
  `cross-pillar-build-order.md` true-up + re-pin substrate `f7fbdb0` + the casework-C17-SIGN-gap note.
- **T6 (always)** — full verification: `--check all`, A1 byte-unchanged + the determination-bar
  regression, build.py firewall grep, validate↔curate parity, `uv run pytest`, the .mjs arcs, the
  honesty word-ban (incl. the new doc), CLAUDE.md true-up.

## 5. Scope

`scripts/curate_merge_cases.py` · `data/merge/cases.json` · `scripts/build.py` (validate_merge_cases) ·
`merge.html` · `dist/merge/**` · `tests/merge-console.test.mjs` · `tests/fixtures/merge-sanctions-org-oracle/**` ·
`data/entity-spine/**` · `scripts/resolution_scorer.py` · `scripts/curate_workbench_cases.py` ·
`scripts/serve_workbench.py` · `data/workbench/**` (incl. `evidence-requirements.json`) · `workbench.html` ·
`tests/workbench.test.mjs` · `docs/*-PLAN-BRIEF.md` · `docs/cross-pillar-build-order.md` · `CLAUDE.md` ·
`.dev-wiki/tasks.md`. **NO change to `scripts/evidence_requirements.py`.**

## 6. Exit criteria

- T1a + T1b captures committed + replay with NO substrate; both gate decisions documented; firewall holds.
- IF T1a two-sided: `--check all` 9/9 (8 byte-frozen + `dist/merge` re-frozen with the org class);
  `node tests/merge-console.test.mjs` green incl. the org basis; validate↔curate parity; honesty word-ban.
  IF one-sided/flaky: `dist/merge` BYTE-FROZEN; a substrate org-emit-two-sidedness brief; honest non-result.
- IF T1b non-degenerate: the C17 exposure leg lights ≥1 case to the determination bar via ≥2 INDEPENDENT
  legs; the determination-bar regression proves the RULE frozen; `git diff --quiet scripts/evidence_requirements.py`;
  `node tests/workbench.test.mjs` green; gather/workbench harnesses pass.
  IF degenerate: the leg ships as a rendered observable + a brief (honest null); no false §12-advance claim.
- The open-sanctions data-fork brief exists with the per-source license matrix + the non-commercial
  boundary; the stale substrate-P35 brief reconciled (TF/C7 cut, org-name done); cross-pillar-build-order
  trued up to substrate-P37 HEAD; the casework-C17-SIGN-gap noted; substrate re-pinned `f7fbdb0`;
  `uv run pytest` green.

## 7. Risks / assumptions

- **A1 [HIGH, weakest, measure-first]:** the C17 exposure leg is A1-preservable (profile data +
  companion assembly) AND adds genuine §12 breadth (≥1 case reaches the bar via ≥2 independent legs).
  The risk: the cohort is degenerate (~10–12 customers; some already determined without it) → an
  honest null. → measure-first T1b; degenerate ⇒ leg ships as a rendered observable + a brief.
- **A2 [HIGH, measure-first]:** substrate Phase 35's `--anchored` ORG emit yields a TWO-SIDED,
  non-circular merge oracle (like the person class). "Label-blind collision" risks all-false-positive-
  by-construction → one-sided (the Phase-77 trap). → measure-first T1a; one-sided ⇒ ABORT merge org
  track (T2/T3) + a substrate org-emit brief; the exposure leg + brief + geo still land.
- **A3 [MED, the bar invariant]:** the sufficiency RULE stays byte-unchanged; new determinations rest
  on genuinely ≥2 independent legs (the same-OFAC-hit dedup enforces independence). → determination-bar
  regression in the workbench selftest (a sanctioned-BO case reaches the bar WITH the leg, is WITHHELD
  without it; exposure + same-hit C14 count as ONE leg).
- **A4 [MED]:** real OFAC org names ship clean (17 USC §105), false-positive trap; OpenSanctions stays
  plan-only (no CC-BY-NC bytes in the repo).
- **A5 [MED]:** `dist/merge` is the ONE sanctioned re-freeze (3rd consecutive phase); 8 non-merge dists
  byte-frozen; validate↔curate parity held.
- **A6 [LOW]:** casework unchanged at `076fb8e`; the C17-SIGN gap is a named handoff, not a blocker (the
  determination is the demo beat).

## 8. Checkpoints

- **T1 DUAL ABORT GATE** — after the emit + scoring, STOP and report (a) the org two-sidedness count +
  the merge gate decision, (b) the exposure-leg cohort + the moves-to-bar count + the leg gate decision,
  before T2/T3/T4 touch any dist or profile. One-sided org ⇒ merge org track does not run; degenerate
  exposure ⇒ the leg degrades to an observable + a brief.
- Post-T3/T4 — adversarial review (the Phase-79 staleness lesson: verify the committed `cases.json` +
  `evidence-requirements.json` CONTENT + `git status` + the specific `--check <target>`, not the
  "wrote…" log; sweep the new brief through the honesty governor).

## 9. Out of scope

- The substrate P35+ BUILD itself (TF/C7 are substrate-CUT; org-sanctions/exposure/geo are what we
  consume; Stage-2/3 open data is brief-only).
- A C20 high-risk-jurisdiction determination leg (P37 is observable-only this phase; the C20 leg is a
  named future item, must control for txn-volume per substrate's caveat).
- Any `evidence_requirements.py` change (A1); casework grounding C17 (a named handoff); integrating any
  real cross-jurisdiction sanctions dataset (the open-sanctions thread is plan-only); the carried
  Lakeshore IND-05/IND-02 grounding-faithfulness fix.
