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

# Phase 41 — closed vocabularies for the enriched entity schema. SINGLE AUTHORITY (this shared gate):
# serve_news's EXTRACT_SCHEMA/SYSTEM_PROMPT and news_store reference these, never redefine them.
# A label/kind is vocab-CHECKED, never correctness-checked (the C/D-code honest split). location/age/
# profession stay flat legacy entity attributes; PROPERTY_KINDS carries the identifier-class additions.
PROPERTY_KINDS = (
    "address", "phone", "email", "client_number", "account_number",
    "dob", "id_registration", "wallet", "domain",
)
RELATION_LABELS = (
    "co-conspirator", "owner-or-controller-of", "front-for", "family-or-associate-of",
    "employee-or-agent-of", "professional-intermediary-for", "counterparty-of",
    "recipient-of-funds-from", "other",
)


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
        # Phase 41 — aliases: RAW-grounded like the name (display + highlight surface). An alias that
        # merely repeats the name (normalized) is silently redundant; an ungrounded one is a DROP finding.
        als = []
        for a in (e.get("aliases") or []):
            a = str(a).strip()
            if not a or news_normalize(a) == news_normalize(nm) \
                    or any(news_normalize(a) == news_normalize(x) for x in als):
                continue
            if a in body:
                als.append(a)
            else:
                dropped.append({"kind": "alias", "value": f"{nm}: {a!r}", "reason": "alias not raw-grounded in article"})
        if als:
            e["aliases"] = als
        else:
            e.pop("aliases", None)
        # Phase 41 — properties: `kind` vocab-checked; `value` NORMALIZE-grounded (the attribute
        # precedent — tolerant of the article's line-wrap/punctuation variance around an identifier,
        # while still rejecting DERIVED/canonicalized forms, e.g. a +1-prefixed phone the article never
        # printed). Canonicalization is deterministic POST-gate work, stored beside the raw span, never gated.
        props = []
        for p in (e.get("properties") or []):
            kind = str((p or {}).get("kind") or "").strip()
            val = str((p or {}).get("value") or "").strip()
            if kind not in PROPERTY_KINDS:
                dropped.append({"kind": "property", "value": f"{nm}.{kind}={val!r}", "reason": "unknown property kind"}); continue
            if not val or news_normalize(val) not in nbody:
                dropped.append({"kind": "property", "value": f"{nm}.{kind}={val!r}", "reason": "property value not grounded"}); continue
            props.append({"kind": kind, "value": val})
        if props:
            e["properties"] = props
        else:
            e.pop("properties", None)
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

    # Phase 41 — relationships: the LABEL is vocab-checked (never correctness-checked — the C/D-code
    # honest split); `evidence` RAW-grounds like a flag quote; `from`/`to` must reference KEPT entity
    # names (referential integrity); a self-edge is shape-invalid. Optional: absent stays absent.
    kept_names = {ke.get("name") for ke in kept_ents}
    rels = []
    for r in (record.get("relationships") or []):
        fr = str((r or {}).get("from") or "").strip()
        to = str((r or {}).get("to") or "").strip()
        lb = str((r or {}).get("label") or "").strip()
        ev = str((r or {}).get("evidence") or "").strip()
        rid = f"{fr!r}-[{lb}]->{to!r}"
        if lb not in RELATION_LABELS:
            dropped.append({"kind": "relationship", "value": rid, "reason": "unknown relation label"}); continue
        if fr not in kept_names or to not in kept_names:
            dropped.append({"kind": "relationship", "value": rid, "reason": "relationship references a non-extracted entity"}); continue
        if fr == to:
            dropped.append({"kind": "relationship", "value": rid, "reason": "self-relationship"}); continue
        if not ev or ev not in body:
            dropped.append({"kind": "relationship", "value": rid, "reason": "relationship evidence not raw-grounded"}); continue
        rels.append({"from": fr, "to": to, "label": lb, "evidence": ev})
    if rels:
        kept["relationships"] = rels
    else:
        kept.pop("relationships", None)
    # Phase 41 — main_subjects: honest none/multiple; each must be a KEPT entity name.
    ms = []
    for s in (record.get("main_subjects") or []):
        s = str(s).strip()
        if s in kept_names and s not in ms:
            ms.append(s)
        elif s:
            dropped.append({"kind": "main_subject", "value": s, "reason": "main_subject is not an extracted entity"})
    if ms:
        kept["main_subjects"] = ms
    else:
        kept.pop("main_subjects", None)
    return kept, dropped


