#!/usr/bin/env python3
"""Validate a typology config and inline it into index.html -> dist/<id>/index.html.

The ship target is a single self-contained file per typology that runs from file:// —
no server, no fetch, no ES modules. This build (a) validates the config against the
schema at the boundary and fails loud, then (b) injects it at the `__CONFIG__`
placeholder; the engine and styles already live in index.html.

Usage:
    python3 scripts/build.py [typology_id]   # default: fentanyl
    python3 scripts/build.py corpus          # build the FinCEN corpus explorer (dist/corpus/)
    python3 scripts/build.py console         # build the gate console (dist/console/) — Phase 47
    python3 scripts/build.py triage          # build the triage console (dist/triage/) — Phase 49
    python3 scripts/build.py all             # every typology + corpus + news + console + triage
    python3 scripts/build.py --check [all|corpus|news|console|triage|<id>]  # drift guard: committed dist == fresh build?

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

import news_ground  # stdlib grounding primitives shared with the live companion (serve_news.py); NOT the authoring layer

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
# Phase 37: the per-indicator typology overlay — a SEPARATE committed artifact mapping a LIVE indicator
# global-id (<doc-id>/<ind-id>) to ONE closed-vocab typology (data/typology-map.json's vocabulary). SPARSE:
# only indicators whose typology differs from their doc's typology-map value are listed (the deterministic
# corruption/TF sections of the FINTRAC sector-guidance pages, which span many typologies); every other
# indicator INHERITS its doc typology at build time. So a sector page's indicators distribute across the
# real typology clusters instead of collapsing into the doc-level catch-all. Derived records stay byte-frozen
# (the overlay carries the typology, not record edits); validated at the build boundary
# (validate_indicator_typology — closed vocab + referential integrity against the live corpus).
INDICATOR_TYPOLOGY_MAP = ROOT / "data" / "indicator-typology-map.json"
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
# Phase 47: the GATE CONSOLE — the FOURTH standalone single-file ship artifact (its own template +
# the committed divergence dataset data/console/cases.json). Dramatizes the blueprint's Class-J
# human-judgment gate over the REAL Phase-34 C/D-tag divergences. Mirrors the corpus pattern: build.py
# validates the cases at the boundary (load_console_cases + validate_console_cases — referential
# integrity + flag grounding against the CURRENT committed derived records) and inlines at __CONSOLE__.
# Offline, no LLM/fetch; dispositions are session-only in the artifact itself.
CONSOLE_TEMPLATE = ROOT / "console.html"
CONSOLE_PLACEHOLDER = "__CONSOLE__"
# Phase 49: the TRIAGE CONSOLE — the FIFTH standalone single-file ship artifact (its own template +
# the committed SYNTHETIC scenario dataset data/triage/scenarios.json). Dramatizes blueprint §14's
# continuous adjudication loop: history-sourced mini-triage scenarios, graded dispositions, the
# decisions-not-correctness reveal. The dataset is SELF-CONTAINED (rule text + signals + novel
# indicator text embedded at curation by scripts/curate_triage_scenarios.py) — build.py NEVER reads
# data/probe-history. Boundary validation here: closed vocabs, referential integrity (panels/rules),
# the US-federal-only novel stratum verified against the merged corpus + source registry, novel
# indicator text drift-checked against the CURRENT committed derived records. Inlines at __TRIAGE__.
TRIAGE_TEMPLATE = ROOT / "triage.html"
TRIAGE_PLACEHOLDER = "__TRIAGE__"
TRIAGE_SCENARIOS = ROOT / "data" / "triage" / "scenarios.json"

# Phase 76: the MERGE CONSOLE — the SIXTH standalone single-file ship artifact (its own template + the
# committed merge-adjudication dataset data/merge/cases.json, curated by scripts/curate_merge_cases.py).
# Dramatizes the blueprint's Class-J MERGE gate over entity-resolution candidate links: the deterministic
# spine resolves what it can and REFUSES the ambiguous; the human adjudicates the residual. The dataset is
# SELF-CONTAINED (Phase 79: TWO SCORED populations — real-substrate candidate SHARES scored against substrate's
# OWN anchored GT- oracle + hand-authored synthetic scored cases, each carrying a latent-truth oracle) —
# build.py NEVER imports the spine/scorer/curate (the companion firewall);
# it loads the committed JSON + validates the shape at the boundary (closed vocab + referential integrity +
# the resolver-input firewall: the pre-adjudication evidence carries NO latent-truth field). Inlines at
# __MERGE__. Offline, no LLM/fetch; adjudications are session-only in the artifact itself.
MERGE_TEMPLATE = ROOT / "merge.html"
MERGE_PLACEHOLDER = "__MERGE__"
MERGE_CASES = ROOT / "data" / "merge" / "cases.json"
# the closed merge vocabularies (defined HERE — build.py must not import the curate companion that owns the
# authoring copy; the two are independent by the firewall, like TRIAGE_STRATA mirrors curate_triage's set).
MERGE_GRADE_IDS = frozenset({"uphold_merge", "reject_as_shares", "both_defensible", "escalate"})
MERGE_BASIS_IDS = frozenset({"strong", "weak", "name"})
# Phase 80 added "substrate-sanctions-slice" (the OFAC name-collision class). The two substrate-derived
# sources share the synthetic-substrate qualifier + the masking firewall (MERGE_SUBSTRATE_SOURCES).
MERGE_SOURCES = frozenset({"substrate-anchored-slice", "substrate-sanctions-slice", "synthetic-oracle"})
MERGE_SUBSTRATE_SOURCES = frozenset({"substrate-anchored-slice", "substrate-sanctions-slice"})
# fields that would LEAK the latent truth into the pre-adjudication evidence — forbidden on a case's a/b.
# Kept in EXACT parity with curate_merge_cases._TRUTH_LEAK_KEYS (incl. free-text `note`, the natural place a
# truth annotation would hide) — the shipping firewall must never be weaker than the authoring one.
MERGE_TRUTH_LEAK_KEYS = ("cluster", "same_entity", "correct_adjudication", "klass", "note", "oracle")
# Phase 79 supersede: BOTH populations are scored; each carries an oracle qualified by provenance (the
# real-substrate population scored against substrate's OWN anchored GT- oracle, synthetic against true_entities).
MERGE_SYNTHETIC_QUALIFIER = "measured on synthetic clusters; production has no ground truth"
MERGE_SUBSTRATE_QUALIFIER = "measured on a synthetic aml-substrate slice; production has no ground truth"

# Phase 55: the launcher — the single front door (dist/index.html, the 8th build target). It links
# the 5 existing offline artifacts (byte-frozen) + inlines the committed cross-pillar bridge state
# (data/pillar-status.json, regenerated by scripts/e2e_chain_check.py) at __STATUS__. NON-engine data.
LAUNCHER_TEMPLATE = ROOT / "launcher.html"
LAUNCHER_PLACEHOLDER = "__STATUS__"
PILLAR_STATUS = ROOT / "data" / "pillar-status.json"
TRIAGE_STRATA = ["history-signal-fired", "history-below-the-line", "synthetic-novel",
                 "random-population"]
TRIAGE_GRAMMAR = ["confirm-risk", "confirm-no-risk", "both-defensible", "escalate",
                  "need-more-info", "no-defensible-option"]
TRIAGE_HISTORY_DISPOSITIONS = ["dismissed", "escalated", "sar_filed", "data_requested"]
NEWS_DERIVED = ROOT / "data" / "news" / "derived"
NEWS_BOOK = ROOT / "data" / "news" / "book.json"
NEWS_MATCH_THRESHOLD = 0.85  # fuzzy-match surface threshold (shared by the ship artifact + the harness)
# Phase 35: the companion-only LIVE-MODE region in news.html — STRIPPED for the offline ship build so the
# single-file dist/news keeps ZERO network code (the live branch is served only by scripts/serve_news.py).
# The pattern eats the leading newline so the strip yields the pre-live bytes exactly (drift guard pins it).
LIVE_REGION_RE = re.compile(r"\n[ \t]*/\*LIVE_START\*/.*?/\*LIVE_END\*/", re.S)

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


def load_indicator_typology_map() -> dict:
    """Load + shape-check the per-indicator typology overlay (data/indicator-typology-map.json).

    Returns mapping: dict[str, str] keyed by indicator global-id "<doc-id>/<ind-id>". Fails loud on a
    missing/invalid file or a malformed shape. SEPARATE committed artifact (the derived records stay
    byte-frozen); referential integrity + closed-vocab are checked in validate_indicator_typology once
    the merged corpus is known. The overlay is SPARSE (override-only) — coverage is NOT required, since
    unlisted indicators inherit their doc typology.
    """
    rel = INDICATOR_TYPOLOGY_MAP.relative_to(ROOT)
    if not INDICATOR_TYPOLOGY_MAP.exists():
        die(f"indicator typology overlay not found: {rel}")
    try:
        doc = json.loads(INDICATOR_TYPOLOGY_MAP.read_text(encoding="utf-8"))
    except json.JSONDecodeError as ex:
        die(f"invalid JSON in {rel}: {ex}")
    mapping = doc.get("map")
    if not isinstance(mapping, dict) or not mapping:
        die(f"{rel}: 'map' must be a non-empty object {{'<doc-id>/<ind-id>': typology}}")
    return mapping


def validate_indicator_typology(advisories: list, vocab: dict, imap: dict) -> list:
    """Boundary check on the per-indicator typology overlay against the merged corpus. Returns errors.

    Two deterministic checks (mirrors validate_typology; the overlay is agent/section-proposed, this
    disposes — the grounding gate derive_signals.py stays untouched):
      1. closed vocab — every mapped typology is a declared typology-map vocabulary term;
      2. referential  — every mapped key is a LIVE (derived) indicator global-id "<doc>/<ind>" (no dangling).
    Coverage is NOT required: the overlay is an override; unlisted indicators inherit their doc typology.
    """
    e = []
    live = set()
    for a in advisories:
        if not a.get("derived"):
            continue
        for i in a.get("indicators") or []:
            live.add(f"{a.get('id', '?')}/{i.get('id', '?')}")
    for key, typ in imap.items():
        if typ not in vocab:
            e.append(f"{key}: typology {typ!r} not in the declared vocabulary")
        if key not in live:
            e.append(f"{key}: mapped key is not a live (derived) corpus indicator")
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


# Phase 47: the gate-console adjudication dataset — REAL rater-A/rater-B C/D-tag divergence cases
# curated deterministically from the Phase-34 correction (scripts/curate_console_cases.py regenerates;
# the committed artifact is the authority — validation NEVER depends on git history). A SEPARATE
# committed artifact (the derived records stay byte-frozen); validated at the build boundary
# (validate_console_cases — referential integrity + flag grounding against the CURRENT committed
# derived records + closed C/D vocab + the FINTRAC attribution rule).
CONSOLE_CASES = ROOT / "data" / "console" / "cases.json"


def load_console_cases() -> list:
    """Load + shape-check the gate-console adjudication dataset (data/console/cases.json).

    Returns cases: list[dict]. Fails loud on a missing/invalid file or a malformed shape (mirrors
    load_typology_map). Referential integrity against the live corpus + the taxonomy is checked in
    validate_console_cases once the merged corpus is known.
    """
    rel = CONSOLE_CASES.relative_to(ROOT)
    if not CONSOLE_CASES.exists():
        die(f"console cases dataset not found: {rel} (regenerate: `python3 scripts/curate_console_cases.py`)")
    try:
        doc = json.loads(CONSOLE_CASES.read_text(encoding="utf-8"))
    except json.JSONDecodeError as ex:
        die(f"invalid JSON in {rel}: {ex}")
    cases = doc.get("cases")
    if not isinstance(cases, list) or not cases:
        die(f"{rel}: 'cases' must be a non-empty array of adjudication cases")
    return cases


def validate_console_cases(cases: list, advisories: list, caps: list, srcs: list) -> list:
    """Boundary check on the gate-console adjudication dataset against the merged corpus. Returns errors.

    The build-boundary GATE for the console dataset (curated from history, this disposes against the
    PRESENT — validation never consults git; mirrors validate_capability_taxonomy):
      1. referential   — every case's doc_id is a LIVE (derived) corpus doc and its indicator_id exists
                         in that doc (no dangling case); case ids unique;
      2. flag grounding — the case's quoted flag is byte-equal to (or an exact substring of) that
                         indicator's CURRENT committed flag (no paraphrase, no drift);
      3. closed vocab  — rater_a/rater_b capability + data_source codes are declared taxonomy ids;
      4. attribution   — a Canada-jurisdiction (FINTRAC) case carries non-empty {title, url} matching
                         the doc's manifest entry; a US public-domain case carries NO attribution
                         (mirrors the corpus footer rule);
      5. provenance    — no case references an uncommitted path (.dev-wiki / tmp scratch).
    """
    e = []
    cap_ids = {x.get("id") for x in caps}
    src_ids = {x.get("id") for x in srcs}
    docs = {a["id"]: a for a in advisories if a.get("derived") and a.get("id")}
    seen = set()
    for c in cases:
        cid = c.get("id", "?")
        if not c.get("id"):
            e.append("a case is missing id")
        elif cid in seen:
            e.append(f"{cid}: case id repeated")
        seen.add(cid)
        if c.get("changed") not in {"C", "D", "both"}:
            e.append(f"{cid}: changed axis {c.get('changed')!r} not in ['C', 'D', 'both']")
        doc = docs.get(c.get("doc_id"))
        if doc is None:
            e.append(f"{cid}: doc_id {c.get('doc_id')!r} is not a live (derived) corpus document")
            continue
        ind = next((i for i in doc.get("indicators") or [] if i.get("id") == c.get("indicator_id")), None)
        if ind is None:
            e.append(f"{cid}: indicator {c.get('indicator_id')!r} not in {c.get('doc_id')}")
            continue
        flag = c.get("flag")
        if not (isinstance(flag, str) and flag and isinstance(ind.get("flag"), str) and flag in ind["flag"]):
            e.append(f"{cid}: flag is not grounded in the indicator's CURRENT committed flag")
        for rater in ("rater_a", "rater_b"):
            r = c.get(rater)
            if not isinstance(r, dict):
                e.append(f"{cid}: missing {rater}")
                continue
            if r.get("capability") not in cap_ids:
                e.append(f"{cid}: {rater} capability {r.get('capability')!r} not in the taxonomy")
            if r.get("data_source") not in src_ids:
                e.append(f"{cid}: {rater} data_source {r.get('data_source')!r} not in the taxonomy")
        attr = c.get("attribution")
        if doc.get("jurisdiction") == "Canada":
            if not (isinstance(attr, dict) and (attr.get("title") or "").strip() and (attr.get("url") or "").strip()):
                e.append(f"{cid}: FINTRAC-sourced case missing non-empty attribution {{title, url}}")
            else:
                if attr["title"] != doc.get("title"):
                    e.append(f"{cid}: attribution title differs from the doc's manifest title")
                if attr["url"] != doc.get("url"):
                    e.append(f"{cid}: attribution url differs from the doc's manifest url")
        elif attr is not None:
            e.append(f"{cid}: US public-domain case must carry no attribution (footer rule)")
        if ".dev-wiki" in json.dumps(c):
            e.append(f"{cid}: case references an uncommitted path (.dev-wiki)")
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

    Phase 46: STRIP the companion-only live-mode region first (the news Phase-35 mechanism), so the
    offline ship file keeps zero network code (the self-contained guard below then holds). The live
    branch is served only by serve_corpus.py.
    """
    template = LIVE_REGION_RE.sub("", template)
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

    # Phase 37: resolve each LIVE indicator's typology = the per-indicator overlay value ELSE inherit the
    # doc typology. So a FINTRAC sector page (multi-typology) contributes its corruption/TF indicators to
    # those real clusters while its generic indicators stay under the doc's headline typology — the
    # Typologies lens groups by indicator, not doc. Gated at the boundary; derived records stay frozen.
    imap = load_indicator_typology_map()
    ierrors = validate_indicator_typology(merged, vocab, imap)
    if ierrors:
        die("indicator typology overlay fails boundary validation:\n  - " + "\n  - ".join(ierrors))
    for entry in merged:
        if not entry.get("derived"):
            continue
        for i in entry.get("indicators") or []:
            i["typology"] = imap.get(f"{entry['id']}/{i.get('id', '?')}", entry.get("typology"))

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


