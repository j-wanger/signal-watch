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
  default (e.g. the FINTRAC Jan-2025 Operational Alert behind the fentanyl demo). ONE exception:
  US FinCEN federal advisories are public domain (17 USC §105) and may be reproduced VERBATIM with
  attribution, kept visually separate from the "Illustrative data & outputs" badge (see Act 1's
  SOURCE DOCUMENT panel, EFE FIN-2022-A002). The verbatim exception is FinCEN-only — it does NOT
  extend to FINTRAC (Canadian Crown copyright → still paraphrase).
- Live mode is optional, isolated, off by default, always has a scripted fallback.
  Never put keys/tokens in the frontend. Copilot is NOT a web backend (HANDOFF §4.5).

## Current state (M6 — Signal Watch ingestion pipeline)
- Generic engine: `index.html` (vanilla HTML/CSS/JS) with a single `__CONFIG__` injection point.
  Typology-agnostic — adding a typology is one JSON file, no engine edits. Presenter controls (M3):
  keyboard nav (←/→/Space/Esc/↺), reset, `prefers-reduced-motion`.
- Content: `config/typologies/*.json` (fentanyl, trade-based, elder-financial-exploitation) against
  `config/schema.md`.
- Build: `scripts/build.py` validates a config against the schema (fails loud), resolves
  `text_file`→inline, and inlines everything → `dist/<id>/index.html`. Baseline preserved in `archive/`.
- Authoring pipeline (M6, build-time ONLY — never in the ship file): `crawl_fincen.py` (Phase 10:
  discover the FinCEN advisories listing → committed manifest `data/fincen/index.json`; pure
  `parse_index` + offline `--selftest`, thin live `--fetch`) → `acquire_fincen.py` (read the manifest,
  resolve each advisory's PDF from its detail page; EFE kept as a zero-hop direct-PDF override) →
  `pdf_to_md.py` (markitdown PDF→markdown, persisted to `data/fincen/<id>.md` as the source of truth)
  → hand-derive a schema-valid config. All authoring tools are stdlib-only (markitdown lives in a
  gitignored uv `.venv`) and never imported by the engine or `build.py`. The elder typology renders
  the FULL verbatim EFE advisory (FinCEN FIN-2022-A002, public domain) in Act 1 via the
  `advisory_full` field.

## How to run
- Build: `python3 scripts/build.py <id>` (or `all`) → `dist/<id>/index.html`.
- Present: open `dist/<id>/index.html` — single self-contained file, offline, no server.
- Iterate: edit `index.html` / a config, rebuild. `python3 -m http.server` optional, never required.

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
M4 (skipped) live/pre-gen mode · M5 ship · M6 Signal Watch ingestion pipeline (FinCEN verbatim).
See HANDOFF.md §8.

## Definition of done
Reliable offline · multi-typology from config · presenter controls · compliance-clean ·
README written. See HANDOFF.md §1.2.
