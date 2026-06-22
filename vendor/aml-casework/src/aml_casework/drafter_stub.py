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
