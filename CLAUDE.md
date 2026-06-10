# Signal Watch — AML Vision Demo

## What this project is
A presenter-driven, offline, browser-based VISION PROTOTYPE for AML stakeholder buy-in.
Not a real detection system — a scripted dramatization of the signal/atom loop.
See HANDOFF.md for full context; it dramatizes POC 5 → POC 1 → POC 3 of the
AML transformation framework. Keep vocabulary consistent with it
(atoms, composition, promotion gate, coverage index, etc.).

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
> **Maintenance contract** (this file bloated to 689 lines once — this is the guard against a repeat).
> No automated process writes this file: there's no `AGENTS.md`/`sync-rules` here, and `/dev-debrief`'s
> refresh only ever rewrites four MACHINE sections (Project Rule Modules / Dynamic State / Project
> Pointers / Project Scope) which this file doesn't have. The implementing agent edits it BY HAND each
> phase — so this discipline is the only guard:
> - `## Current state` is a SNAPSHOT of what is TRUE NOW — **replace facts in place; NEVER append a
>   per-phase bullet.** `## Milestones` is one line per milestone — **never a per-phase line.**
> - Per-phase narrative (what a phase changed, harness/size deltas, frozen-set proofs) goes to the
>   `.dev-wiki/` journal + the git commit message + HANDOFF.md §8 — **not here.**
> - Target ≤ ~200 lines. If it's growing, a phase log is leaking in — move it out.

This section is the DURABLE, currently-true architecture — not a changelog.

### Three ship artifacts (each a single self-contained offline file)
1. **Showcase** — `index.html` → `dist/<id>/index.html`. The generic six-act engine (vanilla
   HTML/CSS/JS), single `__CONFIG__` injection point, typology-agnostic (adding a typology is one
   JSON file, no engine edits). Presenter controls (M3): keyboard nav (←/→/Space/Esc/↺), reset,
   `prefers-reduced-motion`. Content: `config/typologies/*.json` (fentanyl, trade-based,
   elder-financial-exploitation) against `config/schema.md`. The elder typology renders the FULL
   verbatim EFE advisory (FinCEN FIN-2022-A002, public domain) in Act 1 via `advisory_full`.
2. **Corpus explorer** — `corpus.html` → `dist/corpus/index.html`. A SEPARATE artifact that owns
   its own copy of the dossier theme (`index.html` stays byte-untouched). 6-screen per-doc arc:
   Select → Read advisory → Coverage → Build recs (**the human GATE** — per-indicator cover×data,
   BUILD_NOW rows selectable) → Signal → Combination lift → Close. FOUR Select lenses: Documents /
   Typologies / Capabilities / Data sources. Scale: **2,251 indicators / 56 derived / 62
   publications / 5 sources**.
