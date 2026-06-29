# The §12 determination pre-proposer LIVE mode (companion-served; dev/authoring-time only)

> The 6th agentic LIVE loop (the agentification roadmap's **Stage 2** — the second *measurable* agent after
> the merge adjudicator). An agent reads a case's EVIDENCE and PROPOSES its §12 determination beside the human
> gate, and its judgment is **measured two-sided** against aml-substrate's EXOGENOUS `intended_disposition`
> oracle (the Phase-78 capture, authored blind to the sufficiency rule — the SAME non-circular oracle the
> determination-validation harness uses). Synthetic / illustrative throughout; **no rate, score, or multiplier
> is claimed** — agreement is reported as COUNTS, qualified synthetic. The offline ship dists are unaffected:
> the investigator workbench is companion-only and is never built into `dist/`.

## What it is

The investigator workbench (`scripts/serve_workbench.py` + `workbench.html`) dramatizes the §12 determination
loop. This adds an optional pre-proposer: an agent reads a case's **fired detection capabilities + the mapped
crime type** and proposes one of `{file, clear, needs_more_info}` + a one-sentence rationale, shown **beside**
the human determination gate. `propose → gate → decide`: the deterministic sufficiency engine
(`evidence_requirements.py`, A1-frozen) still LICENSES the determination, the human still DECIDES; the
proposal is a presentation, never an engine input.

The agent is deliberately **thin**: the deliverable is the *measurement*, not the agent. It is a proposer over
the already-built `determination_validation_harness` oracle — the proposer is a small layer on top of the
validation harness, reusing its firewall + its deterministic engine baseline (`classify()`).

## The oracle firewall (load-bearing)

The agent never sees the truth. `scripts/determination_proposer.py` reuses the validation harness's
`proposer_input()` (strips each case to `{case_id, caps, crime_type}`) and `assert_no_oracle_leak()` (RAISES
on `intended_disposition` / a renamed surrogate / ANY extra key — the schema boundary, not the field name, so
renaming the leak does not pass). The served `/propose-determination` response carries only
`{case_id, crime_type, proposal:{call, rationale}, backend, qualifier, framing}` — **no oracle field on the
wire** (asserted in `serve_workbench --selftest` and `workbench.test.mjs`). Non-circular by construction: the
oracle was authored BLIND to the sufficiency rule and never reaches a proposer input (the Phase-77
circular-oracle trap avoided).

## How to run

1. Start a local OpenAI-compatible model on `127.0.0.1:8080` (any llama-cpp `/v1` server; set `--ctx-size`
   generously). With no model, the companion DEGRADES to the deterministic `StubProposer` (echo the engine) +
   a named note.
2. `python3 scripts/serve_workbench.py` → http://localhost:8030 (stdlib + the vendored casework venv for the
   DECIDE finale; binds 127.0.0.1, persists nothing).
3. Pick a case → … → **Determination**: the §12 pre-proposer panel sits above the human determine form. Click
   **Ask the agent to propose** → the agent's call + rationale appears, labelled *proposed, not decided*; the
   human still types the risk / mitigation and clicks **Determine**. Pick the backend in the existing picker
   (`stub` = the deterministic engine echo, no model; `openai` = the live agent).

The offline ship dists are untouched. Companion ports: news 8000 · corpus 8010 · chain 8020 · **workbench
8030** · merge 8040.

## The two proposers (the GATHER stub/live split)

