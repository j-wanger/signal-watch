"""Narrative generator — the one neural step, fenced by the six deterministic Class-G verifiers.

``generate_narrative`` fills the narrative seam (``narrative`` + ``narrative_claims`` + the
``grounds_for_suspicion_narrative`` flag) over an injected ``Drafter``, wrapped in a BOUNDED
regenerate-against-verifier-feedback loop. Each attempt: draft -> fill the seam -> run the six verifiers
(``signoff.run_verifiers``). A clean candidate is returned; a violating candidate's violations are fed
back to the drafter and it regenerates, up to ``MAX_DRAFT_ATTEMPTS``. If the drafter refuses or no attempt
verifies, the seam is left OPEN — fail-closed; the chain then reports ``needs_more_info``, never a filed
STR. The "judge" is the deterministic verifier chain, never a neural judge (a stronger, deterministic form
of the "Agent-as-a-Judge" guardrail).

The Drafter is the boundary where a real LLM adapter (``ClaudeDrafter``, a later increment) or a
deterministic test stub plugs in. ``generate_narrative`` itself is pure (it deepcopies the bundle, the
only I/O is structured logging), so the verifier suite stays deterministic: CI injects stub drafters and
the gate, not the model, is the oracle. Each attempt is logged (the generator is now an SR 11-7-governed
model artifact — the attempt trail is the audit record).
"""

from __future__ import annotations

import copy
import logging
from dataclasses import dataclass
from typing import Any, Protocol

from aml_casework.contract import (
    ACTION_FILED_TO,
    ACTION_TIPPING_OFF_NOTE,
    cited_transactions,
    crime_type_for,
    transaction_summary,
)
from aml_casework.signoff import flatten_violations, run_verifiers

_log = logging.getLogger(__name__)

# How many times the drafter may regenerate against verifier feedback before the generator fails closed.
# Pinned: the loop is BOUNDED (no infinite regenerate), and a draft that cannot be made groundable within
# this many tries leaves the seam OPEN — never a filed STR.
MAX_DRAFT_ATTEMPTS = 3


@dataclass(frozen=True)
class GenerationContext:
    """The grounding surface the drafter sees: the subject, the cited transactions the prose may
    reference, and the grounded signal ids its claims must cite. Shaping this surface is the highest-
    leverage lever — but the six verifiers gate the output regardless of how the draft was produced."""

    subject: dict[str, Any]
    cited_transactions: list[dict[str, Any]]
    signal_ids: list[str]


@dataclass(frozen=True)
class Draft:
    """A drafter's output: the human-facing prose plus the structured, cite-resolvable claims. Both fill
    the seam; the verifiers gate them (citation over the claims, narrative_grounding over the prose)."""

    narrative: str
    narrative_claims: list[dict[str, Any]]


class Drafter(Protocol):
    """The neural step's boundary — a real adapter (``ClaudeDrafter``) or a deterministic test stub.

    ``draft`` returns a :class:`Draft`, or ``None`` to refuse (fail-closed — the seam stays open).
    ``feedback`` carries the previous attempt's verifier violations on a regenerate pass; it is ``None``
    on the first attempt."""

    def draft(self, context: GenerationContext, feedback: list[str] | None = None) -> Draft | None: ...


def _build_context(bundle: dict[str, Any]) -> GenerationContext:
    """Extract the grounding surface from a composed bundle (one job: shape what the drafter sees)."""
    signal_ids = [
        a["grounding"]["signal_id"] for a in bundle.get("alerts", []) if a.get("grounding", {}).get("signal_id")
    ]
    return GenerationContext(
        subject=bundle.get("subject", {}),
        cited_transactions=cited_transactions(bundle),
        signal_ids=signal_ids,
    )


