---
title: "Phase 67: Make the LIVE investigator workbench shippable from a bare clone (vendor aml-casework + make setup)"
aliases: []
category: phases
tags: [vendoring, distribution, live-workbench, casework, make-setup, lite]
parents: [dev-wiki]
created: 2026-06-22
updated: 2026-06-22
source: plan
status: active
scope: ["vendor/aml-casework/**", "scripts/vendor_casework.sh", "Makefile", ".gitignore", "scripts/serve_workbench.py", "scripts/serve_chain.py", "README.md", "CLAUDE.md", "docs/case-workbench.md", "vendor/aml-casework/VENDORED_AT", "tests/smoke-checklist.md"]
entry_criteria: "Phase 66 delivered + accepted (committed 0fa3830 + the uncommitted doc-hygiene 7340012); the LIVE investigator workbench (workbench.html + serve_workbench.py + the DECIDE → serve_chain → casework consume finale) runs only with a sibling aml-casework checkout at ../aml-casework; aml-casework@81df91c (feat/phase-1a-deterministic-verifiers) is local-only / no remote — which is WHY we vendor instead of submodule."
exit_criteria: "In an isolated no-siblings clone, git clone && make setup && python3 scripts/serve_workbench.py produces a signed SAR OFFLINE with the stub drafter (the shippability proof); the companion still SUBPROCESSES casework over the file-handoff; build.py imports no casework; the 5 offline ship artifacts + 8 dists BYTE-FROZEN (--check all 8/8); README/CLAUDE.md/docs/case-workbench.md state the clone+make-setup run path + the 3.11/uv live-tier prereq + the GATED fallback; VENDORED_AT pins casework@81df91c."
---

# Phase 67: Make the LIVE investigator workbench shippable from a bare clone (vendor aml-casework + make setup)

## Objective

Make the LIVE investigator workbench SHIPPABLE from a bare `git clone` of signal-watch — a recipient runs the full live workbench, including the DECIDE signed-SAR finale, with NO sibling repo, via `make setup`. The mechanism is to VENDOR a copy of the sibling `aml-casework` (its `src/aml_casework` + pyproject + uv.lock + README; NOT tests/.venv/.dev-wiki) into `vendor/aml-casework/` via `scripts/vendor_casework.sh` + a `VENDORED_AT` pin (casework@81df91c); a `Makefile` `make setup` builds the vendored venv (`uv venv` + `uv sync`). The companion `serve_workbench.py`/`serve_chain.py` default `AML_CASEWORK_DIR`/`_PYTHON` → the vendored path when present, else `../aml-casework`, else a named GATED message. Vendoring is a DISTRIBUTION choice, NOT import-coupling — the companion still SUBPROCESSES casework over the existing file-handoff; build.py NEVER imports casework. Live tier = "real pipeline + model-you-provide": the deterministic stub-drafter SAR pipeline runs OFFLINE; the neural SAR/GATHER need a model set SERVER-SIDE (OPENAI_BASE_URL / Anthropic key), NOT bundled.

## Scope

Files and modules affected:
- `vendor/aml-casework/**` — the vendored copy (src + pyproject + uv.lock + README; NOT tests/.venv/.dev-wiki)
- `scripts/vendor_casework.sh` — the refresh script (rsync + excludes)
- `Makefile` — the `setup` target (`uv venv` + `uv sync` in the vendored tree)
- `.gitignore` — the vendored venv
- `scripts/serve_workbench.py` + `scripts/serve_chain.py` — default `AML_CASEWORK_DIR`/`_PYTHON` → vendored, else `../aml-casework`, else GATED
- `README.md` · `CLAUDE.md` · `docs/case-workbench.md` — the clone+make-setup run path + the 3.11/uv prereq + the GATED fallback
- `vendor/aml-casework/VENDORED_AT` — the casework commit pin (81df91c)
- `tests/smoke-checklist.md` — the shippability E2E + smoke rows

The substrate/casework emit is TOOL-USE (build.py NEVER imports aml_substrate/aml_casework; the companion subprocesses casework over the existing file-handoff — file-contract).

## Exit Criteria

- [ ] The 4 tasks' success fields met.
- [ ] In an isolated no-siblings clone, `git clone && make setup && python3 scripts/serve_workbench.py` produces a signed SAR OFFLINE with the stub drafter (the shippability proof).
- [ ] `serve_workbench`/`serve_chain --selftest` + `uv run pytest` + `node tests/*.test.mjs` green.
- [ ] `build.py --check all` 8/8 ZERO dist drift; build.py imports no casework.
- [ ] README/CLAUDE.md/`docs/case-workbench.md` state the clone+make-setup run path + the 3.11/uv live-tier prereq + the GATED fallback.
- [ ] `VENDORED_AT` pins the casework commit (81df91c).

