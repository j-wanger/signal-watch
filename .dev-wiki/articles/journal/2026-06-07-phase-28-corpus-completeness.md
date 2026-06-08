---
type: journal
date: 2026-06-07
phase: 28
slug: 2026-06-07-phase-28-corpus-completeness
tags: [corpus, completeness, interview, grounded-coverage, taxonomy, capability, re-extraction, streaming-render, dedup, branding, attribution, M7]
title: "Phase 28 — Corpus COMPLETENESS + grounded-coverage interview + streaming render + branding/compliance (M7)"
aliases: []
category: journal
parents: [phase-28-corpus-completeness]
created: 2026-06-07
updated: 2026-06-07
source: debrief
duration: ~full session (multi-stage; post-compaction estimate)
---

# Phase 28 — Corpus COMPLETENESS + grounded-coverage interview + streaming render + branding/compliance (M7)

> COMPLETE — all tasks T1–T10 [x]; delivery accepted in-session; committed `24e4a08` (875 indicators, streaming read). This entry supersedes the mid-phase WIP checkpoint.

## What Happened
- The user reviewed the BUILT Phase-27 corpus and found the CORE defect Phase-27's 44-agent assessment MISSED: verbatim red-flag EXTRACTION was grossly INCOMPLETE — the grounding gate only ever verified each extracted flag was REAL, never that we got them ALL. PROOF (the user's spot-check): fintrac-synthetic-opioids enumerates ~80 bulleted indicators; we shipped 15 (~19%). A grounding gate is not a completeness gate — audit recall, not just faithfulness.
- The user's bigger call: STOP fabricating per-indicator coverage/data — ground it in a structured yes/no/PARTIAL interview reflecting the institution's real posture.
- T1–T9 landed the data foundation + UX/branding on disk (the WIP checkpoint). T10 — scoped as "regate + docs" — EXPANDED under the phase abort rule when the user's browser review surfaced real render bugs and a data-quality bug; those were fixed before the commit, then the phase shipped.

