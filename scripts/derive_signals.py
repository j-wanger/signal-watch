#!/usr/bin/env python3
"""Derive a typology config from a FinCEN advisory markdown — AUTHORING-TIME ONLY.

Part of the Signal Watch ingestion pipeline (Phase 11 — AUTOMATE). This automates the
article -> signal derivation step that was proven MANUALLY in Phase 7 (the EFE advisory
markdown -> the hand-derived elder-financial-exploitation.json config):

    crawl_fincen.py    -> data/fincen/index.json   (manifest)
    acquire_fincen.py  -> data/fincen/raw/<id>.pdf (resolve + download)
    pdf_to_md.py       -> data/fincen/<id>.md      (verbatim source of truth)
    derive_signals.py  -> config/typologies/<id>.draft.json   (THIS TOOL)
    (human review)     -> config/typologies/<id>.json
    build.py           -> dist/<id>/index.html

NON-NEGOTIABLE: nothing here ever runs in the ship artifact. The engine never imports
this; build.py stays stdlib-only and never calls an LLM. This is a developer tool.

TWO LAYERS, sharing one deterministic boundary:
  - DETERMINISTIC (stdlib-only, offline): extract_red_flags(md) parses the advisory's
    enumerated red-flag list; scaffold_config() emits a schema-shaped config SKELETON.
    Verified offline by `--selftest` (same runnable-check spirit as build.py --check).
  - NEURAL (build-time only, env-keyed): `--draft` proposes the judgment fields the
    schema flags as decisions (status, the single target, the signal definition) via the
    Anthropic API. The `anthropic` SDK is LAZY-imported only inside --draft.

The LLM PROPOSES a config/typologies/<id>.draft.json; the deterministic validator
(build.py + schema) + the two human gates DISPOSE. Committed configs stay deterministic
and human-reviewed — no neural judge at the build boundary.

FinCEN advisories are U.S. federal works in the public domain (17 U.S.C. 105).

Usage:
    python3 scripts/derive_signals.py --selftest             # offline: EFE extraction (12+12) + checks
    python3 scripts/derive_signals.py --list <md-path>       # offline: print the extracted red flags
    python3 scripts/derive_signals.py --corpus               # offline: extract across ALL committed md
    python3 scripts/derive_signals.py --corpus-status        # offline: emit data/fincen/corpus-status.json
    python3 scripts/derive_signals.py --scaffold <id> <md>   # offline: md -> <id>.draft.json SKELETON
    python3 scripts/derive_signals.py --draft <id> <md>      # LIVE (authoring): + LLM-drafted judgment
    python3 scripts/derive_signals.py --scaffold-derived <id> <md>   # offline: -> derived/<id>.json skeleton
    python3 scripts/derive_signals.py --check-derived <record.json>  # offline: dispose a derived record

The --draft mode calls the Anthropic API (claude-opus-4-8) to PROPOSE the judgment
fields (status per indicator, the single indicator/candidate target, the signal
definition); it needs ANTHROPIC_API_KEY in the environment and `anthropic` installed
in the gitignored authoring venv. The LLM proposes; build.py + schema + the two human
gates dispose. The key NEVER enters the ship artifact — --draft is build-time only.

CORPUS DERIVATION (Phase 12 — backend for an expanded, singular corpus-backed demo):
  --corpus runs extract_red_flags across the whole committed FinCEN corpus and reports each
  advisory CLEAN / LOW-CONFIDENCE / NEEDS-ATTENTION — the deterministic spine validated on
  ALL 14, flagging non-conformers (heterogeneous formats) rather than forcing a bogus count.
  --scaffold-derived emits a derived-record SKELETON (one indicator per extracted red flag,
  src_line traceable, judgment empty) under data/fincen/derived/. The LLM backend fills the
  judgment — per indicator a coverage status + data availability, a build recommendation, and
  build logic for the BUILD_NOW gaps — and --check-derived DISPOSES via the deterministic
  checks: build_rec consistency (must follow the cover×data matrix, build_rec_category) +
  traceability (every indicator -> a red-flag md line) + the BUILD_NOW build-logic shape.
  The LLM backend may be the Anthropic API (--draft pattern) OR a live model session acting as
  the backend (no key) — either way the LLM PROPOSES and the deterministic checks DISPOSE.
  Derived records are an LLM-derived + checked corpus dataset, NOT ship typology configs.

  --corpus-status emits data/fincen/corpus-status.json (committed): per-advisory extraction
  quality + flag/section counts + title/date/source attribution (titles from index.json) + a
  derivable flag. This is the deterministic data artifact the CORPUS-EXPLORER build reads
  (scripts/build.py corpus merges it with data/fincen/derived/*.json) — build.py never imports
  this authoring tool; it consumes the committed manifest. Regenerate after the corpus changes.
"""
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS_DIR = ROOT / "data" / "fincen"
EFE_MD = CORPUS_DIR / "fin-2022-a002.md"
TYPOLOGY_DIR = ROOT / "config" / "typologies"
DERIVED_DIR = CORPUS_DIR / "derived"
INDEX_JSON = CORPUS_DIR / "index.json"               # crawl manifest (titles/dates/urls)
CORPUS_STATUS_JSON = CORPUS_DIR / "corpus-status.json"  # emitted manifest the corpus build reads

# The committed EFE advisory enumerates exactly these red-flag counts (Phase 7: "24 red
# flags intact"). Pinning them makes --selftest a deterministic validator at the boundary.
_EFE_BEHAVIORAL = 12
_EFE_FINANCIAL = 12

# Generalized red-flag SECTION finder (Phase 12 — corpus-wide). FinCEN advisories
# introduce their enumerated red-flag lists heterogeneously across the committed corpus:
#   INTRO  : "<category> red flags [indicators] ... may include:" / "... the following
#            red flag indicators ..." (EFE fin-2022-a002, ransomware fin-2021-a004, …)
#   HEADER : a standalone "<Category> Red Flags" line directly followed by the list
#            (fin-2024-a002 "Transactional Red Flags", …)
# We anchor on BOTH, take the blank-line-separated blocks that follow each section up to
# the next anchor / footnote run / major section, and FLAG advisories where no section is
# confidently found. markitdown drops bullet glyphs + interleaves page artifacts, so we
# group blank-separated blocks rather than trust list markers.
#
# INTRO: a sentence that introduces the list, with an explicit list lead-in (so a topic
# sentence like EFE's "FinCEN has identified behavioral and financial red flags to help …"
# is NOT mistaken for one). Two orderings recur across the corpus:
#   forward : "<cat> red flags [indicators] ... may include / as follows / listed below"
#             (EFE fin-2022-a002 "may include", Iran fin-2024-a001 "listed below")
#   reverse : "... the following ... red flag [indicators] ..." (ransomware fin-2021-a004,
#             kleptocracy fin-2022-a001). Requiring "the following"/"listed below"/"as
#             follows"/"may include" keeps it to genuine list lead-ins.
_RF_INTRO = re.compile(
    r"\bred\s+flags?(?:\s+indicators?)?\b[^.\n]{0,80}?"
    r"\b(?:may\s+include|as\s+follows|listed\s+below|described\s+below)\b"
    r"|\bthe\s+following\b[^.\n]{0,50}?\bred\s+flags?(?:\s+indicators?)?\b", re.I)
