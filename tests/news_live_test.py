#!/usr/bin/env python3
"""Dep-free test for the Phase 35 live extraction pipeline (runs with NO model).

Exercises serve_news.build_record + parse_llm_json over the COMMITTED OFAC article using a CANNED model
JSON that mixes REAL grounded content (guaranteed grounded — it's straight from the gate-passing derived
record) with PLANTED ungrounded content. Asserts the deterministic gate drops the ungrounded items, keeps
the grounded ones, assigns contiguous ids, matches the inlined article shape, and is idempotent. The model
call (call_llm) is never invoked — only the pure parse/assemble/ground path.

    python3 tests/news_live_test.py
"""
import json
import pathlib
import sys
import threading
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import news_fetch   # noqa: E402
import news_ground  # noqa: E402
import news_store   # noqa: E402
import serve_news   # noqa: E402

HAS_DUCKDB = news_store.duckdb is not None  # the watchlist/disposition store test is DuckDB-gated (runs under .venv)

ARTICLE_MD = (ROOT / "data" / "news" / "articles" / "ofac-tgr-group.md").read_text(encoding="utf-8")

# Phase 38 — recorded-fixture replay. tests/fixtures/news-live/<id>.qwen.json is REAL captured Qwen output;
# <id>.golden.json is its grounded+screened record. The meta supplied at capture is committed HERE (so the
# offline replay is self-contained — no dependency on the .dev-wiki/tmp capture helper).
FIXDIR = ROOT / "tests" / "fixtures" / "news-live"
_BASIS = "Public domain · 17 U.S.C. §105"
FIXTURE_META = {
    # the 4 committed-corpus calibration articles (article .md lives in data/news/articles/)
    "doj-mullings-romance-mule": {"source_org": "DOJ", "basis": _BASIS},
    "doj-goltsev-export-control": {"source_org": "DOJ", "basis": _BASIS},
    "doj-ravenell-attorney-ml": {"source_org": "DOJ", "basis": _BASIS},
    "ofac-tgr-group": {"source_org": "OFAC", "basis": _BASIS},
    # Phase 38 — the 3 promoted STRESS articles (harder: multi-defendant / mass-designation). NOT in the
    # shipped corpus (that would change dist/news); their article .md lives beside the fixture in FIXDIR.
    "doj-chinese-cmlo": {"source_org": "DOJ", "basis": _BASIS},
    "doj-transnational-fraud": {"source_org": "DOJ", "basis": _BASIS},
    "ofac-sinaloa-fentanyl": {"source_org": "OFAC", "basis": _BASIS},
}
LIVE_URL = "http://127.0.0.1:8080/v1/chat/completions"

# Canned "model output": real grounded items (from the gate-passing committed record) + planted ungrounded.
CANNED = {
    "title": "Treasury Targets Russian Illicit Finance Network",
    "typology": "sanctions-evasion",
    "entities": [
        # REAL — name raw-grounded, location + profession normalize-grounded (committed record passed the gate)
        {"name": "George Rossi", "type": "person",
         "location": "Ukrainian national", "profession": "founder of TGR Partners"},
        # REAL name, but a PLANTED ungrounded profession -> entity kept, profession stripped
        {"name": "Siam Expert Trading Company Limited", "type": "org",
         "profession": "intergalactic shipping magnate"},
        # PLANTED ungrounded entity -> dropped entirely
        {"name": "Imaginary Person Zzz", "type": "person"},
    ],
    "red_flags": [
        # REAL verbatim flag -> kept (grounded + distinct + bounded)
        {"flag": "providing an unregistered service to exchange cash and cryptocurrency",
         "red_flag": "Unregistered cash-to-crypto exchange service", "category": "Virtual assets"},
        # PLANTED ungrounded flag -> dropped
        {"flag": "this exact phrase does not occur anywhere in the source",
         "red_flag": "Fabricated mechanism", "category": "x"},
        # REAL verbatim flag but red_flag == flag (not distinct) -> dropped
        {"flag": "arrange for intermediaries to deliver and convert bulk cash into cryptocurrency",
         "red_flag": "arrange for intermediaries to deliver and convert bulk cash into cryptocurrency"},
        # Phase 40 — PLANTED exact duplicate of the first flag (same quote + same category, reworded
        # translation) -> dropped by the gate's dup-collapse; the FIRST survives
        {"flag": "providing an unregistered service to exchange cash and cryptocurrency",
         "red_flag": "Cash-crypto swaps without MSB registration", "category": "Virtual assets"},
    ],
}


def read_extract_stream(resp) -> tuple:
    """Phase 39: /extract answers an NDJSON stream of stage events ending in {"done": …} or {"error": …}.
    Parse the whole body into (progress_events, final) — the final dict is the old single-JSON payload."""
    lines = [json.loads(l) for l in resp.read().decode("utf-8").splitlines() if l.strip()]
    assert lines, "extract stream was empty"
    final = lines[-1]
    assert "done" in final or "error" in final, f"stream did not end in a result/error event: {final}"
    progress = lines[:-1]
    assert all("stage" in ev for ev in progress), f"non-stage event before the final payload: {progress}"
    return progress, (final.get("done") if "done" in final else final)


