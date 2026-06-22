# Chain Workbench — the analyst UI for the substrate→casework→verify chain (Phase 56–57)

> **Phase 57 update.** The neural draft is now **multi-backend** — casework's pluggable `Drafter`
> Protocol exposed through a workbench **picker**: `claude` (Anthropic, OAuth subscription **or** API
> key) · `openai` (any OpenAI-standard `/v1` server — a local model direct) · `opencode` (drafting
> driven **through** opencode's agent loop) · `stub` (deterministic, the always-on baseline). serve_chain
> selects a backend by **name** and resolves its creds/endpoint **server-side** (never the browser). The
> gate stays the oracle on whatever any backend produces. See **Drafter backends** below.

> **Illustrative data & outputs.** A **dev/authoring-time companion**, NOT a ship artifact. `chain.html`
> is companion-served by `scripts/serve_chain.py`; it is never built into `dist/` and is not a
> `build.py` target. The 8 offline ship dists stay byte-frozen (`build.py --check all` → 8/8). Nothing is
> persisted — a signed STR is written to a per-run temp dir and discarded.

## What it is

An analyst **case-workbench** over the 3-pillar chain. Detection is **pre-baked upstream**: each case is a
real `aml-substrate` evidence bundle, vendored under `data/chain-cases/` like the corpus pin (synthetic,
illustrative). Per case, the **downstream runs live**:

1. **Evidence** — the vendored detection bundle (alerts across capabilities, transactions, subject).
2. **Consume** — `aml-casework` ingests the bundle, drafts the STR narrative (the **picked backend** —
   live neural via claude/openai/opencode **or** the deterministic stub), and runs the six Class-G
   verifiers + narrative grounding → signed, zero blocking violations. The consume stage shows the
   **gate verdict on the generated draft** (the gate is the oracle, whatever the backend produced).
3. **Verify** — signal-watch's `e2e_chain_check --real` re-verifies the cross-pillar join.
4. **Connected** — the signed STR + the **flag→corpus audit walk**: every signal traces back to a
   public-source regulator indicator in the frozen corpus. The structured STR record renders its
   **completeness** (Phase 69): the previously-dropped FINTRAC fields (aliases, beneficial ownership, IP/VC,
   DOB, named relationships, account action) are surfaced as explicit **honest-NULL** gaps, and a completeness
   panel reports the required STR elements + the determination ATOMS the case carries vs the honest gaps (what
   a determination needs beyond a filing — see `docs/evidence-driven-filing.md`).

Results stream as NDJSON **stages** (completed/grounded reveals — never a token stream).

## The boundary (load-bearing)

**Subprocess + file-handoff only.** `serve_chain.py` never imports `aml_substrate` / `aml_casework`
(the one-repo-per-pillar rule). The casework consume is a subprocess of its **own** CLI
(`python -m aml_casework.ingest`); the bundle and the signed STR cross as json files. The only imports are
signal-watch's own modules (`e2e_chain_check`, `derive_signals`, `validate_chain_cases`).

The committed `data/pillar-status.json` (which the launcher inlines) is **snapshot + restored** around the
verify subprocess — a workbench run reflects the pre-baked bridge states, it never moves them (that would
drift the launcher dist).

## Run recipe

```bash
# 0. the case library is already vendored + validated:
python3 scripts/validate_chain_cases.py            # every bundle passes the substrate-side bar

# 1. (optional) enable one or more LIVE neural backends — all creds/endpoints stay server-side, the
#    browser only ever sends a backend NAME. Any subset may be set; absent backends show "n/a":
export ANTHROPIC_AUTH_TOKEN=...                    # claude via the Claude subscription (OAuth) …
export ANTHROPIC_API_KEY=sk-...                    # … or claude via an API key (either makes claude available)
export OPENAI_BASE_URL=http://127.0.0.1:8080/v1    # openai: a local llama-server (OPENAI_API_KEY optional)
export OPENCODE_SERVE_URL=http://127.0.0.1:4096    # opencode: an `opencode serve` endpoint (agent loop)
#    (set NONE ⇒ only the deterministic stub is available — the keyless default still runs the full chain)

# 2. point at the casework checkout (defaults to ../aml-casework):
export AML_CASEWORK_DIR=/Users/jwang/aml-casework  # optional; AML_CASEWORK_PYTHON overrides the interpreter

# 3. start the companion + open it:
python3 scripts/serve_chain.py                     # http://localhost:8020
```

Pick a case → choose a **Drafter** in the picker (only server-side-available backends are selectable) →
**Run the chain** → watch the stages reveal to CONNECTED, read the signed STR, and walk each signal down to
its regulator flag. Run the **stub** then a **neural** backend on the same case to see the **drafts
compared** side by side — each one gated. The header chip shows the selected drafter.

## Drafter backends (Phase 57)

The drafter is casework's pluggable `Drafter` Protocol; serve_chain offers it as a **name pass-through**.
The browser sends a backend **name**; serve_chain maps it to the casework CLI's `--drafter` flag and
resolves the creds/endpoint from its **own env** (the casework subprocess inherits them). A name that is
unknown or unavailable falls back **honestly** to the stub with a named note — never a crash, never a
silent neural→neural switch.

| name | what drafts | server-side env to enable | casework adapter |
|------|-------------|---------------------------|------------------|
| `stub` | deterministic, bundle-derived (the baseline) | — (always available) | `drafter_stub.py` ✅ |
| `claude` | Anthropic (claude-opus-4-8) | `ANTHROPIC_AUTH_TOKEN` (OAuth) **or** `ANTHROPIC_API_KEY` | `drafter_claude.py` ✅ (casework Phase 8) |
| `openai` | any OpenAI-standard `/v1` server (a local model direct) | `OPENAI_BASE_URL` (+ optional `OPENAI_API_KEY`/`OPENAI_MODEL`) | `drafter_openai.py` ⛔ **gated** (brief: `aml-casework/docs/openai-drafter-PLAN-BRIEF.md`) |
| `opencode` | drafting driven **through** opencode's agent loop | `OPENCODE_SERVE_URL` | `drafter_opencode.py` ⛔ **gated** (brief: `aml-casework/docs/opencode-drafter-PLAN-BRIEF.md`) |

Whichever backend drafts, casework's **six Class-G verifiers + narrative grounding dispose the result** —
a hallucinated local-model draft is *caught at the gate*, which is the honesty demonstration, not a
regression. **Non-negotiable §4.5:** no key/token/`base_url` is ever inlined into the page or sent to the
browser — `serve_chain --selftest` asserts the served config + page carry only names + booleans.

## Two beats

### Beat 1 — the SPINE + live-claude (now, signal-watch-local)

The signal-watch spine (the N-backend pass-through + the workbench picker + the live-draft staged reveal +
the gate verdict on the generated narrative + the re-grounded casework pin `@2381d71`) is delivered and
selftest-proven. The live **`claude`** path is drivable here whenever `ANTHROPIC_AUTH_TOKEN`/
`ANTHROPIC_API_KEY` is set server-side (casework's OAuth `ClaudeDrafter` landed at Phase 8); **keyless**,
it runs the full chain on the deterministic stub and says so (`drafter_effective: stub`).

> **State of this session:** the spine + the re-grounded pin are done; the real chain **CONNECTED** against
> casework@2381d71 via the stub drafter. No anthropic creds were present in this env, so the *live neural*
> claude draft was not exercised here — it runs end-to-end the moment a token/key is set (the fail-soft is
> built and tested; the live neural path is also covered by casework `@integration`).

#### selftest-proven offline

```bash
python3 scripts/serve_chain.py --selftest          # offline; the casework consume STUBBED → CONNECTED
node tests/chain.test.mjs                           # the workbench client (stage rendering, badge, XSS, NDJSON)
python3 scripts/validate_chain_cases.py --selftest  # the vendored library + the validator
python3 scripts/build.py --check all                # 8/8 — chain.html is not a build target
```

`serve_chain --selftest` runs the full pipeline with the casework consume replaced by an offline
stand-in (a deterministic, check-passing signed STR built from the bundle), and the **real**
`e2e_chain_check --real` verify (offline, pure Python) reaches **CONNECTED** — proving the orchestration,
the audit walk, the stage stream, and the `pillar-status` snapshot/restore, without the sibling CLI.

> The casework **consume CLI** + the `claude` adapter are no longer gated — they landed in casework
> Phases 7–8. What's gated for Phase 57 is the **openai + opencode** adapters (beat 2).

### Beat 2 — the live `openai` + `opencode` backends (gated on casework adapters)

Two sibling adapters, each a thin implementation of casework's `Drafter` Protocol (authored as briefs
here, executed in aml-casework-rooted sessions):

- **`drafter_openai.py`** (`aml-casework/docs/openai-drafter-PLAN-BRIEF.md`) — a `/v1/chat/completions`
  adapter mirroring `drafter_claude.py`; with `OPENAI_BASE_URL` pointed at a local llama-server, a Run
  with the **openai** backend drafts on the local model → the six verifiers gate it → **CONNECTED**.
- **`drafter_opencode.py`** (`aml-casework/docs/opencode-drafter-PLAN-BRIEF.md`) — drives **opencode's
  agent loop** (`opencode serve`, OpenAPI + SSE; a local model via opencode's openai-compatible provider).
  The load-bearing leg (the A0 risk): headless `serve` + SSE feasibility.

Until an adapter lands, picking that backend (when its env is set) routes through the casework CLI; an
absent adapter / failed call fails **honestly** in-stream (a named "drafter error → fell back to the
stub" note), never a faked connection. The signal-watch spine — picker, name pass-through, selftest — is
already in place, so each adapter is a drop-in once it lands.

## Isolation guarantees (the abort rules)

- `chain.html` is **not** a build target and is **not** in `dist/` — `grep -nE "chain\.html|serve_chain"
  scripts/build.py` is clean; `build.py --check all` → 8/8, the offline dists byte-identical.
- No sibling import: `grep -nE "import aml_substrate|import aml_casework" scripts/serve_chain.py` is clean.
- Every backend's creds/endpoint (`ANTHROPIC_AUTH_TOKEN`/`ANTHROPIC_API_KEY`, `OPENAI_BASE_URL`/`OPENAI_API_KEY`,
  `OPENCODE_SERVE_URL`) is read **server-side only** — never inlined into the page or sent to the browser
  (the browser sends a backend **name**); `serve_chain --selftest` asserts no secret/endpoint leaks into
  the served config or page (non-negotiable §4.5).
- A validator/verifier that looks like it needs loosening → fix the data/design, never the validator.
