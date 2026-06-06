# Project: Signal Watch — AML Vision Demo

> Last updated: 2026-06-05 by /dev-debrief (Phase 13 — corpus explorer DELIVERED)

## Recommended Next Action

**Phase 13 (Corpus explorer) DELIVERED — READY FOR COMPLETION; run `/dev-plan` for Phase 14.** All 5 tasks
[x], all exit criteria met. The M7 payoff shipped: a NEW standalone ship artifact `dist/corpus/index.html`
(built from `corpus.html`) — a FinCEN CORPUS EXPLORER where a stakeholder picks 1 of 14 advisories and
watches the loop derive coverage → per-indicator build recommendations → signal spec, in a STAGED 4-screen
flow (SELECT → COVERAGE → BUILD RECOMMENDATIONS → SIGNAL SPEC). All 14 shown with HONEST status (2 derived
live; the other 12 show their --corpus CLEAN/LOW/NEEDS status as "not yet derived"). `derive_signals.py
--corpus-status` emits the committed `data/fincen/corpus-status.json` (14 entries + 7-clean/3-low/4-needs
summary). build.py gained render/build/check_corpus + a fail-loud corpus-data boundary validator + the
"corpus" target (now 4 artifacts in `all` / `--check all`) and stays DECOUPLED — never imports
derive_signals.py. The six-act `index.html`, the 3 typology configs, and their dists stayed BYTE-FROZEN.
Review gate 9/10 ACCEPT (one MEDIUM esc()-quote-escaping fix folded in). Impl commit `54516d4` landed; a
small post-review esc() fix to corpus.html + dist/corpus is uncommitted in the tree.

**Phase 14 candidates (run `/dev-plan`):** scale LLM-backend derivation to the ~5 remaining CLEAN advisories
(fuller live menu) · glued-list splitting in `extract_red_flags` for the 3 LOW advisories · explicitly
exclude/label the 2 FATF advisories in the derivable set · (carried) elder presentation-values true-up ·
fentanyl verbatim re-point · manifest `--fetch` cadence · (optional) a corpus combination-lift "wow" beat.
**Carried:** M6 vision arc (Phases 7–11) + M7 (Phases 12–13) complete; the 3 hand-curated typologies stay
the byte-frozen showcase.

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

