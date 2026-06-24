---
title: "Phase 73: Rich investigation case in the LIVE workbench — the matched FILE/DISMISS pair, rail-aware counterparty network, entity resolution, and the affirmative-clear verdict"
aliases: ["rich investigation case", "the matched FILE/DISMISS pair", "Northgate vs Lakeshore", "north-star rich case"]
category: phases
tags: [companion, rich-case, casefile, evidence-sufficiency, network, entity-resolution, affirmative-clear, north-star, standard]
parents: []
created: 2026-06-23
updated: 2026-06-23
source: plan→delivered
status: active
scope: ["data/casefile/**", "scripts/evidence_requirements.py", "data/workbench/evidence-requirements.json", "scripts/serve_workbench.py", "scripts/curate_workbench_cases.py", "workbench.html", "tests/casefile.test.mjs", "tests/workbench.test.mjs", "tests/smoke-checklist.md", "docs/case-workbench.md", "docs/evidence-driven-filing.md"]
entry_criteria: "Phase 72 DELIVERED + accepted; the live companion workbench runs (serve_workbench + evidence_requirements + workbench.html); the live engine's verdict vocab is {determination, needs_more_info} (evidence_requirements.py) and disposition {cleared, escalated, needs_more_info} (serve_workbench.py); the user's reframe verified against the live workbench/data/engine (the curated substrate cases are all C2/C3, synthetic ids, raw codes, no network); spec generated (STANDARD ceremony); direction gate CLOSED (assumption-ledger Phase-73, all_accept:true with the A1 guard)."
exit_criteria: "The live workbench surfaces the matched pair at the top of the queue; the EXTENDED engine COMPUTES `determination`→file for Northgate and the new affirmative-`cleared` for Lakeshore over the AUTHORED evidence (not frozen strings); all three graphs render with real names (money-flow txnNetwork, entity-resolution shared-identifier edges incl. excluded near-match, named-BO via display_name fixing the :695 party_id bug); names-not-codes throughout; the file/determination bar is PROVABLY unchanged (regression-tested); the metric-token sweep fires on a poisoned string; `--check all` 8/8 byte-frozen (companion-only, no dist drift); `node tests/casefile.test.mjs` (or the workbench arc) + the python selftests + `uv run pytest` green; STANDARD 7-category self-check + the unified reviewer pass; CLAUDE.md trued up."
---

# Phase 73: Rich investigation case in the LIVE workbench — the matched FILE/DISMISS pair, rail-aware counterparty network, entity resolution, and the affirmative-clear verdict

## Objective

Author ONE matched pair of cases in the LIVE companion workbench — **CASE-A "Northgate Hospitality
Group Inc."** (files) and **CASE-B "Lakeshore Catering Group Inc."** (clears) — that fire the SAME
grounded signals (identical indicator ids: C2 rapid pass-through `fin-2023-alert001:IND-03` + C3 funnel
fan-in `fin-2020-alert001:IND-05` + C14 source-not-established `fin-2025-a003:IND-09`) yet resolve
OPPOSITELY, driven only by an authored identity/network layer. THE THESIS: *same grounded signal,
opposite outcome — the network + the source of funds is the difference.* The determination is
**computed by the LIVE engine** over the authored evidence (not a precomputed dist): the extended
`evaluate_sufficiency` produces `determination`→file for Northgate and a NEW affirmative-`cleared`
(distinct from `needs_more_info`) for Lakeshore. Rail-aware counterparty identity (channel WIRE/EMT/AFT/
P2P + named counterparties + populated country), a traceable money-flow network with real names,
shared-identifier entity resolution (strong email/phone vs weak address), a multi-hop named-BO
ownership chain into an address-keyed caution list, a prior-Human-Trafficking-STR link on an INBOUND
source; names-not-codes everywhere; all three graphs wired.

## Scope

Companion-only — NO ship target; the 8 offline dists stay byte-frozen. Files and modules affected:
- `data/casefile/**` — the authored matched-pair dataset (`case.json`) + `schema.md` (synthetic; the
  expected engine verdicts authored as the test oracle)
