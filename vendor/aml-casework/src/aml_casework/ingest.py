"""Ingest/egress boundary (Phase 6) + the consume CLI (Phase 7).

The cross-pillar contract (signal-watch ``pillar-integration-contract.md`` §2) under-specifies the
transaction row as ``{txn_id, account_id, ...}``. The hand-authored casework fixtures filled the ``...``
with ``{kind, ts, counterparty_name}``; the REAL Pillar-1 emission instead carries
``{channel, direction, timestamp, counterparty_ref}``. ``contract.validate_bundle`` passes on BOTH (it
reads only ``txn_id``/``account_id``), but the grounding-replay assertions compute over
``kind``/``ts``/``counterparty_name`` — so a real bundle is reconciled HERE, at the boundary, NOT by
loosening the validator (a non-conforming bundle stays a surfaced violation).

The ingest adapter is IDEMPOTENT: it derives a field ONLY when absent, so casework fixtures (which already
carry the internal fields) pass through unchanged. It derives ONLY the ``kind`` values the assertions need
(``cash_deposit``, ``wire_out``); other channels (EMT/CARD/AFT/CHEQUE) are left unmapped. The source bundle
is never mutated (read-as-data; deepcopy).

Phase 7 adds the CLI (``python -m aml_casework.ingest <bundle> --out <signed> [--drafter stub|claude] …``):
a stable command-line entrypoint signal-watch's chain workbench subprocesses per case. It validates FIRST
(the schema gate), runs the Phase-6 chain with a runtime-chosen drafter, emits the signed STR, and prints a
one-line JSON summary so the caller can stage-stream without re-parsing the file. The boundary stays
subprocess + file-handoff — neither pillar imports the other.
"""

from __future__ import annotations

import argparse
import copy
import json
import sys
import urllib.error
from typing import Any

from aml_casework.contract import load_bundle, validate_bundle
from aml_casework.drafter_stub import RichDeterministicDrafter
from aml_casework.narrative_generator import Drafter, generate_narrative
from aml_casework.signoff import record_signoff

# (channel, direction) -> casework `kind`. Keyed on BOTH so a CASH withdrawal (CASH, DEBIT) is NOT a
# deposit. Only the kinds the replay assertions read are mapped; an unmapped row keeps no `kind`.
_CHANNEL_DIRECTION_TO_KIND: dict[tuple[str, str], str] = {
    ("CASH", "CREDIT"): "cash_deposit",
    ("WIRE", "DEBIT"): "wire_out",
}


def _canonicalize_txn(txn: dict[str, Any]) -> dict[str, Any]:
    """Enrich one real-shaped row with the internal fields the verifiers read — only where absent."""
    t = dict(txn)
    if t.get("ts") in (None, "") and t.get("timestamp"):
        t["ts"] = t["timestamp"]
    if t.get("counterparty_name") in (None, "") and t.get("counterparty_ref"):
        t["counterparty_name"] = t["counterparty_ref"]
    if t.get("kind") in (None, ""):
        channel, direction = t.get("channel"), t.get("direction")
        if isinstance(channel, str) and isinstance(direction, str):
            kind = _CHANNEL_DIRECTION_TO_KIND.get((channel, direction))
            if kind is not None:
                t["kind"] = kind
    return t


def canonicalize_transactions(bundle: dict[str, Any]) -> dict[str, Any]:
    """Return a deepcopy of ``bundle`` with every transaction reconciled to casework's internal shape.

    Idempotent: a bundle whose rows already carry ``kind``/``ts``/``counterparty_name`` is unchanged.
    """
    out = copy.deepcopy(bundle)
    out["transactions"] = [_canonicalize_txn(t) for t in out.get("transactions", [])]
    return out


def load_real_bundle(path: str) -> dict[str, Any]:
    """Load a REAL Pillar-1 evidence bundle as DATA and reconcile its transaction shape.

    Run ``contract.validate_bundle`` on the result BEFORE the chain (the schema gate): the added fields
    do not affect ``validate_bundle``, which reads only ``txn_id``/``account_id``.
    """
    return canonicalize_transactions(load_bundle(path))