# HEADER: a SHORT standalone header line — 1–5 Title-case/connector words then "red
# flag(s) [indicators]" and nothing after (no "... of <topic>" clause; that's a section
# TITLE, not a list header, and is caught by the INTRO instead). Rejects mid-sentence
# "... such financial red flag" (sentences don't start Title-case + end at "red flags").
_RF_HEADER = re.compile(
    r"^(?P<label>[A-Z][\w’'/-]*(?:\s+(?:[A-Z][\w’'/-]*|and|of|the|&|for)){0,4})"
    r"\s+red\s+flags?(?:\s+indicators?)?$", re.I)
# Tier-2 fallbacks — used ONLY when an advisory has no Tier-1 anchor (so EFE and the clean
# advisories never touch them). A LOOSE header allows a trailing "Red Flags <Related to /
# Potentially Indicative of / of …> <topic>" clause (a section TITLE that an advisory like
# fin-2025-a003 puts directly above its blank-separated list), and a WEAK intro catches the
# bare "FinCEN has identified red flags to …" sentence with no explicit list lead-in.
_RF_HEADER_LOOSE = re.compile(
    r"^(?P<label>(?:[A-Z][\w’'/-]*\s+){0,3})red\s+flags?(?:\s+indicators?)?\b"
    r"(?:\s+(?:related|potentially|indicative|of|to|that|associated|targeting)\b.*)?$", re.I)
_RF_INTRO_WEAK = re.compile(r"\bidentified\b[^.\n]{0,40}?\bred\s+flags?(?:\s+indicators?)?\b", re.I)
# a list ends at a footnote run, a numbered/Roman major section, or a wrap-up header.
# `\d+\.(?:\s|$)` catches both "47. Id." and a bare footnote marker alone on a line ("81.").
_SECTION_STOP = re.compile(
    r"^(?:\d+\.(?:\s|$)|\d+\s+[A-Z]|reminder of relevant|for further information|"
    r"sar (?:filing|reporting)|frequently asked|section\s+[ivx]+\b)", re.I)
# A block that is itself a footnote/citation, not a red flag (Phase-12 post-review filter):
# a footnote-numbered line, a legal "supra note"/"Id." marker, or a block that ends with a
# "(Mon DD, YYYY)" citation date. Real red flags describe behaviour; they don't end in a cite.
_CITATION = re.compile(
    r"^\d+\.\s"
    r"|\b(?:supra\s+note|\bid\.\b|see\s+(?:also\s+)?(?:fincen|fbi|doj|ofac|fatf|cisa|dhs|u\.s\.))"
    r"|\([A-Z][a-z]{2,8}\.?\s+\d{1,2},\s+\d{4}\)\.?\s*$", re.I)
# Standard FinCEN boilerplate that wraps the list intro (a multi-line sentence often bleeds
# into the first block). Never a red flag — drop it so the list starts at the real item 1.
_INTRO_NOISE = re.compile(
    r"no single\b.*\b(?:determinative|red flag)"
    r"|detecting,?\s+preventing,?\s+and reporting"
    r"|risk-based approach to compliance"
    r"|relevant facts and circumstances of each transaction", re.I)
_LABEL_WORD = re.compile(r"(\w+)\s+red\s+flags?", re.I)
_LABEL_STOPWORDS = {"the", "of", "and", "a", "an", "following", "identified",
                    "fincen", "has", "these", "such", "associated", "additional"}
_PAGE_NUM = re.compile(r"^\d+$")
_RUNNING_HEADER = re.compile(r"^\s*FINCEN ADVISORY\s*")  # running header glued to content
_BULLET = re.compile(r"^[\s•·▪◦*-]+")  # leading bullet glyphs / dashes


def _clean(line: str) -> str:
    """Strip page-break form-feeds, the running-header glue, and surrounding whitespace."""
    return _RUNNING_HEADER.sub("", line.replace("\x0c", "")).strip()


def _blocks(section_lines):
    """Group consecutive content lines into (start_line, text) blocks.

    A blank line or a bare page number separates blocks; the 'FINCEN ADVISORY' running
    header is stripped so a header-glued red flag still reads as its own block.
    """
    buf: list[str] = []
    start = None
    for lineno, raw in section_lines:
        cleaned = _clean(raw)
        if not cleaned or _PAGE_NUM.match(cleaned):
            if buf:
                yield start, " ".join(buf)
                buf, start = [], None
            continue
        if not buf:
            start = lineno
        buf.append(cleaned)
    if buf:
        yield start, " ".join(buf)


def _section_label(text: str) -> str:
    """Normalized lowercase section label from a header/intro ('Behavioral' -> 'behavioral')."""
    m = _LABEL_WORD.search(text)
    word = m.group(1).lower() if m else ""
    return word if word and word not in _LABEL_STOPWORDS else "redflag"


