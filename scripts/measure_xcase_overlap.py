#!/usr/bin/env python3
"""Phase 75 T1 — the measure-first gate: cross-case strong-identifier overlap in a substrate v0.5 emission.

The persistent entity spine's MEMORY lever (Phase 74) accumulates priors when the SAME entity surfaces
across DIFFERENT cases. Substrate's `resolution_edges` are WITHIN-bundle; the cross-CASE signal the spine
needs is the same normalized STRONG identifier (email/phone) appearing on parties in 2+ DISTINCT customer
cases. This measurement SIZES that — it records a count; it never asserts the count is nonzero (the
news-fixture-disjoint failure mode, Phase 42, is a real outcome the demo must report honestly, not paper
over). Any cross-case link it finds is a REAL substrate-generated coincidence, never a fabricated one
(the Phase-73 de-concentrate-synthetic-identities honesty rule).

COMPANION-ONLY / authoring-time, like curate_workbench_cases.py — build.py NEVER imports this. Deterministic,
stdlib-only, no model. A case = a customer (group emitted bundles by case_id, the curate merge rule).

Usage:
  python3 scripts/measure_xcase_overlap.py --evidence-dir <dir>   # scan a substrate emit (the v0.5 bundles)
  python3 scripts/measure_xcase_overlap.py --selftest             # deterministic fixtures (no emit needed)
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from collections import defaultdict


def _strong_idents(party: dict) -> set:
    """The (kind, normalized) STRONG identifiers a party presents — the spine's strong-merge key shape."""
    out = set()
    for i in (party.get("identifiers") or []):
        if i.get("strength") != "strong":
            continue
        kind = (i.get("kind") or "").strip().lower()
        norm = (i.get("normalized") or i.get("value") or "").strip().lower()
        if kind and norm:
            out.add((kind, norm))
    return out


def scan_bundles(bundles: list) -> dict:
    """Group v0.5 bundles by case_id (a case = a customer) and measure TWO distinct cross-case signals:

      (1) entity_ref RE-SURFACING — the same party_id appearing in 2+ DISTINCT cases. This is REAL
          co-reference: substrate's DECLARED identity (entity_ref == party_id) is its own ground-truth
          identity, so the same entity_ref across cases is the same entity. THE honest memory-lever signal.

      (2) shared STRONG identifier across cases — a normalized email/phone on parties in 2+ cases. In
          substrate this is NOT a same-entity signal: gen/identity.py plants a deliberate coincidental-
          collision noise floor (email~6%/phone~4%) PLUS controller-cluster SHARES_EMAIL edges between
          DISTINCT beneficial owners. So a shared strong identifier is a SHARES_* network edge / collision
          between DISTINCT entities. We split it into corroboration (same entity_ref) vs the OVER-MERGE
          TRAP (distinct entity_refs) — the spine must NOT strong-merge the latter (the exact over-merge
          error substrate's noise floor exists to expose).

    Returns a report dict; always records counts, even all-zero (the Phase-42 disjoint outcome is honest)."""
    ident_cases = defaultdict(set)          # (kind, normalized) -> {case_id, ...}
    ident_xrefs = defaultdict(set)          # (kind, normalized) -> {entity_ref, ...}
    xref_cases = defaultdict(set)           # entity_ref -> {case_id, ...}
    cases = set()
    parties_with_strong = 0
    for b in bundles:
        cid = b.get("case_id")
        if not cid:
            continue
        cases.add(cid)
        for p in (b.get("parties") or []) + (b.get("related_parties") or []):
            xref = p.get("entity_ref") or p.get("party_id")
            if xref:
                xref_cases[xref].add(cid)
            ids = _strong_idents(p)
            if ids:
                parties_with_strong += 1
            for key in ids:
                ident_cases[key].add(cid)
                if xref:
                    ident_xrefs[key].add(xref)

    # (1) real co-reference: same entity_ref across 2+ cases
    xref_reappear = {x: sorted(c) for x, c in xref_cases.items() if len(c) >= 2}

    # (2) shared strong identifier across 2+ cases, split by whether it spans distinct entity_refs
    xcase = {k: sorted(v) for k, v in ident_cases.items() if len(v) >= 2}
    overmerge = {k for k in xcase if len(ident_xrefs.get(k, set())) >= 2}   # distinct entity_refs -> would falsely merge
    corroborate = set(xcase) - overmerge                                   # same entity_ref -> legit corroboration
    by_kind = defaultdict(int)
    for (kind, _norm) in xcase:
        by_kind[kind] += 1
    examples = sorted(
        ({"kind": k, "normalized": n, "cases": cids, "distinct_entity_refs": len(ident_xrefs.get((k, n), set())),
          "over_merge_trap": (k, n) in overmerge}
         for (k, n), cids in xcase.items()),
        key=lambda e: (-len(e["cases"]), e["kind"], e["normalized"]),
    )[:10]
    return {
        "n_cases": len(cases),
        # (1) THE honest memory-lever signal: real co-reference
        "n_entity_refs_reappearing_xcase": len(xref_reappear),
        "xref_reappear_examples": sorted(
            ({"entity_ref": x, "n_cases": len(c), "cases": c} for x, c in xref_reappear.items()),
            key=lambda e: (-e["n_cases"], e["entity_ref"]))[:10],
        # (2) the shared-identifier signal, with the over-merge trap quantified
        "n_parties_with_strong_id": parties_with_strong,
        "n_distinct_strong_ids": len(ident_cases),
        "n_xcase_strong_ids": len(xcase),
        "n_xcase_strong_ids_over_merge_trap": len(overmerge),    # span DISTINCT entity_refs — spine must NOT merge
        "n_xcase_strong_ids_corroboration": len(corroborate),    # same entity_ref — legit corroboration
        "xcase_by_kind": dict(by_kind),
        "xcase_examples": examples,
        "qualifier": ("synthetic substrate population; consistency-not-correctness; a case = a customer "
                      "(curate merge). entity_ref==party_id is substrate's declared identity (ground-truth "
                      "co-reference). A shared strong identifier is a SHARES_* edge / coincidental collision "
                      "between DISTINCT entities (gen/identity.py noise floor + controller clusters), NOT a "
                      "same-entity merge key."),
    }