def reconcile_refs(record, rename=None):
    """Phase 41 — re-establish referential integrity after a post-gate pass changes the entity list
    (the screen_entities alias-folds, the live second-pass verify): remap folded names via `rename`
    (folded name → parent name), then drop relationships/main_subjects that reference an entity no
    longer present — plus any remap-created self-edge. Deterministic; does not mutate the input."""
    out = dict(record)
    rename = rename or {}
    names = {e.get("name") for e in (out.get("entities") or [])}
    rels = []
    for r in (out.get("relationships") or []):
        fr = rename.get(r.get("from"), r.get("from"))
        to = rename.get(r.get("to"), r.get("to"))
        if fr in names and to in names and fr != to:
            rels.append({**r, "from": fr, "to": to})
    if rels:
        out["relationships"] = rels
    else:
        out.pop("relationships", None)
    ms = []
    for s in (out.get("main_subjects") or []):
        s = rename.get(s, s)
        if s in names and s not in ms:
            ms.append(s)
    if ms:
        out["main_subjects"] = ms
    else:
        out.pop("main_subjects", None)
    return out


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


def _adjacent_parent(name, ents, i, text):
    """Phase 41 — the moniker's parent entity, ONLY when the article prints the handle immediately
    after the parent's name (e.g. 'Elena Chirkinyan (@monalisa7)', 'John Doe, a.k.a. jd99') — a
    STRUCTURAL adjacency rule, not an enumerated list. Returns the parent index or None."""
    for j, p in enumerate(ents):
        if j == i:
            continue
        pn = (p.get("name") or "").strip()
        if pn and re.search(re.escape(pn) + r"[\s,]{0,2}[(\[\"']{0,2}\s*(?:a\.?k\.?a\.?\s*)?" + re.escape(name), text):
            return j
    return None