def extract_red_flags(md: str) -> list[dict]:
    """PURE: FinCEN advisory markdown -> the enumerated red-flag list (corpus-wide).

    Returns [{section, n, text, line}] where `section` is the normalized red-flag section
    label ('behavioral'/'financial' for EFE, 'transactional' for fin-2024-a002, …), `n` is
    the 1-based index within its section, and `line` is the source line (traceability).
    Anchors on intro sentences AND short headers (see _RF_INTRO/_RF_HEADER); returns [] when
    no red-flag section is confidently found (the --corpus report flags those). No I/O.
    """
    # split on "\n" (NOT splitlines) so line numbers match \n-based editors/tools; the
    # markdown carries form-feed page breaks that splitlines() would split on (drift vs L507).
    lines = list(enumerate(md.split("\n"), 1))
    cleaned = [(ln, _clean(raw)) for ln, raw in lines]

    # 1) collect section anchors — short headers + intro sentences. Tier 1 = the reliable
    #    signals (clean headers + explicit list-intros). Tier 2 (loose trailing-clause headers
    #    + weak "identified red flags" intros) runs ONLY when Tier 1 finds nothing — so EFE and
    #    the clean advisories never touch it, while a purely-titled advisory still anchors.
    def collect(header_re, intro_re):
        out = []
        for ln, text in cleaned:
            if not text:
                continue
            if header_re.match(text):
                out.append({"line": ln, "label": _section_label(text), "kind": "header"})
            elif intro_re.search(text):
                out.append({"line": ln, "label": _section_label(text), "kind": "intro"})
        return out

    anchors = collect(_RF_HEADER, _RF_INTRO) or collect(_RF_HEADER_LOOSE, _RF_INTRO_WEAK)
    if not anchors:
        return []

    # 2) build sections, each with `boundary` (where the PREVIOUS section ends = the first
    #    anchor line) and `start` (where THIS list begins). A header immediately followed
    #    (≤8 lines) by its intro coalesces: boundary stays the header, the list starts after
    #    the intro's "may include:" lead-in (so the header line isn't mistaken for a flag).
    sections = []
    for a in anchors:
        prev = sections[-1] if sections else None
        # coalesce only a same-label header+intro pair (label-match keeps the wider window
        # safe — EFE's "Behavioral Red Flags" header sits ~10 lines above its "may include:"
        # intro, with a descriptive paragraph between that must NOT be read as a flag).
        if (prev and a["kind"] == "intro" and prev["kind"] == "header"
                and 0 < a["line"] - prev["boundary"] <= 15
                and prev["label"] in (a["label"], "redflag")):
            prev["start"], prev["kind"] = a["line"], "intro"
            if prev["label"] == "redflag":
                prev["label"] = a["label"]
        else:
            sections.append({"boundary": a["line"], "start": a["line"],
                             "label": a["label"], "kind": a["kind"]})

    # 3) per-section span = (after its list-start) up to the next section's boundary / a stop
    #    line; group blank-separated blocks, dropping page artifacts + stray short fragments.
    boundaries = [s["boundary"] for s in sections]
    flags: list[dict] = []
    for idx, sec in enumerate(sections):
        next_boundary = boundaries[idx + 1] if idx + 1 < len(boundaries) else None
        span = []
        for ln, raw in lines:
            if ln <= sec["start"]:
                continue
            if next_boundary and ln >= next_boundary:
                break
            if _SECTION_STOP.match(_clean(raw)):
                break
            span.append((ln, raw))
        n = 0
        for start, text in _blocks(span):
            text = _BULLET.sub("", text).strip()
            if len(text) < 20:               # drop stray fragments / glued page artifacts
                continue
            if _INTRO_NOISE.search(text):    # drop the standard FinCEN intro-caveat boilerplate
                continue
            if _RF_HEADER_LOOSE.match(text):  # a sub-section header captured as a block, not a flag
                continue
            if _CITATION.search(text):        # a footnote/citation captured as a block, not a flag
                continue
            n += 1
            flags.append({"section": sec["label"], "n": n, "text": text, "line": start})
    return flags


def _load_md(path: Path) -> str:
    if not path.exists():
        sys.exit(f"missing markdown {path} — run the acquire/convert pipeline first")
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Deterministic scaffolding: red flags -> a schema-shaped config SKELETON.
# The skeleton fills everything MECHANICAL (the act chrome, the indicator list
# from the financial red flags, the verbatim-source wiring) and leaves the three
# JUDGMENT fields the schema flags as decisions — the single indicator/candidate
# target:true and the signal definition — for the human or the --draft LLM step.
# It is build-INVALID by construction (zero targets) so build.py + schema stay the
# deterministic gate (see config/schema.md + scripts/build.py validate_config).
# ---------------------------------------------------------------------------
_STEPS = ["The blind spot", "Read advisory", "Assess coverage", "Human review",
          "Agent builds", "Combination lift", "Loop closes"]
_NEXT_LABELS = ["Begin ›", "Read the advisory ›", "Assess coverage ›", "Review candidates ›",
                "Build selected ›", "See the lift ›", "Close the loop ›", "Run again ↺"]
_HINTS = ["", "Agent ingests the advisory and proposes signals",
          "Candidates checked against our library + data", "You decide what we build — human in the loop",
          "You confirm the proposal — second human gate", "Why atoms beat monolithic scenarios",
          "The blind spot closes — and stays closed", ""]


def _todo(what: str) -> str:
    return f"TODO: {what}"


def _short_label(text: str, cap: int = 90) -> str:
    """A concise indicator/candidate label from a red-flag sentence."""
    label = text.rstrip(".").strip()
    return label if len(label) <= cap else label[: cap - 1].rstrip() + "…"


def scaffold_config(typ_id: str, flags: list, meta: dict) -> dict:
    """PURE: extracted red flags + meta -> a schema-shaped config SKELETON.

    One indicator + one candidate per FINANCIAL red flag (the data-signal surface; the
    behavioral flags are non-data per the proven elder derivation). status/cover/data get
    neutral defaults; NO target:true and NO signal definition are set — those are the
    judgment the deterministic boundary (build.py) requires before a build can succeed.
    """
    adv_id = meta.get("advisory_id") or "advisory"
    src = meta.get("source") or _todo(f"verbatim attribution for {adv_id}")
    financial = [f for f in flags if f["section"] == "financial"]

    indicators, candidates = [], []
    for i, f in enumerate(financial, 1):
        label = _short_label(f["text"])
        indicators.append({
            "id": f"IND-{i:02d}",
            "label": label,
            "status": "gap",  # JUDGMENT: covered | partial | gap — and mark ONE target:true
            "sub": f"src: {adv_id} financial red flag #{f['n']} · md L{f['line']}",
        })
        candidates.append({
            "id": f"C{i}",
            "name": label,
            "type": "entity",     # JUDGMENT: entity | relationship | motif
            "cover": "gap",       # JUDGMENT
            "data": "available",  # JUDGMENT — and mark ONE target:true + add its definition
        })

    return {
        "id": typ_id,
        "label": meta.get("label") or _todo(f"human label for {typ_id}"),
        "steps": list(_STEPS),
        "next_labels": list(_NEXT_LABELS),
        "hints": list(_HINTS),
        "anchor": {
            "hook_eyebrow": _todo("Act 0 eyebrow"),
            "hook_title": _todo("Act 0 headline — what aren't we watching?"),
            "hook_lead": _todo(f"Act 0 lead naming the typology ({typ_id})"),
            "close_title": _todo("Act 6 headline — the blind spot closes"),
            "close_delta": _todo("Act 6 gauge delta line"),
            "coverage_noun": meta.get("coverage_noun") or _todo("short gauge noun (e.g. 'EFE red flags')"),
            "lift_rationale": _todo("Act 5 atoms-over-monoliths rationale naming the composed signals"),
            "source": src,
        },
        "coverage": {"indicators": indicators},
        "advisory_stream": [
            {"t": _todo("paraphrase the advisory lead for the Act 1 stream "
                        "(advisory_full renders the verbatim panel below)")}
        ],
        "advisory_full": {
            "source": src,
            "text_file": meta.get("text_file", ""),
            "highlights": [],  # JUDGMENT: the exact verbatim phrases that became signals
        },
        "candidates": candidates,
        "lift": [
            {"name": _todo("target signal alone"), "combo": _todo("S-? in isolation"),
             "value": 0, "strength": "weak"},
            {"name": _todo("+ existing signal A"), "combo": _todo("S-? × S-A"),
             "value": 0, "strength": "mid"},
            {"name": _todo("+ existing signal B"), "combo": _todo("S-? × S-A × S-B"),
             "value": 0, "strength": "strong"},
        ],
        "stats": {"fire_count": 0, "standalone_precision": 0, "best_combo_precision": 0},
    }


