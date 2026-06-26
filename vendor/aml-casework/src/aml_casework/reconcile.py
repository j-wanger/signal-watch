"""Advisory reconciliation runner — fire ALL the drift tripwires as one consolidated report.

Phase 15 + 16 built sibling-gated drift tripwires (``detector_reconciliation.check_detector_drift``,
``corpus_grounding.check_corpus_drift``) that SURFACE — never gate — when casework's COPIED screening
logic / vendored corpus drifts off the live substrate source. This module is the single entrypoint that
runs them together: ``python -m aml_casework.reconcile`` (the ``ingest.py`` precedent).

POSTURE (the Phase-15 doctrine, preserved): WARN-NEVER-FAIL — a drift is a human re-pin SIGNAL, not a
build break; the underlying checks never raise. HONEST-SKIP — an absent sibling yields ``skipped``
(observable, never a false ``in_sync``), not a crash. The runner exits non-zero ONLY on ``drift`` so a
local or scheduled run surfaces a LOUD signal; the hosted CI lane runs it NON-REQUIRED
(``continue-on-error``), so the signal never blocks a merge. This is a TOOL, not a per-bundle verifier —
the 6-verifier chain never imports it, and it never imports ``aml_substrate`` (it reuses the existing
AST-read / vendored-read paths). The behavioral ``@integration`` tripwires (C14, replay) run alongside
via ``pytest -m reconciliation``; this runner covers the warn-never-fail ``DriftReport`` checks.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections.abc import Callable
from dataclasses import dataclass

from aml_casework.corpus_grounding import DriftReport, check_corpus_drift
from aml_casework.detector_reconciliation import check_detector_drift


@dataclass(frozen=True)
class TripwireResult:
    """One named tripwire's :class:`DriftReport` (e.g. ``detector-drift`` -> in_sync / drift / skipped)."""

    name: str
    report: DriftReport


def _run_tripwire(name: str, check: Callable[[], DriftReport]) -> TripwireResult:
    """Run one drift check, enforcing warn-never-fail AT THE ENTRYPOINT: a live source that is PRESENT
    but unreadable / malformed (e.g. a mid-rebase sibling) degrades to a ``drift`` WARNING to review,
    never a raise. The checks honest-skip an ABSENT sibling themselves; this guards the present-but-broken
    case the corpus read does not. A SPECIFIC catch (not a blanket one), so a real programming bug still
    surfaces."""
    try:
        return TripwireResult(name, check())
    except (OSError, json.JSONDecodeError) as exc:
        return TripwireResult(
            name,
            DriftReport(
                status="drift",
                warnings=[
                    f"{name}: live source present but unreadable/malformed — {exc} (review; never a silent pass)"
                ],
            ),
        )


def build_report(*, substrate_root: str | None = None, live_corpus_root: str | None = None) -> list[TripwireResult]:
    """Run every drift tripwire and collect its report — one entry per tripwire, in a stable order.

    Reuses the existing checks (no third copy): the copied-constant reconciliation against the live
    substrate detector source, and the vendored-corpus reconciliation against the live sibling corpus.
    Optional roots override each check's sibling resolution (for tests / explicit invocations); ``None``
    uses the check's own env-or-sibling default. NEVER raises — an absent sibling honest-skips, and a
    present-but-malformed source degrades to a ``drift`` warning via :func:`_run_tripwire`."""
    return [
        _run_tripwire("detector-drift", lambda: check_detector_drift(substrate_root)),
        _run_tripwire("corpus-drift", lambda: check_corpus_drift(live_root=live_corpus_root)),
    ]


def format_report(results: list[TripwireResult]) -> str:
    """A human-readable advisory render: a header line per tripwire (``name: status``) followed by an
    indented line per warning (mirrors ``detector_reconciliation._format_report``)."""
    lines = ["reconciliation drift report (advisory — warn-never-fail):"]
    for result in results:
        lines.append(f"{result.name}: {result.report.status}")
        lines.extend(f"  - {warning}" for warning in result.report.warnings)
    return "\n".join(lines)


def exit_code(results: list[TripwireResult]) -> int:
    """Advisory exit: ``1`` if ANY tripwire reports ``drift`` (the loud signal), else ``0`` — both
    ``skipped`` (honest-skip) and ``in_sync`` are ``0``. The hosted lane runs the runner NON-REQUIRED,
    so this signal surfaces drift without ever blocking a build."""
    return 1 if any(result.report.status == "drift" for result in results) else 0


def main(argv: list[str]) -> int:
    """Build the consolidated report, print it (and append to ``$GITHUB_STEP_SUMMARY`` when set — the
    hosted lane), and return the advisory exit code."""
    argparse.ArgumentParser(
        prog="python -m aml_casework.reconcile",
        description=(
            "Advisory reconciliation lane: surface (never gate) drift of casework's copied screening "
            "logic / vendored corpus vs the live substrate sibling. Honest-skips when the sibling is absent."
        ),
    ).parse_args(argv)

    results = build_report()
    rendered = format_report(results)
    print(rendered)  # noqa: T201 — documented standalone runner

    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as fh:
            fh.write(rendered + "\n")

    return exit_code(results)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
