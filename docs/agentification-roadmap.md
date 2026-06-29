# Agentification roadmap

> **The road to agents doing the judgment-heavy work — under deterministic gates, with humans on the
> decision.** This is a coordination + sequencing doc, not a new design: the design contract is the M9
> program blueprint (`program-blueprint.md` §2 universal grounding · §4 per-workload substrate+verifier · §6
> the gateability criterion · §11 the human-work charter). Synthetic / illustrative throughout; **no rate,
> score, or multiplier is claimed.** Code-verified 2026-06-29 (file:line, not recall).

## The thesis (why agentification is the appeal — and stays defensible)

Every agentic surface in this system has the SAME shape:

> **an agent PROPOSES / EXTRACTS → a deterministic gate DISPOSES → a human DECIDES.**

That single pattern is what makes the system *both* agentic (it scales the language-and-judgment-heavy work —
reading advisories, extracting flags, gathering evidence, drafting narratives) *and* examinable (every agent
output is grounded-or-dropped by a replayable gate, and no agent ever files an STR). An examiner can replay
the gate byte-for-byte over the cited source and confirm nothing on screen is ungrounded; the **decision** to
license a filing is a deterministic, public-guidance-authored predicate, never a learned-from-labels judge.
The roadmap below extends the pattern; it never relaxes it.

## Built today — the pattern proven in 6 live loops (the proof it works)

All five share ONE transport (a local OpenAI-compatible model at `127.0.0.1:8080/v1`), so **a single local
model lights up every live demo at once** (no per-loop wiring). The offline ship artifacts make ZERO
model/fetch call (the live code is build-stripped, §4.5) — the agentic work is companion-served only.

| Loop | The agent's job | The deterministic gate | Demoable today |
|------|-----------------|------------------------|----------------|
| **News extraction** (`serve_news.py:272`, `news_ground.py:87`) | extract entities/aliases/red-flags from pasted text or a fetched URL (+ a keep-biased verify pass) | grounded-or-stripped: every name a RAW substring of the article body | needs a live model on :8080 (honest error if absent) |
| **Corpus derivation** (`serve_corpus.py:208`, `derive_signals.py:364`) | propose {section, verbatim flag, red-flag, C/D codes} per indicator | the FROZEN `check_record` gate disposes + **one** violation-guided re-prompt, then drops honestly — the most rigorously gated loop | needs a live model on :8080 |
| **GATHER** (`osint_tools.py:463`, `LivePlanner:405`, `gate_finding:230`) | agentic **tool-calling** over a synthetic OSINT corpus — chains multi-hop, seeks the unmet determination atoms | each finding grounded-or-dropped against the exact records that tool returned | **YES, offline** — `StubPlanner` is the deterministic default + the coverage reference; the live path is the under-test variant |
| **DECIDE drafting** (`serve_workbench.py:388`, the `serve_chain` Drafter Protocol) | draft the STR narrative (claude / openai / opencode drafters) | casework's six grounding verifiers refuse to sign what they can't reproduce | **YES, offline** — deterministic stub drafter; live drafters wired via creds/endpoint |
| **Merge adjudication** (Phase 83 — `serve_merge.py`, `merge_adjudicator.py`, `tests/merge_adjudicator_quality_harness.py`) | propose each merge call (uphold / reject / both-defensible / escalate) + a rationale from the evidence ONLY (the oracle firewall) | scored against the committed non-circular oracle — the ONE gate with a correctness oracle; the `StubAdjudicator` (echo the spine) is the deterministic baseline | **YES, offline** — the stub baseline is dep-free + always checkable; the live agent is the under-test variant on :8080 |

## The roadmap — the next agentic loops (sequenced by leverage × dependency)

The striking finding: **the seams and the gates already exist** — these are mostly *wire a live model to an
existing seam, measure its quality against an existing gate*, not new infrastructure. Each stays under the
propose→gate→decide discipline.

### Stage 1 — the MEASURABLE agent: a merge adjudicator scored against the oracle  ✅ **BUILT (Phase 83)**
**The standout agentic-evaluation story — now live.** The merge console is the ONE gate with a **non-circular
`GT-<hash>` correctness oracle** (`resolution_scorer.py`, the resolver-input firewall enforced at the schema
boundary). The agent proposes each merge call (uphold / reject / both-defensible / escalate) from the evidence
ONLY (the oracle firewall — `merge_adjudicator.adjudicator_input` + `assert_no_oracle_leak`), and its judgment
is **measured against the latent truth** — the most credible "how good is the agent, *really*?" claim in the
system. **Measured (counts only, synthetic + synthetic-aml-substrate-slice oracles; no rate, score, or
multiplier):** over the 66 committed scored cases the agent matched the oracle on **54**, vs **33** for the
deterministic `StubAdjudicator` (echo the spine) — it recovered **21 of the 33 cases the deterministic
resolver got wrong** (18 of 30 fragmentation-gaps + all 3 over-merge-traps). Surfaced as the **5th companion
live loop** (`serve_merge.py` + a build-stripped overlay in `merge.html`; all 9 ship dists byte-frozen) and
pinned as a regression gate (`tests/merge_adjudicator_quality_harness.py`). The human still adjudicates; the
agent's call is a measured proposal beside the latent truth. Full walkthrough: `docs/merge-live.md`.

