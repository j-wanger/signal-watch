#!/usr/bin/env python3
"""Phase 52 — C/D-tag reliability measurement (the unguarded dimension, measured honestly).

NON-SHIP measurement (does NOT touch corpus.html / dist / any committed corpus record — read-only).
stdlib only. The always-on "Illustrative data & outputs" honesty posture governs every number; each
carries its measurement definition. The per-indicator C (capability) / D (data-source) tags are the
ONE corpus dimension the grounding gate NEVER checks ("a grounding gate != a completeness gate != a
correctness gate"); this measures their RELIABILITY honestly, as CONSENSUS / SELF-CONSISTENCY, never
validated correctness.

Two deterministic strata, one blind same-model rater (the Phase-51 T2 / Phase-34 pattern):

RANDOM stratum — a blind rater re-assigns one C + one D to a deterministic sample of the committed
corpus from the flag + red_flag + the closed C/D vocab, NEVER seeing the committed code. Agreement =
blind == committed, per axis. This is REPRODUCIBILITY / SELF-CONSISTENCY (a same-model class redoing
the original extraction task shares its systematic biases), NOT validated correctness — independence
(a different model family / human) + larger N deferred-with-owner.

DIVERGENCE stratum — over the 213 Phase-34 console divergence cases (rater-A pre-correction vs
rater-B post-correction C/D), a blind rater sees the two candidate codes presented NEUTRALLY (order
fixed by seed) and picks option-1 / option-2 / both-defensible / neither, NEVER told which is the
committed correction. Reported as uphold-correction / uphold-original / both / neither — the
closer-to-independent number (the 213 are a real two-pass disagreement; rater-B = the correction).

Usage:
    python3 scripts/cd_correctness.py                                   # measurement (both strata if fixtures present)
    python3 scripts/cd_correctness.py --sample-random N [--seed S]      # dump a blind random sample to judge
    python3 scripts/cd_correctness.py --sample-divergence N [--seed S]  # dump a blind divergence sample to judge
    python3 scripts/cd_correctness.py --verify-fixtures                 # integrity: judgments match the seeded samples
    python3 scripts/cd_correctness.py --report                          # full text report
    python3 scripts/cd_correctness.py --selftest                        # unit-test the logic on fixtures
"""
from __future__ import annotations

import hashlib
import json
import random
import sys
from pathlib import Path

# Reuse the EXACT committed-corpus reader the Phase-51 measurement uses (same dir on sys.path[0] when
# run directly) — one loader, so both measurements read the corpus identically. build.py imports neither.
from corpus_redundancy import load_indicators

ROOT = Path(__file__).resolve().parent.parent
RANDOM_FIXTURE = ROOT / "data" / "cd-correctness" / "random-sample.json"       # NON-corpus; build.py never reads it
DIVERGENCE_FIXTURE = ROOT / "data" / "cd-correctness" / "divergence-sample.json"  # NON-corpus; build.py never reads it
CASES = ROOT / "data" / "console" / "cases.json"          # read-only measurement input (the 213 Phase-34 divergences)
TAXONOMY = ROOT / "data" / "capability-taxonomy.json"     # read-only — the closed C1-C28 / D1-D20 vocab


def load_vocab() -> tuple[dict, dict]:
    """The closed C/D vocab (code -> name) the blind rater chooses from. Read-only."""
    t = json.loads(TAXONOMY.read_text(encoding="utf-8"))
    caps = {c["id"]: c["name"] for c in t["capabilities"]}
    dss = {d["id"]: d["name"] for d in t["data_sources"]}
    return caps, dss


def load_cases() -> list[dict]:
    """The 213 Phase-34 C/D-divergence cases (rater_a pre-correction vs rater_b post-correction)."""
    return json.loads(CASES.read_text(encoding="utf-8"))["cases"]


# ---------------------------------------------------------------------------
# RANDOM stratum — blind same-model re-rate of the committed corpus (self-consistency)
# ---------------------------------------------------------------------------

def sample_random(indicators: list[dict], n: int, seed: int) -> list[dict]:
    """Deterministic blind sample of n committed indicators. random.Random(seed) over a stable order."""
    pool = sorted(indicators, key=lambda i: i["gid"])
    return random.Random(seed).sample(pool, min(n, len(pool)))


