#!/usr/bin/env python3
"""Distill the SANCTIONS-screening merge slice (Phase 80 — companion-only AUTHORING tool).

Reads an aml-substrate `--anchored --emit-screening --emit-eval-oracles` emit dir and distills the
candidate-relevant observations + the GT-<hash> latent oracle into the committed
`data/entity-spine/substrate-sanctions-slice.json` — the no-substrate-replayable capture the merge
curator (`curate_merge_cases.enumerate_substrate_sanctions`) reads to build the OFAC name-collision
merge case class.

THE TWO-SIDEDNESS (the Phase-80 measure-first GATE result, GREEN):
  Phase 34's `--anchored` sanctions overlay sets `sanctions_flag` on a party whose normalized SURNAME
  token collides with the public-domain OFAC SDN index — a LABEL-BLIND collision: NO substrate party IS
  a real designated person (aml-substrate names.py:391). So the merge question is NOT "is this the
  sanctioned person" (that would be one-sided/all-reject — the Phase-77 trap) but the entity-resolution
  question "are these two RECORDS the same customer", with the watchlist flag as the evidence that
  raises the stakes. Two-sidedness comes from the Phase-32 fragment overlay running ALONGSIDE sanctions:
    * UPHOLD — a flagged record + its same-person FRAGMENT (the typo'd fragment evaded screening): merging
      is correct AND consolidates the (coincidental) watchlist exposure. Entity resolution is PREREQUISITE
      to correct sanctions coverage.
    * REJECT — two DISTINCT customers sharing a watchlisted name, >=1 flagged: merging would wrongly spread
      one customer's coincidental sanctions hit onto a stranger — the common-name false positive.
  The GT-<hash> latent cluster (sha1 of the latent entity, != entity_ref -> NON-circular) is the oracle.

THE FIREWALL: the resolver never sees the latent `cluster` (resolution_scorer.resolver_input strips it)
nor `sanctions_screen` (identity-irrelevant); the curator surfaces `sanctions_screen` only on the
post-disposition-safe EVIDENCE side (it is OBSERVABLE bank state, never the truth). Real emails are
domain-masked to example.test (the local-part token kept, proving the collision); phones are already
synthetic. Names are real-FREQUENCY synthetic (common surnames), never a designated individual.

COMPANION-ONLY: build.py NEVER imports this. Needs duckdb (parquet) — run under the .venv.

Re-distill (authoring-time, needs a substrate emit):
  # 1) emit at the pinned HEAD (known-good route — NOT --monitor/--emit-evidence, which ReplayErrors):
  PYTHONPATH=<sub>/src <sub>/.venv/bin/python -m aml_substrate.cli \
    --clients 12000 --months 3 --seed 0 --emergence --anchored --screen --emit-screening \
    --emit-eval-oracles --out <emit>
  # 2) distill:
  .venv/bin/python scripts/distill_sanctions_slice.py --emit-dir <emit>
Selftest (no substrate — replays the committed slice):
  .venv/bin/python scripts/distill_sanctions_slice.py --selftest
"""
from __future__ import annotations

import argparse
import json
import sys
import zlib
from collections import defaultdict
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
ROOT = _HERE.parent
OUT_PATH = ROOT / "data" / "entity-spine" / "substrate-sanctions-slice.json"

# the verified substrate HEAD this slice is distilled from (Phase 34 — seam-5 sanctions screening)
SUBSTRATE_PIN = "1f5901e"
EMIT_COMMAND = ("PYTHONPATH=<sub>/src <sub>/.venv/bin/python -m aml_substrate.cli "
                "--clients 12000 --months 3 --seed 0 --emergence --anchored --screen --emit-screening "
                "--emit-eval-oracles --out <emit>")
PARAMS = {"clients": 12000, "months": 3, "seed": 0, "anchored": True}
QUALIFIER = "measured on a synthetic aml-substrate slice; production has no ground truth"
WATCHLIST_SOURCE = ("OFAC SDN (US-federal public domain, 17 USC 105) — label-blind name collision; "
                    "no party IS a designated person")

from resolution_scorer import resolver_input, run_resolver, candidate_pairs  # noqa: E402


def _mask_email(e: str | None) -> str | None:
    """Domain-mask a real substrate email to example.test, keeping a deterministic local-part token
    (so the exact collision is provable without shipping a real address)."""
    if not e:
        return None
    h = zlib.crc32(str(e).encode()) & 0xFFFFFFFF
    return f"user{h % 100000}@example.test"


