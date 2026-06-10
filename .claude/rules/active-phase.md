# Active Phase Context

Phase: 44 — Live extraction quality: targeted harness, classified fixes, processing page (live news). Lite. 7/7 tasks [x] (T4 = honest skip-with-reason) — READY FOR COMPLETION; delivery gate pending. Spec specs/phase-44-live-extraction-quality.md nana:approved 2026-06-10 (precondition satisfied).

Objective (DELIVERED): both reported failures REPRODUCED + CLASSIFIED + fixed per class. Flag misses = GATE-DROP (raw-substring grounding broken by hard line-wraps / `*`-strip asymmetry / title-line quotes; NOT model recall) → news_ground.locate_span wrap-tolerant REQUOTE to body bytes (the user's seeded STR note 3 drops→0; 13/13 replay green WITHOUT golden regeneration). Alias misassignment = deterministic fold misparent (order-dependent + type-blind) → AMBIGUITY-REFUSAL + TYPE-MATCH (Phase-41 upsides unregressed; P1c wrong-owner model alias = measured-not-gated residual). NEW committed quality harness tests/news_quality_harness.py + quality-baseline.json (17 fixtures, 5 dimensions incl. alias-OWNERSHIP; --check fails on regression) = THE gate for future prompt/gate/model changes. T4 speed = measured honest skip (hotspot = model generation 92–98% of wall; levers named). T5 in-page processing takeover #liveproc (Esc arm→abandon; 409/stream-error/abort NAMED). T6 hygiene archival lossless (tasks.md 755→61 · state 111→89 · architecture 163→94).

Scope (held): tests/news_quality_harness.py · scripts/{news_ground,serve_news}.py · news.html (LIVE region only) · tests/{news_live_test.py,news-stream.test.mjs,fixtures/news-live/} · .dev-wiki/tmp/ph44* (LOCAL gitignored) · .dev-wiki/{tasks,_CURRENT_STATE,_ARCHITECTURE}.md + archive articles (T6) · docs/news-live.md · tests/smoke-checklist.md · CLAUDE.md · specs/.

Key constraints HELD: D2 measure/classify-first. D3 known seams — ZERO re-capture, goldens not regenerated, 4 committed records pass, NO EXTRACT_SCHEMA change. D4 quality-gated speed (honest skip). D5 LIVE-region-only UI + lossless hygiene; PRIVACY — the user's sample sentences local-only gitignored (reviewer-verified zero tracked hits); fixtures US-federal-only. Always-on badge stays; NO non-negotiable change.

Exit criteria: ALL MET — both classes reproduced + classified + fixed; harness committed; --check all 5/5 zero drift; corpus 239 + news-stream 140→150 + all selftests + news_live_test (system/.venv/--live incl. wire-note probe) green; 13/13 replay no re-capture; harness --check OK vs the committed baseline; docs/smoke/CLAUDE.md updated in place. Reviewer 9/10 ACCEPT, zero HIGH+ (2 staleness MEDIUMs fixed by the debrief; CLAUDE.md trim carried). Assumption revisit: A1–A4 ALL held.

Next action: DELIVERY GATE — present the post-implementation report; on acceptance commit to main (phase-work commit, then the gate-log flip in its OWN post-commit-verify commit) and push.

Abort rule (stood down — phase complete): blocked >3 attempts → ask skip or abort.

Gates:
- [x] Direction confirmed by user (assumption gate closed 2026-06-10: A1 accept-w/-conditions, A2 accept, A3 don't-know→defended→accept, A4 accept)
- [ ] Delivery accepted (post-implementation report)
