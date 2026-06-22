"""Narrative-grounding verifier (Class-G, deterministic) — the 6th gate.

The free-text ``str_record.narrative`` is the artifact a human signs and files, yet no other verifier
reads it: ``citation`` checks the ``narrative_claims`` cites, ``completeness`` checks the seam flag, and
``corpus_grounding`` checks the alert flags. Once the narrative is LLM-drafted, that free text can assert
ungrounded specifics — a wrong figure, a phantom date, an invented party — and pass every other gate.
This verifier closes that hole by ATOM-GROUNDING: every grounding-bearing atom in the prose must resolve
to the cited evidence, or the draft is not groundable (grounded-or-dropped, extended to the prose).

The atoms a draft most easily hallucinates: account/txn/signal ids, monetary amounts (including ranges
and the regulatory constants an STR/SAR legitimately cites, e.g. the CTR threshold), dates, and named parties
(the subject and cited counterparties). Free connective language ("consistent with", "the account")
carries no atom and is correctly out of scope. The check is regex + membership/substring under a copied
``normalize`` — never an NLP/neural judge (that would re-introduce the non-determinism the gate chain
exists to fence).

Amounts in transactions are integer ``amount_cents``; the prose states dollars (= ``amount_cents`` / 100).

Returns ``list[str]`` violations (empty == every atom grounds), mirroring the other verifiers.
"""

from __future__ import annotations

import re
from typing import Any

from aml_casework.contract import cited_transactions


def normalize(s: str) -> str:
    """Lowercase + whitespace-collapse so grounding is robust to casing/spacing.

    Deliberate 3-line mirror of the corpus ``normalize`` (see ``corpus_grounding.normalize`` /
    signal-watch ``derive_signals.normalize``). NOT imported — the read-as-data / don't-import-engine
    contract; carried here so this verifier has no engine dependency."""
    return " ".join(s.lower().split())


# A prose dollar amount grounds when it equals a cited transaction's amount_cents/100 within this
# tolerance. A range "$X-$Y" is two separate matches: it grounds iff each endpoint grounds — endpoint
# resolution IS min/max reconciliation, so no special range machinery is needed.
_AMOUNT_TOLERANCE = 0.01  # dollars

# Account/txn ids: a single leading letter, a dash, then >=4 digits (A-90001, L-90000001, A-90042).
# Scoped this tightly (not [A-Za-z]+-\d+) so corpus tokens like "fin-2026" are not mistaken for ids.
_ID_RE = re.compile(r"\b[A-Za-z]-\d{4,}\b")
# Signal ids carry the corpus ":IND-<n>" suffix (fin-2026-alert001:IND-11).
_SIGNAL_RE = re.compile(r"\b[\w.-]+:IND-\d+\b")
# Monetary amounts: a "$" then digits/commas, optional decimal. Suffix multipliers (M/K) are an
# approximation concern handled in a later increment, so they are deliberately not consumed here.
_AMOUNT_RE = re.compile(r"\$\s?(\d[\d,]*(?:\.\d+)?)")
# ISO dates (the transaction ``ts`` date prefix).
_DATE_RE = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")

# Regulatory thresholds an STR/SAR narrative legitimately cites that are NOT transaction amounts — they
# ground to published guidance, not bundle data. Keep small + documented; extend only with provenance.
# The $10,000 threshold is dual-provenance: the US CTR filing threshold (31 CFR 1010.311 / FinCEN) AND,
# in Canadian dollars, the PCMLTFA Large Cash Transaction Report (LCTR) threshold FINTRAC enforces — so a
# FINTRAC STR's structuring grounds may cite it on the same basis. (The KEY 10000.0 is what grounds; this
# value string is documentation only.)
REGULATORY_CONSTANTS: dict[float, str] = {
    10000.0: "CTR/LCTR reporting threshold (31 CFR 1010.311 / FinCEN; CAD 10,000 PCMLTFA LCTR / FINTRAC)",
}

# Named-party spans: single-quoted entities ('Crescent Generic Trading FZE') and maximal runs of >=2
# consecutive Title-Case word tokens ("Northwind Trading Co."). A single capitalized word (a sentence
# start, "Account", an acronym) is NOT a party. Each candidate must substring-ground to a known party.
# The trade is a possible false-positive on a capitalized non-party phrase — caught safely by the
# regenerate loop (fail-closed), never a false-negative that lets an invented party through.
_QUOTED_RE = re.compile(r"'([^']+)'")
_TITLE_TOKEN_RE = re.compile(r"^[A-Z][A-Za-z]*\.?$")


