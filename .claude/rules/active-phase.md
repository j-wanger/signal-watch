# Active Phase Context

Phase: 14 - Scale corpus derivation (3 more CLEAN advisories → 5/14 live) — M7 — DELIVERED, awaiting commit verification.
(all 5 tasks [x], exit criteria MET, 2026-06-05). No next phase planned — run /dev-plan for Phase 15.
Objective: fill the corpus explorer's live menu 2/14 → 5/14 by authoring 3 more derived records — pure authoring, zero engine/spine/front-end edits.

Delivered (verified in tree): 3 new --check-derived-clean records — fin-2020-a008 human trafficking (10 ind, pruned 1 intro-tail noise line, 2 BUILD_NOW) ·
fin-2025-a003 Chinese MLN (17 ind, clean, 5 BUILD_NOW — most buildable) · fin-2025-a002 Iran (16 ind, validate-first passed/no swap, 4 BUILD_NOW · 7 BUILD_ENRICH —
enrichment-hungry contrast). Authored via a matrix-merge script (verbatim flag text + src_line preserved, build_rec auto-derived from build_rec_category).
dist/corpus rebuilt → 5/14 live (each new record renders coverage→build-rec→signal through all 4 screens); README + CLAUDE bumped 2/14→5/14.
Verified: 3× --check-derived · build.py --check all 4-artifact ZERO DRIFT · headless render assertions · node --check · --selftest 12+12.
BYTE-FROZEN: index.html, corpus.html, config/**, scripts/**, dist/{fentanyl,trade-based,elder-financial-exploitation}/ (git diff empty).

Findings (Phase 15): (1) extractor missed a real 18th flag at fin-2025-a003 md L499 — glued to a page-break running-header after a footnote block (same class
as the 3 LOW glued lists); (2) pre-existing fin-2022-a001 record stores `&gt;= 2` → double-escapes under corpus.html esc() on a shipped record (store RAW text).
Carried Phase-15 candidates: remaining CLEAN (EFE corpus record, COVID EIP) + 2 glued NEEDS after the extractor fix · FATF non-derivable labeling · corpus
combination-lift wow beat · elder true-up · fentanyl re-point · --fetch cadence.

Gates:
- [x] Direction confirmed by user (scale derivation; 3 advisories — trafficking/CMLN/Iran; EFE+COVID out — 2026-06-05)
- [ ] Delivery accepted (post-implementation report)
