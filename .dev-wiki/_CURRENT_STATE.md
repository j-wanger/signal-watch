# Project: Signal Watch — AML Vision Demo

> Last updated: 2026-06-05 by /dev-debrief (Phase 12 — FinCEN corpus derivation)

## Recommended Next Action

**Phase 12 (FinCEN corpus derivation foundation — deterministic spine all-14 + LLM proof slice) —
DELIVERED (2026-06-05).** Built the backend for an EXPANDED, **singular** FinCEN demo (eventual: the user
picks one of 14 advisories and watches the loop derive its coverage → build recommendations → signal).
The full 14-advisory FinCEN corpus is committed as md; `extract_red_flags` is now a corpus-wide
**section-FINDER** (Tier-1 clean anchors + a Tier-2 loose-header/weak-intro fallback used only when Tier-1
is empty — so EFE is untouched; + intro-noise/header-block/citation filters). `--corpus` validates all 14:
**7 CLEAN · 3 LOW · 4 NEEDS** (2 NEEDS = FATF jurisdiction advisories with no red-flag list = correctly
flagged). Deterministic checks `build_rec_category` (cover×data matrix) + `check_record` (consistency +
traceability + BUILD_NOW⇒logic) DISPOSE; folded into `--selftest`. The **LLM backend = THIS session, NO
key** derived a 2-advisory proof slice (`data/fincen/derived/fin-2022-a001.json` kleptocracy 5-ind/2-BUILD_NOW
+ `fin-2024-a002.json` PRC precursors 14-ind/4-BUILD_NOW), each passing `--check-derived`; the boundary holds
(a tampered record is rejected). **Key framing recorded:** the spine ASSISTS but does not AUTOMATE — a
complete, demo-quality derived record still needs LLM-backend authoring (judgment + build logic + pruning
residual artifacts). EFE `--selftest` still 12+12; `index.html`/`build.py`/`schema.md` untouched; `--check
all` zero drift; anthropic LAZY.

**Next — Phase 13 (the payoff): the demo scope expansion** — advisory-selection front-end + per-indicator
build-rec render, driven by the derived corpus. Run `/dev-plan`. Other candidates: glued-list splitting for
the 2 NEEDS advisories; scale LLM-backend derivation to the remaining 5 CLEAN advisories; EFE-as-derived
validation vs the hand-authored elder config; (deferred backlog) elder true-up · fentanyl re-point · `--fetch`.

**Carried:** M6 vision arc (Phases 7–11) complete + accepted (Phase 11 committed `c37dc39`/`7c76971`).

## Active Phase

**[[phase-12-fincen-corpus-derivation|Phase 12: FinCEN corpus derivation foundation (deterministic spine all-14 + LLM proof slice)]]** (status: active)

Entry criteria: MET — M6 vision arc complete (derivation pipeline proven on the single EFE advisory);
the 14-advisory corpus is already converted to md on disk. User wants to expand the demo scope toward a
singular corpus-backed demo (user picks an advisory); this phase builds the backend foundation, demo
expansion deferred to Phase 13. Direction approved **backend-only** (over folding a minimal selectable view in).
Exit criteria: 14 corpus md committed · `extract_red_flags` generalized (≥2 formats) + `--corpus` report
across all 14 + EFE `--selftest` still 12+12 · deterministic build-rec-consistency + traceability checks
w/ selftest · LLM-backend proof slice (2–3) in `data/fincen/derived/*.json`, each check-passing ·
`git diff index.html` empty, `--check all` zero drift, deterministic layer stdlib-only, anthropic LAZY ·
documented in docstring + README + CLAUDE.

Progress: ~0% — planned, direction approved; 5 tasks, none started.

## Active Phase Contract

Phase: 12 - FinCEN corpus derivation foundation (deterministic spine all-14 + LLM proof slice)
Tasks: 5 (see tasks.md) — T1 commit the 14-md corpus (S) · T2 generalize `extract_red_flags` + `--corpus`
mode + report (L) · T3 deterministic build-rec-consistency + traceability checks (M) · T4 LLM-backend
derivation proof slice → `data/fincen/derived/*.json` (M) · T5 docs + verify (S).
Transition: continue (lite). Backend-only — engine/build.py untouched. LLM backend = this session (no API key).
Abort: if the corpus formats are too heterogeneous for ≥2 deterministic extractors — narrow to a
section-FINDER that flags non-conformers (the report is the deliverable). If a derived record can't pass
the checks — reject it (boundary holds). Blocked >3 attempts → ask user: skip or abort.

