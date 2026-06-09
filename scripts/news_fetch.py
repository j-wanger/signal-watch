#!/usr/bin/env python3
"""URL acquisition for the live news companion (Phase 39) — COMPANION-ONLY, never on the ship path.

Turns a pasted URL into article text the live pipeline can extract from + ground against. The same
spine as everything else in this project: ACQUISITION PROPOSES, A DETERMINISTIC GATE DISPOSES —
whatever a fetch method returns must pass the scripted STANDARDIZER (format cleanup) and the
VERIFIER (article-shape checks) before it becomes a grounding surface; anything that fails is an
HONEST structured failure telling the analyst to paste the text instead. Never loosen the verifier
to make a URL pass.

The fetch LADDER (bot guards are expected in the wild — three methods, tried in order):
  1. urllib with browser-like headers   (stdlib; most gov/public pages)
  2. curl subprocess                    (different TLS/client fingerprint; passes some guards urllib trips)
  3. markitdown convert_uri             (markitdown fetches itself via requests — a third client)

DEPENDENCY POSTURE (the news_store/DuckDB pattern): import-time this module is STDLIB-ONLY;
`markitdown` (the HTML→markdown converter, the pdf_to_md.py authoring dep) is lazy-imported and
lives in the gitignored uv .venv. Without it URL mode degrades to an honest "run under the .venv
or paste the text" failure — the companion still serves, paste still works. build.py NEVER imports
this module.

    python3 scripts/news_fetch.py --selftest       # dep-free: pins standardizer + verifier + ladder order
    .venv/bin/python scripts/news_fetch.py <url>   # manual: acquire + verify, print the result
"""
import http.cookiejar
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request

MAX_BYTES = 3_000_000          # size cap per fetch — an article page, not an archive
TIMEOUT = 25                   # seconds per fetch method
BROWSER_HEADERS = {            # a realistic browser fingerprint — many sites 403 the default Python-urllib UA
    "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


# ── the fetch ladder ─────────────────────────────────────────────────────────────────────────────
_META_REFRESH = re.compile(r"""http-equiv=["']refresh["']\s+content=["'](\d+);\s*URL=\'?([^'">]+)""", re.I)
MAX_INTERSTITIAL = 16_384      # anti-bot interstitials are tiny; never refresh-follow a real-sized page


def _meta_refresh_target(data: bytes, url: str) -> tuple:
    """Anti-bot interstitial detection (seen live on justice.gov/Akamai): the FIRST response is a tiny
    page that sets a cookie and meta-refreshes to the real URL — a cookie-carrying second request gets
    the article. Returns (follow_url, wait_seconds) or (None, 0). Same-host only, one follow ever."""
    if len(data) > MAX_INTERSTITIAL:
        return None, 0
    m = _META_REFRESH.search(data.decode("utf-8", "replace"))
    if not m:
        return None, 0
    target = urllib.parse.urljoin(url, m.group(2).strip())
    if urllib.parse.urlsplit(target).netloc != urllib.parse.urlsplit(url).netloc:
        return None, 0  # never follow a cross-host refresh
    return target, min(int(m.group(1)), 6)


def fetch_urllib(url: str) -> bytes:
    """Rung 1: stdlib urllib with browser-like headers + a cookie jar, following ONE interstitial
    meta-refresh (the guard sets a cookie on request 1; request 2 carries it back)."""
    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))

    def get(u: str) -> bytes:
        with opener.open(urllib.request.Request(u, headers=BROWSER_HEADERS), timeout=TIMEOUT) as r:
            data = r.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            raise ValueError(f"response exceeds the {MAX_BYTES:,}-byte cap")
        return data

    data = get(url)
    target, wait = _meta_refresh_target(data, url)
    if target:
        time.sleep(wait)
        data = get(target)
    return data


def fetch_curl(url: str) -> bytes:
    """Rung 2: curl subprocess — a different TLS/client fingerprint passes some guards urllib trips.
    Same cookie-jar + one-interstitial-follow dance as rung 1."""
    with tempfile.TemporaryDirectory() as td:
        jar = os.path.join(td, "cookies.txt")

        def get(u: str) -> bytes:
            p = subprocess.run(
                ["curl", "-fsSL", "--max-time", str(TIMEOUT), "--max-filesize", str(MAX_BYTES),
                 "-A", BROWSER_HEADERS["User-Agent"], "-c", jar, "-b", jar, "--", u],
                capture_output=True, timeout=TIMEOUT + 10)
            if p.returncode != 0:
                raise RuntimeError(f"curl exit {p.returncode}: {p.stderr.decode('utf-8', 'replace').strip()[:200]}")
            if not p.stdout:
                raise RuntimeError("curl returned an empty body")
            return p.stdout

        data = get(url)
        target, wait = _meta_refresh_target(data, url)
        if target:
            time.sleep(wait)
            data = get(target)
    return data