# Phase 35: the news grounding PRIMITIVES now live in scripts/news_ground.py (stdlib), SHARED with the
# live companion (serve_news.py) so live grounding == build grounding by construction. news_ground is
# pure string grounding (normalize + the article-body transform), NOT the authoring/LLM layer — build.py
# still imports no derive_signals / markitdown / LLM client. Behavior is byte-identical to the prior
# local copies (the --check news drift guard pins this).
_news_normalize = news_ground.news_normalize
_news_article_body = news_ground.article_body


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
            seen_flag_keys = set()  # Phase 40: duplicate-flag CHECK (same quote + category) — fail loud, never rewrite
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
                key = news_ground.flag_dup_key(rf)
                if key in seen_flag_keys:
                    e.append(f"news[{aid}]/{rf.get('id')}: duplicate flag (same quote + category)")
                seen_flag_keys.add(key)
        # Phase 41 — enriched identity fields (OPTIONAL; the 4 committed records carry none yet).
        # CHECK mode mirrors news_ground.ground_record's live DROP rules: fail loud, never rewrite.
        # Aliases RAW-ground like names; property values normalize-ground (the attribute precedent);
        # relationship labels/kinds are vocab-checked against the news_ground single authority.
        if isinstance(ents, list):
            for ent in ents:
                nm = ent.get("name", "")
                for al in ent.get("aliases") or []:
                    if al not in body:
                        e.append(f"news[{aid}]: alias not raw-grounded in article: {al!r} ({nm})")
                for p in ent.get("properties") or []:
                    kind, val = (p or {}).get("kind"), (p or {}).get("value", "")
                    if kind not in news_ground.PROPERTY_KINDS:
                        e.append(f"news[{aid}]: unknown property kind {kind!r} ({nm})")
                    elif not val or _news_normalize(str(val)) not in nbody:
                        e.append(f"news[{aid}]: property value not grounded: {kind}={val!r} ({nm})")
            ent_names = {ent.get("name") for ent in ents}
            for r in a.get("relationships") or []:
                if r.get("label") not in news_ground.RELATION_LABELS:
                    e.append(f"news[{aid}]: unknown relation label {r.get('label')!r}")
                if r.get("from") not in ent_names or r.get("to") not in ent_names or r.get("from") == r.get("to"):
                    e.append(f"news[{aid}]: relationship references a non-extracted entity or itself "
                             f"({r.get('from')!r}->{r.get('to')!r})")
                ev = r.get("evidence", "")
                if not ev or ev not in body:
                    e.append(f"news[{aid}]: relationship evidence not raw-grounded: {ev!r}")
            for s in a.get("main_subjects") or []:
                if s not in ent_names:
                    e.append(f"news[{aid}]: main_subject is not an extracted entity: {s!r}")
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
    """Validate + assemble the synthetic news dataset and inline it into news.html. Pure (no disk write).

    Phase 35: STRIP the companion-only live-mode region first, so the offline ship file keeps zero network
    code (the self-contained guard below then holds). The live branch is served only by serve_news.py.
    """
    template = LIVE_REGION_RE.sub("", template)
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


