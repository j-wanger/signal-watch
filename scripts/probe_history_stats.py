#!/usr/bin/env python3
"""Phase-48 history-decomposition probe — deterministic stats (stdlib-only).

Aggregates the probe material in data/probe-history/ (an invented legacy TM rulebook
decomposed through the UNCHANGED derivation gate, plus an alert/disposition history) into
measurement-DEFINED numbers for docs/probe-history.md. Every emitted metric line carries its
"definition:" — the no-unmeasured-number rule (program blueprint §9/§10).

Two history sources (Phase 62):
  default        — the SYNTHETIC Phase-48 fixture (data/probe-history/alert-history.json).
  --grounded     — the GROUNDED substrate probe-history (data/probe-history/grounded/), produced
                   by the aml-substrate P22 projector (pinned in grounded/provenance.json).
  --selftest     — validate the capability->TM map (closed vocab + inversion faithfulness).

HONESTY (the Phase-62 A3 split): in --grounded mode the alert FIRINGS are REAL label-blind
detector output (which entity, which capability, the count, the near-misses), but the
DISPOSITIONS are ILLUSTRATIVE (the substrate's chosen-not-measured §7 operating-funnel shape,
seeded from observable alert content, never the hidden label). So firing-derived metrics
(alerts_total, silent_rules, below_the_line_count) are GROUNDED; disposition-derived metrics
(re_review / inconsistency / data_gap / escalation) measure the ILLUSTRATIVE disposition
process, NOT real analyst behaviour. History is evidence, never ground truth.

This script reads ONLY data/probe-history/ + data/capability-taxonomy.json and is never imported
by build.py or the engine.
"""
import argparse
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROBE = ROOT / "data" / "probe-history"
SYNTH = PROBE / "alert-history.json"
GROUNDED = PROBE / "grounded" / "alert-history.json"
CTM_MAP = PROBE / "capability-tm-map.json"
RULEBOOK = PROBE / "derived" / "legacy-rulebook.json"
TAXONOMY = ROOT / "data" / "capability-taxonomy.json"

# The substrate's per-account detector capabilities (what the projector can emit to the
# probe-history). Grounded in capability-tm-map.json's scope_note + the P22 projector
# (ALL_DETECTORS per-account set). Screening caps (C7/C8/C14/C26) flow to evidence bundles,
# not the per-account probe-history, so they are out of scope here.
SUBSTRATE_PERACCOUNT_CAPS = {"C2", "C3", "C4", "C5", "C6", "C15"}


# ---------------------------------------------------------------------------- shared helpers
def _rulebook_indicators() -> list:
    return json.loads(RULEBOOK.read_text())["indicators"]


def _tm_of(section: str) -> str:
    import re
    m = re.search(r"(TM-\d+)", section)
    return m.group(1) if m else "?"


def _tm_to_capability() -> dict:
    """TM-### -> capability C-code, from the committed rulebook."""
    return {_tm_of(i["section"]): i["capability"] for i in _rulebook_indicators()}


def _disposition_counts(alerts: list) -> dict:
    disp: dict = defaultdict(int)
    for a in alerts:
        disp[a["disposition"]] += 1
    return disp


def _re_review(alerts: list) -> int:
    seen_dismissed: set = set()
    rereview = 0
    for a in sorted(alerts, key=lambda x: x["date"]):
        key = (a["entity_id"], a["rule_id"])
        if key in seen_dismissed:
            rereview += 1
        if a["disposition"] == "dismissed":
            seen_dismissed.add(key)
    return rereview


def _inconsistency(alerts: list):
    by_rule: dict = defaultdict(list)
    for a in alerts:
        d = "escalated" if a["disposition"] == "sar_filed" else a["disposition"]
        by_rule[a["rule_id"]].append(d)
    multi = {r: ds for r, ds in by_rule.items() if len(ds) >= 2}
    inconsistent = {r for r, ds in multi.items() if len(set(ds)) >= 2}
    return inconsistent, multi


