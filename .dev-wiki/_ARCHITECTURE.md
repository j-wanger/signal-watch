# Architecture: Signal Watch — AML Vision Demo

> Last updated: 2026-06-06 by /dev-debrief (Phase 21 SHIPPED — OFAC as corpus SOURCE #3: `data/ofac/` (3 OFAC advisory md + 3 derived), registered in `CORPUS_SOURCES` (doc_type "OFAC"). The rf_region anchors were WIDENED for OFAC vocab (`_RF_HEADER_OFAC` + `_RF_INTRO_OFAC` — Risk Indicators/Deceptive Practices/Risk Factors), the issuer parameterized (FinCEN/OFAC) — a regression-gated change to the previously byte-frozen correctness GATE (0 FinCEN rf_region shift; the grounding core `normalize`/`check_record` byte-untouched). The verbatim non-negotiable extended FinCEN-only → US-federal (17 USC §105; FINTRAC excluded). 36 publications, 32 derived live across 3 sources.)

## Directory Layout

signal-watch/
  index.html                      # generic engine template (`__CONFIG__` injection point; vanilla HTML/CSS/JS) — six-act showcase, BYTE-FROZEN
  corpus.html                     # Phase 13: standalone CORPUS EXPLORER template (`__CORPUS__` injection; OWN copy of theme CSS, staged flow). Phase 18: 5-screen arc (human gate + coverage close-the-loop)
  config/
    schema.md                     # content-model contract (incl. `advisory_full`)
    typologies/*.json             # per-typology content (fentanyl, trade-based, elder-financial-exploitation)
  scripts/
    build.py                      # stdlib: render_one (validate+inline = dist-bytes source of truth) + writer; --check drift guard; Phase 13: render/build/check_corpus + special "corpus" target (reads committed data, does NOT import derive_signals.py)
    acquire_fincen.py             # authoring-only: stdlib urllib fetch of a FinCEN advisory PDF. Phase 20: --source; Phase 21: _to_pdf_url treats an absolute /media/.../download or /system/files/ URL as a direct download (the OFAC form)
    pdf_to_md.py                  # authoring-only: markitdown PDF→markdown
    derive_signals.py             # authoring-only, STDLIB-ONLY (Phase 17: 1202→600): inverted loop — LLM extracts → gate disposes (quote-grounding `normalize(flag) ⊂ normalize(md)` + `rf_region` + `_rf_triage` counter); --corpus-status / --check-derived / --selftest. Phase 21: rf_region anchors WIDENED for OFAC vocab (`_RF_HEADER_OFAC`/`_RF_INTRO_OFAC`), issuer parameterized (FinCEN/OFAC) — regression-gated (0 FinCEN rf_region shift); the grounding core normalize/check_record byte-untouched. extract_red_flags + --scaffold/--draft/--scaffold-derived DELETED (Ph17)
  tests/
    corpus-explorer.test.mjs      # Phase 19: ZERO-DEP Node DOM-shim harness — reads the committed dist/corpus/index.html, drives the 5-screen arc (NO jsdom; file:// offline ethos). Phase 21 extended to 49 assertions (3-type menu + an OFAC doc walking the arc)
    fixtures/fincen-index.html    # saved advisory-listing fixture (crawl_fincen.py --selftest, Phase 10)
    fixtures/fincen-alerts.html   # saved alerts-hub fixture (crawl_fincen.py --alerts --selftest, Phase 20)
    smoke-checklist.md            # manual pre-present checklist (Phase 19 references the automated arc test)
  data/fincen/                    # Phase 20: the `fincen-advisories` SOURCE (one of N in the SOURCES registry) — BYTE-FROZEN
    raw/<advisory-id>.pdf         # acquired source PDF (authoring-only, gitignored)
    <advisory-id>.md              # verbatim advisory markdown = source of truth (FULL 14-advisory corpus committed as of Phase 12)
    index.json                    # discovered advisory manifest (Phase 10)
    corpus-status.json            # Phase 13: committed PER-SOURCE status manifest (id, advisory_no, title, source, status, flag_count, derivable) — emitted by derive_signals.py --corpus-status
    derived/<advisory-id>.json    # Phase 12: LLM-backend-derived + deterministically-checked record (NOT a ship config); drives the corpus explorer
  data/fincen-alerts/             # Phase 20: the `fincen-alerts` SOURCE #2 (same shape; FinCEN Alerts, still 17 USC §105 verbatim) — 19 alert md committed, 17 derived (6 in Ph20 + the 11-alert follow-on)
    raw/<alert-id>.pdf            # acquired alert PDF (authoring-only, GITIGNORED — md is the committed source of truth)
    <alert-id>.md                 # verbatim alert markdown (markitdown-converted from direct /system/files/...FinCEN Alert*.pdf)
    index.json                    # alert manifest ({id,title,date,type:"alert",url}) — from the FinCEN alerts hub
    corpus-status.json            # per-source status manifest (derive_signals.py --corpus-status <source-path>) — 19 docs, 17 derivable
    derived/<alert-id>.json       # LLM-extracted + gate-checked alert record (NOT a ship config) — 17 committed
  data/ofac/                      # Phase 21: the `ofac-advisories` SOURCE #3 (US Treasury OFAC, US-federal 17 USC §105 verbatim) — HAND-CURATED (OFAC's site is a JS SPA, no static crawl)
    raw/<id>.pdf                  # acquired OFAC PDF (authoring-only, GITIGNORED — md is the committed source of truth)
    <id>.md                       # verbatim OFAC advisory markdown (markitdown-converted from a direct /media/<id>/download PDF)
    index.json                    # HAND-AUTHORED OFAC manifest ({id,title,date,type,url=/media/<id>/download}) — no OFAC crawler
    corpus-status.json            # per-source status manifest (issuer=OFAC) — 3 docs, all derivable
    derived/<id>.json             # LLM-extracted + gate-checked OFAC record (NOT a ship config) — 3 committed (19 ind / 4 BUILD_NOW; maritime honestly SOURCE_DATA-heavy)
  dist/<typology>/index.html      # built self-contained ship files (per typology); BYTE-FROZEN by Phase 13
  dist/corpus/index.html          # Phase 13: built self-contained CORPUS EXPLORER ship file (committed)
  archive/                        # original baseline (equivalence reference)
  CLAUDE.md  README.md  HANDOFF.md # always-loaded non-negotiables / run / full context
  .dev-wiki/                      # lifecycle tracking (this wiki)

backend/ remains optional (HANDOFF §3.3); M4 live/pre-gen skipped (file:// trap). `tests/` is now a committed zero-dep harness (Phase 19) — node arc test + the manual smoke-checklist + a saved listing fixture.

## Module Responsibilities

| Module | Purpose | Key Entry Points | Inputs | Outputs |
|--------|---------|-----------------|--------|---------|
| index.html | Generic engine template: six-act scripted walkthrough; state machine + render dispatch + animations, all inline; `__CONFIG__` injection point. BYTE-FROZEN (Phase 13 adds a separate corpus artifact, never edits this) | `goto(0)` (bottom of `<script>`) | inlined CONFIG (per typology) + Google Fonts (online; degrades) | rendered DOM |
| corpus.html (Phase 13; Phase 18 arc) | Standalone CORPUS EXPLORER template: OWN copy of the dossier theme CSS (no shared include — showcase stays frozen) + `__CORPUS__` injection point + render JS for the staged 5-screen ARC (SELECT → COVERAGE → BUILD RECS/GATE → SIGNAL → CLOSE THE LOOP). Phase 18: BUILD_NOW rows are selectable div-toggles (the human gate — NOT `<input>`, so Space/arrow keyboard nav + determinism are preserved; per-advisory selection Set, default all-selected, reset on `pick()`); SIGNAL filters to the picks (selected ∩ BUILD_NOW w/ build_logic, honest empty state); CLOSE THE LOOP animates the existing `coverageIndex()` before→after with picked gaps flipped to covered (reduced-motion jumps to after; honest flat-hold for 0-BUILD_NOW). Coverage-only payoff — NO fabricated precision/lift. reduced-motion + keyboard parity; always-on illustrative badge; defensive rendering | the staged-flow entry (bottom of `<script>`) | inlined CORPUS data (corpus-status.json + derived records) | rendered DOM |
| scripts/build.py | `render_one(typ, template) -> str` (validate at boundary, fails loud + resolve `text_file`→inline + inject CONFIG + self-contained guard) is the SINGLE source of truth for a typology's dist bytes; a thin writer persists it; `check_one` byte-compares a fresh render against the committed dist (non-mutating, git-agnostic drift guard); `resolve_targets` shares `all`/`<id>` logic. Phase 13: `render_corpus`/`build_corpus`/`check_corpus` + special "corpus" target resolution + a corpus-data boundary validator (build_rec ∈ enum; BUILD_NOW ⇒ full build_logic shape). **Phase 20: `render_corpus` iterates a thin SOURCES registry (decouples source-id from storage dir), reads EACH source's corpus-status.json + derived/*.json, merges by id into one `__CORPUS__` (per-source shape validation at the boundary), tagging each record with its source type (Advisory / Alert)** — does NOT import derive_signals.py; `data/fincen/` stays byte-frozen (multi-source via the MERGE, not a migration) | `python3 scripts/build.py <id>` (or `all`); `--check [all\|<id>]`; `corpus` / `--check corpus` | config JSON + referenced `.md`; corpus: per-source corpus-status.json + derived/*.json + corpus.html | `dist/<id>/index.html`, `dist/corpus/index.html`; `--check`: per-target drift verdict + exit code |
| scripts/acquire_fincen.py, scripts/pdf_to_md.py | Authoring-only ingestion: fetch advisory PDF, convert to verbatim markdown | run manually at authoring | FinCEN advisory URL / raw PDF | `data/fincen/raw/*.pdf`, `data/fincen/*.md` |
| scripts/derive_signals.py | Authoring-only, **STDLIB-ONLY** (Phase 17: 1202→600, −50%; `os`+`anthropic` removed). **Phase 16 INVERTED the extraction boundary, Phase 17 did the real subtraction**: the LLM (a model session) EXTRACTS candidate red flags + per-indicator status/data + build recommendation + build logic; the deterministic layer is a GROUNDEDNESS GATE that disposes. Traceability authority = QUOTE-GROUNDING (`normalize(flag) ⊂ normalize(md)`, where `normalize` folds the closed FinCEN-md artifact set — running headers/form-feeds/hyphen-breaks/smart-quotes/whitespace — to one rule) + a coarse `rf_region()` section-cite relevance guard + a `_MIN_FLAG_NCHARS` floor. UNCHANGED dispose-logic: `build_rec_category` (cover×data matrix) + `check_record` matrix-consistency + BUILD_NOW⇒build_logic. `extract_red_flags` + the `--scaffold`/`--draft`/`--scaffold-derived` deterministic-scaffold + neural-draft authoring stack DELETED (dead under the inverted loop); its sole surviving job (triage flag-counts for the not-yet-derived chip) is now a ~14-line `_rf_triage(md, region)` counter reusing the `rf_region` span. `--selftest` is gate-only (hardcoded verbatim EFE fixture; Phase 19 adds a glued `_rf_triage` pin). The inverted loop is the SOLE derivation path; the LLM extracts + authors, the deterministic gate + the 2 human gates dispose. **Phase 20: the gate is source-AGNOSTIC + reused across sources; `--corpus-status` takes an optional source path. Phase 21: the rf_region RELEVANCE anchors WIDENED for OFAC heading vocab (`_RF_HEADER_OFAC`/`_RF_INTRO_OFAC` — Risk Indicators/Deceptive Practices/Risk Factors, ORed into the anchor check), the `corpus_status_records` issuer parameterized (FinCEN/OFAC, doubling-guarded → FinCEN output byte-identical). The grounding/traceability core (`normalize`/`check_record`) is byte-UNTOUCHED; the widening is regression-gated (0 FinCEN rf_region shift across all 33 FinCEN mds, 29 FinCEN records clean)** | `--selftest`; `--corpus`; `--corpus-status [<source-path>]`; `--check-derived <rec>` | `data/<source>/<id>.md` | `data/<source>/derived/<id>.json` (committed, gate-checked); `data/<source>/corpus-status.json` |

Inside `index.html`: content read from the injected CONFIG (`advisory_full` carries the verbatim
source); state `act`/`selected`/`confirmed`; `goto(i)`, `updateControls()`, nav `advance()`/`back()`/
`reset()`, `streamAdvisory()`, `esc()`, `act0()`…`act6()` dispatched via the `RENDER` array. M3 added
keyboard nav (←/→/Space/Esc/↺) + `prefers-reduced-motion`. Theme in `:root` CSS variables.

## Dependencies

| Package | Version | Role |
|---------|---------|------|
| (none, ship) | — | Ship artifact has no build/runtime deps. Google Fonts via `<link>`, degrades to system fonts offline. |
| markitdown[pdf] (MIT) | authoring-only | PDF→markdown converter. Confined to `scripts/`, runs in a gitignored uv-managed py3.12 `.venv` (homebrew py3.14 `pyexpat` is broken). NEVER in the ship file. |
| anthropic | GONE (Phase 17) | Was `derive_signals.py --draft` only (lazy). The `--draft`/`--scaffold` authoring stack was DELETED under the inverted loop (the model SESSION is the backend, no API key); derive_signals.py no longer imports it (now stdlib-only). Phase 19 confirmed the "stale pin" is DEAD — `requirements-authoring.txt` does not exist (Ph17's deletion already took it). The ship artifact never called an LLM. |

## Authoring Pipeline (M6 — build-time only, NEVER in the ship artifact)

| Step | Tool | Reads | Writes | Notes |
|------|------|-------|--------|-------|
| acquire | `scripts/acquire_fincen.py` (stdlib `urllib`, online) | FinCEN advisory URL | `data/fincen/raw/<advisory-id>.pdf` | authoring-only; NO runtime fetch in ship file |
| convert | `scripts/pdf_to_md.py` → markitdown (MIT) | raw PDF | `data/fincen/<advisory-id>.md` (verbatim, source of truth) | runs in gitignored uv `.venv` (py3.12); de-risk GATE on quality |
| derive | `scripts/derive_signals.py` (STDLIB-ONLY) → human review | `data/fincen/<advisory-id>.md` | `data/fincen/derived/<id>.json` (committed, gate-checked) | INVERTED loop: the LLM (a model session, no API key) EXTRACTS red flags + per-indicator judgment + build rec + build logic; the deterministic GROUNDEDNESS GATE (`--check-derived`: quote-grounding + `rf_region` + cover×data matrix + BUILD_NOW⇒build_logic) DISPOSES. `--corpus-status` emits the manifest. The LLM proposes (extraction too); the gate + the two human gates DISPOSE. (The old `--scaffold`/`--draft` config-draft path is DELETED.) |
| build | `scripts/build.py` (stdlib, system python) | config JSON (+ referenced `.md`) | `dist/<typology>/index.html` (inlined, self-contained) | validates `advisory_full` at the boundary; resolves `text_file`→inline so the md stays single source of truth. `--check` re-renders in memory + byte-compares vs committed dist (zero-drift guard, non-mutating) — wired into the smoke-checklist |

Naming convention is split: the corpus is **document-id-named** (`data/fincen/fin-2022-a002.md`,
`data/fincen-alerts/<alert-id>.md`) while the typology config is **typology-named**
(`config/typologies/elder-financial-exploitation.json`) — separates the source-document corpus from
derived typologies. Phase 20 generalizes this to MULTIPLE SOURCES: a thin SOURCES registry decouples
source-id from storage dir (`fincen-advisories` → `data/fincen/`, `fincen-alerts` → `data/fincen-alerts/`,
Phase 21 `ofac-advisories` → `data/ofac/` — not a plugin framework). `data/fincen/` + `data/fincen-alerts/`
stay byte-frozen; multi-source is proven via the MERGE in `render_corpus`, not a rename/migration. Still
17 USC §105 verbatim, but Phase 21 EXTENDED the verbatim non-negotiable FinCEN-only → US-federal (covers
FinCEN + OFAC, both US Treasury; FINTRAC excluded — Canadian Crown copyright) and WIDENED the rf_region
anchors (regression-gated) for OFAC's non-red-flag-template heading vocab.

The split is load-bearing: acquire/convert/derive run at authoring; their output is persisted to
`data/fincen/` + `config/` and INLINED by `build.py`. The ship artifact stays single-file, offline,
zero runtime deps, no `fetch` (HANDOFF §4 / §4.5). US-FEDERAL government text (FinCEN + OFAC) is verbatim
public domain (17 USC §105, attributed) — the relaxation of the paraphrase rule, extended FinCEN-only →
US-federal in Phase 21; does NOT extend to FINTRAC (Crown copyright) or any non-US/non-government source.

## Data Flow

| Module | Reads (data) | Writes (data) | Env Vars | Notes |
|--------|-------------|---------------|----------|-------|
| demo | inlined CONFIG (synthetic figures, illustrative) + `advisory_full` (verbatim FinCEN, public domain) | DOM | — | No customer/transaction data, ever. Verbatim gov text kept visually separate from the illustrative badge |
| authoring pipeline | FinCEN advisory PDF (public source) | `data/fincen/raw/*.pdf`, `data/fincen/*.md` | — | build-time only; output never fetched at runtime |

## Development Toolchain

| Category | Tool | Config Path | Status |
|----------|------|-------------|--------|
| Build System | scripts/build.py (stdlib; validates config + inlines → dist/<id>/index.html; `--check` zero-drift guard) | scripts/build.py | detected |
| Authoring deps | markitdown[pdf] (MIT, convert only) in a uv-managed py3.12 .venv (gitignored); `anthropic` GONE since Phase 17 (derive_signals.py stdlib-only); no `requirements-authoring.txt` on disk (Ph17's deletion took it — confirmed Phase 19) | gitignored uv `.venv` | detected (authoring-only) |
| Test harness | node (system) — `tests/corpus-explorer.test.mjs` zero-dep DOM-shim arc test (Phase 19); `derive_signals.py --selftest`; `build.py --check all` drift guard | tests/corpus-explorer.test.mjs | detected (Phase 19) |
| Dev Server | python3 -m http.server (optional, iteration only) | — | optional (never required) |
| Version Control | git | .git/ | detected |

## Related

- HANDOFF.md (§3 target shape, §5 content model) · CLAUDE.md (non-negotiables)
