# Project: Signal Watch — AML Vision Demo

> Last updated: 2026-06-05 by /dev-debrief (Phase 11 — automated derivation)

## Recommended Next Action

**Phase 11 (Automated derivation — LLM-drafted signal config) — DELIVERED + accepted (2026-06-05).**
The article→signal derivation proven MANUALLY in Phase 7 (EFE md → hand-derived elder config) is now
automated by authoring-only `scripts/derive_signals.py`: a **deterministic layer** (`extract_red_flags`
+ `scaffold_config`, stdlib, `--selftest`/`--scaffold`, offline — `--selftest` extracts the 24 EFE red
flags, 12 behavioral + 12 financial) + a **neural layer** (`--draft`, env-keyed, `anthropic` LAZY from
the authoring venv) that PROPOSES the judgment fields (status, the one `target:true`, the signal
`definition`) via the Anthropic API. **Boundary preserved:** the LLM proposes a `.draft.json`; build.py
+ schema + the two human gates DISPOSE (build.py rejects the bare skeleton naming the 2 judgment gaps,
accepts a filled draft). Engine/ship untouched (`git diff index.html` empty); `build.py --check all`
zero drift. **Review gate 9/10 accept** — the Anthropic structured-output shape (claude-opus-4-8 +
`output_config.format` json_schema) verified against the **claude-api reference** (not guessed); 2
MEDIUM `--draft`-path fixes folded in pre-commit (adaptive thinking + `effort:high`; graceful
refusal/max_tokens handling). The live network call stays unexercised (no key) — recorded-manual-run
pattern. **M6 vision arc (Phases 7–11) complete.**

**No next phase planned — run `/dev-plan`** to pick the next increment. Backlog candidates (all
deprioritized at the Phase-11 gate, NOT dropped): **run `--draft` end-to-end on a NEW advisory with a
real key** (the pipe is proven key-free; the manifest carries 14 advisories) · **elder
presentation-values true-up** (smoke-checklist walk-row, carried from Phase 9) · **fentanyl re-point**
to the manifest-discoverable `fin-2024-a002` · optional **manifest `--fetch` cadence**.

**Carried context:** Phase 10 (FinCEN corpus crawler — SCALE) committed `0c87c47`; Phase 9
(build-drift guard) committed `33db22a` — both accepted (2026-06-05).

## Active Phase

**[[phase-11-automated-derivation|Phase 11: Automated derivation (LLM-drafted signal config)]]** (status: active)

Entry criteria: MET — M6 pipeline proven (Phase 7 manual EFE derivation) + guarded (Phase 9) +
scaled (Phase 10 corpus manifest); the manual article→signal step is the remaining M6 vision increment.
User chose AUTOMATE over the elder true-up AND the fentanyl re-point at the direction gate, then chose
variant B (LLM-drafted definition NOW) over A (deterministic scaffolder only) — both USER OVERRIDES.
Exit criteria: `derive_signals.py --selftest` extracts the known EFE red-flag counts (deterministic,
offline) · `--scaffold` emits a schema-shaped `<id>.draft.json` skeleton (line-traced, no target/
definition) · `--draft` (env-keyed, anthropic lazy from the authoring venv) proposes the judgment
fields incl. a schema-valid signal `definition`, grounded on red flags + schema + few-shot · the draft
round-trips the deterministic boundary (build.py/schema accept a human-reviewed valid config OR reject
an invalid one) · `git diff index.html` empty; deterministic layer stdlib-only; anthropic import LAZY;
tool absent from engine/build imports; ship artifact never calls an LLM · documented in docstring +
README + CLAUDE.

Progress: ~0% — planned, direction approved; 5 tasks, none started.

## Active Phase Contract

Phase: 11 - Automated derivation (LLM-drafted signal config)
Tasks: 5 (see tasks.md) — T1 pure `extract_red_flags` + `--selftest` (M) · T2 pure `scaffold_config`
+ `--scaffold` write (M) · T3 LLM `draft_definition` + `--draft` mode (L) · T4 end-to-end proof +
boundary check (S) · T5 docs (S).
Transition: continue (lite). T3 (the single L) consults the **claude-api reference** for the current
model id + Anthropic SDK + structured-output/tool-use — may benefit from a fresh session.
Abort: if the LLM can't be coaxed to schema-valid output build.py accepts (after consulting claude-api)
— fall back to variant A (deterministic scaffolder only; human fills judgment). If red flags can't be
deterministically anchored — thinner section-bounded capture. Blocked >3 attempts → ask user: skip or abort.

## Recent Decisions

| Decision | Confidence | Date |
|----------|------------|------|
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

