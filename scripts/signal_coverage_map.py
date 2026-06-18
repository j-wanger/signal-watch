#!/usr/bin/env python3
"""Phase 58 — corpus->substrate signal-coverage map (design the detection layer FROM the corpus).

NON-SHIP, stdlib only, read-only over the committed corpus (does NOT touch corpus.html / dist / any
committed corpus record). build.py never imports this. The "Illustrative data & outputs" honesty posture
governs every number; each tier carries its definition.

WHAT IT ANSWERS
    "We have 2,251 corpus indicators / 523 buildable; we want to build 200+ grounded signals over the
    synthetic substrate." For each BUILDABLE corpus indicator (status==gap AND data==available), is a
    grounded signal reachable on aml-substrate today, and if not, what is the binding gap?

THE DOCTRINE BOUNDARY (Phase-58 A0)
    The corpus drives DETECTOR + observable-exposure design (top-down). data generation + labels stay
    emergent (bottom-up). This map MEASURES the behavioral-coverage gap; it NEVER stamps it.

HONEST TIERING (the gate's "pinned real data + honest tiering")
    - observable-surface reachability is MEASURED: substrate_class(D) is computed against the substrate's
      schema facts (data/coverage-map/substrate-pin.json, code-verified @ the recorded HEADs) AND the
      real emitted sample (data/chain-cases/CASE-P-0010361/bundle.json) -- e.g. D17 is modeled-inactive
      because counterparty_country is 0/71 non-null in the actual emission.
    - behavioral-emergence reachability is REASONED from DESIGN.md/gen (pin.capabilities[C].behavior_*)
      and flagged behavior_confirmed:false unless the capability fires in the emission.

THE FIVE TIERS (per buildable indicator with capability C and data_source D)
    reachable-now      C has a live detector + casework assertion + emergent behavior ({C2,C3,C4,C5,C15}).
                       grounding_mode = direct if D is exposed-active, else proxy (the detector grounds
                       via an exposed transaction observable substituting D -- e.g. C15/D8 shell via
                       throughput, C3/D13 funnel via transactions; both VALIDATED in the emission).
    needs-detector     D is exposed-active + behavior emerges/plausible, but no detector/assertion yet.
                       The cheapest build: author a detector + a casework assertion. (capability-scaled.)
    needs-view-exposure D is modeled but UNEXPOSED to the detector views (no party view; detail tables).
                       Fix: wire a view. (D8 KYC / D12 PEP / D5 memo / D6 cheque-detail / D9 identity.)
    needs-behavior     D is exposed-active but the pattern never emerges (C6 dormancy), or D is modeled
                       but never populated (D17 country). Fix: the emergence engine. behavior_confirmed=false.
    out-of-reach       D is not modeled / a dead never-set flag (D7 VC, D11 sanctions, D13 adverse-media,
                       D14 gov, D15 trade, D16 maritime, D18 real-estate, D19 trust, D20 lifestyle).
                       The bank/substrate genuinely cannot observe it -- honest, not a defect.

Usage:
    python3 scripts/signal_coverage_map.py            # text report (the measured numbers)
    python3 scripts/signal_coverage_map.py --json      # the coverage.json payload to stdout
    python3 scripts/signal_coverage_map.py --freeze     # (re)write data/coverage-map/coverage.json
    python3 scripts/signal_coverage_map.py --check      # re-derive; FAIL if coverage.json drifted
    python3 scripts/signal_coverage_map.py --selftest   # classifier-integrity tests (no corpus needed)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from corpus_redundancy import SOURCES, agency_of  # reuse the CORPUS_SOURCES registry (single source of truth)

PIN_PATH = ROOT / "data" / "coverage-map" / "substrate-pin.json"
COVERAGE_PATH = ROOT / "data" / "coverage-map" / "coverage.json"
EMISSION_PATH = ROOT / "data" / "chain-cases" / "CASE-P-0010361" / "bundle.json"
TAXONOMY_PATH = ROOT / "data" / "capability-taxonomy.json"

TIERS = ["reachable-now", "needs-detector", "needs-view-exposure", "needs-behavior", "out-of-reach"]


# --------------------------------------------------------------------------- loaders

def load_pin() -> dict:
    return json.loads(PIN_PATH.read_text(encoding="utf-8"))


def load_taxonomy() -> tuple[dict, dict]:
    """code -> name for capabilities (C*) and data sources (D*)."""
    tax = json.loads(TAXONOMY_PATH.read_text(encoding="utf-8"))
    caps = {c["id"]: c["name"] for c in tax.get("capabilities", [])}
    dss = {d["id"]: d["name"] for d in tax.get("data_sources", [])}
    return caps, dss


def load_buildable() -> list[dict]:
    """Every committed BUILDABLE indicator (status==gap AND data==available), with the corpus's own
    resolved typology (per-indicator override else doc-inherit) + capability/data_source."""
    tmap = json.loads((ROOT / "data" / "typology-map.json").read_text(encoding="utf-8"))["map"]
    imap = json.loads((ROOT / "data" / "indicator-typology-map.json").read_text(encoding="utf-8"))["map"]
    out: list[dict] = []
    for sid, ddir, _juris in SOURCES:
        for f in sorted(ddir.glob("*.json")):
            rec = json.loads(f.read_text(encoding="utf-8"))
            doc_id = rec["id"]
            for ind in rec.get("indicators", []):
                if not (ind.get("status") == "gap" and ind.get("data") == "available"):
                    continue
                gid = f"{doc_id}/{ind['id']}"
                typ = imap.get(gid) or tmap.get(doc_id) or "(unmapped)"
                out.append({
                    "gid": gid, "source": sid, "agency": agency_of(sid),
                    "capability": ind.get("capability"), "data_source": ind.get("data_source"),
                    "typology": typ, "red_flag": ind.get("red_flag", ""),
                })
    return out


def measure_emission(bundle: dict) -> dict:
    """MEASURE observable activity from the real emitted sample (the gate's 'pinned real data')."""
    txns = bundle.get("transactions", [])
    fields = ["counterparty_account_id", "counterparty_ref", "counterparty_country", "currency", "amount_cents"]
    return {
        "n_txns": len(txns),
        "channels": sorted({t.get("channel") for t in txns if t.get("channel")}),
        "field_nonnull": {fld: sum(1 for t in txns if t.get(fld) is not None) for fld in fields},
        "alert_caps": sorted({a.get("capability") for a in bundle.get("alerts", []) if a.get("capability")}),
    }


# --------------------------------------------------------------------------- the classifier

def _probe_active(probe: str | None, emission: dict) -> bool:
    """Is the data source's observable ACTIVE in the real emission? (measured)"""
    if not probe:
        return False
    if probe == "any_txn":
        return emission["n_txns"] > 0
    if probe.startswith("channel:"):
        wanted = set(probe.split(":", 1)[1].split("|"))
        return bool(wanted & set(emission["channels"]))
    if probe.startswith("field:"):
        return emission["field_nonnull"].get(probe.split(":", 1)[1], 0) > 0
    raise ValueError(f"unknown emission_probe: {probe}")


def substrate_class(d_code: str, pin: dict, emission: dict) -> str:
    """exposed-active | generated-unexposed | modeled-inactive | not-modeled.
    modeled/exposed are SCHEMA facts (pin, code-verified); active is MEASURED against the emission."""
    ds = pin["data_sources"][d_code]
    if not ds["modeled"]:
        return "not-modeled"
    if not ds["exposed"]:
        return "generated-unexposed"
    return "exposed-active" if _probe_active(ds["emission_probe"], emission) else "modeled-inactive"


def is_live(c_code: str, pin: dict) -> bool:
    cap = pin["capabilities"][c_code]
    return cap["has_detector"] and cap["has_casework_assertion"] and cap["behavior_emergence"] == "emerges"


def classify(c_code: str, d_code: str, pin: dict, emission: dict) -> tuple[str, str | None]:
    """-> (tier, grounding_mode). grounding_mode is set only for reachable-now."""
    sclass = substrate_class(d_code, pin, emission)
    if is_live(c_code, pin):
        return "reachable-now", ("direct" if sclass == "exposed-active" else "proxy")
    if sclass == "not-modeled":
        return "out-of-reach", None
    if sclass == "generated-unexposed":
        return "needs-view-exposure", None
    if sclass == "modeled-inactive":
        return "needs-behavior", None
    # exposed-active, not a live capability: needs-detector only if the behavior genuinely EMERGES
    # (an observable pattern a detector could catch). data-only/absent -> the engine must produce it first.
    if pin["capabilities"][c_code]["behavior_emergence"] == "emerges":
        return "needs-detector", None
    return "needs-behavior", None


# --------------------------------------------------------------------------- the coverage payload

def build_coverage(pin: dict, buildable: list[dict], emission: dict) -> dict:
    cap_names, ds_names = load_taxonomy()
    signals = []
    for ind in buildable:
        c, d = ind["capability"], ind["data_source"]
        tier, mode = classify(c, d, pin, emission)
        sclass = substrate_class(d, pin, emission)
        cap = pin["capabilities"].get(c, {})
        behavior_confirmed = c in emission["alert_caps"]  # fires in the real emission
        signals.append({
            "gid": ind["gid"], "source": ind["source"], "agency": ind["agency"],
            "capability": c, "data_source": d, "typology": ind["typology"],
            "tier": tier, "grounding_mode": mode,
            "data_source_class": sclass,
            "behavior_emergence": cap.get("behavior_emergence"),
            "behavior_confirmed": behavior_confirmed,
            "red_flag": ind["red_flag"],
        })
    signals.sort(key=lambda s: s["gid"])

    by_tier = {t: 0 for t in TIERS}
    by_mode = {"direct": 0, "proxy": 0}
    by_source: dict[str, dict] = {}
    by_typology: dict[str, dict] = {}
    for s in signals:
        by_tier[s["tier"]] += 1
        if s["tier"] == "reachable-now":
            by_mode[s["grounding_mode"]] += 1
        by_source.setdefault(s["source"], {t: 0 for t in TIERS})[s["tier"]] += 1
        by_typology.setdefault(s["typology"], {t: 0 for t in TIERS})[s["tier"]] += 1

    # per-capability ranking: how many buildable signals each capability carries, and how many it would
    # move to reachable-now if a detector+assertion were authored (i.e. its needs-detector signals).
    caps: dict[str, dict] = {}
    for s in signals:
        c = s["capability"]
        row = caps.setdefault(c, {
            "capability": c, "name": cap_names.get(c, "?"),
            "group": pin["capabilities"].get(c, {}).get("group", "?"),
            "live": is_live(c, pin), "total": 0,
            **{t: 0 for t in TIERS},
        })
        row["total"] += 1
        row[s["tier"]] += 1
    capability_ranking = sorted(
        caps.values(),
        key=lambda r: (r["needs-detector"], r["reachable-now"], r["total"]),
        reverse=True,
    )

    reachable = by_tier["reachable-now"]
    plus_detectors = reachable + by_tier["needs-detector"]

    return {
        "_comment": "GENERATED by scripts/signal_coverage_map.py (Phase 58). Re-derive: `--check`. NON-ship.",
        "meta": {
            "grounding_heads": pin["meta"]["grounding_heads"],
            "emission_sample": pin["meta"]["emission_sample"],
            "doctrine": pin["meta"]["doctrine"],
            "tier_definitions": {
                "reachable-now": "a live detector + casework assertion + emergent behavior grounds it (direct on exposed-active data, or via an exposed-transaction proxy)",
                "needs-detector": "exposed-active observable + behavior emerges/plausible, but no detector/assertion yet (the cheapest build)",
                "needs-view-exposure": "the observable is modeled but UNEXPOSED to the detector views",
                "needs-behavior": "exposed observable but the pattern never emerges, or modeled-but-never-populated (REASONED, behavior_confirmed=false)",
                "out-of-reach": "the data source is not modeled / a dead never-set flag -- the substrate genuinely cannot observe it",
            },
            "measured_vs_reasoned": "data_source_class is MEASURED against the schema pin + the emission; behavior_emergence is REASONED from DESIGN.md/gen (behavior_confirmed=true only when the capability fires in the emission)",
        },
        "emission_measured": emission,
        "data_source_classes": {d: substrate_class(d, pin, emission) for d in sorted(pin["data_sources"])},
        "summary": {
            "total_buildable": len(signals),
            "by_tier": by_tier,
            "reachable_now_by_mode": by_mode,
            "path_to_200plus": {
                "reachable_now": reachable,
                "detector_only_total": plus_detectors,
                "then_via_view_exposure": by_tier["needs-view-exposure"],
                "remaining_needs_behavior": by_tier["needs-behavior"],
                "out_of_reach": by_tier["out-of-reach"],
                "note": (
                    f"{plus_detectors} are buildable with DETECTOR-work alone on the current emergent data "
                    f"({reachable} live + {by_tier['needs-detector']} new detectors on exposed-active observables). "
                    "Exceeding 200 goes through VIEW-EXPOSURE: {0} signals' data is GENERATED BY THE SUBSTRATE "
                    "BUT INVISIBLE to the detector views (no party view; detail tables) -- the dominant lever is "
                    "exposing data the substrate ALREADY produces, not designing new data. Each then needs a "
                    "screening/behavioral detector (behavior_emergence carries the secondary gap). needs-behavior "
                    "requires emergence-engine work; out-of-reach is genuinely unobservable. Capability-scaled, "
                    "NOT 200 detector implementations."
                ).format(by_tier["needs-view-exposure"]),
            },
            "by_source": by_source,
            "by_typology": dict(sorted(by_typology.items())),
        },
        "capability_ranking": capability_ranking,
        "signals": signals,
    }


def serialize(coverage: dict) -> str:
    return json.dumps(coverage, indent=2, ensure_ascii=False) + "\n"


# --------------------------------------------------------------------------- report

def report(coverage: dict) -> str:
    s = coverage["summary"]
    heads = coverage["meta"]["grounding_heads"]
    lines = [
        "CORPUS -> SUBSTRATE SIGNAL-COVERAGE MAP  (Phase 58, Illustrative data & outputs)",
        f"  grounded: aml-substrate@{heads['aml_substrate']} - aml-casework@{heads['aml_casework']} - corpus@{heads['signal_watch_corpus']}",
        f"  buildable corpus indicators (status==gap AND data==available): {s['total_buildable']}",
        "",
        "  REACHABILITY ON THE CURRENT SUBSTRATE (measured observable / reasoned behavior):",
    ]
    for t in TIERS:
        n = s["by_tier"][t]
        pct = (100.0 * n / s["total_buildable"]) if s["total_buildable"] else 0.0
        lines.append(f"    {t:<20} {n:>4}  ({pct:4.1f}%)")
    m = s["reachable_now_by_mode"]
    lines += [
        f"      (reachable-now: {m['direct']} direct + {m['proxy']} via transaction-proxy grounding)",
        "",
        "  PATH TO 200+ GROUNDED SIGNALS (capability-scaled, honest about each gap):",
        f"    reachable now (live detectors) ............... {s['path_to_200plus']['reachable_now']}",
        f"    detector-only on exposed emergent data ...... {s['path_to_200plus']['detector_only_total']}",
        f"    then via VIEW-EXPOSURE (data generated, unseen) +{s['path_to_200plus']['then_via_view_exposure']}",
        f"    remaining needs-behavior / out-of-reach ..... {s['path_to_200plus']['remaining_needs_behavior']} / {s['path_to_200plus']['out_of_reach']}",
        "    >> the dominant lever is EXPOSING data the substrate already generates, not designing new data.",
        "",
        "  TOP CAPABILITIES TO WIRE (by needs-detector signals unlocked):",
    ]
    for r in coverage["capability_ranking"]:
        if r["live"] or r["needs-detector"] == 0:
            continue
        lines.append(f"    {r['capability']:<4} {r['name'][:48]:<48} +{r['needs-detector']:>3} signals")
    lines += ["", "  LIVE CAPABILITIES (reachable-now today):"]
    for r in coverage["capability_ranking"]:
        if r["live"]:
            lines.append(f"    {r['capability']:<4} {r['name'][:48]:<48} {r['reachable-now']:>4} signals")
    return "\n".join(lines)


# --------------------------------------------------------------------------- selftest

def selftest() -> None:
    pin = load_pin()
    emission = measure_emission(json.loads(EMISSION_PATH.read_text(encoding="utf-8")))
    fails: list[str] = []

    def check(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    # 1. measured substrate_class ties to the REAL emission + the pin (not hardcoded)
    check(substrate_class("D1", pin, emission) == "exposed-active", "D1 should be exposed-active")
    check(substrate_class("D2", pin, emission) == "exposed-active", "D2 (CASH channel present) should be exposed-active")
    check(substrate_class("D3", pin, emission) == "exposed-active", "D3 (WIRE/EMT/AFT present) should be exposed-active")
    check(substrate_class("D8", pin, emission) == "modeled-inactive", "D8 (KYC exposed via PartyView @5875241, but the txn-only emission carries no party rows) should be modeled-inactive")
    check(substrate_class("D17", pin, emission) == "modeled-inactive", "D17 (counterparty_country 0/71) should be modeled-inactive")
    check(substrate_class("D7", pin, emission) == "not-modeled", "D7 (VC) should be not-modeled")
    check(substrate_class("D13", pin, emission) == "not-modeled", "D13 (adverse-media dead flag) should be not-modeled")

    # 2. the emission MEASUREMENT is real: D17 flips to exposed-active iff counterparty_country gets populated
    tampered = {**emission, "field_nonnull": {**emission["field_nonnull"], "counterparty_country": 5}}
    check(substrate_class("D17", pin, tampered) == "exposed-active",
          "D17 must flip to exposed-active when the emission populates counterparty_country (classifier must read the emission)")

    # 3. the live capabilities are exactly the 5 that fire in the emission's alerts
    live = {c for c in pin["capabilities"] if is_live(c, pin)}
    check(live == {"C2", "C3", "C4", "C5", "C15"}, f"live set should be C2/C3/C4/C5/C15, got {sorted(live)}")
    check(set(emission["alert_caps"]) <= live, "every emission alert capability must be classified live")
    check(not is_live("C6", pin), "C6 has a detector but NO casework assertion AND behavior absent -> not live")

    # 4. live grounding modes: direct on exposed-active data, proxy on unexposed/dead (bundle-validated)
    check(classify("C4", "D2", pin, emission) == ("reachable-now", "direct"), "C4/D2 should be reachable-now/direct")
    check(classify("C3", "D13", pin, emission) == ("reachable-now", "proxy"), "C3/D13 should be reachable-now/proxy (funnel via txns)")
    check(classify("C15", "D8", pin, emission) == ("reachable-now", "proxy"), "C15/D8 should be reachable-now/proxy (shell via throughput)")

    # 5. a FABRICATED reachable-now must fail -- the cascade catches non-live caps on dead data
    check(classify("C21", "D7", pin, emission)[0] == "out-of-reach", "C21/D7 (VC) must be out-of-reach, never reachable-now")
    check(classify("C18", "D11", pin, emission)[0] == "out-of-reach", "C18/D11 (sanctions, dead flag) must be out-of-reach")
    check(classify("C16", "D1", pin, emission)[0] == "needs-detector", "C16/D1 (third-party, emergent on exposed txns, no detector) -> needs-detector")
    check(classify("C7", "D1", pin, emission)[0] == "needs-detector", "C7/D1 (peer-anomaly, emergent via separability, no detector) -> needs-detector")
    check(classify("C13", "D8", pin, emission)[0] == "needs-behavior", "C13/D8 (KYC exposed via PartyView but unmeasurable on the txn-only emission -> modeled-inactive) -> needs-behavior")
    check(classify("C6", "D1", pin, emission)[0] == "needs-behavior", "C6/D1 (dormancy behavior absent) -> needs-behavior")
    check(classify("C8", "D1", pin, emission)[0] == "needs-behavior", "C8/D1 (income-mismatch data-only, no emergent observable pattern) -> needs-behavior")

    # 6. cover the closed sets + determinism
    for c in pin["capabilities"]:
        for d in pin["data_sources"]:
            tier, mode = classify(c, d, pin, emission)
            check(tier in TIERS, f"{c}/{d} produced an unknown tier {tier}")
            check((mode is not None) == (tier == "reachable-now"), f"{c}/{d}: grounding_mode set iff reachable-now")
    buildable = load_buildable()
    cov1, cov2 = build_coverage(pin, buildable, emission), build_coverage(pin, buildable, emission)
    check(serialize(cov1) == serialize(cov2), "build_coverage must be deterministic")
    check(cov1["summary"]["total_buildable"] == len(buildable), "every buildable indicator must be classified")

    if fails:
        print("SELFTEST FAILED:")
        for fmsg in fails:
            print("  -", fmsg)
        sys.exit(1)
    print(f"SELFTEST PASSED ({len(buildable)} buildable indicators classified; "
          f"live={sorted(live)}; emission n_txns={emission['n_txns']}, channels={emission['channels']})")


# --------------------------------------------------------------------------- main

def _derive() -> dict:
    pin = load_pin()
    emission = measure_emission(json.loads(EMISSION_PATH.read_text(encoding="utf-8")))
    return build_coverage(pin, load_buildable(), emission)


def main(argv: list[str]) -> None:
    if "--selftest" in argv:
        selftest()
        return
    coverage = _derive()
    if "--json" in argv:
        sys.stdout.write(serialize(coverage))
    elif "--freeze" in argv:
        COVERAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
        COVERAGE_PATH.write_text(serialize(coverage), encoding="utf-8")
        print(f"FROZE {COVERAGE_PATH.relative_to(ROOT)} ({coverage['summary']['total_buildable']} signals)")
    elif "--check" in argv:
        if not COVERAGE_PATH.exists():
            print(f"CHECK FAILED: {COVERAGE_PATH.relative_to(ROOT)} missing -- run --freeze")
            sys.exit(1)
        got, want = serialize(coverage), COVERAGE_PATH.read_text(encoding="utf-8")
        if got != want:
            print(f"CHECK FAILED: {COVERAGE_PATH.relative_to(ROOT)} drifted from a fresh derivation (re-freeze if intended)")
            sys.exit(1)
        print(f"CHECK OK: {COVERAGE_PATH.relative_to(ROOT)} byte-identical ({coverage['summary']['total_buildable']} signals)")
    else:
        print(report(coverage))


if __name__ == "__main__":
    main(sys.argv[1:])
