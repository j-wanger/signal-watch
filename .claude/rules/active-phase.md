# Active Phase Context

Phase: 35 — News live local-model backend (M8). DELIVERED 2026-06-08 (all 5 tasks [x]; exit criteria met; --check all 5/5 zero drift; both harnesses + the live tests green; frozen set byte-clean; delivery acceptance pending). Direction approved 2026-06-08.

Objective: hook the M8 adverse-media news stream to a REAL local-hosted model (llama-cpp serving a Qwen ~30B-A3B-class MoE) for REAL-TIME, on-demand extraction. Paste/pick an article → the live model extracts entities + red flags + the AML translation → server-side deterministic grounding (ungrounded drops) → the existing client-side fuzzy screen vs the static book → human disposition → exposure. This is the long-anticipated "live mode" the non-negotiable already sanctions (optional, isolated, off by default, scripted fallback). Phase 35 = the live-extraction BACKBONE; persistence (DuckDB→parquet) + the feedback watchlist (book ∪ prior-scanned entities) is Phase 36.

Architecture (3 user choices at the direction gate):
- SERVED-BY-COMPANION: a stdlib Python companion `scripts/serve_news.py` serves news.html over http://localhost + proxies llama-cpp /v1; same-origin → NO CORS. The offline single-file `dist/news` stays the default + scripted fallback, BYTE-IDENTICAL: the live branch is a marked `/*LIVE_START*/…/*LIVE_END*/` region that `render_news` STRIPS for the offline build (offline keeps zero network code; the self-contained guard holds). The companion serves the template whole.
- GROUNDING STAYS IN PYTHON server-side: a shared stdlib `scripts/news_ground.py` (normalize + raw/normalize-substring grounding + the article-body transform), reused by BOTH build.py's gate AND the companion. Live output is JSON-schema/GBNF-constrained then deterministically GROUNDED (ungrounded entities/flags DROP) — "LLM proposes, the gate disposes", moved to runtime. NOT re-ported to JS (revised from the direction-gate's initial framing — the companion makes server-side grounding the clean answer).
- PERSISTENCE = Phase 36: companion → DuckDB row-append → parquet export; watchlist = book ∪ all prior-scanned entities (screen surface grows). Phase 35 screens vs the STATIC book.

Scope (UNFREEZE): `scripts/serve_news.py` (NEW), `scripts/news_ground.py` (NEW), `scripts/build.py` (ADDITIVE — news gate imports news_ground + the offline strip in render_news; existing dist outputs byte-identical), `news.html` (the guarded live branch), `dist/news/index.html` (rebuilt — byte-identical via the strip), `tests/news-stream.test.mjs` + a NEW `tests/news-live.test.mjs` (or a python test), `docs/news-live.md` (or README), `tests/smoke-checklist.md`, `CLAUDE.md` (T5 — in-place `## Current state` snapshot edit per the maintenance contract, NO per-phase bullet), `.claude/rules/active-phase.md`.

Key constraints:
- ZERO new pip deps this phase (stdlib + urllib; DuckDB enters Phase 36).
- `news_ground.py` is stdlib grounding PRIMITIVES, NOT the authoring/LLM layer — build.py STILL never imports derive_signals / markitdown / an LLM client.
- Real-time = on-demand SUBMIT (paste/pick), not a continuous feed.
- HONESTY: real client-side fuzzy scores; synthetic book; the always-on illustrative badge stays; nothing shown that isn't grounded in the submitted source; model output is constrained + grounded, never fabricated.
- Model integration via llama-cpp OpenAI-compatible /v1 (model swappable; thinking disabled / `<think>` stripped).

Exit criteria: live real-time extraction works via the companion; output schema-constrained + server-side-grounded (ungrounded drops); the Read→Screen→Disposition→Exposure arc runs on the live record; offline `dist/news` byte-identical (live code stripped, zero network code, fallback intact); zero new pip deps; `--check all` 5/5 zero drift; `--selftest` PASS; both harnesses green; the frozen set byte-clean; NO non-negotiable change.

Abort rule: if llama-cpp structured-output can't reliably constrain the JSON, fall back GBNF → lenient-parse-then-ground (grounding is the real guard; never ship ungrounded). If the offline `dist/news` can't be byte-identical after the strip, surface it (behavior-identical + recommit + harness green is the floor). If T3 exceeds an L, STOP + split the model-integration sub-task. Blocked >3 attempts on a task → mark [blocked] + ask: skip or abort.

FROZEN byte-clean: the six-act showcase (index.html + config/** + the 3 typology dists), the ENTIRE corpus (corpus.html + dist/corpus + all source dirs + every derived record + data/typology-map.json + data/capability-taxonomy.json), the grounding core derive_signals.py, and `dist/news/index.html` (byte-identical via the strip).

Gates:
- [x] Direction confirmed by user (live local-model backend for the news stream; served-by-companion + DuckDB→parquet [Ph36] + feedback watchlist [Ph36]; approved 2026-06-08)
- [ ] Delivery accepted (post-implementation report)