def _advisory_meta(md_path: Path) -> dict:
    """Derive the source attribution + text_file path from the advisory markdown path."""
    adv_id = md_path.stem.upper()  # fin-2022-a002 -> FIN-2022-A002
    resolved = md_path.resolve()
    rel = resolved.relative_to(ROOT) if resolved.is_relative_to(ROOT) else md_path
    return {
        "advisory_id": adv_id,
        "source": f"FinCEN {adv_id} · public domain, 17 U.S.C. 105 — "
                  + _todo("add advisory title + date"),
        "text_file": str(rel),
    }


def write_scaffold(typ_id: str, md_arg: str) -> int:
    md_path = Path(md_arg)
    flags = extract_red_flags(_load_md(md_path))
    if not flags:
        sys.exit("no red flags extracted — cannot scaffold (check the advisory markdown / anchors)")
    cfg = scaffold_config(typ_id, flags, _advisory_meta(md_path))
    out = TYPOLOGY_DIR / f"{typ_id}.draft.json"
    out.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    n = len(cfg["coverage"]["indicators"])
    print(f"wrote {out} — SKELETON ({n} indicators from financial red flags)")
    print("SCRATCH ARTIFACT (gitignored): review, fill the JUDGMENT fields, then rename to "
          f"{typ_id}.json. Remove before `build.py all` (it globs *.json).")
    print("JUDGMENT to fill (build.py rejects the skeleton until done): ONE indicator target:true · "
          "ONE candidate target:true (cover:gap + data:available) + its signal definition · "
          "anchor copy · lift/stats.")
    return 0


# ---------------------------------------------------------------------------
# Neural layer (BUILD-TIME ONLY): draft the JUDGMENT fields via the Anthropic API.
# The LLM PROPOSES; build.py + schema + the two human gates DISPOSE — committed
# configs stay deterministic + human-reviewed (no neural judge at the build
# boundary). `anthropic` is LAZY-imported here only; the deterministic layer above
# never needs it. Model id + structured-output usage follow the claude-api
# reference (consulted, not guessed): claude-opus-4-8 + output_config.format with
# a json_schema constrains the response to schema-valid JSON.
# ---------------------------------------------------------------------------
_DRAFT_MODEL = "claude-opus-4-8"

_STATUS_ENUM = ["covered", "partial", "gap"]
_TYPE_ENUM = ["entity", "relationship", "motif"]
_DATA_ENUM = ["available", "partial", "insufficient"]

# JSON schema for output_config.format — keep to supported keywords (enums + nested
# objects with additionalProperties:false; no min/maxLength or numeric constraints).
_DRAFT_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "indicator_statuses": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "id": {"type": "string"},
                    "status": {"type": "string", "enum": _STATUS_ENUM},
                },
                "required": ["id", "status"],
            },
        },
        "indicator_target_id": {"type": "string"},
        "candidates": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "id": {"type": "string"},
                    "type": {"type": "string", "enum": _TYPE_ENUM},
                    "cover": {"type": "string", "enum": _STATUS_ENUM},
                    "data": {"type": "string", "enum": _DATA_ENUM},
                },
                "required": ["id", "type", "cover", "data"],
            },
        },
        "candidate_target_id": {"type": "string"},
        "definition": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "signal_name": {"type": "string"},
                "class": {"type": "string"},
                "features": {"type": "array", "items": {"type": "string"}},
                "logic": {"type": "string"},
                "window": {"type": "string"},
                "source": {"type": "string"},
                "route": {"type": "string"},
            },
            "required": ["signal_name", "class", "features", "logic", "window", "source", "route"],
        },
    },
    "required": ["indicator_statuses", "indicator_target_id", "candidates",
                 "candidate_target_id", "definition"],
}

_DEFINITION_CONTRACT = (
    "definition = { signal_name, class, features: string[], logic, window, source, route }\n"
    "- signal_name: proposed signal id, e.g. S-DORMANT-DRAIN-ELDER\n"
    "- class: e.g. 'entity · account-level · stateful'\n"
    "- features: concrete, computable transaction/account features the rule reads\n"
    "- logic: the detection rule (write a literal '<' as &lt;)\n"
    "- window: rolling window, e.g. 'rolling 14 days'\n"
    "- source: upstream data source, e.g. 'Core deposit + transaction features (Gold)'\n"
    "- route: alert routing, e.g. 'Tier-1 alert → review gate'"
)


def _few_shot() -> str:
    """Two hand-authored configs as grounding examples for the derivation pattern."""
    blocks = []
    for stem in ("fentanyl", "elder-financial-exploitation"):
        p = TYPOLOGY_DIR / f"{stem}.json"
        if not p.exists():
            continue
        c = json.loads(p.read_text(encoding="utf-8"))
        tgt = next((x for x in c["candidates"] if x.get("target")), None)
        blocks.append(json.dumps({
            "id": c["id"],
            "indicators": c["coverage"]["indicators"],
            "candidates": c["candidates"],
            "target_definition": tgt.get("definition") if tgt else None,
        }, ensure_ascii=False, indent=2))
    return "\n\n".join(blocks)


