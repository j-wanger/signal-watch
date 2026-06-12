#!/usr/bin/env python3
"""curate_console_cases.py — build the gate console's adjudication-case dataset (Phase 47).

AUTHORING-TIME / REGENERATION-ONLY. This script reads git history; the committed artifact
(data/console/cases.json) is the authority and its validation (build.validate_console_cases)
NEVER depends on git — it checks the dataset against the CURRENT committed derived records only.

What a case is: the Phase-34 C/D-assignment verification (commit 83a79c3) corrected the
capability/data-source codes of 213 derived indicators after a blind inter-rater measurement +
human adjudication. Each before/after pair is a REAL adjudication scenario — rater A (the
pre-correction assignment) vs rater B (the post-correction assignment) disagreeing on an
indicator's C/D tags. Every field is COPIED from committed data or the git pre-image; nothing
is synthesized. The grounded `flag`/`red_flag` were byte-identical across the correction (the
commit pins this; this script re-verifies and fails loud if not).

Deterministic: no randomness, no timestamps; the changed-file set and the pre-images come from
the pinned commit; cases sort by (doc_id, indicator position). Re-running on the same tree
yields byte-identical output. Stdlib only.

Usage: python3 scripts/curate_console_cases.py   # rewrites data/console/cases.json
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# Phase 34: "C/D-assignment verification of the 1,376 new corpus indicators" — the correction commit.
CORRECTION_COMMIT = "83a79c3f481e10db838caccec6bcb2ff3a923eba"
TAXONOMY = ROOT / "data" / "capability-taxonomy.json"
OUT = ROOT / "data" / "console" / "cases.json"


def die(msg: str, code: int = 1) -> None:
    print(f"curate_console_cases: error: {msg}", file=sys.stderr)
    raise SystemExit(code)


def _git(*args: str) -> str:
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        die(f"git {' '.join(args)} failed: {r.stderr.strip()}")
    return r.stdout


def changed_derived_paths() -> list:
    """The derived-record files the correction commit touched (repo-relative, sorted)."""
    names = _git("show", "--name-only", "--pretty=format:", CORRECTION_COMMIT).splitlines()
    return sorted(p for p in names if "/derived/" in p and p.endswith(".json"))


def load_taxonomy_names() -> tuple:
    """code -> human name maps for capabilities + data sources (CURRENT committed taxonomy)."""
    doc = json.loads(TAXONOMY.read_text(encoding="utf-8"))
    return ({x["id"]: x["name"] for x in doc["capabilities"]},
            {x["id"]: x["name"] for x in doc["data_sources"]})


def manifest_entry(source_dir: Path, doc_id: str) -> dict:
    """The doc's entry in its source dir's corpus-status.json (title/url provenance)."""
    manifest = json.loads((source_dir / "corpus-status.json").read_text(encoding="utf-8"))
    for a in manifest.get("advisories", []):
        if a.get("id") == doc_id:
            return a
    die(f"{doc_id}: no entry in {source_dir.name}/corpus-status.json")


def rater(code_c: str, code_d: str, cap_names: dict, src_names: dict, who: str, doc_id: str) -> dict:
    if code_c not in cap_names:
        die(f"{doc_id}: {who} capability {code_c!r} not in the current taxonomy")
    if code_d not in src_names:
        die(f"{doc_id}: {who} data_source {code_d!r} not in the current taxonomy")
    return {"capability": code_c, "capability_name": cap_names[code_c],
            "data_source": code_d, "data_source_name": src_names[code_d]}


def main() -> None:
    cap_names, src_names = load_taxonomy_names()
    cases = []
    for rel in changed_derived_paths():
        pre = json.loads(_git("show", f"{CORRECTION_COMMIT}^:{rel}"))
        cur_path = ROOT / rel
        if not cur_path.exists():
            die(f"{rel}: changed in {CORRECTION_COMMIT[:7]} but missing from the working tree")
        post = json.loads(cur_path.read_text(encoding="utf-8"))
        pre_inds, post_inds = pre.get("indicators") or [], post.get("indicators") or []
        if len(pre_inds) != len(post_inds):
            die(f"{rel}: indicator count differs pre ({len(pre_inds)}) vs current ({len(post_inds)})")
        doc_id = post["id"]
        source_dir = cur_path.parent.parent           # data/<source>/derived/<id>.json -> data/<source>
        source_rel = str(source_dir.relative_to(ROOT))
        # FINTRAC (Canadian Crown copyright) carries the {title, url} attribution; US-federal
        # public-domain docs carry none — mirrors the corpus footer rule.
        is_fintrac = source_dir.name.startswith("fintrac")
        attribution = None
        if is_fintrac:
            m = manifest_entry(source_dir, doc_id)
            if not (m.get("title") and m.get("url")):
                die(f"{doc_id}: FINTRAC doc missing title/url in its manifest")
            attribution = {"title": m["title"], "url": m["url"]}
        for a, b in zip(pre_inds, post_inds):
            if a.get("id") != b.get("id"):
                die(f"{doc_id}: indicator id drift pre {a.get('id')!r} vs current {b.get('id')!r}")
            # The commit pins flag/red_flag byte-identical across the correction — re-verify, so a
            # case's quoted flag is guaranteed to ground against the CURRENT committed record.
            if a.get("flag") != b.get("flag") or a.get("red_flag") != b.get("red_flag"):
                die(f"{doc_id}/{b.get('id')}: flag/red_flag NOT byte-identical pre vs current")
            c_changed = a.get("capability") != b.get("capability")
            d_changed = a.get("data_source") != b.get("data_source")
            if not (c_changed or d_changed):
                continue
            cases.append({
                "id": f"{doc_id}/{b['id']}",
                "doc_id": doc_id,
                "indicator_id": b["id"],
                "source_dir": source_rel,
                "flag": b["flag"],
                "red_flag": b["red_flag"],
                "rater_a": rater(a["capability"], a["data_source"], cap_names, src_names, "rater_a", doc_id),
                "rater_b": rater(b["capability"], b["data_source"], cap_names, src_names, "rater_b", doc_id),
                "changed": "both" if (c_changed and d_changed) else ("C" if c_changed else "D"),
                "attribution": attribution,
            })
    if not cases:
        die("no divergence cases found — wrong commit?")
    cases.sort(key=lambda c: (c["doc_id"], int(c["indicator_id"].split("-")[-1])))
    split = {"C": 0, "D": 0, "both": 0}
    for c in cases:
        split[c["changed"]] += 1
    doc = {
        "_note": ("Gate-console adjudication dataset (Phase 47) — REAL rater-A (pre-correction) vs "
                  "rater-B (post-correction) C/D-tag divergence cases from the Phase-34 verification "
                  "commit. Every field is copied from committed data or the git pre-image; nothing "
                  "synthesized; flags ground verbatim in the CURRENT committed derived records. "
                  "Regenerate: python3 scripts/curate_console_cases.py (authoring-time only — "
                  "validation never reads git). FINTRAC-sourced cases reproduce Crown-copyright "
                  "indicator text for non-commercial use with attribution per FINTRAC's Terms & "
                  "Conditions; US-federal cases are public domain (17 U.S.C. 105)."),
        "correction_commit": CORRECTION_COMMIT,
        "cases": cases,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"curate_console_cases: wrote {OUT.relative_to(ROOT)} — {len(cases)} cases "
          f"(C-only {split['C']} / D-only {split['D']} / both {split['both']})")


if __name__ == "__main__":
    main()