def build_str_blocks(bundle: dict[str, Any]) -> dict[str, Any]:
    """Assemble the deterministic FINTRAC STR structured blocks from the bundle — SYSTEM-STAMPED, never
    model-authored (the Phase-66 lesson: a real model fabricates structured facts — pct, direction, names).
    Every value is bundle-grounded or HONEST-NULL; the no-PII bundle yields null name/aliases/BO/IP/VC. The
    aggregate total lives here as a structured integer (``transaction_summary.total_cited_amount_cents``),
    grounded by recomputation — the figure the gated prose deliberately never prints. Attached at the seam
    (``_apply_draft``) regardless of which drafter produced the prose, so it cannot diverge by backend."""
    subject = bundle.get("subject", {})
    ts = transaction_summary(bundle)
    txns = cited_transactions(bundle)
    counterparties = {(t.get("counterparty_account_id") or t.get("counterparty_ref")) for t in txns}
    refs = sorted(r for r in counterparties if r is not None)
    return {
        "crime_type": crime_type_for(bundle),
        "reporting_entity": {
            # The reporting entity's identity/sector is the FILER's, supplied at filing time — NOT carried
            # by this evidence bundle. Honest-NULL unless the bundle declares it (it never does today); the
            # demo frames "financial entity" at the UI layer, not as a fabricated structured fact.
            "entity_type": bundle.get("reporting_entity", {}).get("entity_type"),
            "entity_ref": None,
            "illustrative": bundle.get("illustrative"),
        },
        "subject": {
            "customer_id": subject.get("customer_id"),
            "account_ids": list(subject.get("account_ids", [])),
            "name": subject.get("name"),
            "aliases": [],
            "beneficial_ownership": None,
            "ip_addresses": [],
            "vc_addresses": [],
            "emt_details": None,
            "date_of_birth": None,
        },
        "transaction_summary": dict(ts),  # carries disposition (honest-NULL unless a txn declares one)
        "action_taken": {
            "filing_disposition": None,  # set post-signoff by ingest.build_signed_sar (the human's act)
            "filed_to": ACTION_FILED_TO,
            "tipping_off_guard": ACTION_TIPPING_OFF_NOTE,
            "account_action": None,
        },
        "relationships": {
            "counterparty_count": ts["counterparty_count"],
            "counterparty_refs": refs,
            "counterparty_country": None,
            "named_relationships": [],
        },
    }


def _apply_draft(bundle: dict[str, Any], draft: Draft) -> dict[str, Any]:
    """Return a NEW bundle with the seam fields filled from the draft plus the deterministic FINTRAC STR
    structured blocks attached (the input is not mutated).

    The drafter authored ONLY ``narrative`` + ``narrative_claims`` (the one neural step). The structured
    blocks + crime_type are recomputed from the bundle and ATTACHED here — so they are identical regardless
    of backend AND any model-supplied block is OVERWRITTEN (the Phase-66 fabrication guard)."""
    result = copy.deepcopy(bundle)
    record = result.setdefault("str_record", {})
    record["narrative"] = draft.narrative
    record["narrative_claims"] = draft.narrative_claims
    record.setdefault("completeness", {})["grounds_for_suspicion_narrative"] = True
    record.update(build_str_blocks(bundle))  # system-stamped; overwrites any model-supplied block
    return result


def generate_narrative(bundle: dict[str, Any], drafter: Drafter) -> dict[str, Any]:
    """Fill the narrative seam over an injected drafter, bounded-regenerate against verifier feedback.

    Returns a NEW bundle (the input is not mutated). A clean draft fills the seam; a violating draft is
    refused at verification and its violations are fed back for regeneration, up to MAX_DRAFT_ATTEMPTS. On
    a drafter refusal or exhausted attempts the seam is left OPEN — fail-closed. Each attempt is logged."""
    context = _build_context(bundle)
    feedback: list[str] | None = None
    for attempt in range(1, MAX_DRAFT_ATTEMPTS + 1):
        draft = drafter.draft(context, feedback=feedback)
        if draft is None:
            _log.info("narrative draft attempt %d refused by drafter; failing closed (seam open)", attempt)
            return copy.deepcopy(bundle)
        candidate = _apply_draft(bundle, draft)
        violations = flatten_violations(run_verifiers(candidate))
        if not violations:
            _log.info("narrative draft attempt %d verified; seam filled", attempt)
            return candidate
        _log.warning(
            "narrative draft attempt %d failed verification (%d violation(s)); regenerating",
            attempt,
            len(violations),
        )
        feedback = violations
    _log.warning("narrative generation failed closed after %d attempts; seam left open", MAX_DRAFT_ATTEMPTS)
    return copy.deepcopy(bundle)
