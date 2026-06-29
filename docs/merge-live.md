# The merge-adjudicator LIVE mode (companion-served; dev/authoring-time only)

> The 5th agentic LIVE loop (the agentification roadmap's **Stage 1** — the first *measurable* agent). An
> agent PROPOSES each merge call beside the human gate, and its judgment is **measured against the committed
> non-circular oracle** in `data/merge/cases.json` — the one gate with a correctness oracle. Synthetic /
> illustrative throughout; **no rate, score, or multiplier is claimed** — agreement is reported as COUNTS,
> qualified synthetic. The offline `dist/merge/index.html` is unaffected: it makes ZERO model/fetch call (the
> live code is build-stripped, §4.5).

## What it is

The merge console (`dist/merge/`) dramatizes the Class-J human gate over entity-resolution candidate links.
This companion adds an optional live overlay: when served by `scripts/serve_merge.py`, an agent reads a
case's **pre-adjudication evidence** (the two records + the shared identifier + the deterministic spine's
call) and proposes one of `{uphold_merge, reject_as_shares, both_defensible, escalate}` + a one-sentence
rationale, shown **beside** the human gate. The human still adjudicates — `propose → gate → decide`. Post
-disposition, the overlay also shows whether the *agent* matched the latent oracle, and the session ledger
carries a counts-only agent-agreement tally.

The agent is deliberately **thin**: the deliverable is the *measurement*, not the agent. It is a proposer
over the already-built `resolution_scorer` oracle.

## The oracle firewall (load-bearing)

The agent never sees the truth. `scripts/merge_adjudicator.py:adjudicator_input()` strips each case to the
evidence surface (`a`, `b`, `basis`, `shared`, `spine_verdict`, `source`, `id`) and `assert_no_oracle_leak()`
RAISES on any truth field (`oracle`, `same_entity`, `correct_adjudication`, `klass`, …) — the schema
boundary, not the field name, so renaming the leak does not pass. The served `/adjudicate` response carries
only `{call, rationale, backend}`; the oracle reveal stays the page's existing post-disposition mechanism.

## How to run

1. Start a local OpenAI-compatible model on `127.0.0.1:8080` (any llama-cpp `/v1` server; set `--ctx-size`
   generously). With no model, the companion DEGRADES to the deterministic `StubAdjudicator` + a named note.
2. `python3 scripts/serve_merge.py` → http://localhost:8040 (stdlib only, binds 127.0.0.1, persists nothing).
   - `--backend stub` forces the deterministic baseline (demoable with no model at all).
   - `--port`, `--backend openai` (default) override.
3. Pick a candidate → Evidence → **Adjudication** (the agent's proposal appears beside the four grades) →
   Verdict (the agent vs the latent truth) → Ledger (the agent-agreement tally, counts only).

The offline `dist/merge` is untouched and remains the scripted demo. Companion ports: news 8000 · corpus
8010 · chain 8020 · workbench 8030 · **merge 8040**.

## The two adjudicators (the GATHER stub/live split)

- **`StubAdjudicator`** — deterministic, NO model: echoes the resolver's `spine_verdict` (`merged →
  uphold_merge`, `kept_distinct → reject_as_shares`). The offline default + the **two-sided baseline** the
  live agent is measured against.
- **`LiveAdjudicator`** — the agent under test: reads the evidence, prompts the model via
  `osint_tools.call_openai`, `parse_llm_json` fail-closed (a non-parsing / out-of-vocab response → `escalate`,
  an honest defer-to-human, counted but never scored).

## The measurement (the headline)

`tests/merge_adjudicator_quality_harness.py` pins ONE live capture and replays it deterministically with no
model (`--check`), beside the always-available deterministic stub baseline (`--freeze` re-captures from a
live model). Over the **66 committed scored cases**, measured on a local model (synthetic + synthetic-aml
-substrate-slice oracles; production has no ground truth — no rate, score, or multiplier is claimed):

| | matched the oracle | differed | deferred |
|---|---|---|---|
| **StubAdjudicator** (echo the spine) | **33** of 66 | 33 | 0 |
| **Live agent** | **54** of 66 | 12 | 0 |

The deterministic spine baseline is **two-sided by construction** — right on every *correct-rejection* (30)
and *real-co-reference* (3), wrong on every *fragmentation-gap* (30) and *over-merge-trap* (3). So the agent
is measured precisely on the 33 the spine gets wrong. Broken out by quadrant:

| quadrant | spine right? | stub matched | agent matched |
|---|---|---|---|
| correct-rejection (30) | yes | 30 | 30 |
| real-co-reference (3) | yes | 3 | 3 |
| **fragmentation-gap (30)** | **no** | 0 | **18** |
| **over-merge-trap (3)** | **no** | 0 | **3** |

The agent **recovered 21 of the 33 cases the deterministic resolver got wrong** — 18 of 30 fragmentation
-gaps (same-person fragments sharing an email that the spine kept distinct) + all 3 over-merge-traps
(distinct people the spine merged on one shared identifier). By provenance: substrate-anchored 22 of 29,
OFAC name-collision 23 of 24, synthetic 9 of 13. The agent committed a binary call on every case (0
deferrals) on this run — an honest finding: the `both_defensible`/`escalate` vocabulary was available, the
model chose to decide each time.

"The agent ties the spine" would have been an honest result too — the measurement is the deliverable, not a
target. The harness is the regression gate: a future prompt/model change is replayed against this frozen
capture, and a cases.json oracle drift fails the always-checkable stub baseline.

## The boundary (firewall + offline guarantees)

- `build.py` imports NO `merge_adjudicator` / `serve_merge` / scorer / spine (a grep guard); the companion
  touches no ship dist.
- The LIVE overlay lives in `merge.html` inside `/*LIVE_START*/.../*LIVE_END*/` and is build-stripped — the
  offline `dist/merge/index.html` is **byte-identical** (`python3 scripts/build.py --check merge`) and carries
  no `fetch(`/live code.
- Scoring is dep-free (the committed oracle is already resolved — no DuckDB/spine); only the live capture
  (`--freeze`) needs a model. Nothing is persisted on any path.

## Tests

- `python3 scripts/merge_adjudicator.py --selftest` — the oracle firewall (rejects a leak incl. a renamed
  surrogate) + the deterministic stub baseline + the scoring shape, dep-free.
- `python3 tests/merge_adjudicator_quality_harness.py --check` — the regression gate (stub baseline +
  pinned live-capture replay, no model). `--freeze` re-baselines from a live model.
- `python3 scripts/serve_merge.py --selftest` — the served page + payload parity with `build.render_merge` +
  the on-the-wire oracle firewall + the stub/live/degrade paths (no model).
- `node tests/merge-console.test.mjs` — the offline-strip assertion (`dist/merge` carries no live code) + the
  companion live-branch (style injection, the gate fires one firewall-clean `/adjudicate` request).
