---
title: "Phase 11: Automated derivation (LLM-drafted signal config)"
aliases: [derive-signals, llm-draft, automate-derivation, article-to-signal]
category: phases
tags: [milestone-m6, authoring-pipeline, automation, llm, anthropic, derivation]
parents: []
created: 2026-06-05
updated: 2026-06-05
source: plan
status: completed
ceremony: lite
scope: ["scripts/derive_signals.py", "scripts/requirements-authoring.txt", "config/typologies/*.draft.json", "README.md", "CLAUDE.md"]
entry_criteria: "M6 pipeline proven (Phase 7 manual EFE article→signal derivation) + guarded (Phase 9 build-drift `--check`) + scaled (Phase 10 corpus manifest). The manual article→signal derivation is the remaining M6 vision increment. User chose AUTOMATE over the elder presentation-values true-up AND the fentanyl verbatim re-point at the direction gate, then chose variant B (LLM-drafted definition NOW) over A (deterministic scaffolder only) — both USER OVERRIDES of the planner's recommendation."
exit_criteria: "`derive_signals.py --selftest` extracts the known EFE red-flag counts from the committed md, exits 0 (deterministic, offline); `--scaffold` emits a schema-shaped `<id>.draft.json` skeleton (indicators line-traced, no target/definition); `--draft` (env-keyed, anthropic lazy from the authoring venv) proposes the judgment fields incl. a schema-valid signal `definition`, grounded on red flags + schema + few-shot; the draft round-trips the deterministic boundary (build.py/schema accept a human-reviewed valid config OR reject an invalid draft; committed configs stay deterministic + human-reviewed); `git diff index.html` empty; deterministic layer stdlib-only; anthropic import LAZY; tool absent from engine/build imports; ship artifact never calls an LLM; documented in docstring + README + CLAUDE."
---

# Phase 11: Automated derivation (LLM-drafted signal config)

## Objective

Automate the **article→signal derivation** step that was proven MANUALLY in Phase 7 (EFE
markdown → hand-derived `elder-financial-exploitation.json`). One new authoring-only tool
`scripts/derive_signals.py` turns a committed FinCEN advisory md into a schema-shaped signal
config: deterministically extracting the red flags + scaffolding the skeleton, then proposing
the judgment fields (status, target, the signal `definition`) via the Anthropic API — the last
M6 vision increment.

## Approach

The AUTOMATE override must NOT abandon the standing Phase-9 principle (deterministic validators
at boundaries, against neural judges at the build boundary). **Mechanism: the LLM PROPOSES, the
deterministic validator + the two human gates DISPOSE.** One tool, two layers:

- **Deterministic layer** (stdlib-only, offline, `--selftest`): `extract_red_flags(md)` — a PURE
  parser keyed on the FinCEN section anchors ("Behavioral red flags ... may include:" L454 /
  "Financial red flags ... may include:" L505 in the committed EFE md) → `[{section, n, text,
  line}]`; `scaffold_config(id, flags, meta)` — a PURE function → a schema-shaped config SKELETON
  (`coverage.indicators[]` one per financial red flag with md-line traceability, candidate stubs,
  `advisory_full.text_file` wired, anchor/lift/stats TODO placeholders, NO target, NO definition).
- **Neural layer** (build-time only, manual, `--draft`, env-keyed): adds the judgment fields the
  schema isolates as decisions — proposes a status per indicator, selects exactly one indicator +
  one candidate `target:true` (the buildable gap = `cover:"gap"` AND `data:"available"`), drafts
  the signal `definition` {signal_name, class, features[], logic, window, source, route} — by
  calling the Anthropic API, GROUNDED on the extracted red flags + the schema definition spec +
  existing configs (fentanyl/elder) as few-shot, constrained to schema-valid structured output.
  `ANTHROPIC_API_KEY` from env only (never hardcoded/committed). The `anthropic` SDK lives in the
  gitignored authoring venv (markitdown precedent), LAZY-imported (only inside `--draft`) so the
  deterministic layer + `--selftest` need no SDK.
- **Boundary** (unchanged, deterministic): `--draft` writes `config/typologies/<id>.draft.json`
  (never auto-promoted) → human reviews/edits → `build.py` + schema validate (reject if invalid)
  → human gates the target → commit. Committed configs stay deterministic + human-reviewed.
  `derive_signals.py` is NEVER imported by `index.html` or `build.py`; the ship artifact never
  calls an LLM (HANDOFF §4/§4.5 hold).

T3 consults the **claude-api reference** for the current Claude model id + Anthropic Python SDK +
structured-output/tool-use pattern (retrieval over parametric guessing).

## Scope

