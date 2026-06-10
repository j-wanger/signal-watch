---
title: "Phase 40: Live red-flag extraction quality (measure-first)"
aliases: []
category: journal
tags: [news, live-mode, red-flags, extraction-quality, measure-first, agreement, prompt, gate, fixtures]
parents: [phase-40-live-redflag-extraction-quality]
created: 2026-06-09
updated: 2026-06-09
source: debrief
duration: unknown
---

# Phase 40: Live red-flag extraction quality — measure-first (M8)

## What Happened
- HEADLINE: the Phase-38 entity playbook applied to FLAGS paid off on HOLDOUT — covR 0.40→0.55, agreement 0.54→0.62, mechCovR 0.46→0.63, and the measured POSITIONAL DECAY was ELIMINATED (second-half miss 0.64→0.43); the federal baseline unregressed (agr 0.73→0.74, covR 0.67→0.69). Budget honored: holdout eval #1 of 2, closed at 1 (user picked path A — freeze the calibration round-2 prompt, spend one eval on it alone, attribution preserved).
- T1 stress corpus: 12 commercial articles (6 cal / 6 hold, 9 domains) + 7 federal, captured LOCAL-ONLY under `.dev-wiki/tmp/ph40/`. DISCOVERY: the negative-news corpus has NO `extraction: full` frontmatter (2,256/2,314 carry no extraction field) — the planned filter field was replaced by the committed `news_fetch.standardize→verify_article` gate + a measured `continue reading < 3` anti-listing rule; selection manifest frozen (still deterministic).
- T2 measure + USER CHECKPOINT: agreement table (federal 0.73 / commercial 0.51–0.54; covR 0.67 fed vs 0.40 com; covQ 0.80–0.86 everywhere) → the residue is RECALL on commercial longreads, precision healthy. 4 clusters (C1 early-stop on long narratives · C2 institutional/control-failure blind spot · C3 over-extraction granularity · C4 latent bounds drift) adjudicated. The user's reference-library REFRAME: covQ measures existence, not extraction quality → registry-based re-measure (category agreement / span tightness / mechanism coverage); T4 = dup-collapse ONLY; T5 precision verify DROPPED (residue was recall) → sectioned-extraction-if-residue.
- T3 context-shape: SYSTEM_PROMPT red_flags contract rewritten — 20-family mechanism-registry checklist (aml-wiki vocabulary) + granularity contract + exemplar register strings from committed records + the 12-200→[12,240] prompt/gate drift fixed TO the gate. THREE calibration rounds: r1 over-merged (covR 0.32), r2 ACCEPTED, r3 REGRESSED (covQ 0.60, drops 3.8/article) → ROLLED BACK to r2. Blind adjudication of r2's 33 reference-unmatched flags: 21 real / 11 marginal / 1 not-a-flag.
- T4 shared-gate dup-collapse: `flag_dup_key` = (normalized quote, normalized category); live `ground_record` DROPs (FIRST survives — input order is the total survivor rule since spans are identical), build `validate_news_data` CHECKs fail-loud, never rewrites. Same-quote-DIFFERENT-category KEPT (one sentence can ground two mechanisms) — both fixture-pinned. The 4 committed records passed CLEAN (no adjudication needed); goldens valid WITHOUT regeneration.
- T5 SKIPPED-WITH-REASON: the delegated trigger (persisting positional decay / coverage lag post-T3) did not fire.
- T6 regate + 3 NEW `.ph40` federal fixtures (ravenell/tgr-group/chinese-cmlo re-captured under the checklist prompt; goldens derived deterministically; variant-tag mapping in the replay test) → 10 total; docs/news-live.md `## Red-flag quality` section; smoke-checklist item; CLAUDE.md in place.

## Decisions Made (impl, recorded here per lite ceremony)
- Holdout path A (freeze r2, one eval, budget closed at 1 of 2) — user call at the pre-holdout checkpoint.
- `flag_dup_key` semantics (quote+category; first-survives; live DROP vs build CHECK; different-category kept).
- Calibration r3 rolled back on measured regression — 3 rounds total, r2 shipped.

