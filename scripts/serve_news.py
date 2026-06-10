#!/usr/bin/env python3
"""Live companion for the M8 adverse-media news stream (Phase 35 — authoring/dev-time ONLY).

This is NOT part of the ship artifact. The shippable `dist/news/index.html` stays a single
self-contained offline file (the scripted fallback, the stakeholder demo). This companion adds the
optional, isolated "live mode" the non-negotiable already sanctions: it serves `news.html` over
http://localhost (so the page is SAME-ORIGIN with the API — no CORS) with `NEWS.live` set, and (T3)
proxies a local llama-cpp server to extract entities + red flags from a submitted article in REAL
TIME. The model PROPOSES; a deterministic gate DISPOSES — every extracted entity/attribute/red-flag
must quote-ground in the submitted source (the shared `news_ground` gate, T2), ungrounded items drop.

Architecture (Phase 35):
  - Served-by-companion: this serves the template WHOLE (with the live branch); `build.py render_news`
    STRIPS the live branch for the offline `dist/news` (zero network code offline).
  - Grounding stays in Python, server-side (shared `news_ground.py`, reused by build.py's gate).
  - Persistence (DuckDB row-append -> parquet export) + the feedback watchlist (book ∪ prior-scanned)
    are Phase 36; T1/T3 screen against the STATIC committed book.

Stdlib + urllib ONLY (zero new pip deps this phase; DuckDB enters Phase 36). Reuses `build.load_news`
for the seed data — build.py never imports the authoring/LLM layer, and neither does this for grounding
(news_ground is stdlib grounding primitives).

Usage:
    python3 scripts/serve_news.py                  # serve on http://localhost:8000, proxy the model at http://127.0.0.1:8080
    python3 scripts/serve_news.py --port 8001 --llm-url http://127.0.0.1:8080/v1/chat/completions
    python3 scripts/serve_news.py --selftest       # assemble the page offline, assert, exit
"""
import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import build  # scripts/ is on sys.path[0] when run as `python3 scripts/serve_news.py`; stdlib-only import
import news_fetch  # Phase 39: URL acquisition (fetch ladder + standardizer + verifier; companion-only)
import news_ground  # the shared grounding gate — drops ungrounded live extractions (live == build by construction)
import news_store  # Phase 36: DuckDB persistence + the escalated-only watchlist (companion-only; build.py never imports it)


