#!/usr/bin/env python3
"""Phase 51 T1 — deterministic cross-regulator co-occurrence (the §13 fm-1 redundancy UPPER BOUND).

NON-SHIP measurement (does NOT touch corpus.html / dist / any committed record — read-only). stdlib only.

WHAT IT MEASURES (honest, in-constraint): over the SAME labels the corpus uses — typology resolved
per-indicator-override-else-doc-inherit (data/indicator-typology-map.json over data/typology-map.json),
capability = the C-code on the derived record, regulator = the agency derived from the source — the
fraction of indicators that share a (typology, capability) CELL with an indicator from a DIFFERENT
regulator. This is honest UNION / CO-OCCURRENCE arithmetic over EXISTING committed labels (the class
CLAUDE.md's honesty constraints ALLOW). It is a candidate-redundancy CEILING / co-occurrence count —
NOT a de-duplication, NOT a similarity/overlap/lift judgment, NOT a claim that two flags say the same
thing (that is the sampled consensus-class refinement of T2, deliberately separate). The always-on
"Illustrative data & outputs" honesty posture governs every number here; each carries its definition.

Usage:
    python3 scripts/corpus_redundancy.py            # emit the real measurement over the committed corpus
    python3 scripts/corpus_redundancy.py --selftest # unit-test the co-occurrence logic on a fixture
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

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
    """Load every committed indicator with the corpus's own resolved labels.

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
                })
    return out, n_override, n_inherit, n_unmapped


def cross_regulator_cooccurrence(indicators: list[dict], regulator_key: str,
                                 cell_keys: tuple[str, ...] = ("typology", "capability")) -> dict:
    """Fraction of indicators whose (cell) is shared by >=2 distinct regulators.

    An indicator 'cross-regulator co-occurs' iff its cell contains an indicator from a different
    value of regulator_key. Returns the upper-bound fraction + the supporting counts + the cells.
    Pure: no I/O. This is the unit under test in --selftest.
    """
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


def measure() -> None:
    inds, n_over, n_inherit, n_unmapped = load_indicators()
    by_agency: dict[str, int] = defaultdict(int)
    for i in inds:
        by_agency[i["agency"]] += 1

    agency = cross_regulator_cooccurrence(inds, "agency")
    juris = cross_regulator_cooccurrence(inds, "jurisdiction")

    print("CORPUS REDUNDANCY — cross-regulator co-occurrence UPPER BOUND (Phase 51 T1)")
    print("  [NON-SHIP measurement · committed corpus read-only · candidate co-occurrence, NOT dedup]")
    print()
    print(f"  indicators: {len(inds)}  (typology: {n_over} per-indicator override + {n_inherit} "
          f"doc-level inherit + {n_unmapped} unmapped)")
    print(f"  by regulator (agency): " + " · ".join(f"{a} {n}" for a, n in sorted(by_agency.items())))
    print()
    print("  DEFINITION — an indicator 'cross-regulator co-occurs' iff another regulator has an")
    print("  indicator in the SAME (typology, capability) cell. The fraction is an UPPER BOUND on")
    print("  redundancy (shared label cell != same indicator); the T2 sampled consensus-class")
    print("  semantic-equivalence estimate refines what share is genuinely redundant.")
    print()
    print(f"  cross-AGENCY co-occurrence upper bound:      {agency['fraction']:.3f}  "
          f"({agency['n_cross']}/{agency['n_total']} indicators in {agency['n_cross_cells']}/"
          f"{agency['n_cells']} shared cells)")
    print(f"  cross-JURISDICTION (US vs Canada) up. bound: {juris['fraction']:.3f}  "
          f"({juris['n_cross']}/{juris['n_total']})")
    print()
    top = sorted(agency["cross_cells"].items(),
                 key=lambda kv: -len(agency["cell_inds"][kv[0]]))[:8]
    print("  top cross-agency cells by indicator count (typology / capability → regulators):")
    for (typ, cap), regs in top:
        print(f"    {len(agency['cell_inds'][(typ, cap)]):4d}  {typ} / {cap}  →  {', '.join(regs)}")


def selftest() -> int:
    # Synthetic fixture: 4 cross-regulator-co-occurring + 1 single-regulator → 0.8 upper bound.
    fixture = [
        {"typology": "structuring", "capability": "C4", "agency": "FinCEN"},
        {"typology": "structuring", "capability": "C4", "agency": "FINTRAC"},   # cell {FinCEN,FINTRAC}
        {"typology": "shell-companies", "capability": "C15", "agency": "FinCEN"},
        {"typology": "shell-companies", "capability": "C15", "agency": "OFAC"},  # cell {FinCEN,OFAC}
        {"typology": "terrorist-financing", "capability": "C8", "agency": "FinCEN"},  # cell {FinCEN} alone
    ]
    r = cross_regulator_cooccurrence(fixture, "agency")
    assert r["n_total"] == 5, r
    assert r["n_cross"] == 4, r["n_cross"]
    assert abs(r["fraction"] - 0.8) < 1e-9, r["fraction"]
    assert r["n_cross_cells"] == 2, r["n_cross_cells"]
    # a single-regulator corpus has zero cross-regulator co-occurrence by construction
    solo = [{"typology": "x", "capability": "C1", "agency": "FinCEN"} for _ in range(3)]
    assert cross_regulator_cooccurrence(solo, "agency")["fraction"] == 0.0
    # the real corpus loads, resolves a typology for (nearly) every indicator, and is reproducible
    inds, n_over, n_inherit, n_unmapped = load_indicators()
    assert len(inds) > 2000, len(inds)
    assert n_unmapped == 0, f"{n_unmapped} indicators have no typology (overlay coverage gap)"
    assert load_indicators()[0] == inds  # deterministic
    print(f"selftest OK — logic verified on the 5-indicator fixture (0.800); corpus loads "
          f"{len(inds)} indicators, 0 unmapped, deterministic.")
    return 0


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    measure()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
