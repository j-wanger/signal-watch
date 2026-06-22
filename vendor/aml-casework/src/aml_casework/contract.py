"""Pillar 1 -> Pillar 2 evidence-bundle contract: schema + a deterministic validator.

This is the executable form of the cross-pillar integration contract
(signal-watch: docs/pillar-integration-contract.md, v0.1). It lets a SYNTHETIC
evidence bundle that follows the contract be validated structurally before any
chain code exists -- the bootstrap that unblocks Pillar 2 in parallel with
Pillar 1's persist step.

`validate_bundle` is the FIRST real verifier: referential integrity over the
reference-by-path grounding chain + the narrative-seam invariant. It checks
structure, NOT correctness (a grounding gate != a completeness gate != a
correctness gate -- the Phase-34 doctrine, carried forward).

Run dependency-free:  python3 src/aml_casework/contract.py <bundle.json>
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from typing import Any

# The STR completeness checklist Pillar 1 emits; the last element is the seam
# Pillar 2 flips when it writes the grounded narrative (mirrors
# aml_substrate.report.str_record.STR_REQUIRED_ELEMENTS at HEAD 0daa3cc).
STR_REQUIRED_ELEMENTS = [
    "reporting_entity",
    "transaction_details",
    "account_information",
    "subject_information",
    "typology_grounds",
    "grounds_for_suspicion_narrative",
]

# A narrative claim's stance toward suspicion. Absent == the default (inculpatory):
# Pillar 1 alerts are inculpatory by construction, so the marker is only carried
# when a claim argues the other way. exculpatory claims are how conflicting
# evidence is RETAINED (conflict-both-kept); the system never weighs which side wins.
DEFAULT_STANCE = "inculpatory"
CLAIM_STANCES = ("inculpatory", "exculpatory")

# Contract versions casework has validated its verifiers against. 0.1 is the original
# cross-pillar contract; 0.2 (aml-substrate Phase 17, evidence.py CONTRACT_VERSION) adds the
# optional, additive `parties` block. The set is enumerated deliberately: a bundle declaring an
# UNVALIDATED version is a violation, not a silent pass -- you cannot consume a contract bump you
# have not validated against (grounded-or-dropped applied to the contract itself).
KNOWN_CONTRACT_VERSIONS = ("0.1", "0.2")

# The 16-field PartyView allow-list the substrate projects into the v0.2 `parties` block (mirrors
# aml_substrate.monitor.detectors.views.PartyView, serialized via to_dict). The projection TYPE is the
# leak firewall: the substrate serializes ONLY these fields, never the raw Person/Organization (no
# label/PII). casework validates the SHAPE (every allow-list key is present) and TRUSTS the projection --
# it does not re-implement the firewall (it cannot leak what it never received). Validate-known-present,
# NOT reject-unknown: an extra field beyond the 16 is tolerated.
PARTY_VIEW_FIELDS = (
    "party_id",
    "is_person",
    "risk_rating",
    "cdd_level",
    "pep_tier",
    "sanctions_flag",
    "adverse_media_flag",
    "occupation",
    "source_of_funds",
    "source_of_wealth",
    "nationality",
    "residency_status",
    "naics_code",
    "nature_of_business",
    "expected_monthly_volume_cents",
    "expected_monthly_txn_count",
)

# --- Phase 13: closed vocabularies for the additive FINTRAC STR structured blocks ------------------
# Each is a CLOSED vocab a present block value must fall within (fail-closed on an unknown value). The
# blocks are OPTIONAL/additive (an absent block is valid); the str_record model is already STR-shaped, so
# these formalize the FINTRAC STR information sections without renaming any existing field.

# The PCMLTFA reporting-entity sectors a Canadian STR is filed by (FINTRAC sector enum, paraphrased).
REPORTING_ENTITY_TYPES = (
    "financial_entity",
    "msb",
    "securities_dealer",
    "life_insurance",
    "dpms",
    "casino",
    "real_estate",
)
# FINTRAC files both completed and attempted transactions; this is the TXN disposition (distinct from the
# human signer's FILING disposition, which simply MIRRORS signoff.disposition — see _validate_action_taken).
TXN_DISPOSITIONS = ("completed", "attempted")
# Account action the reporting entity recorded (the no-PII synthetic bundle records none -> honest NULL).
ACCOUNT_ACTIONS = ("none_recorded", "account_restricted", "relationship_terminated")
# The suspected offence a str_record.crime_type may carry. SURVEYED against the committed fixtures
# (money_laundering, kyc_integrity, None observed); terrorist_financing is the other PCMLTFA STR class.
# None (absent) is always valid — an ungroundable crime class is honest NULL, never fabricated.
CRIME_TYPES = ("money_laundering", "terrorist_financing", "kyc_integrity")
# The capability -> suspected-offence map: the OFFENCE a cited alert's capability implies. The single source
# of truth shared by crime_type_for (the stamped value), validate_bundle's crime_type agree-with-bundle arm,
# and the drafter's offence-aware narrative — so the structured offence, the contract check, and the prose
# can never drift. An unmapped capability implies no offence (contributes nothing -> honest NULL).
CRIME_BY_CAPABILITY: dict[str, str] = {
    "C2": "money_laundering",
    "C3": "money_laundering",
    "C4": "money_laundering",
    "C5": "money_laundering",
    "C7": "money_laundering",
    "C8": "money_laundering",
    "C15": "money_laundering",
    "C14": "kyc_integrity",
}
# Fixed regulatory-constant strings the action_taken block carries (canonical here so the drafter's
# assembler and this validator never drift). 'FINTRAC' is the statutory STR recipient; the tipping-off
# note is a forward CONTROL/intent statement (NOT an asserted past event) paraphrasing the PCMLTFA s.8
# prohibition on disclosing a report to the client.
ACTION_FILED_TO = "FINTRAC"
ACTION_TIPPING_OFF_NOTE = (
    "This report and the intent to file it must not be disclosed to the client (PCMLTFA tipping-off prohibition)."
)


def _validate_parties(b: dict[str, Any]) -> list[str]:
    """Validate the optional v0.2 `parties` PartyView block -- SHAPE only (every allow-list key is
    present). Additive: an absent `parties` is valid. Values may be None (the optional PartyView fields),
    so this checks key-presence, never non-emptiness. Trust the projection (the substrate's PartyView IS
    the firewall): validate the 16 known keys, tolerate unknown extra fields."""
    if "parties" not in b:
        return []
    parties = b["parties"]
    if not isinstance(parties, list):
        return [f"bundle.parties: must be a list of PartyView rows (got {type(parties).__name__})"]
    out: list[str] = []
    for i, p in enumerate(parties):
        where = f"parties[{i}]"
        if not isinstance(p, dict):
            out.append(f"{where}: must be a PartyView object (got {type(p).__name__})")
            continue
        for field in PARTY_VIEW_FIELDS:
            if field not in p:
                out.append(f"{where}: missing PartyView field '{field}'")
    return out


# --- Phase 13: the additive FINTRAC STR structured blocks (under str_record) -----------------------
# Each validator mirrors `_validate_parties`: an ABSENT block is valid (additive/back-compat); a PRESENT
# block is validated SHAPE + AGREE-WITH-BUNDLE (a stored value that disagrees with the bundle's own facts
# is a violation — a structured field is grounded-or-empty, never fabricated). Unknown extra keys are
# tolerated. The blocks live under str_record, so each reads `b["str_record"].get(<block>)`.


def _str_block(b: dict[str, Any], name: str) -> Any:
    return b.get("str_record", {}).get(name)


def _validate_reporting_entity(b: dict[str, Any]) -> list[str]:
    block = _str_block(b, "reporting_entity")
    if block is None:
        return []
    if not isinstance(block, dict):
        return [f"str_record.reporting_entity: must be an object (got {type(block).__name__})"]
    out: list[str] = []
    et = block.get("entity_type")
    if et is not None and et not in REPORTING_ENTITY_TYPES:
        out.append(f"str_record.reporting_entity: entity_type '{et}' not in {REPORTING_ENTITY_TYPES}")
    if "illustrative" in block and block["illustrative"] != b.get("illustrative"):
        out.append("str_record.reporting_entity: 'illustrative' disagrees with bundle.illustrative")
    return out


def _validate_subject_block(b: dict[str, Any]) -> list[str]:
    block = _str_block(b, "subject")
    if block is None:
        return []
    if not isinstance(block, dict):
        return [f"str_record.subject: must be an object (got {type(block).__name__})"]
    out: list[str] = []
    subject = b.get("subject", {})
    if "customer_id" in block and block["customer_id"] != subject.get("customer_id"):
        out.append("str_record.subject: customer_id disagrees with bundle.subject.customer_id")
    acct_ids = set(subject.get("account_ids", []))
    for aid in block.get("account_ids", []):
        if aid not in acct_ids:
            out.append(f"str_record.subject: account_id '{aid}' not in bundle.subject.account_ids")
    # A name may appear ONLY when the bundle actually carries it (grounded-or-empty at the contract): the
    # no-PII substrate emits name=None, so a non-null name disagreeing with the bundle is a fabrication.
    name = block.get("name")
    if name is not None and name != subject.get("name"):
        out.append("str_record.subject: name disagrees with bundle.subject.name (a name may appear only when grounded)")
    for list_field in ("aliases", "ip_addresses", "vc_addresses"):
        if list_field in block and not isinstance(block[list_field], list):
            out.append(f"str_record.subject: '{list_field}' must be a list")
    return out


def _validate_transaction_summary(b: dict[str, Any]) -> list[str]:
    block = _str_block(b, "transaction_summary")
    if block is None:
        return []
    if not isinstance(block, dict):
        return [f"str_record.transaction_summary: must be an object (got {type(block).__name__})"]
    out: list[str] = []
    expected = transaction_summary(b)
    # Agree-by-recomputation: every present roll-up field must equal the value recomputed from the cited
    # transactions (the single-source-of-truth helper) — a tampered aggregate (incl. the structured total)
    # fails closed. The aggregate sum is grounded HERE, never as a prose $ atom.
    # Every roll-up field (incl. direction_breakdown + disposition) is AGREE-BY-RECOMPUTE: the recomputed
    # value fully grounds it, so a tampered / fabricated / extra / missing entry fails equality and closes —
    # no separate closed-vocab gate (a vocab subset gate over an open source field only false-fails a valid
    # non-CREDIT/DEBIT direction the builder would itself recompute).
    for key in (
        "cited_txn_count",
        "total_cited_amount_cents",
        "amount_min_cents",
        "amount_max_cents",
        "currencies",
        "channels",
        "counterparty_count",
        "date_range",
        "direction_breakdown",
        "disposition",
    ):
        if key in block and block[key] != expected[key]:
            out.append(f"str_record.transaction_summary: '{key}' disagrees with the value recomputed from cited txns")
    return out


def _validate_action_taken(b: dict[str, Any]) -> list[str]:
    block = _str_block(b, "action_taken")
    if block is None:
        return []
    if not isinstance(block, dict):
        return [f"str_record.action_taken: must be an object (got {type(block).__name__})"]
    out: list[str] = []
    # filing_disposition MIRRORS signoff.disposition (the human signer's act) — it is None pre-signoff and
    # stamped by ingest.build_signed_sar at sign time. Validate AGREEMENT only: signoff owns the disposition
    # vocabulary (SYSTEM_/HUMAN_DISPOSITIONS), so a separate closed vocab here would falsely reject a valid one.
    fd = block.get("filing_disposition")
    if fd is not None:
        signoff = b.get("signoff")
        if isinstance(signoff, dict) and signoff.get("disposition") is not None and fd != signoff["disposition"]:
            out.append("str_record.action_taken: filing_disposition disagrees with signoff.disposition")
    if "filed_to" in block and block["filed_to"] != ACTION_FILED_TO:
        out.append(f"str_record.action_taken: filed_to must equal '{ACTION_FILED_TO}' (the statutory STR recipient)")
    if "tipping_off_guard" in block and block["tipping_off_guard"] != ACTION_TIPPING_OFF_NOTE:
        out.append("str_record.action_taken: tipping_off_guard disagrees with the canonical regulatory note")
    aa = block.get("account_action")
    if aa is not None and aa not in ACCOUNT_ACTIONS:
        out.append(f"str_record.action_taken: account_action '{aa}' not in {ACCOUNT_ACTIONS}")
    return out


def _validate_relationships(b: dict[str, Any]) -> list[str]:
    block = _str_block(b, "relationships")
    if block is None:
        return []
    if not isinstance(block, dict):
        return [f"str_record.relationships: must be an object (got {type(block).__name__})"]
    out: list[str] = []
    txns = cited_transactions(b)
    cited_refs = {t.get("counterparty_account_id") for t in txns} | {t.get("counterparty_ref") for t in txns}
    cited_refs.discard(None)
    count = block.get("counterparty_count")
    if count is not None and count != transaction_summary(b)["counterparty_count"]:
        out.append("str_record.relationships: counterparty_count disagrees with the cited transactions")
    for ref in block.get("counterparty_refs", []):
        if ref not in cited_refs:
            out.append(f"str_record.relationships: counterparty_ref '{ref}' appears on no cited transaction")
    country = block.get("counterparty_country")
    if country is not None and country not in ({t.get("counterparty_country") for t in txns} - {None}):
        out.append("str_record.relationships: counterparty_country is present on no cited transaction")
    named = block.get("named_relationships")
    if named is not None and not isinstance(named, list):
        out.append("str_record.relationships: named_relationships must be a list")
    return out


def load_bundle(path: str) -> dict[str, Any]:
    with open(path, encoding="utf-8") as fh:
        data: dict[str, Any] = json.load(fh)
        return data


def cited_transactions(bundle: dict[str, Any]) -> list[dict[str, Any]]:
    """The transactions a str_record cites (txn_id in ``cited_txn_ids``), falling back to ALL transactions
    when the bundle declares no cited list. Shared bundle accessor: the narrative-grounding verifier scopes
    prose amounts/dates to these, and the generator shapes the drafter's context from them — one source of
    truth for "the evidence this record is built on" (contract.py owns bundle-shape knowledge)."""
    cited = set(bundle.get("str_record", {}).get("cited_txn_ids", []))
    txns: list[dict[str, Any]] = bundle.get("transactions", [])
    return [t for t in txns if t.get("txn_id") in cited] or txns


def _txn_date(t: dict[str, Any]) -> str | None:
    """A transaction's ISO date prefix, tolerant of the canonicalize boundary: a real Pillar-1 row carries
    ``timestamp``; ``ingest.canonicalize`` adds ``ts``. Read either so the roll-up is identical pre/post
    canonicalize (the narrative-grounding verifier itself reads the canonicalized ``ts``)."""
    raw = t.get("ts") or t.get("timestamp")
    return raw[:10] if isinstance(raw, str) else None


def transaction_summary(bundle: dict[str, Any]) -> dict[str, Any]:
    """The structured roll-up of the CITED transactions — the FINTRAC STR 'transaction(s) & disposition'
    section as pure, recomputable arithmetic. ONE source of truth (like ``cited_transactions``): the drafter's
    block assembler and the contract validator both call this, so the stored block and its check can never
    diverge. Carries the AGGREGATE total as a structured integer (``total_cited_amount_cents``) — the figure
    the gated narrative deliberately never prints as a $ atom (a sum equals no individual cited amount, so it
    is grounded HERE by recomputation, not through the prose gate)."""
    txns = cited_transactions(bundle)
    cents = [t["amount_cents"] for t in txns if isinstance(t.get("amount_cents"), int)]
    dates = sorted(d for d in (_txn_date(t) for t in txns) if d)
    counterparties = {(t.get("counterparty_account_id") or t.get("counterparty_ref")) for t in txns}
    counterparties.discard(None)
    directions = Counter(t["direction"] for t in txns if t.get("direction"))
    # Txn disposition (TXN_DISPOSITIONS: completed vs attempted — FINTRAC files both) is DERIVED from a
    # per-txn status/disposition field, never defaulted: the no-PII synthetic bundle carries none, so this
    # is honest None (a "completed" default would assert a regulatory fact the evidence is silent on).
    statuses = {(t.get("disposition") or t.get("status")) for t in txns}
    statuses.discard(None)
    return {
        "cited_txn_count": len(txns),
        "total_cited_amount_cents": sum(cents),
        "amount_min_cents": min(cents) if cents else None,
        "amount_max_cents": max(cents) if cents else None,
        "currencies": sorted({t["currency"] for t in txns if t.get("currency")}),
        "channels": sorted({t["channel"] for t in txns if t.get("channel")}),
        "direction_breakdown": dict(directions),
        "date_range": {"first": dates[0], "last": dates[-1]} if dates else {"first": None, "last": None},
        "counterparty_count": len(counterparties),
        "disposition": next(iter(statuses)) if len(statuses) == 1 else None,
    }


def _implied_crime_types(bundle: dict[str, Any]) -> set[str]:
    """The offence classes the CITED signals' capabilities imply (``CRIME_BY_CAPABILITY`` over the cited
    alerts) — the grounding basis for ``crime_type``: a declared offence must be one the cited evidence
    actually implies, else it is ungrounded (the validator flags the disagreement)."""
    cited = set(bundle.get("str_record", {}).get("cited_signal_ids") or [])
    implied: set[str] = set()
    for alert in bundle.get("alerts", []):
        if alert.get("grounding", {}).get("signal_id") in cited:
            crime = CRIME_BY_CAPABILITY.get(alert.get("capability") or "")
            if crime is not None:
                implied.add(crime)
    return implied


def crime_type_for(bundle: dict[str, Any]) -> str | None:
    """The suspected offence to STAMP on str_record — PRESERVED if the bundle already declares one (a human
    judgment), else DERIVED as the single offence the cited capabilities imply, else None (honest NULL: no
    cited signal, or the cited capabilities imply no single offence). A declared offence that CONTRADICTS the
    cited capabilities is NOT silently overridden here — ``validate_bundle``'s crime_type arm flags it
    (fail-closed). The single source of truth for both the structured field and the drafter's offence label."""
    declared = bundle.get("str_record", {}).get("crime_type")
    if isinstance(declared, str):
        return declared
    implied = _implied_crime_types(bundle)
    return next(iter(implied)) if len(implied) == 1 else None


