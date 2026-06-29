#!/usr/bin/env python3
"""Phase 83 — the MERGE-ADJUDICATOR quality REGRESSION GATE (the gather_quality_harness pattern).

Pins the merge adjudicator's measurement so it stays honest + reproducible:

  --check  (default)  DEP-FREE, NO model. Two layers:
      (1) re-derive the StubAdjudicator baseline from the committed data/merge/cases.json and assert it
          matches the frozen `stub_expected` (the deterministic, always-available regression — catches a
          cases.json oracle drift). This layer needs NO fixture-live-capture and NO model.
      (2) IF the fixture carries a pinned LIVE capture, REPLAY it deterministically (no network) through the
          LiveAdjudicator and assert the agent's calls + agreement counts still match the frozen
          `live_expected` (the GATHER replay pattern — a fixed transcript, the gate runs for real over it).
  --freeze            re-compute `stub_expected` (always) + ATTEMPT one LIVE capture (a local model on
                      :8080 via osint_tools.call_openai). On model success the fixture gains
                      live_responses + live_expected; on no-model the fixture is written STUB-ONLY with a
                      "live capture pending" note — NEVER a fabricated live number.

Every reported quantity is a COUNT; no rate, score, or multiplier is computed. The oracle is SYNTHETIC +
synthetic-aml-substrate-slice; production has no ground truth. Companion-only — build.py NEVER imports this;
the 9 ship dists are unaffected. Scoring is dep-free (the committed oracle is already resolved; no duckdb).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
ROOT = _HERE.parent
sys.path.insert(0, str(ROOT / "scripts"))

import merge_adjudicator as ma   # noqa: E402  (companion module; scripts/ on the path)
import osint_tools as ot         # noqa: E402

FIXTURE = _HERE / "fixtures" / "merge-adjudicator" / "adjudicator.replay.json"
_KEYS = ("agree", "disagree", "deferred", "scored", "by_quadrant", "by_provenance", "by_basis", "calls")


class _ReplayModel:
    """Returns the pinned model responses IN ORDER — the live adjudication replayed with no network. The
    scorer is deterministic given the same model outputs, so the firewall + parsing + counting run for real
    over a fixed transcript."""

    def __init__(self, responses):
        self._r, self._i = list(responses), 0

    def __call__(self, messages):
        if self._i >= len(self._r):
            raise ot.GatherError("replay exhausted (the pinned capture has fewer calls than cases)")
        out = self._r[self._i]
        self._i += 1
        return out


def _summary(rep: dict) -> dict:
    return {k: rep[k] for k in _KEYS}


def check() -> int:
    if not FIXTURE.exists():
        print(f"merge_adjudicator_quality_harness --check: NO fixture at {FIXTURE} — run --freeze")
        return 1
    fx = json.loads(FIXTURE.read_text(encoding="utf-8"))

    # ── layer 1: the deterministic StubAdjudicator baseline (dep-free, always checkable) ──
    stub_got = _summary(ma.stub_baseline())
    if stub_got != fx.get("stub_expected"):
        print("merge_adjudicator_quality_harness --check: FAIL (stub baseline drifted from the frozen oracle)\n"
              f"  got      {json.dumps(stub_got, sort_keys=True)}\n"
              f"  expected {json.dumps(fx.get('stub_expected'), sort_keys=True)}")
        return 1

    # ── layer 2: the pinned LIVE capture, replayed deterministically (if present) ──
    if fx.get("live_responses") and fx.get("live_expected"):
        planner = ma.LiveAdjudicator(_ReplayModel(fx["live_responses"]))
        live_got = _summary(ma.score_adjudications(ma.load_cases(), planner))
        if live_got != fx["live_expected"]:
            fails = [f"{k}: replay {live_got.get(k)!r} != frozen {fx['live_expected'].get(k)!r}"
                     for k in _KEYS if live_got.get(k) != fx["live_expected"].get(k)]
            print("merge_adjudicator_quality_harness --check: FAIL (live replay drifted)\n  " + "\n  ".join(fails))
            return 1
        le = fx["live_expected"]
        print(f"merge_adjudicator_quality_harness --check: PASS — stub baseline holds "
              f"({stub_got['agree']} right / {stub_got['disagree']} wrong); live agent replay matches the frozen "
              f"capture (agent {le['agree']} agree / {le['disagree']} disagree / {le['deferred']} deferred over "
              f"{le['scored']} scored; no model) [{ma.ADJUDICATOR_QUALIFIER}]")
        return 0

    print(f"merge_adjudicator_quality_harness --check: PASS — StubAdjudicator baseline holds "
          f"({stub_got['agree']} right / {stub_got['disagree']} wrong / {stub_got['deferred']} deferred over the "
          f"{stub_got['scored']} scored cases, no model). Live agent capture PENDING (run --freeze with a model "
          f"on :8080). [{ma.ADJUDICATOR_QUALIFIER}]")
    return 0


def freeze(env=None) -> int:
    """Re-compute the stub baseline (always) + ATTEMPT one live capture. Never fabricates a live number — on
    no model the fixture is written stub-only with a pending note."""
    import os
    env = env if env is not None else os.environ
    cases = ma.load_cases()
    stub_expected = _summary(ma.stub_baseline(cases))
    fx = {"note": ("Phase 83 — the merge-adjudicator regression gate. `stub_expected` is the deterministic "
                   "StubAdjudicator baseline over the committed oracle (dep-free, always checked). "
                   "`live_responses`/`live_expected`, when present, are ONE pinned live capture replayed with "
                   "NO model in --check (the GATHER replay pattern). The oracle is synthetic + "
                   "synthetic-aml-substrate-slice; production has no ground truth. No rate, score, or "
                   "multiplier is claimed — counts only."),
          "model": env.get("OPENAI_MODEL", "local"),
          "stub_expected": stub_expected}

    captured: list = []

    def cap(messages):
        r = ot.call_openai(messages, env)
        captured.append(r)
        return r

    try:
        live_rep = ma.score_adjudications(cases, ma.LiveAdjudicator(cap))
        fx["live_responses"] = captured
        fx["live_expected"] = _summary(live_rep)
        live_note = (f"live captured: {len(captured)} responses; agent {fx['live_expected']['agree']} agree / "
                     f"{fx['live_expected']['disagree']} disagree / {fx['live_expected']['deferred']} deferred")
    except ot.GatherError as e:
        live_note = f"live capture PENDING — no model reachable ({e}); fixture written stub-only (not fabricated)"

    FIXTURE.parent.mkdir(parents=True, exist_ok=True)
    FIXTURE.write_text(json.dumps(fx, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"merge_adjudicator_quality_harness --freeze: wrote {FIXTURE.relative_to(ROOT)} "
          f"(stub baseline {stub_expected['agree']} right / {stub_expected['disagree']} wrong; {live_note})")
    return 0


if __name__ == "__main__":
    sys.exit(freeze() if "--freeze" in sys.argv else check())
