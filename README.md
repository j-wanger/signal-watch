# Signal Watch — AML Vision Demo

A presenter-driven, offline, browser-based **vision prototype** for AML stakeholder
buy-in. It is a scripted, reliable dramatization of a signal/atom monitoring loop —
**not** a working detection system. Every figure shown is illustrative and labelled
as such.

The walkthrough, in six acts:

> read a regulatory advisory → extract candidate signals → assess coverage against
> our library + data → **human selects** what to build → agent drafts a signal
> definition → **human confirms** → backtest → reveal **combination lift** →
> coverage closes → loop repeats.

The persuasion lives in two human-in-the-loop gates (trust) and the combination-lift
reveal (why composed atoms beat monolithic scenarios).

## Run it

Build a typology to a single self-contained file, then open it (no server, no deps
except a Google Fonts `<link>` when online):

```
python3 scripts/build.py fentanyl                     # -> dist/fentanyl/index.html
python3 scripts/build.py trade-based                  # -> dist/trade-based/index.html
python3 scripts/build.py elder-financial-exploitation # -> dist/elder-financial-exploitation/index.html
python3 scripts/build.py corpus                       # -> dist/corpus/index.html (FinCEN corpus explorer)
python3 scripts/build.py all                          # build every typology + the corpus explorer
python3 scripts/build.py --check all                  # drift guard: committed dist == fresh build?

open dist/fentanyl/index.html                         # macOS — or just double-click it
open dist/corpus/index.html                           # the corpus explorer
```

`--check` re-renders every config in memory and byte-compares it against the committed
`dist/<id>/index.html` (non-mutating); it exits non-zero and names the typology if any built
file has drifted from its source. Run it before committing or presenting.

The built file runs offline from `file://`. Fonts fall back to system serif/sans/mono
if offline. Content lives in `config/typologies/*.json`; the engine (`index.html`) is
generic and never carries typology copy.

## Add a typology

1. Copy an existing `config/typologies/<id>.json`, edit it against `config/schema.md`
   (advisory text **public-source and paraphrased** by default; for a **FinCEN** advisory you may
   inline the **verbatim** public-domain text via `advisory_full`, attributed; figures illustrative).
2. `python3 scripts/build.py <id>` — the build validates the config against the schema
   and fails loud on any violation, then writes `dist/<id>/index.html`.

No engine edits required.

## Authoring pipeline (build-time only — never in the ship file)

To source a FinCEN advisory as a derivation surface for a new typology:

```
python3 scripts/crawl_fincen.py --selftest   # offline: verify the parser against the saved fixture
python3 scripts/crawl_fincen.py --write       # offline: regenerate data/fincen/index.json from the fixture
python3 scripts/crawl_fincen.py --fetch       # LIVE: refresh the listing fixture from fincen.gov
python3 scripts/acquire_fincen.py --list      # show the discovered advisory corpus (the manifest)
python3 scripts/acquire_fincen.py <id>        # LIVE: download one advisory PDF -> data/fincen/raw/<id>.pdf
.venv/bin/python scripts/pdf_to_md.py <id>    # convert PDF -> data/fincen/<id>.md (verbatim source of truth)
python3 scripts/derive_signals.py --selftest                     # offline: the deterministic GATE checks (matrix + quote-grounding + relevance + shape)
python3 scripts/derive_signals.py --check-derived <record.json>  # offline: DISPOSE a derived record (the gate)
python3 scripts/derive_signals.py --corpus                       # offline: cheap rf_region triage across ALL 14 committed advisories
python3 scripts/derive_signals.py --corpus-status                # offline: emit data/fincen/corpus-status.json (the corpus-explorer manifest)
```

`crawl_fincen.py` discovers the FinCEN advisories listing into the committed manifest
`data/fincen/index.json`; `acquire_fincen.py` reads it (resolving each advisory's PDF from its
detail page) and keeps the EFE anchor as a zero-hop direct-PDF override. `pdf_to_md.py` converts each PDF
to `data/fincen/<id>.md` (the verbatim source of truth). `derive_signals.py` is then the deterministic
**gate**: the LLM backend (a live model session) reads an advisory's markdown and *extracts* its red flags
plus the per-indicator judgment into `data/fincen/derived/<id>.json`, and `--check-derived` **disposes**
(see below). These tools are authoring-only and are **never** imported by the engine or `build.py` — the
ship artifact stays single-file, offline, never fetches, and never calls an LLM. Only PDF conversion
(`markitdown`) needs a gitignored uv `.venv` (see `scripts/requirements-authoring.txt`); everything in
`derive_signals.py` is pure stdlib. FinCEN advisories are U.S. federal works in the public domain
(17 U.S.C. §105).

