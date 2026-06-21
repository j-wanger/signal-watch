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
    return {"badge": BADGE, "meta": meta, "cases": rows}


def case_detail(case_id: str, index: dict | None = None) -> dict:
    """The per-case CLUTTER payload: the full vendored bundle (KYC, accounts, every txn, alerts,
    counterparty edges) + the GROUNDED signal walk (flag->corpus, server-computed, model-free) + the
    curated entry (confidence/exemplar/gate). Beats 1+2 render entirely from this — no model call."""
    idx = index or load_index()
    entry = _case_entry(idx, case_id)
    bundle = json.loads(_bundle_path(case_id).read_text(encoding="utf-8"))
    return {"badge": BADGE, "case": entry, "bundle": bundle, "signals": audit_walk(bundle)}


# ---- the casework consume — a REFUSAL is a disposition outcome, not a crash (the embrace-fail-closed) -
def casework_consume_wb(bundle_path: Path, out_path: Path, drafter: str) -> dict:
    """Like serve_chain.casework_consume, but a casework REFUSAL (it ran + wrote an UNSIGNED SAR because
    the six Class-G verifiers couldn't independently reproduce a signal — the substrate↔casework C3/C15
    divergence) is a RETURNED outcome (signed:false + blocking_violations), NOT a raised error. Only a
    genuine launch/crash (no SAR written) raises. The verifier is the oracle — we surface its verdict."""
    src = sc.CASEWORK_DIR / "src"
    venv = sc.CASEWORK_DIR / ".venv" / "bin" / "python"
    py = os.environ.get("AML_CASEWORK_PYTHON") or (str(venv) if venv.exists() else sys.executable)
    if not src.exists():
        raise RunError(f"aml-casework not found at {sc.CASEWORK_DIR} (set AML_CASEWORK_DIR) — the consume "
                       f"is the sibling prerequisite; the finale is GATED until it lands")
    env = dict(os.environ)
    env["PYTHONPATH"] = str(src) + os.pathsep + env.get("PYTHONPATH", "")
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


# ---- the served page -----------------------------------------------------------------------------
def live_config(env: dict | None = None) -> dict:
    return {"cases": "/cases", "case": "/case", "run": "/run", "health": "/health", "badge": BADGE,
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
        elif path == "/health":
            self._json(200, {"ok": True, "live": True, "persist": False,
                             "drafter": default_backend(), "backends": available_backends(),
                             "cases": len(load_index().get("cases", []))})
        else:
            self._json(404, {"error": f"not found: {path}"})

    def do_POST(self):
        if self.path.split("?", 1)[0] == "/run":
            self._run(); return
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
    funnel = cases["meta"]["gate_funnel"]
    assert sum(funnel.values()) == len(cases["cases"]), "gate funnel must cover every case"
    assert cases["meta"]["coverage"]["total"] == len(cases["cases"]), "coverage total mismatch"

    # an exemplar case detail carries the full clutter + the GROUNDED signal walk (model-free)
    mule_id = index["meta"]["exemplars"]["mule"]
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

    # NO creds/endpoints reach the browser (§4.5) — the served config carries names + booleans only
    secret = {"ANTHROPIC_API_KEY": "sk-SECRET-DEAD", "OPENAI_BASE_URL": "http://127.0.0.1:8080/v1"}
    blob = json.dumps(live_config(secret)) + render_page(live_config(secret))
    for leak in ("sk-SECRET-DEAD", "127.0.0.1:8080"):
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
          f"coverage {cases['meta']['coverage']['groundable']}/{cases['meta']['coverage']['total']}; "
          f"mule detail grounds {len(detail['signals'])}/{len(detail['signals'])} signals; "
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
    print(f"[serve_workbench] {'LIVE neural SAR draft available' if drafter != 'stub' else 'no key — deterministic stub draft'}; "  # noqa: T201
          "nothing is persisted; the offline dists stay byte-frozen. Ctrl-C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[serve_workbench] stopped.")  # noqa: T201
    return 0


if __name__ == "__main__":
    sys.exit(main())
