---
title: "Phase 20: Multi-source spine, proven with FinCEN Alerts (M7)"
aliases: ["2026-06-06-phase-20-multi-source-spine"]
category: journal
tags: ["M7", "multi-source", "fincen-alerts", "scale", "registry", "lite"]
parents: ["phase-20-multi-source-spine"]
created: 2026-06-06
updated: 2026-06-06
source: debrief
duration: long
---

# Phase 20: Multi-source spine, proven with FinCEN Alerts (M7)

## What Happened

Scaled the corpus beyond FinCEN *advisories* to a SECOND FinCEN publication type — **Alerts** — via a
thin multi-source registry, the first genuine scale move after the M0–M7 roadmap hit Definition of Done.
The frame was set by a USER REFRAME at the gate ("try FinCEN articles first, other than advisories"):
offered US-federal-public-domain/OFAC vs cross-jurisdiction-paraphrased vs a new showcase typology, the
user chose OTHER FinCEN publication types. Rationale that made it cheap: staying inside the verbatim
public-domain regime means NO non-negotiable change (the "FinCEN-only verbatim" rail is untouched) and the
quote-grounding gate (`check_record`/`rf_region`/`normalize`) is reused UNCHANGED — yet the multi-source
generalization is still exercised by genuinely heterogeneous content. OFAC (also 17 USC §105) is the
documented NEXT-source candidate; cross-jurisdiction sources (FINTRAC/FATF) were rejected because
paraphrase breaks quote-grounding.

The architecture was a MERGE, not a migration. A thin `CORPUS_SOURCES` registry in build.py decouples
source-id from storage dir: `data/fincen/` stays the `fincen-advisories` source BYTE-FROZEN (no renaming
the 14 advisory mds / 12 derived), `data/fincen-alerts/` is source #2. `render_corpus` split into a
per-source `_load_source` (manifest+derived merge, per-source orphan check, graceful missing-derived-dir)
+ a thin iterate-and-merge loop; `doc_type` stamped at merge. T1 landed as a PURE byte-identical refactor.
Acquisition generalized: `crawl_fincen.py` gained `parse_alerts` + `--alerts` (the alerts hub lists each
PDF DIRECTLY → zero-hop, literal-space hrefs %20-encoded); `acquire_fincen.py`/`pdf_to_md.py` gained
`--source <dir>` (a manifest url ending in `.pdf` = direct download); `derive_signals.py` gained
`source_dir` params on `--corpus[-status]`. The T2 convert-one-first CHECKPOINT passed on DeepFakes
(rf_region not None), then ALL 19 alerts were acquired+converted (the full honest corpus). 6 alerts were
derived via the inverted loop — one extraction subagent per alert as the LLM-backend role, each self-gating
to `--check-derived` clean, then INDEPENDENTLY re-checked by the orchestrator (exceeds the ≥4 target;
72 indicators / 19 BUILD_NOW; honest enrichment-heavy distributions kept where the typology warrants, e.g.
Russian-elite high-value-assets 17 ind / 2 BUILD_NOW). corpus.html got a unified menu with honest doc_type
chips (Advisory/Alert), and user-facing "advisory" was neutralized to "document" across the shared
5-screen arc. The review gate refined the non-derivable chip to "no enumerated red-flag list" (an honest
under-claim fix).

## Decisions Made

- Phase 20 = scale via OTHER FinCEN publication TYPES (Alerts first), over other agencies (OFAC) and a new
  showcase typology — user reframe; stays inside the verbatim public-domain regime so NO non-negotiable
  change and the gate is reused unchanged. (Lite — recorded in `_CURRENT_STATE.md`.)
- Thin multi-source `CORPUS_SOURCES` registry decoupling source-id from storage dir; `data/fincen/` stays
  byte-frozen, `data/fincen-alerts/` is source #2 — multi-source via the MERGE, not a migration. Registry
  ready for {advisories, alerts, …OFAC} and no more (not a plugin framework). (Lite.)
- Proof batch derived via the inverted loop with per-alert extraction SUBAGENTS as the LLM-backend role,
  each gate-disposed + independently re-checked. (Lite.)

## Problems Solved

- Multi-source without churn — a registry MERGE keeps the 14 advisory mds + 12 derived byte-identical
  (subtraction test rejected renaming them to fit a scheme); the scheme accommodates the existing dir.
- Alert acquisition is simpler than advisories — the alerts hub lists PDFs directly (zero-hop), vs the
  advisory detail-page resolution; `--source` + the direct-.pdf rule unified both paths.
