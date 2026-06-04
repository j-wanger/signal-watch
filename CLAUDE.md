# AML Signal Engine — Vision Demo

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
- NO real customer/transaction data, ever. Advisory text must be public-source and PARAPHRASED
  (FINTRAC Jan-2025 Operational Alert; FinCEN FIN-2019-A006 / FIN-2024-A002).
- Live mode is optional, isolated, off by default, always has a scripted fallback.
  Never put keys/tokens in the frontend. Copilot is NOT a web backend (HANDOFF §4.5).

## Current state (M0 — bootstrap)
- Single baseline file: `aml_vision_demo_fentanyl.html` (vanilla HTML/CSS/JS, no build).
- M1 will extract content into `config/typologies/*.json` and add a build step that
  inlines src + css + config → `dist/index.html` (the ship target).

## How to run
- Present (now): open `aml_vision_demo_fentanyl.html` directly in a browser (no server).
- Develop: edit the file directly, or `python3 -m http.server` then open it.
- Ship target (after M1): open `dist/index.html` — single self-contained file, offline.

## Knowledge wiki
Domain reference comes from the registered **aml-wiki** (central store at
`/Users/jwang/private-knowledge/aml-wiki`) — AML typologies, red-flag indicators,
FINTRAC/FinCEN + OSFI E-23 references, the atom/composition vocabulary. A machine-local
symlink `wiki/ → aml-wiki` (gitignored) makes the harness auto-select it in this dir;
the SessionStart hook activates the knowledge-wiki framework from it.
- Query domain knowledge before guessing: `/wiki-query <question>` (auto-scopes to aml-wiki).
- AML insights worth keeping go back to aml-wiki via `/wiki-add` — it is the canonical home.
- For authoring a new typology (M2), pull paraphrased advisory specifics + indicators
  from the wiki rather than inventing them. Retrieval over parametric guessing.

## Aesthetic
Dark "dossier" theme, amber `--signal` (#f6a623) accent; fonts Newsreader / Archivo /
JetBrains Mono. Theme lives in `:root` CSS variables. Refined, not flashy.

## Milestones
M0 bootstrap · M1 config-driven refactor · M2 multi-typology · M3 presenter polish ·
M4 (optional) live/pre-gen mode · M5 ship. See HANDOFF.md §8.

## Definition of done
Reliable offline · multi-typology from config · presenter controls · compliance-clean ·
README written. See HANDOFF.md §1.2.