def _markitdown():
    """Lazy import — markitdown is a .venv-only authoring dep (the news_store/DuckDB degrade pattern)."""
    try:
        from markitdown import MarkItDown
        return MarkItDown()
    except ImportError:
        return None


MARKITDOWN_HINT = ("URL mode needs markitdown (the HTML converter) — run the companion under the .venv "
                   "(.venv/bin/python scripts/serve_news.py), or paste the article text instead")


def html_to_md(data: bytes, url: str = "") -> tuple:
    """Convert fetched HTML bytes → (markdown, title) via markitdown (in-memory, no temp file)."""
    md = _markitdown()
    if md is None:
        raise RuntimeError(MARKITDOWN_HINT)
    result = md.convert_stream(io.BytesIO(data), file_extension=".html", url=url or None)
    return (getattr(result, "markdown", None) or result.text_content or ""), (getattr(result, "title", None) or "")


def fetch_markitdown(url: str) -> tuple:
    """Rung 3: markitdown fetches AND converts (its own requests client — a third fingerprint)."""
    md = _markitdown()
    if md is None:
        raise RuntimeError(MARKITDOWN_HINT)
    result = md.convert_uri(url)
    return (getattr(result, "markdown", None) or result.text_content or ""), (getattr(result, "title", None) or "")


# ── the scripted format STANDARDIZER (deterministic — no model, no network) ──────────────────────
_IMG_RE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
_LINK_RE = re.compile(r"\[([^\]]*)\]\(\s*[^)]*\)")
_BARE_URL_LINE = re.compile(r"\s*<?https?://\S+>?\s*$")
_FURNITURE = re.compile(r"[|·•\-–—_*\s\d.,:;>/\\]+")


def standardize(md: str) -> str:
    """Clean converted page markdown into a plain grounding surface: drop images, nav/link furniture
    and bare-URL lines, unwrap inline links to their text, collapse blank runs. Conservative + purely
    structural — it must never rewrite article prose (the text is the model input AND the grounding
    surface)."""
    s = md.replace("\r\n", "\n").replace("\r", "\n")
    s = _IMG_RE.sub("", s)
    out = []
    for line in s.split("\n"):
        stripped = line.strip()
        if stripped.startswith("#"):  # keep headings (often the title) — unwrap any link, keep the text
            out.append(_LINK_RE.sub(r"\1", stripped))
            continue
        n_links = len(_LINK_RE.findall(stripped))
        residue = _FURNITURE.sub("", _LINK_RE.sub("", stripped))
        if n_links and not residue:   # nav furniture: nothing but links + separators on the line
            continue
        line = _LINK_RE.sub(r"\1", line)
        if _BARE_URL_LINE.fullmatch(line):
            continue
        out.append(line.rstrip())
    s = "\n".join(out)
    s = re.sub(r"\n{3,}", "\n\n", s).strip()
    return s + "\n" if s else ""


# ── the article-shape VERIFIER (the gate — honest failure beats a polluted grounding surface) ────
GUARD_MARKERS = (
    "verify you are human", "are you a robot", "unusual traffic", "captcha",
    "enable javascript", "javascript is disabled", "javascript is not available",
    "checking your browser", "access denied", "request blocked",
    "subscribe to continue", "subscription required", "sign in to continue", "to continue reading",
)
MIN_CHARS = 600                # below this, no article body survived the conversion
GUARD_SCAN_CHARS = 2000        # guard/paywall walls are short; only marker-scan short results
MIN_SENTENCES = 3              # running prose, not a link farm / index page
MIN_PROSE_RATIO = 0.70         # letters+spaces share of the text


