#!/usr/bin/env python3
"""OSINT evidence-gathering tools + the agent loop (Phase 65 — companion, dev/authoring-time ONLY).

The investigator GATHER beat. On a selected SYNTHETIC case the agent loop calls deterministic TOOLS over a
COMMITTED SYNTHETIC OSINT corpus (data/osint/corpus.json — fictional registry / adverse-media / sanctions),
and EVERY proposed finding is GROUNDED-OR-STRIPPED by the SHARED news_ground gate: the finding's quote must
be a real substring of the CITED record's own text, and any entity / link it puts in the network must itself
ground in that record (or be the case subject). Grounded tool-evidence extends the case grounding chain and
feeds a network view.

THE HONESTY SEAM (load-bearing): the gate proves CONSISTENCY — the quote is a real substring of a synthetic
record — NOT CORRECTNESS (that the synthesis is a right inference, or that the entity is really sanctioned).
The corpus is FICTIONAL; the chained discovery (registry -> linked entity -> sanctions hit) is AUTHORED into
the synthetic corpus, not discovered. Surfaced honestly: a beat-local synthetic-provenance string, the
grounded-quote / illustrative-synthesis split, the always-on badge, and ZERO catch-rate/precision/lift number.

DOCTRINE: stdlib + news_ground ONLY (news_ground is the shared gate build.py imports BY DESIGN). This module
NEVER imports aml_substrate / aml_casework / news_store / serve_chain / serve_workbench. build.py NEVER imports
this. Nothing is persisted; the corpus is read-only; gather() is stateless across calls. The browser sends a
backend NAME only — creds/endpoints live server-side (non-negotiable §4.5); transport errors are sanitized to
a class name (no host/url ever reaches a stage).

Usage:
    python3 scripts/osint_tools.py --selftest     # offline assertions (no model, no socket), exit
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

_HERE = Path(__file__).resolve().parent
ROOT = _HERE.parent
sys.path.insert(0, str(_HERE))
from news_ground import news_normalize, locate_span  # noqa: E402  (the SHARED gate; the one allowed coupling)

BADGE = "Illustrative data & outputs"
CORPUS_PATH = ROOT / "data" / "osint" / "corpus.json"
KINDS = ("sanctions", "adverse_media", "registry")
TOOL_NAMES = ("screen_sanctions", "screen_adverse_media", "lookup_registry")
_KIND_OF_TOOL = {"screen_sanctions": "sanctions", "screen_adverse_media": "adverse_media",
                 "lookup_registry": "registry"}
_LABEL_OF_KIND = {"sanctions": "sanctions screen", "adverse_media": "adverse media",
                  "registry": "registry link"}

# the news red-flag floor, applied to the NORMALIZED quote so punctuation/whitespace/1-token trivial matches
# cannot ground (a single "the" normalizes to 3 chars < 12 and DROPS).
MIN_QUOTE_CHARS = 12
MAX_QUOTE_CHARS = 400
MAX_ITERS = 4

# the same honesty sweep the rendered UI is held to (tests/workbench.test.mjs): a synthetic record may not
# carry a performance %, an "Nx" lift, or detection-metric vocabulary — enforced at corpus validation so a
# legitimate-looking synthetic record can never trip the UI honesty test or smuggle a metric claim.
_BANNED = re.compile(r"\d+(?:\.\d+)?\s*%|\b\d+(?:\.\d+)?x\b|\b(?:lift|precision|recall|catch[\s-]?rate|f1|auroc)\b",
                     re.IGNORECASE)

SYNTHETIC_NOTE = ("Gathered over a COMMITTED SYNTHETIC OSINT corpus — fictional sanctions / registry / "
                  "adverse-media records, NOT a live web search or a real OFAC list. The gate proves each "
                  "quote is a real substring of a synthetic record (consistency), never that the finding is "
                  "true; the chained path is authored into the synthetic corpus, not discovered.")


class GatherError(ValueError):
    """A NAMED, browser-safe gather failure — emitted verbatim in-stream, never a raw transport message
    (which can carry a host/url and break the §4.5 creds boundary)."""


# ---- corpus load + validate (companion-only; NEVER a build-boundary validator — data/osint is no ship input)
def load_corpus(path: Path = CORPUS_PATH) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_osint_corpus(corpus: dict) -> list:
    """Fail-loud structural validation (returns a list of error strings; empty == clean). Enforced:
      - a head-of-file `note` disclaimer is present + non-empty (a synthetic corpus never ships undisclosed);
      - only closed KINDS; each record has a non-empty str id / entity / text;
      - record ids are GLOBALLY unique across all kinds (so a finding's record_id binds to one record);
      - no record text/headline/program/officer string carries a banned metric token (the honesty sweep);
      - registry linked_entities are non-empty strings (each resolves to a graph node)."""
    errors = []
    if not str(corpus.get("note") or "").strip():
        errors.append("corpus missing the head-of-file 'note' synthetic disclaimer (book.json pattern)")
    seen_ids = {}
    for kind in corpus:
        if kind in ("as_of", "badge", "note"):
            continue
        if kind not in KINDS:
            errors.append(f"unknown corpus kind '{kind}' (closed vocab: {KINDS})"); continue
        section = corpus.get(kind) or {}
        if not isinstance(section, dict):
            errors.append(f"corpus['{kind}'] must be an object keyed by entity name"); continue
        for name, recs in section.items():
            if not isinstance(recs, list):
                errors.append(f"{kind}['{name}'] must be a list of records"); continue
            for rec in recs:
                rid = str((rec or {}).get("id") or "").strip()
                ent = str((rec or {}).get("entity") or "").strip()
                txt = str((rec or {}).get("text") or "").strip()
                if not rid:
                    errors.append(f"{kind}['{name}']: a record is missing 'id'"); continue
                if rid in seen_ids:
                    errors.append(f"duplicate record id '{rid}' ({seen_ids[rid]} and {kind}['{name}'])")
                seen_ids[rid] = f"{kind}['{name}']"
                if not ent:
                    errors.append(f"record '{rid}' missing 'entity'")
                if not txt:
                    errors.append(f"record '{rid}' missing/empty 'text'")
                # the honesty sweep over EVERY human-authored field the UI can render (a finding's entity
                # and a registry record's linked_entities reach the graph/finding card, so they count too —
                # news_normalize strips '%', so a percent-bearing name would otherwise ground silently)
                for field in ("text", "headline", "program", "entity", "outlet", "jurisdiction"):
                    v = rec.get(field)
                    if v and _BANNED.search(str(v)):
                        errors.append(f"record '{rid}'.{field} contains a banned metric token "
                                      f"(%/Nx/lift/precision/recall/catch-rate/f1/auroc): {v!r}")
                for off in (rec.get("officers") or []):
                    if _BANNED.search(str(off)):
                        errors.append(f"record '{rid}' officer {off!r} contains a banned metric token")
                if kind == "registry":
                    for le in (rec.get("linked_entities") or []):
                        if not str(le).strip():
                            errors.append(f"record '{rid}' has an empty linked_entity")
                        elif _BANNED.search(str(le)):
                            errors.append(f"record '{rid}' linked_entity {le!r} contains a banned metric token")
    return errors


def build_index(corpus: dict) -> dict:
    """normname -> kind -> [records]. Exact-normalized-name lookup (documented: a query phrased with extra
    words normalizes to a different key and honestly returns [] — a true negative, not a fuzzy near-miss)."""
    idx: dict = {}
    for kind in KINDS:
        for name, recs in (corpus.get(kind) or {}).items():
            idx.setdefault(news_normalize(name), {}).setdefault(kind, []).extend(recs or [])
    return idx


# ---- the deterministic tools (offline; no model, no network) -------------------------------------
def run_tool(index: dict, tool: str, query: str) -> list:
    """Return the records for KIND(tool) under the EXACT normalized query (a COPY list). [] for an unknown
    tool, an empty query, or no hit — never raises (the loop treats [] as 'nothing here')."""
    kind = _KIND_OF_TOOL.get(tool)
    q = news_normalize(query or "")
    if not kind or not q:
        return []
    return list(index.get(q, {}).get(kind, []))


# ---- the grounding gate over ONE proposed finding (the load-bearing honesty seam) ----------------
def _norm_len(s: str) -> int:
    return len(news_normalize(s))


def _span_ok(located) -> bool:
    """A located span is acceptable iff it is single-line, single-sentence (no newline, no '. ' bridge —
    a GATHER tightening over the news wrap-tolerance, so a quote can't stitch two unrelated clauses), and
    carries real substance (>= MIN_QUOTE_CHARS normalized, <= MAX_QUOTE_CHARS raw)."""
    if not located:
        return False
    # reject a span bridging a sentence terminator + ANY whitespace. locate_span collapses the full
    # [ \t\r\n]+ class, so the guard must match that class — not just '\n' and '. ' (else a '.'+TAB/CR
    # boundary slips two unrelated clauses through as one "single-sentence" quote).
    if "\n" in located or re.search(r"[.!?][ \t\r\n]", located):
        return False
    return MIN_QUOTE_CHARS <= _norm_len(located) <= MAX_QUOTE_CHARS and len(located) <= MAX_QUOTE_CHARS


def _record_known_names(record: dict) -> list:
    """The entity names a record DECLARES — its own entity, its officers, and (registry) its linked
    entities. A network endpoint must match one of these (or the subject) EXACTLY under normalize."""
    names = [record.get("entity")]
    names.extend(record.get("officers") or [])
    names.extend(record.get("linked_entities") or [])
    return [str(n) for n in names if str(n or "").strip()]


def _name_grounded(name: str, record: dict, subject: str) -> bool:
    """A network endpoint (entity / link) is admissible iff it is the case subject OR it matches a name the
    cited record DECLARES (entity / officer / linked_entity), EXACTLY under normalize — NOT an arbitrary
    substring of the record text. A bare fragment ('FZE') or a 1-char token is a substring artifact, not a
    grounded entity, and must never ride a grounded quote into the graph (the module doctrine). Mirrors the
    news relationship gate, where from/to must be KNOWN entity names (exact), never free substrings."""
    nn = news_normalize((name or "").strip())
    if not nn:
        return False
    if nn == news_normalize(subject):
        return True
    return any(nn == news_normalize(k) for k in _record_known_names(record))


def gate_finding(finding: dict, returned_records: list, subject: str, kind: str) -> tuple:
    """Dispose ONE proposed finding against the records the IMMEDIATELY-PRECEDING tool call returned.
    Returns (kept | None, drop_reason | None). KEEP requires, as a conjunction:
      (1) record_id resolves to a record IN returned_records (atomic binding to this tool call);
      (2) located = locate_span(quote, that record's text) passes _span_ok (real, single-sentence substring);
      (3) the quote is REQUOTED to `located` (a raw substring of the record by construction — Phase-44);
      (4) a non-empty synthesis distinct (normalize) from the quote;
      (5) the entity and any link endpoint are subject-or-grounded in that record (no ungrounded graph node).
    The gate verifies CONSISTENCY, never CORRECTNESS of the synthesis."""
    rid = str((finding or {}).get("record_id") or "").strip()
    record = next((r for r in returned_records if str(r.get("id") or "") == rid), None)
    if record is None:
        return None, f"record_id {rid!r} was not in the records this tool returned"
    quote = str(finding.get("quote") or "")
    located = locate_span(quote, record.get("text") or "")
    if not _span_ok(located):
        return None, "quote did not ground as a real single-sentence substring of the cited record"
    syn = str(finding.get("finding") or "").strip()
    if not syn:
        return None, "missing synthesis"
    if news_normalize(syn) == news_normalize(located):
        return None, "synthesis is not distinct from the grounded quote"
    entity = (str(finding.get("entity") or "").strip() or record.get("entity") or subject)
    if not _name_grounded(entity, record, subject):           # entity is REQUIRED — a bad one rejects the finding
        return None, f"entity {entity!r} is neither the subject nor a name the cited record declares"
    link = str(finding.get("link_to") or "").strip()
    if link and not _name_grounded(link, record, subject):    # link is OPTIONAL — a bad one is DROPPED, not a
        link = ""                                             # finding-killer (the finding stands on its grounded
                                                              # entity+quote; no ungrounded node enters the graph)
    return ({"source_kind": kind, "record_id": rid, "entity": entity, "quote": located,
             "synthesis": syn, "link": link or None}, None)


def build_graph(kept: list, subject: str) -> dict:
    """The network view from GROUNDED findings only. Nodes = the subject + every kept finding's (grounded)
    entity + link endpoint; edges connect the subject to each named external entity (and entity->link for a
    registry chain), labelled by source kind, evidence = the grounded quote. Deduped by (from,to,label)."""
    entities = {subject: True}
    rels, seen = [], set()
    for f in kept:
        ent, link, ev = f["entity"], f.get("link"), f["quote"]
        label = _LABEL_OF_KIND.get(f["source_kind"], f["source_kind"])
        if ent and news_normalize(ent) != news_normalize(subject):
            entities[ent] = True
            key = (subject, ent, label)
            if key not in seen:
                seen.add(key); rels.append({"from": subject, "to": ent, "label": label, "evidence": ev})
        if link and news_normalize(link) not in (news_normalize(subject), news_normalize(ent)):
            entities[link] = True
            key = (ent or subject, link, label)
            if key not in seen:
                seen.add(key); rels.append({"from": ent or subject, "to": link, "label": label, "evidence": ev})
    return {"entities": [{"name": n} for n in entities], "relationships": rels, "mains": [subject]}


# ---- planners: the model's two decisions, unified so the loop drives stub + live identically ------
class StubPlanner:
    """The deterministic offline planner (NO model) — makes --selftest reproducible AND exercises every
    path: a grounded KEEP, a deliberately-ungrounded DROP, the registry->linked->sanctions CHAIN, and the
    false-positive-trap honest-empty result. Pure; the loop drives it exactly like the live planner."""

    def __init__(self, case_view: dict, index: dict):
        self.subject = case_view.get("subject_name") or ""
        self.index = index
        self._discovered = []   # linked entities surfaced by a registry call (drives the chain)
        self._planted = False   # the one deliberately-ungrounded finding (exercises the gate DROP once)

    def action(self, step: int, history: list) -> dict:
        if step == 0:
            return {"action": "call_tool", "tool": "lookup_registry", "query": self.subject}
        if step == 1 and self._discovered:
            return {"action": "call_tool", "tool": "screen_sanctions", "query": self._discovered[0]}
        if step in (1, 2):
            return {"action": "call_tool", "tool": "screen_adverse_media", "query": self.subject}
        return {"action": "finish"}

    def findings(self, records: list, tool: str) -> list:
        out = []
        for rec in records:
            text = rec.get("text") or ""
            quote = _content_span(text)          # a real, single-sentence substring of THIS record
            if tool == "lookup_registry":
                for le in (rec.get("linked_entities") or []):
                    if le not in self._discovered:
                        self._discovered.append(le)
                ent = (rec.get("linked_entities") or [rec.get("entity")])[0]
                syn = "Registry ties the subject to an affiliated entity (illustrative reading)."
            elif tool == "screen_sanctions":
                ent = rec.get("entity"); syn = "An affiliated entity matches a sanctions listing (illustrative reading)."
            else:
                ent = rec.get("entity"); syn = "Adverse media names the subject (illustrative reading)."
            out.append({"record_id": rec.get("id"), "quote": quote, "finding": syn,
                        "entity": ent, "link_to": self.subject if tool == "lookup_registry" else ""})
        if records and not self._planted:        # one ungrounded finding -> the gate DROPs it (the honest moment)
            self._planted = True
            out.append({"record_id": records[0].get("id"),
                        "quote": "this exact phrase is not present in any synthetic record",
                        "finding": "An unsupported claim the gate must reject.", "entity": self.subject})
        return out


def _content_span(text: str) -> str:
    """Pick a deterministic, gate-passing span of a record's text: the clause after the first ': ' up to
    the final '.' (the records are single-sentence after the colon, so this never spans '. ' or a newline)."""
    body = text.split(": ", 1)[1] if ": " in text else text
    return body.rstrip().rstrip(".")


class LivePlanner:
    """The live planner — drives a real chat model through the SAME two decisions, strict-JSON only, with
    salvage + a per-call hard timeout. Fail-CLOSED: a malformed/timed-out action wastes one iteration with a
    named note; malformed findings yield nothing that turn (never invents)."""

    def __init__(self, case_view: dict, call_model):
        self.subject = case_view.get("subject_name") or ""
        self.kind = case_view.get("subject_kind") or "subject"
        self.counterparties = case_view.get("counterparties") or []
        self.call_model = call_model

    def action(self, step: int, history: list) -> dict:
        discovered = []
        for h in (history or []):
            for nm in (h.get("found") or []):
                if nm not in discovered:
                    discovered.append(nm)
        sys_p = ("You are an AML investigator gathering external evidence on a subject using a FIXED set of "
                 "tools over a synthetic corpus. Respond with STRICT JSON only, no prose. To call a tool: "
                 '{"action":"call_tool","tool":"<screen_sanctions|screen_adverse_media|lookup_registry>",'
                 '"query":"<an entity name>"}. To stop: {"action":"finish"}. Start with lookup_registry on '
                 "the subject. When a lookup reveals an affiliated entity (see discovered_entities), CHAIN: "
                 "screen THAT affiliated entity for sanctions and adverse media before finishing. Query named "
                 "entities, not account/counterparty reference codes.")
        usr = json.dumps({"subject": self.subject, "subject_kind": self.kind,
                          "counterparties": self.counterparties[:12], "discovered_entities": discovered,
                          "history": history})
        txt = self.call_model([{"role": "system", "content": sys_p}, {"role": "user", "content": usr}])
        obj = parse_llm_json(txt) or {}
        return obj if isinstance(obj, dict) else {}

    def findings(self, records: list, tool: str) -> list:
        if not records:
            return []
        sys_p = ("Propose findings ONLY as JSON {\"findings\":[{\"record_id\":\"..\",\"quote\":\"<copy a "
                 "verbatim substring of THAT record's text>\",\"finding\":\"<one-sentence reading, distinct "
                 "from the quote>\",\"entity\":\"<a named entity the record DECLARES — copy it EXACTLY (its "
                 "entity, an officer, or a linked entity); not a fragment>\",\"link_to\":\"<the subject or "
                 "another declared entity name, optional>\"}]}. The quote MUST be copied verbatim from the "
                 "cited record's text and entity/link_to must be full declared names. Do not invent. If "
                 "nothing is relevant, return {\"findings\":[]}.")
        usr = json.dumps({"subject": self.subject, "records": [{"id": r.get("id"), "text": r.get("text")}
                                                               for r in records]})
        txt = self.call_model([{"role": "system", "content": sys_p}, {"role": "user", "content": usr}])
        obj = parse_llm_json(txt) or {}
        fs = obj.get("findings") if isinstance(obj, dict) else None
        return fs if isinstance(fs, list) else []


# ---- the agent loop (capped, no-progress-guarded, fail-closed; stateless across calls) ------------
def gather(case_view: dict, *, on_stage=lambda *a, **k: None, corpus: dict | None = None,
           index: dict | None = None, planner=None, max_iters: int = MAX_ITERS,
           backend_note: dict | None = None) -> dict:
    """Drive ONE case through the GATHER loop, emitting NDJSON stages via on_stage. Returns the result
    {subject, grounded[], dropped[], graph, tools_called[], counts, backend, synthetic_note, badge}.
    Pure + stateless: read-only over the committed corpus, all state local, nothing persisted."""
    corpus = corpus if corpus is not None else load_corpus()
    index = index if index is not None else build_index(corpus)
    subject = case_view.get("subject_name") or ""
    planner = planner or StubPlanner(case_view, index)
    kept, dropped, tools_called, history = [], [], [], []
    seen_calls, note = set(), None
    on_stage("plan", subject=subject, tools=list(TOOL_NAMES))
    for step in range(max_iters):
        try:
            action = planner.action(step, history)
        except GatherError as ex:
            note = str(ex); break
        act = (action or {}).get("action")
        if act != "call_tool":                                   # finish / unknown -> terminate honestly
            break
        tool = str(action.get("tool") or "")
        query = str(action.get("query") or "")
        key = (tool, news_normalize(query))
        if key in seen_calls:                                    # no-progress guard -> stop spinning
            note = "stopped: the planner repeated a tool call (no new evidence)"; break
        seen_calls.add(key)
        if tool not in TOOL_NAMES or not query.strip():          # named skip, counts toward the cap
            dropped.append({"reason": f"skipped malformed tool call (tool={tool!r}, query={query!r})"})
            history.append({"tool": tool, "query": query, "n_records": 0})
            on_stage("tool", tool=tool, query=query, n_records=0, skipped=True)
            continue
        records = run_tool(index, tool, query)
        kind = _KIND_OF_TOOL[tool]
        tools_called.append({"tool": tool, "query": query, "n_records": len(records)})
        hist_entry = {"tool": tool, "query": query, "n_records": len(records), "found": []}
        history.append(hist_entry)
        on_stage("tool", tool=tool, query=query, n_records=len(records))
        try:
            proposed = planner.findings(records, tool)
        except GatherError as ex:                                # transport failed mid-loop: keep what grounded
            note = str(ex)
            on_stage("findings", tool=tool, grounded=0, dropped=0, error=note)
            break
        g_step, d_step = [], []
        for f in (proposed or []):
            keptf, reason = gate_finding(f, records, subject, kind)
            if keptf:
                kept.append(keptf); g_step.append(keptf)
            else:
                d = {"source_kind": kind, "record_id": str((f or {}).get("record_id") or ""),
                     "quote": str((f or {}).get("quote") or "")[:160], "reason": reason}
                dropped.append(d); d_step.append(d)
        # surface newly-discovered entities so the planner can CHAIN (screen what registry just revealed) —
        # without this the model can't see which affiliate a lookup exposed and can't make the multi-hop leap
        for kf in g_step:
            for nm in (kf.get("entity"), kf.get("link")):
                if nm and news_normalize(nm) != news_normalize(subject) and nm not in hist_entry["found"]:
                    hist_entry["found"].append(nm)
        on_stage("findings", tool=tool, grounded=len(g_step), dropped=len(d_step),
                 kept=g_step, rejected=d_step)
    graph = build_graph(kept, subject)
    result = {"badge": BADGE, "subject": subject, "synthetic_note": SYNTHETIC_NOTE,
              "backend": backend_note or {"effective": "stub", "requested": None, "note": None},
              "grounded": kept, "dropped": dropped, "graph": graph, "tools_called": tools_called,
              "counts": {"grounded": len(kept), "dropped": len(dropped), "tools": len(tools_called)}}
    if note:
        result["note"] = note
    return result


# ---- the live transport (per-call hard timeout; SANITIZED errors — no host/url ever leaves) -------
def resolve_gather_backend(requested: str | None, env: dict | None = None) -> dict:
    """The gather loop's chat transport resolves to 'openai' iff OPENAI_BASE_URL is set SERVER-SIDE, else
    'stub' with an honest NAME-only note. claude/opencode are not wired for the gather chat loop (the
    casework drafter subprocess is a different path) -> stub+note. NAME + note only; never an endpoint."""
    e = env if env is not None else os.environ
    req = (requested or "").strip().lower() or None
    has_openai = bool(e.get("OPENAI_BASE_URL"))
    if req in (None, "openai") and has_openai:
        return {"requested": req, "effective": "openai", "note": None}
    if req in ("claude", "opencode"):
        return {"requested": req, "effective": "stub",
                "note": f"backend '{req}' is not wired for the gather loop — using the deterministic stub"}
    if req == "openai" and not has_openai:
        return {"requested": req, "effective": "stub",
                "note": "openai unavailable server-side (no OPENAI_BASE_URL) — using the deterministic stub"}
    return {"requested": req, "effective": "stub", "note": None}


def parse_llm_json(text):
    """Salvage strict JSON from a model reply: strip <think>…</think> and code fences, then take the
    outermost {...}. Returns the parsed object or None (the loop fail-closes on None)."""
    if not text:
        return None
    s = re.sub(r"<think>.*?</think>", "", str(text), flags=re.DOTALL | re.IGNORECASE)
    s = re.sub(r"```(?:json)?", "", s)
    i, j = s.find("{"), s.rfind("}")
    if i < 0 or j <= i:
        return None
    try:
        return json.loads(s[i:j + 1])
    except (ValueError, json.JSONDecodeError):
        return None


def call_openai(messages: list, env: dict | None = None, timeout: int = 60) -> str:
    """Non-streaming POST to {OPENAI_BASE_URL}/chat/completions (each agent turn is small — no streaming/
    idle-gap machinery). Raises a SANITIZED GatherError (class name only) so no host/url can reach a stage."""
    e = env if env is not None else os.environ
    base = (e.get("OPENAI_BASE_URL") or "").rstrip("/")
    if not base:
        raise GatherError("no OPENAI_BASE_URL configured server-side")
    body = json.dumps({"model": e.get("OPENAI_MODEL", "local"), "messages": messages,
                       "temperature": 0, "stream": False}).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if e.get("OPENAI_API_KEY"):
        headers["Authorization"] = "Bearer " + e["OPENAI_API_KEY"]
    req = urllib.request.Request(base + "/chat/completions", data=body, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:        # noqa: S310 (localhost model)
            data = json.loads(r.read().decode("utf-8"))
        return data["choices"][0]["message"]["content"] or ""
    except (urllib.error.URLError, OSError, ValueError, KeyError, IndexError) as ex:
        raise GatherError(f"model transport failed ({ex.__class__.__name__})") from None


def make_planner(case_view: dict, backend: dict, env: dict | None = None):
    """A StubPlanner unless the resolved backend is 'openai' (then a LivePlanner over call_openai)."""
    if backend.get("effective") == "openai":
        return LivePlanner(case_view, lambda msgs: call_openai(msgs, env))
    return StubPlanner(case_view, build_index(load_corpus()))


# ---- selftest (offline: no model, no socket) -----------------------------------------------------
def _selftest() -> int:
    failures = []
    corpus = load_corpus()

    # (1) the committed corpus validates clean; a broken corpus is REJECTED (fail-loud)
    errs = validate_osint_corpus(corpus)
    if errs:
        failures.append(f"committed corpus should validate clean, got: {errs}")
    broken = {"note": "", "sanctions": {"X": [{"id": "d1", "entity": "X", "text": ""}]},
              "registry": {"Y": [{"id": "d1", "entity": "Y", "text": "ok: 50% owned by Z"}],
                           "Acme": [{"id": "d3", "entity": "Acme 50% Holdings",
                                     "text": "Acme 50 Holdings is a firm",          # banned token is in entity, NOT text
                                     "linked_entities": ["Beta 3x Capital"]}]}}
    berr = validate_osint_corpus(broken)
    for need in ("note", "duplicate record id", "missing/empty 'text'", "banned metric token",
                 ".entity contains a banned", "linked_entity 'Beta 3x Capital' contains a banned"):
        if not any(need in e for e in berr):
            failures.append(f"broken-corpus validation should flag {need!r}, got {berr}")

    index = build_index(corpus)
    # (2) tools are deterministic + exact-normname; an unknown tool / phrasing-miss honestly returns []
    s1 = run_tool(index, "lookup_registry", "Zane Zhao")
    s2 = run_tool(index, "lookup_registry", "zane  zhao!")          # normalizes to the same key
    if not s1 or s1 != s2:
        failures.append("run_tool must be deterministic + normalize-keyed for the subject")
    if run_tool(index, "screen_sanctions", "Zane Zhao") != []:
        failures.append("the subject himself is not sanctioned (the hit is on the linked entity)")
    if run_tool(index, "screen_sanctions", "Crescent Dunes Trading FZE") == []:
        failures.append("the linked entity SHOULD have a sanctions record (the chain)")
    if run_tool(index, "bogus_tool", "Zane Zhao") != [] or run_tool(index, "lookup_registry", "") != []:
        failures.append("unknown tool / empty query must return [] (no crash)")
    # fp_trap true negatives: sanctions + adverse on the canonical normname are [] (not a phrasing miss)
    if run_tool(index, "screen_sanctions", "Liam Jain") != [] or run_tool(index, "screen_adverse_media", "Liam Jain") != []:
        failures.append("the fp_trap subject must be a TRUE negative on sanctions + adverse media")

    # (3) the gate predicate: grounded KEEP, and every bypass DROPS
    reg = run_tool(index, "lookup_registry", "Zane Zhao")[0]
    good_quote = _content_span(reg["text"])
    keptf, reason = gate_finding({"record_id": reg["id"], "quote": good_quote,
                                  "finding": "Registry ties the subject to an affiliate (illustrative).",
                                  "entity": "Crescent Dunes Trading FZE", "link_to": "Zane Zhao"},
                                 [reg], "Zane Zhao", "registry")
    if not keptf or keptf["quote"] not in reg["text"]:
        failures.append(f"a grounded finding should KEEP with a raw-substring quote, got {reason}")
    bypasses = [
        ({"record_id": reg["id"], "quote": "the", "finding": "x", "entity": "Zane Zhao"}, "1-token quote"),
        ({"record_id": reg["id"], "quote": ",", "finding": "x", "entity": "Zane Zhao"}, "punctuation quote"),
        ({"record_id": reg["id"], "quote": "phrase absent from the record", "finding": "x", "entity": "Zane Zhao"}, "ungrounded quote"),
        ({"record_id": "nope", "quote": good_quote, "finding": "x", "entity": "Zane Zhao"}, "record_id not returned"),
        ({"record_id": reg["id"], "quote": good_quote, "finding": good_quote, "entity": "Zane Zhao"}, "synthesis == quote"),
        ({"record_id": reg["id"], "quote": good_quote, "finding": "ok", "entity": "Globex Holdings"}, "wholly-foreign entity"),
        ({"record_id": reg["id"], "quote": good_quote, "finding": "ok", "entity": "FZE"}, "fragment-of-a-real-name entity"),
        ({"record_id": reg["id"], "quote": good_quote, "finding": "ok", "entity": "a"}, "1-char entity (substring artifact)"),
    ]
    for f, label in bypasses:
        k, _r = gate_finding(f, [reg], "Zane Zhao", "registry")
        if k is not None:
            failures.append(f"gate bypass NOT closed: {label}")
    # an ungrounded / fragment LINK is DROPPED to None (the finding still stands on its grounded entity +
    # quote) — an optional supplementary field, not a finding-killer (the news_ground keep-entity/strip-attr
    # pattern); the live model commonly proposes a list/phrase link, which must not lose the real finding
    for bad_link in ("Phantom Ltd", "Crescent", "OFAC Specially Designated Nationals list"):
        k, _r = gate_finding({"record_id": reg["id"], "quote": good_quote, "finding": "ok",
                              "entity": "Crescent Dunes Trading FZE", "link_to": bad_link}, [reg], "Zane Zhao", "registry")
        if k is None or k.get("link") is not None:
            failures.append(f"a bad link_to ({bad_link!r}) must DROP to None with the finding KEPT, got {k}")
    # the sentence-bridge guard: a quote stitching two clauses across '. ' DROPs
    two = {"id": "tb1", "entity": "Z", "text": "Z is a registered company. No sanctions were found on file."}
    kb, _ = gate_finding({"record_id": "tb1", "quote": "registered company. No sanctions",
                          "finding": "stitched", "entity": "Z"}, [two], "Z", "registry")
    if kb is not None:
        failures.append("the sentence-bridge guard must DROP a quote spanning '. '")
    # the guard matches locate_span's FULL whitespace class — a '.'+TAB/CR bridge DROPs too (latent fix)
    if _span_ok("registered company.\tNo sanctions were found") or _span_ok("registered company.\rNo sanctions on file"):
        failures.append("_span_ok must reject a '.'+TAB/CR bridge (locate_span collapses the full ws class)")
    if not _span_ok("Zane Zhao is recorded as the sole director of Crescent Dunes Trading FZE"):
        failures.append("_span_ok must still PASS a clean single-sentence span")

    # (4) the STUB loop end-to-end over the mule: grounded KEEP + the planted DROP + the CHAIN + terminates
    stages = []
    cv = {"subject_name": "Zane Zhao", "subject_kind": "person", "counterparties": ["CP-1"]}
    res = gather(cv, on_stage=lambda s, **k: stages.append((s, k)), corpus=corpus, index=index)
    if res["counts"]["grounded"] < 2:
        failures.append(f"the stub loop should KEEP multiple grounded findings, got {res['counts']}")
    if res["counts"]["dropped"] < 1 or not any("not present" in d.get("quote", "") or "not in" in d.get("reason", "")
                                               for d in res["dropped"]):
        failures.append(f"the stub loop should DROP the planted ungrounded finding, got {res['dropped']}")
    if not any(f["source_kind"] == "sanctions" for f in res["grounded"]):
        failures.append("the CHAIN should reach a sanctions finding on the registry-discovered entity")
    for f in res["grounded"]:                                  # every kept quote is a RAW substring (Phase-44)
        recs = run_tool(index, {"sanctions": "screen_sanctions", "adverse_media": "screen_adverse_media",
                                "registry": "lookup_registry"}[f["source_kind"]],
                        f["entity"] if f["source_kind"] == "sanctions" else "Zane Zhao")
        if not any(f["quote"] in (r.get("text") or "") for r in recs):
            failures.append(f"a kept quote is not a raw substring of its source record: {f['quote']!r}")
    if not res["graph"]["relationships"] or res["graph"]["mains"] != ["Zane Zhao"]:
        failures.append("the graph should carry grounded relationships with the subject as main")
    for rel in res["graph"]["relationships"]:                  # every edge endpoint is subject-or-grounded
        if news_normalize(rel["to"]) == news_normalize("Zane Zhao"):
            failures.append("a graph edge points back at the subject as a target (should be external)")
    seq = [s for s, _ in stages]
    for need in ("plan", "tool", "findings"):
        if need not in seq:
            failures.append(f"gather stage '{need}' missing from {seq}")

    # (5) the fp_trap honest-empty: a clean registry finding, ZERO sanctions/adverse
    fp = gather({"subject_name": "Liam Jain", "subject_kind": "person"}, corpus=corpus, index=index)
    if any(f["source_kind"] in ("sanctions", "adverse_media") for f in fp["grounded"]):
        failures.append("the fp_trap subject must surface NO sanctions/adverse findings (honest negative)")

    # (6) determinism + persists-nothing + statelessness
    before = CORPUS_PATH.read_bytes()
    r2 = gather(cv, corpus=corpus, index=index)
    r3 = gather(cv, corpus=corpus, index=index)
    if json.dumps(r2, sort_keys=True) != json.dumps(r3, sort_keys=True):
        failures.append("two sequential stub gathers must be byte-identical (deterministic + stateless)")
    if CORPUS_PATH.read_bytes() != before:
        failures.append("gather must persist NOTHING — corpus.json changed on disk")

    # (7) the no-progress guard + cap: a planner that always repeats one call terminates fast, not at the cap
    class _Spin:
        def action(self, step, history): return {"action": "call_tool", "tool": "lookup_registry", "query": "Zane Zhao"}
        def findings(self, records, tool): return []
    spin = gather(cv, corpus=corpus, index=index, planner=_Spin())
    if spin["counts"]["tools"] > 1:
        failures.append("the no-progress guard should stop a repeated-call planner after one call")

    # (8) the cap: a planner that always calls a NEW tool/query never exceeds max_iters tool calls
    class _Cap:
        def action(self, step, history): return {"action": "call_tool", "tool": "lookup_registry", "query": f"E{step}"}
        def findings(self, records, tool): return []
    cap = gather(cv, corpus=corpus, index=index, planner=_Cap(), max_iters=3)
    if cap["counts"]["tools"] > 3:
        failures.append(f"the loop must not exceed max_iters tool calls, got {cap['counts']['tools']}")

    # (9) §4.5: a live transport error is SANITIZED (no host/url); resolve is NAME-only
    try:
        call_openai([{"role": "user", "content": "x"}], env={"OPENAI_BASE_URL": "http://127.0.0.1:59999/v1"}, timeout=1)
        failures.append("call_openai to a dead endpoint should raise")
    except GatherError as ex:
        if "127.0.0.1" in str(ex) or "59999" in str(ex):
            failures.append(f"transport error leaked the host/url: {ex}")
    rb = resolve_gather_backend("openai", {"OPENAI_BASE_URL": "http://127.0.0.1:8080/v1", "OPENAI_API_KEY": "sk-SECRET"})
    if rb["effective"] != "openai" or "127.0.0.1" in json.dumps(rb) or "sk-SECRET" in json.dumps(rb):
        failures.append(f"resolve_gather_backend must be NAME-only, got {rb}")
    if resolve_gather_backend("claude", {})["effective"] != "stub":
        failures.append("claude/opencode resolve to stub+note for the gather loop")

    # (10) parse_llm_json salvage
    if parse_llm_json('<think>plan</think> ```json\n{"action":"finish"}\n```') != {"action": "finish"}:
        failures.append("parse_llm_json should salvage fenced/think-wrapped JSON")
    if parse_llm_json("no json here") is not None:
        failures.append("parse_llm_json returns None on non-JSON (the loop fail-closes)")

    if failures:
        for f in failures:
            print(f"FAIL: {f}", file=sys.stderr)  # noqa: T201
        return 1
    print(f"osint_tools --selftest: PASS (corpus validates; {res['counts']['grounded']} grounded / "  # noqa: T201
          f"{res['counts']['dropped']} dropped on the mule chain; {len(res['graph']['relationships'])} grounded "
          f"edges; gate bypasses all closed; fp_trap honest-empty; deterministic + persists-nothing; "
          f"transport sanitized)")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    print("osint_tools: OSINT gather tools + agent loop (companion). Run with --selftest.")  # noqa: T201
