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
# Multi-source corpus registry (Phase 20): each source is one FinCEN publication TYPE with its own
# committed corpus-status.json + derived/*.json; render_corpus merges them by id into one __CORPUS__.
# Decoupling source-id from storage dir means adding the Nth FinCEN source (or, later, OFAC — also
# public domain under 17 U.S.C. 105) is a registry entry, not a code change. `doc_type` is the honest
# human label the explorer's menu chip shows per document. The quote-grounding gate (derive_signals.py)
# is source-agnostic; build.py only consumes the committed per-source artifacts.
CORPUS_SOURCES = [
    {"id": "fincen-advisories", "doc_type": "Advisory",
     "status": ROOT / "data" / "fincen" / "corpus-status.json",
     "derived": ROOT / "data" / "fincen" / "derived"},
    {"id": "fincen-alerts", "doc_type": "Alert",
     "status": ROOT / "data" / "fincen-alerts" / "corpus-status.json",
     "derived": ROOT / "data" / "fincen-alerts" / "derived"},
]
# the cover×data build-recommendation vocabulary (mirrors derive_signals.py _REC_MATRIX values;
# re-declared here so build.py's boundary check stays independent of the authoring tool).
BUILD_RECS = {"COVERED", "BUILD_NOW", "BUILD_ENRICH", "SOURCE_DATA", "ENHANCE", "MONITOR"}

STATUS = {"covered", "partial", "gap"}
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
    indicators must each carry a valid status/data and a build_rec in the matrix vocabulary,
    and a BUILD_NOW indicator must carry build_logic with the full definition shape. Traceability
    (every indicator -> a red-flag md line) is the authoring gate's job — run
    `derive_signals.py --check-derived` before committing a derived record.
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
    return e


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
                 ("id", "advisory", "title", "date", "source", "extraction", "flag_count", "derivable")}
        entry["doc_type"] = source["doc_type"]   # honest menu label (Advisory / Alert)
        rec = derived.get(a["id"])
        if rec is not None:
            entry["derived"] = True
            entry["indicators"] = rec.get("indicators")
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

    corpus = {
        "brand": {"title": "Signal Watch", "subtitle": "FinCEN Corpus Explorer · Vision Prototype"},
        "badge": "Illustrative data & outputs",
        "advisories": merged,
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

    # 'corpus' = only the corpus explorer; 'all' = every typology + the corpus; else a typology.
    want_corpus = target in ("corpus", "all")
    want_typologies = target != "corpus"
    corpus_template = None
    if want_corpus:
        if not CORPUS_TEMPLATE.exists():
            die(f"corpus template not found: {CORPUS_TEMPLATE}")
        corpus_template = CORPUS_TEMPLATE.read_text(encoding="utf-8")

    if check:
        # Non-mutating drift guard: committed dist == fresh build? Touches nothing on disk.
        results = []
        if want_typologies:
            results += [check_one(t, template) for t in resolve_targets(target)]
        if want_corpus:
            results.append(check_corpus(corpus_template))
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

    # one-time migration: remove the old single-file M1 layout if present
    stale = ROOT / "dist" / "index.html"
    if stale.exists():
        stale.unlink()
        print(f"build: removed stale {stale.relative_to(ROOT)} (now per-typology dist/<id>/)")


if __name__ == "__main__":
    main()
