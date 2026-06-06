---
title: "Phase 14: Scale corpus derivation (3 more CLEAN advisories → 5/14 live)"
aliases: [scale-derivation, corpus-derivation-scale, fuller-live-menu]
category: phases
tags: [milestone-m7, corpus, llm-backend-derivation, authoring, build-recommendation]
parents: []
created: 2026-06-05
updated: 2026-06-05
source: plan
status: completed
ceremony: lite
scope: ["data/fincen/derived/fin-2020-a008.json", "data/fincen/derived/fin-2025-a003.json", "data/fincen/derived/fin-2025-a002.json", "dist/corpus/index.html", "README.md", "CLAUDE.md"]
entry_criteria: "Phase 13 complete + accepted: the corpus explorer (dist/corpus/index.html via corpus.html) ships, rendering the staged 4-screen flow off the merged corpus-status.json + derived/*.json. The derivation loop (--scaffold-derived → author → --check-derived) and the build/render path (build.py corpus) are proven on 2 records. The explorer shows all 14 with honest status but only 2 are derived/live — a stakeholder clicking around hits 'not yet derived' 12 of 14 times. User wants a fuller live menu."
exit_criteria: "(1) 3 new data/fincen/derived/{fin-2020-a008,fin-2025-a003,fin-2025-a002}.json records (or a COVID-EIP swap if Iran extracts unfaithfully), each --check-derived-clean (matrix-consistent + every indicator traceable to a red-flag md line + BUILD_NOW⇒full build_logic), with ≥1 BUILD_NOW carrying a full definition, residual extraction noise pruned, provenance marking them LLM-backend-derived (this session, no key) + checked (NOT ship configs). (2) dist/corpus/index.html rebuilt showing 5/14 live, each new advisory rendering coverage gauge → build-rec matrix (BUILD_NOW-first) → ≥1 signal-spec card through all 4 screens. (3) git diff index.html corpus.html empty; config/** + the 3 typology dists byte-untouched; build.py --check all zero drift. (4) README + CLAUDE reflect 5/14 derived live (was 2/14)."
---

# Phase 14: Scale corpus derivation (3 more CLEAN advisories → 5/14 live)

## Objective

Make the M7 corpus explorer persuasive as a pitch artifact by filling its live menu. Phase 13 shipped the
explorer with only 2 of 14 advisories derived/live; the demo's biggest weakness is that a stakeholder
clicking around hits "not yet derived" 12 times. Derive 3 more CLEAN advisories so the live menu goes
2/14 → 5/14, with a strong topical spread.

## Approach