3. **News stream** (M8) — `news.html` → `dist/news/index.html`. The adverse-media / negative-news
   stream (a SECOND atom stream: an adverse-media hit is an ATOM that composes with a counterparty's
   transaction signals — the compose payoff is the M8 north star, scoped OUT). Arc: Select → Read →
   Screen → Disposition (the human gate) → Exposure. Runtime fuzzy matcher (normalize → token-sort →
   Jaro-Winkler, REAL scores, 0.85 threshold) is pure client-side JS — the OFFLINE ship file makes no
   LLM/fetch call. **Optional LIVE mode (Phase 35–39):** `scripts/serve_news.py` (a stdlib companion) serves
   the page over http://localhost + proxies a local llama-cpp model so a pasted article — or an article URL,
   acquired ONE-SHOT server-side by `scripts/news_fetch.py` (a fetch LADDER urllib→curl→markitdown with
   cookie-jar + one same-host interstitial-refresh follow, then a deterministic format STANDARDIZER + an
   article-shape VERIFIER gate; a rung wins only by passing the verifier; markitdown is `.venv`-only,
   lazy + graceful degrade; honest "paste instead" failure) — is extracted in REAL TIME → grounded
   server-side via `news_ground.py` (ungrounded dropped) → the same arc. `/extract` streams NDJSON STAGE
   PROGRESS (fetching → converted[text → fills the textarea; pasted text wins over URL on re-run] →
   extracting → grounding → verifying i/N + elapsed; errors travel in-stream) read by the page via
   fetch+ReadableStream. **Optional LIVE mode spans Phase 35–41.** The live
   branch is build-time STRIPPED from the offline `dist/news` (zero network code there); the offline file
   stays the default + fallback. **Persistence + the feedback watchlist (Phase 36):** each live scan
   row-appends to a local DuckDB store (`scripts/news_store.py`, companion-only — build.py NEVER imports it;
   `data/news/.live/store.duckdb`, gitignored, → parquet export). The Disposition gate is the feedback loop:
   ESCALATE (`POST /disposition`) marks an entity, `GET /watchlist` returns book ∪ the escalated entities
   (reconciled + provenance), and the Screen step scores each new article against that GROWING surface — the
   watchlist is ESCALATED-ONLY (a curated surface, not every name). DuckDB is a `.venv`-only dep, never on
   the ship path; the watchlist/disposition client wiring is inside the stripped live region (offline
   `dist/news` byte-identical, screens the static book only). **Entity precision + watchlist view (Phase 38):**
   the extraction prompt carries a SUBJECTS-ONLY rule (extract perpetrators/designated parties/their companies,
   NOT announcing officials/prosecutors/agencies/courts — context shaping, the primary lever; a stress test
   proved an enumerated denylist overfits) backed by a keep-biased per-entity SECOND-PASS verify in
   `extract()` (`verify_entities`, on by default, `--no-verify-entities` off; fail-OPEN=KEEP, LIVE-only,
   layered ON TOP of the deterministic `build_record` the replay fixtures pin). The escalated watchlist is now
   VIEWABLE + prunable (`POST /watchlist/prune {name}` + a Select-screen panel). `news_ground.screen_entities`
   keeps the structural rules (source-line/judicial drops; since Phase 41 alias-dedup + adjacent-moniker
   FOLD into the parent's aliases — audit-trailed `folded_into` — orphan handles still drop). **Flag quality (Phase 40,
   measure-first):** the red_flags prompt contract carries a 20-family mechanism CHECKLIST (a coverage net incl.
   institutional-control-failure + misrepresentation families) + a granularity contract (one flag per distinct
   behaviour, retellings merge) + the [12,240] bounds (prompt/gate drift fixed) — measured against a BLIND
   second-rater reference as inter-rater agreement (consensus, never accuracy): holdout coverage-of-reference
   0.40→0.55, positional decay eliminated, federal layer unregressed; a per-flag precision verify was dropped
   (residue was recall) and sectioned extraction skipped (trigger didn't fire). The shared gate adds ONE
   measurement-earned rule: duplicate-flag collapse (same quote + same category, first survives) — DROP-mode in
   `ground_record` (live), CHECK-mode in `validate_news_data` (build, fail loud). **Entity resolution (Phase
   41):** the live scan is a resolution-grade identity record — entities carry `aliases[]` (verbatim) +
   `properties[]` {kind, value} (closed vocab incl. client_number/account_number — PRIVATE INVESTIGATION
   NOTES are a first-class future input); the record carries `relationships[]` {from,to,label,evidence}
   (closed vocab, labels vocab-checked never correctness-checked) + `main_subjects` (honest none/multiple).
   Vocab authority = `news_ground.PROPERTY_KINDS`/`RELATION_LABELS` (schema + prompt CONSTRUCT from them).
   Gate: aliases RAW-ground, property values NORMALIZE-ground (wrap/punct-tolerant, rejects derived forms —
   canonicalization post-gate only), relationship evidence RAW-grounds + referential integrity; everything
   grounded-or-stripped, shared live-DROP/build-CHECK. `red_flags` sit FIRST in EXTRACT_SCHEMA (measured:
   flags-last cost ~12.5% kept flags; flags-first restored 24→25 on the 3-article regression set). DuckDB
   normalizes to the ANCHOR design: anchors (exact-normalized name = identity spine; cross-scan
   ACCUMULATION; fuzzy merge deferred) + ONE monolithic property association table (per-row scan provenance,
   conflicting values BOTH kept never auto-resolved, confidence RESERVED/NULL) + relationship edges;
   `scans.source_type` (gov-enforcement/commercial-news/investigation-note). Screen matches name ∪ aliases
   (max pair score; single-token/@-handle aliases EXACT-normalized only, never fuzzy). Disposition shows the
   SUBJECT MAP (mains + evidence edges) + identity cards. PRIVACY boundary by CHECK: private data confined
   to the gitignored local store + 127.0.0.1 model; fixture promotion blocked by the US-federal
   `FIXTURE_META` allowlist assert. Recorded-fixture replay
   (`tests/fixtures/news-live/`, 13 real captured-Qwen outputs: 7 original incl. 3 promoted stress articles + 3
   `<id>.ph40.*` checklist-prompt re-captures + 3 `<id>.ph41.*` enriched-schema re-captures) pins the
   deterministic core offline; `tests/news_live_test.py
   --live` is an opt-in real-model smoke. See `docs/news-live.md`.

### Build (`scripts/build.py`)
Validates a config against the schema (fail-loud), resolves `text_file`→inline, inlines everything →
the single ship file. Targets: `<id>`, `corpus`, `news`, `all`; `--check <target>` is the drift
guard (frozen dists must be byte-identical). **build.py NEVER imports the authoring layer.** Baseline
preserved in `archive/`.

### Corpus sources & overlays (committed; merged at build time)
5 sources via the `CORPUS_SOURCES` registry in build.py (source-id → {status dir, derived dir,
doc_type}); each contributes a committed `corpus-status.json` (the extraction manifest from
`derive_signals.py --corpus-status`) + `derived/*.json`, merged by id into `__CORPUS__`, derived
shape validated at the build boundary:
- `data/fincen/` — FinCEN advisories · `data/fincen-alerts/` — FinCEN alerts · `data/ofac/` — OFAC ·
  `data/fintrac/` — FINTRAC OAs/Briefs · `data/fintrac-guidance/` — FINTRAC per-sector ML/TF
  indicator pages (doc_type "FINTRAC Guidance").
- Non-derivable (no enumerated red-flag list, honestly skipped): the 2 FATF advisories, BEC
  fin-2019-a005, FINTRAC crown-agents.

Three committed OVERLAYS, each validated at the build boundary (closed-vocab + referential integrity
against the live corpus; the grounding core is untouched — agent proposes, the gate disposes, the
human reviews):
- `data/typology-map.json` — doc-id → ONE typology (27-term closed vocab); jurisdiction is DERIVED
  from the source registry (FinCEN/OFAC = US, FINTRAC = Canada), not stored. It is the doc HEADLINE +
  the per-indicator INHERIT-DEFAULT.
- `data/indicator-typology-map.json` (Phase 37) — a SPARSE override mapping a LIVE indicator global-id
  (`<doc-id>/<ind-id>`) → one closed-vocab typology. Build-time, each indicator's typology = overlay
  value ELSE inherit its doc typology. This exists because a FINTRAC per-sector page is INHERENTLY
  MULTI-TYPOLOGY (bribery/corruption, TF, structuring, wires…): a doc→one-typology overlay forced 7 of
  the 10 sector pages into a catch-all. Now the deterministic corruption/TF section indicators (350,
  assigned by source SECTION heading — no neural) distribute into those real clusters; the genuinely
  cross-cutting remainder inherits the honest `cross-cutting-indicators` bucket. So the **Typologies
  lens + cross-corpus synthesis group by INDICATOR typology** (a doc appears in every cluster its
  indicators touch); `corruption` + `terrorist-financing` are now cross-jurisdiction US+Canada.
  Combined coverage stays honest union arithmetic over per-indicator statuses — no lift/dedup.
- `data/capability-taxonomy.json` — C1–C28 capabilities + D1–D20 data sources (code → {name, group,
  interview posture}). Powers the Capabilities + Data-sources lenses.

### Authoring pipeline (build-time ONLY — the ship file never fetches or calls an LLM)
`crawl_fincen.py` (discover a listing → committed manifest) → `acquire_fincen.py` (resolve each
doc's PDF, or `--html` for FINTRAC guidance) → `pdf_to_md.py` (markitdown PDF/HTML → committed
`<id>.md`, the derivation SURFACE & source of truth) → `derive_signals.py` (the deterministic GATE).
`derive_signals.py` is stdlib-only; only `markitdown` (convert) lives in a gitignored uv `.venv`. No
authoring tool is imported by the engine or build.py.

### The inverted extraction boundary (LOAD-BEARING — Phase 16/17)
**The LLM EXTRACTS, the deterministic layer GATES.** The old structural `extract_red_flags` is
DELETED. The LLM (a model session as backend, no key) reads `<id>.md` and EXTRACTS the red flags +
per-indicator judgment (status, data, build_rec, build_logic, the `red_flag` translation, C/D tags)
into `derived/<id>.json`. `derive_signals.py --check-derived` DISPOSES via `check_record`:
- **Quote-grounding** — every verbatim `flag` is a substring of the source md under `normalize()`
  (the traceability authority), inside the red-flag region `rf_region`.
- The cover×data matrix (`build_rec_category`); BUILD_NOW ⇒ a full build_logic definition.
- `red_flag` SHAPE check (present / non-empty / distinct-from-verbatim / 12–240 chars).

The LLM proposes (extraction included); the deterministic gate + the two human gates dispose. The
**two-layer model**: the grounded verbatim `flag` (the EVIDENCE) is shown BESIDE a natural-AML
`red_flag` TRANSLATION (the one neural step — mitigated by show-both + the always-on badge). The gate
checks each flag is FAITHFUL and (per-doc) that we got the list; it does NOT check the C/D tag is
correct — that dimension is verified separately (a grounding gate ≠ a completeness gate ≠ a
correctness gate).

### Coverage is GROUNDED, not fabricated
Each indicator's coverage (status / data / build_rec / build_logic) is DERIVED deterministically from
its C/D codes + the institution's 28+20 YES/NO/PARTIAL interview posture (the Phase-28 interview) via
the cover×data matrix + per-capability spec templates. Honest SOURCE_DATA where the bank can't
observe. NO fabricated coverage.

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
§105 public domain — the corpus's basis, applied to news). `book.json` is SYNTHETIC (non-negotiable
#4) — the bridge is REAL adverse-media entity × SYNTHETIC book, seeded with an exact true-positive,
near-matches an exact-name screen misses, and a common-name false-positive trap dismissed at the
gate. `validate_news_data` grounds every entity name + attribute + red-flag `flag` at the build
boundary (a LOCAL normalizer — build.py never imports the authoring layer).

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
- Build: `python3 scripts/build.py <id>` (or `corpus` / `news` / `all`) → the ship file.
  - `corpus` merges every source in `CORPUS_SOURCES` (the 5 `data/*` dirs) + the three overlays.
  - `news` reads `data/news/{articles,derived,book}`. Both are grounded/validated at the build boundary.
- Present: open `dist/<id>/index.html` (or `dist/corpus/index.html`, `dist/news/index.html`) — single
  self-contained file, offline, no server.
- News LIVE mode (Phase 35–41, optional, dev/authoring-time): start a local llama-cpp server, then
  `.venv/bin/python scripts/serve_news.py --llm-url <chat-endpoint> --model <name>` and open
  http://localhost:8000. Submit an article URL (one-shot: news_fetch ladder → standardize → verify →
  extract; the converted text fills the textarea for trim + re-run) or paste text + pick a source type
  (gov-enforcement/commercial-news/investigation-note); stage progress streams
  live (verify i/N + elapsed). Extraction is grounded server-side (ungrounded dropped) + entity-verified
  (subjects-only prompt + keep-biased second pass, on by default; `--no-verify-entities` off) + ER-enriched
  (aliases/properties/relationships/main subjects, all grounded-or-stripped; the Disposition subject map +
  identity cards render it; aliases join the screen surface); each scan
  persists to DuckDB (anchor accumulation by exact-normalized name) and the Disposition-gate ESCALATE grows
  the screen watchlist (viewable + prunable),
  run under `.venv` for persistence (`--export-parquet <dir>` exports; `--no-persist` disables) AND for
  URL mode (markitdown). The offline `dist/news` is unaffected (the live/persistence/view/progress/URL
  code is stripped from it). Details: `docs/news-live.md`.