# ---------------------------------------------------------------------------- role 1 (shared)
def _print_role1(inds: list) -> None:
    by_rec: dict = defaultdict(int)
    for i in inds:
        by_rec[i["build_rec"]] += 1
    mix = " · ".join(f"{k} {v}" for k, v in sorted(by_rec.items()))
    print(f"rules_decomposed: {len(inds)}")
    print("  definition: count of legacy rules whose Indicator sentence passed the UNCHANGED "
          "derivation gate (check_record: quote-grounding in rf_region + cover×data matrix + "
          "red_flag shape), out of 12 authored rules.")
    print(f"coverage_map: {mix}")
    print("  definition: per-rule build_rec derived DETERMINISTICALLY from the agent-proposed "
          "C/D code and the committed Phase-28 interview posture via the cover×data matrix "
          "(the ph33_apply downstream) — no neural coverage authoring.")
    caps_unfired = "C-codes with no legacy rule: " + str(28 - len({i["capability"] for i in inds}))
    print(f"capability_spread: {len({i['capability'] for i in inds})} distinct C-codes, "
          f"{len({i['data_source'] for i in inds})} distinct D-codes ({caps_unfired})")
    print("  definition: distinct capability / data-source codes across the decomposed rules; "
          "the unfired count is the modern-taxonomy surface the legacy rulebook never reached "
          "(a coverage statement about the RULEBOOK, not about risk).")
    print()


# ---------------------------------------------------------------------------------- synthetic
def report_synthetic() -> int:
    inds = _rulebook_indicators()
    alerts = json.loads(SYNTH.read_text())["alerts"]

    print("PHASE-48 HISTORY-DECOMPOSITION PROBE — SYNTHETIC material, measurement-defined stats")
    print()
    _print_role1(inds)

    n = len(alerts)
    disp = _disposition_counts(alerts)
    print(f"alerts_total: {n} across {len({a['rule_id'] for a in alerts})} rules "
          f"({', '.join(f'{k}={v}' for k, v in sorted(disp.items()))})")
    print("  definition: row count of the synthetic alert history; dispositions are authored "
          "fixture values, not analyst behaviour.")

    rereview = _re_review(alerts)
    print(f"re_review_rate: {rereview}/{n} = {rereview / n:.1%}")
    print("  definition: share of alerts whose (entity, rule) pair had at least one EARLIER "
          "dismissed alert — the already-reviewed-and-discounted class the adjudication-history "
          "feedback fold deprioritizes.")

    inconsistent, multi = _inconsistency(alerts)
    print(f"disposition_inconsistency_rate: {len(inconsistent)}/{len(multi)} = "
          f"{len(inconsistent) / len(multi):.1%} (rules: {', '.join(sorted(inconsistent))})")
    print("  definition: among rules with >=2 alerts, the share whose alerts carry >=2 distinct "
          "dispositions (sar_filed folded into escalated); a PROCESS-INCONSISTENCY signal "
          "surfaced for adjudication — never auto-resolved, never a correctness claim.")

    dr = disp.get("data_requested", 0)
    print(f"data_gap_rate: {dr}/{n} = {dr / n:.1%}")
    print("  definition: share of alerts dispositioned data_requested — the need-more-information "
          "class the continuous adjudication loop (blueprint §14) wires into the C/D coverage "
          "model as measured data-gap observations.")

    esc = disp.get("escalated", 0) + disp.get("sar_filed", 0)
    print(f"alert_to_escalation_rate: {esc}/{n} = {esc / n:.1%} "
          f"(sar_filed: {disp.get('sar_filed', 0)})")
    print("  definition: share of alerts escalated or filed — the legacy rulebook's yield over "
          "this synthetic history; the §6 A/B baseline a candidate signal must beat on the same "
          "population.")

    fired = {a["rule_id"] for a in alerts}
    silent = sorted({f"TM-{101 + k}" for k in range(12)} - fired)
    print(f"silent_rules: {len(silent)}/12 ({', '.join(silent)})")
    print("  definition: authored rules with zero alerts in the synthetic history — at adoption, "
          "a real silent rule is itself a finding (dead rule, threshold, or data feed).")
    return 0


# ----------------------------------------------------------------------------------- grounded
def _grounded_silent(fired_ccodes: set, ctm: dict):
    """Capability-level silence: TM rules whose capability never fired. Returns
    (silent_tm_sorted, fired_but_unmapped_ccodes)."""
    cap_to_tm = ctm["capability_to_tm"]
    universe = set(ctm["tm_universe"])
    fired_tm: set = set()
    unmapped: list = []
    for c in sorted(fired_ccodes):
        tms = cap_to_tm.get(c)
        if tms is None:
            unmapped.append(c)            # off-vocab C-code (selftest catches this case)
        elif tms == []:
            unmapped.append(c)            # honest null (e.g. C15 — substrate ahead of rulebook)
        else:
            fired_tm |= set(tms)
    return sorted(universe - fired_tm), unmapped


