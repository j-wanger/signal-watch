# Active Phase Context

Phase: 10 - FinCEN corpus crawler (SCALE) — ACTIVE (planned 2026-06-05, direction approved; begin at T1).
Objective: Widen the authoring scraper from one hand-registered advisory to the discovered FinCEN
advisory corpus — the static 1-entry `REGISTRY` in `acquire_fincen.py` becomes a generated manifest
`data/fincen/index.json`. Core = DISCOVERY, not mass-download. Authoring-only; ship artifact unchanged.
Scope: scripts/crawl_fincen.py (new), scripts/acquire_fincen.py, data/fincen/index.json (new),
tests/fixtures/*, README.md, CLAUDE.md.

Approach: new authoring-only `crawl_fincen.py` = PURE `parse_index(html)→[{id,title,date,type,url}]`
(deterministic, `--selftest` against a saved fixture — Phase-9 `build.py --check` ethos) + a thin live
`fetch_index()` shell (stdlib urllib, manual authoring run, NEVER in smoke/CI). Committed `index.json`
is produced by `parse_index(saved_fixture)` → reproducible OFFLINE. `acquire_fincen.py` reads the
manifest (id→url) with the static EFE entry MERGED as fallback (backward-compatible). Widened pipe
proven on a BOUNDED BATCH (~2–3), not the whole corpus.

Tasks (lite, 4): T1 discovery probe + saved fixture (S) · T2 `crawl_fincen.py` pure parser +
`--selftest` + manifest writer (M) · T3 wire `acquire_fincen.py` to the manifest, EFE fallback (S) ·
T4 bounded batch proof + docs (S).

Key constraints (load-bearing):
- Authoring-only, NEVER in the ship file — engine never imports the crawler; `build.py` stays stdlib;
  ship artifact never fetches. `git diff index.html` must stay empty.
- Stdlib-only crawler (no requests/bs4; urllib + hand parser). markitdown stays confined to pdf_to_md.py.
- Deterministic committed manifest — `index.json` from `parse_index(saved_fixture)`, not a live crawl.
- No repo bloat — `data/fincen/raw/` stays gitignored; commit the manifest + only md actually derived
  from. No bulk-md commit.
- Backward-compatible acquire — static EFE entry merged so `fin-2022-a002` always resolves.

Exit criteria:
- `crawl_fincen.py --selftest` → ≥3 well-formed `{id,title,date,url}` entries from the fixture, exits 0.
- `data/fincen/index.json` committed, valid JSON array (≥3 incl. `fin-2022-a002`), reproducible offline.
- `acquire_fincen.py --list` lists the manifest; `acquire fin-2022-a002` still resolves (backward-compat).
- bounded batch (~2–3) acquired+converted → sampled `data/fincen/<id>.md` non-empty.
- crawler documented in docstrings + README + CLAUDE; `git diff index.html` empty; `raw/` gitignored.

Abort: if FinCEN's index is JS-rendered / requires auth / blocks scraping so no deterministic parser
can be built from a saved page — PAUSE, report, pivot to a hand-curated manifest (still an upgrade over
the 1-entry stub). Blocked >3 attempts on a task → ask user: skip or abort.

Gates:
- [x] Direction confirmed by user (SCALE: FinCEN corpus crawler over the elder true-up; discovery-manifest + bounded batch, not mass-download — 2026-06-05)
- [ ] Delivery accepted (post-implementation report)
