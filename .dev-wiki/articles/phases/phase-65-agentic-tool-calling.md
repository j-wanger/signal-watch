---
title: "Phase 65: Agentic tool-calling — the investigator evidence-gathering loop (companion)"
aliases: [agentic tool-calling, tool-evidence, gather beat, evidence-gathering loop, OSINT loop, network-ER]
category: phases
tags: [m9, lfcm, agentic, tool-calling, grounding, workbench, live, network-er, companion]
parents: []
created: 2026-06-21
updated: 2026-06-21
source: plan
status: active
scope:
  - "scripts/serve_workbench.py"
  - "workbench.html"
  - "data/osint/** (new committed synthetic corpus)"
  - "tests/workbench.test.mjs"
  - "tests/test_selftests.py"
  - "docs/case-workbench.md"
  - "tests/smoke-checklist.md"
  - "scripts/build.py (NO substrate/casework import — companion-only, no build target)"
entry_criteria: "Phase 64 delivered + accepted (committed 0ee4489); the workbench (workbench.html + serve_workbench.py, companion-only, NOT a build target) serves the 200-case slice + the gating engine + the live finale. Feasibility code-verified this session via an Explore scout: NO multi-step agent-loop primitive exists (every companion is single-shot call_llm — this phase authors the first; BUILD-NEW); news_ground.locate_span/ground_record are pure stdlib already shared build↔live (REUSABLE — tool-evidence grounds identically); liveGraphLayout is pure JS (REUSABLE) but news_store [DuckDB] is companion-doctrine-bound (reference, don't import); the plug-in point is clear (SIGNALS → DECIDE); NO synthetic OSINT corpus exists (the phase authors one)."
exit_criteria: "Signal-watch's FIRST multi-step tool-calling agent loop authored + the grounding seam HELD: on a selected case, the agent proposes a tool → calls a deterministic tool over a COMMITTED SYNTHETIC corpus → each finding GROUNDED-OR-STRIPPED via the reused news_ground gate (a finding's claim ⊂ the tool's returned text; ungrounded findings DROP) → grounded tool-evidence extends the case grounding chain + feeds a liveGraphLayout network view. The GATHER beat in workbench.html (stage-completion reveal — never a token stream — the ungrounded-dropped surfaced honestly, the evidence network, badge, both motion modes, XSS-escape); backend by NAME + capped iterations + deterministic-STUB fallback (demo runs model-free); the loop EXECUTED ONCE live over a marquee case (grounded + dropped evidence captured as delivery evidence). serve_workbench.py --selftest + node tests/workbench.test.mjs + uv run pytest green; build.py --check all 8/8 ZERO dist drift; no substrate/casework import; news_store NOT imported; companion-only (NOT a 9th build target)."
---

# Phase 65: Agentic tool-calling — the investigator evidence-gathering loop (companion)

## Objective

Build signal-watch's FIRST multi-step tool-calling agent loop — the one remaining signal-watch-LOCAL
Phase-63 follow-on (OSINT / counterparty gathering / network-ER; tool-evidence extending the grounding
chain), and the next move on the LFCM path: a NEW grounding modality. Add a GATHER beat to the workbench
arc (between SIGNALS and DECIDE): on a selected investigator case, a companion agent loop gathers
counterparty/OSINT/adverse-media evidence over a committed synthetic corpus; the reused `news_ground`
gate disposes; grounded tool-evidence extends the case's grounding chain + feeds a network view.
Companion-only (a `serve_workbench.py` + `workbench.html` extension, NOT a 9th ship target); the loop is
session-only and persists nothing; `--check all` stays 8/8 with ZERO dist drift.

**The starting point (code-verified this session via an Explore scout):**
- **Agent loop = BUILD-NEW (the hard part).** No multi-step / tool-calling primitive exists anywhere —
  serve_news / serve_corpus / serve_chain / serve_workbench all call the model single-shot (`call_llm`);
  serve_corpus's violation-guided RETRY is deterministic control flow, not an agent loop. This phase
  authors the first.
- **Grounding gate = REUSABLE.** `news_ground.ground_record` / `locate_span` are pure stdlib, already
  shared by build.py (deterministic CHECK) and serve_news (live DROP). A tool-derived claim grounds the
  same way: claim ⊂ the tool's OWN returned text (substring), ungrounded drops.
- **Network-ER = PARTIAL reuse.** `liveGraphLayout` (news.html) is pure JS → drop straight into
  workbench.html. The DuckDB `news_store` is companion-doctrine-bound ("build.py NEVER imports this") →
  reference its anchor design, do NOT import it (the loop stays session-only / persists-nothing).
- **Plug-in point clear; corpus absent.** The case arc is clutter → signals → decide; GATHER inserts
  after SIGNALS. Cases carry subject identity + counterparty edges. NO committed synthetic OSINT corpus
  exists → the phase authors one (the book.json / scenarios.json committed-synthetic pattern).

## The delta (four moves)

