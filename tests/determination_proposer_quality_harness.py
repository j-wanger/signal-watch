#!/usr/bin/env python3
"""Phase 85 — the §12 DETERMINATION-PROPOSER quality REGRESSION GATE (the merge_adjudicator /
gather_quality_harness pattern).

Pins the determination pre-proposer's measurement so it stays honest + reproducible:

  --check  (default)  DEP-FREE, NO model. Two layers:
      (1) re-derive the StubProposer baseline (the engine echo) from the committed determination-validation
          capture and assert it matches the frozen `stub_expected` — the deterministic, always-available
          regression that catches a capture/engine drift. No fixture-live-capture, no model.
      (2) IF the fixture carries a pinned LIVE capture, REPLAY it deterministically (no network): the live
          agent's proposal is a function of the cap-SIGNATURE alone, so the capture pins {signature ->
          proposal} (46 signatures cover all 6935 cases); the replay expands them over the full population
          and asserts the agent's two-sided counts still match the frozen `live_expected`.
  --freeze            re-compute `stub_expected` (always) + ATTEMPT one LIVE capture (a local model on :8080
                      via osint_tools.call_openai, deduped by signature -> 46 calls). On model success the
                      fixture gains live_signatures + live_expected; on no-model it is written STUB-ONLY with
                      a "live capture pending" note — NEVER a fabricated live number.

Every reported quantity is a COUNT; the measurement is TWO-SIDED (by oracle class + crime_type), abstentions
counted separately. The oracle is the EXOGENOUS aml-substrate intended_disposition (authored blind to the
sufficiency rule; synthetic slice — production has no ground truth). Companion-only — build.py NEVER imports
this; the 9 ship dists are unaffected. Scoring the stub is dep-free.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
ROOT = _HERE.parent
sys.path.insert(0, str(ROOT / "scripts"))

import determination_proposer as dp   # noqa: E402  (companion module; scripts/ on the path)
import osint_tools as ot              # noqa: E402

FIXTURE = _HERE / "fixtures" / "determination-proposer" / "proposer.replay.json"
_KEYS = ("n_cases", "agree", "disagree", "abstain", "committed", "by_oracle", "by_crime_type", "calls")


def _sig_key(ev: dict) -> str:
    """The cap-signature as a stable string key (sorted, '|'-joined) — the JSON-able form of the proposal's
    sole determinant. The empty signature (no caps fired) keys as ''."""
    return "|".join(sorted({c for c in (ev.get("caps") or []) if c}))


class _ReplayProposer:
    """Returns the pinned proposal for each case's cap-signature — the live capture replayed with NO network.
    score_proposals is deterministic given the per-signature proposal, so the firewall + counting run for real
    over a fixed transcript. A signature absent from the pin (capture drift) RAISES (caught + reported)."""

    name = "live"

    def __init__(self, signatures: dict):
        self.signatures = signatures

    def propose(self, ev: dict) -> dict:
        key = _sig_key(ev)
        if key not in self.signatures:
            raise KeyError(f"replay: no pinned proposal for cap-signature {key!r} — the capture drifted; re-freeze")
        return dict(self.signatures[key])


def _summary(rep: dict) -> dict:
    return {k: rep[k] for k in _KEYS}


def check() -> int:
    if not FIXTURE.exists():
        print(f"determination_proposer_quality_harness --check: NO fixture at {FIXTURE} — run --freeze")
        return 1
    fx = json.loads(FIXTURE.read_text(encoding="utf-8"))
    cases = dp.load_cases()

    # ── layer 1: the deterministic StubProposer (engine echo) baseline (dep-free, always checkable) ──
    stub_got = _summary(dp.stub_baseline(cases))
    if stub_got != fx.get("stub_expected"):
        print("determination_proposer_quality_harness --check: FAIL (stub/engine baseline drifted from the "
              "frozen capture)\n"
              f"  got      {json.dumps(stub_got, sort_keys=True)}\n"
              f"  expected {json.dumps(fx.get('stub_expected'), sort_keys=True)}")
        return 1

    # ── layer 2: the pinned LIVE capture, replayed deterministically by signature (if present) ──
    if fx.get("live_signatures") and fx.get("live_expected"):
        try:
            live_got = _summary(dp.score_proposals(cases, _ReplayProposer(fx["live_signatures"])))
        except KeyError as e:
            print(f"determination_proposer_quality_harness --check: FAIL (capture drift) — {e}")
            return 1
        if live_got != fx["live_expected"]:
            fails = [f"{k}: replay {json.dumps(live_got.get(k), sort_keys=True)} != frozen "
                     f"{json.dumps(fx['live_expected'].get(k), sort_keys=True)}"
                     for k in _KEYS if live_got.get(k) != fx["live_expected"].get(k)]
            print("determination_proposer_quality_harness --check: FAIL (live replay drifted)\n  "
                  + "\n  ".join(fails))
            return 1
        le = fx["live_expected"]
        ov = le["by_oracle"]
        print(f"determination_proposer_quality_harness --check: PASS — engine baseline holds "
              f"(agree {stub_got['agree']} / over-flag disagree {stub_got['disagree']} / abstain "
              f"{stub_got['abstain']}); live agent replay matches the frozen capture (agent agree {le['agree']} "
              f"/ disagree {le['disagree']} / abstain {le['abstain']} over {le['n_cases']} cases; on the clear "
              f"side disagree {ov['clear']['disagree']} vs the engine's {stub_got['by_oracle']['clear']['disagree']}; "
              f"no model) [{dp.PROPOSER_QUALIFIER}]")
        return 0

    print(f"determination_proposer_quality_harness --check: PASS — StubProposer engine baseline holds "
          f"(agree {stub_got['agree']} / over-flag disagree {stub_got['disagree']} / abstain {stub_got['abstain']} "
          f"over {stub_got['n_cases']} cases, no model). Live agent capture PENDING (run --freeze with a model "
          f"on :8080). [{dp.PROPOSER_QUALIFIER}]")
    return 0


def freeze(env=None) -> int:
    """Re-compute the stub baseline (always) + ATTEMPT one live capture (deduped by signature -> 46 model
    calls). Never fabricates a live number — on no model the fixture is written stub-only with a pending note."""
    import os
    env = env if env is not None else os.environ
    cases = dp.load_cases()
    stub_expected = _summary(dp.stub_baseline(cases))
    fx = {"note": ("Phase 85 — the §12 determination-proposer regression gate. `stub_expected` is the "
                   "deterministic StubProposer (engine echo) baseline over the committed determination-"
                   "validation capture (dep-free, always checked). `live_signatures`/`live_expected`, when "
                   "present, are ONE pinned live capture: the agent's proposal per cap-signature (46 cover all "
                   "6935 cases) replayed with NO model in --check. The oracle is the EXOGENOUS aml-substrate "
                   "intended_disposition (synthetic slice; production has no ground truth). Counts only — no "
                   "rate, score, or multiplier is claimed; the measurement is two-sided (by oracle class + "
                   "crime_type), abstentions separate."),
          "model": env.get("OPENAI_MODEL", "local"),
          "stub_expected": stub_expected}

    cached = dp._SignatureCache(dp.LiveProposer(lambda m: ot.call_openai(m, env)))
    try:
        live_rep = dp.score_proposals(cases, cached)
        fx["live_signatures"] = {"|".join(sig): prop for sig, prop in sorted(cached.signatures.items())}
        fx["live_expected"] = _summary(live_rep)
        le = fx["live_expected"]
        live_note = (f"live captured: {len(cached.signatures)} signatures; agent agree {le['agree']} / "
                     f"disagree {le['disagree']} / abstain {le['abstain']} over {le['n_cases']} cases")
    except ot.GatherError as e:
        live_note = f"live capture PENDING — no model reachable ({e}); fixture written stub-only (not fabricated)"

    FIXTURE.parent.mkdir(parents=True, exist_ok=True)
    FIXTURE.write_text(json.dumps(fx, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"determination_proposer_quality_harness --freeze: wrote {FIXTURE.relative_to(ROOT)} "
          f"(stub baseline agree {stub_expected['agree']} / disagree {stub_expected['disagree']}; {live_note})")
    return 0


if __name__ == "__main__":
    sys.exit(freeze() if "--freeze" in sys.argv else check())