- Drift guard before presenting: `python3 scripts/build.py --check all` (frozen dists byte-identical).
- Test (dep-free, no install — except the DuckDB store selftests, which run under `.venv`):
  - `node tests/corpus-explorer.test.mjs` — the story landing + the 6-screen per-doc arc + the
    multi-source menu (doc_type chips, FINTRAC footer attribution) + the 4 lenses + cross-corpus synthesis.
  - `node tests/news-stream.test.mjs` — the adverse-media arc + the fuzzy matcher (seeded matches,
    near-matches, the common-name trap dismissable at the gate); both motion modes; + the companion-served
    live overrides (book ∪ watchlist screen + the escalate gate + the Phase-38 watchlist VIEW/prune panel +
    the Phase-41 alias-aware matcher [exact-yes/fuzzy-no per alias class] + subject-map/identity-card render) +
    the offline-is-book-only strip assertion.
  - `python3 scripts/derive_signals.py --selftest` — the derivation GATE checks + anchor fixtures.
  - `python3 tests/news_live_test.py` — the live extraction pipeline (build_record + grounding incl. the
    duplicate-flag collapse, the recorded-fixture REPLAY [13 captured-Qwen outputs → goldens, no model,
    incl. 3 `.ph40` checklist-prompt + 3 `.ph41` enriched-schema re-captures, every base id asserted
    against the US-federal FIXTURE_META allowlist], the keep-biased second-pass verify,
    the `/extract` NDJSON stage-stream + one-shot URL routes [model + acquisition stubbed; stages precede the
    payload, errors in-stream, text wins over url] + `/watchlist/prune`; `--live` is an opt-in real-model
    smoke); under `.venv` it also drives `/watchlist` + `/disposition` + `/watchlist/prune` over a temp DuckDB
    store (the escalated-only loop) · `python3 scripts/news_ground.py --selftest` (the
    shared gate) · `python3 scripts/news_fetch.py --selftest` (URL acquisition: the standardizer pinned to a
    committed golden, the article-shape verifier, the interstitial detector, the ladder order incl.
    verifier-advances-the-ladder; under `.venv` also a real markitdown fixture conversion) ·
    `.venv/bin/python scripts/news_store.py --selftest` (DuckDB store: append → escalate →
    watchlist union → parquet roundtrip + anchor accumulation/conflict-keep/NULL-confidence/legacy
    migration) · `python3 scripts/serve_news.py --selftest` (the companion page).
  - Pre-present sequence: `--check all` (drift) → `node tests/…` (arcs) → walk `tests/smoke-checklist.md`.
