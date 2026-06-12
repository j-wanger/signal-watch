#!/usr/bin/env python3
"""Phase-48 history-decomposition probe — deterministic stats (stdlib-only).

Aggregates the SYNTHETIC probe material in data/probe-history/ (an invented legacy TM
rulebook decomposed through the UNCHANGED derivation gate, plus an invented alert/disposition
history) into measurement-DEFINED numbers for docs/probe-history.md. Every emitted metric
line carries its "definition:" — the no-unmeasured-number rule (program blueprint §9/§10).

This script reads ONLY data/probe-history/ (synthetic; outside every build.py-read path) and
is never imported by build.py or the engine. History is evidence, never ground truth: the
disposition stats below measure what the fictitious institution DECIDED, not what was correct.
"""
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROBE = ROOT / "data" / "probe-history"


def main() -> int:
    derived = json.loads((PROBE / "derived" / "legacy-rulebook.json").read_text())
    history = json.loads((PROBE / "alert-history.json").read_text())
    inds = derived["indicators"]
    alerts = history["alerts"]

    print("PHASE-48 HISTORY-DECOMPOSITION PROBE — SYNTHETIC material, measurement-defined stats")
    print()

    # --- Role 1: decomposition coverage map ---
    by_rec = defaultdict(int)
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

    # --- Role 2: baseline stats over the synthetic alert history ---
    n = len(alerts)
    disp = defaultdict(int)
    for a in alerts:
        disp[a["disposition"]] += 1
    print(f"alerts_total: {n} across {len({a['rule_id'] for a in alerts})} rules "
          f"({', '.join(f'{k}={v}' for k, v in sorted(disp.items()))})")
    print("  definition: row count of the synthetic alert history; dispositions are authored "
          "fixture values, not analyst behaviour.")

    # re-review rate: alert whose (entity, rule) pair already had a prior DISMISSED alert
    seen_dismissed: set = set()
    rereview = 0
    for a in sorted(alerts, key=lambda x: x["date"]):
        key = (a["entity_id"], a["rule_id"])
        if key in seen_dismissed:
            rereview += 1
        if a["disposition"] == "dismissed":
            seen_dismissed.add(key)
    print(f"re_review_rate: {rereview}/{n} = {rereview / n:.1%}")
    print("  definition: share of alerts whose (entity, rule) pair had at least one EARLIER "
          "dismissed alert — the already-reviewed-and-discounted class the adjudication-history "
          "feedback fold deprioritizes.")

    # disposition-inconsistency rate: rules with >=2 alerts carrying >=2 distinct dispositions,
    # counting sar_filed as escalated (an escalation that progressed, not a divergent call)
    by_rule = defaultdict(list)
    for a in alerts:
        d = "escalated" if a["disposition"] == "sar_filed" else a["disposition"]
        by_rule[a["rule_id"]].append(d)
    multi = {r: ds for r, ds in by_rule.items() if len(ds) >= 2}
    inconsistent = {r for r, ds in multi.items() if len(set(ds)) >= 2}
    print(f"disposition_inconsistency_rate: {len(inconsistent)}/{len(multi)} = "
          f"{len(inconsistent) / len(multi):.1%} (rules: {', '.join(sorted(inconsistent))})")
    print("  definition: among rules with >=2 alerts, the share whose alerts carry >=2 distinct "
          "dispositions (sar_filed folded into escalated); a PROCESS-INCONSISTENCY signal "
          "surfaced for adjudication — never auto-resolved, never a correctness claim.")

    # data-gap rate: the need-more-information class
    dr = disp.get("data_requested", 0)
    print(f"data_gap_rate: {dr}/{n} = {dr / n:.1%}")
    print("  definition: share of alerts dispositioned data_requested — the need-more-information "
          "class the continuous adjudication loop (blueprint §14) wires into the C/D coverage "
          "model as measured data-gap observations.")

    # alert-to-escalation: the legacy yield
    esc = disp.get("escalated", 0) + disp.get("sar_filed", 0)
    print(f"alert_to_escalation_rate: {esc}/{n} = {esc / n:.1%} "
          f"(sar_filed: {disp.get('sar_filed', 0)})")
    print("  definition: share of alerts escalated or filed — the legacy rulebook's yield over "
          "this synthetic history; the §6 A/B baseline a candidate signal must beat on the same "
          "population.")

    # rules with alerts vs rules decomposed
    fired = {a["rule_id"] for a in alerts}
    silent = sorted({f"TM-{101 + k}" for k in range(12)} - fired)
    print(f"silent_rules: {len(silent)}/12 ({', '.join(silent)})")
    print("  definition: authored rules with zero alerts in the synthetic history — at adoption, "
          "a real silent rule is itself a finding (dead rule, threshold, or data feed).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