**Corpus derivation (the backend for a singular corpus-backed demo).** The full 14-advisory FinCEN corpus
is committed as markdown (`data/fincen/*.md`). The LLM backend reads an advisory and *extracts* its red
flags plus, per indicator, a coverage status + data availability, a **build recommendation**, and **build
logic** for the immediately-buildable gaps, writing `data/fincen/derived/<id>.json`. The deterministic gate
`--check-derived` **disposes**: each `build_rec` must follow the cover×data matrix (`build_rec_category`),
every indicator's verbatim flag must be **quote-grounded** in the source md (`normalize(flag)` ⊂
`normalize(md)`, inside the red-flag relevance region `rf_region`), and a `BUILD_NOW` indicator must carry a
full signal definition. The LLM *proposes* (extraction included); the deterministic gate and the two human
gates *dispose*. Derived records are an LLM-derived + checked corpus dataset, **not** ship typology configs.

**The boundary is inverted — the LLM extracts; the deterministic layer gates (Phase 16) — and Phase 17
deleted the old extractor outright.** Earlier phases carried a deterministic `extract_red_flags` that
accreted format special-casing every phase yet only parsed ~half the heterogeneous corpus, and the LLM had
to clean its output anyway. The subtraction test inverted the boundary (the LLM extracts; the gate disposes
by quote-grounding), and then **Phase 17 removed `extract_red_flags` together with the whole `--scaffold` /
`--draft` / `--scaffold-derived` authoring stack it fed** — `derive_signals.py` dropped from ~1200 to ~600
lines, leaving exactly the gate (`normalize` + `rf_region` + `check_record`) plus a ~14-line
`rf_region`-bounded triage counter. That counter is the only counting role the extractor kept: `--corpus` /
`--corpus-status` reuse the already-computed red-flag region to report whether one exists (`derivable` —
false only for the 2 FATF jurisdiction advisories) and a coarse block count, a cheap hint for a
not-yet-derived advisory's status chip (a live advisory renders from its own record, so the count need only
be rough). The inverted loop is now the **sole** derivation path — it reaches even the *glued-no-separator*
advisories (ransomware, health-care fraud) whose PDF→markdown dropped both bullets and blank lines: the LLM
reads and extracts them like a human and the gate grounds each verbatim flag, so they ship derived with no
structure-preserving converter and no post-hoc splitter. The committed corpus ships **12 of 14 advisories
derived** (only the 2 FATF jurisdiction advisories, which carry no enumerated red-flag list, stay
non-derivable).

## The corpus explorer (the singular corpus-backed demo)

`dist/corpus/index.html` is a **second, separate** single-file ship artifact: a FinCEN **corpus
explorer**. Where the six-act typology demos each tell one scripted story, the explorer points the same
loop at the *whole public advisory corpus* — you pick one of the 14 advisories and watch it derive. It
is a **staged 4-screen flow**:

1. **Select** — all 14 advisories, each with an honest status chip: *derived* (live, clickable — 12 of
   them), or *no red-flag list* (non-derivable — the 2 FATF jurisdiction advisories). The chip also has a
   *clean / low* extraction state (ready to derive, not yet derived) for any future advisory added to the
   corpus before it is derived.
2. **Coverage** — the chosen advisory's coverage gauge, derived from its indicator statuses.
3. **Build recommendations** *(the new centerpiece)* — per red-flag indicator: coverage × data →
   one **build recommendation** (`BUILD NOW / ENHANCE / BUILD + ENRICH / SOURCE DATA / MONITOR /
   COVERED`), sorted build-now-first, each row tracing to its red-flag source line.
4. **Signal** — the full signal definition for each immediately-buildable (`BUILD NOW`) gap.

Build it with `python3 scripts/build.py corpus` (or `all`); guard it with `python3 scripts/build.py
--check corpus` (folded into `--check all`). The build is **decoupled from the authoring layer**: it
reads two committed data artifacts — the extraction manifest `data/fincen/corpus-status.json` (emitted
by `derive_signals.py --corpus-status`) and the LLM-derived records `data/fincen/derived/*.json` —
merges them by advisory id, and validates the derived records' shape at the build boundary (every
`build_rec` in the matrix vocabulary; a `BUILD NOW` indicator must carry a full signal definition).
`build.py` never imports `derive_signals.py`. The advisory titles and red-flag text are verbatim public
domain; the coverage/data/build judgments are illustrative (the "Illustrative data & outputs" badge
stays on, with the per-advisory source attribution kept visually distinct from it). The explorer ships
with **12 of 14** advisories derived — only the two FATF jurisdiction advisories (which carry no
enumerated red-flag list) stay non-derivable. The menu is deliberately varied: the transaction-pattern-rich
Chinese money-laundering-networks typology (`fin-2025-a003`) surfaces five immediately-buildable signals;
the enrichment-hungry Iran (`fin-2025-a002`) and Iran-backed-terror-finance (`fin-2024-a001`) typologies
lean to *build + enrich*; the **glued-no-separator** advisories — ransomware (`fin-2021-a004`) and
health-care fraud (`fin-2026-a001`, 24 red flags) — were unreachable by the deleted structural extractor
yet ship derived via the inverted loop (the LLM reads them like a human, the gate grounds every verbatim
flag). The front-end shows the full corpus honestly; the two non-derivable advisories are labelled as such.

