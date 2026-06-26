#!/usr/bin/env python3
"""Chain workbench companion (Phase 56 — dev/authoring-time ONLY; NEVER a ship artifact).

The analyst case-workbench for the 3-pillar chain: detection is pre-baked upstream (the substrate
evidence bundles are vendored under data/chain-cases/, pinned like the corpus), and per case the
DOWNSTREAM runs LIVE — aml-casework consumes the bundle into a verified, signed SAR (the 6 Class-G
verifiers + a neural OR deterministic narrative draft), then signal-watch's e2e_chain_check re-verifies
the cross-pillar join. The result streams as NDJSON stages → CONNECTED + the flag→corpus audit walk.

DOCTRINE (load-bearing — the same boundary the rest of the program holds):
  * subprocess + file-handoff ONLY. This NEVER imports aml_substrate / aml_casework (the
    one-repo-per-pillar rule). The casework consume is a subprocess of its OWN CLI
    (`python -m aml_casework.ingest`, see aml-casework/docs/consume-cli-PLAN-BRIEF.md); the bundle and
    the signed SAR cross the boundary as json files. The only imports are signal-watch's OWN modules
    (e2e_chain_check, derive_signals, validate_chain_cases) — never a sibling.
  * stdlib only. build.py NEVER imports this; chain.html is NOT a build target; the offline dists stay
    byte-frozen. Nothing is persisted — a signed SAR is written to a per-run temp dir and discarded.
  * the committed data/pillar-status.json (which the launcher inlines) is SNAPSHOT + RESTORED around the
    e2e_chain_check subprocess — a workbench run reflects the pre-baked bridge states, it never moves them
    (that would drift the launcher dist and break --check all).
  * TWO-BEAT: the SPINE here is selftest-proven OFFLINE with the casework consume STUBBED. The LIVE run
    (a real signed SAR → CONNECTED) needs the casework consume CLI (the sibling prerequisite). Until it
    lands, the real consume fails HONESTLY in-stream (named "bridge gated"), never silently.

Usage:
    python3 scripts/serve_chain.py                 # http://localhost:8020 (chain.html + the live consume/verify)
    python3 scripts/serve_chain.py --port 8021
    python3 scripts/serve_chain.py --selftest      # offline assertions (no socket, casework stubbed), exit
"""
from __future__ import annotations

import argparse
import copy
import glob
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
import e2e_chain_check        # signal-watch's OWN cross-pillar harness (NOT a sibling)
import validate_chain_cases   # signal-watch's OWN library validator (reuses check_substrate)
from derive_signals import normalize  # the stable grounding core
# Phase 69 — the evidence-requirement profile + the COMPLETENESS measurement (companion; chosen-not-measured).
from evidence_requirements import assess_completeness, crime_type_for_capabilities
from evidence_requirements import requirements as _requirements

DEFAULT_PORT = 8020          # serve_news holds 8000, serve_corpus 8010 — all three run side by side
CASES_DIR = ROOT / "data" / "chain-cases"
MANIFEST_PATH = CASES_DIR / "manifest.json"
CHAIN_TEMPLATE = ROOT / "chain.html"
E2E_SCRIPT = _HERE / "e2e_chain_check.py"
STATUS_PATH = Path(e2e_chain_check.STATUS_PATH)
BADGE = "Illustrative data & outputs"

# Where the casework consume CLI lives + how to invoke it. Subprocess only — never imported.
# Resolution (Phase 67 — shippable from a bare clone): $AML_CASEWORK_DIR override > the VENDORED copy
# (vendor/aml-casework, present after `make setup` — the shippable default) > the ../aml-casework sibling
# (a dev checkout). Neither present → the GATED message fires honestly. Overridable for any layout.
def _resolve_casework_dir() -> Path:
    env = os.environ.get("AML_CASEWORK_DIR")
    if env:
        return Path(env)
    vendored = ROOT / "vendor" / "aml-casework"
    if (vendored / "src" / "aml_casework").is_dir():
        return vendored
    return ROOT.parent / "aml-casework"


CASEWORK_DIR = _resolve_casework_dir()


def casework_python() -> str:
    """The interpreter that runs the casework consume (Phase 67 cross-platform): $AML_CASEWORK_PYTHON >
    the casework venv built by `python scripts/setup_workbench.py` (Windows: .venv\\Scripts\\python.exe;
    POSIX: .venv/bin/python) > this interpreter."""
    explicit = os.environ.get("AML_CASEWORK_PYTHON")
    if explicit:
        return explicit
    venv = CASEWORK_DIR / ".venv" / ("Scripts" if os.name == "nt" else "bin") / ("python.exe" if os.name == "nt" else "python")
    return str(venv) if venv.exists() else sys.executable


