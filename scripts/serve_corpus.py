#!/usr/bin/env python3
"""Live companion for the M7 corpus explorer (Phase 46 — authoring/dev-time ONLY).

This is NOT part of the ship artifact. The shippable `dist/corpus/index.html` stays a single
self-contained offline file (the scripted fallback, the stakeholder demo). This companion adds
the optional, isolated "live mode" the non-negotiable already sanctions: it serves `corpus.html`
over http://localhost (SAME-ORIGIN with the API — no CORS) with `CORPUS.live` set, and proxies a
local llama-cpp server to DERIVE a pasted advisory document in real time — the corpus's inverted
extraction boundary made live. The model PROPOSES {section, flag, red_flag, C, D} per indicator;
the deterministic layer derives EVERYTHING else (src_line locate; posture→status/data — verified
exact on all 2,251 committed indicators at the Phase-46 probe; the cover×data matrix → build_rec;
template build_logic) and the FROZEN gate (`derive_signals.check_record`) DISPOSES. Only
gate-green indicators ever reach the page.

The Phase-46 T1 probe decided the harness (ph46_probe.md, user checkpoint 2026-06-11): the
DIRECT pipeline (this pattern) beat an opencode agent loop — identical extraction quality at
0.32× the wall time; the loop's iterate-on-failure value lands here instead as ONE deterministic
RETRY: gate-failing indicators are re-prompted once WITH their violation text, then
grounded-or-dropped (the news precedent — honest counts, never silent).

LIVE-DERIVED OUTPUT IS DISPLAY/PROPOSE-ONLY (Phase-46 A4): nothing is persisted anywhere by this
companion (there is no store — disconnect-persists-nothing holds by construction), and committing
a derived record to data/ remains a separate human-reviewed act under the licence rules.

Stdlib ONLY. Imports `build` (corpus payload loaders — committed data, never the LLM layer) and
`derive_signals` (the stdlib-only frozen gate; the corpus analogue of serve_news→news_ground).

Usage:
    python3 scripts/serve_corpus.py                 # http://localhost:8010, model at 127.0.0.1:8080
    python3 scripts/serve_corpus.py --port 8011 --llm-url http://127.0.0.1:8080/v1/chat/completions
    python3 scripts/serve_corpus.py --selftest      # offline assertions (no socket, no model), exit
"""
import argparse
import json
import re
import sys
import threading
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import build            # corpus payload loaders + template paths (stdlib-only)
import derive_signals   # the FROZEN derivation gate — imported, never copied

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PORT = 8010      # the news companion holds 8000 — both can run side by side
DEFAULT_LLM_URL = "http://127.0.0.1:8080/v1/chat/completions"
DEFAULT_MODEL = "qwen"   # any model behind llama-cpp's OpenAI-compatible /v1
MAX_GEN_TOKENS = 16384   # the Phase-43-measured budget class; a 17-indicator OA generated ~8K
TAXONOMY = ROOT / "data" / "capability-taxonomy.json"
FEWSHOT_RECORD = ROOT / "data" / "fintrac" / "derived" / "fintrac-cannabis.json"

_CAP_IDS = [f"C{i}" for i in range(1, 29)]
_DS_IDS = [f"D{i}" for i in range(1, 21)]
_S_MAP = {"y": "covered", "partial": "partial", "n": "gap"}
_D_MAP = {"y": "available", "partial": "partial", "n": "insufficient"}

