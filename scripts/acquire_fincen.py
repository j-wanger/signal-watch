#!/usr/bin/env python3
"""Acquire a FinCEN advisory PDF into data/fincen/raw/ — AUTHORING-TIME ONLY.

This is part of the Signal Watch ingestion pipeline. It runs at authoring time to
seed the source-of-truth corpus; its output is persisted to disk and later converted
(pdf_to_md.py) + inlined by build.py.

NON-NEGOTIABLE: nothing here ever runs in the ship artifact. The engine
(index.html / dist/<id>/index.html) never fetches — it reads inlined config.
This script is not imported by the engine or the build; it is a developer tool.

FinCEN advisories are works of the U.S. federal government and are in the public
domain (17 U.S.C. §105), so the full text may be persisted and shown verbatim.

CORPUS SOURCE (Phase 10): the set of acquirable advisories now comes from the
generated manifest data/fincen/index.json (built by crawl_fincen.py from the FinCEN
advisories listing). The manifest holds each advisory's DETAIL-PAGE url — FinCEN PDF
filenames are unpredictable — so for a manifest id we resolve the PDF link from the
detail page at fetch time. A small set of DIRECT-PDF overrides (below) short-circuits
that hop for known-good anchors (the Phase-7 EFE advisory), keeping them zero-hop and
backward-compatible even if the listing markup shifts.

Usage:
    python3 scripts/acquire_fincen.py fin-2022-a002      # acquire one advisory
    python3 scripts/acquire_fincen.py --list             # show the manifest corpus
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "fincen" / "raw"
MANIFEST = ROOT / "data" / "fincen" / "index.json"
BASE = "https://www.fincen.gov"

# Direct-PDF overrides: advisory id -> canonical public-domain PDF URL on fincen.gov.
# These short-circuit the detail-page resolution hop for known-good anchors and
# guarantee backward-compatibility (the Phase-7 EFE slice) regardless of the manifest.
DIRECT_PDF = {
    "fin-2022-a002": (
        "https://www.fincen.gov/system/files/advisory/2022-06-15/"
        "FinCEN%20Advisory%20Elder%20Financial%20Exploitation%20FINAL%20508.pdf"
    ),
}

# fincen.gov returns 403 to the bare urllib UA; present a normal browser UA.
_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Signal-Watch-authoring/0.1"
_PDF_LINK_RE = re.compile(r'href="(/system/files/[^"]+?\.pdf)"', re.I)


def _get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": _UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def load_manifest() -> dict:
    """advisory id -> detail-page url, from data/fincen/index.json (empty if absent)."""
    if not MANIFEST.exists():
        return {}
    return {e["id"]: e["url"] for e in json.loads(MANIFEST.read_text(encoding="utf-8"))}


def resolve_pdf(detail_url: str) -> str:
    """Fetch an advisory detail page and return the absolute URL of its advisory PDF.

    FinCEN detail pages link the PDF under /system/files/...; prefer a link whose path
    looks like the advisory, else take the first PDF link.
    """
    html = _get(detail_url).decode("utf-8", "replace")
    links = _PDF_LINK_RE.findall(html)
    if not links:
        sys.exit(f"no /system/files/*.pdf link found on {detail_url}")
    preferred = [l for l in links if "advisor" in l.lower()] or links
    return BASE + preferred[0]


def acquire(advisory_id: str) -> Path:
    manifest = load_manifest()
    if advisory_id in DIRECT_PDF:
        url = DIRECT_PDF[advisory_id]                 # zero-hop override
    elif advisory_id in manifest:
        url = resolve_pdf(manifest[advisory_id])      # detail-page -> PDF hop
    else:
        known = ", ".join(sorted(set(DIRECT_PDF) | set(manifest))) or "(none — run crawl_fincen.py --write)"
        sys.exit(f"unknown advisory id '{advisory_id}'. Known: {known}")
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    out = RAW_DIR / f"{advisory_id}.pdf"
    print(f"fetching {url}\n     -> {out}")
    data = _get(url)
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
        manifest = load_manifest()
        if not manifest:
            print("no manifest — run: python3 scripts/crawl_fincen.py --write")
            return
        for k in sorted(manifest):
            tag = " [direct-pdf]" if k in DIRECT_PDF else ""
            print(f"{k}\t{manifest[k]}{tag}")
        return
    acquire(argv[0])


if __name__ == "__main__":
    main(sys.argv[1:])
