#!/usr/bin/env python3
"""Curate the Phase-49 triage-console scenario dataset (deterministic, regeneration-only).

AUTHORING-TIME tool (the curate_console_cases.py precedent): reads
data/probe-history/{legacy-rulebook.md, derived/legacy-rulebook.json, alert-history.json}
plus the US-federal-allowlisted committed corpus derived records, and emits the
SELF-CONTAINED committed dataset data/triage/scenarios.json (rule text + signals + novel
indicator text EMBEDDED — build.py never reads data/probe-history).

Everything is SYNTHETIC (the probe-history fixture is synthetic by construction; every
customer, figure, and panel here is invented). The synthetic-novel stratum quotes committed
corpus indicators from US FEDERAL sources only (public domain, 17 U.S.C. §105) — enforced by
US_FEDERAL_ALLOWLIST below.

Usage:
  python3 scripts/curate_triage_scenarios.py            # regenerate data/triage/scenarios.json
  python3 scripts/curate_triage_scenarios.py --selftest # validator + determinism fixtures, no write
"""

import copy
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = ROOT / "data" / "triage" / "scenarios.json"

STRATA = [
    "history-signal-fired",
    "history-below-the-line",
    "synthetic-novel",
    "random-population",
]
# The §14 disposition grammar incl. the need-more-info option and the policy-gap escape.
DISPOSITION_GRAMMAR = [
    "confirm-risk",
    "confirm-no-risk",
    "both-defensible",
    "escalate",
    "need-more-info",
    "no-defensible-option",
]
HISTORY_DISPOSITIONS = ["dismissed", "escalated", "sar_filed", "data_requested"]

# US-federal sources ONLY (public domain, 17 U.S.C. §105) — the novel stratum never quotes
# FINTRAC or any other non-US-federal source (D6: no footer machinery in this artifact).
US_FEDERAL_ALLOWLIST = {
    "fin-2022-a002": "data/fincen",
    "ofac-virtual-currency": "data/ofac",
    "fin-2023-alert004": "data/fincen-alerts",
}
NOVEL_PICKS = [
    ("fin-2022-a002", "IND-02"),
    ("ofac-virtual-currency", "IND-02"),
    ("fin-2023-alert004", "IND-01"),
]


# ---------------------------------------------------------------- source readers

def read_rules():
    """Parse the synthetic rulebook md into {rule_id: {title, logic, indicator}}."""
    md = (ROOT / "data" / "probe-history" / "legacy-rulebook.md").read_text(encoding="utf-8")
    rules = {}
    pattern = re.compile(
        r"\*\*Rule (TM-\d+) — (.+?)\.\*\*\n"
        r"Logic: (.*?)\n"
        r"Indicator: (.*?)(?=\n\n|\Z)",
        re.DOTALL,
    )
    for m in pattern.finditer(md):
        rid, title, logic, indicator = m.groups()
        rules[rid] = {
            "title": title.strip(),
            "logic": " ".join(logic.split()),
            "indicator": " ".join(indicator.split()),
        }
    return rules


def read_signals():
    """Map rule_id -> the grounded signal from the probe derived record."""
    rec = json.loads(
        (ROOT / "data" / "probe-history" / "derived" / "legacy-rulebook.json").read_text(
            encoding="utf-8"
        )
    )
    signals = {}
    for ind in rec["indicators"]:
        m = re.search(r"\((TM-\d+)\)", ind["section"])
        if not m:
            raise ValueError(f"derived indicator {ind['id']} has no (TM-nnn) section tag")
        signals[m.group(1)] = {
            "red_flag": ind["red_flag"],
            "capability": ind["capability"],
            "data_source": ind["data_source"],
            "status": ind["status"],
            "build_rec": ind["build_rec"],
        }
    return signals


def read_alerts():
    h = json.loads(
        (ROOT / "data" / "probe-history" / "alert-history.json").read_text(encoding="utf-8")
    )
    return {a["alert_id"]: a for a in h["alerts"]}