## Recent Decisions

| Decision | Confidence | Date |
|----------|------------|------|
| Phase 12 direction = backend-only foundation (deterministic spine validated on ALL 14 advisories + LLM-backend derivation proven on a 2–3 slice); demo scope expansion (advisory-selection front-end + per-indicator build-rec render) deferred to Phase 13. User chose backend-only over folding a minimal selectable demo view into this phase | high | 2026-06-05 |
| Destination = a SINGULAR corpus-backed demo where the user picks a FinCEN advisory (expand demo scope), NOT 14 separate demos. Per-advisory derivation records (`data/fincen/derived/*.json`) are the analytical artifact; the 3 hand-curated ship typologies stay the showcase | high | 2026-06-05 |
| LLM backend for derivation + build recommendation + build logic = THIS session (me), NOT an API-key `--draft` call (the Phase-11 T4 recorded-run substitution). Deterministic spine (extract + schema/shape + build-rec consistency vs cover×data + traceability) is the dispose-boundary — LLM proposes, deterministic checks dispose | high | 2026-06-05 |
| Commit the full 14-advisory FinCEN corpus md (un-gitignore) — reverses Phase-10's no-bulk-md call, justified now that the corpus backs the demo; public-domain FinCEN (17 USC §105). Network blocked in-session but the corpus is already converted on disk, so no acquisition needed | high | 2026-06-05 |
| Phase 11 direction = AUTOMATE (article→signal derivation), chosen by the user over the elder presentation-values true-up AND the fentanyl verbatim re-point at the direction gate. USER OVERRIDE of the planner's finish-before-scale recommendation (elder true-up stays a Future-phase candidate) | high | 2026-06-05 |
| Within AUTOMATE, chose variant B (LLM-drafted signal definition NOW) over A (deterministic scaffolder only, LLM deferred). USER OVERRIDE of the planner's recommendation of A. The deterministic-only cut A becomes the documented fallback if the LLM can't be coaxed to schema-valid output | high | 2026-06-05 |
| Boundary-preservation design reconciles the override with the standing Phase-9 anti-neural-judge-at-boundary principle: the LLM PROPOSES a `.draft.json`; the deterministic validator (build.py + schema) + the two human gates DISPOSE. No neural judge at the build boundary; committed configs stay deterministic + human-reviewed | high | 2026-06-05 |
| Two-layer split in one authoring-only tool: deterministic layer (stdlib-only, `--selftest`, offline, importable without anthropic via LAZY import) + neural layer (`--draft`, ANTHROPIC_API_KEY from env, anthropic in the gitignored authoring venv per the markitdown precedent, added to requirements-authoring.txt, never a ship dep). derive_signals.py never imported by engine/build.py; ship artifact never calls an LLM | high | 2026-06-05 |
| T3 consults the **claude-api reference** for the current Claude model id + Anthropic Python SDK + structured-output/tool-use pattern rather than guessing from training data (Nana retrieval-over-parametric + standing claude-api lookup instruction) | medium | 2026-06-05 |
| Phase 10 (SCALE) + Phase 9 (HARDEN) decisions — discovery-manifest not mass-download; pure `parse_index` + offline `--selftest` determinism split; in-process `build.py --check` guard, non-mutating + git-agnostic; keep committing built `dist/`; pre-commit/CI deferred (see `[[phase-10-fincen-corpus-crawler]]` + journal) | high | 2026-06-05 |

(Earlier Phase 7–10 decisions: see `[[phase-10-fincen-corpus-crawler]]`, `[[phase-08-doc-true-up]]` + the 2026-06-04 journal entries. Load-bearing carry-overs: authoring-time vs ship-artifact split — scraper/converter/derivation are build-time tools, the ship file stays single-file/offline/no-fetch (HANDOFF §4/§4.5); validate config at the build boundary — deterministic validator, fail loud; FinCEN-only verbatim public-domain exception (17 USC §105, NOT FINTRAC); lite ceremony.)

## Blockers and Open Questions

