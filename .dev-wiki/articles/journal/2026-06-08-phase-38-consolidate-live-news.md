---
title: "Phase 38: Consolidate the live news subsystem (verify agent backend + watchlist management)"
aliases: []
category: journal
tags: [news, live, m8, agent-backend, qwen, opus, grounding, fixtures, entity-precision, context-shaping, second-pass-verify, watchlist, prune, inter-rater-agreement, offline-strip]
parents: [phase-38-consolidate-live-news]
created: 2026-06-08
updated: 2026-06-08
source: debrief
duration: unknown
---

# Phase 38: Consolidate the live news subsystem (verify agent backend + watchlist management)

## What Happened

- CONSOLIDATED the Phase-35/36 LIVE news subsystem (companion-served, dev/authoring-time only) —
  chosen at the dev-plan gate over extending source scale (FINTRAC /intel/ depth OR a third
  jurisdiction AUSTRAC/UK, both DEFERRED). Two halves: verify+lock the agent backend, complete the
  Phase-36 watchlist loop with a view+prune. The phase GREW 5 planned → 7 tasks (T2 + T4 added
  mid-phase per user adjudication).
- **T1 — verified the live Qwen backend end-to-end** across all 4 committed DOJ/OFAC articles
  (16–40s each); the grounding gate dropped 4 ungrounded flags corpus-wide (the messy-real output
  the hand-written CANNED stub never exercised). Captured `<id>.qwen.json` (raw) + `<id>.golden.json`
  (grounded) per article under `tests/fixtures/news-live/`. Claude-reference agreement
  (`.dev-wiki/tmp/ph38_agree.py`, consensus framing, NO accuracy number): 22 consensus subjects,
  ZERO Qwen misses (perfect subject recall) but +22 noise + 8 surname-alias dups; flags 23 consensus,
  Qwen the more-thorough rater. CHECKPOINT → user adjudicated: add an entity-precision filter (new T2).
- **THE PIVOT (the headline): a deterministic denylist OVERFIT, replaced by context shaping.** T2
  shipped a structural `screen_entities` (alias-dedup / source-line / judicial / moniker) PLUS a small
  institutional-noise denylist — which cut OFAC 33→14 cleanly on the 4 CALIBRATION articles. But T4's
  stress test on 3 NEW federal articles (DOJ Chinese-CMLO, DOJ transnational-fraud RICO, OFAC Sinaloa)
  exposed the denylist as overfit: 38 of 69 entities were still noise (announcing officials,
  prosecutors, agency field offices, court districts — an OPEN vocabulary a denylist can't enumerate;
  on transnational-fraud it removed 0). The real lever was CONTEXT SHAPING: one SUBJECTS-ONLY rule in
  `serve_news.SYSTEM_PROMPT` cut Qwen 95→35 raw / ~3 noise and GENERALIZES. So T2 was REVISED — trimmed
  `screen_entities` to its generalizing structural rules and DROPPED the denylist.
- **Qwen-vs-Opus USABILITY VERDICT.** Under the SAME prompt + SAME grounding pipeline (only the model
  differs): under the original prompt Opus (29 entities, ~all real subjects) was 3× cleaner than Qwen;
  under the FIXED prompt Qwen nearly closes the gap (35 vs 29). The gap was INSTRUCTION CLARITY, not
  capability → a well-prompted LOCAL Qwen is usable; NO API/Opus backend needed (keeps the
  offline/no-key design).
- **Keep-biased second-pass entity verify, wired in on-by-default** (user idea, user chose wire-in).
  A naive forced-choice variant LOST 6 real designated parties (net-negative in AML); the keep-biased
  + alias-aware-context variant drops 5 residual institutional entities (incl. the 3 transnational-fraud
  agencies nothing else caught) with ZERO subject loss. Lives in `serve_news.extract` (LIVE-only,
  fail-OPEN=KEEP, layered ON TOP of the deterministic `build_record` the replay fixtures pin);
  `--no-verify-entities` disables.
- **Half B — watchlist view+prune** completed the Phase-36 feedback loop (previously the escalated
  surface only GREW): `news_store.prune(name)` un-escalates (retains the audit row), a
  `POST /watchlist/prune` route, and a `news.html` live-region panel (escalated surface + provenance +
  a ✕ Prune per row, onclick delegation). All inside `/*LIVE_START*/…/*LIVE_END*/` → stripped offline
  → `dist/news` BYTE-IDENTICAL.
- T3 added the OFFLINE recorded-fixture replay (each `<id>.qwen.json` → parse→build→ground→screen →
  asserts the committed golden, 34 drops reproduced, no model) + an opt-in `--live` smoke OFF the
  default run. T7 regated, promoted the 3 stress articles to fixtures (`<id>.article.md` kept in
  tests/, NOT in `data/news/articles` so dist/news stays frozen), updated docs + CLAUDE.md in place,
  committed + pushed.

## Decisions Made

- D1 (DIRECTION) — CONSOLIDATE the live subsystem over extending source scale (FINTRAC /intel/ vs a
  third jurisdiction, both DEFERRED). [USER]