# ---- the model's shape: ONLY the neural fields; coverage is never the model's to claim ---------
DERIVE_SCHEMA = {
    "type": "object",
    "properties": {
        "indicators": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "section": {"type": "string"},
                    "flag": {"type": "string"},
                    "red_flag": {"type": "string"},
                    "capability": {"type": "string", "enum": _CAP_IDS},
                    "data_source": {"type": "string", "enum": _DS_IDS},
                },
                "required": ["section", "flag", "red_flag", "capability", "data_source"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["indicators"],
    "additionalProperties": False,
}


class DeriveError(ValueError):
    """A pipeline failure with a NAMED, analyst-actionable reason (the serve_news ExtractError
    pattern) — emitted verbatim in-stream, never disguised as a generic parse failure."""


def _postures():
    t = json.loads(TAXONOMY.read_text(encoding="utf-8"))
    return {c["id"]: c for c in t["capabilities"]}, {d["id"]: d for d in t["data_sources"]}


def build_spec() -> str:
    """The deterministic system prompt: extraction rules + the FULL C/D vocabulary (from the
    committed taxonomy — single authority, never inlined here) + register exemplars from a
    committed gate-passing FINTRAC record (anchor style to the reference, never to a generic
    style description). Rebuilt per process start — committed-data-driven, no drift."""
    caps, dss = _postures()
    vocab = ["CAPABILITIES (pick the ONE best-fit code per indicator):"]
    vocab += [f"- {c['id']} {c['name']}: {c['desc']}" for c in caps.values()]
    vocab.append("")
    vocab.append("DATA SOURCES (the ONE feed the indicator is primarily observed in):")
    vocab += [f"- {d['id']} {d['name']}: {d['desc']}" for d in dss.values()]
    few = json.loads(FEWSHOT_RECORD.read_text(encoding="utf-8"))
    shots = ["EXAMPLES (from a previously derived FINTRAC Operational Alert — match this register):"]
    shots += [json.dumps({"section": i["section"], "flag": i["flag"], "red_flag": i["red_flag"],
                          "capability": i["capability"], "data_source": i["data_source"]}, indent=1)
              for i in few["indicators"][:3]]
    return f"""You derive detection-signal indicators from a financial-intelligence advisory.

TASK: read the advisory and extract EVERY money-laundering / financial-crime indicator from its
enumerated indicator section (the list under its "indicators" heading, including all subheadings).
Do not stop early — extract the COMPLETE list.

For each indicator emit:
- "section": the subheading the indicator appears under (short, as written).
- "flag": the indicator's text VERBATIM — an EXACT contiguous substring of the advisory, copied
  character-for-character (same words, same punctuation). NEVER paraphrase, NEVER merge two
  bullets, NEVER add or drop words. If a bullet is interrupted by a footnote or page break,
  quote only the contiguous span before the break.
- "red_flag": your TRANSLATION of the flag into natural AML practitioner terms — a crisp phrase
  of 12 to 240 characters, standard AML mechanism vocabulary (structuring, funnel account, rapid
  movement, nominee, layering, third-party deposits, …). NOT a copy of the verbatim text.
- "capability": the ONE detection-capability code (C1-C28) that best detects this indicator.
- "data_source": the ONE data-source code (D1-D20) where this indicator is primarily observed.

{chr(10).join(vocab)}

{chr(10).join(shots)}

Return JSON: {{"indicators": [{{"section", "flag", "red_flag", "capability", "data_source"}}, ...]}}
"""


RETRY_TMPL = """You previously extracted indicators from this advisory; the deterministic gate
REJECTED the ones below. Fix ONLY these and return them in the same JSON shape (one corrected
entry per rejected indicator, same order). The most common failure: "flag not grounded" means
your flag was NOT an exact substring — re-copy it character-for-character from the advisory,
choosing a contiguous span. A red_flag failure means the translation was missing/identical/too
long or short.

REJECTED (with the gate's violation text):
{rejected}

ADVISORY:

{article}
"""

USER_PROMPT_TMPL = "ADVISORY:\n\n{article}\n\nExtract the complete indicator list per the rules."


# ---- transport (the serve_news Phase-43 streaming conventions) ---------------------------------
def _consume_sse(lines, on_tokens=None):
    """Accumulate an OpenAI-style SSE chat stream into (content, finish_reason, n_chunks)."""
    content, finish, n = [], None, 0
    for raw in lines:
        line = raw.decode("utf-8", "replace").strip()
        if not line.startswith("data: "):
            continue
        data = line[6:]
        if data == "[DONE]":
            break
        try:
            d = json.loads(data)
        except json.JSONDecodeError:
            continue
        for ch in d.get("choices") or []:
            piece = (ch.get("delta") or {}).get("content")
            if piece:
                content.append(piece)
                n += 1
                if on_tokens and n % 64 == 0:
                    on_tokens(n)
            if ch.get("finish_reason"):
                finish = ch["finish_reason"]
    return "".join(content), finish, n


def preflight_size(system: str, user: str, llm_url: str, timeout: int = 10) -> None:
    """Honest pre-flight: measured assembled prompt vs the server's n_ctx, reserving the
    generation headroom; NAMED refusal when it can't fit. FAIL-OPEN on probe errors."""
    try:
        base = llm_url.split("/v1/")[0]
        with urllib.request.urlopen(base + "/props", timeout=timeout) as r:
            props = json.loads(r.read().decode("utf-8"))
        n_ctx = (props.get("default_generation_settings") or {}).get("n_ctx") or props.get("n_ctx")
        if not n_ctx:
            return
        req = urllib.request.Request(base + "/tokenize",
                                     data=json.dumps({"content": system + "\n" + user}).encode("utf-8"),
                                     headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=timeout) as r:
            prompt_tokens = len(json.loads(r.read().decode("utf-8")).get("tokens") or [])
        if not prompt_tokens:
            return
        prompt_tokens += 64
    except Exception:  # noqa: BLE001 — fail-open by design (the raise sits BELOW the try)
        return
    if prompt_tokens + MAX_GEN_TOKENS > n_ctx:
        raise DeriveError(
            f"document too large for the model's context: ~{prompt_tokens} prompt tokens + "
            f"{MAX_GEN_TOKENS} generation headroom exceeds n_ctx={n_ctx} — trim the document, "
            f"or relaunch llama-server with a larger --ctx-size")


def call_llm(system: str, user: str, *, llm_url: str, model: str, timeout: int = 120,
             on_progress=None) -> str:
    """One strict-schema streamed call (idle-gap timeout; finish_reason READ — 'length' raises a
    NAMED budget failure instead of truncated JSON masquerading as a parse error)."""
    body = {
        "model": model,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "temperature": 0,
        "max_tokens": MAX_GEN_TOKENS,
        "stream": True,
        "response_format": {"type": "json_schema",
                            "json_schema": {"name": "derivation", "strict": True, "schema": DERIVE_SCHEMA}},
        "chat_template_kwargs": {"enable_thinking": False},
    }
    req = urllib.request.Request(llm_url, data=json.dumps(body).encode("utf-8"),
                                 headers={"Content-Type": "application/json"}, method="POST")
    on_tokens = (lambda n: on_progress(tokens=n)) if on_progress else None
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            content, finish, _n = _consume_sse(r, on_tokens)
    except TimeoutError:
        raise DeriveError(f"model stalled — no output for {timeout}s (idle-gap timeout); "
                          f"check the llama-server console") from None
    if finish == "length":
        raise DeriveError(f"output budget exhausted: the derivation needed more than "
                          f"{MAX_GEN_TOKENS} generated tokens — split the document")
    return content


def parse_llm_json(content: str) -> dict:
    """Strip <think>/fences/prose around the outermost {...} (the serve_news parser)."""
    s = re.sub(r"<think>.*?</think>", "", content, flags=re.S).strip()
    m = re.search(r"```(?:json)?\s*(.*?)```", s, flags=re.S)
    if m:
        s = m.group(1).strip()
    if not s.startswith("{"):
        i, j = s.find("{"), s.rfind("}")
        if i != -1 and j != -1 and j > i:
            s = s[i:j + 1]
    return json.loads(s)


# ---- the deterministic downstream (probe-verified) + the FROZEN gate ----------------------------
def locate_src_line(md_lines, nflag):
    """First 1-based line where the (normalized) flag span begins — a sliding window over the
    wrapped source. Probe-verified: 0 region-misses on the committed cannabis record."""
    n = len(md_lines)
    for i in range(n):
        if nflag in derive_signals.normalize("\n".join(md_lines[i:i + 10])):
            j = i
            while j + 1 < n and nflag in derive_signals.normalize("\n".join(md_lines[j + 1:j + 11])):
                j += 1
            return j + 1
    return None


def template_logic(red_flag: str, cap: dict, dsrc: dict) -> dict:
    """Deterministic shape-valid build_logic for a BUILD_NOW indicator. The committed convention:
    logic is template-generated, NEVER neurally re-authored (the ph33 rule). A live-derived record
    is propose-only, so this minimal template carries the gate's shape contract; a committed
    record would get the full per-capability spec template at human review."""
    rf = red_flag.strip()
    feats = [w.strip(",.()").lower().replace(" ", "_") for w in rf.split()[:4] if len(w) > 3] \
        or ["indicator_hit"]
    return {"signal_name": rf[:60], "class": cap.get("group", cap["name"])[:60], "features": feats,
            "logic": f"Detect: {rf} (per {cap['name']})", "window": "30d rolling",
            "source": dsrc["name"], "route": "AML case review queue"}


def assemble(extract: dict, md: str, doc_id: str) -> tuple:
    """extract.json → a full corpus-shaped derived record: src_line located, posture→status/data,
    matrix→build_rec, template logic on BUILD_NOW. Returns (record, problems) — problems are
    pre-gate failures (unknown codes), reported alongside gate violations."""
    caps, dss = _postures()
    md_lines = md.split("\n")
    inds, problems = [], []
    for k, e in enumerate(extract.get("indicators") or [], 1):
        iid = f"IND-{k:02d}"
        c, d = e.get("capability"), e.get("data_source")
        if c not in caps or d not in dss:
            problems.append(f"{iid}: unknown capability/data_source code ({c!r}/{d!r})")
            continue
        status, data = _S_MAP[caps[c]["posture"]], _D_MAP[dss[d]["posture"]]
        rec = derive_signals.build_rec_category(status, data)
        ind = {"id": iid, "section": (e.get("section") or "").strip(),
               "flag": (e.get("flag") or "").strip(), "red_flag": (e.get("red_flag") or "").strip(),
               "src_line": locate_src_line(md_lines, derive_signals.normalize(e.get("flag") or "")),
               "status": status, "data": data, "capability": c, "data_source": d, "build_rec": rec}
        if rec == "BUILD_NOW":
            ind["build_logic"] = template_logic(ind["red_flag"], caps[c], dss[d])
        else:
            ind["rationale"] = (f"{rec} per interview posture "
                                f"({c} {caps[c]['posture']} / {d} {dss[d]['posture']}).")
        inds.append(ind)
    return {"id": doc_id, "advisory": doc_id.upper(), "indicators": inds}, problems


def split_by_gate(record: dict, problems: list, md: str) -> tuple:
    """Run the FROZEN gate and split indicators into (passing, failing) where failing carries its
    violation text. Doc-level violations (no rf_region) surface as a DeriveError upstream."""
    violations = problems + derive_signals.check_record(record, md)
    doc_level = [v for v in violations if not v.startswith("IND-")]
    by_iid = {}
    for v in violations:
        if v.startswith("IND-"):
            by_iid.setdefault(v.split(":")[0], []).append(v)
    passing = [i for i in record["indicators"] if i["id"] not in by_iid]
    failing = [{"indicator": i, "violations": by_iid[i["id"]]}
               for i in record["indicators"] if i["id"] in by_iid]
    return passing, failing, doc_level


def derive(text: str, meta: dict = None, *, llm_url: str = DEFAULT_LLM_URL, model: str = DEFAULT_MODEL,
           on_progress=None):
    """Full live derivation: model → parse → deterministic assemble → the FROZEN gate → ONE
    violation-guided retry of ONLY the failing indicators (the T1-checkpoint decision) → final
    grounded-or-dropped split. Returns (entry, dropped) where entry is a corpus-advisory-shaped
    dict whose indicators are ALL gate-green, and dropped lists what fell with reasons.
    `on_progress(stage, **detail)` mirrors the serve_news stage-callback contract."""
    notify = on_progress or (lambda stage, **kw: None)
    meta = meta or {}
    title = (meta.get("title") or "").strip() or _first_heading(text) or "Live document"
    doc_id = "live-" + (re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:48] or "doc")

    spec = build_spec()
    user = USER_PROMPT_TMPL.format(article=text)
    preflight_size(spec, user, llm_url)
    notify("extracting")
    raw = call_llm(spec, user, llm_url=llm_url, model=model,
                   on_progress=lambda **kw: notify("extracting", **kw))
    notify("gating")
    extract = parse_llm_json(raw)
    record, problems = assemble(extract, text, doc_id)
    if not record["indicators"]:
        raise DeriveError("the model proposed no indicators with known C/D codes — nothing to gate")
    passing, failing, doc_level = split_by_gate(record, problems, text)
    if doc_level:
        # e.g. "no red-flag region found" — the document itself is not derivable under the anchors
        raise DeriveError("document not derivable: " + "; ".join(doc_level))
    notify("gated", passed=len(passing), failed=len(failing))

    dropped = []
    if failing:
        notify("retrying", count=len(failing))
        rejected = "\n".join(
            f"- {json.dumps({k: f['indicator'][k] for k in ('section', 'flag', 'red_flag', 'capability', 'data_source')})}"
            f"\n  violations: {'; '.join(f['violations'])}" for f in failing)
        try:
            raw2 = call_llm(spec, RETRY_TMPL.format(rejected=rejected, article=text),
                            llm_url=llm_url, model=model,
                            on_progress=lambda **kw: notify("retrying", **kw))
            fixed = parse_llm_json(raw2)
        except (DeriveError, ValueError, json.JSONDecodeError):
            fixed = {"indicators": []}   # the retry is best-effort; originals drop honestly below
        notify("regating")
        merged = {"indicators":
                  [{k: i[k] for k in ("section", "flag", "red_flag", "capability", "data_source")}
                   for i in passing] + (fixed.get("indicators") or [])}
        record2, problems2 = assemble(merged, text, doc_id)
        passing2, failing2, doc_level2 = split_by_gate(record2, problems2, text)
        if doc_level2:
            raise DeriveError("document not derivable after retry: " + "; ".join(doc_level2))
        # honest drop accounting: anything still failing after the one retry is stripped
        dropped = [{"flag": f["indicator"]["flag"][:160], "violations": f["violations"]}
                   for f in failing2]
        # originals whose retry replacement never came back also dropped (count the difference)
        n_unreturned = len(failing) - len(fixed.get("indicators") or [])
        if n_unreturned > 0:
            dropped.append({"flag": f"({n_unreturned} rejected indicator(s) not returned by the retry)",
                            "violations": ["retry returned fewer corrections than rejections"]})
        passing = passing2

    if not passing:
        raise DeriveError("nothing the model proposed survived the gate — no grounded indicators")
    # contiguous ids on the survivors (check_record uniqueness holds on the final record)
    final = {"indicators": [{k: i[k] for k in ("section", "flag", "red_flag", "capability", "data_source")}
                            for i in passing]}
    record, _ = assemble(final, text, doc_id)
    leftover = derive_signals.check_record(record, text)
    if leftover:
        raise DeriveError("internal: final record failed the gate — " + "; ".join(leftover[:3]))
    entry = {"id": doc_id, "advisory": doc_id.upper(), "title": title,
             "date": (meta.get("date") or ""), "url": (meta.get("source_url") or ""),
             "source": (meta.get("source_org") or "Live document — UNREVIEWED live derivation"),
             "derived": True, "live": True,
             "indicators": record["indicators"], "article_text": build._strip_provenance(text)}
    notify("derived", entry={k: v for k, v in entry.items() if k != "article_text"})
    return entry, dropped


