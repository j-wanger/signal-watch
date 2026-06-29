"""Detector-drift reconciliation (sibling-gated, warn-never-fail) — surface copied-formula drift LOUDLY.

casework grounds substrate screening capabilities by RE-DERIVING the detector's screened condition over the
cited evidence — COPIED from the substrate detector WITH PROVENANCE, never imported (the no-sibling-import
doctrine). A copy DRIFTS when the substrate detector changes (C4/C15 in Phase 6, C14 in Phase 14 — twice). A
synthetic fixture where casework authors BOTH the emission and its grounding cannot expose drift; only
reconciliation against the live source can.

This module is the tripwire. It is NOT a per-bundle verifier (the 6-verifier chain + ``record_signoff`` are
byte-unchanged) — it is a standalone, sibling-gated check, mirroring ``corpus_grounding.check_corpus_drift``:

- **Read-only / no import** — it parses the substrate detector SOURCE as data (``ast``), so reconciling a
  copied constant never drags in the substrate engine layer (the no-sibling-import doctrine).
- **Warn, never fail** — a substrate re-key is a HUMAN signal (review + re-pin the copy), not a build break;
  this returns warnings, never raises.
- **Honest-skip** — when the substrate sibling is absent (CI / no checkout), it skips; casework's copies stay
  the pinned oracle.

Scope = every casework copy with a NAMED substrate-symbol provenance and a literal to diff. The screening
floors (Phase 10/11): the C7 peer-anomaly floor (``business_activity.MIN_INFLOW_CENTS``) and the C8
income-mismatch floor + monthly multiple (``income_mismatch.MIN_INFLOW_CENTS`` / ``MISMATCH_MONTHLY_MULTIPLE``).
The replay constants (Phase 20): the C15 shell throughput leg (``shell.RETENTION_TOLERANCE`` float /
``MIN_THROUGHPUT_CENTS`` / ``MIN_COUNTERPARTIES``) and the C4 structuring band leg (``structuring.BAND_LOW_CENTS``
/ ``BAND_HIGH_CENTS`` / ``MIN_DEPOSITS`` / ``AGGREGATE_THRESHOLD_CENTS`` / ``WINDOW`` timedelta) — these are
re-derivations of substrate detectors over copied literals, so they DO diff (Phase 21 widened the extractor to
read float + timedelta). The casework-side value is IMPORTED from :mod:`grounding_replay` (never re-hardcoded
here) so the check reconciles the LIVE copy — there is no third copy to drift. The C14 ``_kyc_defect`` PREDICATE
is branch LOGIC, not a constant; a source-literal diff cannot capture it, so it is reconciled BEHAVIORALLY (run
substrate's real predicate over a synthetic party battery) in ``tests/test_c14_behavioral_reconciliation.py``.
Still OUT of scope (a named boundary, not a silent omission): C2/C3/C5, the C15 generic-trading name-match leg,
and the C4 cash-only leg — Phase-6 reconciled-to-SEMANTICS, with no single substrate constant to diff.

Substrate root resolution: ``AML_SUBSTRATE_ROOT`` env > the conventional sibling checkout (``../aml-substrate``).
"""

from __future__ import annotations

import ast
import os
from dataclasses import dataclass

from aml_casework.corpus_grounding import DriftReport
from aml_casework.grounding_replay import (
    _CTR_THRESHOLD_CENTS,
    _MIN_SHELL_COUNTERPARTIES,
    _MIN_SHELL_THROUGHPUT_CENTS,
    _MIN_STRUCTURING_COUNT,
    _MISMATCH_MIN_INFLOW_CENTS,
    _MISMATCH_MONTHLY_MULTIPLE,
    _PEER_ANOMALY_MIN_INFLOW_CENTS,
    _SHELL_RETENTION_TOLERANCE,
    _STRUCTURING_24H_WINDOW,
    _STRUCTURING_BAND_HIGH_CENTS,
    _STRUCTURING_BAND_LOW_CENTS,
)

# The substrate ref casework's screening constants were copied from (Phase 11/14, copied-with-provenance).
# The live sibling may sit at a later ref; this check surfaces when its source has moved off these values.
SUBSTRATE_PIN = "01ddeaf"

_ROOT_ENV = "AML_SUBSTRATE_ROOT"