def read_novel():
    """Embed the allowlisted US-federal novel indicators (verbatim flag + translation + C/D)."""
    novel = {}
    for doc_id, ind_id in NOVEL_PICKS:
        src_dir = US_FEDERAL_ALLOWLIST[doc_id]
        rec = json.loads(
            (ROOT / src_dir / "derived" / f"{doc_id}.json").read_text(encoding="utf-8")
        )
        ind = next(i for i in rec["indicators"] if i["id"] == ind_id)
        novel[f"{doc_id}/{ind_id}"] = {
            "doc_id": doc_id,
            "indicator_id": ind_id,
            "source_dir": src_dir,
            "flag": ind["flag"],
            "red_flag": ind["red_flag"],
            "capability": ind["capability"],
            "data_source": ind["data_source"],
            "licence": "US federal — public domain (17 U.S.C. §105)",
        }
    return novel


def read_taxonomy():
    tax = json.loads(
        (ROOT / "data" / "capability-taxonomy.json").read_text(encoding="utf-8")
    )
    caps = {c["id"] for c in tax["capabilities"]}
    srcs = {d["id"] for d in tax["data_sources"]}
    return caps, srcs


# ---------------------------------------------------------------- authored panels
# Template-derived skeletons: activity bullets concretize each rule's logic with synthetic
# figures; the authored layer (customer flavour + KYC note) is deliberately thin (D7).
# Panels are the FACT PATTERN unit — the TM-104 divergent pair SHARES P-HF-104 by reference.

