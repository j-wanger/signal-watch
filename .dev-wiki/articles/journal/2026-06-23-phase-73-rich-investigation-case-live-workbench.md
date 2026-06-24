---
title: "Phase 73 — Rich investigation case in the LIVE workbench: the matched FILE/DISMISS pair, the affirmative-clear verdict, three named graphs"
aliases: ["Phase 73 debrief", "Northgate vs Lakeshore delivered", "rich case delivered"]
category: journal
tags: [phase-73, companion, rich-case, casefile, affirmative-clear, network, entity-resolution, standard, delivered]
parents: [phase-73-rich-investigation-case-live-workbench]
created: 2026-06-23
updated: 2026-06-23
source: debrief
duration: ~4h (post-compaction estimate — may undercount)
---

# Phase 73 — Rich investigation case in the LIVE workbench (delivered)

## What Happened

- Authored the north-star rich investigation case as the project's answer to "the workbench is
  terrible": ONE matched pair — **CASE-A "Northgate Hospitality Group Inc."** (files) and **CASE-B
  "Lakeshore Catering Group Inc."** (clears) — firing the SAME grounded signals (identical indicator
  ids C2 `fin-2023-alert001:IND-03` + C3 `fin-2020-alert001:IND-05` + C14 `fin-2025-a003:IND-09`) yet
  resolving OPPOSITELY on an authored identity/network layer. The thesis: *same grounded signal,
  opposite outcome — the network + the source of funds is the difference.*
- The direction was the user's REFRAME (the curated substrate cases are "not it": all C2/C3, synthetic
  ids, raw codes, no network). It INVERTS the pillar dependency — signal-watch AUTHORS the rich case
  first (the artifact is the spec), aml-substrate + aml-casework PARKED as downstream implementers. A
  15-agent design workflow (ground → 6 perspectives → synthesize → 3 critics → revise) produced the
  plan; the critics corrected 3 AML-realism errors pre-build.
- The user OVERRODE two of the four design-gate questions: ship target = EXTEND the COMPANION workbench
  so the live sufficiency engine actually RUNS over the rich data (not a precomputed dist); ceremony =
  STANDARD (two L tasks, all three graphs this phase, unified reviewer) — not the recommended LITE
  money-flow-only descope.
- Mid-implementation, AFTER T1 was marked [x], the user gave refining feedback (USER OVERRIDE escape
  hatch): specific date ranges (2–19 Apr / 2–21 Apr 2026), the two cases UNLINKED (removed CASE-B's
  references to Northgate/James-Calder/"the related case" + the shared `evidence_panel_ref`), and the
  excluded near-match reframed against a self-contained synthetic sanctions-watchlist entry (Jon A.
  Calderón). Standing rule captured: only cross-reference cases when there is a REAL link.
- STANDARD review gate ran (a 4-lens adversarial workflow + per-finding verify) → FIX-THEN-SHIP.

## Decisions Made

- [[phase-73-invert-pillar-dependency|Invert the pillar dependency — signal-watch authors the north-star rich case first; substrate/casework parked]]
- [[phase-73-extend-companion-workbench-not-new-dist|Ship target: extend the companion workbench (live engine), NOT a new offline dist]]
- [[phase-73-affirmative-clear-verdict-file-bar-unchanged|The affirmative-clear verdict — a separate clear path that never loosens the file bar (the A1 guard)]]
- [[phase-73-standard-ceremony-override|STANDARD ceremony override of the project LITE default]]
- [[phase-73-aml-correctness-dismiss-and-prior-str-routing|AML-correctness: the dismiss leads with affirmative reconciliation; the prior-STR sits on an inbound source]]

## Problems Solved