# The conventional sibling checkout (repos are siblings under the same parent). Resolved after the env var.
_SIBLING_SUBSTRATE_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "aml-substrate"))

# The substrate detectors package, relative to the substrate root.
_DETECTOR_SUBDIR = os.path.join("src", "aml_substrate", "monitor", "detectors")


@dataclass(frozen=True)
class _CopiedConstant:
    """One literal casework COPIED from a named substrate detector symbol. ``casework_value`` is the LIVE
    casework copy (imported from :mod:`grounding_replay`), reconciled against the live substrate source. A
    value is an ``int``/``float``, or — for a ``timedelta`` copy (structuring.py ``WINDOW``) — its total-seconds
    ``float`` (so a substrate unit-rewrite of the same duration is in_sync, not a false drift)."""

    capability: str  # the capability the copy grounds (C7 / C8 screening; C15 / C4 replay)
    detector_file: str  # the substrate detector source filename
    symbol: str  # the module-level symbol name in that file
    casework_value: int | float  # the value casework copied (the reconciliation target — the live copy)
    casework_site: str  # where casework holds the copy (named in the warning)


# The copied constants with a NAMED substrate-symbol provenance. The C7/C8 screening floors (Phase 10/11) are
# INDEPENDENT copies of two distinct substrate symbols that numerically coincide ($25k) — both reconciled. The
# C15/C4 replay constants (Phase 20) extend the table to the shell.py / structuring.py copies: a float
# (RETENTION_TOLERANCE) and a timedelta (WINDOW) join here once the extractor reads them (Phase 21). The 8th —
# AGGREGATE_THRESHOLD_CENTS vs casework's regulatory _CTR_THRESHOLD_CENTS — is reconciled despite being framed
# regulatory (the C7/C8 coincident-symbol precedent: reconcile every substrate symbol the grounding depends on).
# (C14's predicate is branch logic, reconciled behaviorally — see the module docstring.)
_COPIED_CONSTANTS: tuple[_CopiedConstant, ...] = (
    _CopiedConstant(
        "C7",
        "business_activity.py",
        "MIN_INFLOW_CENTS",
        _PEER_ANOMALY_MIN_INFLOW_CENTS,
        "grounding_replay._PEER_ANOMALY_MIN_INFLOW_CENTS",
    ),
    _CopiedConstant(
        "C8",
        "income_mismatch.py",
        "MIN_INFLOW_CENTS",
        _MISMATCH_MIN_INFLOW_CENTS,
        "grounding_replay._MISMATCH_MIN_INFLOW_CENTS",
    ),
    _CopiedConstant(
        "C8",
        "income_mismatch.py",
        "MISMATCH_MONTHLY_MULTIPLE",
        _MISMATCH_MONTHLY_MULTIPLE,
        "grounding_replay._MISMATCH_MONTHLY_MULTIPLE",
    ),
    # C15 — substrate shell.py ShellDetector (Phase 20): a float tolerance + two int floors.
    _CopiedConstant(
        "C15",
        "shell.py",
        "RETENTION_TOLERANCE",
        _SHELL_RETENTION_TOLERANCE,
        "grounding_replay._SHELL_RETENTION_TOLERANCE",
    ),
    _CopiedConstant(
        "C15",
        "shell.py",
        "MIN_THROUGHPUT_CENTS",
        _MIN_SHELL_THROUGHPUT_CENTS,
        "grounding_replay._MIN_SHELL_THROUGHPUT_CENTS",
    ),
    _CopiedConstant(
        "C15",
        "shell.py",
        "MIN_COUNTERPARTIES",
        _MIN_SHELL_COUNTERPARTIES,
        "grounding_replay._MIN_SHELL_COUNTERPARTIES",
    ),
    # C4 — substrate structuring.py StructuringDetector (Phase 20): the band + count + aggregate + 24h WINDOW.
    _CopiedConstant(
        "C4",
        "structuring.py",
        "BAND_LOW_CENTS",
        _STRUCTURING_BAND_LOW_CENTS,
        "grounding_replay._STRUCTURING_BAND_LOW_CENTS",
    ),
    _CopiedConstant(
        "C4",
        "structuring.py",
        "BAND_HIGH_CENTS",
        _STRUCTURING_BAND_HIGH_CENTS,
        "grounding_replay._STRUCTURING_BAND_HIGH_CENTS",
    ),
    _CopiedConstant(
        "C4",
        "structuring.py",
        "MIN_DEPOSITS",
        _MIN_STRUCTURING_COUNT,
        "grounding_replay._MIN_STRUCTURING_COUNT",
    ),
    _CopiedConstant(
        "C4",
        "structuring.py",
        "AGGREGATE_THRESHOLD_CENTS",
        _CTR_THRESHOLD_CENTS,
        "grounding_replay._CTR_THRESHOLD_CENTS",
    ),
    _CopiedConstant(
        "C4",
        "structuring.py",
        "WINDOW",
        _STRUCTURING_24H_WINDOW.total_seconds(),  # the timedelta copy, normalized to total-seconds
        "grounding_replay._STRUCTURING_24H_WINDOW",
    ),
)