- [RESOLVED 2026-06-05 · planning] Phase-11 increment → **AUTOMATE: article→signal derivation, variant B (LLM-drafted signal definition NOW)**. User overrode the planner's finish-the-elder-true-up-first recommendation AND its deterministic-only (variant A) recommendation at the direction gate. The elder presentation-values true-up + fentanyl verbatim re-point + manifest `--fetch` cadence stay Future-phase candidates (deprioritized, not dropped). Variant A (deterministic scaffolder only) is the documented fallback if the LLM can't hit schema-valid output
- [OPEN · phase-11] Can the LLM be coaxed (via the claude-api structured-output/tool-use pattern) to emit a schema-valid signal `definition` that build.py accepts? Resolved by T3/T4; abort path = fall back to variant A deterministic scaffolder. Sub-question: can the post-markitdown EFE red-flag list be deterministically anchored on the section headers (Behavioral L454 / Financial L505)? Resolved at T1; thinner section-bounded capture if not (raised 2026-06-05)
- [KNOWLEDGE GAP · phase-11, T3] Current Anthropic model id + Anthropic Python SDK structured-output/tool-use pattern — filled at T3 by consulting the claude-api reference (implementation lookup, not a blocking planning gap)
- [DEFERRED 2026-06-05] Pre-commit hook / CI enforcement of `--check` — out of Phase 9 (lite; HANDOFF "don't over-engineer"). The runnable `--check` + smoke-checklist is the home; a pre-commit hook is a clean follow-up if wanted later
- [RESOLVED 2026-06-04] M6 anchor advisory → **FinCEN EFE FIN-2022-A002** (24 enumerated red flags, cleanest single-signal derivation; cheap to re-point later)
- [RESOLVED 2026-06-04] M6 product name → **"Signal Watch"** (rebrand rides along with the pipeline slice; resolves the M5 OPEN name question)
- [RESOLVED 2026-06-04] M6 where the verbatim advisory renders → **Act 1's existing SOURCE DOCUMENT panel** (`.doc`/`#doctext`) as a NEW top-level `advisory_full` field, bounded scrollable (max-height + overflow-y), attribution kept visually distinct from the illustrative badge (NOT Act 0, NOT an `anchor` subfield)
- [OPEN] M6 converter choice — markitdown (MIT) evaluated first for license-cleanliness; pymupdf4llm (AGPL, authoring-only) is the quality fallback. NONE installed in env. Resolved by the T2 CHECKPOINT against the real EFE PDF; the converter is authoring-only (scripts/), never in the ship file
- [IN PHASE 8 · 2026-06-04] CLAUDE.md/HANDOFF doc update for the FinCEN-only verbatim exception + the fentanyl-config provenance true-up — now the active Phase 8 (planned, direction approved); was deferred from Phase 7
- [DEFERRED 2026-06-04] Closing "ask" slide — out of scope (new act touches six-act-arc + needs config/schema); revisit as a config-driven follow-up
- [RESOLVED 2026-06-04] Ship as single file vs hosted — **single self-contained file** per typology
- [RESOLVED 2026-06-04] Presentation mode → **scripted** (M4 live/pre-gen skipped by decision)

## Key Artifacts

| Path | Purpose | Last Modified |
|------|---------|---------------|
| index.html | Generic engine template (`__CONFIG__` injection point); M3 added keyboard nav + reset + reduced-motion | 2026-06-04 |
| config/schema.md | Content-model contract | 2026-06-04 |
| config/typologies/{fentanyl,trade-based}.json | Typology content (single source of truth per typology) | 2026-06-04 |
| scripts/build.py | Validates config at boundary + inlines → dist/<id>/index.html | 2026-06-04 |
| dist/{fentanyl,trade-based}/index.html | Built self-contained ship files (per typology) | 2026-06-04 |
| archive/aml_vision_demo_fentanyl.baseline.html | Original baseline (equivalence reference) | 2026-06-04 |

## Session Journal (last 5)

