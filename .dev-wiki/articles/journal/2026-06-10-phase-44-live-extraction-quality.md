---
title: "Phase 44: Live extraction quality — targeted harness, classified fixes, processing page (live news) — implemented, ready for completion"
aliases: [phase-44-journal]
category: journal
tags: [news-live, extraction-quality, red-flags, aliases, grounding-gate, quality-harness, processing-page, hygiene, measure-first]
parents: [phase-44-live-extraction-quality]
created: 2026-06-10
updated: 2026-06-10
source: debrief
duration: ~1 session (planned + implemented 2026-06-10, same day)
---

# Phase 44: Live extraction quality — targeted harness, classified fixes, processing page — implemented, ready for completion

## What Happened
- ALL 7 lite tasks T1–T7 [x] same-session under the approved spec `specs/phase-44-live-extraction-quality.md` (nana:approved). Direction = the user's REFRAME at the dev-plan gate: missed high-risk-country wire flags + wrong alias assignments + a fresh processing page + the user's own "better specific harness?" hypothesis as the T1 frame; speed resolved as quality-gated T4.
- **THE CLASSIFICATION VERDICT (T1 — the phase's headline):** the user's "missed wire flags" = **GATE-DROP, NOT model recall** — `ground_record` requires a RAW substring; a model quote crossing a hard line-wrap (newline→space) failed even though `news_normalize` matches (4/5 planted wire facts dropped on wrapped prose; the user's seeded STR sample 3/5). Sibling drop-paths: `*`-strip asymmetry (extract() prompts RAW, grounds vs `article_body` which strips `*`) + title-line quotes. Model recall healthy (5/5 on single-line bullets). Alias misassignment = predominantly DETERMINISTIC fold misparent: rule (a) folded a bare token-subset into the FIRST superset entity (proven ORDER-DEPENDENT — same input, swapped order → different owner) + TYPE-BLIND (person folded as an org's alias); residual: the gate's alias check is PRESENCE-only, never WHOSE — model-assigned wrong-owner alias kept (constructed P1c; zero live evidence — measured, not gated).
- T1 HARNESS (the user's hypothesis, delivered): NEW COMMITTED `tests/news_quality_harness.py` — deterministic replay of all 13 pinned captures (via build_record, the replay-test seam) + the 4 committed records; dimensions kept_flags[≥] · mech_families[≥] · entity_count[=] · alias_suspects[≤] · type_blind_folds[≤] (alias-OWNERSHIP suspicion = the previously-unmeasured dimension); `--check` exits non-zero on any regression vs the NEW committed `tests/fixtures/news-live/quality-baseline.json` (121 flags / 84 fams / 115 ents / 0 suspects / 0 tbf); `--freeze` = a conscious re-baseline. THE regression gate for any future prompt/gate/model change.
- T2 FIX (gate-drop class): `news_ground.locate_span` — wrap-tolerant locator (whitespace runs + `*` as whitespace) that REQUOTES the flag to the body's EXACT bytes (raw substring BY CONSTRUCTION — highlighter + all downstream invariants hold); applied to red-flag `flag` + relationship `evidence`; entity names/aliases left as-is (no evidence — measure-first); title-line quotes still drop honestly. Selftest-pinned (wrap requote · idempotence · `*` · title-None · evidence-wrap). Result: synthetic n2 1/5→5/5 KEPT; the user's seeded STR note 3 drops→0 (Hong Kong (High-1)/China wires + GIC depletion + third-party benefit all grounded). 13/13 replay green WITHOUT golden regeneration (no pinned capture had wrap-broken quotes — purely additive on the live path).
- T3 FIX (fold-misparent class): `screen_entities` fold rule (a) — AMBIGUITY REFUSAL (2+ type-compatible superset parents → honest drop "ambiguous alias of N entities — not folded"; wrong attachment poisons the anchor store, worse than a drop) + TYPE-MATCH (person never folds into org; type DISAMBIGUATES a person+org parent pair). Order-independence selftest-pinned; Phase-41 fold upsides (@monalisa7→Chirkinyan, Rossi→George Rossi) unregressed. Known-honest recall cost: nested parents ("John Smith" ⊂ "John Jacob Smith") now refuse too — a unique-MAXIMAL-parent rule is the named safe recovery if evidenced.
- T4 HONEST SKIP (measured): the user-workload hotspot (model generation, 92–98% of wall on note-register input: 64.5s/0.02 · 15.9s/0.06 · ~10s/0.08 verify share) IS the extraction (≈400–450 tokens/entity) — no quality-preserving lever at a fixed model; verify (the only lever) is 2–8% on notes. Named future levers: slot-parallel per-entity verify (zero semantic change; pays on entity-rich/bulk workloads) + a smaller-model eval gated by the harness. The user's perceived ~200s also included the pre-43 ghost-job/truncation behavior, already fixed.
- T5 SHAPE: dedicated processing page = IN-PAGE viewport takeover `#liveproc` (real navigation would abort the NDJSON stream + leave a 409 ghost) — pure `liveProcBody` + `liveProcKeyAction` (presenter-nav blocked mid-run; Esc ARMS w/ honest warning → Esc ABANDONS via AbortController [disconnect persists nothing]; Esc closes when not running); 409/stream-error/abort all NAMED on the page, grounded partials stay visible; the staged Phase-43 preview retargeted via `livePreviewEl()`. news-stream 140→150.
- T6 ARCHIVAL MECHANISM (the 3-gate-deferred hygiene debt, resolved): verbatim archives + pointer indexes — tasks.md 755 lines/418KB → 61 lines/11KB (`articles/tasks-archive-pre-phase-44.md`, 37 phase blocks verbatim); _CURRENT_STATE 22 pre-Phase-42 resolved blockers → `articles/state-archive-resolved-blockers.md` (111→89 lines); _ARCHITECTURE 11.5KB header narrative + verbose layout/pipeline → `articles/state-archive-architecture-header.md` w/ compact replacements (163→94). Lossless (reviewer-verified: 22+2=24 baseline entries; 37 blocks verbatim). NEW CONVENTION: tasks.md stays active-phase-only + pointer index.
- T7 + PRIVACY: full regate (see Health Delta) + docs/news-live.md + smoke-checklist + CLAUDE.md in place. The user's sample sentences (STR register: Hong Kong (High-1)/China (High-2) wires in favor of a joint-account relative, GIC depletion) live ONLY in gitignored `.dev-wiki/tmp/ph44/` — privacy grep reviewer-verified zero tracked hits.

## Decisions Made
- D1–D5 recorded at planning ([[phase-44-live-extraction-quality|decision article]] + ledger). Implementation-level decisions (lite — recorded above per task): requote-by-construction over normalize-side loosening (T2); ambiguity-refusal over best-guess attachment (T3); measured skip over speculative optimization (T4); in-page takeover over real navigation (T5); verbatim-archive + pointer-index convention (T6).

### Review Gate
- Unified reviewer 9/10 ACCEPT, ZERO HIGH+. 3 MEDIUMs: 2 staleness (active-phase.md + _CURRENT_STATE Active Phase/Key-Artifacts counts) → fixed by THIS debrief (the line-70 count already fixed inline by the orchestrator); 1 carried: CLAUDE.md 238 lines vs the ~200 target (growth 220→225→238 across Phases 42–44; the Phase-42 own-commit trim is the named precedent). 2 suggestions: alias_suspects redundant disjunct → FIXED inline; nested-parents fold recall cost → noted as known-honest (soft obs).

## Open Questions
- None new blocking. Carried residuals: P1c alias-ownership (measured-not-gated) · alias RECALL ("used the alias X" attribution unattached) · nested-parents fold recall cost · CLAUDE.md trim — all in Soft Observations below.

## Artifacts Changed
- `tests/news_quality_harness.py` + `tests/fixtures/news-live/quality-baseline.json` (NEW, committed) · `scripts/news_ground.py` (locate_span requote; fold ambiguity/type rules) · `scripts/serve_news.py` (evidence requote path) · `news.html` (LIVE region: #liveproc processing page) · `tests/news_live_test.py` · `tests/news-stream.test.mjs` (140→150) · `docs/news-live.md` · `tests/smoke-checklist.md` · `CLAUDE.md` · `specs/phase-44-live-extraction-quality.md` · `.dev-wiki/{tasks.md,_CURRENT_STATE.md,_ARCHITECTURE.md}` + 3 archive articles (T6) · `.dev-wiki/tmp/ph44*` (LOCAL scratch, gitignored)

## Health Delta
- news-stream 140→150 (+8 Phase-44 pure-function tests + 2 strip assertions); news_ground --selftest +2 fixture blocks (wrap-requote + fold rules); NEW harness (17 fixtures, 5 gated dimensions); all suites green (--check all 5/5 · corpus 239 · all selftests · news_live_test system + .venv + --live); offline dists byte-identical throughout; ZERO golden regeneration, ZERO re-capture. No escape hatches; no scope growth.

## Assumption Revisit (ledger filled)
- A1 held (failures reproduced on constructible material; the seeded STR sample confirmed the gate-drop class on the real register; speed condition → the T4 measured skip) · A2 held (classification decisive — gate-drop not model recall, fold-misparent not model aliases; fixes followed the class; P1c stayed a measured residual) · A3 held (locate_span + fold changes through known seams — 13/13 replay green ZERO re-capture, goldens not even regenerated; no EXTRACT_SCHEMA change) · A4 held (LIVE-region-only; --check all 5/5; hygiene lossless reviewer-verified). No prior-phase late bites observed (Phase-43 A2' stage-rendering carried cleanly onto the new page).

### Gate Compliance
- tasks.md gate-log `phase-44 direction=approved delivery=pending` — direction present ✓; delivery=pending is CORRECT pre-commit (the delivery flow flips it in its own post-commit-verify commit).

## Related
- [[phase-44|Phase 44: Live extraction quality — targeted harness, classified fixes, processing page (live news)]] — parent phase

## Soft Observations / Phase 45 Candidates
- Alias-ownership verify extension — a keep-biased verify question per model-assigned alias IF seeded real material evidences wrong model-assigned aliases (today: zero live evidence; the harness alias_suspects dimension watches it). Evidence: ph44_probe P1c; harness dimension 0 on all committed material.
- Alias RECALL — the article's own "X used the alias Y" attribution is not attached (live n3: "M. Reyes" extracted as an entity, verify killed it, attached to no one). A prompt-iteration or deterministic attribution-pattern candidate. Evidence: .dev-wiki/tmp/ph44-results.md residuals.
- Slot-parallel per-entity verify — zero semantic risk, pays on entity-rich articles; couples to the deferred bulk-scan candidate. Evidence: T4 profile (verify 2–8% on notes but the majority on 16–25-entity articles, Phase-39 measurement).
- Smaller-model eval — the committed harness's --check makes a quality-gated model swap measurable for the first time. Evidence: tests/news_quality_harness.py.
- Nested-parents fold recall — "Smith" with parents "John Smith"+"John Jacob Smith" now refuses; a unique-MAXIMAL-parent rule recovers it safely if evidenced. Evidence: reviewer suggestion, Phase-44 review.
- CLAUDE.md trim — 238 lines vs the ~200 target (growth 220→225→238 across 42–44); the Phase-42 own-commit trim is the precedent. Evidence: reviewer MEDIUM.
- Real-browser processing-page walk — the page is pure-function-pinned + source-asserted but not yet walked in a real browser; the smoke-checklist Phase-44 item covers it pre-presentation. Evidence: tests/smoke-checklist.md.