## Problems Solved
- Phantom selection filter (`extraction: full` doesn't exist) — rebuilt deterministically on the committed verifier + a measured anti-listing rule.
- covQ under-credited newly-in-scope institutional flags — resolved by blind validity judging of unmatched flags + the registry-scoring reframe, not by trusting the raw proxy (raw covQ 0.85→0.73 breached the −0.05 guard; reported WITH the adjudicated interpretation, user-visible).

## Open Questions
- Semantic instance-dups (reworded retellings of one behaviour; 15/33 in calibration adjudication) — candidate: a batched keep-biased flag-merge pass OR the next prompt iteration.
- Marginal-quote modes: quotes lifted from DENIAL statements as evidence + occasional mechanism mislabels — candidate prompt micro-rule ("never quote a denial/rebuttal as evidence").
- catAgr is noisy (free-text reference categories vs checklist families) — a registry-aligned second-rater would sharpen category agreement next time.

## Escape Hatches
- DISCOVERY: the `extraction: full` frontmatter filter didn't exist (above).
- DISCOVERY/USER-ENVIRONMENT: `~/.claude/enforce` appeared mid-phase (enforce-spec + enforce-memory hooks) — satisfied honestly via `/spec --internal` (adversarial constraints + Tier-1 review → `specs/phase-40-live-redflag-quality.md`, nana:approved) + a genuine memory recall pass. NOTE: `.claude/.memory-consulted` is an untracked session marker — must NOT be committed.

## Artifacts Changed
- `scripts/news_ground.py` (NEW `flag_dup_key` + dup-collapse in `ground_record`) · `scripts/build.py` (`validate_news_data` dup CHECK) · `scripts/serve_news.py` (SYSTEM_PROMPT red_flags contract) · `tests/news_live_test.py` (planted-dup CANNED case + `.ph40` variant mapping) · `tests/fixtures/news-live/` (7→10) · `docs/news-live.md` · `tests/smoke-checklist.md` · `CLAUDE.md` (in place) · `specs/phase-40-live-redflag-quality.md` (NEW). NO client/news.html change; all 5 dists byte-identical.

## Health Delta
- ALL GREEN: news_ground (+2 flag fixtures) / serve_news / news_fetch / derive_signals / news_store selftests · news_live_test (system + .venv + `--live` real-Qwen smoke) · node news-stream 90 + corpus · `--check all` 5/5 ZERO DRIFT · slug-leak grep 0 · remeasure.json assertion PASS (holdout_evals=1, cov_of_ref 0.545 ≥ 0.40).

## Soft Observations / Phase N+1 Candidates
- Semantic instance-dup residue | batched keep-biased flag-merge pass OR next prompt iteration | evidence: `.dev-wiki/tmp/ph40/cal2-unmatched-judged.json` (15/33 instance_dup).
- Denial-quote + mechanism-mislabel marginals | one prompt micro-rule | evidence: blind-judge notes.
- CLAUDE.md now 279 lines (target ~200) — the carried trim candidate is more pressing.
- Global enforce hooks now active (`~/.claude/enforce`) — future phases need an approved spec BEFORE implementation edits | consider folding `/spec --internal` into this project's lite dev-plan flow.
- The registry-scoring upgrade (category agreement / span tightness / mechanism coverage) lives in gitignored scratch | if flag-quality measurement recurs it deserves a committed harness.

### Gate Compliance
- Direction gate: approved via the assumption gate 2026-06-09 (A1/A2 round 1; A3/A4 reject→revised→accept round 2; all_accept: false).
- Delivery gate: PENDING at debrief time — flips post-commit per delivery-flow D3.
- Assumption revisit: A1 HELD (prompt-shaping closed the gap on holdout; the recall/precision frontier took 3 rounds) · A2 HELD-with-deviation (corpus usable; the filter field didn't exist — rebuilt on the committed verifier, still deterministic) · A3 HELD (the blind second-rater design produced the decisive signal incl. the covQ-undercredits finding) · A4 HELD (gate unfroze cleanly — committed records passed, goldens valid without regeneration, zero drift). No `bit` this phase — no confidence review indicated.

## Related
- [[phase-40-live-redflag-extraction-quality|Phase 40: Live red-flag extraction quality]] — parent phase