- D2 (EVALUATION/HONESTY) — Claude/Opus is a SECOND rater, not ground truth: report Qwen-vs-Claude as
  INTER-RATER AGREEMENT (consensus) + divergences, NO accuracy/precision/recall number; the always-on
  badge stays. Mirrors Phase 34/37.
- D3 (ARCHITECTURE) — watchlist view+prune is COMPANION-ONLY; offline `dist/news` byte-frozen (all new
  code in the stripped live region; build.py never imports the live/store layer).
- The entity-precision approach was REVERSED mid-phase: denylist (overfit) → context shaping
  (subjects-only system-prompt rule + trimmed structural filter). [stress-test-driven, USER adjudicated]
- The keep-biased second-pass verify was WIRED IN on-by-default. [USER idea + USER chose wire-in]

## Problems Solved

- The deterministic noise denylist couldn't enumerate the open vocabulary of officials/prosecutors/
  agencies — resolved by moving the lever upstream to the system prompt (a SUBJECTS-ONLY exclusion
  rule that generalizes), and keeping the deterministic filter only for the structural rules
  (alias-dedup/source-line/judicial/moniker) that DO generalize.
- The naive second-pass forced-choice verify lost real designated parties — resolved by making it
  keep-biased + alias-aware-context + fail-open=KEEP (drop institutional noise only, never a subject).
- A latent risk: layering the verify pass ON TOP of `build_record` (LIVE-only, in `extract`) rather
  than inside it keeps the deterministic offline replay core untouched (the fixtures still pin the
  pre-verify contract).

## Open Questions

- Second-pass verify adds one model call per entity per scan (latency). Acceptable for the
  dev/authoring demo; `--no-verify-entities` is the escape if it bites in a live presentation.
- CLAUDE.md is at 255 lines, over the ~200 maintenance-contract target (pre-existing drift). A trim
  pass is deferred — not yet user-requested.

## Artifacts Changed

- `scripts/serve_news.py` (subjects-only `SYSTEM_PROMPT` rule; `verify_entities`/`verify_subject`/
  `_entity_context` keep-biased second pass, on by default, `--no-verify-entities`, fail-open;
  `POST /watchlist/prune` route `_prune`; prune in `live_config`; `httpd.verify` flag)
- `scripts/news_ground.py` (`screen_entities` structural entity-precision pass — alias-dedup/
  source-line/judicial/moniker; the institutional denylist REMOVED after the stress test)
- `scripts/news_store.py` (`prune(name)` un-escalate method — retains the audit row)
- `news.html` (live-region watchlist view panel `liveRenderWatchlistPanel` + `livePrune`, onclick
  delegation — inside the stripped live region)
- `tests/fixtures/news-live/` (NEW recorded-fixture replay corpus — 7 articles = 4 calibration + 3
  promoted real DOJ/OFAC stress; each `<id>.qwen.json` raw + `<id>.golden.json`; the 3 stress also
  carry `<id>.article.md`, NOT added to `data/news/articles` so dist/news stays frozen)
- `tests/news_live_test.py` (+`fixture_replay_test` over 7 fixtures, +`verify_entities_test`, +prune
  route test, +opt-in `--live` smoke)
- `tests/news-stream.test.mjs` (76→81: +strip assertion for view/prune code, +source-carries,
  +behavioral panel render, +empty-state)
- `docs/news-live.md`, `tests/smoke-checklist.md`, `CLAUDE.md` (in-place `## Current state`)
- NO dist/ changes (offline `dist/news` byte-identical), NO committed-corpus / corpus / showcase
  changes. build.py still never imports the live/store layer (it DOES import `news_ground` by design).

## Related

- [[phase-38-consolidate-live-news|Phase 38: Consolidate the live news subsystem]] — parent phase

## Soft Observations / Phase 39 Candidates

- CLAUDE.md 255-line trim pass — a durability/hygiene candidate (the maintenance contract targets
  ≤~200). | Phase 39 = CLAUDE.md trim | evidence: CLAUDE.md line count.
- The standing SCALE frontier deferred at this gate is still open: FINTRAC /intel/ depth (OA001 +
  sanctions-evasion / Russia-ML / dual-use SBs) OR a third jurisdiction (AUSTRAC CC BY / UK OGL). |
  Phase 39 = extend source scale | evidence: _CURRENT_STATE deferred-candidates.
- A recorded-fixture for the SECOND-PASS verify (currently only stub-tested + `--live`) — to pin the
  keep-biased verify deterministically offline. | evidence: tests/news_live_test.py verify_entities_test.
- Second-pass latency optimization (batch the verify into one call, or a smaller/faster verify model)
  if it bites in live demos. | evidence: serve_news.verify_entities (one call per entity).
- Grow the replay-fixture corpus with more varied articles to harden the prompt+verify against
  regressions. | evidence: tests/fixtures/news-live/.

### Retro Check

Not triggered (26 `status: completed` phases after Phase 38 flips; 26 % 5 != 0).