def _observation(pid: str, p: dict, cluster: str) -> dict:
    """An observation in the committed-slice shape (mirrors substrate-anchored-slice.json) + a
    `sanctions_screen` OBSERVABLE annotation. Identifiers demoted to weak (Phase-75 noise-floor)."""
    ids = []
    if p.get("email"):
        m = _mask_email(p["email"])
        ids.append({"kind": "email", "value": m, "normalized": m, "strength": "weak"})
    if p.get("phone"):
        ph = str(p["phone"])
        ids.append({"kind": "phone", "value": ph, "normalized": ph.lstrip("+"), "strength": "weak"})
    return {
        "obs_id": pid,
        "name": f"{p['given']} {p['surname']}".strip(),
        "kind": "person",
        "role": p.get("role") or "LEGIT",
        "identifiers": ids,
        "cluster": cluster,                                   # the EVAL-ONLY GT- oracle (never a resolver input)
        "sanctions_screen": {"flagged": bool(p.get("sanc")), "source": WATCHLIST_SOURCE},
    }


def distill(emit_dir: Path) -> dict:
    """Read the substrate emit dir and distill the sanctions-touching merge slice. Deterministic."""
    import duckdb
    con = duckdb.connect()
    rows = con.execute(
        f"""SELECT party_id, given_name, surname, email, phone, sanctions_flag, latent_role
            FROM '{emit_dir}/persons.parquet'"""
    ).fetchall()
    cols = ["party_id", "given", "surname", "email", "phone", "sanc", "role"]
    persons = {r[0]: dict(zip(cols, r)) for r in rows}
    oracle = {e["entity_ref"]: e["cluster"]
              for e in json.loads((emit_dir / "identity" / "true_entities.json").read_text())["entities"]}

    flagged = [pid for pid, v in persons.items() if v["sanc"]]
    gt2refs = defaultdict(list)
    for ref, gt in oracle.items():
        gt2refs[gt].append(ref)
    byname = defaultdict(list)
    for pid, v in persons.items():
        byname[(v["given"], v["surname"])].append(pid)

    # the sanctions-relevant universe: every flagged party + its same-person fragments (cluster mates)
    # + its exact-name namesakes (the two faces of the merge decision)
    relevant = set()
    for pid in flagged:
        relevant.add(pid)
        for m in gt2refs.get(oracle.get(pid, ""), []):
            relevant.add(m)
        for m in byname[(persons[pid]["given"], persons[pid]["surname"])]:
            relevant.add(m)
    relevant = {r for r in relevant if r in persons and r in oracle}

    full_obs = [_observation(r, persons[r], oracle[r]) for r in sorted(relevant)]
    # enumerate candidates, KEEP only those touching a watchlist-flagged record (the sanctions case class)
    inputs = [resolver_input(o) for o in full_obs]
    pred = run_resolver(inputs)
    true = {o["obs_id"]: o["cluster"] for o in full_obs}
    cands = candidate_pairs(full_obs, pred, true)
    flagset = set(flagged)
    sanc = [c for c in cands if c["a"] in flagset or c["b"] in flagset]
    # TRIM the slice to the obs that participate in a kept candidate (keeps the committed file tight)
    keep_ids = {c["a"] for c in sanc} | {c["b"] for c in sanc}
    obs = [o for o in full_obs if o["obs_id"] in keep_ids]

    n_up = sum(1 for c in sanc if c["same_entity"])
    n_rej = len(sanc) - n_up
    return {
        "contract_version": "0.5",
        "note": ("EVAL-ONLY sanctions-screening merge slice (Phase 80). Each observation's `cluster` is the "
                 "GT-<hash> latent identity oracle — NEVER a resolver input (the firewall). `sanctions_screen` "
                 "is OBSERVABLE bank screening state (a label-blind OFAC name collision — no party IS a "
                 "designated person), surfaced only on the post-disposition-safe evidence side. Emails "
                 "domain-masked to example.test."),
        "provenance": {
            "emit_command": EMIT_COMMAND,
            "substrate_pin": SUBSTRATE_PIN,
            "params": PARAMS,
            "n_observations": len(obs),
            "n_flagged_obs": sum(1 for o in obs if o["sanctions_screen"]["flagged"]),
            "n_candidates_sanctions_touching": len(sanc),
            "two_sided": {"uphold_merge": n_up, "reject_as_shares": n_rej},
            "qualifier": QUALIFIER,
        },
        "observations": obs,
    }


# --------------------------------------------------------------------------------------------------
def load() -> dict:
    return json.loads(OUT_PATH.read_text(encoding="utf-8"))


def replay_candidates(slice_data: dict):
    """Replay the committed slice through candidate_pairs (NO substrate) -> the sanctions-touching candidates."""
    obs = slice_data["observations"]
    flagset = {o["obs_id"] for o in obs if o.get("sanctions_screen", {}).get("flagged")}
    inputs = [resolver_input(o) for o in obs]
    pred = run_resolver(inputs)
    true = {o["obs_id"]: o["cluster"] for o in obs}
    cands = candidate_pairs(obs, pred, true)
    return [c for c in cands if c["a"] in flagset or c["b"] in flagset]


