"""Grounding-replay verifier (Class-G, deterministic).

Each cited signal must be independently re-derivable over its cited data. Per assumption A2 (dev-plan
Phase 1), "re-derivable" is a per-capability PATTERN-ASSERTION over the cited transactions — does the
cited evidence exhibit the indicator's red-flag pattern? — NOT a re-run of Pillar 1's detector (DESIGN
forbids importing ``aml_substrate``). Dispatch is fail-closed: an alert whose capability has no
registered assertion is a violation (grounded-or-dropped).

Two grounding classes mirror Pillar 1's Detector/ScreeningDetector split, and the two dispatch tables
carry DIFFERENT signatures. ``_ASSERTIONS`` holds the replay-reproducible transaction-monitoring signals
(C2-C5, C15) — a per-capability PATTERN re-derivation over the cited transactions ALONE (``Assertion`` =
``(alert, cited_txns)``). ``_SCREENING`` holds context-relative SCREENING signals whose detection is NOT
replay-reproducible from one account's cited records; each ``ScreeningAssertion`` =
``(alert, cited_txns, party)`` ALSO receives the alert's resolved PartyView (mirroring Pillar 1's
ScreeningDetector(txns, accounts, parties)). The replay assertions never see — and never depend on —
party state. A screening signal grounds on a re-derivable floor/ratio PLUS its recorded screening lineage
(``alert.rule``, corpus-resolved by ``verify_corpus_grounding``), never a faked replay:
  - C7 (Phase 10, peer/business-activity anomaly) grounds on the cited CREDIT inflow vs the absolute $25k
    floor; its peer-cohort outlier core is NAMED as lineage (the cohort baseline is absent from one
    account's records). ``party`` is unread.
  - C8 (Phase 11, income/activity mismatch) grounds on the cited inflow vs the resolved party's RECORDED
    declared volume (``expected_monthly_volume_cents`` in the v0.2 ``parties`` block) — re-derivable ratio
    + the $25k floor. The party is resolved by ``_party_by_account`` (customer_id IS party_id); a missing
    party / declared baseline fails closed.
  - C14 (Phase 12, KYC-integrity) is TXN-LESS — a PARTY-LEAF alert (``txn_ids=()`` + a ``party_ref``, the
    leaf-XOR contract rule). It grounds on the resolved party's static KYC STATE alone (no transaction to
    replay): it re-derives the screened DEFECT (substrate ``kyc_integrity._kyc_defect``, copied). The party
    resolves via ``party_ref`` (reference-by-path, ``_party_by_ref``); a non-resolving ref / missing
    cdd_level pivot / clean state fails closed.
C26 (behavioral screening) is NOT registered — it fails closed (an ungroundable capability is a violation;
honest NULL, not a coverage gain). It needs the C3 counterparty-ref gap closed in a later phase.

The assertions read casework's internal transaction shape (``kind``/``ts``/``counterparty_name`` for the
kind-based checks, ``direction``/``amount_cents`` for the flow-based checks). A REAL Pillar-1 bundle is
reconciled to that shape at the boundary by ``ingest.canonicalize_transactions`` BEFORE replay.

Phase-6 reconciliation (the first real ingest of a multi-typology bundle): C4 was broadened from an
over-narrow (9000,10000) band to the canonical sub-$10k-aggregating-to-≥$10k structuring form (the real
detector fires on sub-$10k smurfing, deposits well under $9k); C15 gained a throughput / low-net-retention
sub-signal ALONGSIDE the generic-"trading company" name match (the real shell conduit carries no
counterparty names); C2/C3/C5 were registered (see ``_assert_c2_passthrough`` / ``_assert_c3_funnel_fan``
/ ``_assert_c5_cash_placement``).

Returns ``list[str]`` violations (empty == replays), mirroring ``contract.validate_bundle``.

Run dependency-free via the test runner: ``python3 tests/test_grounding_replay.py``.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime, timedelta
from typing import Any

# --- C4 structuring (sub-CTR): >=N cash deposits, each under the $10,000 CTR-filing threshold,
#     AGGREGATING to >=$10,000 within a short window — the canonical FinCEN structuring red flag (a
#     reportable sum split into sub-threshold cash deposits). Reconciled in Phase 6 from an over-narrow
#     (9000,10000)-dollar band, which rejected the real detector's sub-$10k smurfing (deposits ~$7-8k).
#     Amounts are in cents. ---
_CTR_THRESHOLD_CENTS = 1_000_000  # $10,000 — the CTR-filing threshold the structuring stays under
_MIN_STRUCTURING_COUNT = 3
_STRUCTURING_WINDOW = timedelta(days=7)

# --- C5 cash-placement: >=N cash deposits within a short window (physical cash entering the banking
#     system — the placement stage). Distinct from C4: placement does not require sub-threshold amounts
#     or an aggregate target; it is the cash-intensity red flag. ---
_MIN_PLACEMENT_COUNT = 3
_PLACEMENT_WINDOW = timedelta(days=7)

# --- C2 pass-through: total outflow >= this fraction of total inflow, with both present inside a short
#     window — the layering-conduit pattern. This MIRRORS Pillar 1's stated rule ("forwarded out/in
#     >= 80% within 72h", per alert.rule); it deliberately does NOT impose an inflow-before-outflow
#     ordering the detector does not assert (the A2 contract is to re-derive the detector's pattern over
#     the cited evidence, not to exceed it). The window bounds the span of the cited inflow+outflow set. ---
_PASSTHROUGH_MIN_FRACTION = 0.80
_PASSTHROUGH_WINDOW = timedelta(hours=72)

# --- C3 funnel/fan: >=N outflow transactions within a short window. NOTE (Phase 6, documented honesty
#     gap): the detector's rule is "fan-out to N DISTINCT COUNTERPARTIES", but the real bundle carries
#     counterparty_ref=null on the cited outflows, so distinct-counterparty is NOT re-derivable from the
#     evidence. This is the weaker COUNT-based re-derivation; tightening it needs Pillar 1 to emit
#     counterparty refs (a cross-pillar follow-up). ---
_MIN_FANOUT_COUNT = 5
_FANOUT_WINDOW = timedelta(days=7)

# --- C15 shell / generic "trading company" counterparty: an outflow to a counterparty whose name
#     carries a generic-trading-company marker (the shell red flag — IND-04's general "trading
#     companies"). Substring markers, matched case-insensitively. ---
_GENERIC_TRADING_MARKERS = (
    "trading",
    "generic",
    "general trading",
    "fze",  # free-zone entity — a common opaque-counterparty vehicle
    "holding",
    "import",
    "export",
)
# --- C15 throughput (Phase 6): the shell_nominee conduit also manifests as ~0 net retention — total
#     inflow ~= total outflow over the cited flow (money passes through). The bar: net retention
#     (|in - out| / max(in, out)) at or below this fraction. The real conduit retains ~3.6%, so the bar
#     is set tight (5%) to keep the throughput path discriminating — it is the WEAKER of the two C15
#     sub-signals (a balanced ordinary account can also show low retention), so it backs up the grounded
#     generic-"trading company" name match rather than replacing it. Tightening further (a hop-count or
#     volume floor) is a follow-up; for now the tight ratio + the name-match alternative bound the
#     false-positive surface. ---
_MAX_NET_RETENTION_RATIO = 0.05

# --- C7 peer / business-activity anomaly (SCREENING-grounded, NOT replay-reproducible). Pillar 1's
#     BusinessActivityAnomalyDetector is a ScreeningDetector: it fires on an account whose total inflow
#     is a robust outlier above its PRODUCT-COHORT peers — a cross-account comparison whose cohort
#     baseline is definitionally absent from one account's cited records (Pillar 1's own Class-G gate,
#     monitor/verify.py, replays ALL_DETECTORS only and EXCLUDES C7). So there is no replay-reproducible
#     core to assert. What the cited evidence CAN re-derive is the detector's ABSOLUTE inflow floor; the
#     peer-cohort outlier core is screening-lineage — recorded in alert.rule (contract-enforced) and
#     corpus-resolved by verify_corpus_grounding (the 5th verifier) — NAMED, never faked as a replay.
#     COPIED from substrate business_activity.py MIN_INFLOW_CENTS (signal fin-2023-alert001:IND-06); no
#     sibling import (DESIGN / assumption A2). ---
_PEER_ANOMALY_MIN_INFLOW_CENTS = 2_500_000  # $25,000 — the detector's absolute inflow floor

# --- C8 income / activity mismatch (SCREENING-grounded, PARTY-relative). Pillar 1's IncomeMismatchDetector
#     is a ScreeningDetector: it fires on an account whose inflow grossly exceeds its owning party's DECLARED
#     expected monthly volume — a comparison against the KYC-recorded baseline (in the v0.2 `parties` block),
#     not a transaction pattern. What the cited evidence CAN re-derive is the ratio: sum(cited CREDIT inflow)
#     >= 12 x the recorded expected_monthly_volume_cents AND >= the same $25k absolute floor (below which a
#     ratio is noise). The declared baseline is screening-state (recorded, read from the party projection),
#     never faked. COPIED from substrate income_mismatch.py (MIN_INFLOW_CENTS / MISMATCH_MONTHLY_MULTIPLE,
#     signal fin-2023-alert001:IND-07); no sibling import (DESIGN / assumption A2). The floor numerically
#     coincides with the C7 peer-anomaly floor but is an INDEPENDENT copy of a distinct substrate constant. ---
_MISMATCH_MIN_INFLOW_CENTS = 2_500_000  # $25,000 — below this the income-mismatch ratio is noise
_MISMATCH_MONTHLY_MULTIPLE = 12  # inflow must exceed 12x the declared monthly volume (an annualized baseline)

# --- C14 KYC-integrity (SCREENING-grounded, PARTY-LEAF / txn-less). Pillar 1's KycIntegrityDetector is a
#     ScreeningDetector that fires on a defective STATIC KYC STATE — NOT a transaction pattern — and emits
#     txn_ids=() by design (its lineage is the KYC record, the party leaf). So there is no transaction to
#     replay: the grounding walk roots at the resolved party and re-derives the screened DEFECT over the
#     recorded PartyView state. COPIED from substrate kyc_integrity.py `_kyc_defect` (the screened condition,
#     signal fin-2025-a003:IND-09); no sibling import (DESIGN / assumption A3). The CDDLevel/RiskRating/PEPTier
#     enum VALUES serialize as plain strings into the v0.2+ `parties` block.
#     RECONCILED @ substrate 01ddeaf (Phase 14): substrate Phase 25 RE-KEYED `_kyc_defect`'s primary branch off
#     the old EDD-only tautology (`cdd_level == EDD and not source_of_funds` — which fired on every EDD party and
#     MISSED every elevated-non-EDD subject) onto `elevated_obligation and source_of_funds is None`. The copied
#     rule below is broadened to match, AND switches the old `not source_of_funds` to `source_of_funds is None`
#     to mirror substrate EXACTLY. Over the substrate data domain (source_of_funds is a documented string OR
#     None — the projection never emits "") this is a STRICT SUPERSET of the old EDD-only branch: every party the
#     old rule grounded still grounds, so it only REDUCES false-blocks. (The lone non-superset edge — an
#     empty-string source_of_funds under EDD — cannot arise from a substrate projection and correctly no longer
#     grounds: substrate's own `is None` predicate would not fire on it either.) Behavioral reconciliation against
#     a REAL C14 emission stays the deferred true gate (substrate emits no C14 today; ledger A0, revisit: open). ---
_CDD_EDD = "EDD"  # CDDLevel.EDD — enhanced due diligence (the escalation level every defect branch pivots on)
_RISK_HIGH = "HIGH"  # RiskRating.HIGH — the risk tier that must be escalated to EDD
_RISK_LOW = "LOW"  # RiskRating.LOW — the ONLY tier that is not, by itself, an elevated KYC obligation
_PEP_NONE = "NONE"  # PEPTier.NONE — no politically-exposed-person status (any other tier is elevated)

# A replay assertion grounds a signal over the cited transactions alone. A screening assertion additionally
# receives the alert's resolved PartyView (or None) — mirroring Pillar 1's Detector(txns) vs
# ScreeningDetector(txns, accounts, parties) split. The two tables are dispatched separately so the
# replay-reproducible assertions never see (and never depend on) party state.
Assertion = Callable[[dict[str, Any], list[dict[str, Any]]], list[str]]
ScreeningAssertion = Callable[[dict[str, Any], list[dict[str, Any]], dict[str, Any] | None], list[str]]


def _sorted_times(txns: list[dict[str, Any]], where: str) -> list[datetime] | str:
    """Parsed, sorted timestamps of ``txns``; a string violation if any row lacks a ts (fail-closed:
    an unknown time can't be window-confirmed, so the signal is not re-derivable)."""
    times = []
    for t in txns:
        ts = t.get("ts")
        if not ts:
            return f"{where}: cited txn '{t.get('txn_id')}' has no timestamp; the window is not re-derivable"
        times.append(datetime.fromisoformat(ts))
    times.sort()
    return times


def _assert_c4_structuring(alert: dict[str, Any], cited_txns: list[dict[str, Any]]) -> list[str]:
    where = f"alerts[{alert.get('alert_id')}].replay(C4)"
    deposits = [
        t for t in cited_txns if t.get("kind") == "cash_deposit" and 0 < t.get("amount_cents", 0) < _CTR_THRESHOLD_CENTS
    ]
    if len(deposits) < _MIN_STRUCTURING_COUNT:
        return [
            f"{where}: only {len(deposits)} sub-$10k cash deposit(s); "
            f"the structuring pattern needs >={_MIN_STRUCTURING_COUNT}"
        ]
    total = sum(t["amount_cents"] for t in deposits)
    if total < _CTR_THRESHOLD_CENTS:
        return [
            f"{where}: sub-$10k deposits aggregate to {total} cents (< the $10,000 reportable sum); not structuring"
        ]
    times = _sorted_times(deposits, where)
    if isinstance(times, str):
        return [times]
    if times[-1] - times[0] > _STRUCTURING_WINDOW:
        return [f"{where}: structuring deposits span {times[-1] - times[0]} > the {_STRUCTURING_WINDOW.days}d window"]
    return []


def _assert_c5_cash_placement(alert: dict[str, Any], cited_txns: list[dict[str, Any]]) -> list[str]:
    where = f"alerts[{alert.get('alert_id')}].replay(C5)"
    deposits = [t for t in cited_txns if t.get("kind") == "cash_deposit"]
    if len(deposits) < _MIN_PLACEMENT_COUNT:
        return [
            f"{where}: only {len(deposits)} cash deposit(s); the cash-placement pattern needs >={_MIN_PLACEMENT_COUNT}"
        ]
    times = _sorted_times(deposits, where)
    if isinstance(times, str):
        return [times]
    if times[-1] - times[0] > _PLACEMENT_WINDOW:
        return [f"{where}: cash deposits span {times[-1] - times[0]} > the {_PLACEMENT_WINDOW.days}d window"]
    return []


def _assert_c2_passthrough(alert: dict[str, Any], cited_txns: list[dict[str, Any]]) -> list[str]:
    where = f"alerts[{alert.get('alert_id')}].replay(C2)"
    inflows = [t for t in cited_txns if t.get("direction") == "CREDIT" and t.get("amount_cents", 0) > 0]
    outflows = [t for t in cited_txns if t.get("direction") == "DEBIT" and t.get("amount_cents", 0) > 0]
    if not inflows or not outflows:
        return [f"{where}: pass-through needs both an inflow and an outflow among the cited txns"]
    total_in = sum(t["amount_cents"] for t in inflows)
    total_out = sum(t["amount_cents"] for t in outflows)
    if total_out < _PASSTHROUGH_MIN_FRACTION * total_in:
        return [
            f"{where}: forwarded {total_out} of {total_in} cents "
            f"(< {_PASSTHROUGH_MIN_FRACTION:.0%}); not a pass-through"
        ]
    # the cited inflow + outflow must fall within the window (fail-closed on missing ts); ordering is
    # not asserted — the detector's rule does not state it (see the _PASSTHROUGH_WINDOW note)
    times = _sorted_times(inflows + outflows, where)
    if isinstance(times, str):
        return [times]
    if times[-1] - times[0] > _PASSTHROUGH_WINDOW:
        return [f"{where}: inflow/outflow span {times[-1] - times[0]} > the {_PASSTHROUGH_WINDOW}"]
    return []


def _assert_c3_funnel_fan(alert: dict[str, Any], cited_txns: list[dict[str, Any]]) -> list[str]:
    where = f"alerts[{alert.get('alert_id')}].replay(C3)"
    # COUNT-based fan-out (documented honesty gap: distinct-counterparty is not re-derivable — the
    # bundle omits counterparty refs on the cited outflows; see the module note + ledger A3).
    outflows = [t for t in cited_txns if t.get("direction") == "DEBIT" and t.get("amount_cents", 0) > 0]
    if len(outflows) < _MIN_FANOUT_COUNT:
        return [f"{where}: only {len(outflows)} cited outflow(s); the fan-out pattern needs >={_MIN_FANOUT_COUNT}"]
    times = _sorted_times(outflows, where)
    if isinstance(times, str):
        return [times]
    if times[-1] - times[0] > _FANOUT_WINDOW:
        return [f"{where}: fan-out outflows span {times[-1] - times[0]} > the {_FANOUT_WINDOW.days}d window"]
    return []


def _is_generic_trading(txn: dict[str, Any]) -> bool:
    name = str(txn.get("counterparty_name", "")).lower()
    return any(marker in name for marker in _GENERIC_TRADING_MARKERS)


def _net_retention_ratio(cited_txns: list[dict[str, Any]]) -> float | None:
    """|in - out| / max(in, out) over the cited flow, or None when a side is empty (not a conduit ->
    throughput is not re-derivable). The empty-side guard avoids a divide-by-zero AND a false 'balanced'."""
    total_in = sum(int(t.get("amount_cents", 0)) for t in cited_txns if t.get("direction") == "CREDIT")
    total_out = sum(int(t.get("amount_cents", 0)) for t in cited_txns if t.get("direction") == "DEBIT")
    if total_in <= 0 or total_out <= 0:
        return None
    return abs(total_in - total_out) / max(total_in, total_out)


def _assert_c15_shell(alert: dict[str, Any], cited_txns: list[dict[str, Any]]) -> list[str]:
    where = f"alerts[{alert.get('alert_id')}].replay(C15)"
    # (a) a generic "trading company" counterparty in the cited outflows — grounds to IND-04's general
    #     "trading companies" advisory text (the synthetic fixtures exhibit this).
    if any(_is_generic_trading(t) for t in cited_txns if t.get("kind") == "wire_out"):
        return []
    # (b) conduit throughput — total in ~= total out (low net retention), the shell_nominee pass-through
    #     behavior (the REAL bundle exhibits this; its counterparties carry no generic names).
    retention = _net_retention_ratio(cited_txns)
    if retention is not None and retention <= _MAX_NET_RETENTION_RATIO:
        return []
    return [
        f"{where}: no shell pattern in the cited evidence — neither an outflow to a generic 'trading "
        f"company' counterparty nor low-net-retention throughput (net retention={retention})"
    ]


def _screen_c7_peer_anomaly(
    alert: dict[str, Any], cited_txns: list[dict[str, Any]], party: dict[str, Any] | None
) -> list[str]:
    """Screening-grounding for C7: confirm the cited CREDIT inflow meets the detector's absolute floor.
    The peer-cohort outlier core (an 8-robust-sigma cut above the product-cohort median) is NOT
    re-derivable from one account's cited records — it is screening-lineage, recorded in ``alert.rule``
    and corpus-resolved by ``verify_corpus_grounding``. This grounds what the evidence CAN show; it never
    claims to replay the cohort comparison. ``party`` is part of the uniform screening signature but unused
    here — C7 grounds on the cited transactions, not party state. Fail-closed: a missing/zero/negative
    ``amount_cents`` only lowers the CREDIT inflow (toward a violation), never a false pass; a non-numeric
    ``amount_cents`` propagates as the module's other amount checks do — fail-loud, never a silent sign."""
    _ = party  # uniform screening signature; C7 does not read party state
    where = f"alerts[{alert.get('alert_id')}].screen(C7)"
    inflow = sum(int(t.get("amount_cents", 0)) for t in cited_txns if t.get("direction") == "CREDIT")
    if inflow < _PEER_ANOMALY_MIN_INFLOW_CENTS:
        return [
            f"{where}: cited inflow {inflow} cents < the ${_PEER_ANOMALY_MIN_INFLOW_CENTS // 100:,} "
            f"peer-anomaly floor; the screening signal's floor is not re-derivable over the cited evidence"
        ]
    return []


def _screen_c8_income_mismatch(
    alert: dict[str, Any], cited_txns: list[dict[str, Any]], party: dict[str, Any] | None
) -> list[str]:
    """Screening-grounding for C8: confirm the cited CREDIT inflow grossly exceeds the party's DECLARED
    monthly volume. Re-derivable = sum(cited CREDIT inflow) >= max(the $25k absolute floor, 12x the
    recorded ``expected_monthly_volume_cents``). The declared baseline is screening-state read from the
    v0.2 ``parties`` block (recorded in KYC, never faked). Fail-closed: no resolved party, or a party that
    declares no positive expected volume, means the ratio is not re-derivable over the available evidence —
    a violation, never a silent pass (a missing baseline must not pass an income-mismatch screen)."""
    where = f"alerts[{alert.get('alert_id')}].screen(C8)"
    if party is None:
        return [f"{where}: no party resolved for the alert's account; the declared-volume baseline is absent"]
    expected = party.get("expected_monthly_volume_cents")
    if not expected or int(expected) <= 0:
        return [f"{where}: party declares no positive expected_monthly_volume_cents; the ratio is not re-derivable"]
    inflow = sum(int(t.get("amount_cents", 0)) for t in cited_txns if t.get("direction") == "CREDIT")
    floor = max(_MISMATCH_MIN_INFLOW_CENTS, _MISMATCH_MONTHLY_MULTIPLE * int(expected))
    if inflow < floor:
        return [
            f"{where}: cited inflow {inflow} cents < the income-mismatch floor "
            f"max(${_MISMATCH_MIN_INFLOW_CENTS // 100:,}, {_MISMATCH_MONTHLY_MULTIPLE}x declared monthly "
            f"{expected}) = {floor} cents; the ratio is not re-derivable over the cited evidence"
        ]
    return []


def _screen_c14_kyc_integrity(
    alert: dict[str, Any], cited_txns: list[dict[str, Any]], party: dict[str, Any] | None
) -> list[str]:
    """Screening-grounding for C14: re-derive the static KYC-integrity DEFECT over the resolved party's
    recorded state (the party leaf — this alert cites no transaction). The screened condition is COPIED from
    substrate kyc_integrity._kyc_defect (no sibling import): a defect is (a) the SOURCE-OF-FUNDS DISCLOSURE GAP —
    an ELEVATED-OBLIGATION party (risk_rating != LOW, OR EDD, OR a PEP, OR sanctions/adverse-flagged) whose
    ``source_of_funds`` is absent; (b) a HIGH risk_rating not escalated to EDD; or (c) a sanctions/adverse-media
    flag without EDD. Branch (a) RECONCILED @ substrate 01ddeaf (Phase 14): substrate Phase 25 broadened it off
    the old EDD-only rule onto elevated-obligation; over the substrate data domain (source_of_funds is a
    documented string OR None) this is a strict superset of the old branch — it only REDUCES false-blocks on the
    elevated-non-EDD subjects the old copy missed, and matches substrate's exact `is None` predicate. A clean
    state grounds
    NOTHING (the alert claims a defect the record does not show -> violation). Fail-closed: no resolved party (a
    non-resolving party_ref), or a party missing the cdd_level pivot the screen reads, means the KYC state is not
    re-derivable — a violation, never a silent pass. ``cited_txns`` is part of the uniform screening signature but
    unread: C14 grounds on party state alone."""
    _ = cited_txns  # uniform screening signature; C14 is txn-less — its leaf is the party, not transactions
    where = f"alerts[{alert.get('alert_id')}].screen(C14)"
    if party is None:
        return [f"{where}: no party resolved for the alert's party_ref; the KYC state is absent (fail-closed)"]
    cdd = party.get("cdd_level")
    if cdd is None:
        return [f"{where}: party has no cdd_level; the KYC-integrity state is not re-derivable (fail-closed)"]
    risk = party.get("risk_rating")
    pep = party.get("pep_tier")
    flagged = bool(party.get("sanctions_flag")) or bool(party.get("adverse_media_flag"))
    # An ELEVATED KYC obligation: anything above low risk, or EDD-classified, or a PEP, or already flagged.
    # COPIED from substrate kyc_integrity._kyc_defect's elevated_obligation predicate (@01ddeaf, Phase 25).
    elevated_obligation = risk != _RISK_LOW or cdd == _CDD_EDD or (pep is not None and pep != _PEP_NONE) or flagged
    # the copied screened condition (any defect branch -> the C14 screen grounds)
    if elevated_obligation and party.get("source_of_funds") is None:
        return []
    if risk == _RISK_HIGH and cdd != _CDD_EDD:
        return []
    if flagged and cdd != _CDD_EDD:
        return []
    return [
        f"{where}: the recorded KYC state shows no integrity defect "
        f"(cdd_level={cdd!r}, risk_rating={risk!r}); the C14 screen is not re-derivable"
    ]


# --- replay-reproducible transaction-monitoring signals: a per-capability PATTERN re-derivation over the
#     cited evidence (mirrors Pillar 1's per-account Class-G ALL_DETECTORS). ---
_ASSERTIONS: dict[str, Assertion] = {
    "C2": _assert_c2_passthrough,
    "C3": _assert_c3_funnel_fan,
    "C4": _assert_c4_structuring,
    "C5": _assert_c5_cash_placement,
    "C15": _assert_c15_shell,
}

# --- SCREENING signals: context-relative detections that are NOT replay-reproducible from one account's
#     cited records (mirrors Pillar 1's SCREENING_DETECTORS). They ground on a re-derivable floor/ratio +
#     their recorded screening lineage, never a faked replay. C7 grounds on the cited inflow alone; C8
#     additionally reads the resolved party's DECLARED expected volume; C14 is txn-less and grounds on the
#     resolved party's static KYC state ALONE (the party leaf — see the leaf-XOR contract rule). ---
_SCREENING: dict[str, ScreeningAssertion] = {
    "C7": _screen_c7_peer_anomaly,
    "C8": _screen_c8_income_mismatch,
    "C14": _screen_c14_kyc_integrity,
}


def _party_by_account(bundle: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Map each subject account_id to its PartyView row (v0.2 `parties`). The observable FK is
    customer_id IS party_id (Pillar 1's own join): the subject's accounts all resolve to the subject's
    party. Empty when the bundle carries no parties (v0.1) or no matching party — screening assertions
    that need party state then fail closed."""
    subject = bundle.get("subject", {})
    customer_id = subject.get("customer_id")
    if customer_id is None:
        # Fail closed in isolation: a missing subject customer_id must not join a party row whose
        # party_id is also None (don't rely on the contract verifier firing first).
        return {}
    parties_by_id = {p.get("party_id"): p for p in bundle.get("parties", []) if isinstance(p, dict)}
    party = parties_by_id.get(customer_id)
    if party is None:
        return {}
    return dict.fromkeys(subject.get("account_ids", []), party)


def _party_by_ref(bundle: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Map each declared party_id to its PartyView row (v0.2 `parties`) — the resolution target for a
    party-leaf alert's `party_ref` (reference-by-path). Admits ONLY a non-empty STRING party_id (the same
    predicate as `contract.party_ids`): a party_id is a string by contract, so this excludes None/empty and
    keeps every map key hashable (an unhashable party_id value never crashes the build)."""
    return {
        p["party_id"]: p
        for p in bundle.get("parties", [])
        if isinstance(p, dict) and isinstance(p.get("party_id"), str) and p["party_id"]
    }


def _resolve_party(
    alert: dict[str, Any],
    party_by_account: dict[str, dict[str, Any]] | None,
    party_by_ref: dict[str, dict[str, Any]] | None,
) -> dict[str, Any] | None:
    """Resolve the PartyView a screening alert grounds against. A party-leaf alert (non-empty `party_ref`)
    resolves ONLY via reference-by-path — its `party_ref` against the declared parties; a non-resolving ref
    yields None (fail-closed, no fallback to the account join). A transaction-leaf screening alert (C7/C8,
    no `party_ref`) resolves via the account join (customer_id IS party_id)."""
    party_ref = alert.get("party_ref")
    if isinstance(party_ref, str) and party_ref:
        return (party_by_ref or {}).get(party_ref)
    account_id = alert.get("account_id")
    if party_by_account and isinstance(account_id, str):
        return party_by_account.get(account_id)
    return None


def replay_alert(
    alert: dict[str, Any],
    txns_by_id: dict[str, dict[str, Any]],
    party_by_account: dict[str, dict[str, Any]] | None = None,
    party_by_ref: dict[str, dict[str, Any]] | None = None,
) -> list[str]:
    """Ground one alert's signal over its cited evidence. Empty list == grounds.

    Two grounding classes (mirroring Pillar 1's Detector/ScreeningDetector split): ``_ASSERTIONS`` is a
    per-capability PATTERN re-derivation over the cited transactions; ``_SCREENING`` grounds a
    context-relative signal on its re-derivable floor/ratio + recorded lineage, and additionally receives
    the alert's resolved PartyView (or None). A txn-less party-leaf alert (C14) cites no transaction and
    resolves its party via ``party_ref`` (reference-by-path); a transaction-leaf screening alert resolves
    via the account join. A capability in neither table is a violation (fail-closed: grounded-or-dropped)."""
    capability = alert.get("capability")
    cited_txns = [txns_by_id[tid] for tid in alert.get("txn_ids", []) if tid in txns_by_id]
    if isinstance(capability, str):
        assertion = _ASSERTIONS.get(capability)
        if assertion is not None:
            return assertion(alert, cited_txns)
        screen = _SCREENING.get(capability)
        if screen is not None:
            party = _resolve_party(alert, party_by_account, party_by_ref)
            return screen(alert, cited_txns, party)
    return [
        f"alerts[{alert.get('alert_id')}]: no replay assertion registered for capability "
        f"'{capability}' (fail-closed: an un-replayable signal is a violation)"
    ]


def replay_bundle(bundle: dict[str, Any]) -> list[str]:
    """Re-derive every cited signal in the bundle. Empty list == all signals replay."""
    txns_by_id = {t["txn_id"]: t for t in bundle.get("transactions", []) if t.get("txn_id")}
    party_by_account = _party_by_account(bundle)
    party_by_ref = _party_by_ref(bundle)
    violations: list[str] = []
    for alert in bundle.get("alerts", []):
        violations.extend(replay_alert(alert, txns_by_id, party_by_account, party_by_ref))
    return violations
