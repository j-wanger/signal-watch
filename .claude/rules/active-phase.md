# Active Phase Context

Phase: 28 - Corpus COMPLETENESS + grounded-coverage interview + streaming render + branding/compliance (M7). T1–T10 DONE — all 10 tasks [x], gated, ready to commit. Direction approved 2026-06-07; T10 completed 2026-06-07 (committing now).

Why: the user found the CORE defect Phase-27's assessment MISSED — verbatim red-flag EXTRACTION was grossly INCOMPLETE (the grounding gate only checked each flag was REAL, never that we got them ALL; opioid doc shipped 15 of ~80). Plus the user's bigger call: STOP fabricating coverage/data — ground it in a yes/no/PARTIAL interview.

DONE (T1–T9):
- COMPLETE RE-EXTRACTION (the `ph28-complete-sweep` 84-agent workflow): 634 → **903 indicators**, every flag re-grounds; the disasters fixed (terror 13→77, opioids 15→68, human-trafficking 57→98, maritime 7→40); LLM-enumerate + completeness-critic (deterministic bullet-detect too unreliable — glyphs vary per doc; bullet-count is only the oracle). Tail-stop fixed.
- GROUNDED COVERAGE: a **28-capability + 20-data-source taxonomy** (user-approved) → each indicator tagged capability/data_source → the user's 28+20 y/n/partial interview answers → deterministic apply (cap→status, data→availability, cover×data matrix→build_rec). 258 covered / 191 partial / 454 gap; 220 BUILD_NOW · 147 SOURCE_DATA. NO fabrication.
- TEMPLATED build_logic: 28 capability spec-templates → the 220 BUILD_NOW. All 42 `--check-derived` CLEAN; builds 2.41MB.
- corpus.html: T7/T8 render (superseded by the T10 streaming rewrite below).
- BRANDING "FinCEN Corpus Explorer" → "AML Corpus Explorer".

DONE (T10 — the user's browser review surfaced REAL render bugs, fixed before commit per the abort rule):
- STREAMING READ: the T7 phrase-by-phrase render was "staged" (whole text placed up front) + ~48s-hardcoded. Rewrote `renderArticle` to a FULL-MOTION STREAMING read — the source streams in (caret + scroll-follow), each red-flag phrase highlights ONLY as the read reaches its position, its translation extracts alongside, and BOTH labels count UP from 0 (no full count up-front). Length-scaled ~0.9ms/char, capped ~45s. New full-motion harness section (`__drain` + enriched dynEl) drives the path the old harness couldn't see.
- DISPLAY POLISH: `cleanArticle` de-pipes markitdown PIPE-GRID tables (normalize-invariant → grounding/highlight byte-unchanged).
- FINTRAC ATTRIBUTION RELOCATED (user's call — NOT removed): per-doc page FOOTER carries the full © His Majesty… + title + source URL for the FINTRAC doc on screen, empty for US docs. build.py preserves the © clause as `attribution` + surfaces `url`. Verbatim+attribution non-negotiable HELD — no deviation to log.
- BRANDING FIX: build.py brand subtitle "FinCEN Corpus Explorer" was overriding the template at runtime → set to "AML Corpus Explorer".
- DEDUP: the completeness sweep double-extracted 5 docs (terror under 2 parallel section schemes = 24 dupes + 4 singles: tab-soup / newline / prefix-truncation), 28 genuine duplicates removed byte-surgically (json indent=1 round-trip; only dup objects removed) → 903 → **875 indicators**, terror 77→53, zero unique lost, all confirmed vs source mds.
- HARNESS realigned 143/5 → **165/0** (5 expected stale asserts fixed + new streaming/count-up/footer/de-pipe asserts); `--check all` 4/4 ZERO DRIFT; `--selftest` PASS; all 42 `--check-derived` clean. Docs updated (CLAUDE/HANDOFF/README/tasks).

Constraints (held): the grounding core `derive_signals.py` (normalize/rf_region/check_record) BYTE-UNCHANGED — all 875 re-ground through it; showcase + source mds + corpus-status + typology-map FROZEN. Coverage GROUNDED (user interview), not fabricated. NO fabricated numbers.

Gates:
- [x] Direction confirmed by user (complete extraction + interview-grounded coverage + UX/branding/compliance; prove-then-full-sweep; 2026-06-07)
- [x] Delivery accepted (T1–T10 done; streaming render + footer attribution + table polish + dedup reviewed and approved by the user in-session 2026-06-07; committing)
