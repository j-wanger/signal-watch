---
title: "Phase 73 engine: the affirmative-clear verdict — a separate clear path that never loosens the file bar (the A1 guard)"
aliases: ["affirmative-clear verdict", "cleared not needs_more_info", "the file bar never loosens", "A1 guard"]
category: decisions
tags: [phase-73, evidence-sufficiency, determination, honesty, A1, file-bar, cleared]
parents: [phase-73-rich-investigation-case-live-workbench]
created: 2026-06-23
updated: 2026-06-23
source: plan→delivered
confidence: high
---

## Context

The thesis is "same grounded signal, opposite outcome": Northgate FILES (a `determination`), Lakeshore
CLEARS. But the LIVE engine has no honest "cleared" verdict today — `evaluate_sufficiency` returns
`{determination, needs_more_info}` (evidence_requirements.py), and `needs_more_info` reads as "haven't
looked yet / go gather", NOT "investigated and affirmatively cleared". Mapping Lakeshore's clear to
`needs_more_info` would mislabel a documented dismissal as an open investigation; the naive fix —
widening the determination/FILE bar so the clear-vs-file split falls out of one threshold — would let a
weaker file bar through, the exact failure the honesty posture forbids. This is the T0 weakest
assumption: the new verdict must add a clear path WITHOUT touching the file side.

## Decision

Add a SEPARATE affirmative-clear verdict — mechanism fired + corroborating legs ABSENT + affirmative
mitigation AFFIRMATIVELY ESTABLISHED (source-of-funds established + business reconciliation +
historical-behaviour fit) → a principled `cleared`, distinct from `needs_more_info`. **The file bar
(mechanism + ≥2 INDEPENDENT legs + named predicate + no unrebutted mitigation) stays BYTE-IDENTICAL.**
The clear path REQUIRES positive clean evidence; it widens nothing on the file side. A RED test guards
both directions: a Lakeshore-shape case (no-legs + established mitigation) → `cleared`; a non-affirmative
no-legs case (no established mitigation) → still `needs_more_info`; Northgate-shape → `determination`;
the file bar's existing cases unchanged. GUARD/ABORT: if the only way to clear Lakeshore is to weaken
the file bar or fabricate evidence the authored data doesn't carry → STOP-and-surface (do not loosen,
do not fake).

## Consequences

- The engine gains a third honest verdict; the determination/FILE gate is provably unchanged
  (regression-tested), so the contrast is real, not an artifact of a loosened threshold.
- `cleared` requires AFFIRMATIVE clean evidence (established source + reconciliation + history) — never
  "no negative hit", which is AML-wrong for clearing a funnel alert.
- The new verdict is the one engine extension this phase makes to a sacred control — it earns the
  STANDARD reviewer dispatch.
- Lakeshore's `clearance_record` is documented-by-substance (the reconciled sources + established
  source-of-funds + historical-consistency basis), retained-for-audit, NEVER branded "defensive filing".
