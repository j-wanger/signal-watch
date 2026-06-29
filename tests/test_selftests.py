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
    "entity_spine.py",          # Phase 74 — the persistent entity spine (SKIPs gracefully w/o duckdb; full under .venv)
    "resolution_scorer.py",     # Phase 74 — the resolution-correctness scorer + the resolver-input firewall
    "curate_merge_cases.py",    # Phase 76 — the merge-console case curator (SKIPs gracefully w/o duckdb; full under .venv)
    "merge_adjudicator.py",     # Phase 83 — the merge adjudicator (firewall + stub baseline; dep-free, no model)
    "determination_proposer.py",  # Phase 85 — the §12 determination pre-proposer (firewall + two-sided stub baseline; dep-free)
    "distill_sanctions_slice.py",  # Phase 80 — the OFAC name-collision merge slice (replays the committed slice, no substrate)
    "determination_validation_harness.py",  # Phase 78 — the determination-validation firewall + recompute (dep-free)
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
    "serve_merge.py",           # Phase 83 — the merge-console live companion (offline render + firewall; no model)
]

MJS_TESTS = [
    "corpus-explorer.test.mjs",
    "gate-console.test.mjs",
    "triage-console.test.mjs",
    "merge-console.test.mjs",
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


def test_merge_adjudicator_quality_harness() -> None:
    """Phase 83 — the MERGE-ADJUDICATOR quality REGRESSION GATE: re-derive the StubAdjudicator baseline from
    the committed oracle (dep-free, no model) + replay the pinned live capture (if present) and assert the
    agent's agreement counts still match the frozen baseline (the GATHER replay pattern; counts only)."""
    path = ROOT / "tests" / "merge_adjudicator_quality_harness.py"
    assert path.exists(), "missing tests/merge_adjudicator_quality_harness.py"
    r = subprocess.run([sys.executable, str(path), "--check"], cwd=str(ROOT),
                       capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, f"merge_adjudicator_quality_harness --check FAILED:\n{r.stdout[-2000:]}\n{r.stderr[-2000:]}"


def test_determination_proposer_quality_harness() -> None:
    """Phase 85 — the §12 DETERMINATION-PROPOSER quality REGRESSION GATE: re-derive the StubProposer (engine
    echo) two-sided baseline from the committed capture (dep-free, no model) + replay the pinned live capture
    by cap-signature (if present) and assert the agent's two-sided counts still match the frozen baseline."""
    path = ROOT / "tests" / "determination_proposer_quality_harness.py"
    assert path.exists(), "missing tests/determination_proposer_quality_harness.py"
    r = subprocess.run([sys.executable, str(path), "--check"], cwd=str(ROOT),
                       capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, f"determination_proposer_quality_harness --check FAILED:\n{r.stdout[-2000:]}\n{r.stderr[-2000:]}"


def test_drafter_quality_harness_selftest() -> None:
    """Phase 86 — the STR-DRAFTER quality gate, dep-free scorer unit (no venv/model): assert score_drafts()
    counts the stub-vs-live sign/refuse + verifier-catch + consistency correctly. The committed --check
    regression gate (over the pinned live capture) is test_drafter_quality_harness below."""
    path = ROOT / "tests" / "drafter_quality_harness.py"
    assert path.exists(), "missing tests/drafter_quality_harness.py"
    r = subprocess.run([sys.executable, str(path), "--selftest"], cwd=str(ROOT),
                       capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, f"drafter_quality_harness --selftest FAILED:\n{r.stdout[-2000:]}\n{r.stderr[-2000:]}"


def test_drafter_quality_harness() -> None:
    """Phase 86 — the STR-DRAFTER quality REGRESSION GATE: replay the pinned per-bundle consume results
    (stub + live) through the pure scorer with NO casework subprocess + NO model and assert the counts
    (stub-vs-live sign/refuse, verifier/fabrication-guard catch, consistency) still match the frozen
    baseline. Consistency-not-correctness; counts only (no accuracy/catch-rate)."""
    path = ROOT / "tests" / "drafter_quality_harness.py"
    assert path.exists(), "missing tests/drafter_quality_harness.py"
    r = subprocess.run([sys.executable, str(path), "--check"], cwd=str(ROOT),
                       capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, f"drafter_quality_harness --check FAILED:\n{r.stdout[-2000:]}\n{r.stderr[-2000:]}"


def test_determination_validation_harness() -> None:
    """Phase 78 — the determination-validation REGRESSION GATE: replay the committed substrate-oracle capture
    with NO substrate and assert the live engine still matches the frozen confusion structure (the
    bundle-only signal-assembly vs the exogenous file/clear oracle; the circularity exit)."""
    path = SCRIPTS / "determination_validation_harness.py"
    assert path.exists(), "missing scripts/determination_validation_harness.py"
    r = subprocess.run([sys.executable, str(path), "--check"], cwd=str(ROOT),
                       capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, f"determination_validation_harness --check FAILED:\n{r.stdout[-2000:]}\n{r.stderr[-2000:]}"


@pytest.mark.skipif(shutil.which("node") is None, reason="node not installed — .mjs arc tests skipped")
@pytest.mark.parametrize("mjs", MJS_TESTS)
def test_mjs_arc(mjs: str) -> None:
    path = ROOT / "tests" / mjs
    assert path.exists(), f"missing tests/{mjs}"
    r = subprocess.run(["node", str(path)], cwd=str(ROOT),
                       capture_output=True, text=True, timeout=300)
    assert r.returncode == 0, f"{mjs} FAILED:\n{r.stdout[-2000:]}\n{r.stderr[-2000:]}"
