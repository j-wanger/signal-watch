#!/usr/bin/env python3
"""Shared grounding primitives for the M8 news stream (stdlib only).

The SAME normalize + quote-grounding rule used at the build boundary (build.py validate_news_data,
which imports these) and at runtime by the live companion (serve_news.py). Build mode REPORTS errors;
live mode (ground_record) DROPS ungrounded items. Sharing the primitives makes live grounding ==
build grounding BY CONSTRUCTION.

This is pure string grounding (normalize + the article-body transform) — NOT the authoring/LLM layer:
build.py importing it does not violate "build.py never imports the authoring layer" (no derive_signals,
no markitdown, no model/network).

Usage:
    python3 scripts/news_ground.py --selftest
"""
import re

MIN_RED_FLAG_CHARS = 12
MAX_RED_FLAG_CHARS = 240


def news_normalize(text) -> str:
    """Position-free quote-grounding key — lowercase, keep [a-z0-9] only.

    Mirrors the corpus grounding rule (derive_signals.normalize) so an extracted entity name or a
    red-flag phrase grounds as a substring of its source article regardless of punctuation / wrapping.
    """
    return re.sub(r"[^a-z0-9]+", "", str(text).lower())


def article_body(md: str) -> str:
    """Display/grounding body for the Read screen: drop the leading markdown `# Title` (it renders as the
    screen H1) and the `*…*` emphasis markers (the panel is pre-wrap text). Grounding-safe: entity names +
    red-flag flags live in the body paragraphs, so both the normalize-substring gate and the raw
    highlighter still match.
    """
    lines = md.splitlines()
    if lines and lines[0].lstrip().startswith("# "):
        lines = lines[1:]
    return "\n".join(lines).strip().replace("*", "")


def ground_record(record, article_text=None, min_chars=MIN_RED_FLAG_CHARS, max_chars=MAX_RED_FLAG_CHARS):
    """Filter a news record to only entities / red-flags that quote-ground in the article (DROP mode).

    Returns (kept_record, dropped) where dropped is a list of {"kind", "value", "reason"}. Mirrors
    build.validate_news_data's predicates exactly (same news_normalize):
      - entity: kept iff `name` is a RAW substring of the body (implies normalize-grounded AND
        highlightable) and has a `type`; ungrounded location/age/profession attributes are STRIPPED
        (the entity is kept, the ungrounded attribute removed — nothing shown that isn't in the source).
      - red_flag: kept iff `flag` is a RAW substring of the body AND `red_flag` is present, distinct
        (normalize) from `flag`, and within [min_chars, max_chars].
    Does not mutate the input record.
    """
    body = article_text if article_text is not None else record.get("article_text", "")
    nbody = news_normalize(body)
    dropped = []

    kept_ents = []
    for ent in record.get("entities") or []:
        nm = (ent.get("name") or "").strip()
        if not nm or not ent.get("type"):
            dropped.append({"kind": "entity", "value": ent, "reason": "missing name/type"}); continue
        if nm not in body:  # raw substring ⟹ normalize-grounded AND highlightable
            dropped.append({"kind": "entity", "value": nm, "reason": "name not raw-grounded in article"}); continue
        e = dict(ent)
        for attr in ("location", "age", "profession"):
            av = e.get(attr)
            if av and news_normalize(str(av)) not in nbody:
                dropped.append({"kind": "attr", "value": f"{nm}.{attr}={av!r}", "reason": "attribute not grounded"})
                e.pop(attr, None)
        kept_ents.append(e)

    kept_flags = []
    for rf in record.get("red_flags") or []:
        flag = (rf.get("flag") or "").strip()
        tr = (rf.get("red_flag") or "").strip()
        if not flag:
            dropped.append({"kind": "red_flag", "value": rf, "reason": "missing flag"}); continue
        if flag not in body:
            dropped.append({"kind": "red_flag", "value": flag, "reason": "flag not raw-grounded in article"}); continue
        if not tr or news_normalize(tr) == news_normalize(flag):
            dropped.append({"kind": "red_flag", "value": flag, "reason": "red_flag missing or not distinct from flag"}); continue
        if not (min_chars <= len(tr) <= max_chars):
            dropped.append({"kind": "red_flag", "value": flag, "reason": f"red_flag length {len(tr)} outside [{min_chars},{max_chars}]"}); continue
        kept_flags.append(rf)

    kept = dict(record)
    kept["entities"] = kept_ents
    kept["red_flags"] = kept_flags
    return kept, dropped


def _selftest() -> int:
    # normalize matches the build-boundary formula
    assert news_normalize("Acme, Corp. 123!") == "acmecorp123"
    assert news_normalize("  USDT (Tether) — wired ") == "usdttetherwired"

    # article_body drops the leading "# Title" and the * emphasis markers
    raw = "# Title Line\nAcme Corp wired funds to Bob Smith in *Miami*. They used shell companies to layer cash."
    body = article_body(raw)
    assert "# Title Line" not in body and "*" not in body and "Miami" in body, body

    record = {
        "id": "t", "title": "T", "article_text": body,
        "entities": [
            {"id": "E1", "name": "Acme Corp", "type": "org", "location": "Miami"},        # name + location grounded
            {"id": "E2", "name": "Bob Smith", "type": "person", "profession": "courier"},  # name grounded, profession NOT
            {"id": "E3", "name": "Ghost LLC", "type": "org"},                              # name NOT grounded -> dropped
        ],
        "red_flags": [
            {"id": "R1", "flag": "used shell companies to layer cash", "red_flag": "Layering via shell companies"},  # kept
            {"id": "R2", "flag": "phrase absent from the article", "red_flag": "Some translation here"},             # not grounded
            {"id": "R3", "flag": "wired funds to Bob Smith", "red_flag": "wired funds to Bob Smith"},                # not distinct
            {"id": "R4", "flag": "wired funds", "red_flag": "ok"},                                                   # red_flag too short
        ],
    }
    kept, dropped = ground_record(record)
    assert [e["name"] for e in kept["entities"]] == ["Acme Corp", "Bob Smith"], kept["entities"]
    assert kept["entities"][0].get("location") == "Miami", "grounded attribute should survive"
    assert "profession" not in kept["entities"][1], "ungrounded attribute should be stripped"
    assert [f["id"] for f in kept["red_flags"]] == ["R1"], kept["red_flags"]
    assert any(d["reason"].startswith("name not raw-grounded") for d in dropped)
    assert any(d["reason"] == "attribute not grounded" for d in dropped)
    assert sum(1 for d in dropped if d["kind"] == "red_flag") == 3

    # idempotence: re-grounding the kept record drops nothing
    kept2, dropped2 = ground_record(kept)
    assert dropped2 == [], f"ground_record not idempotent: {dropped2}"
    assert kept2["entities"] == kept["entities"] and kept2["red_flags"] == kept["red_flags"]

    print(f"news_ground --selftest: PASS (kept {len(kept['entities'])} entities, {len(kept['red_flags'])} red flags; "
          f"dropped {len(dropped)} ungrounded; idempotent)")
    return 0


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    print("news_ground: pure grounding library; run with --selftest")
