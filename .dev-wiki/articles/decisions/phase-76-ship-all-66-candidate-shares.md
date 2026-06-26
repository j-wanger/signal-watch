---
title: "Ship all 66 real candidate SHARES (completeness over sampling)"
aliases: ["full over-merge-refused residual", "no sampling of candidate SHARES"]
category: decisions
tags: [phase-76, merge-console, candidate-shares, honesty, sampling]
parents: [phase-76-merge-adjudication-console]
created: 2026-06-25
updated: 2026-06-25
source: plan
confidence: medium
---

## Context

The committed v0.5 slice yields 66 real candidate SHARES (distinct entity_refs sharing a strong
identifier — the over-merge-refused residual the spine declines to merge). For the queue, the choice
was whether to ship all 66 or sample a tighter demo subset. Sampling reads cleaner for a short
presentation but invites a "why these and not those" question.

## Decision

Ship all 66. Including the full over-merge-refused residual avoids any sampling-honesty question —
the queue's strong-basis group is the complete real-data population, not a curated cut. The cost is a
longer strong-basis group in the queue.

## Consequences

The strong-basis queue group is long (the full 66). The user flagged this as easy to cap later if a
tighter demo is wanted — capping is a presentation-only change (a queue limit, not a data or honesty
change), so it stays reversible. Completeness over sampling is the honest default; a cap, if added,
should be a disclosed `slice_rule`-style limit, not a silent subset. (Confidence medium: this is a
demo-shape call the user explicitly left open to revisit.)