def casework_corpus_env() -> dict:
    """Point SIGNAL_WATCH_CORPUS at the vendored (or sibling) pinned corpus snapshot, so the
    corpus_grounding verifier grounds REGARDLESS of how casework is installed — source-on-PYTHONPATH OR a
    wheel/pip install in site-packages (where the package-relative default root would not resolve). No-op
    if the snapshot is absent."""
    corpus = CASEWORK_DIR / "fixtures" / "corpus" / "fincen-alerts" / "derived"
    return {"SIGNAL_WATCH_CORPUS": str(corpus)} if corpus.is_dir() else {}


class RunError(ValueError):
    """A pipeline failure with a NAMED, analyst-actionable reason — emitted verbatim in-stream
    (the serve_corpus DeriveError pattern), never disguised as a generic crash."""


# ---- the vendored case library (data, read-only) ------------------------------------------------
def load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def list_cases(manifest: dict | None = None) -> list:
    """The library index GET /cases returns — display metadata only (no transaction bodies)."""
    m = manifest or load_manifest()
    out = []
    for c in m.get("cases", []):
        out.append({k: c.get(k) for k in
                    ("case_id", "title", "summary", "subject", "alert_count", "txn_count",
                     "capabilities", "provenance")})
    return out


def _case(manifest: dict, case_id: str) -> dict:
    for c in manifest.get("cases", []):
        if c.get("case_id") == case_id:
            return c
    raise RunError(f"unknown case '{case_id}' — not in the vendored library (GET /cases)")


def _bundle_path(case: dict) -> Path:
    return CASES_DIR / case["bundle"]


# ---- the flag→corpus audit walk (the demo's defensibility beat) ---------------------------------
def _corpus_lookup(advisory_id: str, indicator_id: str) -> dict | None:
    """Resolve <advisory_id>:<indicator_id> to the FROZEN corpus record: the verbatim flag, the
    natural-AML red_flag translation, and the source regulator (the dir under data/)."""
    matches = sorted(glob.glob(str(ROOT / "data" / "*" / "derived" / f"{advisory_id}.json")))
    if not matches:
        return None
    path = matches[0]
    source = Path(path).parent.parent.name  # data/<source>/derived/<id>.json -> <source>
    record = json.loads(Path(path).read_text(encoding="utf-8"))

    def walk(o):
        if isinstance(o, dict):
            if o.get("id") == indicator_id:
                yield o
            for v in o.values():
                yield from walk(v)
        elif isinstance(o, list):
            for v in o:
                yield from walk(v)

    for ind in walk(record):
        return {"source": source, "flag": ind.get("flag", ""), "red_flag": ind.get("red_flag", "")}
    return None


def audit_walk(bundle: dict) -> list:
    """Per alert: the chain from the fired detector down to the verbatim regulator flag in the frozen
    corpus, with a GROUNDED verdict (the bundle's flag is a normalize()-substring of the corpus flag).
    This is the analyst's defensibility walk — every signal traces to a public-source indicator."""
    walk = []
    for a in bundle.get("alerts", []):
        g = a.get("grounding", {})
        adv, ind = g.get("advisory_id", ""), g.get("indicator_id", "")
        corpus = _corpus_lookup(adv, ind)
        grounded = bool(corpus) and normalize(g.get("flag", "")) in normalize(corpus["flag"])
        walk.append({
            "capability": a.get("capability"),
            "detector": a.get("detector"),
            "rule": a.get("rule"),
            "signal_id": g.get("signal_id"),
            "advisory_id": adv,
            "indicator_id": ind,
            "source": corpus["source"] if corpus else None,
            "corpus_flag": corpus["flag"] if corpus else None,
            "red_flag": corpus["red_flag"] if corpus else None,
            "grounded": grounded,
        })
    return walk


# ---- drafter backends (server-side creds/endpoints; the browser picks by NAME only) --------------
# The neural draft is casework's pluggable Drafter Protocol. serve_chain offers a SET of backends; the
# browser sends a backend NAME from BACKENDS, serve_chain maps it to the casework CLI's --drafter flag.
# CREDS + ENDPOINTS live in serve_chain's OWN env (inherited by the casework subprocess in
# casework_consume) and NEVER cross to the browser — the served config exposes only names + booleans
# (non-negotiable §4.5: no key/token/base_url in the frontend). 'stub' is always available
# (deterministic, no model); a neural backend is available iff its server-side env is present.
BACKENDS = ("stub", "claude", "openai", "opencode")