def render_console(template: str) -> str:
    """Validate + assemble the gate-console adjudication dataset and inline it into console.html.

    Phase 47: loads the committed divergence cases (load_console_cases), gates them at the build
    boundary against the CURRENT merged corpus + capability taxonomy (validate_console_cases — fail
    loud), then DERIVES the adjudicated rater from the data: rater_b must equal the CURRENT committed
    indicator's C/D codes for every case (the dataset's contract that B is the post-adjudication
    state is verified, never assumed — the console's reveal copy depends on it). Pure: no disk
    write — the single source of truth for dist/console/index.html (shared by build/check).
    """
    merged = []
    for source in CORPUS_SOURCES:
        merged.extend(_load_source(source))
    caps, srcs = load_capability_taxonomy()
    cases = load_console_cases()
    errors = validate_console_cases(cases, merged, caps, srcs)
    if errors:
        die("console cases fail boundary validation:\n  - " + "\n  - ".join(errors))

    # Derive (verify) the adjudicated rater: every case's rater_b == the CURRENT committed codes.
    docs = {a["id"]: a for a in merged if a.get("derived")}
    for c in cases:
        ind = next(i for i in docs[c["doc_id"]]["indicators"] if i.get("id") == c["indicator_id"])
        rb = c["rater_b"]
        if rb.get("capability") != ind.get("capability") or rb.get("data_source") != ind.get("data_source"):
            die(f"console case {c['id']}: rater_b does not match the CURRENT committed C/D codes "
                f"— cannot derive the adjudicated record (the reveal would misattribute history)")

    # Only the docs the cases reference ride along (title for the queue/evidence, jurisdiction for
    # the footer-attribution rule) — sorted for a deterministic payload.
    case_doc_ids = sorted({c["doc_id"] for c in cases})
    doc_meta = {d: {"title": docs[d].get("title"), "doc_type": docs[d].get("doc_type"),
                    "jurisdiction": docs[d].get("jurisdiction")} for d in case_doc_ids}

    payload = {
        "brand": {"title": "Signal Watch", "subtitle": "Gate Console · Vision Prototype"},
        "badge": "Illustrative data & outputs",
        "adjudicated": "b",   # verified against the committed corpus above, per case
        "cases": cases,
        "taxonomy": {"capabilities": caps, "data_sources": srcs},
        "docs": doc_meta,
    }
    n = template.count(CONSOLE_PLACEHOLDER)
    if n != 1:
        die(f"expected exactly one {CONSOLE_PLACEHOLDER} placeholder in console.html, found {n}")
    out = template.replace(CONSOLE_PLACEHOLDER, json.dumps(payload, ensure_ascii=False, indent=2))
    if CONSOLE_PLACEHOLDER in out:
        die("console placeholder survived substitution")
    if "fetch(" in out or "<script src" in out or 'type="module"' in out:
        die("console ship file is not self-contained (fetch / external script / ES module present)")
    return out


