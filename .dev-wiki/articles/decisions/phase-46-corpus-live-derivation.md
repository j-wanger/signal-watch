---
title: "Phase 46 direction: corpus live derivation mode — local-model agentic derivation through the frozen gate"
aliases: [phase-46-direction, corpus-live-mode, opencode-derivation-harness]
category: decisions
tags: [live-mode, corpus, local-model, opencode, derivation, m7, m8]
parents: [phase-46]
created: 2026-06-10
updated: 2026-06-11
source: plan
confidence: medium
---

## Context

Phase 45 delivered the presentation-polished corpus demo (presents to bank stakeholders
2026-06-11). At the Phase-46 dev-plan direction question the user reframed off all five carried
DEFERRED candidates (the 5th reframe at 6 consecutive gates): **"live mode with local model for
the corpus demo as well, ideally with a better harness integration like opencode"** — plus a
pasted practitioner research report on opencode + local models and driving opencode from Claude
Code (maker/checker architecture).

Today the corpus is BUILD-TIME only: the inverted extraction loop (LLM extracts
`derived/<id>.json` from `<id>.md`; `derive_signals.py --check-derived` gates) has been executed
manually in-session across phases 14–34. The news stream has the only live mode
(`serve_news.py`, hand-rolled llama-cpp proxy, single-shot extraction + grounded-or-stripped
gate). The corpus has no live derivation capability.

Environment measured at planning: opencode NOT installed (bun present); llama-server RUNNING at
127.0.0.1:8080 (the news Qwen, top_k 20 / top_p 0.8); serve_news not running.

## Decision

APPROVED at the assumption gate 2026-06-10 (A1–A4 ALL accept — warned + restated per protocol;
ledger block in `.dev-wiki/assumption-ledger.md`). Phase 46 = **corpus live derivation mode**: a companion-served,
dev/authoring-time live mode where a local model derives a NEW advisory document (md/URL →
red-flag indicators + C/D tags + coverage) through the EXISTING frozen gate
(`derive_signals.py check_record` — quote-grounding, cover×data matrix, red_flag shape), with
only gate-green output rendering into the corpus arc.

The harness question is PROBE-GATED, not pre-decided: T1 installs opencode + configures the
local llama-server provider and measures the derive-until-gate-green agent loop (gate pass
rate, iteration count, wall time, tool-call reliability) on ONE held-out document (a FINTRAC
/intel/ frontier doc — composing with the deferred C1 candidate as test material), against a
direct serve_news-pattern pipeline baseline on the same doc. Adopt opencode only if it earns
its complexity (the agentic iterate-on-gate-failure loop is the capability a single-shot
pipeline cannot give); otherwise the phase still ships live corpus mode on the proven pattern.

Alternatives considered: (B) skip opencode entirely, extend the serve_news.py pattern — simpler,
proven, but forfeits the agent loop that distinguishes corpus derivation (multi-field records,
gate iteration) from news extraction (single-shot + drop); (C) opencode as general dev tooling
(maker/checker for building signal-watch itself, per the pasted report's Part 2) — a different
phase entirely; surfaced at the gate as the A1 reading check.

## Consequences

- The corpus gains the live/authoring capability the news stream already has; the inverted
  extraction boundary (LLM extracts, deterministic layer gates) extends from in-session manual
  derivation to an automated local-model loop — the "live layer is becoming a real tool"
  trajectory applied to M7.
- Offline non-negotiables hold by construction: corpus.html live code in /*LIVE_START*/ regions,
  build-stripped, dist/corpus byte-identical; live mode optional/isolated/off-by-default.
- Live-derived records are DISPLAY/PROPOSE-only; committing a new derived record to data/
  remains a separate human-reviewed act under the existing licence rules.
- Presentation 2026-06-11 outranks the phase: nothing presentation-touching moves before it.
- Risk accepted: opencode is a fast-churning dependency (releases every few hours, headless
  permission bugs, quant-sensitive tool-calling per the user's report) — mitigated by the T1
  probe gate + the direct-pipeline fallback.

## Outcome (T1 checkpoint, 2026-06-11)

DIRECT serve_news-pattern pipeline + ONE violation-guided retry CHOSEN over opencode adoption
(user checkpoint taken). Measured on the same held-out doc (FINTRAC-2024-OA001, LOCAL-ONLY):
IDENTICAL 17/17 indicators from both harnesses, both gate-green FIRST shot, 0 violations;
direct 82.6s / 1 strict-schema streamed call vs opencode 1.17.3 255.1s (3.1×) / 7 tool calls /
0 tool-call failures. The differentiator (iterate-on-gate-failure) NEVER ENGAGED — consistent
with Phase-44 (failures gate-class, not model-class); subtraction test: a fast-churn external
dependency for a loop that didn't fire = unearned complexity. The loop's one real idea folded
in as the deterministic retry; opencode stays installed for dev use. Cross-harness C/D tag
agreement C 12/17 / D 15/17 — inside the Phase-34 blind inter-rater band (tags remain the
unguarded neural dimension; human review carries it). The news-side lift eval is explicitly
SEPARATE from Phase 46 (staged ready-to-run in `.dev-wiki/tmp/ph46/`). Full report:
`.dev-wiki/tmp/ph46/ph46_probe.md`.
