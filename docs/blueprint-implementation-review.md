# Blueprint–Implementation Reconciliation Review

> **Status: DESIGN.** This is a design-review companion to `docs/program-blueprint.md` — it
> trues the blueprint up against what is actually committed across three repositories. It is
> NOT a ship artifact and NOT a status tracker; the blueprint stays a design document. The
> always-on **"Illustrative data & outputs"** honesty posture applies to every number and
> artifact named below — pillar implementations run on SYNTHETIC data at probe/demo scale.
>
> **Audit grounded against three pinned HEADs:**
> - `signal-watch` (program-architecture home + demo ship artifacts) — corpus-reference pin
>   **@472b44e**; the live repository HEAD where the audited artifacts are committed is
>   **@67dbd65** (verified `67dbd6506503cf0cac23ad71e8dbd4e7f2c5a6a8`). Every signal-watch
>   artifact citation below was opened at `67dbd65`.
> - `aml-substrate` (Pillar 1 — data substrate + detection layer) — **@34400e2**
>   (verified `34400e27ee63b8826c0be1abe6950c3316bacd0d`).
> - `aml-casework` (Pillar 2 — case → composition → SAR) — **@c6d8401**
>   (verified `c6d8401a242963a3f4dbd6784f6b528bdaee994e`).
>
> **Phase-61 cross-pillar re-ground (batched, verify-first).** This phase also re-grounded the two
> cross-pillar artifacts to the current sibling HEADs: `signal_coverage_map.py`'s pin + `e2e_chain_check.py`'s
> `GROUNDING_HEADS` moved `aml-substrate 9c75c03 (P18) -> 34400e2 (P20)` (casework unchanged @c6d8401). The
> diff `git diff 9c75c03..34400e2` showed P19/P20 touched NO `detectors/`/`views/` file (only the composition
> stress-bench + the advisory-drift seam + 2 probes), so the re-ground produced **ZERO tier movement**
> (reachable-now holds **171**; coverage.json diff = the one `grounding_heads` line, `--check` byte-identical,
> `--selftest` green). The real C8 e2e chain (`CASE-P-0000251` -> casework signed SAR) still **CONNECTS** at
> the new HEAD (zero blocking violations); only the launcher `dist/index.html` re-grounded (the sanctioned
> Phase-60 Option-A cascade), 7/8 dists byte-identical, `--check all` 8/8.
>
> **Audit date:** 2026-06-20 (Phase 61, signal-watch-local, LITE; the audit fan-out ran 96 agents across the three repos under ultracode).

---

## 1. Three-tier status legend

The blueprint's binary partition — `(built)` vs `(design-stage)` — is too coarse for the current
reality. This review uses four statuses:

| Status | Meaning |
|---|---|
| **demo-built** | A COMMITTED `signal-watch` artifact: demo-scale, presented, vision-lab class. The deterministic core is real and regression-gated, but the data is synthetic/curated and the artifact ships as an offline single file (e.g. `derive_signals.py`, the news pipeline, the consoles). |
| **pillar-build-synthetic** | A COMMITTED SIBLING artifact (`aml-substrate` / `aml-casework`): **real-system-class CODE** — production-shaped, tested, fail-closed — but running over **SYNTHETIC data at probe/demo scale**. This is **NOT a deployed or production workload**; it has never seen real customer/transaction data. Verified by opening the code and confirming it does what is claimed. |
| **design-stage** | NO implementation. Design / prose only. Per the blueprint's own rule, these rows "do not exist." |
| **partial** | Some of a section/row is built, some is not — the detail block says which is which. |

The cardinal honesty rule of this review: **a synthetic pillar build is `pillar-build-synthetic`,
never `demo-built`, and never described as deployed.** Where uncertain between two tiers, the
less-built tier is chosen and the reason stated.

---

## 2. Headline finding

**The blueprint's §3 binary partition has been outgrown by a three-tier reality.** The blueprint
(frozen at Phase 47, 2026-06-12) marks four of its six §3 workload rows as `(design-stage)`:
Transaction monitoring, Case investigation, SAR/STR narrative, and the LFCM-assist /
entity-event decisioning layer. **All four now carry committed sibling implementation at
`pillar-build-synthetic`** — the deterministic verifier mechanism each row specifies is REAL,
TESTED, COMMITTED CODE, integrated into a working cross-pillar chain. What remains genuinely
unbuilt (live data, the measured M-layer of composition quality, deployed scale) is correctly
deferred.

Precisely which `(design-stage)` rows now carry pillar code:

| §3 row | Blueprint says | Verified committed implementation | Status |
|---|---|---|---|
| **Transaction monitoring** | (design-stage) | `aml-substrate@34400e2` `src/aml_substrate/monitor/verify.py:verify_alert` — Class-G referential/lineage replay gate; re-runs the cited detector over ONLY cited records, raises `ReplayError` on any tamper. Tests in `tests/test_alert_verify.py` cover all 5 tamper classes. | **pillar-build-synthetic** (Class-G layer; Class-M/J deferred) |
| **Case investigation** | (design-stage) | `aml-casework@c6d8401` `src/aml_casework/contract.py:validate_bundle` + `citation.py:verify_citations` — referential integrity + citation gates over the evidence bundle. | **pillar-build-synthetic** (Class-G gates; the investigative-conclusion J-gate is design) |
| **SAR/STR narrative** | (design-stage) | `aml-casework@c6d8401` 6 Class-G verifiers (`contract`, `grounding_replay`, `completeness`, `citation`, `corpus_grounding`, `narrative_grounding`) + `narrative_generator.py` (bounded regenerate loop, `MAX_DRAFT_ATTEMPTS=3`) + `signoff.py:record_signoff` (Class-A seam). Signed-SAR fixtures committed. | **pillar-build-synthetic** (drafting + Class-G gates; Class-A filer sign-off stays human) |
| **LFCM assist / entity-event decisioning** | (design-stage, §13) | `signal-watch@67dbd65` `e2e_chain_check.py` (Class-G referential-replay spine, CONNECTED end-to-end Phase 55–60) + `aml-substrate@34400e2 monitor/verify.py`. No-unmeasured-number rule structurally enforced. | **partial** — G-layer spine built (`pillar-build-synthetic` + `demo-built`); J-console embryo `demo-built`; the §14 M-layer (composition-quality sampling) genuinely **design-stage** |

