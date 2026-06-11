# Corpus explorer — live local-model derivation mode (Phase 46, M7)

Optional, dev/authoring-time **live mode** for the corpus explorer: paste an advisory's converted
markdown and a local model derives detection-signal indicators in **real time** — through the SAME
frozen deterministic gate that grounds the committed corpus — with live stage progress streamed back
as it works. It is NOT part of the ship artifact — the offline single-file `dist/corpus/index.html`
stays the default and the scripted fallback (it makes no network call; the live branch is build-time
stripped from it, byte-identical to the pre-Phase-46 artifact).

This is the M7 corpus's **inverted extraction boundary made live**: the loop that phases 14–34 ran
manually in-session (LLM extracts → `derive_signals.py --check-derived` disposes) becomes an
automated local-model pipeline behind the explorer's Select screen.

## Architecture
```
http://localhost:8010/         serve_corpus.py (stdlib companion) — serves corpus.html WITH the live branch
  ├── GET  /                   the page (CORPUS.live set → "＋ Derive a new document" control on Select)
  ├── GET  /health             {"ok": true, "live": true, "persist": false}
  └── POST /derive             {text, title?, source_org?, date?} → llama-cpp (strict JSON schema) →
                               deterministic assemble → check_record GATE → ONE violation-guided retry
                               of the rejected → grounded-or-dropped; answers an NDJSON STAGE STREAM
          │  same-origin (no CORS)
          ▼
  llama-cpp /v1 (your local model) — proxied; NOTHING is persisted anywhere (no store, by design)
```

**The model proposes; the FROZEN gate disposes.** The LLM emits only the neural fields per indicator
— `{section, flag (verbatim), red_flag (translation), capability C1–C28, data_source D1–D20}` —
constrained by a strict JSON schema whose C/D enums mirror `data/capability-taxonomy.json` (single
authority). Everything else is DETERMINISTIC, the committed convention (verified exact on all 2,251
committed indicators at the Phase-46 probe):

- `src_line` — located in the submitted md (sliding-window normalize match);
- `status` / `data` — the institution's interview POSTURE per C/D code (y→covered/available,
  partial→partial, n→gap/insufficient) — coverage is never the model's to claim;
- `build_rec` — `derive_signals.build_rec_category` (the cover×data matrix, imported);
- BUILD_NOW `build_logic` — a deterministic shape-valid template (never neurally re-authored; a
  committed record would get the full per-capability spec template at human review);
- the GATE — `derive_signals.check_record`, imported untouched: quote-grounding (every verbatim
  `flag` a normalized substring of the source inside `rf_region`), the cover×data consistency check,
  the `red_flag` shape contract, id/flag uniqueness.

## The one retry (the Phase-46 T1 harness decision)
The T1 probe A/B-measured an **opencode agent loop** against this direct pipeline on the same
held-out FINTRAC document (`.dev-wiki/tmp/ph46/ph46_probe.md`): identical extraction quality
(17/17 pair-matched flags, both gate-green first shot), the agent loop at 3.1× the wall time, its
iterate-on-gate-failure capability never engaging. The user checkpoint chose **direct + retry**:
when the gate rejects indicators, the pipeline re-prompts ONCE with only the rejected entries and
the gate's violation text verbatim; whatever still fails (or never returns) is DROPPED with honest
counts in the stream and the `done` event. No agent runtime; the loop's one real idea, kept.

## Honesty + boundary contract (Phase-46 A4)
- **Display/propose-only.** A live-derived document lives in a session-only "Live derivations (this
  session — UNREVIEWED)" group on Select — it never joins the committed corpus counts, and NOTHING
  is persisted on any path (there is no store; abandoning a run loses nothing). Committing a derived
  record to `data/` remains a separate human-reviewed act under the licence rules (FINTRAC
  Crown-copyright vs US-federal public domain — see CLAUDE.md non-negotiables).
- **Only gate-green indicators ever render.** The `done` event's entry re-validates under
  `check_record` independently (server-asserted before emit; harness-asserted by independent
  recomputation at the probe).
- **Stage-completion rendering, never token streams** (the decided rule): the dedicated processing
  page (the news Phase-44 in-page-takeover pattern: presenter keys guarded; Esc arms → Esc abandons)
  shows completed stages — `extracting (token COUNT only) → gating → gated (passed/rejected) →
  [retrying → regating] → derived` — plus the gate-green `red_flag` chips at the end.
- The C/D tags remain the **unguarded neural dimension** (the gate checks faithfulness, not tag
  correctness — the Phase-34 lesson; probe-measured cross-harness agreement C 71% / D 88%, inside
  the Phase-34 blind inter-rater band). Human review carries it, exactly as for the committed corpus.

## Running it
```
# 1. llama-server with your local model (the news live model works; measured here):
#    llama-server -m <model.gguf> --jinja --ctx-size 131072 --parallel 2 ...
# 2. the companion (stdlib only — no venv needed):
python3 scripts/serve_corpus.py --model <model-alias> [--port 8010] [--llm-url http://127.0.0.1:8080/v1/chat/completions]
# 3. open http://localhost:8010 → Select → "＋ Derive a new document" → paste the advisory md → Run derivation
python3 scripts/serve_corpus.py --selftest    # offline assertions (no socket, no model)
```
Paste the **converted markdown** (the `pdf_to_md.py` output body — the derivation surface). URL mode
is consciously omitted: the FINTRAC `/intel/` frontier is PDF-shaped, outside the news HTML fetch
ladder; the converted md IS the authoring surface. The submitted document must carry a recognizable
enumerated-indicator section (`rf_region`) — a document without one gets a NAMED in-stream refusal,
never a fabricated derivation. Failures are NAMED throughout (context preflight with the
`--ctx-size` remedy · output-budget · idle-gap stall · single-flight 409 — the news Phase-43 class).

Measured wall (Qwen3.6-35B-A3B-UD-Q4_K_XL, M-series laptop): a 22K-char FINTRAC OA derives in
~80–90 s (17 indicators, gate-green first shot, retry not needed).

## What this is NOT
- NOT a web backend; localhost-only, dev/authoring-time, off by default (HANDOFF §4.5 holds).
- NOT a corpus-extension autopilot: live output is a PROPOSAL surface for the authoring loop; the
  human reviews before anything is committed (agent proposes, gate disposes, human reviews).
- NOT connected to the news live companion (port 8000) — the two companions are independent; they
  share only the llama-server and the design conventions.
