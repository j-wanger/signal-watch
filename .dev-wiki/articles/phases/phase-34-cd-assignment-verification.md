---
title: "Phase 34: C/D-assignment verification pass"
aliases: ["phase-34-cd-assignment-verification"]
category: phases
tags: [m7, corpus, verification, capability, data-source, taxonomy, inter-rater-agreement, blind-reassignment, honesty, ph33_apply, data-correctness]
parents: []
created: 2026-06-08
updated: 2026-06-08
source: plan
status: completed
delivery: accepted-2026-06-08 (committed 83a79c3, pushed to main)
scope: [".dev-wiki/tmp/ph34_audit.py", ".dev-wiki/tmp/ph34_reassign.json", ".dev-wiki/tmp/ph34_dispositions.json", "data/fincen/derived/*.json", "data/fintrac-guidance/derived/*.json", "dist/corpus/index.html", "tests/corpus-explorer.test.mjs", "tests/news-stream.test.mjs", "CLAUDE.md", "HANDOFF.md", "tests/smoke-checklist.md"]
entry_criteria: "Phase 33 (corpus completeness + full typology re-segmentation) DELIVERED + accepted + committed 823c0c2 + pushed to main; the corpus is the primary demo (Phase 27). Phase 33 tripled the corpus to 2,251 indicators, but the 1,376 NEW ones (61%, in the 14 new derived records) carry C/D codes assigned as the ONE neural step in Phase 33, gated only for vocabulary VALIDITY (in-set; ph33_apply.py reported 0 flagged), never CORRECTNESS. Direction approved at the goal gate 2026-06-08: verify the 1,376 new C/D assignments (the user picked this over 'add a 3rd jurisdiction' and 'a proper Sector axis' at the dev-plan priority gate)."
exit_criteria: "The 1,376 new C/D assignments verified (deterministic contradictions resolved + blind-re-assignment disagreements adjudicated by the user) and corrected; the MEASURED inter-rater agreement rate + correction count recorded (the honest quality artifact, not a demo number); flag/red_flag byte-frozen; only the 14 new derived records changed; all 56 --check-derived clean; --check all 5/5 zero drift; --selftest PASS; harness green (corpus + news byte-frozen); the frozen set byte-clean; NO non-negotiable change."
---

# Phase 34: C/D-assignment verification pass

## Objective

Verify and correct the 1,376 NEW capability(C1-C28) / data_source(D1-D20) assignments Phase 33 added — the ONE neural step that was gated only for vocabulary VALIDITY, never CORRECTNESS — measure-first and human-adjudicated, changing only the 14 new derived records. The grounded `flag` and `red_flag` stay byte-identical; only the C/D codes and their deterministic downstream (status/data/build_rec/build_logic) move.

## Why now (the defect)

