---
title: "Codebase snapshot — 2026-06-21 (Phase 63 debrief)"
aliases: []
category: status
tags: [snapshot, phase-63, workbench, companion-demo, pytest-wrapper]
parents: []
created: 2026-06-21
updated: 2026-06-21
source: debrief
---

# Codebase snapshot — 2026-06-21 (Phase 63 debrief)

## File metrics
- HTML templates + companions: 9 (`index.html`, `corpus.html`, `news.html`, `console.html`, `triage.html`, `chain.html`, `workbench.html` [Phase 63 NEW] + the launcher `dist/index.html` source)
- `scripts/*.py`: 22 (incl. the NEW `serve_workbench.py` + `curate_workbench_cases.py`)
- node arc tests: 7 (`corpus-explorer`, `news-stream`, `gate-console`, `triage-console`, `chain`, `launcher`, `workbench` [Phase 63 NEW])
- pytest umbrella (Phase 63 NEW): `tests/test_selftests.py` — 17 parametrized cases (11 python `--selftest` + 6 `.mjs`); `uv run pytest` runs the whole suite
- committed dist targets: 7 (3 typologies + corpus + news + console + triage) + the launcher = the 8-target `--check all`

## Module structure (durable — see _ARCHITECTURE.md)
- 5 offline ship artifacts (showcase / corpus / news / console / triage) + the launcher = the 8-target build.
- Companion-only (NOT build targets): the news/corpus live backbones, `serve_chain.py` + `chain.html` (Phase 56/57), and now `serve_workbench.py` + `workbench.html` (Phase 63 — the investigator case workbench over the vendored aml-substrate population slice). build.py imports NO sibling (subprocess + file-contract).

## Dependencies
- Ship: none. Authoring/companion: `markitdown[pdf]` + `duckdb` (gitignored uv `.venv`). Phase 63 added `pytest` as a DEV dep (`pyproject.toml` [tool.uv] package=false; gitignored `.venv`) — NO new runtime dep; the dep-free `--selftest`/`.mjs` paths stay the source of truth.

## Test status (verified this session)
- `uv run pytest` → 17 passed.
- `python3 scripts/build.py --check all` → 8/8, ZERO dist drift (`git diff --stat HEAD -- dist/` empty).
- `node tests/workbench.test.mjs` → 61 assertions green.
- `! grep import aml_substrate|aml_casework` clean in build.py.
- `data/workbench/cases.json` → 200 cases, coverage 57/200 MEASURED, pinned aml-substrate@f90bd39 / aml-casework@c6d8401; gate funnel 129 auto-clear / 52 review / 19 human-gate.

## Recent commits
- `e320661` WIP: snapshot .claude before kit hook re-sync
- `1d35f84` Phase 62 — Grounded probe-history consume (§12); §14-frozen boundary; P22 pin re-ground
- `58925a8` Phase 61 — mark delivery gate accepted (gate-state follows git-state)
- `a4f30e2` Phase 61 — Blueprint review against implementations: three-tier true-up + batched cross-pillar re-ground
- `67dbd65` Phase 60 — Consume the landed sibling halves: the C7 reachable-now rise + the real e2e chain

## Notable
- Phase 63 (Investigator Case Workbench) DELIVERED, READY FOR COMPLETION — delivery gate pending the commit (uncommitted working tree: `workbench.html`, `scripts/{serve_workbench,curate_workbench_cases}.py`, `data/workbench/`, `tests/{workbench.test.mjs,test_selftests.py}`, `pyproject.toml`, `uv.lock`, `docs/case-workbench.md`, plus the smoke-checklist entry + the dev-wiki updates).
- The T4 cross-pillar finding: composed cases fail on a real substrate↔casework C3/C15 replay divergence (~28% of composed cases sign) → embraced as the FAIL-CLOSED defensibility climax; the verifier was never loosened (abort rule held). A C3/C15 contract-alignment phase is the surfaced sibling-repo follow-on.
