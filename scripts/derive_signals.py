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
    python3 scripts/derive_signals.py --selftest             # offline: parse the EFE md + assert
    python3 scripts/derive_signals.py --list <md-path>       # offline: print the extracted red flags
    python3 scripts/derive_signals.py --scaffold <id> <md>   # offline: md -> <id>.draft.json SKELETON
    python3 scripts/derive_signals.py --draft <id> <md>      # LIVE (authoring): + LLM-drafted judgment

The --draft mode calls the Anthropic API (claude-opus-4-8) to PROPOSE the judgment
fields (status per indicator, the single indicator/candidate target, the signal
definition); it needs ANTHROPIC_API_KEY in the environment and `anthropic` installed
in the gitignored authoring venv. The LLM proposes; build.py + schema + the two human
gates dispose. The key NEVER enters the ship artifact — --draft is build-time only.
"""
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EFE_MD = ROOT / "data" / "fincen" / "fin-2022-a002.md"
TYPOLOGY_DIR = ROOT / "config" / "typologies"

# The committed EFE advisory enumerates exactly these red-flag counts (Phase 7: "24 red
# flags intact"). Pinning them makes --selftest a deterministic validator at the boundary.
_EFE_BEHAVIORAL = 12
_EFE_FINANCIAL = 12

# Section anchors in the verbatim FinCEN advisory markdown (post-markitdown). markitdown
# drops the source bullet glyphs and interleaves page artifacts, so we anchor on the
# stable intro phrases and group blank-line-separated blocks rather than trust list markers.
_BEHAVIORAL_ANCHOR = re.compile(r"behavioral red flags.*may include", re.I)
_FINANCIAL_HEADER = re.compile(r"^financial red flags$", re.I)  # bare header ends the behavioral list
_FINANCIAL_ANCHOR = re.compile(r"financial red flags.*may include", re.I)
# financial list ends at the first footnote ref ("47.  Id.") or the next major section
_SECTION_END = re.compile(r"^(\d+\.\s|reminder of relevant bsa)", re.I)
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


def extract_red_flags(md: str) -> list[dict]:
    """PURE: FinCEN advisory markdown -> the enumerated red-flag list.

    Returns [{section: 'behavioral'|'financial', n, text, line}] where `n` is the 1-based
    index within its section and `line` is the source line in the markdown (traceability).
    No I/O — deterministic, offline-reproducible.
    """
    # split on "\n" (NOT splitlines) so line numbers match \n-based editors/tools; the
    # markdown carries form-feed page breaks that splitlines() would split on (drift vs L507).
    lines = list(enumerate(md.split("\n"), 1))
    behav_anchor = fin_header = fin_anchor = None
    for lineno, text in lines:
        stripped = text.strip()
        if behav_anchor is None:
            if _BEHAVIORAL_ANCHOR.search(stripped):
                behav_anchor = lineno
        elif fin_header is None:
            if _FINANCIAL_HEADER.match(stripped):
                fin_header = lineno
        elif fin_anchor is None:
            if _FINANCIAL_ANCHOR.search(stripped):
                fin_anchor = lineno
                break
    if not (behav_anchor and fin_header and fin_anchor):
        return []  # anchors not found — caller (selftest / fallback) handles it

    def span(start_exclusive, stop_pred):
        out = []
        for lineno, text in lines:
            if lineno <= start_exclusive:
                continue
            if stop_pred(lineno, text):
                break
            out.append((lineno, text))
        return out

    behavioral = span(behav_anchor, lambda ln, _t: ln >= fin_header)
    financial = span(fin_anchor, lambda _ln, t: bool(_SECTION_END.match(_clean(t))))

    flags: list[dict] = []
    for section, section_lines in (("behavioral", behavioral), ("financial", financial)):
        n = 0
        for start, text in _blocks(section_lines):
            text = _BULLET.sub("", text).strip()
            if not text:
                continue
            n += 1
            flags.append({"section": section, "n": n, "text": text, "line": start})
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
    print("SELFTEST PASS")
    return 0


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    cmd = argv[0]
    if cmd == "--selftest":
        return selftest()
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
    sys.exit(f"unknown option '{cmd}'. See --help.")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
