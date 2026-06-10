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
#
# Phase 41 — the ANCHOR design (entity resolution): `anchors` is the identity spine — one row per
# exact-normalized name (cross-scan ACCUMULATION lands on the same anchor; fuzzy MERGE adjudication is
# deferred). `entity_properties` is ONE monolithic association table — one row per anchor × kind ×
# value EDGE with scan provenance, NON-DESTRUCTIVE: conflicting values (two DOBs) are BOTH kept and
# surfaced, never auto-resolved; `detail` is reserved JSON for kind-specific structure; `confidence`
# is RESERVED and stays NULL until a measured basis exists (a model-emitted confidence is a
# fabricated-shaped number). `entity_relationships` stores the gate-passed evidence edges.
# `scans.source_type` records what KIND of document fed the scan (gov-enforcement / commercial-news /
# investigation-note — document types differ in significance); an anchor remembers its first.
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
  n_dropped    INTEGER,
  source_type  VARCHAR
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
  disposition  VARCHAR,
  anchor_id    VARCHAR,
  is_main_subject BOOLEAN
);
CREATE TABLE IF NOT EXISTS red_flags(
  scan_id      VARCHAR,
  flag_id      VARCHAR,
  flag         VARCHAR,
  red_flag     VARCHAR,
  category     VARCHAR
);
CREATE TABLE IF NOT EXISTS anchors(
  anchor_id         VARCHAR PRIMARY KEY,
  name_key          VARCHAR,
  display_name      VARCHAR,
  type              VARCHAR,
  first_source_type VARCHAR,
  first_scan_id     VARCHAR,
  first_ts          VARCHAR
);
CREATE TABLE IF NOT EXISTS entity_properties(
  anchor_id  VARCHAR,
  scan_id    VARCHAR,
  entity_id  VARCHAR,
  kind       VARCHAR,
  value      VARCHAR,
  detail     VARCHAR,
  evidence   VARCHAR,
  grounded   BOOLEAN,
  confidence DOUBLE
);
CREATE TABLE IF NOT EXISTS entity_relationships(
  scan_id        VARCHAR,
  from_anchor_id VARCHAR,
  to_anchor_id   VARCHAR,
  from_name      VARCHAR,
  to_name        VARCHAR,
  label          VARCHAR,
  evidence       VARCHAR
);
"""

_TABLES = ("scans", "entities", "red_flags", "anchors", "entity_properties", "entity_relationships")

# Phase 41 — what fed a scan. The honest default is "" (unknown); the live UI offers these.
SOURCE_TYPES = ("gov-enforcement", "commercial-news", "investigation-note")


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
        self._migrate()

    def _migrate(self) -> None:
        """Phase 41 — one-shot ADDITIVE migration for a pre-anchor store file (local-only data; the
        ALTERs keep existing scans rather than recreating). A fresh store already has the full schema."""
        for table, col, decl in (("scans", "source_type", "VARCHAR"),
                                 ("entities", "anchor_id", "VARCHAR"),
                                 ("entities", "is_main_subject", "BOOLEAN")):
            cols = {r[1] for r in self.con.execute(f"PRAGMA table_info('{table}')").fetchall()}
            if col not in cols:
                self.con.execute(f"ALTER TABLE {table} ADD COLUMN {col} {decl}")

    def _anchor_for(self, name: str, etype: str, scan_id: str, ts: str, source_type: str) -> str:
        """Resolve a name to its identity anchor (exact-normalized key) — creating the anchor on first
        sight with its first-seen provenance. CALLER HOLDS the lock. Same-name-different-person
        collisions are a documented limitation of exact-name anchoring (fuzzy merge/split deferred)."""
        key = _norm(name)
        row = self.con.execute("SELECT anchor_id FROM anchors WHERE name_key=?", [key]).fetchone()
        if row:
            return row[0]
        aid = uuid.uuid4().hex
        self.con.execute("INSERT INTO anchors VALUES (?,?,?,?,?,?,?)",
                         [aid, key, name, etype, source_type, scan_id, ts])
        return aid

    # ---- writes (serialized) -------------------------------------------------------------------
    def append_scan(self, record: dict, dropped=None, ts: str = "", source_type: str = "") -> str:
        """Row-append one grounded scan (the record from serve_news.build_record) + its entities (NULL
        disposition) + red flags. Returns the new scan_id (the companion echoes it to the client so a
        later /disposition can target a specific entity).

        Phase 41 — each entity also resolves to its identity ANCHOR (exact-normalized name; created on
        first sight): aliases + properties land as edge rows in entity_properties (per-scan provenance,
        non-destructive — a conflicting value is a second row, never an overwrite; confidence stays
        NULL), gate-passed relationships land as anchor edges, and main_subjects flag their entity row."""
        scan_id = uuid.uuid4().hex
        ents = record.get("entities") or []
        flags = record.get("red_flags") or []
        mains = set(record.get("main_subjects") or [])
        with self._lock:
            self.con.execute(
                "INSERT INTO scans(scan_id, ts, record_id, title, doc_type, typology, source_org, "
                "source_url, article_text, n_grounded, n_dropped, source_type) "
                "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                [scan_id, ts, record.get("id"), record.get("title"), record.get("doc_type"),
                 record.get("typology"), record.get("source_org"), record.get("source_url"),
                 record.get("article_text"), len(ents), len(dropped or []), source_type])
            anchor_by_name = {}
            for e in ents:
                nm = e.get("name")
                aid = self._anchor_for(nm, e.get("type"), scan_id, ts, source_type)
                anchor_by_name[nm] = aid
                self.con.execute(
                    "INSERT INTO entities(scan_id, entity_id, name, type, age, location, profession, "
                    "context, disposition, anchor_id, is_main_subject) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                    [scan_id, e.get("id"), nm, e.get("type"), e.get("age"),
                     e.get("location"), e.get("profession"), e.get("context"), None,
                     aid, nm in mains])
                for a in e.get("aliases") or []:
                    self.con.execute(
                        "INSERT INTO entity_properties VALUES (?,?,?,?,?,?,?,?,?)",
                        [aid, scan_id, e.get("id"), "alias", a, None, None, True, None])
                for p in e.get("properties") or []:
                    self.con.execute(
                        "INSERT INTO entity_properties VALUES (?,?,?,?,?,?,?,?,?)",
                        [aid, scan_id, e.get("id"), p.get("kind"), p.get("value"), None, None, True, None])
            for r in record.get("relationships") or []:
                self.con.execute(
                    "INSERT INTO entity_relationships VALUES (?,?,?,?,?,?,?)",
                    [scan_id, anchor_by_name.get(r.get("from")), anchor_by_name.get(r.get("to")),
                     r.get("from"), r.get("to"), r.get("label"), r.get("evidence")])
            for f in flags:
                self.con.execute(
                    "INSERT INTO red_flags VALUES (?,?,?,?,?)",
                    [scan_id, f.get("id"), f.get("flag"), f.get("red_flag"), f.get("category")])
        return scan_id

    # ---- reads (Phase 41 — the accumulated identity view) ---------------------------------------
    def anchor_summary(self, name: str):
        """The accumulated identity for one anchor (exact-normalized name), or None: the scans that
        touched it, every property/alias edge WITH per-row scan provenance (non-destructive — a
        conflicting value shows as a second row for the analyst, never auto-resolved), and the
        relationship edges it participates in."""
        key = _norm(name)
        with self._lock:
            a = self.con.execute(
                "SELECT anchor_id, display_name, type, first_source_type, first_ts "
                "FROM anchors WHERE name_key=?", [key]).fetchone()
            if not a:
                return None
            aid = a[0]
            scans = self.con.execute(
                "SELECT DISTINCT e.scan_id, s.title, s.ts, s.source_type FROM entities e "
                "JOIN scans s USING(scan_id) WHERE e.anchor_id=? ORDER BY s.ts", [aid]).fetchall()
            props = self.con.execute(
                "SELECT p.kind, p.value, p.scan_id, s.title, s.ts, s.source_type "
                "FROM entity_properties p JOIN scans s USING(scan_id) "
                "WHERE p.anchor_id=? ORDER BY s.ts, p.kind, p.value", [aid]).fetchall()
            rels = self.con.execute(
                "SELECT from_name, to_name, label, evidence FROM entity_relationships "
                "WHERE from_anchor_id=? OR to_anchor_id=? ORDER BY scan_id", [aid, aid]).fetchall()
        return {
            "anchor_id": aid, "name": a[1], "type": a[2],
            "first_source_type": a[3], "first_ts": a[4],
            "scans": [{"scan_id": s, "title": t, "ts": ts_, "source_type": st} for s, t, ts_, st in scans],
            "properties": [{"kind": k, "value": v, "scan_id": s,
                            "provenance": {"title": t, "ts": ts_, "source_type": st}}
                           for k, v, s, t, ts_, st in props],
            "relationships": [{"from": f, "to": t, "label": lb, "evidence": ev} for f, t, lb, ev in rels],
        }

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

    def prune(self, name: str) -> int:
        """Remove an escalated entity from the watchlist surface BY NAME (the watchlist is keyed by
        normalized name, so a scanned row carries no entity_id). Un-escalates EVERY escalated row whose
        normalized name matches — sets disposition='pruned' rather than deleting, so the scan/audit trail
        survives. Returns the number of rows un-escalated (0 if no escalated row matches)."""
        key = _norm(name)
        if not key:
            return 0
        with self._lock:
            rows = self.con.execute(
                "SELECT scan_id, entity_id, name FROM entities WHERE disposition='escalate'").fetchall()
            targets = [(sid, eid) for sid, eid, nm in rows if _norm(nm) == key]
            for sid, eid in targets:
                self.con.execute(
                    "UPDATE entities SET disposition='pruned' WHERE scan_id=? AND entity_id=?", [sid, eid])
        return len(targets)

    # ---- reads ---------------------------------------------------------------------------------
    def escalated(self) -> list:
        """The DISTINCT escalated entities — one row per normalized name (re-escalations collapse), with
        provenance from the MOST RECENT escalating scan (ordered by ts so the latest wins the dict slot).

        Phase 41 — each row also carries the ANCHOR's accumulated aliases (every kind='alias' edge,
        any scan) so the live Screen matches name ∪ aliases, plus the escalating scan's source_type
        in the provenance (document types differ in significance)."""
        with self._lock:
            rows = self.con.execute(
                "SELECT e.name, e.type, s.title, s.ts, s.record_id, s.source_type, e.anchor_id "
                "FROM entities e JOIN scans s USING(scan_id) "
                "WHERE e.disposition='escalate' ORDER BY s.ts").fetchall()
            alias_rows = self.con.execute(
                "SELECT DISTINCT anchor_id, value FROM entity_properties WHERE kind='alias'").fetchall()
        aliases_by_anchor = {}
        for aid, val in alias_rows:
            aliases_by_anchor.setdefault(aid, []).append(val)
        out = {}
        for name, etype, title, ts, rid, stype, aid in rows:
            key = _norm(name)
            if not key:
                continue
            where = title or rid or "a prior article"
            prov = f"escalated from {where}" + (f" ({ts})" if ts else "") + (f" · {stype}" if stype else "")
            out[key] = {"name": name, "type": etype, "kind": "scanned", "provenance": prov,
                        "source_id": rid, "source_title": title, "ts": ts,
                        "source_type": stype or "", "aliases": sorted(aliases_by_anchor.get(aid) or [])}
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
                         "kind": "scanned", "provenance": e["provenance"],
                         "aliases": e.get("aliases") or []})
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

    # prune BY NAME un-escalates every matching row (both scans) → leaves the watchlist; book is untouched
    pruned = st.prune("Acme Holdings Ltd")
    assert pruned == 2, f"prune should un-escalate both escalations of the name, got {pruned}"
    wl2 = st.watchlist_rows(book)
    assert [r for r in wl2 if r["kind"] == "scanned"] == [], "pruned name must leave the watchlist"
    assert any(r["kind"] == "book" and r["name"] == "Globex Bank" for r in wl2), "prune must not touch the book"
    assert st.prune("Nonexistent Name") == 0, "pruning an unknown name un-escalates nothing"
    # re-escalate so the parquet roundtrip below still sees the 2 escalations (prune retained the audit rows)
    st.set_disposition(sid, "E1", "escalate")
    st.set_disposition(sid2, "E1", "escalate")

    # ── Phase 41 — the ANCHOR design: exact-normalized name → ONE identity across scans ──
    acme = st.anchor_summary("acme holdings ltd")  # lookup key is case/punctuation-insensitive
    assert acme and len(acme["scans"]) == 2, "two scans of the same name must land on ONE anchor"
    assert st.anchor_summary("Nobody Known") is None
    rec3 = {**rec, "id": "live-3", "title": "Third Article",
            "entities": [
                {"id": "E1", "name": "Acme Holdings Ltd", "type": "org",
                 "aliases": ["Acme"],
                 "properties": [{"kind": "address", "value": "12 Harbour Rd, Limassol"}]},
                {"id": "E2", "name": "John Doe", "type": "person",
                 "properties": [{"kind": "dob", "value": "2 June 1981"},
                                {"kind": "client_number", "value": "C-77812"}]},
            ],
            "relationships": [{"from": "John Doe", "to": "Acme Holdings Ltd",
                               "label": "owner-or-controller-of", "evidence": "John owns Acme"}],
            "main_subjects": ["John Doe"]}
    st.append_scan(rec3, ts="2026-06-09T09:00:00", source_type="investigation-note")
    rec4 = {**rec, "id": "live-4", "title": "Fourth Article",
            "entities": [{"id": "E1", "name": "John Doe", "type": "person",
                          "properties": [{"kind": "dob", "value": "3 July 1979"}]}]}
    st.append_scan(rec4, ts="2026-06-09T10:00:00", source_type="gov-enforcement")
    jd = st.anchor_summary("John Doe")
    assert len(jd["scans"]) == 4, f"John Doe rode 4 scans onto one anchor, got {len(jd['scans'])}"
    dobs = [p for p in jd["properties"] if p["kind"] == "dob"]
    assert {d["value"] for d in dobs} == {"2 June 1981", "3 July 1979"}, \
        f"CONFLICTING values must BOTH be kept with provenance (never auto-resolved): {dobs}"
    assert {d["provenance"]["source_type"] for d in dobs} == {"investigation-note", "gov-enforcement"}, dobs
    assert any(p["kind"] == "client_number" and p["value"] == "C-77812" for p in jd["properties"])
    assert jd["relationships"] == [{"from": "John Doe", "to": "Acme Holdings Ltd",
                                    "label": "owner-or-controller-of", "evidence": "John owns Acme"}]
    acme2 = st.anchor_summary("ACME HOLDINGS LTD")
    assert any(p["kind"] == "alias" and p["value"] == "Acme" for p in acme2["properties"]), "alias edge missing"
    n_main = st.con.execute("SELECT count(*) FROM entities WHERE is_main_subject").fetchone()[0]
    assert n_main == 1, f"exactly the rec3 John Doe row is flagged main subject, got {n_main}"
    n_conf = st.con.execute("SELECT count(*) FROM entity_properties WHERE confidence IS NOT NULL").fetchone()[0]
    assert n_conf == 0, "confidence is RESERVED — no write path may populate it (no fabricated numbers)"

    d = tempfile.mkdtemp()
    paths = st.export_parquet(d)
    re_con = duckdb.connect(":memory:")
    n_ent = re_con.execute(f"SELECT count(*) FROM read_parquet('{paths['entities']}')").fetchone()[0]
    assert n_ent == 7, f"parquet entities roundtrip expected 7 (2+2+2+1), got {n_ent}"
    n_esc = re_con.execute(
        f"SELECT count(*) FROM read_parquet('{paths['entities']}') WHERE disposition='escalate'").fetchone()[0]
    assert n_esc == 2, f"parquet must preserve the 2 escalations, got {n_esc}"
    n_scans = re_con.execute(f"SELECT count(*) FROM read_parquet('{paths['scans']}')").fetchone()[0]
    assert n_scans == 4, f"parquet scans roundtrip expected 4, got {n_scans}"
    n_props = re_con.execute(f"SELECT count(*) FROM read_parquet('{paths['entity_properties']}')").fetchone()[0]
    assert n_props == 5, f"parquet entity_properties roundtrip expected 5 edges, got {n_props}"
    n_rel = re_con.execute(f"SELECT count(*) FROM read_parquet('{paths['entity_relationships']}')").fetchone()[0]
    assert n_rel == 1, f"parquet entity_relationships roundtrip expected 1 edge, got {n_rel}"
    re_con.close()
    st.close()

    # ── Phase 41 — additive migration: a pre-anchor store file opens, migrates, and accepts new scans ──
    old_path = os.path.join(tempfile.mkdtemp(), "old.duckdb")
    legacy = duckdb.connect(old_path)
    legacy.execute("""
        CREATE TABLE scans(scan_id VARCHAR PRIMARY KEY, ts VARCHAR, record_id VARCHAR, title VARCHAR,
          doc_type VARCHAR, typology VARCHAR, source_org VARCHAR, source_url VARCHAR,
          article_text VARCHAR, n_grounded INTEGER, n_dropped INTEGER);
        CREATE TABLE entities(scan_id VARCHAR, entity_id VARCHAR, name VARCHAR, type VARCHAR,
          age VARCHAR, location VARCHAR, profession VARCHAR, context VARCHAR, disposition VARCHAR);
        CREATE TABLE red_flags(scan_id VARCHAR, flag_id VARCHAR, flag VARCHAR, red_flag VARCHAR, category VARCHAR);
        INSERT INTO scans VALUES ('legacy1','2026-06-01T00:00:00','r','Old Scan','News','', '', '', 'body', 1, 0);
        INSERT INTO entities VALUES ('legacy1','E1','Old Name','person',NULL,NULL,NULL,NULL,'escalate');
    """)
    legacy.close()
    st2 = NewsStore(old_path)
    assert any(r["name"] == "Old Name" for r in st2.watchlist_rows([])), "legacy escalation must survive migration"
    st2.append_scan(rec3, ts="2026-06-09T11:00:00", source_type="investigation-note")
    assert st2.anchor_summary("John Doe"), "post-migration append must anchor"
    st2.close()

    print(f"news_store --selftest: PASS (scan {sid[:8]}…, {n_ent} entity-rows, 2 escalated→1 deduped watchlist row, "
          f"anchors: 4-scan accumulation + both-kept dob conflict + alias/client_number edges + NULL confidence; "
          f"parquet roundtrip {n_ent} entities / {n_scans} scans / {n_props} property edges / {n_rel} relationship edge; "
          f"legacy-store migration ok)")
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