- `scripts/evidence_requirements.py` + `data/workbench/evidence-requirements.json` — the live engine:
  read-from-file (`via:read`) + gathered (`via:gathered`) evidence sources, caution_list/prior_str
  gather kinds, predicate read-from-register, and the AFFIRMATIVE-CLEAR verdict (the file bar UNCHANGED)
- `scripts/serve_workbench.py`, `scripts/curate_workbench_cases.py` — load + serve + COMPUTE the
  determination over the showcase pair; surface it at the top of the queue
- `workbench.html` — names-not-codes; rail-aware counterparty panels; the three graphs (money-flow
  `txnNetwork`; entity-resolution shared-identifier edges incl. the excluded near-match; named-BO via
  `display_name`, fixing the `:695` `party_id` bug); the caution-list ownership chain; the inbound
  prior-STR panel (own synthetic marker); the file-vs-dismiss fork; "N pct" not "%"
- `tests/casefile.test.mjs` (or the workbench arc) + `tests/workbench.test.mjs`, `tests/smoke-checklist.md`,
  `docs/case-workbench.md`, `docs/evidence-driven-filing.md`, `CLAUDE.md`

## Exit Criteria

- [x] T1: `data/casefile/{case.json,schema.md}` author the matched pair (rail-aware txns + named
      counterparties + populated country; resolution_edges email/phone strong, address weak —
      strong-on-address forbidden; multi-hop named ownership_edges; address-keyed caution_list;
      prior_str_register HT predicate on an INBOUND source; the EXPECTED engine verdict authored as the
      test oracle) — all synthetic (.test/.example, 555-01XX); the python invariant check passes
      (identical signal_ids across the pair; all entities synthetic_label; no strength:'strong' on
      kind:'address'; the two expected verdicts present)
- [x] T2: `evidence_requirements.py` + `evidence-requirements.json` gain read/gathered evidence sources,
      caution_list/prior_str gather kinds, predicate read-from-register, and the AFFIRMATIVE-CLEAR
      verdict; THE FILE BAR STAYS BYTE-IDENTICAL — `evidence_requirements.py --selftest` green with the
      new RED cases (Lakeshore-shape→cleared; Northgate-shape→determination; a non-affirmative no-legs
      case still needs_more_info; the file bar unchanged)
- [x] T3: `serve_workbench.py` loads + serves + COMPUTES the determination over the showcase pair,
      surfaced at the top of the queue — `serve_workbench.py --selftest` covers the two computed verdicts
- [x] T4: `workbench.html` renders names-not-codes; rail-aware counterparty panels; all three graphs
      (money-flow / entity-resolution incl. excluded near-match / named-BO via display_name fixing the
      :695 bug); the caution-list ownership chain; the inbound prior-STR panel (own synthetic marker);
      the file-vs-dismiss fork; "N pct" — the casefile/workbench node test (added T5) + grep guards
      pass (no bare code; badge present)
- [x] T5: tests + drift — the workbench `.mjs` test covers the live verdicts, 3 graphs, ER
      resolve/excluded-near-match, names-not-codes, XSS, keyboard guards, both motion modes; the python
      selftests green; `python3 scripts/build.py --check all` 8/8 byte-frozen

## Constraints

- **A1 (the load-bearing guard) — the affirmative-clear verdict must NEVER loosen the file bar.** The
  new `cleared` verdict (mechanism fired + legs absent + affirmative mitigation established) is a
  SEPARATE clear path that requires positive clean evidence; the file/determination bar (mechanism + ≥2
  INDEPENDENT legs + named predicate + no unrebutted mitigation) stays BYTE-IDENTICAL.
  *Prevents: a richer demo laundering a weaker file gate / a fabricated clear.*