## Tasks

- **T1 — Vendor casework + PROVE the venv builds in isolation (the A0 guard, do FIRST).** Write `scripts/vendor_casework.sh` (rsync + excludes) → copy `src/aml_casework` + pyproject + uv.lock + README into `vendor/aml-casework/`; add `VENDORED_AT` (casework@81df91c) + the `Makefile` `setup` target + the `.gitignore` venv entry. PROVE in an ISOLATED /tmp clone (no siblings) that `make setup` builds the casework venv AND an offline stub DECIDE finale runs, BEFORE T2/T3. If `uv sync` won't build standalone → STOP, escalate to a pre-built wheel.
- **T2 — Wire the companion default → vendored.** `serve_workbench.py` + `serve_chain.py` default `AML_CASEWORK_DIR`/`_PYTHON` → the vendored path when present, else `../aml-casework`, else a named GATED message; the subprocess + file-handoff boundary unchanged (no sibling import).
- **T3 — Docs + the pin.** README + CLAUDE.md + `docs/case-workbench.md` state the `git clone && make setup` run path + the Python ≥3.11 + uv live-tier prereq + the GATED `vendor/`-absent fallback + the "real pipeline + model-you-provide" live tier; `VENDORED_AT` pins casework@81df91c.
- **T4 — Regression + shippability E2E + smoke.** `--check all` 8/8 ZERO dist drift; build.py imports no casework; `serve_workbench`/`serve_chain --selftest` + `uv run pytest` + `node tests/*.test.mjs` green; the isolated-clone shippability E2E + smoke rows in `tests/smoke-checklist.md`.

## Constraints (A0–A4)

- **A0 (load-bearing, VERIFY-FIRST; the weakest assumption):** T1 PROVES `make setup` builds the casework venv + an offline stub DECIDE finale runs in an ISOLATED /tmp clone (no siblings) BEFORE T2/T3 — prevents shipping a clone that can't build. If `uv sync` won't build standalone (hidden coupling) → STOP, escalate to a pre-built wheel (or Docker).
- **A1 (boundary):** vendoring is DISTRIBUTION, not import-coupling — the companion subprocesses casework; build.py NEVER imports it; `vendor/` is outside build.py's world; the 5 offline ship artifacts + 8 dists BYTE-FROZEN (`--check all` 8/8) — prevents the vendored copy leaking into the engine or drifting a dist.
- **A2 (mechanism):** a plain COPY (`src/aml_casework` + pyproject + uv.lock + README; NOT tests/.venv/.dev-wiki) + a refresh script + a `VENDORED_AT` pin — NOT git-subtree, NOT a wheel (the wheel is the A0 fallback only) — prevents an over-heavy distribution mechanism.
- **A3 (prereq):** the live tier may require Python ≥3.11 + uv; the offline ship artifacts stay zero-dep (browser only), the stub workbench stdlib-3.10 — prevents the live-tier toolchain leaking into the always-offline non-negotiable.
- **A4 (compliance):** compliance-clean (casework synthetic-only — no real data); live mode optional/off-by-default with the stub-drafter fallback; GATED if `vendor/` absent — prevents real data or a hard live-mode dependency entering the ship surface.

## Checkpoints

- After T1: if `uv sync` won't build the vendored casework venv standalone (hidden coupling) → STOP-and-surface, escalate to a pre-built wheel (or Docker) per A0 — do NOT proceed to T2/T3.
- If any vendored import sneaks into build.py / any dist drift / the subprocess boundary breaks / real data in the vendored source → STOP-and-surface.

## Assumptions

- aml-casework@81df91c (feat/phase-1a-deterministic-verifiers) is local-only / no remote → vendor (copy + refresh script + pin), not submodule. If a public remote later exists: revisit submodule-vs-vendor.
- The vendored casework venv builds standalone via `uv sync`. If false (T1 disproves it): escalate to a pre-built wheel (or Docker) — the A0 fallback.

## Notes

- Ceremony: LITE (the assumption-ledger gate IS the direction gate; spec waived). Direction gate accepted 2026-06-22, all_accept:true — A0 (the venv-builds-standalone risk) + A2 (the copy mechanism) positioned at the gate, A1/A3/A4 by precedent.
- Grounded against signal-watch HEAD (the Phase-66 commit 0fa3830 + the uncommitted doc-hygiene 7340012) and aml-casework@81df91c.
- Sibling-brief precedent: the Phase-55–58 rhythm; here the vendored copy is the distribution, the live run stays subprocess-over-file-handoff.
- Ledger: Phase-67 block in `assumption-ledger.md`.
