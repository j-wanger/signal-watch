---
title: "Phase 71: Adopt the substrate v0.3 slice; close the §12 determination loop in the workbench"
aliases: []
category: phases
tags: [companion, cross-pillar, substrate-v0.3, determination-loop, lfcm, vendor]
parents: []
created: 2026-06-23
updated: 2026-06-23
source: plan
status: delivered
scope: ["data/workbench/**", "vendor/aml-casework/**", "workbench.html", "scripts/serve_workbench.py", "scripts/serve_chain.py", "scripts/curate_workbench_cases.py", "scripts/evidence_requirements.py", "scripts/vendor_casework.sh", "tests/workbench.test.mjs", "docs/case-workbench.md", "docs/evidence-driven-filing.md", "docs/substrate-determination-signals-PLAN-BRIEF.md", "tests/smoke-checklist.md", "CLAUDE.md", "HANDOFF.md"]
entry_criteria: "Phase 70 DELIVERED + accepted; aml-substrate shipped its Phase-25 v0.3 slice (CONTRACT_VERSION=0.3, related_parties[] emitted) but the workbench bundles are v0.2 and the network view renders from the synthetic OSINT corpus, not the real related_parties[]; the §12 determination loop is reachable from gathered corroboration but not yet from REAL signals."
exit_criteria: "A case reaches the ≥2-leg determination bar from REAL signals (the §12 closure) via evidence_requirements.determine (NOT via casework); related_parties[] renders in the network view; the kyc_integrity profile fires on a real case; casework accepts v0.3 + the signed finale still signs ≈ the T1-measured count (no regression); --check all 8/8 ZERO dist drift; build.py imports no casework/substrate/osint_tools; uv run pytest + workbench.test.mjs + all selftests green."
---

# Phase 71: Adopt the substrate v0.3 slice; close the §12 determination loop in the workbench

## Objective

Adopt aml-substrate's just-shipped Phase-25 **v0.3** slice (`related_parties[]` on the evidence
bundle — the real BO graph) and CLOSE the §12 determination loop in the investigator workbench: a
case reaches the **≥2-leg determination bar from REAL signals** (not gathered corroboration), the
real `related_parties[]` renders in the network view, and the `kyc_integrity` profile exercises
end-to-end. The §12 closure is the DETERMINATION beat (`evidence_requirements.determine` over the
fired capabilities) — pure signal-watch; it does NOT route through casework. Companion-only; the 8
offline dists stay byte-frozen.

## Scope

Files and modules affected:
- `data/workbench/**` — re-vendor a v0.3 population (curate from a substrate v0.3 emit;
  bundles carry `contract_version` 0.3 + `related_parties[]`)
- `vendor/aml-casework/**` + `scripts/vendor_casework.sh` — re-vendor the casework that whitelists
  v0.3 (the minimal acceptance bump; `VENDORED_AT` re-pinned)
- `scripts/curate_workbench_cases.py` — curate the v0.3 slice (`--measure-casework` against the
  bumped casework for the no-regression number)
- `scripts/evidence_requirements.py` — the §12 closure: ML-A4 (related_parties) + ML-A7 (re-keyed
  C14→SoF) light from REAL signals; the `kyc_integrity` profile exercises
- `scripts/serve_workbench.py` — wire the determination beat to the real signals; the closure selftest
- `scripts/serve_chain.py` — only if the v0.3 bump rides a shared casework-resolution helper
- `workbench.html` — render the bundle's `related_parties[]` as the labelled ownership-weighted network
- `tests/workbench.test.mjs` — the related_parties render arc
- `docs/case-workbench.md`, `docs/evidence-driven-filing.md`,
  `docs/substrate-determination-signals-PLAN-BRIEF.md` (the consume-side note),
  `tests/smoke-checklist.md`, `CLAUDE.md`, `HANDOFF.md` — the true-up (CLAUDE.md/HANDOFF at T5)

## Exit Criteria

- [ ] T1 STOP+REPORT (scratch only, nothing committed): 4 measurements — (a) the signed-finale count
      preserved against the bumped casework (the A1 no-regression check, ~99/294), (b) # cases reaching
      ≥2-leg from REAL signals via `evidence_requirements.determine` (the A2 §12 number), (c) ≥1
      kyc_integrity case present + its profile fires, (d) `related_parties[]` present on the bundles —
      A1/A2 resolved with real numbers before T2 commits
