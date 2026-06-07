---
title: "Phase 21: OFAC as corpus source #3 (gate widened for OFAC vocab; US-federal public-domain) (M7)"
aliases: ["2026-06-06-phase-21-ofac-corpus-source"]
category: journal
tags: ["M7", "ofac", "multi-source", "corpus", "non-negotiable", "gate", "regression-gated", "lite"]
parents: ["phase-21-ofac-corpus-source"]
created: 2026-06-06
updated: 2026-06-06
source: debrief
duration: long
---

# Phase 21: OFAC as corpus source #3 (gate widened for OFAC vocab; US-federal public-domain) (M7)

## What Happened

Added OFAC (US Treasury, Office of Foreign Assets Control) as the THIRD corpus source — the demo's first
move beyond a single agency — and, decisively, did it WITH a regression-gated widening of the rf_region
anchors. The planning probe was the turning point and reframed the ask: OFAC does NOT use FinCEN's
red-flag template. The Sham Transactions advisory uses "red flags" (anchors UNCHANGED), but maritime uses
"Deceptive Practices", VC guidance uses "Risk Indicators", and the ransomware advisory defers its red
flags to a co-issued FinCEN advisory. So OFAC needed MORE than the compliance sign-off the user had
authorized at the Phase-20 gate — it needed a change to the previously-byte-frozen correctness gate.
Surfaced that honestly at the direction gate; the user chose to **widen the gate** (over a
small-clean-source = red-flag-template OFAC only / no gate change, or holding OFAC).

T1 (the L task) widened the rf_region anchors for OFAC vocab — `_RF_HEADER_OFAC` (standalone "<cat> Risk
Indicators / Deceptive [Shipping] Practices / Risk Factors" heading; trailing `:?$` excludes TOC
dotted-leader lines) + `_RF_INTRO_OFAC` ("risk indicators … may be/include"), mirroring the FinCEN
anchors; rf_region's anchor check ORs them in. The `corpus_status_records` issuer was parameterized
per-source (OFAC iff "ofac" in dir name, else FinCEN) with a doubling-guard so FinCEN output stays
BYTE-IDENTICAL. **The grounding core (`normalize`/`check_record`) is byte-UNTOUCHED — only the rf_region
relevance anchors widened.** The widening was REGRESSION-GATED and held perfectly: a baseline of all 33
FinCEN mds' rf_region captured pre-change → 0 shifted post-change; all 29 FinCEN records still
`--check-derived` clean; `--selftest` passes with 3 new bidirectional OFAC-anchor fixtures.

