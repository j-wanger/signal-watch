# The STR-drafter LIVE mode + its quality measure (companion-served; dev/authoring-time only)

> The agentification roadmap's **Stage 3** — a real agent drafter behind aml-casework's six Class-G grounding
> verifiers (`propose → gate → decide`: the agent drafts, the verifiers gate, the human signs). Unlike Stage 1
> (merge) and Stage 2 (§12), drafting has **NO correctness oracle** — free-text narrative has no latent truth
> — so the measure is **consistency-not-correctness** (the GATHER class), reported as COUNTS, qualified
> synthetic. **No rate, score, or multiplier is claimed.** The offline ship artifacts are unaffected: they make
> ZERO model/fetch call (§4.5). aml-casework is **measured, not modified** — the Drafter Protocol + the six
> verifiers stay byte-frozen.

## What it is (and what already existed)

The DECIDE drafter is NOT new — the **Drafter Protocol** (`aml_casework.narrative_generator.Drafter`), the
`--drafter {stub,claude,openai,opencode}` switch, the server-side backend mapping
(`serve_chain.resolve_backend`), and the live-draft staged reveal in the workbench shipped in **Phase 57**.
A real model on `127.0.0.1:8080` already drafts the STR narrative today, and casework's six verifiers
sign-or-refuse it.

What Stage 3 ADDS is the **measurement frame** the other agentified loops have and this one lacked: a quality
harness that measures the live (local) agent drafter against the deterministic stub over the committed
designed-scenario bundles, pinned as a `--check`/`--freeze` regression gate. The deliverable is the
*measurement*, not the drafter.

## Why there is no oracle (the measure shape)

A merge call (Stage 1) and a §12 determination (Stage 2) each have a latent truth to score against. A free
-text STR narrative does not — there is no committed "gold narrative," and authoring one would be synthetic
judgment, not truth (rejected: overfit + authorship-bias). So the gate IS the measure: aml-casework's six
Class-G verifiers return a binary **SIGNED / REFUSED** + `blocking_violations` (citation grounding, corpus
grounding, the fabrication guard, completeness). The harness counts, per bundle:

- **stub-vs-live SIGN / REFUSE** (the verifiers are the arbiter on whatever each backend wrote),
- the verifier / fabrication-guard **CATCH** (a live draft the verifiers refuse *with* a violation — a
  hallucinated/ungrounded block the guard caught),
- **RECOVERED** (the stub fail-closes, the live agent produces a narrative the verifiers accept),
- per-case **CONSISTENCY** (does the live drafter reach the same sign/refuse outcome as the stub?).

NO accuracy / catch-rate / precision / recall — there is nothing to be "correct" against.

## The population (designed scenarios, not a slice sample)

The committed casefile bundles (file + cleared dispositions) + the ONE narrative-seam slice case the stub
fail-closes on — each a deliberate drafter scenario, NOT a random slice sample (the casework consume is a
subprocess up to 300 s, so a small set keeps the live capture practical):

| bundle | disposition | the scenario |
|---|---|---|
| `cleared-demo.bundle.json` (Riverside) | cleared | a documented dismissal (exculpatory source-of-funds) |
| `case-b.bundle.json` (Lakeshore) | cleared | the north-star clear, fan-in C3 |
| `sanctions-c14-demo.bundle.json` | file | a sanctions-driven C14 file |
| `CASE-P-0025128.json` (slice) | file | the narrative-seam case the **stub fail-closes** on (the contrast) |

The slice bundle is `contract_version 0.5`; casework validates a v0.3 allowlist but tolerates the additive
fields, so it is handed the **v0.3 view** (the committed bundle stays v0.5) — the same translation curate uses
to measure the 256/376 coverage funnel.

## The measurement (the honest headline)

`tests/drafter_quality_harness.py` runs the REAL casework consume (drafter=stub, then drafter=openai on
:8080) per bundle, pins the per-bundle consume results, and replays them through the pure scorer with NO
subprocess + NO model in `--check`. Measured on a local model (synthetic bundles; consistency-not-correctness;
no rate, score, or multiplier):

| | signed | refused | verifier-caught | recovered |
|---|---|---|---|---|
| **stub drafter** (deterministic) | 3 of 4 | 1 (the narrative-seam case) | 0 | — |
| **live agent drafter** (model on :8080) | 3 of 4 | 1 (the same case) | 0 | 0 |

