#!/usr/bin/env python3
"""Validate the vendored chain-case library (Phase 56, NON-ship, NOT a build target).

The case library under data/chain-cases/ is the pre-baked detection input for the chain workbench:
real aml-substrate evidence bundles, pinned like the corpus. This validator confirms every vendored
bundle is still a well-formed, real-grounded substrate emission — it reuses e2e_chain_check's OWN
substrate-side checks (schema + §2 deterministic id-mint + grounding to the FROZEN signal-watch
corpus), so a vendored bundle is held to exactly the bridge-#1 acceptance bar.

DOCTRINE:
  * reuses signal-watch's OWN e2e_chain_check.check_substrate — NEVER imports aml_substrate /
    aml_casework (the one-repo-per-pillar boundary). The library is file-contract data.
  * stdlib only; build.py never imports this (data/chain-cases is not a build target).
  * the manifest's display metadata (capabilities, subject) is referentially checked against the
    bundle bytes, so the workbench can't claim a capability the evidence doesn't carry.

Usage:
  python3 scripts/validate_chain_cases.py            # validate the committed library (exit 0/1)
  python3 scripts/validate_chain_cases.py --selftest # prove the validator catches tampering
"""
from __future__ import annotations

import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _HERE)
from e2e_chain_check import check_substrate  # signal-watch's OWN substrate-side checks (NOT a sibling)

CASES_DIR = os.path.join(_ROOT, "data", "chain-cases")
MANIFEST_PATH = os.path.join(CASES_DIR, "manifest.json")


def _load(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def validate_case(case: dict, bundle: dict) -> list:
    """Return a list of violation strings for one library entry; [] == the case is valid."""
    v: list = []
    cid = case.get("case_id", "<unknown>")

    # the bundle must still pass the bridge-#1 substrate acceptance (schema + id-mint + grounding)
    sub_v, ctx = check_substrate(bundle)
    v.extend(f"{cid}: bundle {m}" for m in sub_v)

    # manifest <-> bundle referential integrity (display metadata can't outrun the evidence)
    if bundle.get("case_id") != case.get("case_id"):
        v.append(f"{cid}: manifest case_id != bundle case_id '{bundle.get('case_id')}'")
    if case.get("illustrative") is False or bundle.get("illustrative") is not True:
        v.append(f"{cid}: bundle 'illustrative' must be true (synthetic-output discipline)")

    subj = case.get("subject", {})
    bsubj = bundle.get("subject", {})
    if subj.get("customer_id") and subj["customer_id"] != bsubj.get("customer_id"):
        v.append(f"{cid}: manifest subject.customer_id != bundle '{bsubj.get('customer_id')}'")
    if subj.get("account_id") and subj["account_id"] not in set(bsubj.get("account_ids", [])):
        v.append(f"{cid}: manifest subject.account_id '{subj['account_id']}' not in bundle account_ids")

    if case.get("alert_count") is not None and case["alert_count"] != len(bundle.get("alerts", [])):
        v.append(f"{cid}: manifest alert_count {case['alert_count']} != bundle {len(bundle.get('alerts', []))}")
    if case.get("txn_count") is not None and case["txn_count"] != len(bundle.get("transactions", [])):
        v.append(f"{cid}: manifest txn_count {case['txn_count']} != bundle {len(bundle.get('transactions', []))}")

    # every capability the manifest advertises must be a real (capability, signal_id) alert in the bundle
    bundle_caps = {(a.get("capability"), a.get("grounding", {}).get("signal_id"))
                   for a in bundle.get("alerts", [])}
    for c in case.get("capabilities", []):
        pair = (c.get("capability"), c.get("signal_id"))
        if pair not in bundle_caps:
            v.append(f"{cid}: manifest capability {pair} has no matching bundle alert")

    # provenance note required (where the bytes came from — the re-vendor contract)
    prov = case.get("provenance", {})
    for k in ("substrate_repo", "substrate_head", "vendored_from"):
        if not prov.get(k):
            v.append(f"{cid}: provenance missing '{k}'")
    return v


def validate_library(manifest: dict, cases_dir: str) -> list:
    """Validate a whole manifest (loading each bundle from cases_dir); return all violations."""
    v: list = []
    if manifest.get("illustrative") is not True:
        v.append("manifest: 'illustrative' must be true")
    cases = manifest.get("cases", [])
    if not cases:
        v.append("manifest: no cases (an empty library proves nothing)")
    seen = set()
    for case in cases:
        cid = case.get("case_id")
        if not cid:
            v.append("manifest: a case is missing 'case_id'")
            continue
        if cid in seen:
            v.append(f"manifest: duplicate case_id '{cid}'")
        seen.add(cid)
        rel = case.get("bundle")
        if not rel:
            v.append(f"{cid}: missing 'bundle' path")
            continue
        bpath = os.path.join(cases_dir, rel)
        if not os.path.exists(bpath):
            v.append(f"{cid}: bundle file not found: {rel}")
            continue
        v.extend(validate_case(case, _load(bpath)))
    return v


def selftest() -> int:
    manifest = _load(MANIFEST_PATH)
    failures = []

    # GREEN — the committed library validates clean
    good = validate_library(manifest, CASES_DIR)
    if good:
        failures.append(f"committed library should be clean, got: {good}")

    # RED — an in-memory tampered bundle (broken id-mint) must be caught
    case = manifest["cases"][0]
    bundle = _load(os.path.join(CASES_DIR, case["bundle"]))
    tampered = json.loads(json.dumps(bundle))
    tampered["alerts"][0]["alert_id"] = "AL-TAMPERED01"
    caught = validate_case(case, tampered)
    if not any("minted" in m for m in caught):
        failures.append(f"tampered alert_id should be caught by the §2 id-mint check, got: {caught}")

    # RED — a manifest claiming a capability the bundle lacks must be caught
    drift = json.loads(json.dumps(case))
    drift["capabilities"] = list(drift.get("capabilities", [])) + [{"capability": "C99", "signal_id": "fake:IND-00"}]
    caught2 = validate_case(drift, bundle)
    if not any("no matching bundle alert" in m for m in caught2):
        failures.append(f"manifest capability drift should be caught, got: {caught2}")

    if failures:
        for f in failures:
            print(f"FAIL: {f}", file=sys.stderr)  # noqa: T201
        return 1
    print("validate_chain_cases --selftest: PASS "  # noqa: T201
          "(committed library clean; tampered id-mint + capability drift both caught)")
    return 0


def main(argv: list) -> int:
    if "--selftest" in argv:
        return selftest()
    manifest = _load(MANIFEST_PATH)
    v = validate_library(manifest, CASES_DIR)
    if v:
        print(f"chain-case library INVALID ({len(v)} violation(s)):", file=sys.stderr)  # noqa: T201
        for m in v:
            print(f"  - {m}", file=sys.stderr)  # noqa: T201
        return 1
    n = len(manifest.get("cases", []))
    print(f"chain-case library VALID — {n} case(s) pass the substrate-side bar "  # noqa: T201
          f"(schema + §2 id-mint + grounding to the frozen corpus); manifest<->bundle integrity holds.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
