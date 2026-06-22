# Active Phase Context

**Phase 67 — *Make the LIVE investigator workbench shippable from a bare clone (vendor aml-casework + make setup)*** (signal-watch-local, LITE) — direction gate accepted 2026-06-22 (all_accept:true; A0 [the venv-builds-standalone risk] + A2 [the copy mechanism] positioned at the gate, A1/A3/A4 by precedent). A recipient who clones signal-watch can run the FULL live workbench — incl. the DECIDE signed-SAR finale — with NO sibling repo, via `make setup`.

## Objective
Vendor a COPY of aml-casework into signal-watch + a `make setup` so `git clone && make setup && python3 scripts/serve_workbench.py` gives the full live workbench OFFLINE (the deterministic stub-drafter SAR pipeline runs; no model, no sibling). The NEURAL SAR + GATHER work when the user points it at a model SERVER-SIDE (OPENAI_BASE_URL / an Anthropic key — model-you-provide, NOT bundled). The companion still SUBPROCESSES casework over the existing file-handoff — vendoring is DISTRIBUTION, not import-coupling.

## Scope
`vendor/aml-casework/**` (the vendored copy) · `scripts/vendor_casework.sh` (rsync + excludes) · `Makefile` (the `setup` target) · `.gitignore` (the vendored venv) · `scripts/serve_workbench.py` + `scripts/serve_chain.py` (default `AML_CASEWORK_DIR`/`_PYTHON` → vendored, else `../aml-casework`, else GATED) · `README.md` · `CLAUDE.md` · `docs/case-workbench.md` · `vendor/aml-casework/VENDORED_AT` · `tests/smoke-checklist.md`.

## Key constraints
- A0 (load-bearing, VERIFY-FIRST): T1 PROVES `make setup` builds the casework venv + an offline stub DECIDE finale runs in an ISOLATED /tmp clone (no siblings) BEFORE T2/T3. If `uv sync` won't build standalone → STOP, escalate to a pre-built wheel.
- A1 (boundary): vendoring is DISTRIBUTION not import-coupling — the companion subprocesses casework; build.py NEVER imports it; `vendor/` is outside build.py's world; the 5 offline ship artifacts + 8 dists BYTE-FROZEN (`--check all` 8/8).
- A2 (mechanism): a plain COPY (`src/aml_casework` + pyproject + uv.lock + README; NOT tests/.venv/.dev-wiki) + a refresh script + a `VENDORED_AT` pin. NOT git-subtree, NOT a wheel (the wheel is the A0 fallback only).
- A3: the live tier may require Python ≥3.11 + uv; the offline ship artifacts stay zero-dep (browser only), the stub workbench stdlib-3.10.
- A4: compliance-clean (casework synthetic-only — no real data); live mode optional/off-by-default with the stub-drafter fallback; GATED if `vendor/` absent.

## Exit criteria
The 4 tasks' success fields met; in an isolated no-siblings clone `git clone && make setup && serve_workbench.py` produces a signed SAR OFFLINE with the stub drafter (the shippability proof); `serve_workbench`/`serve_chain --selftest` + `uv run pytest` + `node tests/*.test.mjs` green; `build.py --check all` 8/8 ZERO dist drift; build.py imports no casework; README/CLAUDE.md/`docs/case-workbench.md` state the clone+make-setup run path + the 3.11/uv prereq + the GATED fallback; `VENDORED_AT` pins the casework commit.

## Abort
If `uv sync` won't build the vendored casework venv standalone (hidden coupling) → STOP-and-surface, escalate to a pre-built wheel (or Docker) per A0. Any vendored import sneaking into build.py / any dist drift / the subprocess boundary broken / real data in the vendored source → STOP-and-surface.

## Gates
- [x] spec — waived under LITE ceremony (the assumption-ledger gate IS the direction gate)
- [x] Direction confirmed by user (assumption positions taken 2026-06-22; A0/A2 explicit, A1/A3/A4 by precedent; all_accept:true)
- [x] Delivery accepted (post-implementation report 2026-06-22; A0 PROVEN in a no-siblings isolation clone — make setup builds the vendored casework venv + the DECIDE finale signs a SAR OFFLINE; the A0 guard surfaced + fixed the corpus-snapshot coupling [vendored fixtures/corpus too]; serve_chain CASEWORK_DIR resolves vendored>sibling>GATED; uv run pytest 18/18, workbench.test.mjs 103/0, --check all 8/8, build.py imports no casework; boundary held; committed + pushed)

Plan [[phases/phase-67-shippable-live-workbench]]; ledger Phase-67.
