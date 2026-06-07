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

## Test

All checks are dep-free (no `npm install`, no test framework — they match the build's offline ethos):

```
python3 scripts/build.py --check all       # drift: every committed dist == a fresh build
node tests/corpus-explorer.test.mjs        # corpus-explorer 6-screen arc, against the committed dist
python3 scripts/derive_signals.py --selftest   # the derivation GATE checks (matrix + quote-grounding + shape)
```

`tests/corpus-explorer.test.mjs` loads `dist/corpus/index.html`, runs its inline script under a
hand-rolled DOM shim (no jsdom), and asserts the arc invariants — the human gate's div-toggle
selection, the two honest Signal empty states, the close-the-loop coverage math (and that the
indicator set is never mutated), reduced-motion landing in one paint, and the 0-picked flat-hold.
Loading the committed dist makes it a build-output smoke test too. Before any presentation, run the
three checks above, then walk `tests/smoke-checklist.md` (the live-visual / pacing / compliance checks
only a human eye can confirm).

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
python3 scripts/derive_signals.py --corpus [source_dir]          # offline: cheap rf_region triage across a source's committed md (default data/fincen)
python3 scripts/derive_signals.py --corpus-status [source_dir]   # offline: emit <source_dir>/corpus-status.json (the corpus-explorer manifest)
# Phase 20 — a second FinCEN source (ALERTS): --alerts on the crawl, --source <dir> on acquire/convert/status
python3 scripts/crawl_fincen.py --alerts --fetch                 # LIVE: refresh the alerts-hub fixture (then `--alerts --write` -> data/fincen-alerts/index.json)
.venv/bin/python scripts/pdf_to_md.py --source data/fincen-alerts <id>   # convert one alert PDF -> data/fincen-alerts/<id>.md
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
(17 U.S.C. §105). Phase 20 generalized these authoring tools to multiple FinCEN sources: `crawl_fincen.py
--alerts` discovers the FinCEN **alerts** hub (each PDF linked directly → zero-hop), and
`acquire_fincen.py` / `pdf_to_md.py` / `derive_signals.py --corpus-status` take a `--source <dir>`, so
alerts (`data/fincen-alerts/`) ingest and derive through the *same* gate — still verbatim, still
public-domain, no non-negotiable changed.

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
loop at the *whole public corpus* — FinCEN advisories + alerts, OFAC, and FINTRAC — you pick one of the 46 publications
and watch it derive. It is a **staged 6-screen arc** (Phase 18 gave it two of the beats the six-act showcase
has and the explorer lacked — a human gate and a close-the-loop payoff; Phase 25 added the article-processing
"read advisory" beat):

1. **Select** — all 46 publications (14 FinCEN advisories + 19 FinCEN alerts + 3 OFAC advisories +
   10 FINTRAC publications — 9 operational alerts + 1 operational brief), each with an honest `doc_type` chip (*Advisory* / *Alert* / *OFAC* / *FINTRAC*) and a status chip: *derived* (live, clickable — 42 of them), or *no
   enumerated red-flag list* (non-derivable — the 4 remaining: the 2 FATF jurisdiction advisories + 2
   alerts whose text mentions red flags but carries no anchorable enumerated list). The *clean / low*
   "ready to derive, not yet derived" chip state remains for any future publication added before it is derived.
2. **Read advisory** *(Phase 25)* — the **full source document**, with each verbatim red-flag phrase
   highlighted, then **translated** into a natural AML `red_flag` shown beside the verbatim quote. This makes
   the corpus's two-layer pipeline visible — *step 1 extract (grounded, verbatim) → step 2 translate (a red
   flag the way an AML programme writes it)* — the same model the six-act showcase uses. The verbatim quote
   stays beside every translation (the grounded evidence; the translation is disclosed-illustrative).
3. **Coverage** — the chosen advisory's coverage gauge, derived from its indicator statuses.
4. **Build recommendations — the human gate** *(the centerpiece)* — per red-flag indicator: coverage ×
   data → one **build recommendation** (`BUILD NOW / ENHANCE / BUILD + ENRICH / SOURCE DATA / MONITOR /
   COVERED`), sorted build-now-first, each row tracing to its red-flag source line. The `BUILD NOW` rows
   are **selectable** (div-toggles, *not* `<input>` — so the keyboard nav still works), defaulting to all
   selected: the presenter picks what to commit. *Agent proposes, human disposes.*
