#!/usr/bin/env python3
"""Phase 83 — the merge adjudicator (companion-only): an AGENT proposes each merge call, MEASURED against
the committed non-circular oracle in data/merge/cases.json — the ONE gate with a correctness oracle. The
agentification roadmap's Stage 1, the first *measurable* agent (docs/agentification-roadmap.md).

propose -> gate -> decide: the agent PROPOSES one of {uphold_merge, reject_as_shares, both_defensible,
escalate} + a rationale from the pre-adjudication EVIDENCE ONLY (the oracle firewall); score_adjudications()
MEASURES agreement vs the committed oracle (COUNTS-only, by quadrant + provenance, deferrals separate, the
synthetic qualifier). No rate, score, or multiplier is claimed. The human still adjudicates; the agent's
call is a measured proposal beside the latent truth — the discipline is never relaxed.

Two adjudicators mirror the GATHER StubPlanner/LivePlanner split (osint_tools.py):
- StubAdjudicator — deterministic, NO model: echoes the resolver's `spine_verdict`
  (merged -> uphold_merge, kept_distinct -> reject_as_shares). The offline default + the TWO-SIDED baseline
  (right 33/66, wrong 33 on the committed slice: right on every correct-rejection + real-co-reference, wrong
  on every fragmentation-gap + over-merge-trap). The live agent's job is to beat it on the 33 the spine errs.
- LiveAdjudicator — the agent under test: reads the evidence, prompts a local OpenAI-compatible model via
  osint_tools.call_openai, parse_llm_json fail-closed, constrained to the 4-way closed vocab.

THE ORACLE FIREWALL (load-bearing): the adjudicator sees ONLY the evidence surface — NEVER the `oracle`
block. adjudicator_input() strips to the allow-list; assert_no_oracle_leak() RAISES on any truth field
(mirrors resolution_scorer.assert_no_cluster_leak — the schema boundary, not the field name, so renaming the
leak does not pass).

COMPANION-ONLY. build.py NEVER imports this. Scoring is DEP-FREE (the committed oracle is already resolved —
no duckdb/spine); only the LIVE agent path needs a model.
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
CASES_JSON = ROOT / "data" / "merge" / "cases.json"

# ── the closed vocabulary (shared with data/merge/cases.json `adjudication_grades`) ──
VOCAB = ("uphold_merge", "reject_as_shares", "both_defensible", "escalate")
BINARY = ("uphold_merge", "reject_as_shares")          # the only calls the binary oracle SCORES
DEFERRAL = ("both_defensible", "escalate")             # honest "defer to the human" — counted, never scored

# ── the merge-adjudication quadrants (shared vocab with resolution_scorer KLASS_*) ──
QUADRANTS = ("real-co-reference", "over-merge-trap", "fragmentation-gap", "correct-rejection")

# ── the oracle firewall: the agent sees ONLY this evidence surface (the a/b records carry identifiers +
#    sanctions_screen; the truth rides the SEPARATE top-level `oracle` block, which is stripped here). ──
EVIDENCE_KEYS = frozenset({"a", "b", "basis", "shared", "spine_verdict", "source", "id"})
# any of these on an adjudicator input is a truth LEAK (mirrors curate_merge_cases._TRUTH_LEAK_KEYS).
TRUTH_LEAK_KEYS = frozenset({"oracle", "same_entity", "correct_adjudication", "klass", "cluster", "note"})

# the mandatory honesty qualifier on EVERY reported number (synthetic + synthetic-aml-substrate slices).
ADJUDICATOR_QUALIFIER = "measured on synthetic + synthetic-aml-substrate-slice oracles; production has no ground truth"


def load_cases(path: Path | None = None) -> list:
    """The committed scored merge cases — the frozen oracle. Read-only; no duckdb, no re-curate."""
    data = json.loads((path or CASES_JSON).read_text(encoding="utf-8"))
    return [c for c in data.get("cases", []) if c.get("scored")]


def adjudicator_input(case: dict) -> dict:
    """Strip a case to the EVIDENCE surface the adjudicator is allowed to see — physically removing the
    `oracle` ground-truth (and anything else not in the allow-list)."""
    return {k: v for k, v in case.items() if k in EVIDENCE_KEYS}


def assert_no_oracle_leak(inputs) -> None:
    """The schema-boundary firewall: every adjudicator input carries ONLY allow-listed evidence keys. An
    `oracle` block, a renamed surrogate (`correct_adjudication`, `same_entity`, `klass`, …), or ANY extra
    field RAISES — the test is the schema boundary, not the field name, so renaming the leak does not pass."""
    for x in inputs:
        extra = set(x) - EVIDENCE_KEYS
        if extra:
            raise AssertionError(
                f"oracle-input firewall: case {x.get('id')!r} carries non-evidence field(s) {sorted(extra)} "
                f"— the oracle truth must NEVER reach the adjudicator")


# --------------------------------------------------------------------------------------------------
# the adjudicators (the GATHER stub/live split)
# --------------------------------------------------------------------------------------------------
class StubAdjudicator:
    """Deterministic baseline — echoes the resolver's `spine_verdict`. No model. The offline default + the
    TWO-SIDED baseline the live agent is measured against."""

    name = "stub"

    def adjudicate(self, ev: dict) -> dict:
        merged = ev.get("spine_verdict") == "merged"
        call = "uphold_merge" if merged else "reject_as_shares"
        return {"call": call,
                "rationale": f"deterministic spine baseline: the resolver {ev.get('spine_verdict')} these records"}


_SYSTEM = (
    "You are an entity-resolution merge adjudicator for an AML investigation. You are given TWO customer "
    "records that share a BASIS (a strong identifier like an exact email/phone, a weak one like an address, "
    "or only a name) and the deterministic resolver's own call. Decide whether they are the SAME real "
    "person/entity or DISTINCT entities that merely share an identifier. Weigh IDENTIFIER evidence over name "
    "similarity: a shared exact email/phone is strong but NOT conclusive (households, recycled numbers, data "
    "entry), and a shared name alone is weak. Reply with STRICT JSON only: "
    '{"call": one of "uphold_merge"|"reject_as_shares"|"both_defensible"|"escalate", "rationale": "<one '
    'sentence>"}. uphold_merge = same entity; reject_as_shares = distinct entities sharing an identifier '
    "(record a SHARES edge, not a merge); both_defensible = the evidence genuinely underdetermines it; "
    "escalate = insufficient to call either way. Prefer a decisive call when the evidence supports it; defer "
    "(both_defensible/escalate) only when it genuinely underdetermines."
)


def _record_line(rec: dict) -> str:
    ids = ", ".join(f"{i['kind']}={i['value']}" for i in rec.get("identifiers", []))
    line = f"name={rec.get('name')!r} kind={rec.get('kind')} role={rec.get('role')} identifiers=[{ids}]"
    scr = rec.get("sanctions_screen")
    if scr:
        line += f" sanctions_screen={{flagged={scr.get('flagged')}, source={scr.get('source')!r}}}"
    return line


def _user_prompt(ev: dict) -> str:
    shared = ev.get("shared")
    shared_s = f"{shared['kind']}={shared['value']!r}" if shared else "(name only — no shared identifier)"
    return (
        f"Record A: {_record_line(ev.get('a', {}))}\n"
        f"Record B: {_record_line(ev.get('b', {}))}\n"
        f"Shared basis: {ev.get('basis')} ({shared_s})\n"
        f"Deterministic resolver's call: {ev.get('spine_verdict')}\n\n"
        "Are A and B the same entity? Reply with the strict JSON object."
    )


class LiveAdjudicator:
    """The agent under test — reads the EVIDENCE (never the oracle) and proposes a call via a local
    OpenAI-compatible model. Strict-JSON only; fail-closed to `escalate` (an honest defer-to-human, counted
    as a deferral, never scored) when the model returns no valid call."""

    name = "live"

    def __init__(self, call_model):
        self.call_model = call_model        # messages -> raw str (e.g. lambda m: osint_tools.call_openai(m, env))

    def adjudicate(self, ev: dict) -> dict:
        import osint_tools as ot            # lazy: the live path only; scoring stays dep-light
        messages = [{"role": "system", "content": _SYSTEM},
                    {"role": "user", "content": _user_prompt(ev)}]
        raw = self.call_model(messages)
        obj = ot.parse_llm_json(raw)
        if not isinstance(obj, dict) or obj.get("call") not in VOCAB:
            return {"call": "escalate",
                    "rationale": "model returned no valid call (fail-closed to escalate — a deferral)"}
        return {"call": obj["call"], "rationale": str(obj.get("rationale", ""))[:500]}


# --------------------------------------------------------------------------------------------------
# scoring — COUNTS-only agreement vs the committed oracle, by quadrant + provenance, deferrals separate
# --------------------------------------------------------------------------------------------------
def _blank() -> dict:
    return {"agree": 0, "disagree": 0, "deferred": 0, "n": 0}


def score_adjudications(cases: list, adjudicator) -> dict:
    """Run `adjudicator` over each case's EVIDENCE (firewalled) and count agreement vs the committed oracle.
    A binary commitment (uphold_merge/reject_as_shares) is AGREE iff it equals the oracle, else DISAGREE; a
    deferral (both_defensible/escalate) is counted SEPARATELY (never scored as right/wrong — the human-gate
    doctrine: an agent that knows when to defer is a feature, not a miss). Every number is a COUNT; no rate,
    score, or multiplier is computed."""
    inputs = [adjudicator_input(c) for c in cases]
    assert_no_oracle_leak(inputs)                         # the firewall, before any proposal
    total = _blank()
    by_quadrant: dict = defaultdict(_blank)
    by_provenance: dict = defaultdict(_blank)
    by_basis: dict = defaultdict(_blank)
    calls: dict = defaultdict(int)
    for case, ev in zip(cases, inputs):
        res = adjudicator.adjudicate(ev)
        call = res["call"]
        calls[call] += 1
        oracle = case["oracle"]["correct_adjudication"]
        klass = case["oracle"]["klass"]
        prov = case.get("source")
        basis = case.get("basis")
        if call in DEFERRAL:
            bucket = "deferred"
        elif call == oracle:
            bucket = "agree"
        else:
            bucket = "disagree"
        for grp in (total, by_quadrant[klass], by_provenance[prov], by_basis[basis]):
            grp[bucket] += 1
            grp["n"] += 1
    scored = total["agree"] + total["disagree"]
    return {"adjudicator": adjudicator.name,
            "n_cases": len(cases),
            "agree": total["agree"], "disagree": total["disagree"], "deferred": total["deferred"],
            "scored": scored,
            "by_quadrant": {k: dict(v) for k, v in by_quadrant.items()},
            "by_provenance": {k: dict(v) for k, v in by_provenance.items()},
            "by_basis": {k: dict(v) for k, v in by_basis.items()},
            "calls": dict(calls),
            "qualifier": ADJUDICATOR_QUALIFIER}


def stub_baseline(cases: list | None = None) -> dict:
    """The always-available deterministic reference — score the StubAdjudicator. No model, dep-free."""
    return score_adjudications(cases if cases is not None else load_cases(), StubAdjudicator())


# --------------------------------------------------------------------------------------------------
def _selftest() -> int:
    """Offline, dep-free assertions over the committed oracle: the firewall rejects an oracle leak; the
    StubAdjudicator baseline reproduces EXACTLY the two-sided 33-right/33-wrong split (right on every
    correct-rejection + real-co-reference, wrong on every fragmentation-gap + over-merge-trap); the scoring
    shape carries the by-quadrant/provenance counts + the deferral channel + the qualifier; the LiveAdjudicator
    parse path fail-closes to a deferral; no banned word appears in the report."""
    cases = load_cases()
    assert len(cases) == 66, f"expected 66 scored cases, got {len(cases)}"

    # ── the firewall: a clean input passes; an oracle-leaked input (even renamed) is REJECTED ──
    clean = [adjudicator_input(c) for c in cases]
    assert all("oracle" not in x and "correct_adjudication" not in x for x in clean), \
        "the adjudicator input must never carry the oracle block nor a truth field"
    assert_no_oracle_leak(clean)
    leaked = [dict(x, oracle=c["oracle"]) for x, c in zip(clean, cases)]
    try:
        assert_no_oracle_leak(leaked)
        raise AssertionError("the firewall must REJECT an oracle leak")
    except AssertionError as e:
        assert "firewall" in str(e), e
    surrogate = [dict(x, correct_adjudication=c["oracle"]["correct_adjudication"]) for x, c in zip(clean, cases)]
    try:
        assert_no_oracle_leak(surrogate)
        raise AssertionError("the firewall must REJECT a renamed truth surrogate")
    except AssertionError as e:
        assert "firewall" in str(e), e

    # ── the StubAdjudicator (echo spine_verdict) reproduces the TWO-SIDED 33/33 baseline EXACTLY ──
    rep = stub_baseline(cases)
    assert rep["agree"] == 33 and rep["disagree"] == 33 and rep["deferred"] == 0, \
        f"the spine baseline must be two-sided 33 right / 33 wrong / 0 deferred: {rep}"
    bq = rep["by_quadrant"]
    assert bq["correct-rejection"] == {"agree": 30, "disagree": 0, "deferred": 0, "n": 30}, bq
    assert bq["real-co-reference"] == {"agree": 3, "disagree": 0, "deferred": 0, "n": 3}, bq
    assert bq["over-merge-trap"] == {"agree": 0, "disagree": 3, "deferred": 0, "n": 3}, bq
    assert bq["fragmentation-gap"] == {"agree": 0, "disagree": 30, "deferred": 0, "n": 30}, bq
    # the spine is RIGHT exactly where its action matches truth, WRONG on the two ambiguous quadrants — the
    # agent's reason to exist is recovering the 30 fragmentation-gaps + 3 over-merge-traps.
    bp = rep["by_provenance"]
    assert sum(v["n"] for v in bp.values()) == 66 and set(bp) == {
        "substrate-anchored-slice", "substrate-sanctions-slice", "synthetic-oracle"}, bp
    assert rep["qualifier"] == ADJUDICATOR_QUALIFIER

    # ── the LiveAdjudicator parse path: a valid call scores; junk fail-closes to a deferral ──
    class _FakeModel:
        def __init__(self, payload):
            self.payload = payload

        def __call__(self, messages):
            return self.payload

    valid = score_adjudications(cases, LiveAdjudicator(_FakeModel('{"call": "uphold_merge", "rationale": "same"}')))
    assert valid["calls"].get("uphold_merge") == 66 and valid["deferred"] == 0, valid["calls"]
    # an all-uphold agent agrees exactly on the 33 uphold_merge-oracle cases — a real measured count
    assert valid["agree"] == 33 and valid["disagree"] == 33, valid
    junk = score_adjudications(cases, LiveAdjudicator(_FakeModel("not json at all")))
    assert junk["deferred"] == 66 and junk["scored"] == 0, \
        f"junk model output must fail-closed to deferrals (counted, never scored): {junk}"

    # ── the honesty governor: no rate/score/multiplier wording anywhere in the report ──
    blob = json.dumps(rep).lower()
    for banned in ("catch-rate", "catch rate", "precision", "lift"):
        assert banned not in blob, f"banned wording in the report: {banned!r}"

    print(  # noqa: T201
        f"merge_adjudicator --selftest: PASS — {rep['n_cases']} scored cases; the oracle firewall rejects a "
        f"leak (incl. a renamed surrogate); the StubAdjudicator spine baseline is TWO-SIDED "
        f"{rep['agree']} right / {rep['disagree']} wrong / {rep['deferred']} deferred "
        f"(wrong on all {bq['fragmentation-gap']['disagree']} fragmentation-gap + {bq['over-merge-trap']['disagree']} "
        f"over-merge-trap — the agent's reason to exist); the live parse path fail-closes to a deferral. "
        f"[{ADJUDICATOR_QUALIFIER}]")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="The merge adjudicator (companion-only, Phase 83).")
    ap.add_argument("--selftest", action="store_true", help="offline dep-free assertions (firewall + baseline), exit")
    ap.add_argument("--report", action="store_true", help="print the StubAdjudicator baseline report as JSON")
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
