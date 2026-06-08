#!/usr/bin/env python3
"""DuckDB persistence + the escalated-only feedback watchlist for the M8 live companion (Phase 36).

Companion/authoring-time ONLY — NOT part of the ship artifact. build.py NEVER imports this module
(the no-authoring/no-store-layer invariant: the deterministic build/grounding layer stays free of the
LLM and now the store). DuckDB lives in the gitignored uv `.venv`; the store file and parquet exports
are gitignored runtime data (the same convention as the raw acquired PDFs under data/*/raw/).

The escalated-only loop (Phase 36, refining D4's "book ∪ all prior-scanned"):
  - serve_news appends each grounded scan        -> append_scan()       (entities land disposition NULL)
  - the human Disposition gate posts back ESCALATE -> set_disposition()  (marks one entity 'escalate')
  - the next scan screens against book ∪ escalated -> watchlist_rows()    (a curated, growing surface)
A dismissed (or never-dispositioned) entity NEVER joins the watchlist — the watchlist is curated by the
human gate, not a dump of every name ever seen. Provenance ("escalated from <article>") keeps the
exposure view honest about WHY a hit fired.

Writes are serialized behind a lock: ThreadingHTTPServer dispatches /extract concurrently and a single
DuckDB connection is not safe for concurrent writes (single-writer is the documented model).
"""
import argparse
import os
import re
import sys
import threading
import uuid

try:
    import duckdb
except ModuleNotFoundError:  # the companion degrades gracefully (persistence disabled); selftest reports it
    duckdb = None

# scans -> entities/red_flags by scan_id; entities.disposition is the watchlist gate (NULL until the
# human Disposition gate escalates/dismisses). One normalized row shape per source field so parquet and
# the watchlist union are stable.
SCHEMA = """
CREATE TABLE IF NOT EXISTS scans(
  scan_id      VARCHAR PRIMARY KEY,
  ts           VARCHAR,
  record_id    VARCHAR,
  title        VARCHAR,
  doc_type     VARCHAR,
  typology     VARCHAR,
  source_org   VARCHAR,
  source_url   VARCHAR,
  article_text VARCHAR,
  n_grounded   INTEGER,
  n_dropped    INTEGER
);
CREATE TABLE IF NOT EXISTS entities(
  scan_id      VARCHAR,
  entity_id    VARCHAR,
  name         VARCHAR,
  type         VARCHAR,
  age          VARCHAR,
  location     VARCHAR,
  profession   VARCHAR,
  context      VARCHAR,
  disposition  VARCHAR
);
CREATE TABLE IF NOT EXISTS red_flags(
  scan_id      VARCHAR,
  flag_id      VARCHAR,
  flag         VARCHAR,
  red_flag     VARCHAR,
  category     VARCHAR
);
"""

_TABLES = ("scans", "entities", "red_flags")


def _norm(name) -> str:
    """The watchlist dedup/identity key — case/punctuation-insensitive. Deliberately coarser than the
    client Jaro-Winkler matcher (this only collapses re-escalations of the SAME name into one row; the
    fuzzy near-match scoring stays client-side, REAL, and unchanged)."""
    return re.sub(r"[^a-z0-9]+", " ", (name or "").lower()).strip()


def reconcile_book(book_rows) -> list:
    """Map the static book rows {id,name,type,role,country,segment} to the uniform screening shape
    {id,name,type,kind:'book',provenance} the client matcher scores by `name`. PURE — no DuckDB — so the
    companion can serve a book-only watchlist when persistence is disabled (duckdb absent)."""
    out = []
    for b in (book_rows or []):
        prov = " · ".join(x for x in [b.get("role"), b.get("segment"), b.get("country")] if x)
        out.append({"id": b.get("id"), "name": b.get("name"), "type": b.get("type"),
                    "kind": "book", "provenance": prov})
    return out