**Consistent with the stub on 4 / 4.** The live agent used the real model on every bundle (no stub fallback).
On the 3 signable cases it wrote narratives the six verifiers **accepted** — identical outcome to the stub. On
the narrative-seam case (`CASE-P-0025128`), **both** fail-closed: the capture records `signed:false`,
`narrative_present:false`, and **empty `blocking_violations`** — neither drafter produced a narrative the
verifiers would sign, and the guard had nothing to catch. (Casework's disposition on this case is
`needs_more_info`, a completeness disposition — verified from its signed SAR; the *precise* unmet element is
not surfaced as a `blocking_violation`, so the captured data shows the outcome, not the verifier's reason.)
Critically, the live agent did **not** fabricate a narrative to force a file there — it fail-closed exactly
like the deterministic stub.

### What the tie means (it is a real result, not a target)

The agent **tied the stub** — and that is an honest measured outcome (as it was for Stage 1, where "the agent
ties the spine" would have been honest too). It says two things:

1. **The agent drafter stays inside the gate.** Every narrative it wrote on the signable cases passed the six
   verifiers, and on the case casework would not complete it honestly fail-closed rather than hallucinating — **0
   fabrications caught**. The consistency-not-correctness discipline holds: the verifiers gate the agent's
   output exactly as they gate the stub's.
2. **The drafter measure is consistency-BOUNDED by design** — the deepest Stage-3 finding. Because the gate
   refuses anything ungrounded, a *competent* agent drafter and the deterministic stub **converge at the
   gate**: both produce signable narratives on signable cases and both fail-close on insufficient ones. They
   diverge only if the agent recovers a narrative the stub couldn't (the stub grounds by construction, so it is
   rarely deficient on signable cases) or fabricates and gets caught (a competent model does not hallucinate on
   grounded evidence). So **the gate, not the drafter, determines defensibility** — which is precisely the
   propose→gate→decide thesis. Drafter quality is largely *invisible above a competence floor*; the gate is the
   load-bearing component.

### The limitation, stated plainly

This population does not EXERCISE the two discriminating behaviors — `recovered` and `caught` are both 0. The
3 signable cases sign for any competent drafter; the 1 hard case casework would not complete fail-closes
regardless of drafter. So the measure confirms grounding- and honest-refusal-CONSISTENCY, but cannot (on these bundles) show
the agent out-drafting or under-drafting the stub. The **fabrication-guard-fires** demonstration lives in the
scripted fail-closed beat (the workbench BEAT-3 composed-mule refusal, with real `blocking_violations` from the
C3/C15 grounding replay) — it is shown there, not contrived here. A deliberately-ungrounded adversarial bundle
(to force a live hallucination the guard catches) is the named follow-on; it was deliberately NOT authored, to
keep the measurement honest rather than dramatized.

## How to run

1. Start a local OpenAI-compatible model on `127.0.0.1:8080` (any llama-cpp `/v1` server). With no model, the
   casework `openai` drafter fails soft to the deterministic stub (`drafter_effective="stub"`) — recorded
   honestly, never a fabricated narrative outcome.
2. `python scripts/setup_workbench.py` (builds the vendored casework venv from the committed wheel), then
   `python scripts/serve_workbench.py` → http://localhost:8030 — pick a backend, run DECIDE; the staged reveal
   shows the draft + the six verifiers' sign/refuse.
3. The measure: `python3 tests/drafter_quality_harness.py --freeze` re-captures the live + stub per bundle;
   `--check` replays the pinned capture with no model/subprocess.

The offline `dist/*` are untouched. Companion ports: news 8000 · corpus 8010 · chain 8020 · workbench 8030 ·
merge 8040.

## The boundary (offline + frozen guarantees)

- `build.py` imports NO `drafter_quality_harness` (a grep guard); the harness touches no ship dist.
- aml-casework is **measured, not modified** — the vendored Drafter Protocol + the six verifiers are
  byte-frozen (the vendor pin is current: `04cc335` == the sibling HEAD); `scripts/evidence_requirements.py`
  (the §12 sufficiency engine) and the 256/376 §12 signing funnel are UNTOUCHED — the drafter is the downstream
  DECIDE beat, not the §12 engine.
- Scoring is dep-free (the pinned consume results replay through a pure scorer — no DuckDB, no subprocess, no
  model); only the live capture (`--freeze`) needs the casework venv + a model. Nothing is persisted.

## Tests

- `python3 tests/drafter_quality_harness.py --selftest` — the dep-free scorer unit (stub-vs-live sign/refuse,
  verifier-catch, recovery, consistency, the no-model fallback), no venv/model.
- `python3 tests/drafter_quality_harness.py --check` — the regression gate (replay the pinned per-bundle
  capture through the scorer, no model/subprocess). `--freeze` re-captures from the casework venv + a model.
- `node tests/workbench.test.mjs` — the live-draft surface (the signed-STR card, the "✗ refused" consume
  stage, the blocking-violation list, the defensibility-climax fail-closed panel, the honest neural-fell-back
  -to-stub banner, and the consistency-not-correctness framing — "the gate is the oracle on whatever the
  backend wrote").