5. **Signal** — the full signal definition for each **picked** `BUILD NOW` gap (an honest empty state if
   none are buildable, or if you deselect them all).
6. **Close the loop** — the coverage index animates **before → after** as the gaps you committed flip
   *gap → covered* (the same model as the showcase's Act 6). The payoff is **coverage, not a precision
   "lift" number**: the derived records carry no precision figures, and fabricating ~12 per-advisory stats
   to mimic the showcase's combination-lift beat would break the *never present synthetic numbers as real*
   rule — so the explorer closes the loop on the one quantity it can honestly show. A 0-build-now advisory
   (or deselecting everything) holds coverage flat with a note, never a fake rise.

Build it with `python3 scripts/build.py corpus` (or `all`); guard it with `python3 scripts/build.py
--check corpus` (folded into `--check all`). The build is **decoupled from the authoring layer**: it
iterates the `CORPUS_SOURCES` registry (Phase 20 — multi-source), reading each source's committed
extraction manifest `corpus-status.json` (emitted by `derive_signals.py --corpus-status [source_dir]`)
and LLM-derived records `derived/*.json`, merging them all by id into one menu, and validating the
derived records' shape at the build boundary (every `build_rec` in the matrix vocabulary; a `BUILD NOW`
indicator must carry a full signal definition). `build.py` never imports `derive_signals.py`. The titles
and red-flag text are verbatim from their public sources (US-federal public domain, or FINTRAC under its
non-commercial reproduction licence); the coverage/data/build judgments are illustrative (the
"Illustrative data & outputs" badge stays on, with the per-document source attribution — each carrying its
own basis — kept visually distinct from it). The explorer ships with **42 derived across 46 publications**
(12 of 14 FinCEN advisories + 17 of 19 FinCEN alerts + 3 of 3 OFAC advisories + 10 of 10 FINTRAC publications
— 9 operational alerts + 1 operational brief) — the non-derivable documents (the 2 FATF advisories + 2 alerts with no enumerated red-flag list) are labelled as such. The menu is deliberately varied: the transaction-pattern-rich
Chinese money-laundering-networks typology (`fin-2025-a003`) surfaces five immediately-buildable signals;
the enrichment-hungry Iran (`fin-2025-a002`) and Iran-backed-terror-finance (`fin-2024-a001`) typologies
lean to *build + enrich*; the **glued-no-separator** advisories — ransomware (`fin-2021-a004`) and
health-care fraud (`fin-2026-a001`, 24 red flags) — were unreachable by the deleted structural extractor
yet ship derived via the inverted loop (the LLM reads them like a human, the gate grounds every verbatim
flag). The front-end shows the full corpus honestly; the non-derivable documents are labelled as such.

**Multi-source (Phases 20-22) — beyond advisories, across agencies and jurisdictions.** A thin `CORPUS_SOURCES` registry
in `build.py` maps each FinCEN publication *type* to its own committed `corpus-status.json` +
`derived/*.json`, and `render_corpus` merges them into one menu with an honest `doc_type` chip per card.
**FinCEN Alerts** are the second source (`data/fincen-alerts/` — 19 alert markdown files, 17 derived):
`crawl_fincen.py --alerts` discovers them from the FinCEN alerts hub (each PDF is linked directly — a
zero-hop download), then `acquire_fincen.py` / `pdf_to_md.py --source data/fincen-alerts` convert them,
and they derive through the **same inverted loop and the same gate** — nothing about the derivation
changed. This stays inside the one verbatim exception: alerts are still FinCEN, still U.S.-federal public
domain (17 U.S.C. §105), so **no non-negotiable changed** and the quote-grounding gate is reused
unchanged; `data/fincen/` (the advisories source) is byte-frozen — the corpus grew by *merge*, not
migration.