class NewsStore:
    """A thread-safe DuckDB store for live news scans + the escalated-only watchlist."""

    def __init__(self, path: str = ":memory:"):
        if duckdb is None:
            raise RuntimeError("duckdb is not installed — run the companion under the .venv for persistence")
        self.path = path
        if path != ":memory:":
            parent = os.path.dirname(path)
            if parent:
                os.makedirs(parent, exist_ok=True)
        self._lock = threading.Lock()
        self.con = duckdb.connect(path)
        self.con.execute(SCHEMA)

    # ---- writes (serialized) -------------------------------------------------------------------
    def append_scan(self, record: dict, dropped=None, ts: str = "") -> str:
        """Row-append one grounded scan (the record from serve_news.build_record) + its entities (NULL
        disposition) + red flags. Returns the new scan_id (the companion echoes it to the client so a
        later /disposition can target a specific entity)."""
        scan_id = uuid.uuid4().hex
        ents = record.get("entities") or []
        flags = record.get("red_flags") or []
        with self._lock:
            self.con.execute(
                "INSERT INTO scans VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                [scan_id, ts, record.get("id"), record.get("title"), record.get("doc_type"),
                 record.get("typology"), record.get("source_org"), record.get("source_url"),
                 record.get("article_text"), len(ents), len(dropped or [])])
            for e in ents:
                self.con.execute(
                    "INSERT INTO entities VALUES (?,?,?,?,?,?,?,?,?)",
                    [scan_id, e.get("id"), e.get("name"), e.get("type"), e.get("age"),
                     e.get("location"), e.get("profession"), e.get("context"), None])
            for f in flags:
                self.con.execute(
                    "INSERT INTO red_flags VALUES (?,?,?,?,?)",
                    [scan_id, f.get("id"), f.get("flag"), f.get("red_flag"), f.get("category")])
        return scan_id

    def set_disposition(self, scan_id: str, entity_id: str, decision: str) -> int:
        """Record the human Disposition-gate decision for one entity ('escalate' joins the watchlist;
        anything else does not). Returns the number of entity rows matched (0 if scan/entity unknown)."""
        with self._lock:
            n = self.con.execute(
                "SELECT count(*) FROM entities WHERE scan_id=? AND entity_id=?",
                [scan_id, entity_id]).fetchone()[0]
            self.con.execute(
                "UPDATE entities SET disposition=? WHERE scan_id=? AND entity_id=?",
                [decision, scan_id, entity_id])
        return int(n)

    # ---- reads ---------------------------------------------------------------------------------
    def escalated(self) -> list:
        """The DISTINCT escalated entities — one row per normalized name (re-escalations collapse), with
        provenance from the MOST RECENT escalating scan (ordered by ts so the latest wins the dict slot)."""
        with self._lock:
            rows = self.con.execute(
                "SELECT e.name, e.type, s.title, s.ts, s.record_id "
                "FROM entities e JOIN scans s USING(scan_id) "
                "WHERE e.disposition='escalate' ORDER BY s.ts").fetchall()
        out = {}
        for name, etype, title, ts, rid in rows:
            key = _norm(name)
            if not key:
                continue
            where = title or rid or "a prior article"
            prov = f"escalated from {where}" + (f" ({ts})" if ts else "")
            out[key] = {"name": name, "type": etype, "kind": "scanned", "provenance": prov,
                        "source_id": rid, "source_title": title, "ts": ts}
        return list(out.values())

    def watchlist_rows(self, book_rows=None) -> list:
        """The screening surface served to the live client: the static book ∪ the escalated entities,
        reconciled to a uniform row {name, type, kind:'book'|'scanned', provenance} the Jaro-Winkler
        matcher scores by `name`. Book takes precedence on a name collision (it is YOUR counterparty;
        the escalation is then redundant). The book passes through here so the store stays book-agnostic;
        the offline (book-only) screen path is untouched."""
        book_rows = book_rows or []
        book_keys = {_norm(b.get("name")) for b in book_rows}
        rows = reconcile_book(book_rows)
        for e in self.escalated():
            if _norm(e["name"]) in book_keys:
                continue  # already in the book — the book row wins
            rows.append({"id": None, "name": e["name"], "type": e["type"],
                         "kind": "scanned", "provenance": e["provenance"]})
        return rows

    def export_parquet(self, out_dir: str) -> dict:
        """Export each table to <out_dir>/<table>.parquet via DuckDB's native COPY (parquet is the
        interchange format; the .duckdb file is the append-friendly working store). Returns {table: path}."""
        os.makedirs(out_dir, exist_ok=True)
        paths = {}
        for tbl in _TABLES:
            p = os.path.join(out_dir, f"{tbl}.parquet")
            with self._lock:
                self.con.execute(f"COPY {tbl} TO '{p.replace(chr(39), chr(39) * 2)}' (FORMAT parquet)")
            paths[tbl] = p
        return paths

    def close(self) -> None:
        with self._lock:
            self.con.close()