def _now() -> str:
    """UTC timestamp stamped on each persisted scan (the watchlist provenance reads from it)."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

DEFAULT_PORT = 8000
DEFAULT_LLM_URL = "http://127.0.0.1:8080/v1/chat/completions"  # the local llama-cpp endpoint (literal IPv4 — llama-cpp binds 127.0.0.1, not IPv6 ::1)
DEFAULT_MODEL = "qwen"  # any model swappable behind llama-cpp's OpenAI-compatible /v1
DEFAULT_DB = "data/news/.live/store.duckdb"  # Phase 36: gitignored runtime store (never on the ship path)

# ---- live extraction: the model PROPOSES, the deterministic gate (news_ground) DISPOSES ----------
# The schema constrains the model's shape; news_ground.ground_record then DROPS anything that doesn't
# quote-ground in the submitted article. Two independent guards, same honesty spine as the build path.
EXTRACT_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "typology": {"type": "string"},
        # Phase 41 calibration r2 — red_flags come FIRST in schema order: the strict-grammar model
        # generates properties in this order, so the measured Phase-40 flag surface is produced with
        # full attention BEFORE the identity enrichment spends any output budget (measured: the
        # enriched one-call prompt with flags last cost ~12.5% kept flags on the regression set).
        "red_flags": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "flag": {"type": "string"},
                    "red_flag": {"type": "string"},
                    "category": {"type": "string"},
                },
                "required": ["flag", "red_flag"],
            },
        },
        "entities": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "type": {"type": "string", "enum": ["person", "org"]},
                    "location": {"type": "string"},
                    "age": {"type": "string"},
                    "profession": {"type": "string"},
                    "context": {"type": "string"},
                    # Phase 41 — resolution-grade identity fields (vocab authority: news_ground)
                    "aliases": {"type": "array", "items": {"type": "string"}},
                    "properties": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "kind": {"type": "string", "enum": list(news_ground.PROPERTY_KINDS)},
                                "value": {"type": "string"},
                            },
                            "required": ["kind", "value"],
                        },
                    },
                },
                "required": ["name", "type"],
            },
        },
        # Phase 41 — structured inter-entity relationships + the main-subject designation
        "relationships": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "from": {"type": "string"},
                    "to": {"type": "string"},
                    "label": {"type": "string", "enum": list(news_ground.RELATION_LABELS)},
                    "evidence": {"type": "string"},
                },
                "required": ["from", "to", "label", "evidence"],
            },
        },
        "main_subjects": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["entities", "red_flags"],
}

SYSTEM_PROMPT = (
    "You are an AML analyst extracting structured intelligence from a single news or enforcement article. "
    "Return ONLY JSON matching the schema — no prose, no markdown, no commentary.\n"
    "- entities: every named person or organisation relevant to financial crime. `name` MUST be copied "
    "VERBATIM from the article (exact characters). `type` is 'person' or 'org'. location/age/profession/"
    "context are optional and, when given, MUST be quoted or directly paraphrased from words present in the "
    "article.\n"
    "- SUBJECTS ONLY (Phase 38 — the highest-leverage control): extract ONLY the subjects of the financial "
    "crime — perpetrators, defendants, designated/sanctioned parties, and the companies, accounts, or "
    "aliases they used. DO NOT extract law-enforcement or government personnel, prosecutors, judges, "
    "investigating agencies or their field offices, officials who announce or comment on the action, "
    "government programs, or prosecuting/court districts. If a person or org appears ONLY because they "
    "announced, investigated, or prosecuted the case, EXCLUDE it.\n"
    "- red_flags (you output these FIRST): extract EVERY DISTINCT suspicious behaviour in the article — be exhaustive. Use the "
    "CHECKLIST below as a coverage net: scan the whole article once per family so nothing is overlooked; a "
    "family yields AS MANY flags as the article has distinct behaviours in it (several distinct behaviours "
    "in one family = several flags). Suspicious behaviour includes INSTITUTIONAL failures — a bank or firm "
    "weakening, ignoring, or misrepresenting its own controls — not only transactions. MERGE RULE (narrow): "
    "only when the article RETELLS the SAME behaviour through repeated anecdotes or examples, extract it "
    "once with the strongest quote; never emit two flags for the same quote or the same behaviour retold.\n"
    "  `flag` MUST be a VERBATIM, CONTIGUOUS quote from the article (an exact substring — do not paraphrase "
    "it, do not stitch across gaps); choose the TIGHTEST span that evidences the behaviour (a clause or "
    "sentence fragment, not a paragraph). `red_flag` is a TERSE, mechanism-named AML translation "
    "(e.g. 'Cash-for-crypto handovers to break the trail', 'Ownership obfuscation: 50%+ held by a blocked "
    "person', 'Commingle illicit cash with legitimate cash-business takings', 'Willful blindness: "
    "monitoring scaled back while high-risk flow grew') — 12-240 characters, DIFFERENT wording from the "
    "verbatim flag. `category` is the checklist family.\n"
    "- CHECKLIST (mechanism families): structuring/threshold-avoidance | rapid movement with no economic "
    "purpose (layering, circular or flow-through transfers) | shell/front companies & nominee or opaque "
    "ownership | professional-gatekeeper misuse (attorneys, trust accounts, corporate service providers) | "
    "bulk-cash placement & couriers | commingling with legitimate revenue | virtual-asset obfuscation "
    "(mixers, chain-hopping, stablecoins, unregistered exchange) | money mules & funnel accounts | "
    "trade-based laundering & invoice fraud | sanctions evasion & designated-party dealings | "
    "export-control/dual-use procurement (transshipment, falsified end-users) | high-risk-jurisdiction & "
    "non-resident flow-through banking | casino, real-estate & luxury-asset laundering | fraud- or "
    "scam-derived victim funds | unregistered/unlicensed financial services | cyber-enabled theft & payment "
    "fraud | concealment & detection-evasion (encrypted comms, fake identities, record destruction, timing) "
    "| institutional control failure (willful blindness, monitoring gaps, paper-only compliance, "
    "profit-over-compliance) | misrepresentation to regulators, counterparties or customers | corruption & "
    "PEP-linked funds\n"
    # Phase 41 — resolution-grade identity enrichment (aliases / properties / relationships / main
    # subjects), AFTER the flag contract: complete the full checklist scan first; the enrichment must
    # NEVER reduce flag coverage. Every value is verbatim-or-dropped downstream.
    "AFTER the red_flags are complete (the identity fields below must NEVER reduce your red_flags "
    "coverage — extract flags with the same exhaustiveness as if they were the only output):\n"
    "- aliases (per entity, optional): OTHER names the ARTICLE ITSELF uses for the same party — a.k.a. "
    "names, shortened forms, nicknames, online handles, transliterations, former or trading names. Each "
    "alias MUST be copied VERBATIM from the article. Do NOT invent variants; most entities have none.\n"
    "- properties (per entity, optional): identifying attributes, ONLY when literally printed in the "
    "article. `kind` is one of " + " | ".join(news_ground.PROPERTY_KINDS) + " (id_registration covers "
    "passport, company/tax registration, case and licence numbers; wallet is a cryptocurrency address; "
    "domain is a website). `value` MUST be copied VERBATIM — exact characters, keeping punctuation, "
    "spacing and line formatting as printed. MOST entities have ZERO properties — that is the normal "
    "case. NEVER guess, derive, or reformat a value: an age like '45-year-old' is NOT a dob; record a "
    "dob ONLY if a birth date is printed.\n"
    "- relationships (optional): how the extracted subjects connect, ONLY where the article states the "
    "connection. `from` and `to` MUST be `name` values from your entities list. `label` is one of "
    + " | ".join(news_ground.RELATION_LABELS) + ". Direction: 'A owner-or-controller-of B' means A owns "
    "or controls B. `evidence` MUST be a VERBATIM, CONTIGUOUS quote from the article stating the "
    "connection. Only STATED connections — no inference chains, not every possible pair. Examples of "
    "label use: a spouse who laundered the scheme's proceeds → family-or-associate-of + co-conspirator; "
    "a Brooklyn company used to source and ship the goods → 'scheme leader owner-or-controller-of "
    "company' (if ownership is stated) or 'company front-for scheme leader'.\n"
    "- main_subjects (optional): the `name`(s) of the entity or entities the article is PRINCIPALLY "
    "about — the target(s) of the enforcement action or investigation. May be one, several (a "
    "multi-defendant case), or empty if genuinely unclear — never force a single pick.\n"
    "A downstream grounding check DISCARDS anything not literally present in the article, so quote exactly."
)
USER_PROMPT_TMPL = ("ARTICLE:\n\n{article}\n\nExtract the entities (with any aliases and printed "
                    "identifying properties), their relationships, the main subject(s), and the red "
                    "flags as JSON.")


def call_llm(text: str, *, llm_url: str, model: str, timeout: int = 180) -> str:
    """Call a local llama-cpp OpenAI-compatible /v1/chat/completions endpoint; return the assistant text.

    This is the ONLY part that needs a running model — kept separate from parse/assemble/ground so the
    pipeline is testable with NO model (the test stubs this or skips it). Requests JSON-schema-constrained
    output and disables Qwen thinking; <think> is also stripped defensively downstream.
    """
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT_TMPL.format(article=text)},
        ],
        "temperature": 0,
        "max_tokens": 4096,
        "response_format": {
            "type": "json_schema",
            "json_schema": {"name": "extraction", "strict": True, "schema": EXTRACT_SCHEMA},
        },
        "chat_template_kwargs": {"enable_thinking": False},  # llama-cpp: skip Qwen reasoning for extraction
    }
    req = urllib.request.Request(
        llm_url, data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"}, method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        resp = json.loads(r.read().decode("utf-8"))
    return resp["choices"][0]["message"]["content"]


def parse_llm_json(content: str) -> dict:
    """Robustly extract the JSON object from a model response: strip a <think> block, code fences, and any
    leading/trailing prose around the outermost {...}."""
    s = re.sub(r"<think>.*?</think>", "", content, flags=re.S).strip()
    m = re.search(r"```(?:json)?\s*(.*?)```", s, flags=re.S)
    if m:
        s = m.group(1).strip()
    if not s.startswith("{"):
        i, j = s.find("{"), s.rfind("}")
        if i != -1 and j != -1 and j > i:
            s = s[i:j + 1]
    return json.loads(s)


def _slugify(t: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", (t or "").lower()).strip("-")[:48]


def build_record(llm_json: dict, text: str, meta: dict = None):
    """Assemble a derived news record (matching the inlined article shape) from the model's JSON, then
    GROUND it (drop ungrounded entities/attributes/red-flags) and assign contiguous E#/R# ids to the
    survivors. Returns (record, dropped). Pure — no model, no network — so it's unit-testable."""
    meta = meta or {}
    body = news_ground.article_body(text)
    title = (llm_json.get("title") or meta.get("title") or "Untitled live article").strip()
    pre = {
        "id": meta.get("id") or ("live-" + (_slugify(title) or "article")),
        "title": title,
        "doc_type": meta.get("doc_type") or "News",
        "typology": (llm_json.get("typology") or meta.get("typology") or "").strip(),
        "source_org": meta.get("source_org") or "Live input (companion)",
        "source_url": meta.get("source_url") or "",
        "basis": meta.get("basis") or "",
        "article_text": body,
        "entities": [
            {k: v for k, v in {
                "name": (e.get("name") or "").strip(),
                "type": (e.get("type") or "").strip().lower(),
                "location": (e.get("location") or "").strip() or None,
                "age": (str(e.get("age")).strip() if e.get("age") not in (None, "") else None),
                "profession": (e.get("profession") or "").strip() or None,
                "context": (e.get("context") or "").strip() or None,
                # Phase 41 — present ONLY when the model emitted them (old captures replay unchanged)
                "aliases": [a for a in (str(x).strip() for x in (e.get("aliases") or [])) if a] or None,
                "properties": [
                    {"kind": pk, "value": pv}
                    for pk, pv in ((str(p.get("kind") or "").strip(), str(p.get("value") or "").strip())
                                   for p in (e.get("properties") or []) if isinstance(p, dict))
                    if pk and pv
                ] or None,
            }.items() if v}
            for e in (llm_json.get("entities") or [])
        ],
        "red_flags": [
            {k: v for k, v in {
                "flag": (f.get("flag") or "").strip(),
                "red_flag": (f.get("red_flag") or "").strip(),
                "category": (f.get("category") or "").strip() or None,
            }.items() if v}
            for f in (llm_json.get("red_flags") or [])
        ],
    }
    # Phase 41 — record-level enrichment, added ONLY when non-empty (old captures replay unchanged).
    main_subjects = [s for s in (str(x).strip() for x in (llm_json.get("main_subjects") or [])) if s]
    if main_subjects:
        pre["main_subjects"] = main_subjects
    relationships = [
        {"from": fr, "to": to, "label": lb, "evidence": ev}
        for fr, to, lb, ev in (
            (str(r.get("from") or "").strip(), str(r.get("to") or "").strip(),
             str(r.get("label") or "").strip(), str(r.get("evidence") or "").strip())
            for r in (llm_json.get("relationships") or []) if isinstance(r, dict))
        if fr and to and lb and ev
    ]
    if relationships:
        pre["relationships"] = relationships
    kept, dropped = news_ground.ground_record(pre, body)
    # Phase 38 — LIVE-mode entity-precision pass: drop institutional noise + surname-alias duplicates the
    # model over-extracts (faithful; never invents; preserves every grounded subject). LIVE PATH ONLY —
    # build.py does not call this, so the committed records + offline dist/news stay byte-frozen.
    kept["entities"], ent_dropped = news_ground.screen_entities(kept["entities"], text)
    dropped = list(dropped) + ent_dropped
    # Phase 41 — the fold inversion renames subset/moniker entities into parent ALIASES; remap +
    # re-filter relationships/main_subjects so referential integrity survives the fold.
    rename = {d["value"]: d["folded_into"] for d in ent_dropped if d.get("folded_into")}
    kept = news_ground.reconcile_refs(kept, rename)
    for i, e in enumerate(kept["entities"], 1):
        e["id"] = f"E{i}"
    for i, f in enumerate(kept["red_flags"], 1):
        f["id"] = f"R{i}"
    return kept, dropped


