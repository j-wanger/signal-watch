#!/usr/bin/env python3
"""Evidence-requirement profile: load + validate + the sufficiency evaluator (Phase 69 — companion).

THE CONTROL (load-bearing). A case's fired signals license a *defensive filing* trivially; they do NOT
license a *determination*. The determination is licensed only when the case carries the
determination-licensing EVIDENCE for its crime_type — a per-typology profile of ATOMS (data/workbench/
evidence-requirements.json). This module is the profile's loader, its fail-loud validator, and the pure
`evaluate_sufficiency` verdict the workbench routes on (Phase 69 supersedes the Phase-64 combo-FREQUENCY
gate; frequency becomes context, sufficiency becomes the trigger).

CHOSEN, NOT MEASURED. The atoms + thresholds are authored from public AML guidance + the capability
taxonomy — never learned from past dispositions (the substrate is label-blind: the §12/§14 honesty seam).
The verdict is illustrative; the always-on badge applies; ZERO catch-rate / precision / lift number.

DOCTRINE: stdlib + the shared honesty sweep only. NEVER imports aml_substrate / aml_casework / serve_chain /
serve_workbench. build.py NEVER imports this (data/workbench/evidence-requirements.json is no ship input).
The casework STR-vocab is MIRRORED here (embedded constants), not imported — the companion subprocesses
casework, it does not import the package at load time. Keep the mirror in sync on re-vendor.

Usage:
    python3 scripts/evidence_requirements.py --selftest   # offline assertions (no model, no socket), exit
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
ROOT = _HERE.parent
sys.path.insert(0, str(_HERE))
REQUIREMENTS_JSON = ROOT / "data" / "workbench" / "evidence-requirements.json"

# The project honesty sweep — REUSE the single source of truth (osint_tools._BANNED): %, Nx,
# lift/precision/recall/catch-rate/f1/auroc. osint_tools does no heavy work at import (the corpus loads
# lazily); importing it keeps the no-metric rule DRY across the companion layer.
from osint_tools import _BANNED  # noqa: E402  (signal-watch's OWN companion module; the shared honesty regex)

# Mirrors aml_casework.contract at the vendored pin (vendor/aml-casework/VENDORED_AT). EMBEDDED, not
# imported — the companion subprocesses casework, never imports its package at module load. STR_REQUIRED_
# ELEMENTS is the FINTRAC STR completeness checklist; CRIME_TYPES is the closed offence vocab.
_STR_REQUIRED_ELEMENTS = (
    "reporting_entity",
    "transaction_details",
    "account_information",
    "subject_information",
    "typology_grounds",
    "grounds_for_suspicion_narrative",
)
_CRIME_TYPES = ("money_laundering", "terrorist_financing", "kyc_integrity")
# Mirrors aml_casework.contract.CRIME_BY_CAPABILITY at the vendored pin — the capability -> suspected-offence
# map. EMBEDDED (the companion never imports casework). An unmapped capability implies no offence.
_CRIME_BY_CAPABILITY = {
    "C2": "money_laundering", "C3": "money_laundering", "C4": "money_laundering",
    "C5": "money_laundering", "C7": "money_laundering", "C8": "money_laundering",
    "C15": "money_laundering", "C14": "kyc_integrity",
}
_ATOM_KINDS = ("mechanism", "leg")
_C_CODE = re.compile(r"^C(\d+)$")   # capability codes C1..C28 (data/capability-taxonomy.json)
_D_CODE = re.compile(r"^D(\d+)$")   # data-source codes D1..D20
_C_MAX, _D_MAX = 28, 20
# Phase 69 T3 — how a GATHER finding's source_kind (osint_tools KINDS) closes a determination atom's
# `gather_signal`. registry ownership edge → a network/UBO atom; a sanctions/adverse hit → corroboration.
GATHER_KIND_TO_SIGNAL = {"registry": "ownership", "sanctions": "corroboration", "adverse_media": "corroboration"}
_GATHER_SIGNALS = frozenset(GATHER_KIND_TO_SIGNAL.values())


def load_requirements(path: Path | None = None) -> dict:
    """Read the committed profile (read-only; never mutated)."""
    return json.loads((path or REQUIREMENTS_JSON).read_text(encoding="utf-8"))


_REQ_CACHE: dict = {}


def requirements() -> dict:
    """The committed evidence-requirement profile, cached read-only — the shared spine the chain + case
    workbenches both consume (the determination control's source of truth)."""
    if "p" not in _REQ_CACHE:
        _REQ_CACHE["p"] = load_requirements()
    return _REQ_CACHE["p"]


def _check_codes(codes, pat, mx, kind, where, errors):
    if not isinstance(codes, list):
        errors.append(f"{where}.{kind} must be a list"); return
    for code in codes:
        m = pat.match(str(code))
        if not m or not (1 <= int(m.group(1)) <= mx):
            errors.append(f"{where}.{kind} has an out-of-range/malformed code {code!r} (expected {kind[:1].upper()}1..{mx})")


def validate_requirements(profile: dict) -> list:
    """Fail-loud structural validation (returns a list of error strings; empty == clean). Enforced:
      - a head-of-file `note` disclaimer + basis 'chosen-not-measured' + schema_version (synthetic, never
        ships undisclosed; never presented as measured);
      - crime_types is a non-empty subset of the casework CRIME_TYPES vocab;
      - per crime_type: required_elements is a non-empty subset of the casework STR_REQUIRED_ELEMENTS;
        atoms have unique ids, a closed kind, valid C*/D* codes, non-empty label+rationale; >=1 mechanism;
      - sufficiency_rule thresholds are non-negative ints that DO NOT exceed the atoms available
        (mechanism_required <= #mechanism atoms; additional_legs_required <= #leg atoms); the two booleans
        are bools; mitigation_atoms subset the atom ids; requiring rebutted-mitigation needs >=1 mitigation atom;
      - the honesty sweep: no rendered string (note/basis/label/rationale/guidance) carries a banned metric token."""
    errors: list = []
    if not isinstance(profile, dict):
        return ["profile is not a JSON object"]
    if not str(profile.get("note") or "").strip():
        errors.append("profile missing the head-of-file 'note' synthetic/chosen-not-measured disclaimer")
    if profile.get("basis") != "chosen-not-measured":
        errors.append("profile.basis must be 'chosen-not-measured' (the label-blind honesty seam)")
    if not str(profile.get("schema_version") or "").strip():
        errors.append("profile missing 'schema_version'")
    # the honesty sweep over the top-level rendered strings
    for f in ("note", "basis"):
        if _BANNED.search(str(profile.get(f) or "")):
            errors.append(f"profile.{f} carries a banned metric token (the no-metric honesty rule)")

    cts = profile.get("crime_types")
    if not isinstance(cts, dict) or not cts:
        errors.append("profile.crime_types must be a non-empty object keyed by crime_type")
        return errors
    for ct, spec in cts.items():
        where = f"crime_types['{ct}']"
        if ct not in _CRIME_TYPES:
            errors.append(f"{where}: unknown crime_type (closed vocab: {_CRIME_TYPES})")
        if not isinstance(spec, dict):
            errors.append(f"{where} must be an object"); continue
        if not str(spec.get("label") or "").strip():
            errors.append(f"{where} missing 'label'")
        req = spec.get("required_elements")
        if not isinstance(req, list) or not req:
            errors.append(f"{where}.required_elements must be a non-empty list")
        else:
            for el in req:
                if el not in _STR_REQUIRED_ELEMENTS:
                    errors.append(f"{where}.required_elements has '{el}' outside the STR checklist {_STR_REQUIRED_ELEMENTS}")

        atoms = spec.get("atoms")
        if not isinstance(atoms, list) or not atoms:
            errors.append(f"{where}.atoms must be a non-empty list"); continue
        seen_ids, n_mech, n_leg = set(), 0, 0
        for atom in atoms:
            if not isinstance(atom, dict):
                errors.append(f"{where}: an atom is not an object"); continue
            aid = str(atom.get("id") or "").strip()
            aw = f"{where}.atoms['{aid or '?'}']"
            if not aid:
                errors.append(f"{where}: an atom is missing 'id'")
            elif aid in seen_ids:
                errors.append(f"{where}: duplicate atom id '{aid}'")
            seen_ids.add(aid)
            kind = atom.get("kind")
            if kind not in _ATOM_KINDS:
                errors.append(f"{aw}.kind must be one of {_ATOM_KINDS}")
            n_mech += kind == "mechanism"
            n_leg += kind == "leg"
            for f in ("label", "rationale"):
                val = str(atom.get(f) or "").strip()
                if not val:
                    errors.append(f"{aw} missing '{f}'")
                elif _BANNED.search(val):
                    errors.append(f"{aw}.{f} carries a banned metric token")
            _check_codes(atom.get("evidence", []), _C_CODE, _C_MAX, "evidence", aw, errors)
            _check_codes(atom.get("data", []), _D_CODE, _D_MAX, "data", aw, errors)
            gs = atom.get("gather_signal")          # optional: a GATHER finding that can close this atom
            if gs is not None and gs not in _GATHER_SIGNALS:
                errors.append(f"{aw}.gather_signal {gs!r} is not a known gather signal {tuple(_GATHER_SIGNALS)}")
        if n_mech < 1:
            errors.append(f"{where} has no 'mechanism' atom (a determination needs the laundering/integrity mechanism)")

        rule = spec.get("sufficiency_rule")
        if not isinstance(rule, dict):
            errors.append(f"{where}.sufficiency_rule must be an object");
        else:
            mr, lr = rule.get("mechanism_required"), rule.get("additional_legs_required")
            if not isinstance(mr, int) or isinstance(mr, bool) or mr < 0:
                errors.append(f"{where}.sufficiency_rule.mechanism_required must be a non-negative int")
            elif mr > n_mech:
                errors.append(f"{where}.sufficiency_rule.mechanism_required ({mr}) exceeds the {n_mech} mechanism atom(s)")
            if not isinstance(lr, int) or isinstance(lr, bool) or lr < 0:
                errors.append(f"{where}.sufficiency_rule.additional_legs_required must be a non-negative int")
            elif lr > n_leg:
                errors.append(f"{where}.sufficiency_rule.additional_legs_required ({lr}) exceeds the {n_leg} leg atom(s)")
            for f in ("named_predicate_risk_required", "no_unrebutted_mitigation_required"):
                if not isinstance(rule.get(f), bool):
                    errors.append(f"{where}.sufficiency_rule.{f} must be a bool")
            mit = spec.get("mitigation_atoms", [])
            if not isinstance(mit, list):
                errors.append(f"{where}.mitigation_atoms must be a list")
            else:
                for mid in mit:
                    if mid not in seen_ids:
                        errors.append(f"{where}.mitigation_atoms references unknown atom '{mid}'")
                if rule.get("no_unrebutted_mitigation_required") is True and not mit:
                    errors.append(f"{where} requires rebutted mitigation but defines no mitigation_atoms")

        guide = str(spec.get("guidance") or "").strip()
        if not guide:
            errors.append(f"{where} missing 'guidance'")
        elif _BANNED.search(guide):
            errors.append(f"{where}.guidance carries a banned metric token")
    return errors


def crime_type_for_capabilities(capabilities, profile: dict | None = None) -> str | None:
    """The dominant suspected offence implied by a case's fired capabilities (via the embedded casework
    CRIME_BY_CAPABILITY). Restricted to crime_types the profile actually covers (TF is unmapped + dropped
    this phase). Ties break toward the most-cited; None when no capability maps."""
    counts: dict = {}
    for cap in capabilities or []:
        ct = _CRIME_BY_CAPABILITY.get(cap)
        if ct and (profile is None or ct in (profile.get("crime_types") or {})):
            counts[ct] = counts.get(ct, 0) + 1
    if not counts:
        return None
    return max(counts, key=lambda k: (counts[k], k != "kyc_integrity"))


def present_atoms(crime_type: str, capabilities, profile: dict, *, gathered=()) -> list:
    """The determination atoms a case CARRIES: an atom is present if any of its `evidence` capabilities
    fired, OR (Phase-69 T3) its `gather_signal` was returned by the GATHER loop (record-sourced). Order
    follows the profile's atom order (stable)."""
    spec = (profile.get("crime_types") or {}).get(crime_type) or {}
    caps, gat = set(capabilities or []), set(gathered or [])
    out = []
    for atom in spec.get("atoms", []):
        if set(atom.get("evidence", [])) & caps or (atom.get("gather_signal") and atom["gather_signal"] in gat):
            out.append(atom["id"])
    return out


def gathered_signals(findings) -> list:
    """The distinct gather-signals a GATHER result carries: each grounded finding's `source_kind`
    (registry/sanctions/adverse_media) mapped to its requirement signal (ownership/corroboration).
    Feeds present_atoms(gathered=...) so a record-sourced finding closes a determination atom."""
    out = []
    for f in findings or []:
        sig = GATHER_KIND_TO_SIGNAL.get((f or {}).get("source_kind"))
        if sig and sig not in out:
            out.append(sig)
    return out


def gather_targets(crime_type: str, present_atom_ids, profile: dict) -> list:
    """The unmet determination atoms a GATHER pass COULD close — the leg atoms that carry a `gather_signal`
    and are not yet present. This is what makes the gather REQUIREMENT-TARGETED (seek the missing evidence),
    not merely additive discovery."""
    spec = (profile.get("crime_types") or {}).get(crime_type) or {}
    have = set(present_atom_ids or [])
    return [{"id": a["id"], "label": a.get("label", ""), "gather_signal": a["gather_signal"]}
            for a in spec.get("atoms", [])
            if a.get("gather_signal") and a["id"] not in have]


def assess_completeness(crime_type: str, capabilities, profile: dict, *,
                        str_completeness: dict | None = None, gathered=()) -> dict:
    """The COMPLETENESS measurement (Phase 69 T2) — required vs have vs gap, for one case. Pure; no verdict
    (the sufficiency DECISION is evaluate_sufficiency, wired in T4). Returns the STR-element completeness
    (from the casework `completeness` dict) + per-atom presence (the determination evidence we have vs the
    honest gaps). `gathered` folds in the GATHER loop's record-sourced findings."""
    spec = (profile.get("crime_types") or {}).get(crime_type)
    if not isinstance(spec, dict):
        return {"crime_type": crime_type, "profiled": False, "str": {"required": [], "satisfied": [], "missing": []},
                "atoms": [], "present_atom_ids": []}
    comp = str_completeness or {}
    required = list(spec.get("required_elements", []))
    satisfied = [el for el in required if comp.get(el) is True]
    missing = [el for el in required if comp.get(el) is not True]
    present = set(present_atoms(crime_type, capabilities, profile, gathered=gathered))
    atoms = [{"id": a["id"], "label": a.get("label", ""), "kind": a.get("kind"),
              "evidence": a.get("evidence", []), "data": a.get("data", []),
              "present": a["id"] in present} for a in spec.get("atoms", [])]
    return {"crime_type": crime_type, "profiled": True,
            "str": {"required": required, "satisfied": satisfied, "missing": missing},
            "atoms": atoms, "present_atom_ids": [a["id"] for a in atoms if a["present"]]}


def signal_brief(crime_type: str, present_atom_ids, profile: dict) -> list:
    """The §12 DISCOVERY-LOOP feedback (Phase 69 T5): the unmet determination atoms that GATHER CANNOT close
    (no `gather_signal`) become a brief of signals / data sources to BUILD in aml-substrate. Each names the
    capability (C*) + data sources (D*) the determination needs but the program does not yet have — the gap
    is evidence of what to build, the way a real program matures (clearly-defined risks, then the detector)."""
    spec = (profile.get("crime_types") or {}).get(crime_type) or {}
    have = set(present_atom_ids or [])
    return [{"atom": a["id"], "label": a.get("label", ""), "capabilities": a.get("evidence", []),
             "data_sources": a.get("data", []), "rationale": a.get("rationale", "")}
            for a in spec.get("atoms", [])
            if a["id"] not in have and not a.get("gather_signal")]


def determine(crime_type: str, capabilities, profile: dict, *, gathered=(), str_completeness: dict | None = None,
              named_predicate_risk: bool = False, mitigation_rebutted: bool = False) -> dict:
    """The full determination verdict (Phase 69 T4) — completeness MEASUREMENT + the sufficiency DECISION,
    over one case. A determination is licensed by evidence-SUFFICIENCY (mechanism + corroborating legs + a
    NAMED predicate risk + no unrebutted mitigation), NEVER by combo-frequency. Insufficiency is a
    legitimate non-decision whose `missing` NAMES the gap (gather it, or build the signal — the §12 loop)."""
    assess = assess_completeness(crime_type, capabilities, profile,
                                 str_completeness=str_completeness, gathered=gathered)
    str_ok = None if str_completeness is None else (not assess["str"]["missing"])
    suff = evaluate_sufficiency(crime_type, assess["present_atom_ids"],
                                named_predicate_risk=named_predicate_risk, mitigation_rebutted=mitigation_rebutted,
                                profile=profile, required_elements_satisfied=str_ok)
    return {"crime_type": crime_type, "completeness": assess, "verdict": suff["verdict"],
            "sufficient": suff["sufficient"], "missing": suff["missing"], "evidence": suff["evidence"],
            "signal_brief": signal_brief(crime_type, assess["present_atom_ids"], profile)}


def evaluate_sufficiency(crime_type: str, present_atom_ids, *, named_predicate_risk: bool,
                         mitigation_rebutted: bool, profile: dict,
                         required_elements_satisfied: bool | None = None) -> dict:
    """The pure determination verdict over an EXPLICIT atom-presence input (Phase 69's core control;
    the case→atom derivation + the UI are wired in T4). Returns:
      {sufficient, verdict('determination'|'needs_more_info'), missing[<reason>], evidence{...}}.
    `missing` is load-bearing — each reason NAMES a gap (what to gather, or what signal to build in the
    substrate — the §12 loop). Sufficiency licenses a DETERMINATION; insufficiency is a legitimate
    non-decision, never a defensive auto-file."""
    spec = (profile.get("crime_types") or {}).get(crime_type)
    if not isinstance(spec, dict):
        return {"sufficient": False, "verdict": "needs_more_info",
                "missing": [f"no requirement profile for crime_type '{crime_type}'"], "evidence": {}}
    by_id = {a["id"]: a for a in spec.get("atoms", []) if isinstance(a, dict) and a.get("id")}
    present = [aid for aid in present_atom_ids if aid in by_id]
    mech = [aid for aid in present if by_id[aid].get("kind") == "mechanism"]
    legs = [aid for aid in present if by_id[aid].get("kind") == "leg"]
    rule = spec.get("sufficiency_rule", {})
    missing: list = []

    if required_elements_satisfied is False:
        missing.append("STR required elements incomplete (complete the filing before a determination)")
    need_mech = int(rule.get("mechanism_required", 0))
    if len(mech) < need_mech:
        missing.append(f"need {need_mech} mechanism atom(s), have {len(mech)} "
                       f"(the laundering/integrity mechanism — gather or build a mechanism signal)")
    need_legs = int(rule.get("additional_legs_required", 0))
    if len(legs) < need_legs:
        missing.append(f"need {need_legs} corroborating leg(s), have {len(legs)} "
                       f"(gather network / source-of-funds / corroboration evidence)")
    if rule.get("named_predicate_risk_required") and not named_predicate_risk:
        missing.append("the specific predicate risk is not named (ground to the cited signals' typology guidance)")
    if rule.get("no_unrebutted_mitigation_required") and not mitigation_rebutted:
        missing.append("a plausible benign explanation is unaddressed "
                       "(establish source of funds / anticipated-activity consistency, or rule it out)")

    sufficient = not missing
    return {
        "sufficient": sufficient,
        "verdict": "determination" if sufficient else "needs_more_info",
        "missing": missing,
        "evidence": {"mechanism_present": mech, "legs_present": legs,
                     "named_predicate_risk": bool(named_predicate_risk),
                     "mitigation_rebutted": bool(mitigation_rebutted)},
    }


# --------------------------------------------------------------------------------------------------
def selftest() -> int:
    """Offline assertions: the committed profile validates clean; tamper fixtures are each rejected; the
    sufficiency evaluator licenses/withholds the determination per the rule (incl. the stricter ML bar)."""
    prof = load_requirements()
    errs = validate_requirements(prof)
    assert errs == [], f"committed profile should validate clean, got: {errs}"
    assert set(prof["crime_types"]) == {"money_laundering", "kyc_integrity"}, \
        "this phase profiles ML + kyc_integrity (TF dropped — no capability maps to it)"

    # --- tamper fixtures: each broken profile must be REJECTED (non-empty error list) ---
    def broke(mut) -> list:
        p = json.loads(json.dumps(prof))   # deep copy
        mut(p)
        return validate_requirements(p)

    def _set_basis(p): p["basis"] = "measured"
    def _bad_element(p): p["crime_types"]["money_laundering"]["required_elements"].append("not_an_str_element")
    def _bad_code(p): p["crime_types"]["money_laundering"]["atoms"][0]["evidence"] = ["C99"]
    def _bad_kind(p): p["crime_types"]["kyc_integrity"]["atoms"][0]["kind"] = "wishful"
    def _no_mechanism(p):
        for a in p["crime_types"]["kyc_integrity"]["atoms"]:
            a["kind"] = "leg"
    def _legs_over(p): p["crime_types"]["money_laundering"]["sufficiency_rule"]["additional_legs_required"] = 99
    def _dup_id(p):
        a = p["crime_types"]["money_laundering"]["atoms"]
        a[1]["id"] = a[0]["id"]
    def _banned(p): p["crime_types"]["money_laundering"]["atoms"][0]["rationale"] = "improves recall by 30%"
    def _mit_missing(p):
        s = p["crime_types"]["money_laundering"]
        s["mitigation_atoms"] = []          # but no_unrebutted_mitigation_required stays True
    def _bad_dangling_mit(p): p["crime_types"]["money_laundering"]["mitigation_atoms"] = ["ML-ZZ"]

    for name, mut in [("measured-basis", _set_basis), ("bad-element", _bad_element), ("bad-Ccode", _bad_code),
                      ("bad-kind", _bad_kind), ("no-mechanism", _no_mechanism), ("legs-over-count", _legs_over),
                      ("dup-id", _dup_id), ("banned-token", _banned), ("mitigation-missing", _mit_missing),
                      ("dangling-mitigation", _bad_dangling_mit)]:
        assert broke(mut), f"tamper '{name}' should have been rejected but validated clean"

    # --- evaluate_sufficiency: the ML stricter bar (mechanism + >=2 legs + named risk + no unrebutted mitigation) ---
    full = evaluate_sufficiency("money_laundering", ["ML-A1", "ML-A3", "ML-A4"],
                                named_predicate_risk=True, mitigation_rebutted=True, profile=prof,
                                required_elements_satisfied=True)
    assert full["sufficient"] and full["verdict"] == "determination", full

    # one leg short -> needs_more_info, and the gap is NAMED
    short = evaluate_sufficiency("money_laundering", ["ML-A1", "ML-A3"],
                                 named_predicate_risk=True, mitigation_rebutted=True, profile=prof,
                                 required_elements_satisfied=True)
    assert not short["sufficient"] and short["verdict"] == "needs_more_info", short
    assert any("corroborating leg" in m for m in short["missing"]), short

    # mechanism absent (frequency would still auto-clear; sufficiency does NOT) -> needs_more_info
    no_mech = evaluate_sufficiency("money_laundering", ["ML-A3", "ML-A4", "ML-A5"],
                                   named_predicate_risk=True, mitigation_rebutted=True, profile=prof,
                                   required_elements_satisfied=True)
    assert not no_mech["sufficient"] and any("mechanism" in m for m in no_mech["missing"]), no_mech

    # unrebutted mitigation blocks the determination even with atoms + named risk
    unrebutted = evaluate_sufficiency("money_laundering", ["ML-A1", "ML-A3", "ML-A4"],
                                      named_predicate_risk=True, mitigation_rebutted=False, profile=prof,
                                      required_elements_satisfied=True)
    assert not unrebutted["sufficient"] and any("benign explanation" in m for m in unrebutted["missing"]), unrebutted

    # named risk absent blocks it (the "state what risk we file for" requirement)
    no_risk = evaluate_sufficiency("money_laundering", ["ML-A1", "ML-A3", "ML-A4"],
                                   named_predicate_risk=False, mitigation_rebutted=True, profile=prof,
                                   required_elements_satisfied=True)
    assert not no_risk["sufficient"] and any("predicate risk" in m for m in no_risk["missing"]), no_risk

    # kyc_integrity: a single mechanism atom + named risk suffices (no extra legs / no mitigation rule)
    kyc = evaluate_sufficiency("kyc_integrity", ["KYC-A1"], named_predicate_risk=True,
                               mitigation_rebutted=True, profile=prof, required_elements_satisfied=True)
    assert kyc["sufficient"] and kyc["verdict"] == "determination", kyc

    # --- crime_type_for_capabilities + present_atoms + assess_completeness (T2 case-assessment) ---
    assert crime_type_for_capabilities(["C2", "C3", "C4"], prof) == "money_laundering"
    assert crime_type_for_capabilities(["C14"], prof) == "kyc_integrity"
    assert crime_type_for_capabilities(["C99"], prof) is None, "unmapped capability implies no offence"
    # the mule mechanism atoms light up from C2/C3 (ML-A1) and C4 (ML-A2); a leg needs C7/C8/C15/C1/C14
    pres = present_atoms("money_laundering", ["C2", "C3", "C4"], prof)
    assert "ML-A1" in pres and "ML-A2" in pres and not ({"ML-A3", "ML-A4"} & set(pres)), pres
    # NO GHOST CAPABILITY: every capability the offence map classifies to a PROFILED crime_type must be cited
    # by at least one of that crime_type's atoms (else it influences classification but lights no evidence —
    # the Phase-69 adversarial-review finding: C5 mapped to ML but was uncited).
    for cap, ct in _CRIME_BY_CAPABILITY.items():
        if ct in prof["crime_types"]:
            cited = {c for a in prof["crime_types"][ct]["atoms"] for c in a.get("evidence", [])}
            assert cap in cited, f"ghost capability {cap}: maps to {ct} but no {ct} atom cites it"
    # C5 (cash placement) alone now lights the mechanism atom — no longer a ghost
    assert present_atoms("money_laundering", ["C5"], prof) == ["ML-A1"], present_atoms("money_laundering", ["C5"], prof)
    # a gathered ownership/sanctions signal lights a leg (T3 wires gather_signal; here assert the seam holds)
    pres_g = present_atoms("money_laundering", ["C2"], prof, gathered=["__none__"])
    assert "ML-A1" in pres_g, pres_g
    # assess_completeness: STR required-vs-satisfied from the casework completeness dict + atom presence
    comp = {"reporting_entity": True, "transaction_details": True, "account_information": True,
            "subject_information": True, "typology_grounds": True, "grounds_for_suspicion_narrative": False}
    ac = assess_completeness("money_laundering", ["C2", "C3", "C4"], prof, str_completeness=comp)
    assert ac["profiled"] and ac["str"]["missing"] == ["grounds_for_suspicion_narrative"], ac["str"]
    assert set(ac["present_atom_ids"]) == {"ML-A1", "ML-A2"} and len(ac["atoms"]) == 7, ac

    # --- T3 gather mapping: a sanctions/adverse finding closes the corroboration leg (ML-A5) ---
    sigs = gathered_signals([{"source_kind": "sanctions"}, {"source_kind": "adverse_media"},
                             {"source_kind": "registry"}, {"source_kind": "junk"}])
    assert set(sigs) == {"corroboration", "ownership"}, sigs
    # the mule (mechanism + ML-A4 from C15) is one leg short; gather_targets names the closeable gap ML-A5
    mule_caps = ["C15", "C2", "C3", "C4", "C5"]
    p0 = present_atoms("money_laundering", mule_caps, prof)
    assert set(p0) == {"ML-A1", "ML-A2", "ML-A4"}, p0
    tgts = gather_targets("money_laundering", p0, prof)
    assert [t["id"] for t in tgts] == ["ML-A5"], tgts          # A4 already present; A3/A6/A7 have no gather_signal
    # a corroboration finding closes ML-A5 -> two legs (A4+A5) -> the determination becomes reachable
    p1 = present_atoms("money_laundering", mule_caps, prof, gathered=["corroboration"])
    leg_now = [a for a in p1 if a in ("ML-A3", "ML-A4", "ML-A5", "ML-A6", "ML-A7")]
    assert set(leg_now) == {"ML-A4", "ML-A5"}, leg_now
    # a bad gather_signal in the profile is rejected
    assert broke(lambda p: p["crime_types"]["money_laundering"]["atoms"][3].__setitem__("gather_signal", "wishful"))

    # --- determine(): the full verdict — frequency-blind, licensed by sufficiency (T4 control) ---
    # the mule from SIGNALS alone (mechanism + 1 leg) is NOT a determination, even with risk + mitigation
    d_sig = determine("money_laundering", mule_caps, prof, named_predicate_risk=True, mitigation_rebutted=True)
    assert d_sig["verdict"] == "needs_more_info" and any("corroborating leg" in m for m in d_sig["missing"]), d_sig
    # after GATHER closes corroboration (2 legs) + a named risk + mitigation rebutted -> a DETERMINATION
    d_full = determine("money_laundering", mule_caps, prof, gathered=["corroboration"],
                       named_predicate_risk=True, mitigation_rebutted=True)
    assert d_full["verdict"] == "determination" and d_full["sufficient"], d_full
    # same evidence, but the predicate risk unnamed -> withheld (the "state what risk we file for" rule)
    d_norisk = determine("money_laundering", mule_caps, prof, gathered=["corroboration"],
                         named_predicate_risk=False, mitigation_rebutted=True)
    assert d_norisk["verdict"] == "needs_more_info" and any("predicate risk" in m for m in d_norisk["missing"]), d_norisk
    # same evidence, mitigation unaddressed (SoF/anticipated not ruled out) -> withheld
    d_nomit = determine("money_laundering", mule_caps, prof, gathered=["corroboration"],
                        named_predicate_risk=True, mitigation_rebutted=False)
    assert d_nomit["verdict"] == "needs_more_info" and any("benign explanation" in m for m in d_nomit["missing"]), d_nomit

    # --- signal_brief (T5 §12 feedback): the unmet, NON-gatherable atoms become a build-in-substrate brief ---
    brief = signal_brief("money_laundering", p0, prof)   # mule signals: A1,A2,A4 present
    brief_ids = {b["atom"] for b in brief}
    assert brief_ids == {"ML-A3", "ML-A6", "ML-A7"}, brief_ids   # A5 is gatherable (excluded); A1/A2/A4 present
    assert all(b["capabilities"] or b["data_sources"] for b in brief), "each brief item names a capability/data to build"
    # determine() carries the brief; after gather closes A5 it stays (A5 was gatherable, not a build item)
    assert {b["atom"] for b in d_full["signal_brief"]} == {"ML-A3", "ML-A6", "ML-A7"}, d_full["signal_brief"]

    print("evidence_requirements --selftest: PASS "  # noqa: T201
          "(profile validates; 10 tampers rejected; ML stricter bar + kyc bar evaluate correctly; "
          "crime_type/present_atoms/assess_completeness over a mule profile)")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    print("evidence_requirements: profile loader + validator + sufficiency evaluator (companion). "  # noqa: T201
          "Run with --selftest.")