def _first_heading(md: str) -> str:
    for line in md.split("\n"):
        s = line.strip().lstrip("#").strip()
        if s and not s.startswith("<!--") and len(s) > 8:
            return s[:120]
    return ""


# ---- the served page (corpus.html + the live config; T3 adds the client live region) ------------
def live_config(args) -> dict:
    return {"derive": "/derive", "model": args.model, "llm_url": args.llm_url}


def corpus_payload(live_cfg: dict) -> dict:
    """Assemble the SAME __CORPUS__ object the offline build inlines (build.render_corpus's
    documented sequence, via build's public loaders + validators — fail-loud, identical gating),
    plus the `live` config the offline build never carries."""
    merged = []
    for source in build.CORPUS_SOURCES:
        merged.extend(build._load_source(source))
    errors = build.validate_corpus_data(merged)
    if errors:
        build.die("corpus data fails boundary validation:\n  - " + "\n  - ".join(errors))
    vocab, tmap = build.load_typology_map()
    terrors = build.validate_typology(merged, vocab, tmap)
    if terrors:
        build.die("typology overlay fails boundary validation:\n  - " + "\n  - ".join(terrors))
    for entry in merged:
        if entry.get("derived") and entry["id"] in tmap:
            entry["typology"] = tmap[entry["id"]]
    imap = build.load_indicator_typology_map()
    ierrors = build.validate_indicator_typology(merged, vocab, imap)
    if ierrors:
        build.die("indicator typology overlay fails boundary validation:\n  - " + "\n  - ".join(ierrors))
    for entry in merged:
        if not entry.get("derived"):
            continue
        for i in entry.get("indicators") or []:
            i["typology"] = imap.get(f"{entry['id']}/{i.get('id', '?')}", entry.get("typology"))
    caps, srcs = build.load_capability_taxonomy()
    cerrors = build.validate_capability_taxonomy(merged, caps, srcs)
    if cerrors:
        build.die("capability taxonomy fails boundary validation:\n  - " + "\n  - ".join(cerrors))
    return {"brand": {"title": "Signal Watch", "subtitle": "AML Corpus Explorer · Vision Prototype"},
            "badge": "Illustrative data & outputs",
            "advisories": merged, "typologies": vocab,
            "taxonomy": {"capabilities": caps, "data_sources": srcs},
            "live": live_cfg}


