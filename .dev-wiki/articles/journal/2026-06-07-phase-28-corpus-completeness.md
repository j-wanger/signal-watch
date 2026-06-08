---
type: journal
date: 2026-06-07
phase: 28
slug: 2026-06-07-phase-28-corpus-completeness
tags: [corpus, completeness, interview, grounded-coverage, taxonomy, capability, re-extraction, M7, wip]
---

# Phase 28 — Corpus COMPLETENESS + grounded-coverage interview + methodical render (M7) — WIP (T1–T9 done, T10 remains)

> Mid-phase checkpoint debrief. NOT complete, NOT committed — the data foundation + UX are done on disk; T10 (harness realign + non-negotiable wording + final regate + commit) remains. The harness currently shows 5 EXPECTED failures (see below).

## The reframe (the core, that Phase 27's assessment missed)
The user reviewed the BUILT Phase-27 corpus and found the real defect: verbatim red-flag EXTRACTION is grossly INCOMPLETE — the grounding gate only ever verified each extracted flag was REAL, never that we got them ALL. PROOF (the user's spot-check, quantified): fintrac-synthetic-opioids enumerates ~80 bulleted indicators across 5 categories; we shipped 15 (~19%). Phase 27's 44-agent "assessment" audited presentation/register/grounding and walked right past completeness — owned directly. The user added the bigger insight: STOP fabricating per-indicator coverage/data; instead design yes/no/PARTIAL interview questions and ground coverage in the user's real answers.

## What shipped (T1–T9, on disk, gated, building — NOT committed)
- **T1 PROOF** — complete-extracted the opioid doc (15→68 grounded) + a 12-cap interview → grounded coverage 19% / 46 BUILD_NOW / 9 SOURCE_DATA. Proved BOTH fixes before the sweep (prove-then-full-sweep).
- **T2 TAXONOMY** — the `ph28-derive-taxonomy` workflow (4 cluster-by-typology agents → 1 synthesize) derived a **28-capability + 20-data-source** taxonomy from 702 indicators; user reviewed + approved, added the PARTIAL state.
- **T3 COMPLETE RE-EXTRACTION** — the `ph28-complete-sweep` workflow (84 agents: 42 extract → 42 completeness-critic). **634 → 903 indicators**; the disasters fixed (terror 13→77, opioids 15→68, human-trafficking 57→98, maritime 7→40); already-complete docs stable. Deterministic bullet-detect proved UNRELIABLE (glyphs vary per doc //•-; FinCEN has none) → LLM-enumerate is the path, the bullet-count the completeness oracle. Tail-stop fixed (bibliography stopped leaking); 2 ungrounded dropped; every flag re-grounds.
- **T4 CLASSIFY** (folded into the sweep) — each indicator tagged capability C1-C28 + data_source D1-D20.
- **T5 INTERVIEW + APPLY** — the user answered 28+20 y/n/partial; deterministic apply: cap-answer→status, data-answer→availability, cover×data matrix→build_rec. GROUNDED corpus-wide: **258 covered / 191 partial / 454 gap**; 220 BUILD_NOW · 147 SOURCE_DATA · 87 BUILD_ENRICH · 179 ENHANCE · 12 MONITOR · 258 COVERED. NO fabrication — the coverage is the institution's real posture.
- **T6 TEMPLATED build_logic** — 28 capability spec-templates (showcase 7-key shape) attached to the 220 BUILD_NOW by capability (the capability IS the signal type → templated, not 220 bespoke). All 42 records `--check-derived` CLEAN; build.py corpus builds 2.41MB; new fields flow through build.py untouched (passthrough at line 505).
- **T9 BRANDING + COMPLIANCE** — "FinCEN Corpus Explorer" → "AML Corpus Explorer"; the FINTRAC "© His Majesty / reproduced…" stripped at DATA (build.py source projection; +`import re`) AND DISPLAY (srcCap strips the © clause; cleanArticle drops the copyright-page boilerplate; framenote/landing simplified).
- **T7 METHODICAL RENDER** — `renderArticle`/`highlightArticle` rewritten: highlight (`<span class="hl on" data-i>` + a `.now` pulse) + extract row reveal AS the read reaches each phrase, in DOCUMENT ORDER, scroll-following, paced to finish under ~50s even on a 98-indicator doc (the user's "render as we reach the phrases / 1 minute is fine"). Template-final + progressive-enhancement (reduced/harness settle on the final state).
- **T8 SIGNAL ANIM SYNC** — the spec card starts `.predraft` (hidden) under full motion and reveals (staggered) as the build-log's "Generate proposals" step (index 2) lands — proposal appears as the agent drafts it.

## Escape hatches
- **USER OVERRIDE** ×2: (1) "extract everything" incl. the generic FINTRAC categories (vs topic-only); (2) REMOVE the FINTRAC Crown-copyright attribution from the page (the user owns the compliance call — diverges from the current non-negotiable; T10 owes the CLAUDE.md/HANDOFF wording update + the override log).
- **DISCOVERY** ×2: (1) the apply stored the D-id in the `data` field instead of availability (field-name collision) → 0/42 gate; fixed by mapping `data`→availability from `data_source`+answers → 42/42 clean. (2) `re` was unimported in build.py → NameError on the source-strip → added `import re`.

## Health Delta
Corpus 634 → **903 indicators** (+42%). New per-indicator fields: `capability`, `data_source`. Coverage moved from FABRICATED → GROUNDED (user interview). dist/corpus 2.15MB → 2.41MB. 2 new dynamic workflows (taxonomy 5 agents; sweep 84 agents) + 2 single agents (classify, templates). Harness: **143 pass / 5 fail** — all EXPECTED (the `class="hl"`→`"hl on"` rename ×2; the 2 attribution-render assertions now testing removed behavior; EFE section change). No runtime/console errors; renders sound. T10 realigns the harness.

## Review Gate
Lite (self-check). The grounding gate (`normalize`/`rf_region`/`check_record`) was NOT modified — all 903 flags re-ground through it unchanged; build_rec follows the unchanged cover×data matrix; the new capability/data fields are additive. The one genuinely new honesty property: coverage is now grounded in the user's answers, not fabricated — a net honesty GAIN.

## Gate Compliance
`<!-- gate-log:phase-28 direction=approved delivery=pending -->` — direction approved (the user directed all of it: complete-extract + interview-coverage + the UX/branding/compliance items; prove-then-full-sweep). Delivery pending (phase incomplete — T10 + the user's browser review).

## Soft Observations / Phase N+1 Candidates
- **T10 is the immediate resume point**: realign `tests/corpus-explorer.test.mjs` to the 903-indicator grounded corpus (the `class="hl on"` rename, drop/flip the FINTRAC-attribution-render asserts, EFE/section changes, the new counts); update the CLAUDE.md/HANDOFF FINTRAC non-negotiable wording to the attribution-removed posture + log the override; `--check all`/`--selftest`/harness green; then commit + the user's browser review.
- **The interview-grounded coverage is the demo's new identity** — it's no longer "illustrative coverage" but a real institution self-assessment; the "Illustrative data & outputs" badge wording may want revisiting (coverage is now grounded; only the combination-lift template stays illustrative).
- **build_logic-at-scale = templated-from-capability** is the established pattern now (28 templates; multiple BUILD_NOW per capability share a spec — the Signal screen may want to DEDUP spec cards by signal_name).
- **Completeness has no deterministic oracle** for markitdown's heterogeneous bullets — the LLM-enumerate + critic is best-effort; a couple of dense docs (e.g. OCSE) may still be slightly under vs their raw bullet count. Acceptable; the disasters are fixed.
- **The capability/data tags are unused in the UI** — a future "capability lens" (group/filter indicators by capability; show the institution's coverage by capability) is a natural payoff of the taxonomy.

## Resume state (uncommitted, on disk)
Changed: 42 `derived/*.json` (full rewrite, 903 indicators), `corpus.html` (T7/T8/T9), `scripts/build.py` (source-strip + `import re`), `dist/corpus`. FROZEN intact: showcase, source mds, corpus-status.json, typology-map.json, the grounding core `derive_signals.py`. `.dev-wiki/tmp/ph28-*.json` hold the intermediate artifacts. A fresh session resumes at T10.
