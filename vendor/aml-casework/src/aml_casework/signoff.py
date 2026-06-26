"""Class-A sign-off seam (the named-human act surface, NOT automation).

``record_signoff`` runs every Class-G verifier (contract, grounding-replay, completeness, citation,
corpus-grounding, narrative-grounding) plus the positive completeness check, and classifies the DISPOSITION the evidence
supports:

- ``blocked`` — any verifier violation (the record carries a defensibility failure);
- ``needs_more_info`` — clean (no violations) but incomplete (a clean data gap, distinct from blocked);
- ``signed`` — clean AND complete; signable.

The system computes only this much. It NEVER weighs suspicion strength — the file/no-file (and
``both_defensible``) judgement stays human, validated against the evidence in a later step (A1/A3).
The returned record snapshots every verifier result so the named signer is the best-informed person
in the room — but the system never approves on their behalf (assumption A6). The signer identity and
timestamp are passed in (the human supplies them).
"""

from __future__ import annotations

from typing import Any

from aml_casework.citation import grounded_stances, verify_citations
from aml_casework.completeness import unsatisfied_elements, verify_completeness
from aml_casework.contract import validate_bundle
from aml_casework.corpus_grounding import verify_corpus_grounding
from aml_casework.grounding_replay import replay_bundle
from aml_casework.narrative_grounding import verify_narrative_grounding

# The disposition the SYSTEM can compute from the deterministic chain alone. A clean-but-incomplete
# record (a data gap) is needs_more_info, NOT blocked — keeping the two distinct is the Phase-2
# distinction (A1): a verifier violation is a defensibility failure, a gap is just missing evidence.
SYSTEM_DISPOSITIONS = ("blocked", "needs_more_info", "signed")

# Dispositions a HUMAN assigns over a signable record. The system never weighs suspicion strength
# (RGS is human); it only validates the assignment is consistent with the grounded evidence (A3):
# `file` needs a grounded inculpatory suspicion; `both_defensible` needs a grounded claim on BOTH
# stances; `cleared` (Phase 18 — an affirmative documented dismissal) is the MIRROR of `file`: a
# grounded exculpatory mitigation AND no grounded inculpatory predicate. It NEVER judges which side
# wins, and it NEVER auto-clears — `cleared` is only ever a validated human claim (system-computing it
# would move a signable exculpatory-only record's verdict signed->cleared, breaking back-compat).
HUMAN_DISPOSITIONS = ("file", "both_defensible", "cleared")


def _validate_claimed_disposition(bundle: dict[str, Any], claimed: str) -> list[str]:
    """Return reasons the human-assigned disposition is NOT consistent with the grounded evidence
    (empty == validated). Uses :func:`grounded_stances` — a stance counts only when an actual claim of
    that stance cites the matching evidence (a bare label does not). Never judges the conflict — only
    checks the required stances are evidence-backed."""
    if claimed not in HUMAN_DISPOSITIONS:
        return [f"unknown claimed disposition '{claimed}' (allowed: {HUMAN_DISPOSITIONS})"]
    stances = grounded_stances(bundle)
    if claimed == "file":
        if "inculpatory" not in stances:
            return ["file requires a grounded inculpatory suspicion, but no inculpatory claim cites a typology signal"]
        return []
    if claimed == "cleared":
        # The MIRROR of file (the affirmative documented dismissal): a grounded exculpatory mitigation
        # (a benign explanation backed by retained counter-evidence) AND no grounded inculpatory
        # predicate (a grounded inculpatory suspicion is file / both_defensible, not a clear).
        if "exculpatory" not in stances:
            return [
                "cleared requires a grounded exculpatory mitigation, but no exculpatory claim cites "
                "retained counter-evidence"
            ]
        if "inculpatory" in stances:
            return [
                "cleared requires NO grounded inculpatory predicate (a grounded inculpatory suspicion is "
                "file or both_defensible, not a clear)"
            ]
        return []
    # both_defensible: an evidence-backed claim on BOTH stances (genuine ambiguity, not adjudicated)
    absent = [stance for stance in ("inculpatory", "exculpatory") if stance not in stances]
    if absent:
        return [f"both_defensible requires an evidence-backed claim on BOTH stances; missing grounded: {absent}"]
    return []


def run_verifiers(bundle: dict[str, Any]) -> dict[str, list[str]]:
    """Run every Class-G verifier over a bundle, in chain order, returning the per-verifier violation
    snapshot. ONE definition of 'the gate': record_signoff reports it, and the narrative generator's
    regenerate loop self-checks a candidate draft against it (the deterministic chain is the judge)."""
    return {
        "contract": validate_bundle(bundle),
        "grounding_replay": replay_bundle(bundle),
        "completeness": verify_completeness(bundle),
        "citation": verify_citations(bundle),
        "corpus_grounding": verify_corpus_grounding(bundle),
        "narrative_grounding": verify_narrative_grounding(bundle),
    }


def flatten_violations(results: dict[str, list[str]]) -> list[str]:
    """Flatten a per-verifier snapshot into ``"<verifier>: <violation>"`` lines — the violation-string
    format shared by record_signoff's blocking_violations and the generator's regenerate feedback."""
    return [f"{name}: {violation}" for name, violations in results.items() for violation in violations]


def record_signoff(
    bundle: dict[str, Any], signer: str, ts: str, claimed_disposition: str | None = None
) -> dict[str, Any]:
    """Assemble the verified state for a named human to sign and classify its disposition.

    The SYSTEM computes ``blocked``/``needs_more_info``/``signed`` from the four verifiers + is_complete.
    When the human supplies a ``claimed_disposition`` (``file``/``both_defensible``/``cleared``), the
    system VALIDATES it against the grounded evidence — only over a signable record, and only that the
    required stances are present; it never judges which side wins. A validated claim becomes the
    ``disposition``; an unvalidated one is refused (disposition unchanged) with a ``disposition_reasons``
    entry. ``signed`` stays the back-compat boolean for the system being signable.

    Returns the per-verifier snapshot plus ``blocking_violations`` (verifier failures -> blocked) and
    ``missing`` reasons (incompleteness -> needs_more_info) in SEPARATE buckets so a data gap is never
    conflated with a violation."""
    verifier_results = run_verifiers(bundle)
    blocking = flatten_violations(verifier_results)
    gaps = unsatisfied_elements(bundle)
    missing: list[str] = []
    if gaps:
        missing.append(f"STR record is incomplete; unsatisfied required element(s): {gaps}")

    if blocking:
        system_disposition = "blocked"
    elif missing:
        system_disposition = "needs_more_info"
    else:
        system_disposition = "signed"

    disposition = system_disposition
    disposition_reasons: list[str] = []
    if claimed_disposition is not None:
        if system_disposition != "signed":
            disposition_reasons.append(
                f"claimed disposition '{claimed_disposition}' cannot be honored: record is "
                f"'{system_disposition}', not signable"
            )
        else:
            disposition_reasons = _validate_claimed_disposition(bundle, claimed_disposition)
            if not disposition_reasons:
                disposition = claimed_disposition

    return {
        "disposition": disposition,
        "claimed_disposition": claimed_disposition,
        "signed": system_disposition == "signed",
        "signer": signer,
        "ts": ts,
        "verifier_results": verifier_results,
        "blocking_violations": blocking,
        "missing": missing,
        "disposition_reasons": disposition_reasons,
    }
