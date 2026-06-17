#!/usr/bin/env python3
"""Phase 51 — corpus redundancy measurement (the §13 fm-1 frontier, measured honestly).

NON-SHIP measurement (does NOT touch corpus.html / dist / any committed corpus record — read-only).
stdlib only. The always-on "Illustrative data & outputs" honesty posture governs every number; each
carries its measurement definition. NO de-duplication, NO similarity/overlap/lift figure on any ship
artifact.

T1 — DETERMINISTIC co-occurrence UPPER BOUND (in-constraint). Over the SAME labels the corpus uses
(typology per-indicator-override-else-doc-inherit; capability = the C-code on the record; regulator =
the agency derived from the source), the fraction of indicators sharing a (typology, capability) CELL
with an indicator from a DIFFERENT regulator. Honest UNION / CO-OCCURRENCE arithmetic over EXISTING
committed labels — a candidate-redundancy CEILING, NOT a dedup and NOT a similarity judgment.

T2 — SAMPLED consensus-class semantic-equivalence REFINEMENT (measure-not-claim). A deterministic
sample of cross-regulator co-occurring pairs is judged for semantic equivalence by a blind rater; the
judgments are a COMMITTED fixture (judged once, replayed deterministically — the Phase-34 neural-
dimension pattern), LABELED single-rater illustrative, consensus (>=2 raters) deferred-with-owner. The
equivalence RATE refines the T1 ceiling into an honest ESTIMATE = upper_bound x equivalence_rate. The
rate is never a validated dedup or a ground-truth claim.

Usage:
    python3 scripts/corpus_redundancy.py                       # T1 measurement
    python3 scripts/corpus_redundancy.py --sample N [--seed S]  # dump a blind sample to judge (T2)
    python3 scripts/corpus_redundancy.py --equiv FIXTURE.json   # T2 rate + estimate from judgments
    python3 scripts/corpus_redundancy.py --report              # full text report (T1 + T2 if fixture present)
    python3 scripts/corpus_redundancy.py --selftest            # unit-test the logic on fixtures
"""
from __future__ import annotations

import json
import random
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EQUIV_FIXTURE = ROOT / "data" / "corpus-redundancy" / "equiv-sample.json"  # NON-corpus; build.py never reads it

# Mirror build.py CORPUS_SOURCES (id, derived dir, jurisdiction). Read-only.
SOURCES = [
    ("fincen-advisories", ROOT / "data" / "fincen" / "derived", "US"),
    ("fincen-alerts", ROOT / "data" / "fincen-alerts" / "derived", "US"),
    ("ofac-advisories", ROOT / "data" / "ofac" / "derived", "US"),
    ("fintrac-advisories", ROOT / "data" / "fintrac" / "derived", "Canada"),
    ("fintrac-guidance", ROOT / "data" / "fintrac-guidance" / "derived", "Canada"),
]


def agency_of(source_id: str) -> str:
    """The REGULATOR grain for 'cross-regulator': FinCEN advisories + alerts are one regulator."""
    if source_id.startswith("fincen"):
        return "FinCEN"
    if source_id.startswith("ofac"):
        return "OFAC"
    if source_id.startswith("fintrac"):
        return "FINTRAC"
    return "?"


def load_indicators() -> tuple[list[dict], int, int, int]:
    """Load every committed indicator with the corpus's own resolved labels (+ its red_flag/flag text).

    Returns (indicators, n_typology_override, n_typology_inherit, n_unmapped).
    """
    tmap = json.loads((ROOT / "data" / "typology-map.json").read_text(encoding="utf-8"))["map"]
    imap = json.loads((ROOT / "data" / "indicator-typology-map.json").read_text(encoding="utf-8"))["map"]
    out: list[dict] = []
    n_override = n_inherit = n_unmapped = 0
    for sid, ddir, juris in SOURCES:
        for f in sorted(ddir.glob("*.json")):
            rec = json.loads(f.read_text(encoding="utf-8"))
            doc_id = rec["id"]
            for ind in rec.get("indicators", []):
                gid = f"{doc_id}/{ind['id']}"
                if gid in imap:
                    typ = imap[gid]
                    n_override += 1
                elif doc_id in tmap:
                    typ = tmap[doc_id]
                    n_inherit += 1
                else:
                    typ = "(unmapped)"
                    n_unmapped += 1
                out.append({
                    "gid": gid, "typology": typ, "capability": ind.get("capability"),
                    "data_source": ind.get("data_source"), "source": sid,
                    "agency": agency_of(sid), "jurisdiction": juris,
                    "red_flag": ind.get("red_flag", ""), "flag": ind.get("flag", ""),
                })
    return out, n_override, n_inherit, n_unmapped


