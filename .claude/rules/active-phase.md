# Active Phase Context

Phase: 43 — Live pipeline robustness + progressive presentation (live news). Lite. 5/5 tasks [x] — READY FOR COMPLETION; delivery gate pending. Spec specs/phase-43-live-pipeline-robustness.md nana:approved 2026-06-10 (precondition satisfied).

Objective (DELIVERED): the user's reframe — a REAL-note live test timed out ~200s with NO intermediate feedback. T1 stress harness REPRODUCED + NAMED it: primary OUTPUT-BUDGET (≈400–450 generated tokens/entity; 4096 truncated at ~10+ entities; discarded finish_reason → opaque parse error), secondary READ-TIMEOUT; context overflow unreachable (n_ctx=262144); intrinsic degradation REFUTED. T2 call_llm STREAMS (SSE, idle-gap 120s, budget 16384, length/stall NAMED in-stream; SAME signature → 13/13 replay green, ZERO re-capture). T3 stage-completion LIVE rendering (grounded flags FINAL + provisional chips refined through verify + token counter; NO token stream; grounded reveal 18s live). T4 preflight n_ctx honest refusal (FAIL-OPEN) + /extract single-flight 409 + disconnect-persists-nothing; sectioned extraction NOT earned. T5 full regate + docs.

Scope (held): scripts/serve_news.py (call_llm transport + stage events + pre-flight ONLY) · news.html (LIVE region only) · tests/{news_live_test.py,news-stream.test.mjs} · .dev-wiki/tmp/ph43_stress.py (LOCAL scratch) · docs/news-live.md · tests/smoke-checklist.md · CLAUDE.md · specs/.

Key constraints HELD: D2 measure-first. D3 stage-completion rendering — NO partial-JSON parsing, NO token stream; flags GROUNDED, entities provisional. D4 pure transport — news_ground/SYSTEM_PROMPT/EXTRACT_SCHEMA/store-writes/fixtures FROZEN (reviewer git-diff-verified); call_llm signature preserved; offline dist/news byte-identical. D5 privacy — real note NEVER committed; stress notes SYNTHETIC; commercial captures LOCAL-ONLY; fixtures US-federal-only. Always-on badge stays; NO non-negotiable change.

Exit criteria: ALL MET — failure class reproduced + named + fixed-or-failing-HONESTLY in-stream; long probe survived >180s (XL 193s); 13/13 fixtures green w/o re-capture; staged reveal in the LIVE region; --check all 5/5 zero drift; news-stream 130→140 + corpus 239 + all selftests + news_live_test (system/.venv/--live incl. the long-note probe) green; docs/smoke/CLAUDE.md updated in place. Reviewer 9/10 ACCEPT (1 HIGH extract_lock leak fixed inline). Assumption revisit: A1/A2'/A3/A4 ALL held.

Next action: DELIVERY GATE — present the post-implementation report; on acceptance commit to main (phase-work commit, then the gate-log flip in its OWN post-commit-verify commit) and push.

Abort rule (stood down — phase complete): blocked >3 attempts → ask skip or abort.

Gates:
- [x] Direction confirmed by user (assumption gate closed 2026-06-10: A1/A3/A4 accept, A2 reject-by-reframe→A2' accept)
- [x] Delivery accepted (post-implementation report 2026-06-10; commit fba2bb0 verified)