def report_grounded() -> int:
    if not GROUNDED.exists():
        print(f"error: grounded probe-history not found at {GROUNDED} (run the substrate P22 "
              f"projector — see data/probe-history/grounded/provenance.json)")
        return 1
    inds = _rulebook_indicators()
    ctm = json.loads(CTM_MAP.read_text())
    history = json.loads(GROUNDED.read_text())
    alerts = history["alerts"]
    below = history.get("below_the_line", [])
    tm_cap = _tm_to_capability()

    pin = json.loads((PROBE / "grounded" / "provenance.json").read_text())["substrate_pin"]
    print("PHASE-62 GROUNDED PROBE-HISTORY — measurement-defined stats")
    print(f"  source: aml-substrate@{pin['head_short']} ({pin['phase']}); meta.synthetic=true.")
    print("  HONESTY (A3 split): alert FIRINGS are REAL label-blind detector output; DISPOSITIONS "
          "are ILLUSTRATIVE (chosen-not-measured, never the hidden label). Firing-derived metrics "
          "are GROUNDED; disposition-derived metrics measure the ILLUSTRATIVE process, not analyst "
          "behaviour. History is evidence, never ground truth.")
    print()
    _print_role1(inds)

    n = len(alerts)
    disp = _disposition_counts(alerts)
    print(f"alerts_total: {n} across {len({a['rule_id'] for a in alerts})} capabilities "
          f"({', '.join(f'{k}={v}' for k, v in sorted(disp.items()))})  [GROUNDED firing]")
    print("  definition: row count of the GROUNDED alert history (real label-blind detector "
          "firings); rule_id is a substrate capability C-code. Dispositions are illustrative.")

    rereview = _re_review(alerts)
    print(f"re_review_rate: {rereview}/{n} = {rereview / n:.1%}  [over illustrative dispositions]")
    print("  definition: share of alerts whose (entity, rule) pair had at least one EARLIER "
          "dismissed alert — the already-reviewed-and-discounted class. NOTE: computed over "
          "ILLUSTRATIVE dispositions, not measured analyst behaviour.")

    inconsistent, multi = _inconsistency(alerts)
    inc_rate = (len(inconsistent) / len(multi)) if multi else 0.0
    print(f"disposition_inconsistency_rate: {len(inconsistent)}/{len(multi)} = {inc_rate:.1%}  "
          f"[over illustrative dispositions]")
    print("  definition: among capabilities with >=2 alerts, the share whose alerts carry >=2 "
          "distinct dispositions (sar_filed folded into escalated). NOTE: a near-1.0 value here "
          "reflects the illustrative disposition SEED's spread over many alerts/capability, not a "
          "measured analyst inconsistency — a structural artefact, surfaced not hidden.")

    dr = disp.get("data_requested", 0)
    print(f"data_gap_rate: {dr}/{n} = {dr / n:.1%}  [over illustrative dispositions]")
    print("  definition: share of alerts dispositioned data_requested — the need-more-information "
          "class. NOTE: illustrative disposition seed, not measured.")

    esc = disp.get("escalated", 0) + disp.get("sar_filed", 0)
    print(f"alert_to_escalation_rate: {esc}/{n} = {esc / n:.1%} (sar_filed: "
          f"{disp.get('sar_filed', 0)})  [over illustrative dispositions]")
    print("  definition: share of alerts escalated or filed — the illustrative §7 operating-funnel "
          "shape (chosen-not-measured); the §6 A/B baseline frame, NOT a measured legacy yield.")

    # silent_rules — GROUNDED (capability-level)
    fired = {a["rule_id"] for a in alerts}
    silent, unmapped = _grounded_silent(fired, ctm)
    no_detector = sorted(t for t in silent if tm_cap.get(t) not in SUBSTRATE_PERACCOUNT_CAPS)
    not_fired = sorted(t for t in silent if tm_cap.get(t) in SUBSTRATE_PERACCOUNT_CAPS)
    print(f"silent_rules: {len(silent)}/12 ({', '.join(silent)})  [GROUNDED capability-level]")
    print("  definition: legacy TM rules whose CAPABILITY never fired in the grounded history "
          "(CAPABILITY-level silence — the substrate detects per-capability, not per-rule-variant; "
          "see capability-tm-map.json).")
    print(f"  breakdown: {len(not_fired)} have a substrate detector that did NOT fire at this build "
          f"(caps {', '.join(sorted({tm_cap[t] for t in not_fired})) or '—'}: {', '.join(not_fired) or '—'}); "
          f"{len(no_detector)} have NO substrate detector "
          f"(caps {', '.join(sorted({tm_cap[t] for t in no_detector})) or '—'} — un-built: {', '.join(no_detector) or '—'}).")
    null_fired = sorted(c for c in unmapped if ctm["capability_to_tm"].get(c) == [])
    if null_fired:
        print(f"  honest-null: capabilities that FIRED but map to NO legacy rule: "
              f"{', '.join(null_fired)} (substrate capability AHEAD of the legacy rulebook).")

    # below_the_line_count — GROUNDED (new 6th metric; absent from the synthetic fixture)
    print(f"below_the_line_count: {len(below)}  [GROUNDED firing]")
    print("  definition: history-below-the-line near-misses (peak == threshold-1 on a "
          "never-surfaced account) — the §14 false-negative-discovery stratum source. A measured "
          "count (0 at this build means the near-miss sampler found no qualifying accounts at this "
          "seed/scale — an honest 0, not an omission).")
    return 0