The blueprint's own standard — "nothing claims to be built unless it names a committed artifact"
— now cuts the other way: it **under-claims**. The fix is documentation, not implementation.

---

## 3. Per-section status table

| Section | Blueprint said | As-built status | Named verified artifact (repo@HEAD) |
|---|---|---|---|
| §1–2 Universal grounding | Principle; TM + narrative rows design-stage | **pillar-build-synthetic** — the principle is operationalized in 6 verifiers across 3 repos; the audit walk is an executable artifact | `e2e_chain_check.py`, `derive_signals.py`, `news_ground.py` (signal-watch@67dbd65); `monitor/verify.py` (substrate@34400e2); `citation.py` (casework@c6d8401) |
| §3 rows 1–2 (Corpus derivation, Adverse-media) | (built) | **demo-built** — accurate | `derive_signals.py:check_record`, `news_ground.py:ground_record`, `tests/news_quality_harness.py` (signal-watch@67dbd65) |
| §3 row 3 (Transaction monitoring) | (design-stage) | **pillar-build-synthetic** (Class-G); M/J deferred | `monitor/verify.py`, `monitor/evidence.py`, `tests/fixtures/evidence/CASE-P-0000251.json` (substrate@34400e2) |
| §3 rows 4–5 (Case investigation, SAR/STR narrative) | (design-stage) | **pillar-build-synthetic** (Class-G + drafting); Class-A human | `citation.py`, `contract.py`, `grounding_replay.py`, `signoff.py`, `narrative_generator.py` (casework@c6d8401) |
| §3 row 6 (LFCM assist) | (design-stage, §13) | **partial** — G spine built, J embryo demo-built, M-layer design-stage | `e2e_chain_check.py`, `signal_coverage_map.py`, `console.html` (signal-watch@67dbd65) |
| §4 gate taxonomy + §5 charter | Roles/concepts | **partial** — G (multi-pillar), M (one control), J (two consoles) realized; A deferred-with-owner | `console.html`, `triage.html`, `cd_correctness.py` (signal-watch@67dbd65); `verify.py`, `citation.py`, `contract.py` (siblings) |
| §6 agentification criterion | Probe rule | **demo-built** — all 5 rules instantiated in committed code/probes | `serve_corpus.py`, `news_ground.py:locate_span`, `serve_chain.py` (signal-watch@67dbd65) |
| §7 control mapping | 6 rows name artifacts | **partial / mixed** — 6 rows accurate; Monitoring row STALE (omits Phase-54 C/D control) | `build.py`, `derive_signals.py --check-derived`, `news_quality_harness.py`, `cd_correctness.py`, `docs/cd-tag-control.md` (signal-watch@67dbd65) |
| §8 validation story | Designed-now + deferred | **mixed** — designed-now mostly built; Phase-54 control omitted; deferred rows correctly deferred | `derive_signals.py`, `news_quality_harness.py`, `cd_correctness.py` (signal-watch); `validate/baseline.py` (substrate@34400e2); `contract.py`, `grounding_replay.py` (casework@c6d8401) |
| §9 honesty + §10 95/5 | Survive/transform; no ratio | **partial** — most constraints held; §9 row-2 third stratum (human-confirmed) NOT built; §10 enforced by absence | `index.html` badge, `build.py --check`, `.gitignore` (signal-watch@67dbd65); `evidence.py illustrative=True` (substrate) |
| §11 roadmap | 4 chains, gate console | **mixed** — two "built" claims overstate (/intel/, REQUOTE-RETRY); §11.4 understates pillar builds | `console.html`, `data/probe-history/` (signal-watch); pillar `monitor/`, `resolve/`, casework `narrative_generator.py` |
| §12 brownfield history | 3 roles, probe-proven | **demo-built** (Role 1 proven; Role 2 demonstrated; Role 3 measurement-only) | `docs/probe-history.md`, `scripts/probe_history_stats.py`, `data/probe-history/` (signal-watch@67dbd65) |
| §13 LFCM | Library embryo + failure modes | **partial** — embryo + coverage map + redundancy bound built; composition-as-learned-model RETIRED (honest divergence); "56 signals" count stale | `coverage.json`, `signal_coverage_map.py`, `corpus_redundancy.py` (signal-watch); `validate/composition.py`, `beyond_linkage.py` (substrate@34400e2) |
| §14 adjudication loop + §15 charter | Loop design; gate console embryo; "four ship artifacts" | **demo-built** — §14 fully realized in triage console; §15 count is STALE (five ship artifacts, plus launcher = eight targets) | `dist/triage/index.html`, `data/triage/scenarios.json`, `build.py:render_triage` (signal-watch@67dbd65) |