## What Shipped
- **COMPLETE RE-EXTRACTION** (`ph28-complete-sweep`, 84 agents: 42 extract → 42 completeness-critic). 634 → 903 indicators; the disasters fixed (terror 13→77, opioids 15→68, human-trafficking 57→98, maritime 7→40). Deterministic bullet-detect proved UNRELIABLE (glyphs vary per doc //•-; FinCEN has none) → LLM-enumerate is the path, bullet-count the completeness ORACLE. Tail-stop fixed; every flag re-grounds through the BYTE-UNCHANGED gate.
- **GROUNDED COVERAGE** — a 28-capability + 20-data-source taxonomy (user-approved, `ph28-derive-taxonomy`) → each indicator tagged capability + data_source → the user's 28+20 y/n/partial interview answers → deterministic apply (cap→status, data→availability, cover×data matrix→build_rec). 258 covered / 191 partial / 454 gap; 220 BUILD_NOW · 147 SOURCE_DATA. Coverage moved FABRICATED → GROUNDED — the institution's real self-assessment. NO fabrication.
- **TEMPLATED build_logic** — 28 capability spec-templates (showcase 7-key shape) attached to the 220 BUILD_NOW by capability (the capability IS the signal type).
- **STREAMING "agent reading" RENDER** (T10, the user's review reframe) — the Phase-27/T7 phrase-by-phrase render was judged "staged" (whole text placed up front) + ~48s-hardcoded. Rewrote `renderArticle` to STREAM the source in (caret + scroll-follow); each phrase highlights ONLY as the read reaches it; translation extracts alongside; both labels (`#doclabel`, the new `#xlabel`) count UP from 0. Length-scaled ~0.9ms/char, cap relaxed to ~45s for long docs. `highlightArticle` now returns char-position spans (not order) so a segment-based stream can fire each highlight at the read edge.
- **DEDUP** — the completeness sweep DOUBLE-EXTRACTED 5 docs (terror under two parallel section schemes = 24 near-dupes + 4 single artifacts: tab-soup / newline / prefix-truncation). All 28 confirmed genuine duplicates vs the source mds (zero unique lost), removed byte-surgically (json indent=1 round-trip). 903 → 875 indicators; terror 77 → 53.
- **DE-PIPED TABLES** — `cleanArticle` now drops markitdown PIPE-GRID rule rows + de-pipes data rows + strips stray #/** (worst: fin-2021-a004 ransomware figure). normalize-INVARIANT → grounding + highlighting byte-unchanged.
- **BRANDING** — "FinCEN Corpus Explorer" → "AML Corpus Explorer" (build.py's injected brand subtitle was OVERRIDING the template at runtime — T9 only renamed the template, so the build.py subtitle was the real fix).
- **FINTRAC ATTRIBUTION RELOCATED** (NOT removed) — the user reversed T9's "attribution removed" posture: the on-screen Source LABEL carries the document title only, while the full Crown-copyright attribution (© His Majesty… + complete title + source URL) renders in a per-doc page FOOTER (`#attribution` slot + `updateAttribution()`), EMPTY for US public-domain docs (a static © line would misattribute US federal works to the Crown → must be per-doc). build.py preserves the © clause as an `attribution` field + surfaces `url`. NET: the verbatim+attribution non-negotiable is HELD (attribution present, relocated) — NO compliance deviation.

## Decisions Made
- (lite — recorded in _CURRENT_STATE Recent Decisions) Streaming "agent reading" read REPLACES the staged phrase-by-phrase render (presenter-believable processing over a staged paint; the user relaxed the cap to ~45s for long docs).
- (lite) FINTRAC attribution RELOCATED to a per-doc page footer, NOT removed (reverses T9; the non-negotiable HELD — no compliance deviation; wording updated to the footer posture in CLAUDE.md + HANDOFF.md).
- (lite) Dedup terror + audit the 4 singles — the "terror highlight 68%" was a DATA bug (double-extraction), not a render bug; 28 genuine dupes removed, zero unique lost.
- (lite) `cleanArticle` de-pipes markitdown PIPE-GRID tables (display-only, normalize-invariant).
- (lite) "FinCEN→AML Corpus Explorer" branding — build.py's injected subtitle was overriding the template at runtime.

## Problems Solved
- The "terror highlight 68%" the review reported looked like a render bug — diagnosed as a DATA bug (double-extraction under two section schemes); fixed at the data, not the renderer.
- The staged-render bug SHIPPED through a harness blind spot: the dep-free DOM-shim cannot natively exercise full-motion animation. Mitigated by a new `__drain` timer-pump + enriched dynEl (insertAdjacentHTML/classList/scrollHeight) giving the FIRST full-motion harness coverage of the streaming read.

## Open Questions
- None unresolved this session.

## Artifacts Changed
- `data/{fincen,fincen-alerts,ofac,fintrac}/derived/*.json` (42 records — complete re-extraction to 903, then dedup to 875; new `capability`/`data_source` fields; grounded status/data/build_rec; templated build_logic; register `red_flag`s)
- `corpus.html` (`renderArticle` streaming rewrite, `highlightArticle` char-position spans, `cleanArticle` de-pipe, `#attribution` footer slot + `updateAttribution()`, branding)
- `scripts/build.py` (projects `url`, derives an `attribution` field from the © source string, `import re`, brand subtitle "AML Corpus Explorer")
- `tests/corpus-explorer.test.mjs` (enriched dynEl + `__drain` timer-pump + `chrome.attribution` → first full-motion streaming coverage; 148 → 165 assertions)
- `dist/corpus/index.html` (rebuilt, ~2.40MB)
- Docs: `CLAUDE.md`, `HANDOFF.md`, `README.md`, `.dev-wiki/*`, `.claude/rules/active-phase.md`

## Related
- [[phase-27-corpus-quality-assessment|Phase 27: Make the corpus demo shippable]] — parent line (Phase 27's assessment missed completeness; Phase 28 owns it)

## Health Delta
- Harness 148 → **165** assertions (+17, incl. the first full-motion streaming coverage)
- Corpus 903 → **875** indicators (dedup −28; terror 77→53)
- `--check all` 4/4 ZERO DRIFT · `--selftest` PASS · all 42 `--check-derived` clean · dist/corpus ~2.40MB
- Frozen byte-clean: the showcase (index.html + config/** + the 3 typology dists), every source md, every corpus-status.json, data/typology-map.json, the grounding core `derive_signals.py`
- Coverage: FABRICATED → GROUNDED (user interview) — a net honesty GAIN

## Escape Hatches
- **DISCOVERY (phase abort rule)** — T10 scoped as "regate + docs," but the browser review surfaced real render bugs (staged streaming, ~48s pacing) + a data-quality bug (28 duplicate indicators). The abort rule ("if T10 surfaces a real render bug, fix before commit") authorized fixing them before the commit, beyond the planned T10 scope.
- **USER OVERRIDE** — FINTRAC attribution handling: the user directed relocate-to-footer (reversing T9's removal). NET EFFECT RESTORES/HOLDS the verbatim+attribution non-negotiable, so no compliance weakening — noted as the owner's compliance call.

## Soft Observations / Phase N+1 Candidates
- **Harness fidelity for animated render paths** — the dep-free DOM-shim cannot natively exercise full-motion animation; the staged-render bug shipped precisely through this blind spot. `__drain` + enriched dynEl give partial-fidelity coverage, but a thin real-DOM/animation smoke path may be warranted (in tension with the no-jsdom file:// ethos). | evidence: this journal "Problems Solved"
- **Add an overlap/dedup guard to the extraction gate** — the completeness sweep PRODUCED duplicate extractions (28 across 5 docs; terror double-extracted under two section schemes). The grounding gate enforces FAITHFULNESS, not UNIQUENESS. A per-doc distinct-highlight (or duplicate/overlap) rate is a cheap corpus-health canary — terror's 68% is exactly what surfaced the bug. Catch duplicates at the gate (`check_record` or the build boundary), not as post-hoc cleanup.
- **The 4 single-dup artifacts** (tab-soup / newline / prefix-truncation) show the re-extraction occasionally emits the same source bullet twice with whitespace/length variants — an extraction-quality signal worth a guard.
- **The capability/data tags are unused in the UI** — a future "capability lens" (group/filter indicators by capability; show the institution's coverage by capability) is a natural payoff of the taxonomy.
- **The "Illustrative data & outputs" badge wording** may want revisiting — coverage is now GROUNDED in the user's answers, not illustrative; only the combination-lift template stays illustrative.
