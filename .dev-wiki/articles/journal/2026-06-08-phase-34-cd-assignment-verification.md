---
title: "Phase 34: C/D-assignment verification pass"
aliases: []
category: journal
tags: [m7, corpus, verification, capability, data-source, taxonomy, inter-rater-agreement, blind-reassignment, honesty, ph34_apply, data-correctness]
parents: [phase-34-cd-assignment-verification]
created: 2026-06-08
updated: 2026-06-08
source: debrief
duration: unknown
---

# Phase 34: C/D-assignment verification pass

## What Happened

Phase 33 tripled the corpus to 2,251 indicators, but the 1,376 NEW ones (in the 14 new derived records) carry capability(C)/data_source(D) codes that were the ONE neural step in Phase 33, gated only for vocabulary VALIDITY (in-set; `ph33_apply.py` reported 0 flagged), NEVER for CORRECTNESS. Those codes drive every coverage field (status/data/build_rec/build_logic) AND the Phase-29/30 capability & data-source executive lenses — a mis-assignment silently shows a wrong posture in the primary demo. Phase 34 verified + corrected them MEASURE-FIRST and HUMAN-adjudicated, a DATA-correctness phase (only the 14 new records changed; corpus.html/build.py are data-driven).

- **T1** — a deterministic consistency audit (`.dev-wiki/tmp/ph34_audit.py`, no LLM): **30.5% (419/1,376)** of new indicators in HARD same-text-different-code contradictions, concentrated in the FINTRAC sector-page common spine; + within-section soft outliers. Sized the problem before the neural pass.
- **T2 [L]** — a BLIND re-assignment workflow (`ph34-blind-reassign`, 30 agents) over the **589 UNIQUE TEXTS** (not 1,376 indicators — 57% fewer judgments AND one canonical code per text structurally prevents re-introducing inconsistency), schema-constrained, blind to the existing code + a deterministic compare (`ph34_compare.py`) → INTER-RATER AGREEMENT **C 74.4% / D 77.9% / both 63.9%** (reported HONESTLY as agreement/consensus, NEVER "proven correct" — a 2nd LLM pass is consensus, not ground truth) + a clustered disagreement surface.
- **T3** — cluster + human disposition (`ph34_dispositions.json`, 243 dispositions): the two user cluster-level RULINGS + consistency-collapse + a keep-existing tail.
- **T4** — a byte-surgical apply (`ph34_apply.py` + a synonym-aware `ph34_straggler.py` pass) reusing `ph33_apply.py`'s deterministic downstream → **213 indicators corrected** (114 C-moves + 129 D-moves + 3 client/customer wording-drift stragglers); flag/red_flag/section/src_line/id byte-identical (git-confirmed 0 +/− on frozen fields); consistency **30.5% → 2.0%**.
- **T5** — rebuilt dist/corpus + full regate + docs.

CLAUDE.md (current-state header + a Phase-34 current-state bullet + a milestone line) and HANDOFF.md (M7 milestone note) were updated this session with the measured agreement + 213 corrections.

## Decisions Made

- **Phase 34 DIRECTION** = verify the 1,376 new C/D assignments (chosen over add-a-3rd-jurisdiction and a-proper-Sector-axis at the dev-plan gate). The corpus tripled on unverified neural assignments; measure/correct the neural step before scaling further (measurement before optimization); the codes drive every coverage field + the executive lenses; ties to ground-judgments-in-a-user-interview (audit correctness, not just validity).
- **Verification METHOD** = measure-first + honest-as-agreement: a deterministic consistency audit (no LLM) sizes the problem, a BLIND re-assignment measures INTER-RATER AGREEMENT (reported as agreement, NEVER "proven correct"), then the USER adjudicates disagreements at the cluster level (the accepted truth source, the Phase-28 model). No new demo number — the agreement + corrections are a journal/quality artifact; the always-on illustrative badge stays the only claim.
- **Re-assign per UNIQUE TEXT (589), not per indicator (1,376)** — 57% fewer judgments AND one canonical code per text structurally prevents re-introducing inconsistency. A method refinement proposed mid-T2 and approved by the user.
- **User cluster-level RULINGS (the human gate):** (1) adverse-media (C19/D13) ≠ KYC (C14/D8) — keep the distinction; the examined C19/D13 cluster was all direct-KYC mis-files (client states criminal involvement / PO-box / disconnected phone), never real adverse-media, so moving them to C14/D8 PRESERVED the separation; genuine OSINT/news stays C19/D13. (2) cash (C5/D2) ≠ PEP (C17) — cash stays cash; the cash→PEP mis-tags collapse to the cash majority. Genuinely-ambiguous clusters (C16↔C15 nominee/shell, C2↔C1 pass-through/out-of-pattern, etc.) KEPT existing — no churn.

