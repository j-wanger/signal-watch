"""OpenAIDrafter — a thin OpenAI-standard ``/v1/chat/completions`` adapter (the Drafter Protocol).

Lets any OpenAI-compatible server — crucially a LOCAL model (llama-server, LM Studio, Ollama, vLLM) — draft
the SAR/STR narrative. Reuses the grounding-aware prompt + the ``_DraftSchema`` shape from ``drafter_prompts``
(no anthropic dependency). Stdlib ``urllib`` only — a single non-streaming POST, no new dependency. The six
verifiers gate whatever it returns, so the adapter carries no business logic: it shapes the request, parses
tolerantly, and refuses (``None``) on a malformed draft.

Tolerant parse, NO dependency on strict json_schema (the optional ``stance`` field breaks strict mode; local
servers vary): the ``response_format`` json_schema is best-effort. TWO parse stages:

* a transport / envelope fault (connection, non-2xx, non-JSON body, malformed envelope) PROPAGATES to
  ``ingest``'s fail-soft envelope → the deterministic stub (it is a server/transport problem, not a model
  refusal);
* a content-refusal (the model's message is not a valid Draft) → ``None`` (fail-closed refuse — the seam
  stays open, the chain reports ``needs_more_info``, never a faked SAR).

The optional ``OPENAI_API_KEY`` is read from the (server-side) env at runtime, never logged. A local model
needs no key.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any, Protocol

from aml_casework.drafter_prompts import _DraftSchema, _system_prompt, build_user_prompt, parse_draft_json
from aml_casework.narrative_generator import Draft, GenerationContext

# A local model draft can be slow; bound the whole request so a stalled server never hangs the consume.
_TIMEOUT_S = 60.0


class _Post(Protocol):
    """The injectable HTTP transport: POST ``body`` to ``url``, return the response bytes, raise a
    ``urllib`` error on a transport / non-2xx fault. Default is stdlib urllib; the offline test injects a
    stub (no network)."""

    def __call__(self, url: str, body: bytes, headers: dict[str, str], timeout: float) -> bytes: ...


def _urlopen_post(url: str, body: bytes, headers: dict[str, str], timeout: float) -> bytes:  # pragma: no cover
    """Stdlib-urllib POST — the default transport, exercised ONLY against a live server (CI injects a stub
    ``post``). Raises ``urllib.error.HTTPError`` on a non-2xx response and ``urllib.error.URLError`` on a
    connection failure; both propagate to ingest's fail-soft envelope."""
    # S310: the URL is operator-provided config (OPENAI_BASE_URL) and we POST to a fixed chat endpoint.
    request = urllib.request.Request(url, data=body, headers=headers, method="POST")  # noqa: S310
    with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310
        data: bytes = response.read()
    return data


def _message_content(envelope: dict[str, Any]) -> str:
    """Pull the assistant message text from an OpenAI ``/v1/chat/completions`` response. A malformed envelope
    (no ``choices`` / wrong shape) raises ``KeyError`` — a server fault that propagates to ingest's fail-soft
    (it is NOT a model refusal). The model's CONTENT is parsed downstream by ``parse_draft_json``."""
    choices = envelope["choices"]
    if not choices:
        raise KeyError("openai response has no choices")
    content = choices[0]["message"]["content"]
    if not isinstance(content, str):
        raise KeyError("openai response message content is not a string")
    return content


class OpenAIDrafter:
    """Thin ``/v1`` adapter. Constructs without creds (env read lazily in ``draft``); the transport is
    injectable so the prompt-shaping + the parse are testable offline."""

    def __init__(
        self,
        base_url: str | None = None,
        model: str | None = None,
        api_key: str | None = None,
        post: _Post | None = None,
    ) -> None:
        self._base_url = base_url
        self._model = model
        self._api_key = api_key
        self._post: _Post = post or _urlopen_post

    def draft(self, context: GenerationContext, feedback: list[str] | None = None) -> Draft | None:
        base_url = (self._base_url or os.environ.get("OPENAI_BASE_URL") or "").rstrip("/")
        if not base_url:
            # No endpoint configured — a transport-class problem, not a model refusal → ingest fail-softs.
            raise urllib.error.URLError("OPENAI_BASE_URL not set")
        model = self._model or os.environ.get("OPENAI_MODEL") or "local-model"
        api_key = self._api_key or os.environ.get("OPENAI_API_KEY")

        payload: dict[str, Any] = {
            "model": model,
            "messages": [
                {"role": "system", "content": _system_prompt()},
                {"role": "user", "content": build_user_prompt(context, feedback)},
            ],
            # Best-effort structured output; strict=False because the optional `stance` field breaks strict
            # mode and local servers vary. parse_draft_json refuses cleanly if the model ignores it.
            "response_format": {
                "type": "json_schema",
                "json_schema": {"name": "sar_draft", "schema": _DraftSchema.model_json_schema(), "strict": False},
            },
        }
        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        # Transport faults (URLError/HTTPError/TimeoutError) from the POST propagate as-is.
        raw = self._post(f"{base_url}/chat/completions", json.dumps(payload).encode(), headers, _TIMEOUT_S)
        try:
            content = _message_content(json.loads(raw))
        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            # A 2xx-but-unusable response (non-JSON / no choices / wrong shape) is a transport-class fault,
            # NOT a model refusal — surface it as URLError so ingest's NARROW (URLError, TimeoutError)
            # fail-soft catches it without ever masking a downstream verifier error.
            raise urllib.error.URLError(f"malformed openai response: {exc}") from exc
        # The model's CONTENT being an invalid Draft IS a refusal → None (fail-closed, the seam stays open).
        return parse_draft_json(content)
