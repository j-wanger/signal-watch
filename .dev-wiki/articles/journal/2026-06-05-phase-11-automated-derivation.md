---
title: "Phase 11: Automated derivation (LLM-drafted signal config)"
aliases: []
category: journal
tags: [milestone-m6, authoring-pipeline, automation, llm, anthropic, derivation]
parents: [phase-11-automated-derivation]
created: 2026-06-05
updated: 2026-06-05
source: debrief
duration: ~60min
---

# Phase 11: Automated derivation (LLM-drafted signal config)

Automated the article→signal derivation step proven MANUALLY in Phase 7 (EFE md → hand-derived elder
config). One new authoring-only `scripts/derive_signals.py`, two layers sharing one deterministic
boundary: a DETERMINISTIC layer (stdlib, offline) that extracts the FinCEN red flags + scaffolds a
schema-shaped config SKELETON, and a NEURAL layer (`--draft`, env-keyed) that PROPOSES the judgment
fields via the Anthropic API. The LLM proposes a `.draft.json`; build.py + schema + the two human
gates DISPOSE — no neural judge at the build boundary, committed configs stay deterministic +
human-reviewed. Authoring-only; engine/ship artifact untouched (`git diff index.html` empty),
`dist/` zero-drift. Lite ceremony, all 5 tasks complete. The AUTOMATE override (variant B) honored
without abandoning the standing Phase-9 deterministic-validators-at-boundaries principle. READY FOR
COMPLETION.

## What Happened

- **T1 — pure `extract_red_flags(md)` + `--selftest` (M).** Anchor + blank-line-block parser: locates
  the "Behavioral red flags … may include" / "Financial red flags … may include" intros, spans each
  section to the next header/footnote, groups blank-separated blocks while stripping page-number +
  "FINCEN ADVISORY" running-header artifacts. Returns `[{section, n, text, line}]` (md-line
  traceability). Pinned counts: behavioral=12 + financial=12 = the 24 known EFE flags; `--selftest`
  exit 0 offline. DISCOVERY: markitdown injects form-feed page breaks → `splitlines()` split on them
  and drifted line numbers ~13 lines vs the `\n`-based editor view; switched to `split("\n")` +
  form-feed strip so `line` traces correctly (financial #1 "Dormant accounts" → L507, matching the
  elder IND-02 source). Stdlib-only; absent from engine/build.
- **T2 — pure `scaffold_config()` + `--scaffold` write (M).** 12 financial flags → IND-01..12 + C1..12;
  neutral status/cover/data defaults, `sub` = `"src: FIN-2022-A002 financial red flag #N · md L<line>"`,
  `advisory_full.text_file` wired, anchor/lift/stats as explicit TODO placeholders, canonical 7-act
  chrome templated; 0/0 targets (build-INVALID by construction). `--scaffold` writes a `.draft.json`.
  DISCOVERY: build.py `resolve_targets("all")` globs `*.json` + uses `Path.stem`, so a lingering
  `<id>.draft.json` would build as a bogus id → gitignored `config/typologies/*.draft.json` (transient
  scratch, Phase-10 batch-artifact precedent) + a "remove before build.py all" warning. build.py
  untouched. BOUNDARY confirmed: `build.py <id>.draft` DIES naming exactly the 2 judgment gaps.
- **T3 — LLM `draft_judgment(...)` + `--draft` mode (L).** Neural layer: lazy-imports `anthropic` +
  reads `ANTHROPIC_API_KEY` from env, calls `claude-opus-4-8` with `output_config.format` json_schema
  (per the claude-api reference — model id + structured-output shape CONSULTED, not guessed), grounded
  on the extracted financial red flags + the schema definition contract + fentanyl/elder configs as
  few-shot. `_apply_judgment` writes the proposed status/targets/definition onto the skeleton, with a
  deterministic guard FORCING the chosen candidate target to `cover:gap`+`data:available`. `anthropic`
  added to `requirements-authoring.txt` (gitignored authoring venv, 0.105.2). Env-guards: key unset →
  clean exit-1; stdlib python (no SDK) → clean exit-1; deterministic `--selftest` stays SDK-free.