# ── Phase 38 — second-pass entity verification (LIVE only; on by default) ───────────────────────────
# A focused, KEEP-BIASED per-entity check that cleans the residual institutional noise the extraction
# prompt's subjects-only rule leaves on articles where the model is inconsistent (e.g. agency/court names
# that survive the first pass). Measured on the stress corpus: drops the residual with ZERO real-subject
# loss (the naive forced-choice variant lost 6 designated parties — the keep-bias is load-bearing). It is
# NEURAL, so it lives in the LIVE pipeline (extract), NOT in the deterministic build_record core that the
# offline replay fixtures pin. It only DROPS, never adds → the grounding gate's faithfulness floor holds.
VERIFY_SYS = (
    "You are an AML analyst reviewing ONE entity extracted from a news/enforcement article. Answer NONSUBJECT "
    "ONLY if the entity is CLEARLY just one of: an announcing official, a prosecutor, a judge, an investigating "
    "agency or its field office, a court, a prosecuting district, or a government program. In EVERY other case "
    "— a perpetrator, defendant, sanctioned/designated party, or ANY company, account, or alias connected to "
    "the scheme — answer SUBJECT. When in doubt, answer SUBJECT (missing a real subject is the costlier error). "
    "Answer with EXACTLY one word: SUBJECT or NONSUBJECT."
)