def http_route_test() -> None:
    """Drive the real /extract route over HTTP with the model call STUBBED (no llama-cpp needed) — proves
    the full live loop: request parse -> call_llm (stubbed) -> parse -> build_record -> ground -> the
    Phase-39 NDJSON progress stream (stage events strictly precede the final payload)."""
    orig = serve_news.call_llm
    serve_news.call_llm = lambda text, **kw: json.dumps(CANNED)  # stub the only model-dependent step
    httpd = serve_news.ThreadingHTTPServer(("127.0.0.1", 0), serve_news.Handler)
    httpd.llm_url, httpd.model, httpd.page = "stub://", "stub", "<html></html>"
    httpd.verify = False  # the deterministic route tests exercise plumbing; the neural verify is tested separately
    httpd.store, httpd.book = None, []  # Phase 36: this route runs persistence-OFF (scan_id None, /extract unchanged)
    port = httpd.server_address[1]
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    try:
        req = urllib.request.Request(
            f"http://127.0.0.1:{port}/extract",
            data=json.dumps({"text": ARTICLE_MD, "source_org": "OFAC"}).encode("utf-8"),
            headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=10) as r:
            assert r.status == 200, r.status
            assert r.headers.get("Content-Type", "").startswith("application/x-ndjson"), r.headers.get("Content-Type")
            progress, data = read_extract_stream(r)
        stages = [ev["stage"] for ev in progress]
        assert stages == ["extracting", "grounding", "grounded", "persisting"], f"verify-off stages should be extracting→grounding→grounded→persisting: {stages}"
        names = [e["name"] for e in data["record"]["entities"]]
        assert names == ["George Rossi", "Siam Expert Trading Company Limited"], names
        assert len(data["record"]["red_flags"]) == 1, data["record"]["red_flags"]
        assert isinstance(data.get("dropped"), list) and data["dropped"], "dropped list should report the ungrounded items"

        code = 0
        try:
            bad = urllib.request.Request(
                f"http://127.0.0.1:{port}/extract", data=b'{"text":"   "}',
                headers={"Content-Type": "application/json"}, method="POST")
            urllib.request.urlopen(bad, timeout=10)
        except urllib.error.HTTPError as he:
            code = he.code
        assert code == 400, f"empty text should return 400, got {code}"

        # Phase 39: a pipeline failure AFTER the stream opens travels IN-stream — still HTTP 200, the
        # final event is {"error": …} (the client reads events, not status codes).
        def _unreachable(text, **kw):
            raise urllib.error.URLError("connection refused (stub)")
        serve_news.call_llm = _unreachable
        with urllib.request.urlopen(req, timeout=10) as r:
            assert r.status == 200, "in-stream errors keep the committed 200"
            progress, final = read_extract_stream(r)
        assert [ev["stage"] for ev in progress] == ["extracting"], progress
        assert "error" in final and "unreachable" in final["error"], final
        serve_news.call_llm = lambda text, **kw: json.dumps(CANNED)
    finally:
        httpd.shutdown()
        serve_news.call_llm = orig
    print("  http route: /extract NDJSON stream (stages precede payload, stubbed model) · empty-text 400 "
          "· dropped reported · mid-stream failure → in-stream error event")


def url_route_test() -> None:
    """Phase 39 — ONE-SHOT URL mode over the real /extract route (model + acquisition both stubbed):
    {url} streams fetching → converted(text) BEFORE the pipeline stages, the converted text becomes the
    grounding surface (source_url stamped), pasted text WINS over a url, and a verifier failure travels
    in-stream as an honest error suggesting paste."""
    orig_llm, orig_acq = serve_news.call_llm, news_fetch.acquire
    serve_news.call_llm = lambda text, **kw: json.dumps(CANNED)
    news_fetch.acquire = lambda url: {"ok": True, "text": ARTICLE_MD, "title": "Fetched Title",
                                      "method": "urllib", "attempts": []}
    httpd = serve_news.ThreadingHTTPServer(("127.0.0.1", 0), serve_news.Handler)
    httpd.llm_url, httpd.model, httpd.page = "stub://", "stub", "<html></html>"
    httpd.verify = False
    httpd.store, httpd.book = None, []
    port = httpd.server_address[1]
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()

    def post_extract(obj):
        req = urllib.request.Request(f"http://127.0.0.1:{port}/extract", data=json.dumps(obj).encode("utf-8"),
                                     headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=10) as r:
            return read_extract_stream(r)

    try:
        # 1) url-only: fetching → converted (the EARLY text event) → extracting → grounding → done
        progress, data = post_extract({"url": "https://example.test/case"})
        stages = [ev["stage"] for ev in progress]
        assert stages == ["fetching", "converted", "extracting", "grounding", "grounded", "persisting"], stages
        conv = progress[1]
        assert conv["text"] == ARTICLE_MD and conv["method"] == "urllib", "converted event must carry the acquired text"
        assert data["record"]["source_url"] == "https://example.test/case", data["record"]["source_url"]
        assert [e["name"] for e in data["record"]["entities"]] == ["George Rossi", "Siam Expert Trading Company Limited"]

        # 2) pasted text WINS over a url (the trim + re-run recovery path) — no acquisition runs
        news_fetch.acquire = lambda url: (_ for _ in ()).throw(AssertionError("acquire must not be called"))
        progress, data = post_extract({"text": ARTICLE_MD, "url": "https://example.test/case"})
        assert [ev["stage"] for ev in progress] == ["extracting", "grounding", "grounded", "persisting"], progress

        # 3) verifier failure → in-stream honest error suggesting paste (still HTTP 200)
        news_fetch.acquire = lambda url: {"ok": False, "attempts": [{"method": "urllib", "error": "403"}],
                                          "error": "fetched, but the result failed the article verifier: "
                                                   "bot-guard — paste the article text instead"}
        progress, final = post_extract({"url": "https://example.test/walled"})
        assert [ev["stage"] for ev in progress] == ["fetching"], progress
        assert "error" in final and "paste the article text" in final["error"], final
        assert final.get("attempts"), "the failed rungs must be reported"
    finally:
        httpd.shutdown()
        serve_news.call_llm, news_fetch.acquire = orig_llm, orig_acq
    print("  url route: {url} streams fetching→converted(text)→stages→done · source_url stamped · "
          "text wins over url · verifier failure → in-stream paste suggestion")


