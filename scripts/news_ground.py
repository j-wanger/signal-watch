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


def flag_dup_key(rf):
    """Phase 40: the duplicate-collapse key for a red-flag row — (normalized quote, normalized category).

    Shared by ground_record (live DROP mode) and build.validate_news_data (build-path CHECK mode) so
    live collapse == build check by construction. Category-aware on purpose: the same quote under a
    different category is two mechanisms, not a duplicate.
    """
    return (news_normalize(rf.get("flag") or ""), news_normalize(rf.get("category") or ""))


def ground_record(record, article_text=None, min_chars=MIN_RED_FLAG_CHARS, max_chars=MAX_RED_FLAG_CHARS):
    """Filter a news record to only entities / red-flags that quote-ground in the article (DROP mode).

    Returns (kept_record, dropped) where dropped is a list of {"kind", "value", "reason"}. Mirrors
    build.validate_news_data's predicates exactly (same news_normalize):
      - entity: kept iff `name` is a RAW substring of the body (implies normalize-grounded AND
        highlightable) and has a `type`; ungrounded location/age/profession attributes are STRIPPED
        (the entity is kept, the ungrounded attribute removed — nothing shown that isn't in the source).
      - red_flag: kept iff `flag` is a RAW substring of the body AND `red_flag` is present, distinct
        (normalize) from `flag`, and within [min_chars, max_chars].
      - duplicate collapse (Phase 40, measurement-earned): two flags quoting the SAME span under the
        SAME category are one behaviour twice — the FIRST survives (spans identical ⟹ input order is
        the total survivor rule; deterministic for golden regeneration). Same quote under a DIFFERENT
        category is NOT collapsed — one sentence can legitimately ground two mechanisms.
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
    seen_flag_keys = set()
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
        key = flag_dup_key(rf)
        if key in seen_flag_keys:
            dropped.append({"kind": "red_flag", "value": flag, "reason": "duplicate flag (same quote + category)"}); continue
        seen_flag_keys.add(key)
        kept_flags.append(rf)

    kept = dict(record)
    kept["entities"] = kept_ents
    kept["red_flags"] = kept_flags
    return kept, dropped


# ── Phase 38 — LIVE-mode entity-precision filter (STRUCTURAL backstop) ──────────────────────────────
# A deterministic precision pass over LIVE model extraction. serve_news.build_record calls this AFTER
# ground_record; build.py does NOT (committed records + offline dist/news stay byte-frozen). FAITHFUL:
# only DROPS — never invents, preserves every real (grounded) subject.
#
# Phase-38 stress test (3 NEW articles) finding: the PRIMARY entity-precision control is the system
# PROMPT's SUBJECTS-ONLY rule (context shaping) — one exclusion line cut Qwen's institutional noise
# (officials/prosecutors/agencies — an OPEN vocabulary) ~90%. An enumerated denylist OVERFIT the 4
# calibration articles and did not generalize, so it was REMOVED. What remains here are only the rules
# that GENERALIZE structurally: alias-dedup, moniker handles, judicial officers, and source-attribution
# publishers (grounded only in the *Source: citation line).
_JUDICIAL = ("judge", "justice")


def _toks(s):
    return set(re.findall(r"[a-z0-9]+", str(s).lower()))


def _without_source_line(md):
    """Article text minus the leading `*Source: …*` citation line (publishers belong there, not the
    subject list). Used to detect source-attribution orgs structurally (grounded ONLY in that line)."""
    keep, src = [], ""
    for ln in str(md).splitlines():
        s = ln.strip().lstrip("*").strip()
        if s.lower().startswith("source:"):
            src = news_normalize(s)
        else:
            keep.append(ln)
    return "\n".join(keep), src


def screen_entities(entities, text=""):
    """Deterministic LIVE-mode entity-precision pass (see module note). Returns (kept, dropped); each
    dropped item is {"kind": "entity", "value": name, "reason": …}. Pure — does not mutate inputs.
    Idempotent: re-screening the kept list drops nothing.
    """
    ents = list(entities or [])
    toksets = [_toks(e.get("name", "")) for e in ents]
    body_ex_src, source_line = _without_source_line(text)
    nbody_ex_src = news_normalize(body_ex_src)
    njudge = news_normalize(text)
    kept, dropped = [], []
    for i, e in enumerate(ents):
        name = (e.get("name") or "").strip()
        nn = news_normalize(name)
        tx, typ = toksets[i], (e.get("type") or "").strip().lower()
        # (a) alias-dedup — a strict token-subset of ANOTHER extracted entity (keep the fuller name)
        if tx and any(j != i and tx < toksets[j] for j in range(len(ents))):
            dropped.append({"kind": "entity", "value": name, "reason": "alias-duplicate of a fuller name"}); continue
        # (b) moniker / handle — @… or a lone all-lowercase token for a person
        if name.startswith("@") or (typ == "person" and len(tx) == 1 and name == name.lower()):
            dropped.append({"kind": "entity", "value": name, "reason": "moniker/alias handle"}); continue
        # (c) judicial officer — a person whose name is preceded by Judge/Justice in the article
        if typ == "person" and nn and any((jt + nn) in njudge for jt in _JUDICIAL):
            dropped.append({"kind": "entity", "value": name, "reason": "judicial officer (not a subject)"}); continue
        # (d) source-attribution org — grounds ONLY in the *Source: citation line, not the body prose
        if typ == "org" and source_line and nn and nn in source_line and nn not in nbody_ex_src:
            dropped.append({"kind": "entity", "value": name, "reason": "source-attribution publisher (not a subject)"}); continue
        kept.append(e)
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
            {"id": "R1", "flag": "used shell companies to layer cash", "red_flag": "Layering via shell companies",
             "category": "shell"},                                                                                   # kept
            {"id": "R2", "flag": "phrase absent from the article", "red_flag": "Some translation here"},             # not grounded
            {"id": "R3", "flag": "wired funds to Bob Smith", "red_flag": "wired funds to Bob Smith"},                # not distinct
            {"id": "R4", "flag": "wired funds", "red_flag": "ok"},                                                   # red_flag too short
            # Phase 40 dup-collapse: same quote + same category as R1 (translation wording differs) → DUP drop;
            # the FIRST (R1) survives — input order is the total survivor rule (spans identical).
            {"id": "R5", "flag": "used shell companies to layer cash", "red_flag": "Shells used for cash layering",
             "category": "shell"},
            # same quote, DIFFERENT category → kept (one sentence can ground two mechanisms)
            {"id": "R6", "flag": "used shell companies to layer cash", "red_flag": "Rapid cash layering chain",
             "category": "rapid-movement"},
        ],
    }
    kept, dropped = ground_record(record)
    assert [e["name"] for e in kept["entities"]] == ["Acme Corp", "Bob Smith"], kept["entities"]
    assert kept["entities"][0].get("location") == "Miami", "grounded attribute should survive"
    assert "profession" not in kept["entities"][1], "ungrounded attribute should be stripped"
    assert [f["id"] for f in kept["red_flags"]] == ["R1", "R6"], kept["red_flags"]
    assert any(d["reason"].startswith("name not raw-grounded") for d in dropped)
    assert any(d["reason"] == "attribute not grounded" for d in dropped)
    assert sum(1 for d in dropped if d["kind"] == "red_flag") == 4
    dup_drops = [d for d in dropped if d["reason"] == "duplicate flag (same quote + category)"]
    assert len(dup_drops) == 1 and dup_drops[0]["value"] == "used shell companies to layer cash", dup_drops

    # idempotence: re-grounding the kept record drops nothing
    kept2, dropped2 = ground_record(kept)
    assert dropped2 == [], f"ground_record not idempotent: {dropped2}"
    assert kept2["entities"] == kept["entities"] and kept2["red_flags"] == kept["red_flags"]

    # ── screen_entities (Phase 38 live-mode precision pass) ──
    se_text = ("# Headline\n\n*Source: U.S. Department of Justice, Office of Public Affairs — justice.gov*\n\n"
               "Judge Jane Doe sentenced George Rossi. Rossi controls the TGR Group with Elena Chirkinyan "
               "(@monalisa7) and an associate, acescom. SH Brothers Inc. shipped the goods. The law firm helped.")
    se_in = [
        {"name": "George Rossi", "type": "person"},        # kept (real subject)
        {"name": "Rossi", "type": "person"},               # alias-dup of George Rossi → drop
        {"name": "Elena Chirkinyan", "type": "person"},    # kept
        {"name": "@monalisa7", "type": "person"},          # moniker → drop
        {"name": "acescom", "type": "person"},             # lone-lowercase handle → drop
        {"name": "Jane Doe", "type": "person"},            # judicial officer (Judge Jane Doe) → drop
        {"name": "TGR Group", "type": "org"},              # kept (NOT dropped by a bare 'group')
        {"name": "SH Brothers Inc.", "type": "org"},       # kept
        {"name": "U.S. Department of Justice", "type": "org"},  # source-attribution (only in *Source: line) → drop
        {"name": "Office of Public Affairs", "type": "org"},   # source-attribution publisher → drop
    ]
    skept, sdrop = screen_entities(se_in, se_text)
    sk = [e["name"] for e in skept]
    # institutional noise (agencies, courts-by-name, generics) is the PROMPT's job now — the structural
    # filter keeps real subjects and drops only alias-dups / monikers / judicial officers / source publishers.
    assert sk == ["George Rossi", "Elena Chirkinyan", "TGR Group", "SH Brothers Inc."], sk
    reasons = {d["value"]: d["reason"] for d in sdrop}
    assert reasons["Rossi"].startswith("alias-duplicate")
    assert reasons["@monalisa7"].startswith("moniker") and reasons["acescom"].startswith("moniker")
    assert reasons["Jane Doe"].startswith("judicial")
    assert reasons["U.S. Department of Justice"].startswith("source-attribution")
    # idempotent + faithful (never invents): re-screening the survivors drops nothing
    skept2, sdrop2 = screen_entities(skept, se_text)
    assert sdrop2 == [] and [e["name"] for e in skept2] == sk, "screen_entities not idempotent"

    print(f"news_ground --selftest: PASS (kept {len(kept['entities'])} entities, {len(kept['red_flags'])} red flags; "
          f"dropped {len(dropped)} ungrounded; screen_entities {len(sk)} kept / {len(sdrop)} noise dropped; idempotent)")
    return 0


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    print("news_ground: pure grounding library; run with --selftest")