- **No honest "cleared" verdict in the live engine** (it had `{determination, needs_more_info}`; mapping
  Lakeshore's clear to `needs_more_info` would mislabel a documented dismissal) — solved with an ADDITIVE
  affirmative-`cleared` branch (mechanism + 0 legs + affirmative mitigation established) sitting AFTER
  `sufficient = not missing`; **the file/determination bar stays BYTE-IDENTICAL** (the A1 guard, proven
  by `evidence_requirements.py --selftest`).
- **Verdicts could read as authored-frozen strings, not engine output** — `serve_workbench` DERIVES the
  engine inputs from the EVIDENCE (caps from alerts; ML-A7 lit/suppressed by `kyc.source_of_funds` read
  from the file; ML-A4 from a resolved/flagged resolution_edge; ML-A5 from a caution-list/prior-STR hit;
  the predicate READ from the matched prior_str record) and runs the LIVE engine; the authored
  `expected_*` is a regression ORACLE only.
- **Review finding (should-fix, FIXED): `scOutcome` rendered bare internal entity ids**
  (E-CALDER/E-1187442/E-MARIC) as STR-claim provenance on CASE-A → resolved to display names via
  `scEntMap`/`scNameOf` (+ a new `.mjs` assertion closing the regex coverage hole).
- **Review finding (should-fix, FIXED): committed render fixtures were disconnected from the live
  computation** → added a json-equals fixture-DRIFT bridge in `serve_workbench --selftest`.
- Nits fixed: `_via()` neutral 'present' fallback (never falsely claim fired/read/gathered);
  `_cf_prior_str_hit` normalizes a raw register email (closes a silent-miss authoring trap);
  schema.md ML-A7 `via:read`→`via:fired`; `scBOGraph` ownership_pct `esc()` consistency.

## Open Questions

- None unresolved.

## Artifacts Changed

- `data/casefile/{case.json,schema.md}` (NEW companion data source — the authored matched pair; build.py
  reads none of it)
- `scripts/evidence_requirements.py` (the affirmative-`cleared` verdict + a `read`-from-file evidence
  source + predicate-from-register; the file bar byte-unchanged)
- `data/workbench/evidence-requirements.json` (the validated `affirmative_clear` block on the ML profile)
- `scripts/serve_workbench.py` (the casefile path: `load_casefile`/`casefile_determination`/
  `casefile_list`/`casefile_detail` + dispatch in `list_cases`/`case_detail`/`determine_case`; the
  fixture-drift bridge in `--selftest`)
- `workbench.html` (`showcaseSurface` — the rich render: 3 graphs names-not-codes, rail-aware
  counterparty panels, the caution chain + inbound prior-STR, the file-vs-dismiss fork)
- `tests/workbench.test.mjs` (+24 showcase assertions, 127→151), `tests/fixtures/casefile/{CASE-A,CASE-B}.detail.json` + `queue.json`, `tests/smoke-checklist.md`

## Related

- [[phase-73-rich-investigation-case-live-workbench|Phase 73 — Rich investigation case in the LIVE workbench]] — parent phase

## Soft Observations / Phase N+1 Candidates

- Money-flow graph legibility | the dense inbound side is hard to read — cap/group into a super-node |
  evidence: `workbench.html` `scMoneyFlowGraph`, the T4 render
- The cross-pillar contract doc | `docs/rich-case-target-contract.md` — the DEFERRED handoff naming what
  aml-substrate must EMIT (channel-aware counterparty identity, seeded shared identifiers, a named
  multi-edge BO graph, an address-keyed caution list + prior-STR register) and what aml-casework must
  SIGN/REFUSE/CLEAR (incl. CW-4: the live cleared-by-established-mitigation verdict + the txn-less
  party-leaf sign) | evidence: phase article Notes
- Roll the determination/affirmative-clear model across the triage + gate consoles (still
  disposition-only — carried from Phase 69/70) | evidence: _CURRENT_STATE Phase 73+ follow-ons
- The casework txn-less-contract follow-on (the 651 txn-less C14 party-leaf cases, sibling — carried
  from Phase 72) | evidence: Phase 72 frontier
- Breadth: more showcase cases / a second matched pair | evidence: the matched-pair architecture
