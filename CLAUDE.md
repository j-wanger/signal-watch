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

### Five ship artifacts (each a single self-contained offline file)
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

### Build (`scripts/build.py`)
Validates a config against the schema (fail-loud), resolves `text_file`→inline, inlines everything →
the single ship file. Targets: `<id>`, `corpus`, `news`, `console`, `triage`, `all`; `--check <target>`
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
- Build: `python3 scripts/build.py <id>` (or `corpus` / `news` / `console` / `triage` / `all`) → the
  ship file (`corpus` merges `CORPUS_SOURCES` + the three overlays; `news` reads
  `data/news/{articles,derived,book}`; `console` reads `data/console/cases.json`; `triage` reads
  `data/triage/scenarios.json` — all grounded/validated at the build boundary).
- Present: open `dist/<id>/index.html` (or `dist/corpus/`, `dist/news/`, `dist/console/`,
  `dist/triage/`) — single self-contained file, offline, no server.
- News LIVE mode (optional, dev/authoring-time): start llama-cpp (set `--ctx-size` — see the doc),
  then `.venv/bin/python scripts/serve_news.py` → http://localhost:8000 (URL or paste + source
  type; `.venv` enables persistence/URL mode). Offline `dist/news` unaffected; full walkthrough +
  flags: `docs/news-live.md`.
- Corpus LIVE derivation mode (optional, dev/authoring-time, stdlib-only — no venv): llama-server up,
  then `python3 scripts/serve_corpus.py` → http://localhost:8010 (paste a converted advisory md;
  derives through the frozen gate, propose-only). Offline `dist/corpus` unaffected; doc:
  `docs/corpus-live.md`.
- Investigator WORKBENCH (companion-only — NOT a ship/build target; never goes to `dist/`): `make setup`
  (Phase 67 — builds the VENDORED casework venv) then `python3 scripts/serve_workbench.py` → http://localhost:8030
  (reads committed `data/workbench/**` + `data/osint/corpus.json`; binds 127.0.0.1; persists nothing). The FULL
  live arc — CLUTTER→SIGNALS→gating-loop + GATHER + the DECIDE signed-SAR finale — runs OFFLINE on the
  deterministic STUB from a BARE CLONE: `aml-casework` is VENDORED into `vendor/aml-casework/` (+ its pinned
  corpus snapshot at `vendor/aml-casework/fixtures/corpus/`); resolution = `AML_CASEWORK_DIR` > vendored >
  `../aml-casework` sibling > GATED. The DECIDE consume is still a SUBPROCESS file-handoff — build.py NEVER
  imports casework, the 8 dists stay byte-frozen (vendoring is DISTRIBUTION, not coupling). Without `make setup`
  the DECIDE finale is a named GATED stage; the rest of the arc is unaffected. LIVE neural (optional,
  server-side only, never in the browser §4.5): a model on `127.0.0.1:8080` (`OPENAI_BASE_URL`) / an Anthropic
  key drives the GATHER loop + DECIDE prose, else the stub (the casework pipeline still shapes/signs/verifies
  offline). Live tier needs Python ≥3.11 + uv (the offline ship artifacts stay zero-dep, stdlib-3.10). Doc:
  `docs/case-workbench.md`. Precursor the CHAIN workbench: `python3 scripts/serve_chain.py` → http://localhost:8020
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
  - `node tests/news-stream.test.mjs` — the adverse-media arc + fuzzy matcher; both motion modes;
    the companion-served live overrides (watchlist screen/escalate/view/prune + the alias-aware
    matcher [exact-yes/fuzzy-no per class] + the SVG network [deterministic liveGraphLayout:
    centrality/bounds/degenerate-shape/XSS-escape; edge click reveals evidence] + the anchor
    dossier [conflict both-kept flag, honest 404/empty states] + the Phase-44 processing page
    [pure liveProcBody/liveProcKeyAction: key guard, Esc arm/abandon]) + the offline strip assertion.
  - `python3 tests/news_quality_harness.py --check` — the extraction-quality REGRESSION GATE
    (deterministic replay of all pinned captures + committed records vs the committed baseline).
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
