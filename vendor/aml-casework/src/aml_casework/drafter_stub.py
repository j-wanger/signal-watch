"""Deterministic, bundle-derived production drafter (Phase 7) — the FIRST drafter shipped in ``src/``.

Every prior drafter was test-only (``FixedDraftStub`` / ``ReplayDrafter``) or demo-only (``ClaudeDrafter``).
This is the deterministic "verifier-is-oracle" drafter the chain workbench falls back to whenever no model is
available: it builds a minimally-grounded :class:`Draft` mechanically from the bundle, so it grounds for ANY
inculpatory-only library case without per-case authoring.

How it grounds by construction (against the six verifiers — ``narrative_grounding`` in particular):

- one INCULPATORY claim per cited signal (``cites=[signal_id]``); each signal_id is grounded by
  construction, so ``citation`` resolves it and the suspicion is grounded.
- prose that names ONLY the subject ``account_id`` (a grounded id) plus generic, all-lowercase typology
  phrases — NO monetary amount, NO date, NO >=2-token Title-Case party run. So ``narrative_grounding`` finds
  no ungroundable atom.

SCOPE — INCULPATORY ONLY (documented limit, Phase-7 A4). A bundle carrying an ``exculpatory: true``
transaction would trip the ``citation`` conflict-both-kept check (an exculpatory-stance claim must cite it),
which this drafter does not emit — so it fails CLOSED (the bounded loop exhausts, the seam stays open,
``record_signoff`` -> ``needs_more_info``), VISIBLY, never a silent or fabricated sign-off. The documented
fallback for an exculpatory or otherwise un-mechanizable library bundle is a per-case committed-draft replay;
never loosen a verifier. Today's vendored library bundle (CASE-P-0010361) is a pure 5-typology mule with no
exculpatory transactions.
"""

from __future__ import annotations

from typing import Any

from aml_casework.contract import crime_type_for, transaction_summary
from aml_casework.narrative_generator import Draft, GenerationContext

# Frozen corpus CAPABILITY vocabulary -> (claim sentence, lowercase prose phrase). Keyed on the capability,
# NOT on a case id, so the drafter generalizes across any bundle citing these red-flags. An unmapped
# capability falls back to generic, atom-free phrasing (still grounds, never fabricates a specific).
_CAPABILITY_PHRASING: dict[str, tuple[str, str]] = {
    "C4": (
        "Cash deposits below the currency-transaction reporting threshold indicate structuring.",
        "cash deposits structured below the reporting threshold",
    ),
    "C2": (
        "Rapid forwarding of received funds indicates pass-through layering.",
        "rapid pass-through forwarding of received funds",
    ),
    "C3": (
        "Outflows across multiple counterparties indicate a fan-out pattern.",
        "outflows fanned out across multiple counterparties",
    ),
    "C5": (
        "Repeated cash deposits indicate placement of physical cash.",
        "repeated placement of physical cash through deposits",
    ),
    "C15": (
        "Near-zero net retention across counterparties indicates a shell conduit.",
        "near-zero-retention throughput consistent with a shell conduit",
    ),
}
_GENERIC_CLAIM = "The cited indicator grounds a suspicion of money laundering."
_GENERIC_PHRASE = "activity consistent with the cited red-flag typology"


def _signal_capability(bundle: dict[str, Any]) -> dict[str, str]:
    """Map each grounded ``signal_id`` to its alert ``capability`` (the lookup the prose/claims phrase on)."""
    mapping: dict[str, str] = {}
    for alert in bundle.get("alerts", []):
        signal_id = alert.get("grounding", {}).get("signal_id")
        capability = alert.get("capability")
        if isinstance(signal_id, str) and isinstance(capability, str):
            mapping[signal_id] = capability
    return mapping


def _claim(signal_id: str, capability: str | None) -> dict[str, Any]:
    """One inculpatory claim citing a grounded signal. The claim text is not atom-checked (``citation``
    reads the ``cites``); the capability map only improves readability."""
    text = _CAPABILITY_PHRASING.get(capability or "", (_GENERIC_CLAIM, ""))[0]
    return {"text": text, "cites": [signal_id], "stance": "inculpatory"}


def _narrative(account_id: str | None, capabilities: list[str | None]) -> str:
    """Prose naming ONLY the subject ``account_id`` + generic lowercase typology phrases — no atom the gate
    cannot ground (no amounts, no dates, no >=2-token Title-Case party)."""
    lead = (
        f"Account {account_id} exhibits the following grounded indicators"
        if account_id
        else "The reviewed account exhibits the following grounded indicators"
    )
    phrases = [_CAPABILITY_PHRASING.get(cap or "", ("", _GENERIC_PHRASE))[1] for cap in capabilities]
    body = "; ".join(p for p in phrases if p) or "activity consistent with the cited red-flag typologies"
    return (
        f"{lead}: {body}. Each cited indicator is independently grounded to the cited "
        "transactions and the regulator corpus."
    )


