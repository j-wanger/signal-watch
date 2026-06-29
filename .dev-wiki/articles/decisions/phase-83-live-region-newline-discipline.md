---
title: "Phase 83: a build-stripped LIVE region must carry no trailing blank line"
aliases: [phase-83-live-region-newline, live-region-newline-drift, strip-newline-discipline]
category: decisions
tags: [agentification, merge, build-strip, live-region, newline-drift, dist-byte-identical]
parents: [phase-83-merge-adjudicator-oracle-scored]
created: 2026-06-29
updated: 2026-06-29
source: implementation
confidence: high
---

## Context

`build.py` strips the companion live overlay by matching a `/*LIVE_START*/.../*LIVE_END*/` region
with `LIVE_REGION_RE` and removing it. The regex eats the LEADING newline of the region (so the
surrounding code closes up cleanly). During Phase-83 T4, `--check merge` failed by exactly one
newline: the inserted region carried a TRAILING blank line before the next statement, and because the
strip already consumes the leading newline, the trailing blank produced a +1-newline drift in the
stripped output — `dist/merge` was no longer byte-identical.

## Decision

A `/*LIVE_START*/.../*LIVE_END*/` region must be inserted with **NO trailing blank line** before the
next statement. The strip eats the leading newline; a trailing blank double-counts. This is a
mechanical insertion rule for the live-region pattern, not a one-off `merge.html` fix.

Rejected: changing `LIVE_REGION_RE` to also consume a trailing newline — that would couple the regex
to a specific surrounding whitespace shape and risk the inverse drift on the other live targets
(corpus/news), whose existing regions already satisfy the no-trailing-blank rule.

## Consequences

- Reusable across the corpus / news / merge live-region pattern: insert the region flush against the
  following statement (no blank line after `/*LIVE_END*/`).
- `--check <target>` is the catch — a +1-newline drift is exactly the byte-identity failure it exists
  to surface; run it immediately after wiring a new strip.
- Pairs with [[phase-83-live-overlay-via-render-wrap]] as the two byte-identity guards for a
  build-stripped live overlay.
