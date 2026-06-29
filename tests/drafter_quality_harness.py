#!/usr/bin/env python3
"""Phase 86 — the STR-DRAFTER quality REGRESSION GATE (Agentification Stage 3; the gather/merge_adjudicator pattern).

CONSISTENCY-NOT-CORRECTNESS by design: the STR drafter has NO correctness oracle (free-text drafting). Its
gate is aml-casework's six Class-G grounding verifiers — a binary SIGNED / REFUSED + blocking_violations
(citation + corpus grounding + the fabrication guard). There is no "gold narrative" truth, so this harness
does NOT score accuracy; it MEASURES the live (local) drafter against the deterministic stub over the
committed designed-scenario bundles, COUNTS ONLY:

  - stub-vs-live SIGN / REFUSE (the verifiers are the arbiter),
  - the verifier / fabrication-guard CATCH (a live draft the verifiers refuse — blocking_violations),
  - per-case CONSISTENCY (does the live drafter reach the same sign/refuse outcome as the stub?),
  - RECOVERED (the stub fail-closes, the live drafter produces a narrative the verifiers accept).

NO rate, score, or multiplier is computed; NEVER an accuracy / catch-rate / precision / recall. The bundles
are SYNTHETIC; production has no narrative ground truth. The population spans SIGN and REFUSE because the
deterministic stub FAIL-CLOSES on the hard narrative-seam case (CASE-P-0025128, a txn-bearing C14) — the
two-sided contrast point (Phase-82 finding).

  --check   (default)  DEP-FREE, NO model, NO casework subprocess. Replay the pinned per-bundle consume
                       results (stub + live) through the pure score_drafts() scorer and assert the counts
                       still match the frozen `expected` (catches a scorer regression or a pinned-data edit).
                       No fixture -> run --freeze.
  --freeze             Run the REAL casework consume (drafter=stub, then drafter=openai on :8080) per bundle
                       -- needs the casework venv + a local model -- capture the per-bundle consume results,
                       score, write the fixture. No model reachable -> the casework drafter fails soft to the
                       stub (drafter_effective="stub"); the live side is recorded as that honest stub-fallback
                       with a pending note, NEVER a fabricated narrative outcome.
  --selftest           DEP-FREE unit check of score_drafts() over synthetic consume-result dicts.

Companion-only -- build.py NEVER imports this; the 9 ship dists are unaffected. aml-casework is MEASURED, not
modified (the Drafter Protocol + the six verifiers stay byte-frozen). scripts/evidence_requirements.py is
untouched -- the drafter is the downstream DECIDE beat, not the §12 sufficiency engine.
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

_HERE = Path(__file__).resolve().parent
ROOT = _HERE.parent
sys.path.insert(0, str(ROOT / "scripts"))

import serve_workbench as sw   # noqa: E402  (companion module; scripts/ on the path; dep-free import)

FIXTURE = _HERE / "fixtures" / "drafter-quality" / "drafter.replay.json"

DRAFTER_QUALIFIER = "synthetic bundles; consistency-not-correctness (no narrative ground truth)"

# The designed-scenario population: the committed casefile bundles (file + cleared dispositions) + the ONE
# narrative-seam slice case the deterministic stub FAIL-CLOSES on (the two-sided contrast). NOT a slice
# sample (Phase-86 A3) -- each entry is a distinct, deliberate drafter scenario.
POPULATION = [
    {"label": "Riverside (cleared-demo)", "bundle": "data/casefile/cleared-demo.bundle.json",
     "disposition": "cleared"},
    {"label": "Lakeshore (case-b, fan-in C3)", "bundle": "data/casefile/case-b.bundle.json",
     "disposition": "cleared"},
    {"label": "Sanctions C14 (file)", "bundle": "data/casefile/sanctions-c14-demo.bundle.json",
     "disposition": "file"},
    {"label": "Narrative-seam CASE-P-0025128 (file)", "bundle": "data/workbench/bundles/CASE-P-0025128.json",
     "disposition": "file"},
]

# The summary keys frozen into the fixture + compared in --check (counts only; by_case is the per-bundle detail).
_KEYS = ("n", "stub_signed", "stub_refused", "live_signed", "live_refused", "live_stub_fallback",
         "agree", "recovered", "caught", "by_case")


def _slim(res: dict) -> dict:
    """The measurable subset of a casework consume result (serve_chain._consume_result_from_sar)."""
    return {
        "signed": res.get("signed") is True,
        "blocking_violations": list(res.get("blocking_violations") or []),
        "narrative_present": bool(res.get("narrative_present")),
        "drafter_effective": res.get("drafter_effective"),
    }


def score_drafts(records: list) -> dict:
    """Pure, dep-free scorer over per-bundle {label, disposition, stub, live} consume-result records.

    Counts only -- no accuracy. `stub`/`live` are _slim() dicts (signed, blocking_violations,
    narrative_present, drafter_effective). The verifiers are the arbiter of signed/refused; a refused live
    draft carries blocking_violations (the fabrication guard among the six Class-G verifiers)."""
    by_case = []
    stub_signed = stub_refused = live_signed = live_refused = live_stub_fallback = 0
    agree = recovered = caught = 0
    for r in records:
        st, lv = r["stub"], r["live"]
        s_sign, l_sign = st["signed"], lv["signed"]
        stub_signed += s_sign
        stub_refused += not s_sign
        live_signed += l_sign
        live_refused += not l_sign
        if lv.get("drafter_effective") == "stub":
            live_stub_fallback += 1          # no model reachable -> the openai drafter fell soft to the stub
        if s_sign == l_sign:
            agree += 1                        # consistency: live reaches the same verifier outcome as the stub
        if (not s_sign) and l_sign:
            recovered += 1                    # the live drafter produced a narrative the stub could not
        if (not l_sign) and lv["blocking_violations"]:
            caught += 1                       # the verifier / fabrication guard refused the live draft
        by_case.append({
            "label": r["label"], "disposition": r["disposition"],
            "stub_signed": s_sign, "live_signed": l_sign,
            "live_effective": lv.get("drafter_effective"),
            "live_violations": lv["blocking_violations"],
        })
    return {
        "n": len(records),
        "stub_signed": stub_signed, "stub_refused": stub_refused,
        "live_signed": live_signed, "live_refused": live_refused,
        "live_stub_fallback": live_stub_fallback,
        "agree": agree, "recovered": recovered, "caught": caught,
        "by_case": by_case,
    }


def _summary(rep: dict) -> dict:
    return {k: rep[k] for k in _KEYS}


def _headline(s: dict, *, live_real: bool) -> str:
    live_src = "live agent (model on :8080)" if live_real else "no model -> live == stub fallback (pending)"
    return (f"{s['n']} designed bundles | stub signed {s['stub_signed']} / refused {s['stub_refused']} "
            f"(fail-close = the narrative-seam contrast) | {live_src}: signed {s['live_signed']} / "
            f"refused {s['live_refused']} (verifier-caught {s['caught']}, recovered {s['recovered']}); "
            f"consistent with the stub on {s['agree']}/{s['n']} [{DRAFTER_QUALIFIER}]")


def check() -> int:
    if not FIXTURE.exists():
        print(f"drafter_quality_harness --check: NO fixture at {FIXTURE.relative_to(ROOT)} — run --freeze "
              f"(needs the casework venv + a local model on :8080)")
        return 1
    fx = json.loads(FIXTURE.read_text(encoding="utf-8"))
    got = _summary(score_drafts(fx["records"]))
    exp = fx["expected"]
    fails = [f"{k}: replay {got.get(k)!r} != frozen {exp.get(k)!r}" for k in _KEYS if got.get(k) != exp.get(k)]
    if fails:
        print("drafter_quality_harness --check: FAIL (scorer drifted from the pinned capture)\n  "
              + "\n  ".join(fails))
        return 1
    print("drafter_quality_harness --check: PASS — " + _headline(got, live_real=bool(fx.get("live_real"))))
    return 0


# casework validates contract_version against a v0.3-only allowlist but TOLERATES the additive v0.5 fields
# (curate_workbench_cases._CASEWORK_VIEW_*). A v0.5 slice bundle is handed to casework as the v0.3 VIEW —
# the SAME bundle with the version string relabeled to "0.3" (the committed bundle stays honestly v0.5;
# casework grounds the identical v0.3 subset). The casefile bundles are already <=0.3 and pass through.
_CASEWORK_VIEW_VERSIONS = frozenset({"0.1", "0.2", "0.3"})
_CASEWORK_VIEW_VERSION = "0.3"


def _casework_view(bundle: Path, td: Path) -> Path:
    """Return a casework-ingestable path for `bundle`: as-is if its contract_version is in the allowlist,
    else a temp copy relabeled to the v0.3 view (mirrors curate's coverage-measurement translation)."""
    b = json.loads(bundle.read_text(encoding="utf-8"))
    if not b.get("contract_version") or b["contract_version"] in _CASEWORK_VIEW_VERSIONS:
        return bundle
    b["contract_version"] = _CASEWORK_VIEW_VERSION
    view = td / f"{bundle.stem}.v03view.json"
    view.write_text(json.dumps(b, ensure_ascii=False), encoding="utf-8")
    return view


def _consume(rec: dict, drafter: str, td: Path) -> dict:
    """Run the REAL casework consume for one bundle (a REFUSAL is a disposition outcome, not a crash)."""
    bundle = _casework_view(ROOT / rec["bundle"], td)
    out = td / f"{Path(rec['bundle']).stem}.{drafter}.signed.json"
    return _slim(sw.casework_consume_wb(bundle, out, drafter, disposition=rec["disposition"]))


def freeze(env=None) -> int:
    """Run the real casework consume (stub, then openai) per bundle, capture, score, write the fixture.
    Needs the casework venv (sw.RunError if absent). The openai drafter defaults to :8080; on no model it
    fails soft to the stub (drafter_effective='stub') -- recorded honestly, never a fabricated outcome."""
    import os
    env = env if env is not None else os.environ
    records = []
    with tempfile.TemporaryDirectory() as tmp:
        td = Path(tmp)
        for rec in POPULATION:
            try:
                stub = _consume(rec, "stub", td)
            except sw.RunError as e:
                print(f"drafter_quality_harness --freeze: casework consume unavailable for {rec['label']} "
                      f"({e}) — the casework venv is the prerequisite (python scripts/setup_workbench.py). "
                      f"Nothing written.")
                return 1
            live = _consume(rec, "openai", td)
            records.append({"label": rec["label"], "disposition": rec["disposition"],
                            "stub": stub, "live": live})
    rep = score_drafts(records)
    live_real = rep["live_stub_fallback"] < rep["n"]   # at least one live draft used the real model
    fx = {"note": ("Phase 86 — the STR-drafter regression gate (Agentification Stage 3). `records` are the "
                   "REAL per-bundle casework consume results (stub + live), pinned; --check replays them "
                   "through the pure score_drafts() scorer with NO subprocess + NO model (the gather replay "
                   "pattern). The STR drafter has NO correctness oracle — counts only, consistency-not-"
                   "correctness; no rate/score/multiplier; the bundles are synthetic. casework is measured, "
                   "not modified."),
          "model": env.get("OPENAI_MODEL", "local"),
          "live_real": live_real,
          "records": records,
          "expected": _summary(rep)}
    FIXTURE.parent.mkdir(parents=True, exist_ok=True)
    FIXTURE.write_text(json.dumps(fx, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"drafter_quality_harness --freeze: wrote {FIXTURE.relative_to(ROOT)} — " + _headline(rep, live_real=live_real))
    return 0


def selftest() -> int:
    """DEP-FREE unit check of score_drafts() over synthetic consume-result dicts (no venv, no model)."""
    def case(label, disp, ss, ls, lv_viol=(), lv_eff="local"):
        return {"label": label, "disposition": disp,
                "stub": {"signed": ss, "blocking_violations": [] if ss else ["x"], "narrative_present": True,
                         "drafter_effective": "stub"},
                "live": {"signed": ls, "blocking_violations": list(lv_viol), "narrative_present": ls or bool(lv_viol),
                         "drafter_effective": lv_eff}}
    recs = [
        case("sign-sign", "file", True, True),                          # consistent sign
        case("recovered", "file", False, True),                         # stub refused, live signed
        case("caught", "file", True, False, lv_viol=["fabrication"]),   # verifier-caught live refusal
        case("bare-refuse", "file", False, False),                      # live refused, NO violations (no narrative)
        case("no-model", "cleared", True, True, lv_eff="stub"),         # live fell back to stub
    ]
    s = score_drafts(recs)
    checks = {
        "n": s["n"] == 5,
        "stub_signed": s["stub_signed"] == 3,         # sign-sign, caught, no-model
        "stub_refused": s["stub_refused"] == 2,       # recovered, both-refuse
        "live_signed": s["live_signed"] == 3,         # sign-sign, recovered, no-model
        "live_refused": s["live_refused"] == 2,       # caught, both-refuse
        "live_stub_fallback": s["live_stub_fallback"] == 1,
        "agree": s["agree"] == 3,                      # sign-sign, both-refuse, no-model
        "recovered": s["recovered"] == 1,
        "caught": s["caught"] == 1,
        "by_case_len": len(s["by_case"]) == 5,
    }
    bad = [k for k, ok in checks.items() if not ok]
    if bad:
        print(f"drafter_quality_harness --selftest: FAIL — {bad}\n  got {json.dumps(_summary(s), default=list)}")
        return 1
    print(f"drafter_quality_harness --selftest: PASS (score_drafts counts correct over 5 synthetic cases; "
          f"dep-free, no venv/model) [{DRAFTER_QUALIFIER}]")
    return 0


if __name__ == "__main__":
    if "--freeze" in sys.argv:
        sys.exit(freeze())
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.exit(check())
