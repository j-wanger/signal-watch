#!/usr/bin/env python3
"""Phase 54 — context-matched, cross-family INDEPENDENT C/D rater (the control's independent
effectiveness challenge, executed once).

DEV-TIME COMPANION. Calls the LOCAL model (127.0.0.1 llama-cpp, a DIFFERENT model family than the
committed extractor) to produce the independent-rater fixture that cd_correctness.py replays. This is
the ONLY code in the C/D-control workstream that touches a model or the network — cd_correctness.py
stays pure stdlib / deterministic, and build.py imports NEITHER this nor cd_correctness.py. Nothing
leaves the machine (127.0.0.1 only); the fixture stores JUDGMENTS over committed indicators (no new
external content).

CONTEXT-MATCHED (Phase 54 A1): the rater sees the SAME inputs the committed assignment had — the
SOURCE-DOCUMENT region for the indicator + the 28+20 capability/data-source interview posture + the
closed vocab — NOT the Phase-53 flag+red_flag-only frame. So agreement-with-committed is a RELIABILITY
comparison, not a re-measurement of the Phase-53 context gap. BLIND by construction: the rater never
sees the committed C/D code (build_messages reads only flag/red_flag/gid, never the committed fields).

The fixture shape matches what cd_correctness.random_agreement / verify_random read (judgments with
blind_capability / blind_data_source / committed_capability / committed_data_source per gid), so the
PURE replay core scores it with no model in the loop.

Usage:
    python3 scripts/cd_rate_independent.py --selftest                 # offline, no model: prompt + parse + schema
    python3 scripts/cd_rate_independent.py --probe 3                  # rate N items live → availability + competence
    python3 scripts/cd_rate_independent.py --rate-sample 96 --seed 0 --out data/cd-correctness/independent-sample.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

# Pure stdlib readers shared with the measurement core (one-way: companion -> core; build.py imports
# NEITHER). sys.path[0] is scripts/ when run directly, so these resolve as siblings.
from corpus_redundancy import SOURCES, load_indicators
from cd_correctness import sample_random

ROOT = Path(__file__).resolve().parent.parent
TAXONOMY = ROOT / "data" / "capability-taxonomy.json"
DEFAULT_LLM_URL = "http://127.0.0.1:8080/v1/chat/completions"  # the corpus-live model port (serve_corpus default)
DEFAULT_MODEL = "qwen"            # any model behind llama-cpp's OpenAI-compatible /v1 (serve_corpus default)
DOC_BUDGET = 18000               # chars of source-doc context: whole doc if smaller, else a window around the flag

# sid -> the source-doc DIRECTORY (parent of the derived dir in SOURCES); the md is <dir>/<doc_id>.md.
SRC_DIR = {sid: ddir.parent for sid, ddir, _juris in SOURCES}


# ---------------------------------------------------------------------------
# Vocab + the strict output schema (enum-constrained -> grammar-bound to in-vocab codes)
# ---------------------------------------------------------------------------

def load_vocab() -> tuple[list[dict], list[dict]]:
    t = json.loads(TAXONOMY.read_text(encoding="utf-8"))
    return t["capabilities"], t["data_sources"]


def cd_schema(caps: list[dict], dss: list[dict]) -> dict:
    """Strict json_schema: exactly one in-vocab C + one in-vocab D, no extra keys."""
    return {"type": "object", "additionalProperties": False,
            "required": ["capability", "data_source"],
            "properties": {"capability": {"type": "string", "enum": [c["id"] for c in caps]},
                           "data_source": {"type": "string", "enum": [d["id"] for d in dss]}}}


# ---------------------------------------------------------------------------
# Context assembly (context-matched: source-doc region + posture-annotated vocab; BLIND to committed)
# ---------------------------------------------------------------------------

def window_region(md: str, flag: str, budget: int) -> tuple[str, bool]:
    """The source-doc context: the whole md if <= budget, else a window around the located flag.
    Returns (region, located). Pure (no IO) so the selftest exercises it offline."""
    if len(md) <= budget:
        return md, True
    idx = md.find(flag[:60]) if flag else -1
    if idx == -1:
        return md[:budget], False          # raw find missed (wrap/whitespace) — head of doc, honestly flagged
    half = budget // 2
    lo, hi = max(0, idx - half), min(len(md), idx + half)
    return md[lo:hi], True


def source_doc_region(gid: str, source: str, flag: str, *, budget: int = DOC_BUDGET) -> tuple[str, bool]:
    """The source-document region the committed assignment read (data/<dir>/<doc_id>.md). gid =
    doc_id/ind_id; ind_id carries no slash, so rsplit isolates the doc id."""
    sid_dir = SRC_DIR.get(source)
    doc_id = gid.rsplit("/", 1)[0]
    md_path = (sid_dir / f"{doc_id}.md") if sid_dir else None
    if not md_path or not md_path.exists():
        return "", False
    return window_region(md_path.read_text(encoding="utf-8"), flag, budget)


def build_messages(ind: dict, region: str, caps: list[dict], dss: list[dict]) -> tuple[str, str]:
    """The context-matched prompt. Reads ONLY ind['flag'/'red_flag'/'gid'] — NEVER the committed
    ind['capability'/'data_source'] (blind by construction)."""
    cap_lines = "\n".join(f"  {c['id']}: {c['name']}  [institution posture: {c.get('posture', '?')}]" for c in caps)
    ds_lines = "\n".join(f"  {d['id']}: {d['name']}  [institution posture: {d.get('posture', '?')}]" for d in dss)
    system = (
        "You are an INDEPENDENT anti-money-laundering analyst. For a single red-flag indicator you "
        "assign exactly ONE detection CAPABILITY (a C-code) and ONE DATA SOURCE (a D-code) from the "
        "closed vocabularies, judging from the SOURCE DOCUMENT the indicator was extracted from and "
        "the institution's stated capability posture. Pick the single best-fitting code on each axis. "
        'Output STRICT JSON only, no prose: {"capability": "C..", "data_source": "D.."}.'
    )
    user = (
        "SOURCE DOCUMENT (the advisory/guidance this indicator was extracted from — context the "
        "original assignment had):\n<<<\n" + region.strip() + "\n>>>\n\n"
        "INDICATOR under assessment:\n"
        f"  verbatim flag:        {ind['flag']!r}\n"
        f"  analyst translation:  {ind['red_flag']!r}\n\n"
        "CAPABILITIES (C) — closed vocabulary, with this institution's interview posture:\n"
        + cap_lines + "\n\n"
        "DATA SOURCES (D) — closed vocabulary, with this institution's interview posture:\n"
        + ds_lines + "\n\n"
        'Assign exactly one C and one D. Output strict JSON: {"capability": "C..", "data_source": "D.."}.'
    )
    return system, user


def parse_cd(content: str) -> tuple[str | None, str | None]:
    """Strip <think>/fences/prose around the outermost {...} (the serve_corpus/serve_news parser)."""
    s = re.sub(r"<think>.*?</think>", "", content, flags=re.S).strip()
    m = re.search(r"```(?:json)?\s*(.*?)```", s, flags=re.S)
    if m:
        s = m.group(1).strip()
    if not s.startswith("{"):
        i, j = s.find("{"), s.rfind("}")
        if i != -1 and j != -1 and j > i:
            s = s[i:j + 1]
    obj = json.loads(s)
    return obj.get("capability"), obj.get("data_source")


# ---------------------------------------------------------------------------
# The model call (mirror serve_corpus.call_llm: strict json_schema; non-stream for a tiny output)
# ---------------------------------------------------------------------------

def call_model(system: str, user: str, schema: dict, *, llm_url: str, model: str, timeout: int = 180) -> str:
    body = {
        "model": model,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "temperature": 0,
        "max_tokens": 200,
        "stream": False,
        "response_format": {"type": "json_schema",
                            "json_schema": {"name": "cd_assignment", "strict": True, "schema": schema}},
        "chat_template_kwargs": {"enable_thinking": False},
    }
    req = urllib.request.Request(llm_url, data=json.dumps(body).encode("utf-8"),
                                 headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        resp = json.loads(r.read().decode("utf-8"))
    return resp["choices"][0]["message"]["content"]


def rate_one(ind: dict, caps: list[dict], dss: list[dict], schema: dict, *,
             llm_url: str, model: str, timeout: int = 180) -> dict:
    region, located = source_doc_region(ind["gid"], ind["source"], ind["flag"])
    system, user = build_messages(ind, region, caps, dss)
    c, d = parse_cd(call_model(system, user, schema, llm_url=llm_url, model=model, timeout=timeout))
    return {"capability": c, "data_source": d, "located": located}


# ---------------------------------------------------------------------------
# Probe (the Phase-46 probe-gate: availability + competence on a few items) + the full rating run
# ---------------------------------------------------------------------------

def probe(n: int, *, llm_url: str, model: str) -> int:
    inds = load_indicators()[0]
    caps, dss = load_vocab()
    schema = cd_schema(caps, dss)
    cap_ids, ds_ids = {c["id"] for c in caps}, {d["id"] for d in dss}
    cap_name = {c["id"]: c["name"] for c in caps}
    ds_name = {d["id"]: d["name"] for d in dss}
    sample = sample_random(inds, 96, 0)[:n]   # the first n of the committed n=96 sample (cross-comparable)
    print(f"# PROBE — {n} items vs {llm_url} (model={model}); the committed C/D shown is MY view, never the prompt's")
    ok = located = c_agree = d_agree = 0
    for i, ind in enumerate(sample):
        try:
            r = rate_one(ind, caps, dss, schema, llm_url=llm_url, model=model)
        except (urllib.error.URLError, OSError, TimeoutError, KeyError, ValueError) as ex:
            print(f"[{i}] {ind['gid']}: ERROR {type(ex).__name__}: {ex}")
            continue
        in_vocab = r["capability"] in cap_ids and r["data_source"] in ds_ids
        ok += in_vocab
        located += r["located"]
        c_agree += (r["capability"] == ind["capability"])
        d_agree += (r["data_source"] == ind["data_source"])
        cm = "==" if r["capability"] == ind["capability"] else "!="
        dm = "==" if r["data_source"] == ind["data_source"] else "!="
        print(f"\n[{i}] {ind['gid']}  ({'in-vocab' if in_vocab else 'OUT-OF-VOCAB'}, doc {'located' if r['located'] else 'MISS'})")
        print(f"    flag: {ind['flag'][:140]!r}")
        print(f"    INDEPENDENT  C={r['capability']:>3} {cap_name.get(r['capability'], '?')[:46]:46} {cm} "
              f"D={r['data_source']:>3} {ds_name.get(r['data_source'], '?')[:40]:40} {dm}")
        print(f"    committed    C={ind['capability']:>3} {cap_name.get(ind['capability'], '?')[:46]:46}    "
              f"D={ind['data_source']:>3} {ds_name.get(ind['data_source'], '?')[:40]}")
    print(f"\n# {ok}/{n} parseable in-vocab · {located}/{n} doc-region located — "
          f"{'PASS' if ok == n else 'REVIEW (fallback?)'} (the mechanical competence gate)")
    print(f"# agreement-with-committed on this probe: C {c_agree}/{n} · D {d_agree}/{n} "
          f"(cross-family, context-matched — vs the same-family self-consistency 0.677; YOUR adjudication call)")
    return 0 if ok == n else 1


def rate_sample(n: int, seed: int, out: str, *, llm_url: str, model: str) -> int:
    inds = load_indicators()[0]
    caps, dss = load_vocab()
    schema = cd_schema(caps, dss)
    cap_ids, ds_ids = {c["id"] for c in caps}, {d["id"] for d in dss}
    sample = sample_random(inds, n, seed)
    judgments = []
    for i, ind in enumerate(sample):
        r = rate_one(ind, caps, dss, schema, llm_url=llm_url, model=model)
        if r["capability"] not in cap_ids or r["data_source"] not in ds_ids:
            raise ValueError(f"out-of-vocab judgment for {ind['gid']}: {r}")
        judgments.append({"gid": ind["gid"],
                          "blind_capability": r["capability"], "blind_data_source": r["data_source"],
                          "committed_capability": ind["capability"], "committed_data_source": ind["data_source"]})
        print(f"  [{i + 1}/{len(sample)}] {ind['gid']} -> C={r['capability']} D={r['data_source']}", file=sys.stderr)
    fixture = {"rater": f"{model}@local", "model": model, "context_matched": True,
               "n": n, "seed": seed,
               "label": "Phase-54 context-matched cross-family independent rater (local llama-cpp)",
               "judgments": judgments}
    Path(out).write_text(json.dumps(fixture, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out} ({len(judgments)} judgments, model={model})")
    return 0


# ---------------------------------------------------------------------------
# Selftest (OFFLINE, no model): prompt assembly (context-matched + blind) · parse · schema · windowing
# ---------------------------------------------------------------------------

def selftest() -> int:
    caps = [{"id": "C12", "name": "Cap twelve", "posture": "yes"},
            {"id": "C8", "name": "Cap eight", "posture": "partial"}]
    dss = [{"id": "D7", "name": "DS seven", "posture": "no"},
           {"id": "D1", "name": "DS one", "posture": "yes"}]

    # schema: enum-constrained to the vocab, exactly two keys, no extras.
    sch = cd_schema(caps, dss)
    assert sch["properties"]["capability"]["enum"] == ["C12", "C8"], sch
    assert sch["properties"]["data_source"]["enum"] == ["D7", "D1"], sch
    assert sch["additionalProperties"] is False and sch["required"] == ["capability", "data_source"], sch

    # build_messages — context-matched (source-doc region + posture-annotated closed vocab + the indicator)
    # AND blind: the committed code is a SENTINEL not in the vocab; it must NEVER appear in the prompt
    # (proves build_messages never reads ind['capability'/'data_source']).
    ind = {"gid": "fin-x/IND-1", "source": "fincen-advisories",
           "flag": "structuring below the reporting threshold",
           "red_flag": "deposits structured below the CTR threshold",
           "capability": "C_SENTINEL_COMMITTED", "data_source": "D_SENTINEL_COMMITTED"}
    region = "FINCEN ADVISORY\n... structuring below the reporting threshold ...\nFiling instructions ..."
    system, user = build_messages(ind, region, caps, dss)
    blob = system + "\n" + user
    assert "SOURCE DOCUMENT" in user and "structuring below the reporting threshold" in user, "doc region missing"
    assert "institution posture" in user and "C12:" in user and "D7:" in user, "posture-annotated vocab missing"
    assert "deposits structured below the CTR threshold" in user, "the indicator translation missing"
    assert "C_SENTINEL_COMMITTED" not in blob and "D_SENTINEL_COMMITTED" not in blob, "committed code leaked (not blind)"

    # parse_cd — strict, fenced, and prose/think-wrapped all recover.
    assert parse_cd('{"capability":"C12","data_source":"D7"}') == ("C12", "D7")
    assert parse_cd('```json\n{"capability":"C8","data_source":"D1"}\n```') == ("C8", "D1")
    assert parse_cd('<think>weigh C8 vs C12</think> answer: {"capability":"C12","data_source":"D1"} done') == ("C12", "D1")

    # window_region — whole doc when small (located), a flag-centred window when large.
    small = "abc structuring def"
    assert window_region(small, "structuring", 1000) == (small, True)
    big = ("x" * 5000) + "STRUCTURING_HERE" + ("y" * 5000)
    reg, loc = window_region(big, "STRUCTURING_HERE", 2000)
    assert loc and "STRUCTURING_HERE" in reg and len(reg) <= 2000 + len("STRUCTURING_HERE"), (loc, len(reg))
    miss_reg, miss_loc = window_region("z" * 5000, "absent-flag", 1000)
    assert miss_loc is False and len(miss_reg) == 1000, (miss_loc, len(miss_reg))

    # the companion must NOT import build.py (the build boundary) — match real import STATEMENTS
    # (line-anchored), not the substring, so this very assertion doesn't trip it.
    src = Path(__file__).read_text(encoding="utf-8")
    assert not re.search(r"^\s*(import|from)\s+build\b", src, re.M), "companion must not import build.py"

    # real taxonomy: the live schema is 28 C + 20 D and every committed code is in-vocab (the rater's space).
    rcaps, rdss = load_vocab()
    assert len(rcaps) == 28 and len(rdss) == 20, (len(rcaps), len(rdss))
    rsch = cd_schema(rcaps, rdss)
    assert len(rsch["properties"]["capability"]["enum"]) == 28 and len(rsch["properties"]["data_source"]["enum"]) == 20
    inds = load_indicators()[0]
    cap_ids, ds_ids = {c["id"] for c in rcaps}, {d["id"] for d in rdss}
    assert all(i["capability"] in cap_ids and i["data_source"] in ds_ids for i in inds), "committed code out of vocab"
    # the source-doc region resolves for a deterministic spread of the committed n=96 sample (path mapping sane).
    sample = sample_random(inds, 96, 0)
    resolved = sum(1 for ind in sample if source_doc_region(ind["gid"], ind["source"], ind["flag"])[0])
    assert resolved >= 90, f"only {resolved}/96 source-doc regions resolved — check SRC_DIR / md naming"

    print(f"selftest OK — schema enum-constrained (28C/20D), context-matched prompt carries the source-doc "
          f"region + posture-annotated vocab + the indicator and is BLIND to the committed code, parse recovers "
          f"strict/fenced/think-wrapped, window_region whole/window/miss; {resolved}/96 source-doc regions resolve; "
          f"no build.py import.")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Phase 54 context-matched cross-family independent C/D rater (dev-time companion).")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--probe", type=int, metavar="N", help="rate N items live → availability + competence gate")
    ap.add_argument("--rate-sample", type=int, metavar="N", help="rate the n=N seeded sample → --out fixture")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", help="fixture path for --rate-sample")
    ap.add_argument("--llm-url", default=DEFAULT_LLM_URL)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if args.probe is not None:
        return probe(args.probe, llm_url=args.llm_url, model=args.model)
    if args.rate_sample is not None:
        if not args.out:
            ap.error("--rate-sample requires --out")
        return rate_sample(args.rate_sample, args.seed, args.out, llm_url=args.llm_url, model=args.model)
    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
