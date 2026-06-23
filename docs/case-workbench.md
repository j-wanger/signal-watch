# Investigator Case Workbench (Phase 63)

A presenter-driven demo that walks a bank stakeholder through **clutter → clarity → live decision** over a
**real (synthetic) aml-substrate alert population**. Companion-served (dev/authoring-time only); **not a
ship artifact** — `workbench.html` is served by `scripts/serve_workbench.py`, never built into `dist/`,
and the offline ship files stay byte-frozen.

> Badge always on: **Illustrative data & outputs**. Synthetic throughout. **Grounded detection,
> illustrative dispositions** (the Phase-62 split).

## What it is

The capstone that ties the three pillars together in one investigator surface:

- **aml-substrate** (Pillar 1) emits the evidence — real detectors firing real advisory-grounded alerts
  over real (synthetic) KYC profiles.
- **signal-watch** renders the investigator view + the grounded signals + the precedent-confidence read.
- **aml-casework** (Pillar 2) decides the case live — drafts + verifies an STR, or **refuses to sign**.

## The three beats

1. **Clutter** — a queue of ~200 real cases + a per-case dense investigator page: the full KYC profile
   (risk/CDD/PEP/sanctions/adverse-media/occupation/source-of-funds/expected-activity), accounts, a
   by-channel activity summary, counterparties, and the **full transaction table** — the wall of
   information an investigator opens cold. A clearly-**synthetic display identity** (name/DOB) is laid
   over the **real** grounded KYC (the substrate omits PII by privacy design).
2. **Signals on** — a master switch. The grounded signals surface, the cited transactions highlight, and
   the **risk picture** composes: the typologies, the **precedent read** (N similar prior firings of this
   signal combo — a **real** sample size), and the **gate** (auto-clear / review / human-gate). The
   flag→corpus **audit walk** shows every signal tracing to a public-source regulator indicator. Clutter
   → clarity. **No catch-rate, precision, or lift number anywhere** — the value is grounding, clarity,
   corroboration, and defensibility, never a higher catch rate (the substrate detection-lift triple-null
   governs).
3. **Decide (the live finale)** — the workbench calls `serve_chain → aml_casework.ingest` on the selected
   case (default Claude, configurable openai/opencode, deterministic-stub fallback). Two honest outcomes:
   - **Signed SAR** (disposition: file) — the verified narrative, grounded end-to-end.
   - **Fail-closed** (disposition: escalate) — the case-investigation pillar **refuses to sign** because
     its six Class-G verifiers independently re-derive each signal and couldn't reproduce it from the
     cited evidence. Routed to a human, never auto-filed, never silently dropped. **That refusal is the
     defensibility.**

## The precedent-confidence mechanic

Each case carries a confidence read anchored to a **real** number — the firing frequency of its
fired-signal combo across the full emitted population. The mechanic: **common combo = large precedent
sample = auto-clear; rare composition = small sample = human gate.** The disposition *direction* (clear
vs escalate) stays **illustrative** ("chosen, not measured" — the substrate is label-blind). The sample
size is real; the disposition is not.

The gate funnel over the vendored slice: **189 auto-clear / 66 review / 39 human-gate** (Phase 66
re-vendored a wider 294-case slice — see *Workbench richness* below) — the firehose collapsing to a real
human workload.

## The precedent-confidence gating engine + the elicitation loop (Phase 64)

Phase 63 **displayed** the gate (the funnel, a frozen label per case). Phase 64 makes the routing a
**live, parameterized control** with a feedback loop — blueprint §14's continuous adjudication loop, the
LFCM elicitation path. The mechanic is unchanged; what moves is that it now *runs*.

**The policy is a knob, not a constant.** The routing thresholds (`auto-clear at ≥ N prior firings`,
`review at ≥ M`) are an explicit `gating_policy` — **chosen, not measured** — adjustable live in the
gating panel. `route(n_precedent, policy)` is **one pure function**: `curate_workbench_cases.py` bakes
the baseline gate with it, and `serve_workbench.py`'s live engine re-derives routing from the *same*
function, so the live funnel can never drift from the committed one (the selftest asserts the default
policy reproduces **189 / 66 / 39**). Routing is **monotone** — a larger precedent sample never yields a
stricter gate.

