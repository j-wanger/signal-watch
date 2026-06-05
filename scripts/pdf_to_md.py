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

Usage:
    .venv/bin/python scripts/pdf_to_md.py <advisory-id>   # e.g. fin-2022-a002
"""
import sys
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "fincen"
RAW_DIR = DATA_DIR / "raw"


def convert(advisory_id: str) -> Path:
    pdf = RAW_DIR / f"{advisory_id}.pdf"
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
    out = DATA_DIR / f"{advisory_id}.md"
    # Provenance header so the corpus file self-documents its source + public-domain status.
    header = (
        f"<!-- source-of-truth: verbatim text of FinCEN advisory {advisory_id.upper()} -->\n"
        f"<!-- acquired via scripts/acquire_fincen.py; public domain, 17 U.S.C. 105 -->\n"
        f"<!-- converted via markitdown (authoring-only); do not hand-edit the body -->\n\n"
    )
    out.write_text(header + text.strip() + "\n", encoding="utf-8")
    print(f"wrote {out} ({len(text):,} chars)")
    return out


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return
    convert(argv[0])


if __name__ == "__main__":
    main(sys.argv[1:])