def substrate_root(root: str | None = None) -> str:
    """Resolve the substrate root: explicit arg > ``AML_SUBSTRATE_ROOT`` env > the conventional sibling checkout."""
    return root or os.environ.get(_ROOT_ENV) or _SIBLING_SUBSTRATE_ROOT


# ``datetime.timedelta`` unit -> seconds, mirroring the constructor signature. Phase 20 copied a ``timedelta``
# constant (structuring.py ``WINDOW``); reconciling it as a total-seconds SCALAR (not a reconstructed object)
# means a substrate unit-rewrite of the SAME duration (``hours=24`` -> ``days=1``) is in_sync, not a false drift.
_TIMEDELTA_UNIT_SECONDS: dict[str, float] = {
    "days": 86_400.0,
    "seconds": 1.0,
    "microseconds": 0.000_001,
    "milliseconds": 0.001,
    "minutes": 60.0,
    "hours": 3_600.0,
    "weeks": 604_800.0,
}
# The positional order of the ``timedelta(...)`` constructor (days, seconds, microseconds, ...).
_TIMEDELTA_POSITIONAL: tuple[str, ...] = (
    "days",
    "seconds",
    "microseconds",
    "milliseconds",
    "minutes",
    "hours",
    "weeks",
)


def _numeric_constant(node: ast.expr | None) -> int | float | None:
    """The value of an ``int``/``float`` literal node (``bool`` excluded — an ``int`` subclass), else ``None``."""
    if isinstance(node, ast.Constant) and isinstance(node.value, int | float) and not isinstance(node.value, bool):
        return node.value
    return None


def _timedelta_seconds(call: ast.Call) -> float | None:
    """Total seconds of a ``timedelta(...)`` / ``<alias>.timedelta(...)`` call built from CONSTANT numeric args,
    or ``None`` when the node is not a statically-readable timedelta literal (a non-timedelta call, a computed
    arg, ``**kwargs``, or an unknown unit). ``None`` is the honest "cannot reconcile this copy" signal — the
    caller fail-louds, never guesses, never raises."""
    func = call.func
    is_timedelta = (isinstance(func, ast.Name) and func.id == "timedelta") or (
        isinstance(func, ast.Attribute) and func.attr == "timedelta"
    )
    if not is_timedelta:
        return None
    if len(call.args) > len(_TIMEDELTA_POSITIONAL):  # more positionals than the signature — not a readable literal
        return None
    total = 0.0
    for unit, arg in zip(_TIMEDELTA_POSITIONAL, call.args, strict=False):  # fewer positionals than 7 is valid
        value = _numeric_constant(arg)
        if value is None:
            return None
        total += value * _TIMEDELTA_UNIT_SECONDS[unit]
    for kw in call.keywords:
        if kw.arg is None or kw.arg not in _TIMEDELTA_UNIT_SECONDS:  # **kwargs or an unknown unit
            return None
        value = _numeric_constant(kw.value)
        if value is None:
            return None
        total += value * _TIMEDELTA_UNIT_SECONDS[kw.arg]
    return total


