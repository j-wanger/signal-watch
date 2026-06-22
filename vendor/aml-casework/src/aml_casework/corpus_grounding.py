"""Corpus-grounding verifier (Class-G, deterministic) — the audit walk's LAST link.

The other verifiers prove a cited flag resolves to an IN-BUNDLE id; none of them opens the corpus. So
"this ``grounding.flag`` IS advisory ``fin-2026-alert001:IND-11``'s real text" was AUTHORED-real — a
human copied the text byte-faithfully and asserted it in a provenance note. This verifier makes it
ENFORCED-real: it reads the FROZEN, vendored signal-watch corpus as DATA and grounds each alert's
``grounding.flag`` (SUBSTRING under :func:`normalize`) against the real committed regulator indicator.
A paraphrased or drifted flag becomes a loud violation, not a silent pass.

Contract (signal-watch is FROZEN):
- **Read-only** on the corpus — this module opens ``derived/*.json`` for reading and never writes.
- **Pinned** — :data:`CORPUS_PIN` records the signal-watch HEAD the vendored snapshot matches;
  :func:`check_corpus_drift` surfaces when the live sibling moves off it.
- **No engine import** — the 3-line :func:`normalize` is a DELIBERATE mirror of signal-watch's
  ``derive_signals.normalize`` (and the ``news_ground.news_normalize`` precedent), copied not imported,
  so reading the corpus as data never drags in the authoring/engine layer.

Corpus root resolution: ``SIGNAL_WATCH_CORPUS`` env > the vendored pinned snapshot under
``fixtures/corpus/`` (default). The vendored copy is committed and present in CI, so the enforcement
path grounds by construction with no sibling checkout; the live sibling is the drift oracle only.

Returns ``list[str]`` violations (empty == every flag grounds to source), mirroring the other verifiers.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from typing import Any

# The signal-watch HEAD the vendored corpus snapshot (fixtures/corpus/) is pinned to. The two records
# are byte-identical at this ref; check_corpus_drift surfaces if the live sibling moves off it.
CORPUS_PIN = "a75a136"

_ROOT_ENV = "SIGNAL_WATCH_CORPUS"

# The vendored snapshot is the default enforcement root: committed, pinned, and present in CI — so the
# corpus-grounding gate fails the build by construction, no sibling checkout required.
_VENDORED_ROOT = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..", "fixtures", "corpus", "fincen-alerts", "derived")
)

# The conventional live sibling location (repos are siblings under the same parent), used only by the
# drift check — never the enforcement path. Resolved after the env var, which names the live corpus.
_SIBLING_LIVE_ROOT = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "signal-watch", "data", "fincen-alerts", "derived")
)


def normalize(text: str) -> str:
    """Collapse text to lowercase alphanumerics for position-free quote-grounding.

    A DELIBERATE 3-line mirror of signal-watch's ``derive_signals.normalize`` (and
    ``news_ground.news_normalize``): copied, NOT imported, so reading the corpus as data never pulls in
    the authoring/engine layer (the same shape ``news_ground`` uses for its build->corpus read). The
    grounding gate is ``normalize(flag) in normalize(corpus_flag)`` — exactly signal-watch's own gate.
    """
    collapsed = re.sub(r"[^a-z0-9]+", "", text.lower())
    return collapsed.replace("fincenadvisory", "")


def corpus_root(root: str | None = None) -> str:
    """Resolve the corpus root: explicit arg > ``SIGNAL_WATCH_CORPUS`` env > the vendored pinned snapshot.

    NOTE: setting ``SIGNAL_WATCH_CORPUS`` grounds enforcement against THAT corpus — deliberately OFF the
    vendored pin (a dev pointing at a live/alternate corpus). CI leaves it unset, so CI enforces against
    the pinned snapshot by construction. The drift check uses the same var as its live oracle."""
    return root or os.environ.get(_ROOT_ENV) or _VENDORED_ROOT


def load_indicator_flag(root: str, advisory_id: str, indicator_id: str) -> str | None:
    """The committed corpus indicator's verbatim ``flag``, read as DATA (``json.load``).

    Returns ``None`` when the advisory file is absent OR the indicator id is not in it — callers that
    must distinguish the two (see :func:`verify_corpus_grounding`) check file existence first. Never
    imports engine code; never writes the corpus."""
    path = os.path.join(root, f"{advisory_id}.json")
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as fh:
        record: dict[str, Any] = json.load(fh)
    for indicator in record.get("indicators", []):
        if indicator.get("id") == indicator_id:
            flag = indicator.get("flag")
            return flag if isinstance(flag, str) else None
    return None


def verify_corpus_grounding(bundle: dict[str, Any], root: str | None = None) -> list[str]:
    """Ground every alert's ``grounding.flag`` to its real corpus indicator (substring under normalize).

    Three distinct, fail-closed violation classes: the advisory file is not in the pinned corpus, the
    indicator id is absent from it, or the flag does not appear (under normalize) in the real indicator
    text. Alerts without a grounding block are skipped here — ``contract.validate_bundle`` owns the
    "grounding present and well-formed" check; this verifier owns only "grounds to SOURCE"."""
    resolved_root = corpus_root(root)
    violations: list[str] = []
    for i, alert in enumerate(bundle.get("alerts", [])):
        grounding = alert.get("grounding")
        if not grounding:
            continue
        where = f"alerts[{i}].grounding"
        advisory_id = grounding.get("advisory_id")
        indicator_id = grounding.get("indicator_id")
        flag = grounding.get("flag")
        if not (advisory_id and indicator_id and isinstance(flag, str)):
            continue  # the contract verifier flags missing/empty grounding fields; nothing to ground here
        path = os.path.join(resolved_root, f"{advisory_id}.json")
        if not os.path.isfile(path):
            violations.append(
                f"{where}: corpus advisory file '{advisory_id}.json' not found under the pinned corpus "
                f"(signal-watch@{CORPUS_PIN}); vendor it or correct the advisory_id"
            )
            continue
        corpus_flag = load_indicator_flag(resolved_root, advisory_id, indicator_id)
        if corpus_flag is None:
            violations.append(f"{where}: indicator '{indicator_id}' not found in corpus advisory '{advisory_id}'")
            continue
        normalized_flag = normalize(flag)
        if not normalized_flag:
            # The empty string is a substring of EVERYTHING — a punctuation/whitespace-only flag would
            # otherwise ground to every indicator (a silent pass of an ungroundable claim). The contract
            # verifier only rejects a falsy flag; "...!!!  " is truthy yet normalizes to "". Fail closed.
            violations.append(
                f"{where}: flag normalizes to empty (punctuation/whitespace only) — no groundable content"
            )
            continue
        if normalized_flag not in normalize(corpus_flag):
            violations.append(
                f"{where}: flag does not ground to corpus indicator '{advisory_id}:{indicator_id}' "
                f"(not a substring of the real indicator text under normalize — paraphrased or drifted)"
            )
    return violations


@dataclass(frozen=True)
class DriftReport:
    """The result of comparing the vendored pin against the live sibling corpus.

    ``status`` is ``in_sync`` (live matches the pin), ``drift`` (the live sibling moved off the pin), or
    ``skipped`` (no live sibling to check against — the CI reality). ``warnings`` is always populated
    for ``drift`` and ``skipped`` so the situation is OBSERVABLE; it is advisory, never a hard fail."""

    status: str
    warnings: list[str] = field(default_factory=list)


def _live_root(live_root: str | None = None) -> str:
    """Resolve the LIVE sibling corpus root: explicit arg > ``SIGNAL_WATCH_CORPUS`` env > the sibling
    checkout. (Distinct from :func:`corpus_root`, which defaults to the vendored pin for enforcement.)"""
    return live_root or os.environ.get(_ROOT_ENV) or _SIBLING_LIVE_ROOT


def _indicators_by_id(path: str) -> dict[str, str]:
    """{indicator_id: flag} for one derived record, read as DATA. Non-string ids/flags are skipped."""
    with open(path, encoding="utf-8") as fh:
        record: dict[str, Any] = json.load(fh)
    out: dict[str, str] = {}
    for indicator in record.get("indicators", []):
        ind_id = indicator.get("id")
        flag = indicator.get("flag")
        if isinstance(ind_id, str) and isinstance(flag, str):
            out[ind_id] = flag
    return out


def check_corpus_drift(vendored_root: str | None = None, live_root: str | None = None) -> DriftReport:
    """Surface (never fail) when the live sibling corpus has moved off the vendored pin.

    Compares each vendored indicator flag byte-for-byte against the live sibling so that ANY upstream
    re-baseline (even one that still grounds under normalize) is visible — silent drift would change
    what the verifier enforces against without anyone choosing to. An upstream re-baseline is a HUMAN
    signal (review + re-pin), not a build break, so this returns warnings, not violations. When the
    live sibling is absent (CI / no sibling checkout), it skips HONESTLY — the vendored snapshot stays
    the pinned oracle. Read-only: it opens both corpora for reading only."""
    vendored = vendored_root or _VENDORED_ROOT
    live = _live_root(live_root)
    if not os.path.isdir(live):
        return DriftReport(
            status="skipped",
            warnings=[
                f"drift-check skipped: live corpus root '{live}' is absent (CI / no sibling checkout); "
                f"the vendored snapshot (signal-watch@{CORPUS_PIN}) remains the pinned oracle"
            ],
        )
    warnings: list[str] = []
    for fname in sorted(os.listdir(vendored)):
        if not fname.endswith(".json"):
            continue
        advisory_id = fname[:-5]
        live_path = os.path.join(live, fname)
        if not os.path.isfile(live_path):
            warnings.append(
                f"drift: vendored advisory '{advisory_id}' has no counterpart in the live corpus "
                f"'{live}' (upstream removed or relocated it)"
            )
            continue
        vend_indicators = _indicators_by_id(os.path.join(vendored, fname))
        live_indicators = _indicators_by_id(live_path)
        for ind_id, vend_flag in vend_indicators.items():
            live_flag = live_indicators.get(ind_id)
            if live_flag is None:
                warnings.append(
                    f"drift: indicator '{advisory_id}:{ind_id}' is in the vendored pin but gone from the "
                    f"live corpus (upstream re-baselined; review and re-pin)"
                )
            elif vend_flag != live_flag:
                warnings.append(
                    f"drift: indicator '{advisory_id}:{ind_id}' flag differs between the vendored pin "
                    f"(signal-watch@{CORPUS_PIN}) and the live corpus (upstream re-baselined; review and re-pin)"
                )
    return DriftReport(status="drift" if warnings else "in_sync", warnings=warnings)
