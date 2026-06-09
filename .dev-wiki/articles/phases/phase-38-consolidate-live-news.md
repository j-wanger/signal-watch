---
title: "Phase 38: Consolidate the live news subsystem (verify agent backend + watchlist management)"
aliases: []
category: phases
tags: [news, live, m8, agent-backend, qwen, grounding, fixtures, watchlist, prune, inter-rater-agreement, claude-reference, offline-strip]
parents: []
created: 2026-06-08
updated: 2026-06-08
source: plan
status: completed
scope: ["tests/fixtures/news-live/**", ".dev-wiki/tmp/**", "tests/news_live_test.py", "scripts/news_store.py", "scripts/serve_news.py", "news.html", "dist/news/index.html", "tests/news-stream.test.mjs", "docs/news-live.md", "tests/smoke-checklist.md", "CLAUDE.md", ".claude/rules/active-phase.md"]
entry_criteria: "Phase 37 DELIVERED + accepted + committed 798fe28 + pushed to main. The Phase-35/36 LIVE news subsystem exists (companion-served serve_news.py + news_store.py + news_ground.py, dev/authoring-time only) but the agent backend was never exercised against a real model (call_llm stubbed with a CANNED dict) and the escalated-only watchlist has no view/prune UI (it only grows). The Qwen model (Qwen3.6-35B-A3B, llama.cpp) is now LIVE on 127.0.0.1:8080; a planning smoke confirmed the backend end-to-end (4 entities + 5 grounded flags, the gate dropped a 6th ungrounded). The user chose at the dev-plan gate to CONSOLIDATE this subsystem over extending source scale."
exit_criteria: "The live agent backend is verified against the real Qwen with committed raw-output fixtures + offline replay tests (parse→build→ground, dep-free) pinning the model's contract incl. the ungrounded-elision drop; a Qwen-vs-Claude agreement+divergence finding is reported as INTER-RATER AGREEMENT (consensus, NO accuracy number; the always-on badge stays); an opt-in --live smoke hits 8080 OFF the default run; the watchlist-management VIEW (escalated surface + provenance) with a PRUNE control lands in the live region (store prune method + serve_news route + news.html panel); the OFFLINE dist/news stays byte-identical; --check all zero drift; node news + corpus harnesses + news_live_test + news_ground/serve_news/news_store --selftest green; build.py never imports the live/store layer; NO non-negotiable change."
---

# Phase 38: Consolidate the live news subsystem (verify agent backend + watchlist management)

## Objective

CONSOLIDATE the Phase-35/36 LIVE news subsystem (companion-served, dev/authoring-time only) — the
user's choice at the dev-plan gate over extending source scale (FINTRAC /intel/ depth or a third
jurisdiction, both DEFERRED). Two halves, BOTH companion-only; the OFFLINE `dist/news` stays
BYTE-FROZEN (the live + watchlist-view code lives in the build-time-STRIPPED
`/*LIVE_START*/…/*LIVE_END*/` region; build.py NEVER imports the live/store layer
(`serve_news`/`news_store`) — it DOES import `news_ground`, the SHARED stdlib grounding primitives, by
design so live grounding == build grounding). **Half A** verifies + locks the agent backend (the
centerpiece). **Half B** completes
the Phase-36 feedback loop with a watchlist-management VIEW + prune.

## The new fact that reframes the phase

The Qwen model (Qwen3.6-35B-A3B, llama.cpp, OpenAI-compatible) is LIVE on 127.0.0.1:8080, and a
planning smoke already confirmed the live backend works end-to-end: one committed article → 4 entities
+ 5 grounded red flags in 17.6s, with the deterministic grounding gate correctly DROPPING a 6th
ungrounded (ellipsis) flag. So this is a **CAPTURE-AND-LOCK** phase, not a fix-broken-backend phase.

## Half A — verify + lock the agent backend (the user's stated intent)

`call_llm` (the model step) is the ONLY thing the test suite currently stubs (a hand-written CANNED
dict); everything downstream (`parse_llm_json` → `build_record` → ground) is already covered. So: run
the real Qwen over the committed DOJ/OFAC articles, CAPTURE each RAW model output as a committed fixture
under `tests/fixtures/news-live/`, add OFFLINE replay tests (parse→build→ground over the fixtures,
dep-free, no model) that pin the real model's output contract including the ungrounded-elision drop,
and add an OPT-IN `--live` smoke that actually hits 8080 but is OFF the default offline run (the same
pattern as the `.venv`-gated DuckDB tests).

**Evaluation is two-layer + honesty-constrained:** (1) deterministic GROUNDING = faithfulness
(automatic; catches hallucination). (2) a CLAUDE-REFERENCE comparison = quality
(completeness/correctness) — Claude extracts the same articles → a reference (grounded by the SAME
gate) → report Qwen-vs-Claude as INTER-RATER AGREEMENT (consensus, NEVER Claude-as-ground-truth) + the
actual divergences, for the user to adjudicate. NO accuracy/precision/recall number presented as real;
the always-on "Illustrative data & outputs" badge stays. This mirrors the Phase 34/37
agreement-as-consensus + human-adjudication method. **Grounding gate ≠ completeness gate ≠ correctness
gate.**

## Half B — watchlist-management view + prune (completes the Phase-36 loop)