---

## 4. Per-section detail

### §1–2 — The universal grounding principle

**Blueprint position.** Grounding is universal; substrate varies. The text case is built;
transaction monitoring (referential/lineage verifiers) and SAR narratives (citation verifiers)
are generalizations. Three consequences: the audit walk down the chain; grounded-or-dropped;
substrate+verifier named per workload.

**As-built finding (`pillar-build-synthetic`).** The principle is operationalized in SIX verifier
implementations across three repos, and the §2 audit walk is a COMMITTED EXECUTABLE artifact, not
prose:
- The **grounding core is reused, not reimplemented**: `e2e_chain_check.py:34` actively
  `from derive_signals import normalize`; `news_ground.py:news_normalize` mirrors it (docstring
  attributes the source). *(Audit caveat: the blueprint's "six implementations" phrase is
  literally true at the verifier level, but vt1 found only 2 distinct `normalize` bodies +
  1 import-reuse inside signal-watch — the "six" counts verifiers, not normalizers; do not read
  it as six cross-pillar normalizer reimplementations.)*
- **The audit walk is executable**: `e2e_chain_check.check_substrate` (line 91) + `check_chain`
  (line 173) walk a signed SAR back to the corpus advisory via signal → alert → transaction
  identity links; deterministic, no NLP. `--real` connected case `CASE-P-0000251` substrate →
  casework → signed SAR at Phase 60 (`data/pillar-status.json`: all three bridge states `done`).
- **Grounded-or-dropped is structural**: `check_record` (violations list), `ground_record`
  (`dropped[{kind,value,reason}]`), `verify_citations` (violations), `verify_alert`
  (`ReplayError`). Every drop is named; silent truncation never passes.

**Drift.** Blueprint-stale: §2 implicitly treats TM and narrative grounding as future; both are
committed verifier code (`verify_alert`, `verify_citations`). The principle's three consequences
are realized, not aspirational.

### §3 rows 1–2 — Corpus derivation + Adverse-media screening (the `(built)` rows)

**Blueprint position.** Both `(built)` with named verifier mechanisms.

**As-built finding (`demo-built`, accurate).** Confirmed across 7 verify targets:
- `derive_signals.check_record` (lines 364–439) disposes all 16 committed `data/fincen/derived/`
  records; `--selftest` + `--check-derived` pass; 279 indicators, 62 BUILD_NOW with `build_logic`,
  100% grounded under `normalize()` within `rf_region`.
- `news_ground.ground_record` + Phase-44 `locate_span` (wrap-tolerant requote) + closed vocabs
  `PROPERTY_KINDS`/`RELATION_LABELS`; `news_quality_harness --check` passes (17 fixtures pinned).
- `build.py` imports `news_ground`, never `derive_signals` (the inverted boundary, line 35).

**Drift.** None. The two `(built)` rows are accurate `demo-built`. *(Minor: `rf_region`
regression comment says "46 mds"; the corpus has since grown to ~51 — the claim's substance
holds, the count string is dated.)*

### §3 row 3 — Transaction monitoring

**Blueprint position.** `(design-stage)`. Substrate = committed signals + data; verifier =
referential/lineage replay; gates G + M + J.

**As-built finding (`pillar-build-synthetic`).** The **Class-G layer is built and hardened** in
`aml-substrate@34400e2`:
- `monitor/verify.py:verify_alert` (lines 32–53) re-runs the cited detector over ONLY cited
  records, byte-identical reproduction, `ReplayError` on swapped/missing/mutated/repointed
  citations. `tests/test_alert_verify.py` covers all 5 tamper classes (committed `7cacb40`).
- `monitor/evidence.py:build_bundle` mints deterministic SHA1 ids
  (`test_evidence.py:test_..._sha1_rule`); bundles are byte-for-byte reproducible; carry
  `illustrative: True`. Fixture `CASE-P-0000251.json` shows the full self-contained grounding
  walk (signal_id, advisory_id, indicator_id, C8, D2, verbatim flag, 5 cited txns).
- Detectors are **label-blind by construction** (`test_detectors.py` static grep guard + view
  projections forbidding label access). `aml-casework@c6d8401 contract.py:validate_bundle`
  enforces the Pillar-1→2 referential integrity at intake.

**Drift.** Blueprint-stale: Class-G is pillar-built, not design. **Honest scope:** Class-M
(alert-quality / above-below-line sampling agreement) exists only at the generic `Measurement`
level, not with monitoring-specific sampling discipline; Class-J (graded alert disposition) does
NOT exist in the monitoring layer. So the row is **pillar-build-synthetic for G, deferred for
M/J** — not a blanket upgrade.

### §3 rows 4–5 — Case investigation + SAR/STR narrative

**Blueprint position.** Both `(design-stage)`.

**As-built finding (`pillar-build-synthetic`).** `aml-casework@c6d8401` is built through Phase 12
with comprehensive committed code + tests, all on SYNTHETIC fixtures:
- **Six Class-G verifiers**, all returning violation lists, fail-closed: `contract.validate_bundle`,
  `grounding_replay.replay_bundle` (C2/C3/C4/C5/C15 replay assertions + C7/C8/C14 screening
  assertions; C14 party-leaf txn-less via `_party_by_ref`; **C26 deliberately unregistered — the
  honest null**), `completeness.verify_completeness`, `citation.verify_citations`,
  `corpus_grounding.verify_corpus_grounding` (substring-grounds each flag to the vendored frozen
  corpus pin), `narrative_grounding.verify_narrative_grounding` (atom-grounds prose, regex +
  membership, no NLP).