PANELS = {
    "P-HF-104": {
        "skeleton": "TM-104 logic",
        "customer": "Personal account, 6-year tenure, salaried profile. SYNTHETIC.",
        "activity": [
            "Outbound wire $14,200 to a jurisdiction on the institution's high-risk country list.",
            "Customer profile records no business, family, or travel connection to the destination.",
            "Wire memo field: 'family support'. No prior wires to this corridor in account history.",
            "Account otherwise in pattern: salary credits, rent, card spend.",
        ],
        "kyc_note": "KYC current (refreshed 14 months ago); occupation: logistics coordinator; no documented overseas ties.",
    },
    "P-HF-101": {
        "skeleton": "TM-101 logic",
        "customer": "Personal account, 9-year tenure. SYNTHETIC.",
        "activity": [
            "Cash deposits $8,400 / $9,100 / $8,950 on three days within one week — each inside the $8,000–9,999 band.",
            "Pattern recurs monthly; this is the NINTH alert on this account for the same behaviour.",
            "All eight prior alerts dismissed (rationale on file each time: 'known cash-intensive side business').",
            "No CTR has ever been triggered; declared occupation: rideshare driver.",
        ],
        "kyc_note": "Profile lists a part-time cash side business (unregistered); expected cash volume field BLANK at onboarding.",
    },
    "P-HF-109": {
        "skeleton": "TM-109 logic",
        "customer": "Personal account opened 11 months ago. SYNTHETIC.",
        "activity": [
            "Cash deposits at branches in four cities across two provinces within 12 days ($3,000–6,500 each).",
            "Aggregate $23,800 consolidated, then a single wire out from a fifth city two days later.",
            "Depositor descriptions on branch slips do not consistently match the account holder.",
        ],
        "kyc_note": "Declared occupation: student. No employment income credits in account history.",
    },
    "P-HF-110": {
        "skeleton": "TM-110 logic",
        "customer": "Small-business account (import/export), 3-year tenure. SYNTHETIC.",
        "activity": [
            "Three incoming wires in 60 days with originator name fields truncated or filled with 'XXX'.",
            "Originating institutions in two different correspondent corridors.",
            "Funds applied to supplier payments consistent with the declared business line.",
        ],
        "kyc_note": "Beneficial ownership on file; counterparty list NOT on file — the institution does not collect expected-counterparty data for this segment.",
    },
    "P-HF-106": {
        "skeleton": "TM-106 logic",
        "customer": "Business account — convenience store, 7-year tenure. SYNTHETIC.",
        "activity": [
            "Monthly cash deposits at 240% and 265% of the onboarding-declared expected volume, two consecutive months.",
            "No change filed to the declared nature of business.",
            "Card-settlement credits flat over the same period (sales mix unchanged on the acquiring side).",
        ],
        "kyc_note": "Onboarding profile dated; last KYC refresh 4 years ago. A refresh request is the obvious next step — history shows the review PAUSED for exactly that.",
    },
    "P-HF-102": {
        "skeleton": "TM-102 logic",
        "customer": "Personal account, 2-year tenure. SYNTHETIC.",
        "activity": [
            "Incoming e-transfer $21,500, then $19,800 wired out 36 hours later (92% pass-through).",
            "Second cycle three weeks later: $24,000 in, $22,300 out within 40 hours.",
            "Residual balance after each cycle under $2,000. THIRD alert on this account this year; both priors dismissed ('expected property-deal flows').",
        ],
        "kyc_note": "Customer note from a prior review mentions 'acting for a relative buying property'; no documentation on file.",
    },
    "P-BT-101": {
        "skeleton": "below TM-101 thresholds",
        "customer": "Personal account, 5-year tenure. SYNTHETIC.",
        "activity": [
            "Cash deposits $7,400 / $7,900 / $7,650 across six days — each BELOW the rule's $8,000 floor.",
            "Same weekly rhythm as classic structuring, shifted down one band.",
            "No alert fired; the pattern is invisible to TM-101 as tuned.",
        ],
        "kyc_note": "Declared occupation: café owner; expected cash volume declared LOW at onboarding.",
    },
    "P-BT-112": {
        "skeleton": "below TM-112 thresholds",
        "customer": "Personal account, 4-year tenure. SYNTHETIC.",
        "activity": [
            "Remittances through two different MSB counterparties to the same beneficiary country: $2,950 + $2,900 + $2,700 in 30 days.",
            "Aggregate $8,550 — UNDER the rule's $9,000 aggregate trigger.",
            "Beneficiary name identical across all three; no alert fired.",
        ],
        "kyc_note": "Profile records family in the destination country (a documented connection).",
    },
    "P-BT-102": {
        "skeleton": "below TM-102 thresholds",
        "customer": "Personal account, 18-month tenure. SYNTHETIC.",
        "activity": [
            "Incoming wire $26,000; $22,100 (85%) transferred out 60 hours later.",
            "Misses TM-102 on both arms: under the 90% ratio and outside the 48-hour window.",
            "One earlier near-identical cycle 5 weeks ago. No alert fired.",
        ],
        "kyc_note": "No declared source-of-funds note for either incoming wire.",
    },
    "P-NV-efe": {
        "skeleton": "novel: fin-2022-a002/IND-02",
        "customer": "Personal account, 23-year tenure, customer age 81. SYNTHETIC.",
        "activity": [
            "Sudden daily debit-card cash withdrawals at the branch ATM ($400–800), prior pattern was one monthly visit.",
            "New e-transfer payees added in a two-week burst; amounts drain the savings sweep.",
            "Branch note: customer accompanied by an unfamiliar 'helper' on two visits; a power-of-attorney change is in progress.",
        ],
        "kyc_note": "File notes a documented cognitive-impairment accommodation from 2024. No legacy TM rule covers elder financial exploitation.",
    },
    "P-NV-vc": {
        "skeleton": "novel: ofac-virtual-currency/IND-02",
        "customer": "Personal account, 3-year tenure, crypto-exchange on/off-ramps in profile. SYNTHETIC.",
        "activity": [
            "Online-banking logins routed through VPN exit nodes; two sessions geolocate to a comprehensively sanctioned jurisdiction.",
            "Card purchases at a virtual-asset platform within hours of those sessions.",
            "Fiat withdrawals from the same platform land back in the account days later.",
        ],
        "kyc_note": "Login telemetry sits in the fraud stack, not the AML stack — the legacy rulebook has no access-geography rule.",
    },
    "P-NV-ec": {
        "skeleton": "novel: fin-2023-alert004/IND-01",
        "customer": "Business account — electronics wholesaler incorporated 8 months ago. SYNTHETIC.",
        "activity": [
            "Incoming payments from a freight forwarder; outgoing wires to component brokers in two transshipment hubs.",
            "Trade documents reference HS codes matching export-controlled microelectronics.",
            "The company has NO trade history before incorporation; director previously at a deregistered trading firm.",
        ],
        "kyc_note": "Trade-document screening is out of scope for every legacy TM rule; the institution holds the docs in a separate trade-finance system.",
    },
    "P-RP-01": {
        "skeleton": "authored benign",
        "customer": "Business account — florist, 12-year tenure. SYNTHETIC.",
        "activity": [
            "Cash deposits spike every February and May (holiday trade), 160% of monthly average.",
            "Supplier payments to two wholesale nurseries; payroll for three staff.",
            "Pattern repeats across all 12 years of history.",
        ],
        "kyc_note": "Declared seasonal cash business at onboarding; expected-volume field anticipates the seasonal peaks.",
    },
    "P-RP-02": {
        "skeleton": "authored benign",
        "customer": "Personal account, 15-year tenure. SYNTHETIC.",
        "activity": [
            "Biweekly salary credit, monthly mortgage debit, automatic savings sweep.",
            "One out-of-pattern event: a $30,000 incoming transfer with memo 'estate distribution', matched by a probate-note on file.",
        ],
        "kyc_note": "KYC current; the estate transfer is documented in a branch note from the same week.",
    },
    "P-RP-03": {
        "skeleton": "authored benign-ambiguous",
        "customer": "Personal account — independent contractor, 6-year tenure. SYNTHETIC.",
        "activity": [
            "Lumpy invoice income: $4,000–11,000 credits at irregular intervals from 5 repeat counterparties.",
            "Three round-amount transfers of $2,000 to the same family member in 60 days (below TM-105's five-transfer trigger).",
            "Periodic cash withdrawals for materials purchases (declared trade: renovation contractor).",
        ],
        "kyc_note": "Occupation documented; counterparties consistent with the declared trade.",
    },
    "P-CT-01": {
        "skeleton": "control: textbook TM-101",
        "customer": "Personal account, 14-month tenure. SYNTHETIC.",
        "activity": [
            "Nine cash deposits in 21 days, every one between $9,300 and $9,900, at three branches.",
            "Each deposit followed within a day by an outbound transfer to the same external account.",
            "Customer asked at the counter about 'the reporting limit' on two occasions (teller notes on file).",
        ],
        "kyc_note": "Declared occupation: unemployed. No declared source of funds.",
    },
    "P-CT-02": {
        "skeleton": "control: textbook TM-108 false positive",
        "customer": "Business account — payroll services bureau, 9-year tenure. SYNTHETIC.",
        "activity": [
            "Transaction count 8× the trailing weekly average in the last 7 days.",
            "The spike is the bureau's quarter-end payroll run; identical spikes every quarter-end in history.",
            "Every outbound credit matches a named employee of a documented client company.",
        ],
        "kyc_note": "Client roster and service agreement on file; the velocity rule has no calendar awareness.",
    },
    "P-CT-03": {
        "skeleton": "control: benign retiree",
        "customer": "Personal account, 31-year tenure, customer age 74. SYNTHETIC.",
        "activity": [
            "Monthly pension credits, utility debits, one annual travel booking.",
            "No cash activity in 5 years.",
        ],
        "kyc_note": "KYC current; nothing out of pattern.",
    },
    "P-CT-04": {
        "skeleton": "control: textbook TM-109",
        "customer": "Personal account opened 4 months ago. SYNTHETIC.",
        "activity": [
            "Cash deposits at branches in five cities within 10 days, $4,000–7,000 each.",
            "Aggregate $28,500 wired out in one transfer to a money services business in another region.",
            "Branch slips name three different depositors, none the account holder.",
        ],
        "kyc_note": "Declared occupation: retail clerk; declared income inconsistent with deposit volume.",
    },
}