# ----------------------------------------------------------------------------------- selftest
def selftest() -> int:
    """Validate the capability->TM map: closed vocab + inversion faithfulness + coverage."""
    errs: list = []
    ctm = json.loads(CTM_MAP.read_text())
    inds = _rulebook_indicators()
    tm_cap = _tm_to_capability()
    rulebook_tms = set(tm_cap)
    taxonomy_codes = {c["id"] for c in json.loads(TAXONOMY.read_text())["capabilities"]}
    cap_to_tm = ctm["capability_to_tm"]
    universe = set(ctm["tm_universe"])

    # 1. tm_universe == the rulebook's 12 TM ids
    if universe != rulebook_tms:
        errs.append(f"tm_universe {sorted(universe)} != rulebook TM ids {sorted(rulebook_tms)}")
    # 2. every C-code key exists in the taxonomy
    for c in cap_to_tm:
        if c not in taxonomy_codes:
            errs.append(f"map C-code {c} not in capability-taxonomy.json")
    # 3. every mapped TM id exists in the rulebook; inversion is faithful (TM's cap == its key)
    for c, tms in cap_to_tm.items():
        for t in tms:
            if t not in rulebook_tms:
                errs.append(f"map {c} -> {t}: TM not in rulebook")
            elif tm_cap[t] != c:
                errs.append(f"inversion broken: {c} -> {t} but rulebook says {t} is {tm_cap[t]}")
    # 4. honest_nulls keys are exactly the map keys whose value is []
    declared_null = set(ctm.get("honest_nulls", {}))
    empty_keys = {c for c, tms in cap_to_tm.items() if tms == []}
    if declared_null != empty_keys:
        errs.append(f"honest_nulls {sorted(declared_null)} != empty-value keys {sorted(empty_keys)}")
    # 5. EVERY capability the substrate can emit is a map key (no silent drop), and every
    #    C-code present in the grounded history resolves (closed-vocab coverage)
    for c in SUBSTRATE_PERACCOUNT_CAPS:
        if c not in cap_to_tm:
            errs.append(f"substrate-emittable capability {c} missing from the map")
    if GROUNDED.exists():
        fired = {a["rule_id"] for a in json.loads(GROUNDED.read_text())["alerts"]}
        for c in sorted(fired):
            if c not in cap_to_tm:
                errs.append(f"grounded-history capability {c} not resolved by the map")

    if errs:
        print("probe_history_stats --selftest: FAIL")
        for e in errs:
            print(f"  - {e}")
        return 1
    print("probe_history_stats --selftest: PASS")
    print(f"  capability->TM map grounded vs rulebook ({len(rulebook_tms)} TM ids) + taxonomy "
          f"({len(taxonomy_codes)} C-codes); inversion faithful; {len(empty_keys)} honest-null "
          f"({', '.join(sorted(empty_keys)) or '—'}); all {len(SUBSTRATE_PERACCOUNT_CAPS)} "
          "substrate-emittable caps resolved.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--grounded", action="store_true",
                   help="measure the GROUNDED substrate probe-history (data/probe-history/grounded/)")
    g.add_argument("--selftest", action="store_true",
                   help="validate the capability->TM map (closed vocab + inversion faithfulness)")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if args.grounded:
        return report_grounded()
    return report_synthetic()


if __name__ == "__main__":
    raise SystemExit(main())
