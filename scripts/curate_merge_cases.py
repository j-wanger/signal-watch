#!/usr/bin/env python3
"""Curate the merge-adjudication console cases (Phase 76 — companion-only AUTHORING tool).

Emits the committed `data/merge/cases.json` that the `merge` ship target inlines into `dist/merge/`.
Two case populations, kept visibly separate (the consensus-vs-scored split — the load-bearing honesty seam):

  1. REAL candidate SHARES (consensus, NO oracle). The committed v0.5 substrate slice carries
     `resolution_edges` (status:"resolved") between DISTINCT `entity_ref`s — substrate's deliberate
     collision noise floor + controller-cluster SHARES (gen/identity.py). The entity spine keys identity on
     `entity_ref` and REFUSES those merges (Phase 75: 66 over-merge-refused). Each refused pair is an
     adjudication case. There is NO ground truth here — substrate emits no `true_entities` for the slice
     (the T5 sibling handoff) — so these are CONSENSUS-not-ground-truth, never scored.

  2. SYNTHETIC scored cases (the oracle). `data/entity-spine/true_entities.json` carries latent identity
     clusters (the eval-only channel behind the resolver-input firewall). For each merge candidate the
     scorer enumerates, the latent truth says whether the adjudication SHOULD uphold or reject — so the
     console's Reveal can SHOW, on synthetic data only, whether the call matched truth. Every scored number
     carries the synthetic-only qualifier.

DETERMINISTIC, regeneration-only. The spine's entity_ids are random per run, but only used to compare
ea != eb WITHIN one run; every emitted field is stable (entity_refs / obs_ids / names / identifiers), so two
runs are byte-identical. Reuses the entity_spine grade grammar + the resolution_scorer firewall — no new
resolution logic. COMPANION-ONLY: build.py NEVER imports this (build.py reads the committed JSON + validates
at the boundary with its own standalone validator). Needs duckdb (the spine) — run under the .venv.

Regenerate:  .venv/bin/python scripts/curate_merge_cases.py
Selftest:    .venv/bin/python scripts/curate_merge_cases.py --selftest
"""
from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
ROOT = _HERE.parent
WORKBENCH_DIR = ROOT / "data" / "workbench"
CASES_INDEX = WORKBENCH_DIR / "cases.json"
BUNDLES_DIR = WORKBENCH_DIR / "bundles"
TRUE_ENTITIES = ROOT / "data" / "entity-spine" / "true_entities.json"
OUT_PATH = ROOT / "data" / "merge" / "cases.json"

# the verified substrate HEAD the committed slice was curated from (Phase 75; mirrors curate_workbench_cases)
SUBSTRATE_HEAD = "fc98b09"

from entity_spine import EntitySpine                                   # noqa: E402  (companion; needs duckdb)
from resolution_scorer import (                                       # noqa: E402
    KLASS_OVER_MERGE_TRAP, KLASS_FRAGMENTATION_GAP, KLASS_REAL_CO_REFERENCE, KLASS_CORRECT_REJECTION,
    SYNTHETIC_QUALIFIER, candidate_pairs, resolver_input, run_resolver, load_true_entities,
)

BADGE = "Illustrative data & outputs"

# ── the closed adjudication vocabulary (the Class-J merge grades — written to cases.json, re-checked at the
#    build boundary). Non-binary, like the gate console: the grade carries the call, the rationale the audit. ──
ADJUDICATION_GRADES = [
    {"id": "uphold_merge", "label": "Uphold the merge",
     "desc": "These records are the SAME entity — confirm the merge the resolver proposed (or should have)."},
    {"id": "reject_as_shares", "label": "Reject — keep distinct (a SHARES edge)",
     "desc": "Distinct entities that merely share an identifier — keep them apart; record the link as a SHARES edge, not a merge."},
    {"id": "both_defensible", "label": "Both defensible",
     "desc": "The evidence genuinely underdetermines it — record the ambiguity instead of forcing same-or-distinct."},
    {"id": "escalate", "label": "Neither — escalate",
     "desc": "Insufficient to call either way — route to expert / await more identifiers."},
]
GRADE_IDS = frozenset(g["id"] for g in ADJUDICATION_GRADES)

