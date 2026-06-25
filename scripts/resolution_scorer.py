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

from entity_spine import EntitySpine  # noqa: E402  (companion module; needs duckdb at runtime)

# The OBSERVABLE resolver-input surface — the schema-boundary firewall. Any key outside this set on a
# resolver input is a leak (the ground-truth cluster id or a surrogate), and the build fails.
ALLOWED_INPUT_KEYS = frozenset({"obs_id", "record_id", "name", "kind", "role", "identifiers"})

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
    return {"qualifier": SYNTHETIC_QUALIFIER,
            "n_observations": len(observations), "n_true_clusters": n_true_clusters,
            "n_resolver_clusters": n_pred_clusters,
            "pairwise": pairwise_metrics(pred, true), "bcubed": bcubed_metrics(pred, true),
            "pred": pred, "true": true}


# --------------------------------------------------------------------------------------------------
def _selftest() -> int:
    """Offline assertions: the resolver-input firewall rejects a cluster surrogate; the deterministic
    resolver recovers the identifier-shared clusters (Calder/Maric merge; Calderon != Calderón) and
    CONSERVATIVELY does NOT merge the name-only pair (precision intact, a recall miss — unknown over wrong);
    every number carries the synthetic-only qualifier."""
    try:
        rep = score()
    except RuntimeError as e:   # duckdb absent (the spine needs it)
        print(f"resolution_scorer --selftest: SKIP ({e})")  # noqa: T201
        return 0

    # ── the resolver-input firewall: a 1:1 cluster surrogate (renamed) is REJECTED at the schema boundary ──
    data = load_true_entities()
    clean = [resolver_input(o) for o in data["observations"]]
    assert all("cluster" not in x for x in clean), "the resolver input must never carry the cluster id"
    assert_no_cluster_leak(clean)                        # clean inputs pass
    leaked = [dict(x, cluster_ref=o["cluster"]) for x, o in zip(clean, data["observations"])]  # a per-cluster ref (1:1)
    try:
        assert_no_cluster_leak(leaked)
        raise AssertionError("the firewall must REJECT a cluster surrogate (renaming the field does not pass)")
    except AssertionError as e:
        assert "firewall" in str(e), e

    # ── the resolver recovered the right clustering ──
    pred = rep["pred"]
    assert pred["o1"] == pred["o2"], "James Calder (shared strong email) must MERGE"
    assert pred["o5"] == pred["o6"], "Vesna Maric (shared strong email) must MERGE"
    assert pred["o3"] != pred["o4"], "John Calderon != Jon A. Calderón (different emails — exact-on-identifier)"
    assert pred["o7"] != pred["o8"], "name-only Sam Okafor pair must NOT merge (conservative — unknown over wrong)"

    # ── the metrics: precision 1.0 (no wrong merge), recall < 1.0 (the conservative name-only miss) ──
    pw = rep["pairwise"]
    assert pw["precision"] == 1.0 and pw["fp"] == 0, f"a false merge is the costly error — precision must be 1.0: {pw}"
    assert abs(pw["recall"] - 2 / 3) < 1e-9 and pw["fn"] == 1, f"the name-only pair is the one missed pair: {pw}"
    bc = rep["bcubed"]
    assert bc["precision"] == 1.0 and abs(bc["recall"] - 0.875) < 1e-9, bc

    # ── every reported number carries the synthetic-only qualifier ──
    assert rep["qualifier"] == SYNTHETIC_QUALIFIER
    assert pw["qualifier"] == SYNTHETIC_QUALIFIER and bc["qualifier"] == SYNTHETIC_QUALIFIER

    print(f"resolution_scorer --selftest: PASS "  # noqa: T201
          f"(firewall rejects a cluster surrogate; deterministic resolver recovered "
          f"{rep['n_resolver_clusters']}/{rep['n_true_clusters']} clusters; "
          f"pairwise P={pw['precision']:.2f}/R={pw['recall']:.2f}, B-cubed P={bc['precision']:.2f}/R={bc['recall']:.3f} "
          f"[{SYNTHETIC_QUALIFIER}])")
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
