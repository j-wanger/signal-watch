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
TRUE_ENTITIES = ROOT / "data" / "entity-spine" / "true_entities.json"
SUBSTRATE_ANCHORED = ROOT / "data" / "entity-spine" / "substrate-anchored-slice.json"
SUBSTRATE_SANCTIONS = ROOT / "data" / "entity-spine" / "substrate-sanctions-slice.json"
OUT_PATH = ROOT / "data" / "merge" / "cases.json"

# the verified substrate HEAD the ANCHORED slice was emitted from (Phase 79 — the Phase-32/33 anchored fork;
# supersedes the Phase-75 consensus slice @fc98b09 now that a non-circular GT-<hash> oracle exists)
SUBSTRATE_HEAD = "c099259"
# the verified substrate HEAD the SANCTIONS slice was emitted from (Phase 80 — Phase-34 seam-5 sanctions screening)
SUBSTRATE_SANCTIONS_HEAD = "1f5901e"

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

SOURCE_SUBSTRATE_SCORED = "substrate-anchored-slice"   # real-substrate — scored vs the anchored GT-<hash> oracle (Phase 79)
SOURCE_SUBSTRATE_SANCTIONS = "substrate-sanctions-slice"  # Phase 80 — the OFAC name-collision merge class (scored vs the GT-<hash> oracle)
SOURCE_SCORED = "synthetic-oracle"                     # hand-authored synthetic — scored vs true_entities
SOURCES = frozenset({SOURCE_SUBSTRATE_SCORED, SOURCE_SUBSTRATE_SANCTIONS, SOURCE_SCORED})
# the two substrate-derived sources share the synthetic-substrate qualifier + the masking firewall
SUBSTRATE_SOURCES = frozenset({SOURCE_SUBSTRATE_SCORED, SOURCE_SUBSTRATE_SANCTIONS})
# Both populations are SYNTHETIC + SCORED; the split is now oracle PROVENANCE, each synthetic-only-qualified.
# (Phase 79 supersede: the substrate slice was never REAL production data — it LACKED an oracle until the
#  anchored fork emitted one; scoring it against substrate's OWN latent ground truth is honest, qualified.)
SUBSTRATE_QUALIFIER = "measured on a synthetic aml-substrate slice; production has no ground truth"

# the latent truth's correct adjudication, in the closed grade vocab
_CORRECT = {True: "uphold_merge", False: "reject_as_shares"}

# fields that would LEAK the latent truth into the pre-disposition evidence — forbidden on a/b (the firewall)
_TRUTH_LEAK_KEYS = ("cluster", "same_entity", "correct_adjudication", "klass", "note", "oracle")
# NB: email domain-masking to example.test now happens at DISTILLATION time (the committed
# data/entity-spine/substrate-anchored-slice.json carries masked locals); validate() re-checks no real
# domain ships. The synthetic-13 emails are authored .test by construction.


# --------------------------------------------------------------------------------------------------
def load_substrate_anchored() -> dict:
    return json.loads(SUBSTRATE_ANCHORED.read_text(encoding="utf-8"))