- **Neural narrative generator** `narrative_generator.generate_narrative` — bounded
  regenerate-against-verifier loop, `MAX_DRAFT_ATTEMPTS=3`, fail-closed (refusal or exhaustion
  leaves the seam OPEN). Pluggable drafters (Claude Opus 4.8, OpenAI, opencode, deterministic
  stub) with fail-soft fallback on SDK/transport fault (`test_ingest_cli.py`).
- **Class-A seam** `signoff.record_signoff` runs all 6 verifiers, computes
  `blocked / needs_more_info / signed`, and validates a human-claimed `file / both_defensible`
  disposition against `grounded_stances()` — **never weighing which side wins** (the file/no-file
  judgment stays human). 24 tests in `test_signoff.py`. Signed-SAR fixtures committed
  (`case-thin-slice-01-signed.json`, `case-c7/c8/c14-screening-01.json`).

**Drift.** Blueprint-stale on both rows: the Class-G gate stack + drafting + signoff seam are
committed pillar code. **Honest boundary held:** the investigative-conclusion J-gate (intent,
story coherence) and the Class-A filer sign-off remain HUMAN — the code assembles and verifies,
it does not judge. The blueprint is 8 days stale relative to casework@c6d8401 (2026-06-19).

### §3 row 6 — LFCM assist / entity-event risk decisioning

**Blueprint position.** `(design-stage, §13)`. Substrate = fired signals + chains + anchors;
verifier = referential replay + the no-unmeasured-number rule; gates G + M + J.

**As-built finding (`partial`).**
- **G-layer spine built** (`demo-built` + `pillar-build-synthetic`): `e2e_chain_check.py` validates
  deterministic id-mint + referential integrity + corpus grounding; `aml-substrate verify_alert`
  re-runs detectors. CONNECTED end-to-end (Phase 55–60).
- **No-unmeasured-number rule CONFIRMED enforced** (vt2, three-repo audit): bundles carry
  `illustrative: True`; `e2e_chain_check.py:107-108` rejects any bundle lacking it; casework
  `contract.py:145-146` blocks ingestion of non-illustrative bundles; `test_compose.py` asserts
  NO field name contains `score`/`risk`/`rating`. The rule is structural, not documentary.
- **J-console embryo built** (`demo-built`): `console.html` dramatizes the graded gate.
- **M-layer genuinely design-stage** (vt5, **refuted**): composition-quality sampling +
  elicited-judgment agreement do NOT exist as a measured harness; §14 design parameters are
  explicitly "chosen, not measured." `aml-substrate validate/composition.py` measures
  DETECTION-quality composition (a different dimension), not the §14 elicited-judgment M-layer.

**Drift.** Impl-diverged: §13 describes composition as "a separately validatable model" that
"must model redundancy explicitly"; the built composition is **evidence-assembly + referential
verification only** — aml-substrate measured a TRIPLE-NULL and RETIRED composition detection-lift.
This is honest (better for auditability), but architecturally tighter than the blueprint prose.

### §4 gate taxonomy + §5 human-work charter

**Blueprint position.** Four gate classes (G/M/J/A); two human streams; the gate console is "the
vision-lab artifact for exactly the human work §5 charters."

**As-built finding (`partial`).** The taxonomy is realized PER WORKLOAD:
- **Class G** — multi-pillar: `verify_alert`, `signal_ref` (substrate); `citation`, `contract`,
  `signoff` chain (casework); `check_record`, `news_ground` (signal-watch).
- **Class M** — ONE committed control: `cd_correctness.py` (`demo-built`, NON-SHIP) — RANDOM
  self-consistency + DIVERGENCE adjudication + Phase-54 cross-family Qwen independent rater, with
  trip-wires (integrity, self-consistency floor ≥0.578, independent floors C≥0.504/D≥0.546),
  `--control-check`/`--control-freeze`, frozen baseline. `docs/cd-tag-control.md` formalizes it as
  an SR 11-7 Pillar-2 / E-23 control with 3-lines-of-defense ownership.
- **Class J** — two consoles `demo-built`: `console.html` (213 real Phase-34 C/D divergences,
  4 grades, rationale-required) and `triage.html` (§14 loop, 6-option grammar).
- **Class A** — deferred-with-owner (SAR sign-off, model approval require institutional roles).

**Drift.** Blueprint-stale: §4-M is richer than designed (risk-tiering, ownership, cadence,
trip-wires in `cd-tag-control.md`). **Honest boundaries:** consoles are session-only (no
persistence); `cd_correctness` is NON-SHIP measurement, not a live control; no Class-A gate
implemented. *(vt `triage_classj_loop` caveat: "double-blind assignment" overstates — the
second-rater is a seeded synthetic field revealed post-hoc, not independent parallel judgment.)*

### §6 agentification criterion

**Blueprint position.** Five-rule probe rule, n=1 per workload class.

**As-built finding (`demo-built`).** All five rules instantiated in committed code/probes:
- A/B probe (`serve_corpus.py@5981b41` + Phase-46 decision article): identical 17/17 indicators,
  82.6s direct vs 255.1s opencode = 3.1× — confirmed.