## Problems Solved

- Re-assigning 1,376 indicators independently could have produced fresh contradictions — resolved by re-assigning per unique text (589 canonical) so each text resolves to one code.
- 3 client/customer wording-drift stragglers (the same indicator phrased "client …" vs "customer …") evaded the exact-text canonicalization — caught by a synonym-aware `ph34_straggler.py` pass.

## Artifacts Changed

- `.dev-wiki/tmp/ph34_{audit.py,audit.json,reassign.json,blind_assignments.json,blind_input.json,compare.py,dispositions.json,apply.py,straggler.py,stragglers.json,prep.py,existing_map.json}` (NEW, authoring-only)
- `data/fincen/derived/*.json` + `data/fintrac-guidance/derived/*.json` (10 of 14 new records changed — only off-canonical C/D codes + their deterministic downstream; flag/red_flag byte-identical)
- `dist/corpus/index.html` (rebuilt, ~4.88MB; data-driven — corrected codes flow through)
- `CLAUDE.md`, `HANDOFF.md` (the measured agreement + 213 corrections)
- `tests/smoke-checklist.md`

## Related

- [[phase-34-cd-assignment-verification|Phase 34: C/D-assignment verification pass]] — parent phase

## Health Delta

- No test-count change (corpus harness 235, news 65 — both green; 56/56 `--check-derived`); no toolchain change
- 10 of 14 new derived records changed (the other 4 had no off-canonical codes); dist/corpus rebuilt (~4.88MB)
- consistency 30.5% → 2.0%; 213 indicators corrected (114 C + 129 D + 3 stragglers)
- `--check all` 5/5 ZERO DRIFT; `--selftest` PASS; the grounding core / build.py / 42 existing records byte-frozen

### Gate Compliance

- gate-log:phase-34 — `direction=approved` present (compliant); `delivery=pending` (correct — the delivery gate flips to `accepted` after the commit verifiably lands; the user accepted delivery 2026-06-08). No missing-gate flag.

## Soft Observations / Phase 35 Candidates

- Phase-33 within-doc extraction left a few degenerate verbatim flags (truncated lead-ins like "A client conducts transactions that involve:" + a section header "Public works and construction" extracted as a flag) — a flag-COMPLETENESS/quality fix (out of Phase-34 scope; flag was frozen). | Phase 35: a flag-completeness/quality sweep over the 56 derived records | Evidence: the T1/T2 residual clusters + `ph34_audit.json`.
- The 875 OLD indicators share the same per-indicator-unverified C/D property (LLM-tagged in Phase 28, per-CODE posture-grounded but never per-indicator verified). Lower priority — fuller Phase-28 treatment, new-set agreement (74/78%) not catastrophic. | Phase 35: extend C/D verification to the old set | Evidence: Phase-28 tagged per-code posture, never per-indicator C/D correctness.
- 28 residual same-text-different-code contradictions remain, ~half new-vs-FROZEN-old (a new record's canonical now differs from a frozen sibling's code for the same text) — only resolvable by unfreezing/re-verifying the 42 protected records; the rest are different verbatim flags sharing one translation (defensible). | Phase 35: a corpus-wide C/D consistency consolidation that unfreezes + re-verifies the 42 protected records | Evidence: `ph34_audit.json` final run.
- No automated guard prevents future same-text-different-code drift within a source. | Phase 35: a harness/build assertion for within-source C/D consistency (mind the documented new-vs-frozen residual to avoid brittleness) | Evidence: the gate checks faithfulness, never C/D consistency.
