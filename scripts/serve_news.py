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
    python3 scripts/serve_news.py                  # serve on http://localhost:8000
    python3 scripts/serve_news.py --port 8001 --llm-url http://localhost:8080/v1/chat/completions
    python3 scripts/serve_news.py --selftest       # assemble the page offline, assert, exit
"""
import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import build  # scripts/ is on sys.path[0] when run as `python3 scripts/serve_news.py`; stdlib-only import
import news_ground  # the shared grounding gate — drops ungrounded live extractions (live == build by construction)
import news_store  # Phase 36: DuckDB persistence + the escalated-only watchlist (companion-only; build.py never imports it)


def _now() -> str:
    """UTC timestamp stamped on each persisted scan (the watchlist provenance reads from it)."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

DEFAULT_PORT = 8000
DEFAULT_LLM_URL = "http://localhost:8080/v1/chat/completions"
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
                },
                "required": ["name", "type"],
            },
        },
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
    "- red_flags: each suspicious behaviour. `flag` MUST be a VERBATIM, CONTIGUOUS quote from the article "
    "(an exact substring — do not paraphrase it, do not stitch across gaps). `red_flag` is a TERSE, "
    "mechanism-named AML translation (e.g. 'Cash-for-crypto handovers to break the trail', "
    "'Ownership obfuscation: 50%+ held by a blocked person') — 12-200 characters, DIFFERENT wording from "
    "the verbatim flag. `category` is a short label.\n"
    "A downstream grounding check DISCARDS anything not literally present in the article, so quote exactly."
)
USER_PROMPT_TMPL = "ARTICLE:\n\n{article}\n\nExtract the entities and red flags as JSON."


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
    kept, dropped = news_ground.ground_record(pre, body)
    # Phase 38 — LIVE-mode entity-precision pass: drop institutional noise + surname-alias duplicates the
    # model over-extracts (faithful; never invents; preserves every grounded subject). LIVE PATH ONLY —
    # build.py does not call this, so the committed records + offline dist/news stay byte-frozen.
    kept["entities"], ent_dropped = news_ground.screen_entities(kept["entities"], text)
    dropped = list(dropped) + ent_dropped
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


def verify_entities(record: dict, article: str, *, llm_url: str, model: str):
    """Second pass over a grounded record's entities — drop the ones the keep-biased verifier rejects as
    NON-subjects, then re-id the survivors E1.. contiguously. Returns (record, dropped). Pure aside from
    the model calls; mutates a copy."""
    body = news_ground.article_body(article)
    kept, dropped = [], []
    for e in record.get("entities") or []:
        if verify_subject(e.get("name", ""), e.get("type", ""), _entity_context(e.get("name", ""), body),
                          llm_url=llm_url, model=model):
            kept.append(e)
        else:
            dropped.append({"kind": "entity", "value": e.get("name"), "reason": "second-pass: not a subject of the financial crime"})
    out = dict(record)
    out["entities"] = [{**e, "id": f"E{i}"} for i, e in enumerate(kept, 1)]
    return out, dropped


def extract(text: str, meta: dict = None, *, llm_url: str = DEFAULT_LLM_URL, model: str = DEFAULT_MODEL,
            verify: bool = True):
    """Full live pipeline: model -> parse -> assemble -> ground (deterministic core) -> optional keep-biased
    second-pass entity verify (Phase 38, on by default). Returns (record, dropped)."""
    record, dropped = build_record(parse_llm_json(call_llm(text, llm_url=llm_url, model=model)), text, meta)
    if verify:
        record, vdropped = verify_entities(record, text, llm_url=llm_url, model=model)
        dropped = list(dropped) + vdropped
    return record, dropped


def live_config(args, persist: bool = False) -> dict:
    """The `NEWS.live` block the served page reads to enable the live branch (absent in the offline build).
    Phase 36 adds the watchlist/disposition endpoints + a `persist` flag the live UI reflects."""
    return {"extract": "/extract", "watchlist": "/watchlist", "disposition": "/disposition",
            "prune": "/watchlist/prune", "persist": persist, "model": args.model, "llm_url": args.llm_url}


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

    def _extract(self) -> None:
        payload, err = self._read_json()
        if err:
            self._json(400, {"error": err}); return
        text = (payload.get("text") or "").strip()
        if not text:
            self._json(400, {"error": "missing 'text' (the article to process)"}); return
        meta = {k: payload[k] for k in ("title", "source_org", "source_url", "doc_type", "typology")
                if payload.get(k)}
        try:
            record, dropped = extract(text, meta, llm_url=self.server.llm_url, model=self.server.model,
                                      verify=getattr(self.server, "verify", True))
        except (urllib.error.URLError, OSError) as ex:
            self._json(502, {"error": f"local model unreachable at {self.server.llm_url}: {ex}"}); return
        except (ValueError, KeyError, json.JSONDecodeError) as ex:
            self._json(502, {"error": f"model returned output that could not be parsed: {ex}"}); return
        # Honest fallback: if NOTHING in the model output grounded, surface it rather than show an empty arc.
        if not record["entities"] and not record["red_flags"]:
            self._json(422, {"error": "nothing in the model output grounded in the submitted article",
                             "dropped": dropped}); return
        # Persist the grounded scan (best-effort — a store failure must NEVER fail the scan). The scan_id is
        # echoed so the client's later /disposition can target a specific entity of THIS scan.
        scan_id = None
        if self.server.store is not None:
            try:
                scan_id = self.server.store.append_scan(record, dropped, ts=_now())
            except Exception as ex:  # noqa: BLE001 — persistence is optional; degrade, don't drop the result
                self.log_message("persist failed: %s", ex)
        self._json(200, {"record": record, "dropped": dropped, "scan_id": scan_id})

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
    assert "const NEWS = {" in page, "NEWS object not inlined as expected"
    assert "liveInit" in page and "fetch(NEWS.live.extract" in page, "companion page missing the live branch"
    assert page.rstrip().endswith("</html>"), "served page is not a complete HTML document"
    assert json.loads(json.dumps(payload)) == payload, "payload is not JSON round-trippable"
    assert payload["articles"] and payload["book"].get("rows"), "seed data empty"
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
