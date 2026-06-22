"""Citation verifier (Class-G, deterministic).

Every narrative claim must resolve to evidence. Per assumption A4 the narrative is a structured set of
cited claims (``narrative_claims: [{text, cites:[signal_id|txn_id]}]``), so "every statement resolves
to an evidence item" is a deterministic resolution check, not an NLP problem. Fail-closed: a dangling
cite, an uncited claim, or a narrative that grounds no suspicion is a violation.

Returns ``list[str]`` violations (empty == every claim is grounded), mirroring the other verifiers.
"""

from __future__ import annotations

from typing import Any

from aml_casework.completeness import narrative_satisfied
from aml_casework.contract import DEFAULT_STANCE


def _signal_ids(bundle: dict[str, Any]) -> set[str]:
    """Grounded signal_ids — citing one connects an indicator to the suspicion (typology grounds)."""
    return {a.get("grounding", {}).get("signal_id") for a in bundle.get("alerts", []) if a.get("grounding")}


def _evidence_ids(bundle: dict[str, Any]) -> set[str]:
    """The id-spaces a claim may cite: grounded signal_ids and transaction txn_ids."""
    txn_ids = {t.get("txn_id") for t in bundle.get("transactions", [])}
    return {x for x in (_signal_ids(bundle) | txn_ids) if x is not None}


def _exculpatory_evidence_ids(bundle: dict[str, Any]) -> set[str]:
    """txn_ids of transactions explicitly marked ``exculpatory: true`` — documented data rows that
    argue AGAINST suspicion. The narrative must retain each one (conflict-both-kept)."""
    return {
        t.get("txn_id")
        for t in bundle.get("transactions", [])
        if t.get("exculpatory") is True and t.get("txn_id") is not None
    }


def grounded_stances(bundle: dict[str, Any]) -> set[str]:
    """The stances actually GROUNDED in the right kind of evidence — not merely labeled. A stance only
    counts when an actual claim of that stance cites the matching evidence:

    - ``inculpatory`` iff an inculpatory-stance claim cites a typology signal_id (the suspicion is
      connected to an indicator), and
    - ``exculpatory`` iff an exculpatory-stance claim cites an ``exculpatory: true`` transaction (real
      retained counter-evidence).

    A bare ``exculpatory`` label hung on the inculpatory side's own evidence does NOT count. Sign-off
    uses this to validate a human-assigned ``file`` / ``both_defensible`` against the evidence — never
    weighing which side wins, only that each claimed stance is evidence-backed."""
    signals = _signal_ids(bundle)
    exculpatory = _exculpatory_evidence_ids(bundle)
    grounded: set[str] = set()
    for claim in bundle.get("str_record", {}).get("narrative_claims", []):
        stance = claim.get("stance", DEFAULT_STANCE)
        cites = claim.get("cites", [])
        if stance == "inculpatory" and any(c in signals for c in cites):
            grounded.add("inculpatory")
        elif stance == "exculpatory" and any(c in exculpatory for c in cites):
            grounded.add("exculpatory")
    return grounded


def verify_citations(bundle: dict[str, Any]) -> list[str]:
    """Flag dangling cites, uncited claims, and a complete narrative that grounds no suspicion.

    An OPEN seam (no narrative) has nothing to ground -> no violation; the grounds-for-suspicion check
    fires only once the seam is filled (``completeness.narrative_satisfied``)."""
    resolvable = _evidence_ids(bundle)
    claims = bundle.get("str_record", {}).get("narrative_claims", [])
    violations: list[str] = []
    for j, claim in enumerate(claims):
        cw = f"narrative_claims[{j}]"
        cites = claim.get("cites", [])
        if not cites:
            violations.append(f"{cw}: claim has no citation; every statement must resolve to evidence")
            continue
        for cite in cites:
            if cite not in resolvable:
                violations.append(f"{cw}: cite '{cite}' resolves to no signal or transaction (dangling)")
    # Indicator -> suspicion connection: a complete narrative needs >=1 claim citing a typology signal.
    if narrative_satisfied(bundle):
        signal_ids = _signal_ids(bundle)
        if not any(cite in signal_ids for claim in claims for cite in claim.get("cites", [])):
            violations.append(
                "narrative_claims: the narrative is marked complete but no claim grounds the suspicion "
                "(no claim cites a typology signal)"
            )
        # conflict-both-kept: exculpatory bundle evidence must be RETAINED — an exculpatory-stance claim
        # must cite each piece. The system retains both sides; it never adjudicates which one wins.
        retained = {cite for claim in claims if claim.get("stance") == "exculpatory" for cite in claim.get("cites", [])}
        for ev_id in sorted(_exculpatory_evidence_ids(bundle) - retained):
            violations.append(
                f"conflict-both-kept: exculpatory evidence '{ev_id}' is present in the bundle but no "
                f"exculpatory-stance claim cites it (the narrative must retain both sides)"
            )
    return violations