# ---------------------------------------------------------------- scenario selection
# Deterministic, hand-selected. history refs are alert_ids resolved from alert-history.json;
# the TM-104 pair (S-01/S-02) SHARES P-HF-104 — the seeded process inconsistency (a1
# dismisses, a2 escalates, materially identical fact patterns).

SCENARIO_SPECS = [
    {"id": "S-01", "stratum": "history-signal-fired", "panel": "P-HF-104", "fired_rule": "TM-104",
     "alert": "A-0011", "second_rater": {"rater": "r2", "label": "synthetic second rater (seeded)",
     "disposition": "escalate", "rationale": "No documented connection to the corridor; unexplained purpose outweighs the in-pattern remainder."}},
    {"id": "S-02", "stratum": "history-signal-fired", "panel": "P-HF-104", "fired_rule": "TM-104",
     "alert": "A-0012", "second_rater": {"rater": "r2", "label": "synthetic second rater (seeded)",
     "disposition": "escalate", "rationale": "Same fact pattern as the dismissed sibling alert; consistency requires the same call."}},
    {"id": "S-03", "stratum": "history-signal-fired", "panel": "P-HF-101", "fired_rule": "TM-101",
     "alert": "A-0009", "prior_alerts": 8, "second_rater": {"rater": "r2", "label": "synthetic second rater (seeded)",
     "disposition": "need-more-info", "rationale": "Nine alerts on one undocumented cash business: the file needs the business documentation before another dismissal.",
     "info_needed": {"data_source": "D8", "what": "KYC refresh — registration and expected cash volume of the declared side business"}}},
    {"id": "S-04", "stratum": "history-signal-fired", "panel": "P-HF-109", "fired_rule": "TM-109",
     "alert": "A-0019"},
    {"id": "S-05", "stratum": "history-signal-fired", "panel": "P-HF-110", "fired_rule": "TM-110",
     "alert": "A-0036"},
    {"id": "S-06", "stratum": "history-signal-fired", "panel": "P-HF-106", "fired_rule": "TM-106",
     "alert": "A-0042"},
    {"id": "S-07", "stratum": "history-signal-fired", "panel": "P-HF-102", "fired_rule": "TM-102",
     "alert": "A-0024", "prior_alerts": 2},
    {"id": "S-08", "stratum": "history-below-the-line", "panel": "P-BT-101", "below_rule": "TM-101",
     "second_rater": {"rater": "r2", "label": "synthetic second rater (seeded)",
     "disposition": "confirm-risk", "rationale": "Band-shifted structuring; the rhythm is the signal, not the band."}},
    {"id": "S-09", "stratum": "history-below-the-line", "panel": "P-BT-112", "below_rule": "TM-112"},
    {"id": "S-10", "stratum": "history-below-the-line", "panel": "P-BT-102", "below_rule": "TM-102"},
    {"id": "S-11", "stratum": "synthetic-novel", "panel": "P-NV-efe", "novel": "fin-2022-a002/IND-02"},
    {"id": "S-12", "stratum": "synthetic-novel", "panel": "P-NV-vc", "novel": "ofac-virtual-currency/IND-02"},
    {"id": "S-13", "stratum": "synthetic-novel", "panel": "P-NV-ec", "novel": "fin-2023-alert004/IND-01",
     "second_rater": {"rater": "r2", "label": "synthetic second rater (seeded)",
     "disposition": "escalate", "rationale": "Controlled-goods HS codes + no trade history + successor-director pattern: escalate to investigations."}},
    {"id": "S-14", "stratum": "random-population", "panel": "P-RP-01"},
    {"id": "S-15", "stratum": "random-population", "panel": "P-RP-02"},
    {"id": "S-16", "stratum": "random-population", "panel": "P-RP-03"},
    {"id": "C-17", "stratum": "history-signal-fired", "panel": "P-CT-01", "fired_rule": "TM-101",
     "control": {"known_disposition": "confirm-risk", "basis": "Textbook structuring with teller-note intent evidence — seeded clear-risk control."}},
    {"id": "C-18", "stratum": "history-signal-fired", "panel": "P-CT-02", "fired_rule": "TM-108",
     "control": {"known_disposition": "confirm-no-risk", "basis": "Documented quarter-end payroll run — seeded clear-benign control behind a firing rule."}},
    {"id": "C-19", "stratum": "random-population", "panel": "P-CT-03",
     "control": {"known_disposition": "confirm-no-risk", "basis": "Long-tenure retiree, fully in pattern — seeded clear-benign control."},
     "second_rater": {"rater": "r2", "label": "synthetic second rater (seeded)",
     "disposition": "confirm-no-risk", "rationale": "Nothing out of pattern; control agreement check."}},
    {"id": "C-20", "stratum": "history-signal-fired", "panel": "P-CT-04", "fired_rule": "TM-109",
     "control": {"known_disposition": "confirm-risk", "basis": "Textbook funnel-account pattern with third-party depositors — seeded clear-risk control."}},
]