def _resolvable_ids(bundle: dict[str, Any]) -> set[str]:
    """The id-space a prose id may reference: every transaction txn_id, subject account_id, and grounded
    alert signal_id. Mirrors the citation verifier's evidence id-space, plus account ids."""
    txn_ids = {t.get("txn_id") for t in bundle.get("transactions", [])}
    account_ids = set(bundle.get("subject", {}).get("account_ids", []))
    signal_ids = {a.get("grounding", {}).get("signal_id") for a in bundle.get("alerts", []) if a.get("grounding")}
    return {x for x in (txn_ids | account_ids | signal_ids) if x is not None}


def _cited_amounts_dollars(bundle: dict[str, Any]) -> list[float]:
    """Cited transaction amounts in dollars (amount_cents / 100)."""
    return [t["amount_cents"] / 100 for t in cited_transactions(bundle) if isinstance(t.get("amount_cents"), int)]


def _cited_dates(bundle: dict[str, Any]) -> set[str]:
    """The ISO date prefixes of cited transaction timestamps."""
    return {t["ts"][:10] for t in cited_transactions(bundle) if isinstance(t.get("ts"), str)}


def _known_parties(bundle: dict[str, Any]) -> set[str]:
    """The named parties a prose entity may reference: the subject and every transaction counterparty,
    normalized. Both carry a "(SYNTHETIC)" suffix, so grounding is substring-under-normalize.

    Deliberately NOT scoped to cited transactions (unlike amounts/dates): a broader known-party set is
    strictly more permissive, so it never false-NEGATIVES an invented party — tightening this to cited
    counterparties would not close any hole, only risk rejecting a real party. Keep it broad."""
    names = {bundle.get("subject", {}).get("name")}
    names |= {t.get("counterparty_name") for t in bundle.get("transactions", [])}
    return {normalize(n) for n in names if n}


def _entity_candidates(narrative: str) -> set[str]:
    """Candidate named-party spans: single-quoted entities + maximal >=2-token Title-Case runs.

    Quoted spans are scanned first and then removed, so a Title-Case run is never a fragment of a quoted
    name. A quoted span counts only if it contains an uppercase letter (entity-like, not a stray clause)."""
    candidates: set[str] = set()
    for span in _QUOTED_RE.findall(narrative):
        if any(c.isupper() for c in span):
            candidates.add(span.strip())
    run: list[str] = []
    for token in _QUOTED_RE.sub(" ", narrative).split():
        if _TITLE_TOKEN_RE.match(token):
            run.append(token)
            continue
        if len(run) >= 2:
            candidates.add(" ".join(run))
        run = []
    if len(run) >= 2:
        candidates.add(" ".join(run))
    return candidates


def verify_narrative_grounding(bundle: dict[str, Any]) -> list[str]:
    """Flag every grounding-bearing prose atom that resolves to no cited evidence.

    An OPEN seam (no narrative) has nothing to ground -> no violation. Otherwise every id, amount, date,
    and named party in the prose must resolve to the cited evidence (ids/amounts/dates) or a known party;
    amounts may also resolve to a documented regulatory constant."""
    narrative = bundle.get("str_record", {}).get("narrative")
    if not narrative:
        return []

    violations: list[str] = []

    resolvable = _resolvable_ids(bundle)
    for token in _SIGNAL_RE.findall(narrative) + _ID_RE.findall(narrative):
        if token not in resolvable:
            violations.append(
                f"narrative: id '{token}' resolves to no cited signal, transaction, or account (ungrounded)"
            )

    groundable_amounts = _cited_amounts_dollars(bundle) + list(REGULATORY_CONSTANTS)
    for raw in _AMOUNT_RE.findall(narrative):
        value = float(raw.replace(",", ""))
        if not any(abs(value - amount) <= _AMOUNT_TOLERANCE for amount in groundable_amounts):
            violations.append(
                f"narrative: amount '${raw}' grounds to no cited transaction amount or regulatory constant"
            )

    dates = _cited_dates(bundle)
    for date in _DATE_RE.findall(narrative):
        if date not in dates:
            violations.append(f"narrative: date '{date}' is absent from cited transaction dates")

    parties = _known_parties(bundle)
    for candidate in sorted(_entity_candidates(narrative)):
        norm = normalize(candidate)
        # Empty-guard (the Phase-3 substring-trap): "" is a substring of every string, so a degenerate
        # candidate would ground vacuously. Fail closed — an empty/uncheckable candidate is a violation,
        # never a silent pass. Non-empty candidates ground by substring membership in a known party.
        if not norm or not any(norm in known for known in parties):
            violations.append(
                f"narrative: named party '{candidate}' resolves to no subject or counterparty (ungrounded)"
            )

    return violations