def _entity_context(name: str, body: str) -> str:
    """Local article context for the verify call: sentences mentioning the name OR its distinctive key
    token (catches alias/short-form mentions — e.g. the '<Alias> was designated…' sentence that
    establishes subject status). Capped; falls back to the article head."""
    sents = re.split(r"(?<=[.!?])\s+", body)
    words = re.findall(r"[A-Za-z]{5,}", name)
    key = max(words, key=len) if words else name
    hit = list(dict.fromkeys(s.strip() for s in sents if name in s or (key and key in s)))
    return " ".join(hit[:4])[:900] or body[:400]


def verify_subject(name: str, etype: str, context: str, *, llm_url: str, model: str) -> bool:
    """One keep-biased classification call. Returns True (KEEP) unless the model clearly says NONSUBJECT.
    Fail-OPEN: any error → KEEP (never drop a subject because the verifier was unreachable)."""
    body = {
        "model": model, "temperature": 0, "max_tokens": 4,
        "messages": [
            {"role": "system", "content": VERIFY_SYS},
            {"role": "user", "content": f"Entity: {name}\nType: {etype}\nContext from the article:\n{context}\n\nSUBJECT or NONSUBJECT?"},
        ],
        "chat_template_kwargs": {"enable_thinking": False},
    }
    try:
        req = urllib.request.Request(llm_url, data=json.dumps(body).encode("utf-8"),
                                     headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=60) as r:
            out = json.loads(r.read().decode("utf-8"))["choices"][0]["message"]["content"]
        return "NONSUBJECT" not in out.upper()
    except Exception:  # noqa: BLE001 — the verifier is an enhancement; degrade to KEEP, never drop on error
        return True