- Phase 33 tripled the corpus to 2,251 indicators. The 1,376 NEW ones (61% of the corpus, in the 14 new derived records — 4 new FinCEN advisories + 10 FINTRAC-guidance sector pages) carry C/D codes that were the ONE neural step in Phase 33, gated ONLY for vocabulary VALIDITY (in-set; `ph33_apply.py` reported 0 flagged), NEVER for CORRECTNESS.
- Those C/D codes drive every downstream field — status, data, build_rec, build_logic — AND the Phase-29 capability lens + Phase-30 data-source lens (the demo's executive views). A mis-assigned code silently shows a WRONG posture in the primary demo's executive views, against the honest-grounding thesis.
- The grounding gate (`derive_signals.py` check_record / normalize / rf_region) is about FAITHFULNESS of the verbatim flag, NOT recall/correctness of the C/D tagging — this phase audits the dimension the gate never checked (memory: "a grounding gate ≠ a completeness gate; audit recall, not just faithfulness").
- The corpus tripled on unverified neural assignments → measure/correct the neural step before scaling further (measurement before optimization).

## Scope

- `.dev-wiki/tmp/ph34_audit.py` (NEW, authoring-only) — the deterministic consistency audit (reads the 14 new records; no LLM).
- `.dev-wiki/tmp/ph34_reassign.json` (NEW, authoring-only) — the blind re-assignment + inter-rater agreement output.
- `.dev-wiki/tmp/ph34_dispositions.json` (NEW, authoring-only) — the clustered human dispositions.
- `data/fincen/derived/*.json` + `data/fintrac-guidance/derived/*.json` — the 14 new derived records: ONLY the changed indicators' `capability`/`data_source` + their deterministic downstream move.
- `dist/corpus/index.html` — rebuilt (data-driven; corrected codes flow through).
- `tests/corpus-explorer.test.mjs`, `tests/news-stream.test.mjs`, `CLAUDE.md`, `HANDOFF.md`, `tests/smoke-checklist.md` — regate + docs (record the measured agreement rate + correction count).

## Exit Criteria

- [ ] The deterministic consistency audit (`ph34_audit.py`) emits the same-text-different-code contradictions + within-section outliers across the 1,376 new indicators, offline (no LLM).
- [ ] A BLIND neural re-assignment covers every one of the 1,376 new indicators (never shown the existing code) → an INTER-RATER AGREEMENT rate (C-axis + D-axis) + a disagreement list; the 14 records unmodified by T2.
- [ ] T2's disagreements + T1's contradictions clustered by (existing→proposed) code-pair/pattern; the user disposes each cluster (keep-existing / take-proposed / other); every flagged indicator has a recorded disposition.
- [ ] The dispositions applied byte-surgically via the reused `ph33_apply.py` deterministic downstream — `git diff` shows ONLY C/D + status/data/build_rec/build_logic; every `flag` and `red_flag` byte-identical; all affected records `--check-derived` clean.
- [ ] `build.py corpus` rebuilt; `--check all` 5/5 ZERO DRIFT; `--selftest` PASS; `validate_capability_taxonomy` + `validate_typology` clean (declared-but-unused handled if it arose); all 56 `--check-derived` clean; `node tests/corpus-explorer.test.mjs` green + news 65 byte-frozen.
- [ ] The MEASURED inter-rater agreement rate + correction count recorded in CLAUDE.md / HANDOFF.md + the journal (the honest quality artifact, NOT a demo number); the frozen set byte-clean; NO non-negotiable change.

## Constraints

- HONEST-AS-AGREEMENT — a second-LLM verification is CONSENSUS, not ground truth. Report inter-rater AGREEMENT, blind the re-assignment (never show it the existing code), let the human adjudicate disagreements. Prevents: a second-LLM pass becoming false confidence.
- No new demo number — the measured agreement rate is a journal/quality artifact; the always-on illustrative badge stays the only claim. Prevents: false precision.
- BYTE-SURGICAL apply — reuse `ph33_apply.py`'s deterministic downstream (cover×data matrix + per-capability build_logic templates); do NOT re-author build_logic neurally. The grounded `flag` and `red_flag` stay byte-identical. Prevents: collateral churn / ungrounded regeneration.
- SCOPE = the 14 new derived records only (1,376 new indicators). The 42 existing records / 875 old indicators stay FROZEN (they had the fuller Phase-28 interview treatment). Prevents: re-litigating already-interviewed assignments. Folding them in is a follow-up ONLY IF T2's measured rate comes back ugly.

## Checkpoints

- After T1 (the deterministic audit): report the contradiction + outlier count — sizes the problem before the neural pass.
- After T2 (the blind re-assignment): report the MEASURED inter-rater agreement rate (C-axis, D-axis) + the disagreement count — before T3's human adjudication. If the rate is UGLY (widely unreliable), STOP and surface (a wholesale re-derive may be the honest call; the 42 existing records may need folding in).

## Assumptions

- The taxonomy (`data/capability-taxonomy.json`) DEFINITIONS are correct and stable — only which code an indicator carries is in question. If false (a code's meaning is itself wrong): out of scope; surface rather than redefining a code mid-phase.
- A correction is unlikely to remove the last use of any C/D code at 2,251 indicators. If false: T5 checks `validate_capability_taxonomy` and handles declared-but-unused (accept it / surface) — never delete a taxonomy DEFINITION (that would be a definitions change, out of scope).

## Notes

- Reuse `ph33_apply.py`'s deterministic downstream (the cover×data matrix + the per-capability build_logic templates) — a corrected C/D code mechanically regenerates status/data/build_rec/build_logic. Do NOT re-author build_logic neurally.
- This is a DATA-correctness phase: `corpus.html` and `build.py` are data-driven, so corrected codes flow through on rebuild — NO UI feature work, NO build change.
- The taxonomy (`data/capability-taxonomy.json`) and the 14 records are committed and self-contained — no knowledge gap blocks the phase.
- Ties to the ground-judgments-in-a-user-interview principle (audit correctness, not just validity) — the user is the accepted truth source for the cluster-level adjudication, the same model as the Phase-28 interview.
