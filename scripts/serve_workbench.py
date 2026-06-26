#!/usr/bin/env python3
"""Investigator case-workbench companion (Phase 63 — dev/authoring-time ONLY; NEVER a ship artifact).

The presenter's investigator surface over a REAL (synthetic) aml-substrate alert POPULATION (vendored
under data/workbench/ by curate_workbench_cases.py). Three beats:
  1. CLUTTER   — a QUEUE of the population + a per-case dense investigator page (the real KYC profile,
                 accounts, transaction summaries + details, real counterparty edges). Offline/model-free.
  2. SIGNALS   — a toggle overlays the case's GROUNDED signals (the flag->corpus audit walk) + the
                 precedent-confidence read; clutter -> clarity. NO catch-rate/precision number.
  3. DECIDE    — the LIVE finale: aml-casework consumes the bundle into a verified, signed SAR (default
                 Claude, configurable, stub fallback), then the cross-pillar check re-verifies the join.

DOCTRINE (inherited verbatim from serve_chain — this REUSES its consume/verify/audit/backend primitives):
  * subprocess + file-handoff ONLY; NEVER imports aml_substrate / aml_casework. stdlib only. build.py
    NEVER imports this; workbench.html is NOT a build target; the offline dists stay byte-frozen.
  * the browser sends a backend NAME only — creds/endpoints live server-side (non-negotiable §4.5).
  * nothing is persisted; the committed data/pillar-status.json is snapshot+restored by verify_e2e.
  * GROUNDED detection (real substrate alerts -> public-source corpus) / ILLUSTRATIVE dispositions; the
    precedent-confidence SAMPLE SIZE is real, the disposition direction illustrative (the Phase-62 split).

Usage:
    python3 scripts/serve_workbench.py                 # http://localhost:8030 (the investigator workbench)
    python3 scripts/serve_workbench.py --port 8031
    python3 scripts/serve_workbench.py --selftest      # offline assertions (no socket, casework stubbed), exit
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

_HERE = Path(__file__).resolve().parent
ROOT = _HERE.parent
sys.path.insert(0, str(_HERE))
# REUSE the chain workbench's primitives — the casework consume, the cross-pillar verify, the
# flag->corpus audit walk, and the whole server-side backend-resolution machinery (DRY; no duplication).
import serve_chain as sc  # noqa: E402  (signal-watch's OWN companion module, never a sibling)
from serve_chain import (  # noqa: E402
    BADGE, RunError, audit_walk, available_backends, casework_consume, default_backend,
    resolve_backend, verify_e2e, _stub_signed_sar,
)
# The GATING POLICY + the pure router live in curate (the authoring source of truth); the live engine
# RE-DERIVES routing from the SAME route() so the live funnel can't drift from the baked one.
from curate_workbench_cases import GATING_POLICY, route  # noqa: E402  (signal-watch's OWN module)
# Phase 65 — the GATHER beat: the OSINT agent loop + tools (stdlib + news_ground only; NEVER a sibling).
from osint_tools import (  # noqa: E402  (signal-watch's OWN companion module)
    CORPUS_PATH as OSINT_CORPUS_PATH, LivePlanner, StubPlanner, build_index as osint_build_index,
    call_openai, gather as osint_gather, load_corpus as osint_load_corpus, resolve_gather_backend,
    validate_osint_corpus,
)
# Phase 69 — the evidence-requirement profile: the determination-sufficiency control (chosen-not-measured).
from evidence_requirements import (  # noqa: E402  (signal-watch's OWN companion module)
    REQUIREMENTS_JSON, assess_completeness, crime_type_for_capabilities, determine, evaluate_sufficiency,
    gather_targets, gathered_signals, load_requirements, present_atoms, requirements as _requirements,
    validate_requirements,
)
# Phase 74 — the entity spine: grade-gate the read-from-file atoms (the grammar's max_grade is the gate);
# the persistent store backs the re-surfacing "memory" path. Confidence rides this SEPARATE read path —
# never through evidence_requirements' byte-frozen file bar.
from entity_spine import EntitySpine, max_grade  # noqa: E402  (signal-watch's OWN companion module)

DEFAULT_PORT = 8030          # serve_news 8000, serve_corpus 8010, serve_chain 8020 — all side by side
WORKBENCH_DIR = ROOT / "data" / "workbench"
CASES_JSON = WORKBENCH_DIR / "cases.json"
BUNDLES_DIR = WORKBENCH_DIR / "bundles"
TEMPLATE = ROOT / "workbench.html"
PLACEHOLDER = "<!--__WORKBENCH_CONFIG__-->"


# ---- the vendored population (data, read-only) ---------------------------------------------------
def load_index() -> dict:
    return json.loads(CASES_JSON.read_text(encoding="utf-8"))


def _case_entry(index: dict, case_id: str) -> dict:
    for c in index.get("cases", []):
        if c.get("case_id") == case_id:
            return c
    raise RunError(f"unknown case '{case_id}' — not in the vendored population (GET /cases)")


def _entry_caps(entry: dict) -> list:
    """The capability CODES a case fired — the index stores plain strings, the chain manifest stores dicts;
    normalize both to codes (the determination control keys on these)."""
    return [c.get("capability") if isinstance(c, dict) else c for c in entry.get("capabilities", [])]


def _bundle_path(case_id: str) -> Path:
    p = (BUNDLES_DIR / f"{case_id}.json").resolve()
    if BUNDLES_DIR.resolve() not in p.parents:       # path-traversal guard (case_id from the wire)
        raise RunError(f"illegal case id '{case_id}'")
    if not p.exists():
        raise RunError(f"vendored bundle missing for '{case_id}'")
    return p


def list_cases(index: dict | None = None) -> dict:
    """The queue payload: meta (coverage, gate funnel, exemplars) + per-case DISPLAY rows (NO txn
    bodies — the clutter detail is fetched per case via GET /case/<id>)."""
    idx = index or load_index()
    rows = []
    funnel: dict = {}
    for c in idx.get("cases", []):
        gate = c.get("confidence", {}).get("gate")
        funnel[gate] = funnel.get(gate, 0) + 1
        rows.append({k: c.get(k) for k in
                     ("case_id", "display", "kyc", "capabilities", "n_alerts", "n_txns",
                      "advisories", "confidence", "exemplar", "grounds_e2e", "e2e_note")})
    meta = dict(idx.get("meta", {}))
    meta["gate_funnel"] = funnel
    showcase = casefile_list()                       # Phase 73 — the authored north-star pair LEADS the queue
    meta["showcase_ids"] = [r["case_id"] for r in showcase]
    return {"badge": BADGE, "meta": meta, "cases": showcase + rows}


def case_detail(case_id: str, index: dict | None = None) -> dict:
    """The per-case CLUTTER payload: the full vendored bundle (KYC, accounts, every txn, alerts,
    counterparty edges) + the GROUNDED signal walk (flag->corpus, server-computed, model-free) + the
    curated entry (confidence/exemplar/gate). Beats 1+2 render entirely from this — no model call."""
    if is_casefile_id(case_id):                      # Phase 73 — the authored showcase pair (its own rich shape)
        return casefile_detail(case_id)
    idx = index or load_index()
    entry = _case_entry(idx, case_id)
    bundle = json.loads(_bundle_path(case_id).read_text(encoding="utf-8"))
    return {"badge": BADGE, "case": entry, "bundle": bundle, "signals": audit_walk(bundle)}


# ---- the LIVE gating engine (the precedent-confidence CONTROL, re-derived per request) ------------
# Phase 64: Phase 63 only DISPLAYED the baked gate. Here the routing is a LIVE control — route() over
# the session precedent + an adjustable policy. The HONESTY SEAM: routing keys on the REAL firing
# frequency (the §12-grounded sample size); the disposition direction it applies stays §14-illustrative.
def session_precedent(index: dict) -> dict:
    """The session precedent map = the committed REAL combo frequencies (a COPY the loop mutates; the
    server never persists it). A case's n_precedent IS its combo's frequency, so routing from this
    reproduces the baked gate under the default policy."""
    return dict(index.get("meta", {}).get("combo_frequency", {}))


def gate_cases(index: dict, policy: dict | None = None, precedent: dict | None = None) -> dict:
    """Route every case LIVE: route(session precedent for its combo, policy). Under the default policy +
    the committed precedent this reproduces the baked 129/52/19 funnel; adjust the policy knobs or grow
    the precedent (the loop) and the funnel re-derives. Pure — persists nothing."""
    policy = policy or GATING_POLICY
    pre = session_precedent(index) if precedent is None else precedent
    funnel: dict = {}
    rows = []
    for c in index.get("cases", []):
        conf = c.get("confidence", {})
        combo = conf.get("combo")
        n = pre.get(combo, conf.get("n_precedent", 0))
        r = route(n, policy)
        funnel[r["gate"]] = funnel.get(r["gate"], 0) + 1
        rows.append({"case_id": c.get("case_id"), "combo": combo, "n_precedent": n,
                     "baked_gate": conf.get("gate"), "baked_n": conf.get("n_precedent"),
                     "exemplar": c.get("exemplar"), **r})
    return {"badge": BADGE, "policy": policy, "funnel": funnel,
            "precedent_note": "session precedent = the REAL committed combo frequencies; the loop grows it",
            "disposition_note": "ROUTING is §12-grounded (real firing frequency); the DISPOSITION it "
                                "applies stays §14-ILLUSTRATIVE — the gate decides WHERE judgment is "
                                "spent, never that an auto-disposition is correct",
            "cases": rows}


def policy_from_query(qs: str) -> dict:
    """Build a gating policy from /gate query params (the live KNOBS): high=<int>&medium=<int>. Missing
    params fall back to the default. Invalid values raise RunError (surfaced as a 400)."""
    from urllib.parse import parse_qs
    q = parse_qs(qs)
    pol = json.loads(json.dumps(GATING_POLICY))   # deep copy — never mutate the shared default
    for level in ("high", "medium"):
        if level in q:
            try:
                pol["thresholds"][level] = int(q[level][0])
            except (ValueError, IndexError):
                raise RunError(f"bad gating knob {level}={q.get(level)!r} — must be an integer sample-size floor")
    if pol["thresholds"]["high"] < pol["thresholds"]["medium"]:
        raise RunError("policy invalid: the high (auto-clear) threshold must be >= the medium (review) threshold")
    return pol


# ---- the elicitation LOOP (Phase 64 T2 — blueprint §14's continuous adjudication loop, made live) --
# A human adjudicates a gated case -> that disposition becomes PRECEDENT -> the combo's sample grows ->
# confidence recomputes -> the next similar case may re-route toward auto. SESSION-ONLY: the precedent +
# ledger live in memory and are NEVER written to disk (committing a record stays a human-reviewed act).
DISPOSITION_VOCAB = ("cleared", "escalated", "needs_more_info")


def new_session(index: dict | None = None) -> dict:
    """A fresh in-memory session: precedent = a COPY of the committed REAL combo frequencies; an empty
    adjudication ledger. The server holds ONE of these; /adjudicate mutates it; nothing persists."""
    return {"precedent": session_precedent(index or load_index()), "ledger": {}}


def adjudicate(index: dict, session: dict, case_id: str, disposition: str,
               policy: dict | None = None, weight: int = 1) -> dict:
    """Record a human disposition on a gated case and GROW the session precedent for its fired-signal
    combo, then re-derive routing. Mutates `session` (precedent + ledger) IN MEMORY; never touches disk.
    THE HONESTY SEAM: only the precedent COUNT grows (the §12-grounded sample size); the disposition
    DIRECTION is recorded but labeled ILLUSTRATIVE and does NOT feed routing — the loop demonstrates
    human judgment CONCENTRATING on sparse/novel patterns, never that an auto-disposition is correct."""
    if disposition not in DISPOSITION_VOCAB:
        raise RunError(f"unknown disposition '{disposition}' — one of {DISPOSITION_VOCAB}")
    entry = _case_entry(index, case_id)                      # validates the case exists
    combo = entry.get("confidence", {}).get("combo")
    pol = policy or GATING_POLICY
    pre = session["precedent"]
    before = route(pre.get(combo, 0), pol)
    pre[combo] = pre.get(combo, 0) + weight                  # one adjudication = one precedent data point
    session["ledger"].setdefault(combo, []).append(
        {"case_id": case_id, "disposition": disposition, "illustrative": True})
    after = route(pre[combo], pol)
    view = gate_cases(index, pol, pre)
    return {"badge": BADGE, "case_id": case_id, "combo": combo,
            "disposition_recorded": {"value": disposition,
                "basis": "ILLUSTRATIVE — label-blind; recorded as precedent VOLUME, not a correctness signal"},
            "before": before, "after": after, "rerouted": before["gate"] != after["gate"],
            "n_precedent": pre[combo], "combo_adjudications": len(session["ledger"][combo]),
            "funnel": view["funnel"], "cases": view["cases"]}


# ---- the casework consume — a REFUSAL is a disposition outcome, not a crash (the embrace-fail-closed) -
def casework_consume_wb(bundle_path: Path, out_path: Path, drafter: str) -> dict:
    """Like serve_chain.casework_consume, but a casework REFUSAL (it ran + wrote an UNSIGNED SAR because
    the six Class-G verifiers couldn't independently reproduce a signal — the substrate↔casework C3/C15
    divergence) is a RETURNED outcome (signed:false + blocking_violations), NOT a raised error. Only a
    genuine launch/crash (no SAR written) raises. The verifier is the oracle — we surface its verdict."""
    src = sc.CASEWORK_DIR / "src"
    py = sc.casework_python()                     # cross-platform venv resolution (Phase 67)
    if not src.exists():
        raise RunError(f"aml-casework not found at {sc.CASEWORK_DIR} (set AML_CASEWORK_DIR) — the consume "
                       f"is the sibling prerequisite; the finale is GATED until it lands")
    env = dict(os.environ)
    env["PYTHONPATH"] = str(src) + os.pathsep + env.get("PYTHONPATH", "")
    env.update(sc.casework_corpus_env())
    env.setdefault("OPENAI_BASE_URL", sc.DEFAULT_OPENAI_BASE)   # the openai drafter defaults to the local model
    cmd = [py, "-m", "aml_casework.ingest", str(bundle_path), "--out", str(out_path), "--drafter", drafter]
    try:
        proc = subprocess.run(cmd, cwd=str(sc.CASEWORK_DIR), env=env, capture_output=True,
                              text=True, timeout=300)
    except (OSError, subprocess.SubprocessError) as ex:
        raise RunError(f"casework consume could not be launched: {ex}") from None
    if not out_path.exists():
        tail = (proc.stderr or proc.stdout or "").strip().splitlines()[-3:]
        raise RunError("casework consume crashed (no SAR written): " + " | ".join(tail))
    return sc._consume_result_from_sar(json.loads(out_path.read_text(encoding="utf-8")), drafter)


# ---- the live finale (REUSES serve_chain's verify + audit; consume = the fail-closed-aware variant) --
def run_case(case_id: str, *, on_stage, consume=casework_consume_wb, verify=verify_e2e,
             drafter: str | None = None, tmpdir: Path | None = None, env: dict | None = None) -> dict:
    """Drive one workbench case through the LIVE finale, emitting NDJSON stages via on_stage. A casework
    REFUSAL (fail-closed) is a legitimate DISPOSITION (escalate to a human), not an error — the
    defensibility climax: the case-investigation pillar won't sign what its own detector fired but it
    can't independently reproduce. A signed case runs the cross-pillar verify → file. A genuine crash
    raises a NAMED RunError (in-stream)."""
    index = load_index()
    entry = _case_entry(index, case_id)
    bundle_path = _bundle_path(case_id)
    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))

    on_stage("evidence", case_id=case_id,
             alert_count=len(bundle.get("alerts", [])), txn_count=len(bundle.get("transactions", [])),
             capabilities=entry.get("capabilities", []), subject=bundle.get("subject", {}))

    resolved = resolve_backend(drafter, env)
    eff = resolved["effective"]
    on_stage("consume", drafter=eff, requested=resolved["requested"],
             available=resolved["available"], note=resolved["note"], status="running")
    tdir = tmpdir or Path(os.environ.get("TMPDIR", "/tmp"))
    signed_path = tdir / f"{case_id}-signed.json"
    consume_res = consume(bundle_path, signed_path, eff)
    on_stage("consume", status="done", **consume_res)
    signed = consume_res["signed"]

    if signed:
        on_stage("verify", status="running")
        verify_res = verify(bundle_path, signed_path)
        on_stage("verify", status="done", connected=verify_res["connected"], exit=verify_res["exit"])
        connected = verify_res["connected"]
        disposition = "file" if connected else "needs_more_info"
    else:
        # fail-closed: the verifiers refused — skip the cross-pillar verify, escalate to a human
        verify_res = {"connected": False, "exit": None, "skipped": "unsigned"}
        on_stage("verify", status="skipped", connected=False,
                 note="casework did not sign — the cross-pillar verify is moot; escalating to a human")
        connected = False
        disposition = "escalate"

    signed_sar = json.loads(signed_path.read_text(encoding="utf-8")) if signed_path.exists() else None
    payload = {
        "case": {k: entry.get(k) for k in ("case_id", "display", "confidence", "exemplar")},
        "consume": consume_res,
        "verify": verify_res,
        "signed_sar": signed_sar,
        "audit_walk": audit_walk(bundle),
        "connected": connected,
        "disposition": disposition,
        "fail_closed": not signed,
    }
    on_stage("connected", connected=connected, disposition=disposition, fail_closed=not signed,
             blocking_violations=consume_res.get("blocking_violations", []))
    return payload


# ---- the GATHER beat (Phase 65): the OSINT evidence-gathering agent loop ---------------------------
# On a selected case the agent loop calls deterministic tools over the COMMITTED SYNTHETIC OSINT corpus;
# each finding is GROUNDED-OR-STRIPPED by the shared news_ground gate (osint_tools), grounded evidence
# extends the case grounding chain + feeds a network view. Read-only; persists nothing; stateless across
# requests; the browser sends a backend NAME only — call_openai errors are sanitized in osint_tools (no
# host/url reaches a stage). build.py never imports osint_tools (companion-only, no ship target).
_OSINT = {"corpus": None, "index": None}


def osint_corpus() -> tuple:
    """Load + VALIDATE the synthetic OSINT corpus once (fail-loud if the disclaimer/shape is wrong — a
    synthetic corpus never serves undisclosed). Cached read-only; never mutated."""
    if _OSINT["corpus"] is None:
        c = osint_load_corpus()
        errs = validate_osint_corpus(c)
        if errs:
            raise RunError("data/osint/corpus.json failed validation: " + "; ".join(errs[:4]))
        _OSINT["corpus"], _OSINT["index"] = c, osint_build_index(c)
    return _OSINT["corpus"], _OSINT["index"]


def gather_demo_case_id(index: dict, corpus: dict | None = None) -> str:
    """The scripted gather/finale DEMO case, resolved DETERMINISTICALLY from the OSINT corpus — NOT the
    volatile 'mule' exemplar. Phase 72: a population re-curate moves the richest-composition exemplar
    (the C14 emission inflated some cases' alert counts), but the hand-crafted chained-discovery corpus
    is tailored to ONE subject (owner -> affiliate -> sanctions hit). Returns the lowest-case_id slice
    case whose synthetic display name keys an OSINT registry record with a relationship to a SANCTIONS-
    listed entity (the designed chain). Falls back to the mule exemplar if the corpus has no such chain,
    so the demo never crashes — it just loses the scripted narrative."""
    corpus = corpus or osint_corpus()[0]
    sanctioned = set(corpus.get("sanctions", {}))
    chain_subjects = {subj for subj, recs in corpus.get("registry", {}).items()
                      for r in recs for rel in r.get("relationships", [])
                      if rel.get("dst") in sanctioned}
    cands = [c for c in index["cases"] if c["display"]["name"] in chain_subjects]
    if not cands:
        return index["meta"]["exemplars"]["mule"]
    return min(cands, key=lambda c: c["case_id"])["case_id"]


def gather_view(entry: dict, bundle: dict) -> dict:
    """The investigator context the agent loop reasons over: the SYNTHETIC display identity + kind + the
    real counterparty refs (context only — the corpus is keyed by named entities, refs honestly miss)."""
    d = entry.get("display") or {}
    cps = []
    for t in (bundle.get("transactions") or []):
        ref = t.get("counterparty_ref") or t.get("counterparty_account_id")
        if ref and ref not in cps:
            cps.append(ref)
    return {"subject_name": d.get("name") or entry.get("case_id"),
            "subject_kind": d.get("kind") or "subject", "counterparties": cps[:12],
            "capabilities": entry.get("capabilities", [])}


def run_gather(case_id: str, *, on_stage, backend: str | None = None, env: dict | None = None,
               planner=None) -> dict:
    """Drive one case through the GATHER loop, emitting NDJSON stages. Resolves the chat backend SERVER-SIDE
    (the browser sent a NAME only) and echoes a NAME-only backend stage; the openai path streams nothing and
    sanitizes transport errors in osint_tools. Pure over the read-only corpus — persists nothing."""
    index = load_index()
    entry = _case_entry(index, case_id)
    bundle = json.loads(_bundle_path(case_id).read_text(encoding="utf-8"))
    corpus, oidx = osint_corpus()
    cv = gather_view(entry, bundle)
    be = resolve_gather_backend(backend, env)
    on_stage("backend", requested=be.get("requested"), effective=be.get("effective"), note=be.get("note"))

    # Phase 69 — REQUIREMENT-TARGETED gather: derive the case's crime_type + the atoms already carried by its
    # fired signals, then NAME the unmet determination atoms a gather pass could close (network / corroboration)
    # BEFORE running. This is the difference between additive discovery and seeking the evidence a determination
    # actually needs.
    prof = _requirements()
    caps = _entry_caps(entry)
    ctype = crime_type_for_capabilities(caps, prof)
    present_before = present_atoms(ctype, caps, prof) if ctype else []
    targets = gather_targets(ctype, present_before, prof) if ctype else []
    on_stage("requirement", crime_type=ctype, present_before=present_before,
             targets=[{"id": t["id"], "label": t["label"]} for t in targets])

    if planner is None:
        planner = (LivePlanner(cv, lambda msgs: call_openai(msgs, env))
                   if be.get("effective") == "openai" else StubPlanner(cv, oidx))
    result = osint_gather(cv, on_stage=on_stage, corpus=corpus, index=oidx, planner=planner, backend_note=be)

    # which targeted atoms the record-sourced findings CLOSED (vs the gaps that stay open → the §12 brief).
    gathered = gathered_signals(result.get("grounded", []))
    present_after = present_atoms(ctype, caps, prof, gathered=gathered) if ctype else []
    closed_ids = [t for t in present_after if t not in present_before]
    target_ids = {t["id"] for t in targets}
    result["requirement"] = {
        "crime_type": ctype,
        "present_before": present_before, "present_after": present_after, "gathered_signals": gathered,
        "targets": [{"id": t["id"], "label": t["label"]} for t in targets],
        "closed": [{"id": tid, "label": next((t["label"] for t in targets if t["id"] == tid), tid)}
                   for tid in closed_ids if tid in target_ids],
        "still_open": [{"id": t["id"], "label": t["label"]} for t in targets if t["id"] not in closed_ids],
    }
    # Phase 70 — the requirement-targeted CLOSURE rate (the second coverage dimension: of the unmet atoms a
    # gather COULD close, how many it did). 1.0 == the gather closed every closeable gap (the stub reference).
    req = result["requirement"]
    req["target_closure"] = round(len(req["closed"]) / len(targets), 3) if targets else None
    return result


# ---- the DIFFERENTIATED DETERMINATION (Phase 69 T4) — sufficiency supersedes frequency ------------
def determine_case(case_id: str, *, gathered=(), named_risk: str | None = None,
                   mitigation_rebutted: bool = False, index: dict | None = None,
                   precedent: dict | None = None) -> dict:
    """The DETERMINATION for one case: licensed by evidence-SUFFICIENCY (mechanism + corroborating legs +
    a NAMED predicate risk + no unrebutted mitigation), NOT combo-frequency. The Phase-64 frequency gate is
    DEMOTED to CONTEXT for the contrast — it decides WHERE to spend judgment (§12), never that a
    determination holds. Insufficiency is a legitimate non-decision whose `missing` NAMES the gap. Pure;
    persists nothing. named_risk + mitigation_rebutted are the HUMAN elicitation inputs (the gate where a
    person fills what the data cannot)."""
    if is_casefile_id(case_id):                      # Phase 73 — the authored pair computes via the SAME engine
        return casefile_determination(case_id)
    index = index or load_index()
    entry = _case_entry(index, case_id)
    prof = _requirements()
    caps = _entry_caps(entry)
    ctype = crime_type_for_capabilities(caps, prof)
    det = (determine(ctype, caps, prof, gathered=gathered, named_predicate_risk=bool(named_risk),
                     mitigation_rebutted=mitigation_rebutted) if ctype else None)
    conf = entry.get("confidence", {})
    combo = conf.get("combo")
    n = (precedent or session_precedent(index)).get(combo, conf.get("n_precedent", 0))
    freq = route(n)
    return {"badge": BADGE, "case_id": case_id, "crime_type": ctype, "named_risk": named_risk or None,
            "determination": det,
            "frequency_context": {"combo": combo, "n_precedent": n, "gate": freq["gate"],
                                  "note": "precedent FREQUENCY — context for WHERE to spend judgment, "
                                          "never the determination trigger"},
            "supersedes": ("the determination is licensed by evidence-sufficiency; the Phase-64 frequency "
                           "gate is context only — seeing a combo more often is not a determination")}


# ---- the authored NORTH-STAR case file (Phase 73) — the rich matched pair, COMPUTED by the live engine
# A SEPARATE source from the vendored population: two AUTHORED cases (data/casefile/case.json) whose verdict
# is COMPUTED live by the same evidence_requirements engine. The engine inputs are DERIVED FROM THE EVIDENCE
# (the fired alerts, the source-of-funds finding read from the file, the resolved network, the caution-list /
# prior-STR record hits) — never from the authored expected verdict. The file/determination bar is unchanged;
# the affirmative-clear branch supplies the documented-dismissal when the benign explanation is established.
CASEFILE_JSON = ROOT / "data" / "casefile" / "case.json"
_CASEFILE_CACHE: dict = {}


def load_casefile() -> dict:
    """The committed authored matched pair, cached read-only. Companion-only; build.py never reads it."""
    if "d" not in _CASEFILE_CACHE:
        _CASEFILE_CACHE["d"] = json.loads(CASEFILE_JSON.read_text(encoding="utf-8"))
    return _CASEFILE_CACHE["d"]


def casefile_case(case_id: str):
    for c in load_casefile().get("cases", []):
        if c.get("case_id") == case_id:
            return c
    return None


def is_casefile_id(case_id: str) -> bool:
    return casefile_case(case_id) is not None


def _cf_entities(case: dict) -> dict:
    return {e["entity_id"]: e for e in case.get("entities", [])}


def _cf_caution_hit(case: dict, ents: dict, ref: dict):
    """A caution-list ADDRESS hit reached THROUGH the ownership chain (a beneficial owner registered at a
    caution-listed address). Record-sourced from reference.caution_list — never model-authored."""
    cl_by = {c["address"]["normalized"]: c for c in ref.get("caution_list", [])
             if c.get("kind") == "address" and (c.get("address") or {}).get("normalized")}
    for o in case.get("ownership_edges", []):
        addr = ((ents.get(o.get("src"), {}).get("identity") or {}).get("address") or {}).get("normalized")
        if addr in cl_by:
            return {"caution": cl_by[addr], "owner": o.get("src"), "chain": [o.get("dst"), o.get("src")]}
    return None


def _norm_email(e) -> str:
    """The casefile email-normalization convention (lowercase, drop dots in the local part) — mirrors the
    `normalized` form stored on entity identifiers, so a register entry carrying only a raw `email` still matches."""
    e = str(e or "").strip().lower()
    if "@" not in e:
        return e
    loc, dom = e.split("@", 1)
    return loc.replace(".", "") + "@" + dom


def _cf_prior_str_hit(case: dict, ents: dict, ref: dict):
    """A prior-STR match on an INBOUND source counterparty (exact on the normalized email). Record-sourced
    from reference.prior_str_register — supplies the named predicate risk (read, not analyst-typed)."""
    reg = {}
    for r in ref.get("prior_str_register", []):
        ids = r.get("identifiers") or {}
        for v in (ids.get("normalized_email"), _norm_email(ids.get("email"))):   # both keyed to the normalized form
            if v:
                reg[v] = r
    for t in case.get("transactions", []):
        if t.get("direction") != "CREDIT":
            continue
        ent = ents.get((t.get("counterparty") or {}).get("entity_ref"), {})
        for i in ent.get("identifiers", []):
            if i.get("normalized") in reg:
                return {"prior_str": reg[i["normalized"]], "source": ent.get("entity_id"), "txn": t.get("txn_id")}
    return None


def _cf_read_manifest(case: dict) -> tuple:
    """GRADE-GATE the read-from-file network atom (ML-A4) against the case's resolution edges, using the
    spine's grammar (max_grade over each resolved/flagged edge's shared-identifier strengths). A strong/weak
    edge ADMITS ML-A4; a reject/empty (name-only) edge is EXCLUDED — the boolean file bar cannot express
    "weak", so a low-grade link is excluded, never down-weighted (docs/confidence-as-provenance-contract.md).
    Returns (read_atoms, manifest) — the manifest lists every candidate as admitted | quarantined-by-low-grade,
    so the file/clear is auditable down to the link grade that supplied each leg."""
    admitted, manifest = [], []
    for e in case.get("resolution_edges", []):
        if e.get("status") not in ("resolved", "flagged"):
            continue   # an excluded/other edge never supplies a read atom
        shared = e.get("shared") or []
        grade = max_grade(s.get("strength") for s in shared)   # strong/weak/reject; empty -> reject (fail-closed)
        entry = {"atom": "ML-A4", "via": "resolution-edge", "between": e.get("between"),
                 "grade": grade, "basis": [s.get("kind") for s in shared]}
        if grade in ("strong", "weak"):
            entry["status"] = "admitted"
            admitted.append("ML-A4")
        else:
            entry["status"] = "quarantined-by-low-grade"
            entry["reason"] = ("resolution edge has no strong/weak shared identifier (name-only / empty) — "
                               "excluded from the filing inputs, never down-weighted")
        manifest.append(entry)
    return sorted(set(admitted)), manifest


def casefile_determination(case_id: str) -> dict:
    """COMPUTE the determination for an authored case by DERIVING the engine inputs from its EVIDENCE and
    running the LIVE engine — the verdict is engine OUTPUT, never the authored expected_*. The honest seam:
    BOTH cases fire C14 (source-of-funds question), but `kyc.source_of_funds` read from the file flips the
    leg — Northgate null (ML-A7 lights, the benign explanation is rebutted by adverse corroboration) vs
    Lakeshore established (ML-A7 mitigated away, mitigation AFFIRMATIVELY established → the clear branch)."""
    cf = load_casefile()
    case = casefile_case(case_id)
    if case is None:
        raise RunError(f"unknown case '{case_id}' — not in the authored case file (data/casefile/case.json)")
    ref = cf.get("reference", {})
    prof = _requirements()
    ents = _cf_entities(case)
    subj = ents.get((case.get("subject") or {}).get("entity_ref"), {})
    sof = (subj.get("kyc") or {}).get("source_of_funds")
    source_established = bool(sof and str(sof).strip())

    caution = _cf_caution_hit(case, ents, ref)
    prior = _cf_prior_str_hit(case, ents, ref)
    gathered = ["corroboration"] if (caution or prior) else []
    read, read_manifest = _cf_read_manifest(case)   # grade-gated: a low-grade link is EXCLUDED, not down-weighted
    named_risk = ((prior or {}).get("prior_str") or {}).get("predicate")
    mitigation_established = source_established
    mitigation_rebutted = (not source_established) and bool(gathered)
    suppress = {"ML-A6", "ML-A7"} if source_established else set()

    caps = sorted({a.get("capability") for a in case.get("alerts", []) if a.get("capability")})
    ctype = crime_type_for_capabilities(caps, prof) or "money_laundering"
    present = [a for a in present_atoms(ctype, caps, prof, gathered=gathered, read=read) if a not in suppress]
    suff = evaluate_sufficiency(ctype, present, named_predicate_risk=bool(named_risk),
                                mitigation_rebutted=mitigation_rebutted, profile=prof,
                                required_elements_satisfied=True, mitigation_established=mitigation_established)
    verdict = suff["verdict"]
    disposition = {"determination": "escalated", "cleared": "cleared"}.get(verdict, "needs_more_info")
    label = {"determination": "file", "cleared": "documented_dismissal"}.get(verdict, "needs_more_info")

    spec_atoms = {a["id"]: a for a in prof["crime_types"].get(ctype, {}).get("atoms", [])}

    def _via(aid: str) -> str:
        atom = spec_atoms.get(aid, {})
        if set(atom.get("evidence", [])) & set(caps):
            return "fired"
        if aid in read:
            return "read"
        if atom.get("gather_signal") in gathered:
            return "gathered"
        return "present"   # neutral — never claim a provenance (fired/read/gathered) the atom didn't earn

    atoms_view = [{"atom": aid, "name": spec_atoms.get(aid, {}).get("label"),
                   "kind": spec_atoms.get(aid, {}).get("kind"), "via": _via(aid)} for aid in present]
    det = case.get("determination", {})
    return {"badge": BADGE, "case_id": case_id, "showcase": True, "crime_type": ctype, "verdict": verdict,
            "disposition": disposition, "presentation_label": label, "named_risk": named_risk,
            "mitigation_established": mitigation_established, "mitigation_rebutted": mitigation_rebutted,
            "present_atoms": atoms_view, "missing": suff["missing"], "sufficiency_line": det.get("sufficiency_line"),
            # the per-decision GRADE manifest — each read atom admitted | quarantined-by-low-grade (auditable)
            "read_manifest": read_manifest,
            "evidence_hits": {"caution_list": caution, "prior_str": prior, "source_established": source_established},
            "str_record": det.get("str_record"), "clearance_record": det.get("clearance_record"),
            # the authored expectation is a REGRESSION ORACLE only — never the served verdict (that is computed above)
            "expected": {"verdict": det.get("expected_verdict"), "label": det.get("presentation_label")},
            "expectation_match": verdict == det.get("expected_verdict")}


def casefile_list() -> list:
    """The showcase queue rows (the authored pair), surfaced at the TOP of the queue. Each carries the
    COMPUTED presentation label + a showcase marker; the rich detail is fetched via GET /case/<id>."""
    rows = []
    for case in load_casefile().get("cases", []):
        ents = _cf_entities(case)
        subj = ents.get((case.get("subject") or {}).get("entity_ref"), {})
        det = casefile_determination(case["case_id"])
        rows.append({"case_id": case["case_id"], "showcase": True,
                     "display": {"name": case.get("display_name"), "kind": subj.get("kind"), "synthetic_label": True},
                     "kyc": subj.get("kyc"),
                     "capabilities": sorted({a.get("capability") for a in case.get("alerts", []) if a.get("capability")}),
                     "n_alerts": len(case.get("alerts", [])), "n_txns": len(case.get("transactions", [])),
                     "presentation_label": det["presentation_label"], "verdict": det["verdict"],
                     "predicate": det.get("named_risk")})
    return rows


def casefile_detail(case_id: str) -> dict:
    """The full authored case evidence + the COMPUTED determination — everything the rich-case render needs."""
    cf = load_casefile()
    case = casefile_case(case_id)
    if case is None:
        raise RunError(f"unknown case '{case_id}' — not in the authored case file")
    return {"badge": BADGE, "showcase": True, "case": case, "reference": cf.get("reference", {}),
            "meta": cf.get("meta", {}), "determination": casefile_determination(case_id)}


# ---- the re-surfacing MEMORY demo (Phase 74) -----------------------------------------------------
# The genuine persistent entity store (gitignored runtime data; 127.0.0.1; never committed, never a dist).
SPINE_STORE = ROOT / "data" / "entity-spine" / "store" / "workbench-spine.duckdb"


def _accumulate_priors(spine, cf: dict) -> None:
    """Observe every case's entities into the spine (so a re-surfacing entity resolves by identifier), and
    attach the prior-STR register records as INDEPENDENT-provenance prior dispositions on the resolved
    subjects (a prior STR is authored separately — it is not hand-set to steer any later verdict)."""
    for case in cf.get("cases", []):
        for e in case.get("entities", []):
            spine.observe(case["case_id"], {"entity_id": e["entity_id"], "display_name": e.get("display_name"),
                          "kind": e.get("kind"), "role": e.get("role"), "identifiers": e.get("identifiers") or []})
    for r in cf.get("reference", {}).get("prior_str_register", []):
        ids = r.get("identifiers") or {}
        nem = ids.get("normalized_email") or _norm_email(ids.get("email"))
        if not nem:
            continue
        res = spine.observe("PSR:" + r["id"], {"entity_id": r["id"], "display_name": r.get("subject_name"),
                            "kind": "person", "role": "prior_str",
                            "identifiers": [{"kind": "email", "value": ids.get("email"), "normalized": nem,
                                             "strength": "strong"}]})
        spine.attach_disposition(res["entity_id"], "PSR:" + r["id"], "escalated",
                                 grounding={"prior_str_id": r.get("prior_str_id"), "predicate": r.get("predicate"),
                                            "source": "prior_str_register"}, decided_at="2023-01-01")


def casefile_memory(store_path: str = ":memory:") -> dict:
    """The re-surfacing MEMORY demo: Vesna Maric resurfaces as a subject; the persistent spine resolves her
    by the shared STRONG email across CASE-A + the INDEPENDENT prior-STR register + this case and surfaces her
    accumulated prior — so the gather targets-to-close SHRINK (a MEASURED number, not a status flag) and the
    predicate is already named. Also exercises the genuine write-then-read-back seam + the event-driven
    stale-prior guard. Confidence/priors ride this SEPARATE path — never through the byte-frozen file bar."""
    cf = load_casefile()
    rs = cf.get("resurfacing") or {}
    prof = _requirements()
    subj_e = (rs.get("entities") or [{}])[0]
    caps = sorted({a.get("capability") for a in rs.get("alerts", []) if a.get("capability")})
    ctype = crime_type_for_capabilities(caps, prof) or "money_laundering"
    # COLD — the re-surfacing case's own signals, no memory (the investigator gathers from scratch)
    cold_present = present_atoms(ctype, caps, prof)
    cold_targets = [t["id"] for t in gather_targets(ctype, cold_present, prof)]

    spine = EntitySpine(store_path)
    try:
        _accumulate_priors(spine, cf)
        res = spine.observe(rs.get("case_id", ""), {"entity_id": subj_e.get("entity_id"),
              "display_name": subj_e.get("display_name"), "kind": "person", "role": "subject",
              "identifiers": subj_e.get("identifiers") or []})
        eid = res["entity_id"]
        priors = spine.prior_dispositions(eid)
        # persistence: write-then-read-back across a store REOPEN (only meaningful on a file store)
        read_back = None
        if store_path != ":memory:":
            spine.close()
            spine = EntitySpine(store_path)
            read_back = len(spine.prior_dispositions(eid))
        prior_predicate = next((p["grounding"].get("predicate") for p in priors if p["grounding"].get("predicate")), None)
        # MEMORY — the prior STR is external corroboration -> closes the corroboration gather-target
        memory_present = present_atoms(ctype, caps, prof, gathered=(["corroboration"] if priors else []))
        memory_targets = [t["id"] for t in gather_targets(ctype, memory_present, prof)]
        # the event-driven STALE-PRIOR guard: a split (retract a link) bumps the version -> the prior reads stale
        link = spine.con.execute(
            "SELECT link_id FROM resolution_links WHERE entity_id=? AND status='active' LIMIT 1", [eid]).fetchone()
        stale_after_split = None
        if link:
            spine.retract_link(link[0])
            after = spine.prior_dispositions(eid)
            stale_after_split = bool(after) and all(p["stale"] for p in after)
    finally:
        spine.close()

    return {"badge": BADGE, "case_id": rs.get("case_id"), "display_name": rs.get("display_name"),
            "resolves_via": rs.get("expected_memory", {}).get("resolves_via"),
            "subject_entity": eid, "n_priors": len(priors), "prior_predicate": prior_predicate,
            "prior_source": (priors[0]["record_id"] if priors else None),
            "cold_targets": cold_targets, "memory_targets": memory_targets,
            "targets_shrink": len(cold_targets) - len(memory_targets),
            "predicate_pre_named_by_memory": bool(prior_predicate),
            "persisted_read_back": read_back, "stale_after_split": stale_after_split,
            "expected": rs.get("expected_memory")}


# ---- the REAL-DATA cross-case memory over the curated substrate slice (Phase 75) -----------------
def _observe_substrate_party(spine, case_id: str, party: dict):
    """Observe one substrate party into the spine keyed on `entity_ref` — substrate's RELIABLE declared
    identity (party_id; 100% name-consistent) — the STRONG merge key. Substrate's shared contact identifiers
    (email/phone) are DEMOTED to `weak` candidate-SHARES links: its deliberate collision noise floor +
    controller-cluster SHARES make a shared identifier NON-discriminative for identity (the T1 over-merge
    trap), so they corroborate-and-render but NEVER drive a merge. Returns (entity_ref, observe-result)."""
    eref = party.get("entity_ref") or party.get("party_id")
    if not eref:
        return None
    idents = [{"kind": "entity_ref", "value": eref, "normalized": eref, "strength": "strong"}]
    for i in (party.get("identifiers") or []):
        if i.get("kind") in ("email", "phone") and i.get("normalized"):
            idents.append({"kind": i["kind"], "value": i.get("value"),
                           "normalized": i["normalized"], "strength": "weak"})   # candidate SHARES, NOT a merge key
    res = spine.observe(case_id, {"entity_id": eref, "display_name": party.get("display_name"),
                                  "kind": "person" if party.get("is_person") else "org",
                                  "role": party.get("label") or party.get("role"), "identifiers": idents})
    return eref, res


def substrate_memory(store_path: str = ":memory:", limit_cases: int | None = None) -> dict:
    """The REAL-DATA cross-case memory over the curated substrate slice (Phase 75 — the consume the user picked:
    "entity_ref memory + SHARES adjudication"). Accumulates every slice case's parties into the spine keyed on
    entity_ref, then MEASURES two honest numbers:
      - CO-REFERENCE: entity_refs re-surfacing in 2+ DISTINCT slice cases (the memory-lever signal — substrate
        ground truth: entity_ref==party_id is 100% name-consistent). A re-surfacing entity carries its prior
        cross-case context (which cases, what role) for free instead of re-gathering it cold.
      - SHARES ADJUDICATION: substrate emits `resolution_edges` (status:"resolved") for ANY shared-strong-id
        pair — but its own gen/identity.py plants those between DISTINCT entities (noise floor + controller
        clusters). The spine, keyed on entity_ref, keeps those endpoints DISTINCT — it REFUSES the over-merge
        substrate's naive resolution asserts. We count the candidate SHARES links the spine declined to merge.
    Every shared identifier stays a SHARES network edge, never a same-entity merge (the Phase-73 'fabricated
    coincidence' guard). The file/determination bar is UNTOUCHED — this is all spine/provenance path."""
    index = load_index()
    cases = index.get("cases", [])
    if limit_cases:
        cases = cases[:limit_cases]
    spine = EntitySpine(store_path)
    eref2eid: dict = {}
    edges: list = []                      # (case_id, A, B) for the SHARES adjudication
    try:
        for c in cases:
            cid = c.get("case_id")
            try:
                b = json.loads(_bundle_path(cid).read_text(encoding="utf-8"))
            except (RunError, OSError, json.JSONDecodeError):
                continue
            for p in (b.get("parties") or []) + (b.get("related_parties") or []):
                r = _observe_substrate_party(spine, cid, p)
                if r:
                    eref2eid[r[0]] = r[1]["entity_id"]
            for e in (b.get("resolution_edges") or []):
                btw = e.get("between") or []
                if isinstance(btw, list) and len(btw) == 2 and btw[0] != btw[1]:
                    edges.append((cid, btw[0], btw[1]))
        # SHARES adjudication: a substrate "resolved" edge between two DISTINCT entity_refs the spine kept apart
        refused_pairs, refused_examples = set(), []
        for cid, a, bb in edges:
            ea, eb = eref2eid.get(a), eref2eid.get(bb)
            if ea and eb and ea != eb:                 # the spine resolved both, kept them DISTINCT -> refused
                pair = tuple(sorted((a, bb)))
                if pair not in refused_pairs:
                    refused_pairs.add(pair)
                    if len(refused_examples) < 8:
                        refused_examples.append({"case_id": cid, "between": list(pair)})
        reappear = spine.entities_in_multiple_records(min_records=2)
    finally:
        spine.close()

    examples = [{"entity_id": e["entity_id"], "display_name": e["display_name"], "n_cases": e["n_records"],
                 "cases": e["records"][:6]} for e in reappear[:8]]
    return {
        "badge": BADGE,
        "n_cases_scanned": len(cases),
        "n_entities": len(eref2eid),
        "n_xcase_coref": len(reappear),                # entity_refs re-surfacing across 2+ slice cases
        "xcase_coref_examples": examples,
        "n_candidate_shares": len(refused_pairs),      # distinct substrate "resolved" pairs of DISTINCT entities
        "n_over_merge_refused": len(refused_pairs),     # ...all kept distinct: the spine refused the naive merge
        "over_merge_examples": refused_examples,
        "qualifier": ("synthetic substrate population; entity_ref==party_id is substrate's declared identity "
                      "(100% name-consistent — real co-reference). A shared strong identifier is a SHARES_* edge "
                      "between DISTINCT entities (substrate's collision noise floor + controller clusters), NEVER "
                      "a same-entity merge — the spine keys identity on entity_ref and ADJUDICATES the SHARES "
                      "candidates (over-merge refused). The file/determination bar is byte-unchanged."),
    }


# ---- the served page -----------------------------------------------------------------------------
def live_config(env: dict | None = None) -> dict:
    return {"cases": "/cases", "case": "/case", "gate": "/gate", "adjudicate": "/adjudicate", "memory": "/memory",
            "gather": "/gather", "run": "/run", "determine": "/determine", "health": "/health", "badge": BADGE,
            "policy": GATING_POLICY,              # the routing KNOBS (the live gating panel's defaults)
            "drafter": sc._drafter_config(env)}   # NAMES + booleans only (§4.5), reused verbatim


def render_page(cfg: dict) -> str:
    if not TEMPLATE.exists():
        return ("<!doctype html><meta charset=utf-8><title>Case workbench</title>"
                f"<body style='font-family:monospace;background:#0c0e12;color:#e9ebf0;padding:2rem'>"
                f"<h1>Investigator case workbench</h1><p>{BADGE}</p>"
                "<p>workbench.html is not built yet. The API is live: "
                "<code>GET /cases</code>, <code>GET /case/&lt;id&gt;</code>, <code>POST /run</code>.</p>")
    tpl = TEMPLATE.read_text(encoding="utf-8")
    n = tpl.count(PLACEHOLDER)
    if n != 1:
        raise RunError(f"expected exactly one {PLACEHOLDER} in workbench.html, found {n}")
    inject = f"<script>window.__WORKBENCH_CONFIG__ = {json.dumps(cfg, ensure_ascii=False)};</script>"
    return tpl.replace(PLACEHOLDER, inject)


# ---- HTTP ----------------------------------------------------------------------------------------
class Handler(BaseHTTPRequestHandler):
    server_version = "SignalWatchCaseWorkbench/0.1"

    def _send(self, code, body, ctype):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _json(self, code, obj):
        self._send(code, json.dumps(obj, ensure_ascii=False).encode("utf-8"),
                   "application/json; charset=utf-8")

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path in ("/", "/index.html"):
            self._send(200, render_page(live_config()).encode("utf-8"), "text/html; charset=utf-8")
        elif path == "/cases":
            self._json(200, list_cases())
        elif path.startswith("/case/"):
            try:
                self._json(200, case_detail(path[len("/case/"):]))
            except RunError as ex:
                self._json(404, {"error": str(ex)})
        elif path == "/gate":
            try:
                qs = self.path.split("?", 1)[1] if "?" in self.path else ""
                with self._session_lock():
                    sess = self._session()
                    self._json(200, gate_cases(load_index(), policy_from_query(qs), sess["precedent"]))
            except RunError as ex:
                self._json(400, {"error": str(ex)})
        elif path == "/health":
            self._json(200, {"ok": True, "live": True, "persist": False,
                             "drafter": default_backend(), "backends": available_backends(),
                             "cases": len(load_index().get("cases", []))})
        elif path == "/memory":
            # the persistent entity intelligence beat (Phase 75): the REAL-DATA cross-case memory over the
            # curated substrate slice (entity_ref-keyed co-reference + the SHARES over-merge adjudication) +
            # the casefile disposition-memory short-circuit (Vesna Maric). Read-only, :memory: store, persists
            # nothing; the file/determination bar is untouched (spine/provenance path).
            try:
                self._json(200, {"badge": BADGE, "substrate": substrate_memory(), "casefile": casefile_memory()})
            except RunError as ex:
                self._json(400, {"error": str(ex)})
        else:
            self._json(404, {"error": f"not found: {path}"})

    def do_POST(self):
        p = self.path.split("?", 1)[0]
        if p == "/run":
            self._run(); return
        if p == "/gather":
            self._gather(); return
        if p == "/determine":
            self._determine(); return
        if p == "/adjudicate":
            self._adjudicate(); return
        self._json(404, {"error": f"not found: {self.path}"})

    def _determine(self):
        payload, err = self._read_json()
        if err:
            self._json(400, {"error": err}); return
        case_id = (payload.get("case") or payload.get("case_id") or "").strip()
        if not case_id:
            self._json(400, {"error": "missing 'case' (the case_id to determine; GET /cases lists them)"}); return
        named_risk = (payload.get("named_risk") or "").strip() or None
        mitigation_rebutted = bool(payload.get("mitigation_rebutted"))
        gathered = payload.get("gathered")
        gathered = gathered if isinstance(gathered, list) else []
        try:
            self._json(200, determine_case(case_id, gathered=gathered, named_risk=named_risk,
                                           mitigation_rebutted=mitigation_rebutted))
        except RunError as ex:
            self._json(400, {"error": str(ex)})

    # ---- the session: in-memory precedent + ledger the elicitation loop mutates (persists NOTHING) ----
    def _session_lock(self):
        return self.server.__dict__.setdefault("session_lock", threading.Lock())

    def _session(self):
        return self.server.__dict__.setdefault("session", new_session())

    @staticmethod
    def _policy_from_payload(payload):
        pol = payload.get("policy") or {}
        parts = [f"{lvl}={pol.get(lvl, payload.get(lvl))}" for lvl in ("high", "medium")
                 if lvl in pol or lvl in payload]
        return policy_from_query("&".join(parts)) if parts else None

    def _adjudicate(self):
        payload, err = self._read_json()
        if err:
            self._json(400, {"error": err}); return
        with self._session_lock():
            index = load_index()
            if payload.get("reset"):     # the demo/test reset — back to the committed baseline precedent
                self.server.__dict__["session"] = new_session(index)
                view = gate_cases(index, None, self.server.__dict__["session"]["precedent"])
                self._json(200, {"badge": BADGE, "reset": True, "funnel": view["funnel"],
                                 "cases": view["cases"]}); return
            case_id = (payload.get("case") or payload.get("case_id") or "").strip()
            if not case_id:
                self._json(400, {"error": "missing 'case' (the case_id to adjudicate; GET /cases lists them)"}); return
            disposition = (payload.get("disposition") or "").strip()
            try:
                out = adjudicate(index, self._session(), case_id, disposition,
                                 self._policy_from_payload(payload))
                self._json(200, out)
            except RunError as ex:
                self._json(400, {"error": str(ex)})

    def _gather(self):
        payload, err = self._read_json()
        if err:
            self._json(400, {"error": err}); return
        case_id = (payload.get("case") or payload.get("case_id") or "").strip()
        if not case_id:
            self._json(400, {"error": "missing 'case' (the case_id to gather; GET /cases lists them)"}); return
        backend = (payload.get("backend") or payload.get("drafter") or "").strip() or None
        # single-flight: a second concurrent gather would split a live model's throughput
        lock = self.server.__dict__.setdefault("gather_lock", threading.Lock())
        if not lock.acquire(blocking=False):
            self._json(409, {"error": "another gather is already running — wait for it to finish"}); return
        try:
            self.send_response(200)
            self.send_header("Content-Type", "application/x-ndjson; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            try:
                out = run_gather(case_id, backend=backend,
                                 on_stage=lambda stage, **kw: self._emit({"stage": stage, **kw}))
                self._emit({"done": out})
            except RunError as ex:
                self._emit({"error": str(ex)})
            except (OSError, ValueError, KeyError, json.JSONDecodeError) as ex:
                self._emit({"error": f"gather failed: {ex}"})
        except (BrokenPipeError, ConnectionResetError):
            self.log_message("client disconnected mid-gather stream")
        finally:
            lock.release()

    def _read_json(self):
        try:
            length = int(self.headers.get("Content-Length") or 0)
            return json.loads(self.rfile.read(length) or b"{}"), None
        except (ValueError, json.JSONDecodeError):
            return None, "invalid JSON body"

    def _emit(self, obj):
        self.wfile.write((json.dumps(obj, ensure_ascii=False) + "\n").encode("utf-8"))
        self.wfile.flush()

    def _run(self):
        payload, err = self._read_json()
        if err:
            self._json(400, {"error": err}); return
        case_id = (payload.get("case") or payload.get("case_id") or "").strip()
        if not case_id:
            self._json(400, {"error": "missing 'case' (the case_id to decide; GET /cases lists them)"}); return
        backend = (payload.get("backend") or payload.get("drafter") or "").strip() or None
        lock = self.server.__dict__.setdefault("run_lock", threading.Lock())
        if not lock.acquire(blocking=False):
            self._json(409, {"error": "another case is already being decided — wait for it to finish "
                                      "(single-flight: the verify step snapshots pillar-status)"}); return
        try:
            self.send_response(200)
            self.send_header("Content-Type", "application/x-ndjson; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            try:
                import tempfile
                with tempfile.TemporaryDirectory() as td:
                    out = run_case(case_id, tmpdir=Path(td), drafter=backend,
                                   on_stage=lambda stage, **kw: self._emit({"stage": stage, **kw}))
                self._emit({"done": out})
            except RunError as ex:
                self._emit({"error": str(ex)})
            except (OSError, ValueError, KeyError, json.JSONDecodeError) as ex:
                self._emit({"error": f"decision run failed: {ex}"})
        except (BrokenPipeError, ConnectionResetError):
            self.log_message("client disconnected mid-run stream")
        finally:
            lock.release()

    def log_message(self, fmt, *a):
        sys.stderr.write("[serve_workbench] " + (fmt % a) + "\n")


# ---- selftest (offline: no socket, casework consume stubbed) -------------------------------------
def selftest() -> int:
    failures = []
    index = load_index()
    cases = list_cases(index)
    assert cases["cases"] and all("case_id" in c for c in cases["cases"]), "queue empty/malformed"
    assert all("bundle" not in c for c in cases["cases"]), "queue rows must not carry the raw bundle"
    # Phase 73 — the authored showcase pair leads the queue but is NOT part of the population funnel/coverage
    # (it has its own computed determination, not a combo-frequency gate); scope these metrics to the population.
    pop_rows = [c for c in cases["cases"] if not c.get("showcase")]
    funnel = cases["meta"]["gate_funnel"]
    assert sum(funnel.values()) == len(pop_rows), "gate funnel must cover every population case"
    assert cases["meta"]["coverage"]["total"] == len(pop_rows), "coverage total mismatch"

    # ---- the LIVE gating engine (Phase 64) re-derives the baked funnel under the default policy ----
    live = gate_cases(index)
    if live["funnel"] != funnel:
        failures.append(f"live gate engine funnel {live['funnel']} != the baked funnel {funnel}")
    baked = {c["case_id"]: c["confidence"]["gate"] for c in index["cases"]}
    for r in live["cases"]:
        if r["gate"] != baked.get(r["case_id"]):
            failures.append(f"{r['case_id']}: live gate {r['gate']} != baked {baked.get(r['case_id'])}")
    # route() monotonicity: a larger sample never yields a STRICTER gate (pure-function property)
    strict = {"auto-clear": 0, "review": 1, "human-gate": 2}
    samples = [0, 1, 49, 50, 51, 499, 500, 501, 5000]
    strs = [strict[route(n)["gate"]] for n in samples]
    if any(strs[i] < strs[i + 1] for i in range(len(strs) - 1)):
        failures.append(f"route() gate not monotone in sample size: {list(zip(samples, strs))}")
    # a custom policy (the live KNOBS) re-derives a DIFFERENT but still-complete funnel
    loosened = gate_cases(index, policy_from_query("medium=1"))
    if sum(loosened["funnel"].values()) != len(index["cases"]):
        failures.append("custom-policy funnel must still cover every case")
    if loosened["funnel"].get("human-gate", 0) != 0:
        failures.append(f"medium=1 should leave no human-gate cases, got {loosened['funnel']}")
    # an invalid knob is a NAMED 400, not a crash
    try:
        policy_from_query("high=10&medium=50"); failures.append("high<medium policy should raise")
    except RunError:
        pass

    # ---- the elicitation LOOP (Phase 64 T2): adjudicate -> grow precedent -> re-route; persists NOTHING
    disk_before = (CASES_JSON.read_bytes(), sorted(p.name for p in BUNDLES_DIR.iterdir()))
    osint_before = OSINT_CORPUS_PATH.read_bytes()
    sess = new_session(index)
    hg = next(c for c in index["cases"] if c["confidence"]["gate"] == "human-gate")
    combo = hg["confidence"]["combo"]
    n0 = sess["precedent"][combo]
    # set the knobs so this combo sits exactly 1 below the review threshold -> ONE adjudication crosses it
    pol = policy_from_query(f"medium={n0 + 1}&high={n0 + 1000}")
    start = gate_cases(index, pol, sess["precedent"])
    if next(r for r in start["cases"] if r["case_id"] == hg["case_id"])["gate"] != "human-gate":
        failures.append("the chosen case should start human-gate under the near-threshold policy")
    res = adjudicate(index, sess, hg["case_id"], "cleared", pol)
    if not res["rerouted"] or res["after"]["gate"] != "review":
        failures.append(f"one adjudication should re-route the human-gate case to review, got {res['after']}")
    if res["n_precedent"] != n0 + 1 or res["combo_adjudications"] != 1:
        failures.append(f"the session precedent should grow by exactly 1, got n={res['n_precedent']} (from {n0})")
    if "ILLUSTRATIVE" not in res["disposition_recorded"]["basis"]:
        failures.append("the recorded disposition must be labeled ILLUSTRATIVE (the §14 honesty seam)")
    # an unknown disposition is a NAMED error, not a crash (and must not mutate the session)
    try:
        adjudicate(index, sess, hg["case_id"], "definitely-guilty", pol)
        failures.append("an unknown disposition should raise")
    except RunError:
        pass
    if sess["precedent"][combo] != n0 + 1:
        failures.append("a rejected adjudication must NOT have grown the precedent")
    # PERSISTS NOTHING: the committed slice is byte-identical after the whole loop ran
    disk_after = (CASES_JSON.read_bytes(), sorted(p.name for p in BUNDLES_DIR.iterdir()))
    if disk_before != disk_after:
        failures.append("the elicitation loop must persist NOTHING — cases.json/bundles changed on disk")

    # the scripted gather/finale DEMO case — resolved from the OSINT corpus (the hand-crafted sanctions
    # chain), NOT the volatile 'mule' exemplar (Phase 72: a re-curate moves the exemplar off the corpus
    # subject). Still a rich human-gate mule by construction; the assertions below hold on it.
    mule_id = gather_demo_case_id(index)
    detail = case_detail(mule_id, index)
    b = detail["bundle"]
    assert b.get("parties") and b.get("transactions") and b.get("alerts"), "clutter bundle incomplete"
    assert detail["signals"] and all(w["grounded"] for w in detail["signals"]), \
        [w for w in detail["signals"] if not w["grounded"]]
    assert detail["case"]["confidence"]["gate"] == "human-gate", "the mule should be a human-gate case"

    # path-traversal + unknown-case guards
    for bad in ("../../etc/passwd", "CASE-DOES-NOT-EXIST"):
        try:
            case_detail(bad, index); failures.append(f"bad case id '{bad}' should raise")
        except RunError:
            pass

    # NO creds/endpoints reach the browser (§4.5) — the served config carries names + booleans only.
    # Probe with a DISTINCTIVE configured endpoint (NOT the generic 127.0.0.1:8080 default, which now
    # legitimately appears in the page's help text) so this tests the real invariant: the operator's
    # CONFIGURED cred/endpoint never reaches the page.
    secret = {"ANTHROPIC_API_KEY": "sk-SECRET-DEAD", "OPENAI_BASE_URL": "http://leak-probe.example:59999/v1"}
    blob = json.dumps(live_config(secret)) + render_page(live_config(secret))
    for leak in ("sk-SECRET-DEAD", "leak-probe.example:59999"):
        assert leak not in blob, f"server-side cred/endpoint leaked into the page: {leak}"

    # the LIVE finale OFFLINE: casework consume STUBBED, e2e verify REAL (pillar-status snapshot+restored)
    status_before = sc.STATUS_PATH.read_bytes() if sc.STATUS_PATH.exists() else None
    stages = []
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        out = run_case(mule_id, tmpdir=Path(td), drafter="stub", consume=_stub_signed_sar,
                       on_stage=lambda s, **kw: stages.append((s, kw)))
    seq = [s for s, _ in stages]
    for needed in ("evidence", "consume", "verify", "connected"):
        if needed not in seq:
            failures.append(f"finale stage '{needed}' missing from {seq}")
    if not out["connected"] or not out["signed_sar"] or not out["audit_walk"]:
        failures.append(f"stubbed finale should CONNECT with a signed SAR + audit walk, got {out['connected']}")
    if out.get("disposition") != "file" or out.get("fail_closed"):
        failures.append(f"a signed case should be disposition=file / fail_closed=false, got {out.get('disposition')}")
    status_after = sc.STATUS_PATH.read_bytes() if sc.STATUS_PATH.exists() else None
    if status_before != status_after:
        failures.append("data/pillar-status.json was mutated by a run (verify_e2e must snapshot+restore)")

    # FAIL-CLOSED is a disposition, NOT a crash: a consume that refuses (signed:false + violations) →
    # disposition=escalate, fail_closed=true, the verify is skipped, and run_case does NOT raise.
    def _refusing_consume(bp, op, d):
        Path(op).write_text(json.dumps({"str_record": {"narrative": None, "completeness": {}},
            "signoff": {"signed": False, "blocking_violations":
                ["grounding_replay: alerts[AL-x].replay(C3): only 0 cited outflow(s); needs >=5"]}}) + "\n",
            encoding="utf-8")
        return sc._consume_result_from_sar(json.loads(Path(op).read_text(encoding="utf-8")), d)
    fc_stages = []
    with tempfile.TemporaryDirectory() as td:
        fc = run_case(mule_id, tmpdir=Path(td), drafter="stub", consume=_refusing_consume,
                      on_stage=lambda s, **kw: fc_stages.append((s, kw)))
    if fc.get("fail_closed") is not True or fc.get("disposition") != "escalate" or fc.get("connected"):
        failures.append(f"a casework refusal should be fail_closed/escalate (not a crash), got {fc.get('disposition')}")
    verify_stage = [kw for s, kw in fc_stages if s == "verify"]
    if not verify_stage or verify_stage[-1].get("status") != "skipped":
        failures.append("on fail-closed the verify stage must be marked skipped (the join is moot)")
    conn_stage = [kw for s, kw in fc_stages if s == "connected"]
    if not conn_stage or not conn_stage[-1].get("blocking_violations"):
        failures.append("the fail-closed disposition stage must carry the blocking_violations (the honest reason)")

    # backend resolution flows through to the consume (server-side; the browser only sent a NAME)
    seen = {}
    with tempfile.TemporaryDirectory() as td:
        run_case(mule_id, tmpdir=Path(td), drafter="opencode", env={"OPENAI_BASE_URL": "http://x/v1"},
                 consume=lambda bp, op, d: (seen.__setitem__("d", d), _stub_signed_sar(bp, op, d))[1],
                 on_stage=lambda s, **kw: None)
    if seen.get("d") != "stub":     # opencode unavailable in this env -> honest stub fallback
        failures.append(f"unavailable backend should fall back to stub, consume saw {seen.get('d')!r}")

    # ---- the GATHER beat (Phase 65): the OSINT agent loop over the synthetic corpus, OFFLINE (stub) ----
    gstages = []
    gout = run_gather(mule_id, on_stage=lambda s, **kw: gstages.append((s, kw)))
    if gout["counts"]["grounded"] < 2:
        failures.append(f"gather should KEEP grounded findings on the mule chain, got {gout['counts']}")
    if gout["counts"]["dropped"] < 1:
        failures.append("gather should DROP the planted ungrounded finding (the gate firing — the honest moment)")
    if not gout["graph"]["relationships"] or gout["graph"]["mains"] != [gather_view(_case_entry(index, mule_id), json.loads(_bundle_path(mule_id).read_text()))["subject_name"]]:
        failures.append("gather should build a grounded network graph with the subject as main")
    if "SYNTHETIC" not in gout["synthetic_note"]:
        failures.append("the gather result must carry the beat-local SYNTHETIC-provenance note")
    if not any(f["source_kind"] == "sanctions" for f in gout["grounded"]):
        failures.append("the gather CHAIN should reach a sanctions finding on the registry-discovered entity")
    gseq = [s for s, _ in gstages]
    for needed in ("backend", "requirement", "plan", "tool", "findings"):
        if needed not in gseq:
            failures.append(f"gather stage '{needed}' missing from {gseq}")
    # Phase 69 — REQUIREMENT-TARGETED gather: the mule (mechanism + ML-A4 from C15) is one corroborating leg
    # short; gather TARGETS ML-A5 and CLOSES it record-sourced (the sanctions + adverse hits on the network),
    # reaching two legs — the determination becomes reachable (the GATHER payoff, not additive discovery).
    req = gout.get("requirement") or {}
    if req.get("crime_type") != "money_laundering":
        failures.append(f"gather requirement should profile money_laundering, got {req.get('crime_type')}")
    if "ML-A5" not in [t["id"] for t in req.get("targets", [])]:
        failures.append(f"gather should TARGET the unmet corroboration atom ML-A5, got {req.get('targets')}")
    if "ML-A5" not in [c["id"] for c in req.get("closed", [])]:
        failures.append(f"gather should CLOSE ML-A5 from the record-sourced sanctions/adverse findings, got {req.get('closed')}")
    # Phase 70 — the COVERAGE measuring stick: the stub is the deterministic REFERENCE. It grounds a finding
    # from EVERY record its tools surface (coverage complete) and CLOSES every targeted atom (closure complete)
    # — the bar a live gather's coverage is measured against (consistency, not a catch-rate).
    cov = gout.get("coverage") or {}
    if cov.get("records_returned", 0) < 3 or cov.get("finding_coverage") != 1.0 or cov.get("complete") is not True:
        failures.append(f"the stub reference should achieve complete extraction coverage, got {cov}")
    if set(cov.get("grounded_record_ids", [])) - set(cov.get("returned_record_ids", [])):
        failures.append("grounded_record_ids must be a subset of returned_record_ids (the coverage invariant)")
    if req.get("target_closure") != 1.0:
        failures.append(f"the stub should CLOSE every targeted atom (full reference closure), got {req.get('target_closure')}")
    if "coverage" not in gseq:
        failures.append(f"gather should emit a 'coverage' stage for the live processing page, got {gseq}")
    # PERSISTS NOTHING: the committed slice + the OSINT corpus are byte-identical after a gather ran
    if disk_before != (CASES_JSON.read_bytes(), sorted(p.name for p in BUNDLES_DIR.iterdir())):
        failures.append("a gather run must persist NOTHING — cases.json/bundles changed on disk")
    if osint_before != OSINT_CORPUS_PATH.read_bytes():
        failures.append("a gather run must persist NOTHING — data/osint/corpus.json changed on disk")

    # ---- the DIFFERENTIATED DETERMINATION (Phase 69 T4): sufficiency SUPERSEDES frequency ----
    # the mule's frequency gate AUTO-CLEARS (high precedent), but from SIGNALS the determination is
    # WITHHELD (one corroborating leg short) — the defensive-filing exposure made concrete.
    d_sig = determine_case(mule_id)
    if d_sig["determination"]["verdict"] != "needs_more_info":
        failures.append(f"the mule determination from signals alone should be needs_more_info, got {d_sig['determination']['verdict']}")
    if d_sig["frequency_context"]["gate"] not in ("auto-clear", "review", "human-gate"):
        failures.append("the determination must carry the frequency gate as DEMOTED context")
    # after GATHER closes corroboration + a named risk + mitigation rebutted -> a DETERMINATION
    d_full = determine_case(mule_id, gathered=["corroboration"], named_risk="human trafficking",
                            mitigation_rebutted=True)
    if d_full["determination"]["verdict"] != "determination" or not d_full["determination"]["sufficient"]:
        failures.append(f"the mule with gather+risk+mitigation should reach a determination, got {d_full['determination']}")
    # the contrast is real: an auto-clear case is NOT an auto-determination from signals alone — the
    # named-risk + mitigation gate (the human's job) is unmet, so frequency never substitutes for it.
    auto_clear = next((c for c in index["cases"] if c["confidence"]["gate"] == "auto-clear"), None)
    if auto_clear:
        dc = determine_case(auto_clear["case_id"])
        if dc["frequency_context"]["gate"] != "auto-clear":
            failures.append("an auto-clear case's frequency context should read auto-clear")
        if dc["determination"]["verdict"] == "determination":
            failures.append("an auto-clear case should NOT be an auto-determination from signals alone "
                            "(the named-risk + mitigation gate is unmet — frequency never substitutes)")

    # ---- Phase 71: the §12 LOOP CLOSES from REAL signals (the substrate v0.3 internal legs) ----
    # The merged v0.3 slice lets a case carry a mechanism + TWO corroborating legs from REAL capabilities
    # ALONE — C8 (ML-A3 profile-inconsistency) beside C15/related_parties (ML-A4 network) — so a
    # determination is REACHABLE from signals (the human still NAMES the risk + rebuts mitigation, the
    # legitimate gate), WITHOUT the GATHER corroboration the pre-v0.3 slice required. kyc_integrity / C1 /
    # C7 stay substrate-emission gaps (deferred — surfaced honestly via signal_brief).
    _LEG_IDS = ("ML-A3", "ML-A4", "ML-A5", "ML-A6", "ML-A7")
    prof_st = _requirements()
    twoleg = next((c for c in index["cases"]
                   if crime_type_for_capabilities(_entry_caps(c), prof_st) == "money_laundering"
                   and len(set(present_atoms("money_laundering", _entry_caps(c), prof_st)) & set(_LEG_IDS)) >= 2),
                  None)
    if not twoleg:
        failures.append("§12 closure: NO case reaches >=2 legs from REAL signals (the v0.3/merge adoption "
                        "regressed — expected C8 ML-A3 + C15 ML-A4 cases from the merged slice)")
    else:
        d_real = determine_case(twoleg["case_id"], named_risk="drug trafficking", mitigation_rebutted=True)
        det = d_real["determination"]
        if det["verdict"] != "determination" or not det["sufficient"]:
            failures.append(f"§12 closure: a >=2-leg case + named risk + mitigation should reach a "
                            f"determination from REAL signals (no gather), got {det}")
        legs_present = [a for a in det["completeness"]["present_atom_ids"] if a in _LEG_IDS]
        if len(legs_present) < 2:
            failures.append(f"§12 closure: the determination should rest on >=2 REAL-signal legs, got {legs_present}")
        # the SAME case WITHOUT the human inputs is WITHHELD — the gate is real, not auto from frequency/legs
        if determine_case(twoleg["case_id"])["determination"]["verdict"] == "determination":
            failures.append("§12: a >=2-leg case must still WITHHOLD without a named risk + rebutted mitigation")
        # the deferred gaps surface honestly (the §12 substrate brief is still named — C1/C14 etc. unmet)
        if not det.get("signal_brief"):
            failures.append("§12: the determination should still carry a signal_brief naming the deferred "
                            "substrate gaps (C1 anticipated-activity / C14 source-of-funds)")

    # ---- Phase 72: the §12 KYC loop CLOSES from a REAL C14 signal (the consumed substrate Phase-26 emission) ----
    # A C14-PURE customer (no ML co-firing) classifies kyc_integrity and reaches a determination from the C14
    # MECHANISM ALONE (KYC-A1; the kyc profile needs mechanism + 0 extra legs) — the human still NAMES the risk.
    # SIGNING is the honest cross-pillar FRONTIER: a txn-bearing C14 case SIGNS end-to-end through the
    # re-vendored casework (bf15535's broadened C14 grounding); a txn-LESS C14 party-leaf fails-CLOSED at
    # casework's no-transactions CONTRACT (surfaced via e2e_note, never loosened) — a named casework follow-on.
    kyc_cases = [c for c in index["cases"]
                 if crime_type_for_capabilities(_entry_caps(c), prof_st) == "kyc_integrity"]
    if not kyc_cases:
        failures.append("§12 kyc: NO kyc_integrity case in the slice — the substrate Phase-26 C14 emission "
                        "was not consumed (expected C14-pure cases classifying kyc_integrity)")
    else:
        kc = kyc_cases[0]
        d_kyc = determine_case(kc["case_id"], named_risk="source of funds not established")
        dk = d_kyc["determination"]
        if d_kyc["crime_type"] != "kyc_integrity":
            failures.append(f"§12 kyc: a C14-pure case should classify kyc_integrity, got {d_kyc['crime_type']}")
        if dk["verdict"] != "determination" or "KYC-A1" not in dk["completeness"]["present_atom_ids"]:
            failures.append(f"§12 kyc: a C14-pure case + named risk should reach a kyc determination on "
                            f"KYC-A1 from the C14 signal ALONE (no gather, no extra legs), got {dk}")
        # the gate is REAL — without a named predicate risk the kyc determination is WITHHELD
        if determine_case(kc["case_id"])["determination"]["verdict"] == "determination":
            failures.append("§12 kyc: a kyc case must WITHHOLD without a named predicate risk (the gate is real)")
        # the SIGN frontier, asserted by RULE (not a count): a kyc case SIGNS iff it carries transactions;
        # a txn-less one fails-CLOSED with the honest casework no-transactions contract reason.
        for c in kyc_cases:
            if c.get("grounds_e2e") is True and c.get("n_txns", 0) == 0:
                failures.append(f"§12 kyc: {c['case_id']} signed with no transactions — casework requires txns")
            if c.get("grounds_e2e") is False and "no transactions" not in (c.get("e2e_note") or ""):
                failures.append(f"§12 kyc: a fail-closed kyc case must surface the honest casework-contract "
                                f"reason (no transactions), got {c.get('e2e_note')!r}")
        if not any(c.get("grounds_e2e") is True for c in kyc_cases):
            failures.append("§12 kyc: expected >=1 txn-bearing kyc case to SIGN end-to-end through the "
                            "re-vendored casework (the consume payoff — none signed in the committed slice)")

    # ---- Phase 73: the authored NORTH-STAR pair COMPUTES file vs cleared via the LIVE engine ----
    # The matched pair fires the IDENTICAL grounded signals but resolves OPPOSITELY — the verdict is engine
    # OUTPUT over the AUTHORED evidence (the source-of-funds finding read from the file, the resolved network,
    # the caution-list / prior-STR record hits), NEVER the authored expected string. The file bar is unchanged;
    # the affirmative-clear branch gives Lakeshore its documented dismissal.
    q = list_cases()
    sc_ids = q["meta"].get("showcase_ids", [])
    if sc_ids != ["CASE-A", "CASE-B"]:
        failures.append(f"the authored pair should be the showcase ids, got {sc_ids}")
    if [c["case_id"] for c in q["cases"][:2]] != ["CASE-A", "CASE-B"]:
        failures.append("the authored pair must LEAD the queue (the top two rows)")
    da = casefile_determination("CASE-A")
    if not (da["verdict"] == "determination" and da["disposition"] == "escalated" and da["presentation_label"] == "file"):
        failures.append(f"CASE-A (Northgate) should COMPUTE determination/escalated/file, got {da['verdict']}/{da['disposition']}")
    if da["named_risk"] != "human trafficking":
        failures.append(f"CASE-A should READ the predicate from the prior-STR record, got {da['named_risk']!r}")
    if not da["expectation_match"]:
        failures.append("CASE-A computed verdict must match its authored oracle (the regression check)")
    a_legs = {a["atom"] for a in da["present_atoms"] if a["kind"] == "leg"}
    if not ({"ML-A4", "ML-A5", "ML-A7"} <= a_legs):
        failures.append(f"CASE-A should rest on the read-network + gathered-corroboration + source legs, got {sorted(a_legs)}")
    a_via = {a["atom"]: a["via"] for a in da["present_atoms"]}
    if not (a_via.get("ML-A4") == "read" and a_via.get("ML-A5") == "gathered" and a_via.get("ML-A1") == "fired"):
        failures.append(f"CASE-A per-leg provenance (via) should be grounded fired/read/gathered, got {a_via}")
    db = casefile_determination("CASE-B")
    if not (db["verdict"] == "cleared" and db["presentation_label"] == "documented_dismissal"):
        failures.append(f"CASE-B (Lakeshore) should COMPUTE the affirmative cleared/documented_dismissal, got {db['verdict']}")
    if not db["mitigation_established"] or db["named_risk"]:
        failures.append("CASE-B should clear on AFFIRMATIVELY established mitigation with no named predicate")
    if [a for a in db["present_atoms"] if a["kind"] == "leg"]:
        failures.append("CASE-B should carry NO corroborating leg (the clear rests on absent legs + positive mitigation)")
    if not db["expectation_match"]:
        failures.append("CASE-B computed verdict must match its authored oracle")
    # the SAME fired signals on both, opposite outcome — the thesis, asserted from the data
    if {a.get("capability") for a in casefile_case("CASE-A")["alerts"]} != {a.get("capability") for a in casefile_case("CASE-B")["alerts"]}:
        failures.append("the pair must fire the IDENTICAL signal set (same grounded signal, opposite outcome)")
    # ── Phase 74 (T4): the GRADE-GATED read path + the per-decision manifest ──
    a_manifest = da.get("read_manifest", [])
    if not (a_manifest and all(m["status"] == "admitted" and m["grade"] == "strong" for m in a_manifest)):
        failures.append(f"CASE-A ML-A4 should be ADMITTED at grade strong (the Calder/Maric edges are strong): {a_manifest}")
    # a resolved/flagged edge with NO shared identifier (name-only / empty) -> the atom is QUARANTINED, EXCLUDED
    _q_read, _q_man = _cf_read_manifest({"resolution_edges": [{"status": "flagged", "between": ["X"], "shared": []}]})
    if _q_read or not (_q_man and _q_man[0]["status"] == "quarantined-by-low-grade" and _q_man[0]["grade"] == "reject"):
        failures.append(f"a null-grade (empty-shared) edge must QUARANTINE the read atom (exclude, not down-weight): {_q_man}")
    # ── Phase 74 (T4): the self-confirming-loop / file-bar guard ──
    # the file bar must be STRUCTURALLY unable to read priors — no prior/disposition/history parameter
    import inspect as _inspect
    for _fn in (evaluate_sufficiency, determine):
        _leak = set(_inspect.signature(_fn).parameters) & {
            "prior", "priors", "prior_disposition", "dispositions", "history", "precedent_disposition"}
        if _leak:
            failures.append(f"the file bar must not read priors — {_fn.__name__} exposes {_leak}")
    # injecting a prior 'cleared' must NOT change the verdict for a fixed evidence set (priors are provenance only)
    _before = json.dumps(casefile_determination("CASE-A"), sort_keys=True, ensure_ascii=False)
    try:
        _sp = EntitySpine(":memory:")
        _subj = (casefile_case("CASE-A").get("subject") or {}).get("entity_ref")
        _r = _sp.observe("PRIOR-CASE", {"entity_id": _subj, "display_name": "prior", "kind": "org",
            "identifiers": [{"kind": "email", "value": "p@p.test", "normalized": "p@p.test", "strength": "strong"}]})
        _sp.attach_disposition(_r["entity_id"], "PRIOR-CASE", "cleared", decided_at="2025-01-01")
        _sp.close()
    except RuntimeError:
        pass   # duckdb absent — the structural signature guard above still holds
    _after = json.dumps(casefile_determination("CASE-A"), sort_keys=True, ensure_ascii=False)
    if _before != _after:
        failures.append("injecting a prior 'cleared' changed the determination — priors must be provenance-only (self-confirming-loop guard)")
    # ── Phase 74 (T5): the re-surfacing MEMORY demo — genuine persistence, measured short-circuit, stale-prior guard ──
    import tempfile as _tempfile
    try:
        _mem = casefile_memory(os.path.join(_tempfile.mkdtemp(), "spine.duckdb"))
    except RuntimeError:
        _mem = None   # duckdb absent (the spine needs it) — the dep-free path skips; .venv runs it fully
    if _mem is not None:
        if _mem["prior_predicate"] != "human trafficking":
            failures.append(f"the re-surfacing subject must carry her INDEPENDENT prior-STR predicate, got {_mem['prior_predicate']!r}")
        if not (_mem["targets_shrink"] >= 1):
            failures.append(f"memory must SHRINK the gather targets-to-close (a measured number, not a flag): "
                            f"cold={_mem['cold_targets']} memory={_mem['memory_targets']}")
        if not _mem["predicate_pre_named_by_memory"]:
            failures.append("memory must PRE-NAME the predicate (no re-gather of what the prior already establishes)")
        if not _mem["n_priors"] or _mem["persisted_read_back"] != _mem["n_priors"]:
            failures.append(f"the write-then-read-back seam must survive a store reopen: "
                            f"read_back={_mem['persisted_read_back']} priors={_mem['n_priors']}")
        if _mem["stale_after_split"] is not True:
            failures.append("the stale-prior guard must fire 're-decision required' after an identity split (event-driven)")
    # ── Phase 75: the REAL-DATA cross-case memory over the curated substrate slice (entity_ref-keyed) ──
    try:
        _sm = substrate_memory(os.path.join(_tempfile.mkdtemp(), "sub-spine.duckdb"))
    except RuntimeError:
        _sm = None   # duckdb absent — dep-free path skips; .venv runs it fully
    if _sm is not None:
        if _sm["n_cases_scanned"] != len(load_index().get("cases", [])):
            failures.append(f"substrate_memory must scan every slice case, got {_sm['n_cases_scanned']}")
        for _k in ("n_xcase_coref", "n_over_merge_refused", "n_candidate_shares", "n_entities"):
            if not isinstance(_sm[_k], int) or _sm[_k] < 0:
                failures.append(f"substrate_memory.{_k} must be a non-negative int, got {_sm[_k]!r}")
        # the entity_ref-keyed design REFUSES every substrate "resolved" edge between distinct entity_refs
        if _sm["n_over_merge_refused"] != _sm["n_candidate_shares"]:
            failures.append("the spine must refuse EVERY candidate SHARES over-merge (entity_ref keys identity), "
                            f"got refused={_sm['n_over_merge_refused']} candidates={_sm['n_candidate_shares']}")
        if "entity_ref" not in _sm["qualifier"] or "SHARES" not in _sm["qualifier"]:
            failures.append("substrate_memory must carry the honesty qualifier (entity_ref co-reference; SHARES not merged)")
        for _e in _sm["xcase_coref_examples"]:
            if not _e.get("cases") or _e.get("n_cases", 0) < 2:
                failures.append(f"a cross-case co-reference must name 2+ cases: {_e}")
    # the detail carries the full evidence for the render, and the routes DISPATCH the authored ids
    da_det = casefile_detail("CASE-A")
    if da_det["case"]["display_name"] != "Northgate Hospitality Group Inc." or not da_det["case"]["transactions"]:
        failures.append("the casefile detail must carry the full authored case for the render")
    if case_detail("CASE-B").get("showcase") is not True:
        failures.append("case_detail must DISPATCH an authored id to the casefile path")
    if determine_case("CASE-B")["verdict"] != "cleared":
        failures.append("determine_case must DISPATCH an authored id to the casefile path (cleared)")
    # the committed RENDER fixtures (tests/fixtures/casefile/*) must EQUAL the live computation — the .mjs test
    # replays them, so this is the bridge: an engine/data edit that forgets a fixture regen fails LOUD here.
    _fixdir = ROOT / "tests" / "fixtures" / "casefile"
    for _cid in ("CASE-A", "CASE-B"):
        try:
            _committed = json.loads((_fixdir / f"{_cid}.detail.json").read_text(encoding="utf-8"))
        except OSError:
            failures.append(f"Phase-73 render fixture missing: tests/fixtures/casefile/{_cid}.detail.json"); continue
        if casefile_detail(_cid) != _committed:
            failures.append(f"Phase-73 fixture DRIFT: tests/fixtures/casefile/{_cid}.detail.json != live casefile_detail('{_cid}') — regenerate it")
    try:
        _qfix = json.loads((_fixdir / "queue.json").read_text(encoding="utf-8")).get("cases", [])
        if [c for c in list_cases()["cases"] if c.get("showcase")] != _qfix:
            failures.append("Phase-73 fixture DRIFT: tests/fixtures/casefile/queue.json showcase rows != live list_cases() — regenerate it")
    except OSError:
        failures.append("Phase-73 render fixture missing: tests/fixtures/casefile/queue.json")

    # an unknown case is a NAMED error, not a crash
    try:
        determine_case("CASE-DOES-NOT-EXIST"); failures.append("determine_case on an unknown case should raise")
    except RunError:
        pass

    # §4.5: NO server-side cred/endpoint reaches the browser via ANY gather NDJSON stage OR the done result
    # (distinctive endpoint, not the generic 127.0.0.1:8080 default — see the §4.5 page-leak note above)
    gsecret = {"ANTHROPIC_API_KEY": "sk-SECRET-DEAD", "OPENAI_BASE_URL": "http://leak-probe.example:59999/v1"}
    gsec_stages = []
    gsec = run_gather(mule_id, backend="claude", env=gsecret,
                      on_stage=lambda s, **kw: gsec_stages.append({"stage": s, **kw}))
    gblob = json.dumps(gsec_stages, ensure_ascii=False) + json.dumps(gsec, ensure_ascii=False)
    for leak in ("sk-SECRET-DEAD", "leak-probe.example:59999"):
        if leak in gblob:
            failures.append(f"gather leaked a server-side cred/endpoint into a stage/result: {leak}")

    # ---- the EVIDENCE-REQUIREMENT profile (Phase 69 T1): the committed profile validates clean, and the
    # sufficiency evaluator is the determination control (mechanism + legs + named risk + no unrebutted
    # mitigation). The deep tamper/evaluator coverage lives in evidence_requirements --selftest; here we
    # assert the COMMITTED profile is consumable by the workbench + the two in-scope crime_types are present.
    prof = load_requirements()
    rerrs = validate_requirements(prof)
    if rerrs:
        failures.append(f"evidence-requirements.json failed validation: {'; '.join(rerrs[:4])}")
    if set(prof.get("crime_types", {})) != {"money_laundering", "kyc_integrity"}:
        failures.append(f"profile crime_types should be ML + kyc_integrity, got {set(prof.get('crime_types', {}))}")
    # the determination control is live: the stricter ML bar withholds when a corroborating leg is short
    _suff = evaluate_sufficiency("money_laundering", ["ML-A1", "ML-A3"], named_predicate_risk=True,
                                 mitigation_rebutted=True, profile=prof, required_elements_satisfied=True)
    if _suff["sufficient"] or not any("corroborating leg" in m for m in _suff["missing"]):
        failures.append(f"the ML sufficiency bar should withhold a determination one leg short, got {_suff}")

    # the served page substitutes the config placeholder iff workbench.html exists
    page = render_page(live_config())
    if TEMPLATE.exists():
        assert PLACEHOLDER not in page and BADGE in page, "config/badge not inlined into workbench.html"
    else:
        assert BADGE in page, "placeholder page must still carry the badge"

    if failures:
        for f in failures:
            print(f"FAIL: {f}", file=sys.stderr)  # noqa: T201
        return 1
    print(f"serve_workbench --selftest: PASS ({len(cases['cases'])} cases; gate funnel {funnel}; "  # noqa: T201
          f"live route() reproduces it + monotone; coverage "
          f"{cases['meta']['coverage']['groundable']}/{cases['meta']['coverage']['total']}; "
          f"mule detail grounds {len(detail['signals'])}/{len(detail['signals'])} signals; "
          f"§12 closure: {twoleg['case_id'] if twoleg else 'NONE'} reaches a determination from REAL signals "
          f"(C8 ML-A3 + C15 ML-A4, no gather); "
          f"§12 kyc: {len(kyc_cases)} C14-pure kyc case(s) determine from KYC-A1, "
          f"{sum(1 for c in kyc_cases if c.get('grounds_e2e') is True)} SIGN / "
          f"{sum(1 for c in kyc_cases if c.get('grounds_e2e') is False)} fail-closed at casework's txn contract; "
          f"Phase-73 north-star pair LEADS the queue + COMPUTES live: "
          f"CASE-A {da['verdict']}/{da['presentation_label']} (predicate {da['named_risk']!r}) vs "
          f"CASE-B {db['verdict']}/{db['presentation_label']} (affirmative mitigation) — same signals, opposite outcome; "
          f"stubbed finale {seq} -> CONNECTED; pillar-status byte-stable)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Investigator case-workbench companion (dev-time only; never a ship artifact).")
    ap.add_argument("--port", type=int, default=DEFAULT_PORT)
    ap.add_argument("--selftest", action="store_true", help="offline assertions (no socket, casework stubbed), exit")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    httpd = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    drafter = default_backend()
    print(f"[serve_workbench] investigator workbench on http://localhost:{args.port}/  "  # noqa: T201
          f"(drafter={drafter}, {len(load_index().get('cases', []))} cases)")
    print(f"[serve_workbench] backends: {', '.join(available_backends())} "  # noqa: T201
          f"(openai → 127.0.0.1:8080 by default — pick it; set OPENAI_BASE_URL to override, or a claude key; "
          f"auto-default={drafter}). Nothing persisted; offline dists byte-frozen. Ctrl-C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[serve_workbench] stopped.")  # noqa: T201
    return 0


if __name__ == "__main__":
    sys.exit(main())
