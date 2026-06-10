<!-- nana:approved 2026-06-10 -->
# Spec: Phase 43 — Live pipeline robustness + progressive presentation (live news)

## Objective
The live extraction pipeline (companion-served news.html + scripts/serve_news.py + a local llama-cpp
model) handles articles and investigation notes of any size/complexity — extracting successfully or
failing FAST with a named, actionable reason — and the page renders staged progressive feedback
during extraction instead of a single opaque label.

## Context
A live test on a real (private, local-only) investigation note failed: ~200s of a static "local
agent extracting" label, then a failure message. Backend facts: `serve_news.call_llm` makes ONE
blocking non-streaming HTTP call to llama-cpp with `timeout=180` and `max_tokens=4096`, and discards
`finish_reason`; the Phase-39 NDJSON stage stream emits a single "extracting" event then nothing
until "grounding"; the per-entity verify loop is the measured wall-time majority of a normal run;
the documented llama-server launch command in docs/news-live.md sets NO `--ctx-size` (llama-server's
default context is small — a long note + the large SYSTEM_PROMPT may silently overflow). The
deterministic grounding gate (scripts/news_ground.py), EXTRACT_SCHEMA, SYSTEM_PROMPT, DuckDB store
write paths (scripts/news_store.py), and the 13 pinned replay fixtures (tests stub `call_llm` and
replay captures) are all FROZEN this phase. The offline ship artifact dist/news must stay
byte-identical — all live client code sits in build-stripped `/*LIVE_START*/…/*LIVE_END*/` markers.
Direction gate closed 2026-06-10: A1/A3/A4 accept; A2 reject-by-reframe→A2' accept
(stage-completion progressive rendering, corpus-demo-style; NO visible token stream or
agent-thinking display; internal streaming serves only the timeout fix + an elapsed/token counter).

## Scope
### In scope
- `.dev-wiki/tmp/ph43_stress.py` + `.dev-wiki/tmp/ph43-stress-results.md` (LOCAL scratch —
  synthetic tiered stress notes, never committed to ship paths)
- `scripts/serve_news.py` (call_llm transport, /extract stage events, pre-flight size handling,
  concurrency honesty)
