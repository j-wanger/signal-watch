---
title: "Phase 46: Corpus live derivation mode — local-model agentic derivation through the frozen gate (M7×M8 convergence)"
aliases: []
category: journal
tags: [live-mode, corpus, local-model, opencode, derivation, m7, m8]
parents: [phase-46-corpus-live-derivation]
created: 2026-06-11
updated: 2026-06-11
source: debrief
duration: unknown
---

# Phase 46 — Corpus live derivation mode (M7×M8 convergence)

## What Happened
- Lite, 4 tasks, ALL [x] same-session (planned evening 2026-06-10, executed overnight into 2026-06-11). READY FOR COMPLETION — delivery gate pending. Direction = the user's 5th reframe in 6 gates: "live mode with local model for the corpus demo as well, ideally with a better harness integration like opencode". The presentation TODAY 2026-06-11 outranked everything — A4 held: dist/corpus BYTE-IDENTICAL, nothing presentation-touching moved.
- T1 HARNESS PROBE (the headline): on the same held-out doc (FINTRAC-2024-OA001, fetched + converted via the committed path, LOCAL-ONLY) both harnesses extracted the IDENTICAL 17 indicators (17/17 pair-matched), both gate-green FIRST shot, 0 violations; direct 82.6s / 1 strict-schema streamed call vs opencode 1.17.3 255.1s (3.1×) / 7 tool calls / 0 tool-call failures. opencode's differentiator (iterate-on-gate-failure) NEVER ENGAGED — consistent with Phase-44 (failures were gate-class, not model-class). Subtraction test → DIRECT + ONE violation-guided retry chosen at the USER CHECKPOINT; the loop's one real idea folded into the pipeline as the deterministic retry; opencode stays installed for dev use. Cross-harness C/D tag agreement C 12/17 / D 15/17 — inside the Phase-34 blind inter-rater band (tags remain the unguarded neural dimension). Report: `.dev-wiki/tmp/ph46/ph46_probe.md`.
- T1 side-findings: the held-out doc parses CLEAN under EXISTING rf_region anchors (region (220,376)) — no anchor extension; the triage flag_count 42 is a line-count heuristic, the genuine list is 17 tofu bullets + 1 glyph-dropped line; probe-local ph46_gate.py verified posture→status/data EXACT on all 2,251 committed indicators; the running model measured Qwen3.6-35B-A3B-UD-Q4_K_XL (agentic-tuned MoE class, --jinja confirmed, n_ctx 65536/slot) — A3's swap clause never fired.
- T2 scripts/serve_corpus.py (NEW, stdlib-only, port 8010 — the SECOND live companion): spec built deterministically from data/capability-taxonomy.json + 3 committed FINTRAC few-shot exemplars; streaming strict-schema call_llm (idle-gap timeout, named failures incl. preflight w/ --ctx-size remedy); deterministic assemble + the imported FROZEN check_record; ONE violation-guided retry then grounded-or-dropped w/ honest counts; NDJSON staged /derive (single-flight 409, disconnect-abandons, NOTHING persisted). Live E2E: 17 kept / 0 dropped, INDEPENDENT re-gate 0 violations.
- T3 corpus.html /*LIVE_START*/…/*LIVE_END*/ region: session-only LIVE_DOCS, "Live derivations (this session — UNREVIEWED)" Select group + paste form (Documents lens only; URL mode consciously omitted — the /intel/ frontier is PDF-shaped), livePick routing the EXISTING 6-screen arc, the Phase-44-pattern processing takeover (Esc arm→abort; presenter keys blocked), stage-completion labels (token COUNTS never content); build.py render_corpus strips LIVE_REGION_RE → dist/corpus BYTE-IDENTICAL.
- T4 docs/corpus-live.md (news-live sibling) + smoke-checklist corpus-live subsection + CLAUDE.md updated IN PLACE; FULL REGATE green across 9 suites.

## Decisions Made
- [[decisions/phase-46-corpus-live-derivation|Phase 46 direction]] — T1 checkpoint OUTCOME appended (direct+retry over opencode; news-lift eval explicitly SEPARATE, staged in .dev-wiki/tmp/ph46/).
- T3 URL-mode omission = a noted in-task deviation (documented in the tasks.md T3 line), not an escape hatch.

## Problems Solved
- build._inline_article takes a PATH not text — its die() killed the /derive handler thread → switched to build._strip_provenance. (Found live at T2 E2E.)
- The arc field is `article_text`, not `article` — fixed at T2 E2E.

## Open Questions
- News-side opencode lift eval (entities+relationships): run it? when? — user's call, outside the phase (ready-to-run in .dev-wiki/tmp/ph46/).
- Deferred candidates carry forward unchanged (FINTRAC /intel/ remainder, third jurisdiction, fuzzy-merge, bulk scan, Phase-45 residuals incl. byte-surgical mojibake repair).

## Artifacts Changed
- `scripts/serve_corpus.py` (NEW live companion; --selftest incl. stubbed full-loop retry + payload-parity guard vs build.render_corpus)
- `corpus.html` (/*LIVE_*/ region) + `scripts/build.py` (render_corpus strip, one line)
- `tests/corpus-explorer.test.mjs` (273→303, +30: strip class, live injection, pure processing-page contract, done/error/409 paths)
- `docs/corpus-live.md` (NEW) + `tests/smoke-checklist.md` + `CLAUDE.md` (245→263 — the carried trim residual got heavier)

## Health Delta
- corpus 273→303 (+30); serve_corpus --selftest NEW; all 9 suites green; --check all 5/5 ZERO DRIFT (dist/corpus byte-identical THROUGH the live-region addition). Review gate: 9/10 ACCEPT, zero HIGH; 4 MEDIUMs (stray log DELETED, stale probe path FIXED, staleness → this debrief, CLAUDE.md 263 vs ~200 carried).

## Related
- [[phase-46-corpus-live-derivation|Phase 46]] — parent phase

## Soft Observations / Phase 47 Candidates
- The retry path has NO live exercise yet (both probe docs passed first-shot — the Phase-44 pattern); a FINTRAC Special Bulletin would likely engage it AND exercise the open rf_region heading-form question — natural corpus-extension material (3 of the /intel/ frontier's 4 docs remain underived; tax-fiscale's gate-green derivation exists local-only as propose-material). | evidence: T1 probe report
- serve_corpus.corpus_payload() duplicates render_corpus's load/validate/merge (parity-guarded); a future build.corpus_payload() factoring kills the duplication. | reviewer suggestion
- Retry-failure reason swallowed into the generic "retry returned fewer corrections" dropped note — small honesty-of-accounting refinement. | reviewer suggestion
- Live-derived FINTRAC docs render verbatim flags WITHOUT the Crown-copyright footer — acceptable for a dev-time propose-only tool; needs a compliance look if live mode is ever shown beyond dev. | T3
- Live BUILD_NOW build_logic is a minimal shape-valid template; promoting a live-derived record to data/ needs the full per-capability spec templates rebuilt (ph33_apply.py is GONE from tmp — reconstruction needed). | T2
- CLAUDE.md 263 vs ~200 — carried trim candidate (own-commit precedent). | review gate
