---
title: "Phase 40: Live red-flag extraction quality (measure-first)"
aliases: [phase-40]
category: phases
tags: [news, live-mode, extraction-quality, prompt, few-shot, measure-first, red-flags, agreement, gate]
parents: [phase-39-live-news-qol]
created: 2026-06-09
updated: 2026-06-09
source: plan
status: ready-for-completion
scope: ["scripts/serve_news.py", "scripts/news_ground.py", "scripts/build.py", "tests/news_live_test.py", "tests/fixtures/news-live/**", "docs/news-live.md", "tests/smoke-checklist.md", "CLAUDE.md", ".dev-wiki/tmp/**", "data/news/.live/**"]
entry_criteria: "Phase 39 delivered + accepted + committed 3786042/3c35902 + pushed; the live companion has streamed progress + one-shot URL acquisition; flags pass the deterministic grounding gate but completeness/span-quality/translation/consistency are unguarded."
exit_criteria: "Measured characterization (proxies + blind second-rater agreement, consensus-honest) user-adjudicated at the T2 checkpoint; SYSTEM_PROMPT context-shaped with holdout holding; measurement-earned checks in the shared news_ground gate with the 4 committed records passing; conditional batched per-flag verify only on measured residue; fixtures green without re-capture + new US-federal fixtures; --check all 5/5; badge stays; no non-negotiable change."
---

# Phase 40: Live red-flag extraction quality (measure-first)

## Objective

Improve LIVE red-flag extraction quality in the news live companion — the Phase-38 entity
playbook applied to FLAGS: measure → context-shape → gate-harden → verify-only-if-residue,
with a human checkpoint between measure and fix. Flags pass the deterministic
faithfulness/grounding gate but have NO structured prompt guidance and NO second pass —
completeness, span quality, translation register, and consistency are unguarded, and the
user sees inconsistent flags in real live tests.

Gate record: direction user-set at the Phase 39 delivery gate; the assumption gate closed
2026-06-09 — A1/A2 accepted round 1; **A3 and A4 were REJECTED round 1, revised, and
accepted round 2** (A3' = blind second-rater agreement instead of proxies-only; A4' =
news_ground.py UNFREEZES for measurement-earned shared-gate checks). Ledger block appended
to `.dev-wiki/assumption-ledger.md`. Decisions D1–D5 in `_CURRENT_STATE.md` (lite).

Method anchors:
- Measurement = deterministic proxies (flag count, span lengths, near-dup rate,
  grounded-drop rate, register shape) + a BLIND second-rater reference extraction →
  per-dimension INTER-RATER AGREEMENT (completeness/span/register), reported as CONSENSUS,
  never ground truth; NO accuracy number presented as real (Phase 34/38 D2 method).
  rf_region does NOT transfer to news (no enumerated red-flag list) — completeness has no
  deterministic anchor; that's why second-rater agreement.
- Prompt = few-shot exemplars from the COMMITTED gate-passing records (anchor-style-to-
  the-reference) + aml-wiki money-laundering-red-flags mechanism vocabulary; fix the
  12-200→[12,240] prompt/gate drift (prompt moves TO the gate); calibration/holdout split
  guards the Phase-38 overfit trap.
- Stress corpus = ~12 commercial articles from the negative-news wiki (2,313 raw files;
  deterministic frontmatter filter: extraction full + source_score floor) + the 7 committed
  federal fixture articles as baseline; captured commercial outputs LOCAL-ONLY/never
  committed; fixture promotion US-federal-only (Phase-39 compliance posture).

## Scope

- `scripts/serve_news.py` — SYSTEM_PROMPT context shaping (T3); conditional BATCHED
  keep-biased per-flag verify (T5, only on measured residue; `--no-verify-flags`)
- `scripts/news_ground.py` + `scripts/build.py` — measurement-earned deterministic
  flag-quality checks in the SHARED gate (T4)
- `tests/news_live_test.py`, `tests/fixtures/news-live/**` — harness; goldens regenerated
  deterministically from pinned qwen.json; NEW US-federal fixtures (T6)
- `docs/news-live.md`, `tests/smoke-checklist.md`, `CLAUDE.md` (in-place) — docs (T6)
- `.dev-wiki/tmp/**`, `data/news/.live/**` — local-only measurement artifacts (T1/T2)
- NO client/news.html change; dists stay byte-identical (Python-side only); NO
  non-negotiable change.

## Exit Criteria

- [ ] T2 measurement presented (agreement table + divergence clusters) and user-adjudicated
      at the checkpoint (residue call + which checks earn gate status recorded)
- [ ] SYSTEM_PROMPT context-shaped; HOLDOUT (not just calibration) improves or holds;
      prompt/gate char-bound drift reconciled to [12,240]
- [ ] Measurement-earned flag-quality checks in shared `news_ground.py`; the 4 committed
      news records pass the extended gate (failures adjudicated, never loosened);
      `news_ground --selftest` extended + PASS
- [ ] Conditional batched per-flag verify built only on measured residue (skipped-with-
      reason otherwise); stubbed-model test green
- [ ] Replay fixtures green WITHOUT re-capture; NEW captured US-federal fixtures replay
      green; `python3 tests/news_live_test.py` PASS
- [ ] `python3 scripts/build.py --check all` 5/5 zero drift; node news-stream + corpus
      harnesses green; all `--selftest`s green
- [ ] Captured commercial outputs local-only/never committed; always-on badge stays;
      NO non-negotiable change

## Notes

Knowledge gaps carried to implementation: few-shot exemplar budget/granularity for
Qwen3.6-35B-A3B (resolve empirically at T3); no prior art on news red-flag completeness
measurement without an enumerated source list — the blind second-rater design is the
answer adopted.
