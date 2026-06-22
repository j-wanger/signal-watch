---
title: "Phase 67 — Make the LIVE investigator workbench shippable from a bare clone (vendor aml-casework + make setup)"
date: 2026-06-22
phase: phase-67-shippable-live-workbench
ceremony: lite
gates: { direction: accepted (all_accept:true), delivery: accepted }
status: delivered
---

# Phase 67 — The live workbench, shippable from a bare clone

**Why.** The five offline ship artifacts were always self-contained, but the *live investigator workbench* —
the most current, most compelling surface — couldn't run its DECIDE signed-SAR finale without the sibling
`../aml-casework` repo present. The user's call: the live workbench must itself be shippable. Forks resolved
at the gate: live tier = **real pipeline + model-you-provide** (bundle casework so the deterministic SAR
pipeline runs offline; the neural prose needs a model set server-side, not bundled); packaging = **vendor a
copy** (`aml-casework` is local-only / no remote, so a git submodule was a non-starter — verified).

## What moved

- **T1 — vendor + the A0 guard.** `scripts/vendor_casework.sh` rsyncs casework's runtime
  (`src/aml_casework` + pyproject + uv.lock + README) into `vendor/aml-casework/`; `make setup` builds the
  venv (`uv sync`); `VENDORED_AT` pins casework@`81df91c`. The venv is gitignored, the source committed.
- **T2 — resolution.** `serve_chain.CASEWORK_DIR` now resolves **`$AML_CASEWORK_DIR` > the vendored copy >
  `../aml-casework` sibling > a named GATED stage**. Both servers use it; the subprocess/file-handoff is
  unchanged (build.py never imports casework).
- **T3 — docs.** README ("shippable vs companion" now says the workbench ships too) + CLAUDE.md run section
  + `docs/case-workbench.md` "Run it" all lead with `make setup`; the 3.11+uv live-tier prereq is stated.
- **T4 — regression + the shippability e2e + smoke.**

## The A0 guard earned its keep

A0 (the weakest assumption) was "the vendored venv builds standalone AND a stub DECIDE runs offline," to be
**proven before building further**. Proving it in a no-siblings `/tmp` clone surfaced a **hidden coupling**:
casework's `corpus_grounding` verifier grounds each SAR alert against a *pinned signal-watch corpus snapshot*
it expects under `fixtures/corpus/` — vendoring `src/` alone left every SAR corpus-gated (`signed: false`).
Fix: vendor casework's `fixtures/corpus/` too (5 derived FinCEN-alert records — signal-watch's own
public-domain corpus). Re-proven: a signable bundle → `signed: true`, zero violations, stub drafter, **no
model, no sibling, no env**. Had this not been caught, "shippable" would have been false on every real device.

## Verification (exit)

A true isolation e2e — a clone rsync'd into a dir with **no sibling repos present** (`../aml-casework` and
`../aml-substrate` both absent): `make setup` → venv built; `serve_chain.CASEWORK_DIR` → `vendor/aml-casework`;
`serve_workbench --selftest` PASS; the DECIDE finale → a **signed SAR offline**. Plus `uv run pytest` 18/18,
`node tests/workbench.test.mjs` 103/0, `build.py --check all` 8/8 ZERO dist drift, `build.py` imports no
casework. A composed mule still `fail_closed`s at the verifier — the designed defensibility climax, unchanged.

## Decisions / notes

- Gate all_accept:true (A0 verify-first/escalate-to-wheel · A1 distribution-not-coupling · A2 copy+refresh+pin
  · A3 3.11+uv live-tier-only · A4 compliance-clean); all HELD at delivery (ledger Phase-67 revisit-status).
- **Vendoring is a distribution choice, not import-coupling** — the parallel-pillar boundary holds at the
  code level (subprocess + file-handoff; build.py clean; dists byte-frozen). The filesystem co-locates the
  pillars; the contract between them is unchanged.
- `make setup` needs network ONCE (to fetch casework's deps: anthropic, pydantic, …); the workbench then runs
  offline. The neural tier is opt-in via a server-side model/key (the browser never sees it, §4.5).
- Verified by the isolation e2e + regression + a self-check — NOT the multi-agent adversarial pass (no
  honesty/gate logic changed; this is packaging). Latent note: casework's corpus_grounding *drift check*
  (a non-enforcement path) points at a sibling path that won't resolve from the vendored location — harmless
  (the enforcement path uses the vendored snapshot), worth knowing if casework's drift check is ever relied on.
- Grounded against signal-watch HEAD (Phase-66 `0fa3830` + the doc-hygiene `7340012`) and aml-casework@`81df91c`.

### Review Gate (dev-debrief Step 5 — size-gated, 4 tasks → unified reviewer)

**Score 10/10 · verdict: accept · no issues.** The reviewer independently re-verified the load-bearing
claims by running commands: `build.py` imports no casework/vendor (grep empty); `--check all` 8/8 ZERO
dist drift; the consume is a subprocess/file-handoff (no import); the vendored content is casework's 15
.py modules + signal-watch's own public-domain FinCEN-alert derived records (no PII / customer / txn data);
`CASEWORK_DIR` resolves to the vendored copy with no env; and the headline holds — multiple cases sign a
SAR fully OFFLINE through the vendored casework with all model/sibling env unset, while composed mules
fail-close at the C3 grounding_replay verifier (the documented climax). Two non-blocking suggestions:
(1) self-document the `fixtures/corpus` coupling next to that rsync — *already covered* by the comment
above the line; (2) the `make setup` echo points at `serve_workbench.py` while the resolution logic lives
in `serve_chain.py` (discoverability only — fine as-is). No HIGH+ findings; no inline fixes required.

### Gate Compliance + Assumption-Ledger Revisit (Step 21)

`gate-log:phase-67 direction=approved delivery=accepted` — compliant (2-gate ceremony). The Phase-67
ledger block's A0–A4 all carry a filled `revisit-status` (HELD/PROVEN, with verification detail) — no
blank rows. Cooldown: 2 phases (66 + 67) completed this session → a fresh session is advised for Phase 68.
