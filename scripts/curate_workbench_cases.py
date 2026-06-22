#!/usr/bin/env python3
"""Curate the investigator case-workbench population (Phase 63 — authoring-time ONLY).

Vendors a DETERMINISTIC bounded slice of aml-substrate's real (synthetic) evidence-bundle emission
into signal-watch as the workbench's case population. The substrate emit is run as TOOL-USE
(file-contract; build.py NEVER imports the substrate — the Phase-62 probe-history pattern). The raw
bundles are vendored verbatim under data/workbench/bundles/ (the surface of truth, like a corpus
`<id>.md`); the curated index data/workbench/cases.json carries the per-case display summary, the
precedent-confidence badge, the exemplar tags, and the coverage statistic.

GROUNDING / HONESTY (the Phase-62 split):
  * The detection side is GROUNDED — real substrate detectors (C2-C5/C15) firing real
    advisory-grounded alerts over real (synthetic) KYC profiles. meta.synthetic holds -> "no real data".
  * The precedent-confidence SAMPLE SIZE is REAL (the fired-signal combo's frequency over the full
    emitted population); the DISPOSITION direction is ILLUSTRATIVE ("chosen, not measured"), bucketed
    from the sample size. The always-on "Illustrative data & outputs" badge stays.
  * Display name/dob are SYNTHETIC labels (the substrate omits PII by privacy design) laid over the
    REAL grounded KYC (risk/cdd/pep/occupation/source-of-funds). The risk-relevant profile is real.
  * Exemplars are tagged by SIGNAL COMPOSITION (label-blind) — the system surfaces composition, not
    ground truth; "textbook mule" means "looks like one by its grounded signals", a demo framing.

Regenerate (deterministic — substrate seed, no clock):
  # 1. run the substrate emit (in the aml-substrate session / as tool-use):
  PYTHONPATH=<substrate>/src <substrate>/.venv/bin/python -m aml_substrate.cli \
      --clients 40000 --months 2 --seed 0 --emergence --monitor --emit-evidence --emit-screening \
      --out /tmp/sw-wb-run
  # 2. vendor the slice + MEASURE real end-to-end grounding through aml-casework (the committed artifact):
  python3 scripts/curate_workbench_cases.py --from /tmp/sw-wb-run/evidence --measure-casework ../aml-casework
  python3 scripts/curate_workbench_cases.py --selftest   # validate the committed slice, no run needed

COVERAGE IS MEASURED, NOT ASSUMED: --measure-casework runs casework's deterministic stub over each
vendored bundle and records `grounds_e2e` per case. The six Class-G verifiers independently re-derive
each signal and REFUSE to sign what they can't reproduce — so the COMPOSED mules (the substrate's fan-IN
C3 / shell C15) fail casework's fan-OUT C3 / C15 replay and DON'T sign. That cross-pillar divergence is
the gate correctly refusing (the honest frontier), surfaced as the e2e_note — never loosened away.
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "data" / "workbench"
BUNDLES_DIR = OUT_DIR / "bundles"
CASES_JSON = OUT_DIR / "cases.json"

BADGE = "Illustrative data & outputs"
SUBSTRATE_REPO = "aml-substrate"
SUBSTRATE_HEAD = "f90bd39"
RUN_ID = "seed0-n40000-m2"
EMIT_COMMAND = ("PYTHONPATH=<substrate>/src <substrate>/.venv/bin/python -m aml_substrate.cli "
                "--clients 40000 --months 2 --seed 0 --emergence --monitor --emit-evidence "
                "--emit-screening --out /tmp/sw-wb-run")

# The capabilities aml-casework has a grounding_replay assertion for (the end-to-end resolvable set):
# txn-monitoring C2-C5 + C15, screening C7/C8/C14. C6 (velocity) + C26 (scam) are NOT casework-asserted.
GROUNDABLE_CAPS = frozenset({"C2", "C3", "C4", "C5", "C15", "C7", "C8", "C14"})

# Slice shape (deterministic): every rich (3+-capability) case + a capped sample of the 1-2 cap noise,
# so the queue keeps the REAL signal:noise feel (the alert-fatigue pain) with the composed cases buried.
RICH_CAP_FLOOR = 3
# Phase 66 — a wider ~320-case slice (more 4+-capability exemplars; a noise-heavy backdrop preserved so the
# composed cases stay BURIED — the alert-fatigue feel). VISIBLE volume, not detection difficulty (the
# substrate is single-signal-separable). Deterministic over the same f90bd39-gen population (seed 0).
DEFAULT_NOISE_CAP = 180
DEFAULT_RICH_CAP = 120

# Synthetic DISPLAY identity pools (clearly-synthetic labels over the real KYC; deterministic by id).
_FIRST = ["Avery", "Bao", "Camila", "Dmitri", "Elena", "Farah", "Gabriel", "Hana", "Ibrahim", "Jin",
          "Khadija", "Liam", "Mei", "Noor", "Omar", "Priya", "Quinn", "Rosa", "Sven", "Tariq",
          "Uma", "Viktor", "Wei", "Ximena", "Yara", "Zane"]
_LAST = ["Adeyemi", "Boucher", "Chen", "Dubois", "Ennis", "Ferreira", "Gagnon", "Hassan", "Ivanov",
         "Jain", "Kowalski", "Lefebvre", "Marchetti", "Nakamura", "Okafor", "Petrov", "Quirke",
         "Romano", "Singh", "Tremblay", "Ueda", "Volkov", "Wong", "Xu", "Yusuf", "Zhao"]
_ORG_SUFFIX = ["Holdings", "Trading Co.", "Group", "Logistics", "Ventures", "Services Ltd.",
               "Imports", "Capital", "Enterprises", "Partners"]


def _h(s: str) -> int:
    return int(hashlib.sha1(s.encode("utf-8")).hexdigest(), 16)


def synthetic_identity(party: dict, customer_id: str) -> dict:
    """A clearly-SYNTHETIC display label over the REAL grounded KYC. Deterministic from the id."""
    is_person = party.get("is_person", True)
    n = _h(customer_id)
    if is_person:
        name = f"{_FIRST[n % len(_FIRST)]} {_LAST[(n // 7) % len(_LAST)]}"
        year = 1956 + (n % 50)
        month = 1 + (n // 11) % 12
        day = 1 + (n // 13) % 28
        return {"kind": "person", "name": name, "dob": f"{year}-{month:02d}-{day:02d}",
                "synthetic_label": True}
    base = (party.get("nature_of_business") or "Numbered Company").split()[0]
    name = f"{base.title()} {_ORG_SUFFIX[n % len(_ORG_SUFFIX)]}"
    return {"kind": "org", "name": name, "synthetic_label": True}


def _caps(bundle: dict) -> list:
    return sorted({a.get("capability") for a in bundle.get("alerts", []) if a.get("capability")})


def _advisories(bundle: dict) -> list:
    return sorted({a.get("grounding", {}).get("advisory_id")
                   for a in bundle.get("alerts", []) if a.get("grounding", {}).get("advisory_id")})


# The GATING POLICY — the routing KNOBS over the REAL precedent sample size ("chosen, not measured").
# ONE source of truth: curate bakes the baseline gate with route(); serve_workbench's live engine
# RE-DERIVES routing from the same route() (and lets the presenter adjust the knobs + grow the session
# precedent — the Phase-64 elicitation loop). §12-grounded: the routing keys on the REAL firing
# frequency; the disposition direction it applies stays §14-illustrative.
GATING_POLICY = {
    "thresholds": {"high": 500, "medium": 50},   # n_precedent floors: >=high -> high, >=medium -> medium
    "gate_of_level": {"high": "auto-clear", "medium": "review", "low": "human-gate"},
    "cleared_pct": {"high": 88, "medium": 62, "low": 28},   # the ILLUSTRATIVE auto-clear share per level
    "basis": "chosen, not measured — routing knobs over the REAL precedent sample size",
}


def route(n_precedent: int, policy: dict = GATING_POLICY) -> dict:
    """Pure routing: map a precedent SAMPLE SIZE to a gate via the policy thresholds. The sample size is
    REAL (the combo's firing frequency); the gate + cleared_pct are ILLUSTRATIVE knobs. Common combo =
    large precedent = auto-clear; rare combo = small precedent = human-gate. Monotone by construction:
    a larger sample never yields a STRICTER gate."""
    th = policy["thresholds"]
    level = "high" if n_precedent >= th["high"] else "medium" if n_precedent >= th["medium"] else "low"
    return {"level": level, "gate": policy["gate_of_level"][level],
            "cleared_pct": policy["cleared_pct"][level]}


def _confidence(combo: str, n_precedent: int) -> dict:
    """Precedent-confidence: SAMPLE SIZE is REAL (the combo's firing frequency over the full
    population); the disposition direction + gate are ILLUSTRATIVE, routed from the sample size via the
    GATING_POLICY through route() (the live engine re-derives the SAME routing — one source of truth)."""
    r = route(n_precedent)
    cleared = r["cleared_pct"]
    return {
        "combo": combo,
        "n_precedent": n_precedent,
        "precedent_basis": "shared fired-signal combo frequency over the emitted population (REAL)",
        "level": r["level"],
        "gate": r["gate"],
        "disposition_illustrative": {"cleared_pct": cleared, "escalated_pct": 100 - cleared},
        "disposition_basis": "ILLUSTRATIVE — chosen, not measured (the substrate is label-blind)",
    }


def _measure_grounding(bundle_paths: dict, casework_dir: Path) -> dict:
    """Run aml-casework's deterministic stub drafter over each vendored bundle (TOOL-USE — file-handoff
    subprocess, NEVER an import) and record whether it SIGNS end-to-end. This is the REAL coverage: the
    six Class-G verifiers independently re-derive each signal and refuse to sign what they can't
    reproduce (e.g. the substrate's fan-IN C3 vs casework's fan-OUT C3 replay). casework@<pin> is the
    oracle — we MEASURE its verdict, never loosen it. Returns {case_id: {"signs": bool, "note": str}}."""
    src = casework_dir / "src"
    if not src.exists():
        raise ValueError(f"aml-casework not found at {casework_dir} (set --measure-casework) — needed to "
                         f"MEASURE real end-to-end grounding")
    venv = casework_dir / ".venv" / "bin" / "python"
    py = str(venv) if venv.exists() else sys.executable
    env = dict(os.environ)
    env["PYTHONPATH"] = str(src.resolve()) + os.pathsep + env.get("PYTHONPATH", "")
    out = {}
    for cid in sorted(bundle_paths):
        bp = str(Path(bundle_paths[cid]).resolve())
        with tempfile.NamedTemporaryFile(suffix=".json") as tf:
            try:
                proc = subprocess.run([py, "-m", "aml_casework.ingest", bp, "--out", tf.name,
                                       "--drafter", "stub"], cwd=str(casework_dir.resolve()), env=env,
                                      capture_output=True, text=True, timeout=120)
            except (OSError, subprocess.SubprocessError) as ex:
                out[cid] = {"signs": False, "note": f"casework could not run: {ex}"}
                continue
        lines = [ln for ln in proc.stdout.splitlines() if ln.strip().startswith("{")]
        try:
            summ = json.loads(lines[-1]) if lines else {}
        except json.JSONDecodeError:
            summ = {}
        signs = bool(summ.get("signed"))
        viols = summ.get("blocking_violations", []) if not signs else []
        # the dominant refused-capability(ies), human-readable (the C3/C15 cross-pillar divergence)
        caps = sorted({v.split("replay(")[1].split(")")[0] for v in viols if "replay(" in v})
        note = ("signed end-to-end" if signs else
                (f"casework refused — independent replay couldn't reproduce {', '.join(caps)} from the "
                 f"cited evidence ({len(viols)} violation(s))" if caps else
                 f"casework refused ({len(viols)} violation(s))"))
        out[cid] = {"signs": signs, "note": note}
    return out


def _read_population(evidence_dir: Path) -> list:
    """Read every emitted bundle (monitoring + screening run dirs) under <evidence_dir>. Returns a
    sorted-by-case_id list of (path, bundle) — deterministic regardless of filesystem order."""
    files = []
    for sub in sorted(p.name for p in evidence_dir.iterdir() if p.is_dir()):
        files += glob.glob(str(evidence_dir / sub / "*.json"))
    pop = []
    for f in sorted(set(files)):
        try:
            b = json.loads(Path(f).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if b.get("case_id"):
            pop.append((f, b))
    # de-dup by case_id (a customer can appear in both monitoring + screening dirs): keep the richer one
    by_id = {}
    for f, b in pop:
        cid = b["case_id"]
        if cid not in by_id or len(b.get("alerts", [])) > len(by_id[cid][1].get("alerts", [])):
            by_id[cid] = (f, b)
    return [by_id[k] for k in sorted(by_id)]


def select_slice(pop: list, combo_freq: dict, *, rich_cap: int, noise_cap: int,
                 sample_3cap: int = 20) -> tuple:
    """Deterministically pick the vendored slice: the rare 4+-capability cases + a sample of the 3-cap
    band (so all composition tiers are present) + a capped sample of the 1-2-cap noise (the
    alert-fatigue backdrop). Returns (selected, exemplars). Exemplars span the THREE gate levels:
    mule (rare composition → human-gate), ambiguous (medium → review), fp_trap + thin (common → auto-clear)."""
    enriched = []
    for f, b in pop:
        caps = _caps(b)
        combo = "+".join(caps)
        enriched.append({"f": f, "b": b, "caps": caps, "combo": combo,
                         "gate": _confidence(combo, combo_freq.get(combo, 0))["gate"],
                         "n_alerts": len(b.get("alerts", [])), "n_txns": len(b.get("transactions", [])),
                         "case_id": b["case_id"]})
    rich4 = sorted([e for e in enriched if len(e["caps"]) >= 4],
                   key=lambda e: (-len(e["caps"]), -e["n_alerts"], e["case_id"]))[:rich_cap]
    band3 = sorted([e for e in enriched if len(e["caps"]) == 3],
                   key=lambda e: (-e["n_alerts"], e["case_id"]))
    band3_sel = band3[::max(1, len(band3) // sample_3cap)][:sample_3cap] if band3 else []
    noise = sorted([e for e in enriched if len(e["caps"]) < RICH_CAP_FLOOR], key=lambda e: e["case_id"])
    noise_sel = noise[::max(1, len(noise) // noise_cap)][:noise_cap] if noise else []

    selected = sorted(rich4 + band3_sel + noise_sel, key=lambda e: e["case_id"])

    # Phase 66 — combo-coverage pass: guarantee EVERY population fired-signal combo has >=1 representative
    # in the slice (a WIDER combo spread — VISIBLE variety, not detection difficulty). Deterministic: the
    # lowest-case_id case of each combo the strided samples missed. Adds only the rare combos (no dupes).
    present = {e["combo"] for e in selected}
    seen_ids = {e["case_id"] for e in selected}
    by_combo: dict = {}
    for e in enriched:
        by_combo.setdefault(e["combo"], []).append(e)
    for combo, cands in sorted(by_combo.items()):
        if combo not in present:
            rep = min(cands, key=lambda e: e["case_id"])
            if rep["case_id"] not in seen_ids:
                selected.append(rep); seen_ids.add(rep["case_id"]); present.add(combo)
    selected = sorted(selected, key=lambda e: e["case_id"])

    # exemplars (label-blind, by composition × gate) — from the SELECTED slice so they're in the queue
    def pick(pool, key):
        return (sorted(pool, key=key)[0]["case_id"] if pool else None)
    s2 = [e for e in selected if len(e["caps"]) == 2]
    s1 = [e for e in selected if len(e["caps"]) == 1]
    review = [e for e in selected if e["gate"] == "review"] or [e for e in selected if len(e["caps"]) == 3]
    exemplars = {
        # richest composition, most alerts → the rare 'investigate this' case (human-gate)
        "mule": pick(selected, lambda e: (-len(e["caps"]), -e["n_alerts"], e["case_id"])),
        # a medium-confidence composed case → the 'needs a look' case (review)
        "ambiguous": pick(review, lambda e: (-len(e["caps"]), -e["n_alerts"], e["case_id"])),
        # the busiest common 2-signal case → 'looks busy, auto-cleared noise' (auto-clear)
        "fp_trap": pick(s2, lambda e: (-e["n_txns"], -e["n_alerts"], e["case_id"])),
        # a lone common single signal → 'one common alert, auto-cleared' (auto-clear)
        "thin": pick(s1, lambda e: (e["n_alerts"], e["case_id"])),
    }
    return selected, exemplars


def generate(evidence_dir: Path, *, rich_cap: int = DEFAULT_RICH_CAP,
             noise_cap: int = DEFAULT_NOISE_CAP, casework_dir: Path | None = None) -> tuple:
    """Build (cases_index, bundle_paths_by_case). Deterministic given the same substrate run (+ the
    deterministic casework stub when --measure-casework grounds the slice)."""
    pop = _read_population(evidence_dir)
    if not pop:
        raise ValueError(f"no evidence bundles under {evidence_dir} — run the substrate emit first "
                         f"(see the module docstring; {EMIT_COMMAND})")
    # combo frequency over the FULL population (the REAL precedent sample sizes)
    combo_freq: dict = {}
    for _f, b in pop:
        key = "+".join(_caps(b))
        combo_freq[key] = combo_freq.get(key, 0) + 1

    selected, exemplars = select_slice(pop, combo_freq, rich_cap=rich_cap, noise_cap=noise_cap)
    exemplar_of = {cid: tag for tag, cid in exemplars.items() if cid}

    cases = []
    bundle_paths = {}
    for e in selected:
        b = e["b"]
        cid = e["case_id"]
        party = (b.get("parties") or [{}])[0]
        caps = e["caps"]
        cases.append({
            "case_id": cid,
            "subject": b.get("subject", {}),
            "display": synthetic_identity(party, b.get("subject", {}).get("customer_id", cid)),
            "kyc": {k: party.get(k) for k in (
                "is_person", "risk_rating", "cdd_level", "pep_tier", "sanctions_flag",
                "adverse_media_flag", "occupation", "nature_of_business", "naics_code",
                "source_of_funds", "source_of_wealth", "nationality", "residency_status",
                "expected_monthly_volume_cents", "expected_monthly_txn_count")},
            "capabilities": caps,
            "n_alerts": e["n_alerts"],
            "n_txns": e["n_txns"],
            "advisories": _advisories(b),
            "confidence": _confidence(e["combo"], combo_freq.get(e["combo"], 0)),
            "exemplar": exemplar_of.get(cid),
            # capability-membership PROXY (cheap); the AUTHORITATIVE coverage is grounds_e2e (measured)
            "cap_assertable": bool(caps) and all(c in GROUNDABLE_CAPS for c in caps),
            "bundle": f"bundles/{cid}.json",
        })
        bundle_paths[cid] = e["f"]

    # MEASURE real end-to-end grounding (casework signs) — the honest coverage, never a capability proxy
    grounding = _measure_grounding(bundle_paths, casework_dir) if casework_dir else {}
    for c in cases:
        g = grounding.get(c["case_id"])
        c["grounds_e2e"] = (None if g is None else bool(g["signs"]))
        c["e2e_note"] = (None if g is None else g["note"])
    measured = bool(casework_dir)
    n_groundable = (sum(1 for c in cases if c.get("grounds_e2e")) if measured
                    else sum(1 for c in cases if c.get("cap_assertable")))

    index = {
        "meta": {
            "illustrative": True,
            "badge": BADGE,
            "substrate_repo": SUBSTRATE_REPO,
            "substrate_head": SUBSTRATE_HEAD,
            "run_id": RUN_ID,
            "emit_command": EMIT_COMMAND,
            "generated_note": ("synthetic substrate emission; GROUNDED detection (real advisory-grounded "
                               "alerts over real KYC), ILLUSTRATIVE dispositions; display identities synthetic"),
            "slice_rule": (f"the rare 4+-capability cases (cap {rich_cap}) + a 3-cap-band sample (20) + a "
                           f"deterministic sample of the 1-2-cap noise (cap {noise_cap}) + a combo-coverage "
                           "pass (>=1 representative of every population combo); sorted by case_id "
                           "[VISIBLE volume + full combo spread, not detection difficulty — single-signal-separable]"),
            "population_total": len(pop),
            "slice_total": len(cases),
            "coverage": {
                "groundable": n_groundable,
                "total": len(cases),
                "measured": measured,
                "casework_pin": ("aml-casework@c6d8401" if measured else None),
                "basis": ("MEASURED: cases aml-casework actually SIGNS end-to-end (drafter=stub; the six "
                          "Class-G verifiers independently re-derive each signal). Composed cases that "
                          "fail are a real substrate↔casework C3/C15 replay divergence — the gate "
                          "correctly refusing, the honest frontier." if measured else
                          "PROXY (UNMEASURED): capability-membership only (C2-C5/C15/C7/C8/C14) — run "
                          "--measure-casework for the real signed-end-to-end count"),
            },
            "exemplars": exemplars,
            "combo_frequency": dict(sorted(combo_freq.items(), key=lambda kv: (-kv[1], kv[0]))),
        },
        "cases": cases,
    }
    return index, bundle_paths


def _write(evidence_dir: Path, rich_cap: int, noise_cap: int, casework_dir: Path | None) -> dict:
    index, bundle_paths = generate(evidence_dir, rich_cap=rich_cap, noise_cap=noise_cap,
                                   casework_dir=casework_dir)
    if BUNDLES_DIR.exists():
        shutil.rmtree(BUNDLES_DIR)
    BUNDLES_DIR.mkdir(parents=True, exist_ok=True)
    for cid, src in bundle_paths.items():
        shutil.copyfile(src, BUNDLES_DIR / f"{cid}.json")
    CASES_JSON.write_text(json.dumps(index, indent=1, sort_keys=True, ensure_ascii=False) + "\n",
                          encoding="utf-8")
    return index


# ---- validator (backs --selftest + the build-boundary check) ------------------------------------
_VALID_GATES = {"auto-clear", "review", "human-gate"}
_VALID_LEVELS = {"high", "medium", "low"}


def validate(index: dict, bundles_dir: Path = BUNDLES_DIR) -> list:
    """Structural + referential + honesty checks over the committed index. Returns a list of problems."""
    problems = []
    meta = index.get("meta", {})
    cases = index.get("cases", [])
    cov = meta.get("coverage", {})
    measured = bool(cov.get("measured"))
    if not cases:
        problems.append("no cases in the index")
    if not meta.get("illustrative") or meta.get("badge") != BADGE:
        problems.append("meta must carry illustrative:true + the always-on badge")
    if meta.get("substrate_head") != SUBSTRATE_HEAD:
        problems.append(f"substrate_head must pin {SUBSTRATE_HEAD}")
    seen = set()
    exemplars_found = set()
    n_groundable = 0
    for c in cases:
        cid = c.get("case_id", "?")
        if cid in seen:
            problems.append(f"duplicate case_id {cid}")
        seen.add(cid)
        if not (bundles_dir / f"{cid}.json").exists():
            problems.append(f"{cid}: vendored bundle missing ({c.get('bundle')})")
        conf = c.get("confidence", {})
        if conf.get("gate") not in _VALID_GATES:
            problems.append(f"{cid}: bad confidence.gate {conf.get('gate')!r}")
        if conf.get("level") not in _VALID_LEVELS:
            problems.append(f"{cid}: bad confidence.level {conf.get('level')!r}")
        if not isinstance(conf.get("n_precedent"), int):
            problems.append(f"{cid}: n_precedent must be an int (the REAL sample size)")
        if "disposition_illustrative" not in conf or "ILLUSTRATIVE" not in conf.get("disposition_basis", ""):
            problems.append(f"{cid}: disposition must be explicitly labeled ILLUSTRATIVE")
        if not c.get("display", {}).get("synthetic_label"):
            problems.append(f"{cid}: display identity must be flagged synthetic_label")
        if c.get("cap_assertable") and not all(cap in GROUNDABLE_CAPS for cap in c.get("capabilities", [])):
            problems.append(f"{cid}: cap_assertable=true but a capability is not casework-asserted")
        if "grounds_e2e" not in c:
            problems.append(f"{cid}: missing grounds_e2e (run --measure-casework)")
        if measured and not isinstance(c.get("grounds_e2e"), bool):
            problems.append(f"{cid}: measured coverage requires grounds_e2e to be a bool")
        if c.get("grounds_e2e") is False and not c.get("e2e_note"):
            problems.append(f"{cid}: a failed-to-ground case must carry an e2e_note (the honest reason)")
        n_groundable += int(c.get("grounds_e2e") is True) if measured else int(bool(c.get("cap_assertable")))
        if c.get("exemplar"):
            exemplars_found.add(c["exemplar"])
    if cov.get("groundable") != n_groundable:
        problems.append(f"meta.coverage.groundable ({cov.get('groundable')}) disagrees with the "
                        f"per-case count ({n_groundable}, measured={measured})")
    for needed in ("mule", "fp_trap", "thin", "ambiguous"):
        if needed not in exemplars_found:
            problems.append(f"exemplar '{needed}' not tagged on any case in the slice")
    return problems


def selftest() -> int:
    failures = []
    if not CASES_JSON.exists():
        print(f"FAIL: {CASES_JSON} not committed — run --from <evidence-dir> first", file=sys.stderr)  # noqa: T201
        return 1
    index = json.loads(CASES_JSON.read_text(encoding="utf-8"))
    failures += validate(index)

    # FAILURE-PATH: validate() must CATCH corruption — not just pass the good committed index. Mirrors
    # the curate_triage "broken fixtures rejected" discipline (the validator is the build-boundary gate).
    import copy as _copy
    bad_cov = _copy.deepcopy(index)
    bad_cov["meta"]["coverage"]["groundable"] = (index["meta"]["coverage"]["groundable"] or 0) + 999
    if not any("groundable" in p for p in validate(bad_cov)):
        failures.append("validate() failed to catch a corrupted coverage.groundable count")
    bad_ex = _copy.deepcopy(index)
    for c in bad_ex["cases"]:
        c["exemplar"] = None
    if not any("exemplar" in p for p in validate(bad_ex)):
        failures.append("validate() failed to catch missing exemplar tags")
    bad_disp = _copy.deepcopy(index)
    bad_disp["cases"][0]["confidence"].pop("disposition_basis", None)
    if not any("ILLUSTRATIVE" in p for p in validate(bad_disp)):
        failures.append("validate() failed to catch a disposition not labeled ILLUSTRATIVE (honesty gate)")

    # confidence mechanic monotonicity: a larger precedent sample never yields a STRICTER gate
    order = {"auto-clear": 0, "review": 1, "human-gate": 2}
    pairs = sorted(((c["confidence"]["n_precedent"], order[c["confidence"]["gate"]])
                    for c in index["cases"] if c["confidence"].get("gate") in order),
                   key=lambda t: t[0])
    if any(pairs[i][1] < pairs[i + 1][1] for i in range(len(pairs) - 1)):
        failures.append("confidence gate is not monotone in the precedent sample size")

    # route() (the live-engine source of truth) reproduces every committed gate from its sample size —
    # proves the _confidence -> route() refactor stays faithful to the frozen records (one routing logic)
    for c in index["cases"]:
        conf = c["confidence"]
        r = route(conf["n_precedent"])
        if (r["level"], r["gate"]) != (conf["level"], conf["gate"]):
            failures.append(f"{c['case_id']}: route() {r['level']}/{r['gate']} disagrees with the "
                            f"committed {conf['level']}/{conf['gate']}")

    # coverage statistic is REAL + within bounds
    cov = index["meta"]["coverage"]
    if not (0 <= cov["groundable"] <= cov["total"] == len(index["cases"])):
        failures.append(f"coverage statistic out of bounds: {cov}")

    if failures:
        for f in failures:
            print(f"FAIL: {f}", file=sys.stderr)  # noqa: T201
        return 1
    m = index["meta"]
    print(f"curate_workbench_cases --selftest: PASS ({m['slice_total']} cases vendored from "  # noqa: T201
          f"{m['population_total']} emitted; coverage {cov['groundable']}/{cov['total']} groundable; "
          f"exemplars {sorted(t for t in m['exemplars'] if m['exemplars'][t])}; "
          f"substrate@{m['substrate_head']})")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Curate the investigator case-workbench population (authoring-time only).")
    ap.add_argument("--from", dest="evidence_dir", help="the substrate run evidence dir (e.g. /tmp/sw-wb-run/evidence)")
    ap.add_argument("--rich-cap", type=int, default=DEFAULT_RICH_CAP)
    ap.add_argument("--noise-cap", type=int, default=DEFAULT_NOISE_CAP)
    ap.add_argument("--measure-casework", dest="casework_dir",
                    help="MEASURE real end-to-end grounding: run aml-casework over each vendored bundle "
                         "(e.g. ../aml-casework). Without it, coverage is the unmeasured capability proxy.")
    ap.add_argument("--selftest", action="store_true", help="validate the committed slice (no run needed), exit")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if not args.evidence_dir:
        ap.error("either --selftest or --from <evidence-dir> is required")
    cwd = Path(args.casework_dir) if args.casework_dir else None
    index = _write(Path(args.evidence_dir), args.rich_cap, args.noise_cap, cwd)
    m = index["meta"]; cov = m["coverage"]
    print(f"wrote {CASES_JSON.relative_to(ROOT)} + {m['slice_total']} bundles "  # noqa: T201
          f"(from {m['population_total']} emitted; coverage {cov['groundable']}/{cov['total']} "
          f"{'MEASURED' if cov.get('measured') else 'PROXY'}; "
          f"exemplars { {t: c for t, c in m['exemplars'].items() if c} })")
    return 0


if __name__ == "__main__":
    sys.exit(main())
