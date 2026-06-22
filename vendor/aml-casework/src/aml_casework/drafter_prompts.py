"""Shared SAR/STR prompt-shaping — the grounding-aware prompt, the structured-output schema, and the
tolerant draft-parse helpers shared by every real-model adapter.

Extracted from ``drafter_claude`` (Phase 9) so EVERY real-model adapter — ``ClaudeDrafter`` (anthropic),
``OpenAIDrafter`` (the ``/v1`` adapter), ``OpencodeDrafter`` (the agent loop) — reuses the EXACT same
grounding-aware prompt, the same ``_DraftSchema`` structured shape, and the same Draft-construction WITHOUT
depending on the anthropic SDK. This module builds strings + a pydantic schema only: it imports no model
SDK, so the openai/opencode adapters stay import-light. ``drafter_claude`` re-exports the prompt symbols, so
its public surface is unchanged.

The shape (``_DraftSchema``/``_Claim``) is plain pydantic — NOT anthropic-specific — so it serializes to a
JSON Schema (``_DraftSchema.model_json_schema()``) any OpenAI-compatible ``response_format`` can consume. The
six deterministic verifiers gate whatever a drafter returns, so the prompt only has to make grounded output
*likely*; it is never the oracle.
"""

from __future__ import annotations

from pydantic import BaseModel, ValidationError

from aml_casework.contract import STR_REQUIRED_ELEMENTS
from aml_casework.narrative_generator import Draft, GenerationContext


class _Claim(BaseModel):
    """Structured-output shape for one cited claim (mirrors the bundle's narrative_claims entry)."""

    text: str
    cites: list[str]
    stance: str | None = None


class _DraftSchema(BaseModel):
    """Structured-output shape the model must return: the prose plus the cited claims."""

    narrative: str
    narrative_claims: list[_Claim]


def _schema_to_draft(parsed: _DraftSchema) -> Draft:
    """Convert a validated ``_DraftSchema`` into the ``Draft`` the seam expects (drops ``stance=None``).

    Shared by every adapter so the schema→Draft mapping lives once, in the module that owns the schema."""
    return Draft(
        narrative=parsed.narrative,
        narrative_claims=[claim.model_dump(exclude_none=True) for claim in parsed.narrative_claims],
    )


def parse_draft_json(content: str) -> Draft | None:
    """Tolerantly parse a model's structured-output STRING into a ``Draft``; return ``None`` on any
    malformed/missing field (fail-closed refuse — the seam stays open, never a faked SAR).

    Used by the openai + opencode adapters, which receive the structured output as a string. (``ClaudeDrafter``
    gets an already-parsed object from ``messages.parse`` and calls ``_schema_to_draft`` directly.) NO
    dependency on strict json_schema enforcement: pydantic validation is the parse, and a malformed draft
    simply refuses. The six verifiers gate the result regardless — this only has to refuse cleanly."""
    try:
        parsed = _DraftSchema.model_validate_json(content)
    except ValidationError:
        return None
    return _schema_to_draft(parsed)


def _system_prompt() -> str:
    return (
        "You draft SAR/STR narratives for SYNTHETIC anti-money-laundering cases. You output a structured set "
        "of cited claims plus rendered prose. Every claim cites real evidence by id; every grounding-bearing "
        "fact in the prose (monetary amounts, dates, account/txn/signal ids, named parties) must trace to the "
        "provided evidence, or be the stated CTR $10,000 regulatory threshold. CONNECT each cited indicator to "
        "the specific suspicion — never merely restate transaction detail. You NEVER weigh which side wins or "
        "decide whether to file; that is the human signer's act. A deterministic verifier chain checks your "
        "output and rejects anything ungrounded, so emit only grounded, cite-resolvable claims."
    )


def build_user_prompt(context: GenerationContext, feedback: list[str] | None = None) -> str:
    """Shape the grounding surface into the prompt: the subject, the cite-able evidence (ids + the amounts/
    dates/parties that ground the prose), the required-elements checklist, and — on a regenerate — the prior
    attempt's verifier violations. Pure + testable without a network call (context shaping is the lever)."""
    subject = context.subject
    lines: list[str] = [
        f"SUBJECT: {subject.get('name')} (customer_id {subject.get('customer_id')}); "
        f"accounts {subject.get('account_ids')}",
        "",
        "CITE-ABLE EVIDENCE — claims may cite ONLY these ids, and every amount/date/party in your prose "
        "must come from these rows (or the CTR $10,000 threshold):",
        f"  typology signals (cite one to ground a suspicion): {context.signal_ids}",
    ]
    for txn in context.cited_transactions:
        cents = txn.get("amount_cents")
        amount = f"${cents / 100:,.2f}" if isinstance(cents, int) else "?"
        row = f"  txn {txn.get('txn_id')}: {txn.get('kind')} {amount} on {str(txn.get('ts'))[:10]}"
        if txn.get("counterparty_name"):
            row += f" to '{txn.get('counterparty_name')}'"
        if txn.get("exculpatory") is True:
            row += f"  [EXCULPATORY counter-evidence — retain it: {txn.get('memo', '')}]"
        lines.append(row)
    if any(txn.get("exculpatory") is True for txn in context.cited_transactions):
        lines += [
            "",
            "RETAIN BOTH SIDES: the evidence above includes EXCULPATORY counter-evidence. You MUST emit an "
            "exculpatory-stance claim that cites each such transaction and present both readings. NEVER "
            "decide which side wins — the deterministic gate rejects a narrative that drops retained "
            "counter-evidence (conflict-both-kept).",
        ]
    lines += [
        "",
        "REQUIRED ELEMENTS the filing must support: " + ", ".join(STR_REQUIRED_ELEMENTS),
        "",
        "Write the SAR narrative. Emit narrative_claims (each {text, cites:[signal_id|txn_id], stance}) that "
        "connect each cited indicator to the specific suspicion; tag stance inculpatory/exculpatory and "
        "retain any counter-evidence. Also write the prose `narrative`; every grounding-bearing fact in it "
        "must appear in the evidence above. The file/no-file judgment stays with the human signer.",
    ]
    if feedback:
        lines += ["", "Your previous draft FAILED these deterministic checks — fix every one:"]
        lines += [f"  - {violation}" for violation in feedback]
    return "\n".join(lines)
