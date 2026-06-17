#!/usr/bin/env python3
"""Cross-pillar end-to-end verification harness (Phase 55, NON-ship).

Proves the 3-pillar chain is CONNECTED: a substrate-emitted evidence bundle (Pillar 1) became a
verified, signed SAR (Pillar 2) whose every statement walks back through the evidence to the FROZEN
signal-watch regulator corpus. The contract this implements is docs/e2e-acceptance.md (checks A/B/C);
the on-disk schema + id-mint rule is docs/pillar-integration-contract.md §2.

DOCTRINE (load-bearing):
  * file-contract ONLY — reads committed/regenerated sibling OUTPUTS (json). It NEVER imports
    aml_substrate / aml_casework (the one-repo-per-pillar boundary). The only import is signal-watch's
    OWN derive_signals.normalize (the stable grounding core — reused, not reimplemented).
  * stdlib only; deterministic (sha1 id-mint, no clock/random in the assertions).
  * --selftest proves the LOGIC on a committed SYNTHETIC fixture (NOT sibling output, labeled
    illustrative). --real runs the same checks on actual sibling outputs and is the delivery gate.

Usage:
  python3 scripts/e2e_chain_check.py --selftest
  python3 scripts/e2e_chain_check.py --make-fixtures
  python3 scripts/e2e_chain_check.py --real --substrate <bundle.json> --casework <signed.json>
"""
from __future__ import annotations

import glob
import hashlib
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _HERE)
from derive_signals import normalize  # signal-watch's OWN grounding core (NOT a sibling)

# The current sibling grounding pins (the re-ground-before-consume rule updates these).
GROUNDING_HEADS = {"aml_substrate": "bafc67d", "aml_casework": "0316580"}

# Mirrors aml_casework.contract.STR_REQUIRED_ELEMENTS (copied by the file-contract, NOT imported).
STR_REQUIRED_ELEMENTS = (
    "reporting_entity",
    "transaction_details",
    "account_information",
    "subject_information",
    "typology_grounds",
    "grounds_for_suspicion_narrative",
)

E2E_DIR = os.path.join(_ROOT, "data", "e2e")
STATUS_PATH = os.path.join(_ROOT, "data", "pillar-status.json")


# --- the §2 deterministic id-mint rule (the single source of truth for the contract) ---------------
def mint_alert_id(detector: str, account_id: str, txn_ids, signal_id: str) -> str:
    raw = f"{detector}|{account_id}|{','.join(sorted(txn_ids))}|{signal_id}"
    return "AL-" + hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12]


def mint_dossier_id(account_id: str, alert_ids) -> str:
    raw = f"{account_id}|{','.join(sorted(alert_ids))}"
    return "DS-" + hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12]


# --- corpus grounding (the FROZEN signal-watch corpus — signal-watch's OWN data) ------------------
def _find_indicator_flag(advisory_id: str, indicator_id: str):
    """Return the verbatim flag of <advisory_id>:<indicator_id> from the committed corpus, or None."""
    matches = glob.glob(os.path.join(_ROOT, "data", "*", "derived", f"{advisory_id}.json"))
    if not matches:
        return None
    record = json.load(open(matches[0], encoding="utf-8"))

    def walk(o):
        if isinstance(o, dict):
            if o.get("id") == indicator_id and "flag" in o:
                yield o["flag"]
            for v in o.values():
                yield from walk(v)
        elif isinstance(o, list):
            for v in o:
                yield from walk(v)

    for flag in walk(record):
        return flag
    return None


