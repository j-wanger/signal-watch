---
type: reference
phase: 26
slug: phase-26-register-rubric
created: 2026-06-07
updated: 2026-06-07
---

# Phase 26 — the AML-indicator register + beat design briefs

The reference for the T2 re-translation workflow and the T3–T5 UI beats. The Phase-25 `red_flag`s read like advisory PROSE; the bar is the showcase's crisp, typology-named detection-scenario **indicators** (`config/typologies/fentanyl.json`, `elder-financial-exploitation.json`).

## The register (the bar the re-translation holds to)

A `red_flag` must read like a showcase indicator, not a sentence:

1. **Name the MECHANISM, not the customer.** Drop subject throat-clearing — "An older customer…", "A customer that…", "A vessel…", "Documentation associated with…". Lead with the laundering pattern.
2. **Terse** — a noun phrase, a label, ideally ≤ ~10 words. No trailing explanatory clause unless it sharpens the mechanism.
3. **AML lexicon** where the verbatim supports it — fan-in, flow-through / pass-through, structuring / sub-threshold, layering, nominee / third-party control, funnel account, money mule, front company, MCC / activity mismatch, rapid conversion, trade-based, round-dollar, smurfing.
4. **Faithful** — name only what the verbatim `flag` states; add NO mechanism / typology / threshold the verbatim doesn't support. A change of REGISTER, never enrichment. The verbatim stays beside it as the grounded check (show-both).
5. **Shape** — present, non-empty, DISTINCT from the verbatim, 12–240 chars (the gate is unchanged; only `red_flag` VALUES change — grounding on the verbatim `flag` is untouched).

## Exemplars (the showcase target)

- **fentanyl.json:** "Rapid pass-through / flow-through account" · "Inbound e-transfer fan-in from unrelated senders" · "Nominee / third-party account control" · "Sub-threshold structured cash deposits" · "Courier / freight payments inconsistent with profile" · "Front-company MCC / activity mismatch".
- **elder.json:** "Dormant account reactivated into a sustained drain" · "Transfers to new payees with no in-person relationship" · "Bulk gift-card / prepaid-access purchases" · "Early CD / account closure ignoring penalties".

## Before → after (Phase-25 prose ✗ → Phase-26 register ✓)

| Verbatim `flag` (grounded, unchanged) | Phase-25 ✗ | Phase-26 register ✓ |
|---|---|---|
| "…receives and transfers money… no in-person relationship…" | Funds received then forwarded interstate or abroad to payees with no in-person relationship (money-mule pattern) | **Receive-and-forward to no-relationship payees (mule pass-through)** |
| "…purchases large numbers of gift cards or prepaid access cards." | Bulk gift-card / prepaid-access-card purchases by an older customer | **Bulk gift-card / prepaid-access purchases** |
| "…memo line such as 'tech support services,' 'winnings,' or 'taxes.'" | Payments carrying scam-marker memo lines ('tech support', 'winnings', 'taxes') | **Scam-marker memo lines (tech-support / winnings / taxes)** |
| "Dormant accounts with large balances begin to show constant withdrawals." | Long-dormant, large-balance account reactivated into a sustained drawdown | **Dormant high-balance account → sustained drawdown** |
| FINTRAC synthetic-opioids: "…cash deposits structured below the reporting threshold across branches…" | (prose) | **Sub-threshold structured cash across branches** |

## Beat design briefs (T3–T5)

### T3a — progressive article render (port `index.html` `streamAdvisory`)
The showcase's Act-1 TYPES a capped opening (the "agent reading" beat), then `reveal()`s the full body with `<span class="hl">` highlights, then extracts. Port to the corpus Read-advisory screen: type a capped opening of `article_text` → reveal the full highlighted article → stagger-reveal the extract→translate `.xrow`s. Reduced-motion = one-shot (current behavior). Reuse the existing `highlightArticle` + `.xrow` list; add the typing/reveal staging via `T()`.

### T3b — grouping + sort (Select)
Group the doc cards by SOURCE — section headers "FinCEN Advisories", "FinCEN Alerts", "OFAC", "FINTRAC" (doc_type) — and within each source sort by **date descending** (newest first; `a.date`). Keep the live-first emphasis (derived cards clickable). The Typologies toggle (Phase 24) stays. Red-flag grouping: within a doc, group indicators by `section` (e.g. financial / behavioral) where present, else flat — surfaced on Coverage / Build-recs as sub-group headers (the per-doc typology is singular, so "group red flags by typology" = group by the doc's section/sub-category; confirm with Jake if he meant the cross-corpus view).

### T4 — build-log + combination-lift wow (port Act-4 + Act-5)
- **Build-log** (Act-4, honest): a `.buildlog` of `.blstep`s — "Draft definition from advisory" → "Map to data features" → "Generate proposal" → ◈ human gate → "Backtest on population" → ⚖ "Route to Model Validation" — auto-completing via `T()` with ✓ marks. Reads the REAL `build_logic` of the picked target signal. Structural, no numbers — safe.
- **Combination-lift** (Act-5, illustrative): the firestat count-ups + animated lift bars. The corpus records carry NO precision/lift figures, so this is a **generic illustrative template** (e.g. signal-alone weak → +combination mid → +combination strong), with a LOUD "illustrative · pending calibration" tag under the always-on badge. NEVER 42 fabricated per-doc findings; NEVER presented as real. Jake supplies real figures later. (Reverses the Phase-18 no-fabricated-lift call — honest because nothing is claimed as real.)

### T5 — landing page
A narrative entry before the Select grid: frame the corpus story (a multi-jurisdiction public corpus — FinCEN + OFAC + FINTRAC, US + Canada — pointed at the same signal loop), an "Enter" CTA → Select. Reduced-motion-safe. The showcase (`index.html`) gets a landing too only if cheap + minimal (else roadmap; it's byte-frozen by default).

## Checkpoint (T1)
Re-translate EFE (+ cross-source exemplars) to the register, confirm `--check-derived` clean + the labels read like the showcase indicators (eyeball vs elder/fentanyl). If the register can't be hit while staying grounded/distinct → report before T2.
