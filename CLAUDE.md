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

## Current state (M7 — corpus-backed derivation; M6 pipeline complete)
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
  → `derive_signals.py` (Phase 11: automate the article→signal step — a DETERMINISTIC layer
  `--selftest`/`--scaffold` extracts the enumerated red flags + emits a schema-shaped config
  SKELETON, and a NEURAL layer `--draft` calls the Anthropic API to PROPOSE the judgment fields
  [indicator statuses, the single target, the signal definition]; the LLM proposes, `build.py` +
  schema + the two human gates DISPOSE — the `.draft.json` is a gitignored scratch artifact, never
  auto-promoted, so committed configs stay deterministic + human-reviewed) → hand-review/rename to a
  schema-valid config. The deterministic authoring layers are stdlib-only; `markitdown` (convert) and
  `anthropic` (`--draft`) live in a gitignored uv `.venv` and `--draft` reads `ANTHROPIC_API_KEY` from
  the env — NO authoring tool is imported by the engine or `build.py`, and the ship artifact never
  fetches or calls an LLM. The elder typology renders the FULL verbatim EFE advisory (FinCEN
  FIN-2022-A002, public domain) in Act 1 via the `advisory_full` field.
- Corpus derivation (Phase 12, M7 — backend for an expanded, singular corpus-backed demo where the
  user picks one of 14 advisories): the full 14-advisory FinCEN corpus is committed as md
  (`data/fincen/*.md`). `derive_signals.py --corpus` runs the (generalized) red-flag extractor across
  all 14 and reports each CLEAN / LOW-CONFIDENCE / NEEDS-ATTENTION — the deterministic spine validated
  on the whole corpus, flagging the heterogeneous non-conformers rather than forcing a count.
  `--scaffold-derived` emits a `data/fincen/derived/<id>.json` skeleton (one indicator per extracted
  red flag, `src_line`-traceable); the LLM backend fills the judgment (status, data, a build
  recommendation, and build logic for the BUILD_NOW gaps) and `--check-derived` DISPOSES — `build_rec`
  must follow the deterministic cover×data matrix (`build_rec_category`), every indicator must trace to
  a red-flag md line, BUILD_NOW must carry a full definition. The LLM backend may be the Anthropic API
  (`--draft`) OR a live model session acting as backend (no key); either way the LLM proposes and the
  deterministic checks dispose. Derived records are an LLM-derived + checked corpus dataset, NOT ship
  typology configs (the 3 hand-curated typologies stay the showcase).
- Corpus explorer (Phase 13, M7 — the demo scope expansion): a SECOND, separate ship artifact
  `dist/corpus/index.html`, built from a standalone template `corpus.html` (owns its own copy of the
  dossier theme — the six-act engine `index.html` is left byte-untouched). A staged 4-screen flow:
  SELECT one of the 14 advisories (honest status chips: derived / clean-or-low-not-yet-derived /
  non-derivable) → COVERAGE gauge → per-indicator BUILD RECOMMENDATIONS (the cover×data build_rec,
  sorted BUILD_NOW-first, each row src_line-traceable) → SIGNAL spec for the BUILD_NOW gaps. Built by
  `build.py corpus` (or `all`; guarded by `--check corpus`), which reads two COMMITTED data artifacts —
  the extraction manifest `data/fincen/corpus-status.json` (emitted by `derive_signals.py
  --corpus-status`) + the derived records `data/fincen/derived/*.json` — merges them by id, and
  validates the derived shape at the build boundary (build_rec ∈ matrix vocabulary; BUILD_NOW ⇒ full
  build_logic). build.py NEVER imports the authoring layer; ships with 2/14 derived (front-end shows
  the full corpus honestly, derivation scales later). No fabricated lift/stats; the always-on badge
  stays, with the verbatim public-domain source attribution kept visually distinct from it.
- IMPORTANT — the spine ASSISTS, it does not AUTOMATE the derivation. `--corpus` extraction is
  deterministic but imperfect (heterogeneous corpus: ~7/14 parse cleanly, the rest are flagged
  LOW/NEEDS; even CLEAN extractions can carry residual artifacts like an intro-tail line). A complete,
  demo-quality derived record still requires **LLM-backend authoring** by the model session: the
  per-indicator status/data judgment, the build-recommendation rationale, the signal build logic, AND
  pruning the residual extraction noise. The deterministic layer extracts + flags + validates; the LLM
  backend authors; the two human gates dispose. Phase 12 proved the loop on a 2-advisory slice — it did
  not (and is not meant to) auto-derive the corpus.

## How to run
- Build: `python3 scripts/build.py <id>` (or `all`) → `dist/<id>/index.html`.
- Corpus explorer: `python3 scripts/build.py corpus` → `dist/corpus/index.html` (from `corpus.html` +
  `data/fincen/corpus-status.json` + `data/fincen/derived/*.json`). Regenerate the manifest with
  `python3 scripts/derive_signals.py --corpus-status` after the corpus md set changes, then rebuild.
- Present: open `dist/<id>/index.html` (or `dist/corpus/index.html`) — single self-contained file,
  offline, no server. Drift guard before presenting: `python3 scripts/build.py --check all`.
- Iterate: edit `index.html` / `corpus.html` / a config, rebuild. `python3 -m http.server` optional, never required.

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
M7 corpus-backed demo (Phase 12 derivation backend + Phase 13 corpus explorer `dist/corpus/`).
See HANDOFF.md §8.

## Definition of done
Reliable offline · multi-typology from config · presenter controls · compliance-clean ·
README written. See HANDOFF.md §1.2.
