---
title: "Phase 12: FinCEN corpus derivation foundation (deterministic spine all-14 + LLM proof slice)"
aliases: [corpus-derivation, deterministic-spine, build-recommendation, fincen-corpus]
category: phases
tags: [milestone-m7, authoring-pipeline, derivation, corpus, build-recommendation, llm-backend]
parents: []
created: 2026-06-05
updated: 2026-06-05
source: plan
status: active
ceremony: lite
scope: ["scripts/derive_signals.py", ".gitignore", "data/fincen/*.md", "data/fincen/derived/*.json", "README.md", "CLAUDE.md"]
entry_criteria: "M6 vision arc complete (Phases 7–11): the derivation pipeline (crawl→acquire→convert→derive) exists + is guarded + scaled, proven on the single EFE advisory. The 14-advisory FinCEN corpus is already converted to md on disk (gitignored). User wants to expand the demo scope toward a SINGULAR corpus-backed demo where the user picks an advisory; this phase builds the backend foundation (deterministic spine + LLM-derived proof slice), demo expansion deferred to Phase 13."
exit_criteria: "(1) all 14 data/fincen/<id>.md committed (corpus un-gitignored — the derivation surface). (2) extract_red_flags generalized to recognize ≥2 FinCEN red-flag section formats beyond EFE's exact phrasing; a `--corpus` batch mode runs extraction across all 14 and emits a per-advisory report (section-found + flag-count, or NEEDS-ATTENTION); EFE `--selftest` still passes (12+12). (3) deterministic checks — pure build-rec consistency (the categorical recommendation must follow the cover×data matrix) + traceability (every derived signal → a red-flag md line) — with a selftest. (4) the LLM backend (this session, NO API key) derives a 2–3 advisory proof slice into committed data/fincen/derived/<id>.json records: per-indicator status + build recommendation (action + rationale) + build logic for the buildable gaps, each passing the deterministic checks. (5) git diff index.html empty; build.py --check all zero drift; deterministic layer stdlib-only; anthropic still lazy. (6) documented in docstring + README + CLAUDE."
---

# Phase 12: FinCEN corpus derivation foundation

## Objective

Build the backend for an EXPANDED, singular FinCEN demo (the eventual user picks one of 14 advisories
and watches the loop derive its coverage → build recommendations → signal). This phase delivers the
**deterministic spine validated across all 14 advisories** + the **LLM-backend derivation proven on a
2–3 advisory slice**. The demo scope expansion itself (advisory-selection front-end + per-indicator
build-rec render) is deferred to Phase 13.

## Approach

Split exactly as the user drew it:
- **Deterministic spine → exercised on ALL 14** (cheap, offline — the validation surface). The current
  `extract_red_flags` is anchored on EFE's exact phrasing ("Behavioral/Financial red flags … may
  include"); the corpus is heterogeneous (e.g. `fin-2020-a009`, `fin-2021-a003` have zero "red
  flag/indicator" grep hits). Generalizing the extractor to the corpus's varied section formats — and
  cleanly FLAGGING non-conformers rather than mis-parsing — is the substantive deterministic work.
- **LLM backend (this session, me) → prove on a slice, scale later.** I produce the derivation: status,
  cover/data, the per-indicator build recommendation (+ rationale), and the build logic (signal
  definition) for the buildable gaps. NO API key / `--draft` network call — the same session-as-backend
  substitution proven in the Phase-11 T4 recorded run.