- Fold-the-idea-in: `news_ground.locate_span` (Phase 44) is the deterministic requote pass.
- ONE violation-guided retry cap in `serve_corpus.derive()`.
- Surface-all-dimensions + creds-isolation in `serve_chain.py@1cf0722` (`backend_available`,
  `resolve_backend`, `_drafter_config` expose names+booleans only; selftest proves no cred leak).
- Tag-class stays Class-M (C/D agreement measured, inside Phase-34 band).

**Drift.** None at the rule level. *(vt6-2 caveat: the full news REQUOTE-**RETRY** pass — the
post-grounding re-prompt loop — was a measured deferral, not a build; only the REQUOTE half
(`locate_span`) shipped. See §11 drift.)*

### §7 control mapping

**Blueprint position.** 8 E-23 × SR 11-7 rows; "built ones name committed artifacts."

**As-built finding (`partial / mixed`).** 6 rows accurately name committed signal-watch artifacts
(`build.py`, `--check-derived`, `news_quality_harness --check/--freeze`, build-boundary
validation). The deterministic boundary (build.py never imports `derive_signals`, line 35) and the
byte-identity drift guard (`check_one`...`check_triage`) are confirmed.

**Drift.** Blueprint-stale: the **Monitoring row** names only `news_quality_harness` but Phase 54
(2026-06-16, after the blueprint) delivered the canonical measured-not-gated control
(`cd_correctness.py --control-check/--control-freeze` + `docs/cd-tag-control.md` +
`data/cd-correctness/cd-control-baseline.json`). The row understates what is committed.

### §8 validation story

**Blueprint position.** Designed-now (deterministic replay, regression-vs-baseline, blind
inter-rater) + deferred-with-owner (outcome loops, drift monitoring, threshold sampling).

**As-built finding (`mixed`).** Designed-now mechanisms are mostly built:
- Deterministic replay: `--check-derived` + news replay fixtures (13) + `build.py --check` —
  all `demo-built`, confirmed. `aml-casework contract.py` + `grounding_replay.py` add Class-G
  replay (`pillar-build-synthetic`).
- Regression-vs-baseline: `news_quality_harness` (signal-watch) + `aml-substrate
  validate/baseline.py` (`check_drift`/`gate`/`write_baseline`, `measure-baseline.json`,
  `pillar-build-synthetic`). aml-casework has Class-G validators but NO `--check`/`--freeze`
  baseline yet — expected phasing, not divergence.
- Blind inter-rater: `cd_correctness.py` RANDOM + DIVERGENCE + Phase-54 INDEPENDENT strata.

**Drift.** Blueprint-stale: §8 "Designed now" omits `--control-check` + `cd-control-baseline.json`
(Phase 54). Deferred rows correctly remain deferred (no outcome-feedback / drift / threshold
sampling code — correct per vision-lab constraint).

### §9 honesty dispositions + §10 95/5 framing

**Blueprint position.** Survive/transform table; 95/5 is direction, never ratio/target.

**As-built finding (`partial`).**
- SURVIVES held: no-fabricated-numbers (badge + measurement-definition caveats incl.
  `aml-substrate measure.py` caveats); licence-basis-named-per-source (corpus footer).
- TRANSFORMS partly held: drift-guard builds (`build.py --check`); privacy-by-construction at
  demo scale (`.gitignore`, 127.0.0.1); graceful degradation operationalized program-wide
  (`serve_corpus` `DeriveError`, `serve_news` `ExtractError` fail-open-to-KEEP, casework
  drafter fail-soft-to-stub — vt confirmed).
- **§9 row-2 output-status labeling — REFUTED for the third stratum** (vt): derived records carry
  NO per-record `output_status` field; only the global badge + a live-mode-only `UNREVIEWED` group
  (build-stripped from `dist/corpus`). The "human-confirmed" stratum is design intent, not built.
- **§9 row-3 institutional-scale privacy — REFUTED as institutional governance** (vt): what exists
  is `PartyView`/`contract.py` label-stripping PROJECTION on synthetic data; no
  governess/licence-gate/persistence-rule layer. The first half (PII-stripping) is built
  `pillar-build-synthetic`; the institutional governance half is design.
- §10 — enforced by ABSENCE: grep across all three repos finds NO automation-ratio /
  percentage-target field (vt confirmed). Held.

**Drift.** Impl-diverged (understated coverage): §9 row-2 oversells the demo by one stratum;
§9 row-3 conflates synthetic PII-projection with institutional privacy governance.

### §11 capability roadmap

**Blueprint position.** Four chains (corpus content `(built)`, screening recovery `(built)`,
entity resolution, monitoring/investigation/SAR `(design-stage)`); the gate console as the
Class-J vision-lab artifact.

**As-built finding (`mixed`).**
- **§11.1 /intel/ + third jurisdiction — REFUTED as committed** (vt1, vt5 `design-stage`):
  `data/` has exactly 5 sources; no `/intel/` sixth source directory, no AUSTRAC/UK. FINTRAC
  operational alerts ARE committed but under the existing `fintrac` source — `/intel/` is the
  website path, not a corpus extension. Both are design aspirations, correctly named "frontier."
- **§11.2 REQUOTE-RETRY — partial** (vt2): the Phase-44 `locate_span` REQUOTE half is built; the
  full RETRY (post-grounding re-prompt loop) is deferred, never implemented.