def enumerate_substrate_scored() -> list:
    """The SUBSTRATE-anchored SCORED real population (Phase 79 — SUPERSEDES the Phase-76/77 consensus-66).
    Reads the committed substrate-anchored capture (data/entity-spine/substrate-anchored-slice.json — the
    aml-substrate `--anchored --emit-eval-oracles` emit's GT-<hash> latent oracle + the candidate-relevant
    observations; emails domain-masked, email/phone DEMOTED to weak per Phase-75's noise-floor finding),
    runs the SAME deterministic resolver the synthetic path uses, enumerates the merge candidates, and scores
    each against the latent GT- cluster. NON-circular (GT-<hash> != entity_ref — the Phase-77 abort is cured)
    + genuinely two-sided (fragment co-references the demoted spine MISSES vs noise-floor collisions it
    correctly refuses). The oracle is substrate's OWN latent ground truth (not fabricated); every scored
    number carries the synthetic-SUBSTRATE qualifier. NO substrate run — replays the committed capture."""
    data = load_substrate_anchored()
    observations = data.get("observations", [])
    inputs = [resolver_input(o) for o in observations]
    pred = run_resolver(inputs)
    true = {o["obs_id"]: o["cluster"] for o in observations}
    cands = candidate_pairs(observations, pred, true)
    by_id = {o["obs_id"]: o for o in observations}
    cases = []
    for c in cands:
        a, b = by_id[c["a"]], by_id[c["b"]]
        shared = c.get("shared") or []
        sh = shared[0] if shared else None
        cases.append({
            "id": f"sub-{c['a']}-{c['b']}",
            "source": SOURCE_SUBSTRATE_SCORED, "scored": True, "basis": c["basis"],
            "shared": ({"kind": sh.get("kind"), "value": sh.get("normalized")} if sh else None),
            "spine_verdict": "merged" if c["resolver_merged"] else "kept_distinct",
            "a": _obs_side(a), "b": _obs_side(b),
            "oracle": {
                "same_entity": c["same_entity"],
                "klass": c["klass"],
                "correct_adjudication": _CORRECT[c["same_entity"]],
                "qualifier": SUBSTRATE_QUALIFIER,
            },
        })
    cases.sort(key=lambda c: (c["basis"], c["a"]["ref"], c["b"]["ref"]))
    return cases


def _obs_side(obs: dict) -> dict:
    """A synthetic case side from a true_entities observation — only the OBSERVABLE surface (the firewall:
    `resolver_input` strips the latent `cluster` + the eval-only `note`). Identifiers shown as kind/value."""
    clean = resolver_input(obs)
    return {"ref": clean.get("obs_id"), "name": clean.get("name"), "kind": clean.get("kind"),
            "role": clean.get("role"),
            "identifiers": [{"kind": i.get("kind"), "value": i.get("value")}
                            for i in (clean.get("identifiers") or [])]}


def _obs_side_sanctions(obs: dict) -> dict:
    """A sanctions case side: the firewall-stripped observable surface (`_obs_side`) PLUS the OBSERVABLE
    `sanctions_screen` bank state (flagged + source). The watchlist flag is observable evidence (the bank's
    OWN screening result), NOT the latent truth — it is INDEPENDENT of same_entity (a flagged record can be
    either an uphold or a reject), so it never leaks the oracle. (`_obs_side` -> resolver_input had stripped
    sanctions_screen because it is identity-irrelevant; we re-attach it here as evidence, not as a key the
    resolver ever saw.)"""
    side = _obs_side(obs)
    sc = obs.get("sanctions_screen") or {}
    side["sanctions_screen"] = {"flagged": bool(sc.get("flagged")), "source": sc.get("source")}
    return side


def load_substrate_sanctions() -> dict:
    return json.loads(SUBSTRATE_SANCTIONS.read_text(encoding="utf-8"))