def build_signed_sar(generated_bundle: dict[str, Any], signoff_record: dict[str, Any]) -> dict[str, Any]:
    """The generated (seam-filled) bundle plus a ``signoff`` block — the SIGNED STR artifact the
    cross-pillar harness (signal-watch ``e2e_chain_check --real``, B/C side) reads. Pure: returns a new
    object. The signoff block mirrors the keys the harness checks (``signed`` true + empty
    ``blocking_violations``), carrying the signer/ts/disposition for provenance."""
    sar = copy.deepcopy(generated_bundle)
    sar["signoff"] = {
        "signed": signoff_record["signed"],
        "signer": signoff_record["signer"],
        "ts": signoff_record["ts"],
        "disposition": signoff_record["disposition"],
        "blocking_violations": signoff_record["blocking_violations"],
    }
    # Phase 13: stamp the human signer's disposition into the FINTRAC STR action_taken block (when present),
    # so the signed STR records the filing decision. The contract validates filing_disposition == this.
    action = sar.get("str_record", {}).get("action_taken")
    if isinstance(action, dict):
        action["filing_disposition"] = signoff_record["disposition"]
    return sar


def emit_signed_sar(generated_bundle: dict[str, Any], signoff_record: dict[str, Any], path: str) -> dict[str, Any]:
    """Write the signed STR (see :func:`build_signed_sar`) to ``path`` as JSON. Returns the written object."""
    sar = build_signed_sar(generated_bundle, signoff_record)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(sar, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return sar


# --------------------------------------------------------------------------------------------------------
# The consume CLI (Phase 7) — `python -m aml_casework.ingest`. The chain-workbench entrypoint.
# --------------------------------------------------------------------------------------------------------


def _real_drafter_spec(name: str) -> tuple[Drafter, tuple[type[BaseException], ...]]:
    """Build a real (non-stub) drafter + its fail-soft fault tuple, importing the adapter — and its optional
    SDK — LAZILY so ``ingest`` carries no hard dependency on ``anthropic`` (nor on a live endpoint). Raises
    ``ImportError`` when an optional SDK is absent (the caller fail-softs to the stub).

    The fault tuple is the NAMED, drafter-specific surface the caller catches around the whole generate loop.
    It is deliberately NARROW so a downstream verifier error is never masked as a drafter fault: ``claude`` ->
    ``anthropic.AnthropicError`` (auth/SDK/network); ``openai`` -> the urllib transport classes (the adapter
    normalizes a malformed/garbage response to ``URLError``, so a generic ``KeyError``/``JSONDecodeError``
    never reaches here to be mistaken for a drafter fault)."""
    if name == "claude":
        import anthropic

        from aml_casework.drafter_claude import ClaudeDrafter

        return ClaudeDrafter(), (anthropic.AnthropicError,)
    if name == "openai":
        from aml_casework.drafter_openai import OpenAIDrafter

        return OpenAIDrafter(), (urllib.error.URLError, TimeoutError)
    if name == "opencode":
        from aml_casework.drafter_opencode import OpencodeDrafter

        # Same narrow surface as openai: the adapter normalizes serve/poll faults to URLError, and a
        # bound-exceeded / unparseable agent reply is a refusal (-> None), NOT a fault caught here.
        return OpencodeDrafter(), (urllib.error.URLError, TimeoutError)
    raise ValueError(f"unknown drafter: {name}")  # unreachable — argparse `choices` gates this


def _generate_with_drafter(bundle: dict[str, Any], drafter_name: str) -> tuple[dict[str, Any], str, str | None]:
    """Run the chosen drafter through the bounded generate loop. Returns
    ``(generated_bundle, drafter_effective, note)``.

    A real adapter (``claude``/``openai``) is FAIL-SOFT: an absent SDK (``ImportError``) or a drafter/transport
    fault (the drafter's NAMED fault tuple — see :func:`_real_drafter_spec`) falls back to the deterministic
    stub, reporting ``drafter_effective='stub'`` + a note. A live hiccup (missing key, unreachable endpoint,
    garbage response) degrades to a connected-but-stubbed result rather than breaking the chain. This is
    DISTINCT from ``generate_narrative``'s fail-CLOSED on a drafter that *refuses* (returns ``None``) — there
    the seam is left open and the record is ``needs_more_info``. Creds/endpoints are read by the adapter from
    the (server-side) environment, never passed here."""

    def _stub(note: str | None) -> tuple[dict[str, Any], str, str | None]:
        return generate_narrative(bundle, RichDeterministicDrafter(bundle)), "stub", note

    if drafter_name == "stub":
        return _stub(None)

    try:
        drafter, fail_soft_faults = _real_drafter_spec(drafter_name)
    except ImportError:
        return _stub(f"{drafter_name} drafter unavailable (SDK not installed); fell back to the deterministic stub")

    try:
        return generate_narrative(bundle, drafter), drafter_name, None
    except fail_soft_faults as exc:
        return _stub(f"{drafter_name} drafter error ({type(exc).__name__}); fell back to the deterministic stub")


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="python -m aml_casework.ingest",
        description="Consume a substrate evidence bundle -> a signed STR (the chain-workbench entrypoint).",
    )
    parser.add_argument("bundle", help="path to the substrate evidence bundle (JSON), read as data")
    parser.add_argument("--out", required=True, help="path to write the signed STR (JSON)")
    parser.add_argument(
        "--drafter",
        choices=("stub", "claude", "openai", "opencode"),
        default="stub",
        help="narrative drafter: 'stub' (deterministic, default), 'claude' (anthropic), 'openai' (any "
        "OpenAI-compatible /v1 server, e.g. a local llama-server), or 'opencode' (drive drafting through a "
        "running `opencode serve` agent loop). Live drafters fail-soft to the stub.",
    )
    parser.add_argument("--signer", default="Jane Examiner (SYNTHETIC)", help="the named human of record (synthetic)")
    parser.add_argument("--ts", default="2026-06-17T00:00:00", help="sign-off timestamp (ISO 8601)")
    parser.add_argument("--disposition", default="file", help="claimed disposition (default: file)")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    """Run the consume chain end-to-end. Exit 0 iff the record is signed with no blocking violations; a
    schema-invalid bundle fails loud at the validator (the violations to stderr) and never produces an STR.

    print() IS the legitimate channel here (this is the CLI boundary): a single JSON summary line to stdout
    (serve_chain.py reads it to stage-stream), validator violations to stderr. The no-print rule targets
    library logic, not this entrypoint."""
    args = _parse_args(argv)
    raw = load_bundle(args.bundle)
    violations = validate_bundle(raw)
    if violations:
        print(f"INVALID: {args.bundle} fails the contract ({len(violations)} violation(s)):", file=sys.stderr)  # noqa: T201
        for violation in violations:
            print(f"  - {violation}", file=sys.stderr)  # noqa: T201
        return 2

    bundle = canonicalize_transactions(raw)
    result, drafter_effective, note = _generate_with_drafter(bundle, args.drafter)
    record = record_signoff(result, args.signer, args.ts, claimed_disposition=args.disposition)
    emit_signed_sar(result, record, args.out)

    summary: dict[str, Any] = {
        "case_id": bundle.get("case_id"),
        "drafter": args.drafter,
        "drafter_effective": drafter_effective,
        "signed": record["signed"],
        "blocking_violations": record["blocking_violations"],
        "out": args.out,
    }
    if note:
        summary["note"] = note
    print(json.dumps(summary))  # noqa: T201  -- the single machine-readable stdout line serve_chain.py reads
    return 0 if record["signed"] and not record["blocking_violations"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
