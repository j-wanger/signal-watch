# Project: AML Signal Engine — Vision Demo

> Last updated: 2026-06-04 by /dev-plan

## Recommended Next Action

**Phase 8 (M6 doc true-up + provenance fix) — ACTIVE, direction approved 2026-06-04; implementing.**
Closing the three doc/provenance debts deferred from Phase 7. Unifying thread: the always-loaded
docs must tell the truth about what the shipped artifact now is and cites. Doc/config-string ONLY —
the engine (`index.html`) is NOT touched.

Three defects: (1) **brand drift** — branded "Signal Engine" survives in CLAUDE.md/HANDOFF.md/
README.md/tests/smoke-checklist.md (the engine self-brands "Signal Watch"; smoke-checklist:31's
header check currently FAILS against the shipped artifact); (2) **stale non-negotiable** — the
"must be paraphrased" rule predates the verbatim-FinCEN render now live in Act 1, so amend it with
the FinCEN-only public-domain exception (17 USC §105, attributed, NOT FINTRAC); (3) **false fentanyl
provenance** — `FIN-2019-A006`/`FIN-2024-A002` get 0 hits in aml-wiki and were never the derivation
surface (the demo is FINTRAC-grounded), so remove them and attribute fentanyl solely to the FINTRAC
Jan-2025 Operational Alert. fentanyl.json content changes → rebuild dist/fentanyl (other two stay
byte-identical); `git diff index.html` must be empty.

(Phase 7 shipped, accepted, committed to main 2026-06-04 — the Signal Watch ingestion pipe proven
end to end on EFE FIN-2022-A002; target signal **S-DORMANT-DRAIN-ELDER**.)

## Active Phase

**[[phase-08-doc-true-up|Phase 8: Doc true-up + provenance fix]]** (status: active)

Entry criteria: MET (Phase 7 delivered + accepted; rebrand + verbatim render live in engine/dist,
but the always-loaded docs still describe the pre-M6 world; three debts explicitly deferred).
Exit criteria: no branded "Signal Engine" in the four docs → CLAUDE.md+HANDOFF carry the FinCEN-only
verbatim public-domain exception (17 USC §105, NOT FINTRAC) → unverifiable fentanyl FinCEN cites
removed (FINTRAC sole attribution) across config + docs → fentanyl dist rebuilt clean (guard 0
tokens, `node --check` PASS) → `git diff index.html` empty → only dist/fentanyl changed.

Progress: ~0% — 4 lite tasks planned (T1 rebrand · T2 non-negotiable amend · T3 provenance fix ·
T4 rebuild+verify); direction approved, implementing.

## Active Phase Contract

Phase: 8 - Doc true-up + provenance fix (M6 debt)
Tasks: 4 (see tasks.md) — T1 rebrand docs → T2 amend paraphrase non-negotiable (FinCEN-verbatim
exception) → T3 fix fentanyl provenance (FINTRAC only) → T4 rebuild fentanyl dist + verify
Transition: continue
Abort: if a fix surfaces a defect needing an engine/schema/config-structure change beyond the
doc/string slice — PAUSE and report. If blocked >3 attempts on a task, ask user: skip or abort.

## Recent Decisions