- [ ] casework `KNOWN_CONTRACT_VERSIONS` += "0.3" (sibling change) + `vendor_casework.sh` re-vendor
      (`VENDORED_AT` updated); `data/workbench/bundles/*.json` carry `contract_version` 0.3 +
      `related_parties[]`; `serve_workbench --selftest` finale signs ≈ the T1-measured count (no
      regression); `curate --selftest` passes vs the new slice
- [ ] `workbench.test.mjs` asserts a case's `related_parties[]` renders as the labelled
      ownership-weighted network; no %/catch-rate/precision/lift vocabulary; XSS-escaped
- [ ] `serve_workbench --selftest` asserts ≥1 case reaches the ≥2-leg determination bar from REAL
      signals (the §12 closure) AND the `kyc_integrity` profile fires on its case
- [ ] `--check all` 8/8 ZERO dist drift; build.py imports no casework/substrate/osint_tools;
      `uv run pytest` + `workbench.test.mjs` + `curate`/`serve_workbench`/`evidence_requirements`
      selftests green; honesty greps clean (no catch-rate/precision/recall/lift/% in workbench.html)

## Constraints

- Companion-only — NOT a ship target; build.py imports no casework/substrate/osint_tools; the 8 offline
  dists stay BYTE-FROZEN (`--check all` 8/8); the agent runs server-side (browser sends a backend NAME
  only — §4.5). Vendoring is DISTRIBUTION not coupling — the companion subprocesses the vendored CLI
  over the file-handoff. *Prevents: a companion edit leaking into a ship artifact / a sibling import
  into build.py.*
- §12 closure is the DETERMINATION beat, NOT the signed STR finale — the determination
  (`evidence_requirements.determine`) is pure signal-watch and does not route through casework. The
  signed DECIDE finale (subprocesses to vendored casework) is a SEPARATE later beat; the casework v0.3
  bump here only keeps it signing on v0.3 cases. *Prevents: conflating the §12 evidence-sufficiency
  closure with the file-handoff signing path.*
