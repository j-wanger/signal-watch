# Signal Watch — AML Vision Demo

## What this project is
A presenter-driven, offline, browser-based VISION PROTOTYPE for AML stakeholder buy-in — not a real
detection system; a scripted dramatization of the signal/atom loop. See HANDOFF.md for full context
(POC 5 → POC 1 → POC 3); keep vocabulary consistent with it (atoms, composition, promotion gate…).

## Non-negotiables (do not violate — HANDOFF §4)
- The shippable artifact MUST run by opening one file, offline, no server.
- Do NOT split into ES modules / fetch()-loaded config in the ship target (file:// breaks).
  Develop modular if useful; the build inlines everything into a single self-contained file.
- Content is config-driven (the engine reads from data arrays / typology configs).
  The engine is generic — no hardcoded typology copy in engine code.
- Keep the six-act arc and the two wow beats (two human gates + combination-lift reveal)
  unless explicitly asked to change them.
- Keep the "Illustrative data & outputs" badge always visible. Never present synthetic
  numbers as real.
- NO real customer/transaction data, ever. Advisory text must be public-source and PARAPHRASED by
  default (e.g. the FINTRAC Jan-2025 Operational Alert behind the fentanyl SHOWCASE is paraphrased).
  TWO verbatim exceptions, each kept visually separate from the always-on "Illustrative data & outputs"
  badge: (1) US FEDERAL GOVERNMENT advisories are public domain (17 USC §105 — works of the US government
  carry no copyright) and may be reproduced VERBATIM with attribution (see Act 1's SOURCE DOCUMENT panel,
  EFE FIN-2022-A002). This US-federal exception covers FinCEN AND OFAC (both US Treasury — Phase 21 added
  OFAC as corpus source #3) and other US federal agencies. (2) FINTRAC (Phase 22, corpus source #4 — the
  FIRST cross-jurisdiction source) is Canadian Crown copyright — NOT public domain — but its publications
  MAY be reproduced VERBATIM for NON-COMMERCIAL use WITH FINTRAC's required attribution (© His Majesty the
  King in Right of Canada + complete title + "a copy of the version available at <URL>"), per FINTRAC's
  Terms & Conditions: a reproduction LICENCE, distinct from the US 17 USC §105 no-copyright basis. NOT
  commercial redistribution (needs FINTRAC's written permission). The verbatim relaxation is US-FEDERAL +
  FINTRAC ONLY — every OTHER non-US / non-FINTRAC / non-government source still paraphrases (the fentanyl
  showcase still paraphrases its FINTRAC OA). Phase 28 (the user's compliance call): in the corpus explorer the
  per-doc Source LABEL carries the document title only; the FINTRAC Crown-copyright attribution (© His Majesty…
  + complete title + source URL) renders in the PAGE FOOTER for the FINTRAC doc on screen (empty for US
  public-domain docs) — verbatim-with-attribution HELD, the attribution relocated, not removed.
- Live mode is optional, isolated, off by default, always has a scripted fallback.
  Never put keys/tokens in the frontend. Copilot is NOT a web backend (HANDOFF §4.5).

## Current state
> **Maintenance contract** (this file bloated to 689 lines once — this is the guard). No automated
> process writes this file; the implementing agent edits it BY HAND each phase:
> - `## Current state` is a SNAPSHOT of what is TRUE NOW — **replace facts in place; NEVER append a
>   per-phase bullet.** `## Milestones` is one line per milestone — never a per-phase line.
> - Per-phase narrative (what a phase changed, deltas, frozen-set proofs) goes to the `.dev-wiki/`
>   journal + the git commit message + HANDOFF.md §8 — **not here.**
> - Target ≤ ~200 lines. If it's growing, a phase log is leaking in — move it out.
This section is the DURABLE, currently-true architecture — not a changelog.

### Six ship artifacts (each a single self-contained offline file)
1. **Showcase** — `index.html` → `dist/<id>/index.html`. The generic six-act engine (vanilla
   HTML/CSS/JS, single `__CONFIG__` injection point, typology-agnostic — adding a typology is one
   JSON file, no engine edits); presenter controls (keyboard nav ←/→/Space/Esc/↺, reset,
   `prefers-reduced-motion`). Content: `config/typologies/*.json` (fentanyl, trade-based,
   elder-financial-exploitation) against `config/schema.md`; the elder typology renders the FULL
   verbatim EFE advisory (FinCEN FIN-2022-A002, public domain) in Act 1 via `advisory_full`.
2. **Corpus explorer** — `corpus.html` → `dist/corpus/index.html`. A SEPARATE artifact (own copy of
   the dossier theme; `index.html` byte-untouched). 6-screen per-doc arc: Select → Read the source →
   Coverage → Build recs (**the human GATE** — all BUILD_NOWs PROPOSED pre-selected, the presenter
   deselects to dispose) → Signal → Combination lift (honest R2 inventory counts — see Honesty
   constraints) → Close; FOUR Select lenses (Documents / Typologies / Capabilities / Data sources);
   FINTRAC Crown-copyright footer attribution on detail AND the quoting capability/data-source drills
   (per contributing doc). Scale: **2,251 indicators / 56 derived / 62 publications / 5 sources**.
   Load-time DISPLAY-ONLY encoding repair (mojibake in some derived records' authored coverage fields
   + PDF-bullet tofu in article md → repaired at render; committed records/md byte-frozen) —
   harness-swept across every doc/screen/drill.
   **Optional LIVE derivation mode (Phase 46 — companion-served, dev/authoring-time only; full
   architecture + walkthrough in `docs/corpus-live.md`):** `scripts/serve_corpus.py` (stdlib) serves
   the page + proxies llama-cpp; pasted advisory md DERIVES in real time through the FROZEN gate —
   the model proposes ONLY {section, verbatim flag, red_flag, C, D}; the deterministic downstream +
   `check_record` DISPOSE; gate-rejected indicators get ONE violation-guided re-prompt then drop
   honestly (the T1 probe decision over an opencode agent loop — ph46_probe.md). NDJSON staged
   /derive, Phase-44-pattern processing takeover (token COUNTS, never content), a session-only
   "Live derivations — UNREVIEWED" Select group; NOTHING persisted — committing a record stays a
   human-reviewed act. Live client code in `/*LIVE_*/`, build-stripped (dist/corpus byte-identical).
3. **News stream** (M8) — `news.html` → `dist/news/index.html`. The adverse-media / negative-news
   stream (a SECOND atom stream — the compose payoff is the M8 north star, scoped OUT). Arc: Select →
   Read → Screen → Disposition (the human gate) → Exposure. Runtime fuzzy matcher (normalize →
   token-sort → Jaro-Winkler, REAL scores, 0.85 threshold) is pure client-side JS — the OFFLINE ship
   file makes no LLM/fetch call; ALL live client code sits in `/*LIVE_START*/…/*LIVE_END*/` and is
   build-time STRIPPED (offline `dist/news` byte-identical, screens the static book only).
   **Optional LIVE mode (companion-served, dev/authoring-time only — full architecture + the demo
   walkthrough live in `docs/news-live.md`):** `scripts/serve_news.py` (stdlib) serves the page over
   localhost + proxies a local llama-cpp model; pasted text or a one-shot URL (`scripts/news_fetch.py`
   fetch ladder + deterministic standardizer + article-shape verifier; honest "paste instead"
   failure) is extracted in real time (subjects-only prompt + keep-biased second-pass verify),
   grounded server-side by the SHARED gate `news_ground.py` (everything grounded-or-stripped; live
   DROP / build CHECK — the ONE allowed build→companion import), and streamed as NDJSON stage
   progress. SIZE-ROBUST (Phase 43; ≈400–450 generated tokens/entity — dense docs are OUTPUT-bound):
   `call_llm` STREAMS (idle-gap timeout, no fixed deadline; live token counter), budget 16384,
   failures NAMED in-stream (output-budget · pre-flight over-context w/ the `--ctx-size` remedy —
   silent truncation would PASS the gate), `/extract` SINGLE-FLIGHT (409 — ghost jobs split slot
   throughput), disconnect-before-done persists NOTHING; Run extraction opens a DEDICATED PROCESSING
   PAGE (Phase 44: an IN-PAGE viewport takeover — real navigation would abort the stream; presenter
   keys guarded, Esc arms → Esc abandons honestly) revealing COMPLETED stages (grounded flags FINAL,
   provisional chips refined through verify) — never a token stream. GROUNDING is wrap-tolerant
   (Phase 44 — the dominant "missed flag" class was a GATE-drop, not model recall): a quote crossing
   a hard line-wrap / keeping a stripped `*` is `locate_span`-REQUOTED to the body's exact bytes
   (raw substring by construction; title-line quotes still drop). Alias FOLDS refuse ambiguity +
   type-mismatch (2+ compatible parents → no fold, order never picks the owner; person ≠ org alias;
   type disambiguates); alias OWNERSHIP stays measured-not-gated (`tests/news_quality_harness.py
   --check`, the committed extraction-quality regression gate vs `quality-baseline.json`; `--freeze`
   = conscious re-baseline). SPEED measured: generation = 92–98% of wall on notes — that IS the
   extraction; future levers = slot-parallel verify / smaller-model eval vs the harness. The scan is a
   resolution-grade identity record — `aliases[]`, closed-vocab
   `properties[]` (incl. client_number/account_number: PRIVATE INVESTIGATION NOTES are a first-class
   input), `relationships[]` (labels vocab-checked, never correctness-checked), honest
   `main_subjects`, `red_flags` FIRST in EXTRACT_SCHEMA (strict-grammar generation order is
   load-bearing); vocab authority = `news_ground.PROPERTY_KINDS`/`RELATION_LABELS` — persisted to a
   local gitignored DuckDB (`scripts/news_store.py`, companion-only — build.py NEVER imports it)
   under the ANCHOR design: exact-normalized-name anchors, cross-scan ACCUMULATION (fuzzy merge
   deferred), per-row provenance, conflicting values BOTH kept (confidence RESERVED/NULL). ESCALATE
   at Disposition grows the escalated-only watchlist (viewable + prunable); Screen scores book ∪
   watchlist over name ∪ aliases (single-token/@-handle aliases EXACT-only). The Disposition subject
   map is a deterministic vanilla-SVG NETWORK (pure `liveGraphLayout`, no lib; edge click reveals
   the grounded evidence); a node/watchlist click opens the ANCHOR DOSSIER (`GET /anchor`):
   per-scan-provenance properties, same-kind conflicts flagged "conflicting values — both kept"
   (presentation-only), honest 404/store-off states; demo seed = the committed SYNTHETIC
   `docs/demo-investigation-note.md`. PRIVACY by CHECK: gitignored store + 127.0.0.1 model; fixture
   promotion blocked by the US-federal `FIXTURE_META` allowlist (the 13-fixture replay pins the
   deterministic core offline).

4. **Gate console** (Phase 47, M9) — `console.html` → `dist/console/index.html`. The program
   blueprint's Class-J human-judgment gate dramatized (design source: `docs/program-blueprint.md`
   §4–§5 — the M9 blueprint: universal grounding / per-workload substrate+verifier / 4-class gate
   taxonomy / human-work charter): 213 REAL C/D-tag adjudication cases — the Phase-34 correction
   divergences, deterministically curated from git history (`scripts/curate_console_cases.py`,
   regeneration-only) into committed `data/console/cases.json`, build-boundary validated
   (referential integrity + flag grounding vs CURRENT records + closed C/D vocab + the
   FINTRAC-attribution rule). Arc: Queue (grouped by changed axis; honest consensus-not-ground-truth
   framing) → Evidence (verbatim `flag` beside the `red_flag` translation; NEUTRAL Assessment A/B,
   differing axis highlighted) → Disposition (graded NON-BINARY: uphold-A / uphold-B /
   both-defensible / neither-escalate; rationale REQUIRED — empty records nothing) → Record reveal
   (the adjudicated outcome DERIVED per case against the current committed codes — dataset drift
   fails the build loudly; "precedent, not a score") → session-only Ledger (JSON copy-out export;
   persists nothing). Badge always-on; FINTRAC footer attribution per on-screen doc (the one US
   case renders an empty footer); NO LLM/fetch.

5. **Triage console** (Phase 49, M9) — `triage.html` → `dist/triage/index.html`. Blueprint §14's
   continuous adjudication loop made demo-able (the gate console's sibling, console byte-frozen):
   20 fully SYNTHETIC mini-triage scenarios across the 4 §14 strata (history-signal-fired /
   below-the-line / synthetic-novel / random-population; 16 + 4 known-disposition controls),
   deterministically curated by `scripts/curate_triage_scenarios.py` (reads `data/probe-history`
   at AUTHORING time only; rule text EMBEDDED — build.py never reads probe-history) into committed
   `data/triage/scenarios.json`, build-boundary validated (closed vocabs + referential integrity
   + the US-federal-ONLY novel stratum drift-checked vs CURRENT committed records). Evidence
   panels are shared BY REFERENCE across divergent-disposition pairs (the seeded process
   inconsistency is structural). Arc: Queue (stratum-grouped; controls hidden) → Evidence →
   Disposition (the §14 grammar: confirm-risk / confirm-no-risk / both-defensible / escalate /
   need-more-info naming a C/D code via taxonomy picker / the policy-gap escape; rationale
   REQUIRED) → Reveal (the historical disposition framed "decisions, not correctness"; LABELED
   synthetic second-rater replay; process-inconsistency surfacing) → Discovery ledger (signal
   gaps DERIVED from fired-rule state · data gaps per D-code · process inconsistencies · policy
   gaps · agreement arithmetic computed at render, every number with its definition; params
   "chosen, not measured"; JSON export; persists nothing). Badge always-on; NO LLM/fetch; no
   FINTRAC content (novel stratum is US-federal public domain only — no footer machinery).

6. **Merge console** (Phase 76, M9) — `merge.html` → `dist/merge/index.html`. The blueprint's Class-J
   **merge-adjudication** gate dramatized — the human gate over entity-resolution candidate links (the
   deterministic spine resolves what it can on the declared `entity_ref` and REFUSES the ambiguous; the
   human adjudicates the residual). **The novelty:** unlike the consensus-only gate console + the
   label-blind §14 triage, the merge gate is the ONE gate with a measurable correctness ORACLE — so the
   Reveal SHOWS, where the oracle exists, whether the call matched truth (synthetic-only, qualified). TWO
   populations in committed `data/merge/cases.json` (curated by `scripts/curate_merge_cases.py` — a
   companion authoring tool that reuses entity_spine + resolution_scorer; build.py imports NEITHER): **66
   REAL candidate SHARES** (the Phase-75 over-merge-refused residual from the v0.5 slice — distinct
   `entity_ref`s sharing a noise-floor identifier; CONSENSUS-not-ground-truth, NO oracle. **Phase 77 tried
   to score these against substrate's `true_entities` and STOPPED at the abort rule: substrate's emitted
   identity clusters are content-addressed `ENT-<entity_ref>` — a 1:1 relabel of the SAME field the spine
   keys on — so any "score" is CIRCULAR (true-by-construction agreement, zero discriminating signal). Real
   scoring stays DEFERRED — it needs a genuine identity layer where `entity_ref ≠ cluster` (real same-person
   fragments / the open-data fork's real collisions): the `docs/substrate-emit-cli-wiring-PLAN-BRIEF.md` +
   `docs/substrate-open-reference-data-fork-PLAN-BRIEF.md` handoffs**) + **13 SYNTHETIC scored cases** (from
   `data/entity-spine/true_entities.json`; a latent-truth `oracle` block spanning the four quadrants
   real-co-reference / over-merge-trap / fragmentation-gap / correct-rejection — genuinely two-sided:
   resolver verdict and truth DIVERGE, independent of any spine key). Arc: Queue
   (grouped by basis: strong-shared-id / weak / name-only) → Evidence (both records + the shared signal +
   the deterministic spine baseline, NEUTRAL) → Adjudication (uphold-merge / reject-as-SHARES /
   both-defensible / escalate; rationale REQUIRED) → Verdict (the consensus/scored SPLIT: real → no
   oracle; synthetic → the latent truth + a match indicator + the synthetic-only qualifier) → session
   ledger (consensus-vs-scored agreement arithmetic; JSON export; persists nothing). THE RESOLVER-INPUT
   FIREWALL translated to the ship artifact: the pre-adjudication evidence carries NO truth field (the
   `oracle` rides a separate block, revealed post-disposition only; build-boundary `validate_merge_cases`
   guards it). Real substrate emails domain-masked to example.test. Badge always-on; NO LLM/fetch; no
   FINTRAC content.

### Build (`scripts/build.py`)
Validates a config against the schema (fail-loud), resolves `text_file`→inline, inlines everything →
the single ship file. Targets: `<id>`, `corpus`, `news`, `console`, `triage`, `merge`, `launcher`, `all`; `--check <target>`
is the drift guard (frozen dists byte-identical). **build.py NEVER imports the authoring layer.** Baseline
in `archive/`.

### Corpus sources & overlays (committed; merged at build time)
5 sources via the `CORPUS_SOURCES` registry in build.py (source-id → {status dir, derived dir,
doc_type}); each contributes a committed `corpus-status.json` manifest + `derived/*.json`, merged by
id into `__CORPUS__`, derived shape validated at the build boundary: `data/fincen/` (advisories) ·
`data/fincen-alerts/` · `data/ofac/` · `data/fintrac/` (OAs/Briefs) · `data/fintrac-guidance/`
(per-sector ML/TF indicator pages). Non-derivable (no enumerated red-flag list, honestly skipped):
the 2 FATF advisories, BEC fin-2019-a005, FINTRAC crown-agents.

Three committed OVERLAYS, each validated at the build boundary (closed-vocab + referential integrity
against the live corpus; the grounding core untouched — agent proposes, gate disposes, human reviews):
- `data/typology-map.json` — doc-id → ONE typology (27-term closed vocab); jurisdiction DERIVED
  from the source registry, not stored; the doc HEADLINE + the per-indicator INHERIT-DEFAULT.
- `data/indicator-typology-map.json` — a SPARSE per-indicator typology override (a FINTRAC sector
  page is inherently MULTI-typology — a doc-level map alone forced a catch-all); the **Typologies
  lens + cross-corpus synthesis group by INDICATOR typology**; the cross-cutting remainder sits in
  the honest `cross-cutting-indicators` bucket; coverage stays honest union arithmetic — no lift/dedup.
- `data/capability-taxonomy.json` — C1–C28 capabilities + D1–D20 data sources (code → {name, group,
  interview posture}); powers the Capabilities + Data-sources lenses.

### Authoring pipeline (build-time ONLY — the ship file never fetches or calls an LLM)
`crawl_fincen.py` (listing → committed manifest) → `acquire_fincen.py` (PDF, or `--html`) →
`pdf_to_md.py` (markitdown → committed `<id>.md`, the derivation SURFACE & source of truth) →
`derive_signals.py` (the deterministic GATE). `derive_signals.py` is stdlib-only; only `markitdown`
lives in the gitignored uv `.venv`. No authoring tool is imported by the engine or build.py.

### The inverted extraction boundary (LOAD-BEARING)
**The LLM EXTRACTS, the deterministic layer GATES.** The LLM reads `<id>.md` and extracts the red
flags + per-indicator judgment (status, data, build_rec, build_logic, the `red_flag` translation,
C/D tags) into `derived/<id>.json`; `derive_signals.py --check-derived` DISPOSES via `check_record`:
quote-grounding (every verbatim `flag` a substring of the source md under `normalize()`, inside
`rf_region`), the cover×data matrix (BUILD_NOW ⇒ a full build_logic), the `red_flag` SHAPE check
(non-empty / distinct-from-verbatim / 12–240 chars). The grounded verbatim `flag` (EVIDENCE) shows
BESIDE the natural-AML `red_flag` TRANSLATION (the one neural step — mitigated by show-both + the
badge). The gate checks faithfulness + (per-doc) completeness; it does NOT check the C/D tag is
correct — verified separately (a grounding gate ≠ a completeness gate ≠ a correctness gate).

### Coverage is GROUNDED, not fabricated
Each indicator's coverage (status / data / build_rec / build_logic) is DERIVED deterministically from
its C/D codes + the institution's 28+20 YES/NO/PARTIAL interview posture via the cover×data matrix +
per-capability spec templates; honest SOURCE_DATA where the bank can't observe.

### Honesty constraints (LOAD-BEARING)
- Cross-corpus / lens coverage is honest UNION arithmetic / honest COUNTS over the existing
  per-indicator status. NO similarity / overlap / lift number is computed or claimed; indicators are
  NOT de-duplicated across regulators. The always-on "Illustrative data & outputs" badge stays.
- The corpus combination-lift beat carries NO lift/precision figure (Phase 45 deleted the Phase-18-era
  generic illustrative template AND its "pending calibration" tag): the screen shows honest INVENTORY
  counts only — covered indicators in the committed signal's typology × contributing regulators,
  computed client-side at render, the same honesty class as the lens counts — framed as candidate
  composition partners feeding the promotion gate. The derived records carry no lift numbers. The
  SHOWCASE Act-5 keeps its illustrative lift template (a deliberate, gate-accepted divergence).

### News data (`data/news/{articles/*.md, derived/*.json, book.json}`)
`articles` are REAL US-federal gov-enforcement docs (DOJ + OFAC, verbatim-excerpted under 17 U.S.C.
§105 public domain). `book.json` is SYNTHETIC (non-negotiable #4) — REAL adverse-media entity ×
SYNTHETIC book, seeded with an exact true-positive, near-matches, and a common-name false-positive
trap dismissed at the gate. `validate_news_data` grounds every entity name + attribute + flag at the
build boundary (a LOCAL normalizer — build.py never imports the authoring layer).

### Conventions (LOAD-BEARING)
- Derived records store RAW text; corpus.html's `esc()` is the SOLE escaper (never pre-escape
  `&gt;`/`&lt;` in a record — it double-escapes).
- `normalize()` drops glued running headers (e.g. `FINCEN ADVISORY`), collapses smart quotes /
  hyphen-wraps / footnote digits, and drops `|`/`#`/`*`/spaces (so de-piped tables + markdown-ATX
  headers stay grounding-INVARIANT). Keep an in-flag footnote marker verbatim where it falls mid-span
  (e.g. `NPO84`).
- The grounding gate logic (`normalize` / `rf_region` / `check_record`) is the STABLE core — extend
  `rf_region` ANCHORS only, REGRESSION-GATED (every existing md's region must stay byte-unchanged;
  `--selftest` fixtures pin each anchor).
- Heterogeneous formats handled by the LLM reading like a human (no structural parser): footnote-
  interrupted lists (extract a contiguous grounded span, drop the across-the-break continuation) and
  glued-no-separator advisories (markitdown dropped bullets + blank lines; the LLM extracts every
  genuine flag, the gate grounds each).

## How to run
- Build: `python3 scripts/build.py <id>` (or `corpus` / `news` / `console` / `triage` / `merge` / `all`) → the
  ship file (`corpus` merges `CORPUS_SOURCES` + the three overlays; `news` reads
  `data/news/{articles,derived,book}`; `console` reads `data/console/cases.json`; `triage` reads
  `data/triage/scenarios.json`; `merge` reads `data/merge/cases.json` — all grounded/validated at the build
  boundary; the merge cases are curated by the companion `scripts/curate_merge_cases.py`, which build.py NEVER imports).
- Present: open `dist/<id>/index.html` (or `dist/corpus/`, `dist/news/`, `dist/console/`,
  `dist/triage/`, `dist/merge/`) — single self-contained file, offline, no server.
- News LIVE mode (optional, dev/authoring-time): start llama-cpp (set `--ctx-size` — see the doc),
  then `.venv/bin/python scripts/serve_news.py` → http://localhost:8000 (URL or paste + source
  type; `.venv` enables persistence/URL mode). Offline `dist/news` unaffected; full walkthrough +
  flags: `docs/news-live.md`.
- Corpus LIVE derivation mode (optional, dev/authoring-time, stdlib-only — no venv): llama-server up,
  then `python3 scripts/serve_corpus.py` → http://localhost:8010 (paste a converted advisory md;
  derives through the frozen gate, propose-only). Offline `dist/corpus` unaffected; doc:
  `docs/corpus-live.md`.
- Investigator WORKBENCH (companion-only — NOT a ship/build target; never goes to `dist/`): `python
  scripts/setup_workbench.py` (Phase 67 — CROSS-PLATFORM [Windows/mac/Linux, no make/Unix-shell]; builds the
  VENDORED casework venv from the committed wheel) then `python scripts/serve_workbench.py` → http://localhost:8030
  (reads committed `data/workbench/**` + `data/osint/corpus.json`; binds 127.0.0.1; persists nothing). The FULL
  live arc — CLUTTER→SIGNALS→gating-loop + GATHER + DETERMINATION + the DECIDE signed-STR finale — runs OFFLINE
  on the deterministic STUB from a BARE CLONE. The DETERMINATION beat (Phase 69, companion-only) is the
  evidence-SUFFICIENCY control: a per-typology `data/workbench/evidence-requirements.json` profile (chosen-not-
  measured determination-licensing ATOMS) + `scripts/evidence_requirements.py` (load/validate + the pure
  `determine` verdict); the decision is licensed by sufficiency (mechanism + ≥2 corroborating legs + a NAMED
  predicate risk + no unrebutted mitigation), NOT combo-FREQUENCY (the Phase-64 gate is DEMOTED to context);
  GATHER is requirement-TARGETED (seek the unmet closeable atoms — UBO/corroboration — record-sourced) + Phase-70
  MEASURED: a `coverage` block measures the LIVE extraction vs the deterministic StubPlanner REFERENCE
  (consistency-not-correctness; pinned via `tests/gather_quality_harness.py --check`, no model). Phase 71/72 ADOPT
  the substrate v0.3 slice + Phase-26 C14 kyc emission (`aml-substrate@f15c241`; vendored `aml-casework@bf15535`
  accepts v0.3 + grounds C14; the casework pin is READ from `VENDORED_AT`): `curate_workbench_cases` MERGES each
  customer's monitoring + C8/C14-screening bundles (a case = a customer) so C8 (ML-A3) co-occurs with
  C15/`related_parties[]` (ML-A4) — the **§12 ML loop CLOSES from REAL signals** (≥2-leg, no GATHER). The **§12 KYC
  loop CLOSES too** (Phase 72): a C14-PURE customer (no ML co-firing → `kyc_integrity` via the dual-map,
  correct-not-bug) determines from KYC-A1 — C14 ALONE (kyc = mechanism + 0 legs); kyc SIGNING is the honest
  cross-pillar FRONTIER — txn-bearing C14 cases SIGN, txn-LESS party-leaf cases fail-CLOSED at casework's
  no-transactions CONTRACT (`e2e_note`, never loosened — a named casework follow-on).
  Slice **376** (substrate v0.5 @fc98b09 + a cross-case CO-REFERENCE pass), coverage **128/376**, funnel (auto/human/review) 202/111/63; 6 kyc cases (2 sign). The bundle's
  `related_parties[]` BO graph renders as the case network (`boGraphHTML`; "N pct"); the gather/finale DEMO case
  resolves from the OSINT corpus (`gather_demo_case_id`), re-curate-robust. **Phase 73** AUTHORS the north-star
  rich case — a SEPARATE companion source `data/casefile/{case.json,schema.md}` (substrate/casework PARKED, the
  artifact-is-the-spec): the matched FILE/DISMISS pair (CASE-A Northgate files / CASE-B Lakeshore clears) firing
  the SAME grounded signals yet resolving OPPOSITELY on an authored network + source-of-funds layer. The pair
  LEADS the queue; the two verdicts are LIVE-ENGINE OUTPUT (`serve_workbench` casefile path DERIVES the engine
  inputs from the evidence; the authored `expected_*` a regression oracle via a fixture-drift bridge). The engine
  gained the affirmative-`cleared` verdict (mechanism + 0 legs + affirmative mitigation established — a SEPARATE
  clear path; **the file/determination bar BYTE-UNCHANGED**, the A1 guard) + a `read`-from-file evidence source +
  predicate-from-register. `workbench.html` `showcaseSurface` renders names-not-codes + 3 graphs
  (`scMoneyFlowGraph`/`scResolutionGraph`/`scBOGraph`). The cross-pillar contract `docs/rich-case-target-contract.md`
  is a DEFERRED follow-on. **Phase 74** adds the companion-only PERSISTENT ENTITY SPINE — `scripts/entity_spine.py`
  (a NEW gitignored-DuckDB module; `news_store` byte-untouched): observations → an append-only, bitemporal, GRADED
  `resolution_links` layer (deterministic strong-id MERGE / weak-corroborate / name-only REJECT; reversible split with
  cascade-invalidation; conflicts both-kept) → `persistent_entities` accumulating prior dispositions. Confidence is a
  deterministic ordinal GRADE (strong/weak/reject, fail-closed) carried as PROVENANCE on a SEPARATE grade-gated read
  path — a low-grade link is EXCLUDED (never down-weighted) from the byte-frozen file bar; priors are analyst-visible
  only (the self-confirming-loop guard — injecting a prior `cleared` → byte-identical verdict). The re-surfacing MEMORY
  demo (`casefile_memory`; the `resurfacing` block — Vesna Maric on her INDEPENDENT prior-STR PSR-0001) MEASURABLY
  shrinks gather targets-to-close + pre-names the predicate; the event-driven STALE-prior guard re-opens a prior whose
  identity changed. `scripts/resolution_scorer.py` scores resolution vs synthetic `data/entity-spine/true_entities.json`
  (pairwise/B-cubed, synthetic-only qualifier) behind a resolver-input firewall (no cluster-id / no 1:1 surrogate).
  **Phase 75** CONSUMES the substrate v0.5 emission (Phase-27/28 named-identity + entity-resolution, additive) into the spine —
  `substrate_memory` (serve_workbench) feeds each slice case's parties keyed on `entity_ref` (substrate's RELIABLE declared
  identity — now a STRONG_KINDS key) + the `/memory` panel renders it. **The T1 measure-first gate caught a MECHANISM error:**
  substrate's shared strong identifiers — and its OWN `resolution_edges` (`status:"resolved"`) — are a deliberate collision
  NOISE FLOOR + controller-cluster SHARES between DISTINCT entities (`gen/identity.py`), so a strong-MERGE would OVER-MERGE.
  Honest consume: key cross-case memory on `entity_ref` (substrate email/phone DEMOTED to weak candidate-SHARES, never a merge
  key); identifiers/resolution_edges are CANDIDATE SHARES links the spine ADJUDICATES. Committed slice: **36 cross-case
  CO-REFERENCES** (the real-data memory beat) + **66 over-merge-REFUSED**. casework rejects contract_version "0.5" but TOLERATES
  the additive fields → curate hands it the v0.3 VIEW (committed bundle stays v0.5). The determination bar BYTE-UNCHANGED (the A1
  guard); `scripts/measure_xcase_overlap.py` is the committed measurement.
  Standards: `docs/{resolution-link-schema,identity-grade-grammar,confidence-as-provenance-contract,true-entities-scorer-contract}.md`;
  sibling EMISSION briefs RE-GROUNDED to live HEADs (Phase 77, CODE-VERIFIED): substrate@f2da3e4 — `true_entities` (P29) +
  `intended_disposition` (P30) EXIST but are UNWIRED into the substrate CLI (the emit_* fns run only in substrate tests → the
  `docs/substrate-emit-cli-wiring-PLAN-BRIEF.md` handoff). Phase 77 ATTEMPTED real-merge scoring from the `--identity` parquet and
  STOPPED at the abort rule: substrate's identity clusters are content-addressed `ENT-<entity_ref>` (1:1 with the spine's own key) →
  any score is CIRCULAR (true-by-construction). Real merge scoring stays DEFERRED — it needs `entity_ref ≠ cluster` (a genuine
  identity layer / the `docs/substrate-open-reference-data-fork-PLAN-BRIEF.md` real collisions). casework@b3546d4 — `cleared` (P18)
  is BUILT and CONSUMED: the workbench DECIDE signs `cleared` end-to-end on the C5-replayable `data/casefile/cleared-demo.bundle.json`;
  the north-star Lakeshore CASE-B still fails-closed on casework's fan-OUT-only C3 (Lakeshore's C3 is fan-IN) → the
  `docs/casework-c3-fan-in-PLAN-BRIEF.md` handoff. Briefs: the Phase-74 `docs/{substrate-graded-counterparty-identifiers,substrate-exogenous-disposition-label,casework-confidence-graded-resolution}-PLAN-BRIEF.md`
  + the Phase-77 `docs/{substrate-emit-cli-wiring,casework-c3-fan-in,substrate-open-reference-data-fork}-PLAN-BRIEF.md` + `docs/cross-pillar-build-order.md`.
  Probabilistic/Splink ER + graph/Kuzu + the medallion/DuckLake are DEFERRED
  (named in the standards; the merge-adjudication Class-J console is now BUILT, Phase 76/77). Still-deferred substrate-emission gaps
  (named in `signal_brief`): C1 anticipated-activity (a PRINCIPLED measured null), broader C7, a TF slice — the
  consolidated §12 BRIEF (`docs/substrate-determination-signals-PLAN-BRIEF.md`). The chain workbench
  renders the structured STR's COMPLETENESS (the previously-dropped fields surfaced honest-NULL). Doc:
  `docs/evidence-driven-filing.md`. `aml-casework` is VENDORED into `vendor/aml-casework/` (its src + a
  cross-platform WHEEL under `dist/` + its pinned corpus snapshot under `fixtures/corpus/`); resolution =
  `AML_CASEWORK_DIR` > vendored > `../aml-casework` sibling > GATED; venv python + `SIGNAL_WATCH_CORPUS` are
  resolved CROSS-PLATFORM (`serve_chain.casework_python`/`casework_corpus_env`). The DECIDE consume is still a
  SUBPROCESS file-handoff (now passing `--disposition` file|cleared) — build.py NEVER imports casework, the 9 ship
  dists stay byte-frozen (the workbench is companion-only, touches no dist; vendoring is DISTRIBUTION, not
  coupling). Without setup the DECIDE finale is a named GATED stage; the rest of the arc is unaffected. LIVE neural (optional, server-side only, never in the browser §4.5): the `openai` backend
  ALWAYS-AVAILABLE, DEFAULTING to a local model at `127.0.0.1:8080` (NO env — `OPENAI_BASE_URL` only OVERRIDES
  the host/port; the auto-default stays stub unless it's set or a claude key) → pick it to drive the GATHER
  loop + DECIDE prose, else the stub (the casework pipeline still shapes/signs/verifies offline; no model →
  fast TCP-refuse → stub + a "no model at :8080" note). Live tier needs Python ≥3.11 + uv-or-pip (the
  offline ship artifacts stay zero-dep, stdlib-3.10; `make setup` is a POSIX shortcut for the script). **The §12
  DISCOVERY FEED (Phase 78, companion-only):** a read-only `/discovery` route + panel surfaces the
  determination-validation harness's engine-vs-oracle disagreement queue — *missed* (oracle-file, signals not
  assembled = a §12 build target, each with the engine's own `missing[]`) + *over-flag* (oracle-clear, signals
  file-ready = defensive exposure, incl. the KYC structural over-flag). PRESENTATION-ONLY: the exogenous oracle
  rides this path, NEVER the determination engine (the priors-are-provenance firewall; `evidence_requirements.py`
  byte-unchanged). Source = `scripts/determination_validation_harness.py` (the "circularity exit"; doc
  `docs/determination-validation.md`). Doc: `docs/case-workbench.md`. Precursor the CHAIN workbench: `python3 scripts/serve_chain.py` → http://localhost:8020
  (`docs/chain-workbench.md`). Companion ports: news 8000 · corpus 8010 · chain 8020 · workbench 8030.
