---
title: "Phase 44: Live extraction quality — targeted harness, classified fixes, processing page"
type: decision
confidence: high
source: plan
created: 2026-06-10
updated: 2026-06-10
tags: [live-news, extraction-quality, red-flags, aliases, measurement, harness]
---

# Phase 44: Live extraction quality (DRAFT — pre-gate)

## Direction (user reframe at the dev-plan gate, 2026-06-10)

The user reframed off the offered menu (fuzzy-merge / bulk-scan / FINTRAC intel / hygiene — all
deferred again, hygiene BUNDLED as a task): live extraction quality is not good enough —
(1) **red-flag recall**: misses obvious flags around high-risk-country wires in limited real testing;
(2) **alias precision**: entities assigned aliases that are clearly not them;
(3) **UX**: after clicking run extraction, processing should show on a fresh dedicated page;
(4) user's own hypothesis: "do we need a better specific harness?" — accepted as the T1 frame.

## Approach (proposed)

Measure-first, classification-first (the Phase-38/40 playbook, now TARGETED):

- **T1 — committed targeted harness.** Promote the gitignored Phase-40 registry-scoring scratch to a
  committed harness; extend it with alias-ASSIGNMENT scoring (ownership, not just verbatim-ness —
  currently unmeasured). Targeted material: synthetic high-risk-country wire notes + local-only
  commercial articles + the user's actual failing examples (local dir, gitignored, NEVER committed).
  REPRODUCE + CLASSIFY both failures:
  - flags: missed-at-generation vs dropped-at-gate (grounding drop / dup-collapse) vs registry blind
    spot (the SYSTEM_PROMPT registry already names "high-risk-jurisdiction" as a family — serve_news.py:158);
  - aliases: model-generated bad alias vs token-subset fold misparent vs `_adjacent_parent` moniker
    fold (news_ground.py:258,293-300 — deterministic, not neural).
- **T2 — red-flag recall fix per T1 class.** Prompt-iteration-first (Phase-41 ruling) with holdout
  eval + the never-reduce guard; if the class is gate-drop → gate fix via the known regate procedure.
- **T3 — alias precision fix per T1 class.** Fold-logic repair (deterministic, fixture-pinned) and/or
  prompt rule and/or a verify extension (the keep-biased verify checks entity existence, not alias
  ownership).
- **T4 — fresh processing page.** Run-extraction navigates to a dedicated processing screen (LIVE
  region only; the Phase-43 staged rendering moves there); offline dist/news byte-identical.
- **T5 — bundled hygiene trim** (user-approved): archive closed tasks.md phase blocks +
  _CURRENT_STATE/_ARCHITECTURE under cap, pointers to journals/articles.
- **T6 — full regate + docs.**

## Constraints carried

- Privacy (Phase-40 D3 / 43 D5): real failing examples + commercial captures LOCAL-ONLY; fixtures
  US-federal-only.
- Prompt changes through the prompt-regression gate (red_flags FIRST schema order preserved;
  never-reduce).
- news_ground changes regate the 4 committed records + 13 replay goldens (deterministic regeneration,
  no re-capture).
- The always-on badge stays; NO non-negotiable change.

## Status

Gate closed 2026-06-10 — A1 accept-with-conditions (sample sentences; speed → quality-gated T4),
A2 accept, A3 don't-know→defended→accept, A4 accept. Ledger block appended.