def build_console(template: str) -> None:
    out = render_console(template)
    out_dir = ROOT / "dist" / "console"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "index.html"
    out_path.write_text(out, encoding="utf-8")
    print(f"build: console -> {out_path.relative_to(ROOT)}  ({len(out):,} bytes)")


def check_console(template: str) -> bool:
    """Drift guard for the gate-console artifact: committed dist/console == a fresh render?"""
    out_path = ROOT / "dist" / "console" / "index.html"
    rel = out_path.relative_to(ROOT)
    try:
        fresh = render_console(template)
    except SystemExit:
        print(f"check: console -> FAIL (console data no longer renders; cannot reproduce {rel})", file=sys.stderr)
        return False
    if not out_path.exists():
        print(f"check: console -> DRIFT (missing built artifact {rel}; run `build.py console`)", file=sys.stderr)
        return False
    if out_path.read_text(encoding="utf-8") != fresh:
        print(f"check: console -> DRIFT ({rel} differs from a fresh build; run `build.py console` and commit)", file=sys.stderr)
        return False
    print(f"check: console -> ok ({rel} matches a fresh build)")
    return True


def load_triage_scenarios() -> dict:
    """Load + shape-check the triage-console scenario dataset (data/triage/scenarios.json).

    Phase 49: the dataset is curated deterministically from the SYNTHETIC probe history by
    scripts/curate_triage_scenarios.py (authoring-time only) and is SELF-CONTAINED — rules,
    panels, and novel indicator text are embedded, so this loader never touches
    data/probe-history. Deep validation happens in validate_triage_scenarios once the merged
    corpus is known (the novel stratum is verified against the CURRENT committed records).
    """
    rel = TRIAGE_SCENARIOS.relative_to(ROOT)
    if not TRIAGE_SCENARIOS.exists():
        die(f"triage scenario dataset not found: {rel} "
            f"(regenerate: `python3 scripts/curate_triage_scenarios.py`)")
    try:
        data = json.loads(TRIAGE_SCENARIOS.read_text(encoding="utf-8"))
    except json.JSONDecodeError as ex:
        die(f"invalid JSON in {rel}: {ex}")
    for key in ("meta", "rules", "panels", "scenarios"):
        if key not in data:
            die(f"{rel}: missing top-level '{key}'")
    if not isinstance(data["scenarios"], list) or not data["scenarios"]:
        die(f"{rel}: 'scenarios' must be a non-empty array")
    return data