# ---------------------------------------------------------------- generation

def generate():
    rules = read_rules()
    signals = read_signals()
    alerts = read_alerts()
    novel = read_novel()

    used_rules = sorted(
        {s.get("fired_rule") for s in SCENARIO_SPECS if s.get("fired_rule")}
        | {s.get("below_rule") for s in SCENARIO_SPECS if s.get("below_rule")}
    )
    rules_block = {}
    for rid in used_rules:
        if rid not in rules:
            raise ValueError(f"rule {rid} not found in legacy-rulebook.md")
        rules_block[rid] = dict(rules[rid])
        rules_block[rid]["signal"] = signals[rid]

    scenarios = []
    for spec in SCENARIO_SPECS:
        sc = {
            "id": spec["id"],
            "stratum": spec["stratum"],
            "panel": spec["panel"],
            "fired_rule": spec.get("fired_rule"),
            "below_rule": spec.get("below_rule"),
            "history": None,
            "prior_alerts": spec.get("prior_alerts", 0),
            "second_rater": spec.get("second_rater"),
            "control": spec.get("control"),
            "novel_source": novel[spec["novel"]] if spec.get("novel") else None,
        }
        if spec.get("alert"):
            a = alerts[spec["alert"]]
            sc["history"] = {
                "alert_id": a["alert_id"],
                "disposition": a["disposition"],
                "analyst": a["analyst"],
                "date": a["date"],
                "entity_id": a["entity_id"],
            }
        scenarios.append(sc)

    return {
        "meta": {
            "synthetic": True,
            "note": (
                "SYNTHETIC triage-scenario dataset for the Phase-49 triage console (blueprint "
                "§14 embryo). Curated deterministically from the SYNTHETIC Phase-48 probe "
                "history (data/probe-history) — every institution, customer, figure, and panel "
                "is invented; no real customer or transaction data. The synthetic-novel stratum "
                "quotes committed corpus indicators from US FEDERAL sources only (public "
                "domain, 17 U.S.C. §105). Historical dispositions are facts about DECISIONS, "
                "never labels of correctness. Regenerate: python3 "
                "scripts/curate_triage_scenarios.py"
            ),
            "strata": STRATA,
            "disposition_grammar": DISPOSITION_GRAMMAR,
            "history_dispositions": HISTORY_DISPOSITIONS,
            "us_federal_allowlist": sorted(US_FEDERAL_ALLOWLIST),
            "design_params": {
                "note": "chosen, not measured — every parameter below is a design choice, not a measured quantity (§14)",
                "scenario_count": len(SCENARIO_SPECS),
                "controls": sum(1 for s in SCENARIO_SPECS if s.get("control")),
                "double_assigned": sum(1 for s in SCENARIO_SPECS if s.get("second_rater")),
            },
            "source": {
                "rulebook": "data/probe-history/legacy-rulebook.md (SYNTHETIC)",
                "alert_history": "data/probe-history/alert-history.json (SYNTHETIC)",
                "derived_signals": "data/probe-history/derived/legacy-rulebook.json",
            },
        },
        "rules": rules_block,
        "panels": PANELS,
        "scenarios": scenarios,
    }