# The server-side env that makes each neural backend available (values are NEVER serialized to the page).
#   claude   — Anthropic: OAuth subscription (ANTHROPIC_AUTH_TOKEN) OR an API key (ANTHROPIC_API_KEY)
#   openai   — any OpenAI-standard /v1 server (OPENAI_BASE_URL; key optional for a local model)
#   opencode — drafting driven THROUGH opencode's agent loop (OPENCODE_SERVE_URL — its serve endpoint)
_BACKEND_ENV = {
    "claude": ("ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_API_KEY"),
    "openai": ("OPENAI_BASE_URL",),
    "opencode": ("OPENCODE_SERVE_URL", "OPENCODE_BASE_URL"),
}

# A local OpenAI-compatible model is conventionally on this port, so `openai` needs NO env to be usable —
# OPENAI_BASE_URL only OVERRIDES the host/port. (A localhost URL is not a secret; §4.5 still holds — the
# browser never sees it.) If no model is actually listening, the run fails fast (TCP refused) and the stub
# takes over with a clear "no model at <this>" note — never a silent stub-as-neural.
DEFAULT_OPENAI_BASE = "http://127.0.0.1:8080/v1"


def backend_available(name: str, env: dict | None = None) -> bool:
    """Is `name` usable given the SERVER-SIDE env? stub always; openai always (it has a built-in default
    localhost endpoint — no env required); claude/opencode iff their endpoint/cred env is present (only
    this boolean ever leaves the server — never the value)."""
    e = env if env is not None else os.environ
    if name in ("stub", "openai"):
        return True
    return any(e.get(k) for k in _BACKEND_ENV.get(name, ()))


def available_backends(env: dict | None = None) -> list:
    """The backends the presenter may pick, in display order (stub first — the always-on baseline)."""
    return [b for b in BACKENDS if backend_available(b, env)]


def default_backend(env: dict | None = None) -> str:
    """The auto-default when the browser names none: claude (if a key/token), else openai ONLY IF
    OPENAI_BASE_URL is EXPLICITLY set, else opencode (if wired), else stub. openai is always one-CLICK
    available (backend_available), but it is NOT the silent auto-default unless the operator pointed at a
    model — so a box with no model isn't auto-aimed at a dead :8080 on every action (it stays clean stub)."""
    e = env if env is not None else os.environ
    if backend_available("claude", e):
        return "claude"
    if e.get("OPENAI_BASE_URL"):
        return "openai"
    if backend_available("opencode", e):
        return "opencode"
    return "stub"


def resolve_backend(requested: str | None, env: dict | None = None) -> dict:
    """Map a browser-sent backend NAME to the effective drafter, SERVER-SIDE. Returns
    {requested, effective, available, note}. An unknown or unavailable backend falls back HONESTLY to
    the stub (never a crash, never a silent neural→neural switch) with a named note; an empty request
    uses the default. The effective name is what gets passed to the casework CLI's --drafter."""
    avail = available_backends(env)
    req = (requested or "").strip().lower()
    if not req:
        return {"requested": None, "effective": default_backend(env), "available": avail, "note": None}
    if req not in BACKENDS:
        return {"requested": requested, "effective": "stub", "available": avail,
                "note": f"unknown backend '{requested}' — fell back to the deterministic stub"}
    if req not in avail:
        return {"requested": req, "effective": "stub", "available": avail,
                "note": f"backend '{req}' unavailable server-side (no endpoint/key) — fell back to the stub"}
    return {"requested": req, "effective": req, "available": avail, "note": None}


def drafter_for_env(env: dict | None = None) -> str:
    """Back-compat alias for the AUTO default (the CLI banner + /health). The neural draft is opt-in by
    the presence of server-side env the browser never sees."""
    return default_backend(env)


# ---- the casework consume (subprocess of the SIBLING's OWN CLI; injectable for the offline test) --
def casework_consume(bundle_path: Path, out_path: Path, drafter: str, *, disposition: str = "file") -> dict:
    """Subprocess `python -m aml_casework.ingest <bundle> --out <signed> --drafter <drafter>
    --disposition <disposition>` and read back the signed SAR it wrote. file-handoff only — NO sibling
    import. `disposition` is the claimed human disposition the CW-4 `cleared` path consumes (default
    "file"; "cleared" for an affirmative documented dismissal). Returns the consume result
    {drafter, drafter_effective, signed, disposition, blocking_violations, narrative_present, completeness}.

    Until the casework consume CLI lands (aml-casework/docs/consume-cli-PLAN-BRIEF.md), this raises a
    NAMED RunError — the bridge is honestly gated, never faked."""
    src = CASEWORK_DIR / "src"
    py = casework_python()
    if not src.exists():
        raise RunError(f"aml-casework not found at {CASEWORK_DIR} (set AML_CASEWORK_DIR) — the consume "
                       f"CLI is the sibling prerequisite; the chain is GATED until it lands")
    env = dict(os.environ)
    env["PYTHONPATH"] = str(src) + os.pathsep + env.get("PYTHONPATH", "")
    env.update(casework_corpus_env())
    env.setdefault("OPENAI_BASE_URL", DEFAULT_OPENAI_BASE)   # the openai drafter defaults to the local model
    cmd = [py, "-m", "aml_casework.ingest", str(bundle_path),
           "--out", str(out_path), "--drafter", drafter, "--disposition", disposition]
    try:
        proc = subprocess.run(cmd, cwd=str(CASEWORK_DIR), env=env, capture_output=True,
                              text=True, timeout=300)
    except (OSError, subprocess.SubprocessError) as ex:
        raise RunError(f"casework consume could not be launched: {ex}") from None
    if proc.returncode != 0 or not out_path.exists():
        tail = (proc.stderr or proc.stdout or "").strip().splitlines()[-3:]
        raise RunError("casework consume failed (the consume CLI may not be implemented yet — bridge "
                       "gated; see aml-casework/docs/consume-cli-PLAN-BRIEF.md): " + " | ".join(tail))
    return _consume_result_from_sar(json.loads(out_path.read_text(encoding="utf-8")), drafter)