def validate_triage_scenarios(data: dict, advisories: list, caps: list, srcs: list) -> list:
    """Boundary check on the triage scenario dataset. Returns errors (render dies on any).

    Checks: synthetic meta flag; closed vocabs (strata, disposition grammar, history
    dispositions); referential integrity (panel + rule refs, unique ids, fired_rule field
    universal); seeded-instrumentation floor (≥1 divergent shared-panel pair, ≥3 controls,
    ≥4 labeled second-rater seeds, all strata populated, ≤20 scenarios); the synthetic-novel
    stratum quotes US-FEDERAL committed docs only (jurisdiction from the source registry via
    the merged corpus) with flag/red_flag/C/D byte-equal to the CURRENT committed indicator
    (dataset drift fails the build loudly — the console precedent).
    """
    errors = []
    cap_ids = {c["id"] for c in caps}
    src_ids = {d["id"] for d in srcs}
    if data["meta"].get("synthetic") is not True:
        errors.append("meta.synthetic must be true (everything in this artifact is synthetic)")
    rules = data["rules"]
    panels = data["panels"]
    scenarios = data["scenarios"]
    if len(scenarios) > 20:
        errors.append(f"{len(scenarios)} scenarios exceed the 20-scenario ceiling")
    for rid, rule in rules.items():
        sig = rule.get("signal", {})
        if sig.get("capability") not in cap_ids:
            errors.append(f"rule {rid}: signal capability {sig.get('capability')!r} not in taxonomy")
        if sig.get("data_source") not in src_ids:
            errors.append(f"rule {rid}: signal data_source {sig.get('data_source')!r} not in taxonomy")
        for key in ("title", "logic", "indicator"):
            if not rule.get(key):
                errors.append(f"rule {rid}: missing {key}")
    docs = {a["id"]: a for a in advisories if a.get("derived")}
    seen = set()
    panel_disp = {}
    for sc in scenarios:
        sid = sc.get("id", "<missing>")
        if sid in seen:
            errors.append(f"duplicate scenario id {sid}")
        seen.add(sid)
        if sc.get("stratum") not in TRIAGE_STRATA:
            errors.append(f"{sid}: stratum {sc.get('stratum')!r} not in the closed vocab")
        if sc.get("panel") not in panels:
            errors.append(f"{sid}: dangling panel ref {sc.get('panel')!r}")
        if "fired_rule" not in sc:
            errors.append(f"{sid}: fired_rule field missing (must be present, possibly null)")
        for key in ("fired_rule", "below_rule"):
            if sc.get(key) is not None and sc[key] not in rules:
                errors.append(f"{sid}: {key} {sc[key]!r} not in the embedded rules block")
        h = sc.get("history")
        if h is not None:
            if h.get("disposition") not in TRIAGE_HISTORY_DISPOSITIONS:
                errors.append(f"{sid}: history disposition {h.get('disposition')!r} off-vocab")
            else:
                panel_disp.setdefault(sc.get("panel"), set()).add(h["disposition"])
        sr = sc.get("second_rater")
        if sr is not None:
            if "synthetic" not in sr.get("label", "").lower():
                errors.append(f"{sid}: second_rater label must declare itself synthetic")
            if sr.get("disposition") not in TRIAGE_GRAMMAR:
                errors.append(f"{sid}: second_rater disposition {sr.get('disposition')!r} off-grammar")
            info = sr.get("info_needed")
            if info and info.get("data_source") not in src_ids:
                errors.append(f"{sid}: info_needed data_source {info.get('data_source')!r} not in taxonomy")
        ctl = sc.get("control")
        if ctl is not None and ctl.get("known_disposition") not in TRIAGE_GRAMMAR:
            errors.append(f"{sid}: control known_disposition {ctl.get('known_disposition')!r} off-grammar")
        nv = sc.get("novel_source")
        if nv is not None:
            doc = docs.get(nv.get("doc_id"))
            if doc is None:
                errors.append(f"{sid}: novel_source doc {nv.get('doc_id')!r} not in the merged corpus")
            elif doc.get("jurisdiction") != "US":
                errors.append(f"{sid}: novel_source doc {nv['doc_id']} is not US-federal "
                              f"(jurisdiction {doc.get('jurisdiction')!r}) — the novel stratum is US-only")
            else:
                ind = next((i for i in doc["indicators"] if i.get("id") == nv.get("indicator_id")), None)
                if ind is None:
                    errors.append(f"{sid}: novel_source indicator {nv.get('indicator_id')!r} "
                                  f"not in {nv['doc_id']}'s CURRENT committed record")
                else:
                    for key in ("flag", "red_flag", "capability", "data_source"):
                        if nv.get(key) != ind.get(key):
                            errors.append(f"{sid}: novel_source {key} drifted from the CURRENT "
                                          f"committed indicator {nv['doc_id']}/{nv['indicator_id']} "
                                          f"— regenerate the dataset")
    if not any(len(v) > 1 for v in panel_disp.values()):
        errors.append("no divergent-disposition pair shares a panel "
                      "(the seeded process inconsistency is required)")
    if sum(1 for sc in scenarios if sc.get("control")) < 3:
        errors.append("fewer than 3 known-disposition control scenarios")
    if sum(1 for sc in scenarios if sc.get("second_rater")) < 4:
        errors.append("fewer than 4 labeled second-rater seeds")
    missing_strata = set(TRIAGE_STRATA) - {sc.get("stratum") for sc in scenarios}
    if missing_strata:
        errors.append(f"strata not all populated: missing {sorted(missing_strata)}")
    return errors


def render_triage(template: str) -> str:
    """Validate + assemble the triage scenario dataset and inline it into triage.html.

    Pure: no disk write — the single source of truth for dist/triage/index.html (shared by
    build/check). The merged corpus is loaded only to verify the novel stratum against the
    CURRENT committed records; nothing from the corpus beyond the validated dataset rides
    into the payload.
    """
    merged = []
    for source in CORPUS_SOURCES:
        merged.extend(_load_source(source))
    caps, srcs = load_capability_taxonomy()
    data = load_triage_scenarios()
    errors = validate_triage_scenarios(data, merged, caps, srcs)
    if errors:
        die("triage scenarios fail boundary validation:\n  - " + "\n  - ".join(errors))

    payload = {
        "brand": {"title": "Signal Watch", "subtitle": "Triage Console · Vision Prototype"},
        "badge": "Illustrative data & outputs",
        "taxonomy": {"capabilities": caps, "data_sources": srcs},
        "triage": data,
    }
    n = template.count(TRIAGE_PLACEHOLDER)
    if n != 1:
        die(f"expected exactly one {TRIAGE_PLACEHOLDER} placeholder in triage.html, found {n}")
    out = template.replace(TRIAGE_PLACEHOLDER, json.dumps(payload, ensure_ascii=False, indent=2))
    if TRIAGE_PLACEHOLDER in out:
        die("triage placeholder survived substitution")
    if "fetch(" in out or "<script src" in out or 'type="module"' in out:
        die("triage ship file is not self-contained (fetch / external script / ES module present)")
    return out


