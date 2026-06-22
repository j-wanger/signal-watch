"""OpencodeDrafter — drive the SAR/STR draft THROUGH opencode's agent runtime (the Drafter Protocol).

Unlike the ``/v1`` adapter (a raw model behind one POST), this hands the drafting task to a running
``opencode serve`` agent loop — which itself wires a LOCAL model via an ``@ai-sdk/openai-compatible``
provider whose model key MUST match the llama-server ``--alias``. casework only talks to ``opencode serve``
(``OPENCODE_SERVE_URL``); the provider block + llama-server config (``--jinja``, ctx >= 16384, 64K+ for real
agent loops) live opencode-side and are operator-provided (documented in the README run recipe).

Use ``opencode serve``, NEVER bare ``opencode run`` (a known headless-permission bug: "Session not found" /
write tools denied). The prompt -> response is ASYNC: create a session, send the shaped prompt, then POLL
(not SSE — simpler, zero-dependency, naturally boundable) for the assistant's final message. The loop is
BOUNDED (a poll-count cap ~= a time cap) so it can never hang the consume.

The six verifiers gate whatever it returns, so the adapter carries no business logic. Outcomes:
* a transport / connection fault (serve unreachable, non-2xx, garbage response) PROPAGATES as ``URLError``
  to ingest's fail-soft envelope -> the deterministic stub (it is infra, not a model refusal);
* the agent's final message is not a valid Draft, OR the poll bound is exceeded -> ``None`` (fail-closed
  refuse — the seam stays open, the chain reports ``needs_more_info``, never a faked STR).

Testing split (so the verifiable part is CI-tested and the unverified part is honestly isolated): the
ORCHESTRATION runs against an injectable ``_ServeClient`` seam (CI stubs it offline). The default
``_HttpServeClient`` encodes the ASSUMED ``opencode serve`` OpenAPI shape and is exercised ONLY by the
@integration demo against a live server (``# pragma: no cover``) — verify/adjust it against the real schema
at ``{OPENCODE_SERVE_URL}/doc`` in that run.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from typing import Any, Protocol

from aml_casework.drafter_prompts import _system_prompt, build_user_prompt, parse_draft_json
from aml_casework.narrative_generator import Draft, GenerationContext

# Bound the agent loop: at most _MAX_POLLS polls spaced _POLL_INTERVAL_S apart (~= the wall-clock cap), each
# HTTP call capped at _TIMEOUT_S. Exceeding the bound -> None (fail-closed refuse), never a hang.
_MAX_POLLS = 120
_POLL_INTERVAL_S = 1.0
_TIMEOUT_S = 30.0

_JSON_ONLY_INSTRUCTION = (
    'Return ONLY a single JSON object of the form {"narrative": str, "narrative_claims": '
    '[{"text": str, "cites": [str], "stance": str}]} as your FINAL message — no prose, no code fences, '
    "nothing else."
)


class _ServeClient(Protocol):
    """The opencode-serve seam the orchestration drives. ``create_session``/``send_prompt`` raise a
    ``urllib`` error on a transport fault (propagates to ingest's fail-soft); ``poll_assistant_text``
    returns the assistant's COMPLETED final message text, or ``None`` while the agent is still working."""

    def create_session(self) -> str: ...

    def send_prompt(self, session_id: str, prompt: str, model: str | None) -> None: ...

    def poll_assistant_text(self, session_id: str) -> str | None: ...


class OpencodeDrafter:
    """Drives ``opencode serve`` over an injectable ``_ServeClient`` (the default talks real HTTP). Constructs
    without a live server — env read lazily in ``draft`` — so the prompt-shaping + orchestration test offline."""

    def __init__(
        self,
        serve_url: str | None = None,
        model: str | None = None,
        client: _ServeClient | None = None,
        max_polls: int = _MAX_POLLS,
        poll_interval_s: float = _POLL_INTERVAL_S,
    ) -> None:
        self._serve_url = serve_url
        self._model = model
        self._client = client
        self._max_polls = max_polls
        self._poll_interval_s = poll_interval_s

    def draft(self, context: GenerationContext, feedback: list[str] | None = None) -> Draft | None:
        serve_url = (self._serve_url or os.environ.get("OPENCODE_SERVE_URL") or "").rstrip("/")
        if not serve_url and self._client is None:
            # No serve configured — a transport-class problem, not a model refusal → ingest fail-softs.
            raise urllib.error.URLError("OPENCODE_SERVE_URL not set")
        model = self._model or os.environ.get("OPENCODE_MODEL")
        client = self._client or _HttpServeClient(serve_url, _TIMEOUT_S)

        prompt = "\n\n".join([_system_prompt(), build_user_prompt(context, feedback), _JSON_ONLY_INSTRUCTION])
        # create_session / send_prompt transport faults propagate (→ ingest fail-soft → stub).
        session_id = client.create_session()
        client.send_prompt(session_id, prompt, model)

        for _ in range(self._max_polls):
            final = client.poll_assistant_text(session_id)
            if final is not None:
                # The agent emitted a final message; the model's CONTENT being an invalid Draft IS a refusal.
                return parse_draft_json(final)
            time.sleep(self._poll_interval_s)
        # Bound exceeded — the agent did not deliver a final message in time → fail-closed refuse.
        return None


class _HttpServeClient:  # pragma: no cover
    """Stdlib-urllib client for the ASSUMED ``opencode serve`` OpenAPI shape. Exercised ONLY by the
    @integration demo against a live server — NOT by CI. Verify/adjust the endpoints + payloads against the
    real schema at ``{serve_url}/doc`` in that run; a transport / malformed-response fault surfaces as
    ``URLError`` so ingest's fail-soft owns it."""

    def __init__(self, serve_url: str, timeout_s: float) -> None:
        self._serve_url = serve_url
        self._timeout_s = timeout_s

    def _request(self, method: str, path: str, body: dict[str, Any] | None) -> Any:
        data = json.dumps(body).encode() if body is not None else None
        headers = {"Content-Type": "application/json"} if data is not None else {}
        # S310: the URL is operator-provided config (OPENCODE_SERVE_URL) and we hit fixed serve endpoints.
        request = urllib.request.Request(f"{self._serve_url}{path}", data=data, headers=headers, method=method)  # noqa: S310
        try:
            with urllib.request.urlopen(request, timeout=self._timeout_s) as response:  # noqa: S310
                raw: bytes = response.read()
            return json.loads(raw) if raw else None
        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            raise urllib.error.URLError(f"malformed opencode serve response: {exc}") from exc

    def create_session(self) -> str:
        session = self._request("POST", "/session", {})
        try:
            return str(session["id"])
        except (KeyError, TypeError) as exc:
            raise urllib.error.URLError(f"opencode serve session response missing id: {exc}") from exc

    def send_prompt(self, session_id: str, prompt: str, model: str | None) -> None:
        body: dict[str, Any] = {"parts": [{"type": "text", "text": prompt}]}
        if model:
            body["model"] = model  # ASSUMED field name — verify against the real OpenAPI
        self._request("POST", f"/session/{session_id}/message", body)

    def poll_assistant_text(self, session_id: str) -> str | None:
        messages = self._request("GET", f"/session/{session_id}/message", None)
        if not isinstance(messages, list):
            return None
        for message in reversed(messages):
            if isinstance(message, dict) and message.get("role") == "assistant" and message.get("completed"):
                parts = message.get("parts", [])
                text = "".join(p.get("text", "") for p in parts if isinstance(p, dict) and p.get("type") == "text")
                return text or None
        return None