def _consume_result_from_sar(sar: dict, drafter: str) -> dict:
    """Derive the consume-stage view from the SIGNED SAR (the contract artifact — more robust than the
    CLI's stdout). drafter_effective falls back honestly if the SAR records a stub fallback."""
    s = sar.get("str_record", {})
    so = sar.get("signoff", {})
    eff = (sar.get("drafter_effective") or so.get("drafter") or drafter)
    return {
        "drafter": drafter,
        "drafter_effective": eff,
        "signed": so.get("signed") is True,
        "disposition": so.get("disposition"),
        "blocking_violations": so.get("blocking_violations", []),
        "narrative_present": bool(s.get("narrative")),
        "completeness": s.get("completeness", {}),
    }


# ---- the e2e_chain_check verify (subprocess; pillar-status snapshot+restored) --------------------
def verify_e2e(bundle_path: Path, signed_path: Path) -> dict:
    """Subprocess `e2e_chain_check.py --real --substrate <bundle> --casework <signed>` and read the
    verdict. The committed data/pillar-status.json is SNAPSHOT before and RESTORED after — a workbench
    run reflects the pre-baked bridge states, it must never move the committed file (the launcher inlines
    it; a move would drift --check all). Returns {connected, exit, output}."""
    snapshot = STATUS_PATH.read_bytes() if STATUS_PATH.exists() else None
    cmd = [sys.executable, str(E2E_SCRIPT), "--real",
           "--substrate", str(bundle_path), "--casework", str(signed_path)]
    try:
        proc = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, timeout=120)
        out = (proc.stdout or "") + (proc.stderr or "")
        connected = proc.returncode == 0 and "CONNECTED" in out
        return {"connected": connected, "exit": proc.returncode, "output": out.strip()}
    finally:
        # restore the committed bridge states regardless of the run's outcome
        if snapshot is not None:
            STATUS_PATH.write_bytes(snapshot)