def validate(slice_data: dict) -> list:
    """Structural validators on the committed slice (no substrate). Returns error strings; never raises."""
    errs = []
    obs = slice_data.get("observations") or []
    if not obs:
        errs.append("no observations")
    seen = set()
    for o in obs:
        oid = o.get("obs_id")
        if not oid or oid in seen:
            errs.append(f"bad/duplicate obs_id {oid!r}")
        seen.add(oid)
        if not str(o.get("cluster", "")).startswith("GT-"):
            errs.append(f"{oid}: cluster must be a GT-<hash> latent id (non-circular), got {o.get('cluster')!r}")
        if "flagged" not in (o.get("sanctions_screen") or {}):
            errs.append(f"{oid}: missing sanctions_screen.flagged")
        for i in o.get("identifiers") or []:
            if i.get("kind") == "email" and not str(i.get("value") or "").endswith("@example.test"):
                errs.append(f"{oid}: a shipped email must be domain-masked to example.test")
    prov = slice_data.get("provenance") or {}
    if prov.get("substrate_pin") != SUBSTRATE_PIN:
        errs.append(f"provenance.substrate_pin must be {SUBSTRATE_PIN!r}")
    if prov.get("qualifier") != QUALIFIER:
        errs.append("provenance.qualifier missing/wrong")
    return errs


def _selftest() -> int:
    try:
        data = load()
    except FileNotFoundError:
        print("distill_sanctions_slice --selftest: SKIP (no committed slice yet)")  # noqa: T201
        return 0
    errs = validate(data)
    assert not errs, f"committed slice must validate: {errs}"
    # failure-path coverage: validate() must REJECT the structural tamperings it guards
    import copy
    def _broken(mut):
        d = copy.deepcopy(data)
        mut(d)
        return validate(d)
    assert any("GT-" in e for e in _broken(lambda d: d["observations"][0].update({"cluster": "ENT-circular"}))), \
        "validate must reject a non-GT (circular) cluster"
    assert any("masked" in e for e in _broken(
        lambda d: d["observations"][0].__setitem__("identifiers", [{"kind": "email", "value": "evil@gmail.com"}]))), \
        "validate must reject an unmasked real email domain"
    assert any("sanctions_screen" in e for e in _broken(
        lambda d: d["observations"][0].pop("sanctions_screen", None))), \
        "validate must reject a missing sanctions_screen flag"
    assert any("substrate_pin" in e for e in _broken(lambda d: d["provenance"].__setitem__("substrate_pin", "deadbeef"))), \
        "validate must reject a wrong substrate pin"
    try:
        sanc = replay_candidates(data)
    except RuntimeError as e:                      # duckdb absent (the spine needs it)
        print(f"distill_sanctions_slice --selftest: SKIP candidate replay ({e}); structure PASS")  # noqa: T201
        return 0
    same = {c["same_entity"] for c in sanc}
    assert same == {True, False}, \
        f"the sanctions slice must be TWO-SIDED (uphold + reject); got same_entity={same} (the Phase-77 cure)"
    # the firewall: a resolver input never carries cluster/sanctions_screen
    from resolution_scorer import assert_no_cluster_leak
    assert_no_cluster_leak([resolver_input(o) for o in data["observations"]])
    n_up = sum(1 for c in sanc if c["same_entity"])
    n_rej = len(sanc) - n_up
    prov = data["provenance"]["two_sided"]
    assert prov == {"uphold_merge": n_up, "reject_as_shares": n_rej}, \
        f"provenance two_sided {prov} disagrees with the replay {n_up}/{n_rej}"
    print(  # noqa: T201
        f"distill_sanctions_slice --selftest: PASS — {len(data['observations'])} obs, "
        f"{len(sanc)} sanctions-touching merge candidates TWO-SIDED "
        f"({n_up} uphold / {n_rej} reject); GT-<hash> non-circular; emails masked; firewall holds. "
        f"[{QUALIFIER}]")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Distill the sanctions-screening merge slice (companion-only, Phase 80).")
    ap.add_argument("--emit-dir", help="a substrate --anchored --emit-screening --emit-eval-oracles emit dir")
    ap.add_argument("--selftest", action="store_true", help="replay the committed slice (no substrate), exit")
    args = ap.parse_args()
    if args.selftest:
        return _selftest()
    if not args.emit_dir:
        ap.error("need --emit-dir <emit> (or --selftest)")
    data = distill(Path(args.emit_dir).expanduser().resolve())
    errs = validate(data)
    if errs:
        print("REFUSING to write — validation failed:", file=sys.stderr)  # noqa: T201
        for e in errs:
            print(f"  - {e}", file=sys.stderr)  # noqa: T201
        return 1
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    ts = data["provenance"]["two_sided"]
    print(f"wrote {OUT_PATH.relative_to(ROOT)} — {len(data['observations'])} obs, "  # noqa: T201
          f"{data['provenance']['n_candidates_sanctions_touching']} sanctions-touching candidates "
          f"({ts['uphold_merge']} uphold / {ts['reject_as_shares']} reject)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