# ── the queue grouping bases (the strongest shared SIGNAL between the two records) ──
BASES = [
    {"id": "strong", "label": "Strong shared identifier",
     "desc": "share an exact email / phone / account number — a strong-kind identifier"},
    {"id": "weak", "label": "Weak corroboration",
     "desc": "share only a weak identifier (an address) — corroborates, never resolves on its own"},
    {"id": "name", "label": "Name-only",
     "desc": "share only a name — no identifier at all"},
]
BASIS_IDS = frozenset(b["id"] for b in BASES)

SOURCE_CONSENSUS = "substrate-v0.5-slice"   # real candidate SHARES — no oracle
SOURCE_SCORED = "synthetic-oracle"          # synthetic — scored against true_entities

# the latent truth's correct adjudication, in the closed grade vocab
_CORRECT = {True: "uphold_merge", False: "reject_as_shares"}

# fields that would LEAK the latent truth into the pre-disposition evidence — forbidden on a/b (the firewall)
_TRUTH_LEAK_KEYS = ("cluster", "same_entity", "correct_adjudication", "klass", "note", "oracle")


def _safe_value(kind: str, value: str) -> str:
    """Render a substrate-generated identifier UNAMBIGUOUSLY synthetic in the SHIPPED artifact (the
    synthetic-by-construction discipline — Phase 73's .test/.example/555 rule). The substrate population is
    already synthetic, but its emails sit on real domains (outlook.com/…); a ship file must never READ as real
    data. We keep the local-part token (it proves the exact-match collision — both sides share it) and swap the
    domain to the reserved `example.test`. Deterministic; identical inputs → identical output, so a shared
    identifier stays shared."""
    v = str(value or "")
    if kind == "email" and "@" in v:
        return v.split("@", 1)[0] + "@example.test"
    return v


# --------------------------------------------------------------------------------------------------
def _observe_substrate_party(spine: "EntitySpine", case_id: str, party: dict):
    """Observe one substrate party into the spine keyed on `entity_ref` (the reliable declared identity =
    the STRONG merge key); email/phone are DEMOTED to `weak` candidate-SHARES (substrate's noise floor makes
    them non-discriminative). Mirrors serve_workbench._observe_substrate_party (Phase 75) — replicated here
    rather than importing the HTTP server, to keep this authoring tool decoupled from the live layer."""
    eref = party.get("entity_ref") or party.get("party_id")
    if not eref:
        return None
    idents = [{"kind": "entity_ref", "value": eref, "normalized": eref, "strength": "strong"}]
    for i in (party.get("identifiers") or []):
        if i.get("kind") in ("email", "phone") and i.get("normalized"):
            idents.append({"kind": i["kind"], "value": i.get("value"),
                           "normalized": i["normalized"], "strength": "weak"})
    res = spine.observe(case_id, {"entity_id": eref, "display_name": party.get("display_name"),
                                  "kind": "person" if party.get("is_person") else "org",
                                  "role": party.get("label") or party.get("role"), "identifiers": idents})
    return eref, res