**The elicitation loop.** A human adjudicates a gated case (`POST /adjudicate`); that disposition becomes
**precedent** — the combo's session sample grows by one — confidence recomputes, and the next similar
case may re-route toward auto. Session-only and **in-memory: nothing is persisted** (committing a record
stays a human-reviewed act). As precedent accumulates on a pattern, the human-gate funnel shrinks and
judgment **concentrates on the sparse / novel patterns** — the bank's scarce judgment spent where there
is no precedent to lean on.

**The §12 / §14 honesty seam (load-bearing).** The loop grows the **count** — the **§12**-grounded real
firing frequency — and routes on it. The disposition *direction* it records and auto-applies stays
**§14-illustrative** (label-blind; recorded as precedent *volume*, never as a correctness signal). The
loop demonstrates *where human judgment is spent and how precedent concentrates it* — it **never claims an
auto-disposition is correct**. This holds the Phase-62 boundary: route on §12 *measurement*; do **not**
re-ground §14 from the substrate's label-blind history. The thresholds are presenter knobs, not a
calibration; the funnel is honest counts, never a precision/lift figure.

**Executed once over the real slice.** The engine ran live over the committed slice (Phase 64 over the
then-200-case population; Phase 66 re-vendored it to **294 cases**, funnel re-derived to **189 / 66 / 39**):
the live funnel reproduces the baked one, and the loop shifts a real decision — a near-threshold human-gate
case crosses to **review** after a few adjudications grow its combo's precedent past the review threshold,
the human-gate funnel ticking down by one. The knobs move it instantly too — dropping the review threshold
folds the rare composed cases out of the human queue, live.

## The agentic evidence-gathering loop (Phase 65)

The **GATHER** beat sits between *signals-on* and *decide*: having read the grounded signals, the
investigator gathers EXTERNAL evidence. A companion **agent loop** — signal-watch's first multi-step
tool-calling loop (`scripts/osint_tools.py`) — calls a fixed set of deterministic tools over a
**committed SYNTHETIC OSINT corpus** (`data/osint/corpus.json`: fictional registry / adverse-media /
sanctions records), and EVERY proposed finding is **grounded-or-stripped** by the shared `news_ground`
gate before it can render.

**The chained discovery (the payoff).** `lookup_registry(subject)` surfaces an affiliated entity →
`screen_sanctions(that entity)` returns the OFAC hit the investigator would never have spotted in the
transaction clutter → `screen_adverse_media`. The agent chooses the hops; the gate disposes each finding;
the grounded links feed a network view.

**The honesty seam (load-bearing) — CONSISTENCY, not correctness.** The gate proves a finding's quote is
a **real substring of the cited synthetic record** (`locate_span`, plus a normalized-length floor, a
single-sentence guard, and a requote to the exact span). It does **NOT** prove the synthesis is a correct
inference, or that the entity is *really* sanctioned. Two consequences, surfaced everywhere:

