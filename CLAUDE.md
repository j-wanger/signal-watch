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
  → `derive_signals.py` (the deterministic GATE — Phase 16 inverted the boundary, Phase 17 deleted the
  old extractor: the LLM backend reads `<id>.md` and EXTRACTS the red flags + per-indicator judgment into
  `data/fincen/derived/<id>.json`, and `--check-derived` DISPOSES — see the corpus-derivation bullet).
  `derive_signals.py` is now stdlib-only (no `anthropic` dep); only `markitdown` (convert) lives in a
  gitignored uv `.venv` — NO authoring tool is imported by the engine or `build.py`, and the ship artifact
  never fetches or calls an LLM. The elder typology renders the FULL verbatim EFE advisory (FinCEN
  FIN-2022-A002, public domain) in Act 1 via the `advisory_full` field.
- Corpus derivation (Phase 12+, M7 — backend for an expanded, singular corpus-backed demo where the
  user picks one of 14 advisories): the full 14-advisory FinCEN corpus is committed as md
  (`data/fincen/*.md`). The LLM backend (a live model session, no key) reads an advisory and EXTRACTS its
  red flags + per-indicator judgment (status, data, a build recommendation, build logic for the BUILD_NOW
  gaps) into `data/fincen/derived/<id>.json`; `--check-derived` DISPOSES — `build_rec` must follow the
  cover×data matrix (`build_rec_category`), every verbatim `flag` must QUOTE-GROUND in the source md
  (`normalize(flag)` ⊂ `normalize(md)`, inside the red-flag region `rf_region`), BUILD_NOW must carry a
  full definition. `--corpus` / `--corpus-status` are a cheap rf_region triage HINT (`derivable` = a
  red-flag region exists, false only for the 2 FATF advisories; + a coarse block count via `_rf_triage`) —
  never the derivation authority. The LLM proposes (extraction included); the deterministic gate + the two
  human gates dispose. Derived records are an LLM-derived + checked corpus dataset, NOT ship typology
  configs (the 3 hand-curated typologies stay the showcase).