def enumerate_substrate_sanctions() -> list:
    """The OFAC NAME-COLLISION merge case class (Phase 80 — the Phase-34 sanctions-screening consume).
    Reads the committed substrate-sanctions-slice.json (the Phase-34 `--anchored --emit-screening
    --emit-eval-oracles` emit's GT-<hash> latent oracle + the sanctions-relevant observations; emails
    domain-masked), runs the SAME demoted resolver, enumerates the merge candidates, and KEEPS those
    touching a watchlist-flagged record. Scored against the latent GT- cluster (NON-circular: GT != the
    declared entity_ref). Genuinely TWO-SIDED:
      * uphold_merge — a flagged record + its same-person FRAGMENT that evaded screening (the typo broke the
        watchlist token): entity resolution is PREREQUISITE to correct sanctions coverage;
      * reject_as_shares — two DISTINCT customers sharing a watchlisted name, >=1 flagged: the common-name
        false positive (merging would spread one customer's coincidental hit onto a stranger).
    The watchlist match is a LABEL-BLIND collision — no party IS a designated person. Spans the strong + name
    bases. NO substrate run — replays the committed slice."""
    data = load_substrate_sanctions()
    observations = data.get("observations", [])
    by_id = {o["obs_id"]: o for o in observations}
    flagset = {o["obs_id"] for o in observations if (o.get("sanctions_screen") or {}).get("flagged")}
    inputs = [resolver_input(o) for o in observations]
    pred = run_resolver(inputs)
    true = {o["obs_id"]: o["cluster"] for o in observations}
    cands = candidate_pairs(observations, pred, true)
    cases = []
    for c in cands:
        if c["a"] not in flagset and c["b"] not in flagset:
            continue                                      # the sanctions class = at least one watchlist-flagged side
        a, b = by_id[c["a"]], by_id[c["b"]]
        shared = c.get("shared") or []
        sh = shared[0] if shared else None
        cases.append({
            "id": f"sanc-{c['a']}-{c['b']}",
            "source": SOURCE_SUBSTRATE_SANCTIONS, "scored": True, "basis": c["basis"],
            "shared": ({"kind": sh.get("kind"), "value": sh.get("normalized")} if sh else None),
            "spine_verdict": "merged" if c["resolver_merged"] else "kept_distinct",
            "a": _obs_side_sanctions(a), "b": _obs_side_sanctions(b),
            "oracle": {
                "same_entity": c["same_entity"],
                "klass": c["klass"],
                "correct_adjudication": _CORRECT[c["same_entity"]],
                "qualifier": SUBSTRATE_QUALIFIER,
            },
        })
    cases.sort(key=lambda c: (c["basis"], c["a"]["ref"], c["b"]["ref"]))
    return cases


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
    substrate = enumerate_substrate_scored()
    sanctions = enumerate_substrate_sanctions()
    syn = enumerate_synthetic_scored()
    cap = load_substrate_anchored()
    sanc_cap = load_substrate_sanctions()
    return {
        "_note": ("FULLY curated merge-adjudication cases (Phase 76; SUPERSEDE Phase 79; + the Phase-80 "
                  "sanctions class; regeneration-only — .venv/bin/python scripts/curate_merge_cases.py). THREE "
                  "SCORED populations, kept visibly separate by oracle PROVENANCE (all synthetic, all scored "
                  "against a non-circular GT-<hash>/true_entities oracle, each provenance-qualified): "
                  f"(1) {len(substrate)} REAL-SUBSTRATE candidate SHARES from aml-substrate's --anchored "
                  f"--emit-eval-oracles slice (@{SUBSTRATE_HEAD}, Phase-32/33 anchored fork) — scored against "
                  "substrate's OWN latent GT-<hash> identity oracle (NON-circular: GT != entity_ref). The "
                  "demoted spine (email/phone weak — Phase-75's noise floor) refuses every candidate; the "
                  "oracle reveals which are real fragment co-references it MISSED (uphold_merge) vs noise-floor "
                  "collisions it correctly refused (reject_as_shares). "
                  f"(2) {len(sanctions)} OFAC NAME-COLLISION sanctions-screening cases from the Phase-34 "
                  f"--anchored sanctions slice (@{SUBSTRATE_SANCTIONS_HEAD}) — a LABEL-BLIND watchlist name "
                  "collision (no party IS a designated person); the merge question is 'are these two RECORDS "
                  "the same customer', with the watchlist flag as evidence. Two-sided: a flagged record + its "
                  "same-person fragment that evaded screening (uphold_merge — entity resolution is prerequisite "
                  "to correct sanctions coverage) vs two distinct customers sharing a watchlisted name "
                  "(reject_as_shares — the common-name false positive). "
                  f"(3) {len(syn)} hand-authored SYNTHETIC scored cases from data/entity-spine/true_entities.json "
                  "— spanning all 4 quadrants / 3 bases. ALL populations' latent truth rides ONLY each case's "
                  "`oracle` block (revealed post-disposition); the pre-disposition evidence (a/b) carries no "
                  "truth field (the resolver-input firewall). Shared emails are domain-masked to example.test "
                  "(the local-part token kept, proving the exact collision). Illustrative; no rate, score, or "
                  "multiplier is claimed; every scored number is synthetic-only-qualified."),
        "badge": BADGE,
        "brand": {"title": "Signal Watch", "subtitle": "Merge Console · Vision Prototype"},
        "adjudication_grades": ADJUDICATION_GRADES,
        "bases": BASES,
        "provenance": {
            "substrate_head": SUBSTRATE_HEAD,
            "substrate_slice": cap.get("provenance", {}),
            "substrate_sanctions_head": SUBSTRATE_SANCTIONS_HEAD,
            "substrate_sanctions_slice": sanc_cap.get("provenance", {}),
            "n_substrate_scored": len(substrate),
            "n_substrate_sanctions_scored": len(sanctions),
            "n_synthetic_scored": len(syn),
            "synthetic_qualifier": SYNTHETIC_QUALIFIER,
            "substrate_qualifier": SUBSTRATE_QUALIFIER,
        },
        "cases": substrate + sanctions + syn,
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
    seen, n_substrate, n_sanctions, n_syn = set(), 0, 0, 0
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
        if src not in SOURCES:
            errs.append(f"{cid}: source {src!r} not in {sorted(SOURCES)}")
        else:
            # ALL populations are SCORED — each carries an oracle, qualified by provenance (the two substrate
            # sources share the synthetic-substrate qualifier; the hand-authored set the synthetic-only one).
            want_qual = SUBSTRATE_QUALIFIER if src in SUBSTRATE_SOURCES else SYNTHETIC_QUALIFIER
            if scored is not True:
                errs.append(f"{cid}: a scored case must have scored=true")
            if not isinstance(oracle, dict):
                errs.append(f"{cid}: a scored case must carry an oracle block")
            else:
                if not isinstance(oracle.get("same_entity"), bool):
                    errs.append(f"{cid}: oracle.same_entity must be a bool")
                if oracle.get("correct_adjudication") not in GRADE_IDS:
                    errs.append(f"{cid}: oracle.correct_adjudication not in the grade vocab")
                if oracle.get("correct_adjudication") != _CORRECT.get(oracle.get("same_entity")):
                    errs.append(f"{cid}: oracle.correct_adjudication must follow same_entity")
                if oracle.get("qualifier") != want_qual:
                    errs.append(f"{cid}: scored case must carry its provenance qualifier "
                                f"({'synthetic-substrate' if src in SUBSTRATE_SOURCES else 'synthetic-only'})")
            if src in SUBSTRATE_SOURCES:
                # both substrate populations are demoted-spine refused + masked (no real email domain may ship)
                if c.get("spine_verdict") != "kept_distinct":
                    errs.append(f"{cid}: substrate cases are demoted-spine refused (spine_verdict=kept_distinct)")
                sh = c.get("shared") or {}
                if sh.get("kind") == "email" and not str(sh.get("value") or "").endswith("@example.test"):
                    errs.append(f"{cid}: a shipped substrate email must be domain-masked to example.test")
            if src == SOURCE_SUBSTRATE_SCORED:
                n_substrate += 1
                # the anchored population is the DEMOTED-spine refused residual over strong-shared ids
                if c.get("basis") != "strong":
                    errs.append(f"{cid}: substrate candidate SHARES are strong-shared-id (basis=strong)")
            elif src == SOURCE_SUBSTRATE_SANCTIONS:
                n_sanctions += 1
                # the OFAC name-collision class spans the strong + name bases; >=1 side carries the watchlist flag
                if c.get("basis") not in ("strong", "name"):
                    errs.append(f"{cid}: sanctions cases span the strong + name bases (basis in strong|name)")
                flagged = [s for s in (c.get("a"), c.get("b"))
                           if isinstance(s, dict) and (s.get("sanctions_screen") or {}).get("flagged")]
                if not flagged:
                    errs.append(f"{cid}: a sanctions case needs >=1 watchlist-flagged side (sanctions_screen.flagged)")
            else:
                n_syn += 1
        if c.get("basis") in ("strong", "weak") and not (c.get("shared") and c["shared"].get("kind")):
            errs.append(f"{cid}: a {c.get('basis')} basis needs a shared identifier")
        if c.get("basis") == "name" and c.get("shared"):
            errs.append(f"{cid}: a name-only basis must have no shared identifier")
    if n_substrate == 0:
        errs.append("no substrate-scored candidate SHARES (the anchored-slice population is missing)")
    if n_sanctions == 0:
        errs.append("no substrate-sanctions cases (the OFAC name-collision population is missing)")
    if n_syn == 0:
        errs.append("no synthetic scored cases (the hand-authored scored population is missing)")
    # the substrate populations must be TWO-SIDED (uphold + reject) — a one-sided "scored" oracle is the Phase-77 trap
    for label, src_id in (("substrate-anchored", SOURCE_SUBSTRATE_SCORED),
                          ("substrate-sanctions", SOURCE_SUBSTRATE_SANCTIONS)):
        sides = {c["oracle"]["same_entity"] for c in cases
                 if c.get("source") == src_id and isinstance(c.get("oracle"), dict)
                 and isinstance(c["oracle"].get("same_entity"), bool)}
        if sides and sides != {True, False}:
            errs.append(f"the {label} population must be TWO-SIDED (uphold + reject); got same_entity={sorted(sides)}")
    prov = data.get("provenance") or {}
    if (prov.get("n_substrate_scored") != n_substrate or prov.get("n_synthetic_scored") != n_syn
            or prov.get("n_substrate_sanctions_scored") != n_sanctions):
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
    substrate = [c for c in cases if c["source"] == SOURCE_SUBSTRATE_SCORED]
    sanctions = [c for c in cases if c["source"] == SOURCE_SUBSTRATE_SANCTIONS]
    syn = [c for c in cases if c["source"] == SOURCE_SCORED]
    assert substrate and sanctions and syn, "all three scored populations must be present"
    # the SUBSTRATE-anchored population: SCORED (oracle), demoted-spine refused, TWO-SIDED, substrate-qualified
    assert all(c["scored"] is True and isinstance(c.get("oracle"), dict) for c in substrate), \
        "substrate cases are scored (carry an oracle)"
    assert all(c["basis"] == "strong" and c["spine_verdict"] == "kept_distinct" for c in substrate), \
        "substrate candidate SHARES are strong-shared-id, demoted-spine refused"
    assert all(c["oracle"]["qualifier"] == SUBSTRATE_QUALIFIER for c in substrate), \
        "substrate cases carry the synthetic-substrate qualifier"
    sub_same = {c["oracle"]["same_entity"] for c in substrate}
    assert sub_same == {True, False}, \
        f"the anchored slice must be TWO-SIDED (uphold + reject), got same_entity={sub_same} (the Phase-77 cure)"
    # the SANCTIONS population (Phase 80): scored, demoted-spine refused, strong+name bases, >=1 flagged side, TWO-SIDED
    assert all(c["scored"] is True and isinstance(c.get("oracle"), dict) for c in sanctions), \
        "sanctions cases are scored (carry an oracle)"
    assert all(c["spine_verdict"] == "kept_distinct" for c in sanctions), "sanctions cases are demoted-spine refused"
    assert all(c["basis"] in ("strong", "name") for c in sanctions), "sanctions cases span the strong + name bases"
    assert all(c["oracle"]["qualifier"] == SUBSTRATE_QUALIFIER for c in sanctions), \
        "sanctions cases carry the synthetic-substrate qualifier"
    assert all(any((s.get("sanctions_screen") or {}).get("flagged") for s in (c["a"], c["b"])) for c in sanctions), \
        "every sanctions case carries the watchlist flag on >=1 side"
    sanc_same = {c["oracle"]["same_entity"] for c in sanctions}
    assert sanc_same == {True, False}, \
        f"the sanctions slice must be TWO-SIDED (uphold + reject), got same_entity={sanc_same} (the Phase-77 cure)"
    assert {c["basis"] for c in sanctions} == {"strong", "name"}, \
        "sanctions cases must exercise BOTH the strong (fragment-evades-screening) + name (namesake) bases"
    # the SYNTHETIC scored population spans the quadrants + carries the oracle
    klasses = {c["oracle"]["klass"] for c in syn}
    assert {KLASS_OVER_MERGE_TRAP, KLASS_FRAGMENTATION_GAP, KLASS_REAL_CO_REFERENCE,
            KLASS_CORRECT_REJECTION} <= klasses, f"scored cases must span all four quadrants: {klasses}"
    assert all(c["oracle"]["qualifier"] == SYNTHETIC_QUALIFIER for c in syn), "every synthetic scored case is qualified"
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

    def _unscored_substrate(d):                # a substrate case stripped of its oracle (must stay scored)
        r = next(c for c in d["cases"] if c["source"] == SOURCE_SUBSTRATE_SCORED)
        r["scored"] = False
        r.pop("oracle", None)

    def _wrong_qualifier_substrate(d):         # a substrate case carrying the WRONG provenance qualifier
        next(c for c in d["cases"] if c["source"] == SOURCE_SUBSTRATE_SCORED)["oracle"]["qualifier"] = SYNTHETIC_QUALIFIER

    def _unmasked_email(d):                    # a real substrate email shipped on a real domain (mask firewall)
        next(c for c in d["cases"] if c["source"] == SOURCE_SUBSTRATE_SCORED)["shared"] = {"kind": "email", "value": "evil@gmail.com"}

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

    def _substrate_nonstrong(d):               # a substrate case mis-shaped off the strong-shared-id residual
        next(c for c in d["cases"] if c["source"] == SOURCE_SUBSTRATE_SCORED)["basis"] = "name"

    def _sanctions_unflagged(d):               # a sanctions case stripped of the watchlist flag on BOTH sides
        s = next(c for c in d["cases"] if c["source"] == SOURCE_SUBSTRATE_SANCTIONS)
        for side in ("a", "b"):
            s[side]["sanctions_screen"] = {"flagged": False, "source": "x"}

    checks = [
        ("substrate case stripped of its oracle", _unscored_substrate, "must carry an oracle block"),
        ("substrate case with the wrong provenance qualifier", _wrong_qualifier_substrate, "provenance qualifier"),
        ("a real substrate email shipped unmasked", _unmasked_email, "domain-masked to example.test"),
        ("truth leaked into evidence", _leak_truth, "firewall"),
        ("a free-text note leaked onto evidence", _note_leak, "firewall"),
        ("scored case missing the qualifier", _strip_qualifier, "provenance qualifier"),
        ("adjudication vocab widened", _bad_grade, "adjudication_grades must be exactly"),
        ("oracle correct_adjudication flipped", _flip_correct, "must follow same_entity"),
        ("a substrate case mis-shaped off basis=strong", _substrate_nonstrong, "strong-shared-id"),
        ("a sanctions case stripped of the watchlist flag", _sanctions_unflagged, "watchlist-flagged side"),
    ]
    for name, mut, needle in checks:
        es = broken(mut)
        assert any(needle in e for e in es), f"validate must REJECT: {name} (looked for {needle!r}; got {es})"

    print(  # noqa: T201
        f"curate_merge_cases --selftest: PASS — {len(substrate)} REAL-SUBSTRATE scored candidate SHARES "
        f"(anchored GT- oracle, NON-circular, two-sided: "
        f"{sum(1 for c in substrate if c['oracle']['same_entity'])} uphold / "
        f"{sum(1 for c in substrate if not c['oracle']['same_entity'])} reject) + {len(sanctions)} OFAC "
        f"NAME-COLLISION sanctions cases (two-sided: "
        f"{sum(1 for c in sanctions if c['oracle']['same_entity'])} uphold / "
        f"{sum(1 for c in sanctions if not c['oracle']['same_entity'])} reject; strong+name bases) + "
        f"{len(syn)} SYNTHETIC scored cases across all 4 quadrants / 3 bases; firewall holds (no truth in "
        f"evidence); deterministic; {len(checks)} broken fixtures rejected. [scored numbers: synthetic-only-qualified]")
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
    n_sub = data["provenance"]["n_substrate_scored"]
    n_sanc = data["provenance"]["n_substrate_sanctions_scored"]
    n_syn = data["provenance"]["n_synthetic_scored"]
    print(f"wrote {OUT_PATH.relative_to(ROOT)} — {n_sub} substrate-scored + {n_sanc} sanctions "  # noqa: T201
          f"+ {n_syn} synthetic scored cases")
    return 0


if __name__ == "__main__":
    sys.exit(main())
