# Project: Signal Watch — AML Vision Demo

> Last updated: 2026-06-05 by /dev-plan (Phase 13 — corpus explorer)

## Recommended Next Action

**Phase 13 (Corpus explorer — advisory-selection front-end + per-indicator build-rec render) — PLANNED,
direction approved (2026-06-05).** The PAYOFF for M7: render the Phase-12 derived records as a NEW
standalone ship artifact `dist/corpus/index.html` (built from `corpus.html`) — a FinCEN CORPUS EXPLORER
where a stakeholder picks 1 of 14 advisories and watches the loop derive coverage → per-indicator build
recommendations → signal. Single self-contained file, offline, no fetch (same non-negotiable as the
showcase). A STAGED 4-screen flow: **SELECT** (14 advisories, honest status chips — DERIVED live ·
CLEAN/LOW/NEEDS "not yet derived" · FATF non-derivable; the 2 derived advisories clickable) → **COVERAGE**
(gauge covered=1/partial=0.5/gap=0 + indicator list) → **BUILD RECOMMENDATIONS** (the new centerpiece —
per-indicator cover×data → build_rec matrix, BUILD_NOW-first, src_line-traceable) → **SIGNAL SPEC**
(BUILD_NOW cards from build_logic). The six-act `index.html`, the 3 typology configs, and their dists stay
**byte-untouched** (corpus.html owns its own theme CSS). build.py stays **decoupled** — reads committed data
(corpus-status.json + derived/*.json), never imports derive_signals.py. No fabricated lift/stats; the
always-on "Illustrative data & outputs" badge stays.

**Next:** T1 (`--corpus-status` manifest) → T2 (corpus.html template, the L) → T3 (build.py corpus path) →
T4 (build + verify) → T5 (docs); then `/dev-debrief`. Follow-ups (not in scope): scale derivation to the 5
remaining CLEAN advisories; glued-list splitting for the 2 NEEDS; exclude the 2 FATF advisories; (deferred)
elder true-up · fentanyl re-point · `--fetch`. **Carried:** M6 vision arc (7–11) + M7 foundation (Phase 12,
commit `90939b4`/`348ba81`) complete + accepted — the spine + 2 derived proof-slice records this phase renders.

## Active Phase

**[[phase-13-corpus-explorer|Phase 13: Corpus explorer (advisory-selection front-end + per-indicator build-rec render)]]** (status: active)

Entry criteria: MET — Phase 12 complete + accepted: the deterministic spine is validated on all 14 advisories
(7 CLEAN / 3 LOW / 4 NEEDS) and the LLM backend (no key) derived 2 check-passing proof-slice records
(fin-2022-a001 5-ind/2-BUILD_NOW + fin-2024-a002 14-ind/4-BUILD_NOW). The derived-record shape is stable.
User wants the payoff: render the corpus-backed demo. Direction approved **standalone artifact + staged
4-screen flow + all-14 honest status** (over fold-into-index.html / dashboard / only-2-derived).
Exit criteria: `dist/corpus/index.html` = a NEW self-contained offline 4-screen explorer (SELECT → COVERAGE
→ BUILD RECOMMENDATIONS → SIGNAL SPEC) · `--corpus-status` emits the committed 14-entry manifest · `build.py
corpus`/`--check corpus` work, build.py does NOT import derive_signals.py · "Illustrative data & outputs"
badge + reduced-motion + keyboard parity present · `git diff index.html` empty, config/** + the 3 typology
dists byte-untouched, `--check all` zero drift · documented in README + CLAUDE.

Progress: ~0% — planned, direction approved; 5 tasks, none started.

## Active Phase Contract

Phase: 13 - Corpus explorer (advisory-selection front-end + per-indicator build-rec render)
Tasks: 5 (see tasks.md) — T1 `--corpus-status` → committed corpus-status.json, 14 entries (M) · T2 corpus.html
standalone 4-screen explorer template, own theme CSS + `__CORPUS__` + render JS (L) · T3 build.py corpus path
(render/build/check_corpus + special target + boundary validator, decoupled) (M) · T4 build + verify (S) · T5 docs (S).
Transition: continue (lite). Showcase byte-frozen (index.html/config/** + 3 typology dists untouched).
Abort: if the derived shape needs an engine edit to render — re-implement the component standalone in
corpus.html, don't touch index.html. Blocked >3 attempts → ask user: skip or abort.

## Recent Decisions

| Decision | Confidence | Date |
|----------|------------|------|
| Phase 13 deliverable = a NEW standalone corpus-explorer artifact (`dist/corpus/index.html` via `corpus.html`), NOT folded into the existing `index.html` engine. Honors the "keep the six-act arc + two wow beats" non-negotiable literally, protects the 3-typology showcase from pre-demo regression, and the derived-record shape (no lift/stats/anchor) fits a coverage→build-rec→signal view. Trade accepted: corpus.html duplicates the frozen theme CSS (two independent single-file artifacts). User chose standalone over fold-into-index.html | high | 2026-06-05 |
| Corpus scope = all 14 advisories shown in selection with HONEST status — the 2 already-derived are live/explorable, the other 12 show their --corpus extraction status (CLEAN/LOW/NEEDS) as "not yet derived", FATF advisories shown non-derivable. Tells the 14-corpus story without faking content; derivation scales as a follow-up. User chose this over "only the 2 derived" and "derive ~5 more first" | high | 2026-06-05 |
| Corpus view = a STAGED 4-screen flow (select → coverage → build-recs → signal-spec), NOT a single dense dashboard. The project is a vision-prototype-for-stakeholder-buy-in (pitch artifact), so staged theatre fits better than an analyst dashboard; reuses the existing act-staging muscle. User chose staged over dashboard | high | 2026-06-05 |
| build.py stays decoupled from the authoring layer: it reads committed data artifacts (corpus-status.json + derived/*.json) and never imports derive_signals.py; the deterministic status manifest is emitted by `derive_signals.py --corpus-status`. Preserves the standing "no authoring tool imported by engine or build.py" non-negotiable; build.py re-implements only a light renderable-shape check at its boundary | high | 2026-06-05 |
| Phase 12 direction = backend-only foundation (deterministic spine validated on ALL 14 advisories + LLM-backend derivation proven on a 2–3 slice); demo scope expansion deferred to Phase 13. User chose backend-only over folding a minimal selectable demo view into Phase 12 | high | 2026-06-05 |
| Destination = a SINGULAR corpus-backed demo where the user picks a FinCEN advisory (expand demo scope), NOT 14 separate demos. Per-advisory derivation records (`data/fincen/derived/*.json`) are the analytical artifact; the 3 hand-curated ship typologies stay the showcase | high | 2026-06-05 |
| LLM backend for derivation + build recommendation + build logic = THIS session, NOT an API-key `--draft` call. Deterministic spine (extract + schema/shape + build-rec consistency vs cover×data + traceability) is the dispose-boundary — LLM proposes, deterministic checks dispose | high | 2026-06-05 |

(Earlier Phase 7–11 decisions: see `[[phase-11-automated-derivation]]`, `[[phase-10-fincen-corpus-crawler]]`, `[[phase-08-doc-true-up]]` + journal. Load-bearing carry-overs: Phase 11 AUTOMATE → variant B (LLM-drafted signal NOW), boundary-preserving (LLM proposes a `.draft.json`; build.py + schema + 2 human gates dispose), two-layer authoring tool (deterministic stdlib `--selftest` + lazy-anthropic `--draft`, never a ship dep, never imported by engine/build.py); authoring-time vs ship-artifact split (build-time tools; ship file stays single-file/offline/no-fetch, HANDOFF §4/§4.5); validate at the build boundary (deterministic validator, fail loud); FinCEN-only verbatim public-domain exception (17 USC §105, NOT FINTRAC); lite ceremony.)

## Blockers and Open Questions

- [RESOLVED 2026-06-05 · planning] Phase-13 demo scope expansion → **a NEW standalone corpus-explorer artifact (`dist/corpus/index.html` via `corpus.html`), STAGED 4-screen flow (select → coverage → build-recs → signal-spec), all 14 advisories shown with HONEST status (2 derived live, the rest "not yet derived"/non-derivable)**. User chose standalone over fold-into-index.html (showcase byte-frozen); staged over a dense dashboard; all-14-honest over only-2-derived or derive-5-more-first. build.py reads committed data (corpus-status.json + derived/*.json), never imports derive_signals.py. Open sub-question, resolved at impl: can the Act-0 gauge / Act-2 matrix / Act-4 spec-card markup be re-implemented in corpus.html without an engine edit? Abort path = keep corpus.html fully standalone (re-implement the renderable component in its own CSS/JS), never touch index.html
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