- **§11.4 monitoring/investigation/SAR — understated**: the pillar-INTERNAL mechanics
  (`aml-substrate monitor/`, `aml-casework` narrative + verifiers) are `pillar-build-synthetic`,
  NOT design-stage. Only the cross-pillar integrated case/investigation flow is design.
- Gate console: `demo-built`, accurately positioned. Entity resolution: fuzzy-merge built in
  `aml-substrate resolve/` (`pillar-build-synthetic`), but the human merge-adjudication console
  is NOT built (only the C/D-divergence gate console exists).

**Drift.** Two over-claims (§11.1 /intel/ and third jurisdiction; §11.2 RETRY) and one
under-claim (§11.4 pillar builds). Internal history as a 6th source class is a SYNTHETIC PROBE
(`data/probe-history/`), correctly isolated, not a production integration.

### §12 brownfield substrate

**Blueprint position.** Three roles; Role 1 probe-proven (12/12 gate-green); Role 2 baseline;
Role 3 outcome-feedback embryo.

**As-built finding (`demo-built`).**
- **Role 1 proven** (vt1, with a correction): the 12-rule synthetic rulebook derives gate-green
  through the UNCHANGED frozen gate, zero violations, coverage derived deterministically via the
  cover×data matrix (`--check-derived data/probe-history/derived/legacy-rulebook.json` → CHECK OK,
  BUILD_NOW=1 · COVERED=8 · ENHANCE=3). **Correction:** the prompt's "all 12 status='covered'" is
  wrong — the JSON is 8 covered / 3 partial / 1 gap; "12/12 gate-green" is accurate, the coverage
  distribution is not all-covered.
- **Role 2 demonstrated**: `probe_history_stats.py` computes re-review 27.3%,
  disposition-inconsistency 66.7%, escalation 27.3% over the 44-alert synthetic history, each with
  its definition string.
- **Role 3 partial**: the MEASUREMENT framework exists (`sar_filed: 2` counted); the EXTRACTION
  machinery (real filings → structured outcome signals) is deferred. Investigation-narrative
  extraction (Role 1 second bullet) is NOT implemented anywhere.

**Drift.** Impl-diverged (framing): §12 groups investigation-narrative extraction with the proven
rulebook decomposition, suggesting equal maturity; only the rulebook path is proven. *(vt2
caveat: `probe_history_stats.py` READS pre-computed `build_rec`; the deterministic derivation
happened in the one-off `ph33_apply.py`, not the named stats script.)*

### §13 LFCM

**Blueprint position.** Library-not-monolith embryo (2,251 indicators, 56 signals); coverage map;
five named failure modes; composition as a separately validatable model; dossier-now/score-deferred.

**As-built finding (`partial`).**
- Embryo + tiers: `coverage.json` (523 buildable, 171 reachable-now), `signal_coverage_map.py`
  (`--check` byte-identical, `--selftest` green) — `demo-built`, confirmed.
- Failure-mode-1 (correlated double-counting) MEASURED: `corpus_redundancy.py` +
  `corpus-redundancy-report.md` — T1 ceiling 0.325, T2 strict equivalence 0.042 → ≈1.4% genuine
  redundancy (single-rater, illustrative, NON-SHIP). 2,251 indicators verified
  (FINTRAC 1,705 + FinCEN 495 + OFAC 51).
- Composition-lift RETIRED: `aml-substrate validate/{reachability,composition,beyond_linkage}.py`
  measured the TRIPLE-NULL with sealed pre-registered bars; network subsumption 3/3
  (`pillar-build-synthetic`).
- Dossier-now/score-deferred realized: `e2e_chain_check` + the connected `CASE-P-0010361` chain;
  no `score`/`risk`/`rating` field anywhere.

**Drift.** Impl-diverged: composition is built as deterministic assembly + referential
verification, NOT a learned statistical aggregation model (honest, post-triple-null).
Blueprint-stale (minor): "56 derived signals" is an embryo-snapshot count; the corpus now carries
~60+ committed derived source documents — clarify whether "56" is a frozen snapshot or a living
count.

### §14 continuous adjudication loop + §15 demo charter

**Blueprint position.** The §14 loop (4 strata, 6-option grammar, discovery outputs,
self-instrumentation); gate console as the committed embryo; §15 "the four ship artifacts remain
demo-class."

**As-built finding (`demo-built`).** §14 is FULLY realized in `dist/triage/index.html` (Phase 49,
fifth ship artifact):
- All 4 strata populated + build-validated (`build.py:TRIAGE_STRATA`); 20 synthetic scenarios.
- Full 6-option grammar (`confirm-risk / confirm-no-risk / both-defensible / escalate /
  need-more-info / no-defensible-option`) in `scenarios.json` meta + `build.py:TRIAGE_GRAMMAR` +
  the shipped HTML.
- Discovery ledger (signal/data/policy gaps, process inconsistencies, agreement) DERIVED at render
  from session records, each with a definition string.
- `need-more-info` carries `info_needed.data_source` (C/D code) — wires to the coverage model
  (vt confirmed, e.g. D8).
- Process inconsistencies surfaced by shared-panel matching, by reference.
- "Chosen, not measured" design params preserved in `meta`.

**Drift.** Blueprint-stale: §15 says "the four ship artifacts" — Phase 49 made it FIVE (triage),
and the launcher `dist/index.html` is an eighth build target. *(Two honest vt caveats: (a) the
seeded second-rater is NOT independent double-blind judgment; (b) `dist/triage/index.html` is
self-contained for JS/data but loads Google Fonts via `<link>` — it is NOT strictly offline-pure;
the launcher itself is clean.)*

