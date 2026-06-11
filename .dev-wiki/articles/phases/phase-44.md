---
title: "Phase 44 — Live extraction quality: targeted harness, classified fixes, processing page (live news)"
aliases: [phase-44, phase-44-live-extraction-quality]
category: phases
tags: [live-news, extraction-quality, red-flags, aliases, measurement, harness, m8]
parents: []
created: 2026-06-10
updated: 2026-06-10
source: plan
status: completed
scope: [tests/news_quality_harness.py, scripts/serve_news.py, scripts/news_ground.py, news.html, tests/news_live_test.py, tests/news-stream.test.mjs, tests/fixtures/news-live/**, .dev-wiki/tmp/ph44*, .dev-wiki/tasks.md, .dev-wiki/_CURRENT_STATE.md, .dev-wiki/_ARCHITECTURE.md, docs/news-live.md, tests/smoke-checklist.md, CLAUDE.md, specs/]
entry_criteria: "Phase 43 delivered + accepted + committed (fba2bb0/58a9ed6) + pushed; 0 open tasks; assumption gate closed 2026-06-10."
exit_criteria: "Both reported failure classes reproduced + classified + fixed-or-honestly-reported; the targeted quality harness committed (deterministic on fixture material, alias-ownership scoring); quality-gated speed optimization at the T1-proven hotspot or an honest skip-with-reason; the fresh processing page in the LIVE region only; the hygiene trim lossless; 13/13 replay fixtures green NO re-capture; the 4 committed records pass the gate; offline dist/news byte-identical (--check all 5/5); node news-stream + corpus green; all selftests + news_live_test (system + .venv + --live incl. a wire-note probe) green; docs/smoke/CLAUDE.md updated in place."
---

# Phase 44 — Live extraction quality: targeted harness, classified fixes, processing page (live news)

## Objective

The user's REFRAME at the dev-plan gate 2026-06-10 (off the offered candidates — fuzzy-merge, bulk
scan, FINTRAC /intel/, AUSTRAC/UK — all deferred again; hygiene BUNDLED as T6): live extraction
quality is not good enough — (1) red-flag RECALL: misses obvious flags around high-risk-country
wires in limited real testing; (2) alias PRECISION: entities assigned aliases that are clearly not
them; (3) UX: after clicking run extraction, processing should show on a FRESH dedicated page;
(4) the user's own hypothesis "do we need a better specific harness?" accepted as the T1 frame;
(5) processing SPEED surfaced at the gate — resolved as a QUALITY-GATED optimization task
(optimize only where the harness proves quality holds).

## Approach

Measure-first, CLASSIFICATION-first (the Phase-38/40 playbook, now targeted):

- **T1 (M)** — promote the gitignored Phase-40 registry-scoring scratch to a COMMITTED harness;
  extend with alias-ASSIGNMENT scoring (ownership — currently unmeasured: the gate checks an alias
  is verbatim, never WHOSE it is); targeted material = synthetic high-risk-country wire notes
  EMBEDDING the user's sample sentences + local-only commercial articles (ALL local gitignored,
  never committed); per-stage wall-time profile; REPRODUCE + CLASSIFY both failures:
  flags = missed-at-generation vs dropped-at-gate (grounding drop / dup-collapse) vs registry blind
  spot (the SYSTEM_PROMPT registry already names "high-risk-jurisdiction" — serve_news.py:158);
  aliases = model-generated bad alias vs deterministic fold misparent (token-subset rule or
  _adjacent_parent moniker fold — news_ground.py:258,293-300).
- **T2 (M)** — red-flag recall fix per T1 class: prompt-iteration-first per the Phase-41 ruling
  (prompt-regression gate: red_flags FIRST schema order, never-reduce guard, holdout eval); gate
  fixes via the known regate procedure (4 committed records + 13 replay goldens regenerate
  deterministically, NO re-capture); a structural EXTRACT_SCHEMA change = a surfaced FINDING first.
- **T3 (M)** — alias precision fix per T1 class: fold-logic repair (deterministic, fixture-pinned)
  and/or prompt rule and/or verify extension (alias-ownership check); the Phase-41 fold upside
  cases (e.g. @monalisa7→Zhdanova) unregressed.
- **T4 (M)** — quality-gated speed optimization at the T1-proven hotspot (likely the verify loop —
  the batched one-call shape per Phase-40 D5); honest skip-with-reason if no optimization preserves
  quality.
- **T5 (M)** — fresh processing page: run-extraction navigates to a dedicated processing screen;
  the Phase-43 staged rendering moves onto it; LIVE region only; offline dist/news byte-identical.
- **T6 (S)** — bundled hygiene trim (user-approved): archive closed tasks.md phase blocks +
  _CURRENT_STATE/_ARCHITECTURE under their ~100-line caps; pointers to journals/articles; lossless.
- **T7 (S)** — full regate + docs.

## Constraints carried

- PRIVACY: the user's sample sentences + real failing examples + commercial captures LOCAL-ONLY
  (gitignored), never committed; fixtures US-federal-only (FIXTURE_META allowlist).
- The always-on badge stays; NO non-negotiable change; offline dist/news byte-identical throughout
  (--check all 5/5).
- PRECONDITION satisfied: specs/phase-44-live-extraction-quality.md nana:approved 2026-06-10 via
  /spec --internal (Phase 40/42/43 precedent).

## Assumption gate

Closed 2026-06-10: A1 accept-with-conditions (sample sentences; speed → quality-gated T4),
A2 accept, A3 don't-know→defended→accept, A4 accept. Ledger block in assumption-ledger.md;
decision article [[decisions/phase-44-live-extraction-quality]].

## Notes

Knowledge gaps carried to implementation: whether the user's wire-miss material reproduces (T1's
job); the actual failure classes (T1); whether batched verify preserves quality (T4).

## Status (2026-06-10 debrief)

7/7 tasks [x] same-session (T4 = honest skip-with-reason per its success criterion: the hotspot is
model generation, 92–98% of wall on notes — no quality-preserving lever at a fixed model). Exit
criteria MET: both failures reproduced + classified + fixed per class (flags = GATE-DROP →
news_ground.locate_span wrap-tolerant requote, the user's seeded STR note 3 drops→0; aliases =
deterministic fold misparent → ambiguity-refusal + type-match, Phase-41 upsides unregressed);
harness COMMITTED (tests/news_quality_harness.py + quality-baseline.json — 17 fixtures, 5 gated
dimensions incl. alias-ownership); processing page LIVE-region-only; hygiene trim lossless. Full
regate GREEN: --check all 5/5 zero drift · corpus 239 · news-stream 140→150 · all selftests ·
news_live_test system/.venv/--live · 13/13 replay NO re-capture · harness --check OK. Reviewer 9/10
ACCEPT, zero HIGH+. Assumption revisit: A1–A4 ALL held. READY FOR COMPLETION — delivery gate
pending (status flips at the delivery flow, not here). Journal:
[[2026-06-10-phase-44-live-extraction-quality]].