- `news.html` — the `/*LIVE_START*/…/*LIVE_END*/` region ONLY (staged rendering)
- `tests/news_live_test.py`, `tests/news-stream.test.mjs` (new assertions)
- `docs/news-live.md` (--ctx-size launch guidance + staged-rendering walkthrough),
  `tests/smoke-checklist.md`, `CLAUDE.md` (## Current state in-place)
### Out of scope
- `scripts/news_ground.py` (the SHARED gate), `EXTRACT_SCHEMA`, `SYSTEM_PROMPT`,
  `scripts/news_store.py` write paths, `scripts/build.py`, `scripts/news_fetch.py`
- Replay fixtures `tests/fixtures/news-live/**` (NO re-capture, goldens untouched)
- The offline dists (news/corpus/showcase), committed derived records, book.json
- Fuzzy-merge adjudication, bulk scan, FINTRAC /intel/, AUSTRAC/UK, living-doc hygiene (carried)

## Approach
MEASURE-FIRST. T1: a local stress harness generates SYNTHETIC investigation notes at
size/complexity tiers (length × entity count × relationship density) + long commercial articles
(local-only), runs each through extract() against the live llama-server, records per-stage
wall-time, prompt/completion token counts, finish_reason, and failure class; queries the server's
REAL n_ctx (`/props`). Classify: read-timeout vs output-budget truncation vs context overflow vs
intrinsic model degradation; reproduce the ~200s class. T2: streaming transport INSIDE `call_llm` —
same name/signature/full-text return (the fixture stub seam) — where an idle-gap timeout replaces
the 180s whole-response deadline; token-count progress events feed the existing stage stream. T3:
stage-completion progressive rendering in the LIVE region — the grounding-complete event carries
the grounded record; the page reveals converted text → GROUNDED red flags + provisional entities →
entities refine through verify i/N → final record at done. T4 (EARNED by T1): pre-flight size check
of the FULL assembled prompt + generation headroom against real n_ctx with an honest in-stream
refusal; finish_reason handling; concurrency honesty; sectioned extraction ONLY IF T1 shows
intrinsic degradation (STOP first — needs a user ruling, prompt/schema frozen). T5: full regate +
docs.

### Domain Research Questions
1. Does the user's llama-cpp build compose `stream:true` with `response_format: json_schema`
   (strict grammar)? Verify with a live probe before committing T2's design.
2. What does llama-cpp do with an in-flight request whose client disconnected (the ghost-job
   question) — does a retry queue behind dead work, and is that what produced the user's ~200s
   failure profile?
3. What are the server's real `n_ctx`, slot count, and `/tokenize` + `/props` endpoint
   availability in the user's launch configuration?

## Constraints (CRITICAL)
- **Silent context truncation must be impossible**: an over-context input must NEVER return a
  normal-looking record — the grounding gate CANNOT catch it (grounding is a substring check
  against the full source; it passes a record extracted from only the head). Guard: pre-flight
  token measurement of the FULL assembled prompt (SYSTEM_PROMPT + template + schema overhead) plus
  reserved generation headroom (= the configured max_tokens, currently 4096) against the server's
  REAL n_ctx, emitting an explicit in-stream size event; a stubbed test asserts over-context input
  yields the size event, never a normal record.
- **finish_reason must be read**: `length` → a specific "output budget exhausted" in-stream error
  distinct from a JSON parse failure. Guard: stubbed test with finish_reason="length".
- **No private text persisted or emitted outside the gitignored store**: no server logs of prompt
  snippets, no error captures embedding note text, no timing rows carrying content; any NEW fixture
  must pass the US-federal FIXTURE_META allowlist (already asserted). Guard: a stubbed test asserts
  the size/error/progress events carry token counts and failure classes ONLY — no substring of the
  input text appears in any event except the existing `converted` echo; the stress harness +
  results stay in .dev-wiki/tmp (never committed).
- **Concurrency honesty**: /extract is single-flight — a second concurrent request gets an honest
  busy answer, so a retry cannot queue behind a ghost job; on client disconnect before `done`,
  NOTHING is written to the store (the scan never happened — the decided atomic boundary). Guard:
  tests for the busy answer + mid-stream disconnect leaving the store row-count unchanged.
- **Verify-stage legibility at scale**: n=0, n=1, and n=large entity counts all render sane
  progress (never "0 of 0"); large runs show elapsed + projected time. Guard: NEW
  `news-stream.test.mjs` assertions at the three counts (committed harness, not scratch).
- **Frozen surfaces hold**: news_ground.py untouched; all client changes inside the LIVE markers;
  offline dist/news byte-identical. Guard: `--check all` 5/5 + the offline strip assertion + git
  diff review at T5.
- **The fixture stub seam survives by name, signature, AND call-count**: `call_llm` keeps its
  name/signature/full-text return; the 13 replay fixtures stay green with ZERO re-capture;
  fixture-sized inputs traverse the un-sectioned path (the stub fires exactly once per fixture).
  Guard: replay suite + a stub-call-count assertion.
- **No free parameters**: the idle-gap timeout is T1-derived (default 120s — it must tolerate the
  measured prompt-eval latency before the FIRST chunk on a near-cliff input); reserved generation
  headroom = max_tokens (4096, raised only by a T1 finding). Guard: both values named in
  ph43-stress-results.md with the measurement that set them.
- **Docs are part of the fix**: docs/news-live.md's llama-server launch command gains --ctx-size
  guidance in the SAME phase — a code-only fix leaves the next operator reproducing the failure.
- **No prompt/schema/store-write change**: any discovered need = a surfaced finding + STOP, never
  silent drift.

## Success Vision
A long, dense investigation note either extracts fully — the page revealing converted text, then
grounded red flags early (the gate has already disposed), then entities refining live through the
verify pass — or fails FAST with a named reason the analyst can act on ("note exceeds the model's
context window (N tokens over)", "output budget exhausted", "model busy with another extraction").
No more 200s opaque waits ending in generic failure. The next operator who launches llama-server
gets context-size guidance before reproducing the old failure. The replay suite proves the
deterministic core is untouched, and the offline ship artifact is byte-identical.

## Exit Criteria (machine-checkable)
- [ ] `python3 tests/news_live_test.py` — green incl. 13/13 replay with zero re-capture + NEW
  stubbed tests: finish_reason=length event, over-context size event, busy single-flight answer,
  mid-stream disconnect leaves the store unchanged, no-input-substring-in-events privacy assertion,
  stub-call-count
- [ ] `node tests/news-stream.test.mjs` — green incl. NEW staged-reveal assertions
  (grounded-flags-before-done, provisional→verified entity refinement, sane progress at
  n=0 / n=1 / n=large) + the offline strip assertion
- [ ] `node tests/corpus-explorer.test.mjs` — green (no corpus regression)
- [ ] `python3 scripts/build.py --check all` — 5/5 byte-identical
- [ ] `python3 scripts/serve_news.py --selftest && python3 scripts/news_ground.py --selftest &&
  python3 scripts/news_fetch.py --selftest && python3 scripts/derive_signals.py --selftest &&
  .venv/bin/python scripts/news_store.py --selftest` — all green
- [ ] `test -f .dev-wiki/tmp/ph43-stress-results.md && grep -q "## T4 re-run"
  .dev-wiki/tmp/ph43-stress-results.md && ! grep -q "UNHANDLED"
  .dev-wiki/tmp/ph43-stress-results.md` — the T1 matrix exists with a T4 re-run tier table where
  every tier is `PASS` or `HONEST(<named reason>)`, none `UNHANDLED`
- [ ] `python3 tests/news_live_test.py --live` — real-model smoke incl. one probe sized AT OR ABOVE
  the T1-measured failure cliff that completes or fails with a NAMED size reason (size-relative,
  not wall-clock-relative)
- [ ] `grep -q "ctx-size" docs/news-live.md` — launch guidance present (functional walkthrough at
  T5; grep is the machine check)

## Checkpoints
- After T1 (failure classification): report the matrix — which failure classes reproduced, where
  the size cliff sits, which T4 fixes are EARNED — before implementing T4.
- If T1 shows intrinsic model degradation on large inputs (not limits): STOP — sectioned
  extraction needs a user ruling (prompt/schema are frozen; chunk-merge semantics are a design
  decision, not a task detail).
- If stream:true does not compose with json_schema in the user's build: fall back to non-streaming
  with a T1-measured raised timeout + socket read-timeout idle detection; report the fallback at
  the T1 checkpoint. A2' rendering is unaffected (stage-driven, not token-driven).
- If offline dist/news cannot stay byte-identical after the LIVE-region edits: STOP and surface.
- T1 and the --live probes need the user's llama-server running: flag when needed rather than
  silently skipping.

## Assumptions
- The user's llama-server exposes `/props` (n_ctx) and `/tokenize`. If false: estimate tokens
  conservatively (assembled-prompt chars/3) and say so in the refusal message —
  imprecise-but-honest beats silent truncation.
- `stream:true` composes with `response_format: json_schema` in this llama-cpp build. If false:
  the checkpoint fallback above (raised timeout, no streaming); the timeout fix still lands via
  measured limits.
- The ~200s failure class reproduces on synthetic tiered material. If false: instrument ONE live
  run on the user's real note locally at a checkpoint (results reported as numbers only, no
  content persisted or echoed).
- llama-cpp serializes concurrent requests (single slot default). If false: the single-flight
  guard is still correct, merely less load-bearing.
- The negative-news wiki's stored bodies provide long commercial stress articles locally. If
  false: synthetic tiers alone cover the size dimension (complexity tiers are already synthetic).
