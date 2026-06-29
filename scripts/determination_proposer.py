#!/usr/bin/env python3
"""Phase 85 — the §12 determination pre-proposer (companion-only): an AGENT proposes each case's §12
determination, MEASURED against aml-substrate's EXOGENOUS intended_disposition oracle (the SAME committed
capture the determination-validation harness froze, Phase 78) — the agentification roadmap's Stage 2, the
6th live loop, the second *measurable* agent after the Phase-83 merge adjudicator
(docs/agentification-roadmap.md).

propose -> gate -> decide. The agent PROPOSES one of {file, clear, needs_more_info} + a rationale from the
case EVIDENCE ONLY (the fired capabilities + the mapped crime_type — the oracle firewall, the SAME allow-list
the validation harness enforces). score_proposals() MEASURES agreement vs the exogenous oracle: COUNTS-only,
TWO-SIDED by oracle class (file|clear) + crime_type, abstentions (needs_more_info) counted SEPARATELY (never
scored as a wrong call — an agent that knows when to defer is a feature, the human-gate doctrine). No rate,
score, or multiplier is claimed. The deterministic sufficiency engine still LICENSES the determination
(evidence_requirements — BYTE-UNCHANGED); the human still DECIDES. The agent's call is a measured proposal
beside the latent truth.

THE HONEST HEADROOM (the A1 frame, gate-accepted). The agent's measurable headroom is on the OVER-FLAG /
clear side — correcting the engine's STRUCTURAL false-files (the 727 KYC-pure cases the rigid sufficiency
rule marks file-ready though a customer-due-diligence gap ALONE, with no laundering mechanism, is not a
filing basis). On the file-MISS side it ties the engine: the 71 missed oracle-file cases are a DATA gap (the
second corroborating leg is not in the bundle — substrate Ask #3 measured-null at HEAD 3716f77), so reasoning
over the same evidence cannot recover them. A null on the miss side IS the finding (it shows the misses are
substrate-gated, not reasoning-gated).

Two proposers mirror the merge StubAdjudicator/LiveAdjudicator + the GATHER stub/live split:
- StubProposer — deterministic, NO model: echoes the engine's bundle-only verdict (classify().file_ready ->
  "file" else "needs_more_info"; bundle-only the engine cannot affirmatively CLEAR, so it abstains). The
  offline default + the engine-vs-oracle baseline (the Phase-78 confusion: commits "file" on the 1370
  file-ready cases [50 agree on oracle-file + 1320 disagree over-flags], abstains on the 5565 not-ready).
- LiveProposer — the agent under test: reads caps + crime_type (+ deterministic capability descriptions),
  prompts a local OpenAI-compatible model via osint_tools.call_openai (temperature 0), parse_llm_json
  fail-closed to needs_more_info, constrained to the 3-way closed vocab. Because the proposal is a function
  of (caps, crime_type) ALONE, _SignatureCache dedupes by cap-signature — 46 distinct signatures cover all
  6935 capture cases, so the FULL population is measured with 46 live calls (no sampling; full coverage).

THE ORACLE FIREWALL (load-bearing). The proposer sees ONLY the engine-input view (case_id + caps +
crime_type); proposer_input() strips to that allow-list and assert_no_oracle_leak() RAISES on
intended_disposition / a renamed surrogate / ANY extra key — REUSED verbatim from the validation harness (the
schema boundary, not the field name, so renaming the leak does not pass). Non-circular by construction (the
Phase-77 circular-oracle trap avoided): the oracle was authored BLIND to the sufficiency rule and never
reaches a proposer input.

COMPANION-ONLY. build.py NEVER imports this. evidence_requirements is READ for the engine baseline +
crime_type mapping; the file/determination bar is BYTE-UNCHANGED (the agent proposes, the engine licenses,
the human decides). Scoring the StubProposer is DEP-FREE; only the LIVE agent path needs a model.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
ROOT = _HERE.parent

import determination_validation_harness as dvh  # noqa: E402  (the firewall + engine baseline + the capture)

CAP_TAXONOMY = ROOT / "data" / "capability-taxonomy.json"

# ── the closed vocabulary ──
VOCAB = ("file", "clear", "needs_more_info")
COMMITTED = ("file", "clear")          # the only calls the binary oracle SCORES
ABSTENTION = ("needs_more_info",)      # honest "defer to the human" — counted, never scored

# the mandatory honesty qualifier on EVERY reported number (REUSE the validation harness's).
PROPOSER_QUALIFIER = dvh.SYNTHETIC_QUALIFIER

# the oracle firewall — REUSED verbatim from the validation harness (the same allow-list {case_id, caps,
# crime_type}; an intended_disposition / oracle_basis / renamed surrogate / any extra key RAISES).
proposer_input = dvh.engine_input
assert_no_oracle_leak = dvh.assert_no_oracle_leak


def load_cases(path: Path | None = None) -> list:
    """The committed determination-validation capture cases that carry a scored oracle (file|clear) — the
    SAME frozen capture the validation harness measures the engine over. Read-only; no substrate, no model."""
    data = json.loads((path or dvh.CAPTURE).read_text(encoding="utf-8"))
    return [c for c in data.get("cases", []) if c.get("oracle_disposition") in COMMITTED]


def _load_cap_names(path: Path | None = None) -> dict:
    """code -> human-readable capability name (deterministic, from the committed taxonomy). Used ONLY to
    enrich the prompt; derived from caps, never added to the firewalled input — the allow-list stays tight."""
    try:
        d = json.loads((path or CAP_TAXONOMY).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return {c["id"]: c.get("name", c["id"]) for c in d.get("capabilities", []) if c.get("id")}


# --------------------------------------------------------------------------------------------------
# the proposers (the merge stub/live split)
# --------------------------------------------------------------------------------------------------
class StubProposer:
    """Deterministic baseline — echoes the engine's bundle-only verdict. No model. The offline default + the
    engine-vs-oracle baseline the live agent is measured against. file_ready -> "file"; not file-ready ->
    "needs_more_info" (bundle-only the engine cannot affirmatively CLEAR, so it abstains honestly)."""

    name = "stub"

    def __init__(self, profile: dict | None = None):
        self.profile = profile or dvh._profile()

    def propose(self, ev: dict) -> dict:
        cls = dvh.classify(ev.get("caps") or [], self.profile)
        ready = cls["file_ready"]
        call = "file" if ready else "needs_more_info"
        return {"call": call,
                "rationale": ("deterministic engine baseline: the bundle-only signal is "
                              f"{'file-ready' if ready else 'not file-ready'} "
                              f"({cls['n_mech']} mechanism / {cls['n_legs']} legs for {cls['crime_type']})")}


_SYSTEM = (
    "You are an AML determination pre-proposer reviewing a transaction-monitoring case. You are given the "
    "case's FIRED DETECTION CAPABILITIES (signal codes with plain-language descriptions) and the mapped crime "
    "type. Decide whether the evidence, AS ASSEMBLED, supports FILING a suspicious-activity report, "
    "affirmatively CLEARING the case, or is INSUFFICIENT to call either way. Weigh whether a laundering "
    "MECHANISM is present AND corroborated by independent legs: a single control gap on its own — e.g. a "
    "customer-due-diligence / KYC gap with NO laundering mechanism — is NOT by itself a filing basis. "
    # The BASE-RATE discipline below is the documented transaction-monitoring false-positive reality (a public
    # AML standard, NOT this case's oracle label) — the user's Phase-85 call to give the agent fair population
    # context; ONE principled revision, not iterated-to-fit against the oracle.
    "IMPORTANT — the base-rate reality of transaction monitoring: detection signals are tuned for sensitivity "
    "and the OVERWHELMING majority of alerted cases turn out benign. Several red flags CO-OCCURRING is common "
    "among ordinary legitimate customers and is NOT by itself proof of laundering. File ONLY when the "
    "assembled evidence SPECIFICALLY establishes a laundering mechanism with independent corroboration that a "
    "legitimate customer would not plausibly exhibit; when the same signals are equally consistent with "
    "ordinary business, prefer needs_more_info (defer to the human) over filing. Reply with STRICT JSON only: "
    '{"call": one of "file"|"clear"|"needs_more_info", "rationale": "<one sentence>"}. '
    "file = the assembled signals specifically support a report; clear = the assembled signals affirmatively "
    "indicate no suspicious activity; needs_more_info = insufficient to call either way (defer to the human). "
    "Be decisive when the evidence genuinely supports filing; otherwise defer rather than over-file."
)


def _user_prompt(ev: dict, cap_names: dict) -> str:
    caps = list(ev.get("caps") or [])
    lines = "\n".join(f"  - {c}: {cap_names.get(c, c)}" for c in caps) or "  (no capabilities fired)"
    return (
        f"Crime type (mapped from the fired capabilities): {ev.get('crime_type') or 'unmapped'}\n"
        f"Fired detection capabilities:\n{lines}\n\n"
        "Does the assembled evidence support filing, clearing, or is it insufficient? "
        "Reply with the strict JSON object."
    )


class LiveProposer:
    """The agent under test — reads the EVIDENCE (never the oracle) and proposes a call via a local
    OpenAI-compatible model. Strict-JSON only; fail-closed to needs_more_info (an honest abstention, counted
    never scored) when the model returns no valid call."""

    name = "live"

    def __init__(self, call_model, cap_names: dict | None = None):
        self.call_model = call_model              # messages -> raw str (e.g. lambda m: osint_tools.call_openai(m, env))
        self.cap_names = cap_names if cap_names is not None else _load_cap_names()

    def propose(self, ev: dict) -> dict:
        import osint_tools as ot                  # lazy: the live path only; scoring stays dep-light
        messages = [{"role": "system", "content": _SYSTEM},
                    {"role": "user", "content": _user_prompt(ev, self.cap_names)}]
        raw = self.call_model(messages)
        obj = ot.parse_llm_json(raw)
        if not isinstance(obj, dict) or obj.get("call") not in VOCAB:
            return {"call": "needs_more_info",
                    "rationale": "model returned no valid call (fail-closed to needs_more_info — an abstention)"}
        return {"call": obj["call"], "rationale": str(obj.get("rationale", ""))[:500]}


class _SignatureCache:
    """Memoize a proposer's call by cap-SIGNATURE (the sorted fired-capability set). The proposal is a
    function of (caps, crime_type) alone, so identical signatures get one call — 46 distinct signatures cover
    all 6935 capture cases, making the FULL-population live measurement 46 model calls (no sampling). Exposes
    `.signatures` (signature -> proposal) so --freeze can pin exactly what the model decided."""

    def __init__(self, inner):
        self.inner = inner
        self.name = inner.name
        self.signatures: dict = {}

    @staticmethod
    def _sig(ev: dict):
        return tuple(sorted({c for c in (ev.get("caps") or []) if c}))

    def propose(self, ev: dict) -> dict:
        sig = self._sig(ev)
        if sig not in self.signatures:
            self.signatures[sig] = self.inner.propose(ev)
        return dict(self.signatures[sig])


# --------------------------------------------------------------------------------------------------
# scoring — COUNTS-only agreement vs the exogenous oracle, TWO-SIDED, abstentions separate
# --------------------------------------------------------------------------------------------------
def _blank() -> dict:
    return {"agree": 0, "disagree": 0, "abstain": 0, "n": 0}


def score_proposals(cases: list, proposer) -> dict:
    """Run `proposer` over each case's firewalled EVIDENCE and count agreement vs the exogenous oracle
    (`oracle_disposition` ∈ {file, clear}). A committed call (file/clear) is AGREE iff it equals the oracle,
    else DISAGREE; an abstention (needs_more_info) is counted SEPARATELY (never scored — the human-gate
    doctrine). The split is TWO-SIDED — by oracle class AND by crime_type — so the over-flag (clear-side) and
    the miss (file-side) are visible distinctly. Every number is a COUNT; no rate/score/multiplier."""
    inputs = [proposer_input(c) for c in cases]
    assert_no_oracle_leak(inputs)                          # the firewall, before any proposal
    total = _blank()
    by_oracle: dict = defaultdict(_blank)
    by_crime_type: dict = defaultdict(_blank)
    calls: dict = defaultdict(int)
    for case, ev in zip(cases, inputs):
        disp = case.get("oracle_disposition")
        if disp not in COMMITTED:
            continue
        res = proposer.propose(ev)
        call = res["call"]
        calls[call] += 1
        ct = ev.get("crime_type") or "unmapped"
        if call in ABSTENTION:
            bucket = "abstain"
        elif call == disp:
            bucket = "agree"
        else:
            bucket = "disagree"
        for grp in (total, by_oracle[disp], by_crime_type[ct]):
            grp[bucket] += 1
            grp["n"] += 1
    committed = total["agree"] + total["disagree"]
    return {"proposer": proposer.name,
            "n_cases": total["n"],
            "agree": total["agree"], "disagree": total["disagree"], "abstain": total["abstain"],
            "committed": committed,
            "by_oracle": {k: dict(v) for k, v in by_oracle.items()},
            "by_crime_type": {k: dict(v) for k, v in by_crime_type.items()},
            "calls": dict(calls),
            "qualifier": PROPOSER_QUALIFIER}


def stub_baseline(cases: list | None = None) -> dict:
    """The always-available deterministic reference — score the StubProposer (the engine echo). No model."""
    return score_proposals(cases if cases is not None else load_cases(), StubProposer())


# --------------------------------------------------------------------------------------------------
def _selftest() -> int:
    """Offline, dep-free assertions over the committed capture: the firewall rejects an oracle leak (incl. a
    renamed surrogate); the StubProposer reproduces EXACTLY the Phase-78 engine-vs-oracle confusion as a
    two-sided proposal (commit-file on 1370 file-ready -> 50 agree + 1320 over-flag disagree, abstain on the
    5565 not-ready); the by_oracle/by_crime_type split is two-sided; the LiveProposer parse path fail-closes
    to an abstention; the signature cache covers the population with 46 calls; no banned word in the report."""
    cases = load_cases()
    assert len(cases) == 6935, f"expected 6935 scored capture cases, got {len(cases)}"

    # ── the firewall: a clean input passes; an oracle-leaked input (even renamed) is REJECTED ──
    clean = [proposer_input(c) for c in cases]
    assert all("oracle_disposition" not in x and "intended_disposition" not in x for x in clean), \
        "the proposer input must never carry the oracle disposition"
    assert_no_oracle_leak(clean)
    leaked = [dict(x, intended_disposition=c["oracle_disposition"]) for x, c in zip(clean, cases)]
    try:
        assert_no_oracle_leak(leaked)
        raise AssertionError("the firewall must REJECT an oracle leak")
    except AssertionError as e:
        assert "firewall" in str(e), e
    surrogate = [dict(x, truth=c["oracle_disposition"]) for x, c in zip(clean, cases)]
    try:
        assert_no_oracle_leak(surrogate)
        raise AssertionError("the firewall must REJECT a renamed truth surrogate")
    except AssertionError as e:
        assert "firewall" in str(e), e

    # ── the StubProposer reproduces the Phase-78 engine-vs-oracle confusion as a two-sided proposal ──
    rep = stub_baseline(cases)
    assert rep["agree"] == 50 and rep["disagree"] == 1320 and rep["abstain"] == 5565, \
        f"the engine baseline must be agree 50 / disagree 1320 (over-flag) / abstain 5565: {rep}"
    assert rep["committed"] == 1370 and rep["n_cases"] == 6935, rep
    bo = rep["by_oracle"]
    assert bo["file"] == {"agree": 50, "disagree": 0, "abstain": 71, "n": 121}, bo
    assert bo["clear"] == {"agree": 0, "disagree": 1320, "abstain": 5494, "n": 6814}, bo
    # the engine is RIGHT only where its file-ready signal matches an oracle-file; on the clear side it
    # over-flags (1320, of which the 727 KYC-pure cases are the structural class the agent's reason to exist).
    bct = rep["by_crime_type"]
    assert bct["kyc_integrity"] == {"agree": 0, "disagree": 727, "abstain": 0, "n": 727}, bct
    assert bct["money_laundering"] == {"agree": 50, "disagree": 593, "abstain": 5565, "n": 6208}, bct
    assert rep["calls"].get("file") == 1370 and rep["calls"].get("needs_more_info") == 5565, rep["calls"]
    assert rep["qualifier"] == PROPOSER_QUALIFIER

    # ── the LiveProposer parse path: a valid call scores; junk fail-closes to an abstention ──
    class _FakeModel:
        def __init__(self, payload):
            self.payload = payload

        def __call__(self, messages):
            return self.payload

    names = _load_cap_names()
    assert names.get("C14") and names.get("C3"), "capability names must load for the prompt"
    # an agent that CLEARS the KYC-pure over-flag (the honest over-flag recovery): on the kyc cases it agrees
    # with the oracle (clear) where the engine disagreed (over-flag) — a real, measured count.
    clearer = LiveProposer(_FakeModel('{"call": "clear", "rationale": "kyc gap alone, no mechanism"}'), names)
    cscore = score_proposals(cases, clearer)
    assert cscore["calls"].get("clear") == 6935 and cscore["abstain"] == 0, cscore["calls"]
    # all-clear agrees on the 6814 oracle-clear, disagrees on the 121 oracle-file — a measured two-sided count
    assert cscore["agree"] == 6814 and cscore["disagree"] == 121, cscore
    assert cscore["by_crime_type"]["kyc_integrity"]["agree"] == 727, cscore["by_crime_type"]
    junk = score_proposals(cases, LiveProposer(_FakeModel("not json at all"), names))
    assert junk["abstain"] == 6935 and junk["committed"] == 0, \
        f"junk model output must fail-closed to abstentions (counted, never scored): {junk}"

    # ── the signature cache covers the full population with 46 model calls (no sampling) ──
    class _CountingModel:
        def __init__(self):
            self.calls = 0

        def __call__(self, messages):
            self.calls += 1
            return '{"call": "needs_more_info", "rationale": "stubbed"}'

    cm = _CountingModel()
    cached = _SignatureCache(LiveProposer(cm, names))
    score_proposals(cases, cached)
    assert cm.calls == 46, f"the signature cache must reduce 6935 cases to 46 model calls, got {cm.calls}"
    assert len(cached.signatures) == 46, cached.signatures

    # ── the honesty governor: no banned metric token (rate/score/multiplier) anywhere in the report ──
    blob = json.dumps(rep)
    import osint_tools as ot
    assert not ot._BANNED.search(blob), f"banned metric token in the report: {blob[:200]}"

    print(  # noqa: T201
        f"determination_proposer --selftest: PASS — {rep['n_cases']} capture cases; the oracle firewall "
        f"rejects a leak (incl. a renamed surrogate); the StubProposer engine baseline is TWO-SIDED "
        f"agree {rep['agree']} / disagree {rep['disagree']} (over-flag, incl. all {bct['kyc_integrity']['n']} "
        f"KYC structural over-flags) / abstain {rep['abstain']}; the live parse path fail-closes to an "
        f"abstention; the signature cache covers the population in 46 calls. [{PROPOSER_QUALIFIER}]")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="The §12 determination pre-proposer (companion-only, Phase 85).")
    ap.add_argument("--selftest", action="store_true", help="offline dep-free assertions (firewall + baseline), exit")
    ap.add_argument("--report", action="store_true", help="print the StubProposer engine baseline as JSON")
    args = ap.parse_args()
    if args.selftest:
        return _selftest()
    if args.report:
        print(json.dumps(stub_baseline(), indent=2))  # noqa: T201
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
