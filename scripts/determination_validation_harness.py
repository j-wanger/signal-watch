#!/usr/bin/env python3
"""Determination-validation harness (Phase 78 — the "circularity exit"). COMPANION-ONLY: build.py NEVER
imports this; it touches no ship dist.

WHAT IT DOES. Validate signal-watch's determination engine (`evidence_requirements`) against aml-substrate's
EXOGENOUS disposition oracle (`eval/intended_disposition.json`, wired to the substrate CLI by substrate Phase
31 `--emit-eval-oracles`). The oracle's `file`|`clear` label is authored BLIND to the sufficiency rule — so
comparing the engine's signal-assembly to it is a genuine measurement, NOT the tautology that killed the
Phase-77 merge-66 consume (whose `true_entities` oracle was a relabel of the spine's own key).

THE NON-CIRCULAR FRAME (load-bearing). The `file` bar = mechanism + >=N corroborating legs + a NAMED predicate
risk + no unrebutted mitigation. Of these, mechanism + leg count are BUNDLE-DERIVED (the §12 signal layer);
named_predicate_risk + mitigation are HUMAN-GATE inputs not present in a raw bundle. The harness scores the
BUNDLE-ONLY signal structure (mechanism present AND >= the required legs, from the fired capabilities alone,
human-gate inputs HELD OUT and set False) and compares it to the oracle. The oracle label NEVER enters an
engine input (`assert_no_oracle_leak` + the signature guard). The deliverable is a per-class CONFUSION
STRUCTURE — counts only, synthetic-only qualified, NO catch-rate/precision/lift (the oracle is ~99% clear; an
accuracy is meaningless).

THE POPULATION. The oracle covers the substrate SCREENING-slice flagged customers (keyed `case_id` =
`CASE-<customer>`). A customer may also carry a MONITORING bundle (C2/C3/C5/C15) sharing the same case_id. The
harness MERGES per-customer (screening ∪ monitoring fired capabilities) — the Phase-71 "a case = a customer"
frame the workbench determination engine actually decides over — so the engine sees its mechanism (C2/C3/C5)
+ leg (C8/C15/...) capabilities.

USAGE.
  python3 scripts/determination_validation_harness.py --check        # replay the committed capture, NO substrate
  python3 scripts/determination_validation_harness.py --selftest      # dep-free assertions (firewall + recompute)
  python3 scripts/determination_validation_harness.py --freeze --emit-dir <out>   # re-capture from a substrate emit

  # the substrate emit (authoring-time only; pin 9677a37):
  #   PYTHONPATH=<substrate>/src <substrate>/.venv/bin/python -m aml_substrate.cli \
  #     --clients 40000 --months 2 --seed 0 --emergence --monitor \
  #     --emit-evidence --emit-screening --emit-eval-oracles --out <out>
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent          # scripts/
ROOT = _HERE.parent
sys.path.insert(0, str(ROOT / "scripts"))        # so evidence_requirements + osint_tools resolve

import evidence_requirements as er  # noqa: E402  (companion engine; the file/determination bar — BYTE-UNCHANGED)
from osint_tools import _BANNED     # noqa: E402  (the shared honesty regex — REUSE, never re-declare)

FIXDIR = ROOT / "tests" / "fixtures" / "determination-validation"
CAPTURE = FIXDIR / "capture.json"
BASELINE = FIXDIR / "baseline.json"
DELIVERABLE_DOC = ROOT / "docs" / "determination-validation.md"  # the prose surface the governor must ALSO sweep

SUBSTRATE_PIN = "9677a37"  # aml-substrate Phase 31 (emit-cli-wiring); the oracle is CLI-reachable here
EMIT_COMMAND = ("PYTHONPATH=<substrate>/src <substrate>/.venv/bin/python -m aml_substrate.cli "
                "--clients 40000 --months 2 --seed 0 --emergence --monitor "
                "--emit-evidence --emit-screening --emit-eval-oracles --out <out>")
SYNTHETIC_QUALIFIER = ("measured over a synthetic substrate slice; production has no ground-truth disposition. "
                       "Counts only — no rate, score, or multiplier is claimed.")

# The asserted summary keys (--check recompute must match the frozen baseline over these).
_ASSERT_KEYS = ("n_cases", "confusion", "by_crime_type", "oracle_split", "per_basis_fileready",
                "n_missed_total", "n_over_flag_total", "degenerate", "disagreement_sample")
_SAMPLE_CAP = 25  # bounded, disclosed sample per disagreement cell (the feed; n_*_total carries the full count)

# ---------------------------------------------------------------------------------------------------
# The resolver-input firewall, translated: the per-case ENGINE-INPUT view carries ONLY observable keys.
# An oracle field (intended_disposition/basis), a renamed surrogate, or ANY extra key RAISES — the test is
# the schema boundary, not the field name (mirrors resolution_scorer.assert_no_cluster_leak).
ALLOWED_ENGINE_INPUT_KEYS = frozenset({"case_id", "caps", "crime_type"})


def engine_input(case: dict) -> dict:
    """Strip a capture case to the engine-input view: case_id + the fired capabilities. The oracle
    (disposition/basis) and the screening/monitoring provenance are DROPPED — the engine never sees them."""
    caps = sorted({c for c in (case.get("caps") or []) if c})
    return {"case_id": case.get("case_id"), "caps": caps,
            "crime_type": er.crime_type_for_capabilities(caps, _profile())}


def assert_no_oracle_leak(inputs) -> None:
    """The firewall: every engine input carries ONLY allow-listed observable keys. An oracle label, a renamed
    surrogate (`oracle`, `intended_disposition`, `disposition`, `truth`, `label`, …), or ANY extra field
    RAISES — renaming the leak does NOT pass (the boundary is the schema, not the name)."""
    for x in inputs:
        extra = set(x) - ALLOWED_ENGINE_INPUT_KEYS
        if extra:
            raise AssertionError(
                f"oracle-input firewall: case {x.get('case_id')!r} carries non-observable field(s) "
                f"{sorted(extra)} — the disposition oracle must NEVER reach the determination engine")


def assert_engine_blind_to_oracle() -> None:
    """The signature guard (mirrors the Phase-74 priors-are-provenance guard): the file-bar functions must be
    STRUCTURALLY unable to read a disposition/oracle — no such parameter exists."""
    import inspect
    forbidden = {"oracle", "disposition", "intended_disposition", "intended_basis", "truth", "label",
                 "prior", "priors", "dispositions"}
    for fn in (er.evaluate_sufficiency, er.determine, er.present_atoms):
        leak = set(inspect.signature(fn).parameters) & forbidden
        if leak:
            raise AssertionError(f"the determination engine must be blind to the oracle — "
                                 f"{fn.__name__} exposes {sorted(leak)}")


# ---------------------------------------------------------------------------------------------------
_REQ = None


def _profile() -> dict:
    global _REQ
    if _REQ is None:
        _REQ = er.requirements()
    return _REQ


def classify(caps, profile: dict) -> dict:
    """The BUNDLE-ONLY signal-file-ready classification for one case, from the fired capabilities ALONE.
    Reuses the engine's OWN mechanism/leg split (evidence.mechanism_present/legs_present) so the harness
    tracks any profile/engine edit. The human-gate inputs are HELD OUT (named_predicate_risk=False, no
    gathered, no read, no mitigation) — the non-circular firewall. Returns the classification + the engine's
    `missing[]` gap names (what to build/gather — the §12 loop)."""
    caps = sorted({c for c in caps if c})
    ct = er.crime_type_for_capabilities(caps, profile)
    if not ct:
        return {"crime_type": None, "file_ready": False, "n_mech": 0, "n_legs": 0, "missing": [],
                "present": []}
    present = er.present_atoms(ct, caps, profile)                     # NO gathered, NO read — bundle-only
    suff = er.evaluate_sufficiency(ct, present, named_predicate_risk=False, mitigation_rebutted=False,
                                   profile=profile, mitigation_established=False)
    ev = suff.get("evidence", {})
    rule = (profile.get("crime_types", {}).get(ct, {}) or {}).get("sufficiency_rule", {}) or {}
    n_mech = len(ev.get("mechanism_present", []))
    n_legs = len(ev.get("legs_present", []))
    file_ready = (n_mech >= int(rule.get("mechanism_required", 1))
                  and n_legs >= int(rule.get("additional_legs_required", 0)))
    # the §12 gap names: the mechanism/leg-shortfall reasons (drop the held-out predicate/mitigation reasons —
    # those are the human gate, not a buildable signal gap).
    sig_missing = [m for m in suff.get("missing", [])
                   if ("mechanism" in m.lower() or "leg" in m.lower())]
    return {"crime_type": ct, "file_ready": file_ready, "n_mech": n_mech, "n_legs": n_legs,
            "missing": sig_missing, "present": present}


# ---------------------------------------------------------------------------------------------------
def _empty_confusion() -> dict:
    return {"file_ready__file": 0, "file_ready__clear": 0, "not_ready__file": 0, "not_ready__clear": 0}


def summarize(cases, profile: dict) -> dict:
    """Recompute the confusion structure from the capture cases by RE-RUNNING the engine on each case's caps
    (NO oracle input). This is the validation: if the engine's file-ready computation drifts, the summary
    moves and --check fails."""
    inputs = [engine_input(c) for c in cases]
    assert_no_oracle_leak(inputs)               # the firewall, before any classification
    assert_engine_blind_to_oracle()

    overall = _empty_confusion()
    by_ct: dict = {}
    oracle_split = {"file": 0, "clear": 0}
    per_basis: dict = {}
    missed, over_flag = [], []

    for case in sorted(cases, key=lambda c: str(c.get("case_id"))):
        disp = case.get("oracle_disposition")               # eval-only — read ONLY into the comparison target
        basis = case.get("oracle_basis")
        if disp not in ("file", "clear"):
            continue
        oracle_split[disp] += 1
        cls = classify(case.get("caps") or [], profile)
        ready = cls["file_ready"]
        cell = f"{'file_ready' if ready else 'not_ready'}__{disp}"
        overall[cell] += 1
        ct = cls["crime_type"] or "unmapped"
        by_ct.setdefault(ct, _empty_confusion())[cell] += 1
        pb = per_basis.setdefault(basis if basis is not None else "null", {"n": 0, "file_ready": 0})
        pb["n"] += 1
        if ready:
            pb["file_ready"] += 1
        row = {"case_id": case.get("case_id"), "caps": sorted({c for c in (case.get("caps") or []) if c}),
               "crime_type": cls["crime_type"], "oracle_basis": basis, "missing": cls["missing"],
               "n_mech": cls["n_mech"], "n_legs": cls["n_legs"]}
        if disp == "file" and not ready:
            missed.append(row)                  # §12 signal gap: oracle would file, signals not assembled
        elif disp == "clear" and ready:
            over_flag.append(row)               # defensive exposure: signals assembled, oracle clear

    n_fileready = overall["file_ready__file"] + overall["file_ready__clear"]
    # NON-degenerate iff at least ONE crime_type GENUINELY separates the classes — its file-ready proportion
    # among oracle-file differs from among oracle-clear, with BOTH classes present per crime_type (guard the
    # 0/0 hole). Judged PER crime_type, NOT on the pooled split: pooling is a Simpson's-paradox hazard (a
    # discriminating ML + an all-clear KYC could fake a pooled separation while neither class separates). A
    # deterministic, frozen, ADVISORY diagnostic — the T2 measure-first gate reads it; it does NOT gate
    # --check (which asserts the frozen value).
    def _separates(cc: dict) -> bool:
        nf = cc["file_ready__file"] + cc["not_ready__file"]
        nc = cc["file_ready__clear"] + cc["not_ready__clear"]
        if nf == 0 or nc == 0:                       # a crime_type missing either class cannot separate it
            return False
        return round(cc["file_ready__file"] / nf, 6) != round(cc["file_ready__clear"] / nc, 6)
    degenerate = (n_fileready == 0) or not any(_separates(cc) for cc in by_ct.values())

    return {
        "n_cases": oracle_split["file"] + oracle_split["clear"],
        "confusion": overall,
        "by_crime_type": {k: by_ct[k] for k in sorted(by_ct)},
        "oracle_split": oracle_split,
        "per_basis_fileready": {k: per_basis[k] for k in sorted(per_basis)},
        "n_missed_total": len(missed),
        "n_over_flag_total": len(over_flag),
        "degenerate": degenerate,
        "disagreement_sample": {
            "missed": missed[:_SAMPLE_CAP],
            "over_flag": over_flag[:_SAMPLE_CAP],
        },
    }


_DEFINITIONS = {
    "signal_file_ready": ("the BUNDLE-ONLY signal structure reaches the crime_type's file-bar STRUCTURE — "
                          "mechanism atom present AND >= the required corroborating legs — computed from the "
                          "merged fired capabilities alone, with the human-gate inputs (named predicate risk, "
                          "mitigation) HELD OUT. NOT a full determination, which also needs the held-out human "
                          "gate; this measures whether the §12 signal layer pre-positions the decision."),
    "file_ready__file": "signals assembled AND the oracle would file — the signal layer pre-positions correctly.",
    "file_ready__clear": ("OVER-FLAG: signals assembled but the oracle is clear — a defensive-filing exposure "
                          "(the signals fire on a benign case the human gate must dismiss)."),
    "not_ready__file": ("MISSED: the oracle would file but the signals did NOT assemble to file-ready — a §12 "
                        "signal/gather gap; the case's `missing` names the absent mechanism/leg to build."),
    "not_ready__clear": "signals not assembled AND the oracle is clear — appropriately not pre-positioned to file.",
    "degenerate": ("the structure does not discriminate: zero file-ready, or the file-ready rate among "
                   "oracle-file equals the rate among oracle-clear. If set, the measure-first gate down-scopes "
                   "to an honest report rather than a discovery feed."),
}


def _baseline_doc(summary: dict) -> dict:
    return {
        "note": ("EVAL-ONLY determination-validation baseline (Phase 78). The frozen per-class confusion "
                 "structure of signal-watch's bundle-only signal-assembly vs aml-substrate's exogenous "
                 "intended_disposition oracle (authored blind to the sufficiency rule). " + SYNTHETIC_QUALIFIER),
        "substrate_pin": SUBSTRATE_PIN,
        "definitions": _DEFINITIONS,
        **summary,
    }


# ---------------------------------------------------------------------------------------------------
# --freeze : build the capture from a substrate emit dir, then write the baseline.
def _run_id(out: Path, prefix: str) -> Path | None:
    base = out / "evidence"
    if not base.is_dir():
        return None
    cands = sorted(p for p in base.iterdir() if p.is_dir() and p.name.startswith(prefix))
    return cands[0] if cands else None


def _caps_by_case(run_dir: Path | None) -> dict:
    """case_id -> sorted fired capability set, from every CASE-*.json bundle in a run dir."""
    out: dict = {}
    if run_dir is None:
        return out
    for bp in sorted(run_dir.glob("CASE-*.json")):
        # fail-loud (the project ethos): a malformed bundle in a completed emit is a real defect to
        # surface, never a silent skip that would corrupt the capture's join.
        b = json.loads(bp.read_text(encoding="utf-8"))
        cid = b.get("case_id") or bp.stem
        out[cid] = sorted({a.get("capability") for a in b.get("alerts", []) if a.get("capability")})
    return out


def build_capture(out: Path) -> dict:
    """Join the disposition oracle to the screening (+ monitoring) bundles by case_id; merge caps per
    customer. Deterministic (substrate seed 0, no clock)."""
    oracle_path = out / "eval" / "intended_disposition.json"
    if not oracle_path.exists():
        raise SystemExit(f"--freeze: no oracle at {oracle_path} — the emit needs --emit-eval-oracles "
                         f"(+ --emergence --emit-screening). Run:\n  {EMIT_COMMAND}")
    oracle = json.loads(oracle_path.read_text(encoding="utf-8"))
    screening = _caps_by_case(_run_id(out, "screening-"))
    monitoring = _caps_by_case(_run_id(out, "seed"))      # monitoring run dir is `seed{S}-n{N}-m{M}`

    cases = []
    for row in oracle.get("dispositions", []):
        cid = row.get("case_id")
        scaps = screening.get(cid, [])
        mcaps = monitoring.get(cid, [])
        merged = sorted(set(scaps) | set(mcaps))
        cases.append({
            "case_id": cid,
            "screening_caps": scaps,
            "monitoring_caps": mcaps,
            "caps": merged,
            "oracle_disposition": row.get("intended_disposition"),
            "oracle_basis": row.get("intended_basis"),
        })
    cases.sort(key=lambda c: str(c["case_id"]))
    return {
        "note": ("EVAL-ONLY determination-validation capture (Phase 78). Per substrate slice case: the merged "
                 "(screening ∪ monitoring) fired capabilities + the EXOGENOUS intended_disposition oracle "
                 "(file|clear + basis, authored BLIND to the sufficiency rule). The oracle NEVER feeds the "
                 "engine — it is the comparison target only. " + SYNTHETIC_QUALIFIER),
        "substrate_pin": SUBSTRATE_PIN,
        "emit_command": EMIT_COMMAND,
        "population": ("the substrate screening-slice flagged customers (the population intended_disposition "
                       "covers), each enriched with its monitoring-slice signals — the per-customer merge the "
                       "workbench determination engine decides over."),
        "n_cases": len(cases),
        "cases": cases,
    }


def freeze() -> int:
    emit_dir = None
    if "--emit-dir" in sys.argv:
        emit_dir = Path(sys.argv[sys.argv.index("--emit-dir") + 1]).expanduser().resolve()
    if emit_dir is None or not emit_dir.is_dir():
        print("determination_validation_harness --freeze: pass --emit-dir <substrate --out dir>. Emit with:\n  "
              + EMIT_COMMAND)
        return 1
    capture = build_capture(emit_dir)
    summary = summarize(capture["cases"], _profile())
    doc = _baseline_doc(summary)
    _assert_no_banned(doc)                 # honesty governor BEFORE any write — a real pre-commit guard
    FIXDIR.mkdir(parents=True, exist_ok=True)
    CAPTURE.write_text(json.dumps(capture, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    BASELINE.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"determination_validation_harness --freeze: wrote {CAPTURE.relative_to(ROOT)} "
          f"({summary['n_cases']} cases) + {BASELINE.relative_to(ROOT)}")
    _print_matrix(summary)
    return 0


# ---------------------------------------------------------------------------------------------------
def _assert_no_banned(doc: dict) -> None:
    """The honesty governor — sweep every authored/rendered string in the doc; no %, Nx, lift/precision/
    recall/catch-rate/f1/auroc (REUSE osint_tools._BANNED, never re-declare)."""
    def walk(v):
        if isinstance(v, str):
            if _BANNED.search(v):
                raise AssertionError(f"honesty governor: a banned metric token (%/Nx/lift/precision/recall/"
                                     f"catch-rate) in: {v!r}")
        elif isinstance(v, dict):
            for x in v.values():
                walk(x)
        elif isinstance(v, list):
            for x in v:
                walk(x)
    walk(doc)


def _assert_doc_clean() -> None:
    """Extend the honesty governor to the DELIVERABLE PROSE: the named companion doc a presenter reads must
    pass the SAME _BANNED sweep the JSON/HTML artifacts do. The doc was the one authored surface the gate
    originally missed (a presenter reads prose, not baseline.json) — close that gap."""
    if not DELIVERABLE_DOC.exists():
        return
    for i, line in enumerate(DELIVERABLE_DOC.read_text(encoding="utf-8").splitlines(), 1):
        if _BANNED.search(line):
            raise AssertionError(f"honesty governor: {DELIVERABLE_DOC.name}:{i} carries a banned metric token "
                                 f"(%/Nx/lift/precision/recall/catch-rate): {line.strip()!r}")


def _print_matrix(summary: dict) -> None:
    c = summary["confusion"]
    print(f"  cases={summary['n_cases']}  oracle file/clear={summary['oracle_split']['file']}/"
          f"{summary['oracle_split']['clear']}  degenerate={summary['degenerate']}")
    print(f"  file_ready×file={c['file_ready__file']}  file_ready×clear(over-flag)={c['file_ready__clear']}  "
          f"not_ready×file(missed)={c['not_ready__file']}  not_ready×clear={c['not_ready__clear']}")
    for ct, cc in summary["by_crime_type"].items():
        print(f"    [{ct}] fr×f={cc['file_ready__file']} fr×c={cc['file_ready__clear']} "
              f"nr×f={cc['not_ready__file']} nr×c={cc['not_ready__clear']}")


def check() -> int:
    if not CAPTURE.exists() or not BASELINE.exists():
        print(f"determination_validation_harness --check: missing fixture(s) under "
              f"{FIXDIR.relative_to(ROOT)} — run --freeze (needs a substrate emit).")
        return 1
    capture = json.loads(CAPTURE.read_text(encoding="utf-8"))
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    got = summarize(capture["cases"], _profile())
    fails = [f"{k}: replay != frozen baseline" for k in _ASSERT_KEYS
             if json.dumps(got.get(k), sort_keys=True) != json.dumps(baseline.get(k), sort_keys=True)]
    _assert_no_banned(baseline)
    if fails:
        print("determination_validation_harness --check: FAIL (engine drift vs the frozen oracle)\n  "
              + "\n  ".join(fails))
        return 1
    print(f"determination_validation_harness --check: PASS — {got['n_cases']} cases, engine matches the frozen "
          f"confusion structure vs the exogenous oracle.")
    _print_matrix(got)
    return 0


# ---------------------------------------------------------------------------------------------------
def _selftest() -> int:
    prof = _profile()
    fails = []

    # (1) the firewall REJECTS a leaked oracle field (a renamed surrogate does not pass).
    clean = [engine_input({"case_id": "CASE-X", "caps": ["C3", "C8"], "oracle_disposition": "file"})]
    assert_no_oracle_leak(clean)
    leaked = [dict(clean[0], intended_disposition="file")]
    try:
        assert_no_oracle_leak(leaked)
        fails.append("firewall must REJECT an oracle field on the engine input")
    except AssertionError as e:
        if "firewall" not in str(e):
            fails.append(f"firewall raised the wrong error: {e}")
    surrogate = [dict(clean[0], truth="file")]               # renamed surrogate still raises (allow-list)
    try:
        assert_no_oracle_leak(surrogate)
        fails.append("firewall must REJECT a renamed oracle surrogate (allow-list, not denylist)")
    except AssertionError:
        pass

    # (2) the engine is structurally blind to the oracle.
    try:
        assert_engine_blind_to_oracle()
    except AssertionError as e:
        fails.append(str(e))

    # (3) classify is correct on hand-checked cases (the bundle-only mechanism+>=2-legs recipe).
    ml_ready = classify(["C3", "C8", "C15"], prof)            # ML-A1 mech + ML-A3,ML-A4 legs -> file-ready
    if not (ml_ready["crime_type"] == "money_laundering" and ml_ready["file_ready"]
            and ml_ready["n_mech"] >= 1 and ml_ready["n_legs"] >= 2):
        fails.append(f"classify(C3,C8,C15) should be ML file-ready: {ml_ready}")
    ml_thin = classify(["C8"], prof)                          # ML-A3 leg only, no mechanism -> NOT ready
    if ml_thin["file_ready"] or ml_thin["n_mech"] != 0:
        fails.append(f"classify(C8) should be NOT file-ready (no mechanism): {ml_thin}")
    kyc = classify(["C14"], prof)                            # KYC-A1 mech, additional_legs_required 0 -> ready
    if not (kyc["crime_type"] == "kyc_integrity" and kyc["file_ready"]):
        fails.append(f"classify(C14) should be kyc file-ready (mechanism alone): {kyc}")
    if classify([], prof)["crime_type"] is not None:
        fails.append("classify([]) should map to no crime_type")

    # (4) summarize is deterministic + correct on a tiny synthetic capture (the four cells).
    tiny = [
        {"case_id": "CASE-1", "caps": ["C3", "C8", "C15"], "oracle_disposition": "file", "oracle_basis": "structuring_below_threshold"},   # file_ready × file
        {"case_id": "CASE-2", "caps": ["C3", "C8", "C15"], "oracle_disposition": "clear", "oracle_basis": "legitimate_business_pattern"},  # file_ready × clear (over-flag)
        {"case_id": "CASE-3", "caps": ["C8"], "oracle_disposition": "file", "oracle_basis": "structuring_below_threshold"},                # not_ready × file (missed)
        {"case_id": "CASE-4", "caps": ["C8"], "oracle_disposition": "clear", "oracle_basis": "explained_source_of_funds"},                 # not_ready × clear
    ]
    s = summarize(tiny, prof)
    want = {"file_ready__file": 1, "file_ready__clear": 1, "not_ready__file": 1, "not_ready__clear": 1}
    if s["confusion"] != want:
        fails.append(f"summarize tiny confusion {s['confusion']} != {want}")
    if s["n_missed_total"] != 1 or s["n_over_flag_total"] != 1:
        fails.append(f"summarize tiny disagreements wrong: {s['n_missed_total']}/{s['n_over_flag_total']}")
    if [r["case_id"] for r in s["disagreement_sample"]["missed"]] != ["CASE-3"]:
        fails.append("the missed sample should name CASE-3")
    # determinism: same input -> byte-identical summary
    if json.dumps(summarize(tiny, prof), sort_keys=True) != json.dumps(s, sort_keys=True):
        fails.append("summarize is not deterministic")

    # (5) a DEGENERATE capture is reported, not crashed (zero file-ready -> degenerate True).
    degen = summarize([{"case_id": "CASE-D", "caps": ["C8"], "oracle_disposition": "file", "oracle_basis": None},
                       {"case_id": "CASE-E", "caps": ["C8"], "oracle_disposition": "clear", "oracle_basis": None}],
                      prof)
    if not degen["degenerate"]:
        fails.append("a zero-file-ready capture must be flagged degenerate")

    # (6) the honesty governor passes on the baseline doc (definitions + qualifier carry no banned token)
    #     AND on the deliverable PROSE (the doc surface the gate originally missed).
    try:
        _assert_no_banned(_baseline_doc(s))
        _assert_doc_clean()
    except AssertionError as e:
        fails.append(f"honesty governor flagged an authored surface: {e}")

    # (7) the engine file/determination bar shape is intact (this harness only READS it).
    import inspect
    if "named_predicate_risk" not in inspect.signature(er.evaluate_sufficiency).parameters:
        fails.append("evidence_requirements.evaluate_sufficiency unexpectedly changed shape")

    # (8) the degenerate criterion judges PER crime_type (Simpson's-paradox guard): a non-discriminating ML
    #     (file-ready proportion equal across file/clear) + an all-clear, never-ready unmapped population must
    #     report DEGENERATE — pooling the rates across crime_types would falsely certify a separation.
    simpson = [
        {"case_id": "S1", "caps": ["C3", "C8", "C15"], "oracle_disposition": "file", "oracle_basis": None},   # ML ready × file
        {"case_id": "S2", "caps": ["C8"], "oracle_disposition": "file", "oracle_basis": None},                # ML not-ready × file
        {"case_id": "S3", "caps": ["C3", "C8", "C15"], "oracle_disposition": "clear", "oracle_basis": None},  # ML ready × clear
        {"case_id": "S4", "caps": ["C8"], "oracle_disposition": "clear", "oracle_basis": None},               # ML not-ready × clear
        {"case_id": "S5", "caps": [], "oracle_disposition": "clear", "oracle_basis": None},                   # unmapped, never ready
        {"case_id": "S6", "caps": [], "oracle_disposition": "clear", "oracle_basis": None},
    ]
    sp = summarize(simpson, prof)
    if not sp["degenerate"]:
        fails.append(f"the degenerate criterion must judge PER crime_type (Simpson guard) — "
                     f"neither class separates yet it reported non-degenerate: by_ct={sp['by_crime_type']}")

    if fails:
        print("determination_validation_harness --selftest: FAIL\n  " + "\n  ".join(fails))
        return 1
    print("determination_validation_harness --selftest: PASS (firewall + signature guard + classify + "
          "confusion recompute + degenerate handling + honesty governor)")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    sys.exit(freeze() if "--freeze" in sys.argv else check())
