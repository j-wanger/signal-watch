#!/usr/bin/env python3
"""Phase 70 — the GATHER extraction-quality REGRESSION GATE (the news_quality_harness pattern, minimal).

Pins ONE live capture of the GATHER loop (the model's raw responses) and REPLAYS it deterministically with
NO model, asserting the replayed outcome still matches the FROZEN BASELINE (the static oracle — it catches a
downstream gate / coverage / leg-mapping regression) and stays consistent with the deterministic StubPlanner
(which grounds a finding from every record it surfaces — consistency, not a catch-rate). This
guards the Phase-70 prompt fix: a future prompt/schema change that re-introduces the under-extraction (the
live model fetched the sanctions record but produced no grounded finding → finding_coverage 0.5,
target_closure 0.0) fails the gate.

  --check  (default)  replay the pinned capture, NO model — the committed regression gate.
  --freeze            re-capture from a LIVE model (OPENAI_BASE_URL / a local model) — the conscious
                      re-baseline. The corpus is SYNTHETIC, so re-capture carries no compliance gate.

Companion-only: build.py NEVER imports this; the 8 ship dists are unaffected. Dep-free (stdlib + the
companion scripts). Pure over the read-only corpus — persists nothing except the fixture on --freeze.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
ROOT = _HERE.parent
sys.path.insert(0, str(ROOT / "scripts"))

import osint_tools as ot           # noqa: E402  (companion modules; scripts/ on the path)
import serve_workbench as sw       # noqa: E402

FIXTURE = _HERE / "fixtures" / "workbench-gather" / "zane-zhao.replay.json"
_KEYS = ("finding_coverage", "complete", "target_closure", "grounded_record_ids", "closed")


class _ReplayModel:
    """Returns the pinned model responses IN ORDER — the live gather replayed with no network. The loop is
    deterministic given the same model outputs, so the gate + coverage run for real over a fixed transcript."""

    def __init__(self, responses):
        self._r, self._i = list(responses), 0

    def __call__(self, messages):
        if self._i >= len(self._r):
            raise ot.GatherError("replay exhausted (the pinned capture has fewer calls than the loop made)")
        out = self._r[self._i]
        self._i += 1
        return out


def _cv(fx: dict) -> dict:
    return {"subject_name": fx["subject"], "subject_kind": "subject",
            "counterparties": fx.get("counterparties", [])}


def _summary(out: dict) -> dict:
    cov = out.get("coverage") or {}
    req = out.get("requirement") or {}
    return {"finding_coverage": cov.get("finding_coverage"), "complete": cov.get("complete"),
            "grounded_record_ids": sorted(cov.get("grounded_record_ids", [])),
            "target_closure": req.get("target_closure"),
            "closed": sorted(c["id"] for c in req.get("closed", []))}


def _stub_reference(mule_id: str) -> list:
    """The deterministic reference: the StubPlanner grounds a finding from every record it surfaces."""
    out = sw.run_gather(mule_id, backend="stub", on_stage=lambda *a, **k: None)
    return sorted((out.get("coverage") or {}).get("grounded_record_ids", []))


def check() -> int:
    if not FIXTURE.exists():
        print(f"gather_quality_harness --check: NO fixture at {FIXTURE} — run --freeze (needs a live model)")
        return 1
    fx = json.loads(FIXTURE.read_text(encoding="utf-8"))
    idx = sw.load_index()
    mule_id = idx["meta"]["exemplars"]["mule"]
    # the planner reasons over the FIXTURE subject while run_gather grounds against the live case subject —
    # assert they agree so a re-pointed exemplar / hand-edited fixture fails loudly, never grounds silently
    # against a different subject.
    live_subject = sw.gather_view(sw._case_entry(idx, mule_id),
                                  json.loads(sw._bundle_path(mule_id).read_text(encoding="utf-8")))["subject_name"]
    assert fx["subject"] == live_subject, \
        f"fixture subject {fx['subject']!r} != the live case subject {live_subject!r} — re-freeze the fixture"
    planner = ot.LivePlanner(_cv(fx), _ReplayModel(fx["responses"]))           # the live decisions, replayed
    out = sw.run_gather(mule_id, backend="openai", on_stage=lambda *a, **k: None, planner=planner)
    got, exp, ref = _summary(out), fx["expected"], _stub_reference(mule_id)
    # the frozen `expected` block is the ORACLE (computed at --freeze, static — it catches a downstream gate /
    # coverage / leg-mapping regression). The stub check below is a CONSISTENCY check (the live replay should
    # agree with the deterministic stub); it SHARES gate_finding with the replay, so it is not an independent
    # oracle — the frozen baseline is.
    fails = [f"{k}: replay {got.get(k)!r} != frozen baseline {exp.get(k)!r}" for k in _KEYS if got.get(k) != exp.get(k)]
    if got["grounded_record_ids"] != ref:                                     # consistency vs the deterministic stub
        fails.append(f"live replay grounded {got['grounded_record_ids']} inconsistent with the stub {ref}")
    if fails:
        print("gather_quality_harness --check: FAIL\n  " + "\n  ".join(fails))
        return 1
    print(f"gather_quality_harness --check: PASS (live replay matches the frozen baseline + stays consistent "
          f"with the deterministic stub {ref}; finding_coverage={got['finding_coverage']}, "
          f"target_closure={got['target_closure']}, ML-A5 {got['closed']}, no model)")
    return 0


def freeze(env=None) -> int:
    """Re-capture from a LIVE model (the conscious re-baseline). Refuses to freeze a capture UNDER the stub
    reference — a re-baseline must still match the deterministic bar, never lock in a regression."""
    import os
    env = env if env is not None else os.environ
    index = sw.load_index()
    mule_id = index["meta"]["exemplars"]["mule"]
    entry = sw._case_entry(index, mule_id)
    bundle = json.loads(sw._bundle_path(mule_id).read_text(encoding="utf-8"))
    cv = sw.gather_view(entry, bundle)
    captured: list = []

    def cap(messages):
        r = ot.call_openai(messages, env)
        captured.append(r)
        return r

    planner = ot.LivePlanner(cv, cap)
    out = sw.run_gather(mule_id, backend="openai", on_stage=lambda *a, **k: None, planner=planner)
    got, ref = _summary(out), _stub_reference(mule_id)
    if (got["grounded_record_ids"] != ref or got["finding_coverage"] != 1.0
            or got["target_closure"] != 1.0 or got["complete"] is not True):
        print(f"gather_quality_harness --freeze: live capture is UNDER the stub reference or incomplete "
              f"(got {got}, reference {ref}) — fix the prompts before freezing, do not lock a regression")
        return 1
    fx = {"note": ("Phase 70 — pinned LIVE gather capture (a local model), replayed deterministically with NO "
                   "model in --check. The corpus is SYNTHETIC, so re-capture carries no compliance gate. The "
                   "'expected' block is the coverage-regression baseline; --freeze is the conscious re-baseline."),
          "model": env.get("OPENAI_MODEL", "local"), "subject": cv["subject_name"],
          "counterparties": cv["counterparties"], "responses": captured, "expected": got}
    FIXTURE.parent.mkdir(parents=True, exist_ok=True)
    FIXTURE.write_text(json.dumps(fx, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"gather_quality_harness --freeze: wrote {FIXTURE.relative_to(ROOT)} "
          f"({len(captured)} responses; expected {got})")
    return 0


if __name__ == "__main__":
    sys.exit(freeze() if "--freeze" in sys.argv else check())
