---
type: journal
date: 2026-06-07
phase: 27
slug: 2026-06-07-phase-27-corpus-shippability
tags: [corpus, presentation, re-extraction, assessment, workflow, shippability, M7]
---

# Phase 27 — Make the corpus demo shippable: assess → presentation fixes → faithfulness-guarded re-extraction (M7)

> Lite, 7 tasks (incl. 2 dynamic workflows + an L), DELIVERED → committed/pushed to `main` per user instruction (runtime browser review DEFERRED by the user to before the next phase — a USER OVERRIDE on the delivery-gate ordering). Reviewer gate: self-check (lite). All gates green.

## Objective & the reframe
Phase 26 marked the corpus demo "showcase quality" (its reviewer scored 10/10) but the user reviewed the BUILT artifact and judged it **NOT shippable**: the Read-advisory extract/translate beat "brutally bad", the build animation "not in place" unlike the six-act showcase, and floated **foregoing the grounding system** to rely on LLM extraction+translation fully. This is the 4th consecutive phase (24→25→26→27) where the user reframed to an output-quality gap he saw in the dist — confirming the `[[reframes-to-output-quality]]` memory. A new framing landed too: **"the corpus demo IS the showcase"** — the corpus explorer is now the PRIMARY artifact; the six-act showcase recedes to the oracle/reference.

## The load-bearing move: assess before churning
The user chose **ASSESS-ONLY FIRST, THEN REPLAN** over keep-gate-fix-now / go-fully-LLM-now (his cost-of-error pattern — evidence before committing to a build tier). A READ-ONLY assessment (deterministic metrics + the `ph27-corpus-quality-assessment` 44-agent workflow) DISPOSED the framing: the brutality was **PRESENTATION, not the grounding system** — tiers **PRESENTATION_ONLY 39 · RE_TRANSLATE 1 · RE_EXTRACT 2→3**; register already held (36/42 @5); the verbatim flags were real. PUSHBACK held against "forego the gate": it would risk fabricated "verbatim" quotes (a compliance non-negotiable) AND wouldn't fix the raw-article render. Findings → `articles/phase-27-assessment-findings.md`. The user then chose **broader re-extract** (crisper quotes everywhere) at the build-replan gate.