def _selftest() -> int:
    """Exercise the full store contract on a temp DuckDB: append → watchlist-is-book-only → escalate →
    watchlist-grows-with-provenance → dismiss-does-not-grow → parquet roundtrip preserves the escalation."""
    if duckdb is None:
        print("news_store --selftest: SKIP (duckdb not installed — run under .venv)")
        return 0
    import tempfile

    st = NewsStore(":memory:")
    rec = {
        "id": "live-test", "title": "Test Article", "doc_type": "News", "typology": "fraud",
        "source_org": "Live input", "source_url": "", "article_text": "Acme and John laundered funds.",
        "entities": [
            {"id": "E1", "name": "Acme Holdings Ltd", "type": "org", "location": "Cyprus"},
            {"id": "E2", "name": "John Doe", "type": "person", "age": "44"},
        ],
        "red_flags": [{"id": "R1", "flag": "layered funds", "red_flag": "Layering via shells", "category": "Layering"}],
    }
    book = [{"id": "bk-1", "name": "Globex Bank", "type": "org", "role": "counterparty",
             "country": "United States", "segment": "Trade finance"}]

    sid = st.append_scan(rec, dropped=[{"name": "noise"}], ts="2026-06-08T10:00:00")
    assert sid and len(sid) == 32, f"expected a uuid4 hex scan_id, got {sid!r}"

    wl0 = st.watchlist_rows(book)
    assert [r for r in wl0 if r["kind"] == "scanned"] == [], "no escalations yet — watchlist must be book-only"
    assert any(r["kind"] == "book" and r["name"] == "Globex Bank" for r in wl0), "book row missing from watchlist"
    assert "counterparty" in next(r["provenance"] for r in wl0 if r["kind"] == "book"), "book provenance missing"

    assert st.set_disposition(sid, "E1", "escalate") == 1, "escalate should match exactly one entity"
    assert st.set_disposition(sid, "E2", "dismiss") == 1, "dismiss should match exactly one entity"
    assert st.set_disposition(sid, "E9", "escalate") == 0, "unknown entity_id should match zero rows"

    wl1 = st.watchlist_rows(book)
    scanned = [r for r in wl1 if r["kind"] == "scanned"]
    assert len(scanned) == 1, f"only the escalated entity joins the watchlist, got {scanned}"
    assert scanned[0]["name"] == "Acme Holdings Ltd", scanned
    assert "escalated from Test Article" in scanned[0]["provenance"], scanned[0]["provenance"]
    assert all(r["name"] != "John Doe" for r in wl1), "dismissed entity must NOT be on the watchlist"

    # re-escalating the SAME name in another scan collapses to one watchlist row (no duplicate surface)
    sid2 = st.append_scan({**rec, "id": "live-2", "title": "Second Article"}, ts="2026-06-08T12:00:00")
    st.set_disposition(sid2, "E1", "escalate")
    assert len([r for r in st.watchlist_rows(book) if r["kind"] == "scanned"]) == 1, "re-escalation must dedup by name"

    d = tempfile.mkdtemp()
    paths = st.export_parquet(d)
    re_con = duckdb.connect(":memory:")
    n_ent = re_con.execute(f"SELECT count(*) FROM read_parquet('{paths['entities']}')").fetchone()[0]
    assert n_ent == 4, f"parquet entities roundtrip expected 4 (2 entities × 2 scans), got {n_ent}"
    n_esc = re_con.execute(
        f"SELECT count(*) FROM read_parquet('{paths['entities']}') WHERE disposition='escalate'").fetchone()[0]
    assert n_esc == 2, f"parquet must preserve the 2 escalations, got {n_esc}"
    n_scans = re_con.execute(f"SELECT count(*) FROM read_parquet('{paths['scans']}')").fetchone()[0]
    assert n_scans == 2, f"parquet scans roundtrip expected 2, got {n_scans}"
    re_con.close()
    st.close()

    print(f"news_store --selftest: PASS (scan {sid[:8]}…, 4 entity-rows, 2 escalated→1 deduped watchlist row, "
          f"parquet roundtrip {n_ent} entity rows / {n_scans} scans)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="DuckDB store + escalated-only watchlist (companion-only, Phase 36).")
    ap.add_argument("--selftest", action="store_true", help="exercise the store contract on a temp DuckDB, exit")
    args = ap.parse_args()
    if args.selftest:
        return _selftest()
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