| Decision | Confidence | Date |
|----------|------------|------|
| Phase 8 fentanyl provenance fix = REMOVE the unverifiable FinCEN cites (FIN-2019-A006/FIN-2024-A002 — 0 hits in aml-wiki, never the derivation surface) and attribute fentanyl solely to the FINTRAC Jan-2025 Operational Alert (the verified, actually-used source). Honest attribution > chasing unverifiable cites — the project's own provenance thesis applied to its docs | high | 2026-06-04 |
| Doc H1 rebrand wording: "AML Signal Engine — Vision Demo" → "Signal Watch — AML Vision Demo" (product-name-first, matches the engine's "Signal Watch — AML …" ordering; keeps the docs' "Demo" word rather than the engine's "Prototype") | high | 2026-06-04 |
| Phase 8 scope correction: filed as "doc-only" but defect 3's false cite lives inside `config/typologies/fentanyl.json` (`anchor.source`) → the fix touches one config string + forces a dist/fentanyl rebuild. The engine (`index.html`) still stays untouched (diff empty) | high | 2026-06-04 |
| Phase 7 = thin vertical slice of the Signal Watch pipeline (acquire → PDF→MD persist → hand-derive one signal → render verbatim in Act 1) — prove the pipe on ONE item before widening the scraper or automating derivation (both explicitly LATER phases) | high | 2026-06-04 |
| Project identity pivot: "hand-authored scripted dramatization" → "public-data-seeded ingestion pipeline" whose demo output is the existing frontend, designed to later take real data; upgrades buy-in via provenance | high | 2026-06-04 |
| Non-negotiable relaxed for FinCEN ONLY: verbatim public-domain federal text (17 USC §105), attributed — NOT paraphrased. Does NOT extend to FINTRAC (Canadian Crown copyright). Needs CLAUDE.md/HANDOFF update (a doc task, not done this phase) | high | 2026-06-04 |
| Rebrand "Signal Engine" → "Signal Watch" (resolves the M5 OPEN product-name question) | high | 2026-06-04 |
| Slice advisory = FinCEN EFE FIN-2022-A002 (24 enumerated red flags = cleanest derivation; cheap to re-point at a higher-impact advisory like FIN-2025-A003 once the pipe is proven) | high | 2026-06-04 |
| Verbatim article renders in Act 1's existing SOURCE DOCUMENT panel, NOT Act 0 — reuses structure, strengthens the "agent reads the advisory" beat with the real document, spares the Act 0 blind-spot hook | high | 2026-06-04 |
| Authoring-time vs ship-artifact split is load-bearing: scraper/converter/derivation are build-time tools (output persisted + inlined); the ship artifact stays single-file, offline, zero runtime deps, no fetch (HANDOFF §4 / §4.5 hold) | high | 2026-06-04 |
| PROVENANCE DEFECT flagged (out of scope here): fentanyl.json anchor.source + CLAUDE.md cite FinCEN FIN-2019-A006/FIN-2024-A002, neither verifiable in aml-wiki; the existing fentanyl demo is actually FINTRAC-grounded. True-up is a separate doc task | medium | 2026-06-04 |
| Converter selected via quality checkpoint (markitdown MIT first, pymupdf4llm AGPL fallback), authoring-only, out of the ship file | medium | 2026-06-04 |
| M4 (live/pre-gen) skipped: pre-gen needs `fetch()` (breaks `file://`) — scripted IS the ship path | high | 2026-06-04 |
| Ship target = single self-contained `dist/<id>/index.html` per typology (old single `dist/index.html` retired) | high | 2026-06-04 |
| Validate config at the build boundary (build.py fails loud on schema violation) — deterministic validator at boundary | high | 2026-06-04 |
| Single source of truth = config JSON; index.html uses a `__CONFIG__` injection point (no inline duplicate) | high | 2026-06-04 |
| Lite ceremony (small single-artifact demo; HANDOFF says don't over-engineer) | high | 2026-06-04 |
| Ship target = single self-contained file; no ES modules/fetch (file:// trap) | settled | 2026-06-04 |

## Blockers and Open Questions

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

- [2026-06-04] M6 pipeline walking skeleton: proved the "Signal Watch" ingestion pipe end to end on ONE real FinCEN advisory. T1 `acquire_fincen.py` (stdlib urllib) → EFE FIN-2022-A002 PDF (824KB). T2 `pdf_to_md.py` markitdown (MIT) → `data/fincen/fin-2022-a002.md` (48KB, all 24 red flags intact; de-risk GATE passed, no fallback). Forced detour: homebrew py3.14 broken `pyexpat` → converter runs under a gitignored uv-managed py3.12 `.venv`; `build.py` stays stdlib. T3 new `advisory_full` first-class field (Act 1 SOURCE DOCUMENT panel: bounded scrollable + `.docsrc` attribution distinct from the illustrative badge; `text_file`→build-time inline keeps md as source of truth) + "Signal Engine"→"Signal Watch" rebrand (engine+dist). T4 hand-derived `elder-financial-exploitation.json` (target S-DORMANT-DRAIN-ELDER ← md line 507; all 12 financial red flags mapped, 12 behavioral excluded as non-data signals). T5 all 3 dist build clean, self-contained guard 0 tokens, `node --check` PASS. NOT committed yet; doc rebrand + provenance true-up deferred to a follow-up phase.
- [2026-06-04] M5 ship: doc/verify only (zero engine/config edits — `index.html`+`config/`+`scripts/` clean). Parameterized `tests/smoke-checklist.md` per typology (removed stale single-file `dist/index.html` path; per-typology fill table for the 6 values that differ; M3 controls moved deferred→active checks). Refreshed README (M2→ship; shipped M3 controls; both-typology compliance). Compliance + offline `file://` **HARD GATE PASS**: zero drift (`build.py all` byte-identical, `git status dist/` clean), badge both, self-contained (no fetch/external script; only Google Fonts), advisories paraphrased+attributed, no secrets/PII. M4 skipped (inert under file://). Runtime render carries from M3 (byte-identical dist; no fresh browser run this session). Committed to main.
- [2026-06-04] M3 presenter polish: engine-only — centralized nav (advance/back/reset) + keys (←/→/Space/Esc) reusing the gate logic via the `nextBtn.disabled` guard; ↺ reset control; `prefers-reduced-motion` final-state (CSS @media + synchronous `T()`/`animVal`). Verified both shipped dist × both motion modes (gates hold, no Act 5 without confirm, 0 pending timers reduced); real Chrome 149 renders. `config/`+`build.py` byte-identical. Speaker notes deferred.
- [2026-06-04] M2 multi-typology: added trade-based.json (TBML) from aml-wiki survey, paraphrased; build.py gained per-typology dist + build-boundary validation. TBML verified; engine untouched (zero index.html diff); fentanyl regression byte-identical.
- [2026-06-04] M1 config-driven refactor: schema + fentanyl.json extracted; engine genericized (`__CONFIG__` injection, literals promoted); defensive rendering; stdlib build. Verified byte-identical act HTML to baseline; baseline archived.

## Cross-References

- HANDOFF.md · CLAUDE.md · README.md
- Knowledge wiki: **aml-wiki** (registered central store) — domain reference for typologies,
  indicators, FINTRAC/FinCEN/E-23. Linked via gitignored `wiki/` symlink; query with `/wiki-query`.