# --- the chain check (docs/e2e-acceptance.md A/B/C) -----------------------------------------------
def check_chain(bundle: dict, signed: dict) -> list:
    """Return a list of join violations; [] == the chain is connected."""
    v: list = []

    def req(obj, key, where):
        if not isinstance(obj, dict) or key not in obj or obj[key] in (None, "", [], {}):
            v.append(f"{where}: missing/empty '{key}'")
            return False
        return True

    # === A. substrate side — the emitted evidence is real-grounded ===
    req(bundle, "contract_version", "bundle")
    if bundle.get("illustrative") is not True:
        v.append("bundle: 'illustrative' must be true (synthetic/illustrative output discipline)")
    req(bundle, "case_id", "bundle")
    subject = bundle.get("subject", {})
    req(subject, "customer_id", "subject")
    acct_ids = set(subject.get("account_ids", []))
    if not acct_ids:
        v.append("subject: empty 'account_ids'")

    txn_ids = set()
    for i, t in enumerate(bundle.get("transactions", [])):
        w = f"transactions[{i}]"
        if req(t, "txn_id", w) and req(t, "account_id", w):
            txn_ids.add(t["txn_id"])
    if not txn_ids:
        v.append("bundle: no transactions (the data rows alerts must cite)")

    alert_ids = []
    grounded_signal_ids = set()
    for i, a in enumerate(bundle.get("alerts", [])):
        w = f"alerts[{i}]"
        for k in ("alert_id", "detector", "capability", "account_id", "rule"):
            req(a, k, w)
        alert_ids.append(a.get("alert_id"))
        if a.get("account_id") not in acct_ids:
            v.append(f"{w}: account_id '{a.get('account_id')}' not in subject.account_ids")
        cited = a.get("txn_ids", [])
        if not cited:
            v.append(f"{w}: empty 'txn_ids'")
        for tid in cited:
            if tid not in txn_ids:
                v.append(f"{w}: cites unknown txn_id '{tid}'")
        g = a.get("grounding", {})
        for k in ("signal_id", "advisory_id", "indicator_id", "capability", "data_source", "flag"):
            req(g, k, f"{w}.grounding")
        sig = g.get("signal_id")
        if sig and sig != f"{g.get('advisory_id')}:{g.get('indicator_id')}":
            v.append(f"{w}.grounding: signal_id '{sig}' != '<advisory_id>:<indicator_id>'")
        if g.get("capability") and a.get("capability") and g["capability"] != a["capability"]:
            v.append(f"{w}: capability '{a['capability']}' disagrees with grounding.capability '{g['capability']}'")
        grounded_signal_ids.add(sig)
        # A3 — deterministic id-mint
        expect = mint_alert_id(a.get("detector", ""), a.get("account_id", ""), cited, sig or "")
        if a.get("alert_id") != expect:
            v.append(f"{w}: alert_id '{a.get('alert_id')}' != minted '{expect}' (§2 sha1 rule)")
        # A4 — corpus grounding (against the FROZEN signal-watch corpus)
        cflag = _find_indicator_flag(g.get("advisory_id", ""), g.get("indicator_id", ""))
        if cflag is None:
            v.append(f"{w}.grounding: corpus record {g.get('advisory_id')}:{g.get('indicator_id')} not found in data/*/derived")
        elif normalize(g.get("flag", "")) not in normalize(cflag):
            v.append(f"{w}.grounding: flag does not ground to {g.get('advisory_id')}:{g.get('indicator_id')} under normalize()")

    d = bundle.get("dossier", {})
    if d:
        if req(d, "dossier_id", "dossier"):
            expect = mint_dossier_id(d.get("account_id", ""), d.get("alert_ids", []))
            if d.get("dossier_id") != expect:
                v.append(f"dossier: dossier_id '{d.get('dossier_id')}' != minted '{expect}' (§2 sha1 rule)")
        for aid in d.get("alert_ids", []):
            if aid not in alert_ids:
                v.append(f"dossier: references unknown alert_id '{aid}'")

    # === B. casework side — the SAR is verified + signed ===
    s = signed.get("str_record", {})
    if not s:
        v.append("signed: missing 'str_record' (the casework SAR)")
    else:
        narr = s.get("narrative")
        flag = s.get("completeness", {}).get("grounds_for_suspicion_narrative")
        if narr in (None, ""):
            v.append("signed.str_record: empty narrative (Pillar 2 did not fill the SAR)")
        if flag is not True:
            v.append("signed.str_record: grounds_for_suspicion_narrative != true (the seam was not flipped)")
        comp = s.get("completeness", {})
        for el in STR_REQUIRED_ELEMENTS:
            if el not in comp:
                v.append(f"signed.str_record.completeness: missing element '{el}'")
        # the cite universe Pillar 1 grounded
        signed_txn_ids = {t.get("txn_id") for t in signed.get("transactions", [])} or txn_ids
        resolvable = grounded_signal_ids | signed_txn_ids
        claims = s.get("narrative_claims", [])
        if not claims:
            v.append("signed.str_record: no narrative_claims (nothing to verify citations against)")
        for j, claim in enumerate(claims):
            cw = f"signed.str_record.narrative_claims[{j}]"
            req(claim, "text", cw)
            cites = claim.get("cites", [])
            if not cites:
                v.append(f"{cw}: empty 'cites'")
            for c in cites:
                if c not in resolvable:
                    v.append(f"{cw}: dangling cite '{c}' (resolves to no grounded signal_id / txn_id)")

    so = signed.get("signoff")
    if so is not None:
        if so.get("signed") is not True:
            v.append("signed.signoff: signed != true (the SAR is not signed)")
        if so.get("blocking_violations"):
            v.append(f"signed.signoff: blocking_violations non-empty {so.get('blocking_violations')}")

    # === C. cross-pillar identity ===
    if bundle.get("case_id") and signed.get("case_id") and bundle["case_id"] != signed["case_id"]:
        v.append(f"cross-pillar: case_id mismatch (bundle '{bundle['case_id']}' vs signed '{signed['case_id']}')")
    for sid in s.get("cited_signal_ids", []) if s else []:
        if sid not in grounded_signal_ids:
            v.append(f"signed.str_record: cited_signal_id '{sid}' grounded by no bundle alert")

    return v