- Measure-first — T1 re-vendors + bumps in a SCRATCH dir and STOP+REPORTs the no-regression + ≥2-leg
  numbers before ANYTHING commits (mirrors the substrate's own P25 verifier-first/STOP+REPORT shape).
  *Prevents: committing a v0.3 slice that silently regresses the signed finale or fails to close the
  loop.*
- The Phase-66 honesty guard — structured facts (ownership label/pct/direction) read from the BUNDLE,
  never the model; "N pct" not "N%"; demo-visible richness, ZERO catch-rate/precision/lift number (the
  single-signal-separable governor). *Prevents: the model authoring an ownership fact (the Phase-66
  ownership-pct lesson) / a detection-difficulty framing.*
- Deeper new-detector verifiers DEFERRED — the casework verifiers for the new C14/C1 detectors (so
  v0.3-SPECIFIC cases SIGN, not just DETERMINE) are a casework-pillar follow-on (the C3/C15 pattern).
  This phase delivers DETERMINE on real signals + the minimal casework acceptance bump. *Prevents:
  scope-creep into a sibling-repo verifier build.*

## Checkpoints

- After T1 (the keystone): STOP+REPORT the 4 measurements. If A1 shows a finale regression (the
  v0.3-curated slice signs materially fewer than ~99/294) → STOP-and-surface (do not commit T2). If A2
  shows ZERO cases reach ≥2-leg from real signals → STOP-and-surface (the §12 closure is unreachable;
  report, do not force).
- If the casework v0.3 bump is NOT one-line-cheap (validate_bundle gates on more than the version
  whitelist) → STOP-and-surface; the deeper acceptance work is a casework-pillar phase.
- If a live run shows a model-authored structured fact → record-source / sweep / fail-closed, never
  render the fabrication (the Phase-66 lesson).

## Assumptions

- A0 [boundary, accept] companion-only / build.py imports no casework/substrate/osint_tools / 8 dists
  byte-frozen / agent server-side (§4.5) / vendoring is distribution-not-coupling. If false:
  STOP-and-surface.
- A1 [T0, don't-know → T1 probe] the minimal casework bump (version whitelist + re-vendor) PRESERVES
  the existing ~99/294 signings (no finale regression). T1 MEASURES it in a scratch dir before T2
  commits. If it regresses: STOP-and-surface, do not commit the slice.
- A2 [don't-know → T1 probe] the re-vendored v0.3 slice contains a case reaching the ≥2-leg
  determination bar from REAL signals (not gathered corroboration). T1 MEASURES the count. If zero:
  report the measurement, do not force a synthetic close.
- A3 [accept] §12 closure = the determination beat (≥2-leg from real signals), NOT the signed STR
  finale; the determination is pure signal-watch and does not route through casework. If the bar can
  only be reached via gathered corroboration: re-word, do not claim a real-signal closure.
- A4 [accept] include the minimal casework v0.3 acceptance bump (whitelist + re-vendor) as an in-scope
  cross-pillar DEPENDENCY; defer deeper new-detector verifiers to a casework phase. If the bump can't
  stay minimal: STOP-and-surface.
- A5 [accept] `related_parties[]` mirrors the Phase-66 OSINT corpus shape 1:1 → the existing network
  render consumes it with no rework; ownership facts read from the bundle, never the model. If the
  shape diverged: document the delta, keep ownership record-sourced.
- A6 [accept] measure-first — T1 STOP+REPORTs the no-regression + ≥2-leg numbers before anything
  commits (the substrate P25 verifier-first shape). If T1 can't measure honestly: STOP-and-surface.

## Notes

LITE phase — no decision articles. The three planning decisions (recorded here per the lite ceremony):

1. **§12 closure = the determination beat (≥2-leg from real signals), NOT the signed STR finale.** The
   determination (`evidence_requirements.determine`) is pure signal-watch and does not route through
   casework. The signed DECIDE finale is a separate later beat that subprocesses to vendored casework;
   the casework v0.3 bump here only keeps it signing on v0.3 cases.
2. **Include the minimal casework v0.3 acceptance bump** (version whitelist + `vendor_casework.sh`
   re-vendor) as an in-scope cross-pillar DEPENDENCY. The deeper casework verifiers for the new
   C14/C1 detectors (so v0.3-specific cases SIGN, not just DETERMINE) are a DEFERRED casework-pillar
   follow-on (the C3/C15 pattern). User chose "Bump + re-vendor (full E2E)".
3. **Measure-first.** T1 re-vendors + bumps in a SCRATCH dir and STOP+REPORTs the no-regression +
   ≥2-leg numbers before anything commits — mirroring the substrate's own P25 verifier-first/STOP+REPORT
   shape.

Cross-pillar reality CODE-VERIFIED at planning (the cross-pillar rule — verify the sibling's live
state, never reason from loaded pins; the brief's prior pin b53855c was STALE):
- **aml-substrate @443e4a6** is v0.3 — `evidence.py:49 CONTRACT_VERSION="0.3"`, `related_parties`
  emitted (its Phase-25 slice).
- **aml-casework @021fb80** (the live sibling AND the vendored copy) is
  `KNOWN_CONTRACT_VERSIONS=("0.1","0.2")` — REJECTS v0.3 (`contract.py:48/391`). The gating dependency
  is casework and it is CHEAP: `validate_bundle` gates only on the version whitelist + tolerates
  unknown extra fields → a one-line bump + re-vendor SHOULD preserve the ~99/294 signings (T1 MEASURES
  it).
- **signal-watch @9a7637a** workbench bundles are `contract_version` 0.2; the network view renders
  from the synthetic OSINT corpus (`data/osint/corpus.json`), not `related_parties[]`.

Grounding (no wiki articles — the knowledge wiki is empty): the cross-pillar code-verify rule (memory
`cross-pillar-consume-batch-not-thin`, `cross-pillar-review-verify-sibling-repo`); the Phase-66
record-sourced ownership-fact lesson + the OSINT `RelationshipEdge`-mirroring shape; the
single-signal-separable honesty governor (demo-visible richness, never catch-rate/lift); vendoring is
distribution-not-coupling (the Phase-67 vendor pattern; `scripts/vendor_casework.sh` + `VENDORED_AT`);
the §12 `signal_brief`/`determine` mechanism (`evidence_requirements.py`); the Phase-69 finding that
SoF is null + a C1 DETECTOR (not data) is what ML-A6/A7 need.

Knowledge gaps carried to impl (resolved by T1's STOP+REPORT): A1 — does the minimal casework bump
preserve the existing ~99/294 signings (no finale regression)? A2 — does the re-vendored slice contain
a ≥2-leg-reachable case from REAL signals?

Direction gate 2026-06-23 (NOT all-accept): A0 accept · A1/A2 don't-know→T1 probe · A3/A4/A5/A6 accept.
Ledger Phase-71 block. Grounded against signal-watch HEAD 9a7637a / the Phase-70 workbench /
aml-substrate@443e4a6 / aml-casework@021fb80.
