# Spec — Phase 83: Agentification Stage 1 — the merge adjudicator agent, oracle-scored (the 5th companion live loop)

> Synthetic / illustrative throughout; **no rate, score, or multiplier is claimed** — agreement is reported
> COUNTS-only with the synthetic-substrate qualifier. Companion-only; the offline ship artifacts make zero
> model/fetch call (§4.5). Code-verified seams (file:line) 2026-06-29; siblings stalled at the Phase-82 pins
> (substrate `294d3e5` / casework `04cc335`) → no new emission to consume; this is the signal-watch-internal
> forward path (`docs/agentification-roadmap.md` Stage 1).

## 1. Objective

Build the **first MEASURABLE agent** of the agentification roadmap: a merge adjudicator that, given a merge
case's pre-adjudication evidence, PROPOSES one of `{uphold_merge, reject_as_shares, both_defensible, escalate}`
+ a rationale, and whose judgment is **measured against the committed non-circular oracle** in
`data/merge/cases.json` (the one gate with a correctness oracle). Run it live once, pin the capture, record the
measured agreement counts. Surface it as the **5th companion live loop** (a served page beside the human gate),
keeping all 9 ship dists byte-frozen. The human still adjudicates; the agent's call is a measured proposal
beside the latent truth — `propose → gate → decide`, never relaxed.

## 2. The headline (why it is credible)

The deterministic StubAdjudicator baseline (echo `spine_verdict`) is **TWO-SIDED**: right on 33/66 committed
scored cases, wrong on 33 (30 fragmentation-gap where same-person fragments share an email but the spine kept
them distinct + 3 over-merge-trap). So the agent is measured precisely on the 33 the spine gets WRONG, reported
**broken out by quadrant + provenance**. "The agent ties the spine" is an honest result, not a failure — the
MEASUREMENT is the deliverable; the agent is deliberately thin (a proposer over the *built* `resolution_scorer`).

## 3. In scope

- `scripts/merge_adjudicator.py` (companion-only, dep-free scoring): `StubAdjudicator` + `LiveAdjudicator` +
  `adjudicator_input()` firewall + `assert_no_oracle_leak()` + `score_adjudications()` (counts by quadrant +
  provenance; deferrals separate; synthetic qualifier).
- `tests/merge_adjudicator_quality_harness.py` (the `gather_quality_harness.py` pattern): `--check` (dep-free
  replay + stub-baseline regression), `--freeze` (one live capture). Wired into `tests/test_selftests.py`.
- `scripts/serve_merge.py` (companion server, stdlib, 127.0.0.1, the `serve_corpus.py` pattern): serves
  `merge.html` + proxies the adjudicator (stub offline / live on :8080), `resolve_backend` degrade.
- `merge.html` LIVE overlay in `/*LIVE_START*/.../*LIVE_END*/` (build-stripped) + `build.py` strip coverage for
  the `merge` target (`dist/merge` byte-identical via `--check merge`).
- `tests/merge-console.test.mjs`: offline-strip assertion + the companion live-branch tests.
- Execute-once: the live run, pinned capture, recorded counts.
- Docs: `docs/merge-live.md`, CLAUDE.md current-state, `docs/agentification-roadmap.md` (Stage 1 → BUILT),
  HANDOFF.md §8; honesty sweep.

## 4. Out of scope (YAGNI)

- Baking the agent's call into the offline ship dist (rejected at the gate — design A, companion-live).
- Any `evidence_requirements.py` / determination-engine touch (this is merge, not §12).
- Stages 2–4 of the agentification roadmap (determination pre-proposer / STR drafter / triage second-rater).
- Probabilistic ER / fuzzy name-matching (the wiki ER caveat: loosened name matching without identifier
  layering explodes false positives).

## 5. Load-bearing constraints (the firewall)

- **§4.5 / dist boundary:** all 9 ship dists BYTE-FROZEN (`--check all` 9/9); the live overlay is build-stripped
  → `dist/merge` byte-identical. The offline file makes NO model call.
- **The oracle firewall:** the agent provably never sees the `oracle` block — `adjudicator_input()` strips to
  the evidence surface, `assert_no_oracle_leak()` (the `_TRUTH_LEAK_KEYS` set) RAISES on any truth field; the
  served `/adjudicate` payload carries no oracle pre-disposition (same as the static page).
- **build.py firewall:** imports NO `merge_adjudicator` / `serve_merge` / scorer / spine / curate / casework
  (grep guard).
- **Honesty:** counts-only; the synthetic-substrate qualifier on every number; the word-ban (no
  `catch-rate`/`lift`/`precision`) extends to the LIVE markers + the docs.
- **Compliance:** nothing new ships; the committed cases already ship clean (real OFAC names = the
  false-positive trap; badge always-on).

## 6. Exit criteria

- `python3 scripts/merge_adjudicator.py --selftest` exits 0 (firewall rejects an oracle leak; stub baseline
  reproduces 33-right/33-wrong; scoring emits counts-by-quadrant + deferrals + qualifier; no banned words).
- `python3 tests/merge_adjudicator_quality_harness.py --check` exits 0 (stub baseline reproduces; a pinned live
  capture, if present, replays to the frozen agreement); in `uv run pytest`.
- `python3 scripts/serve_merge.py --selftest` exits 0 (page render + payload parity + stub loop + degrade +
  the no-oracle-pre-disposition firewall).
- `python3 scripts/build.py --check merge` byte-identical (LIVE strip); `--check all` 9/9.
- `node tests/merge-console.test.mjs` green (existing + the live-branch + the offline-strip assertion).
- The measured agreement counts recorded (stub baseline unconditionally; the live capture pinned, or the live
  freeze flagged pending with a model-absent note — never fabricated).
- Docs written; CLAUDE.md current-state trued in place; honesty sweep clean.

## 7. Abort rules

- Any unsanctioned dist drift (esp. `dist/merge` not byte-identical after strip) / a `build.py` companion
  import / an oracle leak to the client pre-disposition → STOP-and-surface.
- No model on :8080 for the live freeze → ship the StubAdjudicator baseline + flag the live capture as a named
  follow-on; never fabricate a live agent number.
- Any agreement count presented as a catch-rate / lift / precision / recall → STOP.
