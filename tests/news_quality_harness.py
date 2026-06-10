#!/usr/bin/env python3
"""Phase 44 — committed extraction-quality harness (deterministic, NO model).

Replays every pinned capture (tests/fixtures/news-live/<id>[.tag].qwen.json + its article) through
serve_news.build_record — the same seam the replay test uses — and scores the result on the
quality dimensions Phase 40/44 measure, plus the 4 committed news records (data/news/derived/).

Dimensions (direction in brackets — how --check compares against the baseline):
  kept_flags        [>=]  red flags surviving the gate (never-reduce — the Phase-41 lesson)
  mech_families     [>=]  distinct mechanism-registry families covered by kept flags
  entity_count      [==]  entities surviving the gate (exact pin; a conscious change re-freezes)
  alias_suspects    [<=]  deterministic alias-OWNERSHIP suspicion (the dimension nothing measured
                          before Phase 44 — the gate checks an alias is verbatim, never WHOSE it is):
                            multi-parent: alias token-set ⊂ 2+ kept entity names (ambiguous owner)
                            cross-subset: alias ⊂ a DIFFERENT entity's name but NOT its parent's
  type_blind_folds  [<=]  fold audit rows where the folded entity's type ≠ its parent's type

Modes:
  report (default)           print the per-fixture table + aggregates
  --check                    exit non-zero if any dimension regresses vs the committed baseline
                             (tests/fixtures/news-live/quality-baseline.json) or a fixture is missing
  --freeze                   write the current metrics as the new baseline (a CONSCIOUS act — do it
                             only when a quality change is measured and accepted)
  --live-profile <runs.json> additionally report wall-time stages from a local live-run capture
                             (report-only; wall-time is never gated — no model runs here)

Stdlib-only; runs offline. The baseline file is committed; local/private material never enters
this harness (committed/fixture material only — the privacy boundary).
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent
FIXDIR = HERE / "fixtures" / "news-live"
BASELINE = FIXDIR / "quality-baseline.json"
DERIVED = ROOT / "data" / "news" / "derived"
ARTICLES = ROOT / "data" / "news" / "articles"

sys.path.insert(0, str(ROOT / "scripts"))
import news_ground  # noqa: E402
import serve_news  # noqa: E402

# mechanism-family registry (Phase 40, promoted from .dev-wiki/tmp/ph40/analyze.py — the committed
# home; keyword map applied to category + red_flag + flag text, first family wins)
FAMILIES = {
    "structuring": ["structur", "threshold", "smurf", "below reporting", "small-denomination", "small denomination"],
    "rapid-movement": ["rapid", "layer", "circular", "flow-through", "flow through", "no economic purpose", "pass-through"],
    "shell-front": ["shell", "front compan", "front business", "nominee", "opaque owner", "straw", "beneficial owner"],
    "gatekeeper": ["attorney", "lawyer", "trust account", "gatekeeper", "corporate service", "law firm", "law-firm", "professional"],
    "bulk-cash": ["bulk cash", "bulk-cash", "courier", "cash pickup", "cash handover", "cash placement", "cash deposit"],
    "commingling": ["commingl", "mixing cash", "legitimate revenue", "legitimate cash"],
    "virtual-asset": ["crypto", "stablecoin", "usdt", "mixer", "mixing service", "chain-hopping", "virtual asset", "virtual-asset", "wallet"],
    "mule-funnel": ["mule", "funnel", "romance", "third-party account"],
    "tbml": ["trade-based", "invoice", "tbml", "shipping record", "trade transaction"],
    "sanctions": ["sanction", "designated", "blocked person", "ofac", "garantex", "circumvent"],
    "export-control": ["export control", "export-control", "dual-use", "dual use", "transship", "end-user", "end user", "procurement"],
    "high-risk-jurisdiction": ["high-risk jurisdiction", "non-resident", "nonresident", "offshore", "secrecy jurisdiction", "high-risk countr"],
    "asset-laundering": ["casino", "real estate", "real-estate", "luxury", "chip", "property", "artifact", "antiquit", "art market"],
    "fraud-proceeds": ["fraud", "scam", "victim", "ponzi", "pig butchering", "embezzl", "stolen"],
    "unregistered": ["unregistered", "unlicensed", "without a license", "msb registration", "licensure"],
    "cyber": ["cyber", "phish", "hack", "credential", "swift", "intrusion", "account takeover", "payment instruction"],
    "concealment": ["conceal", "encrypted", "fake identit", "false identit", "counterfeit", "destruction", "destroy", "evasion of detection", "detection", "record-keeping", "disguise", "obfusc", "weekend", "timing", "moniker", "alias"],
    "institutional-failure": ["willful blind", "wilful blind", "monitoring gap", "paper-only", "paper only", "profit over", "profit-over", "control failure", "compliance failure", "due diligence failure", "due-diligence", "ignored", "warning", "oversight", "governance", "abandoned"],
    "misrepresentation": ["misrepresent", "false assurance", "false claim", "false statement", "withheld", "withhold", "false filing", "forged", "understat", "false authorization"],
    "corruption-pep": ["corrupt", "bribe", "pep", "politically exposed", "official"],
}

GATED = {  # dimension -> direction ('+' never-reduce, '-' never-grow, '=' exact)
    "kept_flags": "+", "mech_families": "+", "entity_count": "=",
    "alias_suspects": "-", "type_blind_folds": "-",
}


def fam_of(item):
    for text in ((item.get("category") or ""), (item.get("red_flag") or ""), (item.get("flag") or "")):
        t = str(text).lower()
        if not t:
            continue
        for fam, kws in FAMILIES.items():
            if any(k in t for k in kws):
                return fam
    return "unmapped"


def _toks(s):
    return set(re.findall(r"[a-z0-9]+", str(s).lower()))


def alias_suspects(record, fold_audit=()):
    """Deterministic alias-OWNERSHIP suspicion over a final record. Returns (count, details)."""
    ents = record.get("entities") or []
    namesets = [(e.get("name") or "", _toks(e.get("name") or "")) for e in ents]
    out = []
    for e in ents:
        own = _toks(e.get("name") or "")
        for a in (e.get("aliases") or []):
            at = _toks(a)
            if not at:
                continue
            supersets = [nm for nm, ts in namesets if at < ts]
            if len(supersets) >= 2:
                out.append({"alias": a, "on": e.get("name"), "why": f"ambiguous owner — subset of {len(supersets)} entity names"})
            elif supersets and not at <= own:
                out.append({"alias": a, "on": e.get("name"), "why": f"subset of OTHER entity {supersets[0]!r}, not its own parent"})
    by_name = {(e.get("name") or ""): (e.get("type") or "") for e in ents}
    tbf = [d for d in fold_audit
           if d.get("folded_into") and d.get("_folded_type")
           and by_name.get(d["folded_into"]) and d["_folded_type"] != by_name[d["folded_into"]]]
    return out, tbf


def score_fixture(qwen_path):
    """Replay one pinned capture through build_record; return the metric row."""
    fid = qwen_path.name[: -len(".qwen.json")]
    base = fid.split(".")[0]
    art_p = FIXDIR / f"{base}.article.md"
    if not art_p.exists():
        art_p = ARTICLES / f"{base}.md"
    art = art_p.read_text(encoding="utf-8")
    raw_json = qwen_path.read_text(encoding="utf-8")
    raw = json.loads(raw_json)
    # type lookup for fold-type-blindness BEFORE the fold erases the folded entity
    pre_types = {(e.get("name") or "").strip(): (e.get("type") or "").strip().lower()
                 for e in (raw.get("entities") or [])}
    rec, dropped = serve_news.build_record(serve_news.parse_llm_json(raw_json), art,
                                           serve_news.FIXTURE_META.get(base) if hasattr(serve_news, "FIXTURE_META") else None)
    folds = [dict(d, _folded_type=pre_types.get(str(d.get("value", "")).strip(), ""))
             for d in dropped if d.get("folded_into")]
    susp, tbf = alias_suspects(rec, folds)
    kept = rec.get("red_flags") or []
    fams = {fam_of(f) for f in kept} - {"unmapped"}
    return fid, {
        "kept_flags": len(kept),
        "mech_families": len(fams),
        "entity_count": len(rec.get("entities") or []),
        "alias_suspects": len(susp),
        "type_blind_folds": len(tbf),
    }, {"suspects": susp, "type_blind_folds": [d.get("value") for d in tbf],
        "families": sorted(fams),
        "flag_drops": [d.get("reason") for d in dropped if d.get("kind") == "red_flag"]}


def score_committed(rec_path):
    """Score a committed derived record (already final — alias-ownership + registry only)."""
    rec = json.loads(rec_path.read_text(encoding="utf-8"))
    susp, _ = alias_suspects(rec)
    kept = rec.get("red_flags") or []
    fams = {fam_of(f) for f in kept} - {"unmapped"}
    return f"committed:{rec_path.stem}", {
        "kept_flags": len(kept),
        "mech_families": len(fams),
        "entity_count": len(rec.get("entities") or []),
        "alias_suspects": len(susp),
        "type_blind_folds": 0,
    }, {"suspects": susp, "families": sorted(fams)}


def collect():
    rows, details = {}, {}
    for p in sorted(FIXDIR.glob("*.qwen.json")):
        fid, m, det = score_fixture(p)
        rows[fid], details[fid] = m, det
    for p in sorted(DERIVED.glob("*.json")):
        fid, m, det = score_committed(p)
        rows[fid], details[fid] = m, det
    return rows, details


def main():
    args = sys.argv[1:]
    rows, details = collect()

    hdr = f"{'fixture':42s} {'flags':>5s} {'fams':>4s} {'ents':>4s} {'aSusp':>5s} {'tbf':>3s}"
    print(hdr)
    for fid, m in rows.items():
        print(f"{fid[:42]:42s} {m['kept_flags']:5d} {m['mech_families']:4d} {m['entity_count']:4d} "
              f"{m['alias_suspects']:5d} {m['type_blind_folds']:3d}")
        for s in details[fid].get("suspects", []):
            print(f"    suspect: {s['alias']!r} on {s['on']!r} — {s['why']}")
    tot = {k: sum(m[k] for m in rows.values()) for k in GATED}
    print(f"{'TOTAL':42s} {tot['kept_flags']:5d} {tot['mech_families']:4d} {tot['entity_count']:4d} "
          f"{tot['alias_suspects']:5d} {tot['type_blind_folds']:3d}")

    if "--live-profile" in args:
        runs_p = Path(args[args.index("--live-profile") + 1])
        for r in json.loads(runs_p.read_text()):
            print(f"  live {r.get('note', '?'):24s} wall={r.get('wall_s')}s grounded@{r.get('grounded_at_s')}s "
                  f"verify_share={r.get('verify_share')}")

    if "--freeze" in args:
        BASELINE.write_text(json.dumps(rows, indent=1, sort_keys=True) + "\n", encoding="utf-8")
        print(f"baseline frozen -> {BASELINE}")
        return 0

    if "--check" in args:
        if not BASELINE.exists():
            print("CHECK FAIL: no committed baseline (run --freeze consciously first)")
            return 1
        base = json.loads(BASELINE.read_text())
        fails = []
        for fid, bm in base.items():
            cm = rows.get(fid)
            if cm is None:
                fails.append(f"{fid}: fixture missing from current run")
                continue
            for dim, direction in GATED.items():
                b, c = bm.get(dim), cm.get(dim)
                bad = (direction == "+" and c < b) or (direction == "-" and c > b) or (direction == "=" and c != b)
                if bad:
                    fails.append(f"{fid}.{dim}: {b} -> {c} (direction {direction})")
        if fails:
            print("CHECK FAIL:")
            for f in fails:
                print(f"  {f}")
            return 1
        print(f"CHECK OK — {len(base)} fixtures, all dimensions within baseline")
    return 0


if __name__ == "__main__":
    sys.exit(main())
