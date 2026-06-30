# Signal Watch — AML Vision Demo

A presenter-driven, **offline, browser-based vision prototype** for AML stakeholder buy-in. It is a
scripted, reliable dramatization of a signal/atom monitoring loop — **not** a working detection system.
Every figure shown is illustrative and labelled as such (an always-on "Illustrative data & outputs" badge).

The loop, in six acts:

> read a regulatory advisory → extract candidate signals → assess coverage against our library + data →
> **human selects** what to build → agent drafts a signal definition → **human confirms** → backtest →
> reveal **combination lift** → coverage closes → loop repeats.

The persuasion lives in the human-in-the-loop gates (trust) and the combination-lift reveal (why composed
atoms beat monolithic scenarios).

> **This README is a thin pointer — it carries the run story only.** The durable, always-current
> architecture lives in **`CLAUDE.md`** (self-maintained each phase) and the per-subsystem docs under
> **`docs/`**; the phase-by-phase history is in **`.dev-wiki/`**. `HANDOFF.md` is a frozen M0-bootstrap
> document, not current state. *Run story last verified: Phase 66 (2026-06-22).*

## What's in here

**Six offline ship artifacts** — each a single self-contained `file://` HTML, built by `scripts/build.py`,
opened with no server:

| Artifact | Build target | What it is |
|---|---|---|
| Showcase | `fentanyl`, `trade-based`, `elder-financial-exploitation` | the generic six-act engine, one config per typology |
| Corpus explorer | `corpus` | the public regulatory corpus (FinCEN/OFAC/FINTRAC) → the signal loop, 4 lenses |
| News stream | `news` | adverse-media / negative-news screening (a second atom stream) |
| Gate console | `console` | the Class-J human-judgment adjudication gate |
| Triage console | `triage` | the §14 continuous-adjudication loop |
| Merge console | `merge` | the Class-J entity-resolution merge-adjudication gate (the one gate with a correctness oracle) |

**One companion-only investigator workbench** (`workbench.html`, served — **not** a ship/build target):
the clutter → signals → GATHER → DETERMINATION → decide arc over a vendored case population. The
DETERMINATION beat licenses the decision by **evidence-sufficiency, not combo-frequency** (a chosen-not-measured
per-typology requirement profile; the unmet gaps name what to gather or build — see `docs/evidence-driven-filing.md`);
the agentic GATHER beat is requirement-targeted; the finale is a cross-pillar signed STR.

> **Shippable vs companion — the whole dependency story in one place.** The **six ship artifacts above are
> the deliverable, fully self-contained**: a browser opens them, zero external dependencies (verified by an
> isolated clone with no sibling repos present). The **investigator workbench is a companion**, but it too is
> now shippable from a bare clone — its DECIDE signed-STR finale runs `aml-casework`, which is **vendored** into
> `vendor/aml-casework/` and built by a cross-platform `python scripts/setup_workbench.py` (Windows/mac/Linux;
> no sibling repo; offline; a model is optional, see below).
> `build.py` never imports a sibling and the offline artifacts are byte-frozen, so vendoring is a *distribution*
> choice, not coupling. The only remaining sibling touch is `../aml-substrate`, needed solely to *regenerate*
> the committed case data — never to run the demo.

## Run it — the offline demos (no build needed)

`dist/` is committed, so a fresh clone already has every demo. Just open the launcher in any browser:

```sh
git clone <repo-url> signal-watch
open signal-watch/dist/index.html        # launcher → links all 8 demos; or open dist/<target>/index.html
```

The only runtime dependency is a **web browser**. There is no server, no `pip install`, no `npm install`.

**Optional — rebuild from source** (needs only **Python ≥3.10, stdlib — no pip/uv/node**):

```sh
python3 scripts/build.py all          # or a single target: fentanyl | trade-based |
                                      #   elder-financial-exploitation | corpus | news | console | triage
python3 scripts/build.py --check all  # drift guard — committed dist == a fresh build (8/8, byte-identical)
```

