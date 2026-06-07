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

CORPUS SOURCE (Phase 10): the set of acquirable advisories comes from the generated manifest
<source>/index.json (built by crawl_fincen.py). For ADVISORIES the manifest holds each advisory's
DETAIL-PAGE url — FinCEN PDF filenames are unpredictable — so we resolve the PDF link from the
detail page at fetch time. A manifest url that already ENDS IN .pdf is taken as a direct (zero-hop)
download — this is how FinCEN ALERTS resolve (Phase 20: their hub links the PDF directly), and how
the DIRECT-PDF overrides below short-circuit the hop for known-good anchors (the Phase-7 EFE advisory).

Phase 20 — multi-source: `--source <dir>` targets another FinCEN publication source
(e.g. data/fincen-alerts/); the manifest + raw/ live under that dir. Default: data/fincen.

Usage:
    python3 scripts/acquire_fincen.py fin-2022-a002                       # acquire one advisory
    python3 scripts/acquire_fincen.py --source data/fincen-alerts <id>    # acquire one alert
    python3 scripts/acquire_fincen.py [--source <dir>] --list            # show the manifest corpus
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE = ROOT / "data" / "fincen"   # Phase 20: --source <dir> targets another FinCEN source
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


def load_manifest(source_dir: Path) -> dict:
    """document id -> url, from <source>/index.json (empty if absent).

    For advisories the url is a detail page; for alerts it is a direct .pdf (Phase 20).
    """
    manifest = source_dir / "index.json"
    if not manifest.exists():
        return {}
    return {e["id"]: e["url"] for e in json.loads(manifest.read_text(encoding="utf-8"))}


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


def _to_pdf_url(manifest_url: str) -> str:
    """A manifest url that is already a direct PDF download is fetched as-is; otherwise it is a detail
    page whose PDF link we resolve. Direct = ends in .pdf (FinCEN alerts + the EFE override) OR is an
    absolute agency media/file URL that serves a PDF body — /media/<id>/download (Phase 21: OFAC) or
    /system/files/… . Relative paths are made absolute against BASE."""
    url = manifest_url
    low = url.lower().split("?")[0]
    direct = low.endswith(".pdf") or (url.startswith("http") and ("/media/" in low or "/system/files/" in low))
    if direct:
        return url if url.startswith("http") else BASE + url
    return resolve_pdf(url)


def acquire(advisory_id: str, source_dir: Path) -> Path:
    manifest = load_manifest(source_dir)
    if advisory_id in DIRECT_PDF:
        url = DIRECT_PDF[advisory_id]                 # zero-hop override
    elif advisory_id in manifest:
        url = _to_pdf_url(manifest[advisory_id])      # direct .pdf, else detail-page -> PDF hop
    else:
        known = ", ".join(sorted(set(DIRECT_PDF) | set(manifest))) or "(none — run crawl_fincen.py --write)"
        sys.exit(f"unknown id '{advisory_id}'. Known: {known}")
    raw_dir = source_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    out = raw_dir / f"{advisory_id}.pdf"
    print(f"fetching {url}\n     -> {out}")
    data = _get(url)
    if not data.startswith(b"%PDF"):
        sys.exit(f"refusing to write: response is not a PDF (first bytes: {data[:16]!r})")
    out.write_bytes(data)
    print(f"ok: {len(data):,} bytes")
    return out


def _source_arg(argv) -> tuple:
    """Pull an optional `--source <dir>` (relative to ROOT or absolute); return (source_dir, rest)."""
    if "--source" in argv:
        i = argv.index("--source")
        if i + 1 >= len(argv):
            sys.exit("usage: --source <dir>")
        d = Path(argv[i + 1])
        if not d.is_absolute():
            d = ROOT / d
        return d, argv[:i] + argv[i + 2:]
    return DEFAULT_SOURCE, argv


def main(argv):
    source_dir, argv = _source_arg(argv)
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return
    if argv[0] == "--list":
        manifest = load_manifest(source_dir)
        if not manifest:
            print(f"no manifest under {source_dir.relative_to(ROOT)} — run crawl_fincen.py")
            return
        for k in sorted(manifest):
            tag = " [direct-pdf]" if k in DIRECT_PDF or manifest[k].lower().endswith(".pdf") else ""
            print(f"{k}\t{manifest[k]}{tag}")
        return
    acquire(argv[0], source_dir)


if __name__ == "__main__":
    main(sys.argv[1:])