- **Boundary preserved (Phase-11 principle, extended to build-rec + build-logic + the corpus):** the LLM
  PROPOSES; the deterministic spine DISPOSES — schema/shape, **build-rec consistency** (the categorical
  recommendation must follow the cover×data matrix; can't tag a `covered` indicator "BUILD NOW"), and
  **traceability** (every derived signal → a red-flag md line in the source).

## Scope

- `data/fincen/*.md` — commit the full 14-advisory corpus (un-gitignore; public-domain FinCEN, reverses
  Phase-10's no-bulk-md call now that the corpus backs the demo).
- `.gitignore` — un-ignore `data/fincen/*.md` (keep `raw/` + `*.draft.json` ignored).
- `scripts/derive_signals.py` — generalize `extract_red_flags`; add `--corpus` batch mode + report; add
  the deterministic build-rec-consistency + traceability checks.
- `data/fincen/derived/<id>.json` (NEW) — the LLM-backend-derived proof-slice records (committed, marked
  LLM-derived + deterministically-checked; NOT ship typology configs).
- `README.md`, `CLAUDE.md` — document the corpus mode + spine-on-all-14 + LLM-backend proof-slice.

Engine `index.html` + `build.py` MUST stay untouched (backend-only phase). config/schema.md untouched
(the derived records are a derive_signals.py artifact, not ship configs).

## Exit Criteria

- [ ] All 14 `data/fincen/<id>.md` committed (corpus un-gitignored).
- [ ] `extract_red_flags` recognizes ≥2 FinCEN red-flag section formats beyond EFE's; `--corpus` runs across all 14 + emits a per-advisory report; EFE `--selftest` still passes (12+12).
- [ ] Deterministic checks: build-rec consistency (cover×data matrix) + traceability (signal → md line), with a selftest; offline, stdlib.
- [ ] LLM backend (this session, no key) derives a 2–3 advisory proof slice → committed `data/fincen/derived/<id>.json`, each passing the deterministic checks.
- [ ] `git diff index.html` empty; `build.py --check all` zero drift; deterministic layer stdlib-only; anthropic import still LAZY.
- [ ] Documented in docstring + README + CLAUDE.

## Constraints (load-bearing)

- **Backend-only** — `index.html` + `build.py` untouched; the demo expansion (selection UI + build-rec render) is Phase 13. `git diff index.html` stays empty.
- **Deterministic spine first, validated on all 14** — extraction + checks run across the whole corpus; the LLM backend only fills judgment for the proof slice.
- **LLM = this session, not an API call** — no `ANTHROPIC_API_KEY` use this phase; the `--draft` network path stays as-is (lazy anthropic untouched). I write the derivation directly, gated by the deterministic checks.
- **Boundary preserved** — LLM proposes the build-rec + build-logic; the deterministic checks (consistency + traceability + shape) dispose. No neural judge at the check boundary.
- **Derived records ≠ ship configs** — `data/fincen/derived/*.json` is an LLM-derived + checked corpus dataset, clearly marked; the 3 hand-curated ship typologies are unaffected.

## Checkpoints

- After T2: if the corpus's red-flag formats are too heterogeneous for a deterministic extractor to cover ≥2 formats cleanly — narrow to a robust section-FINDER that flags non-conformers (don't force a brittle universal regex); report coverage. The report itself is the deliverable.
- After T4: if a derived record can't pass the deterministic checks (inconsistent build-rec / untraceable signal) — fix the check or the derivation; the boundary must hold (a failing record is rejected, not waved through).
- Blocked >3 attempts on a task → ask the user: skip or abort.

## Assumptions

- The 14 md's already on disk are faithful conversions (verified: 12–66KB each, advisory-shaped). If a md is mangled → flag it in the corpus report (don't silently derive from garbage).
- A useful deterministic build-rec exists as a function of cover×data (the LLM proposes the category + rationale; the check enforces the category). If the mapping proves too coarse → the rationale carries the nuance; the category stays the deterministic guardrail.

## Notes

Direction approved by user 2026-06-05: **backend-only this phase** (user chose this over folding a
minimal selectable demo view into Phase 12). Destination = a singular corpus-backed demo with
advisory selection (Phase 13). The build-recommendation-per-indicator ask (raised this session) is
satisfied here as a derived + LLM-proposed + deterministically-checked concept; its RENDER lands in
Phase 13. This opens **M7 (corpus-backed demo)** beyond the completed M6 vision arc.