## Present it

- Build the typology you want and open `dist/<id>/index.html` in the presentation browser,
  fullscreen. To switch typologies on stage, open the other built file.
- Drive it with the on-screen **Back / Next** buttons, or the **keyboard**: **→ / Space**
  advance, **←** goes back, **Esc** (or the on-screen **↺**) resets to a clean Act 0. The
  stepper rail at the top is clickable to jump to any act already reached.
- **Act 3** (Human review) requires you to select at least one candidate before Next
  enables — this is the first human gate. **Act 4** (Agent builds) waits on your
  confirm — the second gate. Don't skip these; they are the point. The gates hold under
  the keyboard too — advancing past them without selecting / confirming does nothing.
- The final act loops back to the start (**Run again ↺**) for a clean reset between runs.
- Honors **`prefers-reduced-motion`**: with the OS "reduce motion" setting on, every act
  lands in its final state with no animation. (A speaker-notes overlay is not built.)

## Compliance

- No real customer, account, or transaction data — anywhere. Coverage, population, and
  precision numbers are synthetic and illustrative.
- The only real-world content is **public advisory material** — paraphrased by default, per typology:
  - **fentanyl** — FINTRAC Operational Alert on illicit synthetic opioids (Jan 2025).
  - **trade-based** — FinCEN Alert on fentanyl-linked trade-based laundering (Apr 2025);
    FATF report on TBML trends & developments (2024).
  - **elder financial exploitation** — FinCEN Advisory EFE FIN-2022-A002, reproduced **verbatim**
    (US federal advisories are public domain, 17 USC §105; attributed, kept visually separate from
    the illustrative badge). The verbatim exception is FinCEN-only — it does not extend to FINTRAC.
- The "Illustrative data & outputs" badge stays visible at all times — it is a trust
  device for a compliance audience, not a disclaimer to hide.

## Project docs

- `HANDOFF.md` — full context, constraints, content model, milestone plan, decision log.
- `CLAUDE.md` — always-loaded project memory / non-negotiables for the agent.

## Status

**M7 — corpus-backed demo.** Phase 12 built the derivation backend (the deterministic red-flag spine
validated across all 14 advisories + an LLM-derived, deterministically-checked proof slice in
`data/fincen/derived/`); Phase 13 added the **corpus explorer** (`dist/corpus/index.html`) — a second
single-file artifact with an advisory-selection front-end and the per-indicator build-recommendation
render, built from `corpus.html` + the committed corpus manifest + derived records, with the six-act
showcase engine left byte-untouched. The earlier arc still stands:

**M6 — Signal Watch ingestion pipeline.** Config-driven engine (M1) + three typologies
(**fentanyl**, **trade-based ML** — M2; **elder financial exploitation** — M6), switchable at build
time with no engine edits, plus presenter polish (M3: keyboard nav, reset, `prefers-reduced-motion`).
M6 added a build-time authoring pipeline (acquire a FinCEN advisory PDF → convert to markdown →
hand-derive a signal) and renders the FULL verbatim EFE advisory (FinCEN FIN-2022-A002, public
domain) in Act 1. Phase 10 widened that pipeline with a **FinCEN corpus crawler**
(`scripts/crawl_fincen.py`) that discovers the FinCEN advisories listing into a committed manifest
(`data/fincen/index.json`), so acquisition reads the corpus instead of a hand-kept stub. Phase 11 added
`scripts/derive_signals.py` for the article→signal derivation step; Phases 12–13 extended it across the
14-advisory corpus and built the corpus explorer; Phase 16 **inverted** the boundary (the LLM extracts, a
deterministic gate disposes by quote-grounding) and Phase 17 **deleted** the original deterministic
extractor plus the scaffold/draft authoring stack, leaving the gate as the whole of `derive_signals.py`
(the engine never calls an LLM). Runs offline from a single `file://` artifact per typology. Live /
pre-generated mode (M4) is intentionally not built — scripted is the ship path. See `HANDOFF.md §8`
for the milestone plan.