- The non-derivable chip over-claimed "no red-flag list" for fin-2022-alert001 (has red-flag mentions but
  no anchorable enumerated list) → refined to "no enumerated red-flag list" (review-gate honesty fix).

## Open Questions

- None unresolved.

## Artifacts Changed

- `scripts/build.py` (CORPUS_SOURCES registry; render_corpus → _load_source + iterate-merge; doc_type stamp)
- `scripts/crawl_fincen.py` (parse_alerts + --alerts; parameterized helpers, advisory-identical defaults)
- `scripts/acquire_fincen.py`, `scripts/pdf_to_md.py` (--source, direct-.pdf rule)
- `scripts/derive_signals.py` (source_dir params on --corpus[-status]; the gate UNCHANGED)
- `corpus.html` (doc_type chip + .acleft; unified-menu copy/counts; "advisory"→"document")
- `dist/corpus/index.html` (rebuilt — 33 publications, 18 derived live)
- `data/fincen-alerts/**` (19 alert md + 6 derived + index.json + corpus-status.json; raw/ gitignored)
- `tests/corpus-explorer.test.mjs` (+12 assertions → 40/40), `tests/fixtures/fincen-alerts.html` (new)
- `README.md`, `CLAUDE.md` (multi-source spine, alerts as source #2, OFAC next), `.gitignore`

## Related

- [[phase-20-multi-source-spine|Phase 20: Multi-source spine, proven with FinCEN Alerts]] — parent phase

## Soft Observations / Phase N+1 Candidates

- 11 derivable-but-not-yet-derived alerts (+ any future) are cheap INCREMENTAL follow-on derivation via the
  inverted loop — NOT a phase. | next: a lightweight derivation pass, no new architecture. | evidence: this journal "What Happened" + data/fincen-alerts/corpus-status.json (17 derivable, 6 derived)
- OFAC is the documented NEXT source; adopting it requires extending the verbatim non-negotiable from
  FinCEN-only to US-federal-public-domain (17 USC §105) — a compliance sign-off, flagged not taken. | next: a source-#3 phase gated on the sign-off. | evidence: _CURRENT_STATE decision + CLAUDE.md
- The `_rf_triage` region counts for some alerts are coarse/over-inclusive (e.g. DeepFakes region sized 46)
  — harmless (live render from records; build ignores the manifest count for live ones), but the carried
  "tighten rf_region" item persists. | evidence: T3 task line + the Ph17 carry-over
- fin-2022-alert001 + fin-2025-alert003 mention red flags without an rf_region-anchorable enumerated list →
  honestly labeled non-derivable (an under-claim, not a fabrication); a future rf_region anchor-pattern
  widening could reach them. | evidence: T2 verify note
- The six-act showcase still has no harness equivalent (the corpus explorer's now extends to 40 assertions);
  a future durability pass could extend the same `vm`+shim. | evidence: Ph19 carry-over + tests/

### Retro Check (Phases 16-20)

| Dimension | Findings | Signal |
|-----------|----------|--------|
| 1. Recurring Blockers | 0 | none |
| 2. Decision Reversals | 0 | none |
| 3. User Corrections | 1 (recurring frame) | high |

Dim 1: clean across the M7 arc — no blocked tasks, no escape hatches this phase; the T2 degrade path
(pivot to Financial Trend Analyses) was carried but never needed (DeepFakes checkpoint passed). Dim 2: no
reversals — each phase's thesis held (invert → delete → arc → durability → multi-source); confidence stayed
high. Dim 3 (highest signal, recurring across Ph11/16/17/19/20): the user repeatedly REFRAMES the gate
toward scale/architecture/durability over the carried showcase-debt true-up (elder presentation-values +
fentanyl verbatim re-point). This phase's "try FinCEN articles first, other than advisories" is the same
pattern — Jake allocates attention to the scale/generalization frontier and to honesty (rejecting
fabricated lift, refining the non-derivable chip), and consistently defers the showcase true-up.

Recommendations:
- Stop offering the showcase-debt true-up as a default direction option — it has been declined at 5+ gates.
  Lead with the scale/architecture/honesty frontier the user actually picks (now: incremental alert
  derivation, OFAC source #3 pending sign-off). This is already captured in memory ("Prioritizes scale over
  showcase-polish") — keep honoring it.

### Activation Quality

No `active-knowledge.md` present this session (lite ceremony, no knowledge wiki activation file) — activation
quality not measured.