- Drift guard before presenting: `python3 scripts/build.py --check all` (frozen dists byte-identical).
- Test (dep-free, no install — except the DuckDB store selftests, which run under `.venv`):
  - `node tests/corpus-explorer.test.mjs` — the story landing + the 6-screen per-doc arc + the
    multi-source menu (FINTRAC footer attribution) + the 4 lenses + cross-corpus synthesis + the
    Phase-46 live mode (the offline strip assertion + the companion-served live branch: injection,
    pure processing-page contract, done/error/409 paths) ·
    `python3 scripts/serve_corpus.py --selftest` — the corpus live companion (offline, no model:
    schema↔taxonomy mirror, deterministic-downstream exactness on a committed record, the stubbed
    full derive loop incl. the violation-guided retry, page render + payload parity with the build).
  - `node tests/gate-console.test.mjs` — the gate-console adjudication arc (queue/evidence, the
    rationale-REQUIRED graded disposition gate, record reveal only post-disposition, ledger +
    JSON export, badge + per-doc FINTRAC footer [US case empty], XSS-escape, keyboard guards,
    both motion modes).
  - `node tests/triage-console.test.mjs` — the triage-console §14 arc (stratified queue [controls
    hidden], the 6-option graded gate [rationale required; need-more-info requires a C/D pick;
    policy-gap escape], reveal locked pre-disposition [decisions-not-correctness; labeled
    second-rater replay; process-inconsistency surfacing], the DERIVED discovery ledger
    [hand-computed agreement fixture + definition strings], XSS, keyboard guards, both motion
    modes) · `python3 scripts/curate_triage_scenarios.py --selftest` — the curate validators
    (broken fixtures rejected; deterministic regen; 12 rules parsed).
  - `node tests/merge-console.test.mjs` — the merge-console Class-J arc (queue grouped by basis +
    the consensus/scored chips; Evidence NEUTRALITY [the firewall: the oracle truth never appears
    pre-adjudication]; the rationale-REQUIRED graded gate; the Verdict locked pre-adjudication + the
    real-consensus/synthetic-scored SPLIT [synthetic → latent truth + match indicator + the synthetic-only
    qualifier; real → no oracle]; ledger agreement arithmetic [matched/scored vs consensus] + JSON export;
    the honesty-governor word-ban [no catch-rate/lift/precision]; XSS, keyboard guards, both motion modes) ·
    `python3 scripts/curate_merge_cases.py --selftest` — the merge-case curator validators (firewall: no
    truth in evidence; consensus/scored split; closed vocab; deterministic regen; 7 broken fixtures rejected;
    reproduces the Phase-75 66 over-merge-refused). Needs DuckDB — run under `.venv` (SKIPs without it).
  - `node tests/news-stream.test.mjs` — the adverse-media arc + fuzzy matcher; both motion modes;
    the companion-served live overrides (watchlist screen/escalate/view/prune + the alias-aware
    matcher [exact-yes/fuzzy-no per class] + the SVG network [deterministic liveGraphLayout:
    centrality/bounds/degenerate-shape/XSS-escape; edge click reveals evidence] + the anchor
    dossier [conflict both-kept flag, honest 404/empty states] + the Phase-44 processing page
    [pure liveProcBody/liveProcKeyAction: key guard, Esc arm/abandon]) + the offline strip assertion.
  - `python3 tests/news_quality_harness.py --check` — the extraction-quality REGRESSION GATE
    (deterministic replay of all pinned captures + committed records vs the committed baseline).
  - `python3 tests/gather_quality_harness.py --check` — the GATHER extraction-coverage REGRESSION GATE
    (Phase 70: replay the pinned live capture with NO model; assert finding_coverage/target-closure still
    match the baseline + the deterministic StubPlanner reference; `--freeze` re-captures from a live model).
  - `python3 scripts/determination_validation_harness.py --check` / `--selftest` — the DETERMINATION-VALIDATION
    REGRESSION GATE (Phase 78, the "circularity exit"): replay the committed substrate-oracle capture with NO
    substrate, RE-RUN the engine per case (bundle-only: mechanism + ≥legs, human-gate inputs HELD OUT) and
    assert the live engine still matches the frozen confusion structure vs aml-substrate's EXOGENOUS
    `intended_disposition` oracle (authored blind to the sufficiency rule; `assert_no_oracle_leak` + the
    signature guard hold the firewall). `--freeze --emit-dir <out>` re-captures from a substrate emit @9677a37.
  - `python3 scripts/entity_spine.py --selftest` — the persistent entity spine (strong-id merge / name-only
    reject / weak corroborate; append-only graded links; conflicts both-kept; reversible split with
    cascade-invalidation; event-driven stale-prior; the no-news-import firewall; Phase-75 entity_ref-keyed cross-case
    memory + SHARES over-merge refusal) · `python3 scripts/measure_xcase_overlap.py --selftest` — the Phase-75 measure-first
    gate (cross-case entity_ref co-reference vs the shared-identifier over-merge trap; records a count, never asserts nonzero) ·
    `python3 scripts/resolution_scorer.py
    --selftest` — the resolution-correctness scorer (pairwise/B-cubed vs synthetic true_entities; the resolver-input
    firewall rejects a cluster surrogate; Phase-76 expanded the oracle to 25 obs / 17 clusters spanning the four
    merge-adjudication quadrants — `candidate_pairs()` enumerates the merge-console queue). Both need DuckDB — run
    under `.venv` (they SKIP gracefully without it); both are in the `uv run pytest` umbrella.
  - `python3 scripts/derive_signals.py --selftest` — the derivation GATE checks + anchor fixtures.
  - `python3 tests/news_live_test.py` — the live pipeline: build_record + grounding, the 13-fixture
    REPLAY (goldens, no model; US-federal FIXTURE_META allowlist asserted), the second-pass verify,
    the `/extract` stream + URL routes (stubbed) + `/watchlist/prune` + `/anchor`; `--live` = the
    real-model smoke; under `.venv` also the watchlist/disposition/anchor DuckDB loop ·
    `python3 scripts/news_ground.py --selftest` · `python3 scripts/news_fetch.py --selftest` ·
    `.venv/bin/python scripts/news_store.py --selftest` · `python3 scripts/serve_news.py --selftest`.
  - Pre-present sequence: `--check all` (drift) → `node tests/…` (arcs) → walk `tests/smoke-checklist.md`.
