---
phase: 35
title: News live local-model backend
status: active
milestone: M8
ceremony: lite
created: 2026-06-08
updated: 2026-06-08
tags: [m8, news, live-mode, llama-cpp, companion, grounding, real-time]
---

# Phase 35: News live local-model backend (M8)

## Objective
Hook the M8 adverse-media news stream to a REAL local-hosted model (llama-cpp serving a Qwen
~30B-A3B-class MoE) for REAL-TIME, on-demand extraction. The arc is unchanged
(Select → Read → Screen → Disposition → Exposure) but Read is now driven LIVE: submit an article →
the model extracts entities + red flags + the AML translation → server-side deterministic grounding
(ungrounded drops) → the existing client-side fuzzy screen vs the book → human disposition. This is
the long-anticipated "live mode" the non-negotiable already sanctions (optional, isolated, off by
default, scripted fallback). It is the project's first move from a scripted DRAMATIZATION to a working
INSTANCE of the loop.

## Why now
The user steered Phase 35 off the queued C/D-quality candidates at the dev-plan gate. The news stream
is the cleanest place to add live processing (the corpus/showcase stay frozen), and the existing
`news.html` render pipeline is fully `NEWS`-driven + the streaming render is parameterized — so the
live path is mostly additive.

## Architecture (3 direction-gate choices)
1. **Served-by-companion** — a stdlib Python companion `scripts/serve_news.py` serves news.html over
   `http://localhost` and proxies llama-cpp; same-origin → no CORS. The offline single-file `dist/news`
   stays the default + scripted fallback, **byte-identical**: the live branch lives in a marked
   `/*LIVE_START*/…/*LIVE_END*/` region that `render_news` strips for the offline build (offline keeps
   zero network code; the self-contained `die("fetch(")` guard holds). The strip strengthens the
   non-negotiable.
2. **Grounding stays in Python server-side** — a shared stdlib `scripts/news_ground.py`
   (normalize + raw/normalize-substring grounding + the article-body transform), reused by BOTH
   build.py's gate AND the companion. Live output is JSON-schema/GBNF-constrained then deterministically
   grounded (ungrounded entities/flags DROP). NOT re-ported to JS — revised from the direction-gate's
   initial framing; the companion makes server-side grounding the clean, DRY answer.
3. **Persistence = Phase 36** — companion → DuckDB row-append → parquet export; watchlist =
   book ∪ all prior-scanned entities (the screen surface grows). Phase 35 screens vs the STATIC book.

## Honesty
The "LLM proposes, the deterministic gate disposes" spine, moved to runtime. Real client-side fuzzy
scores; synthetic book; the always-on "Illustrative data & outputs" badge stays; nothing shown that
isn't grounded in the submitted source; model output is constrained + grounded, never fabricated.

## Tasks (lite)
- T1 (M) Companion server skeleton (`scripts/serve_news.py`; serve + seed NEWS + `/health` + `/extract` stub; `--selftest`).
- T2 (M) Shared grounding gate `scripts/news_ground.py` + reuse in build.py (dist/news byte-identical).
- T3 (L) Live `/extract` — model + JSON-schema constraint + `build_record` + `ground_record`; `call_llm` separable so the test runs with no model.
- T4 (M) `news.html` LIVE_MODE Read+Screen path + the offline strip in `render_news`.
- T5 (S) Run docs + full regate + in-place CLAUDE.md `## Current state` refresh.

## Constraints / non-negotiables
ZERO new pip deps (stdlib + urllib; DuckDB enters Phase 36). `news_ground.py` is stdlib grounding
primitives, not the authoring/LLM layer — build.py still never imports derive_signals/markitdown/an LLM
client. Real-time = on-demand submit (paste/pick), not a feed. Model via llama-cpp's OpenAI-compatible
`/v1` (swappable; thinking disabled / `<think>` stripped).

## Exit criteria
Live real-time extraction via the companion; output schema-constrained + server-side-grounded
(ungrounded drops); the full arc runs on the live record; offline `dist/news` byte-identical (live code
stripped, zero network code, fallback intact); zero new pip deps; `--check all` 5/5 zero drift;
`--selftest` PASS; both harnesses green; the frozen set byte-clean; NO non-negotiable change.

## Frozen byte-clean
The six-act showcase (index.html + config/** + 3 typology dists), the entire corpus (corpus.html +
dist/corpus + all source dirs + every derived record + data/typology-map.json +
data/capability-taxonomy.json), the grounding core derive_signals.py, and `dist/news/index.html`
(byte-identical via the strip).