OFAC acquisition is HAND-CURATED (OFAC's site is a JS SPA with no static crawlable listing):
`data/ofac/index.json` is hand-authored from `/media/<id>/download` PDFs; `acquire_fincen.py`/`pdf_to_md.py`
reused via `--source` + a `_to_pdf_url` tweak (an absolute `/media/.../download` or `/system/files/` URL =
direct download); `crawl_fincen.py` stays FinCEN-only. The honest yield is 3 OFAC docs (sham-transactions,
maritime, virtual-currency), NOT the plan's optimistic ≥4 — OFAC's cleanly-anchoring advisory set is
genuinely small (the art advisory media/49091 + 2 more candidates 932436/932391 were probed and do NOT
anchor: defer-to-FinCEN / sanctions-compliance-framework, not the red-flag template) → honestly skipped,
not forced. 3 records were derived via the inverted loop (19 indicators / 4 BUILD_NOW); OFAC content is
sanctions/vessel-oriented, so the maritime record is honestly SOURCE_DATA-heavy (4 of 7 are vessel-behavior
the FI can't observe → SOURCE_DATA, never a fabricated signal). build.py registered ofac-advisories as
source #3; corpus.html got a 3-type menu; the harness grew 40→49. The compliance non-negotiable was
extended FinCEN-only → US-federal (17 USC §105) in BOTH CLAUDE.md and HANDOFF.md, stated identically.

## Decisions Made

- Phase 21 = OFAC as corpus source #3 WITH a regression-gated rf_region anchor widening — user chose "widen
  the gate" over a small-clean-source / holding OFAC; the probe reframed the ask (OFAC doesn't use the
  red-flag template → needed a gate change, not just the compliance sign-off). (Lite — `_CURRENT_STATE.md`.)
- Compliance: extend the verbatim public-domain non-negotiable FinCEN-only → US-federal (17 USC §105 —
  works of the US government; FinCEN + OFAC + other US federal agencies), STILL excluding FINTRAC (Canadian
  Crown copyright) + any non-US/non-government source. Updated identically in CLAUDE.md + HANDOFF.md. (Lite.)
- OFAC acquisition is HAND-CURATED (OFAC's SPA has no static crawl); acquire/pdf_to_md reused via --source +
  a `_to_pdf_url` direct-download tweak; the issuer parameterized; crawl_fincen.py stays FinCEN-only. (Lite.)

## Problems Solved

- OFAC vocab vs the byte-frozen gate — OFAC uses Risk Indicators/Deceptive Practices/Risk Factors, not "red
  flags", and `check_record` treats `rf_region==None` as a HARD violation. Solved by ADDING OFAC heading
  anchors (the grounding core untouched), regression-gated to 0 FinCEN rf_region shift + 29 records clean.
- Widening without contaminating the core — the change is confined to the rf_region RELEVANCE anchors;
  `normalize`/`check_record` (the grounding/traceability authority) stayed byte-identical, so the
  subtraction-style discipline held (complexity didn't leak into the correctness path).
- Honest 3-not-4 yield — OFAC's cleanly-anchoring set is small; rather than force the optimistic ≥4, the
  non-anchoring candidates were probed and honestly skipped (the phase-exit ≥3 is met).
- Reviewer-caught comment inaccuracy — the `_RF_HEADER_OFAC` comment overstated inertness ("0 mds use
  'deceptive practices'"); 4 FinCEN/alert mds actually contain "deceptive shipping practices" in PROSE (the
  T1 grep's literal "deceptive practic" missed the "shipping" infix). The invariant still holds (all
  mid-prose, never headers → 0 rf_region shift) but the comment was wrong → reworded to "appears only
  mid-prose, never as a heading/lead-in"; re-verified 0 shifts + --selftest + --check all + harness 49/49.

## Open Questions

- None unresolved.

## Artifacts Changed

- `scripts/derive_signals.py` (rf_region anchors WIDENED: `_RF_HEADER_OFAC` + `_RF_INTRO_OFAC`, ORed into
  the anchor check; `corpus_status_records` issuer parameterized per-source with a doubling-guard so FinCEN
  output is byte-identical; 3 new bidirectional OFAC `--selftest` fixtures; a corrected anchor comment. The
  grounding core `normalize`/`check_record` is byte-untouched — but this IS a change to the previously
  byte-frozen correctness GATE, regression-gated to 0 FinCEN rf_region shift)
- `scripts/acquire_fincen.py` (`_to_pdf_url`: an absolute `/media/.../download` or `/system/files/` URL is a
  direct download — the OFAC URL form; FinCEN behavior unchanged)
- `scripts/build.py` (CORPUS_SOURCES gained `ofac-advisories` source #3, doc_type "OFAC")
- `data/ofac/**` (NEW source #3: 3 md + 3 derived + index.json + corpus-status.json; raw/ gitignored)
- `corpus.html` (3-type menu — advN/alertN/ofacN by doc_type; eyebrow "FinCEN + OFAC corpus"; lead = public
  US-federal corpus, 17 §105; count line names FinCEN advisories · FinCEN alerts · OFAC)
- `dist/corpus/index.html` (rebuilt — 36 publications: 14 Advisory + 19 Alert + 3 OFAC; 32 derived/live)
- `tests/corpus-explorer.test.mjs` (40→49: 3-type doc_type-chip count, ≥1 OFAC live, an OFAC-advisory
  full-arc walk)
- `CLAUDE.md`, `HANDOFF.md` (the verbatim non-negotiable extended FinCEN-only → US-federal, FINTRAC
  excluded — a structural change to a load-bearing project rail, stated identically in both)
- `README.md`, `CLAUDE.md` (OFAC source #3 + the rf_region widening + hand-curated acquisition; counts →
  32 derived across 36 publications)
- `.gitignore` (`data/ofac/raw/`)

## Related

- [[phase-21-ofac-corpus-source|Phase 21: OFAC as corpus source #3]] — parent phase
- [[2026-06-06-phase-20-multi-source-spine|Phase 20: Multi-source spine]] — the registry source #3 reuses

## Soft Observations / Phase N+1 Candidates

- OFAC's running header "OFAC SANCTIONS ADVISORY - <date>" (variable date, unlike the FIXED FINCEN header)
  glues into page-break flags; `normalize()` doesn't strip it → handled per-flag via the established
  contiguous-span convention. | next: add OFAC-header handling to `normalize`/`_clean` IF OFAC scales (not
  needed at 3 docs). | evidence: T3 task line + this journal.
- OFAC's cleanly-anchoring advisory set is genuinely SMALL (3). Further OFAC scale needs either more
  anchor-widening (each addition = correctness-core regression surface) or accepting the small set. The
  cross-agency proof is MADE; pushing OFAC bigger has diminishing returns + rising core risk. | next: only
  scale OFAC if a stakeholder asks for it specifically. | evidence: T2 verify note (probed non-anchoring
  candidates).
- The maritime record is honestly SOURCE_DATA-heavy (vessel behavior non-FI-observable) — an honest demo
  insight (sanctions/vessel red flags need external data unlike transaction red flags), but OFAC adds fewer
  buildable signals than FinCEN. | evidence: T3 (maritime 4 of 7 → SOURCE_DATA).
- A cleaner next-scale source within the NO-gate-change regime would be FinCEN Financial Trend Analyses
  (FinCEN template) if more scale is wanted without further correctness-core risk. | next: a no-gate-change
  scale phase if scale is wanted. | evidence: this journal soft-obs + the Ph20 OFAC-next note.

### Activation Quality

No `active-knowledge.md` present this session (lite ceremony, no knowledge-wiki activation file) —
activation quality not measured.