- [2026-06-05] [[2026-06-05-phase-12-fincen-corpus-derivation|Phase 12 FinCEN corpus derivation foundation (M7)]] (lite, 5 tasks + 2 user refinement passes, DELIVERED) — backend for a singular corpus-backed FinCEN demo (user picks 1 of 14 advisories). Committed the full 14-advisory corpus md; rewrote `extract_red_flags` as a corpus-wide **section-FINDER** (Tier-1 clean anchors + a Tier-2 loose-header/weak-intro fallback used only when Tier-1 is empty — EFE untouched; + intro-noise/header-block/citation filters). `--corpus` → **7 CLEAN · 3 LOW · 4 NEEDS** (2 NEEDS = FATF jurisdiction advisories = correct). Deterministic checks `build_rec_category` (cover×data matrix) + `check_record` (consistency + traceability + BUILD_NOW⇒logic) in `--selftest`. LLM backend = THIS session (no key) derived 2 records (kleptocracy 5-ind/2-BUILD_NOW + PRC precursors 14-ind/4-BUILD_NOW), each `--check-derived` clean; boundary holds (tampered record rejected). RECORDED: the spine ASSISTS but does not AUTOMATE — complete records need LLM-backend authoring. EFE still 12+12; `index.html`/`build.py`/`schema` untouched; `--check all` zero drift. Opens M7.
- [2026-06-05] [[2026-06-05-phase-11-automated-derivation|Phase 11 Automated derivation (LLM-drafted signal config)]] (lite, 5 tasks, DELIVERED + accepted) — automated the Phase-7 manual article→signal step in authoring-only `derive_signals.py`: deterministic `extract_red_flags`/`scaffold_config` (`--selftest` extracts 24 EFE flags offline, stdlib-only; form-feed `split("\n")` fix keeps md-line traceability) + neural `--draft` (lazy `anthropic`, env-keyed) PROPOSING status/the-one-target/the-signal-`definition` via the Anthropic API (claude-opus-4-8 + `output_config.format` json_schema, verified vs the **claude-api reference**, not guessed). Boundary preserved: LLM proposes a gitignored `.draft.json`; build.py + schema + 2 human gates DISPOSE (rejects the bare skeleton naming the 2 judgment gaps, accepts a filled draft). Review gate **9/10 accept**; 2 MEDIUM `--draft`-path fixes folded in (adaptive thinking + `effort:high`; refusal/max_tokens handling). Engine/ship untouched; `--check all` zero drift. **M6 vision arc (Phases 7–11) complete.**
- [2026-06-05] [[2026-06-05-phase-10-fincen-corpus-crawler|Phase 10 FinCEN corpus crawler (SCALE)]] (lite, 4 tasks, COMPLETED + accepted, committed `0c87c47`) — widened the authoring scraper from a 1-entry stub to the discovered FinCEN corpus. New authoring-only `crawl_fincen.py` (pure `parse_index` → `data/fincen/index.json`, 14 advisories; `--selftest`/`--write`/`--list`/`--fetch`); `acquire_fincen.py` REGISTRY→manifest + `resolve_pdf` detail-page hop + EFE direct-PDF zero-hop override. Discovery over mass-download; detail→PDF resolution keeps the committed manifest deterministic. Widened pipe proven on a 2-advisory batch (deleted per user call). Stdlib-only; engine untouched; `--check all` zero drift.
- [2026-06-05] [[2026-06-05-phase-09-build-drift-guard|Phase 9 build-drift guard]] (lite, 3 tasks, COMPLETED + accepted, committed `33db22a`) — turned the M5 zero-drift invariant into a runnable, non-mutating guard. `build.py` refactored: `build_one` split into `render_one(typ, template) -> str` (the SINGLE source of truth for a typology's dist bytes) + thin writer; new `check_one` (git-agnostic byte-compare of committed dist vs fresh in-memory render, per-typology verdict, invalid-config = per-typology FAIL) + `resolve_targets`; `main` gained `--check [all|<id>]`. Wired into smoke-checklist (de-staled "both dist"→3 typologies; `git status --porcelain dist/` complement noted) + documented in docstring + README. Build byte-DETERMINISTIC (built twice → identical sha), HEAD dist == fresh build, `node --check` PASS ×3, `git diff index.html` empty, zero config edits → all 3 dist byte-identical. Discovered Phase 10 candidate: elder presentation-values true-up in the smoke-checklist.

(Earlier entries — Phase 8 doc true-up, M6 pipeline walking skeleton, M5 ship, M3/M2/M1 — see `index.md` journal list + their journal articles. Trimmed to last 4 per the _CURRENT_STATE size budget.)

## Cross-References

- HANDOFF.md · CLAUDE.md · README.md
- Knowledge wiki: **aml-wiki** (registered central store) — domain reference for typologies,
  indicators, FINTRAC/FinCEN/E-23. Linked via gitignored `wiki/` symlink; query with `/wiki-query`.