### Stage 2 — the HIGH-VALUE agent: a §12 determination pre-proposer  ✅ **BUILT (Phase 85)**
An agent reads the case EVIDENCE (the fired capabilities + the mapped crime type — the oracle firewall:
`determination_proposer.proposer_input` + `assert_no_oracle_leak`, reused from the validation harness) and
proposes **file / clear / needs-more-info + a rationale**, measured **two-sided** against aml-substrate's
EXOGENOUS `intended_disposition` oracle (the Phase-78 capture, authored blind to the sufficiency rule — the
SAME non-circular oracle the determination-validation harness uses) vs the deterministic engine baseline. The
seam was already built — `determine_case` takes `named_risk` / `mitigation_established` as override kwargs; the
**A1-frozen** sufficiency engine still LICENSES the determination, the human still DECIDES; the proposal is a
presentation beside the gate, never an engine input. **Measured (counts only, synthetic substrate slice — no
rate, score, or multiplier; the full 6935-case capture, the agent deduped to 46 cap-signatures so the whole
population is covered, with a base-rate-informed prompt):** the live agent (a local Qwen MoE) **eliminated all
727 KYC structural over-flags** the rigid rule marks file-ready (a customer-due-diligence gap alone is not a
filing basis) and **committed `file` on 74 oracle-file cases vs the engine's 50** (higher file sensitivity) —
but it **over-files on the volume ML class** (committed-wrong **4482** vs the engine's **593**), because it
reasons from per-case red-flag CO-OCCURRENCE without the base-rate prior the calibrated rule encodes. Even
GIVEN the public base-rate context, a per-case agent over-files on the dominant `C2|C3|C8` signature (4040
cases, 4029 benign) — the benign-ness is a POPULATION property invisible in a single case. **The honest
finding VINDICATES propose→gate→decide:** the agent is a sensitivity-rich *proposer* (it surfaces files +
fixes the structural KYC over-flag); the deterministic engine + the human gate supply the population-calibrated
discipline the per-case agent cannot. Surfaced as the **6th companion live loop** (`serve_workbench.py`
`/propose-determination` + the proposal panel in `workbench.html`; all 9 ship dists byte-frozen,
`evidence_requirements.py` byte-unchanged) and pinned as a regression gate
(`tests/determination_proposer_quality_harness.py`). Full walkthrough: `docs/determination-live.md`.

### Stage 3 — the DRAFTING agent: a real STR drafter behind the verifiers  *(high leverage, near-zero new code)*
Replace the deterministic stub drafter with a real agent drafter — the **Drafter Protocol + a `--drafter`
switch already exist** and the six casework grounding verifiers are backend-agnostic (a hallucinated block is
caught by the fabrication guard). This is exactly the "narrative seam" that fail-closed on a hard case this
quarter — the slot a real drafter fills, while the verifiers keep it honest (signing what it cannot reproduce
stays refused — the defensibility climax). Dependency: a live model + SDK creds.

### Stage 4 — the SECOND-RATER agent: a §14 triage first pass  *(medium leverage, very light dependency)*
The triage console already plumbs a labeled synthetic **second-rater** field end-to-end (curate → build → html
→ test) + an agreement metric. Swap an agent into that slot to produce the first-pass disposition and surface
inter-rater disagreement (decisions, not correctness — the §14 frame). Dependency: a live model constrained to
the §14 disposition vocabulary; NO new gate code.

### Cross-cutting — the EVALUATION discipline (what makes the agentic claim credible)
Every agentified loop ships with an honest quality measure: **oracle-scored** where a ground truth exists (the
merge gate — Stage 1), **consistency-not-correctness** where it doesn't (the GATHER stub-vs-live harness,
`tests/gather_quality_harness.py`, is the model). No agent output is presented without its measure; every
measure is framed as counts only (no rate, score, or multiplier). This track is what turns "we use agents" into "here is how good the
agent is, examinably."

## What stays deterministic / human — by design (the non-negotiables)

These are the load-bearing reason the agentic layer is defensible; agentification never touches them:

- **The grounding gates** — `news_ground` quote-grounding, `derive_signals.check_record` + the cover×data
  matrix, the news fuzzy matcher (REAL Jaro-Winkler scores). Replayable by an examiner, no neural judgment.
- **The §12 sufficiency RULE** (`evidence_requirements.py`, A1-frozen) — a deterministic, public-guidance
  predicate licenses a determination; an LLM-judge never replaces it.
- **The decision** (file / clear) — a human gate by doctrine (blueprint §12 Class-J / §4); the captured human
  rationale IS the model-risk-governance artifact. Agents propose; humans dispose.
- **The §4.5 boundary** — no keys in the frontend; the offline ship artifacts provably cannot fetch or call a
  model. Compliance-clean by construction.

## Status & sequencing

- **Built:** the 4 original live loops + **Stage 1 (the merge adjudicator — the measured-quality headline,
  Phase 83)** + **Stage 2 (the §12 determination pre-proposer — the propose→gate→decide vindication, Phase
  85)** = 6 live loops. **Next, in leverage order:** Stage 3 (STR drafter — the Drafter Protocol + a
  `--drafter` switch already exist, near-zero new code) → Stage 4 (triage second-rater). Each is independently
  shippable + companion-only; none touches a ship dist or a frozen gate.
- **Contract:** `program-blueprint.md` §2/§4/§6/§11 (the design); this doc is the build sequencing over it.
  Cross-pillar note: signal-watch RUNS the agents; substrate + casework are the deterministic producers/verifiers.
- **The honest frame:** agentification here is mostly *wiring live models to seams that already exist, under
  gates that already exist, with a quality measure attached* — not new infrastructure. The discipline (gate +
  human decision + a measure) is what makes it a credible AML story rather than an LLM bolt-on.