def cross_regulator_cooccurrence(indicators: list[dict], regulator_key: str,
                                 cell_keys: tuple[str, ...] = ("typology", "capability")) -> dict:
    """Fraction of indicators whose (cell) is shared by >=2 distinct regulators. Pure (the unit under test)."""
    cell_regs: dict[tuple, set] = defaultdict(set)
    cell_inds: dict[tuple, list] = defaultdict(list)
    for ind in indicators:
        cell = tuple(ind[k] for k in cell_keys)
        cell_regs[cell].add(ind[regulator_key])
        cell_inds[cell].append(ind)
    n_total = len(indicators)
    n_cross = sum(len(inds) for cell, inds in cell_inds.items() if len(cell_regs[cell]) >= 2)
    cross_cells = {cell: sorted(regs) for cell, regs in cell_regs.items() if len(regs) >= 2}
    return {
        "fraction": (n_cross / n_total) if n_total else 0.0,
        "n_cross": n_cross, "n_total": n_total,
        "n_cells": len(cell_inds), "n_cross_cells": len(cross_cells),
        "cross_cells": cross_cells, "cell_inds": cell_inds, "cell_regs": cell_regs,
    }


def cross_regulator_pairs(indicators: list[dict], regulator_key: str = "agency") -> list[dict]:
    """All cross-regulator pairs within a shared (typology, capability) cell, in a STABLE order.

    A pair = two indicators in the same cell from different regulators. Stable-sorted by (cell, gids)
    so a seeded sample is reproducible. Pure.
    """
    co = cross_regulator_cooccurrence(indicators, regulator_key)
    pairs: list[dict] = []
    for cell in sorted(co["cross_cells"]):
        inds = sorted(co["cell_inds"][cell], key=lambda i: i["gid"])
        for x in range(len(inds)):
            for y in range(x + 1, len(inds)):
                a, b = inds[x], inds[y]
                if a[regulator_key] != b[regulator_key]:
                    pairs.append({"cell": cell, "a": a, "b": b})
    return pairs


def sample_pairs(pairs: list[dict], n: int, seed: int) -> list[dict]:
    """Deterministic blind sample of n pairs. random.Random(seed) over the stable-ordered list."""
    rng = random.Random(seed)
    return rng.sample(pairs, min(n, len(pairs)))


def dump_sample(n: int, seed: int) -> None:
    inds = load_indicators()[0]
    pairs = cross_regulator_pairs(inds)
    sample = sample_pairs(pairs, n, seed)
    print(f"# blind equivalence sample — {len(sample)} cross-regulator pairs (seed={seed}, of {len(pairs)} total)")
    print("# judge each: equivalent | partial | distinct  (does the same underlying behavior get described?)")
    for i, p in enumerate(sample):
        typ, cap = p["cell"]
        print(f"\n[{i:02d}] cell: {typ} / {cap}")
        print(f"  A [{p['a']['agency']:7s}] {p['a']['gid']}: {p['a']['red_flag']!r}")
        print(f"  B [{p['b']['agency']:7s}] {p['b']['gid']}: {p['b']['red_flag']!r}")


