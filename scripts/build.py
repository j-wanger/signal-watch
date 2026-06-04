#!/usr/bin/env python3
"""Validate a typology config and inline it into index.html -> dist/<id>/index.html.

The ship target is a single self-contained file per typology that runs from file:// —
no server, no fetch, no ES modules. This build (a) validates the config against the
schema at the boundary and fails loud, then (b) injects it at the `__CONFIG__`
placeholder; the engine and styles already live in index.html.

Usage:
    python3 scripts/build.py [typology_id]   # default: fentanyl
    python3 scripts/build.py all             # build every config/typologies/*.json

Stdlib only. Exits non-zero on a missing or schema-invalid config.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "index.html"
TYPOLOGY_DIR = ROOT / "config" / "typologies"
PLACEHOLDER = "__CONFIG__"
DEFAULT_TYPOLOGY = "fentanyl"

STATUS = {"covered", "partial", "gap"}
CAND_TYPE = {"entity", "relationship", "motif"}
DATA = {"available", "partial", "insufficient"}
STRENGTH = {"weak", "mid", "strong"}
DEF_KEYS = {"signal_name", "class", "features", "logic", "window", "source", "route"}
ANCHOR_REQ = {"hook_title", "hook_lead", "close_title", "close_delta", "lift_rationale", "source", "coverage_noun"}


def die(msg: str, code: int = 1) -> None:
    print(f"build: error: {msg}", file=sys.stderr)
    raise SystemExit(code)


def validate_config(c: dict) -> list:
    """Deterministic schema check at the build boundary. Returns a list of error strings."""
    e = []
    if not isinstance(c, dict):
        return ["config is not a JSON object"]

    for k in ("id", "label", "steps", "next_labels", "hints", "anchor", "coverage",
              "advisory_stream", "candidates", "lift", "stats"):
        if k not in c:
            e.append(f"missing top-level field: {k}")

    def arr(name, n=None):
        v = c.get(name)
        if not isinstance(v, list):
            e.append(f"{name} must be an array")
            return None
        if n is not None and len(v) != n:
            e.append(f"{name} must have {n} entries (has {len(v)})")
        return v

    steps = arr("steps")
    if steps is not None and len(steps) != 7:
        e.append(f"steps must have exactly 7 entries, one per act (has {len(steps)})")
    nl = arr("next_labels")
    if nl is not None and len(nl) < 7:
        e.append(f"next_labels must have >= 7 entries (has {len(nl)})")
    h = arr("hints")
    if h is not None and len(h) < 7:
        e.append(f"hints must have >= 7 entries (has {len(h)})")

    anchor = c.get("anchor")
    if isinstance(anchor, dict):
        for k in ANCHOR_REQ:
            if not anchor.get(k):
                e.append(f"anchor.{k} is required")
    else:
        e.append("anchor must be an object")

    cov = c.get("coverage")
    inds = cov.get("indicators") if isinstance(cov, dict) else None
    if not isinstance(inds, list) or not inds:
        e.append("coverage.indicators must be a non-empty array")
    else:
        targets = 0
        for i, x in enumerate(inds):
            if not isinstance(x, dict) or not x.get("id") or not x.get("label"):
                e.append(f"coverage.indicators[{i}] needs id + label")
                continue
            if x.get("status") not in STATUS:
                e.append(f"coverage.indicators[{i}].status invalid: {x.get('status')}")
            if x.get("target"):
                targets += 1
        if targets != 1:
            e.append(f"exactly one indicator must have target:true (found {targets})")

    adv = arr("advisory_stream")
    if adv is not None:
        for i, s in enumerate(adv):
            if not isinstance(s, dict) or "t" not in s:
                e.append(f"advisory_stream[{i}] needs a 't' field")

    cands = c.get("candidates")
    if not isinstance(cands, list) or not cands:
        e.append("candidates must be a non-empty array")
    else:
        targets = []
        for i, x in enumerate(cands):
            if not isinstance(x, dict):
                e.append(f"candidates[{i}] must be an object")
                continue
            if not x.get("id") or not x.get("name"):
                e.append(f"candidates[{i}] needs id + name")
            if x.get("type") not in CAND_TYPE:
                e.append(f"candidates[{i}].type invalid: {x.get('type')}")
            if x.get("cover") not in STATUS:
                e.append(f"candidates[{i}].cover invalid: {x.get('cover')}")
            if x.get("data") not in DATA:
                e.append(f"candidates[{i}].data invalid: {x.get('data')}")
            if x.get("target"):
                targets.append(x)
        if len(targets) != 1:
            e.append(f"exactly one candidate must have target:true (found {len(targets)})")
        else:
            t = targets[0]
            if t.get("cover") != "gap" or t.get("data") != "available":
                e.append("target candidate must be buildable (cover:gap + data:available)")
            d = t.get("definition")
            if not isinstance(d, dict):
                e.append("target candidate must have a definition object")
            else:
                missing = DEF_KEYS - set(d)
                if missing:
                    e.append(f"target definition missing keys: {sorted(missing)}")
                if not isinstance(d.get("features"), list) or not d.get("features"):
                    e.append("target definition.features must be a non-empty array")

    lift = c.get("lift")
    if not isinstance(lift, list) or not lift:
        e.append("lift must be a non-empty array")
    else:
        for i, l in enumerate(lift):
            if not isinstance(l, dict):
                e.append(f"lift[{i}] must be an object")
                continue
            if not l.get("name") or "combo" not in l:
                e.append(f"lift[{i}] needs name + combo")
            if not isinstance(l.get("value"), (int, float)) or not (0 <= l.get("value", -1) <= 100):
                e.append(f"lift[{i}].value must be a number 0-100")
            if l.get("strength") not in STRENGTH:
                e.append(f"lift[{i}].strength invalid: {l.get('strength')}")

    stats = c.get("stats")
    if isinstance(stats, dict):
        for k in ("fire_count", "standalone_precision", "best_combo_precision"):
            if not isinstance(stats.get(k), (int, float)):
                e.append(f"stats.{k} must be a number")
    else:
        e.append("stats must be an object")

    return e


def build_one(typ: str, template: str) -> None:
    cfg_path = TYPOLOGY_DIR / f"{typ}.json"
    if not cfg_path.exists():
        die(f"config not found: {cfg_path} (have you authored config/typologies/{typ}.json?)")

    try:
        data = json.loads(cfg_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as ex:
        die(f"invalid JSON in {cfg_path.name}: {ex}")

    errors = validate_config(data)
    if errors:
        die(f"{cfg_path.name} fails schema validation:\n  - " + "\n  - ".join(errors))

    n = template.count(PLACEHOLDER)
    if n != 1:
        die(f"expected exactly one {PLACEHOLDER} placeholder in index.html, found {n}")

    config_js = json.dumps(data, ensure_ascii=False, indent=2)
    out = template.replace(PLACEHOLDER, config_js)  # str.replace is literal

    if PLACEHOLDER in out:
        die("placeholder survived substitution")
    if "fetch(" in out or "<script src" in out or 'type="module"' in out:
        die("ship file is not self-contained (fetch / external script / ES module present)")

    out_dir = ROOT / "dist" / typ
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "index.html"
    out_path.write_text(out, encoding="utf-8")
    print(f"build: {typ} -> {out_path.relative_to(ROOT)}  "
          f"({len(out):,} bytes; config {len(config_js):,} chars)")


def main() -> None:
    if not TEMPLATE.exists():
        die(f"template not found: {TEMPLATE}")
    template = TEMPLATE.read_text(encoding="utf-8")

    arg = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_TYPOLOGY
    if arg == "all":
        configs = sorted(TYPOLOGY_DIR.glob("*.json"))
        if not configs:
            die("no typology configs found under config/typologies/")
        for p in configs:
            build_one(p.stem, template)
    else:
        build_one(arg, template)

    # one-time migration: remove the old single-file M1 layout if present
    stale = ROOT / "dist" / "index.html"
    if stale.exists():
        stale.unlink()
        print(f"build: removed stale {stale.relative_to(ROOT)} (now per-typology dist/<id>/)")


if __name__ == "__main__":
    main()
