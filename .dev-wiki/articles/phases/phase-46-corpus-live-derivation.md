---
title: "Phase 46: Corpus live derivation mode — local-model agentic derivation through the frozen gate (M7×M8 convergence)"
aliases: [phase-46, corpus-live-mode]
category: phases
tags: [live-mode, corpus, local-model, opencode, derivation, m7, m8]
parents: []
created: 2026-06-10
updated: 2026-06-11
source: plan
status: active # READY FOR COMPLETION 2026-06-11 — all 4 tasks [x], exit criteria met; delivery gate pending (delivery flow flips to completed after commit)
scope: [".dev-wiki/tmp/**", "scripts/serve_corpus.py", "corpus.html", "scripts/build.py", "tests/corpus-explorer.test.mjs", "docs/corpus-live.md", "tests/smoke-checklist.md", "CLAUDE.md"]
entry_criteria: "Phase 45 DELIVERED + accepted + committed (324734e/7e9fa23) + pushed; assumption gate closed 2026-06-10 all_accept: TRUE"
exit_criteria: "T1 probe report w/ measured numbers BOTH harnesses + user checkpoint; serve_corpus.py --selftest + end-to-end gate-green staged NDJSON derivation; corpus suite green incl. live-strip assertion; dist/corpus BYTE-IDENTICAL (--check all 5/5); docs/corpus-live.md + smoke + CLAUDE.md in place; full regate green; nothing presentation-touching before 2026-06-11"
---

# Phase 46: Corpus live derivation mode (M7×M8 convergence)

## Objective

Bring a LIVE mode (local model) to the corpus demo, mirroring the news-live architecture: a
companion-served, dev/authoring-time live mode where a local model derives a NEW advisory
document (pasted md / URL → red-flag indicators + C/D tags + coverage) through the EXISTING
frozen gate (`derive_signals.py check_record` — quote-grounding, cover×data matrix, red_flag
shape); only gate-green output renders into the corpus 6-screen arc. The inverted extraction
boundary (LLM extracts, deterministic layer gates) extends from in-session manual derivation
to an automated local-model loop.

Direction source: the user's REFRAME at the dev-plan gate (5th reframe in 6 gates) — "live mode
with local model for the corpus demo as well, ideally with a better harness integration like
opencode" + a pasted opencode/local-model practitioner research report. Decision article:
[[decisions/phase-46-corpus-live-derivation]].

## Scope

Files and modules affected:
- `.dev-wiki/tmp/**` — T1 probe artifacts (probe report, held-out doc LOCAL-ONLY gitignored)
- `scripts/serve_corpus.py` — NEW live companion (serve_news pattern)
- `corpus.html` — /*LIVE_START*/…/*LIVE_END*/ region ONLY
- `scripts/build.py` — strip extension to the corpus target
- `tests/corpus-explorer.test.mjs`, `docs/corpus-live.md`, `tests/smoke-checklist.md`, `CLAUDE.md`

## Exit Criteria

- [x] T1 probe report `.dev-wiki/tmp/ph46/ph46_probe.md` with measured numbers (gate pass rate /
      iterations / wall time / tool-call failures) for BOTH harnesses on the SAME held-out doc;
      user CHECKPOINT taken on the harness verdict before T2 (2026-06-11: direct + ONE
      violation-guided retry chosen; opencode 3.1× wall at identical quality, loop never engaged)
- [x] `python3 scripts/serve_corpus.py --selftest` green; live derivation of the held-out doc
      end-to-end emits ONLY gate-green indicators via staged NDJSON (17 kept / 0 dropped;
      independent re-gate 0 violations)
- [x] `node tests/corpus-explorer.test.mjs` green incl. a live-strip assertion (273→303);
      `python3 scripts/build.py --check all` 5/5 (dist/corpus BYTE-IDENTICAL)
- [x] docs/corpus-live.md + smoke-checklist live-corpus notes + CLAUDE.md current-state in place;
      full regate green (9 suites)

## Constraints

- dist/corpus BYTE-IDENTICAL via the /*LIVE_*/ build strip — prevents breaking the
  one-file/offline non-negotiable (live mode optional, isolated, off by default, scripted fallback).
- Grounding core FROZEN; rf_region anchor extension (if the held-out doc needs it) is
  REGRESSION-GATED — every existing md's region byte-unchanged + --selftest fixtures — prevents
  silent gate loosening.
- Live-derived records DISPLAY/PROPOSE-only — committing a new derived record to data/ remains
  a separate human-reviewed act under existing licence rules — prevents licence/compliance drift.
- The 2026-06-11 presentation OUTRANKS the phase — nothing presentation-touching moves before it;
  --check all 5/5 before any commit — prevents demo-day breakage.
- Held-out probe material LOCAL-ONLY, gitignored, never committed.

## Checkpoints

- After T1: present the harness verdict (opencode vs direct pipeline, measured) — WAIT for the
  user's call before T2.
- If opencode cannot drive a reliable tool-calling loop with the existing Qwen: report honestly,
  ship on the direct pipeline (the designed fallback).

## Assumptions

- A1 (accept): the phase IS corpus live derivation — opencode evaluated strictly as the
  derivation-loop RUNTIME, not dev tooling. If false: re-gate direction.
- A2 (accept): harness adoption is probe-gated at T1; opencode must earn its complexity on
  measured numbers. If the probe is inconclusive: ship the proven pattern.
- A3 (accept): existing Qwen serving first; FINTRAC /intel/ frontier doc as held-out material
  (probe-local). Model swap only on measured tool-call-class failure.
- A4 (accept): /*LIVE_*/ strip keeps dist/corpus byte-identical; live output propose-only;
  presentation outranks. If byte-identity cannot hold: STOP and surface.

## Notes

Knowledge gaps carried to implementation: whether the FINTRAC /intel/ frontier doc parses under
the existing rf_region anchor set (T1 exercises it); whether opencode + the existing Qwen can
drive a reliable tool-calling agent loop at all (T1's whole job — the report says agentic-tuned
MoE models are the reliable class); wall-time for a full-advisory derivation at local-model
speed (dozens of indicators × C/D tags + build_logic — may force a short-doc demo shape or
per-indicator staged reveal; T1 measures).

Operational facts from the user's pasted report (for T1): llama-server needs `--jinja` for tools
(no `--chat-template` alongside); ctx floor 16384, 64K+ preferred for agent loops; opencode
config via the @ai-sdk/openai-compatible provider block, model key must match `--alias`;
headless `opencode run` has a known permission bug — prefer `opencode serve` + SDK/--attach;
all SWE-bench numbers vendor-reported. Environment measured at planning: opencode NOT installed
(bun present), llama-server running at 127.0.0.1:8080, serve_news not running.

Reference pattern for every companion decision: docs/news-live.md (NDJSON staging, single-flight,
stage-completion rendering — never token streams, /*LIVE_*/ strip, scripted fallback).