- the corpus is **fictional** and the chained path is **authored into it, not discovered** — the UI says
  so (a beat-local synthetic-provenance line; the network is labelled "authored over synthetic records,
  not discovered"); the always-on "Illustrative data & outputs" badge stays;
- each finding shows the **grounded verbatim quote** as EVIDENCE beside a **subordinate, labelled
  illustrative synthesis** ("illustrative reading — not verified") — the quote never lends its grounded
  authority to the inference. This mirrors the corpus inverted-extraction doctrine (the verbatim flag
  beside the natural-AML translation).

The gate also closes the bypasses an adversarial design review surfaced: a trivial / punctuation /
one-token quote (the normalized-length floor), a quote stitching two clauses across a sentence break (the
single-sentence guard), an ungrounded **entity or network endpoint** riding a grounded quote (entity and
link must be the subject or grounded in the same record — mirroring the news relationship gate), and a
record-id from a different tool call (the id binds to the immediately-preceding tool's records).
Ungrounded findings DROP **with their reason shown** — the gate firing is the honest moment, not hidden
behind a count.

**Tools + transport.** Three deterministic tools (`screen_sanctions`, `screen_adverse_media`,
`lookup_registry`) over an exact-normalized-name index. The loop is **hand-rolled** (propose-tool →
run-tool → propose-findings → gate → chain), capped at 4 iterations with a no-progress guard; a
deterministic **stub planner** makes it fully offline + reproducible and exercises a planted-ungrounded
DROP. The live transport is the **openai `/v1`** path (a local model — Phase-57 §4.5: the browser sends a
backend NAME only, creds stay server-side; transport errors are sanitized to a class name, never a
host/url), **fail-closed** on any doubt (it never invents a finding). Session-only — **nothing persists**;
`build.py` never imports the gather layer (companion-only, no ship target).

**Executed once, live.** Run once over the mule (CASE-P-0002174 "Zane Zhao") against a local
Qwen3.6-35B: the chain fired end-to-end — registry → discovered *Crescent Dunes Trading FZE* →
sanctions → the OFAC hit → adverse-media (an honest empty). **2 grounded, 0 dropped, 0 fabricated** — the
grounding gate held with the real model. The first live run surfaced a real fix: the planner couldn't
chain until it could *see* the discovered entity (it received only `{tool, n_records}` history); the loop
now threads discovered-entity context into the planner, and the chain fired.

## Workbench richness (Phase 66)

Two demo-visible richness wins + a sibling handoff, governed by one honest constraint.

**A wider slice.** The vendored population grew from **200 → 294 cases** (a deterministic re-emit of the
same `f90bd39`-gen substrate population, then a re-curate with wider caps + a **combo-coverage pass** that
guarantees ≥1 representative of *every* one of the 23 population fired-signal combos — up from 14 surfaced).
More 4+-capability exemplars (85 vs 60), coverage re-measured (**99/294**), the gate funnel re-derived
(**189 / 66 / 39**).

**A deeper OSINT corpus that mirrors the substrate ownership graph.** The GATHER corpus
(`data/osint/corpus.json`) grew to ~24 records across 14 subjects, and its registry records now carry
`relationships:[{src, dst, label, ownership_pct}]` **mirroring aml-substrate's `RelationshipEdge`**
(`BENEFICIAL_OWNER` / `DIRECTOR_OF` / `OFFICER_OF` / `CONTROLS` / `OWNS`). GATHER renders these as a labelled,
ownership-weighted network — two ownership→sanctions chains (a subject's beneficial owner / affiliate that a
sanctions screen then flags), cross-subject ownership links, and honest-clean subjects. **The ownership facts
(label, percent, direction) are read from the synthetic record, never from the model** — the live run
surfaced a model *fabricating* an ownership percent and flipping the direction, so the gate now resolves the
relationship from the record's structured data (the model only grounds the quote + names the two parties).
The percent renders as "N pct" (never "N%" — the no-% honesty rule). This local corpus is the **rendering
prototype** for the substrate's emitted beneficial-owner graph.

**The handoff.** `docs/substrate-determination-signals-PLAN-BRIEF.md` (Phase 70 — supersedes the Phase-66
BO-graph brief) specifies the aml-substrate work to *emit* the real beneficial-owner graph (a `PartyGraphView`,
`related_parties[]` in the bundle, a non-tautological C14 detector) **plus** the internal determination-signal
data + detectors (anticipated-activity, source-of-funds, profile inconsistency) the §12 loop named — and the
emitted ownership shape maps 1:1 onto what GATHER already renders, so the workbench needs no rework when it lands.

**The governor (load-bearing) — single-signal-separable.** Every richness here is **demo-visible** (more
cases, deeper profiles, a richer ownership network) — **never a detection-difficulty or catch-rate claim.**
The substrate's own measurement work found it *single-signal-separable* (composition is architecturally
subsumed by network linkage): more cases / typologies / detectors add visible *volume*, not detection
difficulty. The richness that *compounds* is the network — exactly the BO graph the handoff brief targets.
ZERO catch-rate / precision / lift / % number anywhere.

## Coverage is MEASURED, not assumed (the cross-pillar finding)

The headline coverage number — **99 of 294 cases ground end-to-end** (Phase 66's wider slice; was 57/200) — is **measured**, not a capability
proxy: `curate_workbench_cases.py --measure-casework` runs aml-casework's deterministic stub over every
vendored bundle and records `grounds_e2e` per case.

The gradient is the finding: **1-cap 16/17 sign, but 4-cap 5/56 and 5-cap 0/4.** The more composed the
case, the more likely casework **refuses**. The cause is a real **substrate↔casework C3/C15 replay
divergence**: the substrate's C3 is fan-**in** (funnel receipts) but casework's C3 replay checks
fan-**out**; the C15 shell thresholds disagree. casework@c6d8401 is the oracle — **the verifier is never
loosened**; the refusal is surfaced honestly as the `e2e_note` and demoed as the fail-closed climax. The
composed-case frontier is real cross-pillar engineering (a C3/C15 contract alignment), deferred to a
sibling-repo phase.

## Run it

**From a bare clone — the shippable live workbench (Phase 67):**

```bash
python scripts/setup_workbench.py   # CROSS-PLATFORM (Win: python scripts\setup_workbench.py; POSIX: make setup)
                                     #   builds vendor/aml-casework/.venv from the committed wheel — Python >=3.11 + uv-or-pip, network once
python scripts/serve_workbench.py   # http://localhost:8030 — the FULL arc incl. the DECIDE signed-STR finale, OFFLINE, no sibling
#   aml-casework is VENDORED into vendor/aml-casework/ (src + a cross-platform WHEEL under dist/ + its pinned
#   corpus snapshot under fixtures/corpus/). resolution: AML_CASEWORK_DIR > vendored > ../aml-casework > GATED;
#   the venv-python + SIGNAL_WATCH_CORPUS are resolved cross-platform (serve_chain.casework_python/_corpus_env).
#   auto-default drafter = stub (offline). For neural: the "openai" backend DEFAULTS to a local model at
#   127.0.0.1:8080 (just start one + pick openai — NO env; OPENAI_BASE_URL only OVERRIDES host/port), or set
#   ANTHROPIC_API_KEY|ANTHROPIC_AUTH_TOKEN for "claude" — SERVER-SIDE; the browser sends a NAME only (§4.5).
#   refresh the vendored copy + rebuild the wheel (POSIX maintainer): scripts/vendor_casework.sh
```

Without setup, the workbench still runs clutter → signals → GATHER on the stdlib stub; only the DECIDE
finale is GATED (a named stage, never a crash).

**Re-vendor the case population (authoring-time only — needs `../aml-substrate`):**

```bash
PYTHONPATH=../aml-substrate/src ../aml-substrate/.venv/bin/python -m aml_substrate.cli \
    --clients 40000 --months 2 --seed 0 --emergence --monitor --emit-evidence --emit-screening \
    --out /tmp/sw-wb-run
python3 scripts/curate_workbench_cases.py --from /tmp/sw-wb-run/evidence --measure-casework ../aml-casework
```

Offline `dist/*` are unaffected (the workbench is never built). Privacy by check: synthetic data only, nothing
real leaves the box; no key/token in the frontend. Vendoring aml-casework is a **distribution** choice —
`build.py` never imports it; the companion subprocesses the vendored CLI over the file-handoff.

## The DETERMINATION beat (Phase 69) — evidence-sufficiency, not frequency

Between GATHER and DECIDE the workbench now asks the load-bearing question: *is there enough evidence for a
**determination**, or only a defensive filing?* The decision is licensed by a per-typology
**evidence-requirement profile** (`data/workbench/evidence-requirements.json`, chosen-not-measured) — a
money_laundering determination needs a mechanism atom (placement/layering / evasion-intent) **AND ≥2 corroborating legs**
(network, external corroboration, profile-inconsistency, anticipated-activity, source-of-funds) **AND** a
**named predicate risk** (the specific risk we file for) **AND** **no unrebutted mitigation**. The Phase-64
combo-frequency gate is **demoted to context** — it decides *where* to spend judgment, never *that* a
determination holds. `POST /determine` (pure; `scripts/evidence_requirements.py` `determine` / `serve_workbench
determine_case`) returns the verdict; `named_risk` + `mitigation_rebutted` are the **human elicitation**.
Insufficiency is a legitimate non-decision whose gaps NAME what to gather; the unmet, **non-gatherable** atoms
become a **§12 substrate-signal brief** (what to build next). Measured over the population: every auto-clear
case is `needs_more_info` from signals alone (no case reaches the ≥2-leg bar) — the defensive-filing exposure,
concrete. The live execute-once held the honesty seam (zero structured-fact fabrication; the determination
withholds honestly when the live gather under-closes). Full design: `docs/evidence-driven-filing.md`.

## Tests

```bash
node tests/workbench.test.mjs                 # the full arc: clutter, signals-on, finale (signed + fail-closed), the GATING panel + knobs + the adjudication LOOP, XSS, both motion modes, no catch-rate/% vocabulary
python3 scripts/serve_workbench.py --selftest # the companion: queue/detail, grounded walk, the live finale (stubbed) + the fail-closed disposition, the live GATE engine (funnel reproduced + monotone) + the elicitation LOOP (re-route + persists-nothing), §4.5 no-leak, pillar-status byte-stable
python3 scripts/curate_workbench_cases.py --selftest  # the committed slice: schema, exemplars span the gates, MEASURED coverage matches per-case grounds_e2e, route() faithful to the baked gate
```

## Deferred to follow-on phases

- The substrate **determination-signal emission queue** (the real ownership graph + the internal legs —
  anticipated-activity, source-of-funds, profile inconsistency — and a kyc/TF case slice; would let the
  GATHER network + the determination atoms draw on real emitted signals rather than the synthetic corpus) —
  **consolidated in Phase 70** (`docs/substrate-determination-signals-PLAN-BRIEF.md`, superseding the Phase-66
  BO-graph brief); the consume side already renders the ownership shape. Sibling-executed.
- The **C3/C15 cross-pillar contract alignment** (substrate fan-in vs casework fan-out) — the
  composed-case grounding frontier.
- A **real OSINT substrate** for the GATHER loop (a real screening list / registry feed) — out of scope
  here by the no-real-data non-negotiable; the synthetic corpus demonstrates the gather→ground→chain loop
  without it.
- **Precedent-confidence as a *governed* control** — Phase 64 made the gating mechanism live; a real
  deployment would add the calibration + monitoring (SR-11-7) that turns the "chosen, not measured" knobs
  into measured thresholds, and would source dispositions from a real adjudication record (not the
  substrate's label-blind history — the §12/§14 boundary still binds).

> **Built in Phase 64:** the precedent-confidence **gating engine + the elicitation loop** (above) — the
> confidence display became a live routing control with an adjudicate→grow-precedent→re-route loop.
>
> **Built in Phase 65:** the **agentic evidence-gathering loop** (above) — the GATHER beat: a companion
> agent loop gathers counterparty/OSINT/sanctions evidence over a committed synthetic corpus, every finding
> grounded-or-stripped (consistency, not correctness), feeding an authored-not-discovered network. Executed
> once live; the registry→sanctions chain fired with the local model, 0 fabricated.
>
> **Added in Phase 66:** a wider **294-case** slice (full 23-combo spread), a deeper GATHER OSINT corpus whose
> ownership records **mirror the substrate `RelationshipEdge`** (the rendering prototype for the emitted BO
> graph; ownership read from the record, never the model), and the **aml-substrate BO-graph emission handoff
> brief**. Governor: demo-visible richness, never detection difficulty (single-signal-separable).