**OFAC is the third source (Phase 21) — a second US-federal agency.** OFAC (US Treasury) advisories are
also public domain under the same statute, so the verbatim exception was **extended FinCEN-only →
US-federal** (FinCEN + OFAC + US federal agencies; at this point FINTRAC and any non-US / non-government
source still paraphrased — Phase 22 then added FINTRAC as a verbatim source under a separate licence, below).
OFAC mostly frames its indicators as "Risk Indicators" / "Deceptive Practices" rather than
FinCEN's "red flags", so `rf_region`'s anchors were **widened** (`_RF_HEADER_OFAC` + `_RF_INTRO_OFAC`) —
strictly **regression-gated**: every existing FinCEN md's region stays byte-unchanged and all 29 FinCEN
records + `--selftest` stay clean (the new vocab is inert for FinCEN; the grounding `normalize` is
untouched). OFAC's site is a JS app with no static listing, so `data/ofac/index.json` is **hand-curated**
from `/media/<id>/download` PDFs (acquired via `acquire_fincen.py --source data/ofac`; `crawl_fincen.py`
stays FinCEN-only). The cleanly-anchoring OFAC advisory set is **small** (3 — sham-transactions, maritime,
virtual-currency, each a different vocab form): most OFAC docs defer red flags to a co-issued FinCEN
advisory or use non-anchoring framing, and are honestly skipped. OFAC content is sanctions/vessel-oriented,
so its records are honestly enrichment / `SOURCE_DATA`-heavy with few build-now signals (the maritime
deceptive practices are vessel behavior an FI can't see in its transaction data — `SOURCE_DATA`, never a
fabricated signal).

**FINTRAC is the fourth source (Phase 22) — the first cross-*jurisdiction* source.** FINTRAC (Canada's
financial-intelligence unit) is **Canadian Crown copyright, not US public domain** — the first source the
US-federal verbatim exception did *not* already cover. Rather than paraphrase (the earlier assumption), the
verbatim exception gained a **second, distinct basis**: FINTRAC's [Terms &
Conditions](https://fintrac-canafe.canada.ca/help-aide/no-av-eng) permit reproducing its publications
**verbatim for non-commercial use with attribution** (© His Majesty the King in Right of Canada + title +
"a copy of the version at &lt;URL&gt;") — a reproduction *licence*, not the 17 U.S.C. §105 no-copyright
basis (every *other* non-US / non-FINTRAC source still paraphrases). FINTRAC **Operational Alerts** head
their list with "Money laundering indicators" / "Terrorist activity financing indicators" — neither "red
flags" nor OFAC's "risk indicators" — so `rf_region` was **widened again** (`_RF_HEADER_FINTRAC` +
`_RF_INTRO_FINTRAC`, ML/TF-qualified plus an optional "… indicators *of &lt;topic&gt;*" section-title
clause), strictly **regression-gated**: the ML/TF-qualified phrasing occurs **0×** across all 36 FinCEN +
OFAC mds, so every existing region stays byte-unchanged and all 32 records + `--selftest` stay clean (the
grounding `normalize` is untouched). Acquisition is **hand-curated** (`data/fintrac/index.json`): FINTRAC
serves a PDF at `<page-url>.pdf`, which the existing direct-download path handled with no change
(`acquire_fincen.py --source data/fintrac`; the `pdf_to_md.py` provenance header was made source-aware so a
FINTRAC file is never mislabelled public domain). **Phase 23 then deepened FINTRAC 3 → 10** — the demo's
audience is a Canadian bank, so depth weighted Canadian-relevant typologies: six more Operational Alerts
(human trafficking / Project Protect, online child sexual exploitation / Project Shadow, romance fraud /
Project Chameleon, illegal wildlife trade / Project Anton, professional money laundering, illicit cannabis /
Project Legion) plus the **real-estate Operational Brief** (FINTRAC-2016-OB001 — snow-washing, the marquee
Canadian typology). Those Briefs (and some OAs) head their lists with the *inverted* form "Indicators **of**
money laundering …", so `rf_region` was widened once more (`_RF_HEADER_FINTRAC_INV`, two narrow branches)
strictly regression-gated — **0 of 39** prior FinCEN + OFAC + FINTRAC regions shifted, the grounding core
untouched, and any document whose heading couldn't anchor without disturbing an existing region is skipped,
not forced. The 10 FINTRAC documents contribute **225 indicators / 50 build-now**, honest yield over count:
the OCSE and wildlife alerts are deliberately `SOURCE_DATA`-heavy (their indicators hinge on external
attribution a bank can't see), while cannabis and professional-ML are build-now-rich (bank-observable
EMT / cheque / cash / utility patterns) — and FINTRAC alerts run far denser than FinCEN advisories. The
explorer's source panel renders each document's own basis, so a FINTRAC document shows its Crown-copyright
attribution, never the US public-domain line.