def render_page(live_cfg: dict) -> str:
    """Inline the corpus payload (with `live`) into corpus.html. Unlike build.render_corpus this
    does NOT enforce the offline self-contained guard — the companion-served page is intentionally
    allowed to fetch its same-origin /derive endpoint (the serve_news.render_page precedent)."""
    template = build.CORPUS_TEMPLATE.read_text(encoding="utf-8")
    n = template.count(build.CORPUS_PLACEHOLDER)
    if n != 1:
        build.die(f"expected exactly one {build.CORPUS_PLACEHOLDER} in corpus.html, found {n}")
    out = template.replace(build.CORPUS_PLACEHOLDER,
                           json.dumps(corpus_payload(live_cfg), ensure_ascii=False, indent=2))
    if build.CORPUS_PLACEHOLDER in out:
        build.die("corpus placeholder survived substitution")
    return out


# ---- HTTP (the serve_news handler conventions: NDJSON stages, single-flight, named errors) ------
class Handler(BaseHTTPRequestHandler):
    server_version = "SignalWatchCorpusLive/0.1"

    def _send(self, code, body, ctype):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _json(self, code, obj):
        self._send(code, json.dumps(obj).encode("utf-8"), "application/json; charset=utf-8")

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path in ("/", "/index.html"):
            self._send(200, self.server.page.encode("utf-8"), "text/html; charset=utf-8")
        elif path == "/health":
            self._json(200, {"ok": True, "live": True, "persist": False})
        else:
            self._json(404, {"error": f"not found: {path}"})

    def do_POST(self):
        if self.path.split("?", 1)[0] == "/derive":
            self._derive(); return
        self._json(404, {"error": f"not found: {self.path}"})

    def _read_json(self):
        try:
            length = int(self.headers.get("Content-Length") or 0)
            return json.loads(self.rfile.read(length) or b"{}"), None
        except (ValueError, json.JSONDecodeError):
            return None, "invalid JSON body"

    def _emit(self, obj):
        self.wfile.write((json.dumps(obj, ensure_ascii=False) + "\n").encode("utf-8"))
        self.wfile.flush()

    def _derive(self):
        payload, err = self._read_json()
        if err:
            self._json(400, {"error": err}); return
        text = (payload.get("text") or "").strip()
        if not text:
            self._json(400, {"error": "missing 'text' (the advisory markdown to derive)"}); return
        meta = {k: payload[k] for k in ("title", "source_org", "source_url", "date") if payload.get(k)}
        # SINGLE-FLIGHT (the Phase-43 lesson): a second concurrent derivation would silently split
        # the local model's throughput — honest 409 pre-stream instead.
        lock = self.server.__dict__.setdefault("derive_lock", threading.Lock())
        if not lock.acquire(blocking=False):
            self._json(409, {"error": "another derivation is already running — wait for it to finish "
                                      "(the local model would split throughput between the two)"}); return
        # NDJSON stage stream; the 200 commits before the pipeline runs — later failures travel
        # IN-stream, NAMED. Nothing is persisted anywhere on any path (display/propose-only).
        try:
            self.send_response(200)
            self.send_header("Content-Type", "application/x-ndjson; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            try:
                entry, dropped = derive(text, meta, llm_url=self.server.llm_url, model=self.server.model,
                                        on_progress=lambda stage, **kw: self._emit({"stage": stage, **kw}))
            except DeriveError as ex:
                self._emit({"error": str(ex)}); return
            except (urllib.error.URLError, OSError) as ex:
                self._emit({"error": f"local model unreachable at {self.server.llm_url}: {ex}"}); return
            except (ValueError, KeyError, json.JSONDecodeError) as ex:
                self._emit({"error": f"model returned output that could not be parsed: {ex}"}); return
            self._emit({"done": {"entry": entry, "dropped": dropped,
                                 "counts": {"kept": len(entry["indicators"]), "dropped": len(dropped)}}})
        except (BrokenPipeError, ConnectionResetError):
            self.log_message("client disconnected mid-derive stream")  # nothing persisted by design
        finally:
            lock.release()

    def log_message(self, fmt, *a):
        sys.stderr.write("[serve_corpus] " + (fmt % a) + "\n")


# ---- selftest (offline: no socket, no model) ----------------------------------------------------
def selftest() -> int:
    caps, dss = _postures()
    assert len(caps) == 28 and len(dss) == 20, "taxonomy shape moved"
    assert DERIVE_SCHEMA["properties"]["indicators"]["items"]["properties"]["capability"]["enum"] == list(caps), \
        "capability enum must mirror the committed taxonomy ids (single authority)"
    assert DERIVE_SCHEMA["properties"]["indicators"]["items"]["properties"]["data_source"]["enum"] == list(dss), \
        "data_source enum must mirror the committed taxonomy ids"
    spec = build_spec()
    for needle in ("VERBATIM", "C1 ", "D1 ", "EXAMPLES", "12 to 240"):
        assert needle in spec, f"spec missing {needle!r}"

    # the deterministic downstream reproduces a committed record EXACTLY (the probe's invariant)
    md = (ROOT / "data" / "fintrac" / "fintrac-cannabis.md").read_text(encoding="utf-8")
    committed = json.loads(FEWSHOT_RECORD.read_text(encoding="utf-8"))
    ex = {"indicators": [{k: i[k] for k in ("section", "flag", "red_flag", "capability", "data_source")}
                         for i in committed["indicators"]]}
    record, problems = assemble(ex, md, "live-selftest")
    assert not problems, problems
    for got, want in zip(record["indicators"], committed["indicators"]):
        assert (got["status"], got["data"], got["build_rec"]) == \
               (want["status"], want["data"], want["build_rec"]), (got["id"], got, want)
    passing, failing, doc_level = split_by_gate(record, problems, md)
    assert not failing and not doc_level, (failing[:2], doc_level)
    assert len(passing) == len(committed["indicators"])

    # a tampered flag FAILS the gate and lands in `failing` with its violation text
    bad = json.loads(json.dumps(ex))
    bad["indicators"][0]["flag"] = "This sentence does not appear in the advisory at all."
    record_b, problems_b = assemble(bad, md, "live-selftest")
    _, failing_b, _ = split_by_gate(record_b, problems_b, md)
    assert any("IND-01" in v for f in failing_b for v in f["violations"]), failing_b
    # an unknown C code is a pre-gate problem, not a crash
    bad2 = json.loads(json.dumps(ex))
    bad2["indicators"][1]["capability"] = "C99"
    _, problems2 = assemble(bad2, md, "live-selftest")
    assert problems2 and "C99" in problems2[0], problems2

    # template_logic satisfies the gate's BUILD_NOW shape contract
    tl = template_logic("Funnel-account fan-in across unrelated third parties", list(caps.values())[0],
                        list(dss.values())[0])
    for k in ("signal_name", "class", "features", "logic", "window", "source", "route"):
        assert tl.get(k), k
    assert isinstance(tl["features"], list) and all(isinstance(x, str) and x for x in tl["features"])

    # SSE reassembly + the NAMED budget path (the Phase-43 transport contract)
    c, f, n = _consume_sse(iter([
        b'data: {"choices":[{"delta":{"content":"hi"},"finish_reason":null}]}',
        b'data: {"choices":[{"delta":{},"finish_reason":"length"}]}', b"data: [DONE]"]))
    assert (c, f, n) == ("hi", "length", 1), (c, f, n)
    assert MAX_GEN_TOKENS > 4096

    # a region-less document routes to a DOC-LEVEL violation (the named "not derivable" path)
    record_n, problems_n = assemble(ex, "Just some prose with no indicator section at all.", "live-x")
    _, _, doc_level_n = split_by_gate(record_n, problems_n, "Just some prose with no indicator section at all.")
    assert any("no red-flag region" in v for v in doc_level_n), doc_level_n

    # the FULL derive() loop OFFLINE (stubbed transport — the news replay-stub pattern): two
    # ungroundable flags force the RETRY (the T1-checkpoint feature); the retry fixes ONE and
    # omits the other → kept = fixed + originally-passing, dropped carries the honest
    # unreturned-correction note, and the stage sequence shows gated→retrying→regating.
    three = ex["indicators"][:3]
    bad_a = dict(three[0]); bad_a["flag"] = "This sentence appears nowhere in the advisory."
    bad_b = dict(three[1]); bad_b["flag"] = "Neither does this entirely invented sentence."
    calls, stages_seen = [], []
    def _stub(system, user, **kw):
        calls.append(user)
        if len(calls) == 1:
            return json.dumps({"indicators": [bad_a, bad_b, three[2]]})
        assert "REJECTED" in user and "violation" in user, "retry prompt must carry the gate's violations"
        return json.dumps({"indicators": [three[0]]})    # fixes bad_a only; bad_b's fix omitted
    _orig = globals()["call_llm"]
    globals()["call_llm"] = _stub
    try:
        entry, dropped = derive(md, {"title": "Stubbed OA"}, llm_url="http://offline-stub/v1/x",
                                model="stub", on_progress=lambda s, **kw: stages_seen.append(s))
    finally:
        globals()["call_llm"] = _orig
    assert len(calls) == 2, "the violation-guided retry must fire exactly once"
    assert len(entry["indicators"]) == 2, entry["indicators"]
    kept_flags = {i["flag"] for i in entry["indicators"]}
    assert three[0]["flag"] in kept_flags and three[2]["flag"] in kept_flags, kept_flags
    assert len(dropped) == 1 and "retry returned fewer" in dropped[0]["violations"][0], dropped
    for s in ("extracting", "gating", "gated", "retrying", "regating", "derived"):
        assert s in stages_seen, (s, stages_seen)
    assert entry["live"] is True and entry["id"].startswith("live-stubbed-oa"), entry["id"]
    leftover = derive_signals.check_record({"indicators": entry["indicators"]}, md)
    assert not leftover, leftover

    # the served page: placeholder gone, live config + the corpus payload inlined, doc complete
    cfg = live_config(argparse.Namespace(model=DEFAULT_MODEL, llm_url=DEFAULT_LLM_URL))
    page = render_page(cfg)
    assert build.CORPUS_PLACEHOLDER not in page
    assert '"live"' in page and '"derive": "/derive"' in page, "live config not inlined"
    assert '"advisories"' in page and '"taxonomy"' in page, "corpus payload not inlined"
    assert "liveInit" in page and "fetch(CORPUS.live.derive" in page, \
        "companion page missing the live branch (the build would strip it; the companion must NOT)"
    assert "liveProcBody" in page and "liveStageLabel" in page, \
        "companion page missing the processing-page/stage-label live code"
    assert page.rstrip().endswith("</html>"), "served page is not a complete HTML document"

    # parity guard: the companion's payload (minus `live`) must MATCH what build.render_corpus
    # inlines — the two assemble from the same loaders; drift here means the sequences diverged
    p = corpus_payload(cfg)
    offline = build.render_corpus(build.CORPUS_TEMPLATE.read_text(encoding="utf-8"))
    q = dict(p)
    q.pop("live")
    assert json.dumps(q, ensure_ascii=False, indent=2) in offline, \
        "companion corpus payload diverged from build.render_corpus"

    print(f"serve_corpus --selftest: PASS ({len(p['advisories'])} corpus docs; spec {len(spec):,} chars; "
          f"downstream exact on {len(committed['indicators'])} committed indicators; page {len(page):,} bytes)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Live companion for the M7 corpus explorer (dev/authoring-time only).")
    ap.add_argument("--port", type=int, default=DEFAULT_PORT)
    ap.add_argument("--llm-url", default=DEFAULT_LLM_URL)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--selftest", action="store_true", help="offline assertions (no socket, no model), exit")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    page = render_page(live_config(args))
    httpd = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    httpd.page = page
    httpd.llm_url = args.llm_url
    httpd.model = args.model
    print(f"[serve_corpus] live companion on http://localhost:{args.port}/  "
          f"(model={args.model} via {args.llm_url})")
    print("[serve_corpus] live-derived output is DISPLAY-ONLY — nothing is persisted; "
          "the offline dist/corpus/index.html remains the scripted fallback. Ctrl-C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[serve_corpus] stopped.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