## What shipped (T1–T7)
- **T1** assessment (above) — read-only, no ship mutation.
- **T2 cleanArticle** (corpus.html) — markitdown-sanitize the DISPLAYED source: `\f`/`\r`→`\n` (the page-break **form-feed** was the real glued-header cause `FINCEN ADVISORY\fIn contrast…`), tab-soup→space, drop running headers / letter-spaced `F I N C E N` / bare page-numbers / `OPERATIONAL ALERT|BRIEF`. **Subtraction:** dropped the footnote-digit strip — it removed digits `normalize()` KEEPS, desyncing the highlighter (→96.2%); dropping it restored 100% (the `.10` superscripts stay, minor). Validated on all 42 mds: ≤2.1% removal, 0 years/amounts lost.
- **T3 highlightArticle** — rewrote to NORMALIZE BOTH SIDES (the gate's own `normalize()`) + an index map back to source positions. **634/634 flags highlight = 100%** (from 95.3% raw; the literal matcher on cleaned text would REGRESS to 91% → T2+T3 are COUPLED, ship together). Gate untouched.
- **T4 build-beat** — ported the showcase Act-4 `.run` "working-pulse" rhythm into `renderSignal` in a `.proposal` grid (spec | buildside) + a `.liftwrap`/`.liftside` rationale panel on `renderLift`; `firestat` OMITTED (its fire-count/precision stats would be fabricated). No numbers.
- **progressive read** (user's checkpoint note) — removed the 1600-char CAP; types the WHOLE article, per-tick chunk length-scaled to a bounded ~6s. The demo's first wow, now complete.
- **T5 re-extraction** (the `ph27-reextract-tighten` 72-agent workflow: 36 tighten → 36 INDEPENDENT verify) — tightened 121 over-long verbatim flags to crisp **contiguous SUB-SPANS** of the current flag. THE SAFETY DESIGN: a sub-span of an already-grounded quote can't fabricate → grounding is TRANSITIVE; a deterministic applier relocated each proposal to the exact raw sub-span, gated on `normalize(new) ⊂ normalize(current)` + ≥24 nchars + red_flag-distinct, byte-surgically rewrote only the flag line (OFAC compact arrays preserved). 123 proposed → 121 applied / 2 gate-rejected; 33/33 `--check-derived` clean; 0 non-flag lines changed. **FAITHFULNESS HELD:** mean 331→212 (~36% tighter); the 36 still >240 are genuinely-long single-sentence advisory indicators KEPT WHOLE — trimming would drop the qualifying condition (= fabricated brevity, rejected; a deterministic first-sentence trim was WORSE at 262, proving no clean clause boundary). Ties to `[[honesty-over-demo-drama]]`.
- **T6** — re-translated `fin-2022-a001` IND-02/IND-04 prose-y red_flags to the mechanism-named register (kleptocracy: "State-entity services billed through high-risk-jurisdiction intermediaries", "PEP luxury / real-estate purchases beyond declared source of wealth").
- **T7** — regate: `--check all` 4/4 ZERO DRIFT, `--selftest` PASS, all 42 `--check-derived` clean; harness 139→**148** (+9 T2/T3/T4 asserts — the `.run`/`.ok` animation is post-render classList so asserted via STRUCTURE not `_html`); CLAUDE + README updated (compliance wording byte-unchanged). dist/corpus 2.17MB→**2.15MB**.

## Escape hatches
- **USER OVERRIDE** ×2: (1) **broader re-extract** chosen over the recommended minimal-data-touch (I surfaced the magnitude — 180 flags/39 docs — + the faithfulness risk; held a faithfulness guard); (2) **commit+push to main before the runtime review** (review deferred to before next phase). Both noted.
- **DISCOVERY**: the agent tightening was too conservative (mean 212, 36 still >240); I tested a deterministic first-sentence trim as an alternative — it was WORSE (262) — confirming the dense advisory indicators have no clean clause boundary and the kept-whole outcome is the faithful one.

## Health Delta
Harness 139 → 148 (+9). `--check all` 4/4 zero drift. `--selftest` PASS. 42/42 derived `--check-derived` clean. No new deps (workflows are session-driven; the applier was a transient `.dev-wiki/tmp` script, deleted). dist/corpus 2.17→2.15MB.

## Review Gate
Lite (self-check is the quality gate — no unified reviewer dispatch). Self-check: scope held (corpus.html + 33 derived + dist + tests + docs); grounding core + showcase + source mds + corpus-status + typology-map byte-frozen; no fabricated numbers; compliance wording unchanged; every tightened flag gate-grounded.

## Gate Compliance
`<!-- gate-log:phase-27 direction=approved delivery=pending -->` — direction gate satisfied (assess-only-first + broader-re-extract both user-approved). Delivery gate **pending the user's deferred runtime review** (he authorized commit/push without reviewing; will eyeball before the next phase) — honest pending, not auto-accepted.

## Soft Observations / Phase N+1 Candidates
- **The corpus is now the primary demo** ("the corpus demo IS the showcase") — future polish weights the corpus; the six-act showcase is the oracle. Saved to memory.
- **Showcase landing** (index.html) still roadmapped (carried since Phase 26) — the corpus has one; the showcase doesn't. Needs unfreezing index.html.
- **Real backtested combination-lift figures** to replace the illustrative template (no date) — standing obligation, now also relevant to the corpus's lift screen.
- **The 36 kept-whole long flags** are faithful (not a defect) — but a future "smart display clamp" (clause-boundary truncation in the xrow) could make even the long verbatims read complete without touching data. Display-side, additive.
- **Pre-commit `--check all` gate** still deferred (the partial-commit defect has bitten before) — would have auto-caught nothing this phase (clean), but remains a durability candidate.

## Activation Quality
No `active-knowledge.md` this phase (lite, no knowledge-wiki retrieval at plan time) — skipped.