def screen_entities(entities, text=""):
    """Deterministic LIVE-mode entity-precision pass (see module note). Returns (kept, dropped); each
    dropped item is {"kind": "entity", "value": name, "reason": …}. Pure — does not mutate inputs.
    Idempotent: re-screening the kept list drops nothing.

    Phase 41 (the fold INVERSION): the alias-dedup and adjacent-moniker rules now FOLD instead of
    DROP — the article's own name variations are entity-resolution SIGNAL, not noise. The subset
    name / adjacent handle attaches to its parent entity's `aliases` (its own aliases/properties merge
    up); the fold is reported in `dropped` with a `folded_into` key (the audit trail — callers remap
    relationship/main_subject references via reconcile_refs). A moniker with NO structurally adjacent
    parent still drops, as do judicial officers and source-attribution publishers.
    """
    ents = list(entities or [])
    toksets = [_toks(e.get("name", "")) for e in ents]
    body_ex_src, source_line = _without_source_line(text)
    nbody_ex_src = news_normalize(body_ex_src)
    njudge = news_normalize(text)
    decisions = []
    for i, e in enumerate(ents):
        name = (e.get("name") or "").strip()
        nn = news_normalize(name)
        tx, typ = toksets[i], (e.get("type") or "").strip().lower()
        # (a) alias-dedup — a strict token-subset of ANOTHER extracted entity → FOLD into the fuller name
        if tx and any(j != i and tx < toksets[j] for j in range(len(ents))):
            parent = next(j for j in range(len(ents)) if j != i and tx < toksets[j])
            decisions.append(("fold", parent)); continue
        # (b) moniker / handle — @… or a lone all-lowercase token for a person → FOLD if structurally
        # adjacent to a parent name in the text, else DROP (no parent to attach the alias to)
        if name.startswith("@") or (typ == "person" and len(tx) == 1 and name == name.lower()):
            parent = _adjacent_parent(name, ents, i, text)
            decisions.append(("fold", parent) if parent is not None else ("drop", "moniker/alias handle"))
            continue
        # (c) judicial officer — a person whose name is preceded by Judge/Justice in the article
        if typ == "person" and nn and any((jt + nn) in njudge for jt in _JUDICIAL):
            decisions.append(("drop", "judicial officer (not a subject)")); continue
        # (d) source-attribution org — grounds ONLY in the *Source: citation line, not the body prose
        if typ == "org" and source_line and nn and nn in source_line and nn not in nbody_ex_src:
            decisions.append(("drop", "source-attribution publisher (not a subject)")); continue
        decisions.append(("keep", None))
    # Apply: keeps are shallow copies (folds mutate the parent's aliases); a fold whose parent was
    # itself folded/dropped degrades to a plain drop (no chain-following — not measurement-earned).
    kept, dropped, out_by_idx = [], [], {}
    for i, e in enumerate(ents):
        if decisions[i][0] == "keep":
            ne = dict(e)
            out_by_idx[i] = ne
            kept.append(ne)
    for i, e in enumerate(ents):
        verdict, arg = decisions[i]
        name = (e.get("name") or "").strip()
        if verdict == "fold":
            parent = out_by_idx.get(arg)
            if parent is None:
                dropped.append({"kind": "entity", "value": name, "reason": "moniker/alias handle"
                                if name.startswith("@") or name == name.lower()
                                else "alias-duplicate of a fuller name"})
                continue
            als = list(parent.get("aliases") or [])
            for cand in [name] + list(e.get("aliases") or []):
                if news_normalize(cand) != news_normalize(parent.get("name", "")) \
                        and all(news_normalize(cand) != news_normalize(x) for x in als):
                    als.append(cand)
            parent["aliases"] = als
            seen_props = [(p.get("kind"), news_normalize(p.get("value", ""))) for p in (parent.get("properties") or [])]
            for p in (e.get("properties") or []):
                if (p.get("kind"), news_normalize(p.get("value", ""))) not in seen_props:
                    parent["properties"] = (parent.get("properties") or []) + [p]
            dropped.append({"kind": "entity", "value": name,
                            "reason": f"folded as alias into {parent.get('name')!r}",
                            "folded_into": parent.get("name")})
        elif verdict == "drop":
            dropped.append({"kind": "entity", "value": name, "reason": arg})
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

    # ── Phase 41 — enriched-schema grounding (aliases / properties / relationships / main_subjects) ──
    ph41_body = ("Maria Lopez, also known as M. Lopez, ran Lopez Imports LLC. Call (212) 555-1234 or "
                 "write maria@lopez-imports.example for invoices. Wallet bc1qar0srrr7xfkvy5l643lydnw9re\n"
                 "59gtzxyzf5mdq received the funds. Account No. 4471-889 at the bank was hers. "
                 "Lopez Imports LLC was a front for Maria Lopez, prosecutors said.")
    ph41 = {
        "id": "t41", "title": "T41", "article_text": ph41_body,
        "entities": [
            {"name": "Maria Lopez", "type": "person",
             "aliases": ["M. Lopez", "Maria the Ghost"],          # grounded · NOT grounded → alias drop
             "properties": [
                 {"kind": "phone", "value": "212-555-1234"},       # punctuation-VARIED vs "(212) 555-1234" → normalize-grounds
                 {"kind": "wallet", "value": "bc1qar0srrr7xfkvy5l643lydnw9re59gtzxyzf5mdq"},  # LINE-WRAPPED in source → grounds
                 {"kind": "account_number", "value": "4471-889"},  # grounded
                 {"kind": "phone", "value": "+1 212 555 1234"},    # DERIVED/canonicalized (+1 never printed) → drop
                 {"kind": "ssn", "value": "000-00-0000"},          # unknown kind → drop
             ]},
            {"name": "Lopez Imports LLC", "type": "org",
             "properties": [{"kind": "email", "value": "maria@lopez-imports.example"}]},
        ],
        "red_flags": [{"id": "R1", "flag": "was a front for Maria Lopez", "red_flag": "Front company conceals the true controller", "category": "shell"}],
        "relationships": [
            {"from": "Lopez Imports LLC", "to": "Maria Lopez", "label": "front-for",
             "evidence": "Lopez Imports LLC was a front for Maria Lopez"},                       # kept
            {"from": "Maria Lopez", "to": "Lopez Imports LLC", "label": "henchman-of", "evidence": "ran Lopez Imports LLC"},  # unknown label → drop
            {"from": "Maria Lopez", "to": "Ghost Co", "label": "counterparty-of", "evidence": "ran Lopez Imports LLC"},       # non-extracted → drop
            {"from": "Maria Lopez", "to": "Maria Lopez", "label": "other", "evidence": "ran Lopez Imports LLC"},              # self-edge → drop
            {"from": "Maria Lopez", "to": "Lopez Imports LLC", "label": "owner-or-controller-of", "evidence": "a quote the article never printed"},  # evidence ungrounded → drop
        ],
        "main_subjects": ["Maria Lopez", "Ghost Co"],              # kept · non-extracted → drop
    }
    k41, d41 = ground_record(ph41)
    ml = k41["entities"][0]
    assert ml.get("aliases") == ["M. Lopez"], ml.get("aliases")
    assert [p["kind"] for p in ml["properties"]] == ["phone", "wallet", "account_number"], ml["properties"]
    r41 = {d["reason"] for d in d41}
    assert "alias not raw-grounded in article" in r41 and "unknown property kind" in r41
    assert sum(1 for d in d41 if d["reason"] == "property value not grounded") == 1, d41  # the +1-canonical phone
    assert k41.get("relationships") == [{"from": "Lopez Imports LLC", "to": "Maria Lopez", "label": "front-for",
                                         "evidence": "Lopez Imports LLC was a front for Maria Lopez"}], k41.get("relationships")
    for reason in ("unknown relation label", "relationship references a non-extracted entity",
                   "self-relationship", "relationship evidence not raw-grounded",
                   "main_subject is not an extracted entity"):
        assert any(d["reason"] == reason for d in d41), f"missing drop: {reason}"
    assert k41.get("main_subjects") == ["Maria Lopez"], k41.get("main_subjects")
    k41b, d41b = ground_record(k41)
    assert d41b == [] and k41b == k41, f"Phase-41 grounding not idempotent: {d41b}"

    # reconcile_refs — fold remap + dangling-ref filtering (the post-screen/post-verify pass)
    rr = reconcile_refs(
        {"entities": [{"name": "George Rossi"}, {"name": "TGR Group"}],
         "relationships": [
             {"from": "Rossi", "to": "TGR Group", "label": "owner-or-controller-of", "evidence": "x"},   # remapped via fold
             {"from": "Elena Chirkinyan", "to": "TGR Group", "label": "co-conspirator", "evidence": "y"},  # dangling → drop
             {"from": "Rossi", "to": "George Rossi", "label": "other", "evidence": "z"}],                 # remap-created self-edge → drop
         "main_subjects": ["Rossi", "Elena Chirkinyan"]},
        rename={"Rossi": "George Rossi"})
    assert rr["relationships"] == [{"from": "George Rossi", "to": "TGR Group",
                                    "label": "owner-or-controller-of", "evidence": "x"}], rr["relationships"]
    assert rr["main_subjects"] == ["George Rossi"], rr["main_subjects"]
    assert "relationships" not in reconcile_refs({"entities": [], "relationships": [
        {"from": "A", "to": "B", "label": "other", "evidence": "q"}]}), "empty result must remove the key"

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
    # filter keeps real subjects and drops only judicial officers / source publishers / orphan monikers.
    assert sk == ["George Rossi", "Elena Chirkinyan", "TGR Group", "SH Brothers Inc."], sk
    reasons = {d["value"]: d["reason"] for d in sdrop}
    # Phase 41 — the fold INVERSION: the subset name + the structurally adjacent handle are now ALIASES
    # of their parents (entity-resolution signal kept), reported with a folded_into audit key; the
    # orphan handle (no adjacent parent in the text) still drops.
    assert skept[0].get("aliases") == ["Rossi"], skept[0]
    assert skept[1].get("aliases") == ["@monalisa7"], skept[1]
    folds = {d["value"]: d.get("folded_into") for d in sdrop if d.get("folded_into")}
    assert folds == {"Rossi": "George Rossi", "@monalisa7": "Elena Chirkinyan"}, folds
    assert reasons["Rossi"] == "folded as alias into 'George Rossi'"
    assert reasons["acescom"].startswith("moniker"), "orphan handle (no adjacent parent) must still DROP"
    assert reasons["Jane Doe"].startswith("judicial")
    assert reasons["U.S. Department of Justice"].startswith("source-attribution")
    # idempotent + faithful (never invents): re-screening the survivors drops nothing
    skept2, sdrop2 = screen_entities(skept, se_text)
    assert sdrop2 == [] and [e["name"] for e in skept2] == sk, "screen_entities not idempotent"
    assert skept2[0].get("aliases") == ["Rossi"], "fold result must survive re-screening unchanged"

    print(f"news_ground --selftest: PASS (kept {len(kept['entities'])} entities, {len(kept['red_flags'])} red flags; "
          f"dropped {len(dropped)} ungrounded; screen_entities {len(sk)} kept / {len(sdrop)} noise dropped; idempotent)")
    return 0


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    print("news_ground: pure grounding library; run with --selftest")