- [2026-06-05] [[2026-06-05-phase-13-corpus-explorer|Phase 13 Corpus explorer — THE PAYOFF (M7)]] (lite, 5 tasks, DELIVERED — READY FOR COMPLETION) — rendered the Phase-12 derived records as a NEW standalone ship artifact `dist/corpus/index.html` (from `corpus.html`): a FinCEN CORPUS EXPLORER, STAGED 4-screen flow (SELECT → COVERAGE → BUILD RECOMMENDATIONS → SIGNAL SPEC), all 14 advisories with HONEST status (2 derived live, 12 "not yet derived" by --corpus status). T1 `derive_signals.py --corpus-status` → committed `corpus-status.json` (14 entries, 7-clean/3-low/4-needs summary; shared `_section_counts`/`_load_index` helpers, stdlib-only, anthropic lazy). T2 (the L) `corpus.html` — own copy of the dossier theme CSS (showcase byte-frozen), `__CORPUS__` injection, staged render JS, reduced-motion + keyboard parity, always-on illustrative badge, defensive rendering. T3 build.py `render/build/check_corpus` + `validate_corpus_data` (fail-loud: build_rec ∈ enum; BUILD_NOW ⇒ full build_logic) + "corpus" target, folded into `all`/`--check all` (now 4 artifacts); build.py NEVER imports derive_signals.py (only comment/hint mentions). T4 built end-to-end + 17 headless DOM-shim assertions + 3 browser screenshots. T5 README + CLAUDE docs, milestone → M7. Review 9/10 ACCEPT (one MEDIUM esc() quote-escaping FIXED inline + rebuilt). `index.html` + `config/**` + 3 typology dists byte-untouched; `--check all` 4-artifact zero drift; `--selftest` still 12+12; both derived records `--check-derived` clean. Impl commit `54516d4`.
- [2026-06-05] [[2026-06-05-phase-12-fincen-corpus-derivation|Phase 12 FinCEN corpus derivation foundation (M7)]] (lite, 5 tasks + 2 user refinement passes, DELIVERED) — backend for a singular corpus-backed FinCEN demo (user picks 1 of 14 advisories). Committed the full 14-advisory corpus md; rewrote `extract_red_flags` as a corpus-wide **section-FINDER** (Tier-1 clean anchors + a Tier-2 loose-header/weak-intro fallback used only when Tier-1 is empty — EFE untouched; + intro-noise/header-block/citation filters). `--corpus` → **7 CLEAN · 3 LOW · 4 NEEDS** (2 NEEDS = FATF jurisdiction advisories = correct). Deterministic checks `build_rec_category` (cover×data matrix) + `check_record` (consistency + traceability + BUILD_NOW⇒logic) in `--selftest`. LLM backend = THIS session (no key) derived 2 records (kleptocracy 5-ind/2-BUILD_NOW + PRC precursors 14-ind/4-BUILD_NOW), each `--check-derived` clean; boundary holds (tampered record rejected). RECORDED: the spine ASSISTS but does not AUTOMATE — complete records need LLM-backend authoring. EFE still 12+12; `index.html`/`build.py`/`schema` untouched; `--check all` zero drift. Opens M7.
- [2026-06-05] [[2026-06-05-phase-11-automated-derivation|Phase 11 Automated derivation (LLM-drafted signal config)]] (lite, 5 tasks, DELIVERED + accepted) — automated the Phase-7 manual article→signal step in authoring-only `derive_signals.py`: deterministic `extract_red_flags`/`scaffold_config` (`--selftest` extracts 24 EFE flags offline, stdlib-only; form-feed `split("\n")` fix keeps md-line traceability) + neural `--draft` (lazy `anthropic`, env-keyed) PROPOSING status/the-one-target/the-signal-`definition` via the Anthropic API (claude-opus-4-8 + `output_config.format` json_schema, verified vs the **claude-api reference**, not guessed). Boundary preserved: LLM proposes a gitignored `.draft.json`; build.py + schema + 2 human gates DISPOSE (rejects the bare skeleton naming the 2 judgment gaps, accepts a filled draft). Review gate **9/10 accept**; 2 MEDIUM `--draft`-path fixes folded in (adaptive thinking + `effort:high`; refusal/max_tokens handling). Engine/ship untouched; `--check all` zero drift. **M6 vision arc (Phases 7–11) complete.**
- [2026-06-05] [[2026-06-05-phase-10-fincen-corpus-crawler|Phase 10 FinCEN corpus crawler (SCALE)]] (lite, 4 tasks, COMPLETED + accepted, committed `0c87c47`) — widened the authoring scraper from a 1-entry stub to the discovered FinCEN corpus. New authoring-only `crawl_fincen.py` (pure `parse_index` → `data/fincen/index.json`, 14 advisories; `--selftest`/`--write`/`--list`/`--fetch`); `acquire_fincen.py` REGISTRY→manifest + `resolve_pdf` detail-page hop + EFE direct-PDF zero-hop override. Discovery over mass-download; detail→PDF resolution keeps the committed manifest deterministic. Widened pipe proven on a 2-advisory batch (deleted per user call). Stdlib-only; engine untouched; `--check all` zero drift.

(Earlier entries — Phase 9 build-drift guard, Phase 8 doc true-up, M6 pipeline walking skeleton, M5 ship, M3/M2/M1 — see `index.md` journal list + their journal articles. Trimmed to last 5 per the _CURRENT_STATE size budget.)

## Cross-References

- HANDOFF.md · CLAUDE.md · README.md
- Knowledge wiki: **aml-wiki** (registered central store) — domain reference for typologies,
  indicators, FINTRAC/FinCEN/E-23. Linked via gitignored `wiki/` symlink; query with `/wiki-query`.
