# Active Phase Context

Phase: 41 — Entity-resolution schema enrichment (live news). Lite. ALL 6 tasks T1–T6 [x] — READY FOR COMPLETION; delivery gate pending (present → commit+push to main → flip post-commit-verify). Spec: specs/phase-41-entity-resolution-schema.md (nana:approved 2026-06-09).

Objective (DELIVERED): the LIVE entity scan enriched for proper ER — aliases[] verbatim-KEPT (DROP→FOLD inversion), properties[] {kind,value} closed vocab (incl. client_number/account_number — private investigation notes a first-class future input), relationships[] {from,to,label,evidence} + main_subject, all grounded-or-stripped by the SHARED gate (labels vocab-checked, never correctness-checked). DuckDB normalized to ANCHORS (anchors + source_type, ONE monolithic property table w/ confidence NULL-reserved, relationship edges); exact-name cross-scan accumulation; screen matches name ∪ aliases (max score). D5: red_flags FIRST in EXTRACT_SCHEMA order (strict-grammar generation order is load-bearing — flags-last cost −12.5%, r2 cleared it).

Scope: scripts/{serve_news,news_ground,news_store}.py · scripts/build.py (shared-gate consequence) · news.html (LIVE region only) · tests/{news_live_test.py,news-stream.test.mjs,fixtures/news-live/**} · docs/news-live.md · tests/smoke-checklist.md · CLAUDE.md.

Key constraints HELD: offline dist/news + 4 committed records + book.json BYTE-FROZEN (--check all 5/5 zero drift); replay goldens regenerated deterministically (old captures default-empty; pinned pre-41 captures byte-clean); PRIVACY boundary (gitignored DuckDB; 127.0.0.1 model; fixtures US-federal-only w/ FIXTURE_META allowlist assert); the always-on badge stays; NO non-negotiable change.

Exit criteria: MET — all selftests + news_live_test (+--live smoke) + node news-stream 103 + corpus 239 green; 3 NEW .ph41 fixtures; docs/smoke-checklist/CLAUDE.md updated. Reviewer 9/10 ACCEPT, zero HIGH+.

Next: delivery gate → commit + push to main (commits-phases-to-main) → flip delivery=accepted → /dev-plan Phase 42 (candidates: anchor dossier view + conflict surfacing · fuzzy-merge adjudication · CLAUDE.md trim · FINTRAC /intel/ · AUSTRAC/UK · negative-news bulk scan).

Gates:
- [x] Direction confirmed by user (assumption gate closed 2026-06-09: A1 reject→A1' accept-with-conditions, A3 reject→A3'a/A3'b accept, A2/A4/A5 accept)
- [ ] Delivery accepted (post-implementation report)