def watchlist_disposition_route_test() -> None:
    """Phase 36: drive /extract → /watchlist → /disposition(escalate) → /watchlist over HTTP against a
    temp DuckDB store. Proves the escalated-only loop: a scan persists (scan_id echoed), the watchlist
    starts book-only, escalating an entity at the gate adds it (with provenance), a dismiss does not."""
    if not HAS_DUCKDB:
        print("  watchlist/disposition route: SKIP (duckdb not installed — run under .venv)")
        return
    book = [{"id": "bk-1", "name": "Globex Bank", "type": "org", "role": "counterparty",
             "country": "United States", "segment": "Trade finance"}]  # deliberately NOT containing George Rossi
    orig = serve_news.call_llm
    # Phase 41 — the canned output gains a subset-name entity ("Rossi", raw-grounded) that the screen
    # FOLDS into George Rossi as an alias, plus a main-subject pick: proves the alias rides the anchor
    # onto the escalated watchlist row, with the scan's source_type in the provenance.
    canned41 = {**CANNED,
                "entities": CANNED["entities"] + [{"name": "Rossi", "type": "person"}],
                "main_subjects": ["George Rossi"]}
    serve_news.call_llm = lambda text, **kw: json.dumps(canned41)
    store = news_store.NewsStore(":memory:")
    httpd = serve_news.ThreadingHTTPServer(("127.0.0.1", 0), serve_news.Handler)
    httpd.llm_url, httpd.model, httpd.page = "stub://", "stub", "<html></html>"
    httpd.verify = False  # the deterministic route tests exercise plumbing; the neural verify is tested separately
    httpd.store, httpd.book = store, book
    port = httpd.server_address[1]
    base = f"http://127.0.0.1:{port}"
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()

    def post(path, obj):
        req = urllib.request.Request(base + path, data=json.dumps(obj).encode("utf-8"),
                                     headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status, json.loads(r.read().decode("utf-8"))

    def get(path):
        with urllib.request.urlopen(base + path, timeout=10) as r:
            return r.status, json.loads(r.read().decode("utf-8"))

    try:
        req = urllib.request.Request(base + "/extract",
                                     data=json.dumps({"text": ARTICLE_MD, "source_org": "OFAC",
                                                      "source_type": "investigation-note"}).encode("utf-8"),
                                     headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=10) as r:
            progress, data = read_extract_stream(r)   # Phase 39: the persisted path streams stages too
        assert progress, "expected stage events before the persisted payload"
        scan_id = data.get("scan_id")
        assert scan_id and len(scan_id) == 32, f"persisted scan should echo a scan_id, got {scan_id!r}"
        # Phase 41 — the subset name folded into the parent as an alias (gate-side), audit-trailed
        e1 = data["record"]["entities"][0]
        assert e1["name"] == "George Rossi" and e1.get("aliases") == ["Rossi"], e1
        assert data["record"].get("main_subjects") == ["George Rossi"], data["record"].get("main_subjects")
        assert any(d.get("folded_into") == "George Rossi" for d in data["dropped"]), data["dropped"]

        _, wl0 = get("/watchlist")
        kinds0 = {r["kind"] for r in wl0["rows"]}
        assert wl0["persist"] is True, "watchlist should report persistence on"
        assert [r for r in wl0["rows"] if r["kind"] == "scanned"] == [], "no escalations yet — book-only"
        assert any(r["name"] == "Globex Bank" and r["kind"] == "book" for r in wl0["rows"]), kinds0

        # escalate E1 (George Rossi) at the gate -> joins the watchlist; dismiss E2 -> does not
        s, d = post("/disposition", {"scan_id": scan_id, "entity_id": "E1", "decision": "escalate"})
        assert s == 200 and d["updated"] == 1, d
        post("/disposition", {"scan_id": scan_id, "entity_id": "E2", "decision": "dismiss"})

        _, wl1 = get("/watchlist")
        scanned = [r for r in wl1["rows"] if r["kind"] == "scanned"]
        assert len(scanned) == 1 and scanned[0]["name"] == "George Rossi", scanned
        assert "escalated from" in scanned[0]["provenance"], scanned[0]["provenance"]
        # Phase 41 — the anchor's accumulated alias + the scan's source_type ride the watchlist row
        assert scanned[0].get("aliases") == ["Rossi"], scanned[0]
        assert "investigation-note" in scanned[0]["provenance"], scanned[0]["provenance"]
        assert all(r["name"] != "Siam Expert Trading Company Limited" or r["kind"] == "book"
                   for r in wl1["rows"]), "a dismissed entity must not appear as a scanned watchlist row"

        # a bad disposition target -> 404
        code = 0
        try:
            post("/disposition", {"scan_id": scan_id, "entity_id": "E99", "decision": "escalate"})
        except urllib.error.HTTPError as he:
            code = he.code
        assert code == 404, f"unknown entity should 404, got {code}"

        # Phase 38 — prune George Rossi from the watchlist BY NAME -> he leaves; the book is untouched
        s, d = post("/watchlist/prune", {"name": "George Rossi"})
        assert s == 200 and d["pruned"] == 1, d
        _, wl2 = get("/watchlist")
        assert [r for r in wl2["rows"] if r["kind"] == "scanned"] == [], "pruned entity must leave the watchlist"
        assert any(r["name"] == "Globex Bank" and r["kind"] == "book" for r in wl2["rows"]), "prune must not touch the book"
        code = 0
        try:
            post("/watchlist/prune", {"name": "Nobody On The List"})
        except urllib.error.HTTPError as he:
            code = he.code
        assert code == 404, f"pruning an unknown name should 404, got {code}"
    finally:
        httpd.shutdown()
        serve_news.call_llm = orig
        store.close()
    print("  watchlist/disposition route: /extract persists (scan_id) · /watchlist book→escalated · dismiss excluded · bad target 404 · prune removes by name")


def anchor_route_test() -> None:
    """Phase 42: GET /anchor?name= serves news_store.anchor_summary() — the accumulated identity the
    dossier renders. Two scans of the same article prove cross-scan ACCUMULATION (2 scan rows; the
    fold-alias lands one provenance'd row PER scan, non-destructive); unknown and empty-normalizing
    names 404 honestly (never a 500); a missing name param is a 400."""
    if not HAS_DUCKDB:
        print("  anchor route: SKIP (duckdb not installed — run under .venv)")
        return
    orig = serve_news.call_llm
    canned = {**CANNED, "entities": CANNED["entities"] + [{"name": "Rossi", "type": "person"}],
              "main_subjects": ["George Rossi"]}
    serve_news.call_llm = lambda text, **kw: json.dumps(canned)
    store = news_store.NewsStore(":memory:")
    httpd = serve_news.ThreadingHTTPServer(("127.0.0.1", 0), serve_news.Handler)
    httpd.llm_url, httpd.model, httpd.page = "stub://", "stub", "<html></html>"
    httpd.verify = False  # the deterministic route tests exercise plumbing; the neural verify is tested separately
    httpd.store, httpd.book = store, []
    port = httpd.server_address[1]
    base = f"http://127.0.0.1:{port}"
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    try:
        for _ in range(2):  # two scans of the SAME article -> the same anchors accumulate
            req = urllib.request.Request(base + "/extract",
                                         data=json.dumps({"text": ARTICLE_MD, "source_org": "OFAC",
                                                          "source_type": "gov-enforcement"}).encode("utf-8"),
                                         headers={"Content-Type": "application/json"}, method="POST")
            with urllib.request.urlopen(req, timeout=10) as r:
                read_extract_stream(r)
        quoted = urllib.parse.quote("George Rossi")
        with urllib.request.urlopen(base + "/anchor?name=" + quoted, timeout=10) as r:
            assert r.status == 200, r.status
            a = json.loads(r.read().decode("utf-8"))
        assert a["name"] == "George Rossi" and a["type"] == "person" and a["anchor_id"], a
        assert a["first_source_type"] == "gov-enforcement", a
        assert len(a["scans"]) == 2 and all(s["source_type"] == "gov-enforcement" for s in a["scans"]), \
            f"two scans must accumulate on ONE anchor: {a['scans']}"
        alias_rows = [p for p in a["properties"] if p["kind"] == "alias" and p["value"] == "Rossi"]
        assert len(alias_rows) == 2 and all(p["provenance"]["source_type"] for p in alias_rows), \
            "the fold-alias must land one provenance'd property row PER scan (non-destructive)"
        assert isinstance(a["relationships"], list), a
        # unknown name / empty-normalizing name -> honest 404 (never 500); missing name -> 400
        for q, want in (("?name=" + urllib.parse.quote("Nobody Anywhere"), 404),
                        ("?name=" + urllib.parse.quote("***"), 404),
                        ("", 400)):
            code = 0
            try:
                urllib.request.urlopen(base + "/anchor" + q, timeout=10)
            except urllib.error.HTTPError as he:
                code = he.code
            assert code == want, f"/anchor{q}: expected {want}, got {code}"
    finally:
        httpd.shutdown()
        serve_news.call_llm = orig
        store.close()
    print("  anchor route: 200 accumulated identity (2 scans · per-scan alias provenance) · 404 unknown/empty-norm · 400 missing name")


def disposition_persist_off_test() -> None:
    """Persistence OFF (store None): /watchlist serves the static book reconciled; /disposition returns 503.
    Runs WITHOUT duckdb — proves the graceful-degradation path."""
    book = [{"id": "bk-1", "name": "Globex Bank", "type": "org", "role": "counterparty", "country": "US"}]
    httpd = serve_news.ThreadingHTTPServer(("127.0.0.1", 0), serve_news.Handler)
    httpd.llm_url, httpd.model, httpd.page = "stub://", "stub", "<html></html>"
    httpd.verify = False  # the deterministic route tests exercise plumbing; the neural verify is tested separately
    httpd.store, httpd.book = None, book
    port = httpd.server_address[1]
    base = f"http://127.0.0.1:{port}"
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    try:
        with urllib.request.urlopen(base + "/watchlist", timeout=10) as r:
            wl = json.loads(r.read().decode("utf-8"))
        assert wl["persist"] is False and len(wl["rows"]) == 1 and wl["rows"][0]["kind"] == "book", wl
        code = 0
        try:
            req = urllib.request.Request(base + "/disposition", data=b'{"scan_id":"x","entity_id":"E1","decision":"escalate"}',
                                         headers={"Content-Type": "application/json"}, method="POST")
            urllib.request.urlopen(req, timeout=10)
        except urllib.error.HTTPError as he:
            code = he.code
        assert code == 503, f"disposition with persistence off should 503, got {code}"
        code = 0
        try:
            req = urllib.request.Request(base + "/watchlist/prune", data=b'{"name":"X"}',
                                         headers={"Content-Type": "application/json"}, method="POST")
            urllib.request.urlopen(req, timeout=10)
        except urllib.error.HTTPError as he:
            code = he.code
        assert code == 503, f"prune with persistence off should 503, got {code}"
        code = 0
        try:  # Phase 42 — the dossier route degrades honestly too (503, never a 500)
            urllib.request.urlopen(base + "/anchor?name=Globex%20Bank", timeout=10)
        except urllib.error.HTTPError as he:
            code = he.code
        assert code == 503, f"/anchor with persistence off should 503, got {code}"
    finally:
        httpd.shutdown()
    print("  persistence-off: /watchlist book-only (persist=false) · /disposition 503 · /watchlist/prune 503 · /anchor 503")


def fixture_replay_test() -> None:
    """OFFLINE replay (NO model): each committed RAW Qwen output (<id>.qwen.json) → parse_llm_json →
    build_record → ground+screen MUST equal the committed <id>.golden.json. Pins the REAL model's output
    contract — incl. the ungrounded-elision DROP and the Phase-38 entity-precision filter — deterministically."""
    fixtures = sorted(FIXDIR.glob("*.qwen.json"))
    assert fixtures, f"no captured fixtures under {FIXDIR}"
    ids = {p.name[: -len(".qwen.json")] for p in fixtures}
    committed = {p.stem for p in (ROOT / "data" / "news" / "articles").glob("*.md")}
    assert committed <= ids, f"missing replay fixtures for committed articles: {committed - ids}"
    total_drops = 0
    for p in fixtures:
        aid = p.name[: -len(".qwen.json")]
        # Phase 40: a fixture may carry a prompt-variant tag (e.g. <id>.ph40.qwen.json = the same article
        # re-captured under the Phase-40 checklist prompt). The variant shares the BASE article + meta;
        # only the golden pairing uses the full tagged name.
        base = aid.rsplit(".", 1)[0] if "." in aid else aid
        # Phase 41 — the PRIVACY allowlist CHECK (boundary by check, not convention): every fixture's
        # base id must be in the committed US-federal FIXTURE_META registry. A private/commercial
        # capture can NEVER be promoted by habit — promotion requires a deliberate registry edit.
        assert base in FIXTURE_META, \
            f"fixture {p.name}: base id {base!r} is NOT in the committed US-federal allowlist (FIXTURE_META)"
        raw = p.read_text(encoding="utf-8")
        # the article lives beside the fixture (promoted stress articles) or in the shipped corpus
        local = FIXDIR / f"{base}.article.md"
        art = (local if local.exists() else ROOT / "data" / "news" / "articles" / f"{base}.md").read_text(encoding="utf-8")
        rec, dropped = serve_news.build_record(serve_news.parse_llm_json(raw), art, FIXTURE_META.get(base))
        golden = json.loads((FIXDIR / f"{aid}.golden.json").read_text(encoding="utf-8"))
        assert rec == golden, f"replay mismatch for {aid} (re-capture if build_record changed intentionally)"
        for i, e in enumerate(rec["entities"], 1):
            assert e["id"] == f"E{i}" and e["name"] in rec["article_text"], f"{aid} entity {e}"
        for i, f in enumerate(rec["red_flags"], 1):
            assert f["id"] == f"R{i}" and f["flag"] in rec["article_text"], f"{aid} flag {f}"
        total_drops += len(dropped)
    # the captured corpus must carry the real-model messiness (ungrounded flags + over-extracted entities)
    assert total_drops > 0, "expected ungrounded/noise drops across the captured fixtures"
    print(f"  fixture replay: {len(fixtures)} real-Qwen outputs → parse→build→ground→screen == committed goldens "
          f"({total_drops} ungrounded/noise drops reproduced, no model invoked)")


def live_smoke_test() -> None:
    """OPT-IN (`--live` only): hit the real local model at 127.0.0.1:8080 and assert the live backend still
    extracts + grounds. OFF by default — never hit by the standard offline run (the model/.venv-gated pattern)."""
    art = (ROOT / "data" / "news" / "articles" / "doj-mullings-romance-mule.md").read_text(encoding="utf-8")
    rec, dropped = serve_news.extract(art, {"source_org": "DOJ"}, llm_url=LIVE_URL, model="qwen")
    assert rec["entities"] and rec["red_flags"], "live model returned nothing groundable"
    print(f"  --live smoke: real model @8080 → {len(rec['entities'])} entities, {len(rec['red_flags'])} flags grounded "
          f"(incl. the keep-biased second-pass entity verify)")


def verify_entities_test() -> None:
    """Phase 38 — the keep-biased second pass. With verify_subject STUBBED (no model), verify_entities drops
    the NON-subjects, keeps subjects, and re-ids E1.. contiguously. Also asserts the load-bearing fail-OPEN:
    an unreachable verifier KEEPS (never drops a subject on error)."""
    art = "# T\n\nAcme Holdings laundered funds. Judge Jane Doe presided. The U.S. District Court ruled."
    rec = {"entities": [
        {"id": "E1", "name": "Acme Holdings", "type": "org"},
        {"id": "E2", "name": "U.S. District Court", "type": "org"},
        {"id": "E3", "name": "Jane Doe", "type": "person"},
    ], "red_flags": []}
    orig = serve_news.verify_subject
    serve_news.verify_subject = lambda name, etype, ctx, **kw: name == "Acme Holdings"  # only the subject is kept
    seen = []  # Phase 39: the per-entity verify loop is where progress lives — record the callback
    try:
        out, dropped = serve_news.verify_entities(rec, art, llm_url="stub://", model="stub",
                                                  on_progress=lambda stage, **kw: seen.append((stage, kw)))
    finally:
        serve_news.verify_subject = orig
    assert [e["name"] for e in out["entities"]] == ["Acme Holdings"], out["entities"]
    assert out["entities"][0]["id"] == "E1", "survivors must be re-id'd contiguously"
    assert len(dropped) == 2 and all("second-pass" in d["reason"] for d in dropped), dropped
    # Phase 43 — each "verifying i/N" is followed by a per-entity VERDICT event (chip refinement)
    assert seen == [
        ("verifying", {"i": 1, "n": 3, "name": "Acme Holdings"}),
        ("verified", {"name": "Acme Holdings", "kept": True}),
        ("verifying", {"i": 2, "n": 3, "name": "U.S. District Court"}),
        ("verified", {"name": "U.S. District Court", "kept": False}),
        ("verifying", {"i": 3, "n": 3, "name": "Jane Doe"}),
        ("verified", {"name": "Jane Doe", "kept": False}),
    ], seen
    # fail-open — an unreachable verifier returns KEEP (the AML-safe default), never drops a subject
    assert serve_news.verify_subject("Anyone", "person", "ctx", llm_url="http://127.0.0.1:9/x", model="stub") is True
    print("  verify-entities (2nd pass): drops non-subjects · keeps subjects · re-ids · fail-open=KEEP · progress i/N")


def _sse_lines(pieces, finish="stop"):
    """Synthetic llama-cpp SSE chat stream (byte lines), one content delta per piece."""
    lines = [("data: " + json.dumps({"choices": [{"delta": {"content": p}, "finish_reason": None}]})).encode("utf-8")
             for p in pieces]
    lines += [b"", b": keep-alive comment",  # noise the parser must skip
              ("data: " + json.dumps({"choices": [{"delta": {}, "finish_reason": finish}]})).encode("utf-8"),
              b"data: [DONE]"]
    return lines


class _FakeStreamResp:
    """Stands in for urlopen()'s response: context manager + line-iterable (what _consume_sse reads)."""
    def __init__(self, lines):
        self._lines = lines

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def __iter__(self):
        return iter(self._lines)


def streaming_transport_test() -> None:
    """Phase 43 — the streaming transport. call_llm streams (idle-gap timeout, not a whole-response
    deadline), reads finish_reason ("length" → a NAMED ExtractError, never a disguised parse error),
    fires token-count progress, and keeps the fixture stub seam (same name / kwargs-compatible /
    full-text return). Progress events carry COUNTS ONLY — never input content (the privacy rule)."""
    # 1) _consume_sse: accumulation, finish_reason, token cadence (~every 64), noise tolerance
    calls = []
    content, finish, n = serve_news._consume_sse(_sse_lines(["a"] * 130), on_tokens=calls.append)
    assert (content, finish, n) == ("a" * 130, "stop", 130), (len(content), finish, n)
    assert calls == [64, 128], calls

    # 2) call_llm over a FAKE streamed response: full-text return, stream:true + the raised
    #    generation budget in the request body, idle-gap timeout passed to urlopen, token progress
    sentinel = "PH43-PRIVATE-NOTE-SENTINEL-XYZZY"
    pieces = [json.dumps(CANNED)[i:i + 7] for i in range(0, len(json.dumps(CANNED)), 7)]
    captured = {}

    def fake_urlopen(req, timeout=None):
        captured["body"] = json.loads(req.data.decode("utf-8"))
        captured["timeout"] = timeout
        return _FakeStreamResp(_sse_lines(pieces))

    orig = serve_news.urllib.request.urlopen
    serve_news.urllib.request.urlopen = fake_urlopen
    events = []
    try:
        out = serve_news.call_llm("body " + sentinel, llm_url="stub://", model="qwen",
                                  on_progress=lambda **kw: events.append(kw))
        assert json.loads(out) == CANNED, "streamed content must reassemble to the full text"
        assert captured["body"]["stream"] is True, "transport must request a stream"
        assert captured["body"]["max_tokens"] == serve_news.MAX_GEN_TOKENS, captured["body"]["max_tokens"]
        assert captured["timeout"] is not None, "idle-gap socket timeout must be set"
        assert events and all(set(e) == {"tokens"} and isinstance(e["tokens"], int) for e in events), events

        # 3) finish_reason="length" → ExtractError NAMING the budget (distinct from a parse failure)
        serve_news.urllib.request.urlopen = \
            lambda req, timeout=None: _FakeStreamResp(_sse_lines(['{"trunca'], finish="length"))
        try:
            serve_news.call_llm("x", llm_url="stub://", model="qwen")
            raise AssertionError("finish_reason=length must raise ExtractError")
        except serve_news.ExtractError as ex:
            assert "output budget exhausted" in str(ex) and str(serve_news.MAX_GEN_TOKENS) in str(ex), ex

        # 3b) a mid-stream stall (the idle-gap deadline) is NAMED — never disguised as "unreachable"
        class _Stall:
            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

            def __iter__(self):
                raise TimeoutError("read timed out")

        serve_news.urllib.request.urlopen = lambda req, timeout=None: _Stall()
        try:
            serve_news.call_llm("x", llm_url="stub://", model="qwen")
            raise AssertionError("a stalled stream must raise ExtractError")
        except serve_news.ExtractError as ex:
            assert "model stalled" in str(ex) and "idle-gap" in str(ex), ex

        # 4) privacy: the full pipeline's progress events never carry input content (counts only)
        serve_news.urllib.request.urlopen = \
            lambda req, timeout=None: _FakeStreamResp(_sse_lines(pieces))
        stages = []
        rec, _ = serve_news.extract(ARTICLE_MD + "\n" + sentinel, {"source_org": "OFAC"},
                                    llm_url="stub://", model="qwen", verify=False,
                                    on_progress=lambda stage, **kw: stages.append({"stage": stage, **kw}))
        assert rec["entities"], "pipeline should still ground the canned record"
        assert sentinel not in json.dumps(stages), f"progress events leaked input content: {stages}"
        token_evs = [s for s in stages if "tokens" in s]
        assert token_evs and all(s["stage"] == "extracting" for s in token_evs), stages
    finally:
        serve_news.urllib.request.urlopen = orig
    print("  streaming transport: SSE reassembly · token cadence 64 · stream:true + "
          f"max_tokens={serve_news.MAX_GEN_TOKENS} · ExtractError(length) named · events content-free")


def size_and_concurrency_test() -> None:
    """Phase 43 — the T1-earned size/complexity handling. (1) preflight_size: an over-context input
    raises a NAMED ExtractError (silent truncation would pass the grounding gate — the gate can't
    catch what the model never saw) and fails OPEN when the server can't answer. (2) the route emits
    the refusal IN-stream WITHOUT ever invoking the model (stub-call-count 0). (3) /extract is
    SINGLE-FLIGHT: a second concurrent request gets an honest 409 (slots=4 means a retry would run
    BESIDE the ghost job, splitting throughput). (4, DuckDB-gated) a client disconnect before done
    writes NOTHING to the store (the 'persisting' probe emit precedes append_scan)."""
    import socket
    import time

    # (1a) over-context → ExtractError naming the overflow + the --ctx-size remedy
    def fake_urlopen_small_ctx(req, timeout=None):
        url = req if isinstance(req, str) else req.full_url
        if url.endswith("/props"):
            return _FakeBody(json.dumps({"default_generation_settings": {"n_ctx": 2048}}))
        if url.endswith("/tokenize"):
            return _FakeBody(json.dumps({"tokens": list(range(1500))}))
        raise AssertionError(f"unexpected url {url}")

    orig_open = serve_news.urllib.request.urlopen
    serve_news.urllib.request.urlopen = fake_urlopen_small_ctx
    try:
        try:
            serve_news.preflight_size("x" * 100, "http://stub/v1/chat/completions")
            raise AssertionError("over-context input must raise ExtractError")
        except serve_news.ExtractError as ex:
            assert "input too large" in str(ex) and "--ctx-size" in str(ex) and "n_ctx=2048" in str(ex), ex
    finally:
        serve_news.urllib.request.urlopen = orig_open
    # (1b) fail-open: an unreachable probe endpoint never blocks the pipeline
    serve_news.preflight_size("x", "http://127.0.0.1:9/v1/chat/completions")

    # (2) route-level: the refusal travels IN-stream, and the model is NEVER called
    calls = []
    orig_llm, orig_pf = serve_news.call_llm, serve_news.preflight_size
    serve_news.call_llm = lambda text, **kw: calls.append(1) or json.dumps(CANNED)
    serve_news.preflight_size = lambda text, llm_url, timeout=10: (_ for _ in ()).throw(
        serve_news.ExtractError("input too large for the model's context: stubbed"))
    httpd = serve_news.ThreadingHTTPServer(("127.0.0.1", 0), serve_news.Handler)
    httpd.llm_url, httpd.model, httpd.page = "stub://", "stub", "<html></html>"
    httpd.verify, httpd.store, httpd.book = False, None, []
    port = httpd.server_address[1]
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    try:
        req = urllib.request.Request(f"http://127.0.0.1:{port}/extract",
                                     data=json.dumps({"text": ARTICLE_MD}).encode("utf-8"),
                                     headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=10) as r:
            _, final = read_extract_stream(r)
        assert "input too large" in final.get("error", ""), final
        assert calls == [], "the refusal must happen BEFORE any model call"
    finally:
        serve_news.preflight_size = orig_pf
        serve_news.call_llm = orig_llm
        httpd.shutdown()

    # (3) single-flight: while one extraction runs, a second gets an honest 409 busy.
    # Stubs restore in the trailing finally — a failed assertion must not leak slow_llm
    # into the later route tests.
    gate_open = threading.Event()
    started = threading.Event()

    def slow_llm(text, **kw):
        started.set()
        assert gate_open.wait(10), "test gate never opened"
        calls.append(1)
        return json.dumps(CANNED)

    serve_news.call_llm = slow_llm
    httpd2 = serve_news.ThreadingHTTPServer(("127.0.0.1", 0), serve_news.Handler)
    httpd2.llm_url, httpd2.model, httpd2.page = "stub://", "stub", "<html></html>"
    httpd2.verify, httpd2.store, httpd2.book = False, None, []
    port2 = httpd2.server_address[1]
    threading.Thread(target=httpd2.serve_forever, daemon=True).start()
    results = {}

    def first():
        req = urllib.request.Request(f"http://127.0.0.1:{port2}/extract",
                                     data=json.dumps({"text": ARTICLE_MD}).encode("utf-8"),
                                     headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=30) as r:
            results["first"] = read_extract_stream(r)[1]

    try:
        t1 = threading.Thread(target=first, daemon=True)
        t1.start()
        assert started.wait(10), "first extraction never reached the model stub"
        code = 0
        try:
            req2 = urllib.request.Request(f"http://127.0.0.1:{port2}/extract",
                                          data=json.dumps({"text": "short text"}).encode("utf-8"),
                                          headers={"Content-Type": "application/json"}, method="POST")
            urllib.request.urlopen(req2, timeout=10)
        except urllib.error.HTTPError as he:
            code = he.code
            busy = json.loads(he.read().decode("utf-8"))
            assert "another extraction" in busy.get("error", ""), busy
        assert code == 409, f"concurrent /extract should answer 409 busy, got {code}"
        gate_open.set()
        t1.join(30)
        assert results.get("first", {}).get("record"), "the first extraction must complete after the busy answer"
        assert calls == [1], "exactly ONE model call across both requests (the second never ran)"
    finally:
        serve_news.call_llm = orig_llm
        httpd2.shutdown()

    # (4) disconnect before done → NOTHING in the store (DuckDB-gated)
    disc = "store untouched on mid-stream disconnect: SKIP (duckdb not installed)"
    if HAS_DUCKDB:
        serve_news.call_llm = lambda text, **kw: time.sleep(0.8) or json.dumps(CANNED)
        store = news_store.NewsStore(":memory:")
        httpd3 = serve_news.ThreadingHTTPServer(("127.0.0.1", 0), serve_news.Handler)
        httpd3.llm_url, httpd3.model, httpd3.page = "stub://", "stub", "<html></html>"
        httpd3.verify, httpd3.store, httpd3.book = False, store, []
        port3 = httpd3.server_address[1]
        threading.Thread(target=httpd3.serve_forever, daemon=True).start()
        try:
            body = json.dumps({"text": ARTICLE_MD, "source_type": "investigation-note"}).encode("utf-8")
            s = socket.create_connection(("127.0.0.1", port3), timeout=10)
            s.sendall(b"POST /extract HTTP/1.1\r\nHost: t\r\nContent-Type: application/json\r\n"
                      + f"Content-Length: {len(body)}\r\n\r\n".encode("ascii") + body)
            s.recv(64)   # the response has started → the pipeline is running
            s.close()    # …and the analyst walks away mid-extract
            time.sleep(2.5)  # let the server hit the post-disconnect emits (grounding/grounded/persisting)
            n_scans = store.con.execute("SELECT count(*) FROM scans").fetchone()[0]
            assert n_scans == 0, f"a disconnected scan must never persist (found {n_scans} scans)"
            disc = "store untouched on mid-stream disconnect (persisting probe precedes append_scan)"
        finally:
            serve_news.call_llm = orig_llm
            httpd3.shutdown()
    serve_news.call_llm = orig_llm
    print(f"  size+concurrency: over-context → named in-stream refusal (0 model calls) · fail-open probe "
          f"· concurrent /extract → 409 busy · {disc}")


class _FakeBody:
    """urlopen()-shaped stub: context manager + .read()."""
    def __init__(self, text):
        self._b = text.encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def read(self):
        return self._b


def main() -> int:
    rec, dropped = serve_news.build_record(CANNED, ARTICLE_MD, {"source_org": "OFAC", "basis": "Public domain · 17 U.S.C. §105"})

    # shape matches the inlined article shape
    for k in ("id", "title", "article_text", "entities", "red_flags"):
        assert k in rec, f"missing key {k}"
    assert rec["article_text"] and "# " not in rec["article_text"].splitlines()[0], "article_text not body-normalized"

    # entities: ungrounded entity dropped; grounded ones kept; ungrounded attribute stripped
    names = [e["name"] for e in rec["entities"]]
    assert names == ["George Rossi", "Siam Expert Trading Company Limited"], names
    assert rec["entities"][0]["id"] == "E1" and rec["entities"][1]["id"] == "E2", "ids not contiguous"
    assert rec["entities"][0].get("location") == "Ukrainian national", "grounded attribute should survive"
    assert rec["entities"][0].get("profession") == "founder of TGR Partners", "grounded profession should survive"
    assert "profession" not in rec["entities"][1], "ungrounded profession should be stripped"

    # red_flags: only the grounded + distinct + bounded one survives
    assert len(rec["red_flags"]) == 1, rec["red_flags"]
    assert rec["red_flags"][0]["id"] == "R1"
    assert rec["red_flags"][0]["red_flag"] == "Unregistered cash-to-crypto exchange service"

    # every survivor is a RAW substring of the article body (so the runtime highlighter will match it)
    for e in rec["entities"]:
        assert e["name"] in rec["article_text"], f"entity not raw-grounded: {e['name']}"
    for f in rec["red_flags"]:
        assert f["flag"] in rec["article_text"], f"flag not raw-grounded: {f['flag']}"

    # the planted ungrounded items are gone
    assert "Imaginary Person Zzz" not in names
    assert all("does not occur" not in f["flag"] for f in rec["red_flags"])

    # something was actually dropped (the gate did work)
    assert any(d["reason"].startswith("name not raw-grounded") for d in dropped)
    assert any(d["reason"] == "attribute not grounded" for d in dropped)
    assert sum(1 for d in dropped if d["kind"] == "red_flag") == 3
    # Phase 40: the planted same-quote+category duplicate is collapsed (first survives)
    assert any(d["reason"] == "duplicate flag (same quote + category)" for d in dropped), dropped

    # idempotent: re-grounding the assembled record drops nothing more
    _, again = news_ground.ground_record(rec, rec["article_text"])
    assert again == [], f"build_record output not idempotent under the gate: {again}"

    # parse_llm_json strips a <think> block and code fences, and tolerates surrounding prose
    assert serve_news.parse_llm_json('<think>reasoning here</think>\n```json\n{"a": 1}\n```') == {"a": 1}
    assert serve_news.parse_llm_json('Sure! {"b": 2} done') == {"b": 2}
    assert serve_news.parse_llm_json('{"c": 3}') == {"c": 3}

    fixture_replay_test()      # Phase 38 — offline replay of REAL captured Qwen output (no model)
    verify_entities_test()     # Phase 38 — the keep-biased second pass (model stubbed)
    streaming_transport_test() # Phase 43 — streaming call_llm (idle-gap, finish_reason, content-free events)
    size_and_concurrency_test()  # Phase 43 — pre-flight refusal · single-flight 409 · disconnect≠persist
    http_route_test()
    url_route_test()           # Phase 39 — one-shot URL mode (acquisition stubbed)
    watchlist_disposition_route_test()
    anchor_route_test()        # Phase 42 — the dossier read route (accumulated identity)
    disposition_persist_off_test()

    if "--live" in sys.argv:   # opt-in only — the default run never touches 127.0.0.1:8080
        live_smoke_test()

    print(f"news_live_test: PASS (kept {len(rec['entities'])} entities, {len(rec['red_flags'])} red flag; "
          f"dropped {len(dropped)} ungrounded; ids contiguous; idempotent; parse robust; "
          f"fixture-replay locked; watchlist loop {'exercised' if HAS_DUCKDB else 'SKIPPED (no duckdb)'}; "
          f"live-smoke {'RAN' if '--live' in sys.argv else 'off (pass --live to hit 8080)'})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
