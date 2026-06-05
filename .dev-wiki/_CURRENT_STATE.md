# Project: Signal Watch — AML Vision Demo

> Last updated: 2026-06-05 by /dev-plan

## Recommended Next Action

**Phase 10 (FinCEN corpus crawler — SCALE) — DELIVERED, accepted, committed to main `0c87c47`
(2026-06-05). Gate flip in the follow-up commit.**
The static 1-entry `REGISTRY` is now a generated manifest `data/fincen/index.json` (14 advisories),
built by a new authoring-only `crawl_fincen.py` (pure `parse_index` + offline `--selftest`/`--write`,
thin live `--fetch`). `acquire_fincen.py` reads the manifest, resolving each advisory's PDF from its
detail page, EFE kept as a zero-hop direct-PDF override (backward-compatible). Widened pipe proven on
a live batch (`fin-2021-a004` 672KB→34KB/15 indicators, `fin-2024-a002` 565KB→56KB/14 — batch
artifacts deleted per user call, regenerable). Determinism held: committed manifest is
`parse_index(saved_fixture)`, re-`--write` → no diff. Engine/ship untouched (`git diff index.html`
empty), `build.py --check all` zero drift.

**Next — project between phases.** Plan the next increment with `/dev-plan`. Open forks:
**elder presentation-values true-up** (carried from Phase 9; smoke-checklist still 2 of 3 typologies),
**automate article→signal derivation** (AUTOMATE — the last M6 vision increment; manifest + corpus md
are now a derivation surface), **re-point fentanyl to the now-discoverable `fin-2024-a002` Supplemental
Fentanyl Advisory** (verbatim upgrade), and optional manifest `--fetch` refresh cadence. Push to main
pending the user's separate OK.

**Phase 9 (Build-drift guard) — DELIVERED, accepted, committed to main `33db22a` (2026-06-05).**
The Phase-7 silent-drift failure mode is now a one-command `build.py --check [all|<id>]` guard.

## Active Phase

**[[phase-10-fincen-corpus-crawler|Phase 10: FinCEN corpus crawler (SCALE)]]** (status: completed)

Entry criteria: MET — Phase 9 delivered + accepted (commit 33db22a). M6 pipeline thesis proven
(Phase 7) + guarded (Phase 9); `acquire_fincen.py` carries a static 1-entry `REGISTRY` whose docstring
defers the crawler to "a LATER phase". User chose SCALE over the smaller elder true-up at the gate.
Exit criteria: `crawl_fincen.py` (authoring-only, stdlib) discovers the index → committed
`data/fincen/index.json` (reproducible offline via `--selftest`/`parse_index(fixture)`);
`acquire_fincen.py` reads the manifest (EFE fallback merged, backward-compatible); widened pipe proven
on a bounded batch; crawler documented in docstrings + README + CLAUDE; `git diff index.html` empty;
`raw/` still gitignored, no bulk-md commit.

Progress: 100% — all 4 tasks complete; delivery accepted, committed to main `0c87c47` (2026-06-05).

## Active Phase Contract

Phase: 10 - FinCEN corpus crawler (SCALE)
Tasks: 4 (see tasks.md) — T1 discovery probe + saved fixture · T2 `crawl_fincen.py` pure parser +
`--selftest` + manifest writer · T3 wire `acquire_fincen.py` to the manifest (EFE fallback) ·
T4 bounded batch proof + docs. Sizes S/M/S/S (T2 = M).
Transition: continue (lite). May benefit from a fresh session at T2 if context is long.
Abort: if FinCEN's index can't be deterministically parsed from a saved page (JS-rendered / auth /
anti-scraping) — PAUSE, report, pivot to a hand-curated manifest. Blocked >3 attempts → ask user: skip or abort.

## Recent Decisions