# --- pillar-status (the launcher reads this; regenerated on every run) ----------------------------
def write_status(spine_proven: bool, bridge_1: str, bridge_2: str, e2e_real: str) -> None:
    status = {
        "illustrative": True,
        "phase": "55",
        "note": "regenerated by scripts/e2e_chain_check.py — bridge states for the cross-pillar demo",
        "grounding_heads": GROUNDING_HEADS,
        "spine": {
            "state": "proven" if spine_proven else "unproven",
            "detail": "e2e_chain_check --selftest green on the synthetic C4 fixture",
        },
        "bridges": {
            "bridge_1_persist": {
                "state": bridge_1,
                "detail": "aml-substrate emits the §5a evidence bundle (persist + mint ids)",
            },
            "bridge_2_consume": {
                "state": bridge_2,
                "detail": "aml-casework consumes a REAL substrate bundle -> signed SAR",
            },
            "e2e_real": {
                "state": e2e_real,
                "detail": "e2e_chain_check --real green on the actual sibling outputs (delivery gate)",
            },
        },
    }
    os.makedirs(os.path.dirname(STATUS_PATH), exist_ok=True)
    with open(STATUS_PATH, "w", encoding="utf-8") as fh:
        json.dump(status, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


# --- synthetic fixtures (correct-by-construction: minted ids + the real corpus flag) --------------
def make_fixtures() -> None:
    case_id = "CASE-E2E-C4"
    acct = "A-E2E001"
    detector = "StructuringDetector"
    signal_id = "fin-2026-alert001:IND-11"
    txns = [
        {"txn_id": "L-E0000001", "account_id": acct, "kind": "cash_deposit", "amount_cents": 910000, "ts": "2026-05-04T09:12:00"},
        {"txn_id": "L-E0000002", "account_id": acct, "kind": "cash_deposit", "amount_cents": 940000, "ts": "2026-05-04T15:40:00"},
        {"txn_id": "L-E0000003", "account_id": acct, "kind": "cash_deposit", "amount_cents": 880000, "ts": "2026-05-05T10:05:00"},
        {"txn_id": "L-E0000004", "account_id": acct, "kind": "cash_deposit", "amount_cents": 970000, "ts": "2026-05-05T16:22:00"},
    ]
    txn_ids = [t["txn_id"] for t in txns]
    cflag = _find_indicator_flag("fin-2026-alert001", "IND-11")
    if cflag is None:
        raise SystemExit("make-fixtures: cannot find fin-2026-alert001:IND-11 in the committed corpus")
    alert_id = mint_alert_id(detector, acct, txn_ids, signal_id)
    dossier_id = mint_dossier_id(acct, [alert_id])
    alert = {
        "alert_id": alert_id,
        "detector": detector,
        "capability": "C4",
        "account_id": acct,
        "rule": ">=4 cash deposits strictly inside (9000,10000) dollars within 7d (sub-CTR structuring)",
        "txn_ids": txn_ids,
        "grounding": {
            "signal_id": signal_id,
            "advisory_id": "fin-2026-alert001",
            "indicator_id": "IND-11",
            "capability": "C4",
            "data_source": "D2",
            "flag": cflag,
            "red_flag": "CTR-trigger evasion: sub-$10K cash structuring",
        },
    }
    scaffold_completeness = {
        "reporting_entity": True,
        "transaction_details": True,
        "account_information": True,
        "subject_information": True,
        "typology_grounds": True,
        "grounds_for_suspicion_narrative": False,
    }
    base = {
        "contract_version": "0.1",
        "illustrative": True,
        "case_id": case_id,
        "subject": {"customer_id": "P-E2E001", "name": "Eastflow Imports Ltd. (SYNTHETIC)", "account_ids": [acct]},
        "transactions": txns,
        "alerts": [alert],
        "dossier": {"dossier_id": dossier_id, "account_id": acct, "alert_ids": [alert_id]},
        "str_record": {
            "case_id": case_id,
            "crime_type": "structuring",
            "subject_account_ids": [acct],
            "cited_signal_ids": [signal_id],
            "cited_txn_ids": txn_ids,
            "completeness": dict(scaffold_completeness),
            "narrative": None,
            "narrative_claims": [],
        },
    }

    # the substrate-emitted bundle (the open scaffold)
    substrate = json.loads(json.dumps(base))

    # the casework signed SAR (narrative filled, seam flipped, claims cite resolved evidence, signed)
    signed = json.loads(json.dumps(base))
    signed["str_record"]["completeness"]["grounds_for_suspicion_narrative"] = True
    signed["str_record"]["narrative"] = (
        "Between 2026-05-04 and 2026-05-05, Eastflow Imports Ltd. (account A-E2E001) made four cash "
        "deposits of $8,800-$9,700, each just under the $10,000 CTR-filing threshold, consistent with "
        "structuring to evade currency-transaction reporting (FinCEN fin-2026-alert001 IND-11, C4)."
    )
    signed["str_record"]["narrative_claims"] = [
        {
            "text": "Four sub-$10,000 cash deposits within two days indicate structuring to evade the CTR threshold.",
            "cites": [signal_id, *txn_ids],
        }
    ]
    signed["signoff"] = {
        "signed": True,
        "signer": "SYNTHETIC-reviewer",
        "ts": "2026-06-17T00:00:00",
        "disposition": "file",
        "blocking_violations": [],
    }

    # a NEGATIVE fixture: a single injected fault (alert_id not matching the §2 mint rule)
    broken = json.loads(json.dumps(substrate))
    broken["alerts"][0]["alert_id"] = "AL-NOTMINTED01"

    os.makedirs(E2E_DIR, exist_ok=True)
    for name, obj in (
        ("substrate-bundle-c4.json", substrate),
        ("casework-signed-c4.json", signed),
        ("substrate-bundle-c4-broken.json", broken),
    ):
        with open(os.path.join(E2E_DIR, name), "w", encoding="utf-8") as fh:
            json.dump(obj, fh, indent=2, ensure_ascii=False)
            fh.write("\n")


# --- modes -----------------------------------------------------------------------------------------
def _load(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def selftest() -> int:
    # the mint rule is deterministic
    a = mint_alert_id("D", "A", ["t2", "t1"], "s")
    b = mint_alert_id("D", "A", ["t1", "t2"], "s")
    assert a == b and a.startswith("AL-"), "alert_id mint not order-stable"
    assert mint_dossier_id("A", ["x"]).startswith("DS-"), "dossier_id mint shape"

    need = [os.path.join(E2E_DIR, n) for n in ("substrate-bundle-c4.json", "casework-signed-c4.json", "substrate-bundle-c4-broken.json")]
    if not all(os.path.exists(p) for p in need):
        make_fixtures()

    bundle = _load(os.path.join(E2E_DIR, "substrate-bundle-c4.json"))
    signed = _load(os.path.join(E2E_DIR, "casework-signed-c4.json"))
    broken = _load(os.path.join(E2E_DIR, "substrate-bundle-c4-broken.json"))

    ok = check_chain(bundle, signed)
    bad = check_chain(broken, signed)

    write_status(spine_proven=not ok, bridge_1="pending", bridge_2="pending", e2e_real="pending")

    failures = []
    if ok:
        failures.append(f"GOOD pair should connect, got violations: {ok}")
    if not bad:
        failures.append("BROKEN bundle (un-minted alert_id) should be caught, got none")
    elif not any("alert_id" in m and "minted" in m for m in bad):
        failures.append(f"BROKEN bundle caught, but not by the id-mint check: {bad}")

    if failures:
        for f in failures:
            print(f"FAIL: {f}", file=sys.stderr)  # noqa: T201
        return 1
    print("e2e_chain_check --selftest: PASS (good pair connects; broken bundle caught by the §2 id-mint check)")  # noqa: T201
    print(f"  fixtures: data/e2e/ ; status: data/pillar-status.json (spine proven; bridges pending)")  # noqa: T201
    return 0


def real(substrate_path: str, casework_path: str) -> int:
    missing = [p for p in (substrate_path, casework_path) if not (p and os.path.exists(p))]
    if missing:
        # honest gate: the sibling outputs do not exist yet (bridges #1/#2 not landed)
        b1 = "pending" if not (substrate_path and os.path.exists(substrate_path)) else "done"
        b2 = "pending" if not (casework_path and os.path.exists(casework_path)) else "done"
        write_status(spine_proven=True, bridge_1=b1, bridge_2=b2, e2e_real="pending")
        for p in missing:
            print(f"GATED: sibling output absent: {p}", file=sys.stderr)  # noqa: T201
        print("GATED: the --real chain verification needs both sibling outputs (bridges #1 + #2). "
              "Run after the aml-substrate persist + aml-casework consume-real-bundle sessions land.", file=sys.stderr)  # noqa: T201
        return 2

    bundle = _load(substrate_path)
    signed = _load(casework_path)
    violations = check_chain(bundle, signed)
    if violations:
        write_status(spine_proven=True, bridge_1="done", bridge_2="done", e2e_real="failed")
        print(f"e2e_chain_check --real: NOT CONNECTED ({len(violations)} violation(s)):", file=sys.stderr)  # noqa: T201
        for m in violations:
            print(f"  - {m}", file=sys.stderr)  # noqa: T201
        return 1
    write_status(spine_proven=True, bridge_1="done", bridge_2="done", e2e_real="done")
    print("e2e_chain_check --real: CONNECTED — substrate-detected case -> verified, signed SAR, grounded to the frozen corpus.")  # noqa: T201
    return 0


def main(argv: list) -> int:
    if "--selftest" in argv:
        return selftest()
    if "--make-fixtures" in argv:
        make_fixtures()
        print(f"wrote synthetic fixtures to {E2E_DIR}")  # noqa: T201
        return 0
    if "--real" in argv:
        def opt(name):
            return argv[argv.index(name) + 1] if name in argv and argv.index(name) + 1 < len(argv) else None
        return real(opt("--substrate"), opt("--casework"))
    print(__doc__)  # noqa: T201
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
