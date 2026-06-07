---
type: phase
phase: 26
slug: phase-26-corpus-elevation
status: completed
ceremony: lite
created: 2026-06-07
updated: 2026-06-07
milestone: M7
---

# Phase 26: Elevate the corpus demo to showcase quality

> Planned 2026-06-07, direction approved. Workflow-driven, largest phase to date (6 tasks, two L). All 6 tasks [x]; exit criteria met → READY FOR COMPLETION (delivery gate pending acceptance). Reviewer 10/10 ACCEPT. Commits 7a35147 (T1) · 44c24a6 (T2) · 83be590 (T3) · 337b8aa (T4–T6).

## Objective
Reviewing the BUILT Phase-25 corpus artifact, the user reframed AGAIN — to a QUALITY elevation of the whole corpus demo to the six-act showcase's bar. Five gaps, fixed ALL-IN in one **workflow-driven** phase (the user asked to "build a workflow"):
1. The `red_flag` translations read like PROSE, not the showcase's crisp typology-named AML INDICATORS — Phase 25 never anchored to `config/typologies/fentanyl.json` (the register miss).
2. The per-doc "Read advisory" article screen renders STATIC — no progressive "agent reading" reveal.
3. The Signal screen is STATIC — no build-log / combination-lift WOW ("doesn't wow").
4. Docs aren't grouped (want grouped by SOURCE, newest-first) and red flags aren't grouped.
5. No LANDING page.

## The Register (the bar)
The corpus `red_flag` must read like the SHOWCASE's red flags — short typology-named mechanism-naming noun phrases (the `config/typologies/fentanyl.json` style, the register Phase 25 missed). SHOW-BOTH stays: the verbatim `flag` remains beside each translation as the grounded evidence. ONLY the `red_flag` VALUES change — the grounding logic (normalize/rf_region/flag⊂md) and the SHAPE gate (present / non-empty / distinct / length-bounded) are BYTE-UNCHANGED. T1 distils a register RUBRIC from fentanyl/elder and proves it on EFE + 2 exemplars (resemble the showcase oracle, else degrade) BEFORE T2 churns all 42.

## Scope
UNFREEZE: the 42 `data/{fincen,fincen-alerts,ofac,fintrac}/derived/*.json` (the `red_flag` VALUES only), `corpus.html`, `scripts/build.py` (ONLY if a wow beat needs it), `dist/corpus/index.html`, `tests/**`, `CLAUDE.md`, `README.md`, a register-rubric note.
FROZEN byte-untouched: the six-act showcase (`index.html` + `config/typologies/**` + the 3 typology dists), every source MD, every `corpus-status.json`, `data/typology-map.json`, the grounding core `scripts/derive_signals.py` + the authoring scripts (acquire/crawl/pdf_to_md). The verbatim `flag` + the grounding logic stay untouched — only the `red_flag` VALUES change.

## Wow-numbers honesty (load-bearing — REVERSES the Phase-18 no-fabricated-lift call, user-approved)
The Signal screen gets the showcase's build-log + combination-lift wow. The build-log animates the REAL `build_logic` (honest). The combination-lift figures are a GENERIC illustrative TEMPLATE shown with a LOUD "illustrative · pending calibration" tag UNDER the always-on badge — NEVER 42 fabricated per-doc findings, NEVER presented as real; the user supplies real figures later. A single disclosed template is honest in a way ~42 fabricated per-doc stats were not (the Phase-18 rejection). If a beat needs a fabricated per-doc finding, CUT it to the template.

## Exit criteria
- All 42 live docs' `red_flag` values re-translated to the fentanyl-register AML-indicator style (grounding + the red_flag SHAPE gate byte-unchanged — only VALUES change).
- The per-doc article screen renders progressively ("agent reading").
- Docs grouped by SOURCE / newest-first + red flags grouped.
- The build-log + combination-lift WOW beats land, illustrative-badged (loud "illustrative · pending calibration" tag, never per-doc fabricated).
- A story-driven LANDING page.
- `python3 scripts/build.py --check all` zero drift; the harness extended.
- The six-act showcase + every source md + corpus-status.json + data/typology-map.json + the grounding core `derive_signals.py` byte-frozen.
- CLAUDE + README updated; NO non-negotiable change.

## Tasks
See tasks.md (phase-26 block): T1 register rubric + workflow briefs + re-translate EFE + 2 exemplars as the PROOF/checkpoint (M, checkpoint) · T2 the re-translation workflow over all 42 (L) · T3 progressive article render + grouping/sort (M) · T4 build-log + combination-lift wow beats, illustrative-badged (L) · T5 story-driven landing page (M) · T6 rebuild + harness + docs (S).

## Decisions
See _CURRENT_STATE.md `## Recent Decisions` (the three Phase-26 rows): (1) ALL-IN elevation in one workflow-driven phase; (2) the REGISTER bar (terse mechanism-named, show-both, only red_flag VALUES change); (3) the WOW-NUMBERS honesty reversal of Phase-18 (illustrative template, loud tag, generic-not-per-doc). Direction approved by user 2026-06-07.

## Abort / degrade
If T1's register PROOF fails (the re-translations can't resemble the showcase oracle / would over-interpret), REPORT before T2 — don't churn all 42. If a wow beat needs a fabricated per-doc finding, CUT it to the generic illustrative-badged template (never 42 fabricated per-doc lift figures; never presented as real). Blocked >3 attempts → ask the user: skip or abort.