---

## 5. Both-direction drift inventory

### (a) Blueprint-stale — the doc UNDER-states what is built

1. **§3 row 3 (TM)** → Class-G layer is `pillar-build-synthetic` (`monitor/verify.py`,
   substrate@34400e2), not design-stage.
2. **§3 rows 4–5 (Case investigation, SAR/STR)** → 6 Class-G verifiers + drafter + signoff seam
   are `pillar-build-synthetic` (casework@c6d8401), not design-stage.
3. **§3 row 6 (LFCM assist)** → the G-layer referential-replay spine is built and CONNECTED
   end-to-end (Phase 55–60); only the M-layer is design-stage.
4. **§2** → the audit-walk-down-the-chain is an executable committed artifact (`e2e_chain_check`),
   not a design consequence.
5. **§4-M / §7 Monitoring row / §8 Designed-now** → omit the Phase-54 C/D control
   (`cd_correctness.py` + `cd-tag-control.md` + `cd-control-baseline.json`).
6. **§11.4** → pillar-internal monitoring/investigation/SAR mechanics are built
   (`pillar-build-synthetic`); only the integrated cross-pillar flow is design.
7. **§15** → "the four ship artifacts" undercounts: five demo artifacts + the launcher
   (eight build targets).
8. **§13** → "56 derived signals" embryo count is dated relative to ~60+ committed sources.

### (b) Impl-diverged — built DIFFERENTLY than designed (mostly honestly)

1. **§13 composition** → designed as "a separately validatable [statistical] model that models
   redundancy explicitly"; built as deterministic assembly + referential verification, with
   detection-lift RETIRED after the aml-substrate TRIPLE-NULL. Honest, tighter, better for
   auditability.
2. **§3 row 6 / §14 M-layer** → composition-quality + elicited-judgment AGREEMENT sampling is NOT
   measured (vt5 refuted); design parameters are "chosen, not measured." The G+M+J stack is G-live,
   J-scaffolded, **M-deferred**.
3. **§9 row 2** → output-status labeling built to TWO strata (illustrative + live-UNREVIEWED), not
   three; "human-confirmed" per-record status is design, not built.
4. **§9 row 3** → privacy-by-construction built as synthetic PII-PROJECTION (`PartyView`), not as
   institutional governance (governess / licence-gate / persistence rules — design).
5. **§12 framing** → investigation-narrative extraction is grouped with the proven rulebook
   decomposition but is unimplemented; only the rulebook path is probe-proven.
6. **§11.1 / §11.2** → two roadmap "built" implications OVER-state: `/intel/` + third jurisdiction
   are NOT committed corpus extensions (design); the news REQUOTE-**RETRY** loop is deferred (only
   the REQUOTE/`locate_span` half shipped).

---

## 6. The verified blueprint-edit list (the spec for the revision)

Each edit cites the verified finding. **Status stays DESIGN** — this trues up the design doc; it
does not turn it into a status tracker. Where a row stays design or partial, that is stated
explicitly to avoid over-claim.

### §3 table — the row markers

- **Row 3 (Transaction monitoring):** change `(design-stage)` → **`(pillar-build-synthetic —
  Class-G; M/J deferred)`**. Add footnote: *"Referential/lineage replay verifier built and
  hardened: `aml-substrate@34400e2 monitor/verify.py:verify_alert`, all tamper classes tested.
  Class-M alert-quality sampling and Class-J graded disposition remain design-stage."* Justified by
  §3-row-3 findings (vt_1–vt_5).
