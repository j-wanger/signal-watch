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

**Five offline ship artifacts** — each a single self-contained `file://` HTML, built by `scripts/build.py`,
opened with no server:

| Artifact | Build target | What it is |
|---|---|---|
| Showcase | `fentanyl`, `trade-based`, `elder-financial-exploitation` | the generic six-act engine, one config per typology |
| Corpus explorer | `corpus` | the public regulatory corpus (FinCEN/OFAC/FINTRAC) → the signal loop, 4 lenses |
| News stream | `news` | adverse-media / negative-news screening (a second atom stream) |
| Gate console | `console` | the Class-J human-judgment adjudication gate |
| Triage console | `triage` | the §14 continuous-adjudication loop |

**One companion-only investigator workbench** (`workbench.html`, served — **not** a ship/build target):
the clutter → signals → decide arc over a vendored case population, with an agentic GATHER beat and a
cross-pillar signed-SAR finale.

> **Shippable vs companion — the whole dependency story in one place.** The **five ship artifacts above are
> the deliverable, and are fully self-contained**: a browser opens them, zero external dependencies (verified
> by cloning into an isolated dir with no sibling repos present). The **workbench is a companion dev/presenter
> tool, not a ship target** — and only its final **DECIDE** beat depends on the sibling `../aml-casework` repo;
> if that's absent, DECIDE fails closed with a named "GATED" message (never a crash) and the rest of the arc
> still runs. `build.py` never imports a sibling. There is **no other cross-repo dependency** — the case data
> the workbench reads is committed (`../aml-substrate` is needed only to *regenerate* it, never to run it).

## Run it — the offline demos (no build needed)

`dist/` is committed, so a fresh clone already has every demo. Just open the launcher in any browser:

```sh
git clone <repo-url> signal-watch
open signal-watch/dist/index.html        # launcher → links all 7 demos; or open dist/<target>/index.html
```

The only runtime dependency is a **web browser**. There is no server, no `pip install`, no `npm install`.

**Optional — rebuild from source** (needs only **Python ≥3.10, stdlib — no pip/uv/node**):

```sh
python3 scripts/build.py all          # or a single target: fentanyl | trade-based |
                                      #   elder-financial-exploitation | corpus | news | console | triage
python3 scripts/build.py --check all  # drift guard — committed dist == a fresh build (8/8, byte-identical)
```

## Run it — the companion servers (dev / authoring-time)

Each is a thin **stdlib** server on `localhost` that reads committed data and **persists nothing**.

```sh
python3 scripts/serve_workbench.py     # → http://localhost:8030   the investigator workbench (what you most likely want)
python3 scripts/serve_chain.py         # → http://localhost:8020   the 3-pillar chain workbench (its precursor)
python3 scripts/serve_corpus.py        # → http://localhost:8010   live corpus derivation (paste an advisory md)
.venv/bin/python scripts/serve_news.py # → http://localhost:8000   live news extraction (.venv adds persistence/URL mode)
```

The clutter → signals → GATHER beats run on a **deterministic stub with no model**. Two things go beyond plain
stdlib — both **set server-side** (the browser never sees credentials):

- **LIVE neural mode** *(optional, all companions)* — a local OpenAI-compatible model on `127.0.0.1:8080`:
  `export OPENAI_BASE_URL=http://127.0.0.1:8080/v1` (e.g. a llama-server with a Qwen ~30B-A3B GGUF). Without
  it, GATHER / extraction fall back to the deterministic stub with a named note. The offline ship artifacts
  carry no model code at all.
- **The workbench DECIDE finale** *(the signed-SAR step)* — subprocesses the sibling **`../aml-casework`** repo
  (override with `$AML_CASEWORK_DIR`). Required in **both stub and live modes** — the model backend only
  chooses the SAR *prose*; the shaping/signing/verifying is the sibling's job and has **no local fallback**.
  Absent → DECIDE returns a named **"GATED"** message; clutter → signals → GATHER are unaffected. *(The slice
  re-vendor is the only other sibling touch — it needs `../aml-substrate` — but that regenerates committed
  data; running the demo never needs it.)*

Walkthroughs: `docs/case-workbench.md`, `docs/chain-workbench.md`, `docs/corpus-live.md`, `docs/news-live.md`.

> Note: `uv` / a `.venv` is **only** for `markitdown` (the PDF→md authoring pipeline), the DuckDB news
> store, and the `uv run pytest` test umbrella — never to run a demo.

## Test

```sh
uv run pytest                          # the umbrella (wraps the --selftests + the .mjs arc tests)
python3 scripts/build.py --check all   # drift: every committed dist == a fresh build (8/8)
node tests/corpus-explorer.test.mjs    # plus: gate-console / triage-console / news-stream / workbench .test.mjs
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