- Corpus explorer (Phase 13, M7 — the demo scope expansion): a SECOND, separate ship artifact
  `dist/corpus/index.html`, built from a standalone template `corpus.html` (owns its own copy of the
  dossier theme — the six-act engine `index.html` is left byte-untouched). A staged 5-screen ARC
  (Phase 18 gave the explorer the showcase's two missing beats — a human gate + a close-the-loop payoff):
  SELECT one of the 14 advisories (honest status chips: derived / clean-or-low-not-yet-derived /
  non-derivable) → COVERAGE gauge → BUILD RECOMMENDATIONS **= the human GATE** (per-indicator cover×data
  build_rec, sorted BUILD_NOW-first, each row src_line-traceable; the BUILD_NOW rows are SELECTABLE
  div-toggles [NOT `<input>`, so Space/arrow nav still works] — default all-selected, "agent proposes,
  human disposes"; non-BUILD_NOW rows read-only) → SIGNAL spec for the PICKED BUILD_NOW gaps → CLOSE THE
  LOOP (the coverage index animates before→after as the picked gaps flip gap→covered — same model as the
  showcase's Act 6; 0-picked / 0-BUILD_NOW holds coverage flat with a note, never a fake rise). The payoff
  is COVERAGE, NOT precision combination-lift: the derived records carry no precision/lift numbers, so
  porting the showcase lift beat would FABRICATE ~12 per-advisory stats — rejected (the "never present
  synthetic numbers as real" non-negotiable); coverage is already disclosed illustrative. Phase 18 unfroze
  ONLY `corpus.html` (the arc reuses existing data fields — no schema/data/`build.py` change). Built by
  `build.py corpus` (or `all`; guarded by `--check corpus`), which reads two COMMITTED data artifacts —
  the extraction manifest `data/fincen/corpus-status.json` (emitted by `derive_signals.py
  --corpus-status`) + the derived records `data/fincen/derived/*.json` — merges them by id, and
  validates the derived shape at the build boundary (build_rec ∈ matrix vocabulary; BUILD_NOW ⇒ full
  build_logic). build.py NEVER imports the authoring layer; ships with **12/14 derived** (Phase 17 added
  health-care fin-2026-a001 [glued, 24 flags] + COVID health-insurance fin-2021-a001 + Iran-terror
  fin-2024-a001 + ISIS fin-2025-a001 + the EFE corpus record fin-2022-a002 to the Phase-16 seven). Only
  the 2 FATF jurisdiction advisories (fin-2020-a009, fin-2021-a003 — no enumerated red-flag list) stay
  non-derivable. The glued advisories (ransomware fin-2021-a004, health-care fin-2026-a001) were
  unreachable by the deleted structural extractor yet ship derived via the inverted loop (the LLM reads
  them like a human, the gate grounds each verbatim flag). No fabricated lift/stats; the always-on badge
  stays, with the verbatim public-domain source attribution kept visually distinct from it.
- IMPORTANT — INVERTED extraction boundary (Phase 16) + the SUBTRACTION (Phase 17): the **LLM EXTRACTS, the
  deterministic layer GATES**, and the old extractor is **DELETED**. The earlier deterministic
  `extract_red_flags` accreted format special-casing every phase yet the LLM still had to author/prune its
  output, so the subtraction test inverted it: the LLM (the model session as backend) extracts the candidate
  red flags + per-indicator status/data judgment + build recommendation + signal logic; the deterministic
  layer DISPOSES via `check_record` — **quote-GROUNDING** (each verbatim `flag` is a substring of the source
  md under `normalize()`, the traceability authority, replacing src_line ∈ extractor) + a cheap section-cite
  RELEVANCE region (`rf_region`) + the cover×data matrix + BUILD_NOW⇒full-build_logic shape. Complexity moved
  from brittle section-PARSING (open problem — every advisory differs) to a closed-set md NORMALIZER and
  SHRANK. **Phase 17 then DELETED `extract_red_flags` and the whole `--scaffold` / `--draft` /
  `--scaffold-derived` authoring stack it fed** (`derive_signals.py` ~1200 → ~600 lines), leaving exactly the
  gate (`normalize` + `rf_region` + `check_record`) + a ~14-line `rf_region`-bounded triage counter
  (`_rf_triage` — the only counting role the extractor kept; it reuses the already-computed region span). The
  inverted loop is the SOLE derivation path; the LLM proposes (extraction too), the deterministic gate + the
  two human gates dispose.
- Extraction faithfulness (the LLM extracts; the gate grounds): faithfulness is now enforced by the gate, not
  a structural parser — every verbatim `flag` must QUOTE-GROUND in the source md. Two heterogeneous formats
  the deleted deterministic extractor could not parse are handled by the LLM reading like a human:
  **footnote-interrupted** lists (a clause split across a page-break footnote run — the LLM extracts a
  CONTIGUOUS grounded span and drops the across-the-break continuation rather than bridging it, e.g.
  fin-2021-a001 IND-01) and **glued-no-separator** advisories (fin-2021-a004 ransomware, fin-2026-a001
  health-care — markitdown dropped both bullets AND blank lines so flags fuse into one block; the `_rf_triage`
  counter sizes them as a few blocks, but the LLM extracts every genuine flag, e.g. health-care 24, and the
  gate grounds each). No structure-preserving converter and no post-hoc splitter were needed. Convention:
  derived records store RAW text; corpus.html's `esc()` is the sole escaper (never pre-escape `&gt;`/`&lt;`
  in a record — it double-escapes). `normalize()` drops the glued `FINCEN ADVISORY` running header and
  collapses smart quotes / hyphen-wraps / footnote digits, so a header-glued or marker-glued flag still
  grounds (keep an in-flag footnote marker verbatim where it falls mid-span, e.g. `NPO84`).

## How to run
- Build: `python3 scripts/build.py <id>` (or `all`) → `dist/<id>/index.html`.
- Corpus explorer: `python3 scripts/build.py corpus` → `dist/corpus/index.html` (from `corpus.html` +
  `data/fincen/corpus-status.json` + `data/fincen/derived/*.json`). Regenerate the manifest with
  `python3 scripts/derive_signals.py --corpus-status` after the corpus md set changes, then rebuild.
- Present: open `dist/<id>/index.html` (or `dist/corpus/index.html`) — single self-contained file,
  offline, no server. Drift guard before presenting: `python3 scripts/build.py --check all`.
- Test (all dep-free, no install): `node tests/corpus-explorer.test.mjs` drives the corpus explorer's
  5-screen arc against the committed `dist/corpus/index.html` (gate toggle, Signal empty states,
  close-the-loop coverage math, reduced-motion) · `python3 scripts/derive_signals.py --selftest` runs
  the derivation GATE checks. Pre-present sequence: `--check all` (drift) → `node tests/…` (arc) → walk
  `tests/smoke-checklist.md` (the human-eye checks).
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
