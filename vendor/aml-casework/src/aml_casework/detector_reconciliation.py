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

Scope = the screening copies with a NAMED substrate-symbol provenance: the C7 peer-anomaly floor
(``business_activity.MIN_INFLOW_CENTS``) and the C8 income-mismatch floor + monthly multiple
(``income_mismatch.MIN_INFLOW_CENTS`` / ``MISMATCH_MONTHLY_MULTIPLE``). The casework-side value is IMPORTED
from :mod:`grounding_replay` (never re-hardcoded here) so the check reconciles the LIVE copy — there is no
third copy to drift. The C14 ``_kyc_defect`` PREDICATE is branch LOGIC, not a constant; a source-literal diff
cannot capture it, so it is reconciled BEHAVIORALLY (run substrate's real predicate over a synthetic party
battery) in ``tests/test_c14_behavioral_reconciliation.py``. The replay assertions (C2-C5, C15) were Phase-6
reconciled-to-SEMANTICS, not copied from a single substrate constant, so they have no literal to diff and are
OUT of scope (a named boundary, not a silent omission).

Substrate root resolution: ``AML_SUBSTRATE_ROOT`` env > the conventional sibling checkout (``../aml-substrate``).
"""

from __future__ import annotations

import ast
import os
from dataclasses import dataclass

from aml_casework.corpus_grounding import DriftReport
from aml_casework.grounding_replay import (
    _MISMATCH_MIN_INFLOW_CENTS,
    _MISMATCH_MONTHLY_MULTIPLE,
    _PEER_ANOMALY_MIN_INFLOW_CENTS,
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
    """One integer literal casework COPIED from a named substrate detector symbol. ``casework_value`` is the
    LIVE casework copy (imported from :mod:`grounding_replay`), reconciled against the live substrate source."""

    capability: str  # the screening capability the copy grounds (C7 / C8)
    detector_file: str  # the substrate detector source filename
    symbol: str  # the module-level symbol name in that file
    casework_value: int  # the value casework copied (the reconciliation target — the live copy)
    casework_site: str  # where casework holds the copy (named in the warning)


# The copied screening constants with a NAMED substrate-symbol provenance (Phase 10/11). The C7 floor and the
# C8 floor are INDEPENDENT copies of two distinct substrate symbols that numerically coincide ($25k) — both
# are reconciled. (C14's predicate is branch logic, reconciled behaviorally — see the module docstring.)
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
)


def substrate_root(root: str | None = None) -> str:
    """Resolve the substrate root: explicit arg > ``AML_SUBSTRATE_ROOT`` env > the conventional sibling checkout."""
    return root or os.environ.get(_ROOT_ENV) or _SIBLING_SUBSTRATE_ROOT


def _module_int_literals(path: str) -> dict[str, int] | None:
    """Every module-level ``NAME = <int literal>`` (plain or annotated) in a Python source file, read by AST
    (no import, no exec).

    Read-only and import-free: parses the substrate source as DATA, so reconciling a constant never drags in
    the substrate engine. Only plain int literals are captured (``bool`` is excluded — it is an ``int``
    subclass); a COMPUTED constant is absent from the map, so a caller's ``.get`` fails closed to a warning.
    Returns ``None`` when the source cannot be read/parsed (a malformed / mid-refactor checkout) — the caller
    emits a warning and NEVER raises (the warn-never-fail contract; a broken sibling must not crash the
    tripwire)."""
    try:
        with open(path, encoding="utf-8") as fh:
            tree = ast.parse(fh.read(), filename=path)
    except (OSError, SyntaxError):
        return None
    out: dict[str, int] = {}
    for node in tree.body:
        # plain `NAME = <int>` (possibly chained targets) or annotated `NAME: int = <int>`
        if isinstance(node, ast.Assign):
            targets = [t for t in node.targets if isinstance(t, ast.Name)]
            value: ast.expr | None = node.value
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            targets = [node.target]
            value = node.value  # None for a bare annotation (`NAME: int`) — skipped below
        else:
            continue
        if not (isinstance(value, ast.Constant) and isinstance(value.value, int) and not isinstance(value.value, bool)):
            continue
        for target in targets:
            out[target.id] = value.value
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
    literals_by_file: dict[str, dict[str, int] | None] = {}
    for c in _COPIED_CONSTANTS:
        path = os.path.join(detectors_dir, c.detector_file)
        if not os.path.isfile(path):
            warnings.append(
                f"drift: substrate detector source '{c.detector_file}' is absent — casework's "
                f"{c.casework_site} (copied from {c.symbol}) can no longer be reconciled (review)"
            )
            continue
        if path not in literals_by_file:
            literals_by_file[path] = _module_int_literals(path)
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