def verify_article(text: str) -> dict:
    """Deterministic article-shape checks on the STANDARDIZED text. Returns {ok, reason}."""
    t = (text or "").strip()
    low = t.lower()
    if len(t) < GUARD_SCAN_CHARS:
        for m in GUARD_MARKERS:
            if m in low:
                return {"ok": False, "reason": f"the page answered with a bot-guard/paywall wall ({m!r})"}
    if len(t) < MIN_CHARS:
        return {"ok": False, "reason": f"converted text too short to be an article ({len(t)} chars < {MIN_CHARS})"}
    sentences = re.findall(r"[A-Za-z][^.!?\n]{20,}[.!?]", t)
    if len(sentences) < MIN_SENTENCES:
        return {"ok": False, "reason": "no running prose found — this looks like an index/listing page, not an article"}
    prose = sum(1 for c in t if c.isalpha() or c.isspace())
    if prose / len(t) < MIN_PROSE_RATIO:
        return {"ok": False, "reason": "content is mostly non-prose (markup/tables/code survived conversion)"}
    return {"ok": True, "reason": ""}


# ── orchestration ────────────────────────────────────────────────────────────────────────────────
def acquire(url: str) -> dict:
    """Fetch (ladder) → convert → standardize → verify. Returns
      {ok: True,  text, title, method, attempts}            on success, or
      {ok: False, error, attempts}                          with every failed rung recorded.
    The verifier verdict is FINAL — a fetch that succeeds but fails article-shape is an honest
    failure (paste instead), never a loosened gate."""
    if not re.match(r"^https?://", (url or "").strip()):
        return {"ok": False, "error": "need an http(s):// URL", "attempts": []}
    url = url.strip()
    if _markitdown() is None:   # no converter → no rung can produce text; degrade before any network call
        return {"ok": False, "error": MARKITDOWN_HINT, "attempts": []}
    # Each rung runs the FULL pipeline and must PASS THE VERIFIER to win — a fetch that "succeeds" with
    # a guard page / empty conversion advances the ladder just like a connection error (caught live on
    # justice.gov: urllib gets bytes, conversion yields 0 chars — the next fingerprint may get the page).
    attempts = []
    rungs = (("urllib", lambda: html_to_md(fetch_urllib(url), url)),
             ("curl", lambda: html_to_md(fetch_curl(url), url)),
             ("markitdown", lambda: fetch_markitdown(url)))
    for name, fn in rungs:
        try:
            text_md, title = fn()
        except Exception as ex:  # noqa: BLE001 — each rung's failure is recorded, the ladder continues
            attempts.append({"method": name, "error": str(ex)[:200]})
            continue
        text = standardize(text_md)
        v = verify_article(text)
        if v["ok"]:
            return {"ok": True, "text": text, "title": (title or "").strip(), "method": name, "attempts": attempts}
        attempts.append({"method": name, "error": f"verifier: {v['reason']}"})
    return {"ok": False, "attempts": attempts,
            "error": "could not acquire an article from the URL (urllib → curl → markitdown each failed "
                     "or failed the article verifier) — paste the article text instead"}