- **Row 4 (Case investigation):** `(design-stage)` → **`(pillar-build-synthetic — Class-G gates;
  investigative-conclusion J-gate human/design)`**. Footnote: *"`aml-casework@c6d8401
  contract.py`, `citation.py`, `grounding_replay.py` committed + tested on synthetic fixtures."*
- **Row 5 (SAR/STR narrative):** `(design-stage)` → **`(pillar-build-synthetic — drafting +
  Class-G; Class-A filer sign-off human)`**. Footnote: *"`aml-casework@c6d8401`: 6 Class-G
  verifiers + `narrative_generator.py` (bounded regenerate loop) + `signoff.py:record_signoff`;
  signed-SAR fixtures committed. `record_signoff` never weighs file/no-file — that stays human."*
- **Row 6 (LFCM assist):** keep `(design-stage)` framing but split: **`(partial — Class-G
  referential-replay spine pillar-built + CONNECTED; Class-J console demo-built; Class-M
  composition-quality sampling design-stage)`**. Justified by §3-row-6 (vt1–vt5; vt5 refuted).
- **Add a one-line note under the table:** *"`(design-stage)` rows 3–5 carry committed SIBLING
  verifier code at pillar-build-synthetic scale — real code, synthetic data, not deployed; the
  HUMAN-owned gates (J-disposition, A-sign-off) and the live-data M-layers remain unbuilt."*

### §8 — deferred-row dispositions / Designed-now list

- **Add to "Designed now":** *"C/D-tag measured-not-gated control: `cd_correctness.py
  --control-check/--control-freeze` against the committed `cd-control-baseline.json` (Phase 54);
  trip-wires + cross-family independent rater; `docs/cd-tag-control.md` formalizes it as an SR 11-7
  Pillar-2 / E-23 Monitoring control (NON-SHIP, consensus never accuracy)."* Justified by §7/§8
  findings.
- **Keep the deferred rows unchanged** (outcome-feedback, drift, threshold sampling) — verified
  correctly deferred (no implementation, by design). Do NOT upgrade.

### §7 — Monitoring row

- **Monitoring row, Program-control cell:** append *"+ the C/D-tag control
  (`cd_correctness.py --control-check`/`--control-freeze`; `docs/cd-tag-control.md`;
  `cd-control-baseline.json`)"* alongside `news_quality_harness`. Justified by §7 blueprint-stale
  drift.

### §11 — roadmap re-sequence

- **§11.1:** soften `/intel/ ... as committed corpus extension` and `a third jurisdiction
  (AUSTRAC/UK OGL)` to explicit FRONTIER language — *neither is a committed source; `data/` holds
  exactly 5 sources*. (vt1/vt5 refuted as committed; they are design.)
- **§11.2:** correct to *"the REQUOTE half (`locate_span`, Phase 44) is folded in;
  the REQUOTE-**RETRY** loop remains the deferred candidate"* — only half shipped (vt6-2/§11-vt2).
- **§11.4:** re-mark — *"the pillar-INTERNAL monitoring/investigation/SAR mechanics are
  pillar-build-synthetic (`aml-substrate monitor/`, `aml-casework` narrative + verifiers); the
  cross-pillar integrated case flow is the design-stage remainder."* (vt3.)
- **§11.3:** note fuzzy-merge is built in `aml-substrate resolve/` (`pillar-build-synthetic`) but
  the human merge-adjudication console is NOT built — keep that console as the open roadmap item.

### §13 — LFCM-embryo claims

- **"56 derived signals":** annotate as a *frozen embryo snapshot* OR refresh to the current
  committed count (~60+ derived source docs) — pick one; the 2,251-indicator count is verified
  current. (vt1.)
- **Failure-mode-1 sentence:** add that it is now MEASURED — *"corpus_redundancy.py:
  T1 ceiling 0.325, ≈1.4% genuine redundancy (single-rater, illustrative)."* (vt3.)
- **Composition paragraph:** add the honest divergence — *"detection-lift composition RETIRED
  after the aml-substrate TRIPLE-NULL; the built composition is deterministic evidence-assembly +
  referential verification, not a learned aggregation model."* (vt4.)
- **Dossier-now/score-deferred:** mark REALIZED + ENFORCED (no `score`/`risk`/`rating` field;
  `illustrative:True` gated at three boundaries). (vt5.)

### §9 / §15 — honesty + charter (precision, not over-claim)

- **§9 row 2:** correct to *"output-status labeling built to two strata (illustrative +
  live-UNREVIEWED); the per-record human-confirmed stratum remains design."* (vt refuted.)
- **§9 row 3:** correct to *"synthetic PII-PROJECTION (`PartyView`) built pillar-side; institutional
  governance (governess / licence-gate / persistence rules) remains design."* (vt refuted.)
- **§15:** update "the four ship artifacts" → *"the five ship artifacts (the triage console is the
  fifth, Phase 49) plus the launcher — eight build targets, all byte-frozen"*; note the triage
  console loads Google Fonts via `<link>` (not strictly offline-pure). (§14/§15 findings.)

---

## 7. Re-grounded next-frontier (ranked)

Given the as-built reality, where the highest-value next work is — and an honest read on the
coverage-map near-ceiling:

1. **[sibling-rooted — aml-substrate] The §14 M-layer / emergence engine.** This is the one
   genuinely `design-stage` piece of the otherwise-built §3 row 6, AND it is the bottleneck the
   coverage map already identified: reachable-now is near a CEILING from signal-watch's side
   (needs-detector exhausted at 0; the remaining 281 needs-behavior + 69 needs-view-exposure tiers
   move only when EMERGENT BEHAVIOR lands, which is substrate-rooted, bottom-up). The Phase-60
   honest finding — "only the cap whose behavior genuinely emerges reaches reachable-now" — points
   here. Highest leverage; cannot be done signal-watch-local.

2. **[sibling-rooted — aml-casework] Close the C26 honest null + extend grounding_replay.** C26 is
   deliberately unregistered; the screening-assertion set (C7/C8/C14) is the live frontier. Pairs
   with #1: substrate emits emergent behavior → casework asserts it.

3. **[signal-watch-local] The blueprint revision itself (this report's §6 edit list).** Cheap,
   high-defensibility-value, Status: DESIGN — converts the eight blueprint-stale items + six
   impl-diverged items into an accurate design doc. The single most cost-effective local task: it
   makes the doc match the verified three-tier reality without touching a frozen artifact.

4. **[signal-watch-local] Phase-54 control wiring into §7/§8 + the §9-row-2 third stratum.** If a
   `human-confirmed` per-record output-status field is wanted, it is a small, demo-scale,
   honest-labeling addition that closes a refuted §9 claim. Low blast radius.

5. **[signal-watch-local, lower] The news REQUOTE-RETRY fold** (§11.2's deferred half) — a measured
   agentification-criterion follow-through, but n=1 evidence already exists; lower marginal value
   than #1–#3.

**Honest ceiling note:** the coverage-map reachable-now lever is near-exhausted from
signal-watch's side (needs-detector = 0). Do NOT expect another local +78-class jump; the next
real rise is a sibling aml-substrate emergence phase (#1). Signal-watch's highest-value local work
is now DOCUMENTATION fidelity (#3) and honest-labeling closure (#4), not a new measured number.