def equivalence_rate(fixture: dict) -> dict:
    """Compute the single-rater equivalence rate + the redundancy estimate from a committed judgment fixture."""
    js = fixture["judgments"]
    n = len(js)
    n_eq = sum(1 for j in js if j["verdict"] == "equivalent")
    n_partial = sum(1 for j in js if j["verdict"] == "partial")
    n_distinct = sum(1 for j in js if j["verdict"] == "distinct")
    # strict equivalence rate; partials counted at half as a sensitivity band
    rate_strict = n_eq / n if n else 0.0
    rate_band = (n_eq + 0.5 * n_partial) / n if n else 0.0
    return {"n": n, "n_eq": n_eq, "n_partial": n_partial, "n_distinct": n_distinct,
            "rate_strict": rate_strict, "rate_band": rate_band, "rater": fixture.get("rater", "?"),
            "seed": fixture.get("seed"), "label": fixture.get("label", "")}


def measure(report: bool = False) -> None:
    inds, n_over, n_inherit, n_unmapped = load_indicators()
    by_agency: dict[str, int] = defaultdict(int)
    for i in inds:
        by_agency[i["agency"]] += 1
    agency = cross_regulator_cooccurrence(inds, "agency")
    juris = cross_regulator_cooccurrence(inds, "jurisdiction")

    print("CORPUS REDUNDANCY — cross-regulator co-occurrence (Phase 51; the §13 fm-1 frontier, measured)")
    print("  [NON-SHIP · committed corpus read-only · candidate co-occurrence, NOT dedup · illustrative]")
    print()
    print(f"  indicators: {len(inds)}  (typology: {n_over} per-indicator override + {n_inherit} "
          f"doc-level inherit + {n_unmapped} unmapped)")
    print(f"  by regulator (agency): " + " · ".join(f"{a} {n}" for a, n in sorted(by_agency.items())))
    print()
    print("  T1 — DETERMINISTIC UPPER BOUND. DEFINITION: an indicator 'cross-regulator co-occurs' iff")
    print("  another regulator has an indicator in the SAME (typology, capability) cell. This is a")
    print("  CEILING on redundancy (a shared label cell is not the same indicator).")
    print(f"    cross-AGENCY upper bound:      {agency['fraction']:.3f}  "
          f"({agency['n_cross']}/{agency['n_total']} in {agency['n_cross_cells']}/{agency['n_cells']} shared cells)")
    print(f"    cross-JURISDICTION up. bound:  {juris['fraction']:.3f}  ({juris['n_cross']}/{juris['n_total']})")

    if EQUIV_FIXTURE.exists():
        fx = json.loads(EQUIV_FIXTURE.read_text(encoding="utf-8"))
        eq = equivalence_rate(fx)
        # integrity: the committed judgments provably correspond to the deterministic seeded sample
        smp = sample_pairs(cross_regulator_pairs(inds), fx["n"], fx["seed"])
        smp_keys = sorted((p["a"]["gid"], p["b"]["gid"]) for p in smp)
        fx_keys = sorted((j["a"], j["b"]) for j in fx["judgments"])
        integrity = "VERIFIED (judgments match the seeded sample)" if smp_keys == fx_keys else "!! MISMATCH !!"
        est_strict = agency["fraction"] * eq["rate_strict"]
        est_band = agency["fraction"] * eq["rate_band"]
        print()
        print(f"  T2 — SAMPLED SEMANTIC-EQUIVALENCE REFINEMENT (single-rater, illustrative; consensus")
        print(f"  >=2 raters deferred-with-owner). rater={eq['rater']}, seed={eq['seed']}, n={eq['n']}; "
              f"sample integrity: {integrity}.")
        print(f"  DEFINITION: of the sampled cross-regulator co-occurring pairs, the share judged to")
        print(f"  describe the SAME underlying behavior (consensus-class, never ground truth).")
        print(f"    equivalence rate: {eq['rate_strict']:.3f} strict ({eq['n_eq']} eq / {eq['n_partial']} "
              f"partial / {eq['n_distinct']} distinct of {eq['n']})  |  {eq['rate_band']:.3f} partial-as-half band")
        print(f"    ESTIMATED real cross-agency redundancy = upper_bound x rate = {agency['fraction']:.3f} x "
              f"{eq['rate_strict']:.3f} = ~{est_strict:.3f}  (band ~{est_band:.3f})")
        print(f"    READ AS: candidate cross-regulator redundancy <= {agency['fraction']:.1%} (deterministic");
        print(f"    co-occurrence ceiling); a single-rater illustrative sample estimates ~{est_strict:.1%} of")
        print(f"    co-occurring pairs are genuinely equivalent. NOT a validated dedup; consensus deferred.")
    else:
        print()
        print("  T2 — no equivalence fixture yet (run --sample N then commit the judgments to")
        print(f"  {EQUIV_FIXTURE.relative_to(ROOT)}). The T1 ceiling stands alone until then.")

    if report:
        top = sorted(agency["cross_cells"].items(), key=lambda kv: -len(agency["cell_inds"][kv[0]]))[:12]
        print()
        print("  top cross-agency cells by indicator count (typology / capability → regulators):")
        for (typ, cap), regs in top:
            print(f"    {len(agency['cell_inds'][(typ, cap)]):4d}  {typ} / {cap}  →  {', '.join(regs)}")


