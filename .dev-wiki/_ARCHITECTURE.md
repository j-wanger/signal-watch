# Architecture: Signal Watch — AML Vision Demo

> Last updated: 2026-06-05 by /dev-debrief (Phase 12 — FinCEN corpus derivation)

## Directory Layout

signal-watch/
  index.html                      # generic engine template (`__CONFIG__` injection point; vanilla HTML/CSS/JS)
  config/
    schema.md                     # content-model contract (incl. `advisory_full`)
    typologies/*.json             # per-typology content (fentanyl, trade-based, elder-financial-exploitation)
  scripts/
    build.py                      # stdlib: render_one (validate+inline = dist-bytes source of truth) + writer; --check drift guard
    acquire_fincen.py             # authoring-only: stdlib urllib fetch of a FinCEN advisory PDF
    pdf_to_md.py                  # authoring-only: markitdown PDF→markdown
    derive_signals.py             # authoring-only: md→config draft (deterministic --selftest/--scaffold + neural --draft; LLM proposes, build.py disposes)
    requirements-authoring.txt    # authoring deps (markitdown, anthropic) — uv `.venv`, gitignored
  data/fincen/
    raw/<advisory-id>.pdf         # acquired source PDF (authoring-only, gitignored)
    <advisory-id>.md              # verbatim advisory markdown = source of truth (FULL 14-advisory corpus committed as of Phase 12)
    index.json                    # discovered advisory manifest (Phase 10)
    derived/<advisory-id>.json    # Phase 12: LLM-backend-derived + deterministically-checked record (NOT a ship config)
  dist/<typology>/index.html      # built self-contained ship files (per typology)
  archive/                        # original baseline (equivalence reference)
  CLAUDE.md  README.md  HANDOFF.md # always-loaded non-negotiables / run / full context
  .dev-wiki/                      # lifecycle tracking (this wiki)

backend/ + tests/ remain optional (HANDOFF §3.3); M4 live/pre-gen skipped (file:// trap).

## Module Responsibilities

| Module | Purpose | Key Entry Points | Inputs | Outputs |
|--------|---------|-----------------|--------|---------|
| index.html | Generic engine template: six-act scripted walkthrough; state machine + render dispatch + animations, all inline; `__CONFIG__` injection point | `goto(0)` (bottom of `<script>`) | inlined CONFIG (per typology) + Google Fonts (online; degrades) | rendered DOM |
| scripts/build.py | `render_one(typ, template) -> str` (validate at boundary, fails loud + resolve `text_file`→inline + inject CONFIG + self-contained guard) is the SINGLE source of truth for a typology's dist bytes; a thin writer persists it; `check_one` byte-compares a fresh render against the committed dist (non-mutating, git-agnostic drift guard); `resolve_targets` shares `all`/`<id>` logic | `python3 scripts/build.py <id>` (or `all`); `--check [all\|<id>]` (drift guard) | config JSON + referenced `.md` | `dist/<id>/index.html`; `--check`: per-typology drift verdict + exit code |
| scripts/acquire_fincen.py, scripts/pdf_to_md.py | Authoring-only ingestion: fetch advisory PDF, convert to verbatim markdown | run manually at authoring | FinCEN advisory URL / raw PDF | `data/fincen/raw/*.pdf`, `data/fincen/*.md` |
| scripts/derive_signals.py | Authoring-only. DETERMINISTIC spine (stdlib, offline): `extract_red_flags` is a corpus-wide section-FINDER (Tier-1 clean headers + explicit list-intros; Tier-2 loose-header/weak-intro fallback only when Tier-1 is empty — EFE untouched; intro-noise/header-block/citation filters); `extraction_quality` + `--corpus` classify all 14 advisories CLEAN/LOW/NEEDS; deterministic checks `build_rec_category` (cover×data matrix) + `check_record` (build-rec consistency + src_line traceability + BUILD_NOW⇒build_logic). NEURAL/AUTHORING layer: `--draft` (lazy `anthropic`, env-keyed) OR a model SESSION as backend proposes per-indicator status/data + build recommendation + build logic; `--check-derived` DISPOSES. The spine ASSISTS, it does not AUTOMATE — a complete record needs LLM-backend authoring; the 2 human gates dispose | `--selftest`; `--corpus`; `--scaffold-derived <id> <md>`; `--check-derived <rec>`; `--scaffold`/`--draft` (config draft) | `data/fincen/<id>.md` (+ `ANTHROPIC_API_KEY` for `--draft`) | `data/fincen/derived/<id>.json` (committed, checked); `config/typologies/<id>.draft.json` (gitignored scratch) |

Inside `index.html`: content read from the injected CONFIG (`advisory_full` carries the verbatim
source); state `act`/`selected`/`confirmed`; `goto(i)`, `updateControls()`, nav `advance()`/`back()`/
`reset()`, `streamAdvisory()`, `esc()`, `act0()`…`act6()` dispatched via the `RENDER` array. M3 added
keyboard nav (←/→/Space/Esc/↺) + `prefers-reduced-motion`. Theme in `:root` CSS variables.

## Dependencies

| Package | Version | Role |
|---------|---------|------|
| (none, ship) | — | Ship artifact has no build/runtime deps. Google Fonts via `<link>`, degrades to system fonts offline. |
| markitdown[pdf] (MIT) | authoring-only | PDF→markdown converter. Confined to `scripts/`, runs in a gitignored uv-managed py3.12 `.venv` (homebrew py3.14 `pyexpat` is broken). NEVER in the ship file. |
| anthropic | authoring-only | Anthropic Python SDK — `derive_signals.py --draft` ONLY, LAZY-imported. In the gitignored uv `.venv`; `ANTHROPIC_API_KEY` from env. NEVER a ship dep; the ship artifact never calls an LLM. |

## Authoring Pipeline (M6 — build-time only, NEVER in the ship artifact)

| Step | Tool | Reads | Writes | Notes |
|------|------|-------|--------|-------|
| acquire | `scripts/acquire_fincen.py` (stdlib `urllib`, online) | FinCEN advisory URL | `data/fincen/raw/<advisory-id>.pdf` | authoring-only; NO runtime fetch in ship file |
| convert | `scripts/pdf_to_md.py` → markitdown (MIT) | raw PDF | `data/fincen/<advisory-id>.md` (verbatim, source of truth) | runs in gitignored uv `.venv` (py3.12); de-risk GATE on quality |
| derive | `scripts/derive_signals.py` (stdlib deterministic + lazy `anthropic` for `--draft`) → human review | `data/fincen/<advisory-id>.md` | `config/typologies/<typology>.draft.json` (scratch, gitignored) → human → `<typology>.json` | `--scaffold` emits a schema-shaped SKELETON (deterministic, offline); `--draft` proposes the judgment fields (status, the one target, the signal `definition`) via the Anthropic API. The LLM PROPOSES; build.py + schema + the two human gates DISPOSE — committed configs stay deterministic + human-reviewed. `advisory_full` via `text_file`→inline |
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
| Authoring deps | markitdown[pdf] (MIT) + anthropic (SDK, `--draft` only) in a uv-managed py3.12 .venv (gitignored) | scripts/requirements-authoring.txt | detected (authoring-only) |
| Dev Server | python3 -m http.server (optional, iteration only) | — | optional (never required) |
| Version Control | git | .git/ | detected |

## Related

- HANDOFF.md (§3 target shape, §5 content model) · CLAUDE.md (non-negotiables)