def build_triage(template: str) -> None:
    out = render_triage(template)
    out_dir = ROOT / "dist" / "triage"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "index.html"
    out_path.write_text(out, encoding="utf-8")
    print(f"build: triage -> {out_path.relative_to(ROOT)}  ({len(out):,} bytes)")


def check_triage(template: str) -> bool:
    """Drift guard for the triage-console artifact: committed dist/triage == a fresh render?"""
    out_path = ROOT / "dist" / "triage" / "index.html"
    rel = out_path.relative_to(ROOT)
    try:
        fresh = render_triage(template)
    except SystemExit:
        print(f"check: triage -> FAIL (triage data no longer renders; cannot reproduce {rel})", file=sys.stderr)
        return False
    if not out_path.exists():
        print(f"check: triage -> DRIFT (missing built artifact {rel}; run `build.py triage`)", file=sys.stderr)
        return False
    if out_path.read_text(encoding="utf-8") != fresh:
        print(f"check: triage -> DRIFT ({rel} differs from a fresh build; run `build.py triage` and commit)", file=sys.stderr)
        return False
    print(f"check: triage -> ok ({rel} matches a fresh build)")
    return True


def load_merge_cases() -> dict:
    """Load + shape-check the merge-adjudication dataset (data/merge/cases.json).

    Phase 76: curated deterministically by scripts/curate_merge_cases.py (authoring-time only) and
    SELF-CONTAINED — real candidate SHARES (the v0.5 over-merge-refused residual, consensus, no oracle)
    + synthetic scored cases (a latent-truth oracle). This loader never touches the spine/scorer/slice;
    deep validation happens in validate_merge_cases.
    """
    rel = MERGE_CASES.relative_to(ROOT)
    if not MERGE_CASES.exists():
        die(f"merge dataset not found: {rel} (regenerate: `.venv/bin/python scripts/curate_merge_cases.py`)")
    try:
        data = json.loads(MERGE_CASES.read_text(encoding="utf-8"))
    except json.JSONDecodeError as ex:
        die(f"invalid JSON in {rel}: {ex}")
    if not isinstance(data.get("cases"), list) or not data["cases"]:
        die(f"{rel}: 'cases' must be a non-empty array")
    return data