def verify_entities(record: dict, article: str, *, llm_url: str, model: str, on_progress=None):
    """Second pass over a grounded record's entities — drop the ones the keep-biased verifier rejects as
    NON-subjects, then re-id the survivors E1.. contiguously. Returns (record, dropped). Pure aside from
    the model calls; mutates a copy. `on_progress` (Phase 39) is notified per entity ("verifying", i, n,
    name) — the N sequential verify calls are the wall-time majority, so this is where progress lives."""
    notify = on_progress or (lambda stage, **kw: None)
    body = news_ground.article_body(article)
    ents = record.get("entities") or []
    kept, dropped = [], []
    for i, e in enumerate(ents, 1):
        notify("verifying", i=i, n=len(ents), name=e.get("name", ""))
        if verify_subject(e.get("name", ""), e.get("type", ""), _entity_context(e.get("name", ""), body),
                          llm_url=llm_url, model=model):
            kept.append(e)
        else:
            dropped.append({"kind": "entity", "value": e.get("name"), "reason": "second-pass: not a subject of the financial crime"})
    out = dict(record)
    out["entities"] = [{**e, "id": f"E{i}"} for i, e in enumerate(kept, 1)]
    # Phase 41 — a verify-dropped entity must not leave dangling relationship/main_subject references
    out = news_ground.reconcile_refs(out)
    return out, dropped


def extract(text: str, meta: dict = None, *, llm_url: str = DEFAULT_LLM_URL, model: str = DEFAULT_MODEL,
            verify: bool = True, on_progress=None):
    """Full live pipeline: model -> parse -> assemble -> ground (deterministic core) -> optional keep-biased
    second-pass entity verify (Phase 38, on by default). Returns (record, dropped). `on_progress` (Phase 39)
    is an optional stage callback (`on_progress(stage, **detail)`) — default no-op, so every existing caller
    (the replay fixtures, the --live smoke) is byte-for-byte unaffected."""
    notify = on_progress or (lambda stage, **kw: None)
    notify("extracting")
    raw = call_llm(text, llm_url=llm_url, model=model)
    notify("grounding")
    record, dropped = build_record(parse_llm_json(raw), text, meta)
    if verify:
        record, vdropped = verify_entities(record, text, llm_url=llm_url, model=model, on_progress=notify)
        dropped = list(dropped) + vdropped
    return record, dropped


def live_config(args, persist: bool = False) -> dict:
    """The `NEWS.live` block the served page reads to enable the live branch (absent in the offline build).
    Phase 36 adds the watchlist/disposition endpoints + a `persist` flag the live UI reflects."""
    return {"extract": "/extract", "watchlist": "/watchlist", "disposition": "/disposition",
            "prune": "/watchlist/prune", "anchor": "/anchor",
            "persist": persist, "model": args.model, "llm_url": args.llm_url}


def news_payload(live_cfg: dict) -> dict:
    """Assemble the seed NEWS object — the committed articles + book, mirroring build.render_news, plus
    the `live` config. The offline build inlines the same object WITHOUT `live` (so its live branch is
    inert and gets stripped)."""
    articles, book = build.load_news()
    return {
        "brand": {"title": "Signal Watch", "subtitle": "Adverse-Media Stream · Vision Prototype"},
        "badge": "Illustrative data & outputs",
        "articles": articles,
        "book": book,
        "match": {"threshold": build.NEWS_MATCH_THRESHOLD},
        "live": live_cfg,
    }


def render_page(live_cfg: dict) -> str:
    """Inline the seed NEWS (with `live`) into news.html and return the served HTML. Unlike
    build.render_news this does NOT enforce the offline self-contained guard — the companion-served page
    is intentionally allowed to fetch its same-origin /extract endpoint."""
    template = build.NEWS_TEMPLATE.read_text(encoding="utf-8")
    n = template.count(build.NEWS_PLACEHOLDER)
    if n != 1:
        build.die(f"expected exactly one {build.NEWS_PLACEHOLDER} in news.html, found {n}")
    payload = news_payload(live_cfg)
    out = template.replace(build.NEWS_PLACEHOLDER, json.dumps(payload, ensure_ascii=False, indent=2))
    if build.NEWS_PLACEHOLDER in out:
        build.die("news placeholder survived substitution")
    return out


