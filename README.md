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
python3 scripts/build.py corpus                       # -> dist/corpus/index.html (AML corpus explorer)
python3 scripts/build.py news                         # -> dist/news/index.html (adverse-media stream, M8)
python3 scripts/build.py all                          # build every typology + the corpus explorer + the news stream
python3 scripts/build.py --check all                  # drift guard: committed dist == fresh build?

open dist/fentanyl/index.html                         # macOS — or just double-click it
open dist/corpus/index.html                           # the corpus explorer
open dist/news/index.html                             # the adverse-media stream
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
node tests/corpus-explorer.test.mjs        # corpus-explorer: landing + per-doc arc + wow beats, vs the committed dist
node tests/news-stream.test.mjs            # adverse-media stream (M8): the screening arc + the fuzzy matcher, vs the committed dist
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
and watch it derive. Phase 26 elevated it to the showcase's bar; **Phase 27 made it shippable** — an assessment
workflow showed the remaining weakness was *presentation, not the grounding system*, so the Read-advisory source
is now **markitdown-cleaned** (no running headers / tab-soup), highlighting **normalizes both sides** to land
~every grounded phrase, the build-log runs in a proper proposal grid, the "agent reading" types the **whole**
article, and 121 over-long verbatim quotes were **tightened to crisp grounded sub-spans** (faithfulness-guarded —
genuinely-long advisory indicators are kept whole). It opens on a
**landing** (frames the multi-jurisdiction public corpus → one signal loop; an "Enter the corpus" CTA), then
runs a **staged 6-screen per-doc arc** (Phase 18 gave it the human gate + the close-the-loop payoff; Phase 25
added the article-processing "read advisory" beat; Phase 26 added the combination-lift beat):

1. **Select** — all 46 publications (14 FinCEN advisories + 19 FinCEN alerts + 3 OFAC advisories +
   10 FINTRAC publications — 9 operational alerts + 1 operational brief), **grouped by source** (FinCEN
   Advisories / Alerts / OFAC / FINTRAC), newest-first within each, each with an honest `doc_type` chip
   (*Advisory* / *Alert* / *OFAC* / *FINTRAC*) and a status chip: *derived* (live, clickable — 42 of them), or *no
   enumerated red-flag list* (non-derivable — the 4 remaining: the 2 FATF jurisdiction advisories + 2
   alerts whose text mentions red flags but carries no anchorable enumerated list). The *clean / low*
   "ready to derive, not yet derived" chip state remains for any future publication added before it is derived.
2. **Read advisory** *(Phase 25; Phase 26 progressive render)* — the **full source document**, rendered with
   the showcase's "agent reading" beat (it types a capped opening, then reveals the full text with each verbatim
   red-flag phrase highlighted, then staggers in the translations; reduced-motion settles to the final state in
   one paint). Each verbatim phrase is **translated** into a natural AML `red_flag` shown beside the verbatim
   quote — the corpus's two-layer pipeline made visible: *step 1 extract (grounded, verbatim) → step 2 translate*.
   Phase 26 re-translated all 42 documents' red flags to the showcase's register (terse, mechanism-named —
   *fan-in / flow-through / structuring / nominee / funnel*) so they read like the six-act showcase's indicators,
   not prose; the verbatim quote stays beside every translation (the grounded evidence; the translation is
   disclosed-illustrative).
3. **Coverage** — the chosen advisory's coverage gauge, derived from its indicator statuses; for a document
   with more than one enumerated section, the indicators are **sub-grouped by section** (else flat).
4. **Build recommendations — the human gate** *(the centerpiece)* — per red-flag indicator: coverage ×
   data → one **build recommendation** (`BUILD NOW / ENHANCE / BUILD + ENRICH / SOURCE DATA / MONITOR /
   COVERED`), sorted build-now-first, each row tracing to its red-flag source line. The `BUILD NOW` rows
   are **selectable** (div-toggles, *not* `<input>` — so the keyboard nav still works), defaulting to all
   selected: the presenter picks what to commit. *Agent proposes, human disposes.*
5. **Signal** — the agent **build-log** (a structural "agent builds" reveal — Draft → Map → Generate → the
   human gate, already passed → Backtest → Route to Model Validation — animating the *real* `build_logic`, no
   numbers) followed by the full signal definition for each **picked** `BUILD NOW` gap (an honest empty state if
   none are buildable, or if you deselect them all).