The escalated-only feedback loop is currently invisible: the watchlist only GROWS, `GET /watchlist`
serves it but there is no view/prune UI. Add a `news_store` prune/un-escalate method, a `serve_news`
prune route, and a `news.html` LIVE-REGION watchlist panel (view the escalated surface with provenance
+ a prune control). Stripped from offline; `dist/news` byte-identical.

## Scope

Files and modules affected:
- `tests/fixtures/news-live/**` — committed raw Qwen output (`<article>.qwen.json`) + grounded golden
  (`<article>.golden.json`) per committed article (a planning-session smoke already seeded all 4; T1
  verifies/completes coverage).
- `tests/news_live_test.py` — fixture-replay tests + the opt-in `--live` smoke (capture helper in T1).
- `scripts/news_store.py` — a prune/un-escalate method (+ extended `--selftest`).
- `scripts/serve_news.py` — a companion-only prune route.
- `news.html` (live region only) + `dist/news/index.html` (rebuilt, byte-identical via the strip).
- `tests/news-stream.test.mjs` — the offline book-only strip assertion holds.
- `.dev-wiki/tmp/**` — the T1 verify + agreement artifacts (intermediate, non-ship).
- `docs/news-live.md`, `tests/smoke-checklist.md`, `CLAUDE.md` (in-place `## Current state` edit),
  `.claude/rules/active-phase.md`.

## Exit Criteria

- [ ] The live agent backend is verified against the real Qwen; committed raw-output fixtures under
      `tests/fixtures/news-live/` + offline replay tests (parse→build→ground, dep-free) pin the model's
      contract incl. the ungrounded-elision drop
- [ ] A Qwen-vs-Claude agreement+divergence finding is reported as INTER-RATER AGREEMENT (consensus, NO
      accuracy/precision/recall number; the always-on badge stays)
- [ ] An opt-in `--live` smoke hits 127.0.0.1:8080 OFF the default offline run; `python3
      tests/news_live_test.py` green offline
- [ ] The watchlist-management VIEW (escalated surface + provenance) with a PRUNE control lands in the
      live region: a `news_store` prune method + a `serve_news` route + a `news.html` panel
- [ ] The OFFLINE `dist/news` stays byte-identical (`--check news` zero drift, screens the static book
      only); build.py never imports the live/store layer
- [ ] `--check all` zero drift; node news + corpus harnesses + news_live_test + news_ground/serve_news/
      news_store `--selftest` green; NO non-negotiable change

## Constraints

- OFFLINE-STRIP non-negotiable: ALL new live + watchlist-view code lives inside
  `/*LIVE_START*/…/*LIVE_END*/` so `render_news` strips it → `dist/news` byte-identical, zero
  network/store code offline. The static offline page screens the synthetic book ONLY.
- build.py NEVER imports the AUTHORING layer or the LIVE/STORE layer (`serve_news`/`news_store` stay
  companion-only; the no-store-on-the-ship-path invariant holds). It DOES import `news_ground` — the
  SHARED stdlib grounding primitives, by design, so live grounding == build grounding.
- AGREEMENT-HONEST evaluation (the Phase-34/37 guard): the Claude reference is a SECOND rater, NOT
  ground truth — Qwen-vs-Claude is reported as INTER-RATER AGREEMENT + the divergences for the USER to
  adjudicate. NO accuracy/precision/recall number presented as real; the always-on "Illustrative data
  & outputs" badge stays. Grounding gate ≠ completeness gate ≠ correctness gate.
- The deterministic grounding gate is the FAITHFULNESS backstop — do NOT loosen it to make a fixture
  pass; an ungrounded item DROPS (the smoke's ellipsis-flag drop is the contract to pin).

## Checkpoints

- After T1 (the verify + capture): CHECKPOINT the Qwen-vs-Claude agreement + divergence findings to the
  user (the accepted adjudicator) before locking the goldens.
- If the live backend regresses against the real Qwen → STOP + report (the gate is the backstop; do NOT
  loosen it).
- If `dist/news` can't stay byte-identical after the strip → surface it (behavior-identical + recommit
  + harness green is the floor).

## Assumptions

- The Qwen server (127.0.0.1:8080) stays reachable during T1 capture. If it goes down mid-capture:
  capture what's available, mark the gap, the offline replay still locks the captured contract.
- The committed DOJ/OFAC articles are the right verification surface (they ARE the live `/extract`
  inputs). If a committed article is too short to exercise the gate's drop path, note it; the smoke
  already proved the drop on the real corpus.
- A captured raw output drives a DETERMINISTIC offline replay (parse→build→ground is pure given fixed
  input). If false: re-confirm the recorded-fixture approach vs the hand-written CANNED stub.

## Notes

- This is the project's first VERIFICATION of the live agent backend against a real model — Phase 35/36
  shipped it stubbed (call_llm CANNED); the carried caveat ("real call_llm vs an actual llama-cpp server
  UNVERIFIED") is exactly what Half A closes.
- The fixture-replay pattern generalizes the existing CANNED-stub: instead of a hand-written dict, the
  stub is driven by REAL captured model output — a stronger contract, still offline/dep-free.
- Half B makes the Phase-36 human Disposition gate fully reversible (escalate grows the surface; prune
  shrinks it) — the loop is now bidirectional and inspectable.
- DEFERRED at this gate (for a future /dev-plan): the derivable FINTRAC /intel/ frontier (OA001 +
  sanctions-evasion SB + Russia-linked-ML SB + dual-use advisory) · a third jurisdiction (AUSTRAC CC BY
  / UK OGL — the standing scale frontier now the Canadian source frontier is exhausted).
