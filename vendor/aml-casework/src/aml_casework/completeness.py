"""Completeness verifier (Class-G, deterministic).

The deterministic checklist vs the filing guidance's required elements (``STR_REQUIRED_ELEMENTS``).
Distinct from ``contract.validate_bundle`` (which checks the completeness KEYS are present): this
checks each element CLAIMED complete is actually SUBSTANTIATED by the bundle — the overclaim direction
(``completeness[el]=true`` with no grounding) is the defensibility failure a filing must not carry.

Grounding for the element definitions: real STR/SAR quality guidance names the recurring deficiencies
as missing/incomplete client-identification fields, failure to connect cited indicators to the
suspicion, and unsubstantiated transaction detail (aml-wiki: suspicious-activity-reporting,
canadian-str-reporting-quality). Each element below maps to a concrete bundle locus.

The narrative element (``grounds_for_suspicion_narrative``) is the Pillar-2 seam handled separately
(see ``verify_completeness`` once the narrative lands); here only the 5 deterministic elements.

Txn-less party-leaf invariant (Phase 12): a C14-style screening case cites NO transactions — its factual
basis is the recorded KYC state, reached by a resolving ``party_ref`` (reference-by-path). For such a
case ``transaction_details`` is substantiated by that party leaf, not by cited txns. This stays
fail-closed: no cited txns AND no resolving party leaf is unsubstantiated; whether the leaf actually
GROUNDS is grounding-replay's job (a distinct gate — completeness is not a grounding gate).

Returns ``list[str]`` violations (empty == every claimed element is substantiated).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from aml_casework.contract import STR_REQUIRED_ELEMENTS, party_ids

Predicate = Callable[[dict[str, Any]], bool]

NARRATIVE_ELEMENT = "grounds_for_suspicion_narrative"


def _has_reporting_entity(b: dict[str, Any]) -> bool:
    # Structural proxy: the bundle is attributable to a reporting entity (it carries the contract
    # stamp + the subject whose accounts the entity holds). The contract has no dedicated
    # reporting_entity field yet — tighten this when real Pillar-1 output supplies one. [soft spot]
    return bool(b.get("contract_version")) and bool(b.get("subject"))


def _has_resolving_party_leaf(b: dict[str, Any]) -> bool:
    """True iff some alert is a party-leaf alert whose ``party_ref`` resolves to a declared ``parties[]``
    row — the party-leaf analogue of a resolving txn cite (reference-by-path). A txn-less screening case
    (e.g. C14 KYC-integrity, ``txn_ids=()``) grounds its factual basis at a party, so this is what
    substantiates the detail element for it. Fail-closed by construction: a non-resolving ref is not a
    resolving leaf (the contract verifier independently flags the dangling ref). Resolves against the
    shared ``contract.party_ids`` accessor (one definition of a declared party set). The isinstance guard
    short-circuits before the membership test, so an unhashable ``party_ref`` fails closed (not a resolving
    leaf) instead of raising a TypeError on untrusted input."""
    declared = party_ids(b)
    return any(isinstance(a.get("party_ref"), str) and a.get("party_ref") in declared for a in b.get("alerts", []))


def _has_transaction_details(b: dict[str, Any]) -> bool:
    cited = b.get("str_record", {}).get("cited_txn_ids", [])
    txn_ids = {t.get("txn_id") for t in b.get("transactions", [])}
    if cited:
        return all(tid in txn_ids for tid in cited)
    # A txn-less party-leaf case (e.g. C14 KYC-integrity, txn_ids=()) cites no transactions: its factual
    # basis is the recorded KYC STATE, substantiated through a resolving party leaf, not transaction
    # detail. Satisfied iff such a leaf is present. Fail-closed: no cited txns AND no resolving party leaf
    # is unsubstantiated (whether the leaf actually GROUNDS is grounding_replay's job — a distinct gate).
    return _has_resolving_party_leaf(b)


def _has_account_information(b: dict[str, Any]) -> bool:
    accounts = set(b.get("subject", {}).get("account_ids", []))
    subject_accounts = b.get("str_record", {}).get("subject_account_ids", [])
    return bool(accounts) and all(a in accounts for a in subject_accounts)


def _has_subject_information(b: dict[str, Any]) -> bool:
    # The subject is identified by the OBSERVABLE ``customer_id`` — the no-PII identifier this synthetic,
    # "no real customer data, ever" program is built on (the substrate's whole design centres on
    # customer_id as the subject FK; it emits NO personal names by design). A personal ``name`` is
    # OPTIONAL: requiring one contradicted the program doctrine and rejected real emissions, which carry
    # customer_id + account_ids but no name. Reconciled in Phase 6 from the first real ingest (DISCOVERY:
    # the hand-authored fixtures invented PII names the real no-PII substrate never emits).
    return bool(b.get("subject", {}).get("customer_id"))


def _has_typology_grounds(b: dict[str, Any]) -> bool:
    cited = b.get("str_record", {}).get("cited_signal_ids", [])
    grounded = {a.get("grounding", {}).get("signal_id") for a in b.get("alerts", [])}
    return bool(cited) and all(sid in grounded for sid in cited)


_SUBSTANTIATION: dict[str, Predicate] = {
    "reporting_entity": _has_reporting_entity,
    "transaction_details": _has_transaction_details,
    "account_information": _has_account_information,
    "subject_information": _has_subject_information,
    "typology_grounds": _has_typology_grounds,
}

# The deterministic (non-narrative) required elements, in checklist order.
DETERMINISTIC_ELEMENTS = [e for e in STR_REQUIRED_ELEMENTS if e != NARRATIVE_ELEMENT]


def narrative_satisfied(bundle: dict[str, Any]) -> bool:
    """The narrative element is satisfied iff Pillar 2 wrote a narrative AND flipped its flag."""
    record = bundle.get("str_record", {})
    narrative = record.get("narrative")
    flag = record.get("completeness", {}).get(NARRATIVE_ELEMENT)
    return narrative not in (None, "") and flag is True


def unsatisfied_elements(bundle: dict[str, Any]) -> list[str]:
    """The required elements NOT actually satisfied: each deterministic element whose substantiation is
    absent, plus the narrative seam if unfilled. The positive 'what is still missing' view (distinct
    from verify_completeness's overclaim flags) — it is what turns a clean-but-incomplete record into
    needs_more_info and tells the human which evidence to collect. Empty == complete."""
    missing = [element for element, predicate in _SUBSTANTIATION.items() if not predicate(bundle)]
    if not narrative_satisfied(bundle):
        missing.append(NARRATIVE_ELEMENT)
    return missing


def is_complete(bundle: dict[str, Any]) -> bool:
    """Every required element is actually SATISFIED: the 5 deterministic ones substantiated AND the
    narrative seam filed. Distinct from verify_completeness (which flags overclaims) — an open seam has
    no overclaim violation yet is not complete, so a filing must check this before sign-off."""
    return not unsatisfied_elements(bundle)


def _narrative_seam_violations(bundle: dict[str, Any]) -> list[str]:
    """The seam invariant from the completeness angle: narrative present iff its flag is set. An open
    seam (both off) is consistent — not a violation; only a flag/narrative DISAGREEMENT is."""
    record = bundle.get("str_record", {})
    narrative = record.get("narrative")
    flag = record.get("completeness", {}).get(NARRATIVE_ELEMENT)
    present = narrative not in (None, "")
    if present and flag is not True:
        return [f"completeness['{NARRATIVE_ELEMENT}']: narrative present but flag!=true (Pillar 2 must flip it)"]
    if not present and flag is True:
        return [f"completeness['{NARRATIVE_ELEMENT}']=true but narrative is empty"]
    return []


def verify_completeness(bundle: dict[str, Any]) -> list[str]:
    """Flag every deterministic element claimed-but-unsubstantiated, plus narrative-seam disagreement.

    An open seam (narrative absent, flag false) is NOT a violation — it is the legitimate Pillar-2
    hand-off state; ``narrative_satisfied`` reports that element's status without erroring."""
    completeness = bundle.get("str_record", {}).get("completeness", {})
    violations: list[str] = []
    for element in DETERMINISTIC_ELEMENTS:
        if completeness.get(element) is True and not _SUBSTANTIATION[element](bundle):
            violations.append(f"completeness['{element}']=true but the bundle does not substantiate it")
    violations.extend(_narrative_seam_violations(bundle))
    return violations
