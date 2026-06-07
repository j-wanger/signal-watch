---
title: "Phase 26 — Elevate the corpus demo to showcase quality (register re-translation + progressive render + build/lift wow + grouping/sort + landing)"
aliases: []
category: journal
tags: [corpus-explorer, register, re-translation, workflow, progressive-render, wow-beats, combination-lift, landing, honesty, M7]
parents: [phase-26-corpus-elevation]
created: 2026-06-07
updated: 2026-06-07
source: debrief
duration: long multi-task session (a dynamic re-translation workflow + 5 implementation tasks + this debrief)
---

# Phase 26 — Elevate the corpus demo to showcase quality (M7)

## What Happened
Phase 25 shipped the corpus's two-layer red-flag model, but the user reviewed the BUILT artifact and named five quality gaps at once: the `red_flag` translations read like PROSE (Phase 25 never anchored to `config/typologies/fentanyl.json` — the register miss), the article screen renders STATIC, the Signal screen "doesn't wow", docs + red flags aren't grouped, and there is no landing page. Phase 26 elevated ALL of it to showcase quality in one workflow-driven phase (6 tasks, two L). All 6 tasks are [x]; exit criteria met → READY FOR COMPLETION (delivery gate pending user acceptance).

- **T1** (committed at planning, 7a35147) authored the register rubric (distilled from fentanyl/elder) + 4 beat design briefs in `.dev-wiki/articles/phase-26-register-rubric.md`, and validated the register PROOF in-session (re-translating EFE to the register passes `--check-derived` clean, verbatim untouched + still grounds, matches the showcase elder labels nearly 1:1). The 3 exemplar re-translations were NOT persisted — they fold into T2's full-42 sweep (committing then re-doing them is wasted churn). The T2 abort gate cleared.
- **T2 (L)** ran the **re-translation as a DYNAMIC WORKFLOW** — 84 agents (42 translate → 42 independent adversarial verify, pipelined) producing an authoritative `{id:red_flag}` sidecar per doc, then a **byte-surgical applier** wrote ONLY the `red_flag` values (proven no-op-stable across all 42; a naive JSON round-trip would have reformatted OFAC maritime's compact `features` array), then `--check-derived` gated. 633/634 indicators re-translated (1 already register-quality, retained); git diff = 42 files, every changed line a `red_flag` line; the verbatim `flag`/`src_line`/`status`/`build_logic` byte-untouched. The LLM proposes, the deterministic layer disposes — mirrors the project's inverted-loop philosophy. (dist/corpus stayed STALE through T2–T5 by design; T6 rebuilt.)
- **T3 (M)** corpus.html: (a) ported the showcase `streamAdvisory` progressive "agent reading" typing/reveal to `renderArticle` as a progressive-enhancement; (b) Select grouped by SOURCE into 4 `.srcgroup` sections, date-DESC (newest-first); (c) red-flag SECTION sub-grouping on Coverage (multi-section docs show sectheads, single-section flat — NOT applied to Build-recs, whose BUILD_NOW-first gate sort is load-bearing).
- **T4 (L)** ported the wow beats: a **build-log** on the Signal screen (6 structural steps auto-completing, reading the REAL `build_logic`, no numbers) + a NEW **Combination-lift** screen (DETAIL index 4, between Signal & Close) animating a GENERIC illustrative template (18→64→83, identical across every doc; only the signal name is real/per-doc) behind a LOUD "illustrative · pending calibration — NOT measured on this document" tag. The per-doc arc grew 5→6 detail screens.
- **T5 (M)** added a story-driven LANDING page (`view='landing'`, the new initial view) ahead of Select — a story hero, 4 HONEST stat tiles (46 docs · 42 derived · 4 sources · 2 jurisdictions), an "Enter" CTA, and a compliance framenote. The SHOWCASE landing (index.html) was ROADMAPPED, not built (index.html stays byte-frozen).
- **T6 (S)** rebuilt dist/corpus (2.19MB→2.17MB), `--check all` 4/4 ZERO DRIFT, realigned + extended the harness 108→139 (boot auto-enters Select since the landing is the new entry; the close-screen index shifted 4→5), updated CLAUDE.md + README.md (the non-negotiable wording byte-unchanged).

## Decisions Made
*(CEREMONY=lite — no decision articles; journal context only)*
- **Bundle T4–T6 into one green commit** (user-chosen via a question): T4's new Combination-lift screen shifts the committed harness's hardcoded close-screen index, so T4 is not independently green against the committed harness. Bundling keeps every commit green and respects the plan's harness=T6 scope.
- **The "template-final + browser-only progressive-enhancement" pattern** for renderArticle and the wow beats: render the FINAL state into `stage.innerHTML` first (so reduced-motion AND the string-DOM test-shim settle on it with no extra work), and only under full motion reset-and-replay the typing/animation. This resolved a real test-shim limitation — it does not write back content set via post-render `getElementById().innerHTML` (the first cut, which deferred-populated #doc/#xlate, failed the harness).
- **T2 ran as a dynamic workflow** (84 agents) + a byte-surgical applier + the `--check-derived` gate — the LLM proposes, the deterministic layer disposes.
- **Combination-lift honesty = a GENERIC illustrative template** (18→64→83, identical across every doc; only the signal name is real/per-doc) behind a LOUD "illustrative · pending calibration — NOT measured on this document" tag, distinct from the always-on badge — the deliberate, user-approved, scoped reversal of Phase-18's no-lift rejection (honest because nothing is claimed real and the records carry no lift figures). Section sub-grouping was applied to Coverage but deliberately NOT to Build-recs.

## Problems Solved
- **The register miss** (Phase 25's prose-style red flags) — fixed by anchoring all 42 docs' `red_flag` to the fentanyl/elder AML-indicator register via the T2 workflow; quality on-bar (e.g. "Receive-and-forward to no-relationship payees (mule pass-through)", "Multi-originator geographic funnel-in to one SW-border beneficiary"); length min24/max126/mean64, no prose leaked.
- **The string-DOM test-shim's no-writeback limitation** (recurred from Phase 25) — resolved by the template-final + progressive-enhancement pattern, now the established corpus.html convention for any animated screen.
- **OFAC maritime's compact `features` array reformatting risk** — avoided by the byte-surgical applier that writes only `red_flag` values rather than round-tripping JSON.

## Open Questions
- None new.

## Artifacts Changed
- `data/{fincen,fincen-alerts,ofac,fintrac}/derived/*.json` (42 records; ONLY the `red_flag` VALUES re-translated to the register — verbatim `flag` + grounding byte-untouched; 634/634 indicators carry a distinct, 12–240-char red_flag — full parity)
- `corpus.html` (per-doc arc grew 5→6 detail screens — added a Combination-lift screen between Signal & Close; a new `view='landing'` entry view; a build-log on the Signal screen; progressive `renderArticle`; Select source-grouping + date-desc; Coverage red-flag section sub-grouping)
- `dist/corpus/index.html` (rebuilt, 2.19MB→2.17MB)
- `tests/corpus-explorer.test.mjs` (108→139 assertions; boot() auto-enters Select; close-screen index 4→5)
- `CLAUDE.md`, `README.md` (Phase-26 elevation; non-negotiable wording byte-unchanged)
- `.dev-wiki/articles/phase-26-register-rubric.md` (T1, committed 7a35147 — register rubric + 4 beat design briefs)

## Related
- [[phase-26-corpus-elevation|Phase 26: Elevate the corpus demo to showcase quality]] — parent phase
- [[2026-06-07-phase-25-corpus-translation|Phase 25 — corpus output quality (extract → translate)]] — the predecessor whose register miss this phase fixes

### Review Gate
Unified reviewer (dispatched this debrief) returned **Score 10/10, Verdict ACCEPT** — no CRITICAL/HIGH/MEDIUM findings. Independently re-verified all gates green (`--check all` 4/4, harness 139/139, `--selftest` PASS, clean tree at 337b8aa) and the load-bearing honesty constraints: the lift template is a single hardcoded constant identical across docs (only the signal name is per-doc from real build_logic) behind the loud pending-calibration tag with an honest empty state; the red_flag translations are faithful register changes (no added thresholds/typologies/mechanisms — AML lexicon all grounded in the verbatim); byte-freeze held across the entire phase (baa0374..HEAD) with 0 non-red_flag lines changed in any derived record and the full frozen set untouched; full 634/634 red_flag parity. Code quality surgical + reduced-motion-safe (no XSS in the typed render, Object.assign copies in renderClose, keyboard nav + div-toggle gate preserved). 1 non-blocking suggestion: renderArticle's typing animation hardcodes CAP=1600 / 3-char-per-10ms, so the typed "reading" prefix is doc-length-agnostic (same ~5s open on a short alert or a long FINTRAC OA) — acceptable as a cue; a future polish could scale the cap to doc length.

### Health Delta
- Harness 108→**139** (+31 assertions, all green).
- `python3 scripts/build.py --check all` — **4/4 ZERO DRIFT**.
- `python3 scripts/derive_signals.py --selftest` — **PASS** (grounding core byte-untouched).
- 42/42 derived records `--check-derived` **clean** (634/634 indicators carry a distinct, 12–240-char `red_flag` — full parity).
- No new runtime dependency (the re-translation workflow is ephemeral, not shipped).
- dist/corpus 2.19MB→**2.17MB**.
- No change to `scripts/`, the showcase, or any data file beyond the 42 derived records' `red_flag` values.

## Soft Observations / Phase N+1 Candidates
- A story-driven LANDING for the six-act SHOWCASE (index.html) is the natural next-phase candidate — the corpus got one this phase; the showcase stayed byte-frozen. | Phase N+1: unfreeze index.html, port the corpus landing pattern to the showcase. | evidence: T5 (roadmapped, not built).
- The string-DOM test-shim's no-writeback limitation recurred (Phase 25 noted it; Phase 26-T3 hit it): the harness cannot observe content set via post-render `getElementById().innerHTML`. The "template-final + progressive-enhancement" pattern is now the established corpus.html convention for any animated screen — a reusable insight worth capturing. | evidence: T3 decision.
- renderArticle's typing animation hardcodes CAP=1600 / 3-char-per-10ms (the reviewer's non-blocking note): the typed "reading" prefix is doc-length-agnostic, so a presenter sees the same ~5s open on a short alert or a long FINTRAC OA. Acceptable as a cue; a future polish could scale the cap to doc length. | evidence: reviewer suggestion.
- The combination-lift figures carry an explicit "pending calibration" tag — a standing future obligation: the user supplies real, backtested lift figures later (no date set). | evidence: T4 / the wow-numbers honesty decision.
