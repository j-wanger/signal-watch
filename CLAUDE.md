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

### Three ship artifacts (each a single self-contained offline file)
1. **Showcase** — `index.html` → `dist/<id>/index.html`. The generic six-act engine (vanilla
   HTML/CSS/JS, single `__CONFIG__` injection point, typology-agnostic — adding a typology is one
   JSON file, no engine edits); presenter controls (keyboard nav ←/→/Space/Esc/↺, reset,
   `prefers-reduced-motion`). Content: `config/typologies/*.json` (fentanyl, trade-based,
   elder-financial-exploitation) against `config/schema.md`; the elder typology renders the FULL
   verbatim EFE advisory (FinCEN FIN-2022-A002, public domain) in Act 1 via `advisory_full`.
2. **Corpus explorer** — `corpus.html` → `dist/corpus/index.html`. A SEPARATE artifact (own copy of
   the dossier theme; `index.html` byte-untouched). 6-screen per-doc arc: Select → Read advisory →
   Coverage → Build recs (**the human GATE**) → Signal → Combination lift → Close; FOUR Select lenses
   (Documents / Typologies / Capabilities / Data sources). Scale: **2,251 indicators / 56 derived /
   62 publications / 5 sources**.
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
   progress. The scan is a resolution-grade identity record — `aliases[]`, closed-vocab
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

### Build (`scripts/build.py`)
Validates a config against the schema (fail-loud), resolves `text_file`→inline, inlines everything →
the single ship file. Targets: `<id>`, `corpus`, `news`, `all`; `--check <target>` is the drift guard
(frozen dists byte-identical). **build.py NEVER imports the authoring layer.** Baseline in `archive/`.

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
- The ONE approved fabrication-shaped reversal: the corpus combination-lift figures are a GENERIC
  illustrative template (18→64→83), identical across docs, behind a LOUD "Illustrative · pending
  calibration — NOT measured" tag (distinct from the always-on badge). The derived records carry no
  lift numbers.

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
- Build: `python3 scripts/build.py <id>` (or `corpus` / `news` / `all`) → the ship file (`corpus`
  merges `CORPUS_SOURCES` + the three overlays; `news` reads `data/news/{articles,derived,book}` —
  both grounded/validated at the build boundary).
- Present: open `dist/<id>/index.html` (or `dist/corpus/`, `dist/news/`) — single self-contained
  file, offline, no server.
- News LIVE mode (optional, dev/authoring-time): start a local llama-cpp server, then
  `.venv/bin/python scripts/serve_news.py --llm-url <chat-endpoint> --model <name>` → open
  http://localhost:8000; submit a URL or paste text + pick a source type (run under `.venv` for
  persistence + URL mode; `--export-parquet <dir>`; `--no-persist` disables). The offline
  `dist/news` is unaffected. Demo walkthrough + details: `docs/news-live.md`.
- Drift guard before presenting: `python3 scripts/build.py --check all` (frozen dists byte-identical).
- Test (dep-free, no install — except the DuckDB store selftests, which run under `.venv`):
  - `node tests/corpus-explorer.test.mjs` — the story landing + the 6-screen per-doc arc + the
    multi-source menu (FINTRAC footer attribution) + the 4 lenses + cross-corpus synthesis.
  - `node tests/news-stream.test.mjs` — the adverse-media arc + fuzzy matcher; both motion modes;
    the companion-served live overrides (watchlist screen/escalate/view/prune + the alias-aware
    matcher [exact-yes/fuzzy-no per class] + the SVG network [deterministic liveGraphLayout:
    centrality/bounds/degenerate-shape/XSS-escape; edge click reveals evidence] + the anchor
    dossier [conflict both-kept flag, honest 404/empty states]) + the offline strip assertion.
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
stream (`dist/news/`). Per-phase detail: git log + `.dev-wiki/` journal + HANDOFF.md §8.

## Definition of done
Reliable offline · multi-typology from config · presenter controls · compliance-clean · README
written. See HANDOFF.md §1.2.
