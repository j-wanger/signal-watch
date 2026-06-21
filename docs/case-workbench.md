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
- **aml-casework** (Pillar 2) decides the case live — drafts + verifies a SAR, or **refuses to sign**.

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

The gate funnel over the vendored slice: **129 auto-clear / 52 review / 19 human-gate** — the firehose
collapsing to a real human workload.

## The precedent-confidence gating engine + the elicitation loop (Phase 64)

Phase 63 **displayed** the gate (the funnel, a frozen label per case). Phase 64 makes the routing a
**live, parameterized control** with a feedback loop — blueprint §14's continuous adjudication loop, the
LFCM elicitation path. The mechanic is unchanged; what moves is that it now *runs*.

**The policy is a knob, not a constant.** The routing thresholds (`auto-clear at ≥ N prior firings`,
`review at ≥ M`) are an explicit `gating_policy` — **chosen, not measured** — adjustable live in the
gating panel. `route(n_precedent, policy)` is **one pure function**: `curate_workbench_cases.py` bakes
the baseline gate with it, and `serve_workbench.py`'s live engine re-derives routing from the *same*
function, so the live funnel can never drift from the committed one (the selftest asserts the default
policy reproduces **129 / 52 / 19**). Routing is **monotone** — a larger precedent sample never yields a
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

**Executed once over the real slice.** The engine ran live over the committed 200-case population: the
funnel re-derives to the baked **129 / 52 / 19**, and the loop shifts one real decision —
`CASE-P-0003008` (signal combo `C3+C5`, **45** prior firings, human-gate) crosses to **review** after 5
adjudications (sample 45 → 50, the review threshold), the human-gate funnel ticking **19 → 18**. The
knobs move it instantly too — dropping the review threshold folds the rare composed cases out of the
human queue, live.

## Coverage is MEASURED, not assumed (the cross-pillar finding)

The headline coverage number — **57 of 200 cases ground end-to-end** — is **measured**, not a capability
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

```bash
# build the population once (deterministic; substrate seed, no clock):
PYTHONPATH=../aml-substrate/src ../aml-substrate/.venv/bin/python -m aml_substrate.cli \
    --clients 40000 --months 2 --seed 0 --emergence --monitor --emit-evidence --emit-screening \
    --out /tmp/sw-wb-run
python3 scripts/curate_workbench_cases.py --from /tmp/sw-wb-run/evidence --measure-casework ../aml-casework

# serve the workbench (companion, dev-time):
python3 scripts/serve_workbench.py            # http://localhost:8030
#   default drafter = Claude iff ANTHROPIC_API_KEY/ANTHROPIC_AUTH_TOKEN is set server-side, else stub.
#   the browser sends a backend NAME only — creds never cross the wire (§4.5).
```

Offline `dist/*` are unaffected (the workbench is never built). Privacy by check: synthetic data only,
nothing real leaves the box; no key/token in the frontend.

## Tests

```bash
node tests/workbench.test.mjs                 # the full arc: clutter, signals-on, finale (signed + fail-closed), the GATING panel + knobs + the adjudication LOOP, XSS, both motion modes, no catch-rate/% vocabulary
python3 scripts/serve_workbench.py --selftest # the companion: queue/detail, grounded walk, the live finale (stubbed) + the fail-closed disposition, the live GATE engine (funnel reproduced + monotone) + the elicitation LOOP (re-route + persists-nothing), §4.5 no-leak, pillar-status byte-stable
python3 scripts/curate_workbench_cases.py --selftest  # the committed slice: schema, exemplars span the gates, MEASURED coverage matches per-case grounds_e2e, route() faithful to the baked gate
```

## Deferred to follow-on phases

- The **agentic tool-calling** during investigation/narrative (open-source verification, counterparty
  gathering, network/entity-resolution) — tool-gathered evidence extending the grounding chain.
- The substrate **ownership/beneficial-owner graph emission** (a richer network view than the emitted
  transaction counterparty edges).
- The **C3/C15 cross-pillar contract alignment** (substrate fan-in vs casework fan-out) — the
  composed-case grounding frontier.
- **Precedent-confidence as a *governed* control** — Phase 64 made the gating mechanism live; a real
  deployment would add the calibration + monitoring (SR-11-7) that turns the "chosen, not measured" knobs
  into measured thresholds, and would source dispositions from a real adjudication record (not the
  substrate's label-blind history — the §12/§14 boundary still binds).

> **Built in Phase 64:** the precedent-confidence **gating engine + the elicitation loop** (above) — the
> confidence display became a live routing control with an adjudicate→grow-precedent→re-route loop.