def dump_random(n: int, seed: int) -> None:
    inds = load_indicators()[0]
    caps, dss = load_vocab()
    sample = sample_random(inds, n, seed)
    print(f"# BLIND C/D re-rate sample — {len(sample)} committed indicators (seed={seed}, of {len(inds)})")
    print("# For each item assign exactly ONE capability (C) and ONE data-source (D) from the vocab below,")
    print("# judging ONLY from the flag + red_flag. You are NOT shown the committed code — this is blind.")
    print("\n# CAPABILITIES (C):")
    for cid, name in sorted(caps.items(), key=lambda kv: int(kv[0][1:])):
        print(f"#   {cid}: {name}")
    print("\n# DATA SOURCES (D):")
    for did, name in sorted(dss.items(), key=lambda kv: int(kv[0][1:])):
        print(f"#   {did}: {name}")
    for i, ind in enumerate(sample):
        print(f"\n[{i:02d}] {ind['gid']}")
        print(f"  flag:     {ind['flag']!r}")
        print(f"  red_flag: {ind['red_flag']!r}")
        print(f"  -> assign C? D?")


# ---------------------------------------------------------------------------
# DIVERGENCE stratum — blind adjudication of the 213 Phase-34 corrections (closer-to-independent)
# ---------------------------------------------------------------------------

def divergence_options(case: dict, seed: int) -> tuple[dict, dict, dict]:
    """Neutral, seed-fixed presentation of the two candidate codes — blind to which is the correction.

    rater_b is the committed correction; rater_a the original. Returns (option_1, option_2, mapping)
    where mapping records which rater each option is ('a'/'b'). Order flipped per case by a stable
    sha256 of (seed, case-id) — deterministic + version-independent, so the dump and scoring agree.
    """
    a, b = case["rater_a"], case["rater_b"]
    h = int(hashlib.sha256(f"{seed}:{case['id']}".encode()).hexdigest(), 16)
    flip = bool(h & 1)
    o_a = {"capability": a["capability"], "capability_name": a["capability_name"],
           "data_source": a["data_source"], "data_source_name": a["data_source_name"]}
    o_b = {"capability": b["capability"], "capability_name": b["capability_name"],
           "data_source": b["data_source"], "data_source_name": b["data_source_name"]}
    if flip:
        return o_b, o_a, {"option_1": "b", "option_2": "a"}
    return o_a, o_b, {"option_1": "a", "option_2": "b"}


def sample_divergence(cases: list[dict], n: int, seed: int) -> list[dict]:
    """Deterministic blind sample of n divergence cases. random.Random(seed) over a stable order."""
    pool = sorted(cases, key=lambda c: c["id"])
    return random.Random(seed).sample(pool, min(n, len(pool)))


def dump_divergence(n: int, seed: int) -> None:
    cases = load_cases()
    sample = sample_divergence(cases, n, seed)
    print(f"# BLIND C/D adjudication sample — {len(sample)} divergence cases (seed={seed}, of {len(cases)})")
    print("# Two raters assigned different C/D codes to the same indicator. Judging ONLY from the flag +")
    print("# red_flag, pick the better assignment: 1 | 2 | both (both defensible) | neither (escalate).")
    print("# You are NOT told which option is which rater's — this is blind.")
    for i, case in enumerate(sample):
        o1, o2, _mp = divergence_options(case, seed)
        changed = {"C": "capability", "D": "data-source", "both": "capability + data-source"}[case["changed"]]
        print(f"\n[{i:02d}] {case['id']}  (differs on: {changed})")
        print(f"  flag:     {case['flag']!r}")
        print(f"  red_flag: {case['red_flag']!r}")
        print(f"  option 1: {o1['capability']} ({o1['capability_name']}) / {o1['data_source']} ({o1['data_source_name']})")
        print(f"  option 2: {o2['capability']} ({o2['capability_name']}) / {o2['data_source']} ({o2['data_source_name']})")
        print(f"  -> pick: 1 | 2 | both | neither")


# ---------------------------------------------------------------------------
# Agreement arithmetic (pure)
# ---------------------------------------------------------------------------