**Read advisory + red-flag translation (Phase 25) — red flags that read like red flags.** The grounded
indicator text is a *verbatim quote* lifted from the source document — faithful, but it reads like advisory
prose, not how an AML programme writes a red flag. So every derived indicator now carries a second field,
`red_flag`: a natural-AML translation of the verbatim quote, re-derived across all 42 documents. The
explorer's new **Read advisory** screen (step 2 of the arc) renders the **full source document** with each
verbatim phrase highlighted, then shows the translation beside it — making the *extract → translate* pipeline
visible (the same two-layer model the six-act showcase uses). The honesty is structural: the verbatim quote
stays the **grounded authority**, shown beside every translation (never replaced); the quote-grounding gate is
byte-unchanged; and the gate's new check on `red_flag` is *shape only* (present, distinct from the verbatim,
length-bounded) — translation faithfulness is the one judgment a deterministic gate can't make, so the
verbatim sits right beside it for the eye to check, under the always-on illustrative badge. Because paraphrase
is the project's default compliance posture, the translation **aligns** with the non-negotiables rather than
bending them. The full articles are inlined at build time (the single offline file grows to ~2.2 MB); the
showcase, every source document, and the grounding core stay byte-frozen.

**Cross-corpus synthesis (Phase 24) — the corpus becomes analytical.** Once the corpus spans two
jurisdictions, the same money-laundering typology often shows up under more than one regulator — and no
single advisory enumerates it all. The explorer's **Select** screen now has a **Documents / Typologies**
toggle: in typology mode you pick a typology and see its **cross-jurisdiction cluster** — every corpus
document on that typology, across FinCEN, OFAC, and FINTRAC — with a **combined coverage** gauge and each
jurisdiction's contribution, then drill into any document's own 6-screen loop (Back returns to the
cluster). The point it makes: *no single regulator covers a typology; the combined corpus does.* Five
typologies span both the US and Canada (terrorist financing, synthetic opioids, human trafficking,
professional money laundering, romance-and-investment fraud); two more span US agencies (sanctions evasion
across FinCEN advisories + alerts + OFAC; public-benefits fraud). The honesty rule is the same one that
ruled out a fabricated "lift" number in [§ close-the-loop](#the-corpus-explorer-the-singular-corpus-backed-demo):
**combined coverage is honest union arithmetic** over the existing per-indicator statuses (illustrative,
under the always-on badge), per-jurisdiction figures are honest counts, and every clustered indicator stays
traceable to its source document — **no similarity, overlap, or "lift" between regulators is computed or
claimed**, and indicators are *not* de-duplicated or matched across regulators (that would require
fabricated matching). The typology label is a **separate committed overlay** (`data/typology-map.json`,
doc-id → one closed-vocabulary typology), so the 42 derived records and the grounding core stay
byte-frozen; `build.py` validates it at the build boundary (closed vocabulary + referential integrity +
total live-document coverage, fail-loud) — agent proposes the map, the deterministic gate disposes. No
non-negotiable changed.

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
    the illustrative badge). Verbatim reproduction now covers **US-federal** sources (FinCEN, OFAC —
    public domain) and, since Phase 22, **FINTRAC** (Canadian Crown copyright, reproduced for
    non-commercial use with attribution per its Terms & Conditions — a licence, not public domain);
    every other non-US / non-FINTRAC source still paraphrases.
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
