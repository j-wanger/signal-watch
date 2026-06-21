# Architecture: Signal Watch — AML Vision Demo

> Last updated 2026-06-21 (Phase 63 debrief — Development Toolchain test-harness row trued up: the 8-target build + the new companion case-workbench arc test + the pytest umbrella). Per-phase architecture narrative archived to [articles/state-archive-architecture-header.md](articles/state-archive-architecture-header.md) + the journals; this file is the durable structure snapshot only.
>
> [Phases 24–27 carry] Cross-corpus synthesis (`data/typology-map.json` overlay + build-boundary gate + the Documents/Typologies toggle, honest union coverage, NO similarity/overlap/lift) · the two-layer red-flag model (grounded verbatim `flag` + register `red_flag`) · per-doc Read-advisory screen · `cleanArticle` + normalize-both-sides highlighting — corpus.html + derived-record VALUE changes; the grounding core byte-frozen throughout.

## Directory Layout (compact — full annotated tree in the archive article)

    index.html / corpus.html / news.html / console.html   # the 4 ship templates (one injection point each)
    config/{schema.md, typologies/*.json}     # showcase content model + per-typology content
    scripts/                                  # build.py · news_{ground,store,fetch}.py · serve_news.py ·
                                              #   serve_corpus.py (Phase 46) · derive_signals.py ·
                                              #   crawl/acquire/pdf_to_md (authoring)
    tests/                                    # corpus-explorer + news-stream node harnesses ·
                                              #   news_live_test.py · news_quality_harness.py (Phase 44) ·
                                              #   fixtures/news-live/ (replay captures + quality-baseline.json)
    data/{fincen,fincen-alerts,ofac,fintrac,fintrac-guidance}/   # 5 corpus sources: committed <id>.md +
                                              #   corpus-status.json + derived/*.json (raw PDFs gitignored)
    data/{typology-map,indicator-typology-map,capability-taxonomy}.json   # the 3 committed overlays
    data/news/{articles,derived,book.json}    # M8 news data (US-federal verbatim; synthetic book)
    data/console/cases.json                   # Phase 47: 213 C/D adjudication cases (Phase-34 pairs)
    dist/{<id>,corpus,news,console}/          # committed byte-frozen ship artifacts (6 --check targets)
    data/probe-history/ + scripts/probe_history_stats.py    # Phase 48 SYNTHETIC probe (outside build.py)
    docs/ archive/ specs/ .dev-wiki/          # live-mode docs · program-blueprint.md §1–§15 (M9 design source-of-truth) · blueprint-report.html (non-ship) + probe-history.md · baseline · specs · wiki

## Module Responsibilities

| Module | Purpose | Key Entry Points | Inputs | Outputs |
|--------|---------|-----------------|--------|---------|
| index.html | Generic engine template: six-act scripted walkthrough; state machine + render dispatch + animations, all inline; `__CONFIG__` injection point. BYTE-FROZEN (Phase 13 adds a separate corpus artifact, never edits this) | `goto(0)` (bottom of `<script>`) | inlined CONFIG (per typology) + Google Fonts (online; degrades) | rendered DOM |
| corpus.html (Phase 13; Phase 18 arc) | Standalone CORPUS EXPLORER template: OWN copy of the dossier theme CSS (no shared include — showcase stays frozen) + `__CORPUS__` injection point + render JS for the staged 5-screen ARC (SELECT → COVERAGE → BUILD RECS/GATE → SIGNAL → CLOSE THE LOOP). Phase 18: BUILD_NOW rows are selectable div-toggles (the human gate — NOT `<input>`, so Space/arrow keyboard nav + determinism are preserved; per-advisory selection Set, default all-selected, reset on `pick()`); SIGNAL filters to the picks (selected ∩ BUILD_NOW w/ build_logic, honest empty state); CLOSE THE LOOP animates the existing `coverageIndex()` before→after with picked gaps flipped to covered (reduced-motion jumps to after; honest flat-hold for 0-BUILD_NOW). Coverage-only payoff — NO fabricated precision/lift. **Phase 24: a Documents/Typologies toggle on Select (`selMode`, default 'doc' → doc-mode byte-identical) + the cross-corpus SYNTHESIS view (`clusters()`/`typoCard`/`renderSynthesis`, `view='synthesis'` + `currentTypology`/`fromTypology` + `enterSynthesis`/`pick(id,from)`): group-by-typology → a cross-jurisdiction cluster + honest COMBINED coverage (pooled `coverageIndex` over the UNION of every regulator's flags) + per-jurisdiction counts → drill-through to the per-doc arc. NO similarity/overlap/lift number; a framenote discloses "NOT de-duplicated or matched across regulators" — additive, the per-doc arc unchanged**. **Phase 29: a THIRD Select mode (`selMode='capability'`) + the CAPABILITY LENS (`view='capability'` + `currentCapability`/`fromCapability` + `capAgg`/`indsForCap`/`postureChip`/`covSeg`/`capCard`/`renderCapability`/`enterCapability`): a card per demanded capability (posture chip + honest demand count + a covered/partial/gap micro-bar, gap-sorted) → drill into its pooled cross-regulator indicators (grouped by source doc + a "Depends on data" data-source row) → the per-doc arc, Back returns to the capability (mirrors `fromTypology`). Pure RE-PROJECTION of the inlined per-indicator capability/data_source codes + the `taxonomy` overlay — NO fabricated/overlap number; additive, the per-doc arc unchanged**. reduced-motion + keyboard parity; always-on illustrative badge; defensive rendering | the staged-flow entry (bottom of `<script>`) | inlined CORPUS data (corpus-status.json + derived records + typology/jurisdiction + capability-taxonomy overlay) | rendered DOM |
| scripts/build.py | `render_one(typ, template) -> str` (validate at boundary, fails loud + resolve `text_file`→inline + inject CONFIG + self-contained guard) is the SINGLE source of truth for a typology's dist bytes; a thin writer persists it; `check_one` byte-compares a fresh render against the committed dist (non-mutating, git-agnostic drift guard); `resolve_targets` shares `all`/`<id>` logic. Phase 13: `render_corpus`/`build_corpus`/`check_corpus` + special "corpus" target resolution + a corpus-data boundary validator (build_rec ∈ enum; BUILD_NOW ⇒ full build_logic shape). **Phase 20: `render_corpus` iterates a thin SOURCES registry (decouples source-id from storage dir), reads EACH source's corpus-status.json + derived/*.json, merges by id into one `__CORPUS__` (per-source shape validation at the boundary), tagging each record with its source type (Advisory / Alert / OFAC / FINTRAC)** — does NOT import derive_signals.py; the pre-existing sources stay byte-frozen (multi-source via the MERGE, not a migration; Phase 22 registered `fintrac-advisories` as source #4). **Phase 24: each CORPUS_SOURCES entry carries a `jurisdiction` (US for FinCEN/OFAC, Canada for FINTRAC) projected into every merged entry; `load_typology_map` (shape gate) + `validate_typology` (the build-boundary GATE: closed vocab + referential integrity + total live-doc coverage, fail-loud) read `data/typology-map.json` and attach a `typology` to each derived entry + inject the typology vocab into `__CORPUS__` — first structural build.py touch since Phase 20. **Phase 29: `load_capability_taxonomy` (shape gate) + `validate_capability_taxonomy` (the build-boundary GATE: shape + posture ∈ {y,n,partial} via a `POSTURE` constant + closed-vocab referential integrity against all indicator `capability`/`data_source` codes across the records, fail-loud) read `data/capability-taxonomy.json` (path `CAPABILITY_TAXONOMY`) and inline it into `__CORPUS__` as `taxonomy`; the per-indicator codes already merged via `_load_source`**. **Phase 33: a 5th CORPUS_SOURCES entry `fintrac-guidance` (doc_type "FINTRAC Guidance", jurisdiction Canada) — ADDITIVE, existing target code paths untouched; corpus 875→2,251 indicators / 42→56 records / 4→5 sources**. **Phase 47: `load_console_cases`/`validate_console_cases` (fail-loud: every case's quoted flag a substring of its named CURRENT committed derived record by id; adjudicated codes 213/213 re-verified at build — regeneration drift fails loudly; FINTRAC rows carry manifest-byte-matched attribution) + the `console` target (console.html + `__CASES__` → dist/console) wired into `all`/`--check` — 6 artifacts checked** | `python3 scripts/build.py <id>` (or `all`); `--check [all\|<id>]`; `corpus` / `--check corpus` / `console` | config JSON + referenced `.md`; corpus: per-source corpus-status.json + derived/*.json + `data/typology-map.json` + `data/capability-taxonomy.json` + corpus.html | `dist/<id>/index.html`, `dist/corpus/index.html`; `--check`: per-target drift verdict + exit code |
| scripts/acquire_fincen.py, scripts/pdf_to_md.py | Authoring-only ingestion: fetch advisory PDF, convert to verbatim markdown | run manually at authoring | FinCEN advisory URL / raw PDF | `data/fincen/raw/*.pdf`, `data/fincen/*.md` |
| scripts/derive_signals.py | Authoring-only, **STDLIB-ONLY** (Phase 17: 1202→600, −50%; `os`+`anthropic` removed). **Phase 16 INVERTED the extraction boundary, Phase 17 did the real subtraction**: the LLM (a model session) EXTRACTS candidate red flags + per-indicator status/data + build recommendation + build logic; the deterministic layer is a GROUNDEDNESS GATE that disposes. Traceability authority = QUOTE-GROUNDING (`normalize(flag) ⊂ normalize(md)`, where `normalize` folds the closed FinCEN-md artifact set — running headers/form-feeds/hyphen-breaks/smart-quotes/whitespace — to one rule) + a coarse `rf_region()` section-cite relevance guard + a `_MIN_FLAG_NCHARS` floor. UNCHANGED dispose-logic: `build_rec_category` (cover×data matrix) + `check_record` matrix-consistency + BUILD_NOW⇒build_logic. `extract_red_flags` + the `--scaffold`/`--draft`/`--scaffold-derived` deterministic-scaffold + neural-draft authoring stack DELETED (dead under the inverted loop); its sole surviving job (triage flag-counts for the not-yet-derived chip) is now a ~14-line `_rf_triage(md, region)` counter reusing the `rf_region` span. `--selftest` is gate-only (hardcoded verbatim EFE fixture; Phase 19 adds a glued `_rf_triage` pin). The inverted loop is the SOLE derivation path; the LLM extracts + authors, the deterministic gate + the 2 human gates dispose. **Phase 20: the gate is source-AGNOSTIC + reused across sources; `--corpus-status` takes an optional source path. Phase 21: the rf_region RELEVANCE anchors WIDENED for OFAC heading vocab (`_RF_HEADER_OFAC`/`_RF_INTRO_OFAC` — Risk Indicators/Deceptive Practices/Risk Factors, ORed into the anchor check), the `corpus_status_records` issuer parameterized (FinCEN/OFAC, doubling-guarded → FinCEN output byte-identical). The grounding/traceability core (`normalize`/`check_record`) is byte-UNTOUCHED; the widening is regression-gated (0 FinCEN rf_region shift across all 33 FinCEN mds, 29 FinCEN records clean)** | `--selftest`; `--corpus`; `--corpus-status [<source-path>]`; `--check-derived <rec>` | `data/<source>/<id>.md` | `data/<source>/derived/<id>.json` (committed, gate-checked); `data/<source>/corpus-status.json` |

Inside `index.html`: state machine + `RENDER`-array act dispatch off the injected CONFIG; M3 keyboard
nav + `prefers-reduced-motion`; theme in `:root` CSS variables. **console.html (Phase 47, 4th
artifact):** dossier-theme single file off injected `__CASES__` — Queue (grouped by changed axis;
consensus-not-ground-truth framing) → Evidence (verbatim flag + `red_flag`, neutral Assessment A/B) →
Disposition (graded 4-way, rationale REQUIRED) → Record reveal → session-only Ledger (copy-out; persists nothing; no LLM/fetch).

## Dependencies

| Package | Version | Role |
|---------|---------|------|
| (none, ship) | — | Ship artifact has no build/runtime deps. Google Fonts via `<link>`, degrades to system fonts offline. |
| markitdown[pdf] (MIT) | authoring-only | PDF→markdown converter. Confined to `scripts/`, runs in a gitignored uv-managed py3.12 `.venv` (homebrew py3.14 `pyexpat` is broken). NEVER in the ship file. |
| anthropic | GONE (Phase 17) | Was `derive_signals.py --draft` only (lazy). The `--draft`/`--scaffold` authoring stack was DELETED under the inverted loop (the model SESSION is the backend, no API key); derive_signals.py no longer imports it (now stdlib-only). Phase 19 confirmed the "stale pin" is DEAD — `requirements-authoring.txt` does not exist (Ph17's deletion already took it). The ship artifact never called an LLM. |
| duckdb (1.5.3, MIT) | Phase 36, .venv-only | News-stream LIVE-mode persistence store (`scripts/news_store.py`). Confined to the gitignored uv `.venv` (where markitdown lives); NEVER imported by `build.py` and NEVER inlined into any dist (the self-contained, offline, no-fetch non-negotiable holds). The store file + parquet exports are gitignored (`data/news/.live/`, `*.duckdb`, `*.parquet`). |

**News-stream LIVE backbone (Phase 35–44, companion/dev-time only — the offline `dist/news` is byte-identical).**
Same-origin stdlib companion `scripts/serve_news.py` (serves `news.html` + proxies local llama-cpp; routes
`/health` · `/extract` {url|text} → ALWAYS an NDJSON stage stream (`extract(on_progress=None)` = the replay-fixture
seam; STREAMING `call_llm`: SSE idle-gap timeout, budget 16384, failures NAMED in-stream, preflight n_ctx refusal,
single-flight 409) · `/watchlist[/prune]` · `/disposition` · `/anchor?name=` (wraps `news_store.anchor_summary()`;
400/503/404/200)). Companion-only `scripts/news_fetch.py` (fetch ladder urllib→curl→markitdown + standardizer +
article-shape verifier). Grounding = shared stdlib `scripts/news_ground.py` (`ground_record` DROP-mode; Phase-44
wrap-tolerant `locate_span` REQUOTE; ambiguity-refusing/type-matched folds), reused by BOTH the companion AND
build.py's `validate_news_data` gate. `scripts/news_store.py` OWNS DuckDB (anchors/scans/dispositions; parquet
export; build.py NEVER imports it). ALL client live code in `/*LIVE_START*/…/*LIVE_END*/`, stripped by
`render_news` → zero network code ships. Quality gate: `tests/news_quality_harness.py` + `quality-baseline.json`
(17-fixture deterministic regression gate, 5 dimensions incl. alias-ownership; `--freeze` = conscious re-baseline).

**Corpus LIVE derivation backbone (Phase 46, companion/dev-time only — the offline `dist/corpus` is byte-identical).**
The SECOND live companion `scripts/serve_corpus.py` (stdlib, port 8010): a local model derives a PASTED advisory md
(spec deterministic from the taxonomy + 3 FINTRAC few-shots; streaming strict-schema `call_llm`) through the imported
FROZEN `derive_signals.check_record` gate — ONE violation-guided retry then grounded-or-dropped; staged NDJSON
`/derive` (single-flight 409, NOTHING persisted). T1 probe: direct + retry CHOSEN over opencode (17/17 identical,
3.1× wall, the iterate loop never engaged). corpus.html's live code in its own `/*LIVE_*/` region, stripped by
`render_corpus`; live-derived docs session-only, UNREVIEWED, DISPLAY/PROPOSE-only. `serve_corpus.corpus_payload()`
duplicates `render_corpus`'s merge (parity-guarded; `build.corpus_payload()` factoring named). Doc: `docs/corpus-live.md`.

## Authoring Pipeline (compact — full narrative in the archive article + CLAUDE.md)

crawl_fincen.py (manifest) → acquire_fincen.py (PDF/HTML, gitignored raw) → pdf_to_md.py (committed
<id>.md = the derivation surface) → the INVERTED loop: the LLM extracts derived/<id>.json, the
deterministic gate disposes (derive_signals.py --check-derived). scripts/curate_console_cases.py
(Phase 47): deterministic regeneration-only curation of data/console/cases.json from the Phase-34
git history. No authoring tool is imported by the engine; news_ground = the ONE allowed build→companion import.

## Data Flow

| Module | Reads (data) | Writes (data) | Env Vars | Notes |
|--------|-------------|---------------|----------|-------|
| demo | inlined CONFIG (synthetic figures, illustrative) + `advisory_full` (verbatim FinCEN, public domain) | DOM | — | No customer/transaction data, ever. Verbatim gov text kept visually separate from the illustrative badge |
| authoring pipeline | FinCEN advisory PDF (public source) | `data/fincen/raw/*.pdf`, `data/fincen/*.md` | — | build-time only; output never fetched at runtime |

## Development Toolchain

| Category | Tool | Config Path | Status |
|----------|------|-------------|--------|
| Build System | scripts/build.py (stdlib; validates config + inlines → dist/<id>/index.html; `--check` zero-drift guard) | scripts/build.py | detected |
| Authoring/companion deps | markitdown[pdf] (MIT, convert only) + duckdb (1.5.3, MIT — Phase 36 news-store, companion-only) in a uv-managed py3.12 .venv (gitignored); `anthropic` GONE since Phase 17 (derive_signals.py stdlib-only); no `requirements-authoring.txt` on disk (Ph17's deletion took it — confirmed Phase 19) | gitignored uv `.venv` | detected (authoring/companion-only) |
| Test harness | node (system) — `tests/corpus-explorer.test.mjs` + `tests/news-stream.test.mjs` (150) + `tests/gate-console.test.mjs` (68) + `tests/triage-console.test.mjs` (93) + `tests/chain.test.mjs` + `tests/launcher.test.mjs` (23) + `tests/workbench.test.mjs` (Phase 63, 61 assertions — the companion case-workbench arc) zero-dep DOM-shim arc tests; `tests/news_quality_harness.py --check` (Phase 44 quality-regression gate vs the committed baseline); `derive_signals.py --selftest`; `scripts/{news_ground,serve_news,serve_corpus,news_store,news_fetch,serve_chain,serve_workbench,curate_workbench_cases}.py --selftest`; `tests/news_live_test.py` (recorded-fixture replay, model stubbed; `--live` opt-in); `build.py --check all` 8-target drift guard (3 typologies + corpus + news + console + triage + launcher; the chain/workbench companions are NOT build targets). **Phase 63 pytest umbrella:** `pyproject.toml` ([tool.uv] package=false, pytest dev-only) + `tests/test_selftests.py` (17 parametrized cases shelling out to each `scripts/*.py --selftest` + `node tests/*.test.mjs`) → `uv run pytest` runs the whole suite while the dep-free paths stay the source of truth | tests/*.test.mjs, tests/test_selftests.py, tests/news_live_test.py | detected |
| Dev Server | python3 -m http.server (optional, iteration only) | — | optional (never required) |
| Version Control | git | .git/ | detected |

## Related

- HANDOFF.md (§3 target shape, §5 content model) · CLAUDE.md (non-negotiables)