Files affected:
- `scripts/derive_signals.py` — NEW authoring-only: deterministic `extract_red_flags`/`scaffold_config` + `--selftest`/`--scaffold` + neural `draft_definition`/`--draft` (lazy anthropic).
- `scripts/requirements-authoring.txt` — add `anthropic` (authoring venv only, never a ship dep).
- `config/typologies/*.draft.json` — scratch DRAFT output (NOT a shipped typology).
- `README.md`, `CLAUDE.md` — document the two-layer model + the LLM-proposes/validator-disposes boundary + the env-key requirement.

Reads the committed `data/fincen/fin-2022-a002.md`. Ship artifact `index.html` and `build.py` MUST stay untouched.

## Exit Criteria

- [x] `derive_signals.py --selftest` extracts the known EFE red-flag counts from the committed md, exits 0 (deterministic layer, offline)
- [x] `--scaffold` emits a schema-shaped `<id>.draft.json` skeleton (indicators line-traced, no target/definition)
- [x] `--draft` (env-keyed; anthropic lazy-imported from the authoring venv) proposes the judgment fields incl. a schema-valid signal `definition`, grounded on red flags + schema + few-shot
- [x] the draft round-trips the deterministic boundary: build.py/schema accept a human-reviewed valid config OR reject an invalid draft (LLM proposes, validator disposes); committed configs stay deterministic + human-reviewed
- [x] `git diff index.html` empty; deterministic layer stdlib-only; anthropic import LAZY; tool absent from engine/build imports; ship artifact never calls an LLM
- [x] documented in docstring + README + CLAUDE (two-layer model + boundary + env-key)

## Constraints (load-bearing)

- **Authoring-only, never in the ship file** — `derive_signals.py` is a developer tool; the engine never imports it, `build.py` stays stdlib, the ship artifact never calls an LLM. Prevents leaking a network/LLM dependency into `file://`.
- **Deterministic layer stdlib-only, anthropic LAZY** — `--selftest`/`--scaffold` run without the SDK; `import anthropic` only inside `--draft`. Prevents the neural dep from creeping into the offline deterministic path.
- **No committed key** — `ANTHROPIC_API_KEY` from env only; `! grep sk-ant`. Prevents secret leakage (HANDOFF §4.5: never keys in the frontend / committed).
- **Boundary preserved (no neural judge at the build boundary)** — the LLM only PROPOSES a `.draft.json`; `build.py` + schema + the two human gates DISPOSE. Prevents the AUTOMATE override from regressing the Phase-9 deterministic-validators-at-boundaries decision.
- **Drafts are scratch** — `config/typologies/*.draft.json` is never auto-promoted to a shipped typology; committed configs stay human-reviewed.

## Checkpoints

- After T3 (`--draft`): if the LLM can't be coaxed (via the claude-api structured-output/tool-use pattern) to schema-valid output that `build.py` accepts — STOP and report; fall back to **variant A** (deterministic scaffolder only; human fills the judgment fields), still a usable increment.
- After T1: if the post-markitdown EFE red-flag list can't be deterministically anchored on the section headers — pivot to a thinner section-bounded bullet capture.
- If blocked >3 attempts on a task: ask the user — skip or abort.

## Assumptions

- The committed `data/fincen/fin-2022-a002.md` red-flag sections are deterministically anchorable on the "Behavioral red flags ... may include:" (L454) / "Financial red flags ... may include:" (L505) headers. If false: thinner section-bounded capture (T1 abort path).
- The Anthropic API, given the red flags + schema spec + few-shot configs and a structured-output/tool-use constraint, can emit a schema-valid signal `definition`. If false: variant A fallback (deterministic scaffolder only).

## Notes

Direction: at the Phase-11 gate the user chose **AUTOMATE** over two smaller forks — the elder
presentation-values true-up (carried from Phase 9) and the fentanyl verbatim re-point to the
now-discoverable `fin-2024-a002`. Both forks, plus the optional manifest `--fetch` cadence,
remain **Future-phase candidates (deprioritized at this gate, not dropped)**. Within AUTOMATE the
user chose variant **B** (LLM-drafted signal definition NOW) over **A** (deterministic scaffolder
only). Both were USER OVERRIDES of the planner: the planner recommended finishing the carried
elder true-up first, then recommended the deterministic-only cut A. Honored. Variant A is now the
documented fallback if the LLM can't hit schema-valid output.

Grounding from planning: Phase 7 hand-derived the elder config from `data/fincen/fin-2022-a002.md`
(target `S-DORMANT-DRAIN-ELDER` ← md line 507) — that manual step is exactly what this phase
automates. The red-flag→signal derivation pattern (`config/schema.md`): advisory red flag →
`coverage.indicator` (status covered/partial/gap, exactly one `target:true`) → buildable candidate
(`cover:"gap"` AND `data:"available"`) → target `candidate.definition` {signal_name, class,
features[], logic, window, source, route}. The `anthropic` SDK follows the markitdown precedent
(authoring venv, gitignored, never a ship dep).