| Decision | Confidence | Date |
|----------|------------|------|
| Phase 10 direction = SCALE (FinCEN corpus crawler), chosen by the user over the smaller elder presentation-values true-up (which stays a Future-phase candidate). Overrides the planner's finish-before-scale recommendation — the user wants to grow the M6 vision next | high | 2026-06-05 |
| Crawler scope = discovery-manifest + bounded batch, NOT mass-download. "Crawl all" ≠ "download all": the ship artifact is unchanged, so the reusable/testable/low-bloat core is the generated `data/fincen/index.json` manifest; downloading hundreds of PDFs adds git+network cost without improving the demo. Mirrors Phase-7 (prove the pipe on a bounded set) + Phase-9 YAGNI | high | 2026-06-05 |
| Crawler determinism split = pure `parse_index(html)` (offline, `--selftest` against a saved fixture — Phase-9 `build.py --check` ethos) + a thin live `fetch_index()` shell (manual authoring, never in smoke/CI). Committed `index.json` is produced by `parse_index(saved_fixture)`, reproducible offline — keeps non-deterministic network out of committed state, honoring deterministic-validators-at-boundaries | high | 2026-06-05 |
| Repo-hygiene rails held: `data/fincen/raw/` stays gitignored (PDFs regenerable); commit the manifest + only the md actually derived from (no bulk-md commit); `acquire_fincen.py` keeps the static EFE entry as a merged fallback so `fin-2022-a002` stays backward-compatible; stdlib-only crawler (no requests/bs4) | high | 2026-06-05 |
| Phase 9 direction = HARDEN (build-drift guard) before SCALE (FinCEN crawler) or AUTOMATE (article→signal derivation). The M6 pipeline thesis is already proven by the Phase-7 walking skeleton; a corpus crawler / automated derivation don't earn their complexity for a ~3-typology demo, and automated derivation risks pulling a neural judge toward the build boundary (against deterministic-validators-at-boundaries). The guard closes a real Phase-7 invariant breach and is cheap | high | 2026-06-05 |
| Guard mechanism = in-process `build.py --check` (render + byte-compare vs committed dist), NOT `build.py all && git diff --exit-code dist/`. Non-mutating (doesn't dirty the tree to test), git-agnostic (build.py stays pure-stdlib, works outside a checkout), per-typology drift report. `git status --porcelain dist/` documented in the smoke-checklist as the complement (catches untracked stray dist files `--check` won't) | high | 2026-06-05 |
| Keep committing built `dist/` (rejected gitignore-dist + build-in-CI). The committed single file IS the deliverable — must open straight from the repo, offline, no Python. So guard the invariant rather than dissolve it | high | 2026-06-05 |
| Pre-commit hook / CI enforcement explicitly DEFERRED (lite ceremony + HANDOFF "don't over-engineer"). The runnable `--check` + smoke-checklist is the home; a pre-commit hook running `--check` is a clean follow-up if wanted later | medium | 2026-06-05 |

(Earlier Phase 7–8 decisions: see `[[phase-08-doc-true-up]]` + the 2026-06-04 journal entries.)
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

- [RESOLVED 2026-06-05 · planning] Phase-10 increment → **SCALE: FinCEN corpus crawler** (user chose over the smaller elder presentation-values true-up at the direction gate). Scoped to discovery-manifest + bounded batch, NOT mass-download. Elder true-up + automate-derivation stay Future-phase candidates
- [OPEN · phase-10] Is FinCEN's advisories index server-rendered + deterministically scrapeable from a saved page? Resolved by the T1 probe; abort path = hand-curated manifest if not (raised 2026-06-05)
- [RESOLVED 2026-06-05 · planning] Next-increment direction → **HARDEN (Phase 9 build-drift guard)** before SCALE (FinCEN crawler) or AUTOMATE (derivation). Closes a real Phase-7 invariant breach cheaply; the two SCALE/AUTOMATE increments stay in Future phases
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