# ---- the run pipeline (stage-streamed; consume + verify injectable for the offline selftest) -----
def run_case(case_id: str, *, on_stage, consume=casework_consume, verify=verify_e2e,
             drafter: str | None = None, tmpdir: Path | None = None, env: dict | None = None) -> dict:
    """Drive one case end to end, emitting stages via on_stage(stage, **detail). Returns the final
    payload {case, bundle_summary, signed_sar, consume, verify, audit_walk, connected}.

    `drafter` is the browser-sent backend NAME (resolved server-side against `env`/os.environ — creds
    never crossed the wire). `consume`/`verify` are injected so the selftest runs OFFLINE (casework
    subprocess stubbed); the defaults are the real subprocesses. A failed stage raises RunError
    (named, emitted in-stream)."""
    manifest = load_manifest()
    case = _case(manifest, case_id)
    bundle_path = _bundle_path(case)
    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))

    # stage 1 — evidence (the pre-baked detection input)
    on_stage("evidence", case_id=case_id,
             alert_count=len(bundle.get("alerts", [])), txn_count=len(bundle.get("transactions", [])),
             capabilities=[a.get("capability") for a in bundle.get("alerts", [])],
             subject=bundle.get("subject", {}))

    # stage 2 — consume (the LIVE casework SAR draft + the 6 Class-G verifiers, via the sibling CLI).
    # `drafter` is the browser-sent backend NAME; resolve it SERVER-SIDE (unknown/unavailable → honest stub).
    resolved = resolve_backend(drafter, env)
    eff_drafter = resolved["effective"]
    on_stage("consume", drafter=eff_drafter, requested=resolved["requested"],
             available=resolved["available"], note=resolved["note"], status="running")
    tdir = tmpdir or Path(os.environ.get("TMPDIR", "/tmp"))
    signed_path = tdir / f"{case_id}-signed.json"
    consume_res = consume(bundle_path, signed_path, eff_drafter)
    on_stage("consume", status="done", **consume_res)

    # stage 3 — cross-pillar verify (signal-watch re-verifies the join; pillar-status preserved)
    on_stage("verify", status="running")
    verify_res = verify(bundle_path, signed_path)
    on_stage("verify", status="done", connected=verify_res["connected"], exit=verify_res["exit"])

    # stage 4 — connected (the final payload + the flag→corpus audit walk)
    signed_sar = json.loads(signed_path.read_text(encoding="utf-8")) if signed_path.exists() else None
    # Phase 69 — the COMPLETENESS measurement: required STR elements (vs casework's completeness dict) +
    # the determination ATOMS the case carries vs the honest gaps. crime_type comes from the stamped STR
    # record (casework), falling back to the capability→offence map for the stub. Pure; renders honest-NULL.
    _rec = (signed_sar or {}).get("str_record", {})
    _caps = [c.get("capability") for c in case.get("capabilities", []) if isinstance(c, dict)]
    _ct = _rec.get("crime_type") or crime_type_for_capabilities(_caps, _requirements())
    completeness = (assess_completeness(_ct, _caps, _requirements(), str_completeness=_rec.get("completeness", {}))
                    if _ct else {"crime_type": None, "profiled": False,
                                 "str": {"required": [], "satisfied": [], "missing": []},
                                 "atoms": [], "present_atom_ids": []})
    payload = {
        "case": {k: case.get(k) for k in ("case_id", "title", "summary", "subject", "provenance")},
        "bundle_summary": {
            "alert_count": len(bundle.get("alerts", [])),
            "txn_count": len(bundle.get("transactions", [])),
            "capabilities": case.get("capabilities", []),
        },
        "consume": consume_res,
        "verify": verify_res,
        "signed_sar": signed_sar,
        "completeness": completeness,
        "audit_walk": audit_walk(bundle),
        "connected": verify_res["connected"] and consume_res["signed"],
    }
    on_stage("connected" if payload["connected"] else "not_connected", **{
        "connected": payload["connected"]})
    return payload