- **Companion-only (A0/A6)** — NOT a 9th ship target; build.py imports no casework/substrate/companion
  layer; the 8 offline dists stay BYTE-FROZEN (`--check all` 8/8); the rich case is served + computed by
  the live workbench, never inlined by build.py; the cross-pillar contract doc is a DEFERRED follow-on
  (`docs/rich-case-target-contract.md`), substrate/casework PARKED.
  *Prevents: a companion edit leaking into a ship artifact / a sibling import into build.py.*
- **A2 — verdicts are live-engine OUTPUT over authored evidence**, never authored-frozen strings; T1
  authors the expected verdict as a test ORACLE, T2 makes the engine produce it, T3 serves the engine's
  actual output. *Prevents: the demo telling a story the engine can't actually compute.*
- **A4 (the honesty governor)** — demo-visible RICHNESS + DEFENSIBILITY only, NEVER a catch-rate /
  detection-lift / precision claim; the contrast is QUALITATIVE; structured facts (ownership pct → "N
  pct", identifiers, the HT predicate) read from the RECORD never the model (the Phase-66 guard); every
  value synthetic-by-construction (.test/.example emails, 555-01XX phones, authored-pool addresses → a
  shared-identifier match can only resolve two synthetic parties); always-on badge + a per-panel
  synthetic marker on the prior-STR panel. *Prevents: a "harder to detect / better catch" framing / a
  model-authored structured fact.*

## Checkpoints

- After T1 (the load-bearing data authoring): the matched-pair invariant check must pass (identical
  signal_ids; all synthetic_label; no strong-on-address; both expected verdicts present) before the
  engine work begins.
- If clearing Lakeshore requires WEAKENING the file/determination bar or FABRICATING evidence the
  authored data doesn't carry (A1 false) → STOP-and-surface (do not loosen the gate, do not fake).
- If the live engine cannot be made to COMPUTE the two verdicts over the authored evidence without
  authored-frozen strings (A2 false) → STOP, surface the live-engine path as blocked.
- If any render/doc reads as a catch-rate / detection-lift / precision improvement → re-word (the
  honesty governor). If a structured fact would render from the model rather than the record → record-
  source it, never render the fabrication (the Phase-66 lesson).

## Assumptions

- A0 [boundary, accept] companion-only; build.py imports no sibling/companion; the 8 dists byte-frozen.
  If a sibling/companion import sneaks into build.py or a dist drifts → STOP-and-surface.
- A1 [T0 weakest, accept-with-GUARD] the live engine can express an honest affirmative-`cleared` WITHOUT
  moving the file bar. If the only way to clear Lakeshore is to weaken the file bar or fabricate evidence
  → STOP-and-surface.
- A2 [accept] the rendered verdicts are engine OUTPUT over authored evidence, not authored-frozen
  strings. If the engine can't yield the right verdicts without fabricated evidence → STOP (the A1 guard).
- A3 [accept] the three graphs render over the authored data REUSING the existing dependency-free layout
  engines (`liveGraphLayout`/`boGraphHTML`), `boGraphHTML` fed `display_name` not `party_id` (fixing the
  :695 violation). If a shape diverges → a small local adapter.
- A4 [honesty governor, accept] everything is demo-visible richness + defensibility, NEVER a
  catch-rate/lift/precision claim; structured facts record-sourced; synthetic-by-construction; badge +
  the prior-STR synthetic marker. If a framing reads as "harder to detect / better catch" → re-word.
- A5 [ceremony, accept — user override] STANDARD ceremony (spec + full 7-category self-check + unified
  reviewer; two L tasks) — a conscious override of the project LITE default.
- A6 [scope, accept] the cross-pillar contract doc stays DEFERRED to a follow-on
  (`docs/rich-case-target-contract.md`), touching no sibling code; substrate + casework PARKED.

## Notes

STANDARD phase (user override of the project LITE default — decision
[[decisions/phase-73-standard-ceremony-override]]). The five planning decisions (confidence as noted,
source plan):

1. **Invert the pillar dependency** — signal-watch AUTHORS the north-star rich case first; the artifact
   is the spec; substrate/casework parked ([[decisions/phase-73-invert-pillar-dependency]], high).
2. **Extend the companion workbench (live engine), NOT a new offline dist** — the user overrode the
   dist recommendation so the live sufficiency engine actually RUNS over the rich data
   ([[decisions/phase-73-extend-companion-workbench-not-new-dist]], high).
3. **The affirmative-clear verdict** — a separate clear path (mechanism + legs-absent + affirmative
   mitigation established → `cleared`) that NEVER loosens the file bar (the A1 guard)
   ([[decisions/phase-73-affirmative-clear-verdict-file-bar-unchanged]], high).
4. **STANDARD ceremony override** — accept two L tasks + all three graphs this phase
   ([[decisions/phase-73-standard-ceremony-override]], medium).
5. **The two AML-correctness calls** — the dismiss leads with affirmative reconciliation + established
   source (clearing a funnel alert on "no negative hit" is AML-wrong); the prior-HT-STR sits on an
   INBOUND funds source, the outbound controller is a DIFFERENT identity
   ([[decisions/phase-73-aml-correctness-dismiss-and-prior-str-routing]], high).

The direction is the user's REFRAME, verified against the live workbench/data/engine before planning
(memory [[reframes-to-output-quality]]): the curated substrate cases are "not it" (all C2/C3, synthetic
ids, raw C-codes, no counterparty/identity/network, an STR that drafts without the info). A 15-agent
design workflow (ground → 6 design perspectives → synthesize → 3 adversarial critics → revise; the
critics corrected 3 AML-realism errors) produced the plan.

Honesty seam VERIFIED in-repo at planning (not asserted): the live engine's verdict vocab is
`{determination, needs_more_info}` (evidence_requirements.py:348) and disposition `{cleared, escalated,
needs_more_info}` (serve_workbench.py:182) — the plan's earlier `{file, documented_dismissal}` strings
do NOT exist; the schema records them as DIST-PRESENTATION LABELS mapped from the real atoms
(determination→escalated→file; needs_more_info+established-mitigation→cleared→documented_dismissal). The
live txn key is `channel` (not `rail`), values WIRE/EMT/AFT/P2P/CARD/CASH/CHEQUE, counterparty_country
0/25,391 null today → the data model mirrors `channel` and POPULATES country; the named renderers
(`liveGraphLayout`/`boGraphHTML`) live in the companion `workbench.html` (in-place extension, no
re-home). The `_BANNED` metric-token + "N pct"-not-"%" sweep is NET-NEW (build.py has only the showcase
lift validators) with a RED test (a poisoned "94% precision" string must fail validation), scoped to
case.json STRING VALUES so CSS "%" is untouched.

The claim most likely to be wrong (named at planning): that the determination/clear verdicts are
honestly computable over the authored evidence WITHOUT loosening the bar. Defense: the new `cleared`
verdict is a SEPARATE path requiring affirmative clean evidence; the file bar is regression-tested
byte-identical; the via-tag referential integrity (via:'fired' must cite an alert in alerts[]; via:'read'/
'gathered' must reference a present record) is the guard against authored-frozen-masquerading-as-fired.
If the engine can't compute the two verdicts without fabricated evidence → the A1/A2 STOP fires.

Direction gate 2026-06-23 (all_accept:true — warned + restated; the load-bearing risk is A1, defended
by a hard STOP not a silent pass). Ledger Phase-73 block. Grounded against signal-watch HEAD (Phase-72
delivered) / the live workbench (355 cases) / `evidence_requirements.py` verdict vocab verified
in-repo. The deferred cross-pillar contract (`docs/rich-case-target-contract.md`) names what aml-substrate
must EMIT (channel-aware counterparty identity, seeded shared identifiers, a named multi-edge BO graph,
named source-party identity, an address-keyed caution list + prior-STR register, a historical baseline)
and what aml-casework must SIGN/REFUSE/CLEAR (channel identity grounding, exact-on-identifier ER, the
txn-less party-leaf sign — the carried Phase-72/73 no-transactions frontier — and CW-4: the live
cleared-by-established-mitigation verdict it must add).
