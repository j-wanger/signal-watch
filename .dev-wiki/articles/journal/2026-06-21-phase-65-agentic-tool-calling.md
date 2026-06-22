---
title: "Phase 65 — Agentic tool-calling: the investigator evidence-gathering loop (companion)"
date: 2026-06-21
phase: phase-65-agentic-tool-calling
ceremony: lite
gates: { direction: accepted (all_accept:true), delivery: accepted }
status: delivered
---

# Phase 65 — Agentic tool-calling: the investigator evidence-gathering loop

**What it is.** Signal-watch's FIRST multi-step tool-calling agent loop — the one remaining
signal-watch-LOCAL Phase-63 follow-on. A GATHER beat in the investigator case workbench (between
*signals* and *decide*): on a selected synthetic case the agent proposes a tool → calls a deterministic
tool over a COMMITTED SYNTHETIC OSINT corpus (`data/osint/corpus.json` — registry / adverse-media /
sanctions) → each finding is GROUNDED-OR-STRIPPED by the reused `news_ground` gate → grounded
tool-evidence extends the grounding chain + feeds a `liveGraphLayout` network. Companion-only
(`scripts/osint_tools.py` + `serve_workbench.py /gather` + the `workbench.html` beat); NOT a ship target.

**The honesty seam (load-bearing): CONSISTENCY, not correctness.** The gate proves the quote is a real
substring of the cited synthetic record (`locate_span` + a normalized-length floor + a single-sentence
guard + requote-to-exact-span) and that the entity/link is a name the record DECLARES (exact, not a free
substring). It does NOT prove the synthesis is a correct inference. Surfaced: a beat-local
synthetic-provenance line, the chain labelled authored-not-discovered, the grounded quote beside a
SUBORDINATE illustrative synthesis, rejections shown with reason, ZERO catch-rate/% number.

**Executed once, live.** Over the mule (CASE-P-0002174 "Zane Zhao") against a local Qwen3.6-35B the
chain fired: `lookup_registry` → discovered *Crescent Dunes Trading FZE* → `screen_sanctions` → the OFAC
hit → `screen_adverse_media` → honest empty. **2 grounded / 0 dropped / 0 fabricated**, reproducible.

## What moved

- NEW `scripts/osint_tools.py` (stdlib + `news_ground` only): `validate_osint_corpus`, `run_tool` (3
  deterministic tools, exact-normname), `gate_finding` (the full grounding conjunction), `build_graph`,
  `StubPlanner`/`LivePlanner`, `gather` (capped + no-progress-guarded, fail-closed), `call_openai`
  (sanitized), `parse_llm_json`, `--selftest`.
- NEW `data/osint/corpus.json` — committed synthetic OSINT corpus (head-of-file disclaimer).
- `scripts/serve_workbench.py` — `/gather` NDJSON endpoint + the gather selftest block (grounded/dropped/
  graph/persists-nothing/§4.5 cred-leak over all stages).
- `workbench.html` — the GATHER beat (provenance line, grounded-quote-beside-subordinate-synthesis,
  rejections with reason, the `liveGraphLayout` network, edge-reveal) + the gather test arc (+17 → 100/0).
- `tests/test_selftests.py` — `osint_tools.py` added to `PY_SELFTESTS`.
- `docs/case-workbench.md` + `tests/smoke-checklist.md` — the Phase-65 sections.

## The two adversarial passes (the ultracode discipline)

1. **Pre-build design review** (4 agents) → folded every must-hold before writing: the
   entity-into-graph hole, the span-bridge, the record-id binding, the synthetic-provenance
   requirements, the %-rule collision with verbatim synthetic text.
2. **Post-build code review** (3 skeptics + per-finding re-verification) → security/§4.5/XSS: ZERO real
   issues; 3 honesty-gate findings, all fixed + locked with selftests:
   - **MEDIUM** `_name_grounded` admitted a fragment (`'FZE'`, `'a'`) of a real name as a graph node →
     changed to exact-against-the-record's-DECLARED-names (entity/officers/linked_entities ∪ subject).
   - **LOW (latent)** `_span_ok` bridge guard didn't match `locate_span`'s full `[ \t\r\n]` class (a
     `.`+TAB/CR slipped) → regex `[.!?][ \t\r\n]`.
   - **LOW (latent)** the validator's banned-token sweep skipped `entity`/`linked_entities` → extended.
   - Fixing the medium surfaced a real **link-granularity** bug: an ungrounded OPTIONAL link was killing
     an otherwise-valid grounded finding (the live model kept proposing `link_to="OFAC … list"`). Corrected
     so a bad link drops to `None` while the grounded finding survives (the `news_ground`
     keep-entity/strip-attr pattern) — which is *why* the live chain now fires reliably.

## Verification (exit)

`uv run pytest` 18/18 · `node tests/workbench.test.mjs` 100/0 · `osint_tools`/`serve_workbench --selftest`
green · `python3 scripts/build.py --check all` 8/8 ZERO dist drift · build.py imports no sibling/companion.

## Decisions / notes

- Gate all_accept:true (A0 the honesty seam [T0 weakest] · A1 companion-only · A2 BUILD-NEW bounded loop ·
  A3 committed synthetic corpus · A4 reuse liveGraphLayout + execute-once); all HELD at delivery (see the
  ledger Phase-65 revisit-status). Grounded against signal-watch HEAD 0ee4489 + the committed Phase-64
  workbench; aml-substrate@9d2e65c / aml-casework@81df91c verified live but NOT consumed (companion-only).
- `news_ground` now has a THIRD consumer (`osint_tools`, alongside `serve_news` + `build.py`) — a future
  gate edit must re-run `osint_tools --selftest` alongside the news selftests.
- Hand-rolled propose/parse loop over a single-shot `/v1` endpoint chosen over llama `--jinja`
  tool-calling (deterministic, offline-stubbable, backend-agnostic — the Phase-46 quant-fragility note).
- No active signal-watch-local phase now; the remaining LFCM frontiers (C3/C15 alignment; substrate
  ownership-graph emission) are SIBLING-rooted.