def random_agreement(fixture: dict) -> dict:
    """Blind-vs-committed agreement per axis. Self-consistency, NOT validated correctness."""
    js = fixture["judgments"]
    n = len(js)
    c = sum(1 for j in js if j["blind_capability"] == j["committed_capability"])
    d = sum(1 for j in js if j["blind_data_source"] == j["committed_data_source"])
    both = sum(1 for j in js if j["blind_capability"] == j["committed_capability"]
               and j["blind_data_source"] == j["committed_data_source"])
    return {"n": n, "c_agree": c, "d_agree": d, "both_agree": both,
            "c_rate": c / n if n else 0.0, "d_rate": d / n if n else 0.0,
            "both_rate": both / n if n else 0.0,
            "rater": fixture.get("rater", "?"), "seed": fixture.get("seed"), "label": fixture.get("label", "")}


def divergence_agreement(fixture: dict) -> dict:
    """Which pole a blind pick upholds. rater_b = the committed correction (uses each judgment's stored mapping)."""
    counts = {"uphold_correction": 0, "uphold_original": 0, "both_defensible": 0, "neither": 0}
    for j in fixture["judgments"]:
        pick = j["pick"]
        mp = {"option_1": j["option_1"], "option_2": j["option_2"]}
        if pick in ("both", "both_defensible"):
            counts["both_defensible"] += 1
        elif pick in ("neither", "escalate"):
            counts["neither"] += 1
        elif pick in ("1", "option_1"):
            counts["uphold_correction" if mp["option_1"] == "b" else "uphold_original"] += 1
        elif pick in ("2", "option_2"):
            counts["uphold_correction" if mp["option_2"] == "b" else "uphold_original"] += 1
        else:
            raise ValueError(f"unknown pick {pick!r} for {j.get('id')}")
    n = len(fixture["judgments"])
    return {"n": n, **counts,
            "uphold_correction_rate": counts["uphold_correction"] / n if n else 0.0,
            "rater": fixture.get("rater", "?"), "seed": fixture.get("seed"), "label": fixture.get("label", "")}


# ---------------------------------------------------------------------------
# Integrity (the Phase-51 sample-integrity pattern — committed judgments provably match the seeded sample)
# ---------------------------------------------------------------------------

def verify_random(fixture: dict) -> tuple[bool, str]:
    inds = load_indicators()[0]
    by_gid = {i["gid"]: i for i in inds}
    smp = sample_random(inds, fixture["n"], fixture["seed"])
    smp_gids = sorted(i["gid"] for i in smp)
    fx_gids = sorted(j["gid"] for j in fixture["judgments"])
    if smp_gids != fx_gids:
        return False, "gids do not match the seeded sample"
    for j in fixture["judgments"]:
        ind = by_gid[j["gid"]]
        if j["committed_capability"] != ind["capability"] or j["committed_data_source"] != ind["data_source"]:
            return False, f"committed C/D drift for {j['gid']}"
    return True, "judgments match the seeded sample + the current committed C/D"


