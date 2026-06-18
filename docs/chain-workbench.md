# Chain Workbench — the analyst UI for the substrate→casework→verify chain (Phase 56)

> **Illustrative data & outputs.** A **dev/authoring-time companion**, NOT a ship artifact. `chain.html`
> is companion-served by `scripts/serve_chain.py`; it is never built into `dist/` and is not a
> `build.py` target. The 8 offline ship dists stay byte-frozen (`build.py --check all` → 8/8). Nothing is
> persisted — a signed SAR is written to a per-run temp dir and discarded.

## What it is

An analyst **case-workbench** over the 3-pillar chain. Detection is **pre-baked upstream**: each case is a
real `aml-substrate` evidence bundle, vendored under `data/chain-cases/` like the corpus pin (synthetic,
illustrative). Per case, the **downstream runs live**:

1. **Evidence** — the vendored detection bundle (alerts across capabilities, transactions, subject).
2. **Consume** — `aml-casework` ingests the bundle, drafts the SAR narrative (live neural **or**
   deterministic stub), and runs the six Class-G verifiers → signed, zero blocking violations.
3. **Verify** — signal-watch's `e2e_chain_check --real` re-verifies the cross-pillar join.
4. **Connected** — the signed SAR + the **flag→corpus audit walk**: every signal traces back to a
   public-source regulator indicator in the frozen corpus.

Results stream as NDJSON **stages** (completed/grounded reveals — never a token stream).

## The boundary (load-bearing)

**Subprocess + file-handoff only.** `serve_chain.py` never imports `aml_substrate` / `aml_casework`
(the one-repo-per-pillar rule). The casework consume is a subprocess of its **own** CLI
(`python -m aml_casework.ingest`); the bundle and the signed SAR cross as json files. The only imports are
signal-watch's own modules (`e2e_chain_check`, `derive_signals`, `validate_chain_cases`).

The committed `data/pillar-status.json` (which the launcher inlines) is **snapshot + restored** around the
verify subprocess — a workbench run reflects the pre-baked bridge states, it never moves them (that would
drift the launcher dist).

## Run recipe

```bash
# 0. the case library is already vendored + validated:
python3 scripts/validate_chain_cases.py            # every bundle passes the substrate-side bar

# 1. (optional) the LIVE neural draft — server-side key, never reaches the browser:
export ANTHROPIC_API_KEY=sk-...                    # absent ⇒ deterministic stub draft (the default)

# 2. point at the casework checkout (defaults to ../aml-casework):
export AML_CASEWORK_DIR=/Users/jwang/aml-casework  # optional; AML_CASEWORK_PYTHON overrides the interpreter

# 3. start the companion + open it:
python3 scripts/serve_chain.py                     # http://localhost:8020
```

Pick a case → **Run the chain** → watch the four stages reveal to CONNECTED, then read the signed SAR and
walk each signal down to its regulator flag. With a key set, the header chip shows **live · claude-opus-4-8**;
without one, **deterministic stub**.

## Two beats (like Phase 55)

The chain workbench has the same two-beat shape as the cross-pillar bridge: the signal-watch **spine** is
deliverable + proven now; the **live neural run** is gated on one sibling prerequisite.

### Beat 1 — the SPINE (now, selftest-proven offline)

```bash
python3 scripts/serve_chain.py --selftest          # offline; the casework consume STUBBED → CONNECTED
node tests/chain.test.mjs                           # the workbench client (stage rendering, badge, XSS, NDJSON)
python3 scripts/validate_chain_cases.py --selftest  # the vendored library + the validator
python3 scripts/build.py --check all                # 8/8 — chain.html is not a build target
```

`serve_chain --selftest` runs the full pipeline with the casework consume replaced by an offline
stand-in (a deterministic, check-passing signed SAR built from the bundle), and the **real**
`e2e_chain_check --real` verify (offline, pure Python) reaches **CONNECTED** — proving the orchestration,
the audit walk, the stage stream, and the `pillar-status` snapshot/restore, without the sibling CLI.

### Beat 2 — the LIVE run (the delivery gate; gated on the casework consume CLI)

The one prerequisite is the thin casework consume CLI — `aml-casework/docs/consume-cli-PLAN-BRIEF.md`
(authored here, executed in an aml-casework-rooted session). Once it lands:

- **No key:** Run a case → the workbench subprocesses `python -m aml_casework.ingest … --drafter stub` →
  a deterministic signed SAR → `e2e_chain_check --real` → **CONNECTED** end-to-end on real sibling code.
- **Key set:** the same path with `--drafter claude` → a **real neural SAR drafted in the browser** →
  the six verifiers gate it → **CONNECTED**. A live API hiccup falls back to the stub and says so
  (`drafter_effective: stub`) — a hiccup degrades, it never breaks the chain.

Until the CLI lands, a live Run fails **honestly** in-stream: a named *"casework consume failed (the
consume CLI may not be implemented yet — bridge gated)"* banner, never a faked connection.

## Isolation guarantees (the abort rules)

- `chain.html` is **not** a build target and is **not** in `dist/` — `grep -nE "chain\.html|serve_chain"
  scripts/build.py` is clean; `build.py --check all` → 8/8, the offline dists byte-identical.
- No sibling import: `grep -nE "import aml_substrate|import aml_casework" scripts/serve_chain.py` is clean.
- The `ANTHROPIC_API_KEY` is read server-side only; it is never inlined into the page or sent to the browser.
- A validator/verifier that looks like it needs loosening → fix the data/design, never the validator.