- Authoring a new corpus source (build-time only; raw PDFs gitignored, committed `<dir>/*.md` is the
  surface): `crawl_fincen.py --fetch`/`--write` → `acquire_fincen.py [--html] <id>` → `pdf_to_md.py
  <id>` → derive via the inverted loop → `derive_signals.py --corpus-status <dir>` → rebuild.
- Iterate: edit a template/config, rebuild. `python3 -m http.server` optional, never required.

## Knowledge wiki
Domain reference = the registered **aml-wiki** (`/Users/jwang/private-knowledge/aml-wiki`) — AML
typologies, red-flag indicators, FINTRAC/FinCEN + OSFI E-23, the atom/composition vocabulary; a
gitignored symlink `wiki/ →` it auto-selects it here. Query before guessing (`/wiki-query`);
keep-worthy AML insights go back via `/wiki-add`. For a new typology, pull paraphrased advisory
specifics from the wiki — or derive from verbatim FinCEN markdown via the M6 pipeline.

## Aesthetic
Dark "dossier" theme, amber `--signal` (#f6a623) accent; fonts Newsreader / Archivo / JetBrains
Mono; theme in `:root` CSS variables. Refined, not flashy.

## Milestones
M0 bootstrap · M1 config-driven refactor · M2 multi-typology · M3 presenter polish · M4 (skipped) ·
M5 ship · M6 ingestion pipeline (FinCEN verbatim) · M7 corpus-backed demo (`dist/corpus/`: inverted
derivation loop, 5 sources, 4 lenses, cross-corpus synthesis, grounded coverage) · M8 adverse-media
stream (`dist/news/`) · M9 program design (`docs/program-blueprint.md` §1–§15 — Phase 48 added
§12 brownfield history utilization ["history is evidence, never ground truth"], §13 LFCM target
architecture [library-not-monolith; dossier-now/score-deferred], §14 the continuous adjudication
loop — + the `dist/console/` gate console + the history-decomposition probe `data/probe-history/`
w/ `scripts/probe_history_stats.py` [outside every build path; writeup `docs/probe-history.md`; the
SYNTHETIC Phase-48 fixture PLUS, since Phase 62, a GROUNDED probe-history `data/probe-history/grounded/`
projected by the aml-substrate P22 projector (`probe_history_stats.py --grounded`, pinned to
substrate@ae98924, capability→TM map `capability-tm-map.json`) — §12 MEASUREMENT only: the §14
triage console stays synthetic-curated by design (the substrate's label-blind alerts carry no
adjudicable fact pattern — the §12-right/§14-wrong-source boundary)] + the NON-ship offline report
`docs/blueprint-report.html` + the `dist/triage/` triage console [Phase 49 — §14's loop embryo made
demo-able]).
Per-phase detail: git log + `.dev-wiki/` journal + HANDOFF.md §8.

## Definition of done
Reliable offline · multi-typology from config · presenter controls · compliance-clean · README
written. See HANDOFF.md §1.2.
