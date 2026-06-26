#!/usr/bin/env python3
"""Resolution-correctness scorer (Phase 74 — companion-only).

Measures the deterministic resolver's clustering against SYNTHETIC ground-truth clusters (`true_entities`) —
the one place the program's "no ground truth" epistemology gets a clean validation (on synthetic data the
latent identity is known; on real data it is not). Contract: docs/true-entities-scorer-contract.md.

The RESOLVER-INPUT FIREWALL (enforced at the schema boundary, NOT by convention): the resolver sees ONLY
the observable attributes (name, kind, role, identifiers) — NEVER the ground-truth `cluster` id nor a
surrogate 1:1-correlated with it. The cluster id lives only in this scorer's evaluation-only channel.
A tampered input carrying any field outside the observable allow-list is REJECTED — renaming `cluster` to
a per-cluster `*_ref` does NOT pass.

Every reported number is qualified "measured on synthetic clusters; production has no ground truth". The
full scorer over aml-substrate's `true_entities.parquet` is the sibling's job (its `resolve/measure.py`
already implements B-cubed/pairwise) — this proves the contract runs HERE before handoff.

COMPANION-ONLY. build.py NEVER imports this. Degrades gracefully when duckdb is absent (the spine needs it).
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
TRUE_ENTITIES_JSON = ROOT / "data" / "entity-spine" / "true_entities.json"

from entity_spine import EntitySpine, _norm  # noqa: E402  (companion module; needs duckdb at runtime)

# The OBSERVABLE resolver-input surface — the schema-boundary firewall. Any key outside this set on a
# resolver input is a leak (the ground-truth cluster id or a surrogate), and the build fails.
ALLOWED_INPUT_KEYS = frozenset({"obs_id", "record_id", "name", "kind", "role", "identifiers"})

# The four merge-adjudication quadrants — the human gate exists to handle the two AMBIGUOUS ones (a
# basis-only rule disagrees with truth). Shared vocab with the merge console (Phase 76).
KLASS_REAL_CO_REFERENCE = "real-co-reference"   # same entity, resolver merged          (uphold-merge; resolver correct)
KLASS_OVER_MERGE_TRAP = "over-merge-trap"       # distinct entities, resolver merged     (reject-as-SHARES; resolver WRONG — a false merge)
KLASS_FRAGMENTATION_GAP = "fragmentation-gap"   # same entity, resolver did NOT merge    (uphold-merge; resolver WRONG — a missed merge)
KLASS_CORRECT_REJECTION = "correct-rejection"   # distinct entities, resolver not merged (reject-as-SHARES; resolver correct)
AMBIGUOUS_KLASSES = (KLASS_OVER_MERGE_TRAP, KLASS_FRAGMENTATION_GAP)

# The mandatory honesty qualifier on EVERY resolver-quality number (synthetic clusters; not production).
SYNTHETIC_QUALIFIER = "measured on synthetic clusters; production has no ground truth"


def load_true_entities(path: Path | None = None) -> dict:
    return json.loads((path or TRUE_ENTITIES_JSON).read_text(encoding="utf-8"))


def resolver_input(obs: dict) -> dict:
    """Strip an observation to the OBSERVABLE surface the resolver is allowed to see — physically removing
    the `cluster` ground-truth (and anything else not in the allow-list)."""
    return {k: v for k, v in obs.items() if k in ALLOWED_INPUT_KEYS}


def assert_no_cluster_leak(inputs) -> None:
    """The schema-boundary firewall: every resolver input carries ONLY allow-listed observable keys. A
    `cluster` id, a renamed surrogate (`cluster_ref`, `true_entity_id`, …), or ANY extra field RAISES —
    the test is the schema boundary, not the field name, so renaming the leak does not pass."""
    for x in inputs:
        extra = set(x) - ALLOWED_INPUT_KEYS
        if extra:
            raise AssertionError(
                f"resolver-input firewall: observation {x.get('obs_id')!r} carries non-observable field(s) "
                f"{sorted(extra)} — a cluster id or surrogate must NEVER reach the resolver")


def run_resolver(inputs) -> dict:
    """Run the deterministic resolver (the spine's strong-identifier linkage) over the observable inputs.
    Returns {obs_id -> resolver_entity_id}. The resolver never sees `cluster`."""
    spine = EntitySpine(":memory:")
    try:
        out = {}
        for x in inputs:
            party = {"entity_id": x["obs_id"], "display_name": x.get("name"), "kind": x.get("kind"),
                     "role": x.get("role"), "identifiers": x.get("identifiers") or []}
            res = spine.observe(x.get("record_id", ""), party)
            out[x["obs_id"]] = res["entity_id"]
        return out
    finally:
        spine.close()


def _pairs(label_map: dict) -> set:
    obs = sorted(label_map)
    same = set()
    for i in range(len(obs)):
        for j in range(i + 1, len(obs)):
            if label_map[obs[i]] == label_map[obs[j]]:
                same.add((obs[i], obs[j]))
    return same


def pairwise_metrics(pred: dict, true: dict) -> dict:
    """Pairwise precision/recall — over all observation pairs, did the resolver co-cluster same-entity pairs
    (recall) without co-clustering different-entity pairs (precision)? A false merge is far costlier than a
    miss here, so precision is the load-bearing number."""
    sp, st = _pairs(pred), _pairs(true)
    tp, fp, fn = len(sp & st), len(sp - st), len(st - sp)
    return {"precision": tp / (tp + fp) if (tp + fp) else 1.0,
            "recall": tp / (tp + fn) if (tp + fn) else 1.0,
            "tp": tp, "fp": fp, "fn": fn, "qualifier": SYNTHETIC_QUALIFIER}


def bcubed_metrics(pred: dict, true: dict) -> dict:
    """B-cubed precision/recall — per-observation cluster purity, robust to cluster-size skew."""
    obs = list(true)
    pg, tg = defaultdict(set), defaultdict(set)
    for o in obs:
        pg[pred[o]].add(o)
        tg[true[o]].add(o)
    psum = rsum = 0.0
    for o in obs:
        pc, tc = pg[pred[o]], tg[true[o]]
        inter = len(pc & tc)
        psum += inter / len(pc)
        rsum += inter / len(tc)
    n = len(obs) or 1
    return {"precision": psum / n, "recall": rsum / n, "qualifier": SYNTHETIC_QUALIFIER}


def candidate_pairs(observations, pred, true) -> list:
    """Enumerate the merge-adjudication CANDIDATE pairs — every pair of observations that share a BASIS (a
    strong identifier / a weak identifier / an exact name) and therefore land in the human merge gate's
    queue. Each candidate is classified against the latent truth (eval-only `cluster`) AND the deterministic
    resolver's action into the four quadrants (KLASS_*). The 'ambiguous' queue = over-merge-trap +
    fragmentation-gap — exactly the cases where a basis-only rule disagrees with truth, the human gate's
    reason to exist. Reuses the spine's `edge_grade` grammar (strong/weak/reject) so basis is shared
    vocabulary with the spine, never a re-implementation."""
    by_id = {o["obs_id"]: o for o in observations}
    ids = sorted(by_id)
    out = []
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            a, b = by_id[ids[i]], by_id[ids[j]]
            grade, shared = EntitySpine.edge_grade(a.get("identifiers"), b.get("identifiers"))
            if grade == "strong":
                basis = "strong"
            elif grade == "weak":
                basis = "weak"
            elif _norm(a.get("name")) and _norm(a.get("name")) == _norm(b.get("name")):
                basis = "name"
            else:
                continue                                  # nothing shared -> not a merge candidate
            same = true[a["obs_id"]] == true[b["obs_id"]]
            merged = pred[a["obs_id"]] == pred[b["obs_id"]]
            klass = (KLASS_REAL_CO_REFERENCE if (same and merged) else
                     KLASS_OVER_MERGE_TRAP if (not same and merged) else
                     KLASS_FRAGMENTATION_GAP if (same and not merged) else
                     KLASS_CORRECT_REJECTION)
            out.append({"a": a["obs_id"], "b": b["obs_id"], "basis": basis, "shared": shared,
                        "same_entity": same, "resolver_merged": merged, "klass": klass,
                        "qualifier": SYNTHETIC_QUALIFIER})
    return out


def score(path: Path | None = None) -> dict:
    """The full resolution-correctness report over the synthetic fixture. Every number carries the
    synthetic-only qualifier; the resolver-input firewall is enforced before scoring."""
    data = load_true_entities(path)
    observations = data.get("observations", [])
    inputs = [resolver_input(o) for o in observations]
    assert_no_cluster_leak(inputs)                       # the firewall, before any scoring
    pred = run_resolver(inputs)
    true = {o["obs_id"]: o["cluster"] for o in observations}   # the eval-only channel (resolver never saw it)
    n_pred_clusters = len(set(pred.values()))
    n_true_clusters = len(set(true.values()))
    cands = candidate_pairs(observations, pred, true)
    counts = defaultdict(int)
    for c in cands:
        counts[c["klass"]] += 1
    n_ambiguous = sum(counts[k] for k in AMBIGUOUS_KLASSES)
    return {"qualifier": SYNTHETIC_QUALIFIER,
            "n_observations": len(observations), "n_true_clusters": n_true_clusters,
            "n_resolver_clusters": n_pred_clusters,
            "pairwise": pairwise_metrics(pred, true), "bcubed": bcubed_metrics(pred, true),
            "candidates": cands, "candidate_counts": dict(counts), "n_candidates": len(cands),
            "n_ambiguous": n_ambiguous,
            "pred": pred, "true": true}


# --------------------------------------------------------------------------------------------------
def _selftest() -> int:
    """Offline assertions over the Phase-76 expanded ambiguity oracle: the resolver-input firewall rejects a
    cluster surrogate; the deterministic resolver behaves exactly as the grammar dictates on EACH ambiguity
    class (real co-references merge; single-shared-id OVER-MERGES distinct people; fragmented same-people are
    NOT auto-merged incl. the refuse path; weak-shared neighbours stay separate); the merge-candidate queue
    spans all four quadrants with a meaningful AMBIGUOUS count (the merge gate's reason to exist); every
    number carries the synthetic-only qualifier."""
    try:
        rep = score()
    except RuntimeError as e:   # duckdb absent (the spine needs it)
        print(f"resolution_scorer --selftest: SKIP ({e})")  # noqa: T201
        return 0

    # ── the resolver-input firewall: a 1:1 cluster surrogate (renamed) is REJECTED at the schema boundary ──
    data = load_true_entities()
    clean = [resolver_input(o) for o in data["observations"]]
    assert all("cluster" not in x and "note" not in x for x in clean), \
        "the resolver input must never carry the cluster id NOR the eval-only note"
    assert_no_cluster_leak(clean)                        # clean inputs pass
    leaked = [dict(x, cluster_ref=o["cluster"]) for x, o in zip(clean, data["observations"])]  # a per-cluster ref (1:1)
    try:
        assert_no_cluster_leak(leaked)
        raise AssertionError("the firewall must REJECT a cluster surrogate (renaming the field does not pass)")
    except AssertionError as e:
        assert "firewall" in str(e), e

    # ── the resolver behaved exactly as the grammar dictates on each ambiguity class ──
    pred = rep["pred"]
    for x, y in (("o1", "o2"), ("o5", "o6"), ("o19", "o20")):       # real co-references — shared strong id MERGES
        assert pred[x] == pred[y], f"real co-reference {x}/{y} (shared strong id) must MERGE"
    for x, y in (("o9", "o10"), ("o11", "o12"), ("o13", "o14")):    # OVER-MERGE traps — one shared id over-merges DISTINCT people
        assert pred[x] == pred[y], f"the deterministic resolver over-merges the shared-identifier trap {x}/{y}"
    for x, y in (("o7", "o8"), ("o15", "o16"), ("o17", "o18"),       # fragmentation gaps — same person, NOT auto-merged
                 ("o21", "o22"), ("o21", "o23"), ("o22", "o23")):    #   (incl. the 3-way REFUSE bridge: o23)
        assert pred[x] != pred[y], f"fragmented same-person {x}/{y} must NOT be auto-merged (the gate adjudicates)"
    assert pred["o24"] != pred["o25"], "distinct neighbours sharing only a WEAK address must NOT merge (correct rejection)"
    assert pred["o3"] != pred["o4"], "John Calderon != Jon A. Calderón (different emails — exact-on-identifier, never fuzzy-on-name)"

    # ── the pairwise metrics REFLECT the seeded ambiguity (the deterministic resolver necessarily errs) ──
    pw = rep["pairwise"]
    assert pw["tp"] == 3 and pw["fp"] == 3 and pw["fn"] == 6, \
        f"3 real co-references merge (tp); the 3 over-merge traps are false merges (fp); 6 fragmented pairs are missed (fn): {pw}"
    assert pw["precision"] == 0.5 and abs(pw["recall"] - 1 / 3) < 1e-9, \
        f"pairwise P=0.5 (half the merges are over-merges) / R=1/3 (two-thirds of true pairs missed): {pw}"
    bc = rep["bcubed"]
    assert bc["precision"] < 1.0 and bc["recall"] < 1.0, f"B-cubed must show both error directions on the ambiguity oracle: {bc}"

    # ── the merge-candidate queue spans all four quadrants with a meaningful AMBIGUOUS count ──
    cc = rep["candidate_counts"]
    assert cc[KLASS_REAL_CO_REFERENCE] == 3, cc
    assert cc[KLASS_OVER_MERGE_TRAP] == 3, cc
    assert cc[KLASS_FRAGMENTATION_GAP] == 6, cc
    assert cc[KLASS_CORRECT_REJECTION] == 1, cc
    assert rep["n_candidates"] == 13 and rep["n_ambiguous"] == 9, rep
    bases = {c["basis"] for c in rep["candidates"]}
    assert bases == {"strong", "weak", "name"}, f"all three candidate bases must be exercised: {bases}"
    # the LOAD-BEARING ambiguity proof: the SAME weak-address basis carries OPPOSITE truths (a basis-only rule cannot decide)
    weak = {(c["a"], c["b"]): c for c in rep["candidates"] if c["basis"] == "weak"}
    assert weak[("o17", "o18")]["same_entity"] and not weak[("o24", "o25")]["same_entity"], \
        "same weak-address basis, opposite truth (Rahman same / Reyes-Haddad distinct) — the merge gate's reason to exist"

    # ── every reported number carries the synthetic-only qualifier ──
    assert rep["qualifier"] == SYNTHETIC_QUALIFIER
    assert pw["qualifier"] == SYNTHETIC_QUALIFIER and bc["qualifier"] == SYNTHETIC_QUALIFIER
    assert all(c["qualifier"] == SYNTHETIC_QUALIFIER for c in rep["candidates"])

    print(  # noqa: T201
        f"resolution_scorer --selftest: PASS — expanded ambiguity oracle "
        f"({rep['n_observations']} obs / {rep['n_true_clusters']} latent clusters; {rep['n_candidates']} merge "
        f"candidates = {cc[KLASS_REAL_CO_REFERENCE]} real-co-reference / {cc[KLASS_OVER_MERGE_TRAP]} over-merge-trap "
        f"/ {cc[KLASS_FRAGMENTATION_GAP]} fragmentation-gap / {cc[KLASS_CORRECT_REJECTION]} correct-rejection; "
        f"{rep['n_ambiguous']} GENUINELY AMBIGUOUS). Deterministic resolver pairwise "
        f"P={pw['precision']:.2f}/R={pw['recall']:.2f} (fp={pw['fp']} false merges, fn={pw['fn']} missed merges) "
        f"— the human merge gate's reason to exist. [{SYNTHETIC_QUALIFIER}]")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Resolution-correctness scorer (companion-only, Phase 74).")
    ap.add_argument("--selftest", action="store_true", help="offline assertions (the firewall + the metrics), exit")
    ap.add_argument("--report", action="store_true", help="print the score report as JSON")
    args = ap.parse_args()
    if args.selftest:
        return _selftest()
    if args.report:
        print(json.dumps(score(), indent=2))  # noqa: T201
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
