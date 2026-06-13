---
title: "Phase 49: Triage-loop embryo made demo-able — §14 as a fifth ship artifact"
type: decision
status: approved
confidence: high
source: plan
created: 2026-06-12
updated: 2026-06-12
tags: [triage-loop, adjudication, lfcm, gate-console, synthetic-history, ship-artifact]
---

# Phase 49: Triage-loop embryo made demo-able

## Context

Phase 48 closed (blueprint §12–§15 + synthetic-history probe + offline blueprint report;
committed 83e4218, gate flip e53f8f0). The user picked the **§14 triage-loop embryo** at the
Phase-49 direction question (no reframe — first time in 3 gates the recommended option was
taken as offered). Blueprint §14 names the gate console (Phase 47) as the loop's committed
embryo: "same arc … pointed at a continuous scenario stream instead of a one-off divergence
set."

Substrate inventory (measured at plan):
- `data/probe-history/alert-history.json` — 44 SYNTHETIC alerts, each a 6-field stub
  ({alert_id, entity_id, rule_id, analyst, date, disposition}; dispositions: dismissed /
  escalated / sar_filed / data_requested; re-review, inconsistency, and data-request patterns
  deliberately seeded). **No judgable fact pattern per alert** — evidence panels must be
  authored.
- `data/probe-history/legacy-rulebook.md` + `derived/` — 12 rules, 12/12 gate-green through
  the unchanged gate (Phase 48 T5a).
- `console.html` → `dist/console/` — the Phase-47 Class-J arc (Queue → Evidence → graded
  Disposition w/ required rationale → Record reveal → session Ledger), 213 real C/D cases.
