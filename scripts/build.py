#!/usr/bin/env python3
"""Validate a typology config and inline it into index.html -> dist/<id>/index.html.

The ship target is a single self-contained file per typology that runs from file:// —
no server, no fetch, no ES modules. This build (a) validates the config against the
schema at the boundary and fails loud, then (b) injects it at the `__CONFIG__`
placeholder; the engine and styles already live in index.html.

Usage:
    python3 scripts/build.py [typology_id]   # default: fentanyl
    python3 scripts/build.py all             # build every config/typologies/*.json
    python3 scripts/build.py --check [all|<id>]  # drift guard: committed dist == fresh build?

`--check` is non-mutating and git-agnostic: it re-renders each config in memory and
byte-compares against the committed dist/<id>/index.html, exiting non-zero (and naming the
typology) on any drift or a missing built artifact. Run it before committing or presenting.

Stdlib only. Exits non-zero on a missing or schema-invalid config, or (under --check) on drift.
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

    # advisory_full is OPTIONAL — a verbatim public-domain source document shown in Act 1.
    # Either inline `text`, or a `text_file` pointing at the markdown corpus (build resolves it).
    af = c.get("advisory_full")
    if af is not None:
        if not isinstance(af, dict):
            e.append("advisory_full must be an object")
        else:
            if not af.get("source"):
                e.append("advisory_full.source is required (verbatim attribution)")
            has_text = isinstance(af.get("text"), str) and af.get("text").strip()
            tf = af.get("text_file")
            if not has_text and not tf:
                e.append("advisory_full needs a non-empty `text` or a `text_file`")
            elif tf and not (ROOT / tf).exists():
                e.append(f"advisory_full.text_file not found: {tf}")

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


def render_one(typ: str, template: str) -> str:
    """Validate config + inline it into the template, returning the self-contained HTML.

    Pure: no disk write, no stdout. The single source of truth for what a typology's
    `dist/<id>/index.html` *should* contain — shared by `build_one` (writes it) and
    `check_one` (compares against the committed file). Fails loud (die) on a missing /
    invalid config or a non-self-contained result.
    """
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

    # Resolve a verbatim advisory_full.text_file reference into inlined text. The markdown
    # corpus (data/fincen/<id>.md) stays the single source of truth; the build bakes its
    # body into the offline single-file artifact (no runtime fetch). Strips the leading
    # HTML-comment provenance header so only the advisory body is shown.
    af = data.get("advisory_full")
    if isinstance(af, dict) and af.get("text_file") and not af.get("text"):
        lines = (ROOT / af["text_file"]).read_text(encoding="utf-8").splitlines()
        while lines and (lines[0].lstrip().startswith("<!--") or not lines[0].strip()):
            lines.pop(0)
        af["text"] = "\n".join(lines).strip()
        af.pop("text_file", None)

    n = template.count(PLACEHOLDER)
    if n != 1:
        die(f"expected exactly one {PLACEHOLDER} placeholder in index.html, found {n}")

    config_js = json.dumps(data, ensure_ascii=False, indent=2)
    out = template.replace(PLACEHOLDER, config_js)  # str.replace is literal

    if PLACEHOLDER in out:
        die("placeholder survived substitution")
    if "fetch(" in out or "<script src" in out or 'type="module"' in out:
        die("ship file is not self-contained (fetch / external script / ES module present)")

    return out


def build_one(typ: str, template: str) -> None:
    out = render_one(typ, template)
    out_dir = ROOT / "dist" / typ
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "index.html"
    out_path.write_text(out, encoding="utf-8")
    print(f"build: {typ} -> {out_path.relative_to(ROOT)}  ({len(out):,} bytes)")


def check_one(typ: str, template: str) -> bool:
    """Drift guard: does the committed dist/<typ>/index.html still equal a fresh render?

    Non-mutating and git-agnostic (byte-compares in process). Returns True if the
    committed artifact matches, False on drift / a missing build / a config that no
    longer renders. Prints a per-typology verdict.
    """
    out_path = ROOT / "dist" / typ / "index.html"
    rel = out_path.relative_to(ROOT)
    try:
        fresh = render_one(typ, template)
    except SystemExit:
        # render_one already printed the underlying error via die()
        print(f"check: {typ} -> FAIL (config no longer renders; cannot reproduce {rel})", file=sys.stderr)
        return False
    if not out_path.exists():
        print(f"check: {typ} -> DRIFT (missing built artifact {rel}; run `build.py {typ}`)", file=sys.stderr)
        return False
    if out_path.read_text(encoding="utf-8") != fresh:
        print(f"check: {typ} -> DRIFT ({rel} differs from a fresh build of {typ}.json; "
              f"run `build.py {typ}` and commit)", file=sys.stderr)
        return False
    print(f"check: {typ} -> ok ({rel} matches a fresh build)")
    return True


def resolve_targets(target: str) -> list:
    """A single id, or every config/typologies/*.json for 'all' (sorted, stable)."""
    if target == "all":
        configs = sorted(TYPOLOGY_DIR.glob("*.json"))
        if not configs:
            die("no typology configs found under config/typologies/")
        return [p.stem for p in configs]
    return [target]


def main() -> None:
    if not TEMPLATE.exists():
        die(f"template not found: {TEMPLATE}")
    template = TEMPLATE.read_text(encoding="utf-8")

    args = sys.argv[1:]
    check = "--check" in args
    positional = [a for a in args if not a.startswith("-")]
    target = positional[0] if positional else DEFAULT_TYPOLOGY

    if check:
        # Non-mutating drift guard: committed dist == fresh build? Touches nothing on disk.
        results = [check_one(t, template) for t in resolve_targets(target)]
        drifted = results.count(False)
        if drifted:
            die(f"build-drift check FAILED: {drifted}/{len(results)} "
                f"{'typology' if len(results) == 1 else 'typologies'} drifted "
                f"(committed dist != fresh build). Rebuild with `python3 scripts/build.py all` "
                f"and commit the dist.")
        print(f"check: OK — all {len(results)} built artifact(s) match a fresh build (zero drift)")
        return

    for t in resolve_targets(target):
        build_one(t, template)

    # one-time migration: remove the old single-file M1 layout if present
    stale = ROOT / "dist" / "index.html"
    if stale.exists():
        stale.unlink()
        print(f"build: removed stale {stale.relative_to(ROOT)} (now per-typology dist/<id>/)")


if __name__ == "__main__":
    main()