6. **Combination lift** *(Phase 26)* — the showcase's Act-5 "alone it's noise; together it's a case" beat:
   composition bars (the committed signal alone → + a correlated signal → + a second signal) animate to show
   that composed atoms beat a monolithic rule. **The lift figures are a generic illustrative template, identical
   across every document, behind a loud "Illustrative · pending calibration — NOT measured on this document"
   tag** (kept visually distinct from the always-on badge). This is the deliberate, scoped reversal of Phase 18's
   rejection: the records still carry *no* precision figures, and fabricating ~42 distinct per-document lift stats
   would break the *never present synthetic numbers as real* rule — so the beat shows the *shape* of composition
   as an openly-templated placeholder, never a measured rate. An empty selection shows an honest empty state.
7. **Close the loop** — the coverage index animates **before → after** as the gaps you committed flip
   *gap → covered* (the same model as the showcase's Act 6). The honestly-measurable payoff is **coverage**: a
   0-build-now advisory (or deselecting everything) holds coverage flat with a note, never a fake rise.

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
explorer renders each document's own compliance basis. (Phase 28, the owner's compliance call: a FINTRAC
document's Crown-copyright attribution — © His Majesty… + complete title + source URL — now renders in the
**page footer** for the document on screen rather than in the per-doc Source label; US public-domain documents
show no footer attribution, and never the US public-domain line is claimed for FINTRAC.)

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