def party_ids(bundle: dict[str, Any]) -> set[str]:
    """The party_ids declared in the v0.2 ``parties`` block — the resolution target for a party-leaf
    alert's ``party_ref`` (reference-by-path). Shared bundle accessor (contract.py owns bundle-shape
    knowledge, like ``cited_transactions``): the leaf-XOR rule resolves a ``party_ref`` against this set,
    and the completeness verifier reuses it to substantiate a txn-less case via its resolving party leaf.
    Tolerates a malformed/absent block (returns what resolves) and admits ONLY a non-empty STRING
    party_id: a party_id is a string by contract, so a None/empty/non-string value is not a resolution
    target (fail-closed) — and restricting to strings keeps the set hashable (an unhashable party_id
    value never crashes the membership tests this set backs)."""
    parties = bundle.get("parties", [])
    if not isinstance(parties, list):
        return set()
    return {
        p["party_id"] for p in parties if isinstance(p, dict) and isinstance(p.get("party_id"), str) and p["party_id"]
    }


def validate_bundle(b: dict[str, Any]) -> list[str]:
    """Return a list of contract violations; empty list == conforms."""
    v: list[str] = []

    def req(obj: dict[str, Any], key: str, where: str) -> bool:
        if key not in obj or obj[key] in (None, "", [], {}):
            v.append(f"{where}: missing/empty '{key}'")
            return False
        return True

    # --- bundle-level honesty + identity ---
    req(b, "contract_version", "bundle")
    cv = b.get("contract_version")
    if cv is not None and cv not in KNOWN_CONTRACT_VERSIONS:
        v.append(f"bundle: unknown contract_version '{cv}' (validated versions: {', '.join(KNOWN_CONTRACT_VERSIONS)})")
    if b.get("illustrative") is not True:
        v.append("bundle: 'illustrative' must be true (synthetic bootstrap fixtures are labeled)")
    req(b, "case_id", "bundle")

    subject = b.get("subject", {})
    req(subject, "customer_id", "subject")
    acct_ids = set(subject.get("account_ids", []))
    if not acct_ids:
        v.append("subject: empty 'account_ids'")

    # --- data rows the alerts cite ---
    txn_ids = set()
    for i, t in enumerate(b.get("transactions", [])):
        where = f"transactions[{i}]"
        if req(t, "txn_id", where) and req(t, "account_id", where):
            txn_ids.add(t["txn_id"])
        # exculpatory marker: a transaction may be documented counter-evidence (argues AGAINST suspicion).
        # It lives on the data row — the grounding leaf — not on a derived alert (an exculpatory alert
        # has no inculpatory pattern to replay and no real exculpatory corpus indicator to ground).
        # Absent == inculpatory by default. Fail-closed: a non-boolean marker is unverifiable -> violation.
        exc = t.get("exculpatory")
        if exc is not None and not isinstance(exc, bool):
            v.append(f"{where}: 'exculpatory' must be a boolean when present (got {type(exc).__name__})")
    if not txn_ids:
        v.append("bundle: no transactions (the data rows alerts must cite)")

    # The party_ids the v0.2 `parties` block declares -- the resolution target for a party-leaf alert's
    # `party_ref` (reference-by-path). An absent/malformed parties block resolves to nothing, so any
    # party_ref fails to resolve -> fail-closed (the shared accessor also excludes a falsy party_id).
    declared_party_ids = party_ids(b)

    # --- alerts: the reference-by-path grounding chain ---
    alert_ids = set()
    alert_signal_ids = set()
    for i, a in enumerate(b.get("alerts", [])):
        where = f"alerts[{i}]"
        for k in ("alert_id", "detector", "capability", "account_id", "rule"):
            req(a, k, where)
        alert_ids.add(a.get("alert_id"))
        if a.get("account_id") not in acct_ids:
            v.append(f"{where}: account_id '{a.get('account_id')}' not in subject.account_ids")
        # The grounding LEAF rule, widened (Phase 12): an alert grounds on EXACTLY ONE leaf --
        # a non-empty `txn_ids` (a transaction-leaf alert: replay/screen over cited data rows) XOR a
        # resolving `party_ref` (a party-leaf alert: a static-state screen rooting the grounding walk at a
        # party row, e.g. txn-less C14 KYC-integrity). The reference-by-path doctrine extends from
        # txn-leaf-only to txn-leaf XOR party-leaf; neither leaf or both leaves is a violation (no
        # ungrounded alert, no double-cite). A party_ref that resolves to no parties[].party_id fails
        # closed -- an unresolvable reference is ungroundable, never a silent pass.
        cited = a.get("txn_ids", [])
        party_ref = a.get("party_ref")
        has_txn_leaf = bool(cited)
        has_party_leaf = party_ref not in (None, "")
        if has_txn_leaf and has_party_leaf:
            v.append(f"{where}: cites both a txn leaf and a party_ref (an alert grounds on EXACTLY ONE leaf)")
        elif not has_txn_leaf and not has_party_leaf:
            v.append(f"{where}: cites neither leaf (EXACTLY ONE required: non-empty txn_ids XOR a resolving party_ref)")
        for tid in cited:
            if tid not in txn_ids:
                v.append(f"{where}: cites unknown txn_id '{tid}'")
        # Resolution: only a STRING party_ref can match a declared id. The isinstance guard short-circuits
        # before the membership test, so an unhashable party_ref (a list/dict) fails closed with a
        # violation -- never a TypeError that crashes the verifier on untrusted input.
        if has_party_leaf and not (isinstance(party_ref, str) and party_ref in declared_party_ids):
            v.append(f"{where}: party_ref '{party_ref}' does not resolve to any parties[].party_id (fail-closed)")
        g = a.get("grounding", {})
        for k in ("signal_id", "advisory_id", "indicator_id", "capability", "data_source", "flag"):
            req(g, k, f"{where}.grounding")
        if g.get("signal_id") and g.get("signal_id") != f"{g.get('advisory_id')}:{g.get('indicator_id')}":
            v.append(f"{where}.grounding: signal_id '{g.get('signal_id')}' != '<advisory_id>:<indicator_id>'")
        if g.get("capability") and a.get("capability") and g["capability"] != a["capability"]:
            v.append(f"{where}: capability '{a['capability']}' disagrees with grounding.capability '{g['capability']}'")
        alert_signal_ids.add(g.get("signal_id"))

    # --- dossier (account-keyed; mirrors aml_substrate.monitor.compose.Dossier) ---
    d = b.get("dossier", {})
    if d:
        req(d, "dossier_id", "dossier")
        if d.get("account_id") not in acct_ids:
            v.append(f"dossier: account_id '{d.get('account_id')}' not in subject.account_ids")
        for aid in d.get("alert_ids", []):
            if aid not in alert_ids:
                v.append(f"dossier: references unknown alert_id '{aid}'")

    # --- STR scaffold + the narrative seam ---
    s = b.get("str_record", {})
    if s:
        if s.get("case_id") != b.get("case_id"):
            v.append("str_record: case_id disagrees with bundle.case_id")
        for aid in s.get("subject_account_ids", []):
            if aid not in acct_ids:
                v.append(f"str_record: subject account '{aid}' not in subject.account_ids")
        for sid in s.get("cited_signal_ids", []):
            if sid not in alert_signal_ids:
                v.append(f"str_record: cited_signal_id '{sid}' is grounded by no alert")
        for tid in s.get("cited_txn_ids", []):
            if tid not in txn_ids:
                v.append(f"str_record: cited_txn_id '{tid}' is unknown")
        comp = s.get("completeness", {})
        for el in STR_REQUIRED_ELEMENTS:
            if el not in comp:
                v.append(f"str_record.completeness: missing element '{el}'")
        # the seam invariant, both directions: narrative present iff its flag is set
        narr = s.get("narrative")
        flag = comp.get("grounds_for_suspicion_narrative")
        if narr in (None, "") and flag is True:
            v.append("str_record: grounds_for_suspicion_narrative=true but narrative is empty")
        if narr not in (None, "") and flag is not True:
            v.append("str_record: narrative present but grounds_for_suspicion_narrative!=true (Pillar 2 must flip it)")
        # structured narrative: Pillar 2 writes narrative_claims; the contract checks STRUCTURE only
        # (each claim has non-empty text + cites). citation.verify_citations checks the cites RESOLVE.
        for j, claim in enumerate(s.get("narrative_claims", [])):
            cw = f"str_record.narrative_claims[{j}]"
            req(claim, "text", cw)
            req(claim, "cites", cw)
            stance = claim.get("stance")
            if stance is not None and stance not in CLAIM_STANCES:
                v.append(f"{cw}: invalid stance '{stance}' (allowed: {CLAIM_STANCES}; absent = inculpatory)")
        # crime_type (Phase 13): the suspected offence, a closed-vocab enum. None (absent) is valid —
        # an ungroundable crime class is honest NULL, never fabricated. A non-None crime_type must be in
        # the closed vocab AND be grounded by at least one cited signal (a crime claim with no grounding
        # signal fails closed — grounded-or-dropped applied to the offence label).
        crime_type = s.get("crime_type")
        if crime_type is not None:
            if crime_type not in CRIME_TYPES:
                v.append(f"str_record: crime_type '{crime_type}' not in {CRIME_TYPES}")
            if not s.get("cited_signal_ids"):
                v.append("str_record: crime_type is set but cited_signal_ids is empty (no grounding signal)")
            else:
                # Agree-with-bundle: a declared offence must be one the CITED capabilities actually imply —
                # else the label contradicts the evidence (e.g. 'money_laundering' over a kyc_integrity-only
                # case). Mirrors the structured blocks' agree-with-bundle arms.
                implied = _implied_crime_types(b)
                if implied and crime_type not in implied:
                    v.append(
                        f"str_record: crime_type '{crime_type}' disagrees with the cited capabilities' "
                        f"implied offence {sorted(implied)}"
                    )

    # --- v0.2 additive: the optional `parties` PartyView block (the screening-grounding data source) ---
    v.extend(_validate_parties(b))
    # --- Phase 13 additive: the optional FINTRAC STR structured blocks (under str_record) ---
    v.extend(_validate_reporting_entity(b))
    v.extend(_validate_subject_block(b))
    v.extend(_validate_transaction_summary(b))
    v.extend(_validate_action_taken(b))
    v.extend(_validate_relationships(b))

    return v


def main(argv: list[str]) -> int:
    # CLI boundary: print() is the legitimate stdout/stderr channel here (README documents
    # `python3 src/aml_casework/contract.py <bundle.json>`). The no-print rule targets library logic.
    if len(argv) != 2:
        print("usage: python3 contract.py <bundle.json>", file=sys.stderr)  # noqa: T201
        return 2
    violations = validate_bundle(load_bundle(argv[1]))
    if violations:
        print(f"INVALID ({len(violations)} violation(s)):")  # noqa: T201
        for x in violations:
            print(f"  - {x}")  # noqa: T201
        return 1
    print(f"OK -- {argv[1]} conforms to the Pillar-1->Pillar-2 contract")  # noqa: T201
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
