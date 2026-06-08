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

import news_ground  # noqa: E402
import serve_news   # noqa: E402

ARTICLE_MD = (ROOT / "data" / "news" / "articles" / "ofac-tgr-group.md").read_text(encoding="utf-8")

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
    ],
}


def http_route_test() -> None:
    """Drive the real /extract route over HTTP with the model call STUBBED (no llama-cpp needed) — proves
    the full live loop: request parse -> call_llm (stubbed) -> parse -> build_record -> ground -> JSON."""
    orig = serve_news.call_llm
    serve_news.call_llm = lambda text, **kw: json.dumps(CANNED)  # stub the only model-dependent step
    httpd = serve_news.ThreadingHTTPServer(("127.0.0.1", 0), serve_news.Handler)
    httpd.llm_url, httpd.model, httpd.page = "stub://", "stub", "<html></html>"
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
            data = json.loads(r.read().decode("utf-8"))
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
    finally:
        httpd.shutdown()
        serve_news.call_llm = orig
    print("  http route: /extract 200 grounded (stubbed model) · empty-text 400 · dropped reported")


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
    assert sum(1 for d in dropped if d["kind"] == "red_flag") == 2

    # idempotent: re-grounding the assembled record drops nothing more
    _, again = news_ground.ground_record(rec, rec["article_text"])
    assert again == [], f"build_record output not idempotent under the gate: {again}"

    # parse_llm_json strips a <think> block and code fences, and tolerates surrounding prose
    assert serve_news.parse_llm_json('<think>reasoning here</think>\n```json\n{"a": 1}\n```') == {"a": 1}
    assert serve_news.parse_llm_json('Sure! {"b": 2} done') == {"b": 2}
    assert serve_news.parse_llm_json('{"c": 3}') == {"c": 3}

    http_route_test()

    print(f"news_live_test: PASS (kept {len(rec['entities'])} entities, {len(rec['red_flags'])} red flag; "
          f"dropped {len(dropped)} ungrounded; ids contiguous; idempotent; parse robust)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