- [2026-06-05] [[2026-06-05-phase-10-fincen-corpus-crawler|Phase 10 FinCEN corpus crawler (SCALE)]] (lite, 4 tasks, READY FOR COMPLETION — delivery gate pending) — widened the authoring scraper from a 1-entry stub to the discovered FinCEN advisory corpus. New authoring-only `crawl_fincen.py` (pure `parse_index` per-`<tr>` extraction → id/title/`<time>`-ISO-date; `--selftest`/`--write`/`--list`/`--fetch`) generates `data/fincen/index.json` (14 advisories). `acquire_fincen.py` REGISTRY→manifest with `resolve_pdf` detail-page hop + EFE direct-PDF zero-hop override (backward-compatible). DISCOVERY (T1): listing yields detail-page URLs not PDF URLs (filenames unpredictable — batch proved it: `…Ransomware…_508_.pdf` vs `…Fentanyl-508C.pdf`); detail→PDF resolution at acquire time keeps the committed manifest deterministic (`parse_index(saved_fixture)`, re-write→no diff). Widened pipe proven live on `fin-2021-a004` (34KB md/15 indicators) + `fin-2024-a002` (56KB md/14); batch artifacts deleted per user call (regenerable). User chose SCALE over the elder true-up at the direction gate. Stdlib-only crawler+acquire; engine untouched; `build.py --check all` zero drift. Docs in README + CLAUDE.
- [2026-06-05] [[2026-06-05-phase-09-build-drift-guard|Phase 9 build-drift guard]] (lite, 3 tasks, COMPLETED + accepted, committed `33db22a`) — turned the M5 zero-drift invariant into a runnable, non-mutating guard. `build.py` refactored: `build_one` split into `render_one(typ, template) -> str` (the SINGLE source of truth for a typology's dist bytes) + thin writer; new `check_one` (git-agnostic byte-compare of committed dist vs fresh in-memory render, per-typology verdict, invalid-config = per-typology FAIL) + `resolve_targets`; `main` gained `--check [all|<id>]`. Wired into smoke-checklist (de-staled "both dist"→3 typologies; `git status --porcelain dist/` complement noted) + documented in docstring + README. Build byte-DETERMINISTIC (built twice → identical sha), HEAD dist == fresh build, `node --check` PASS ×3, `git diff index.html` empty, zero config edits → all 3 dist byte-identical. Discovered Phase 10 candidate: elder presentation-values true-up in the smoke-checklist.
- [2026-06-04] Phase 8 doc true-up + provenance fix (M6 debt) — doc/config-string only, engine untouched, committed `042d732`. Rebrand `Signal Engine`→`Signal Watch` (4 docs; fixed a smoke-checklist header check that had been failing vs the shipped brand). Paraphrase non-negotiable amended with the FinCEN-only verbatim public-domain exception (17 USC §105, NOT FINTRAC) in CLAUDE+HANDOFF §4.4. Fentanyl provenance: removed unverifiable `FIN-2019-A006`/`FIN-2024-A002` (0 hits in aml-wiki, never the derivation surface), attributed solely to FINTRAC Jan-2025 — reframing sweep caught 2 extra bad-cite sites in smoke-checklist. M6 doc staleness folded in (user add): CLAUDE M2→M6 + pipeline + 3 typologies; README M5→M6 + elder + verbatim exception. DISCOVERY: rebuild exposed Phase 7 committed STALE `dist/{fentanyl,trade-based}` (missing engine highlights feature; only elder current) → `build.py all` didn't reproduce committed dist, M5 zero-drift invariant had broken; all fresh dist staged (user-approved), invariant restored. Guard 0 tokens ×3, `node --check` PASS ×3, `git diff index.html` empty.
- [2026-06-04] M6 pipeline walking skeleton: proved the "Signal Watch" ingestion pipe end to end on ONE real FinCEN advisory. T1 `acquire_fincen.py` (stdlib urllib) → EFE FIN-2022-A002 PDF (824KB). T2 `pdf_to_md.py` markitdown (MIT) → `data/fincen/fin-2022-a002.md` (48KB, all 24 red flags intact; de-risk GATE passed, no fallback). Forced detour: homebrew py3.14 broken `pyexpat` → converter runs under a gitignored uv-managed py3.12 `.venv`; `build.py` stays stdlib. T3 new `advisory_full` first-class field (Act 1 SOURCE DOCUMENT panel: bounded scrollable + `.docsrc` attribution distinct from the illustrative badge; `text_file`→build-time inline keeps md as source of truth) + "Signal Engine"→"Signal Watch" rebrand (engine+dist). T4 hand-derived `elder-financial-exploitation.json` (target S-DORMANT-DRAIN-ELDER ← md line 507; all 12 financial red flags mapped, 12 behavioral excluded as non-data signals). T5 all 3 dist build clean, self-contained guard 0 tokens, `node --check` PASS. NOT committed yet; doc rebrand + provenance true-up deferred to a follow-up phase.
- [2026-06-04] M5 ship: doc/verify only (zero engine/config edits — `index.html`+`config/`+`scripts/` clean). Parameterized `tests/smoke-checklist.md` per typology (removed stale single-file `dist/index.html` path; per-typology fill table for the 6 values that differ; M3 controls moved deferred→active checks). Refreshed README (M2→ship; shipped M3 controls; both-typology compliance). Compliance + offline `file://` **HARD GATE PASS**: zero drift (`build.py all` byte-identical, `git status dist/` clean), badge both, self-contained (no fetch/external script; only Google Fonts), advisories paraphrased+attributed, no secrets/PII. M4 skipped (inert under file://). Runtime render carries from M3 (byte-identical dist; no fresh browser run this session). Committed to main.
## Cross-References

- HANDOFF.md · CLAUDE.md · README.md
- Knowledge wiki: **aml-wiki** (registered central store) — domain reference for typologies,
  indicators, FINTRAC/FinCEN/E-23. Linked via gitignored `wiki/` symlink; query with `/wiki-query`.