# ---------------------------------------------------------------- validation (authoring-side)

def validate(data):
    """Raise ValueError on any structural violation. build.py carries its own copy of these
    checks at the build boundary (T2); this authoring-side validator backs --selftest."""
    meta = data.get("meta", {})
    if meta.get("synthetic") is not True:
        raise ValueError("meta.synthetic must be true")
    caps, srcs = read_taxonomy()
    rules = data.get("rules", {})
    panels = data.get("panels", {})
    scenarios = data.get("scenarios", [])
    if not (1 <= len(scenarios) <= 20):
        raise ValueError(f"scenario count {len(scenarios)} outside 1..20")
    seen = set()
    panel_disp = {}
    for sc in scenarios:
        sid = sc.get("id", "<missing>")
        if sid in seen:
            raise ValueError(f"duplicate scenario id {sid}")
        seen.add(sid)
        if sc.get("stratum") not in STRATA:
            raise ValueError(f"{sid}: stratum {sc.get('stratum')!r} not in closed vocab")
        if sc.get("panel") not in panels:
            raise ValueError(f"{sid}: dangling panel ref {sc.get('panel')!r}")
        if "fired_rule" not in sc:
            raise ValueError(f"{sid}: fired_rule field missing (must be present, possibly null)")
        for key in ("fired_rule", "below_rule"):
            if sc.get(key) is not None and sc[key] not in rules:
                raise ValueError(f"{sid}: {key} {sc[key]!r} not in embedded rules block")
        h = sc.get("history")
        if h is not None:
            if h.get("disposition") not in HISTORY_DISPOSITIONS:
                raise ValueError(f"{sid}: history disposition {h.get('disposition')!r} off-vocab")
            panel_disp.setdefault(sc["panel"], set()).add(h["disposition"])
        sr = sc.get("second_rater")
        if sr is not None:
            if "synthetic" not in sr.get("label", "").lower():
                raise ValueError(f"{sid}: second_rater label must declare synthetic")
            if sr.get("disposition") not in DISPOSITION_GRAMMAR:
                raise ValueError(f"{sid}: second_rater disposition off-grammar")
            info = sr.get("info_needed")
            if info and info.get("data_source") not in srcs:
                raise ValueError(f"{sid}: info_needed data_source {info.get('data_source')!r} not in taxonomy")
        ctl = sc.get("control")
        if ctl is not None and ctl.get("known_disposition") not in DISPOSITION_GRAMMAR:
            raise ValueError(f"{sid}: control known_disposition off-grammar")
        nv = sc.get("novel_source")
        if nv is not None:
            if nv.get("doc_id") not in US_FEDERAL_ALLOWLIST:
                raise ValueError(f"{sid}: novel_source doc {nv.get('doc_id')!r} not US-federal-allowlisted")
            if nv.get("capability") not in caps or nv.get("data_source") not in srcs:
                raise ValueError(f"{sid}: novel_source C/D refs not in taxonomy")
    for rid, rule in rules.items():
        sig = rule.get("signal", {})
        if sig.get("capability") not in caps or sig.get("data_source") not in srcs:
            raise ValueError(f"rule {rid}: signal C/D refs not in taxonomy")
    if not any(len(v) > 1 for v in panel_disp.values()):
        raise ValueError("no divergent-disposition pair shares a panel (the seeded inconsistency is required)")
    if sum(1 for sc in scenarios if sc.get("control")) < 3:
        raise ValueError("fewer than 3 control scenarios")
    if sum(1 for sc in scenarios if sc.get("second_rater")) < 4:
        raise ValueError("fewer than 4 second-rater seeds")
    strata_present = {sc["stratum"] for sc in scenarios}
    if strata_present != set(STRATA):
        raise ValueError(f"strata not all populated: missing {set(STRATA) - strata_present}")