def selftest() -> int:
    # T1: synthetic fixture — 4 cross-regulator-co-occurring + 1 single-regulator → 0.8 upper bound.
    fixture = [
        {"typology": "structuring", "capability": "C4", "agency": "FinCEN", "gid": "a"},
        {"typology": "structuring", "capability": "C4", "agency": "FINTRAC", "gid": "b"},
        {"typology": "shell-companies", "capability": "C15", "agency": "FinCEN", "gid": "c"},
        {"typology": "shell-companies", "capability": "C15", "agency": "OFAC", "gid": "d"},
        {"typology": "terrorist-financing", "capability": "C8", "agency": "FinCEN", "gid": "e"},
    ]
    r = cross_regulator_cooccurrence(fixture, "agency")
    assert r["n_total"] == 5 and r["n_cross"] == 4 and abs(r["fraction"] - 0.8) < 1e-9, r
    assert r["n_cross_cells"] == 2, r["n_cross_cells"]
    solo = [{"typology": "x", "capability": "C1", "agency": "FinCEN", "gid": str(i)} for i in range(3)]
    assert cross_regulator_cooccurrence(solo, "agency")["fraction"] == 0.0
    # T2: pairs + deterministic sampling on the fixture
    fp = [dict(d, red_flag="rf") for d in fixture]
    pairs = cross_regulator_pairs(fp)
    assert len(pairs) == 2, pairs  # (a,b) and (c,d); e is alone
    s1 = sample_pairs(pairs, 1, seed=0)
    assert sample_pairs(pairs, 1, seed=0) == s1, "sampling must be deterministic for a fixed seed"
    # T2: equivalence-rate math
    eq = equivalence_rate({"judgments": [{"verdict": "equivalent"}, {"verdict": "partial"},
                                         {"verdict": "distinct"}, {"verdict": "equivalent"}]})
    assert eq["rate_strict"] == 0.5 and eq["rate_band"] == 0.625, eq
    # real corpus: loads, every indicator resolves a typology, deterministic
    inds, _o, _i, n_unmapped = load_indicators()
    assert len(inds) > 2000 and n_unmapped == 0, (len(inds), n_unmapped)
    assert load_indicators()[0] == inds
    print(f"selftest OK — T1 logic (0.800 fixture), T2 sampler determinism + rate math (0.500/0.625), "
          f"corpus loads {len(inds)} indicators, 0 unmapped, deterministic.")
    return 0


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    if "--sample" in argv:
        i = argv.index("--sample")
        n = int(argv[i + 1])
        seed = int(argv[argv.index("--seed") + 1]) if "--seed" in argv else 0
        dump_sample(n, seed)
        return 0
    if "--equiv" in argv:
        fx = json.loads(Path(argv[argv.index("--equiv") + 1]).read_text(encoding="utf-8"))
        eq = equivalence_rate(fx)
        print(json.dumps(eq, indent=2))
        return 0
    measure(report="--report" in argv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
