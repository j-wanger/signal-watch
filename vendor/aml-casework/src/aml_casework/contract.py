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

    # --- v0.2 additive: the optional `parties` PartyView block (the screening-grounding data source) ---
    v.extend(_validate_parties(b))

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