## Run it — the companion servers (dev / presenter-time)

Each is a thin server on `localhost` that reads committed data and **persists nothing**.

The **investigator workbench** has a one-time setup — its DECIDE signed-STR finale runs the **vendored**
`aml-casework` pipeline (`vendor/aml-casework/`), so build that venv once (needs **Python ≥3.11 + uv** [or
pip], and network the first time). The setup is a **cross-platform Python script** — no `make`, no Unix
shell — so it runs the same on Windows / macOS / Linux:

```sh
python  scripts/setup_workbench.py    # Windows: python scripts\setup_workbench.py  (or, on POSIX: make setup)
python  scripts/serve_workbench.py    # → http://localhost:8030   the investigator workbench
```

It installs the **committed wheel** (`vendor/aml-casework/dist/aml_casework-*.whl`, pure-Python /
cross-platform) into `vendor/aml-casework/.venv`. Without setup, the workbench still runs clutter → signals
→ GATHER on the stdlib stub; only the DECIDE finale is GATED (a named message, never a crash). The other
three companions are pure **stdlib**, no setup:

```sh
python3 scripts/serve_chain.py         # → http://localhost:8020   the 3-pillar chain workbench (its precursor)
python3 scripts/serve_corpus.py        # → http://localhost:8010   live corpus derivation (paste an advisory md)
.venv/bin/python scripts/serve_news.py # → http://localhost:8000   live news extraction (.venv adds persistence/URL mode)
```

**LIVE neural mode** *(optional, all companions)* — the **openai** backend already targets a local model at
**`127.0.0.1:8080`** by default, so just start your model there and **pick "openai"** in the workbench — no env
needed. Set `OPENAI_BASE_URL` **only to override** the host/port (e.g. a different port), or set an Anthropic
key for the "claude" backend — both **server-side** (the browser never sees them). Without any model, GATHER
and the STR narrative fall back to the deterministic
stub with a named note — and the casework pipeline still shapes / signs / verifies the STR **offline**. The
vendored casework copy is pinned in `vendor/aml-casework/VENDORED_AT`; refresh it (POSIX maintainer) with
`scripts/vendor_casework.sh`, which rebuilds the wheel.

Walkthroughs: `docs/case-workbench.md`, `docs/chain-workbench.md`, `docs/corpus-live.md`, `docs/news-live.md`.

> Note: the **offline ship artifacts** need nothing but a browser. `uv` (or pip) is for
> `setup_workbench.py` (the live workbench's vendored casework venv), the DuckDB news store, the `markitdown`
> PDF→md authoring pipeline, and `uv run pytest` — never to open a ship demo.

## Test

```sh
uv run pytest                          # the umbrella (wraps the --selftests + the .mjs arc tests)
python3 scripts/build.py --check all   # drift: every committed dist == a fresh build (9/9)
node tests/corpus-explorer.test.mjs    # plus: gate-console / triage-console / merge-console / news-stream / workbench .test.mjs
python3 scripts/derive_signals.py --selftest   # the derivation GATE (and the other scripts' --selftest)
```

Before presenting, run `--check all`, the `.test.mjs` arcs, then walk `tests/smoke-checklist.md` (the
live-visual / pacing / compliance checks a human eye must confirm).

## Compliance

- **No real customer, account, or transaction data — anywhere.** All coverage / population / precision
  numbers are synthetic and illustrative, under the always-on "Illustrative data & outputs" badge.
- Real-world content is **public advisory / enforcement material, paraphrased by default**. Two verbatim
  exceptions, kept visually separate from the illustrative badge: **US-federal** sources (FinCEN, OFAC —
  public domain, 17 U.S.C. §105) and **FINTRAC** (Canadian Crown copyright, reproduced for non-commercial
  use with its required attribution). See `CLAUDE.md` for the exact compliance posture.
