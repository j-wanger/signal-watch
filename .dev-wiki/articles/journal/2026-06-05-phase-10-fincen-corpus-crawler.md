---
title: "Phase 10: FinCEN corpus crawler (SCALE)"
aliases: []
category: journal
tags: [milestone-m6, authoring-pipeline, crawler, manifest, scale, fincen]
parents: [phase-10-fincen-corpus-crawler]
created: 2026-06-05
updated: 2026-06-05
source: debrief
duration: ~60min
---

# Phase 10: FinCEN corpus crawler (SCALE)

Widened the authoring scraper from one hand-registered advisory to the discovered FinCEN advisory
corpus. The static 1-entry `REGISTRY` in `acquire_fincen.py` is now a generated manifest
`data/fincen/index.json` (14 advisories), produced by a new authoring-only `crawl_fincen.py`. Core =
DISCOVERY, not mass-download. Authoring-only; engine/ship artifact untouched (`git diff index.html`
empty), `dist/` zero-drift. Lite ceremony, one session, all 4 tasks complete. READY FOR COMPLETION.

## What Happened

- **T1 — discovery probe + saved fixture.** Located the FinCEN advisories listing
  (`/resources/advisoriesbulletinsfact-sheets/advisories`), fetched it the way `acquire_fincen.py`
  does (urllib + browser UA), saved a provenance-stamped fixture to `tests/fixtures/fincen-index.html`
  (49KB, server-rendered HTML table, 14 advisories incl. the EFE anchor). Abort rail (JS-rendered /
  auth / anti-scraping → hand-curated manifest) never triggered.
- **T2 — `crawl_fincen.py` (new, authoring-only, stdlib).** Pure `parse_index(html) -> [entries]`
  (per-`<tr>` extraction: advisory link → id from slug, descriptive subject column → title,
  `<time datetime>` → ISO date; sorted-by-id determinism; EFE `setdefault` guarantee). Modes:
  `--selftest` (offline assert against the fixture — Phase-9 `build.py --check` ethos), `--write`
  (manifest from the saved fixture, reproducible offline), `--list`, `--fetch` (thin live shell to
  refresh the fixture, manual authoring only). `--selftest` → 14 entries, 0 malformed, exit 0.
- **T3 — wire `acquire_fincen.py` to the manifest.** `load_manifest()` reads `index.json` (id →
  detail-page url); `DIRECT_PDF` overrides keep the EFE anchor zero-hop with its canonical URL
  byte-preserved (backward-compatible); `resolve_pdf(detail_url)` does the detail-page → PDF hop for
  manifest-only ids. `--list` shows 14 ids, EFE tagged `[direct-pdf]`. Stdlib-only preserved.
- **T4 — bounded batch proof + docs.** Live batch (`fin-2021-a004`, `fin-2024-a002`) exercised the
  new `resolve_pdf` hop end-to-end: 672KB→34KB md/15 indicator hits, 565KB→56KB md/14 hits. Crawler
  + generated-manifest model documented in both docstrings + README authoring section + CLAUDE
  "Current state". Batch artifacts deleted per user call (proof in-record, regenerable).

## Decisions Made

(Captured in `_CURRENT_STATE` ## Recent Decisions at plan time — lite ceremony writes no decision
articles.) Direction = **SCALE (crawler) over the elder true-up**, user override of the planner's
finish-before-scale rec; scope = **discovery-manifest + bounded batch, NOT mass-download**;
**determinism split** (pure `parse_index` + `--selftest` offline / thin live `fetch`); repo-hygiene
rails (`raw/` gitignored, no bulk-md commit, EFE direct-PDF fallback). In-session: batch md **deleted**
(user call) rather than committed.

## Problems Solved

- **Unpredictable PDF filenames.** The listing yields detail-page URLs, not PDF URLs — the batch
  proved why: `…Ransomware%20Advisory_FINAL_508_.pdf` vs `…Supplemental-Advisory-on-Fentanyl-508C.pdf`,
  two unguessable formats. Solved by a detail-page → PDF resolution hop at acquire time (T1 DISCOVERY
  escape-hatch; refined T2/T3 scope), keeping the committed manifest deterministic (detail URLs only).
- **Network non-determinism vs committed state.** The committed manifest is `parse_index(saved_fixture)`,
  not a live crawl — verified reproducible (re-`--write` → no diff). Live network stays in the manual
  `--fetch`/acquire shells, never in smoke/CI.

## Artifacts Changed

- `scripts/crawl_fincen.py` (NEW — pure parser + `--selftest`/`--write`/`--list`/`--fetch`)
- `data/fincen/index.json` (NEW — 14-advisory manifest)
- `tests/fixtures/fincen-index.html` (NEW — provenance-stamped parser fixture)
- `scripts/acquire_fincen.py` (REGISTRY → manifest; `resolve_pdf` hop; EFE direct-PDF override; `--list`)
- `README.md` (Status + new "Authoring pipeline" section), `CLAUDE.md` ("Current state" pipeline bullet)

## Related

- [[phase-10-fincen-corpus-crawler|Phase 10: FinCEN corpus crawler (SCALE)]] — parent phase
- [[phase-07-pipeline-walking-skeleton|Phase 7]] — proved the one-advisory pipe this phase widens

## Health Delta

No automated test framework (demo project). New verification capability = `crawl_fincen.py --selftest`
(runnable stdlib parser check, exit-coded). Authoring deps unchanged (markitdown in the gitignored uv
`.venv`); crawler + acquire are pure stdlib (no requests/bs4). Engine untouched (`git diff index.html`
empty); `build.py --check all` zero drift on all 3 dist; py_compile clean on both scripts.

## Soft Observations / Phase N+1 Candidates

- **Elder presentation-values true-up (carried from Phase 9):** still open — the smoke-checklist
  per-typology table (≈L15) + compliance attribution (≈L62) cover only fentanyl + trade-based;
  `elder-financial-exploitation` has no walk-row. Doc-slice. Evidence: `tests/smoke-checklist.md` L15, L62.
- **Automate article→signal derivation (AUTOMATE fork):** the remaining M6 vision increment — now that
  discovery is widened, the manifest + corpus md make a derivation surface; automate red-flag→signal
  keeping the deterministic validator at the build boundary. Manual path proven (Phase 7).
- **`fin-2024-a002` (Supplemental Fentanyl Advisory) is now in the manifest** — a natural higher-impact
  re-point for the existing fentanyl typology (currently FINTRAC-grounded), if a fentanyl-verbatim
  upgrade is wanted. Evidence: `data/fincen/index.json`.
- **Manifest staleness / `--fetch` cadence:** the committed manifest is a point-in-time snapshot
  (through `fin-2026-a001`). No refresh trigger; a periodic `--fetch` + `--write` + `--selftest` would
  keep it current. Optional — only matters if the corpus is actively used downstream.

## Activation Quality

No `active-knowledge.md` (lite phase, none generated) — step skipped.