class Handler(BaseHTTPRequestHandler):
    server_version = "SignalWatchNewsLive/0.1"

    def _send(self, code: int, body: bytes, ctype: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _json(self, code: int, obj: dict) -> None:
        self._send(code, json.dumps(obj).encode("utf-8"), "application/json; charset=utf-8")

    def do_GET(self) -> None:
        path = self.path.split("?", 1)[0]
        if path in ("/", "/index.html"):
            self._send(200, self.server.page.encode("utf-8"), "text/html; charset=utf-8")
        elif path == "/health":
            self._json(200, {"ok": True, "live": True, "persist": self.server.store is not None})
        elif path == "/watchlist":
            # the live screening surface: book ∪ escalated (reconciled + provenance). With persistence off
            # this is the static book reconciled to the same shape (no growth) — never an error.
            store = self.server.store
            rows = (store.watchlist_rows(self.server.book) if store
                    else news_store.reconcile_book(self.server.book))
            self._json(200, {"rows": rows, "persist": store is not None})
        elif path == "/anchor":
            # Phase 42 — the dossier read: the accumulated identity for one anchor, name-keyed (the
            # store resolves name→anchor server-side — the merge-robust seam). READ-ONLY: conflicting
            # property values arrive as separate provenance'd rows and are never resolved here.
            name = (urllib.parse.parse_qs(self.path.partition("?")[2]).get("name") or [""])[0].strip()
            if not name:
                self._json(400, {"error": "missing 'name' (the anchor to look up)"}); return
            store = self.server.store
            if store is None:
                self._json(503, {"error": "persistence off — no anchor store (run under .venv, without --no-persist)"})
                return
            a = store.anchor_summary(name)
            if a is None:
                self._json(404, {"error": f"no anchor for {name!r}"}); return
            self._json(200, a)
        else:
            self._json(404, {"error": f"not found: {path}"})

    def do_POST(self) -> None:
        path = self.path.split("?", 1)[0]
        if path == "/extract":
            self._extract(); return
        if path == "/disposition":
            self._disposition(); return
        if path == "/watchlist/prune":
            self._prune(); return
        self._json(404, {"error": f"not found: {path}"})

    def _read_json(self):
        """Parse a JSON request body; returns (obj, None) or (None, error_str)."""
        try:
            length = int(self.headers.get("Content-Length") or 0)
            return json.loads(self.rfile.read(length) or b"{}"), None
        except (ValueError, json.JSONDecodeError):
            return None, "invalid JSON body"

    def _emit(self, obj: dict) -> None:
        """One NDJSON progress/result line, flushed immediately (Phase 39). The handler speaks HTTP/1.0
        (BaseHTTPRequestHandler default) — no Content-Length, the body ends when the connection closes —
        so a plain write+flush per event reaches the browser's fetch ReadableStream as it happens."""
        self.wfile.write((json.dumps(obj, ensure_ascii=False) + "\n").encode("utf-8"))
        self.wfile.flush()

    def _extract(self) -> None:
        payload, err = self._read_json()
        if err:
            self._json(400, {"error": err}); return
        text = (payload.get("text") or "").strip()
        url = (payload.get("url") or "").strip()
        if not text and not url:
            self._json(400, {"error": "missing 'text' or 'url' (the article to process)"}); return
        meta = {k: payload[k] for k in ("title", "source_org", "source_url", "doc_type", "typology")
                if payload.get(k)}
        # Phase 41 — what KIND of document this is (drives anchor provenance significance). Closed
        # vocab; anything else degrades to "" (unknown) rather than erroring — the scan still runs.
        source_type = (payload.get("source_type") or "").strip()
        if source_type not in news_store.SOURCE_TYPES:
            source_type = ""
        # Phase 39 — the response is an NDJSON STREAM of stage events ending in {"done": …} or {"error": …}.
        # The 200 is committed before the pipeline runs, so every later failure travels IN-stream (the
        # client reads events, not status codes). Request-shape errors above still fail fast as plain 400s.
        self.send_response(200)
        self.send_header("Content-Type", "application/x-ndjson; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        try:
            # Phase 39 — ONE-SHOT URL mode: acquire (fetch ladder) → standardize → verify, then run the
            # same pipeline on the verified text. Pasted text WINS over a URL (the trim + re-run recovery
            # path). The converted text streams back EARLY so the client can fill the textarea — the
            # analyst sees exactly what the model saw, and can trim + re-run if the conversion was noisy.
            if url and not text:
                self._emit({"stage": "fetching", "url": url})
                acq = news_fetch.acquire(url)
                if not acq.get("ok"):
                    self._emit({"error": acq.get("error") or "URL acquisition failed",
                                "attempts": acq.get("attempts") or []}); return
                text = acq["text"]
                meta.setdefault("source_url", url)
                if acq.get("title") and not meta.get("title"):
                    meta["title"] = acq["title"]
                self._emit({"stage": "converted", "text": text,
                            "title": acq.get("title") or "", "method": acq.get("method") or ""})
            try:
                record, dropped = extract(text, meta, llm_url=self.server.llm_url, model=self.server.model,
                                          verify=getattr(self.server, "verify", True),
                                          on_progress=lambda stage, **kw: self._emit({"stage": stage, **kw}))
            except (urllib.error.URLError, OSError) as ex:
                self._emit({"error": f"local model unreachable at {self.server.llm_url}: {ex}"}); return
            except (ValueError, KeyError, json.JSONDecodeError) as ex:
                self._emit({"error": f"model returned output that could not be parsed: {ex}"}); return
            # Honest fallback: if NOTHING in the model output grounded, surface it rather than show an empty arc.
            if not record["entities"] and not record["red_flags"]:
                self._emit({"error": "nothing in the model output grounded in the submitted article",
                            "dropped": dropped}); return
            # Persist the grounded scan (best-effort — a store failure must NEVER fail the scan). The scan_id is
            # echoed so the client's later /disposition can target a specific entity of THIS scan.
            scan_id = None
            if self.server.store is not None:
                try:
                    scan_id = self.server.store.append_scan(record, dropped, ts=_now(), source_type=source_type)
                except Exception as ex:  # noqa: BLE001 — persistence is optional; degrade, don't drop the result
                    self.log_message("persist failed: %s", ex)
            self._emit({"done": {"record": record, "dropped": dropped, "scan_id": scan_id}})
        except (BrokenPipeError, ConnectionResetError):
            # the client navigated away mid-stream — abandon this scan quietly (nothing to answer to)
            self.log_message("client disconnected mid-extract stream")

    def _disposition(self) -> None:
        # The human Disposition gate posts back here; 'escalate' adds the entity to the watchlist.
        if self.server.store is None:
            self._json(503, {"error": "persistence disabled (duckdb not installed) — dispositions are not recorded"}); return
        payload, err = self._read_json()
        if err:
            self._json(400, {"error": err}); return
        scan_id = (payload.get("scan_id") or "").strip()
        entity_id = (payload.get("entity_id") or "").strip()
        decision = (payload.get("decision") or "").strip()
        if not scan_id or not entity_id or decision not in ("escalate", "dismiss"):
            self._json(400, {"error": "need scan_id, entity_id, and decision ('escalate'|'dismiss')"}); return
        updated = self.server.store.set_disposition(scan_id, entity_id, decision)
        if not updated:
            self._json(404, {"error": f"no entity '{entity_id}' in scan '{scan_id}'"}); return
        self._json(200, {"ok": True, "updated": updated, "decision": decision})

    def _prune(self) -> None:
        # Watchlist management (Phase 38): un-escalate (remove) an escalated entity from the screening
        # surface BY NAME. The book is never touched — only escalated rows leave; the audit trail survives.
        if self.server.store is None:
            self._json(503, {"error": "persistence disabled (duckdb not installed) — the watchlist is the static book only"}); return
        payload, err = self._read_json()
        if err:
            self._json(400, {"error": err}); return
        name = (payload.get("name") or "").strip()
        if not name:
            self._json(400, {"error": "need a 'name' to prune from the watchlist"}); return
        removed = self.server.store.prune(name)
        if not removed:
            self._json(404, {"error": f"no escalated entity named {name!r} on the watchlist"}); return
        self._json(200, {"ok": True, "pruned": removed, "name": name})

    def log_message(self, fmt, *a):  # quieter than the default stderr spam
        sys.stderr.write("[serve_news] " + (fmt % a) + "\n")


def selftest() -> int:
    """Offline assertion (no socket bind): the assembled page drops the placeholder, carries the live
    config, inlines a valid NEWS object, and is a complete HTML doc."""
    cfg = live_config(argparse.Namespace(model=DEFAULT_MODEL, llm_url=DEFAULT_LLM_URL))
    page = render_page(cfg)
    payload = news_payload(cfg)
    assert build.NEWS_PLACEHOLDER not in page, "placeholder survived"
    assert '"live"' in page and '"extract": "/extract"' in page, "live config not inlined"
    assert '"watchlist": "/watchlist"' in page and '"disposition": "/disposition"' in page, \
        "live config missing the Phase-36 watchlist/disposition endpoints"
    assert '"prune": "/watchlist/prune"' in page, "live config missing the Phase-38 watchlist prune endpoint"
    assert '"anchor": "/anchor"' in page, "live config missing the Phase-42 anchor dossier endpoint"
    assert "const NEWS = {" in page, "NEWS object not inlined as expected"
    assert "liveInit" in page and "fetch(NEWS.live.extract" in page, "companion page missing the live branch"
    assert "liveReadStream" in page and "liveStageLabel" in page, \
        "companion page missing the Phase-39 progress-stream reader"
    assert page.rstrip().endswith("</html>"), "served page is not a complete HTML document"
    assert json.loads(json.dumps(payload)) == payload, "payload is not JSON round-trippable"
    assert payload["articles"] and payload["book"].get("rows"), "seed data empty"
    # Phase 41 — the enriched extraction contract, vocab authority in news_ground (never redefined here)
    ent_props = EXTRACT_SCHEMA["properties"]["entities"]["items"]["properties"]
    assert "aliases" in ent_props and "properties" in ent_props, "entity schema missing aliases/properties"
    assert ent_props["properties"]["items"]["properties"]["kind"]["enum"] == list(news_ground.PROPERTY_KINDS), \
        "property-kind enum must mirror news_ground.PROPERTY_KINDS (single authority)"
    rel = EXTRACT_SCHEMA["properties"]["relationships"]["items"]["properties"]
    assert rel["label"]["enum"] == list(news_ground.RELATION_LABELS), \
        "relation-label enum must mirror news_ground.RELATION_LABELS (single authority)"
    assert "main_subjects" in EXTRACT_SCHEMA["properties"], "schema missing main_subjects"
    for needle in ("aliases", "properties", "relationships", "main_subjects", "NOT a dob"):
        assert needle in SYSTEM_PROMPT, f"SYSTEM_PROMPT missing the Phase-41 {needle!r} contract"
    for kind in news_ground.PROPERTY_KINDS:
        assert kind in SYSTEM_PROMPT, f"SYSTEM_PROMPT missing property kind {kind!r}"
    # Phase 41 — build_record passes enrichment through ONLY when present (old captures replay unchanged)
    bj = {"title": "T", "entities": [{"name": "Acme Corp", "type": "org",
                                      "aliases": ["ACME"], "properties": [{"kind": "wallet", "value": "bc1qxy"}]},
                                     {"name": "Bo Vance", "type": "person"}],
          "red_flags": [], "main_subjects": ["Acme Corp"],
          "relationships": [{"from": "Bo Vance", "to": "Acme Corp", "label": "owner-or-controller-of",
                             "evidence": "Bo Vance, who controls Acme Corp"}]}
    rec41, _ = build_record(bj, "# T\nAcme Corp (ACME) moved funds to wallet bc1qxy for Bo Vance, who controls Acme Corp.")
    assert rec41["entities"] and rec41["entities"][0].get("aliases") == ["ACME"], rec41["entities"]
    assert rec41["entities"][0].get("properties") == [{"kind": "wallet", "value": "bc1qxy"}], rec41["entities"]
    assert rec41.get("main_subjects") == ["Acme Corp"], rec41
    assert rec41.get("relationships") == [{"from": "Bo Vance", "to": "Acme Corp",
                                           "label": "owner-or-controller-of",
                                           "evidence": "Bo Vance, who controls Acme Corp"}], rec41
    rec_legacy, _ = build_record({"title": "T", "entities": [{"name": "Acme Corp", "type": "org"}],
                                  "red_flags": []}, "# T\nAcme Corp moved funds yesterday.")
    assert "aliases" not in rec_legacy["entities"][0] and "properties" not in rec_legacy["entities"][0]
    assert "main_subjects" not in rec_legacy and "relationships" not in rec_legacy, \
        "legacy captures must NOT gain new keys (golden compatibility)"
    print(f"serve_news --selftest: PASS "
          f"({len(payload['articles'])} articles, {len(payload['book']['rows'])} book rows, "
          f"{len(page):,} bytes served)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Live companion for the M8 news stream (dev/authoring-time only).")
    ap.add_argument("--port", type=int, default=DEFAULT_PORT)
    ap.add_argument("--llm-url", default=DEFAULT_LLM_URL, help="llama-cpp OpenAI-compatible chat endpoint")
    ap.add_argument("--model", default=DEFAULT_MODEL, help="model name passed to llama-cpp (swappable)")
    ap.add_argument("--db", default=DEFAULT_DB, help="DuckDB store path (gitignored runtime data; Phase 36)")
    ap.add_argument("--no-persist", action="store_true",
                    help="disable the DuckDB store — screen against the static book only (no watchlist growth)")
    ap.add_argument("--export-parquet", metavar="DIR", help="export the store tables to DIR/*.parquet and exit")
    ap.add_argument("--no-verify-entities", action="store_true",
                    help="disable the Phase-38 keep-biased second-pass entity verify (on by default; one extra model call per extracted entity)")
    ap.add_argument("--selftest", action="store_true", help="assemble the page offline, assert, exit")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    store = _open_store(args)

    if args.export_parquet:
        if store is None:
            print("[serve_news] cannot export — persistence unavailable (install duckdb in the .venv)."); return 1
        paths = store.export_parquet(args.export_parquet)
        print("[serve_news] exported parquet: " + ", ".join(f"{k}={v}" for k, v in paths.items()))
        return 0

    page = render_page(live_config(args, persist=store is not None))
    httpd = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    httpd.page = page
    httpd.llm_url = args.llm_url
    httpd.model = args.model
    httpd.store = store
    httpd.book = (build.load_news()[1].get("rows") or [])     # the static book — the watchlist base
    httpd.verify = not args.no_verify_entities                # Phase 38 — second-pass entity verify (default ON)
    url = f"http://localhost:{args.port}/"
    print(f"[serve_news] live companion on {url}  (model={args.model} via {args.llm_url}; "
          f"entity-verify {'ON' if httpd.verify else 'off'})")
    print(f"[serve_news] the offline dist/news/index.html remains the scripted fallback. Ctrl-C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[serve_news] stopped.")
    finally:
        if store is not None:
            store.close()
    return 0


def _open_store(args):
    """Open the DuckDB store, or return None (persistence disabled) — gracefully, so the companion still
    serves the page + /extract when duckdb is absent or --no-persist is set."""
    if args.no_persist:
        print("[serve_news] persistence disabled (--no-persist) — screening against the static book only.")
        return None
    try:
        store = news_store.NewsStore(args.db)
        print(f"[serve_news] persistence: DuckDB store at {args.db} — escalations feed the watchlist.")
        return store
    except Exception as ex:  # noqa: BLE001 — duckdb missing / unopenable: degrade, don't crash the companion
        print(f"[serve_news] persistence disabled ({ex}). Install duckdb in the .venv to enable the watchlist.")
        return None


if __name__ == "__main__":
    sys.exit(main())
