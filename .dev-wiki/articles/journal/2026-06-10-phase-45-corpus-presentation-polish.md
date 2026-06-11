---
title: "Phase 45: Corpus demo presentation polish (pre-presentation day) — 6/6 same-session"
aliases: []
category: journal
tags: [corpus-explorer, presentation, polish, honesty, combination-lift, fintrac-attribution, mojibake, m7]
parents: [phase-45-corpus-presentation-polish]
created: 2026-06-10
updated: 2026-06-10
source: debrief
duration: unknown
---

# Phase 45: Corpus demo presentation polish — lift honesty completed, walkthrough frozen

## What Happened
- One-day pre-presentation phase (dist/corpus presents to bank stakeholders 2026-06-11). 6/6 tasks [x] same-session; READY FOR COMPLETION, delivery gate pending (two-commit convention; the frozen dist/corpus baseline MOVED by design).
- T2 was the headline: the fake 18→64→83 LIFT template + the "Illustrative · pending calibration" tag DELETED; the beat now renders R2 REAL inventory counts (covered indicators in the committed signal's typology × contributing regulators, client-side from `__CORPUS__`, honest corpus-wide fallback; NO performance claim — nothing left to disclaim). Completes the Phase-18 honesty arc. R1 zero-numbers fallback designed but never needed (user confirmed R2 at the walkthrough).
- T1 live-risk fixes (stagger cap, human-gate copy reframe "agent has PROPOSED all N — deselect to dispose", zero-build-now dead-end, "Queue backtest"); T3 FINTRAC Crown-copyright attribution EXTENDED to the two QUOTING lens drills, MULTI-DOC (the licence attributes per reproduced work — footer lists every contributing FINTRAC doc, re-derives per render; synthesis drill stays silent per the Phase-28 precedent); T4 ranked copy pass; T5 walkthrough + FREEZE (2 feedback items, 2 refinement rounds); T6 full regate.
- T5 feedback #1 ("non-ASCII characters") classified into TWO defect classes: (a) UTF-8-as-latin1 mojibake in the fincen-alerts derived records' AUTHORED coverage fields (~2.2K occurrences), (b) PDF symbol-font PUA bullets in 9 FINTRAC/OFAC article mds. Disposition: LOAD-TIME DISPLAY-ONLY repair in corpus.html (MOJI map, \u-escaped; fixEncoding walk at validateCorpus — placed BEFORE the CORPUS load after a TDZ bite); committed records/md BYTE-FROZEN per contract; byte-surgical record repair = the named DEFERRED permanent fix.
- T5 feedback #2: landing hook reshaped onto "effective and regulatorily defensible financial-crime program" — round 2 removed the dangling hero dash and RESTORED the "hard part was never access: extensive human review" body beat; examiner/cited-verbatim payoff moved to the loop paragraph.

## Decisions Made
- D1–D7 recorded in [[phase-45-corpus-presentation-polish|the approved decision article]] (pre-existing, current) + the gate ledger; in-impl additions D6 (two-class non-ASCII disposition) + D7 (landing hook, two rounds) captured in tasks.md T5 notes.

## Problems Solved
- Mojibake/tofu across 56 docs — display-only fixEncoding + a permanent harness sweep (full content × 6 screens + all lens drills) as the verify-all-contents gate.
- Bare vs doc-qualified overlay keys — killed on first contact by the independent-recomputation test pattern (expected values recomputed from committed data files, never from `__CORPUS__`/the DOM).

## Artifacts Changed
- `corpus.html` (display layer only: fixEncoding, docRef display mapper, multi-doc updateAttribution, R2 renderLift) · `dist/corpus/index.html` (rebuilt — frozen baseline moves) · `tests/corpus-explorer.test.mjs` (239→273) · `tests/smoke-checklist.md` (presenter/demo-path notes) · `CLAUDE.md` (honesty paragraph rewritten in place). No scripts/, data/, or module changes.

## Health Delta
- corpus-explorer 239→273 (+34: stagger cap, gate copy, dead-end states, R2 independent-recomputation counts, multi-doc attribution incl. US-only-empty + synthesis-silent, copy coherence, FULL-CONTENT mojibake sweep, landing hook); news-stream 150 unchanged-green; --check all 5/5 zero drift (corpus baseline moved by design); derive_signals --selftest + news_quality_harness --check green; self-check clean (lite cats 1-2; one path-style wiki link normalized).

## Assumption Revisit
- A1–A5 ALL held; A4 held with an UPSIDE (the spec's adversarial pass surfaced the multi-doc per-reproduced-work attribution requirement — the extension is licence-complete; C1 lists 18 docs). No bites.

## Soft Observations / Phase N+1 Candidates
- fincen-alerts derived records carry ~2.2K mojibake bytes in authored coverage fields | Phase N+1: byte-surgical record repair (display repair becomes the safety net) | tasks.md T5 dispositions
- Independent-recomputation test pattern (recompute expected from committed data, never the DOM) killed a real bug on first contact | reusable anti-tautology guard; /wiki-capture candidate | tests/corpus-explorer.test.mjs R2 block
- Typology overlay keys are DOC-QUALIFIED (`<doc-id>/<IND-id>`) — bare-id lookups silently miss all 350 overrides | consumer trap to document | data/indicator-typology-map.json
- The adversarial-constraints spec pass earned its cost (surfaced multi-doc attribution) | keep for compliance-adjacent phases | specs/phase-45
- CLAUDE.md 245 lines vs ~200 target — trim residual carries (Phase-44 lineage) | bundle into a future hygiene task
- Showcase Act-5 still carries the illustrative lift template (gate-accepted divergence) | future true-up if the showcase is ever presented again

## Related
- [[phase-45-corpus-presentation-polish|Phase 45: Corpus demo presentation polish]] — parent phase
