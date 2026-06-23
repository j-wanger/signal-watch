"""Pytest umbrella over signal-watch's REAL, dep-free test mechanism.

signal-watch ships self-contained offline HTML (NO Python ships); its Python is build/authoring tooling
tested dep-free via `--selftest` entrypoints, and its HTML clients via zero-dep Node `.mjs` harnesses.
This module is a THIN wrapper so `uv run pytest` runs the whole suite (parity with the sibling Python
pillars aml-substrate / aml-casework) WITHOUT changing that mechanism — each case shells out to the
EXACT dep-free command, so `python3 scripts/X.py --selftest` and `node tests/X.test.mjs` stay the
no-install source of truth. There is intentionally no `src/` package and no in-process import coupling.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"

# Dep-free `--selftest` entrypoints (stdlib only; no venv/model/network). The DuckDB-store selftests
# (news_store.py, the .venv-gated halves of news_live_test.py) are deliberately EXCLUDED — they need the
# gitignored uv .venv and are run separately, per CLAUDE.md.
PY_SELFTESTS = [
    "curate_workbench_cases.py",
    "osint_tools.py",
    "evidence_requirements.py",
    "serve_workbench.py",
    "serve_chain.py",
    "validate_chain_cases.py",
    "e2e_chain_check.py",
    "curate_triage_scenarios.py",
    "derive_signals.py",
    "news_ground.py",
    "news_fetch.py",
    "serve_corpus.py",
    "serve_news.py",
]

MJS_TESTS = [
    "corpus-explorer.test.mjs",
    "gate-console.test.mjs",
    "triage-console.test.mjs",
    "news-stream.test.mjs",
    "chain.test.mjs",
    "workbench.test.mjs",
]


@pytest.mark.parametrize("script", PY_SELFTESTS)
def test_python_selftest(script: str) -> None:
    path = SCRIPTS / script
    assert path.exists(), f"missing scripts/{script}"
    r = subprocess.run([sys.executable, str(path), "--selftest"], cwd=str(ROOT),
                       capture_output=True, text=True, timeout=300)
    assert r.returncode == 0, f"{script} --selftest FAILED:\n{r.stdout[-2000:]}\n{r.stderr[-2000:]}"


def test_gather_quality_harness() -> None:
    """Phase 70 — the GATHER extraction-coverage REGRESSION GATE: replay the pinned live capture with NO
    model and assert the outcome still matches the baseline + the deterministic stub reference."""
    path = ROOT / "tests" / "gather_quality_harness.py"
    assert path.exists(), "missing tests/gather_quality_harness.py"
    r = subprocess.run([sys.executable, str(path), "--check"], cwd=str(ROOT),
                       capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, f"gather_quality_harness --check FAILED:\n{r.stdout[-2000:]}\n{r.stderr[-2000:]}"


@pytest.mark.skipif(shutil.which("node") is None, reason="node not installed — .mjs arc tests skipped")
@pytest.mark.parametrize("mjs", MJS_TESTS)
def test_mjs_arc(mjs: str) -> None:
    path = ROOT / "tests" / mjs
    assert path.exists(), f"missing tests/{mjs}"
    r = subprocess.run(["node", str(path)], cwd=str(ROOT),
                       capture_output=True, text=True, timeout=300)
    assert r.returncode == 0, f"{mjs} FAILED:\n{r.stdout[-2000:]}\n{r.stderr[-2000:]}"
