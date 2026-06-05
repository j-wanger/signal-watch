---
title: "2026-06-04 · M6 pipeline walking skeleton"
aliases: []
category: journal
tags: [milestone-m6, pipeline, fincen, ingestion, signal-watch, provenance]
parents: [phase-07-pipeline-walking-skeleton]
created: 2026-06-04
updated: 2026-06-04
source: debrief
duration: unknown
---

# 2026-06-04 · M6 pipeline walking skeleton (Phase 7)

Planned + implemented the M6 thin vertical slice in one session: prove the "Signal Watch"
ingestion pipe on ONE real FinCEN advisory end to end — acquire PDF → PDF→markdown → hand-derive
ONE signal → render verbatim in Act 1 — before widening the scraper or automating derivation
(both explicitly later phases). All 5 tasks done.

## What Happened

- **T1 · Acquire.** `scripts/acquire_fincen.py` (stdlib `urllib`, authoring-only, no runtime fetch)
  pulled EFE **FIN-2022-A002** → `data/fincen/raw/fin-2022-a002.pdf` (824,692 bytes, %PDF-1.7).
- **T2 · Convert + de-risk gate.** `scripts/pdf_to_md.py` ran **markitdown** (MIT) →
  `data/fincen/fin-2022-a002.md` (48KB, 793 lines). All 24 enumerated red flags intact and in
  order; minor running-header/page-number artifacts, body kept verbatim. GATE PASSED — no
  converter fallback (pymupdf4llm) needed. Forced detour: this machine's homebrew Python 3.14 has
  a broken `pyexpat` (dlopen symbol mismatch) that takes `pip` down, so the converter runs under a
  **uv-managed Python 3.12 `.venv`** (gitignored); `build.py` stays stdlib on system python.
- **T3 · `advisory_full` first-class + rebrand.** Engine: `ADVISORY_FULL` const +
  `validateConfig()` defensive default + Act 1 `streamAdvisory` branch (bounded scrollable
  `docfull`, `.docsrc` attribution kept VISUALLY DISTINCT from the illustrative badge) + `esc()`
  helper. `build.py`: optional `advisory_full` validation + **`text_file`→inline resolution** so the
  markdown corpus stays the single source of truth (no 47KB duplicated into JSON). Rebrand "Signal
  Engine" → "Signal Watch" at `<title>` + header + JS default; 0 "Signal Engine" left in dist.