def enumerate_real_shares() -> list:
    """The 66 REAL candidate SHARES the spine refused over the committed v0.5 slice — consensus cases, no
    oracle. Deterministic over the FIXED committed population (Phase-75 measured: 66)."""
    index = json.loads(CASES_INDEX.read_text(encoding="utf-8"))
    spine = EntitySpine(":memory:")
    eref2eid: dict = {}
    eref2party: dict = {}
    edges: list = []
    try:
        for c in index.get("cases", []):
            cid = c.get("case_id")
            try:
                b = json.loads((BUNDLES_DIR / f"{cid}.json").read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            for p in (b.get("parties") or []) + (b.get("related_parties") or []):
                r = _observe_substrate_party(spine, cid, p)
                if not r:
                    continue
                eref, res = r
                eref2eid[eref] = res["entity_id"]
                if eref not in eref2party:                 # first observation wins (deterministic given stable order)
                    eref2party[eref] = {"name": p.get("display_name"),
                                        "kind": "person" if p.get("is_person") else "org",
                                        "role": p.get("label") or p.get("role"),
                                        "risk": p.get("risk_rating"), "pep": p.get("pep_tier"),
                                        "sanctions": bool(p.get("sanctions_flag")),
                                        "adverse_media": bool(p.get("adverse_media_flag"))}
            for e in (b.get("resolution_edges") or []):
                btw = e.get("between") or []
                if isinstance(btw, list) and len(btw) == 2 and btw[0] != btw[1]:
                    edges.append((cid, btw[0], btw[1], e.get("shared") or [], bool(e.get("cross_institution"))))
        seen, cases = set(), []
        for cid, a, bb, shared, xinst in edges:
            ea, eb = eref2eid.get(a), eref2eid.get(bb)
            if not (ea and eb and ea != eb):               # both resolved + kept DISTINCT -> the spine refused
                continue
            pair = tuple(sorted((a, bb)))
            if pair in seen:
                continue
            seen.add(pair)
            pa, pb = eref2party.get(pair[0], {}), eref2party.get(pair[1], {})
            sh = shared[0] if shared else {}
            cases.append({
                "id": f"real-{pair[0]}-{pair[1]}",
                "source": SOURCE_CONSENSUS, "scored": False, "basis": "strong",
                "shared": {"kind": sh.get("kind"),
                           "value": _safe_value(sh.get("kind"), sh.get("value") or sh.get("normalized"))},
                "cross_institution": xinst,
                "spine_verdict": "kept_distinct", "substrate_claim": "resolved",
                "a": {"ref": pair[0], "name": pa.get("name"), "kind": pa.get("kind"), "role": pa.get("role"),
                      "attrs": {"risk": pa.get("risk"), "pep": pa.get("pep"),
                                "sanctions": pa.get("sanctions"), "adverse_media": pa.get("adverse_media")}},
                "b": {"ref": pair[1], "name": pb.get("name"), "kind": pb.get("kind"), "role": pb.get("role"),
                      "attrs": {"risk": pb.get("risk"), "pep": pb.get("pep"),
                                "sanctions": pb.get("sanctions"), "adverse_media": pb.get("adverse_media")}},
            })
    finally:
        spine.close()
    # deterministic order: by shared identifier, then the sorted entity_ref pair
    cases.sort(key=lambda c: (c["shared"].get("value") or "", c["a"]["ref"], c["b"]["ref"]))
    return cases


def _obs_side(obs: dict) -> dict:
    """A synthetic case side from a true_entities observation — only the OBSERVABLE surface (the firewall:
    `resolver_input` strips the latent `cluster` + the eval-only `note`). Identifiers shown as kind/value."""
    clean = resolver_input(obs)
    return {"ref": clean.get("obs_id"), "name": clean.get("name"), "kind": clean.get("kind"),
            "role": clean.get("role"),
            "identifiers": [{"kind": i.get("kind"), "value": i.get("value")}
                            for i in (clean.get("identifiers") or [])]}


def enumerate_synthetic_scored() -> list:
    """The synthetic SCORED cases: every merge candidate the scorer enumerates over `true_entities`, carrying
    the deterministic spine verdict AND the latent-truth oracle (synthetic-only, qualified). The evidence
    sides are firewall-stripped to the observable surface — the truth rides ONLY the separate `oracle` block,
    revealed post-disposition."""
    data = load_true_entities()
    observations = data.get("observations", [])
    by_id = {o["obs_id"]: o for o in observations}
    inputs = [resolver_input(o) for o in observations]
    pred = run_resolver(inputs)
    true = {o["obs_id"]: o["cluster"] for o in observations}
    cands = candidate_pairs(observations, pred, true)
    cases = []
    for c in cands:
        a, b = by_id[c["a"]], by_id[c["b"]]
        shared = c.get("shared") or []
        sh = shared[0] if shared else None
        cases.append({
            "id": f"syn-{c['a']}-{c['b']}",
            "source": SOURCE_SCORED, "scored": True, "basis": c["basis"],
            "shared": ({"kind": sh.get("kind"), "value": sh.get("normalized")} if sh else None),
            "spine_verdict": "merged" if c["resolver_merged"] else "kept_distinct",
            "a": _obs_side(a), "b": _obs_side(b),
            "oracle": {
                "same_entity": c["same_entity"],
                "klass": c["klass"],
                "correct_adjudication": _CORRECT[c["same_entity"]],
                "qualifier": SYNTHETIC_QUALIFIER,
            },
        })
    cases.sort(key=lambda c: (c["basis"], c["a"]["ref"], c["b"]["ref"]))
    return cases


def build() -> dict:
    real = enumerate_real_shares()
    syn = enumerate_synthetic_scored()
    return {
        "_note": ("FULLY curated merge-adjudication cases (Phase 76; regeneration-only — "
                  ".venv/bin/python scripts/curate_merge_cases.py). TWO populations kept visibly separate: "
                  f"(1) {len(real)} REAL candidate SHARES from the committed aml-substrate v0.5 slice "
                  f"(@{SUBSTRATE_HEAD}) — the spine refused these over-merges (substrate's collision noise "
                  "floor / controller clusters); CONSENSUS-not-ground-truth, NO oracle (substrate emits no "
                  "true_entities for the slice — the T5 sibling handoff). (2) the SYNTHETIC scored cases from "
                  "data/entity-spine/true_entities.json — latent identity clusters behind the resolver-input "
                  "firewall let the Reveal SHOW, ON SYNTHETIC DATA ONLY, whether the call matched truth. The "
                  "latent truth rides ONLY each scored case's `oracle` block (revealed post-disposition); the "
                  "pre-disposition evidence (a/b) carries no truth field. The real population is synthetic "
                  "(substrate-generated); its shared email identifiers are domain-masked to example.test in this "
                  "ship artifact so nothing reads as real data (the local-part token, kept, proves the exact "
                  "collision). Illustrative; no catch-rate/lift is claimed; every scored number is qualified "
                  "synthetic-only."),
        "badge": BADGE,
        "brand": {"title": "Signal Watch", "subtitle": "Merge Console · Vision Prototype"},
        "adjudication_grades": ADJUDICATION_GRADES,
        "bases": BASES,
        "provenance": {
            "substrate_head": SUBSTRATE_HEAD,
            "slice_cases": len(json.loads(CASES_INDEX.read_text(encoding="utf-8")).get("cases", [])),
            "n_real_consensus": len(real),
            "n_synthetic_scored": len(syn),
            "synthetic_qualifier": SYNTHETIC_QUALIFIER,
        },
        "cases": real + syn,
    }


# --------------------------------------------------------------------------------------------------
def validate(data: dict) -> list:
    """Validate the committed cases.json shape (closed vocab + referential integrity + the resolver-input
    firewall translated to the ship artifact + the consensus/scored honesty split). Returns error strings;
    NEVER raises. This backs the curate --selftest; build.py carries an INDEPENDENT standalone copy at the
    build boundary (it must not import this companion)."""
    errs = []
    if data.get("badge") != BADGE:
        errs.append(f"badge must be {BADGE!r}")
    grade_ids = {g.get("id") for g in data.get("adjudication_grades") or []}
    if grade_ids != GRADE_IDS:
        errs.append(f"adjudication_grades must be exactly {sorted(GRADE_IDS)}; got {sorted(grade_ids)}")
    basis_ids = {b.get("id") for b in data.get("bases") or []}
    if basis_ids != BASIS_IDS:
        errs.append(f"bases must be exactly {sorted(BASIS_IDS)}; got {sorted(basis_ids)}")
    cases = data.get("cases") or []
    if not cases:
        errs.append("no cases")
    seen, n_real, n_syn = set(), 0, 0
    for c in cases:
        cid = c.get("id")
        if not cid:
            errs.append("a case is missing an id")
            continue
        if cid in seen:
            errs.append(f"duplicate case id {cid!r}")
        seen.add(cid)
        if c.get("basis") not in BASIS_IDS:
            errs.append(f"{cid}: basis {c.get('basis')!r} not in {sorted(BASIS_IDS)}")
        if c.get("spine_verdict") not in ("merged", "kept_distinct"):
            errs.append(f"{cid}: spine_verdict {c.get('spine_verdict')!r} invalid")
        for side in ("a", "b"):
            s = c.get(side)
            if not isinstance(s, dict) or not s.get("ref") or not s.get("name"):
                errs.append(f"{cid}.{side}: needs at least ref + name")
                continue
            # THE FIREWALL: the pre-disposition evidence must carry NO latent-truth field
            leak = [k for k in _TRUTH_LEAK_KEYS if k in s]
            if leak:
                errs.append(f"{cid}.{side}: resolver-input firewall — evidence carries truth field(s) {leak}")
        src, scored, oracle = c.get("source"), c.get("scored"), c.get("oracle")
        if src == SOURCE_CONSENSUS:
            n_real += 1
            if scored is not False:
                errs.append(f"{cid}: real consensus case must have scored=false")
            if oracle is not None:
                errs.append(f"{cid}: a REAL case must carry NO oracle (no fabricated ground truth on real data)")
            if c.get("basis") != "strong":
                errs.append(f"{cid}: real candidate SHARES are strong-shared-id (basis=strong)")
            if c.get("spine_verdict") != "kept_distinct":
                errs.append(f"{cid}: real candidate SHARES are over-merge-REFUSED (spine_verdict=kept_distinct)")
        elif src == SOURCE_SCORED:
            n_syn += 1
            if scored is not True:
                errs.append(f"{cid}: synthetic scored case must have scored=true")
            if not isinstance(oracle, dict):
                errs.append(f"{cid}: synthetic case must carry an oracle block")
            else:
                if not isinstance(oracle.get("same_entity"), bool):
                    errs.append(f"{cid}: oracle.same_entity must be a bool")
                if oracle.get("correct_adjudication") not in GRADE_IDS:
                    errs.append(f"{cid}: oracle.correct_adjudication not in the grade vocab")
                if oracle.get("correct_adjudication") != _CORRECT.get(oracle.get("same_entity")):
                    errs.append(f"{cid}: oracle.correct_adjudication must follow same_entity")
                if oracle.get("qualifier") != SYNTHETIC_QUALIFIER:
                    errs.append(f"{cid}: every scored case must carry the synthetic-only qualifier")
        else:
            errs.append(f"{cid}: source {src!r} not in {{{SOURCE_CONSENSUS}, {SOURCE_SCORED}}}")
        if c.get("basis") in ("strong", "weak") and not (c.get("shared") and c["shared"].get("kind")):
            errs.append(f"{cid}: a {c.get('basis')} basis needs a shared identifier")
        if c.get("basis") == "name" and c.get("shared"):
            errs.append(f"{cid}: a name-only basis must have no shared identifier")
    if n_real == 0:
        errs.append("no real consensus candidate SHARES (expected the v0.5 over-merge-refused residual)")
    if n_syn == 0:
        errs.append("no synthetic scored cases (the scored differentiator is missing)")
    prov = data.get("provenance") or {}
    if prov.get("n_real_consensus") != n_real or prov.get("n_synthetic_scored") != n_syn:
        errs.append("provenance counts disagree with the actual case populations")
    return errs


# --------------------------------------------------------------------------------------------------
def _selftest() -> int:
    try:
        data = build()
    except RuntimeError as e:                 # duckdb absent (the spine needs it)
        print(f"curate_merge_cases --selftest: SKIP ({e})")  # noqa: T201
        return 0

    errs = validate(data)
    assert not errs, f"the freshly built dataset must validate clean: {errs}"

    cases = data["cases"]
    real = [c for c in cases if c["source"] == SOURCE_CONSENSUS]
    syn = [c for c in cases if c["source"] == SOURCE_SCORED]
    assert real and syn, "both populations must be present"
    # the REAL consensus population matches the Phase-75 over-merge-refused finding
    assert all(c["scored"] is False and "oracle" not in c for c in real), "real cases are consensus-only"
    assert all(c["basis"] == "strong" and c["spine_verdict"] == "kept_distinct" for c in real), \
        "real candidate SHARES are strong-shared-id over-merges the spine refused"
    # the SYNTHETIC scored population spans the quadrants + carries the oracle
    klasses = {c["oracle"]["klass"] for c in syn}
    assert {KLASS_OVER_MERGE_TRAP, KLASS_FRAGMENTATION_GAP, KLASS_REAL_CO_REFERENCE,
            KLASS_CORRECT_REJECTION} <= klasses, f"scored cases must span all four quadrants: {klasses}"
    assert all(c["oracle"]["qualifier"] == SYNTHETIC_QUALIFIER for c in syn), "every scored case is qualified"
    bases = {c["basis"] for c in syn}
    assert bases == {"strong", "weak", "name"}, f"scored cases must exercise all three bases: {bases}"

    # the FIREWALL: no a/b evidence side carries a latent-truth field, on ANY case
    for c in cases:
        for side in ("a", "b"):
            assert not any(k in c[side] for k in _TRUTH_LEAK_KEYS), f"{c['id']}.{side} leaks truth"

    # DETERMINISM: two independent builds are byte-identical
    a = json.dumps(build(), indent=2, sort_keys=True, ensure_ascii=False)
    b = json.dumps(build(), indent=2, sort_keys=True, ensure_ascii=False)
    assert a == b, "build() must be deterministic (byte-identical across runs)"

    # broken-fixture rejection (the RED set — copy.deepcopy so mutations don't bleed)
    def broken(mut):
        d = copy.deepcopy(data)
        mut(d)
        return validate(d)

    def _put_oracle_on_real(d):
        r = next(c for c in d["cases"] if c["source"] == SOURCE_CONSENSUS)
        r["oracle"] = {"same_entity": True, "correct_adjudication": "uphold_merge",
                       "qualifier": SYNTHETIC_QUALIFIER}

    def _leak_truth(d):
        s = next(c for c in d["cases"] if c["source"] == SOURCE_SCORED)
        s["a"]["cluster"] = "C-LEAK"

    def _strip_qualifier(d):
        s = next(c for c in d["cases"] if c["source"] == SOURCE_SCORED)
        s["oracle"]["qualifier"] = "trust me"

    def _bad_grade(d):
        d["adjudication_grades"].append({"id": "auto_merge", "label": "x", "desc": "y"})

    def _flip_correct(d):
        s = next(c for c in d["cases"] if c["source"] == SOURCE_SCORED)
        s["oracle"]["correct_adjudication"] = ("reject_as_shares"
                                               if s["oracle"]["same_entity"] else "uphold_merge")

    def _note_leak(d):                         # the natural place a truth annotation would hide on evidence
        next(c for c in d["cases"])["a"]["note"] = "these are the same person, cluster C-LEAK"

    def _real_nonstrong(d):                    # a real case mis-shaped off the strong-shared-id residual
        next(c for c in d["cases"] if c["source"] == SOURCE_CONSENSUS)["basis"] = "name"

    checks = [
        ("oracle fabricated on a real case", _put_oracle_on_real, "no fabricated ground truth"),
        ("truth leaked into evidence", _leak_truth, "firewall"),
        ("a free-text note leaked onto evidence", _note_leak, "firewall"),
        ("scored case missing the qualifier", _strip_qualifier, "synthetic-only qualifier"),
        ("adjudication vocab widened", _bad_grade, "adjudication_grades must be exactly"),
        ("oracle correct_adjudication flipped", _flip_correct, "must follow same_entity"),
        ("a real case mis-shaped off basis=strong", _real_nonstrong, "strong-shared-id"),
    ]
    for name, mut, needle in checks:
        es = broken(mut)
        assert any(needle in e for e in es), f"validate must REJECT: {name} (looked for {needle!r}; got {es})"

    print(  # noqa: T201
        f"curate_merge_cases --selftest: PASS — {len(real)} REAL consensus candidate SHARES (over-merge "
        f"refused, no oracle) + {len(syn)} SYNTHETIC scored cases across all 4 quadrants / 3 bases; "
        f"firewall holds (no truth in evidence); deterministic; 7 broken fixtures rejected. "
        f"[scored numbers: {SYNTHETIC_QUALIFIER}]")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Curate the merge-adjudication console cases (companion-only, Phase 76).")
    ap.add_argument("--selftest", action="store_true", help="offline validators + determinism + broken-fixture rejection, exit")
    args = ap.parse_args()
    if args.selftest:
        return _selftest()
    data = build()
    errs = validate(data)
    if errs:
        print("REFUSING to write — validation failed:", file=sys.stderr)  # noqa: T201
        for e in errs:
            print(f"  - {e}", file=sys.stderr)  # noqa: T201
        return 1
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    n_real = data["provenance"]["n_real_consensus"]
    n_syn = data["provenance"]["n_synthetic_scored"]
    print(f"wrote {OUT_PATH.relative_to(ROOT)} — {n_real} real consensus + {n_syn} synthetic scored cases")  # noqa: T201
    return 0


if __name__ == "__main__":
    sys.exit(main())