def verify_divergence(fixture: dict) -> tuple[bool, str]:
    cases = load_cases()
    by_id = {c["id"]: c for c in cases}
    smp = sample_divergence(cases, fixture["n"], fixture["seed"])
    smp_ids = sorted(c["id"] for c in smp)
    fx_ids = sorted(j["id"] for j in fixture["judgments"])
    if smp_ids != fx_ids:
        return False, "ids do not match the seeded sample"
    for j in fixture["judgments"]:
        _o1, _o2, mp = divergence_options(by_id[j["id"]], fixture["seed"])
        if mp["option_1"] != j["option_1"] or mp["option_2"] != j["option_2"]:
            return False, f"option mapping drift for {j['id']}"
    return True, "judgments match the seeded sample + the seed-fixed option order"


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def measure(report: bool = False) -> None:
    inds = load_indicators()[0]
    cases = load_cases()
    print("C/D-TAG RELIABILITY — the unguarded dimension, measured (Phase 52)")
    print("  [NON-SHIP · committed corpus read-only · consensus / self-consistency, NOT validated correctness · illustrative]")
    print()
    print(f"  corpus: {len(inds)} committed indicators (each carries a C + D the grounding gate never checks)")
    print(f"  divergence material: {len(cases)} Phase-34 C/D-correction cases (rater-A vs rater-B)")

    if RANDOM_FIXTURE.exists():
        fx = json.loads(RANDOM_FIXTURE.read_text(encoding="utf-8"))
        r = random_agreement(fx)
        ok, msg = verify_random(fx)
        print()
        print("  RANDOM stratum — DEFINITION: a blind rater re-assigns C + D from the flag + red_flag + the")
        print("  closed vocab, never seeing the committed code; agreement = blind == committed, per axis.")
        print(f"  rater={r['rater']}, seed={r['seed']}, n={r['n']}; integrity: {'VERIFIED' if ok else '!! ' + msg + ' !!'}.")
        print(f"    C (capability) agreement: {r['c_rate']:.3f}  ({r['c_agree']}/{r['n']})")
        print(f"    D (data-source) agreement: {r['d_rate']:.3f}  ({r['d_agree']}/{r['n']})")
        print(f"    both axes agree:           {r['both_rate']:.3f}  ({r['both_agree']}/{r['n']})")
        print("    READ AS: REPRODUCIBILITY / self-consistency (a same-model re-rate shares the original")
        print("    extractor's biases) — necessary-not-sufficient for correctness; independence deferred.")
    else:
        print()
        print(f"  RANDOM stratum — no fixture yet (run --sample-random N, commit judgments to "
              f"{RANDOM_FIXTURE.relative_to(ROOT)}).")

    if DIVERGENCE_FIXTURE.exists():
        fx = json.loads(DIVERGENCE_FIXTURE.read_text(encoding="utf-8"))
        d = divergence_agreement(fx)
        ok, msg = verify_divergence(fx)
        print()
        print("  DIVERGENCE stratum — DEFINITION: over the Phase-34 corrections, a blind rater picks the")
        print("  better of two neutrally-presented codes (rater-B = the committed correction); reported as")
        print("  which pole the pick upholds. The 213 are a real two-pass disagreement (closer-to-independent).")
        print(f"  rater={d['rater']}, seed={d['seed']}, n={d['n']}; integrity: {'VERIFIED' if ok else '!! ' + msg + ' !!'}.")
        print(f"    uphold CORRECTION (rater-B): {d['uphold_correction']}/{d['n']}  ({d['uphold_correction_rate']:.3f})")
        print(f"    uphold ORIGINAL (rater-A):   {d['uphold_original']}/{d['n']}")
        print(f"    both defensible:             {d['both_defensible']}/{d['n']}")
        print(f"    neither / escalate:          {d['neither']}/{d['n']}")
    else:
        print()
        print(f"  DIVERGENCE stratum — no fixture yet (run --sample-divergence N, commit judgments to "
              f"{DIVERGENCE_FIXTURE.relative_to(ROOT)}).")

    if report:
        print()
        print("  HONESTY BOUNDARY:")
        print("    - Consensus / self-consistency, NEVER ground truth or validated correctness. The random")
        print("      number is a SAME-MODEL re-rate (shared biases) — independence (a different model family")
        print("      / human) + a larger sample are deferred-with-owner.")
        print("    - Sample size (n) + seed are CHOSEN, not derived; the deliverable is the reproducible")
        print("      machinery + an honest first instance, not a final number.")
        print("    - NON-SHIP: the ship corpus (corpus.html / dist/corpus / all derived / the overlays) is")
        print("      byte-frozen; build.py never reads data/cd-correctness/.")


# ---------------------------------------------------------------------------
# Selftest
# ---------------------------------------------------------------------------

