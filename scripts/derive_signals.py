#!/usr/bin/env python3
"""Dispose of an LLM-derived FinCEN-advisory record — AUTHORING-TIME ONLY (the GATE).

Part of the Signal Watch ingestion pipeline. The boundary is INVERTED (Phase 16) and the
deterministic EXTRACTOR is now DELETED (Phase 17 — the real subtraction): the LLM EXTRACTS
the enumerated red flags + per-indicator judgment (a generative task it does well across the
heterogeneous + glued corpus, where structural parsing was brittle and accreted special-casing
every phase); this module is the DETERMINISTIC GATE that DISPOSES. The pipeline:

    crawl_fincen.py    -> data/fincen/index.json   (manifest)
    acquire_fincen.py  -> data/fincen/raw/<id>.pdf (resolve + download)
    pdf_to_md.py       -> data/fincen/<id>.md      (verbatim source of truth)
    (LLM backend)      -> data/fincen/derived/<id>.json   (extract + judgment)
    derive_signals.py  -> --check-derived DISPOSES   (THIS TOOL — the gate)
    build.py           -> dist/corpus/index.html

NON-NEGOTIABLE: nothing here ever runs in the ship artifact. The engine never imports this;
build.py stays stdlib-only, never calls an LLM, and never imports this tool. Developer tool.

THE GATE (check_record) — what disposes of what the LLM proposed (no neural judge at the
boundary): (1) each indicator's build_rec follows the cover×data matrix (build_rec_category);
(2) GROUNDEDNESS — every indicator's verbatim `flag` is a substring of the source md under
normalize() (the traceability authority; replaces the deleted src_line ∈ extract_red_flags
structural parse); (3) RELEVANCE — the flag's src_line falls inside the red-flag region
(rf_region), so a grounded-but-irrelevant quote lifted from the overview / SAR section is
rejected; (4) a BUILD_NOW indicator carries build_logic with the full definition shape.
The LLM backend is a live model session acting as backend (no API key) — it PROPOSES the
extraction + judgment; the deterministic gate + the two human gates DISPOSE. Derived records
are an LLM-derived + checked corpus dataset, NOT ship typology configs (the 3 hand-curated
typologies stay the byte-frozen showcase).

FinCEN advisories are U.S. federal works in the public domain (17 U.S.C. 105).

Usage:
    python3 scripts/derive_signals.py --selftest             # offline: gate checks (build-rec matrix
                                                             #   + quote-grounding + relevance + shape)
    python3 scripts/derive_signals.py --check-derived <record.json>  # offline: DISPOSE a derived record
    python3 scripts/derive_signals.py --corpus [source_dir]        # offline: cheap rf_region triage across a source
    python3 scripts/derive_signals.py --corpus-status [source_dir] # offline: emit <source_dir>/corpus-status.json
                                                             #   (source_dir defaults to data/fincen — Phase 20 multi-source)

TRIAGE (the rf_region-bounded counter — replaces the deleted extractor's counting role):
  --corpus / --corpus-status are a cheap deterministic HINT, never the derivation authority. For
  every committed advisory md they report whether a red-flag REGION exists (rf_region — false ONLY
  for the 2 FATF jurisdiction advisories, which carry no enumerated red-flag list) and a coarse
  flag_count from the blank-separated blocks inside that region (_rf_triage). An advisory goes
  "live" in the explorer by the presence of a gate-passing data/fincen/derived/<id>.json — NOT by
  this triage. The chip/count a not-yet-derived advisory shows in the explorer comes from here; a
  derived advisory renders from its record's indicators (build.py ignores the manifest flag_count
  for live advisories), so the counter need only be a rough hint.

  --corpus-status emits data/fincen/corpus-status.json (committed): per-advisory extraction hint +
  flag/section counts + title/date/source attribution (titles from index.json) + a derivable flag.
  This is the deterministic data artifact the CORPUS-EXPLORER build reads (scripts/build.py corpus
  merges it with data/fincen/derived/*.json) — build.py never imports this tool; it consumes the
  committed manifest. Regenerate after the corpus md set changes.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# CORPUS_DIR is the DEFAULT corpus source (fincen-advisories). Phase 20 — multi-source: the
# per-source functions below take a `source_dir`, so OTHER FinCEN publication types (e.g.
# data/fincen-alerts/) regenerate their own corpus-status.json with the SAME gate + triage via
# `--corpus-status [source_dir]`. Each source dir holds <id>.md + index.json + corpus-status.json.
# The gate (check_record/rf_region/normalize) is source-agnostic and unchanged across sources.
CORPUS_DIR = ROOT / "data" / "fincen"
EFE_MD = CORPUS_DIR / "fin-2022-a002.md"  # selftest gate fixture (verbatim EFE red flags)

# Red-flag REGION anchors — the heading/intro that OPENS an advisory's enumerated red-flag
# list. These now serve rf_region() (the relevance region the gate cites) + the _rf_triage()
# block counter — NOT a structural parse (the extractor that consumed them was deleted in
# Phase 17). FinCEN advisories open that list heterogeneously across the committed corpus:
#   INTRO  : "<category> red flags [indicators] ... may include / the following ... red flags"
#            (EFE fin-2022-a002, ransomware fin-2021-a004, kleptocracy fin-2022-a001, …)
#   HEADER : a standalone "<Category> Red Flags" line directly above the list
#            (fin-2024-a002 "Transactional Red Flags", …)
# Tier-1 = clean headers + explicit list-intros; the Tier-2 LOOSE header (trailing-clause
# title) + WEAK "identified red flags" intro are the fallback for a purely-titled advisory.
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
# Phase 21 — OFAC vocabulary. OFAC sanctions advisories open their indicator list with vocab other than
# "red flags": a standalone "<Category> Risk Indicators / Deceptive [Shipping] Practices / Risk Factors"
# HEADER (maritime "Deceptive Practices", art/VC "Risk Indicators"), or a "risk indicators … may be /
# include" INTRO. These mirror the FinCEN anchors (the red-flag-template OFAC advisories — e.g. the Sham
# Transactions advisory's "the red flags listed below" — already match _RF_INTRO unchanged). They are
# inert for the committed FinCEN corpus (verified across all 33 mds: the OFAC vocab appears in FinCEN
# text ONLY mid-prose — e.g. "deceptive shipping practices" in a few advisories, and "risk factors" in a
# footnote citation — NEVER as a line-start heading or a list lead-in, and both anchors require that
# position (the HEADER `^…:?$`, the INTRO a "may be/include"-style lead-in)), so every FinCEN rf_region
# stays byte-unchanged — pinned by the --selftest fixtures + the all-33-md baseline check. The HEADER also
# excludes table-of-contents dotted-leader lines (the trailing `:?$` rejects "Risk Indicators ...... 17").
_RF_HEADER_OFAC = re.compile(
    r"^(?:[A-Z][\w’'/-]*(?:\s+(?:[A-Z][\w’'/-]*|and|of|the|&|for)){0,4}\s+)?"
    r"(?:risk\s+indicators?|deceptive\s+(?:shipping\s+)?practices?|risk\s+factors?)\s*:?$", re.I)
_RF_INTRO_OFAC = re.compile(
    r"\brisk\s+indicators?\b[^.\n]{0,80}?\b(?:may\s+be|may\s+include|include|as\s+follows|listed\s+below)\b"
    r"|\bthe\s+following\b[^.\n]{0,50}?\brisk\s+indicators?\b", re.I)
# Phase 22 — FINTRAC vocabulary (the FIRST cross-jurisdiction source: Canada's FIU). FINTRAC Operational
# Alerts open their enumerated list with "indicators", not "red flags": a standalone "Money laundering |
# Terrorist (activity) financing | ML/TF indicators" HEADER directly above the bulleted list (e.g. the
# underground-banking OA's "Money laundering indicators"), or that same ML/TF-specific phrase in a "…
# indicators … may be/include" INTRO. DELIBERATELY NARROW — restricted to the ML/TF-qualified phrasing,
# NOT a broad "<category> indicators": fin-2020-a008 carries header-glued "Financial Indicators" /
# "Behavioral Indicators" lines, so a bare "indicators" anchor would shift its rf_region. The qualified
# forms have ZERO occurrences anywhere across all 36 committed FinCEN+OFAC mds (verified — not even
# mid-prose, unlike OFAC's "deceptive shipping practices"), so every existing rf_region stays byte-
# unchanged, pinned by the --selftest fixtures + the all-36-md baseline. The HEADER's trailing `:?$`
# excludes a "… indicators ..... 12" TOC dotted-leader line. The grounding core (normalize/check_record)
# is untouched — only this relevance-region anchor set widens.
_RF_HEADER_FINTRAC = re.compile(
    r"^(?:money\s+laundering(?:\s+(?:and|&|/)\s+terrorist\s+(?:activity\s+)?financing)?"
    r"|terrorist\s+(?:activity\s+)?financing"
    r"|ml\s*(?:[/&]|and)\s*tf)"
    r"\s+indicators?\b"
    # optional trailing topic clause — the section-TITLE form (e.g. "Money laundering indicators of
    # synthetic opioid activity"), mirroring FinCEN's strict-vs-LOOSE _RF_HEADER split. The clause must
    # START with a connector (of/related to/for/…), so a TOC dotted-leader line ("… indicators .... 12")
    # is NOT consumed (no `.*` catch-all). Still regression-safe: the ML/TF base phrase occurs 0× in all
    # 36 FinCEN+OFAC mds, so no line starts with it, clause or no clause.
    r"(?:\s+(?:of|related\s+to|for|associated\s+with|in)\b.*)?\s*:?$", re.I)
_RF_INTRO_FINTRAC = re.compile(
    r"\b(?:money\s+laundering|terrorist\s+(?:activity\s+)?financing|ml\s*(?:[/&]|and)\s*tf)"
    r"\s+indicators?\b[^.\n]{0,80}?"
    r"\b(?:may\s+(?:be|include|reflect)|reflective\s+of|listed\s+below|as\s+follows|include)\b", re.I)
# Phase 23 — FINTRAC INVERTED "Indicators of <X>" heading form. The Operational BRIEFS (real estate)
# and some OAs (professional ML) head their enumerated lists with "indicators" LEADING — "Indicators
# of money laundering", "Indicators of professional money laundering through …", "Indicators relating
# to romance fraud victims" — vs the forward "Money laundering indicators" the HEADER above matches.
# The regression trap: a boilerplate FINTRAC SENTENCE — "Indicators of <ML/TF> can be thought of as
# red flags …" — opens the existing 3 FINTRAC OAs BEFORE their forward heading, so a naive inverted
# anchor would shift underground-banking / synthetic-opioids / terrorist-financing's rf_region. Two
# narrow branches keep it 0-shift across all 39 existing FinCEN+OFAC+FINTRAC mds (verified): (1) the
# "of <ML/TF>" branch REQUIRES the line to END at the ML phrase (`:?$`) or continue with a CONNECTOR-
# led clause (by/through/of/related to/for/associated with/in) — the boilerplate continues with "can"
# (not a connector, not EOL) so it is excluded, exactly mirroring the forward HEADER's strict-vs-
# trailing-clause split; (2) the "relating to | associated with <topic>" branch uses connectors the
# boilerplate (always "of") never uses → 0 collision, so it may be topic-broad. Grounding core
# (normalize/check_record) is untouched — only this relevance-region anchor widens.
_RF_HEADER_FINTRAC_INV = re.compile(
    r"^(?:\d+\.\s+)?indicators\s+(?:"
    r"of\s+(?:[\w-]+\s+){0,2}?"
    r"(?:money\s+laundering|terrorist\s+(?:activity\s+)?financing|ml\s*(?:[/&]|and)\s*tf)"
    r"(?:\s+(?:by|through|of|related\s+to|for|associated\s+with|in)\b.*)?"
    r"|(?:relating\s+to|associated\s+with)\s+\w.*"
    r")\s*:?$", re.I)
# A block that is itself a footnote/citation, not a red flag (Phase-12 filter, retained for the
# _rf_triage block counter): a footnote-numbered line, a legal "supra note"/"Id." marker, a
# federal case-docket number, or a block ending in a "(Mon[ DD], YYYY)" citation date — real red
# flags describe behaviour, they don't end in a cite or carry a docket number.
_CITATION = re.compile(
    r"^\d+\.\s"
    r"|\b(?:supra\s+note|\bid\.\b|see\s+(?:also\s+)?(?:fincen|fbi|doj|ofac|fatf|cisa|dhs|u\.s\.))"
    r"|\b\d{1,2}:\d{2}-[a-z]{2,3}-\d{2,}\b"
    r"|\([A-Z][a-z]{2,8}\.?\s+(?:\d{1,2},\s+)?\d{4}\)\.?\s*$", re.I)
_PAGE_NUM = re.compile(r"^\d+$")
_RUNNING_HEADER = re.compile(r"^\s*FINCEN ADVISORY\s*")  # running header glued to content


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






def _load_md(path: Path) -> str:
    if not path.exists():
        sys.exit(f"missing markdown {path} — run the acquire/convert pipeline first")
    return path.read_text(encoding="utf-8")



# ---------------------------------------------------------------------------
# Deterministic checks on a DERIVED record. The LLM backend EXTRACTS + PROPOSES, per indicator,
# the verbatim red-flag `flag`, a coverage status + data availability, a build recommendation,
# and (for buildable gaps) build logic; these checks DISPOSE — a record only stands if its
# recommendations follow the cover×data matrix and every indicator QUOTE-GROUNDS to the source
# md (normalize(flag) ⊂ normalize(md)) inside the red-flag region. LLM proposes, the
# deterministic gate disposes — no neural judge at the check boundary.
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


# ---------------------------------------------------------------------------
# Phase 16 — the INVERTED boundary. The LLM EXTRACTS candidate red flags (a generative task it
# does well across the heterogeneous corpus, where structural parsing is brittle); the
# deterministic layer is a GATE that DISPOSES. Traceability moved from src_line ∈
# extract_red_flags() (a structural parse that accreted special-casing every phase, yet whose
# output the LLM already overrode) to QUOTE-GROUNDING: a record's verbatim `flag` must be a
# substring of the source md under normalize(), which collapses the CLOSED set of md artifacts.
# Plus a cheap section-cite RELEVANCE guard (the flag's src_line must sit inside the red-flag
# region), so a grounded-but-irrelevant quote (lifted from the overview or the SAR section) is
# rejected. Grounding proves the text is REAL; the region proves it's a RED FLAG; the LLM
# extracts; the deterministic gate + the two human gates dispose.
# ---------------------------------------------------------------------------
def normalize(text: str) -> str:
    """PURE: collapse text to lowercase alphanumerics for position-free quote-grounding.

    One rule absorbs every md artifact at once — line wraps, word-wrap hyphens
    ('foreign-\\nbased' == 'foreign-based'), smart quotes, punctuation, footnote-ref digits, and
    the page-break running header ('FINCEN ADVISORY' and the letter-spaced
    'F I N C E N A D V I S O R Y' both collapse to 'fincenadvisory', which we drop). The gate
    checks normalize(flag) in normalize(md). Far simpler than parsing structure — the complexity
    that used to live in extract_red_flags' section-finding collapses to this closed normalizer.
    """
    collapsed = re.sub(r"[^a-z0-9]+", "", text.lower())
    return collapsed.replace("fincenadvisory", "")


# The red-flag region ends at the first document-level terminal AFTER the first red-flag anchor —
# the standard FinCEN closing sections, which always follow every red-flag list. Deliberately
# narrow (no generic numbered-section match) so a numbered SUBsection inside the region can't
# truncate it early.
_RF_REGION_END = re.compile(
    r"^(?:reminder of\b|for further information|sar (?:filing|reporting)"
    r"|frequently asked|the information contained in this advisory)", re.I)


def rf_region(md: str):
    """PURE: (start_line, end_line) bounding the red-flag region, or None if no anchor found.

    Coarse + robust: the FIRST red-flag heading/intro anchor (reusing the calibrated _RF_*
    patterns) up to the first _RF_REGION_END terminal after it (else EOF). One start anchor + one
    terminal — no per-flag parsing. Used ONLY for the section-cite relevance guard (decision A),
    so over-inclusiveness is safe; the strong guarantee is grounding.
    """
    lines = [(ln, _clean(raw)) for ln, raw in enumerate(md.split("\n"), 1)]
    start = None
    for ln, t in lines:
        if t and (_RF_HEADER.match(t) or _RF_HEADER_LOOSE.match(t)
                  or _RF_INTRO.search(t) or _RF_INTRO_WEAK.search(t)
                  or _RF_HEADER_OFAC.match(t) or _RF_INTRO_OFAC.search(t)  # Phase 21: OFAC vocab
                  or _RF_HEADER_FINTRAC.match(t) or _RF_INTRO_FINTRAC.search(t)  # Phase 22: FINTRAC vocab
                  or _RF_HEADER_FINTRAC_INV.match(t)):  # Phase 23: FINTRAC inverted "Indicators of X" form
            start = ln
            break
    if start is None:
        return None
    for ln, t in lines:
        if ln > start and t and _RF_REGION_END.match(t):
            return (start, ln)
    return (start, (lines[-1][0] + 1) if lines else start + 1)


# A grounded `flag` must clear a minimum normalized length — a too-short generic span (e.g.
# "a customer") would trivially substring-match the md and pass. Real red flags are full sentences;
# 24 normalized chars (~4–5 words) cleanly separates them from a degenerate fragment. Mirrors the
# extractor's old `len(text) < 20` stray-fragment floor, recomputed on whitespace-stripped text.
_MIN_FLAG_NCHARS = 24


def check_record(record: dict, md: str) -> list:
    """PURE: run all deterministic checks on a derived record; return violations ([] = OK).

    Disposes of what the LLM backend proposed (Phase 16 — inverted boundary, the LLM extracts):
    (1) each indicator's build_rec follows the cover×data matrix; (2) GROUNDEDNESS — every
    indicator's verbatim `flag` is a substring of the source md under normalize() (the
    traceability authority, replacing the old src_line ∈ extract_red_flags() structural parse);
    (3) RELEVANCE — the flag's src_line falls inside the advisory's red-flag region, so a grounded
    quote lifted from the overview / SAR section is rejected (the cheap section-cite guard);
    (4) a BUILD_NOW indicator carries build_logic with the full definition shape, COVERED/
    SOURCE_DATA carry none.
    """
    violations: list = []
    inds = record.get("indicators")
    if not isinstance(inds, list) or not inds:
        return ["record has no indicators[]"]
    # indicator ids must be unique, and each must trace to a DISTINCT red flag — no two indicators
    # may carry the same grounded text (membership alone would let a collapsed duplicate through).
    ids = [ind.get("id") for ind in inds]
    if len(ids) != len(set(ids)):
        violations.append(f"duplicate indicator id(s): {sorted({i for i in ids if ids.count(i) > 1})}")
    norms = [normalize(ind.get("flag") or "") for ind in inds]
    dups = sorted({n[:48] for n in norms if n and norms.count(n) > 1})
    if dups:
        violations.append(f"{len(dups)} flag text(s) repeated across indicators — each must trace to a distinct red flag")
    nmd = normalize(md)
    region = rf_region(md)
    if region is None:
        violations.append("no red-flag region found in source md — advisory not cleanly derivable (relevance gate)")
    for ind in inds:
        iid = ind.get("id", "?")
        v = check_build_rec(ind.get("status"), ind.get("data"), ind.get("build_rec"))
        if v:
            violations.append(f"{iid}: {v}")
        flag = ind.get("flag")
        nflag = normalize(flag) if isinstance(flag, str) else ""
        if not (isinstance(flag, str) and flag.strip()):
            violations.append(f"{iid}: missing flag text — cannot ground")
        elif len(nflag) < _MIN_FLAG_NCHARS:
            violations.append(f"{iid}: flag too short ({len(nflag)} normalized chars < {_MIN_FLAG_NCHARS}) — a degenerate/generic span, not a red flag")
        elif nflag not in nmd:
            violations.append(f"{iid}: flag not grounded in source md (not a verbatim red-flag span)")
        elif region is not None:
            sl = ind.get("src_line")
            if not (isinstance(sl, int) and region[0] <= sl < region[1]):
                violations.append(f"{iid}: src_line {sl!r} outside the red-flag region {region} (relevance)")
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
    # record check: a valid record passes; tampered ones fail on every axis. Phase 16: records
    # now carry the verbatim `flag` and the gate GROUNDS it (normalize(flag) in normalize(md)).
    md = _load_md(EFE_MD)
    # Two VERBATIM EFE financial red flags (grounded inside rf_region(EFE)=(419,539)) as the gate
    # fixture — replaces the deleted extract_red_flags, regression-pinning the GATE itself rather
    # than a structural parse. These are the elder target's source flags (md L507/L509).
    f0 = {"flag": "Dormant accounts with large balances begin to show constant withdrawals.",
          "line": 507}
    f1 = {"flag": "An older customer purchases large numbers of gift cards or prepaid access cards.",
          "line": 509}
    good_logic = {k: (["dormancy_days_prior", "outbound_value_ratio"] if k == "features" else "x")
                  for k in _DEFN_KEYS}
    good = {"indicators": [
        {"id": "IND-01", "section": "financial", "flag": f0["flag"],
         "src_line": f0["line"], "status": "gap", "data": "available",
         "build_rec": "BUILD_NOW", "build_logic": good_logic},
        {"id": "IND-02", "section": "financial", "flag": f1["flag"],
         "src_line": f1["line"], "status": "covered", "data": "available",
         "build_rec": "COVERED"},
    ]}
    if check_record(good, md):
        fails.append(f"valid record rejected: {check_record(good, md)}")
    # tampered: a matrix contradiction + a FABRICATED (ungrounded) flag must both be caught
    bad = json.loads(json.dumps(good))
    bad["indicators"][0]["build_rec"] = "COVERED"   # contradicts gap+available
    bad["indicators"][1]["flag"] = "this sentence appears nowhere in the advisory source text"
    if len(check_record(bad, md)) < 2:
        fails.append("tampered record not caught (matrix contradiction + ungrounded flag — expected ≥2)")
    # a PARAPHRASE (real meaning, reworded — NOT a verbatim span) must be rejected: grounding is verbatim
    para = json.loads(json.dumps(good))
    para["indicators"][0]["flag"] = "the customer reactivates a long dormant account and quickly drains the balance"
    if not check_record(para, md):
        fails.append("paraphrased (non-verbatim) flag not caught by grounding")
    # a DEGENERATE too-short prefix grounds (it IS a verbatim substring) but the length floor must reject it
    tiny = json.loads(json.dumps(good))
    tiny["indicators"][0]["flag"] = f0["flag"][:12]
    if not check_record(tiny, md):
        fails.append("degenerate too-short flag not caught by the length floor")
    # build_logic SHAPE hole must be closed: features-as-int + empty logic must both be caught
    shape_bad = json.loads(json.dumps(good))
    shape_bad["indicators"][0]["build_logic"]["features"] = 123
    shape_bad["indicators"][0]["build_logic"]["logic"] = ""
    if len(check_record(shape_bad, md)) < 2:
        fails.append("build_logic-shape hole not caught (features-as-int + empty logic)")
    # a duplicate indicator id must be caught
    dup = json.loads(json.dumps(good))
    dup["indicators"][1]["id"] = "IND-01"
    if not check_record(dup, md):
        fails.append("duplicate indicator id not caught")
    # Phase-16 normalizer invariants (the closed artifact set) + the escrow grounding STRESS case
    # (header-glued 'FINCEN ADVISORY' prefix + a 'foreign-\nbased' word-wrap hyphen at src L499).
    if normalize("foreign-\nbased") != normalize("foreign-based"):
        fails.append("normalize: word-wrap hyphen not collapsed")
    if normalize("a customer FINCEN ADVISORY pays") != normalize("a customer pays"):
        fails.append("normalize: page-break running header not stripped")
    a003 = CORPUS_DIR / "fin-2025-a003.md"
    if a003.exists():
        escrow = ("A customer that is a U.S.-based escrow company receives funds from an "
                  "unaffiliated, foreign- based shell company or entity in a disparate line of "
                  "business that are used to purchase real estate in the United States.")
        if normalize(escrow) not in normalize(a003.read_text(encoding="utf-8")):
            fails.append("normalize: escrow stress flag (header-glued + hyphen-wrap) not grounded")
    # _rf_triage is a COARSE hint, NOT a flag-accurate count — pin that it tracks blank-line
    # SEPARATORS, not flags (the Phase-17 reviewer-MEDIUM footgun, disclosed not fixed: an accurate
    # glued count would reintroduce the deleted parser). The SAME three red flags read 'low·1' when
    # glued-no-separator (one fused block) vs 'clean·3' when blank-separated; pinning both directions
    # stops a future "fix" from silently changing the documented behavior.
    rf = ["A customer makes structured cash deposits just below the reporting threshold across multiple branches in a single day.",
          "A customer's account receives many small incoming transfers that are immediately aggregated and wired offshore.",
          "A customer uses a business account with no apparent commercial purpose to move funds rapidly in and out."]
    glued = "\n".join(["# Advisory", "", "Financial Red Flags", *rf, "", "Reminder of Regulatory Obligations", "", "SAR text."])
    sep = "\n".join(["# Advisory", "", "Financial Red Flags", "", rf[0], "", rf[1], "", rf[2], "", "Reminder of Regulatory Obligations", "", "SAR text."])
    if _rf_triage(glued, rf_region(glued)) != ("low", 1, {"redflag": 1}):
        fails.append("_rf_triage glued pin drifted (3 glued flags must read coarse-undercount ('low', 1))")
    if _rf_triage(sep, rf_region(sep)) != ("clean", 3, {"redflag": 3}):
        fails.append("_rf_triage separated pin drifted (the same 3 blank-separated flags must read ('clean', 3))")
    # Phase 21 — OFAC vocabulary anchors (widened rf_region). Pin BOTH directions: an OFAC-style
    # "Deceptive Practices" header and a "risk indicators … may be" intro each OPEN a region; a passing
    # prose mention of the vocab (no heading, no list lead-in) does NOT falsely anchor one.
    ofac_hdr = "\n".join(["# OFAC Advisory", "", "Deceptive Practices", "",
                          "A vessel disables its AIS transponder to obscure its location during a sanctioned-port call.",
                          "", "Reminder of Sanctions Obligations", "", "x"])
    if rf_region(ofac_hdr) is None:
        fails.append("OFAC 'Deceptive Practices' header did not open an rf_region (widening regressed)")
    ofac_intro = "\n".join(["# OFAC", "", "Examples of risk indicators may be entities that:", "",
                            "An entity routes payments through a front company in a jurisdiction with no commercial nexus.",
                            "", "For further information", "", "x"])
    if rf_region(ofac_intro) is None:
        fails.append("OFAC 'risk indicators … may be' intro did not open an rf_region")
    ofac_prose = "\n".join(["# Doc", "",
                            "This paragraph mentions risk factors and risk indicators only in passing prose, never as a heading.",
                            "", "x"])
    if rf_region(ofac_prose) is not None:
        fails.append("a passing prose mention of OFAC vocab falsely opened an rf_region (anchor too loose)")
    # Phase 22 — FINTRAC vocabulary anchors (widened rf_region for Canada's FIU). Pin BOTH directions: a
    # FINTRAC-style "Money laundering indicators" header and a "ML/TF indicators … may include" intro each
    # OPEN a region; a passing prose mention of bare "indicators" (no ML/TF-qualified heading/lead-in) does
    # NOT — the narrowness that keeps fin-2020-a008's "Financial/Behavioral Indicators" region byte-stable.
    fintrac_hdr = "\n".join(["# FINTRAC Operational Alert", "", "Money laundering indicators", "",
                             "A client receives funds from multiple unrelated third parties then immediately remits them abroad.",
                             "", "For further information", "", "x"])
    if rf_region(fintrac_hdr) is None:
        fails.append("FINTRAC 'Money laundering indicators' header did not open an rf_region (widening regressed)")
    # the section-TITLE form: "<ML/TF> indicators of <topic>" (a trailing topic clause) must also OPEN a
    # region (FINTRAC's synthetic-opioids OA heads its list this way), but a TOC dotted-leader must NOT.
    fintrac_title = "\n".join(["# FINTRAC", "", "Money laundering indicators of synthetic opioid activity", "",
                               "A client structures cash deposits just below the reporting threshold across several branches.",
                               "", "For further information", "", "x"])
    if rf_region(fintrac_title) is None:
        fails.append("FINTRAC '<ML/TF> indicators of <topic>' section-title header did not open an rf_region")
    fintrac_toc = "\n".join(["# FINTRAC", "", "Money laundering indicators ........... 12", "",
                             "Body text.", "", "x"])
    if rf_region(fintrac_toc) is not None:
        fails.append("a FINTRAC TOC dotted-leader 'indicators ..... 12' line falsely opened an rf_region")
    fintrac_intro = "\n".join(["# FINTRAC", "", "The following terrorist financing indicators may include transactions where a client:", "",
                               "Sends small-value transfers to a jurisdiction associated with a listed terrorist entity.",
                               "", "For further information", "", "x"])
    if rf_region(fintrac_intro) is None:
        fails.append("FINTRAC 'terrorist financing indicators … may include' intro did not open an rf_region")
    fintrac_prose = "\n".join(["# Doc", "",
                               "This paragraph notes that various indicators were considered, only in passing prose, never as a heading.",
                               "", "x"])
    if rf_region(fintrac_prose) is not None:
        fails.append("a passing prose mention of bare 'indicators' falsely opened an rf_region (FINTRAC anchor too broad)")
    # Phase 23 — FINTRAC INVERTED "Indicators of <X>" heading form (Operational Briefs + some OAs lead
    # with "indicators"). Pin BOTH directions: the inverted "Indicators of money laundering" header, an
    # "Indicators of <qual> money laundering through …" connector-clause header, and an "Indicators
    # relating to <topic>" header each OPEN a region; the boilerplate SENTENCE "Indicators of <ML/TF>
    # can be thought of as red flags …" (which opens the existing FINTRAC OAs BEFORE their forward
    # heading) does NOT — the connector-gated `:?$` is exactly what keeps underground-banking /
    # synthetic-opioids / terrorist-financing 0-shift.
    fintrac_inv = "\n".join(["# FINTRAC Operational Brief", "", "Indicators of money laundering", "",
                             "Real estate purchased well above or below market value relative to comparable properties.",
                             "", "For further information", "", "x"])
    if rf_region(fintrac_inv) is None:
        fails.append("FINTRAC inverted 'Indicators of money laundering' header did not open an rf_region")
    fintrac_inv2 = "\n".join(["# FINTRAC", "", "Indicators of professional money laundering through money services businesses", "",
                              "A money services business processes large volumes of third-party remittances with no commercial rationale.",
                              "", "For further information", "", "x"])
    if rf_region(fintrac_inv2) is None:
        fails.append("FINTRAC inverted '<...> money laundering through <...>' connector-clause header did not open an rf_region")
    fintrac_inv_rel = "\n".join(["# FINTRAC", "", "Indicators relating to romance fraud victims", "",
                                 "A client suddenly sends escalating EMTs to a new overseas payee they cannot identify.",
                                 "", "For further information", "", "x"])
    if rf_region(fintrac_inv_rel) is None:
        fails.append("FINTRAC inverted 'Indicators relating to <topic>' header did not open an rf_region")
    fintrac_boiler = "\n".join(["# FINTRAC", "",
                                "Indicators of money laundering can be thought of as red flags indicating that something may very well be wrong.",
                                "", "Body text describing methodology, not a heading.", "", "x"])
    if rf_region(fintrac_boiler) is not None:
        fails.append("the FINTRAC boilerplate 'Indicators of <ML/TF> can be thought of as red flags …' sentence falsely opened an rf_region (inverted anchor too loose)")
    return fails



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
          f"quote-grounded; {len(builds)} BUILD_NOW w/ build_logic. [{spread}]")
    return 0


def selftest() -> int:
    """Offline GATE regression. The deleted extractor is gone; what's pinned now is check_record —
    it must accept a valid EFE record and reject every known tampering (matrix contradiction,
    ungrounded / paraphrased / degenerate-too-short flag, build_logic shape hole, duplicate id) +
    the normalizer + escrow grounding invariants (see _checks_selftest)."""
    check_fails = _checks_selftest()
    if check_fails:
        print("CHECKS SELFTEST FAIL:", *check_fails, sep="\n  ", file=sys.stderr)
        return 1
    print("SELFTEST PASS (build-rec matrix + quote-grounding + relevance + shape + normalizer checks)")
    return 0


# Cheap rf_region-bounded triage — the ONLY counting role the deleted extract_red_flags kept.
# An advisory reads "clean" if its red-flag region holds at least this many block-flags, else "low".
_MIN_CLEAN_FLAGS = 3


def _rf_triage(md: str, region) -> tuple:
    """PURE: a coarse (extraction, flag_count, sections) HINT for one advisory. NOT an extractor.

    Reuses the already-located red-flag REGION (rf_region, passed in) and counts the blank-
    separated blocks inside it that clear the grounding length floor and aren't citations — no
    section-finding, no per-format special-casing (rf_region already found the list; this just
    sizes it). The result feeds the corpus-status chip a NOT-YET-DERIVED advisory shows in the
    explorer; a derived advisory renders from its record's indicators (build.py ignores the
    manifest flag_count for live ones), so a rough hint suffices. region=None → not derivable.

    COARSE HINT, NOT a flag-accurate count: the count tracks blank-line SEPARATORS, so a
    GLUED-no-separator advisory (markitdown dropped its blank lines) UNDERCOUNTS — N fused flags
    read as one block (pinned both ways in --selftest). An accurate glued count would reintroduce
    the per-flag parser Phase 17 deleted; the inverted loop has the LLM read glued advisories
    instead, and no live (derived) record depends on this number — so the coarse hint is by design.
    """
    if region is None:
        return ("none", 0, {})
    inside = [(ln, raw) for ln, raw in enumerate(md.split("\n"), 1) if region[0] < ln < region[1]]
    n = sum(1 for _, text in _blocks(inside)
            if len(normalize(text)) >= _MIN_FLAG_NCHARS and not _CITATION.search(text))
    return (("clean" if n >= _MIN_CLEAN_FLAGS else "low"), n, {"redflag": n} if n else {})


def _load_index(source_dir: Path = CORPUS_DIR) -> dict:
    """advisory id -> {title, date, url, …} from the source's committed crawl manifest (best-effort).

    Missing/malformed index.json degrades to empty metadata (titles blank) rather than failing
    — the extraction status is the load-bearing data; titles are presentation polish.
    """
    index_json = source_dir / "index.json"
    if not index_json.exists():
        return {}
    try:
        entries = json.loads(index_json.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return {e["id"]: e for e in entries if isinstance(e, dict) and e.get("id")} \
        if isinstance(entries, list) else {}


def corpus_status_records(source_dir: Path = CORPUS_DIR) -> list:
    """PURE-ish (reads corpus md + index.json): per-advisory extraction-status records.

    The deterministic input the corpus-explorer build consumes. For every committed source md:
    a cheap rf_region triage HINT (extraction clean|low|none + flag_count + sections via
    _rf_triage), the title/date/url/source attribution (from index.json), and a `derivable` flag.
    `derivable` = a red-flag REGION exists (rf_region) — true even for the glued advisories (the
    LLM backend extracts them); false ONLY for the 2 FATF jurisdiction advisories (no red-flag
    list at all). The triage is no longer the derivability authority — a document goes "live" in
    the explorer by the presence of a gate-passing <source_dir>/derived/<id>.json.
    Phase 20: `source_dir` defaults to fincen-advisories but takes any FinCEN-publication source
    (e.g. data/fincen-alerts/) — same triage, same attribution shape. Deterministic: md glob is
    sorted; the triage reuses the calibrated rf_region span.
    """
    mds = sorted(source_dir.glob("*.md"))
    if not mds:
        sys.exit(f"no corpus md under {source_dir.relative_to(ROOT)} — acquire/convert first")
    index = _load_index(source_dir)
    records = []
    for p in mds:
        md = p.read_text(encoding="utf-8")
        region = rf_region(md)
        extraction, flag_count, sections = _rf_triage(md, region)
        meta = index.get(p.stem, {})
        advisory_no = p.stem.upper()
        title = meta.get("title", "")
        # Phase 21/22 — per-source issuer + licence basis. Issuer: FINTRAC (data/fintrac/), OFAC
        # (data/ofac/), else FinCEN. The prefix is dropped when advisory_no already starts with the
        # issuer (OFAC/FINTRAC ids are `ofac-…`/`fintrac-…`), so it never doubles; FinCEN output stays
        # byte-identical ("FinCEN FIN-2020-A008 · …"). LICENCE basis differs by jurisdiction and is the
        # compliance-load-bearing suffix: US-federal works (FinCEN, OFAC) are public domain (17 U.S.C.
        # 105 — no copyright); FINTRAC (Canadian Crown copyright) is reproduced verbatim under FINTRAC's
        # NON-COMMERCIAL reproduction terms WITH attribution — NOT public domain (kept distinct so the
        # verbatim rail never mislabels a Canadian source as US public domain).
        name = source_dir.name.lower()
        issuer = "FINTRAC" if "fintrac" in name else "OFAC" if "ofac" in name else "FinCEN"
        issuer_prefix = "" if advisory_no.startswith(issuer.upper()) else f"{issuer} "
        licence = (" · © His Majesty the King in Right of Canada — reproduced for non-commercial use "
                   "per FINTRAC's Terms & Conditions" if issuer == "FINTRAC"
                   else " · public domain (17 U.S.C. 105)")
        source = f"{issuer_prefix}{advisory_no}" + (f" · {title}" if title else "") + licence
        records.append({
            "id": p.stem,
            "advisory": advisory_no,
            "title": title,
            "date": meta.get("date", ""),
            "url": meta.get("url", ""),
            "source": source,
            "extraction": extraction,
            "flag_count": flag_count,
            "sections": sections,
            # derivable iff a red-flag REGION exists (rf_region) — true even for the glued
            # advisories (the LLM backend extracts them); false ONLY for the 2 FATF advisories
            # (no red-flag list). `extraction`/`flag_count` are a cheap triage HINT (_rf_triage),
            # not the derivability authority — an advisory goes live via a gate-passing
            # derived/<id>.json, and build.py ignores the manifest count for a live advisory.
            "derivable": region is not None,
        })
    return records


def write_corpus_status(source_dir: Path = CORPUS_DIR) -> int:
    """Emit <source_dir>/corpus-status.json — the committed manifest the corpus build reads."""
    records = corpus_status_records(source_dir)
    status_path = source_dir / "corpus-status.json"
    summary = {"clean": 0, "low": 0, "needs": 0, "total": len(records)}
    for r in records:
        summary[{"clean": "clean", "low": "low", "none": "needs"}[r["extraction"]]] += 1
    # the per-source derived path the note cites — byte-identical for the default fincen-advisories
    # source (so its committed manifest never drifts), accurate for any other FinCEN source.
    derived_ref = ("data/fincen/derived/*.json" if source_dir == CORPUS_DIR
                   else f"{source_dir.relative_to(ROOT).as_posix()}/derived/*.json")
    manifest = {
        "_generated_by": "scripts/derive_signals.py --corpus-status",
        "_note": ("Deterministic per-advisory manifest for the corpus-explorer build "
                  f"(scripts/build.py corpus reads this + {derived_ref}). `derivable` "
                  "= a red-flag region exists (rf_region; false only for the 2 FATF advisories); "
                  "`extraction`/`flag_count` are a cheap rf_region-bounded triage HINT (_rf_triage), "
                  "NOT the derivability authority — an advisory goes live via a gate-passing "
                  "derived/<id>.json (the LLM extracts; check_record grounds), and build.py ignores "
                  "the manifest count for a live advisory. Authoring artifact, NOT a ship config. "
                  "Regenerate after the corpus md set changes."),
        "summary": summary,
        "advisories": records,
    }
    status_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {status_path.relative_to(ROOT)} — {len(records)} documents "
          f"({summary['clean']} clean · {summary['low']} low · {summary['needs']} needs)")
    return 0


def corpus_report(source_dir: Path = CORPUS_DIR) -> int:
    """Cheap rf_region triage across a whole committed FinCEN source + report per document.

    Deterministic + offline. For each document: DERIVABLE (a red-flag region exists) with a coarse
    block-flag count classified CLEAN (≥ _MIN_CLEAN_FLAGS) / LOW (fewer — e.g. a glued advisory the
    counter sizes as one block) / or NON-DERIVABLE (no red-flag region — the 2 FATF advisories).
    A HINT, not the derivation authority (the LLM extracts; check_record grounds). Exit 0 always.
    `source_dir` defaults to fincen-advisories; pass any FinCEN-publication source (data/fincen-alerts/).
    """
    mds = sorted(source_dir.glob("*.md"))
    if not mds:
        sys.exit(f"no corpus md under {source_dir.relative_to(ROOT)} — acquire/convert first")
    clean = low = attn = 0
    print(f"corpus: {len(mds)} documents under {source_dir.relative_to(ROOT)}\n")
    for p in mds:
        md = p.read_text(encoding="utf-8")
        extraction, flag_count, _ = _rf_triage(md, rf_region(md))
        if extraction == "none":
            print(f"  {p.stem:14}  NON-DERIVABLE     no enumerated red-flag list")
            attn += 1
        elif extraction == "low":
            print(f"  {p.stem:14}  LOW   {flag_count:>3} block-flag(s) — review "
                  f"(few blocks; e.g. a glued list the counter sizes as one)")
            low += 1
        else:
            print(f"  {p.stem:14}  CLEAN {flag_count:>3} block-flag(s)")
            clean += 1
    print(f"\n{clean} clean · {low} low · {attn} non-derivable  / {len(mds)} "
          f"(cheap rf_region triage — a hint; the LLM extracts + the gate grounds)")
    return 0


def _source_dir_arg(argv) -> Path:
    """Resolve the optional source-dir positional for --corpus/--corpus-status (default: data/fincen).

    Phase 20 — multi-source: `--corpus-status data/fincen-alerts` regenerates that source's manifest
    with the same triage. A path is taken relative to ROOT (or absolute); it must be an existing dir.
    """
    if len(argv) >= 2 and not argv[1].startswith("-"):
        d = Path(argv[1])
        if not d.is_absolute():
            d = ROOT / d
        if not d.is_dir():
            sys.exit(f"source dir not found: {argv[1]} (expected a dir with <id>.md + index.json)")
        return d
    return CORPUS_DIR


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    cmd = argv[0]
    if cmd == "--selftest":
        return selftest()
    if cmd == "--corpus":
        return corpus_report(_source_dir_arg(argv))
    if cmd == "--corpus-status":
        return write_corpus_status(_source_dir_arg(argv))
    if cmd == "--check-derived":
        if len(argv) < 2:
            sys.exit("usage: --check-derived <record.json>")
        return load_and_check_derived(argv[1])
    sys.exit(f"unknown option '{cmd}'. See --help.")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