- Authoring a new corpus source (build-time only; raw PDFs gitignored, the committed `<dir>/*.md` is
  the surface): `crawl_fincen.py [--alerts] --fetch`/`--write` → `acquire_fincen.py --source <dir>
  [--html] <id>` → `pdf_to_md.py --source <dir> <id>` → derive via the inverted loop →
  `derive_signals.py --corpus-status <dir>` to regenerate the manifest → rebuild.
- Iterate: edit `index.html` / `corpus.html` / `news.html` / a config, rebuild. `python3 -m
  http.server` optional, never required.

## Knowledge wiki
Domain reference comes from the registered **aml-wiki** (central store at
`/Users/jwang/private-knowledge/aml-wiki`) — AML typologies, red-flag indicators,
FINTRAC/FinCEN + OSFI E-23 references, the atom/composition vocabulary. A machine-local
symlink `wiki/ → aml-wiki` (gitignored) makes the harness auto-select it in this dir;
the SessionStart hook activates the knowledge-wiki framework from it.
- Query domain knowledge before guessing: `/wiki-query <question>` (auto-scopes to aml-wiki).
- AML insights worth keeping go back to aml-wiki via `/wiki-add` — it is the canonical home.
- For authoring a new typology, pull paraphrased advisory specifics + indicators from the wiki
  rather than inventing them — or, for a FinCEN advisory, run the M6 pipeline (acquire→convert) and
  derive from the verbatim markdown. Retrieval over parametric guessing.

## Aesthetic
Dark "dossier" theme, amber `--signal` (#f6a623) accent; fonts Newsreader / Archivo /
JetBrains Mono. Theme lives in `:root` CSS variables. Refined, not flashy.

## Milestones
M0 bootstrap · M1 config-driven refactor · M2 multi-typology · M3 presenter polish ·
M4 (skipped) live/pre-gen mode · M5 ship · M6 Signal Watch ingestion pipeline (FinCEN verbatim) ·
M7 corpus-backed demo (the corpus explorer `dist/corpus/`: the inverted derivation loop, 5 sources,
the 4 lenses, cross-corpus synthesis, grounded coverage) ·
M8 adverse-media / negative-news stream (`dist/news/`).
Per-phase detail: git log + `.dev-wiki/` journal + HANDOFF.md §8.

## Definition of done
Reliable offline · multi-typology from config · presenter controls · compliance-clean ·
README written. See HANDOFF.md §1.2.
