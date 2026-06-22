"""ClaudeDrafter — the real neural step (a thin anthropic-SDK adapter implementing the Drafter Protocol).

Lives in its own module so the generator core (``narrative_generator``) stays import-light: only this file
depends on ``anthropic``, and it is exercised ONLY by the network-marked integration test — the
deterministic stub drafters drive CI. The adapter is deliberately thin: shape a grounding-aware prompt,
call the model with structured output, hand back a ``Draft``. The six-verifier chain (and the bounded
regenerate loop) gate whatever it returns, so the adapter carries no business logic of its own.

The grounding-aware prompt, the structured-output schema, and the schema->Draft mapping (``_system_prompt``,
``build_user_prompt``, ``_DraftSchema``/``_Claim``, ``_schema_to_draft``) live in ``drafter_prompts``
(anthropic-free) so the openai/opencode adapters reuse them without the anthropic SDK; the prompt symbols
are re-exported here so this module's public surface is unchanged.

Model: ``claude-opus-4-8`` (quality-sensitive drafting). NO ``temperature`` — it is removed on Opus 4.8
(passing it 400s), and determinism is irrelevant here anyway: the gate, not the model, is the oracle.
"""

from __future__ import annotations

import os
from collections.abc import Mapping

import anthropic
from anthropic.types import MessageParam

# Re-export the prompt-shaping surface (explicit `as` re-export — drafter_claude's public surface stays
# byte-identical so test_strata_generation / test_oauth_probe keep importing these from here; the canonical
# home is drafter_prompts, which is anthropic-free for the openai/opencode adapters).
from aml_casework.drafter_prompts import _DraftSchema as _DraftSchema
from aml_casework.drafter_prompts import _schema_to_draft
from aml_casework.drafter_prompts import _system_prompt as _system_prompt
from aml_casework.drafter_prompts import build_user_prompt as build_user_prompt
from aml_casework.narrative_generator import Draft, GenerationContext

_MODEL = "claude-opus-4-8"
_MAX_TOKENS = 8000


def _oauth_headers(env: Mapping[str, str]) -> dict[str, str]:
    """The beta header ``/v1/messages`` requires when authenticating with the Claude subscription via OAuth
    (``ANTHROPIC_AUTH_TOKEN`` Bearer auth) — empty for the API-key path, which is left byte-unchanged.

    OAuth needs three things (Anthropic SDK/CLI reference): the token in ``ANTHROPIC_AUTH_TOKEN`` (the SDK
    reads it natively and sends ``Authorization: Bearer``, not ``x-api-key``), the
    ``anthropic-beta: oauth-2025-04-20`` header (the beta-header requirement is endpoint-dependent —
    ``/v1/messages`` 401s without it), and ``ANTHROPIC_API_KEY`` UNSET (if both are set the SDK sends both
    and the API rejects). So the header is added ONLY for the pure-OAuth case; with an API key present (or no
    token) we stay on the unchanged API-key path."""
    if env.get("ANTHROPIC_AUTH_TOKEN") and not env.get("ANTHROPIC_API_KEY"):
        return {"anthropic-beta": "oauth-2025-04-20"}
    return {}


def _build_client() -> anthropic.Anthropic:
    """The lazy SDK client, OAuth-aware. Additive: with no ``ANTHROPIC_AUTH_TOKEN`` set (CI) the default
    headers are empty — equivalent to a bare ``anthropic.Anthropic()``. The token is read from the (server-
    side) environment by the SDK; it is never passed here and never logged."""
    return anthropic.Anthropic(default_headers=_oauth_headers(os.environ))


class ClaudeDrafter:
    """Thin anthropic-SDK adapter. The SDK client is created lazily (only in ``draft``), so the drafter
    constructs without credentials — the prompt-shaping is testable offline; only ``draft`` needs network."""

    def __init__(self, client: anthropic.Anthropic | None = None, model: str = _MODEL) -> None:
        self._client = client
        self._model = model

    def draft(self, context: GenerationContext, feedback: list[str] | None = None) -> Draft | None:
        client = self._client or _build_client()
        messages: list[MessageParam] = [{"role": "user", "content": build_user_prompt(context, feedback)}]
        response = client.messages.parse(
            model=self._model,
            max_tokens=_MAX_TOKENS,
            system=_system_prompt(),
            messages=messages,
            output_format=_DraftSchema,
        )
        parsed = response.parsed_output
        if parsed is None:
            return None
        return _schema_to_draft(parsed)