1. **A committed synthetic evidence universe + a deterministic tool layer.** Author `data/osint/**`
   (registry / adverse-media / counterparty hits indexed by entity name; clearly synthetic) + a fixed
   2-3 deterministic TOOL functions querying it + a shape validator (the validate_news_data pattern).
2. **The multi-step tool-calling agent loop.** propose-tool → call-tool → parse → GATE each finding via
   `news_ground` (grounded-or-stripped) → capped-iteration refine. Backend by NAME (creds server-side —
   Phase-57 §4.5); deterministic-STUB fallback (model-free); NDJSON stage events.
3. **The GATHER beat UI.** Insert the gather action between SIGNALS and DECIDE: stage-completion reveal of
   grounded tool-evidence (ungrounded-dropped surfaced honestly, never a token stream), the evidence /
   counterparty network reusing `liveGraphLayout`, always-on badge.
4. **EXECUTE ONCE.** Run the loop live over a marquee exemplar (grounded + dropped-ungrounded evidence
   captured as delivery evidence — the measuring→controlling / execute-once pattern).

## The honesty seam (LOAD-BEARING)

Tools query a COMMITTED SYNTHETIC universe; the agent PROPOSES, the deterministic gate DISPOSES;
ungrounded findings DROP. The gate verifies CONSISTENCY (a finding's claim ⊂ the tool's returned text),
not CORRECTNESS — the known limit of the grounding contract. That limit is BOUNDED here because the
corpus is COMMITTED (not model-generated, so the scout's "tool fabricates its own citation" bypass is
low-risk) and is SURFACED honestly (the always-on badge; ZERO catch-rate/detection-lift number). The
beat demonstrates tool-evidence EXTENDING the grounding chain the same way every other evidence modality
does — "grounding is universal, the substrate varies" ([[grounding-universal-substrate-varies]]) — NEVER
that the synthetic findings are true; final correctness stays with the human / the cross-pillar verifier.

**Decisions (direction gate 2026-06-21, all_accept:true — lite skips decision articles):**
1. **Phase 65 direction = agentic tool-calling** — chosen at the Step-9 gate over (B) the sibling-rooted
   C3/C15 alignment (highest-value but un-drivable from this repo) and (C) a consolidation/pitch-polish
   phase. The one remaining signal-watch-LOCAL Phase-63 follow-on; the LFCM new-grounding-modality path.
2. **The honesty seam is the load-bearing design invariant (A0)** — committed synthetic tools, the agent
   proposes / the deterministic gate disposes, consistency-not-correctness surfaced honestly.
3. **Companion-only / LITE holds** — a `serve_workbench` + `workbench.html` extension, NOT a 9th ship
   target; the loop is session-only / persists-nothing (reuse `liveGraphLayout`, NOT `news_store`).

## Scope

Files and modules affected (companion-only — NOT a build target):
- `scripts/serve_workbench.py` — the deterministic tool layer + shape validator; the multi-step agent
  loop (propose → call → parse → `news_ground` gate → capped refine); backend by NAME; STUB fallback;
  NDJSON stage events. REUSES `news_ground`; does NOT import `news_store` or the siblings.
- `workbench.html` — the GATHER beat (gather action, stage-completion reveal, ungrounded-dropped surfaced,
  the evidence network reusing `liveGraphLayout`, always-on badge).
- `data/osint/**` — the new committed synthetic evidence universe (registry / adverse-media /
  counterparty by entity name).
- `tests/workbench.test.mjs` — the gather arc (render + grounded-kept/ungrounded-dropped + the network
  view + badge + both motion modes + XSS-escape).
- `tests/test_selftests.py` — the gather selftests added to the pytest wrapper.
- `docs/case-workbench.md` — the gather-loop section + the consistency-not-correctness honesty boundary.
- `tests/smoke-checklist.md` — a gather presenter entry.
- `scripts/build.py` — NEVER imports aml_substrate / aml_casework; the OSINT corpus is companion data
  (NOT a build target — validated by the companion validator, not build.py).

## Exit Criteria

- [ ] T1: `data/osint/**` committed synthetic corpus + a fixed 2-3 deterministic tool layer + a shape
      validator; `serve_workbench.py --selftest` — tools return DETERMINISTIC results for a known entity
      + the validator REJECTS a broken fixture; no sibling/news_store import.
- [ ] T2: the multi-step agent loop + the grounding seam; `serve_workbench.py --selftest` covers the
      stubbed loop end-to-end — a GROUNDED finding KEPT + an UNGROUNDED finding DROPPED + the iteration
      cap enforced + persists-nothing + backend resolved by NAME (no creds in the request).
- [ ] T3: the GATHER beat renders (gather action, stage-completion reveal, ungrounded-dropped surfaced,
      the network view, always-on badge); `node tests/workbench.test.mjs` gather arc green (both motion
      modes, XSS-escape).
- [ ] T4: the loop EXECUTED ONCE live over a marquee case (grounded + dropped evidence captured); `uv run
      pytest` + `node tests/workbench.test.mjs` green; `build.py --check all` 8/8 ZERO dist drift; no
      substrate/casework import in build.py.