# ── selftest (dep-free, no network — committed fixtures pin the gate) ────────────────────────────
def selftest() -> int:
    import pathlib
    fixdir = pathlib.Path(__file__).resolve().parent.parent / "tests" / "fixtures" / "news-fetch"

    # 1) the STANDARDIZER is pinned byte-exact against a committed golden (markitdown-converted page)
    raw = (fixdir / "article.raw.md").read_text(encoding="utf-8")
    golden = (fixdir / "article.golden.md").read_text(encoding="utf-8")
    got = standardize(raw)
    assert got == golden, "standardize() drifted from the committed golden (re-bless only if intentional)"
    assert "![" not in got and "](http" not in got, "images/link targets must not survive standardization"
    assert standardize(golden) == golden, "standardize() must be idempotent"

    # 2) the VERIFIER: a clean article passes; the failure modes each fail with their OWN reason
    assert verify_article(golden)["ok"], "the standardized article fixture must verify"
    bot = verify_article((fixdir / "botguard.md").read_text(encoding="utf-8"))
    assert not bot["ok"] and "bot-guard" in bot["reason"], bot
    farm = verify_article(standardize((fixdir / "linkfarm.md").read_text(encoding="utf-8")))
    assert not farm["ok"], "a link-farm/index page must fail the verifier"
    assert not verify_article("Too short.")["ok"]
    assert not verify_article("word " * 500)["ok"], "no sentences → no running prose"

    # 2.5) interstitial detection (the justice.gov/Akamai two-step): tiny same-host refresh → follow
    t, w = _meta_refresh_target(b'<meta http-equiv="refresh" content="5; URL=\'/real/page\'">', "https://ex.test/a")
    assert t == "https://ex.test/real/page" and w == 5, (t, w)
    t, _w = _meta_refresh_target(b'<meta http-equiv="refresh" content="0; URL=https://evil.test/x">', "https://ex.test/a")
    assert t is None, "a cross-host refresh must never be followed"
    t, _w = _meta_refresh_target(b"x" * (MAX_INTERSTITIAL + 1), "https://ex.test/a")
    assert t is None, "a real-sized page is not an interstitial"
    assert _meta_refresh_target(b"<html>no refresh</html>", "https://ex.test/a") == (None, 0)

    # 3) the LADDER order + honest failure (fetch methods stubbed — no network)
    g = globals()
    orig = {k: g[k] for k in ("fetch_urllib", "fetch_curl", "fetch_markitdown", "html_to_md", "_markitdown")}
    try:
        g["_markitdown"] = lambda: object()                      # converter "present" for ladder tests
        g["fetch_urllib"] = lambda u: (_ for _ in ()).throw(RuntimeError("403 (stub)"))
        g["fetch_curl"] = lambda u: b"<html>stub</html>"
        g["html_to_md"] = lambda data, url="": (raw, "Stub Title")
        r = acquire("https://example.test/a")
        assert r["ok"] and r["method"] == "curl" and r["text"] == golden, r
        assert [a["method"] for a in r["attempts"]] == ["urllib"], r["attempts"]

        g["fetch_curl"] = lambda u: (_ for _ in ()).throw(RuntimeError("blocked (stub)"))
        g["fetch_markitdown"] = lambda u: (raw, "Stub Title")    # rung 3 catches what rungs 1-2 can't
        r = acquire("https://example.test/b")
        assert r["ok"] and r["method"] == "markitdown", r

        g["fetch_markitdown"] = lambda u: (_ for _ in ()).throw(RuntimeError("also blocked (stub)"))
        r = acquire("https://example.test/c")
        assert not r["ok"] and len(r["attempts"]) == 3 and "paste the article text" in r["error"], r

        # the LOAD-BEARING ladder rule (caught live on justice.gov): a fetch that "succeeds" with a
        # guard page must ADVANCE the ladder — the verifier verdict is recorded as that rung's failure
        g["fetch_urllib"] = lambda u: b"<html>guard</html>"      # fetch OK but the page is a guard wall
        g["html_to_md"] = lambda data, url="": ("Checking your browser… verify you are human.", "")
        r = acquire("https://example.test/d")
        assert not r["ok"] and "paste the article text" in r["error"], r
        assert r["attempts"][0]["method"] == "urllib" and "verifier:" in r["attempts"][0]["error"], r["attempts"]
        assert [a["method"] for a in r["attempts"]] == ["urllib", "curl", "markitdown"], r["attempts"]

        g["_markitdown"] = lambda: None                          # no converter → honest degrade, no network
        r = acquire("https://example.test/e")
        assert not r["ok"] and "markitdown" in r["error"] and r["attempts"] == [], r
    finally:
        g.update(orig)
    assert not acquire("ftp://nope")["ok"] and not acquire("")["ok"]

    # 4) .venv-gated (the duckdb pattern): real markitdown converts the committed HTML end-to-end
    if _markitdown() is not None:
        html = (fixdir / "article.html").read_bytes()
        text_md, _title = html_to_md(html, "https://example.test/article")
        v = verify_article(standardize(text_md))
        assert v["ok"], f"real markitdown conversion of the committed HTML failed the gate: {v}"
        conv = "exercised (markitdown present)"
    else:
        conv = "SKIPPED (markitdown not installed — run under .venv)"

    print(f"news_fetch --selftest: PASS (standardizer golden-pinned + idempotent; verifier: article ok, "
          f"bot-guard/link-farm/short/no-prose fail honestly; ladder urllib→curl→markitdown ordered, "
          f"failures recorded, no-converter degrade; real conversion {conv})")
    return 0


def main() -> int:
    if "--selftest" in sys.argv[1:]:
        return selftest()
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    if not args:
        print(__doc__)
        return 1
    result = acquire(args[0])
    out = dict(result)
    if out.get("ok"):
        out["text"] = out["text"][:400] + ("…" if len(out["text"]) > 400 else "")
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