def validate_merge_cases(data: dict) -> list:
    """Boundary check on the merge dataset. Returns errors (render dies on any). STANDALONE — build.py
    must not import the curate companion that owns the authoring-side copy (the firewall); this validates
    the COMMITTED shape only.

    Checks: badge; the closed adjudication-grade + basis vocabularies; per-case referential integrity
    (unique ids, valid basis/source/spine_verdict, a/b each carry ref+name); THE RESOLVER-INPUT FIREWALL
    translated to the ship artifact (the pre-adjudication evidence a/b carries NO latent-truth field; the
    truth rides ONLY each scored case's `oracle` block, revealed post-adjudication); the Phase-79 supersede —
    BOTH populations are SCORED (the real-substrate population scored against substrate's OWN anchored GT-
    oracle, the synthetic against true_entities), each oracle's correct_adjudication follows same_entity and
    carries its provenance qualifier (synthetic-substrate / synthetic-only); the provenance counts agree.
    """
    errors = []
    if data.get("badge") != "Illustrative data & outputs":
        errors.append("badge must be 'Illustrative data & outputs'")
    grade_ids = {g.get("id") for g in data.get("adjudication_grades") or []}
    if grade_ids != set(MERGE_GRADE_IDS):
        errors.append(f"adjudication_grades must be exactly {sorted(MERGE_GRADE_IDS)}; got {sorted(grade_ids)}")
    basis_ids = {b.get("id") for b in data.get("bases") or []}
    if basis_ids != set(MERGE_BASIS_IDS):
        errors.append(f"bases must be exactly {sorted(MERGE_BASIS_IDS)}; got {sorted(basis_ids)}")
    correct_of = {True: "uphold_merge", False: "reject_as_shares"}
    seen, n_substrate, n_sanctions, n_syn = set(), 0, 0, 0
    for c in data.get("cases", []):
        cid = c.get("id")
        if not cid:
            errors.append("a case is missing an id"); continue
        if cid in seen:
            errors.append(f"duplicate case id {cid!r}")
        seen.add(cid)
        if c.get("basis") not in MERGE_BASIS_IDS:
            errors.append(f"{cid}: basis {c.get('basis')!r} not in {sorted(MERGE_BASIS_IDS)}")
        if c.get("spine_verdict") not in ("merged", "kept_distinct"):
            errors.append(f"{cid}: spine_verdict {c.get('spine_verdict')!r} invalid")
        for side in ("a", "b"):
            s = c.get(side)
            if not isinstance(s, dict) or not s.get("ref") or not s.get("name"):
                errors.append(f"{cid}.{side}: needs at least ref + name"); continue
            leak = [k for k in MERGE_TRUTH_LEAK_KEYS if k in s]
            if leak:
                errors.append(f"{cid}.{side}: resolver-input firewall — evidence carries truth field(s) {leak}")
        src, scored, oracle = c.get("source"), c.get("scored"), c.get("oracle")
        if src not in MERGE_SOURCES:
            errors.append(f"{cid}: source {src!r} not in {sorted(MERGE_SOURCES)}")
        else:
            # ALL populations are SCORED — each carries an oracle, qualified by provenance (the two substrate
            # sources share the synthetic-substrate qualifier; the hand-authored set the synthetic-only one).
            want_qual = MERGE_SUBSTRATE_QUALIFIER if src in MERGE_SUBSTRATE_SOURCES else MERGE_SYNTHETIC_QUALIFIER
            if scored is not True:
                errors.append(f"{cid}: a scored case must have scored=true")
            if not isinstance(oracle, dict):
                errors.append(f"{cid}: a scored case must carry an oracle block")
            else:
                if not isinstance(oracle.get("same_entity"), bool):
                    errors.append(f"{cid}: oracle.same_entity must be a bool")
                if oracle.get("correct_adjudication") not in MERGE_GRADE_IDS:
                    errors.append(f"{cid}: oracle.correct_adjudication not in the grade vocab")
                elif oracle.get("correct_adjudication") != correct_of.get(oracle.get("same_entity")):
                    errors.append(f"{cid}: oracle.correct_adjudication must follow same_entity")
                if oracle.get("qualifier") != want_qual:
                    errors.append(f"{cid}: scored case must carry its provenance qualifier "
                                  f"({'synthetic-substrate' if src in MERGE_SUBSTRATE_SOURCES else 'synthetic-only'})")
            if src in MERGE_SUBSTRATE_SOURCES:
                # both substrate populations are demoted-spine refused + masked — enforce at the SHIP boundary
                # (mirrors curate_merge_cases.validate; the shipping firewall must never be weaker — catches a hand-edit)
                if c.get("spine_verdict") != "kept_distinct":
                    errors.append(f"{cid}: substrate cases are demoted-spine refused (spine_verdict=kept_distinct)")
                sh = c.get("shared") or {}
                if sh.get("kind") == "email" and not str(sh.get("value") or "").endswith("@example.test"):
                    errors.append(f"{cid}: a shipped substrate email must be domain-masked to example.test")
            if src == "substrate-anchored-slice":
                n_substrate += 1
                # the anchored population is the DEMOTED-spine refused residual over strong-shared ids
                if c.get("basis") != "strong":
                    errors.append(f"{cid}: substrate candidate SHARES are strong-shared-id (basis=strong)")
            elif src == "substrate-sanctions-slice":
                n_sanctions += 1
                # the OFAC name-collision class spans the strong + name bases; >=1 side carries the watchlist flag
                if c.get("basis") not in ("strong", "name"):
                    errors.append(f"{cid}: sanctions cases span the strong + name bases (basis in strong|name)")
                flagged = [s for s in (c.get("a"), c.get("b"))
                           if isinstance(s, dict) and (s.get("sanctions_screen") or {}).get("flagged")]
                if not flagged:
                    errors.append(f"{cid}: a sanctions case needs >=1 watchlist-flagged side (sanctions_screen.flagged)")
            else:
                n_syn += 1
        if c.get("basis") in ("strong", "weak") and not (c.get("shared") and c["shared"].get("kind")):
            errors.append(f"{cid}: a {c.get('basis')} basis needs a shared identifier")
        if c.get("basis") == "name" and c.get("shared"):
            errors.append(f"{cid}: a name-only basis must have no shared identifier")
    if n_substrate == 0:
        errors.append("no substrate-scored candidate SHARES (the anchored-slice population is missing)")
    if n_sanctions == 0:
        errors.append("no substrate-sanctions cases (the OFAC name-collision population is missing)")
    if n_syn == 0:
        errors.append("no synthetic scored cases (the hand-authored scored population is missing)")
    # the substrate populations must be TWO-SIDED (uphold + reject) — a one-sided "scored" oracle is the Phase-77 trap
    for label, src_id in (("substrate-anchored", "substrate-anchored-slice"),
                          ("substrate-sanctions", "substrate-sanctions-slice")):
        sides = {c["oracle"]["same_entity"] for c in data.get("cases", [])
                 if c.get("source") == src_id and isinstance(c.get("oracle"), dict)
                 and isinstance(c["oracle"].get("same_entity"), bool)}
        if sides and sides != {True, False}:
            errors.append(f"the {label} population must be TWO-SIDED (uphold + reject); got same_entity={sorted(sides)}")
    prov = data.get("provenance") or {}
    if (prov.get("n_substrate_scored") != n_substrate or prov.get("n_synthetic_scored") != n_syn
            or prov.get("n_substrate_sanctions_scored") != n_sanctions):
        errors.append("provenance counts disagree with the actual case populations")
    return errors


def render_merge(template: str) -> str:
    """Validate + inline the merge-adjudication dataset into merge.html. Pure: no disk write — the single
    source of truth for dist/merge/index.html (shared by build/check). No corpus/taxonomy load: the merge
    cases reference no corpus docs (self-contained entity_refs / obs_ids), so the only boundary check is the
    structural + vocab + firewall validator above. Phase 83: the companion merge-adjudicator LIVE overlay
    (`/*LIVE_START*/.../*LIVE_END*/` in merge.html, served only by serve_merge.py) is STRIPPED here — the
    regex eats the leading newline so the offline dist stays byte-identical, and the strip runs BEFORE the
    self-contained guard so the live region's fetch never trips it (the corpus/news precedent)."""
    template = LIVE_REGION_RE.sub("", template)
    data = load_merge_cases()
    errors = validate_merge_cases(data)
    if errors:
        die("merge cases fail boundary validation:\n  - " + "\n  - ".join(errors))
    n = template.count(MERGE_PLACEHOLDER)
    if n != 1:
        die(f"expected exactly one {MERGE_PLACEHOLDER} placeholder in merge.html, found {n}")
    out = template.replace(MERGE_PLACEHOLDER, json.dumps(data, ensure_ascii=False, indent=2))
    if MERGE_PLACEHOLDER in out:
        die("merge placeholder survived substitution")
    if "fetch(" in out or "<script src" in out or 'type="module"' in out:
        die("merge ship file is not self-contained (fetch / external script / ES module present)")
    return out


def build_merge(template: str) -> None:
    out = render_merge(template)
    out_dir = ROOT / "dist" / "merge"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "index.html"
    out_path.write_text(out, encoding="utf-8")
    print(f"build: merge -> {out_path.relative_to(ROOT)}  ({len(out):,} bytes)")


