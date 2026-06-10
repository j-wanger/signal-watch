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
        assert stages == ["extracting", "grounding"], f"verify-off stages should be extracting→grounding: {stages}"
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
        assert stages == ["fetching", "converted", "extracting", "grounding"], stages
        conv = progress[1]
        assert conv["text"] == ARTICLE_MD and conv["method"] == "urllib", "converted event must carry the acquired text"
        assert data["record"]["source_url"] == "https://example.test/case", data["record"]["source_url"]
        assert [e["name"] for e in data["record"]["entities"]] == ["George Rossi", "Siam Expert Trading Company Limited"]

        # 2) pasted text WINS over a url (the trim + re-run recovery path) — no acquisition runs
        news_fetch.acquire = lambda url: (_ for _ in ()).throw(AssertionError("acquire must not be called"))
        progress, data = post_extract({"text": ARTICLE_MD, "url": "https://example.test/case"})
        assert [ev["stage"] for ev in progress] == ["extracting", "grounding"], progress

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
    finally:
        httpd.shutdown()
    print("  persistence-off: /watchlist book-only (persist=false) · /disposition 503 · /watchlist/prune 503")


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
                                                  on_progress=lambda stage, **kw: seen.append((stage, kw.get("i"), kw.get("n"))))
    finally:
        serve_news.verify_subject = orig
    assert [e["name"] for e in out["entities"]] == ["Acme Holdings"], out["entities"]
    assert out["entities"][0]["id"] == "E1", "survivors must be re-id'd contiguously"
    assert len(dropped) == 2 and all("second-pass" in d["reason"] for d in dropped), dropped
    assert seen == [("verifying", 1, 3), ("verifying", 2, 3), ("verifying", 3, 3)], seen
    # fail-open — an unreachable verifier returns KEEP (the AML-safe default), never drops a subject
    assert serve_news.verify_subject("Anyone", "person", "ctx", llm_url="http://127.0.0.1:9/x", model="stub") is True
    print("  verify-entities (2nd pass): drops non-subjects · keeps subjects · re-ids · fail-open=KEEP · progress i/N")


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
    http_route_test()
    url_route_test()           # Phase 39 — one-shot URL mode (acquisition stubbed)
    watchlist_disposition_route_test()
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
