#!/usr/bin/env python3
"""Live companion for the merge console (Phase 83 — the 5th agentic LIVE loop; dev/authoring-time ONLY).

This is NOT part of the ship artifact. The shippable `dist/merge/index.html` stays a single self-contained
offline file (the scripted demo) that makes ZERO model/fetch call. This companion adds the optional, isolated
"live mode" the agentification roadmap's Stage 1 calls for: it serves `merge.html` over http://localhost
(SAME-ORIGIN with the API — no CORS) with `MERGE.live` set, and a `/adjudicate` endpoint runs the merge
adjudicator (the StubAdjudicator offline, or the LiveAdjudicator against a local OpenAI-compatible model) to
PROPOSE a call beside the human gate. The agent's call is measured against the committed oracle elsewhere
(merge_adjudicator_quality_harness); here it is a live proposal the presenter sees next to the human's.

THE ORACLE FIREWALL (load-bearing): the /adjudicate handler strips the case to merge_adjudicator's evidence
surface (adjudicator_input) BEFORE the adjudicator sees it, and the response carries ONLY {call, rationale,
backend} — NEVER the oracle. The oracle reveal stays the page's existing post-disposition mechanism. propose
-> gate -> decide: the agent proposes; the human disposes; nothing is persisted.

Stdlib ONLY. Imports `build` (the merge payload loader + validator — committed data, never the agent layer),
`merge_adjudicator` (the adjudicators + the firewall), and `osint_tools` (the call_openai transport +
backend resolution). build.py NEVER imports THIS.

Usage:
    python3 scripts/serve_merge.py                 # http://localhost:8040, model at 127.0.0.1:8080
    python3 scripts/serve_merge.py --port 8041 --backend stub
    python3 scripts/serve_merge.py --selftest      # offline assertions (no socket, no model), exit
"""
import argparse
import json
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
ROOT = _HERE.parent

import build                # the merge payload loader + the boundary validator (committed data)
import merge_adjudicator as ma   # the adjudicators + the oracle-input firewall
import osint_tools as ot    # the call_openai transport + resolve_gather_backend

DEFAULT_PORT = 8040         # companions: news 8000 · corpus 8010 · chain 8020 · workbench 8030 · merge 8040


# ---- the served page (merge.html + the live config; the LIVE region is added in merge.html, T4) -----------
def live_config(args) -> dict:
    return {"adjudicate": "/adjudicate", "backend": args.backend}


def merge_payload(live_cfg: dict) -> dict:
    """The SAME __MERGE__ object build.render_merge inlines (load + boundary-validate the committed cases),
    PLUS the `live` config the offline build never carries. Validation runs on the committed data BEFORE the
    live key is added, so the firewall/vocab validator sees exactly what ships."""
    data = build.load_merge_cases()
    errors = build.validate_merge_cases(data)
    if errors:
        build.die("merge cases fail boundary validation:\n  - " + "\n  - ".join(errors))
    out = dict(data)
    out["live"] = live_cfg
    return out


def render_page(live_cfg: dict) -> str:
    """Inline the merge payload (with `live`) into merge.html. Unlike build.render_merge this does NOT strip
    the LIVE region and does NOT enforce the offline self-contained guard — the companion-served page is
    intentionally allowed to fetch its same-origin /adjudicate endpoint (the serve_corpus precedent)."""
    template = build.MERGE_TEMPLATE.read_text(encoding="utf-8")
    n = template.count(build.MERGE_PLACEHOLDER)
    if n != 1:
        build.die(f"expected exactly one {build.MERGE_PLACEHOLDER} placeholder in merge.html, found {n}")
    out = template.replace(build.MERGE_PLACEHOLDER, json.dumps(merge_payload(live_cfg), ensure_ascii=False, indent=2))
    if build.MERGE_PLACEHOLDER in out:
        build.die("merge placeholder survived substitution")
    return out


def case_index(payload: dict) -> dict:
    return {c["id"]: c for c in payload.get("cases", [])}


# ---- the adjudication (the firewall + the stub/live split + degrade-to-stub) ------------------------------
def adjudicate_case(case: dict, backend: str, env) -> dict:
    """Run the requested adjudicator over the case's EVIDENCE ONLY (the oracle firewall) and return the
    proposal. A live transport failure (no model) DEGRADES to the deterministic stub with a NAMED note — the
    presenter is never blocked, and a fabricated number is never produced."""
    res = ot.resolve_gather_backend(backend, env)        # {requested, effective, note}
    ev = ma.adjudicator_input(case)                      # the firewall strip — the oracle never enters
    ma.assert_no_oracle_leak([ev])                       # belt-and-braces: the schema-boundary guard
    if res["effective"] == "openai":
        try:
            out = ma.LiveAdjudicator(lambda m: ot.call_openai(m, env)).adjudicate(ev)
        except ot.GatherError as e:
            out = ma.StubAdjudicator().adjudicate(ev)
            res = {"requested": backend, "effective": "stub",
                   "note": f"no model reachable ({e}); used the deterministic stub"}
    else:
        out = ma.StubAdjudicator().adjudicate(ev)
    # the response carries ONLY the proposal + the backend resolution — NEVER the oracle truth.
    return {"call": out["call"], "rationale": out["rationale"], "backend": res}


