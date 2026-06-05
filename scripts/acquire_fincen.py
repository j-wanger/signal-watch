#!/usr/bin/env python3
"""Acquire one FinCEN advisory PDF into data/fincen/raw/ — AUTHORING-TIME ONLY.

This is part of the Signal Watch ingestion pipeline (Phase 7 walking skeleton).
It runs at authoring time to seed the source-of-truth corpus; its output is
persisted to disk and later converted (pdf_to_md.py) + inlined by build.py.

NON-NEGOTIABLE: nothing here ever runs in the ship artifact. The engine
(index.html / dist/<id>/index.html) never fetches — it reads inlined config.
This script is not imported by the engine or the build; it is a developer tool.

FinCEN advisories are works of the U.S. federal government and are in the public
domain (17 U.S.C. §105), so the full text may be persisted and shown verbatim.

Usage:
    python3 scripts/acquire_fincen.py fin-2022-a002      # one advisory
    python3 scripts/acquire_fincen.py --list             # show the registry

The registry below is a deliberate single-fetch stub. Widening this into a
general FinCEN crawler (scan all advisories) is a LATER phase, out of scope here.
"""
import sys
import urllib.request
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "fincen" / "raw"

# advisory id -> canonical public-domain PDF URL on fincen.gov
REGISTRY = {
    "fin-2022-a002": (
        "https://www.fincen.gov/system/files/advisory/2022-06-15/"
        "FinCEN%20Advisory%20Elder%20Financial%20Exploitation%20FINAL%20508.pdf"
    ),
}

# fincen.gov returns 403 to the bare urllib UA; present a normal browser UA.
_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Signal-Watch-authoring/0.1"


def acquire(advisory_id: str) -> Path:
    if advisory_id not in REGISTRY:
        sys.exit(f"unknown advisory id '{advisory_id}'. Known: {', '.join(REGISTRY)}")
    url = REGISTRY[advisory_id]
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    out = RAW_DIR / f"{advisory_id}.pdf"
    print(f"fetching {url}\n     -> {out}")
    req = urllib.request.Request(url, headers={"User-Agent": _UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()
    if not data.startswith(b"%PDF"):
        sys.exit(f"refusing to write: response is not a PDF (first bytes: {data[:16]!r})")
    out.write_bytes(data)
    print(f"ok: {len(data):,} bytes")
    return out


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return
    if argv[0] == "--list":
        for k, v in REGISTRY.items():
            print(f"{k}\t{v}")
        return
    acquire(argv[0])


if __name__ == "__main__":
    main(sys.argv[1:])
