# Active Phase Context

Phase: 42 — Anchor dossier view + per-scan network visualizer (live news). Lite. ALL 6 tasks T1–T6 [x] — READY FOR COMPLETION; delivery gate pending (present → commit+push to main → flip post-commit-verify). Spec: specs/phase-42-anchor-dossier-network-view.md (nana:approved 2026-06-10).

Objective (DELIVERED): CONSUME the Phase-41 ER model — GET /anchor read route (400/503/404/200, name-keyed) wrapping the previously-unconsumed anchor_summary(); deterministic SVG network visualizer at Disposition (liveGraphLayout radial+relaxation, esc() everywhere, edge evidence closed-until-clicked); anchor dossier panel (scans w/ source-type provenance, properties by kind, conflicts "both kept" presentation-only, honest 404/store-off/empty, watchlist wdoss); committed SYNTHETIC note docs/demo-investigation-note.md + the documented accumulation demo (live checkpoint confirmed: 2 scans, client_number, phone conflict both-kept).

Scope: scripts/serve_news.py (/anchor route) · news.html (LIVE region only) · tests/{news_live_test.py,news-stream.test.mjs} · docs/{demo-investigation-note.md,news-live.md} · tests/smoke-checklist.md · CLAUDE.md (T5 snapshot + T6 trim).

Key constraints HELD: --check all 5/5 zero drift (offline dist/news + 4 committed records + book.json byte-frozen); PURE CONSUMPTION (news_ground/EXTRACT_SCHEMA/SYSTEM_PROMPT/store-writes/replay-fixtures untouched — reviewer git-diff-verified); privacy held (seeded store local/gitignored; note SYNTHETIC-labeled); CLAUDE.md trim 319→220 w/ non-negotiables/honesty/conventions diff-clean; the always-on badge stays; NO non-negotiable change.

Exit criteria: MET — all selftests + news_live_test (+--live real-Qwen smoke) + node news-stream 130 + corpus 239 green; docs/smoke-checklist/CLAUDE.md updated. Reviewer 9/10 ACCEPT, zero HIGH+.

Next: delivery gate → commit + push to main (commits-phases-to-main; TWO commits — phase work w/ post-T5 CLAUDE.md, then the trim) → flip delivery=accepted → /dev-plan Phase 43 (candidates: fuzzy-merge adjudication · negative-news bulk scan · FINTRAC /intel/ · AUSTRAC/UK · living-doc hygiene).

Gates:
- [x] Direction confirmed by user (assumption gate closed 2026-06-10: A1/A3 accept, A2→A2' accept after evidence-refuted round 1, A4 accept-with-condition, A5 scope constraint)
- [ ] Delivery accepted
