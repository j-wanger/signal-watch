# Active Phase Context

Phase: 16 - Invert extraction (LLM extracts, deterministic groundedness gate disposes) + scale to 7/14 — M7 — DELIVERED + ACCEPTED (all 5 tasks [x], exit criteria MET, reviewer ACCEPT 9/10; impl commit bca3612, 2026-06-06). No next phase planned — run /dev-plan for Phase 17.
Objective: subtraction test on the extraction spine — relocate complexity from brittle section-PARSING (open) to md NORMALIZATION (closed). The LLM extracts
candidate red flags; the deterministic layer became a GROUNDEDNESS GATE (`normalize(flag) ⊂ normalize(md)`, replacing src_line∈extractor-output as the
traceability authority) + a coarse `rf_region()` section-cite relevance guard. Then scale as PROOF: 2 new records incl. ≥1 previously-unreachable advisory → corpus 5/14 → 7/14.

Delivered (verified in tree): T1 ONE `normalize()` rule absorbs the whole closed FinCEN-md artifact set (the escrow STRESS case fin-2025-a003 L499 grounds without
special-casing); `check_record` rewired to grounding + `rf_region()` + a `_MIN_FLAG_NCHARS=24` floor — correctness complexity SHRANK. T2 all 5 committed records migrated
NEAR-FREE (gate-pass unedited). T3 `extract_red_flags` DEMOTED to the EFE selftest-anchor + triage hint; `--corpus-status` SHAPE preserved, `derivable` rebased on
`rf_region(md) is not None` (false only for the 2 FATF advisories; the 2 glued advisories flip false→true). T4 THE PROOF — ransomware fin-2021-a004 (0 deterministic flags,
glued-no-separator, previously unreachable) → LLM extracted all 12, every one grounds verbatim, NO converter/splitter (Phase-15 glued-deferral DISSOLVED); COVID-EIP
fin-2021-a002 → 3 ind → corpus 5/14 → 7/14 live. T5 dist/corpus rebuilt (~95K→~110K B), `--check all` 4-artifact ZERO DRIFT, README + CLAUDE document the inverted
architecture + honesty shift. 2 MEDIUM reviewer findings fixed inline (length floor + 2 regression-pin selftest cases). `--selftest` EFE 12+12. index.html/corpus.html/config/** + 3 typology dists BYTE-FROZEN.

Deferred (Phase-17 candidates): DELETE `extract_red_flags` outright (re-home the EFE selftest anchor + triage hint) — the REAL line-count subtraction (decision B retained it,
so derive_signals.py GREW 1063→~1200; correctness shrank, the file didn't) · scale the live menu further via the inverted loop (glued health-care fin-2026-a001 now
derivable=true/not-yet-derived = easiest; LOW advisories ISIS fin-2025-a001 + Iran-terror fin-2024-a001; EFE corpus record) · tighten the coarse `rf_region` if scaling widely ·
(carried) FATF non-derivable labeling polish · corpus combination-lift wow beat · elder presentation-values true-up · fentanyl verbatim re-point.

Gates:
- [x] Direction confirmed by user (invert extraction + scale as proof; groundedness gate + section-cite; demote extractor; converter dissolved — 2026-06-06)
- [x] Delivery accepted (post-implementation report 2026-06-06; impl commit bca3612)