- **T4 — end-to-end proof + boundary check (S).** BOTH boundary directions proven KEY-FREE: (b) the
  bare skeleton → build.py REJECTS naming the 2 missing judgment fields; (a) a substituted judgment →
  `_apply_judgment` → 1 indicator + 1 buildable candidate target + signal definition → build.py
  ACCEPTS. Recorded `--draft`-shaped run (no API key — Opus 4.8 stood in as the model backend, faithful
  since `--draft` calls the same family): target IND-01/C1 (dormant-reactivation-drain), signal
  `S-DORMANT-REACTIVATION-DRAIN`, coverage spread covered:3/partial:4/gap:5. Scratch cleaned
  (gitignored). `git diff index.html` clean; `build.py --check all` zero drift.
- **T5 — docs (S).** Module docstring + Usage block (two-layer model, env-key, propose/dispose
  boundary, anthropic-in-authoring-venv-not-ship). README authoring section extended with
  `--selftest`/`--scaffold`/`--draft`; CLAUDE M6 pipeline chain extended
  crawl→acquire→pdf_to_md→**derive_signals**→hand-review. No AGENTS.md in repo → CLAUDE.md edited
  directly (Phase 8/M6 precedent).

## Decisions Made

(Captured in `_CURRENT_STATE` ## Recent Decisions at plan time — lite ceremony writes no decision
articles.) Direction = **AUTOMATE over the elder true-up AND the fentanyl re-point** (user override of
the planner's finish-first rec); within AUTOMATE, **variant B (LLM-drafted definition NOW) over A**
(deterministic scaffolder only — A is the documented fallback); **boundary-preservation design**
reconciles the override with the Phase-9 anti-neural-judge principle (LLM proposes, build.py + schema +
2 human gates dispose); **two-layer split in one tool** (deterministic stdlib + neural lazy-anthropic
in the authoring venv); **T3 consults the claude-api reference** for the model id + SDK +
structured-output rather than guessing.

## Problems Solved

- **Form-feed line drift.** markitdown's page-break form-feeds made `splitlines()` miscount source
  lines (~13-line drift), breaking the md-line traceability that anchors the derivation to the verbatim
  advisory. Fixed by `split("\n")` + form-feed strip — confirmed: "Dormant accounts" reports L507.
- **Draft scratch leaking into the build glob.** build.py globs `config/typologies/*.json`; a draft
  with a `.json` suffix would be picked up as a bogus typology. Solved by `*.draft.json` (gitignored)
  + an explicit remove-before-build warning.
- **Honoring AUTOMATE without regressing the deterministic boundary.** The neural layer only PROPOSES;
  the deterministic `_apply_judgment` guard + build.py + schema + human gates remain dispositive — the
  validator disposes of what the model proposes.

## Artifacts Changed

- `scripts/derive_signals.py` (NEW — deterministic `extract_red_flags`/`scaffold_config` +
  `--selftest`/`--scaffold`/`--list`; neural `draft_judgment`/`_apply_judgment`/`--draft`)
- `scripts/requirements-authoring.txt` (+`anthropic` — authoring venv only, never a ship dep)
- `.gitignore` (+`config/typologies/*.draft.json` — scratch skeletons, never committed)
- `README.md` (authoring section: two-layer model + propose/dispose boundary + Status),
  `CLAUDE.md` ("Current state" M6 pipeline chain + the LLM-draft boundary + env-key caveat)

## Related

- [[phase-11-automated-derivation|Phase 11: Automated derivation]] — parent phase
- [[phase-07-pipeline-walking-skeleton|Phase 7]] — the manual EFE article→signal step this automates
- [[phase-09-build-drift-guard|Phase 9]] — the deterministic-validator-at-boundary principle preserved here

## Health Delta

No automated test framework (demo project). New verification capability = `derive_signals.py
--selftest` (runnable stdlib parser check, exit-coded, offline). Authoring deps +`anthropic` (in the
gitignored uv `.venv`, `--draft` only, LAZY-imported — deterministic layer stays stdlib). Engine
untouched (`git diff index.html` empty); `build.py --check all` zero drift on all 3 dist; deterministic
`--selftest` PASS (24 flags, 12+12). The live Anthropic network call remains unexercised (no key in
env) — recorded-manual-run pattern, like Phase-7 convert / Phase-10 batch.

### Review Gate

Size-gated reviewer dispatched (5 completed tasks ≥ 4). **Score 9/10, Verdict: accept.** Highest-value
check (the one surface static verification couldn't reach — the never-exercised live `--draft` call)
VERIFIED CORRECT against the claude-api reference, not guessed: `model="claude-opus-4-8"` valid;
`output_config={"format":{"type":"json_schema","schema":…}}` is the correct current SDK shape
(deprecated `output_format` correctly avoided; `_DRAFT_SCHEMA` stays inside the supported keyword
subset — enums + nested objects + `additionalProperties:false` + `required`, no numeric/length
constraints); text-block extraction + `json.loads` is the documented pattern. Boundary, lazy import,
env-key, no `sk-ant`, zero engine/build drift all re-confirmed. Two **MEDIUM** findings, both
robustness/quality on the unexercised `--draft` path, neither a correctness defect: (1) `:430` —
`thinking`/`effort` omitted; for a reasoning-shaped judgment task the reference recommends
`thinking={"type":"adaptive"}` + `output_config={"effort":"high", …}`; (2) `:434-437` — degrades
poorly on `stop_reason=="refusal"` (misleading "no text block") or `=="max_tokens"` (uncaught
`JSONDecodeError`); harden with a `stop_reason` check + `try/except` around `json.loads`. Disposition
surfaced to the user at the delivery gate (fold-in vs defer).

### Gate Compliance

`<!-- gate-log:phase-11 direction=approved delivery=… -->`. Direction gate approved 2026-06-05 (present,
required). Delivery gate set to `accepted` only after the commit verifiably lands (D3 — gate-state
follows git-state).

## Soft Observations / Phase N+1 Candidates

- **`--draft` live-path hardening (from the review gate):** the two MEDIUMs — `thinking={"type":"adaptive"}`
  + `output_config.effort:"high"` for the judgment task, and graceful `stop_reason` (refusal/max_tokens)
  handling around `json.loads`. Cheap, surgical, on exactly the surface no test exercises. Evidence:
  `scripts/derive_signals.py:430`, `:434-437`.
- **Use `--draft` to derive a NEW typology end-to-end (with a real key).** The pipe is proven key-free;
  the manifest carries 14 advisories. The natural next increment is to actually run the full
  acquire→convert→derive→review→build chain on a fresh FinCEN advisory and ship the derived typology.
- **Elder presentation-values true-up (carried from Phase 9, deprioritized at the Phase-11 gate):**
  still open — smoke-checklist per-typology table (≈L15) + compliance attribution (≈L62) cover only
  fentanyl + trade-based; `elder-financial-exploitation` has no walk-row. Doc-slice.
- **Re-point fentanyl to `fin-2024-a002` (Supplemental Fentanyl Advisory, now manifest-discoverable):**
  a verbatim upgrade for the currently FINTRAC-grounded fentanyl typology. Deprioritized, not dropped.
- **Manifest `--fetch` refresh cadence (carried from Phase 10):** the committed manifest is a
  point-in-time snapshot; a periodic `--fetch`+`--write`+`--selftest` keeps it current. Optional.

## Activation Quality

No `active-knowledge.md` (lite phase, none generated) — step skipped.
