"""Narrative generator — the one neural step, fenced by the six deterministic Class-G verifiers.

``generate_narrative`` fills the narrative seam (``narrative`` + ``narrative_claims`` + the
``grounds_for_suspicion_narrative`` flag) over an injected ``Drafter``, wrapped in a BOUNDED
regenerate-against-verifier-feedback loop. Each attempt: draft -> fill the seam -> run the six verifiers
(``signoff.run_verifiers``). A clean candidate is returned; a violating candidate's violations are fed
back to the drafter and it regenerates, up to ``MAX_DRAFT_ATTEMPTS``. If the drafter refuses or no attempt
verifies, the seam is left OPEN — fail-closed; the chain then reports ``needs_more_info``, never a filed
SAR. The "judge" is the deterministic verifier chain, never a neural judge (a stronger, deterministic form
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

from aml_casework.contract import cited_transactions
from aml_casework.signoff import flatten_violations, run_verifiers

_log = logging.getLogger(__name__)

# How many times the drafter may regenerate against verifier feedback before the generator fails closed.
# Pinned: the loop is BOUNDED (no infinite regenerate), and a draft that cannot be made groundable within
# this many tries leaves the seam OPEN — never a filed SAR.
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


def _apply_draft(bundle: dict[str, Any], draft: Draft) -> dict[str, Any]:
    """Return a NEW bundle with the three seam fields filled from the draft (the input is not mutated)."""
    result = copy.deepcopy(bundle)
    record = result.setdefault("str_record", {})
    record["narrative"] = draft.narrative
    record["narrative_claims"] = draft.narrative_claims
    record.setdefault("completeness", {})["grounds_for_suspicion_narrative"] = True
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