- **`StubProposer`** — deterministic, NO model: echoes the engine's bundle-only verdict (`classify().file_ready
  → file`, else `needs_more_info` — bundle-only the engine cannot affirmatively CLEAR, so it abstains). The
  offline default + the **engine-vs-oracle baseline** the live agent is measured against.
- **`LiveProposer`** — the agent under test: reads the caps + crime type (+ deterministic capability
  descriptions), prompts the model via `osint_tools.call_openai` (temperature 0), `parse_llm_json` fail-closed
  (a non-parsing / out-of-vocab response → `needs_more_info`, an honest abstention, counted but never scored).
  Because the proposal is a function of the cap-SIGNATURE alone, the harness dedupes by signature — **46
  distinct signatures cover all 6935 capture cases**, so the FULL population is measured with 46 live calls (no
  sampling).

## The measurement (the headline)

`tests/determination_proposer_quality_harness.py` pins ONE live capture (the 46 signature→proposal decisions)
and replays it deterministically with no model (`--check`), beside the always-available deterministic stub
baseline (`--freeze` re-captures from a live model). Over the **6935-case capture** (121 oracle-`file`, 6814
oracle-`clear`), measured on a local Qwen MoE with a base-rate-informed prompt (synthetic substrate slice;
production has no ground-truth disposition — no rate, score, or multiplier is claimed; an abstention =
`needs_more_info`, counted SEPARATELY, never a wrong call):

| | matched the oracle | differed | abstained |
|---|---|---|---|
| **StubProposer** (echo the engine) | **50** | **1320** (over-flag) | 5565 |
| **Live agent** | **74** | **4482** | 2379 |

This is **NOT a clean "agent beats engine" story** — it is a richer, two-sided one. Broken out by class:

| class | engine (stub) | live agent |
|---|---|---|
| oracle-`file` (121) | committed `file` 50 · abstained 71 | committed `file` **74** · abstained 47 |
| oracle-`clear` (6814) | over-filed 1320 · abstained 5494 | over-filed **4482** · abstained 2332 |
| KYC-pure (727, all oracle-clear) | over-filed all **727** | **abstained all 727** |
| money-laundering (6208) | committed 50 / over-filed 593 | committed 74 / over-filed **4482** |

The agent **trades the engine's conservatism for sensitivity**: it recovers more oracle-`file` cases (74 vs 50)
and **eliminates all 727 KYC structural over-flags** the rigid rule marks file-ready (a customer-due-diligence
gap alone, with no laundering mechanism, is not a filing basis). But it **over-files on the volume ML class**
(4482 vs the engine's 593) — it reasons from per-case red-flag CO-OCCURRENCE ("rapid pass-through + a
multi-originator network + income inconsistency = a corroborated mechanism") and files the dominant `C2|C3|C8`
signature (4040 cases, **4029 of them benign**). Even GIVEN the public base-rate context in the prompt (TM
detectors fire frequently on legitimate activity; co-occurring flags are usually coincidental), the per-case
agent still over-files on that signature, **because the benign-ness is a POPULATION property invisible in a
single case** — the calibrated deterministic 2-leg rule encodes the base-rate discipline the agent cannot
infer one case at a time.

**The honest finding VINDICATES `propose → gate → decide`:** the agent is a sensitivity-rich *proposer* (it
surfaces candidate files + fixes the structural KYC over-flag a human should weigh); the deterministic engine
+ the human gate supply the population-calibrated discipline the per-case agent lacks. Neither alone is the
decider — which is exactly why the architecture keeps the calibrated rule LICENSING and the human DECIDING.
"The agent ties the engine" would have been an honest result too — the measurement is the deliverable, not a
target. The harness is the regression gate: a future prompt/model change is replayed against this frozen
capture, and a capture/engine drift fails the always-checkable stub baseline.

## The boundary (firewall + offline guarantees)

- `build.py` imports NO `determination_proposer` / `serve_workbench` / `evidence_requirements` companion path
  for this loop (a grep guard); the workbench is companion-only and touches no ship dist. All 9 ship dists stay
  byte-identical (`python3 scripts/build.py --check all`).
- `evidence_requirements.py` is **byte-unchanged** (the agent proposes; the deterministic engine licenses) —
  A1-frozen, `git diff --quiet scripts/evidence_requirements.py`.
- Scoring the stub baseline is dep-free (the committed capture is already resolved — no substrate, no model);
  only the live capture (`--freeze`) needs a model. Nothing is persisted on any path.

## Tests

- `python3 scripts/determination_proposer.py --selftest` — the oracle firewall (rejects a leak incl. a renamed
  surrogate) + the two-sided StubProposer engine baseline (50 agree / 1320 over-flag / 5565 abstain, all 727
  KYC over-flags surfaced) + the 46-call signature cache + the live fail-closed abstention, dep-free.
- `python3 tests/determination_proposer_quality_harness.py --check` — the regression gate (the stub baseline +
  the pinned live-capture replay by signature, no model). `--freeze` re-baselines from a live model.
- `python3 scripts/serve_workbench.py --selftest` — includes the served `/propose-determination` route (stub
  default, the propose→gate→decide framing, the on-the-wire oracle firewall, an unknown case is a named error).
- `node tests/workbench.test.mjs` — the pre-proposer panel (the call + rationale + the proposed-not-decided
  framing + the synthetic qualifier; the human Determine gate unchanged; the live/stub backend labels; XSS
  escaped; the oracle never renders).