def scan_evidence_dir(evidence_dir: str) -> dict:
    bundles = []
    for f in sorted(glob.glob(os.path.join(evidence_dir, "**", "*.json"), recursive=True)):
        try:
            bundles.append(json.load(open(f)))
        except (json.JSONDecodeError, OSError):
            continue
    report = scan_bundles(bundles)
    report["evidence_dir"] = evidence_dir
    report["n_bundles_scanned"] = len(bundles)
    return report


def _selftest() -> int:
    weak = {"kind": "address", "value": "1 Main St", "normalized": "1 main st", "strength": "weak"}

    # (1) REAL co-reference: the SAME entity_ref (P-OWNER) re-surfaces as a related party across 2 cases.
    same_ent = {"kind": "email", "value": "Owner@Corp.test", "normalized": "owner@corp.test", "strength": "strong"}
    reappear = [
        {"case_id": "C-A", "parties": [{"party_id": "P-A", "entity_ref": "P-A"}],
         "related_parties": [{"party_id": "P-OWNER", "entity_ref": "P-OWNER", "identifiers": [same_ent]}]},
        {"case_id": "C-B", "parties": [{"party_id": "P-OWNER", "entity_ref": "P-OWNER", "identifiers": [same_ent]}]},
    ]
    r = scan_bundles(reappear)
    assert r["n_entity_refs_reappearing_xcase"] == 1, r        # P-OWNER spans C-A + C-B (real co-reference)
    assert r["xref_reappear_examples"][0]["entity_ref"] == "P-OWNER", r
    # the same entity_ref's shared identifier is CORROBORATION, never the over-merge trap
    assert r["n_xcase_strong_ids"] == 1 and r["n_xcase_strong_ids_over_merge_trap"] == 0, r
    assert r["n_xcase_strong_ids_corroboration"] == 1, r

    # (2) the OVER-MERGE TRAP: one strong email shared by DISTINCT entity_refs across cases (the substrate
    # noise-floor / controller-cluster pattern). It is NOT co-reference; the spine must not strong-merge it.
    trap = [
        {"case_id": "C-1", "parties": [{"party_id": "P-1", "entity_ref": "P-1", "identifiers": [same_ent]}]},
        {"case_id": "C-2", "parties": [{"party_id": "P-2", "entity_ref": "P-2", "identifiers": [same_ent]}]},
        {"case_id": "C-3", "parties": [{"party_id": "P-3", "entity_ref": "P-3", "identifiers": [same_ent]}]},
    ]
    rt = scan_bundles(trap)
    assert rt["n_entity_refs_reappearing_xcase"] == 0, rt      # 3 DISTINCT entity_refs, none re-surfaces
    assert rt["n_xcase_strong_ids"] == 1 and rt["n_xcase_strong_ids_over_merge_trap"] == 1, rt
    assert rt["xcase_examples"][0]["over_merge_trap"] is True and rt["xcase_examples"][0]["distinct_entity_refs"] == 3, rt

    # the WEAK shared identifier never counts (grade gate)
    weak_shared = [
        {"case_id": "C-X", "parties": [{"party_id": "P", "entity_ref": "P", "identifiers": [weak]}]},
        {"case_id": "C-Y", "parties": [{"party_id": "Q", "entity_ref": "Q", "identifiers": [weak]}]},
    ]
    assert scan_bundles(weak_shared)["n_xcase_strong_ids"] == 0, "weak identifiers must not produce cross-case overlap"

    # the DISJOINT case (the Phase-42 failure mode): a count of 0 is RECORDED, not an error.
    disjoint = [
        {"case_id": "C-1", "parties": [{"party_id": "A", "entity_ref": "A", "identifiers": [
            {"kind": "email", "value": "a@x.test", "normalized": "a@x.test", "strength": "strong"}]}]},
        {"case_id": "C-2", "parties": [{"party_id": "B", "entity_ref": "B", "identifiers": [
            {"kind": "email", "value": "b@x.test", "normalized": "b@x.test", "strength": "strong"}]}]},
    ]
    rd = scan_bundles(disjoint)
    assert rd["n_xcase_strong_ids"] == 0 and rd["n_entity_refs_reappearing_xcase"] == 0 and rd["n_cases"] == 2, rd
    assert "n_entity_refs_reappearing_xcase" in rd, "the measurement must RECORD a count even when zero"
    print("measure_xcase_overlap --selftest OK")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--evidence-dir", help="a substrate emit's evidence/ dir (recursively scanned for *.json)")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return _selftest()
    if not args.evidence_dir:
        ap.error("provide --evidence-dir or --selftest")
    print(json.dumps(scan_evidence_dir(args.evidence_dir), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