**Showcase-quality elevation (Phase 26) — the register, the wow, the entry.** Phase 25 shipped the two-layer
model but the output was still weak: the translations read like prose, the article render was static, the Signal
screen didn't land, nothing was grouped, and there was no front door. Phase 26 raised the whole explorer to the
six-act showcase's bar. **The register:** all 42 documents' `red_flag`s were re-translated to the showcase's
terse, mechanism-named AML-indicator style (*"Receive-and-forward to no-relationship payees (mule pass-through)"*,
*"Multi-originator geographic funnel-in"*) — done with a **dynamic workflow** (42 translate agents → 42 *independent*
adversarial verifiers; the model proposes, a byte-surgical applier writes only the `red_flag` value, and
`--check-derived` disposes), so the verbatim quote and the grounding logic stay byte-unchanged and only the
translation register changed. **The render:** the Read-advisory screen now **streams** the source document in as
if the agent were reading it (a blinking caret trails the read edge, the panel scroll-follows) — each red-flag
phrase highlights *only as the read reaches its position*, its translation extracting alongside, and both the
"phrases extracted" and "red flags" counters climb from 0 (Phase 28 — replacing the Phase-26/27 render that placed
the whole text up front; reduced-motion settles in one paint).
**Grouping:** Select is grouped by source (newest-first); red flags sub-group by section on Coverage. **The wow
beats:** the Signal screen gained the showcase's build-log (animating the *real* `build_logic`), and a new
**Combination-lift** screen ports the "alone it's noise, together it's a case" beat — with its lift figures held
to a *generic illustrative template behind a loud "pending calibration" tag* (never per-document fabricated; the
deliberate, scoped reversal of Phase 18's no-lift rule). **The entry:** a story-driven **landing** now frames the
corpus before the Select grid. The showcase (`index.html` + the 3 typology dists), every source document, every
manifest, the typology overlay, and the grounding core stay byte-frozen; no non-negotiable changed.

**Cross-corpus synthesis (Phase 24) — the corpus becomes analytical.** Once the corpus spans two
jurisdictions, the same money-laundering typology often shows up under more than one regulator — and no
single advisory enumerates it all. The explorer's **Select** screen now has a **Documents / Typologies**
toggle: in typology mode you pick a typology and see its **cross-jurisdiction cluster** — every corpus
document on that typology, across FinCEN, OFAC, and FINTRAC — with a **combined coverage** gauge and each
jurisdiction's contribution, then drill into any document's own per-doc loop (Back returns to the
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

**Capability & data-source lenses (Phase 29–30) — coverage by what you *have*.** The **Select** toggle now
carries four modes: **Documents / Typologies / Capabilities / Data sources**. The Phase-28 interview tagged
every indicator with both a detection-**capability** code (C1–C28) and a **data-source** code (D1–D20), each
with the institution's own posture (in place / partial / not yet) — these two lenses re-project the whole
corpus by those axes. In **Capabilities** mode you see, per detection capability, how many corpus indicators
demand it + your posture + the covered/partial/gap split (gap-priority sorted); drill one to pool its
indicators across every regulator and jurisdiction, then into any document's loop. **Data sources** mode is
the symmetric counterpart on the data axis — and it makes a *distinct* point: a capability is a **build**
problem, a data source is an **access** problem. **7 of 20 feeds are "not yet" available** (blockchain
analytics, beneficial-ownership data, …) — exactly the indicators the bank can't action until it acquires the
data, now legible corpus-wide instead of buried per document. Both lenses are **pure honest re-projection** —
demand and coverage are counts over the existing per-indicator statuses, posture is the interview answer; **no
similarity, overlap, or "lift" is computed or claimed**, and indicators are *not* de-duplicated across sources.
The capability/data-source labels + postures live in one committed overlay (`data/capability-taxonomy.json`,
validated at the build boundary); the 42 derived records already carry the codes, so they and `build.py` stay
byte-frozen. No non-negotiable changed.

## The adverse-media / negative-news stream (M8 — Phase 31 + Phase 32)

`dist/news/index.html` is a **third** single-file ship artifact, opening a **second atom stream**:
adverse-media / negative-news screening. Where the corpus stream derives signals from *regulatory* text,
this stream points the same loop at *real enforcement news* — and proves the muscle the corpus can't: **entity
resolution against your own book.** The thesis is unchanged — an adverse-media hit is an **atom** that
composes with a counterparty's transaction signals — and it makes concrete the "what aren't we watching?"
anxiety the showcase opens on (TD Bank's 2024 penalty was a CDD/adverse-media failure).

The articles are **real US-federal enforcement records** — DOJ press releases and OFAC sanctions designations
(an attorney trust-account laundering case, a romance-/BEC-mule case, a Canadian export-control shell network, and
a Russian shadow-finance designation) — reproduced **verbatim** (excerpted) under **17 U.S.C. §105** (US federal
works are public domain; the corpus's exact verbatim basis, applied to news). The client/counterparty **book stays
synthetic** — real adverse-media entity × synthetic book. (Acquisition is build-time only; the runtime never fetches.)

The arc (build with `python3 scripts/build.py news`):

1. **Select** — pick one of the real enforcement articles (an honest source chip: DOJ / OFAC; stat tiles).
2. **Read** — a **streaming "agent reading"** render: the source streams in, each grounded red-flag phrase
   highlights *as the read reaches it*, and the **named entities** are tagged and **carded** with their grounded
   details (name · location · age · profession), the **typology**, and a natural-AML `red_flag` translation beside
   each verbatim quote (the corpus's two-layer model, reused). The source attribution (public domain, §105) is shown.
3. **Screen** — a visible **scan process**: each extracted entity is scored against every row of the client &
   counterparty **book** (normalize → token-sort → **Jaro-Winkler**, real string-similarity computed in-browser),
   swept in and ranked across a threshold line. The point it makes: it surfaces the **near-matches an exact-name
   screen would miss** (a transliteration, a dropped suffix, a reversed word order) — and the one **exact** hit
   where a counterparty *is* a designated entity.
4. **Disposition — the human gate** — every surfaced hit is a keyboard-safe toggle, defaulting to *confirmed*;
   the analyst **dismisses false positives** (a common name can collide with an unrelated person at a perfect
   1.0 score — high score ≠ confirmation). *Agent proposes, human disposes.*
5. **Exposure** — the confirmed hits, framed as adverse-media **atoms** ready to compose with transaction
   signals (the M8 north star).

**Honesty:** the source articles are **real** public-domain US-federal enforcement records; the **book is
synthetic** (no real customers, accounts, or transactions, ever), under the always-on illustrative badge; the fuzzy
scores are **real** computed similarity (never fabricated); counts are honest; the near-match and the false-positive
trap are *designed into the synthetic book to teach the mechanism*, not claimed as detection rates. Build-time, the
entities (and their attributes) + red-flag phrases are **quote-grounded** in their source article at the build
boundary (`validate_news_data` — the same faithfulness discipline as the corpus, with a local normalizer so
`build.py` never imports the authoring layer); the runtime is pure client-side JS (no LLM, no fetch). `node
tests/news-stream.test.mjs` drives the whole arc + the matcher against the committed `dist/news/index.html` (both
motion modes). The showcase, the entire corpus, and the grounding core stay byte-frozen; `build.py` is edited only
additively. No non-negotiable changed (US-federal verbatim public domain is the corpus's existing basis).

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

**M8 — the adverse-media / negative-news stream (in progress).** Phase 31 opened a **second atom stream** as
a third single-file artifact (`dist/news/index.html`): synthetic news → grounded entity + red-flag extraction
→ a client-side **fuzzy match** against a synthetic client/counterparty book → potential exposure → a human
disposition gate. A walking skeleton — the "compose with the transaction signal" payoff is named and scoped for
later M8 work. The showcase and the entire corpus stay byte-frozen; `build.py` gained only an additive `news`
target.

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