# --- Phase 13: the FINTRAC-STR-rich narrative (grounded-by-construction) ---------------------------
#
# The thin ``_narrative`` above commits FINTRAC's named STR-quality deficiency: "generic narratives that
# restate transaction details without explaining why they are suspicious" (aml-wiki:
# canadian-str-reporting-quality). ``_rich_narrative`` is the richer "Details of suspicion": it weaves
# atoms the narrative_grounding verifier ALREADY grounds — the subject account id, INDIVIDUAL cited
# transaction amounts (min/max endpoints), and the $10,000 CTR regulatory constant — plus bare-integer
# counts (out of the verifier's atom scope), and articulates reasonable-grounds-to-suspect by connecting
# each observed indicator to the specific money-laundering suspicion. The verifier is UNCHANGED: every $
# figure is an exact cited amount (or the documented CTR constant), there is no ISO date and no >=2-token
# Title-Case run (the no-PII synthetic bundle carries no party names to ground), so the prose grounds by
# construction. Aggregate SUMS are stated as counts, never as $ figures (a sum is not a cited amount).

# RGS-framed grounds clause per capability — all-lowercase (no Title-Case run the verifier reads as a
# party), connecting the indicator to the suspicion rather than merely restating it. The C4 clause names
# the $10,000 threshold (a grounded REGULATORY_CONSTANT) under its Canadian name (LCTR). An unmapped
# capability falls back generic. Keyed on the SAME capability vocab the structured offence map uses.
_RGS_GROUNDS: dict[str, str] = {
    "C4": (
        "cash deposits were structured below the $10,000 large-cash-transaction reporting (LCTR) threshold, "
        "consistent with deliberate evasion of reporting rather than the dollar amount alone"
    ),
    "C5": "physical cash was placed into the account through repeated deposits",
    "C2": (
        "received funds were forwarded onward within a short interval and with no apparent economic "
        "purpose, consistent with pass-through layering"
    ),
    "C3": "outflows were fanned out across {n_cp} distinct counterparties",
    "C15": (
        "near-zero net retention across those counterparties is consistent with use of the account as a shell conduit"
    ),
    "C14": (
        "the recorded customer due-diligence information is incomplete or inconsistent, undermining the "
        "integrity of the know-your-customer record"
    ),
}
_GENERIC_GROUND = "activity consistent with the cited red-flag indicator was observed"

# The suspected-offence phrasing, keyed on the structured crime_type (contract.crime_type_for) so the prose
# offence and the str_record.crime_type can NEVER disagree (the review's self-contradicting-STR class). The
# typology adjective is offered only for the typology offences (ML/TF); a KYC-integrity / None offence is
# NOT a transaction typology, so it gets no "typologies" framing.
_OFFENCE_NOUN: dict[str, str] = {
    "money_laundering": "money laundering",
    "terrorist_financing": "terrorist financing",
    "kyc_integrity": "a customer due-diligence (KYC) integrity deficiency",
}
_OFFENCE_TYPOLOGY_ADJ: dict[str, str] = {
    "money_laundering": "money-laundering",
    "terrorist_financing": "terrorist-financing",
}