# ---- HTTP (the serve_corpus handler conventions) ----------------------------------------------------------
class Handler(BaseHTTPRequestHandler):
    server_version = "SignalWatchMergeLive/0.1"

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
        if self.path.split("?", 1)[0] == "/adjudicate":
            self._adjudicate(); return
        self._json(404, {"error": f"not found: {self.path}"})

    def _adjudicate(self):
        try:
            length = int(self.headers.get("Content-Length") or 0)
            payload = json.loads(self.rfile.read(length) or b"{}")
        except (ValueError, json.JSONDecodeError):
            self._json(400, {"error": "invalid JSON body"}); return
        case_id = payload.get("case_id")
        case = self.server.cases.get(case_id)
        if not case:
            self._json(404, {"error": f"unknown case_id: {case_id!r}"}); return
        backend = payload.get("backend") or self.server.backend
        # SINGLE-FLIGHT (the Phase-43 lesson): a second concurrent live call would split the local model's
        # throughput — serialize the adjudications behind one lock.
        with self.server.adjudicate_lock:
            try:
                result = adjudicate_case(case, backend, self.server.env)
            except Exception as ex:  # noqa: BLE001 — never leak a stack to the browser; name the class
                self._json(500, {"error": f"adjudication failed ({ex.__class__.__name__})"}); return
        self._json(200, result)

    def log_message(self, fmt, *a):
        sys.stderr.write("[serve_merge] " + (fmt % a) + "\n")


# ---- selftest (offline: no socket, no model) --------------------------------------------------------------
def selftest() -> int:
    import os
    cfg = live_config(argparse.Namespace(backend="stub"))
    payload = merge_payload(cfg)
    assert payload.get("live") == {"adjudicate": "/adjudicate", "backend": "stub"}, "live config not set"
    assert len(payload["cases"]) == 66, f"expected 66 cases, got {len(payload.get('cases', []))}"

    # ── payload parity: the companion's payload (minus `live`) MATCHES what build.render_merge inlines ──
    page = render_page(cfg)
    assert build.MERGE_PLACEHOLDER not in page
    assert '"live"' in page and '"adjudicate": "/adjudicate"' in page, "live config not inlined"
    assert '"cases"' in page, "merge payload not inlined"
    assert page.rstrip().endswith("</html>"), "served page is not a complete HTML document"
    q = dict(payload)
    q.pop("live")
    offline = build.render_merge(build.MERGE_TEMPLATE.read_text(encoding="utf-8"))
    assert json.dumps(q, ensure_ascii=False, indent=2) in offline, \
        "companion merge payload diverged from build.render_merge"

    # ── the adjudicate handler: the oracle firewall holds + the stub proposes a valid call ──
    idx = case_index(payload)
    a_case = idx["sub-P-0000016-P-0000051"]
    out = adjudicate_case(a_case, "stub", os.environ)
    assert out["call"] in ma.VOCAB, out
    assert out["backend"]["effective"] == "stub"
    # the response carries NO truth field (the firewall translated to the wire)
    blob = json.dumps(out)
    for leak in ("oracle", "correct_adjudication", "same_entity", "klass"):
        assert leak not in blob, f"the adjudicate response leaked {leak!r} — the oracle must never reach the wire"
    # the stub echoes the spine verdict: this case is kept_distinct -> reject_as_shares
    assert out["call"] == "reject_as_shares", out

    # ── degrade-to-stub: a live backend with no reachable model falls back to the stub + a NAMED note ──
    _orig = ot.call_openai
    ot.call_openai = lambda *a, **k: (_ for _ in ()).throw(ot.GatherError("model transport failed (test)"))
    try:
        deg = adjudicate_case(a_case, "openai", {"OPENAI_BASE_URL": "http://127.0.0.1:8080/v1"})
    finally:
        ot.call_openai = _orig
    assert deg["backend"]["effective"] == "stub" and "no model reachable" in deg["backend"]["note"], deg
    assert deg["call"] in ma.VOCAB

    # ── the live path runs the agent through the firewall (a fake model, no network) ──
    _orig2 = ot.call_openai
    ot.call_openai = lambda m, env=None, **k: '{"call": "uphold_merge", "rationale": "shared exact email"}'
    try:
        live = adjudicate_case(a_case, "openai", {"OPENAI_BASE_URL": "http://127.0.0.1:8080/v1"})
    finally:
        ot.call_openai = _orig2
    assert live["call"] == "uphold_merge" and live["backend"]["effective"] == "openai", live

    print(f"serve_merge --selftest: PASS ({len(payload['cases'])} merge cases; page {len(page):,} bytes; "
          f"payload parity with build.render_merge; the oracle firewall holds on the wire; "
          f"stub/live/degrade paths exercised, no model)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Live companion for the merge console (dev/authoring-time only).")
    ap.add_argument("--port", type=int, default=DEFAULT_PORT)
    ap.add_argument("--backend", default="openai", choices=["stub", "openai"],
                    help="default adjudicator backend (the client may override per request)")
    ap.add_argument("--selftest", action="store_true", help="offline assertions (no socket, no model), exit")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    import os
    page = render_page(live_config(args))
    httpd = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    httpd.page = page
    httpd.cases = case_index(merge_payload(live_config(args)))
    httpd.backend = args.backend
    httpd.env = os.environ
    httpd.adjudicate_lock = threading.Lock()
    print(f"[serve_merge] live companion on http://localhost:{args.port}/  (default backend={args.backend})")
    print("[serve_merge] the agent's call is a DISPLAY-ONLY proposal beside the human gate — nothing is "
          "persisted; the offline dist/merge/index.html remains the scripted demo. Ctrl-C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[serve_merge] stopped.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