- [ ] T5: `docs/case-workbench.md` has the gather section + the consistency-not-correctness boundary;
      `tests/smoke-checklist.md` has the gather entry.

## Constraints

- Companion-only — a `serve_workbench` + `workbench.html` extension, NOT a 9th build/dist target —
  prevents the Phase-49 new-ship→standard ceremony escalation + the launcher cascade.
- The loop is session-only and persists NOTHING (reuse `liveGraphLayout`; do NOT import the DuckDB
  `news_store`) — keeps "committing is a human-reviewed act"; no stateful artifact masquerading as a
  learned store.
- BUILD-NEW agent loop, BOUNDED — a fixed 2-3 tool set, capped iterations (the Phase-47 D3
  max-iteration mandate) — prevents an open-ended autonomous agent; the deterministic STUB keeps the
  demo robust model-free.
- Tools query COMMITTED SYNTHETIC data; the agent proposes / the deterministic gate disposes; ungrounded
  findings DROP; the consistency-not-correctness limit is surfaced — prevents the beat reading as "real
  OSINT" or implying the synthetic findings are true.
- Agent runs server-side; the browser sends a backend NAME only (Phase-57 §4.5) — no keys/tokens in the
  frontend.
- ZERO catch-rate / detection-lift / precision number; the always-on "Illustrative data & outputs" badge
  stays.
- build.py NEVER imports aml_substrate / aml_casework — file-contract / vendored-pin only.

## Checkpoints

- **Honesty checkpoint (A0, T0 weakest):** if the live tool-evidence can't be kept honest over synthetic
  data (it reads as "real OSINT", or a claim can't be grounded to its synthetic source) → fall back to
  network-ER over the EXISTING committed counterparty edges only (no OSINT lookup, trivially grounded),
  report don't force (the named A0 fallback).
- **Live-loop checkpoint (A2/A4):** run the loop live ONCE early; if it needs real debugging beyond creds
  → surface as a FINDING and ship the deterministic stub (the Phase-57/63 checkpoint pattern), don't
  silently absorb it.

## Assumptions (gate-resolved — the honesty seam carries the weakest, T0)

- **A0 [T0 weakest — the honesty seam].** Tool-evidence stays honest: committed synthetic tools, every
  finding grounded-or-stripped via `news_ground`, consistency-not-correctness bounded + surfaced. ACCEPT
  (synthetic tools, grounded-or-stripped). If false → fall back to network-ER over existing edges only.
- **A1 companion-only.** A serve_workbench + workbench.html extension, NOT a 9th ship target (Phase-49
  new-ship→standard does NOT fire); `--check all` stays 8/8; build.py never imports the siblings; agent
  server-side, browser sends a NAME only. ACCEPT (by precedent).
- **A2 BUILD-NEW but BOUNDED.** The first multi-step tool-calling loop; fixed 2-3 tool set, capped
  iterations, deterministic-STUB fallback. ACCEPT (full live loop). If unreliable beyond creds → surface
  as a finding, ship the stub.
- **A3 committed synthetic corpus.** Registry / adverse-media / counterparty by entity name; shape-
  validated; NO real-web fetch. ACCEPT (by precedent). If false → re-scope.
- **A4 reuse liveGraphLayout + EXECUTE ONCE.** Reuse the pure-JS layout (NOT the DuckDB store; session-
  only); run the loop live once as delivery evidence. ACCEPT (execute-once). If false → drop the graph /
  drop the live run.

## Notes

- **The remaining signal-watch-local frontier.** The two higher-value follow-ons (C3/C15 cross-pillar
  alignment; the substrate ownership/BO graph emission) are SIBLING-rooted — they live in aml-substrate /
  aml-casework, which this repo cannot drive ([[cross-pillar-review-verify-sibling-repo]],
  [[cross-pillar-consume-batch-not-thin]]). Agentic tool-calling is the one frontier signal-watch can
  drive locally.
- **The live layer is becoming a real tool.** Private investigation notes are a first-class future input
  ([[live-layer-is-becoming-real-tool]]); the news anchor + entity-resolution substrate
  ([[wiki:entity-resolution-and-network-analytics]]) is the design reference for the network-ER beat.
- **Stage rendering, not token streaming** ([[stage-rendering-not-token-streaming]]) — the gather reveal
  shows completed/grounded results, never a token stream or agent-thinking.
- **The measure→control / execute-once habit** ([[measuring-to-controlling-pivot]]) — the loop is
  EXECUTED once live, not just designed.
- **Knowledge gaps:** the agent-loop transport (llama-server `--jinja` tool-calling vs opencode-driven
  vs a hand-rolled propose/parse loop over a single-shot endpoint) is the one open implementation
  question — the Phase-46 plan's llama.cpp tool-calling notes apply ([[phase-46-corpus-live-derivation]]).
  Resolve at T2; the deterministic stub de-risks it (the demo is verifiable model-free regardless).
- **Follow-on (still sequenced OUT):** the C3/C15 cross-pillar contract alignment (a sibling-repo phase);
  the substrate ownership/beneficial-owner graph emission (a substrate-rooted phase).