# ---------------------------------------------------------------- selftest fixtures (RED set)

def selftest():
    data = generate()
    validate(data)  # the valid dataset must pass

    def broken(mutate, expect):
        d = copy.deepcopy(data)
        mutate(d)
        try:
            validate(d)
        except ValueError as e:
            if expect not in str(e):
                raise AssertionError(f"wrong violation for {expect!r}: {e}")
            return
        raise AssertionError(f"broken fixture passed validation: {expect}")

    broken(lambda d: d["scenarios"][0].update(stratum="off-vocab"), "closed vocab")
    broken(lambda d: d["scenarios"][0].update(panel="P-NOPE"), "dangling panel ref")
    broken(lambda d: d["meta"].update(synthetic=False), "meta.synthetic")
    broken(lambda d: d["scenarios"][10]["novel_source"].update(doc_id="fintrac-2024-oa001"),
           "not US-federal-allowlisted")
    broken(lambda d: d["scenarios"][10]["novel_source"].update(capability="C99"),
           "not in taxonomy")
    broken(lambda d: [d["scenarios"].__setitem__(i, dict(d["scenarios"][i], second_rater=None))
                      for i in range(len(d["scenarios"]))],
           "second-rater seeds")
    broken(lambda d: [d["scenarios"].__setitem__(i, dict(d["scenarios"][i], control=None))
                      for i in range(len(d["scenarios"]))],
           "control scenarios")
    broken(lambda d: d["scenarios"][1]["history"].update(disposition="dismissed"),
           "divergent-disposition")
    broken(lambda d: d["scenarios"][0].pop("fired_rule"), "fired_rule field missing")
    broken(lambda d: d["scenarios"][0]["second_rater"].update(label="second rater"),
           "declare synthetic")

    # determinism: two independent generations serialize byte-identically
    a = json.dumps(generate(), indent=1, sort_keys=True, ensure_ascii=False)
    b = json.dumps(generate(), indent=1, sort_keys=True, ensure_ascii=False)
    assert a == b, "generation is not deterministic"

    # parse sanity: all 12 rulebook rules parsed; every used rule has a derived signal
    rules = read_rules()
    assert len(rules) == 12, f"expected 12 parsed rules, got {len(rules)}"
    assert set(read_signals()) == set(rules), "derived signals do not cover the parsed rules"

    print("selftest: OK (valid dataset passes; 10 broken fixtures rejected; deterministic; 12 rules parsed)")


def main():
    if "--selftest" in sys.argv:
        selftest()
        return
    data = generate()
    validate(data)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(
        json.dumps(data, indent=1, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {OUT_PATH.relative_to(ROOT)} "
          f"({len(data['scenarios'])} scenarios, {len(data['panels'])} panels, "
          f"{len(data['rules'])} rules embedded)")


if __name__ == "__main__":
    main()
