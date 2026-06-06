# Architecture: Signal Watch — AML Vision Demo

> Last updated: 2026-06-06 by /dev-debrief (Phase 17 — deleted extract_red_flags + the scaffold/draft authoring stack; derive_signals.py 1202→600, stdlib-only; inverted loop the sole derivation path)

## Directory Layout

signal-watch/
  index.html                      # generic engine template (`__CONFIG__` injection point; vanilla HTML/CSS/JS) — six-act showcase, BYTE-FROZEN
  corpus.html                     # Phase 13: standalone CORPUS EXPLORER template (`__CORPUS__` injection; OWN copy of theme CSS, staged flow). Phase 18: 5-screen arc (human gate + coverage close-the-loop)
  config/
    schema.md                     # content-model contract (incl. `advisory_full`)
    typologies/*.json             # per-typology content (fentanyl, trade-based, elder-financial-exploitation)
  scripts/
    build.py                      # stdlib: render_one (validate+inline = dist-bytes source of truth) + writer; --check drift guard; Phase 13: render/build/check_corpus + special "corpus" target (reads committed data, does NOT import derive_signals.py)
    acquire_fincen.py             # authoring-only: stdlib urllib fetch of a FinCEN advisory PDF
    pdf_to_md.py                  # authoring-only: markitdown PDF→markdown
    derive_signals.py             # authoring-only, STDLIB-ONLY (Phase 17: 1202→600): inverted loop — LLM extracts → gate disposes (quote-grounding `normalize(flag) ⊂ normalize(md)` + `rf_region` + `_rf_triage` counter); --corpus-status / --check-derived / --selftest (gate-only). extract_red_flags + the --scaffold/--draft/--scaffold-derived stack DELETED
    requirements-authoring.txt    # authoring deps (markitdown[pdf], convert only) — uv `.venv`, gitignored
  data/fincen/
    raw/<advisory-id>.pdf         # acquired source PDF (authoring-only, gitignored)
    <advisory-id>.md              # verbatim advisory markdown = source of truth (FULL 14-advisory corpus committed as of Phase 12)
    index.json                    # discovered advisory manifest (Phase 10)
    corpus-status.json            # Phase 13: committed per-advisory status manifest (id, advisory_no, title, source, status, flag_count, derivable) — emitted by derive_signals.py --corpus-status
    derived/<advisory-id>.json    # Phase 12: LLM-backend-derived + deterministically-checked record (NOT a ship config); drives the corpus explorer
  dist/<typology>/index.html      # built self-contained ship files (per typology); BYTE-FROZEN by Phase 13
  dist/corpus/index.html          # Phase 13: built self-contained CORPUS EXPLORER ship file (committed)
  archive/                        # original baseline (equivalence reference)
  CLAUDE.md  README.md  HANDOFF.md # always-loaded non-negotiables / run / full context
  .dev-wiki/                      # lifecycle tracking (this wiki)

backend/ + tests/ remain optional (HANDOFF §3.3); M4 live/pre-gen skipped (file:// trap).

## Module Responsibilities

| Module | Purpose | Key Entry Points | Inputs | Outputs |
|--------|---------|-----------------|--------|---------|
| index.html | Generic engine template: six-act scripted walkthrough; state machine + render dispatch + animations, all inline; `__CONFIG__` injection point. BYTE-FROZEN (Phase 13 adds a separate corpus artifact, never edits this) | `goto(0)` (bottom of `<script>`) | inlined CONFIG (per typology) + Google Fonts (online; degrades) | rendered DOM |
| corpus.html (Phase 13; Phase 18 arc) | Standalone CORPUS EXPLORER template: OWN copy of the dossier theme CSS (no shared include — showcase stays frozen) + `__CORPUS__` injection point + render JS for the staged 5-screen ARC (SELECT → COVERAGE → BUILD RECS/GATE → SIGNAL → CLOSE THE LOOP). Phase 18: BUILD_NOW rows are selectable div-toggles (the human gate — NOT `<input>`, so Space/arrow keyboard nav + determinism are preserved; per-advisory selection Set, default all-selected, reset on `pick()`); SIGNAL filters to the picks (selected ∩ BUILD_NOW w/ build_logic, honest empty state); CLOSE THE LOOP animates the existing `coverageIndex()` before→after with picked gaps flipped to covered (reduced-motion jumps to after; honest flat-hold for 0-BUILD_NOW). Coverage-only payoff — NO fabricated precision/lift. reduced-motion + keyboard parity; always-on illustrative badge; defensive rendering | the staged-flow entry (bottom of `<script>`) | inlined CORPUS data (corpus-status.json + derived records) | rendered DOM |
| scripts/build.py | `render_one(typ, template) -> str` (validate at boundary, fails loud + resolve `text_file`→inline + inject CONFIG + self-contained guard) is the SINGLE source of truth for a typology's dist bytes; a thin writer persists it; `check_one` byte-compares a fresh render against the committed dist (non-mutating, git-agnostic drift guard); `resolve_targets` shares `all`/`<id>` logic. Phase 13: `render_corpus`/`build_corpus`/`check_corpus` + special "corpus" target resolution + a corpus-data boundary validator (build_rec ∈ enum; BUILD_NOW ⇒ full build_logic shape); assembles `__CORPUS__` from committed corpus-status.json + derived/*.json — does NOT import derive_signals.py | `python3 scripts/build.py <id>` (or `all`); `--check [all\|<id>]`; `corpus` / `--check corpus` | config JSON + referenced `.md`; corpus: corpus-status.json + derived/*.json + corpus.html | `dist/<id>/index.html`, `dist/corpus/index.html`; `--check`: per-target drift verdict + exit code |
| scripts/acquire_fincen.py, scripts/pdf_to_md.py | Authoring-only ingestion: fetch advisory PDF, convert to verbatim markdown | run manually at authoring | FinCEN advisory URL / raw PDF | `data/fincen/raw/*.pdf`, `data/fincen/*.md` |
| scripts/derive_signals.py | Authoring-only, **STDLIB-ONLY** (Phase 17: 1202→600, −50%; `os`+`anthropic` removed). **Phase 16 INVERTED the extraction boundary, Phase 17 did the real subtraction**: the LLM (a model session) EXTRACTS candidate red flags + per-indicator status/data + build recommendation + build logic; the deterministic layer is a GROUNDEDNESS GATE that disposes. Traceability authority = QUOTE-GROUNDING (`normalize(flag) ⊂ normalize(md)`, where `normalize` folds the closed FinCEN-md artifact set — running headers/form-feeds/hyphen-breaks/smart-quotes/whitespace — to one rule) + a coarse `rf_region()` section-cite relevance guard + a `_MIN_FLAG_NCHARS` floor. UNCHANGED dispose-logic: `build_rec_category` (cover×data matrix) + `check_record` matrix-consistency + BUILD_NOW⇒build_logic. `extract_red_flags` + the `--scaffold`/`--draft`/`--scaffold-derived` deterministic-scaffold + neural-draft authoring stack DELETED (dead under the inverted loop); its sole surviving job (triage flag-counts for the not-yet-derived chip) is now a ~14-line `_rf_triage(md, region)` counter reusing the `rf_region` span. `--selftest` is gate-only (hardcoded verbatim EFE fixture). The inverted loop is the SOLE derivation path; the LLM extracts + authors, the deterministic gate + the 2 human gates dispose | `--selftest`; `--corpus`; `--corpus-status`; `--check-derived <rec>` | `data/fincen/<id>.md` | `data/fincen/derived/<id>.json` (committed, gate-checked); `data/fincen/corpus-status.json` |

Inside `index.html`: content read from the injected CONFIG (`advisory_full` carries the verbatim
source); state `act`/`selected`/`confirmed`; `goto(i)`, `updateControls()`, nav `advance()`/`back()`/
`reset()`, `streamAdvisory()`, `esc()`, `act0()`…`act6()` dispatched via the `RENDER` array. M3 added
keyboard nav (←/→/Space/Esc/↺) + `prefers-reduced-motion`. Theme in `:root` CSS variables.

## Dependencies

| Package | Version | Role |
|---------|---------|------|
| (none, ship) | — | Ship artifact has no build/runtime deps. Google Fonts via `<link>`, degrades to system fonts offline. |
| markitdown[pdf] (MIT) | authoring-only | PDF→markdown converter. Confined to `scripts/`, runs in a gitignored uv-managed py3.12 `.venv` (homebrew py3.14 `pyexpat` is broken). NEVER in the ship file. |
| anthropic | UNUSED (Phase 17) | Was `derive_signals.py --draft` only (lazy). The `--draft`/`--scaffold` authoring stack was DELETED under the inverted loop (the model SESSION is the backend, no API key); derive_signals.py no longer imports it (now stdlib-only). Still pinned in requirements-authoring.txt — a stale pin (cleanup candidate). The ship artifact never called an LLM. |

## Authoring Pipeline (M6 — build-time only, NEVER in the ship artifact)

| Step | Tool | Reads | Writes | Notes |
|------|------|-------|--------|-------|
| acquire | `scripts/acquire_fincen.py` (stdlib `urllib`, online) | FinCEN advisory URL | `data/fincen/raw/<advisory-id>.pdf` | authoring-only; NO runtime fetch in ship file |
| convert | `scripts/pdf_to_md.py` → markitdown (MIT) | raw PDF | `data/fincen/<advisory-id>.md` (verbatim, source of truth) | runs in gitignored uv `.venv` (py3.12); de-risk GATE on quality |
| derive | `scripts/derive_signals.py` (STDLIB-ONLY) → human review | `data/fincen/<advisory-id>.md` | `data/fincen/derived/<id>.json` (committed, gate-checked) | INVERTED loop: the LLM (a model session, no API key) EXTRACTS red flags + per-indicator judgment + build rec + build logic; the deterministic GROUNDEDNESS GATE (`--check-derived`: quote-grounding + `rf_region` + cover×data matrix + BUILD_NOW⇒build_logic) DISPOSES. `--corpus-status` emits the manifest. The LLM proposes (extraction too); the gate + the two human gates DISPOSE. (The old `--scaffold`/`--draft` config-draft path is DELETED.) |
| build | `scripts/build.py` (stdlib, system python) | config JSON (+ referenced `.md`) | `dist/<typology>/index.html` (inlined, self-contained) | validates `advisory_full` at the boundary; resolves `text_file`→inline so the md stays single source of truth. `--check` re-renders in memory + byte-compares vs committed dist (zero-drift guard, non-mutating) — wired into the smoke-checklist |

Naming convention is split: the corpus is **advisory-named** (`data/fincen/fin-2022-a002.md`) while the
typology config is **typology-named** (`config/typologies/elder-financial-exploitation.json`) — separates
the source-document corpus from derived typologies (scales to "all FinCEN advisories").

The split is load-bearing: acquire/convert/derive run at authoring; their output is persisted to
`data/fincen/` + `config/` and INLINED by `build.py`. The ship artifact stays single-file, offline,
zero runtime deps, no `fetch` (HANDOFF §4 / §4.5). FinCEN advisory text is verbatim public domain
(17 USC §105, attributed) — the ONE relaxation of the paraphrase rule; does NOT extend to FINTRAC.

## Data Flow

| Module | Reads (data) | Writes (data) | Env Vars | Notes |
|--------|-------------|---------------|----------|-------|
| demo | inlined CONFIG (synthetic figures, illustrative) + `advisory_full` (verbatim FinCEN, public domain) | DOM | — | No customer/transaction data, ever. Verbatim gov text kept visually separate from the illustrative badge |
| authoring pipeline | FinCEN advisory PDF (public source) | `data/fincen/raw/*.pdf`, `data/fincen/*.md` | — | build-time only; output never fetched at runtime |

## Development Toolchain

| Category | Tool | Config Path | Status |
|----------|------|-------------|--------|
| Build System | scripts/build.py (stdlib; validates config + inlines → dist/<id>/index.html; `--check` zero-drift guard) | scripts/build.py | detected |
| Authoring deps | markitdown[pdf] (MIT, convert only) in a uv-managed py3.12 .venv (gitignored); `anthropic` now UNUSED (derive_signals.py stdlib-only Phase 17) but still pinned in the requirements file (stale) | scripts/requirements-authoring.txt | detected (authoring-only) |
| Dev Server | python3 -m http.server (optional, iteration only) | — | optional (never required) |
| Version Control | git | .git/ | detected |

## Related

- HANDOFF.md (§3 target shape, §5 content model) · CLAUDE.md (non-negotiables)