**Pure authoring, no engineering.** The spine tools (`--scaffold-derived`, `--check-derived`, the cover×data
matrix `build_rec_category`) and the front-end (`corpus.html`, `build.py corpus`) already exist from Phases
12–13. build.py makes an advisory "live" in the explorer simply by the presence of
`data/fincen/derived/<id>.json` — it merges corpus-status.json + derived/*.json by id. So deriving 3 more
records + rebuilding is the whole mechanism — **zero changes** to `index.html`, `corpus.html`, `config/**`,
`scripts/**`, or the 3 typology dists. Lowest-risk possible phase against the byte-frozen showcase.

Per advisory, the proven loop (Phase 12):
1. `python3 scripts/derive_signals.py --scaffold-derived <id> data/fincen/<id>.md` → skeleton (indicators
   from `extract_red_flags`, src_line-traceable, empty judgment).
2. Author each indicator's judgment: `status` (covered/partial/gap) + `data` (available/partial/insufficient)
   → `build_rec` via the cover×data matrix + free-text `rationale`; `build_logic` (signal_name, class,
   features[], logic, window, source, route) for every BUILD_NOW gap.
3. **Prune residual extraction noise** — even CLEAN extractions can carry intro-tail / header / citation
   artifacts; every shipped indicator must be a real advisory red flag.
4. `python3 scripts/derive_signals.py --check-derived data/fincen/derived/<id>.json` DISPOSES (build-rec
   matrix-consistent + traceability + BUILD_NOW⇒full definition).

**Picks (strong topical spread → corruption · fentanyl-precursors · trafficking · CMLN · Iran-sanctions):**
- `fin-2020-a008` human trafficking (11 flags) — iconic, recognizable AML typology.
- `fin-2025-a003` Chinese money-laundering networks (17) — current top FinCEN priority, distinct.
- `fin-2025-a002` Iran illicit finance (16) — current, sanctions/proliferation angle.

**Deliberately out:** EFE (`fin-2022-a002`, 24) — already the full showcase elder typology; a duplicate
corpus record adds little for 24 indicators of effort (stays honest as CLEAN-not-derived). COVID EIP
(`fin-2021-a002`, 7) — cheap but dated for a 2026 pitch; documented stretch/follow-up (and the T3 swap
target if Iran extracts unfaithfully).

The LLM backend is THIS session (no API key, no `--draft`) — the same boundary as Phase 12: the LLM proposes
status/data/build_rec/rationale/build_logic; the deterministic `--check-derived` disposes.

## Scope

Files affected (all NEW data + rebuild + docs — no engine/spine/front-end edits):
- `data/fincen/derived/fin-2020-a008.json` (NEW) — human trafficking record.
- `data/fincen/derived/fin-2025-a003.json` (NEW) — Chinese MLN record.
- `data/fincen/derived/fin-2025-a002.json` (NEW) — Iran record (or `fin-2021-a002.json` on T3 swap).
- `dist/corpus/index.html` — rebuilt (commit-dist convention).
- `README.md`, `CLAUDE.md` — bump corpus live-count 2/14 → 5/14.

UNTOUCHED (byte-frozen): `index.html`, `corpus.html`, `config/**`, `scripts/**` (the spine tools already
exist), `dist/{fentanyl,trade-based,elder-financial-exploitation}/`. `data/fincen/corpus-status.json` is
regenerated as a no-op safety check (status/derivable don't change on derivation).

## Exit Criteria

- [x] 3 new `data/fincen/derived/{fin-2020-a008,fin-2025-a003,fin-2025-a002}.json` records (no swap needed), each `--check-derived`-clean with ≥1 BUILD_NOW carrying full build_logic, residual noise pruned, provenance set (LLM-backend-derived + checked, NOT a ship config).
- [x] `dist/corpus/index.html` rebuilt showing 5/14 live; each new advisory renders coverage gauge → build-rec matrix (BUILD_NOW-first, src_line-traceable) → ≥1 signal-spec card through all 4 screens.
- [x] `build.py corpus` / `--check corpus` work; `build.py --check all` zero drift.
- [x] `git diff index.html corpus.html` empty; `config/**` + the 3 typology dists byte-untouched.
- [x] README + CLAUDE reflect 5/14 derived live (was 2/14), naming the 3 new advisories.

## Constraints (load-bearing)

- **Pure authoring — no engine/spine/front-end edits.** corpus.html, index.html, config/**, scripts/** stay byte-untouched; the phase touches only new derived/*.json + a dist rebuild + docs.
- **Honest, traceable, demo-quality data only.** Every indicator is a real advisory red flag (prune extraction artifacts); every src_line traces to a flagged md line (`--check-derived` enforces); build_rec follows the cover×data matrix; no fabricated lift/stats; coverage/data values are ILLUSTRATIVE (the always-on badge stays).
- **LLM-backend boundary preserved (Phase 11/12 principle).** The model session proposes the judgment; the deterministic `--check-derived` disposes. Records carry provenance marking them LLM-backend-derived + checked — NOT ship typology configs (the 3 hand-curated typologies stay the showcase).

## Checkpoints

- T3: spot-check the Iran scaffold against the md BEFORE authoring (its extraction was not spot-verified in Phase 12). If faithful, proceed; if too noisy/unfaithful, SWAP to COVID EIP (fin-2021-a002) and note the deviation.
- T4: after rebuild, confirm `git diff index.html corpus.html` is empty and `--check all` is zero-drift before declaring the explorer updated.
- Abort: if ≥2 of the 3 chosen advisories extract too noisily/unfaithfully to author a demo-quality traceable record, narrow to fewer (quality over count) and raise an extractor-improvement (glued-list splitting) Phase-15 item rather than shipping filler. Blocked >3 attempts on a task → ask the user: skip or abort.

## Assumptions

- The 3 chosen CLEAN advisories extract faithfully enough that the scaffold needs only judgment + light pruning (T0 weakest assumption — validated per-task against the md; Iran first). fin-2020-a008 + fin-2025-a003 flags were spot-verified genuine in Phase 12; Iran was not, hence the T3 validate-first gate + swap path.
- The derived-record shape (per-indicator status/data/build_rec/rationale + build_logic on BUILD_NOW) and the build/render path are stable (proven on 2 records in Phases 12–13); adding records of the same shape needs no front-end change.

## Notes

Direction approved by user 2026-06-05: **scale derivation** (fuller live menu) over the genuine alternatives
— spine robustness (glued-list splitting + FATF labeling), a corpus combination-lift wow beat, or showcase
debt true-up (elder values / fentanyl re-point). User confirmed 3 advisories (human trafficking, Chinese MLN,
Iran), EFE + COVID out. The bar set at the direction gate: each new record must be **demo-quality, not
filler** (breadth was chosen over the depth/wow-beat alternative). Follow-ups not in scope (Phase 15
candidates): the remaining CLEAN advisories (EFE corpus record, COVID EIP); glued-list splitting in
`extract_red_flags` for the 2 NEEDS advisories (fin-2021-a004, fin-2026-a001); explicit FATF non-derivable
labeling; the corpus combination-lift wow beat; (carried) elder presentation-values true-up · fentanyl
verbatim re-point · manifest `--fetch` cadence.
