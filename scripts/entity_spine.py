#!/usr/bin/env python3
"""The persistent entity intelligence spine (Phase 74 — companion-only).

A NEW, pillar-neutral module — NOT a generalization of news_store.py (which stays byte-untouched; the M8
news pillar is inherently safe). The spine ties records to the same counterparty over time, accumulates
prior dispositions on the entity, and grades every identity link so confidence travels as PROVENANCE.

Contract (docs/): resolution-link-schema.md · identity-grade-grammar.md · confidence-as-provenance-contract.md
· true-entities-scorer-contract.md.

The three layers (resolution is its OWN layer — identity is a derived, revisable, GRADED assertion, never a
join key you discover once):
  1. observations          — raw presented attributes per record (immutable, provenance-linked).
  2. resolution_links       — append-only, bitemporal mapping observation -> persistent_entity, GRADED.
  3. persistent_entities    — the accumulating record (best-view + facts + prior dispositions).

Deterministic linkage ONLY this phase (probabilistic/Splink + the merge-adjudication Class-J console are
DEFERRED, named in the standards): a STRONG shared identifier (email/phone/account/…) MERGES; a WEAK-only
identifier (address) CORROBORATES but never merges on its own; NAME-only is REJECT (not a link). The
exact-normalized NAME is one deterministic rule feeding the link layer — never the entity key.

COMPANION-ONLY. build.py NEVER imports this. DuckDB lives in the gitignored uv .venv; the store file is
gitignored runtime data. NO news_store / serve_news import (the directional firewall — the selftest asserts
it). Degrades gracefully when duckdb is absent (the selftest SKIPs).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import threading
import uuid

try:
    import duckdb
except ModuleNotFoundError:  # the companion degrades gracefully; selftest reports it
    duckdb = None

# ── the identity-grade grammar (docs/identity-grade-grammar.md) — the closed, shared vocabulary ──
GRADES = ("reject", "weak", "strong")          # ordinal, weakest-first: reject < weak < strong
_GRADE_RANK = {g: i for i, g in enumerate(GRADES)}
STRONG_KINDS = ("email", "phone", "account_number", "client_number", "id_registration", "wallet", "domain")
WEAK_KINDS = ("address",)
# name is NEITHER — an observation that may trigger a candidate link, graded `reject` until an identifier
# corroborates it.


def grade_of_kind(kind: str) -> str:
    """The grade a single identifier KIND can confer when it matches exactly: strong / weak / reject."""
    if kind in STRONG_KINDS:
        return "strong"
    if kind in WEAK_KINDS:
        return "weak"
    return "reject"


def max_grade(grades) -> str:
    """The strongest grade in a set (a link is graded by its STRONGEST shared identifier). Empty -> reject
    (fail-closed: no basis is the weakest)."""
    best = "reject"
    for g in grades or ():
        if _GRADE_RANK.get(g, 0) > _GRADE_RANK[best]:
            best = g
    return best


def _norm(text) -> str:
    """Case/punctuation-insensitive key (names + a fallback for identifiers that arrive un-normalized)."""
    return re.sub(r"[^a-z0-9]+", "", (text or "").lower()).strip()


def _norm_ident(kind: str, value: str, normalized: str | None) -> str:
    """The normalized identifier key. Prefer the record-supplied `normalized` (the casefile authors it);
    fall back to a deterministic normalization so the spine is self-contained."""
    if normalized:
        return normalized
    if kind == "email":
        return re.sub(r"[^a-z0-9@.]+", "", (value or "").lower())
    return _norm(value)


SCHEMA = """
CREATE TABLE IF NOT EXISTS observations(
  obs_id         VARCHAR PRIMARY KEY,
  record_id      VARCHAR,
  presented_id   VARCHAR,
  presented_name VARCHAR,
  kind           VARCHAR,
  role           VARCHAR,
  source_type    VARCHAR,
  ts             VARCHAR,
  entity_id      VARCHAR
);
CREATE TABLE IF NOT EXISTS observation_identifiers(
  obs_id     VARCHAR,
  kind       VARCHAR,
  value      VARCHAR,
  normalized VARCHAR,
  strength   VARCHAR
);
CREATE TABLE IF NOT EXISTS persistent_entities(
  entity_id          VARCHAR PRIMARY KEY,
  display_name       VARCHAR,
  kind               VARCHAR,
  first_record_id    VARCHAR,
  first_ts           VARCHAR,
  resolution_version INTEGER
);
CREATE TABLE IF NOT EXISTS resolution_links(
  link_id            VARCHAR PRIMARY KEY,
  entity_id          VARCHAR,
  obs_id             VARCHAR,
  method             VARCHAR,
  grade              VARCHAR,
  basis              VARCHAR,
  valid_time_start   VARCHAR,
  valid_time_end     VARCHAR,
  decision_time      VARCHAR,
  resolution_version INTEGER,
  supersedes         VARCHAR,
  status             VARCHAR
);
CREATE TABLE IF NOT EXISTS entity_dispositions(
  disp_id            VARCHAR PRIMARY KEY,
  entity_id          VARCHAR,
  record_id          VARCHAR,
  verdict            VARCHAR,
  decided_at         VARCHAR,
  resolution_version INTEGER,
  grounding_links    VARCHAR,
  grounding          VARCHAR,
  status             VARCHAR
);
"""

_TABLES = ("observations", "observation_identifiers", "persistent_entities", "resolution_links",
           "entity_dispositions")

# method values for resolution_links (probabilistic / human-adjudicated are DEFERRED — named, not used here)
_DETERMINISTIC_IDENTIFIER = "deterministic-identifier"
_DETERMINISTIC_NAME = "deterministic-name"


class EntitySpine:
    """A thread-safe DuckDB persistent entity spine. Deterministic linkage; append-only, bitemporal,
    graded resolution; reversible split with cascade-invalidation."""

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

    # ── pairwise grade (pure; the grade-gating helper the consumer uses for read atoms) ──
    @staticmethod
    def edge_grade(idents_a, idents_b) -> tuple:
        """The grade of the resolution edge between two presented parties: STRONG if they share an exact
        normalized STRONG identifier, WEAK if they share only a WEAK identifier, REJECT otherwise (name-only
        / nothing). Returns (grade, basis[]) — basis names the shared identifier(s) that drove the grade.
        PURE: no store access; fail-closed (no shared identifier -> reject)."""
        by_key_a = {(i["kind"], _norm_ident(i["kind"], i.get("value"), i.get("normalized"))) for i in idents_a or []}
        shared = []
        for i in idents_b or []:
            key = (i["kind"], _norm_ident(i["kind"], i.get("value"), i.get("normalized")))
            if key in by_key_a:
                shared.append({"kind": i["kind"], "normalized": key[1], "grade": grade_of_kind(i["kind"])})
        grade = max_grade(g["grade"] for g in shared)
        return grade, shared

    # ── writes (serialized) ──
    def observe(self, record_id: str, party: dict, *, source_type: str = "", ts: str = "") -> dict:
        """Record one presented party from a record (its name + identifiers), resolve it to a persistent
        entity by DETERMINISTIC strong-identifier match (create a new entity if none), and append a graded
        resolution link. Returns {obs_id, entity_id, grade, basis, new_entity}.

        The merge rule (the grammar): a STRONG shared identifier with EXACTLY ONE existing entity -> MERGE
        (grade strong). Ambiguity (a strong identifier shared with 2+ distinct entities) REFUSES to merge
        (a new entity) — order never picks the owner. WEAK-only / NAME-only -> a new entity (weak corroborates
        but does not resolve; name-only is reject)."""
        idents = party.get("identifiers") or []
        with self._lock:
            obs_id = uuid.uuid4().hex
            strong_keys = [(i["kind"], _norm_ident(i["kind"], i.get("value"), i.get("normalized")))
                           for i in idents if i.get("strength") == "strong"]
            matched: dict = {}
            for kind, key in strong_keys:
                rows = self.con.execute(
                    "SELECT DISTINCT o.entity_id FROM observation_identifiers oi "
                    "JOIN observations o USING(obs_id) WHERE oi.strength='strong' AND oi.normalized=? "
                    "AND o.entity_id IS NOT NULL", [key]).fetchall()
                for (eid,) in rows:
                    matched.setdefault(eid, []).append({"kind": kind, "normalized": key, "grade": "strong"})

            new_entity = False
            if len(matched) == 1:
                entity_id = next(iter(matched))
                grade, basis, method = "strong", matched[entity_id], _DETERMINISTIC_IDENTIFIER
            else:
                # none, or AMBIGUOUS (2+ distinct entities) -> refuse to merge; seed a new entity
                entity_id = uuid.uuid4().hex
                new_entity = True
                self.con.execute("INSERT INTO persistent_entities VALUES (?,?,?,?,?,?)",
                                 [entity_id, party.get("display_name"), party.get("kind"),
                                  record_id, ts, 1])
                grade = max_grade(grade_of_kind(i["kind"]) for i in idents if i.get("strength"))
                basis = [{"kind": i["kind"], "normalized": _norm_ident(i["kind"], i.get("value"), i.get("normalized")),
                          "grade": grade_of_kind(i["kind"])} for i in idents]
                method = _DETERMINISTIC_IDENTIFIER if strong_keys else _DETERMINISTIC_NAME

            self.con.execute(
                "INSERT INTO observations VALUES (?,?,?,?,?,?,?,?,?)",
                [obs_id, record_id, party.get("entity_id") or party.get("presented_id"),
                 party.get("display_name"), party.get("kind"), party.get("role"),
                 source_type, ts, entity_id])
            for i in idents:
                self.con.execute(
                    "INSERT INTO observation_identifiers VALUES (?,?,?,?,?)",
                    [obs_id, i["kind"], i.get("value"),
                     _norm_ident(i["kind"], i.get("value"), i.get("normalized")), i.get("strength")])
            ev = self._entity_version(entity_id)
            self.con.execute(
                "INSERT INTO resolution_links VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                [uuid.uuid4().hex, entity_id, obs_id, method, grade, json.dumps(basis),
                 ts, None, ts, ev, None, "active"])
        return {"obs_id": obs_id, "entity_id": entity_id, "grade": grade, "basis": basis,
                "new_entity": new_entity}

    def _entity_version(self, entity_id: str) -> int:
        row = self.con.execute("SELECT resolution_version FROM persistent_entities WHERE entity_id=?",
                               [entity_id]).fetchone()
        return int(row[0]) if row else 1

    def resolution_version(self, entity_id: str) -> int:
        with self._lock:
            return self._entity_version(entity_id)

    def link_for_obs(self, obs_id: str) -> str | None:
        """The active resolution-link id for an observation (the edge a disposition's grounding crosses)."""
        with self._lock:
            row = self.con.execute(
                "SELECT link_id FROM resolution_links WHERE obs_id=? AND status='active'", [obs_id]).fetchone()
        return row[0] if row else None

    def attach_disposition(self, entity_id: str, record_id: str, verdict: str, *,
                           grounding_links=None, grounding: dict | None = None, decided_at: str = "") -> str:
        """Attach a prior disposition to an entity, STAMPED with the entity's current resolution_version
        (the stale-prior guard reads this). `grounding_links` are the resolution_link ids the disposition's
        evidence crossed — a later retraction of any of them cascade-marks this disposition re-decision."""
        with self._lock:
            disp_id = uuid.uuid4().hex
            self.con.execute(
                "INSERT INTO entity_dispositions VALUES (?,?,?,?,?,?,?,?,?)",
                [disp_id, entity_id, record_id, verdict, decided_at, self._entity_version(entity_id),
                 json.dumps(grounding_links or []), json.dumps(grounding or {}), "active"])
        return disp_id

    def retract_link(self, link_id: str) -> dict:
        """Reversible split / un-merge: retract a resolution link (status 'retracted', append-only — the row
        is never deleted), BUMP the entity's resolution_version, and CASCADE-MARK every disposition whose
        grounding crossed the retracted link as 're-decision required' (the audit row preserved, never
        deleted). Returns {entity_id, new_version, cascaded:[disp_id...]}."""
        with self._lock:
            row = self.con.execute("SELECT entity_id FROM resolution_links WHERE link_id=? AND status='active'",
                                   [link_id]).fetchone()
            if not row:
                return {"entity_id": None, "new_version": None, "cascaded": []}
            entity_id = row[0]
            self.con.execute("UPDATE resolution_links SET status='retracted' WHERE link_id=?", [link_id])
            new_v = self._entity_version(entity_id) + 1
            self.con.execute("UPDATE persistent_entities SET resolution_version=? WHERE entity_id=?",
                             [new_v, entity_id])
            cascaded = []
            disps = self.con.execute(
                "SELECT disp_id, grounding_links FROM entity_dispositions WHERE entity_id=? AND status='active'",
                [entity_id]).fetchall()
            for disp_id, gl in disps:
                if link_id in (json.loads(gl) if gl else []):
                    self.con.execute(
                        "UPDATE entity_dispositions SET status='re-decision required' WHERE disp_id=?", [disp_id])
                    cascaded.append(disp_id)
        return {"entity_id": entity_id, "new_version": new_v, "cascaded": cascaded}

    # ── reads ──
    def prior_dispositions(self, entity_id: str) -> list:
        """The dispositions accumulated on an entity, each flagged `stale` when it was decided under an
        EARLIER resolution_version (event-driven staleness — a merge/split since means it may have been
        about a party that is now two; surfaced 're-decision required', never trusted silently)."""
        with self._lock:
            cur = self._entity_version(entity_id)
            rows = self.con.execute(
                "SELECT disp_id, record_id, verdict, decided_at, resolution_version, grounding, status "
                "FROM entity_dispositions WHERE entity_id=? ORDER BY decided_at", [entity_id]).fetchall()
        out = []
        for disp_id, rid, verdict, da, rv, grounding, status in rows:
            stale = status == "re-decision required" or int(rv) < cur
            out.append({"disp_id": disp_id, "record_id": rid, "verdict": verdict, "decided_at": da,
                        "resolution_version": int(rv), "current_version": cur, "stale": stale,
                        "status": "re-decision required" if stale and status == "active" else status,
                        "grounding": json.loads(grounding) if grounding else {}})
        return out

    def accumulated(self, entity_id: str) -> dict:
        """The accumulated identity for one persistent entity: its observations (per-record provenance) and
        every identifier edge (conflicting values BOTH kept, never auto-resolved) + its prior dispositions."""
        with self._lock:
            ent = self.con.execute(
                "SELECT display_name, kind, resolution_version FROM persistent_entities WHERE entity_id=?",
                [entity_id]).fetchone()
            if not ent:
                return {}
            obs = self.con.execute(
                "SELECT obs_id, record_id, presented_name, role, source_type, ts FROM observations "
                "WHERE entity_id=? ORDER BY ts", [entity_id]).fetchall()
            idents = self.con.execute(
                "SELECT DISTINCT oi.kind, oi.value, oi.normalized, oi.strength FROM observation_identifiers oi "
                "JOIN observations o USING(obs_id) WHERE o.entity_id=? ORDER BY oi.kind, oi.value",
                [entity_id]).fetchall()
        return {
            "entity_id": entity_id, "display_name": ent[0], "kind": ent[1], "resolution_version": int(ent[2]),
            "observations": [{"obs_id": o, "record_id": r, "name": n, "role": ro, "source_type": st, "ts": t}
                             for o, r, n, ro, st, t in obs],
            "identifiers": [{"kind": k, "value": v, "normalized": nz, "strength": s} for k, v, nz, s in idents],
            "dispositions": self.prior_dispositions(entity_id),
        }

    def entity_count(self) -> int:
        with self._lock:
            return int(self.con.execute("SELECT count(*) FROM persistent_entities").fetchone()[0])

    def close(self) -> None:
        with self._lock:
            self.con.close()


# --------------------------------------------------------------------------------------------------
def _selftest() -> int:
    """Exercise the spine contract on a temp DuckDB: deterministic strong-id merge / weak-corroborate /
    name-only reject; append-only graded links; conflicting values both-kept; disposition attach + read;
    reversible split WITH cascade-invalidation; the event-driven stale-prior guard; fail-closed grade."""
    if duckdb is None:
        print("entity_spine --selftest: SKIP (duckdb not installed — run under .venv)")  # noqa: T201
        return 0

    s = EntitySpine(":memory:")

    # ── 1. deterministic STRONG-id merge: two James Calder observations sharing an email -> ONE entity ──
    a = s.observe("CASE-A", {"entity_id": "E-CALDER-INT", "display_name": "James Calder", "kind": "person",
                             "role": "related_party",
                             "identifiers": [{"kind": "email", "value": "jcalder.mgmt@swiftmail.test",
                                              "normalized": "jcaldermgmt@swiftmail.test", "strength": "strong"}]},
                  source_type="case", ts="2026-04-15")
    b = s.observe("CASE-A", {"entity_id": "E-CALDER-EXT", "display_name": "James Calder", "kind": "person",
                             "role": "counterparty",
                             "identifiers": [{"kind": "email", "value": "jcalder.mgmt@swiftmail.test",
                                              "normalized": "jcaldermgmt@swiftmail.test", "strength": "strong"}]},
                  source_type="case", ts="2026-04-15")
    assert a["new_entity"] and not b["new_entity"], (a, b)
    assert a["entity_id"] == b["entity_id"], "shared strong email must resolve to ONE entity"
    assert b["grade"] == "strong", b

    # ── 2. NAME-only is REJECT (no merge): John Calderon — two presentations, no shared identifier ──
    c = s.observe("CASE-B", {"entity_id": "E-CALDERON", "display_name": "John Calderon", "kind": "person",
                             "identifiers": [{"kind": "email", "value": "jcalderon.events@example.test",
                                              "normalized": "jcalonevents@example.test", "strength": "strong"}]},
                  ts="2026-04-06")
    d = s.observe("CASE-B", {"entity_id": "E-CALDERON-2", "display_name": "John Calderon", "kind": "person",
                             "identifiers": []}, ts="2026-04-06")
    assert c["entity_id"] != d["entity_id"], "name-only must NOT merge (reject)"
    g_name, basis_name = EntitySpine.edge_grade([], [])
    assert g_name == "reject" and basis_name == [], (g_name, basis_name)
    g_cc, _ = EntitySpine.edge_grade(
        [{"kind": "email", "value": "jcalderon.events@example.test", "normalized": "jcalonevents@example.test"}],
        [{"kind": "email", "value": "joncalderon@other.test", "normalized": "joncalderon@other.test"}])
    assert g_cc == "reject", "different emails, similar name -> reject (exact-on-identifier, never fuzzy-on-name)"

    # ── 3. edge grades: strong (shared email) vs weak (shared address only); fail-closed unknown ──
    g_strong, basis_strong = EntitySpine.edge_grade(
        [{"kind": "email", "value": "x@y.test", "normalized": "x@y.test"}],
        [{"kind": "email", "value": "x@y.test", "normalized": "x@y.test"}])
    assert g_strong == "strong" and basis_strong[0]["kind"] == "email", (g_strong, basis_strong)
    g_weak, _ = EntitySpine.edge_grade(
        [{"kind": "address", "value": "44 Holloway Court", "normalized": "44hollowaycourtbramptononca"}],
        [{"kind": "address", "value": "44 Holloway Court", "normalized": "44hollowaycourtbramptononca"}])
    assert g_weak == "weak", "a shared address alone is WEAK (corroborates, never resolves)"
    assert grade_of_kind("favourite_colour") == "reject" and max_grade([]) == "reject"

    # ── 4. conflicting values BOTH kept (two phones on one resolved entity) ──
    s.observe("CASE-X", {"entity_id": "E-DUP", "display_name": "Dana Vale", "kind": "person",
                         "identifiers": [{"kind": "email", "value": "dana@vale.test", "normalized": "dana@vale.test", "strength": "strong"},
                                         {"kind": "phone", "value": "+1-555-0111", "normalized": "15550111", "strength": "strong"}]},
              ts="2026-01-01")
    dup = s.observe("CASE-Y", {"entity_id": "E-DUP-2", "display_name": "Dana Vale", "kind": "person",
                              "identifiers": [{"kind": "email", "value": "dana@vale.test", "normalized": "dana@vale.test", "strength": "strong"},
                                              {"kind": "phone", "value": "+1-555-0999", "normalized": "15550999", "strength": "strong"}]},
                   ts="2026-02-01")
    acc = s.accumulated(dup["entity_id"])
    phones = sorted(i["value"] for i in acc["identifiers"] if i["kind"] == "phone")
    assert phones == ["+1-555-0111", "+1-555-0999"], f"conflicting phones must BOTH be kept: {phones}"
    assert len(acc["observations"]) == 2, "the two presentations rode onto one entity"

    # ── 5. disposition attach + read ──
    eid = a["entity_id"]
    link_ext = s.link_for_obs(b["obs_id"])
    disp = s.attach_disposition(eid, "CASE-A", "escalated", grounding_links=[link_ext],
                                grounding={"reason": "structured-drain recipient resolves to the director"},
                                decided_at="2026-04-20")
    priors = s.prior_dispositions(eid)
    assert len(priors) == 1 and priors[0]["verdict"] == "escalated" and not priors[0]["stale"], priors

    # ── 6. reversible SPLIT with cascade-invalidation: retract the link -> disposition flips re-decision ──
    res = s.retract_link(link_ext)
    assert res["entity_id"] == eid and res["new_version"] == 2 and disp in res["cascaded"], res
    priors2 = s.prior_dispositions(eid)
    assert priors2[0]["status"] == "re-decision required" and priors2[0]["stale"], \
        f"a disposition whose grounding crossed the retracted edge must flip re-decision: {priors2}"
    n_ret = s.con.execute("SELECT count(*) FROM resolution_links WHERE status='retracted'").fetchone()[0]
    assert n_ret == 1, "the retracted link must be kept (status='retracted'), never deleted"

    # ── 7. event-driven staleness: a NEW disposition decided AFTER the split (version 2) is NOT stale ──
    disp2 = s.attach_disposition(eid, "CASE-A2", "needs_more_info", decided_at="2026-05-01")
    fresh = [p for p in s.prior_dispositions(eid) if p["disp_id"] == disp2][0]
    assert fresh["resolution_version"] == 2 and not fresh["stale"], fresh

    # 4 distinct entities: E-CALDER + E-CALDERON + E-CALDERON-2 + E-DUP
    assert s.entity_count() == 4, f"expected 4 distinct entities, got {s.entity_count()}"

    # ── 8. persistence roundtrip on a real (temp) store file ──
    import tempfile
    p = os.path.join(tempfile.mkdtemp(), "spine.duckdb")
    s2 = EntitySpine(p)
    s2.observe("R1", {"entity_id": "P1", "display_name": "Roundtrip Co", "kind": "org",
                      "identifiers": [{"kind": "email", "value": "r@t.test", "normalized": "r@t.test", "strength": "strong"}]}, ts="2026-01-01")
    s2.close()
    s3 = EntitySpine(p)
    assert s3.entity_count() == 1, "the entity must survive a store reopen (genuine persistence)"
    s3.close()
    s.close()

    # ── 9. the DIRECTIONAL FIREWALL (live): the news-pillar disposition MACHINERY is core-ABSENT ──
    # (the spine uses attach_disposition + its own grade vocab, NOT news_store's set_disposition /
    # escalation-watchlist surface; "escalated" appears only as a generic verdict value, never as machinery).
    # Introspect method names (not the source text, which would self-match this very list).
    _surface = set(dir(EntitySpine)) | {n for n in globals() if callable(globals().get(n))}
    for banned in ("set_disposition", "watchlist_rows", "escalated", "reconcile_book", "append_scan", "anchor_summary"):
        assert banned not in _surface, f"news-pillar disposition vocab leaked into the spine core: {banned!r}"
    assert "news_store" not in sys.modules and "serve_news" not in sys.modules, \
        "the spine core must not import the news pillar"

    print("entity_spine --selftest: PASS "  # noqa: T201
          "(strong-id merge + name-only reject + weak corroboration; append-only graded links; "
          "conflicting values both-kept; disposition attach/read; reversible split with cascade-invalidation; "
          "event-driven stale-prior guard; fail-closed grade; persistence roundtrip)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Persistent entity intelligence spine (companion-only, Phase 74).")
    ap.add_argument("--selftest", action="store_true", help="exercise the spine contract on a temp DuckDB, exit")
    args = ap.parse_args()
    if args.selftest:
        return _selftest()
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
