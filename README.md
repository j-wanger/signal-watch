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
python3 scripts/derive_signals.py --selftest          # offline: EFE red-flag parser (12+12) + deterministic checks
python3 scripts/derive_signals.py --scaffold <id> <md># offline: md -> config/typologies/<id>.draft.json SKELETON
.venv/bin/python scripts/derive_signals.py --draft <id> <md>  # LIVE: + LLM-drafted judgment (needs ANTHROPIC_API_KEY)
python3 scripts/derive_signals.py --corpus                       # offline: extract red flags across ALL 14 committed advisories
python3 scripts/derive_signals.py --corpus-status                # offline: emit data/fincen/corpus-status.json (the corpus-explorer manifest)
python3 scripts/derive_signals.py --scaffold-derived <id> <md>   # offline: -> data/fincen/derived/<id>.json skeleton
python3 scripts/derive_signals.py --check-derived <record.json>  # offline: dispose a derived record (matrix + traceability)
```

`crawl_fincen.py` discovers the FinCEN advisories listing into the committed manifest
`data/fincen/index.json`; `acquire_fincen.py` reads it (resolving each advisory's PDF from its
detail page) and keeps the EFE anchor as a zero-hop direct-PDF override. `derive_signals.py` then
automates the article→signal step in two layers: a **deterministic** layer (stdlib, `--selftest`/
`--scaffold`) extracts the advisory's enumerated red flags and emits a schema-shaped config
**skeleton**, and a **neural** layer (`--draft`, build-time only) calls the Anthropic API to *propose*
the judgment fields (indicator statuses, the single target, the signal definition). The LLM proposes;
`build.py` + the schema + the two human gates **dispose** — the `.draft.json` is a gitignored scratch
artifact you review and rename to `<id>.json`, never auto-promoted, so committed configs stay
deterministic and human-reviewed. These tools are authoring-only and are **never** imported by the
engine or `build.py` — the ship artifact stays single-file, offline, never fetches, and never calls an
LLM. Conversion (`markitdown`) and the draft step (`anthropic`) need a gitignored uv `.venv` (see
`scripts/requirements-authoring.txt`) and, for `--draft`, `ANTHROPIC_API_KEY` in the environment (the
key never enters the ship file); everything else is pure stdlib. FinCEN advisories are U.S. federal
works in the public domain (17 U.S.C. §105).

**Corpus derivation (the backend for a singular corpus-backed demo).** The full 14-advisory FinCEN
corpus is committed as markdown (`data/fincen/*.md`). `derive_signals.py --corpus` runs the red-flag
extractor across all 14 and reports each advisory **CLEAN** / **LOW-CONFIDENCE** / **NEEDS-ATTENTION** —
the deterministic spine validated on the whole corpus, honestly flagging the heterogeneous formats it
can't cleanly split rather than forcing a bogus count. `--scaffold-derived` then emits a derived-record
skeleton (one indicator per extracted red flag, each `src_line`-traceable) under `data/fincen/derived/`;
the LLM backend fills the judgment — per indicator a coverage status + data availability, a **build
recommendation**, and **build logic** for the immediately-buildable gaps — and `--check-derived`
**disposes**: each `build_rec` must follow the deterministic cover×data matrix (`build_rec_category`),
every indicator must trace to a red-flag md line, and a `BUILD_NOW` indicator must carry a full signal
definition. The LLM backend can be the Anthropic API (the `--draft` pattern) or a live model session
acting as the backend (no key) — either way the LLM *proposes* and the deterministic checks *dispose*.
Derived records are an LLM-derived + checked corpus dataset, **not** ship typology configs.

The spine **assists**; it does not automate the derivation. Extraction is deterministic but imperfect
(the corpus is heterogeneous — roughly half parses cleanly, the rest is flagged), so a complete,
demo-quality derived record still requires **LLM-backend authoring**: the per-indicator status/data
judgment, the recommendation rationale, the signal build logic, and pruning any residual extraction
noise. The deterministic layer extracts, flags, and validates; the model session authors; the two
human gates dispose.

## The corpus explorer (the singular corpus-backed demo)

`dist/corpus/index.html` is a **second, separate** single-file ship artifact: a FinCEN **corpus
explorer**. Where the six-act typology demos each tell one scripted story, the explorer points the same
loop at the *whole public advisory corpus* — you pick one of the 14 advisories and watch it derive. It
is a **staged 4-screen flow**:

1. **Select** — all 14 advisories, each with an honest status chip: *derived* (live, clickable),
   *clean / low* extraction (ready to derive, not yet derived), or *no red-flag list* (non-derivable,
   e.g. the FATF jurisdiction advisories).
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
with **5 of 14** advisories derived — kleptocracy, PRC precursor chemicals, human trafficking
(`fin-2020-a008`), Chinese money-laundering networks (`fin-2025-a003`), and Iranian illicit finance
(`fin-2025-a002`) — a deliberately varied menu (the transaction-pattern-rich CMLN typology surfaces
five immediately-buildable signals; the enrichment-hungry Iran typology leans to *build + enrich*). The
front-end shows the full corpus honestly, and derivation of the remaining clean advisories scales as a
follow-up.

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
(`data/fincen/index.json`), so acquisition reads the corpus instead of a hand-kept stub. Phase 11
added `scripts/derive_signals.py`, which automates the article→signal derivation step: a deterministic
scaffolder plus an authoring-only LLM-draft mode whose output is gated by `build.py` + the human review
(the engine never calls an LLM). Runs offline from a single `file://` artifact per typology. Live /
pre-generated mode (M4) is intentionally not built — scripted is the ship path. See `HANDOFF.md §8`
for the milestone plan.