# ---- the offline casework stand-in (TEST DOUBLE — the selftest's stub, NEVER the real consume) ---
def _stub_signed_sar(bundle_path: Path, out_path: Path, drafter: str) -> dict:
    """A deterministic, offline stand-in for the casework consume — builds a check_chain-passing signed
    SAR from the bundle WITHOUT the sibling CLI (the seam stays open until that CLI lands). Used ONLY by
    --selftest. It mirrors the casework contract's signed-SAR shape: seam flipped, six completeness
    elements, one grounded inculpatory claim per alert, signed signoff with empty blocking_violations."""
    bundle = json.loads(Path(bundle_path).read_text(encoding="utf-8"))
    sar = copy.deepcopy(bundle)
    rec = sar.setdefault("str_record", {})
    acct = (bundle.get("subject", {}).get("account_ids") or ["the subject account"])[0]
    rec["narrative"] = (f"Account {acct} exhibits a multi-typology laundering pattern across the "
                        f"reviewed period; each signal is grounded to the cited transactions and the "
                        f"regulator corpus.")
    rec["narrative_claims"] = [
        {"text": f"Detector {a.get('detector')} fired and grounds to its cited indicator.",
         "cites": [a.get("grounding", {}).get("signal_id")], "stance": "inculpatory"}
        for a in bundle.get("alerts", [])
    ]
    comp = rec.setdefault("completeness", {})
    for el in e2e_chain_check.STR_REQUIRED_ELEMENTS:
        comp.setdefault(el, True)
    comp["grounds_for_suspicion_narrative"] = True
    sar["signoff"] = {"signed": True, "signer": "SYNTHETIC-stub (offline selftest)",
                      "ts": "2026-06-17T00:00:00", "disposition": "file", "blocking_violations": []}
    sar["drafter_effective"] = "stub"
    Path(out_path).write_text(json.dumps(sar, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return _consume_result_from_sar(sar, drafter)


# ---- the served page (chain.html + the workbench config) -----------------------------------------
# An HTML-comment marker so the RAW chain.html stays valid, lintable, self-contained JS (the client
# falls back to defaults when window.__CHAIN_CONFIG__ is absent). render_page replaces the marker with a
# config <script>; tests/chain.test.mjs loads the raw template the same way (set window.__CHAIN_CONFIG__).
CHAIN_PLACEHOLDER = "<!--__CHAIN_CONFIG__-->"


def _drafter_config(env: dict | None = None) -> dict:
    """The drafter view the browser gets — NAMES + booleans ONLY, never a key/token/base_url (§4.5).
    `backends` drives the picker; `available` is the subset the presenter may actually run."""
    return {"mode": drafter_for_env(env), "key_present": backend_available("claude", env),
            "default": default_backend(env), "available": available_backends(env),
            "backends": [{"name": b, "available": backend_available(b, env)} for b in BACKENDS]}


def live_config(server=None, env: dict | None = None) -> dict:
    return {"cases": "/cases", "run": "/run", "health": "/health", "badge": BADGE,
            "drafter": _drafter_config(env)}


def render_page(cfg: dict) -> str:
    """Inline the workbench config into chain.html (T4). If the template is absent (the spine is built
    before T4), serve a labeled placeholder — the companion is still functional via /cases + /run."""
    if not CHAIN_TEMPLATE.exists():
        return ("<!doctype html><meta charset=utf-8><title>Chain workbench</title>"
                f"<body style='font-family:monospace;background:#111;color:#eee;padding:2rem'>"
                f"<h1>Chain workbench companion</h1><p>{BADGE}</p>"
                "<p>chain.html (T4) is not built yet. The API is live: "
                "<code>GET /cases</code>, <code>POST /run</code>, <code>GET /health</code>.</p>")
    template = CHAIN_TEMPLATE.read_text(encoding="utf-8")
    n = template.count(CHAIN_PLACEHOLDER)
    if n != 1:
        raise RunError(f"expected exactly one {CHAIN_PLACEHOLDER} in chain.html, found {n}")
    inject = f"<script>window.__CHAIN_CONFIG__ = {json.dumps(cfg, ensure_ascii=False)};</script>"
    return template.replace(CHAIN_PLACEHOLDER, inject)


# ---- HTTP (the serve_corpus handler conventions: NDJSON stages, single-flight, named errors) -----
class Handler(BaseHTTPRequestHandler):
    server_version = "SignalWatchChainWorkbench/0.1"

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
            self._send(200, render_page(live_config(self.server)).encode("utf-8"),
                       "text/html; charset=utf-8")
        elif path == "/cases":
            self._json(200, {"badge": BADGE, "cases": list_cases()})
        elif path == "/health":
            self._json(200, {"ok": True, "live": True, "persist": False,
                             "drafter": drafter_for_env(), "backends": available_backends(),
                             "casework_dir": str(CASEWORK_DIR)})
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
            self._json(400, {"error": "missing 'case' (the case_id to run; GET /cases lists them)"}); return
        # the browser sends only a backend NAME; serve_chain resolves it server-side (creds never crossed)
        backend = (payload.get("backend") or payload.get("drafter") or "").strip() or None
        # SINGLE-FLIGHT (the Phase-43 lesson): a second concurrent run would split the model's
        # throughput AND race the pillar-status snapshot/restore — honest 409 pre-stream instead.
        lock = self.server.__dict__.setdefault("run_lock", threading.Lock())
        if not lock.acquire(blocking=False):
            self._json(409, {"error": "another case run is already in progress — wait for it to finish "
                                      "(single-flight: the verify step snapshots pillar-status)"}); return
        try:
            self.send_response(200)
            self.send_header("Content-Type", "application/x-ndjson; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            try:
                import tempfile
                with tempfile.TemporaryDirectory() as td:
                    payload_out = run_case(case_id, tmpdir=Path(td), drafter=backend,
                                           on_stage=lambda stage, **kw: self._emit({"stage": stage, **kw}))
                self._emit({"done": payload_out})
            except RunError as ex:
                self._emit({"error": str(ex)})
            except (OSError, ValueError, KeyError, json.JSONDecodeError) as ex:
                self._emit({"error": f"run failed: {ex}"})
        except (BrokenPipeError, ConnectionResetError):
            self.log_message("client disconnected mid-run stream")  # nothing persisted by design
        finally:
            lock.release()

    def log_message(self, fmt, *a):
        sys.stderr.write("[serve_chain] " + (fmt % a) + "\n")


# ---- selftest (offline: no socket, casework consume stubbed) ------------------------------------
def selftest() -> int:
    failures = []

    # the vendored library validates (reuses validate_chain_cases — single source of truth)
    manifest = load_manifest()
    lib_v = validate_chain_cases.validate_library(manifest, str(CASES_DIR))
    if lib_v:
        failures.append(f"library should validate clean: {lib_v}")

    # GET /cases shape: display metadata only, no transaction bodies leaked
    cases = list_cases(manifest)
    assert cases and all("case_id" in c for c in cases), "cases listing empty/malformed"
    assert all("transactions" not in c for c in cases), "cases listing must not carry txn bodies"
    case_id = cases[0]["case_id"]

    # backend availability from SERVER-SIDE env (the browser only ever sends a NAME)
    assert backend_available("stub", {}) and backend_available("stub", {"X": "1"})
    assert backend_available("claude", {"ANTHROPIC_AUTH_TOKEN": "oauth-x"})   # OAuth subscription
    assert backend_available("claude", {"ANTHROPIC_API_KEY": "sk-x"})         # or an API key
    assert not backend_available("claude", {})
    assert backend_available("openai", {"OPENAI_BASE_URL": "http://127.0.0.1:8080/v1"})
    assert backend_available("openai", {})         # openai ALWAYS usable — it defaults to 127.0.0.1:8080 (no env)
    assert backend_available("opencode", {"OPENCODE_SERVE_URL": "http://127.0.0.1:4096"})
    assert not backend_available("opencode", {})
    assert available_backends({}) == ["stub", "openai"]    # openai always selectable; claude/opencode need their env
    assert available_backends({"OPENAI_BASE_URL": "http://x/v1"}) == ["stub", "openai"]

    # back-compat auto-default (Phase-56): key present -> claude, absent -> stub
    assert drafter_for_env({"ANTHROPIC_API_KEY": "sk-x"}) == "claude"
    assert drafter_for_env({}) == "stub"                                    # openai is one-click, NOT the silent
    assert default_backend({}) == "stub"                                    #   auto-default without an explicit URL
    assert default_backend({"OPENAI_BASE_URL": "http://x/v1"}) == "openai"   # explicit URL -> auto-default openai
    assert resolve_backend("openai", {})["effective"] == "openai"           # picked openai w/ no env still runs (defaults :8080)

    # name pass-through + HONEST fallback (never a crash, never a silent neural->neural switch)
    full = {"ANTHROPIC_API_KEY": "sk-x", "OPENAI_BASE_URL": "http://x/v1"}
    assert resolve_backend("openai", full)["effective"] == "openai"
    assert resolve_backend("claude", full)["effective"] == "claude"
    assert resolve_backend(None, full)["effective"] == "claude"             # default = first neural
    r_unavail = resolve_backend("opencode", full)                          # known but unavailable here
    assert r_unavail["effective"] == "stub" and "unavailable" in (r_unavail["note"] or "")
    r_unknown = resolve_backend("../etc/passwd", full)                     # unknown name -> stub, no injection
    assert r_unknown["effective"] == "stub" and "unknown" in (r_unknown["note"] or "")
    assert resolve_backend("stub", {})["effective"] == "stub"

    # NO creds/endpoints reach the browser: the served config + page carry only names + booleans (§4.5)
    secret_env = {"ANTHROPIC_API_KEY": "sk-SECRET-DEADBEEF", "ANTHROPIC_AUTH_TOKEN": "oauth-SECRET-DEADBEEF",
                  "OPENAI_API_KEY": "sk-openai-SECRET", "OPENAI_BASE_URL": "http://127.0.0.1:8080/v1",
                  "OPENCODE_SERVE_URL": "http://127.0.0.1:4096"}
    cfg_secret = live_config(env=secret_env)
    blob = json.dumps(cfg_secret) + render_page(cfg_secret)
    for leak in ("sk-SECRET-DEADBEEF", "oauth-SECRET-DEADBEEF", "sk-openai-SECRET",
                 "127.0.0.1:8080", "127.0.0.1:4096"):
        assert leak not in blob, f"server-side cred/endpoint leaked into the served config/page: {leak}"
    assert [b["name"] for b in cfg_secret["drafter"]["backends"]] == list(BACKENDS)
    assert cfg_secret["drafter"]["available"] == ["stub", "claude", "openai", "opencode"]

    # the audit walk grounds every alert to the frozen corpus
    bundle = json.loads(_bundle_path(_case(manifest, case_id)).read_text(encoding="utf-8"))
    walk = audit_walk(bundle)
    assert walk and all(w["grounded"] for w in walk), [w for w in walk if not w["grounded"]]
    assert all(w["source"] and w["corpus_flag"] and w["red_flag"] for w in walk), walk

    # the FULL run OFFLINE: casework consume STUBBED, e2e_chain_check verify is REAL (offline, pure
    # Python) — the committed pillar-status.json is snapshot+restored by verify_e2e. Reaches CONNECTED.
    status_before = STATUS_PATH.read_bytes() if STATUS_PATH.exists() else None
    stages = []
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        payload = run_case(case_id, tmpdir=Path(td), drafter="stub",
                           consume=_stub_signed_sar, on_stage=lambda s, **kw: stages.append((s, kw)))
    seq = [s for s, _ in stages]
    for needed in ("evidence", "consume", "verify", "connected"):
        if needed not in seq:
            failures.append(f"stage '{needed}' missing from {seq}")
    if not payload["connected"]:
        failures.append(f"stubbed run should reach CONNECTED, got verify={payload['verify']}, "
                        f"consume={payload['consume']}")
    if not payload["signed_sar"] or not payload["audit_walk"]:
        failures.append("final payload missing signed_sar / audit_walk")
    # Phase 69 — the COMPLETENESS measurement rides the payload: the mule is money_laundering, its
    # mechanism atoms light up from the structuring/funnel/pass-through capabilities, and the determination
    # legs that did NOT fire are the honest GAPS the GATHER beat targets (the "lazy filing" made visible).
    comp = payload.get("completeness") or {}
    if not comp.get("profiled") or comp.get("crime_type") != "money_laundering":
        failures.append(f"the mule completeness should profile money_laundering, got {comp.get('crime_type')}")
    if "ML-A1" not in comp.get("present_atom_ids", []) and "ML-A2" not in comp.get("present_atom_ids", []):
        failures.append(f"a mechanism atom should be present for the mule, got {comp.get('present_atom_ids')}")
    if not any(not a["present"] for a in comp.get("atoms", [])):
        failures.append("the mule should carry at least one HONEST GAP (an unmet determination atom)")
    # the committed pillar-status.json MUST be byte-identical after the run (no launcher drift)
    status_after = STATUS_PATH.read_bytes() if STATUS_PATH.exists() else None
    if status_before != status_after:
        failures.append("data/pillar-status.json was mutated by a run (verify_e2e must snapshot+restore)")

    # the run resolves the requested backend SERVER-SIDE and hands the EFFECTIVE name to consume:
    # an available request passes through; an unavailable one falls back to the stub (deterministic env)
    for requested, env_in, expect in (("openai", {"OPENAI_BASE_URL": "http://x/v1"}, "openai"),
                                      ("opencode", {"OPENAI_BASE_URL": "http://x/v1"}, "stub")):
        seen = {}
        with tempfile.TemporaryDirectory() as td:
            run_case(case_id, tmpdir=Path(td), drafter=requested, env=env_in,
                     consume=lambda b, o, d: (seen.__setitem__("d", d), _stub_signed_sar(b, o, d))[1],
                     on_stage=lambda s, **kw: None)
        if seen.get("d") != expect:
            failures.append(f"backend '{requested}' should resolve to '{expect}', consume saw {seen.get('d')!r}")

    # honest GATED path: the REAL casework consume on an absent CLI raises a NAMED RunError (not a crash)
    try:
        with tempfile.TemporaryDirectory() as td:
            run_case(case_id, tmpdir=Path(td), drafter="stub",
                     consume=lambda b, o, d: (_ for _ in ()).throw(
                         RunError("casework consume failed (bridge gated)")),
                     on_stage=lambda s, **kw: None)
        failures.append("a failing consume should raise RunError, not pass")
    except RunError as ex:
        if "gated" not in str(ex):
            failures.append(f"gated error not surfaced: {ex}")

    # error path: an unknown case is a NAMED RunError
    try:
        run_case("CASE-DOES-NOT-EXIST", on_stage=lambda s, **kw: None, consume=_stub_signed_sar)
        failures.append("unknown case should raise RunError")
    except RunError:
        pass

    # the served page: placeholder substituted iff chain.html exists (T4); config inlined
    cfg = live_config()
    page = render_page(cfg)
    if CHAIN_TEMPLATE.exists():
        assert CHAIN_PLACEHOLDER not in page, "chain config placeholder survived substitution"
        assert '"run"' in page and BADGE in page, "workbench config / badge not inlined"
    else:
        assert BADGE in page, "placeholder page must still carry the badge"

    if failures:
        for f in failures:
            print(f"FAIL: {f}", file=sys.stderr)  # noqa: T201
        return 1
    print(f"serve_chain --selftest: PASS ({len(cases)} vendored case(s); audit walk grounds "  # noqa: T201
          f"{len(walk)}/{len(walk)} alerts; stubbed run streams {seq} -> CONNECTED; "
          f"pillar-status byte-stable; gated/error paths named)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Chain workbench companion (dev/authoring-time only; never a ship artifact).")
    ap.add_argument("--port", type=int, default=DEFAULT_PORT)
    ap.add_argument("--selftest", action="store_true", help="offline assertions (no socket, casework stubbed), exit")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    httpd = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    drafter = drafter_for_env()
    print(f"[serve_chain] chain workbench on http://localhost:{args.port}/  "  # noqa: T201
          f"(casework={CASEWORK_DIR}, drafter={drafter})")
    print(f"[serve_chain] {'ANTHROPIC_API_KEY set — LIVE neural SAR draft' if drafter == 'claude' else 'no key — deterministic stub draft'}; "  # noqa: T201
          "nothing is persisted; the offline dists stay byte-frozen. Ctrl-C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[serve_chain] stopped.")  # noqa: T201
    return 0


if __name__ == "__main__":
    sys.exit(main())