def _module_literals(path: str) -> dict[str, int | float] | None:
    """Every module-level ``NAME = <literal>`` (plain or annotated) in a Python source file, read by AST (no
    import, no exec). A literal is an ``int`` or ``float`` constant, or a ``timedelta(...)`` call of constant
    numeric args (normalized to total-seconds, ``float``).

    Read-only and import-free: parses the substrate source as DATA, so reconciling a constant never drags in
    the substrate engine. ``bool`` is excluded (an ``int`` subclass); a COMPUTED constant — or a timedelta the
    extractor cannot statically read — is ABSENT from the map, so a caller's ``.get`` fails closed to a warning
    (never a guess). Returns ``None`` when the source cannot be read/parsed (a malformed / mid-refactor
    checkout) — the caller emits a warning and NEVER raises (the warn-never-fail contract; a broken sibling
    must not crash the tripwire)."""
    try:
        with open(path, encoding="utf-8") as fh:
            tree = ast.parse(fh.read(), filename=path)
    except (OSError, SyntaxError):
        return None
    out: dict[str, int | float] = {}
    for node in tree.body:
        # plain `NAME = <literal>` (possibly chained targets) or annotated `NAME: T = <literal>`
        if isinstance(node, ast.Assign):
            targets = [t for t in node.targets if isinstance(t, ast.Name)]
            value: ast.expr | None = node.value
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            targets = [node.target]
            value = node.value  # None for a bare annotation (`NAME: int`) — skipped below
        else:
            continue
        literal = _numeric_constant(value)
        if literal is None and isinstance(value, ast.Call):
            literal = _timedelta_seconds(value)
        if literal is None:
            continue
        for target in targets:
            out[target.id] = literal
    return out


def check_detector_drift(root: str | None = None) -> DriftReport:
    """Reconcile casework's COPIED screening constants against the live substrate detector source.

    Mirrors :func:`corpus_grounding.check_corpus_drift`: warn-never-fail, honest-skip when the sibling is
    absent. For each copied constant, read the live substrate source literal and compare to the value casework
    copied; a divergence is a WARNING naming the symbol + both values (substrate re-keyed -> review + re-pin
    the copy). A copied symbol that has VANISHED from the source (renamed / made non-literal) is also a warning
    (the copy can no longer be reconciled — fail loud, never a silent pass). Read-only; never imports substrate."""
    base = substrate_root(root)
    detectors_dir = os.path.join(base, _DETECTOR_SUBDIR)
    if not os.path.isdir(detectors_dir):
        return DriftReport(
            status="skipped",
            warnings=[
                f"detector-drift check skipped: substrate detectors dir '{detectors_dir}' is absent "
                f"(CI / no sibling checkout); casework's copies (provenance aml-substrate@{SUBSTRATE_PIN}) "
                f"remain the pinned oracle"
            ],
        )
    warnings: list[str] = []
    literals_by_file: dict[str, dict[str, int | float] | None] = {}
    for c in _COPIED_CONSTANTS:
        path = os.path.join(detectors_dir, c.detector_file)
        if not os.path.isfile(path):
            warnings.append(
                f"drift: substrate detector source '{c.detector_file}' is absent — casework's "
                f"{c.casework_site} (copied from {c.symbol}) can no longer be reconciled (review)"
            )
            continue
        if path not in literals_by_file:
            literals_by_file[path] = _module_literals(path)
        literals = literals_by_file[path]
        if literals is None:
            warnings.append(
                f"drift: substrate source '{c.detector_file}' could not be parsed (malformed / mid-refactor "
                f"checkout) — casework's {c.casework_site} cannot be reconciled (review); never a silent pass"
            )
            continue
        live = literals.get(c.symbol)
        if live is None:
            warnings.append(
                f"drift: substrate symbol '{c.symbol}' is gone from '{c.detector_file}' (renamed or made "
                f"non-literal) — casework's {c.casework_site}={c.casework_value} can no longer be reconciled (review)"
            )
        elif live != c.casework_value:
            warnings.append(
                f"drift: {c.capability} constant '{c.symbol}' in '{c.detector_file}' is {live} live but casework "
                f"copied {c.casework_value} ({c.casework_site}); substrate re-keyed — review and re-pin the copy"
            )
    return DriftReport(status="drift" if warnings else "in_sync", warnings=warnings)


def _format_report(report: DriftReport) -> str:
    """One-line-per-warning render for the dependency-free runner."""
    lines = [f"detector-drift: {report.status}"]
    lines.extend(f"  - {w}" for w in report.warnings)
    return "\n".join(lines)


if __name__ == "__main__":
    print(_format_report(check_detector_drift()))  # noqa: T201 — documented standalone runner
