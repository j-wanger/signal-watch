# Architecture: AML Signal Engine — Vision Demo

> Last updated: 2026-06-04 by /dev-debrief (M6 — Signal Watch ingestion pipeline)

## Directory Layout

signal-watch/
  index.html                      # generic engine template (`__CONFIG__` injection point; vanilla HTML/CSS/JS)
  config/
    schema.md                     # content-model contract (incl. `advisory_full`)
    typologies/*.json             # per-typology content (fentanyl, trade-based, elder-financial-exploitation)
  scripts/
    build.py                      # stdlib: validates config at boundary + inlines → dist/<id>/index.html
    acquire_fincen.py             # authoring-only: stdlib urllib fetch of a FinCEN advisory PDF
    pdf_to_md.py                  # authoring-only: markitdown PDF→markdown
    requirements-authoring.txt    # authoring deps (markitdown) — uv `.venv`, gitignored
  data/fincen/
    raw/<advisory-id>.pdf         # acquired source PDF (authoring-only)
    <advisory-id>.md              # verbatim advisory markdown = source of truth
  dist/<typology>/index.html      # built self-contained ship files (per typology)
  archive/                        # original baseline (equivalence reference)
  CLAUDE.md  README.md  HANDOFF.md # always-loaded non-negotiables / run / full context
  .dev-wiki/                      # lifecycle tracking (this wiki)

backend/ + tests/ remain optional (HANDOFF §3.3); M4 live/pre-gen skipped (file:// trap).

## Module Responsibilities

| Module | Purpose | Key Entry Points | Inputs | Outputs |
|--------|---------|-----------------|--------|---------|
| index.html | Generic engine template: six-act scripted walkthrough; state machine + render dispatch + animations, all inline; `__CONFIG__` injection point | `goto(0)` (bottom of `<script>`) | inlined CONFIG (per typology) + Google Fonts (online; degrades) | rendered DOM |
| scripts/build.py | Validates a typology config at the boundary (fails loud) + resolves `text_file`→inline + injects CONFIG → self-contained `dist/<id>/index.html` | `python3 scripts/build.py <id>` (or `all`) | config JSON + referenced `.md` | `dist/<id>/index.html` |
| scripts/acquire_fincen.py, scripts/pdf_to_md.py | Authoring-only ingestion: fetch advisory PDF, convert to verbatim markdown | run manually at authoring | FinCEN advisory URL / raw PDF | `data/fincen/raw/*.pdf`, `data/fincen/*.md` |

Inside `index.html`: content read from the injected CONFIG (`advisory_full` carries the verbatim
source); state `act`/`selected`/`confirmed`; `goto(i)`, `updateControls()`, nav `advance()`/`back()`/
`reset()`, `streamAdvisory()`, `esc()`, `act0()`…`act6()` dispatched via the `RENDER` array. M3 added
keyboard nav (←/→/Space/Esc/↺) + `prefers-reduced-motion`. Theme in `:root` CSS variables.

## Dependencies

| Package | Version | Role |
|---------|---------|------|
| (none, ship) | — | Ship artifact has no build/runtime deps. Google Fonts via `<link>`, degrades to system fonts offline. |
| markitdown[pdf] (MIT) | authoring-only | PDF→markdown converter. Confined to `scripts/`, runs in a gitignored uv-managed py3.12 `.venv` (homebrew py3.14 `pyexpat` is broken). NEVER in the ship file. |

## Authoring Pipeline (M6 — build-time only, NEVER in the ship artifact)

| Step | Tool | Reads | Writes | Notes |
|------|------|-------|--------|-------|
| acquire | `scripts/acquire_fincen.py` (stdlib `urllib`, online) | FinCEN advisory URL | `data/fincen/raw/<advisory-id>.pdf` | authoring-only; NO runtime fetch in ship file |
| convert | `scripts/pdf_to_md.py` → markitdown (MIT) | raw PDF | `data/fincen/<advisory-id>.md` (verbatim, source of truth) | runs in gitignored uv `.venv` (py3.12); de-risk GATE on quality |
| derive | human (hand-authored) | `data/fincen/<advisory-id>.md` | `config/typologies/<typology>.json` (`advisory_full` via `text_file`→inline) | NOT auto-extracted; deterministic schema validator at the boundary |
| build | `scripts/build.py` (stdlib, system python) | config JSON (+ referenced `.md`) | `dist/<typology>/index.html` (inlined, self-contained) | validates `advisory_full` at the boundary; resolves `text_file`→inline so the md stays single source of truth |

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
| Build System | scripts/build.py (stdlib; validates config + inlines → dist/<id>/index.html) | scripts/build.py | detected |
| Authoring deps | markitdown[pdf] (MIT) in a uv-managed py3.12 .venv (gitignored) | scripts/requirements-authoring.txt | detected (authoring-only) |
| Dev Server | python3 -m http.server (optional, iteration only) | — | optional (never required) |
| Version Control | git | .git/ | detected |

## Related

- HANDOFF.md (§3 target shape, §5 content model) · CLAUDE.md (non-negotiables)