- **T4 · Hand-derive EFE config.** `config/typologies/elder-financial-exploitation.json` —
  schema-valid, hand-authored (NOT auto-extracted). Target signal **S-DORMANT-DRAIN-ELDER** traces
  to financial red-flag md line 507 ("Dormant accounts with large balances begin to show constant
  withdrawals") + line 516. Later expanded (user-driven) to map ALL 12 FINANCIAL red flags as
  candidates (11 candidates / 12 indicators); the 12 BEHAVIORAL red flags deliberately EXCLUDED as
  branch-staff observations, not data signals — only the data-observable POA/control-change flag kept.
- **T5 · Build + offline verify.** All 3 dist build clean; self-contained guard 0 tokens on all 3;
  `node --check` on inlined engine PASS (template-literal edit sound); badge vs "public domain ·
  verbatim" attribution distinct; EFE carries 47K verbatim, legacy configs fall back via the default.
  Live `file://` render = human sign-off at the delivery gate.

## Decisions Made

- **Phase 7 = pipeline walking skeleton** — prove the pipe on ONE advisory before widening/automating.
- **Project identity pivot** — "scripted dramatization" → "public-data-seeded ingestion pipeline"
  whose demo output is the existing frontend, designed to later take real data. Provenance upgrades buy-in.
- **FinCEN-only verbatim exception** — verbatim public-domain federal text (17 U.S.C. §105),
  attributed; does NOT extend to FINTRAC (Crown copyright). Doc true-up of the "paraphrased"
  non-negotiable is DEFERRED to its own phase.
- **Rebrand "Signal Engine" → "Signal Watch"** — resolves the M5 open product-name question
  (engine + dist rebranded; docs deferred with the doc true-up).
- **Slice advisory = EFE FIN-2022-A002** — 24 enumerated red flags = cleanest derivation;
  reuse-fentanyl rejected (existing fentanyl demo is FINTRAC-grounded, not FinCEN).
- **Verbatim renders in Act 1's existing SOURCE DOCUMENT panel, not Act 0** — loader reframe reuses
  structure, strengthens the "agent reads the advisory" beat, spares the Act 0 hook.
- **Authoring-time vs ship-artifact split is load-bearing** — scraper/converter/derivation are
  build-time; ship artifact stays single-file, offline, zero runtime deps, no fetch.
- **`advisory_full` via `text_file`→build-time inline** — markdown corpus is the single source of
  truth; no 47KB duplication in JSON.
- **Corpus advisory-named** (`data/fincen/fin-2022-a002.md`); **config typology-named**
  (`elder-financial-exploitation.json`) — separates source-document corpus from derived typologies.
- **Derivation hand-authored, not auto-extracted** — deterministic schema validator at the build boundary.
- **Behavioral red flags excluded** (user-confirmed) — branch-staff observations, not data signals.

## Problems Solved

- Broken homebrew Python 3.14 `pyexpat` (dlopen symbol mismatch) took `pip` down → installed/ran the
  converter under a uv-managed Python 3.12 `.venv` (gitignored, isolated from the zero-dep ship file);
  `build.py` stays stdlib on system python. (DISCOVERY escape hatch.)
- 47KB verbatim text would have duplicated into JSON → `text_file` field resolved+inlined at build time,
  keeping the markdown corpus as the single source of truth.

## Open Questions

- **Doc true-up phase** (REQUIRED follow-up, deferred) — rebrand README/HANDOFF/CLAUDE/smoke-checklist
  to "Signal Watch", and formally amend the "paraphrased" non-negotiable to the FinCEN-verbatim exception.
- **fentanyl.json provenance defect** — `anchor.source` + CLAUDE.md cite FinCEN FIN-2019-A006 /
  FIN-2024-A002, neither verifiable in aml-wiki; the demo is actually FINTRAC-grounded. True-up deferred.
- **Commit hygiene** — whether to gitignore the reproducible 824KB raw PDF (regenerable via
  `acquire_fincen.py`) and commit only the `.md`. Pending (orchestrator decides at commit).
- Nothing committed this session yet.

## Artifacts Changed

- `scripts/acquire_fincen.py` (NEW — stdlib urllib fetch, authoring-only)
- `scripts/pdf_to_md.py` (NEW — markitdown PDF→markdown, authoring-only)
- `scripts/requirements-authoring.txt` (NEW — authoring deps)
- `data/fincen/raw/fin-2022-a002.pdf` (NEW — acquired source PDF, 824KB)
- `data/fincen/fin-2022-a002.md` (NEW — verbatim source of truth, 48KB)
- `config/typologies/elder-financial-exploitation.json` (NEW — hand-derived EFE config)
- `dist/elder-financial-exploitation/index.html` (NEW — built self-contained ship file)
- `index.html` (advisory_full render + highlights + esc() helper; Signal Watch rebrand)
- `config/schema.md` (advisory_full field documented; brand default)
- `scripts/build.py` (advisory_full boundary validation + text_file→inline resolution)
- `dist/{fentanyl,trade-based}/index.html` (rebuilt under Signal Watch rebrand)

## Related

- [[phase-07-pipeline-walking-skeleton|Phase 7: Pipeline walking skeleton (M6)]] — parent phase

## Soft Observations / Phase N+1 Candidates

- **Doc true-up + provenance fix** | "Phase 8 · Doc true-up + provenance fix" — rebrand docs to
  Signal Watch + formally amend the "paraphrased" non-negotiable to the FinCEN-verbatim exception, and
  fix the fentanyl FINTRAC-vs-FinCEN citation in the same pass | evidence: Open Questions above.
- **Widen the scraper to all FinCEN advisories** | "Phase · FinCEN corpus crawler" — the original
  vision's next increment | evidence: this slice proved the pipe on ONE item.
- **Automate article→signal derivation** but keep the deterministic validator boundary — this session
  proved the manual path first | evidence: T4 hand-authored derivation.
- **Behavioral-vs-data-signal boundary** could become a demo feature later (deferred by user this session).

### Retro Check (Phases 1-6, 5 completed)

| Dimension | Findings | Signal |
|-----------|----------|--------|
| 1. Recurring Blockers | 0 (no blocked tasks; the M6 homebrew py3.14 `pyexpat` defect was a one-phase env issue, worked around via uv venv — not recurring) | none |
| 2. Decision Reversals | 0 (M4 skipped by deliberate decision, not reversed; the M5-deferred rename was actioned in M6, not reversed) | low |
| 3. User Corrections | M6 USER OVERRIDE post-task refinements (restore streaming, extend typed span, restore highlights, expand derivation to all financial red flags) + a user-confirmed behavioral-flag exclusion — scope refinements within an accepted direction, concentrated in one phase | low |

Recommendations:
- No systemic issues across the 5 completed phases. The single env blocker (py3.14 pyexpat) is machine-specific, not process — the uv-venv isolation is the durable fix. Continue the established pattern: confirm direction up front, then iterate against the delivery gate.