- [2026-06-05] [[2026-06-05-phase-11-automated-derivation|Phase 11 Automated derivation (LLM-drafted signal config)]] (lite, 5 tasks, DELIVERED + accepted) — automated the Phase-7 manual article→signal step in authoring-only `derive_signals.py`: deterministic `extract_red_flags`/`scaffold_config` (`--selftest` extracts 24 EFE flags offline, stdlib-only; form-feed `split("\n")` fix keeps md-line traceability) + neural `--draft` (lazy `anthropic`, env-keyed) PROPOSING status/the-one-target/the-signal-`definition` via the Anthropic API (claude-opus-4-8 + `output_config.format` json_schema, verified vs the **claude-api reference**, not guessed). Boundary preserved: LLM proposes a gitignored `.draft.json`; build.py + schema + 2 human gates DISPOSE (rejects the bare skeleton naming the 2 judgment gaps, accepts a filled draft). Review gate **9/10 accept**; 2 MEDIUM `--draft`-path fixes folded in (adaptive thinking + `effort:high`; refusal/max_tokens handling). Engine/ship untouched; `--check all` zero drift. **M6 vision arc (Phases 7–11) complete.**
- [2026-06-05] [[2026-06-05-phase-10-fincen-corpus-crawler|Phase 10 FinCEN corpus crawler (SCALE)]] (lite, 4 tasks, COMPLETED + accepted, committed `0c87c47`) — widened the authoring scraper from a 1-entry stub to the discovered FinCEN corpus. New authoring-only `crawl_fincen.py` (pure `parse_index` → `data/fincen/index.json`, 14 advisories; `--selftest`/`--write`/`--list`/`--fetch`); `acquire_fincen.py` REGISTRY→manifest + `resolve_pdf` detail-page hop + EFE direct-PDF zero-hop override. Discovery over mass-download; detail→PDF resolution keeps the committed manifest deterministic. Widened pipe proven on a 2-advisory batch (deleted per user call). Stdlib-only; engine untouched; `--check all` zero drift.
- [2026-06-05] [[2026-06-05-phase-09-build-drift-guard|Phase 9 build-drift guard]] (lite, 3 tasks, COMPLETED + accepted, committed `33db22a`) — turned the M5 zero-drift invariant into a runnable, non-mutating guard. `build.py` refactored: `build_one` split into `render_one(typ, template) -> str` (the SINGLE source of truth for a typology's dist bytes) + thin writer; new `check_one` (git-agnostic byte-compare of committed dist vs fresh in-memory render, per-typology verdict, invalid-config = per-typology FAIL) + `resolve_targets`; `main` gained `--check [all|<id>]`. Wired into smoke-checklist (de-staled "both dist"→3 typologies; `git status --porcelain dist/` complement noted) + documented in docstring + README. Build byte-DETERMINISTIC (built twice → identical sha), HEAD dist == fresh build, `node --check` PASS ×3, `git diff index.html` empty, zero config edits → all 3 dist byte-identical. Discovered Phase 10 candidate: elder presentation-values true-up in the smoke-checklist.
- [2026-06-04] Phase 8 doc true-up + provenance fix (M6 debt) — doc/config-string only, engine untouched, committed `042d732`. Rebrand `Signal Engine`→`Signal Watch` (4 docs; fixed a smoke-checklist header check that had been failing vs the shipped brand). Paraphrase non-negotiable amended with the FinCEN-only verbatim public-domain exception (17 USC §105, NOT FINTRAC) in CLAUDE+HANDOFF §4.4. Fentanyl provenance: removed unverifiable `FIN-2019-A006`/`FIN-2024-A002` (0 hits in aml-wiki, never the derivation surface), attributed solely to FINTRAC Jan-2025 — reframing sweep caught 2 extra bad-cite sites in smoke-checklist. M6 doc staleness folded in (user add): CLAUDE M2→M6 + pipeline + 3 typologies; README M5→M6 + elder + verbatim exception. DISCOVERY: rebuild exposed Phase 7 committed STALE `dist/{fentanyl,trade-based}` (missing engine highlights feature; only elder current) → `build.py all` didn't reproduce committed dist, M5 zero-drift invariant had broken; all fresh dist staged (user-approved), invariant restored. Guard 0 tokens ×3, `node --check` PASS ×3, `git diff index.html` empty.

(Earlier entries — M6 pipeline walking skeleton, M5 ship, M3/M2/M1 — see `index.md` journal list + their journal articles. Trimmed to last 4 per the _CURRENT_STATE size budget.)

## Cross-References

- HANDOFF.md · CLAUDE.md · README.md
- Knowledge wiki: **aml-wiki** (registered central store) — domain reference for typologies,
  indicators, FINTRAC/FinCEN/E-23. Linked via gitignored `wiki/` symlink; query with `/wiki-query`.
