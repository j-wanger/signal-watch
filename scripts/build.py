#!/usr/bin/env python3
"""Inline a typology config into index.html -> dist/index.html.

The ship target is a single self-contained file that runs from file:// — no server,
no fetch, no ES modules. This build only injects the chosen typology config at the
`__CONFIG__` placeholder; the engine and styles already live in index.html.

Usage:
    python3 scripts/build.py [typology_id]    # default: fentanyl

Stdlib only. Exits non-zero on a missing or invalid config (fail loud, never ship a
broken file).
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "index.html"
PLACEHOLDER = "__CONFIG__"
DEFAULT_TYPOLOGY = "fentanyl"


def die(msg: str, code: int = 1) -> None:
    print(f"build: error: {msg}", file=sys.stderr)
    raise SystemExit(code)


def main() -> None:
    typ = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_TYPOLOGY
    cfg_path = ROOT / "config" / "typologies" / f"{typ}.json"

    if not TEMPLATE.exists():
        die(f"template not found: {TEMPLATE}")
    if not cfg_path.exists():
        die(f"config not found: {cfg_path} (have you authored config/typologies/{typ}.json?)")

    try:
        data = json.loads(cfg_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        die(f"invalid JSON in {cfg_path.name}: {e}")

    template = TEMPLATE.read_text(encoding="utf-8")
    n = template.count(PLACEHOLDER)
    if n != 1:
        die(f"expected exactly one {PLACEHOLDER} placeholder in index.html, found {n}")

    # JSON is a subset of JS object-literal syntax, so the raw value inlines directly.
    # str.replace is literal (no regex/backreference surprises).
    config_js = json.dumps(data, ensure_ascii=False, indent=2)
    out = template.replace(PLACEHOLDER, config_js)

    # The ship file must be self-contained and file://-safe.
    if PLACEHOLDER in out:
        die("placeholder survived substitution")
    if "fetch(" in out or "<script src" in out or 'type="module"' in out:
        die("ship file is not self-contained (fetch / external script / ES module present)")

    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    out_path = dist / "index.html"
    out_path.write_text(out, encoding="utf-8")

    print(f"build: {typ} -> {out_path.relative_to(ROOT)}  "
          f"({len(out):,} bytes; config {len(config_js):,} chars)")


if __name__ == "__main__":
    main()
