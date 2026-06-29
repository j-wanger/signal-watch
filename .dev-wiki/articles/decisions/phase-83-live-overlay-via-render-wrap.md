---
title: "Phase 83: the LIVE overlay installs by WRAPPING render() inside the build-stripped region"
aliases: [phase-83-live-overlay-render-wrap, merge-live-overlay, live-wrap-not-monkeypatch]
category: decisions
tags: [agentification, merge, live-mode, build-strip, dist-byte-identical, render-wrap]
parents: [phase-83-merge-adjudicator-oracle-scored]
created: 2026-06-29
updated: 2026-06-29
source: implementation
confidence: high
---

## Context

The merge adjudicator's companion LIVE mode needs to add CSS, JS, and DOM to `merge.html` — the
agent's call + rationale beside the human gate, the post-disposition oracle match, a counts-only
agreement ledger. The non-negotiable: ALL of those bytes must sit inside the single build-stripped
`/*LIVE_START*/.../*LIVE_END*/` region so the offline `dist/merge` stays BYTE-IDENTICAL after
`build.py` strips the region (the §4.5 / dist-boundary constraint). Two structural traps: static
live CSS/HTML in the markup survives the strip (→ `dist/merge` drifts); and the page's screen
functions are captured by reference in a `CASE_SCREENS` array at definition time.

## Decision

Install the overlay by **wrapping the `render` function** (a reassignable function *declaration*)
inside the `/*LIVE_*/` region AND injecting its own `<style>` via JS at runtime — so every live byte
(CSS + JS + DOM) lives in the stripped region. The wrap targets `render()` because `CASE_SCREENS`
holds function *references* captured at definition; `render()` is the call site the array routes
through, so wrapping it (not the array entries, not the individual screen functions) is what actually
intercepts every screen.

Rejected: (a) static live CSS/HTML in the markup — it survives the strip, so `dist/merge` is no
longer byte-identical (the abort condition). (b) monkeypatching the screen functions — `CASE_SCREENS`
captured stale references, so reassigning the named functions after the array is built does nothing.

## Consequences

- `dist/merge` is byte-identical via `--check merge` after the strip (verified; the A3 contract held).
- The reusable pattern for any future build-stripped live overlay: find the single reassignable call
  site (here `render()`), wrap it in-region, inject styles via JS — never static live markup, never a
  reference-captured array entry.
- Pairs with the newline-discipline decision ([[phase-83-live-region-newline-discipline]]) — both are
  the byte-identity guards for the live-region pattern.
