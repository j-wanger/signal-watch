#!/usr/bin/env python3
"""Convert one acquired FinCEN advisory PDF → markdown — AUTHORING-TIME ONLY.

Part of the Signal Watch ingestion pipeline (Phase 7 walking skeleton):
    acquire_fincen.py  → data/fincen/raw/<id>.pdf
    pdf_to_md.py       → data/fincen/<id>.md   (verbatim source of truth)
    (hand-derive)      → config/typologies/<typology>.json
    build.py           → dist/<typology>/index.html  (inlined, offline)

The markdown is the SOURCE OF TRUTH for the verbatim advisory text. FinCEN
advisories are U.S. federal works in the public domain (17 U.S.C. §105), so the
full text is persisted and later shown verbatim (attributed) in Act 1.

DEPENDENCY ISOLATION: this needs `markitdown` (MIT). It is NOT a runtime/ship
dependency — the engine never imports it and `build.py` stays stdlib-only.
Install + run it in the gitignored authoring venv (the homebrew python 3.14 on
this machine has a broken pyexpat, so we use a uv-managed interpreter):

    uv venv .venv --python 3.12
    uv pip install --python .venv "markitdown[pdf]"     # see requirements-authoring.txt
    .venv/bin/python scripts/pdf_to_md.py fin-2022-a002

Phase 20 — multi-source: `--source <dir>` converts from another FinCEN publication source
(e.g. data/fincen-alerts/); the raw/ + <id>.md live under that dir. Default: data/fincen.

Usage:
    .venv/bin/python scripts/pdf_to_md.py <advisory-id>                     # e.g. fin-2022-a002
    .venv/bin/python scripts/pdf_to_md.py --source data/fincen-alerts <id> # convert an alert
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE = ROOT / "data" / "fincen"


def convert(advisory_id: str, source_dir: Path) -> Path:
    pdf = source_dir / "raw" / f"{advisory_id}.pdf"
    if not pdf.exists():
        sys.exit(f"missing {pdf} — run acquire_fincen.py {advisory_id} first")
    try:
        from markitdown import MarkItDown
    except ImportError:
        sys.exit(
            "markitdown not importable. This is an AUTHORING tool — run it in the "
            "uv venv:\n    .venv/bin/python scripts/pdf_to_md.py " + advisory_id
        )
    result = MarkItDown().convert(str(pdf))
    text = getattr(result, "markdown", None) or result.text_content
    out = source_dir / f"{advisory_id}.md"
    # Per-source issuer + publication noun + LICENCE basis for the provenance header. Phase 22 added the
    # FINTRAC branch ONLY: FINTRAC (Canadian Crown copyright) is reproduced verbatim under FINTRAC's
    # NON-COMMERCIAL reproduction terms WITH attribution — NOT public domain. The non-FINTRAC branch is
    # left EXACTLY as before (FinCEN/OFAC = US-federal public domain, 17 U.S.C. 105), so every committed
    # FinCEN + OFAC md reproduces byte-identically (those sources are frozen).
    name = source_dir.name.lower()
    if "fintrac" in name:
        issuer, kind = "FINTRAC", "operational alert"
        licence = ("Crown copyright (© His Majesty the King in Right of Canada); reproduced for "
                   "non-commercial use with attribution per FINTRAC's Terms & Conditions — NOT public domain")
        # Provenance header so the corpus file self-documents its source + reproduction basis.
        header = (
            f"<!-- source-of-truth: verbatim text of {issuer} {kind} {advisory_id.upper()} -->\n"
            f"<!-- acquired via scripts/acquire_fincen.py; {licence} -->\n"
            f"<!-- converted via markitdown (authoring-only); do not hand-edit the body -->\n\n"
        )
    else:
        # the FinCEN publication noun for the provenance header (advisories vs alerts)
        kind = "alert" if "alert" in name else "advisory"
        # Provenance header so the corpus file self-documents its source + public-domain status.
        header = (
            f"<!-- source-of-truth: verbatim text of FinCEN {kind} {advisory_id.upper()} -->\n"
            f"<!-- acquired via scripts/acquire_fincen.py; public domain, 17 U.S.C. 105 -->\n"
            f"<!-- converted via markitdown (authoring-only); do not hand-edit the body -->\n\n"
        )
    out.write_text(header + text.strip() + "\n", encoding="utf-8")
    print(f"wrote {out} ({len(text):,} chars)")
    return out


def _source_arg(argv) -> tuple:
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
    convert(argv[0], source_dir)


if __name__ == "__main__":
    main(sys.argv[1:])