def _rich_narrative(bundle: dict[str, Any]) -> str:
    """A grounded, FINTRAC-structured "Details of suspicion" narrative built mechanically from the bundle.

    Follows FINTRAC's STR narrative shape — WHO / WHAT / WHEN / WHERE / WHY-grounds-per-indicator (RGS) /
    HOW / action-taken / honest-gap — and grounds by construction against the UNCHANGED narrative_grounding
    verifier: the only $ figures are exact INDIVIDUAL cited amounts (min/max endpoints) and the $10,000 CTR
    constant (NEVER an aggregate sum — a sum equals no cited amount; the total lives structured in
    transaction_summary); dates are exact cited-txn ISO prefixes; counts are bare integers (out of atom
    scope); no >=2-token Title-Case run (the no-PII bundle has no party names to ground); customer_id /
    counterparty refs / jurisdictions are NEVER printed (they ungroundor are not in evidence). Every number
    comes from the single-source-of-truth ``transaction_summary`` so prose and the structured block agree.
    Generalizes across any inculpatory bundle — phrasing keys on the cited capabilities, not on a case id."""
    ts = transaction_summary(bundle)
    subject = bundle.get("subject", {})
    account_ids = subject.get("account_ids") or []
    account_id = account_ids[0] if account_ids else None
    n_txn = ts["cited_txn_count"]
    n_cp = ts["counterparty_count"]
    capabilities = sorted({a.get("capability") for a in bundle.get("alerts", []) if a.get("capability")})

    # The offence label comes from the SAME source as the structured crime_type, so prose + record agree.
    crime = crime_type_for(bundle)
    offence_noun = _OFFENCE_NOUN.get(crime or "", "the activity reported here")
    typology_adj = _OFFENCE_TYPOLOGY_ADJ.get(crime or "")  # None for a non-typology offence (KYC / unknown)

    # WHO + WHAT — names ONLY the subject account_id (a grounded id; customer_id would NOT ground). The
    # "composite pattern across N typologies" framing is asserted ONLY for a typology offence with >1 cited
    # indicator (never "across 1 typologies", never a typology claim for a KYC-integrity case). Pluralized.
    txn_word = "transaction" if n_txn == 1 else "transactions"
    subject_lead = f"Account {account_id}" if account_id else "The reviewed account"
    lead = f"{subject_lead} conducted {n_txn} {txn_word}"
    if typology_adj and len(capabilities) > 1:
        lead += f" exhibiting a composite pattern across {len(capabilities)} {typology_adj} typologies"
    elif typology_adj and len(capabilities) == 1:
        lead += f" exhibiting a {typology_adj} typology"
    lead += "."

    # WHEN — exact cited-txn date endpoints (omitted if the bundle carries no timestamps).
    dr = ts["date_range"]
    when = ""
    if dr.get("first") and dr.get("last"):
        when = f" The reviewed activity spanned {dr['first']} to {dr['last']}."

    # HOW — magnitude as INDIVIDUAL min/max amounts, never an aggregate $ sum.
    amin, amax = ts["amount_min_cents"], ts["amount_max_cents"]
    span = (
        f" Individual transaction values ranged from ${amin / 100:,.2f} to ${amax / 100:,.2f}."
        if amin is not None and amax is not None
        else ""
    )

    # WHERE — channels + currency. The currency code stays MID-sentence (the sentence ends on the lowercase
    # "channels") so an uppercase code is never sentence-final before a capitalized next word — that adjacency
    # ("CAD. The") would read to narrative_grounding as a >=2-token Title-Case party run. Channels lowercased.
    where = ""
    if ts["channels"]:
        chans = ", ".join(c.lower() for c in ts["channels"])
        curr = ", ".join(ts["currencies"]) if ts["currencies"] else "the recorded currency"
        where = f" Funds moved in {curr} through {chans} channels."

    # WHY — RGS grounds, one clause per cited indicator, connecting each to the specific ML suspicion.
    clauses = [_RGS_GROUNDS.get(cap or "", _GENERIC_GROUND).format(n_cp=n_cp) for cap in capabilities]
    grounds = "; ".join(clauses) if clauses else _GENERIC_GROUND
    body = (
        f" The following grounds support a reasonable suspicion of {offence_noun}: {grounds}."
        if clauses
        else f" {grounds.capitalize()}."
    )

    # ACTION TAKEN — procedural, disposition-neutral; the tipping-off line is a forward CONTROL/intent (it
    # must NOT be disclosed), never an asserted past event. NO possessive apostrophe anywhere in the prose:
    # the verifier reads a pair of apostrophes as a quoted party span, so the narrative stays apostrophe-free.
    action = (
        " A suspicious transaction report has been prepared for filing with FINTRAC; this report and the "
        "intent to file it must not be disclosed to the client. The decision to file remains the act of the "
        "human signer."
    )

    # HONEST GAP — the FINTRAC-requested fields the no-PII record cannot supply, surfaced not hidden.
    gap = (
        " The following FINTRAC-requested details are not available in this record and are reported as "
        "unavailable: subject name, aliases, beneficial ownership, identification numbers, IP and "
        "virtual-currency addresses, and counterparty jurisdiction."
    )

    close = " Each cited indicator is independently grounded to the cited transactions and the regulator corpus."
    return f"{lead}{when}{span}{where}{body}{action}{gap}{close}"


class DeterministicDrafter:
    """Mechanical, bundle-derived drafter implementing the ``Drafter`` Protocol. Constructed with the bundle
    so it can phrase each claim/clause by the cited signal's capability; ``draft`` then iterates the
    context's grounded signal ids (the grounding surface the verifiers check). Pure + deterministic; ignores
    feedback (its first draft grounds by construction — if it ever did not, ignoring feedback fails CLOSED)."""

    def __init__(self, bundle: dict[str, Any]) -> None:
        self._capability_by_signal = _signal_capability(bundle)

    def draft(self, context: GenerationContext, feedback: list[str] | None = None) -> Draft | None:
        capabilities = [self._capability_by_signal.get(signal_id) for signal_id in context.signal_ids]
        claims = [_claim(sig, cap) for sig, cap in zip(context.signal_ids, capabilities, strict=True)]
        account_ids = context.subject.get("account_ids") or []
        account_id = account_ids[0] if account_ids else None
        return Draft(narrative=_narrative(account_id, capabilities), narrative_claims=claims)


class RichDeterministicDrafter(DeterministicDrafter):
    """Phase 13: the DeterministicDrafter with the rich FINTRAC "Details of suspicion" narrative.

    Reuses the parent's one-inculpatory-claim-per-signal machinery (the ``narrative_claims`` the citation
    verifier reads) and swaps the thin prose for ``_rich_narrative``. Still pure + deterministic; ignores
    feedback (its first draft grounds by construction — if it ever did not, ignoring feedback fails CLOSED)."""

    def __init__(self, bundle: dict[str, Any]) -> None:
        super().__init__(bundle)
        self._bundle = bundle

    def draft(self, context: GenerationContext, feedback: list[str] | None = None) -> Draft | None:
        base = super().draft(context, feedback)
        if base is None:
            return None
        return Draft(narrative=_rich_narrative(self._bundle), narrative_claims=base.narrative_claims)