def draft_judgment(typ_id: str, flags: list, scaffold: dict) -> dict:
    """NEURAL: ask Claude to PROPOSE the judgment fields, grounded on the red flags.

    Build-time only. Returns the validated structured object (statuses, the two
    targets, and the signal definition). Lazy-imports anthropic; reads the key from
    the environment; the result is applied to a draft and disposed of by build.py.
    """
    try:
        import anthropic  # lazy: only the --draft path needs the SDK
    except ImportError:
        sys.exit("anthropic SDK not installed — run `uv pip install -r scripts/requirements-authoring.txt` "
                 "in the gitignored authoring venv. The deterministic --selftest/--scaffold paths need no SDK.")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY not set — --draft calls the Anthropic API at authoring time. "
                 "Export the key first (it NEVER enters the ship artifact; --draft is build-time only).")

    financial = [f for f in flags if f["section"] == "financial"]
    indicators = scaffold["coverage"]["indicators"]
    candidates = scaffold["candidates"]
    flag_lines = "\n".join(
        f"{ind['id']} / {cand['id']}: {f['text']}  (md L{f['line']})"
        for ind, cand, f in zip(indicators, candidates, financial)
    )
    system = (
        "You are an AML detection engineer in the Signal Watch authoring pipeline. From a FinCEN "
        "advisory's enumerated FINANCIAL red flags you derive ONE candidate detection signal. Ground "
        "every choice in the red flags provided — do not invent indicators. Your output is a DRAFT a "
        "human reviews and a deterministic validator (build.py) checks; it is never shipped unreviewed. "
        "Pick the single highest-value TARGET: a genuine coverage GAP that is also DATA-AVAILABLE "
        "(buildable). The signal definition's features must be concrete, computable transaction/account "
        "features."
    )
    user = (
        f"TYPOLOGY: {typ_id}\n\n"
        f"SIGNAL DEFINITION CONTRACT:\n{_DEFINITION_CONTRACT}\n\n"
        f"FINANCIAL RED FLAGS (indicator id / candidate id : text):\n{flag_lines}\n\n"
        f"TWO HAND-AUTHORED EXAMPLES (the judgment + signal style to emulate):\n{_few_shot()}\n\n"
        "TASK: (1) assign each indicator a status (covered|partial|gap). (2) choose exactly ONE "
        "indicator id as the target — a real gap worth building. (3) for every candidate set type "
        "(entity|relationship|motif), cover (covered|partial|gap), data (available|partial|insufficient). "
        "(4) choose exactly ONE candidate id as the target; it MUST be cover=gap AND data=available. "
        "(5) draft that target candidate's signal definition. Pair the target indicator with the target "
        "candidate (same red flag). Return only the structured object."
    )
    client = anthropic.Anthropic()  # resolves ANTHROPIC_API_KEY from the environment
    resp = client.messages.create(
        model=_DRAFT_MODEL,
        max_tokens=8192,  # headroom: adaptive thinking shares the output budget with the JSON
        # This is reasoning-shaped judgment (assign statuses, pick the single highest-value
        # gap+available target, draft a computable signal). Per the claude-api reference, the
        # request surface defaults to thinking OFF; turn on adaptive thinking + high effort for
        # intelligence-sensitive work. effort and format coexist in one output_config.
        thinking={"type": "adaptive"},
        output_config={"effort": "high",
                       "format": {"type": "json_schema", "schema": _DRAFT_SCHEMA}},
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    # Fail loud with the real cause rather than a raw traceback: a refusal yields no schema-valid
    # text; a max_tokens stop truncates the JSON mid-object so json.loads would raise.
    if resp.stop_reason == "refusal":
        sys.exit("draft: model refused the request — no schema-valid output to apply")
    if resp.stop_reason == "max_tokens":
        sys.exit("draft: response hit max_tokens (truncated JSON) — raise max_tokens and retry")
    text = next((b.text for b in resp.content if b.type == "text"), None)
    if not text:
        sys.exit(f"draft: model returned no text block (stop_reason={resp.stop_reason})")
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        sys.exit(f"draft: model output was not valid JSON ({e}) — stop_reason={resp.stop_reason}")


def _apply_judgment(scaffold: dict, j: dict) -> dict:
    """Apply the LLM-proposed judgment onto the deterministic skeleton.

    Deterministic guard on top of the neural output: the chosen candidate target is
    FORCED to cover:gap + data:available because the schema/build.py require a
    buildable target — the validator disposes of what the model proposes.
    """
    status_by_id = {s["id"]: s["status"] for s in j.get("indicator_statuses", [])}
    for ind in scaffold["coverage"]["indicators"]:
        ind.pop("target", None)
        if ind["id"] in status_by_id:
            ind["status"] = status_by_id[ind["id"]]
    for ind in scaffold["coverage"]["indicators"]:
        if ind["id"] == j.get("indicator_target_id"):
            ind["status"] = "gap"          # a target is, by definition, the gap being built
            ind["target"] = True

    cand_by_id = {c["id"]: c for c in j.get("candidates", [])}
    for cand in scaffold["candidates"]:
        cand.pop("target", None)
        cand.pop("definition", None)
        upd = cand_by_id.get(cand["id"])
        if upd:
            cand["type"], cand["cover"], cand["data"] = upd["type"], upd["cover"], upd["data"]
    for cand in scaffold["candidates"]:
        if cand["id"] == j.get("candidate_target_id"):
            cand["cover"], cand["data"] = "gap", "available"  # build.py requires a buildable target
            cand["target"] = True
            cand["definition"] = j["definition"]
    return scaffold


def write_draft(typ_id: str, md_arg: str) -> int:
    md_path = Path(md_arg)
    flags = extract_red_flags(_load_md(md_path))
    if not flags:
        sys.exit("no red flags extracted — cannot draft (check the advisory markdown / anchors)")
    scaffold = scaffold_config(typ_id, flags, _advisory_meta(md_path))
    print(f"drafting judgment via {_DRAFT_MODEL} (authoring-time Anthropic API call)…")
    cfg = _apply_judgment(scaffold, draft_judgment(typ_id, flags, scaffold))
    out = TYPOLOGY_DIR / f"{typ_id}.draft.json"
    out.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tgt = next((c for c in cfg["candidates"] if c.get("target")), {})
    defn = tgt.get("definition", {})
    print(f"wrote {out} — LLM-drafted target {tgt.get('id')} ({defn.get('signal_name')})")
    print("SCRATCH ARTIFACT (gitignored): the LLM PROPOSED; build.py + schema + your two human gates "
          "DISPOSE. Review, fill the anchor copy + lift/stats, then rename to "
          f"{typ_id}.json and validate: python3 scripts/build.py {typ_id}")
    return 0


# ---------------------------------------------------------------------------
# Deterministic checks on a DERIVED record (Phase 12). The LLM backend PROPOSES,
# per indicator, a coverage status + data availability, a build recommendation, and
# (for buildable gaps) build logic; these checks DISPOSE — a record only stands if its
# recommendations follow the cover×data matrix and every indicator traces to a red-flag
# line the extractor found. LLM proposes, the deterministic spine disposes — no neural
# judge at the check boundary (the Phase-11 principle, extended to the corpus).
# ---------------------------------------------------------------------------
_STATUS_VALUES = ("covered", "partial", "gap")
_DATA_VALUES = ("available", "partial", "insufficient")
# the SINGLE allowed build recommendation per (coverage status, data availability) pair
_REC_MATRIX = {
    ("covered", "available"): "COVERED", ("covered", "partial"): "COVERED",
    ("covered", "insufficient"): "COVERED",
    ("gap", "available"): "BUILD_NOW", ("gap", "partial"): "BUILD_ENRICH",
    ("gap", "insufficient"): "SOURCE_DATA",
    ("partial", "available"): "ENHANCE", ("partial", "partial"): "ENHANCE",
    ("partial", "insufficient"): "MONITOR",
}
BUILD_RECS = tuple(sorted(set(_REC_MATRIX.values())))
_DEFN_KEYS = ("signal_name", "class", "features", "logic", "window", "source", "route")


def build_rec_category(status: str, data: str) -> str:
    """PURE: the single ALLOWED build recommendation for a (coverage status, data) pair."""
    if (status, data) not in _REC_MATRIX:
        raise ValueError(f"unknown (status, data) = ({status!r}, {data!r})")
    return _REC_MATRIX[(status, data)]


def check_build_rec(status: str, data: str, rec: str) -> str:
    """PURE: '' if `rec` is consistent with the cover×data matrix, else a violation message."""
    if status not in _STATUS_VALUES:
        return f"status {status!r} not in {_STATUS_VALUES}"
    if data not in _DATA_VALUES:
        return f"data {data!r} not in {_DATA_VALUES}"
    expected = build_rec_category(status, data)
    return "" if rec == expected else f"build_rec {rec!r} contradicts ({status},{data}); must be {expected!r}"


def check_record(record: dict, md: str) -> list:
    """PURE: run all deterministic checks on a derived record; return violations ([] = OK).

    Disposes of what the LLM backend proposed: (1) each indicator's build_rec follows the
    cover×data matrix; (2) every indicator's src_line is a line the extractor flagged
    (traceability to the deterministic extraction); (3) a BUILD_NOW indicator carries
    build_logic with the full definition shape, and COVERED/SOURCE_DATA carry none.
    """
    violations: list = []
    inds = record.get("indicators")
    if not isinstance(inds, list) or not inds:
        return ["record has no indicators[]"]
    # indicator ids must be unique, and each must trace to a DISTINCT red flag (no collapsing
    # many indicators onto one line — membership alone would let that through).
    ids = [ind.get("id") for ind in inds]
    if len(ids) != len(set(ids)):
        violations.append(f"duplicate indicator id(s): {sorted({i for i in ids if ids.count(i) > 1})}")
    src_lines = [ind.get("src_line") for ind in inds]
    dup_lines = sorted({l for l in src_lines if l is not None and src_lines.count(l) > 1})
    if dup_lines:
        violations.append(f"multiple indicators share src_line(s) {dup_lines} — each must trace to a distinct red flag")
    flag_lines = {f["line"] for f in extract_red_flags(md)}
    for ind in inds:
        iid = ind.get("id", "?")
        v = check_build_rec(ind.get("status"), ind.get("data"), ind.get("build_rec"))
        if v:
            violations.append(f"{iid}: {v}")
        if ind.get("src_line") not in flag_lines:
            violations.append(f"{iid}: src_line {ind.get('src_line')!r} is not an extracted red-flag line")
        rec, logic = ind.get("build_rec"), ind.get("build_logic")
        if rec == "BUILD_NOW":
            if not isinstance(logic, dict):
                violations.append(f"{iid}: BUILD_NOW requires build_logic (the signal definition)")
            else:
                # the disposer validates SHAPE, not just key presence: every definition field a
                # non-empty string, features a non-empty list[str] (an empty/typo'd logic must fail).
                for k in _DEFN_KEYS:
                    val = logic.get(k)
                    if k == "features":
                        if not (isinstance(val, list) and val and all(isinstance(x, str) and x.strip() for x in val)):
                            violations.append(f"{iid}: build_logic.features must be a non-empty list of strings")
                    elif not (isinstance(val, str) and val.strip()):
                        violations.append(f"{iid}: build_logic.{k} must be a non-empty string")
        elif rec in ("COVERED", "SOURCE_DATA") and logic:
            violations.append(f"{iid}: {rec} must not carry build_logic")
    return violations


def _checks_selftest() -> list:
    """Assert the deterministic checks accept a valid record + reject known violations. PURE."""
    fails: list = []
    # matrix is total over the enum product, every value a known rec
    for s in _STATUS_VALUES:
        for d in _DATA_VALUES:
            if build_rec_category(s, d) not in BUILD_RECS:
                fails.append(f"matrix({s},{d}) not a valid rec")
    # consistency: catches a contradiction, accepts a valid pairing
    if not check_build_rec("covered", "available", "BUILD_NOW"):
        fails.append("consistency check missed covered→BUILD_NOW contradiction")
    if check_build_rec("gap", "available", "BUILD_NOW"):
        fails.append("consistency check rejected a valid gap+available→BUILD_NOW")
    # record check: a valid record passes; tampered ones fail on every axis
    md = _load_md(EFE_MD)
    flags = extract_red_flags(md)
    good_logic = {k: (["dormancy_days_prior", "outbound_value_ratio"] if k == "features" else "x")
                  for k in _DEFN_KEYS}
    good = {"indicators": [
        {"id": "IND-01", "status": "gap", "data": "available", "build_rec": "BUILD_NOW",
         "src_line": flags[0]["line"], "build_logic": good_logic},
        {"id": "IND-02", "status": "covered", "data": "available", "build_rec": "COVERED",
         "src_line": flags[1]["line"]},
    ]}
    if check_record(good, md):
        fails.append(f"valid record rejected: {check_record(good, md)}")
    bad = json.loads(json.dumps(good))
    bad["indicators"][0]["build_rec"] = "COVERED"   # contradicts gap+available
    bad["indicators"][1]["src_line"] = 10 ** 9      # untraceable
    if len(check_record(bad, md)) < 2:
        fails.append("tampered record not caught (expected ≥2 violations)")
    # build_logic SHAPE hole must be closed: features-as-int + empty logic must both be caught
    shape_bad = json.loads(json.dumps(good))
    shape_bad["indicators"][0]["build_logic"]["features"] = 123
    shape_bad["indicators"][0]["build_logic"]["logic"] = ""
    if len(check_record(shape_bad, md)) < 2:
        fails.append("build_logic-shape hole not caught (features-as-int + empty logic)")
    # duplicate ids / collapsed src_lines must be caught
    dup = json.loads(json.dumps(good))
    dup["indicators"][1]["id"] = "IND-01"
    dup["indicators"][1]["src_line"] = flags[0]["line"]
    if not check_record(dup, md):
        fails.append("duplicate id / collapsed src_line not caught")
    return fails


# ---------------------------------------------------------------------------
# Derived-record authoring (Phase 12). A deterministic SKELETON (one indicator per
# extracted red flag, src_line traceable) is written to data/fincen/derived/<id>.json; the
# LLM backend (THIS session — no API key, the Phase-11 T4 substitution) fills the judgment —
# status, data, build_rec, rationale, and build_logic for the BUILD_NOW gaps — and
# `--check-derived` DISPOSES via check_record. These records are an LLM-derived + checked
# corpus dataset, NOT ship typology configs.
# ---------------------------------------------------------------------------
def _derived_skeleton(advisory_id: str, md_path: Path) -> dict:
    """PURE-ish (reads md): extracted red flags -> a derived-record SKELETON (judgment empty)."""
    md = _load_md(md_path)
    flags = extract_red_flags(md)
    if not flags:
        sys.exit(f"no red-flag section found in {md_path.name} — NEEDS-ATTENTION (see --corpus)")
    resolved = md_path.resolve()
    rel = resolved.relative_to(ROOT) if resolved.is_relative_to(ROOT) else md_path
    indicators = [{
        "id": f"IND-{i:02d}",
        "section": f["section"],
        "flag": f["text"],
        "src_line": f["line"],
        "status": None,        # FILL (LLM): covered | partial | gap
        "data": None,          # FILL (LLM): available | partial | insufficient
        "build_rec": None,     # FILL (LLM): MUST equal build_rec_category(status, data)
        "rationale": None,     # FILL (LLM): one line on the recommendation
        # build_logic (FILL on BUILD_NOW only): {signal_name, class, features[], logic, window, source, route}
    } for i, f in enumerate(flags, 1)]
    return {
        "id": advisory_id,
        "advisory": md_path.stem.upper(),
        "source_md": str(rel),
        "extraction_quality": extraction_quality(flags),
        "provenance": ("LLM-backend-derived (this session, no API key) + deterministic-checked — "
                       "NOT a ship typology config. build_rec follows the cover×data matrix "
                       "(build_rec_category); every indicator traces to an extracted red-flag md line."),
        "indicators": indicators,
    }


def write_derived_scaffold(advisory_id: str, md_arg: str) -> int:
    md_path = Path(md_arg)
    rec = _derived_skeleton(advisory_id, md_path)
    DERIVED_DIR.mkdir(parents=True, exist_ok=True)
    out = DERIVED_DIR / f"{advisory_id}.json"
    out.write_text(json.dumps(rec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} — SKELETON ({len(rec['indicators'])} indicators, "
          f"extraction_quality={rec['extraction_quality']})")
    print("FILL (LLM backend): per indicator set status/data/build_rec/rationale — build_rec MUST "
          "equal build_rec_category(status,data); add build_logic on BUILD_NOW. Then validate: "
          f"python3 scripts/derive_signals.py --check-derived {out.relative_to(ROOT)}")
    return 0


def load_and_check_derived(path_arg: str) -> int:
    path = Path(path_arg)
    if not path.exists():
        sys.exit(f"no such record {path}")
    try:
        rec = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.exit(f"{path.name}: not valid JSON ({e})")
    md_path = ROOT / rec.get("source_md", "")
    if not md_path.exists():
        sys.exit(f"source_md {rec.get('source_md')!r} not found — cannot check traceability")
    violations = check_record(rec, _load_md(md_path))
    if violations:
        print(f"CHECK FAIL — {path.name}: {len(violations)} violation(s):", file=sys.stderr)
        for v in violations:
            print(f"  - {v}", file=sys.stderr)
        return 1
    inds = rec["indicators"]
    builds = [i for i in inds if i.get("build_rec") == "BUILD_NOW"]
    by_rec: dict[str, int] = {}
    for i in inds:
        by_rec[i["build_rec"]] = by_rec.get(i["build_rec"], 0) + 1
    spread = " · ".join(f"{k}={v}" for k, v in sorted(by_rec.items()))
    print(f"CHECK OK — {path.name}: {len(inds)} indicators, all build_recs matrix-consistent + "
          f"traceable; {len(builds)} BUILD_NOW w/ build_logic. [{spread}]")
    return 0


def selftest() -> int:
    flags = extract_red_flags(_load_md(EFE_MD))
    behavioral = [f for f in flags if f["section"] == "behavioral"]
    financial = [f for f in flags if f["section"] == "financial"]
    print(f"extracted {len(flags)} red flags "
          f"(behavioral={len(behavioral)}, financial={len(financial)})")
    ok = (
        len(behavioral) == _EFE_BEHAVIORAL
        and len(financial) == _EFE_FINANCIAL
        and all(f["text"] and f["line"] for f in flags)
        and bool(financial) and "Dormant accounts" in financial[0]["text"]
    )
    if not ok:
        print(f"SELFTEST FAIL — expected behavioral={_EFE_BEHAVIORAL}, "
              f"financial={_EFE_FINANCIAL}; first financial must start at the "
              f"'Dormant accounts' red flag (the elder target's source)", file=sys.stderr)
        return 1
    check_fails = _checks_selftest()
    if check_fails:
        print("CHECKS SELFTEST FAIL:", *check_fails, sep="\n  ", file=sys.stderr)
        return 1
    print("SELFTEST PASS (EFE extraction 12+12 · deterministic build-rec + traceability checks)")
    return 0


# A single extracted "flag" longer than this is almost certainly several flags glued
# together (an advisory whose list isn't blank-line separated — markitdown dropped the
# bullet glyphs). We FLAG that rather than report a bogus count (Phase-12 abort rule).
# Calibrated across the committed corpus: genuine single flags top out ~573 chars
# (fin-2025-a003); cleanly blank-separated advisories max ~490; glued blocks run 630–1300+.
# 600 sits in the gap — above legit single flags, below the glued floor.
_MAX_FLAG_CHARS = 600
_MIN_CLEAN_FLAGS = 3


def extraction_quality(flags: list) -> str:
    """Classify an extraction: 'none' | 'low' (unsplit/partial — review) | 'clean'. PURE."""
    if not flags:
        return "none"
    if len(flags) < _MIN_CLEAN_FLAGS or max(len(f["text"]) for f in flags) > _MAX_FLAG_CHARS:
        return "low"
    return "clean"


def _section_counts(flags: list) -> dict:
    """PURE: per-section flag counts, in the order sections are first encountered."""
    counts: dict[str, int] = {}
    for f in flags:
        counts[f["section"]] = counts.get(f["section"], 0) + 1
    return counts


def _load_index() -> dict:
    """advisory id -> {title, date, url, …} from the committed crawl manifest (best-effort).

    Missing/malformed index.json degrades to empty metadata (titles blank) rather than failing
    — the extraction status is the load-bearing data; titles are presentation polish.
    """
    if not INDEX_JSON.exists():
        return {}
    try:
        entries = json.loads(INDEX_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return {e["id"]: e for e in entries if isinstance(e, dict) and e.get("id")} \
        if isinstance(entries, list) else {}


def corpus_status_records() -> list:
    """PURE-ish (reads corpus md + index.json): per-advisory extraction-status records.

    The deterministic input the corpus-explorer build consumes. For every committed advisory
    md: its extraction quality (clean | low | none), flag count, per-section counts, the
    title/date/url/source attribution (from index.json), and a `derivable` flag (a red-flag
    section was confidently found — none ⇒ non-derivable, e.g. the FATF jurisdiction advisories).
    Deterministic: md glob is sorted and section counts keep encounter order.
    """
    mds = sorted(CORPUS_DIR.glob("*.md"))
    if not mds:
        sys.exit(f"no corpus md under {CORPUS_DIR.relative_to(ROOT)} — acquire/convert first")
    index = _load_index()
    records = []
    for p in mds:
        flags = extract_red_flags(p.read_text(encoding="utf-8"))
        q = extraction_quality(flags)
        meta = index.get(p.stem, {})
        advisory_no = p.stem.upper()
        title = meta.get("title", "")
        source = f"FinCEN {advisory_no}" + (f" · {title}" if title else "") \
            + " · public domain (17 U.S.C. 105)"
        records.append({
            "id": p.stem,
            "advisory": advisory_no,
            "title": title,
            "date": meta.get("date", ""),
            "url": meta.get("url", ""),
            "source": source,
            "extraction": q,
            "flag_count": len(flags),
            "sections": _section_counts(flags),
            "derivable": q != "none",
        })
    return records


def write_corpus_status() -> int:
    """Emit data/fincen/corpus-status.json — the committed manifest the corpus build reads."""
    records = corpus_status_records()
    summary = {"clean": 0, "low": 0, "needs": 0, "total": len(records)}
    for r in records:
        summary[{"clean": "clean", "low": "low", "none": "needs"}[r["extraction"]]] += 1
    manifest = {
        "_generated_by": "scripts/derive_signals.py --corpus-status",
        "_note": ("Deterministic extraction-status manifest for the corpus-explorer build "
                  "(scripts/build.py corpus reads this + data/fincen/derived/*.json). Authoring "
                  "artifact, NOT a ship config. Regenerate after the corpus md set changes."),
        "summary": summary,
        "advisories": records,
    }
    CORPUS_STATUS_JSON.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {CORPUS_STATUS_JSON.relative_to(ROOT)} — {len(records)} advisories "
          f"({summary['clean']} clean · {summary['low']} low · {summary['needs']} needs)")
    return 0


def corpus_report() -> int:
    """Run extract_red_flags across the whole committed FinCEN corpus + report per advisory.

    Deterministic + offline. Classifies each advisory CLEAN (cleanly extracted, blank-block
    or header format) / LOW-CONFIDENCE (a section was found but the list didn't split — an
    unsplit giant block or too few flags, likely a non-blank-separated advisory) / NEEDS-
    ATTENTION (no red-flag section found). This is the honest validation of the deterministic
    spine across the heterogeneous corpus (Phase 12) — it flags non-conformers, never forces a
    bogus count. Exit 0 always (a flagged advisory is a reported finding, not a tool failure).
    """
    mds = sorted(CORPUS_DIR.glob("*.md"))
    if not mds:
        sys.exit(f"no corpus md under {CORPUS_DIR.relative_to(ROOT)} — acquire/convert first")
    clean = low = attn = 0
    print(f"corpus: {len(mds)} advisories under {CORPUS_DIR.relative_to(ROOT)}\n")
    for p in mds:
        flags = extract_red_flags(p.read_text(encoding="utf-8"))
        q = extraction_quality(flags)
        if q == "none":
            print(f"  {p.stem:14}  NEEDS-ATTENTION   no red-flag section confidently found")
            attn += 1
            continue
        by_section = _section_counts(flags)
        summary = " · ".join(f"{lbl}={n}" for lbl, n in by_section.items())
        if q == "low":
            print(f"  {p.stem:14}  LOW-CONFIDENCE    {len(flags)} block(s) [{summary}] — review "
                  f"(unsplit/partial; likely no blank separators)")
            low += 1
        else:
            print(f"  {p.stem:14}  CLEAN  {len(flags):>3} flags   [{summary}]")
            clean += 1
    print(f"\n{clean} clean · {low} low-confidence · {attn} needs-attention  / {len(mds)} "
          f"(deterministic spine — heterogeneous corpus, flagged not forced)")
    return 0


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    cmd = argv[0]
    if cmd == "--selftest":
        return selftest()
    if cmd == "--corpus":
        return corpus_report()
    if cmd == "--corpus-status":
        return write_corpus_status()
    if cmd == "--list":
        path = Path(argv[1]) if len(argv) > 1 else EFE_MD
        for f in extract_red_flags(_load_md(path)):
            print(f"{f['section'][:4]}\t{f['n']:>2}\tL{f['line']}\t{f['text']}")
        return 0
    if cmd == "--scaffold":
        if len(argv) < 3:
            sys.exit("usage: --scaffold <id> <md-path>")
        return write_scaffold(argv[1], argv[2])
    if cmd == "--draft":
        if len(argv) < 3:
            sys.exit("usage: --draft <id> <md-path>")
        return write_draft(argv[1], argv[2])
    if cmd == "--scaffold-derived":
        if len(argv) < 3:
            sys.exit("usage: --scaffold-derived <id> <md-path>")
        return write_derived_scaffold(argv[1], argv[2])
    if cmd == "--check-derived":
        if len(argv) < 2:
            sys.exit("usage: --check-derived <record.json>")
        return load_and_check_derived(argv[1])
    sys.exit(f"unknown option '{cmd}'. See --help.")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