def selftest() -> int:
    # Random-stratum agreement math on a hand fixture: 2/3 C, 3/3 D, 2/3 both.
    rf = {"judgments": [
        {"gid": "x/1", "blind_capability": "C4", "blind_data_source": "D1",
         "committed_capability": "C4", "committed_data_source": "D1"},   # both match
        {"gid": "x/2", "blind_capability": "C8", "blind_data_source": "D8",
         "committed_capability": "C8", "committed_data_source": "D8"},   # both match
        {"gid": "x/3", "blind_capability": "C9", "blind_data_source": "D2",
         "committed_capability": "C7", "committed_data_source": "D2"},   # C miss, D match
    ]}
    r = random_agreement(rf)
    assert r["c_agree"] == 2 and r["d_agree"] == 3 and r["both_agree"] == 2, r
    assert abs(r["c_rate"] - 2 / 3) < 1e-9 and r["d_rate"] == 1.0, r

    # divergence_options: deterministic + neutral; rater_b recoverable via the mapping.
    case = {"id": "doc/IND-1", "changed": "C", "flag": "f", "red_flag": "rf",
            "rater_a": {"capability": "C8", "capability_name": "a", "data_source": "D8", "data_source_name": "da"},
            "rater_b": {"capability": "C14", "capability_name": "b", "data_source": "D8", "data_source_name": "db"}}
    o1, o2, mp = divergence_options(case, seed=0)
    assert divergence_options(case, seed=0) == (o1, o2, mp), "option order must be deterministic"
    # the option flagged 'b' in the mapping must carry rater_b's capability
    optb = o1 if mp["option_1"] == "b" else o2
    assert optb["capability"] == "C14", (optb, mp)
    # flip actually varies across ids (neutrality): both orders appear over a spread of ids
    orders = {divergence_options({**case, "id": f"d/IND-{i}"}, 0)[2]["option_1"] for i in range(20)}
    assert orders == {"a", "b"}, orders

    # divergence agreement math on a hand fixture (mapping stored per judgment):
    df = {"judgments": [
        {"id": "d/1", "pick": "1", "option_1": "b", "option_2": "a"},   # picked b -> uphold correction
        {"id": "d/2", "pick": "2", "option_1": "b", "option_2": "a"},   # picked a -> uphold original
        {"id": "d/3", "pick": "both", "option_1": "a", "option_2": "b"},
        {"id": "d/4", "pick": "neither", "option_1": "a", "option_2": "b"},
    ]}
    d = divergence_agreement(df)
    assert d["uphold_correction"] == 1 and d["uphold_original"] == 1, d
    assert d["both_defensible"] == 1 and d["neither"] == 1, d

    # real inputs: corpus loads (>2000, each with C+D), cases == 213, both deterministic.
    inds = load_indicators()[0]
    assert len(inds) > 2000 and all(i["capability"] and i["data_source"] for i in inds), "every indicator needs C+D"
    cases = load_cases()
    assert len(cases) == 213, len(cases)
    assert {c["changed"] for c in cases} <= {"C", "D", "both"}, "unexpected changed axis"
    s1 = sample_random(inds, 24, 0)
    assert [i["gid"] for i in sample_random(inds, 24, 0)] == [i["gid"] for i in s1], "random sample must be deterministic"
    s2 = sample_divergence(cases, 24, 0)
    assert [c["id"] for c in sample_divergence(cases, 24, 0)] == [c["id"] for c in s2], "divergence sample must be deterministic"
    # vocab: closed 28 C + 20 D, and every committed code is in-vocab (the rater's choice space).
    caps, dss = load_vocab()
    assert len(caps) == 28 and len(dss) == 20, (len(caps), len(dss))
    assert all(i["capability"] in caps and i["data_source"] in dss for i in inds), "committed code out of vocab"

    print(f"selftest OK — random agreement math (2/3 C, 3/3 D), divergence options determinism + neutrality + "
          f"scoring, corpus loads {len(inds)} indicators (all C+D in a 28/20 vocab), {len(cases)} cases, "
          f"both samplers deterministic.")
    return 0


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    if "--sample-random" in argv:
        i = argv.index("--sample-random")
        seed = int(argv[argv.index("--seed") + 1]) if "--seed" in argv else 0
        dump_random(int(argv[i + 1]), seed)
        return 0
    if "--sample-divergence" in argv:
        i = argv.index("--sample-divergence")
        seed = int(argv[argv.index("--seed") + 1]) if "--seed" in argv else 0
        dump_divergence(int(argv[i + 1]), seed)
        return 0
    if "--verify-fixtures" in argv:
        rc = 0
        for label, path, verify in (("random", RANDOM_FIXTURE, verify_random),
                                    ("divergence", DIVERGENCE_FIXTURE, verify_divergence)):
            if not path.exists():
                print(f"  {label}: no fixture yet ({path.relative_to(ROOT)})")
                continue
            ok, msg = verify(json.loads(path.read_text(encoding="utf-8")))
            print(f"  {label}: {'VERIFIED' if ok else 'MISMATCH'} — {msg}")
            rc = rc or (0 if ok else 1)
        return rc
    measure(report="--report" in argv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
