#!/usr/bin/env python3
"""Validate a typology config and inline it into index.html -> dist/<id>/index.html.

The ship target is a single self-contained file per typology that runs from file:// —
no server, no fetch, no ES modules. This build (a) validates the config against the
schema at the boundary and fails loud, then (b) injects it at the `__CONFIG__`
placeholder; the engine and styles already live in index.html.

Usage:
    python3 scripts/build.py [typology_id]   # default: fentanyl
    python3 scripts/build.py corpus          # build the FinCEN corpus explorer (dist/corpus/)
    python3 scripts/build.py all             # build every typology + the corpus explorer
    python3 scripts/build.py --check [all|corpus|<id>]  # drift guard: committed dist == fresh build?

The corpus explorer (Phase 13) is a separate single-file artifact built from corpus.html + the
committed per-source data artifacts. Phase 20 made it MULTI-SOURCE: CORPUS_SOURCES registers each
FinCEN publication type (advisories, alerts, …), and render_corpus merges every source's
corpus-status.json (extraction manifest) + derived/*.json (LLM-derived records) by id into one
__CORPUS__. build.py reads those committed data artifacts and NEVER imports the authoring layer
(derive_signals.py); the derived records' shape is validated at this boundary.

`--check` is non-mutating and git-agnostic: it re-renders each config in memory and
byte-compares against the committed dist/<id>/index.html, exiting non-zero (and naming the
typology) on any drift or a missing built artifact. Run it before committing or presenting.

Stdlib only. Exits non-zero on a missing or schema-invalid config, or (under --check) on drift.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "index.html"
TYPOLOGY_DIR = ROOT / "config" / "typologies"
PLACEHOLDER = "__CONFIG__"
DEFAULT_TYPOLOGY = "fentanyl"

# Corpus explorer (Phase 13) — a SEPARATE ship artifact: its own template + data sources,
# built alongside the typologies. build.py reads the committed data artifacts (per-source
# extraction manifests + the LLM-derived records) and NEVER imports the authoring layer
# (derive_signals.py).
CORPUS_TEMPLATE = ROOT / "corpus.html"
CORPUS_PLACEHOLDER = "__CORPUS__"
# Phase 24: the cross-corpus typology overlay — a SEPARATE committed artifact mapping each LIVE
# (derived) doc-id to one closed-vocabulary typology, so the explorer can group documents across
# sources/jurisdictions. Kept separate from the 42 derived records (which stay byte-frozen); validated
# at the build boundary (validate_typology — closed vocab + referential integrity + total coverage).
TYPOLOGY_MAP = ROOT / "data" / "typology-map.json"
# Phase 29: the capability-lens overlay — labels + group + the institution's interview posture per
# capability (C*) / data-source (D*) code. The per-indicator codes already ride in each derived record
# (riding along with the indicators array); this SEPARATE committed artifact supplies the human label +
# the Phase-28 interview self-assessment (y/partial/n), so the explorer can re-project the corpus by
# DETECTION CAPABILITY. Kept separate from the 42 derived records (which stay byte-frozen); validated at
# the build boundary (validate_capability_taxonomy — shape + closed vocab + referential integrity).
CAPABILITY_TAXONOMY = ROOT / "data" / "capability-taxonomy.json"
# Multi-source corpus registry (Phase 20): each source is one FinCEN publication TYPE with its own
# committed corpus-status.json + derived/*.json; render_corpus merges them by id into one __CORPUS__.
# Decoupling source-id from storage dir means adding the Nth FinCEN source (or, later, OFAC — also
# public domain under 17 U.S.C. 105) is a registry entry, not a code change. `doc_type` is the honest
# human label the explorer's menu chip shows per document. The quote-grounding gate (derive_signals.py)
# is source-agnostic; build.py only consumes the committed per-source artifacts. `jurisdiction` (Phase 24)
# is the country whose regime the source belongs to — US (FinCEN + OFAC, US Treasury) or Canada (FINTRAC);
# the cross-corpus synthesis groups documents by typology ACROSS jurisdictions, so each merged entry carries
# it. It is source-level (not per-doc), so it lives here in the registry, not in the typology overlay.
CORPUS_SOURCES = [
    {"id": "fincen-advisories", "doc_type": "Advisory", "jurisdiction": "US",
     "status": ROOT / "data" / "fincen" / "corpus-status.json",
     "derived": ROOT / "data" / "fincen" / "derived"},
    {"id": "fincen-alerts", "doc_type": "Alert", "jurisdiction": "US",
     "status": ROOT / "data" / "fincen-alerts" / "corpus-status.json",
     "derived": ROOT / "data" / "fincen-alerts" / "derived"},
    # Phase 21: OFAC (US Treasury) — a second US-federal agency, also public domain under 17 U.S.C. 105.
    {"id": "ofac-advisories", "doc_type": "OFAC", "jurisdiction": "US",
     "status": ROOT / "data" / "ofac" / "corpus-status.json",
     "derived": ROOT / "data" / "ofac" / "derived"},
    # Phase 22: FINTRAC (Canada's FIU) — the FIRST CROSS-JURISDICTION source. NOT US public domain:
    # Canadian Crown copyright, reproduced verbatim for NON-COMMERCIAL use with attribution per FINTRAC's
    # Terms & Conditions (the `source` attribution string each record carries states this distinct basis;
    # the corpus.html source panel renders it verbatim, so FINTRAC never shows the US "public domain" line).
    {"id": "fintrac-advisories", "doc_type": "FINTRAC", "jurisdiction": "Canada",
     "status": ROOT / "data" / "fintrac" / "corpus-status.json",
     "derived": ROOT / "data" / "fintrac" / "derived"},
    # Phase 33: FINTRAC `/guidance-directives/` per-sector ML/TF INDICATOR pages — a SECOND FINTRAC
    # product area (the Operational Alerts above are /intel/ strategic intelligence). Same Crown-copyright
    # non-commercial basis; far denser (each sector page is a 100+-indicator baseline). A distinct doc_type
    # so the SELECT menu separates the sector baselines from the OAs.
    {"id": "fintrac-guidance", "doc_type": "FINTRAC Guidance", "jurisdiction": "Canada",
     "status": ROOT / "data" / "fintrac-guidance" / "corpus-status.json",
     "derived": ROOT / "data" / "fintrac-guidance" / "derived"},
]
# the cover×data build-recommendation vocabulary (mirrors derive_signals.py _REC_MATRIX values;
# re-declared here so build.py's boundary check stays independent of the authoring tool).
BUILD_RECS = {"COVERED", "BUILD_NOW", "BUILD_ENRICH", "SOURCE_DATA", "ENHANCE", "MONITOR"}
# Phase 25 — red_flag (the natural AML-term translation beside the verbatim flag) is shape-checked
# at this boundary too (build stays decoupled from the authoring gate; mirrors derive_signals.py's
# _MIN/_MAX_RED_FLAG_CHARS so the two checks stay in parity).
MIN_RED_FLAG_CHARS = 12
MAX_RED_FLAG_CHARS = 240

# Phase 31 (M8): the adverse-media / negative-news stream — a SECOND standalone ship artifact (its own
# template + committed SYNTHETIC data), built alongside the typologies + corpus. Mirrors the corpus pattern:
# build.py reads committed data (synthetic news articles + their derived entities/red-flags + a synthetic
# client/counterparty book) and inlines it at __NEWS__; the ship file runs the fuzzy entity-match entirely
# CLIENT-SIDE (no runtime LLM / fetch). Entities + red-flag phrases are quote-grounded in the source article
# at the build boundary (validate_news_data) — the same faithfulness discipline as the corpus, with a LOCAL
# normalizer so build.py stays decoupled from the authoring layer (never imports derive_signals.py).
NEWS_TEMPLATE = ROOT / "news.html"
NEWS_PLACEHOLDER = "__NEWS__"
NEWS_DERIVED = ROOT / "data" / "news" / "derived"
NEWS_BOOK = ROOT / "data" / "news" / "book.json"
NEWS_MATCH_THRESHOLD = 0.85  # fuzzy-match surface threshold (shared by the ship artifact + the harness)

STATUS = {"covered", "partial", "gap"}
POSTURE = {"y", "n", "partial"}   # Phase 29 — the capability-lens interview self-assessment vocabulary
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


def validate_corpus_data(advisories: list) -> list:
    """Deterministic boundary check on the merged corpus dataset. Returns error strings.

    SHAPE only — build.py stays decoupled from the authoring layer: a derived advisory's
    indicators must each carry a valid status/data, a build_rec in the matrix vocabulary, and
    (Phase 25) a red_flag — the natural AML-term translation, present + distinct from the verbatim
    flag + phrase-length-bounded; a BUILD_NOW indicator must carry build_logic with the full
    definition shape. Traceability (every indicator -> a red-flag md line) + translation
    faithfulness are the authoring gate's job — run `derive_signals.py --check-derived` first.
    """
    e = []
    if not isinstance(advisories, list) or not advisories:
        return ["corpus has no advisories[]"]
    for a in advisories:
        aid = a.get("id", "?")
        if not a.get("id"):
            e.append("an advisory is missing id")
        if "indicators" not in a:
            continue  # a non-derived advisory carries only status metadata — nothing to validate
        inds = a.get("indicators")
        if not isinstance(inds, list) or not inds:
            e.append(f"{aid}: derived advisory has an empty/invalid indicators array")
            continue
        for i in inds:
            iid = i.get("id", "?")
            if not i.get("id"):
                e.append(f"{aid}: an indicator is missing id")
            if i.get("status") not in STATUS:
                e.append(f"{aid}/{iid}: status invalid: {i.get('status')}")
            if i.get("data") not in DATA:
                e.append(f"{aid}/{iid}: data invalid: {i.get('data')}")
            rec = i.get("build_rec")
            if rec not in BUILD_RECS:
                e.append(f"{aid}/{iid}: build_rec invalid: {rec!r} (not in {sorted(BUILD_RECS)})")
            logic = i.get("build_logic")
            if rec == "BUILD_NOW":
                if not isinstance(logic, dict):
                    e.append(f"{aid}/{iid}: BUILD_NOW requires build_logic (the signal definition)")
                else:
                    missing = DEF_KEYS - set(logic)
                    if missing:
                        e.append(f"{aid}/{iid}: build_logic missing keys {sorted(missing)}")
                    feats = logic.get("features")
                    if not isinstance(feats, list) or not feats:
                        e.append(f"{aid}/{iid}: build_logic.features must be a non-empty array")
            # Phase 25 — red_flag (the natural AML-term translation) shape: present, non-empty, a
            # rephrase (not a verbatim copy of `flag`), phrase-length-bounded. The authoring gate
            # (derive_signals.py) is the stricter check; this keeps the build boundary independent.
            rf = i.get("red_flag")
            if not (isinstance(rf, str) and rf.strip()):
                e.append(f"{aid}/{iid}: missing red_flag (the natural AML-term translation)")
            elif isinstance(i.get("flag"), str) and rf.strip() == i.get("flag").strip():
                e.append(f"{aid}/{iid}: red_flag is identical to the verbatim flag (must be a rephrase)")
            elif not (MIN_RED_FLAG_CHARS <= len(rf.strip()) <= MAX_RED_FLAG_CHARS):
                e.append(f"{aid}/{iid}: red_flag length {len(rf.strip())} outside [{MIN_RED_FLAG_CHARS}, {MAX_RED_FLAG_CHARS}] chars")
    return e


def load_typology_map() -> tuple:
    """Load + shape-check the cross-corpus typology overlay (data/typology-map.json).

    Returns (vocabulary: set[str], mapping: dict[str, str]). Fails loud on a missing/invalid file
    or a malformed shape. The overlay is a SEPARATE committed artifact (the derived records stay
    byte-frozen); referential integrity + coverage against the live corpus are checked in
    validate_typology once the merged corpus is known.
    """
    rel = TYPOLOGY_MAP.relative_to(ROOT)
    if not TYPOLOGY_MAP.exists():
        die(f"typology overlay not found: {rel}")
    try:
        doc = json.loads(TYPOLOGY_MAP.read_text(encoding="utf-8"))
    except json.JSONDecodeError as ex:
        die(f"invalid JSON in {rel}: {ex}")
    vocab = doc.get("vocabulary")
    mapping = doc.get("map")
    if not isinstance(vocab, dict) or not vocab:
        die(f"{rel}: 'vocabulary' must be a non-empty object {{typology: description}}")
    if not isinstance(mapping, dict) or not mapping:
        die(f"{rel}: 'map' must be a non-empty object {{doc-id: typology}}")
    return vocab, mapping


def validate_typology(advisories: list, vocab: dict, mapping: dict) -> list:
    """Boundary check on the typology overlay against the merged corpus. Returns error strings.

    Three deterministic checks (the build-boundary GATE for the overlay — the map is agent-proposed,
    this disposes):
      1. closed vocab   — every mapped typology is a declared vocabulary term;
      2. referential    — every mapped doc-id is a LIVE (derived) doc in the corpus (no dangling);
      3. total coverage — every LIVE (derived) doc carries a typology (no gaps).
    Non-derived docs (no indicators → nothing to combine in synthesis) are NOT required to be mapped
    and MUST NOT appear in the map (a map entry for one would be a dangling reference, caught by #2).
    """
    e = []
    live = {a["id"] for a in advisories if a.get("derived") and a.get("id")}
    for doc_id, typ in mapping.items():
        if typ not in vocab:
            e.append(f"{doc_id}: typology {typ!r} not in the declared vocabulary")
        if doc_id not in live:
            e.append(f"{doc_id}: mapped doc-id is not a live (derived) corpus document")
    for doc_id in sorted(live - set(mapping)):
        e.append(f"{doc_id}: live (derived) document has no typology in the overlay")
    return e


def load_capability_taxonomy() -> tuple:
    """Load + shape-check the capability-lens overlay (data/capability-taxonomy.json).

    Returns (capabilities: list[dict], data_sources: list[dict]) — each entry {id, name, posture, …}.
    The per-indicator `capability`/`data_source` codes already ride in each derived record; this overlay
    supplies the human label + group + the institution's Phase-28 interview posture (y/partial/n) per code,
    so the explorer can re-project the corpus by DETECTION CAPABILITY. A SEPARATE committed artifact (the
    derived records stay byte-frozen); referential integrity against the live corpus is checked in
    validate_capability_taxonomy once the merged corpus is known.
    """
    rel = CAPABILITY_TAXONOMY.relative_to(ROOT)
    if not CAPABILITY_TAXONOMY.exists():
        die(f"capability taxonomy not found: {rel}")
    try:
        doc = json.loads(CAPABILITY_TAXONOMY.read_text(encoding="utf-8"))
    except json.JSONDecodeError as ex:
        die(f"invalid JSON in {rel}: {ex}")
    caps = doc.get("capabilities")
    srcs = doc.get("data_sources")
    if not isinstance(caps, list) or not caps:
        die(f"{rel}: 'capabilities' must be a non-empty array")
    if not isinstance(srcs, list) or not srcs:
        die(f"{rel}: 'data_sources' must be a non-empty array")
    return caps, srcs


def validate_capability_taxonomy(advisories: list, caps: list, srcs: list) -> list:
    """Boundary check on the capability taxonomy against the merged corpus. Returns error strings.

    The build-boundary GATE for the lens overlay (agent-proposed labels + interview posture, this
    disposes — mirrors validate_typology; the grounding gate derive_signals.py stays untouched):
      1. shape        — every entry has an id + name + posture ∈ {y,n,partial}; no repeated id;
      2. closed vocab + referential integrity — every capability/data_source code a LIVE indicator
         carries is a declared taxonomy id (no dangling code with no label/posture);
      3. completeness — every LIVE indicator carries BOTH a capability and a data_source code (the lens
         re-projects by these; a missing code would silently drop an indicator from the capability view).
    """
    e = []
    cap_ids, src_ids = set(), set()
    for label, items, ids in (("capability", caps, cap_ids), ("data_source", srcs, src_ids)):
        for x in items:
            cid = x.get("id")
            if not cid or not x.get("name"):
                e.append(f"{label} entry missing id or name: {x!r}")
                continue
            if cid in ids:
                e.append(f"{label} id repeated: {cid}")
            ids.add(cid)
            if x.get("posture") not in POSTURE:
                e.append(f"{label} {cid}: posture {x.get('posture')!r} not in {sorted(POSTURE)}")
    for a in advisories:
        if not a.get("derived"):
            continue
        for i in a.get("indicators") or []:
            iid = f"{a.get('id', '?')}/{i.get('id', '?')}"
            c, d = i.get("capability"), i.get("data_source")
            if not c:
                e.append(f"{iid}: indicator missing capability code")
            elif c not in cap_ids:
                e.append(f"{iid}: capability {c!r} not in the taxonomy")
            if not d:
                e.append(f"{iid}: indicator missing data_source code")
            elif d not in src_ids:
                e.append(f"{iid}: data_source {d!r} not in the taxonomy")
    return e


def _strip_provenance(md: str) -> str:
    """Strip a corpus md's leading provenance HTML-comment header + blank lines → the body only.

    Mirrors render_one's text_file resolution (the 3 single-line `<!-- … -->` provenance comments
    pdf_to_md.py writes, then a blank line, then the advisory body) but as a STANDALONE helper, so
    render_one and the byte-frozen typology dists stay untouched.
    """
    lines = md.splitlines()
    while lines and (lines[0].lstrip().startswith("<!--") or not lines[0].strip()):
        lines.pop(0)
    return "\n".join(lines).strip()


def _inline_article(source_md: str) -> str:
    """Read a LIVE derived doc's verbatim source md and return its body for the full-article view.

    Phase 25: the corpus explorer's article-processing screen renders the whole source document
    (the grounded red-flag phrases highlighted → translated). The md (data/<source>/<id>.md) stays
    the single source of truth; the build bakes its body into the offline single-file artifact (no
    runtime fetch), exactly as advisory_full does for the showcase. Fails loud on a missing path.
    """
    if not source_md:
        die("a derived record is missing 'source_md' — cannot inline the full article")
    p = ROOT / source_md
    if not p.exists():
        die(f"source_md not found for the full-article view: {source_md}")
    return _strip_provenance(p.read_text(encoding="utf-8"))


def _load_source(source: dict) -> list:
    """Merge ONE corpus source's committed status manifest with its derived records.

    Reads <source>/corpus-status.json (the extraction manifest) + <source>/derived/*.json (the
    LLM-derived records), merges them by id, and projects to the fields corpus.html renders, with
    the derived indicators attached where a gate-passing record exists. build.py stays decoupled
    from derive_signals.py — it consumes committed data, never imports the tool. Fails loud on a
    missing/invalid manifest or a derived record with no manifest entry (orphan).
    """
    status_path, derived_dir = source["status"], source["derived"]
    rel = status_path.relative_to(ROOT)
    regen = f"python3 scripts/derive_signals.py --corpus-status {status_path.parent.relative_to(ROOT)}"
    if not status_path.exists():
        die(f"corpus status manifest not found: {rel} (run `{regen}`)")
    try:
        manifest = json.loads(status_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as ex:
        die(f"invalid JSON in {rel}: {ex}")
    advisories = manifest.get("advisories")
    if not isinstance(advisories, list) or not advisories:
        die(f"{rel}: 'advisories' must be a non-empty array (regenerate with `{regen}`)")

    # load this source's LLM-derived records by id (sorted glob → deterministic merge)
    derived = {}
    for p in (sorted(derived_dir.glob("*.json")) if derived_dir.exists() else []):
        try:
            rec = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as ex:
            die(f"invalid JSON in derived record {p.name}: {ex}")
        if not rec.get("id"):
            die(f"derived record {p.name} has no 'id'")
        derived[rec["id"]] = rec

    manifest_ids = {a.get("id") for a in advisories if isinstance(a, dict)}
    orphan = sorted(i for i in derived if i not in manifest_ids)
    if orphan:
        die(f"derived record(s) {orphan} in {derived_dir.relative_to(ROOT)} have no entry in "
            f"{rel.name} (regenerate the manifest: `{regen}`)")

    # project to the fields corpus.html renders + attach the derived indicators where present
    merged = []
    for a in advisories:
        if not isinstance(a, dict) or not a.get("id"):
            die(f"{rel}: every advisory needs an id")
        entry = {k: a.get(k) for k in
                 ("id", "advisory", "title", "date", "source", "url", "extraction", "flag_count", "derivable")}
        # Phase 28: the on-screen Source LABEL carries the title only (per the user's compliance call), but
        # the reproduction/copyright clause (" · © …") is preserved as `attribution` so the page FOOTER can
        # render the full licence attribution (© His Majesty… + title + URL) for the document on screen —
        # shown only for the doc being reproduced (FINTRAC's Crown-copyright basis), never for US sources.
        if isinstance(entry.get("source"), str):
            m = re.split(r"\s+·\s+©|\s+©", entry["source"], maxsplit=1)
            entry["source"] = m[0].strip()
            if len(m) > 1:
                entry["attribution"] = "© " + m[1].strip()
        entry["doc_type"] = source["doc_type"]   # honest menu label (Advisory / Alert)
        entry["jurisdiction"] = source["jurisdiction"]   # US / Canada — for cross-corpus grouping
        rec = derived.get(a["id"])
        if rec is not None:
            entry["derived"] = True
            entry["indicators"] = rec.get("indicators")
            # Phase 25 — inline the FULL source article (body only) so the explorer's article-
            # processing screen renders it offline with the grounded phrases highlighted.
            entry["article_text"] = _inline_article(rec.get("source_md"))
        merged.append(entry)
    return merged


def render_corpus(template: str) -> str:
    """Validate + assemble the multi-source corpus dataset and inline it into corpus.html.

    Iterates CORPUS_SOURCES (each one FinCEN publication type — advisories, alerts, …), merging
    each source's committed corpus-status.json + derived/*.json by id (via _load_source) into one
    __CORPUS__, validates the merged derived records at the boundary (validate_corpus_data — fail
    loud), and injects the result. Pure: no disk write, no stdout — the single source of truth for
    what dist/corpus/index.html should contain (shared by build_corpus + check_corpus). build.py
    stays decoupled from derive_signals.py: it consumes committed data, never imports the tool.
    """
    merged = []
    for source in CORPUS_SOURCES:
        merged.extend(_load_source(source))

    errors = validate_corpus_data(merged)
    if errors:
        die(f"corpus data fails boundary validation:\n  - " + "\n  - ".join(errors))

    # Phase 24: overlay the cross-corpus typology onto each live (derived) doc, gated at the boundary.
    vocab, tmap = load_typology_map()
    terrors = validate_typology(merged, vocab, tmap)
    if terrors:
        die("typology overlay fails boundary validation:\n  - " + "\n  - ".join(terrors))
    for entry in merged:
        if entry.get("derived") and entry["id"] in tmap:
            entry["typology"] = tmap[entry["id"]]

    # Phase 29: the capability-lens overlay — labels + group + interview posture per capability/data-source
    # code (the codes already ride in each derived indicator). Gated at the boundary; derived records frozen.
    caps, srcs = load_capability_taxonomy()
    cerrors = validate_capability_taxonomy(merged, caps, srcs)
    if cerrors:
        die("capability taxonomy fails boundary validation:\n  - " + "\n  - ".join(cerrors))

    corpus = {
        "brand": {"title": "Signal Watch", "subtitle": "AML Corpus Explorer · Vision Prototype"},
        "badge": "Illustrative data & outputs",
        "advisories": merged,
        "typologies": vocab,   # closed-vocab typology -> description (for the cross-corpus synthesis view)
        "taxonomy": {"capabilities": caps, "data_sources": srcs},   # Phase 29 — the capability lens
    }

    n = template.count(CORPUS_PLACEHOLDER)
    if n != 1:
        die(f"expected exactly one {CORPUS_PLACEHOLDER} placeholder in corpus.html, found {n}")
    out = template.replace(CORPUS_PLACEHOLDER, json.dumps(corpus, ensure_ascii=False, indent=2))
    if CORPUS_PLACEHOLDER in out:
        die("corpus placeholder survived substitution")
    if "fetch(" in out or "<script src" in out or 'type="module"' in out:
        die("corpus ship file is not self-contained (fetch / external script / ES module present)")
    return out


def build_corpus(template: str) -> None:
    out = render_corpus(template)
    out_dir = ROOT / "dist" / "corpus"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "index.html"
    out_path.write_text(out, encoding="utf-8")
    print(f"build: corpus -> {out_path.relative_to(ROOT)}  ({len(out):,} bytes)")


def check_corpus(template: str) -> bool:
    """Drift guard for the corpus artifact: committed dist/corpus == a fresh render?"""
    out_path = ROOT / "dist" / "corpus" / "index.html"
    rel = out_path.relative_to(ROOT)
    try:
        fresh = render_corpus(template)
    except SystemExit:
        print(f"check: corpus -> FAIL (corpus data no longer renders; cannot reproduce {rel})", file=sys.stderr)
        return False
    if not out_path.exists():
        print(f"check: corpus -> DRIFT (missing built artifact {rel}; run `build.py corpus`)", file=sys.stderr)
        return False
    if out_path.read_text(encoding="utf-8") != fresh:
        print(f"check: corpus -> DRIFT ({rel} differs from a fresh build; run `build.py corpus` and commit)", file=sys.stderr)
        return False
    print(f"check: corpus -> ok ({rel} matches a fresh build)")
    return True


def _news_normalize(text: str) -> str:
    """Position-free quote-grounding key for the news stream — lowercase, keep [a-z0-9] only.

    Mirrors the corpus grounding rule (derive_signals.normalize) so an extracted entity name or a
    red-flag phrase grounds as a substring of its source article regardless of punctuation / wrapping.
    A LOCAL copy on purpose: build.py never imports the authoring layer.
    """
    return re.sub(r"[^a-z0-9]+", "", text.lower())


def _news_article_body(md: str) -> str:
    """Display body for the Read screen: drop the leading markdown `# Title` (it renders as the screen H1)
    and the `*…*` emphasis markers (the .article panel is pre-wrap text, so raw `#`/`*` would show
    literally). Grounding-safe: the entity names + red-flag flags live in the body paragraphs, never the
    title or the italic disclaimer, so both the normalize-substring gate and the raw highlighter still match.
    """
    lines = md.splitlines()
    if lines and lines[0].lstrip().startswith("# "):
        lines = lines[1:]
    return "\n".join(lines).strip().replace("*", "")


def validate_news_data(articles: list, book: dict) -> list:
    """Build-boundary gate for the adverse-media stream. Returns a list of error strings.

    Enforces the FAITHFULNESS invariant (the compliance-load-bearing one): every extracted entity
    name and every red-flag `flag` must quote-ground (normalize-substring) in its source article —
    nothing is shown that isn't in the synthetic source — AND must ground as a RAW substring too, which
    locks the runtime highlighter (it matches raw, so normalize-only grounding would silently fail to
    highlight). Plus shape checks (ids; red_flag present / distinct / bounded) and book referential
    sanity. The near-match / false-positive SEEDING is a demo-quality property the harness asserts (it
    runs the real fuzzy matcher), not here — keeping the build gate free of the matcher (subtraction test).
    """
    e = []
    if not isinstance(articles, list) or not articles:
        return ["news: articles must be a non-empty array"]
    seen = set()
    for a in articles:
        aid = a.get("id", "?")
        if aid in seen:
            e.append(f"news: duplicate article id {aid}")
        seen.add(aid)
        body = a.get("article_text")
        if not body:
            e.append(f"news[{aid}]: missing inlined article_text"); continue
        nbody = _news_normalize(body)
        ents = a.get("entities")
        if not isinstance(ents, list) or not ents:
            e.append(f"news[{aid}]: entities must be a non-empty array")
        else:
            for ent in ents:
                nm = ent.get("name", "")
                if not nm or not ent.get("id") or not ent.get("type"):
                    e.append(f"news[{aid}]: entity missing id/name/type ({ent})")
                elif _news_normalize(nm) not in nbody:
                    e.append(f"news[{aid}]: entity not grounded in article: {nm!r}")
                elif nm not in body:
                    e.append(f"news[{aid}]: entity grounds normalized but not raw (would not highlight): {nm!r}")
                # Phase 32 — the rich entity attributes (location / age / profession) shown on the
                # entity cards must quote-ground too (normalize-substring): nothing on a card that
                # isn't in the source article. Optional per entity; grounded only when present.
                for attr in ("location", "age", "profession"):
                    av = ent.get(attr)
                    if av and _news_normalize(str(av)) not in nbody:
                        e.append(f"news[{aid}]: entity {attr} not grounded in article: {av!r} ({nm})")
        rfs = a.get("red_flags")
        if not isinstance(rfs, list) or not rfs:
            e.append(f"news[{aid}]: red_flags must be a non-empty array")
        else:
            for rf in rfs:
                flag = rf.get("flag", ""); tr = rf.get("red_flag", "")
                if not flag or not rf.get("id"):
                    e.append(f"news[{aid}]: red_flag missing id/flag ({rf})"); continue
                if _news_normalize(flag) not in nbody:
                    e.append(f"news[{aid}]: red-flag not grounded in article: {flag!r}")
                elif flag not in body:
                    e.append(f"news[{aid}]: red-flag grounds normalized but not raw (would not highlight): {flag!r}")
                if not tr or _news_normalize(tr) == _news_normalize(flag):
                    e.append(f"news[{aid}]/{rf.get('id')}: red_flag missing or not distinct from the verbatim flag")
                elif not (MIN_RED_FLAG_CHARS <= len(tr) <= MAX_RED_FLAG_CHARS):
                    e.append(f"news[{aid}]/{rf.get('id')}: red_flag length {len(tr)} outside [{MIN_RED_FLAG_CHARS},{MAX_RED_FLAG_CHARS}]")
    rows = book.get("rows") if isinstance(book, dict) else None
    if not isinstance(rows, list) or not rows:
        e.append("news: book.rows must be a non-empty array")
    else:
        bids = set()
        for r in rows:
            rid = r.get("id")
            if not rid or not r.get("name") or not r.get("type") or not r.get("role"):
                e.append(f"news: book row missing id/name/type/role ({r})")
            if rid in bids:
                e.append(f"news: duplicate book row id {rid}")
            bids.add(rid)
    return e


def load_news() -> tuple:
    """Read the committed synthetic news data: each derived record + its inlined source article + the book."""
    if not NEWS_DERIVED.exists():
        die(f"news derived dir not found: {NEWS_DERIVED.relative_to(ROOT)}")
    articles = []
    for p in sorted(NEWS_DERIVED.glob("*.json")):
        rec = json.loads(p.read_text(encoding="utf-8"))
        src = rec.get("source_md")
        if not src or not (ROOT / src).exists():
            die(f"news record {p.name} has a missing/nonexistent source_md: {src}")
        rec["article_text"] = _news_article_body((ROOT / src).read_text(encoding="utf-8"))
        articles.append(rec)
    if not articles:
        die("no news derived records found under data/news/derived/")
    if not NEWS_BOOK.exists():
        die(f"news book not found: {NEWS_BOOK.relative_to(ROOT)}")
    book = json.loads(NEWS_BOOK.read_text(encoding="utf-8"))
    return articles, book


def render_news(template: str) -> str:
    """Validate + assemble the synthetic news dataset and inline it into news.html. Pure (no disk write)."""
    articles, book = load_news()
    errors = validate_news_data(articles, book)
    if errors:
        die("news data fails boundary validation:\n  - " + "\n  - ".join(errors))
    news = {
        "brand": {"title": "Signal Watch", "subtitle": "Adverse-Media Stream · Vision Prototype"},
        "badge": "Illustrative data & outputs",
        "articles": articles,
        "book": book,
        "match": {"threshold": NEWS_MATCH_THRESHOLD},
    }
    n = template.count(NEWS_PLACEHOLDER)
    if n != 1:
        die(f"expected exactly one {NEWS_PLACEHOLDER} placeholder in news.html, found {n}")
    out = template.replace(NEWS_PLACEHOLDER, json.dumps(news, ensure_ascii=False, indent=2))
    if NEWS_PLACEHOLDER in out:
        die("news placeholder survived substitution")
    if "fetch(" in out or "<script src" in out or 'type="module"' in out:
        die("news ship file is not self-contained (fetch / external script / ES module present)")
    return out


def build_news(template: str) -> None:
    out = render_news(template)
    out_dir = ROOT / "dist" / "news"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "index.html"
    out_path.write_text(out, encoding="utf-8")
    print(f"build: news -> {out_path.relative_to(ROOT)}  ({len(out):,} bytes)")


def check_news(template: str) -> bool:
    """Drift guard for the news artifact: committed dist/news == a fresh render?"""
    out_path = ROOT / "dist" / "news" / "index.html"
    rel = out_path.relative_to(ROOT)
    try:
        fresh = render_news(template)
    except SystemExit:
        print(f"check: news -> FAIL (news data no longer renders; cannot reproduce {rel})", file=sys.stderr)
        return False
    if not out_path.exists():
        print(f"check: news -> DRIFT (missing built artifact {rel}; run `build.py news`)", file=sys.stderr)
        return False
    if out_path.read_text(encoding="utf-8") != fresh:
        print(f"check: news -> DRIFT ({rel} differs from a fresh build; run `build.py news` and commit)", file=sys.stderr)
        return False
    print(f"check: news -> ok ({rel} matches a fresh build)")
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

    # 'corpus' = only the corpus explorer; 'news' = only the adverse-media stream;
    # 'all' = every typology + the corpus + the news stream; else a typology.
    want_corpus = target in ("corpus", "all")
    want_news = target in ("news", "all")
    want_typologies = target not in ("corpus", "news")
    corpus_template = None
    if want_corpus:
        if not CORPUS_TEMPLATE.exists():
            die(f"corpus template not found: {CORPUS_TEMPLATE}")
        corpus_template = CORPUS_TEMPLATE.read_text(encoding="utf-8")
    news_template = None
    if want_news:
        if not NEWS_TEMPLATE.exists():
            die(f"news template not found: {NEWS_TEMPLATE}")
        news_template = NEWS_TEMPLATE.read_text(encoding="utf-8")

    if check:
        # Non-mutating drift guard: committed dist == fresh build? Touches nothing on disk.
        results = []
        if want_typologies:
            results += [check_one(t, template) for t in resolve_targets(target)]
        if want_corpus:
            results.append(check_corpus(corpus_template))
        if want_news:
            results.append(check_news(news_template))
        drifted = results.count(False)
        if drifted:
            die(f"build-drift check FAILED: {drifted}/{len(results)} artifact(s) drifted "
                f"(committed dist != fresh build). Rebuild with `python3 scripts/build.py all` "
                f"and commit the dist.")
        print(f"check: OK — all {len(results)} built artifact(s) match a fresh build (zero drift)")
        return

    if want_typologies:
        for t in resolve_targets(target):
            build_one(t, template)
    if want_corpus:
        build_corpus(corpus_template)
    if want_news:
        build_news(news_template)

    # one-time migration: remove the old single-file M1 layout if present
    stale = ROOT / "dist" / "index.html"
    if stale.exists():
        stale.unlink()
        print(f"build: removed stale {stale.relative_to(ROOT)} (now per-typology dist/<id>/)")


if __name__ == "__main__":
    main()
