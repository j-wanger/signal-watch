# Active Phase Context

Phase: 15 - Harden extraction faithfulness + fix shipped defects — M7 — DELIVERED, awaiting commit verification.
(all 5 tasks [x], exit criteria MET, 2026-06-05). No next phase planned — run /dev-plan for Phase 16.
Objective: fix the 2 concrete defects Phase 14 surfaced, scoped by MEASUREMENT — a CLEAN advisory's silent miss (fin-2025-a003 L499) + the fin-2022-a001 esc() double-escape.

Delivered (verified in tree): footnote-resume fix in extract_red_flags (split stop logic — _SECTION_STOP terminals always break + a NEW conditional _FOOTNOTE_STOP:
a mid-list page-boundary footnote run is transient when another red-flag section follows [next_boundary set] → skip + resume to the next anchor; terminal for a last
section → break) + 2 targeted _CITATION signatures (federal case-docket + no-day "(Mon YYYY)" paren-date) to kill 2 footnote-tail leaks. SURGICAL: fin-2025-a003
recovered its silently-dropped L499 escrow flag (17→18), 0 collateral — all 13 other advisories BYTE-IDENTICAL, EFE 12+12, summary 7C/3L/4N. esc() entity sweep
(html.unescape over fin-2022-a001 + fin-2024-a002 `&gt;=`/`&lt;=` → raw text, verified end-to-end in the built file: data holds raw ">= 2", old "&gt;=" gone). Escrow
IND-18 added to fin-2025-a003 (18 ind, --check-derived clean). Manifest regen (a003 17→18) + dist/corpus rebuilt + --check all 4-artifact ZERO DRIFT.
BYTE-FROZEN: index.html, corpus.html, config/**, dist/{fentanyl,trade-based,elder-financial-exploitation}/ (git diff empty). --selftest 12+12.

Deferred (investigated, re-confirmed Phase-12): glued-no-separator splitting (fin-2021-a004 ransomware, fin-2026-a001 health-care) — markitdown dropped bullets AND
blank lines; no safe deterministic split. Stays FLAGGED; needs a structure-preserving converter (pymupdf4llm, authoring-only), not a post-hoc splitter. ISIS
fin-2025-a001 stays LOW (single-section, footnotes terminal) — correctly flagged, not a regression.

Phase-16 candidates: scale live menu to 6–7/14 (remaining CLEAN: EFE corpus record, COVID-EIP fin-2021-a002 — derivable now, same Phase-14 loop) · structure-preserving
converter for the glued advisories · FATF non-derivable labeling · corpus combination-lift wow beat · (carried) elder true-up · fentanyl re-point · --fetch cadence.

Gates:
- [x] Direction confirmed by user (harden spine + fix defects; footnote-resume + esc() sweep; glued-splitting deferred — 2026-06-05)
- [ ] Delivery accepted (post-implementation report)