- `data/capability-taxonomy.json` — C1–C28 / D1–D20 (the need-more-info picker's vocabulary).

## Decision

**D1 — Deliverable shape: a FIFTH ship artifact, `triage.html` → `dist/triage/index.html`;
the gate console stays byte-frozen.** The repo precedent (corpus, news, console were each
born separate to keep the prior artifact byte-untouched) + presentation safety (console just
shipped and was demoed into the M9 story). Rejected alternative: extending console.html in
place (unfreezes a just-shipped dist; conflates two different gates — Class-J divergence
adjudication vs the daily triage loop).

**D2 — Scenario source: a NEW committed SYNTHETIC dataset `data/triage/scenarios.json`,
deterministically curated by `scripts/curate_triage_scenarios.py`** (the
curate_console_cases.py precedent: authoring-time regeneration-only; build.py reads only the
committed JSON) from: the probe-history rulebook + alert stubs (replayed, evidence panels
AUTHORED synthetic) + committed corpus indicators (the synthetic-novel stratum — typologies
from the ingestion frontier not in any historical alert, exactly §14's wording). Phase-48's
"probe outputs outside every build.py-read path" constraint is consciously superseded for
the NEW dataset only (probe-history itself stays outside build paths; the curate script
reads it at authoring time) — surfaced as gate assumption A2.

**D3 — The four §14 strata + controls are first-class data:** every scenario carries a
stratum (history-signal-fired / history-below-the-line / synthetic-novel /
random-population, closed vocab) + interleaved known-disposition CONTROL scenarios +
double-assignment markers (dramatized agreement instrumentation). Build-boundary validation:
strata closed-vocab, rule refs ground in the probe derived record, C/D refs in the taxonomy,
synthetic meta flag mandatory.

**D4 — The disposition grammar is §14's, including the load-bearing one:** confirm-risk /
confirm-no-risk / both-defensible / escalate + **"I need more information (naming which)"**
wired to a C/D-taxonomy picker — every need-more-info disposition lands in the discovery
ledger as a measured data-gap observation per D-code. Rationale required (empty records
nothing — the console rule).

**D5 — The reveal is decisions-not-correctness (the Phase-48 A1 condition carried forward):**
the historical disposition is shown as what the institution decided, never as ground truth;
seeded process inconsistencies (same fact pattern, divergent historical dispositions)
surface at the reveal for adjudication, never auto-resolved. The session ledger closes with
the §14 discovery outputs: signal gaps / data gaps per D-code / process inconsistencies /
policy gaps + an agreement panel labeled **"chosen, not measured"** where parameters appear.

**D6 — Licence simplicity for the novel stratum:** synthetic-novel scenarios quote committed
corpus indicators; the novel stratum sources US-federal (public-domain) indicators ONLY,
pre-committed as an allowlist in the curate script (the FIXTURE_META pattern) — no live
"or the footer ports" branch (subtraction test; reviewer-tightened).

**D7 — Evidence panels have a NAMED verifier (reviewer finding — the Phase-47 D2 doctrine
applied to ourselves):** one evidence panel per FACT PATTERN, shared BY REFERENCE across the
divergent-disposition pair — fact-pattern identity for the process-inconsistency beat is
STRUCTURAL, validated at the build boundary, never an authored coincidence. Panel skeletons
are template-derived deterministically from rule logic + stub fields ({rule fired, entity,
date, disposition}); the authored synthetic layer on top stays thin. Scope ceiling: ~16
scenarios across the 4 strata + ~4 known-disposition controls (bounds the A3 authoring
risk). Each scenario carries fired-rule state (rule_id | none for below-the-line/random
strata) so the signal-gap discovery output is DERIVABLE, not asserted.

**D8 — No fake instrumentation (reviewer finding):** "chosen, not measured" covers
parameters; VALUES are a different class. Any agreement-looking number renders ONLY as
deterministic arithmetic computed at render time from the committed synthetic dataset, each
with a measurement definition (the probe_history_stats class) — never a typed-in figure.
Double-assignment is dramatized honestly: seeded, LABELED second-rater dispositions in the
committed data (replayed at the reveal), not simulated-live agreement. The policy-gap
discovery output gets a real capture mechanism: a grammar escape "no defensible option —
flag for policy review" (rationale required); without it the ledger line is decorative.

## Alternatives considered

**Instrument-first (the T0.2 fork):** extend the 213-case console with strata +
need-more-info and run the loop on ourselves over real divergences. Cheaper; makes the loop
REAL before dramatizing it. Rejected as the primary shape because the 213 divergence cases
are not alert history — there is no historical *disposition* to reveal, so the loop's
defining beat (judgment vs what the institution actually decided) cannot be shown on that
data. Not mutually exclusive long-term — the natural follow-on phase once real divergence
streams exist (sequencing, not dismissal). Falls back in if A1 rejects.

**Non-ship offline artifact (reviewer finding — the repo's own middle shape):**
`docs/triage-loop.html` on the booth.html / blueprint-report precedent (no build.py target,
no dist freeze, no node harness; promote to ship-class only after the embryo survives one
presentation). Defers the fifth-artifact overhead. Counter-consideration: an INTERACTIVE
artifact presented to stakeholders without a test harness is presentation risk the console
deliberately paid down (68 tests); ship-class discipline is what makes it safe to demo.
Surfaced at the gate as A4's explicit either/or.

## Gate outcome (assumption gate closed 2026-06-12; all_accept: false; ledger block in assumption-ledger.md)

- **A1 (HIGH) demo-first — ACCEPT.** The triage-loop embryo is an artifact to present
  (bank-audience class), not an internal instrument; instrument-first stays the natural
  follow-on (sequencing, not dismissal).
- **A2 data path — DON'T-KNOW round 1 → defended → ACCEPT round 2.** Defense: Phase-48 A4's
  verbatim text scopes the probe's OWN files + __CORPUS__ (untouched here); the
  data/console/cases.json curation precedent ("validation never reads git"); §14 itself
  prescribes history replayed as scenarios. Curate script reads probe-history at AUTHORING
  time only; build.py reads only the committed, build-boundary-validated scenarios.json.
- **A3 authored evidence panels — ACCEPT** (mitigated by D7: template-derived skeletons,
  structural panel sharing, ~16+4 ceiling).
- **A4 fifth SHIP artifact — ACCEPT** (full discipline: build target, --check, dedicated
  harness; the non-ship docs/ shape surfaced and declined).

Reviews: approach 7/10 → revised (D7 panel verifier + D8 no-fake-instrumentation added);
plan 7/10 → revised → 9/10 ACCEPT.