def check_merge(template: str) -> bool:
    """Drift guard for the merge-console artifact: committed dist/merge == a fresh render?"""
    out_path = ROOT / "dist" / "merge" / "index.html"
    rel = out_path.relative_to(ROOT)
    try:
        fresh = render_merge(template)
    except SystemExit:
        print(f"check: merge -> FAIL (merge data no longer renders; cannot reproduce {rel})", file=sys.stderr)
        return False
    if not out_path.exists():
        print(f"check: merge -> DRIFT (missing built artifact {rel}; run `build.py merge`)", file=sys.stderr)
        return False
    if out_path.read_text(encoding="utf-8") != fresh:
        print(f"check: merge -> DRIFT ({rel} differs from a fresh build; run `build.py merge` and commit)", file=sys.stderr)
        return False
    print(f"check: merge -> ok ({rel} matches a fresh build)")
    return True


def render_launcher(template: str) -> str:
    """Inline the committed cross-pillar bridge state into the launcher (dist/index.html).

    Phase 55: the single front door. Reads data/pillar-status.json (regenerated by
    scripts/e2e_chain_check.py — build.py NEVER imports the harness, only its committed output) and
    injects it at __STATUS__. The launcher links the 5 existing artifacts by relative path and carries
    no engine data. Pure: no disk write — the single source of truth for dist/index.html.
    """
    if not PILLAR_STATUS.exists():
        die(f"launcher: missing {PILLAR_STATUS.relative_to(ROOT)} "
            f"(run `python3 scripts/e2e_chain_check.py --selftest` to regenerate it)")
    try:
        status = json.loads(PILLAR_STATUS.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        die(f"launcher: {PILLAR_STATUS.relative_to(ROOT)} is not valid json ({e})")
    if status.get("illustrative") is not True:
        die("launcher: pillar-status.json must carry illustrative:true (the always-on synthetic posture)")
    bridges = status.get("bridges", {})
    for k in ("bridge_1_persist", "bridge_2_consume", "e2e_real"):
        if k not in bridges or "state" not in bridges.get(k, {}):
            die(f"launcher: pillar-status.json bridges missing '{k}.state'")
    n = template.count(LAUNCHER_PLACEHOLDER)
    if n != 1:
        die(f"expected exactly one {LAUNCHER_PLACEHOLDER} placeholder in launcher.html, found {n}")
    out = template.replace(LAUNCHER_PLACEHOLDER, json.dumps(status, ensure_ascii=False, indent=2))
    if LAUNCHER_PLACEHOLDER in out:
        die("launcher placeholder survived substitution")
    if "fetch(" in out or "<script src" in out or 'type="module"' in out:
        die("launcher ship file is not self-contained (fetch / external script / ES module present)")
    return out


def build_launcher(template: str) -> None:
    out = render_launcher(template)
    out_path = ROOT / "dist" / "index.html"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(out, encoding="utf-8")
    print(f"build: launcher -> {out_path.relative_to(ROOT)}  ({len(out):,} bytes)")


def check_launcher(template: str) -> bool:
    """Drift guard for the launcher: committed dist/index.html == a fresh render?"""
    out_path = ROOT / "dist" / "index.html"
    rel = out_path.relative_to(ROOT)
    try:
        fresh = render_launcher(template)
    except SystemExit:
        print(f"check: launcher -> FAIL (launcher data no longer renders; cannot reproduce {rel})", file=sys.stderr)
        return False
    if not out_path.exists():
        print(f"check: launcher -> DRIFT (missing built artifact {rel}; run `build.py launcher`)", file=sys.stderr)
        return False
    if out_path.read_text(encoding="utf-8") != fresh:
        print(f"check: launcher -> DRIFT ({rel} differs from a fresh build; run `build.py launcher` and commit)", file=sys.stderr)
        return False
    print(f"check: launcher -> ok ({rel} matches a fresh build)")
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

    # 'corpus' = only the corpus explorer; 'news' = only the adverse-media stream; 'console' = only
    # the gate console; 'triage' = only the triage console; 'merge' = only the merge console; 'launcher' =
    # only the dist/index.html front door; 'all' = every typology + corpus + news + console + triage +
    # merge + launcher; else a typology.
    want_corpus = target in ("corpus", "all")
    want_news = target in ("news", "all")
    want_console = target in ("console", "all")
    want_triage = target in ("triage", "all")
    want_merge = target in ("merge", "all")
    want_launcher = target in ("launcher", "all")
    want_typologies = target not in ("corpus", "news", "console", "triage", "merge", "launcher")
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
    console_template = None
    if want_console:
        if not CONSOLE_TEMPLATE.exists():
            die(f"console template not found: {CONSOLE_TEMPLATE}")
        console_template = CONSOLE_TEMPLATE.read_text(encoding="utf-8")
    triage_template = None
    if want_triage:
        if not TRIAGE_TEMPLATE.exists():
            die(f"triage template not found: {TRIAGE_TEMPLATE}")
        triage_template = TRIAGE_TEMPLATE.read_text(encoding="utf-8")
    merge_template = None
    if want_merge:
        if not MERGE_TEMPLATE.exists():
            die(f"merge template not found: {MERGE_TEMPLATE}")
        merge_template = MERGE_TEMPLATE.read_text(encoding="utf-8")
    launcher_template = None
    if want_launcher:
        if not LAUNCHER_TEMPLATE.exists():
            die(f"launcher template not found: {LAUNCHER_TEMPLATE}")
        launcher_template = LAUNCHER_TEMPLATE.read_text(encoding="utf-8")

    if check:
        # Non-mutating drift guard: committed dist == fresh build? Touches nothing on disk.
        results = []
        if want_typologies:
            results += [check_one(t, template) for t in resolve_targets(target)]
        if want_corpus:
            results.append(check_corpus(corpus_template))
        if want_news:
            results.append(check_news(news_template))
        if want_console:
            results.append(check_console(console_template))
        if want_triage:
            results.append(check_triage(triage_template))
        if want_merge:
            results.append(check_merge(merge_template))
        if want_launcher:
            results.append(check_launcher(launcher_template))
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
    if want_console:
        build_console(console_template)
    if want_triage:
        build_triage(triage_template)
    if want_merge:
        build_merge(merge_template)
    if want_launcher:
        build_launcher(launcher_template)
    # (Phase 55: the old one-time M1 stale-`dist/index.html` removal was deleted — dist/index.html is
    # now the launcher artifact, the 8th build target, not the obsolete single-file M1 layout.)


if __name__ == "__main__":
    main()
