<!-- nana:approved 2026-06-10 -->
# Spec: Phase 45 — Corpus demo presentation polish (pre-presentation day)

## Objective

Polish dist/corpus for tomorrow's (2026-06-11) bank-stakeholder presentation: fix the
review-found live-risk issues, replace the fabricated combination-lift percentages with
honestly-derived inventory counts (concept-focused beat), close the FINTRAC lens-view
attribution gap, and run a ranked copy-coherence pass — absorbing late user feedback behind an
explicit freeze checkpoint.

## Context

The corpus explorer is the primary demo (a presenter-driven offline vision prototype over a
real derived corpus: 2,251 indicators / 56 derived records / 62 publications / 5 sources).
Two independent review agents (2026-06-10) found: three live-risk HIGHs (up to ~15s blank
rows on FINTRAC guidance docs from an uncapped animation stagger; the human gate reading
pre-decided; two zero-build-now docs dead-ending with impossible advice), one compliance HIGH
(FINTRAC verbatim excerpts on the Capabilities/Data-sources lens screens render with an empty
footer attribution — the Phase-28 relocated-attribution mechanism only fires on detail views),
and ranked copy MEDIUMs (atom vocabulary unintroduced before the final beat, landing omits the
largest source family, "Advisories" chrome residue, de-hyphenated typology slugs, etc.).
Separately, the user directed removal of the lift screen's generic 18→64→83 illustrative
template (Phase 18's compromise; its removal completes that honesty arc). The assumption gate
closed 2026-06-10: R2 real-inventory-counts replacement (A1, don't-know→worked-examples→accept),
showcase Act-5 untouched (A2), gate fix = copy + stagecraft (A3), attribution extended not
suppressed (A4), global polish + demo-path notes (A5). Ledger block appended.

## Scope

### In scope
- corpus.html (copy, lift screen, attribution mechanism, presentation timing) and its rebuild
  into dist/corpus/index.html (the frozen corpus baseline intentionally MOVES this phase).
- tests/corpus-explorer.test.mjs (assertions move with the redesign, same commit).
- tests/smoke-checklist.md (presenter/demo-path notes, pre-present sequence).
- CLAUDE.md "Honesty constraints" rewritten in place (the approved-fabrication-reversal
  paragraph is replaced by the honest-inventory description); HANDOFF.md §8 phase note if the
  lift template is named there.
- .dev-wiki bookkeeping + specs/ (this file).

### Out of scope
- index.html / the three showcase dists and news.html / dist/news — byte-identical (the
  showcase Act-5 lift template stays by gate decision A2).
- scripts/build.py, scripts/derive_signals.py, the grounding core, all derived records,
  manifests, and overlays — no data or pipeline edit; this is a corpus.html-side phase.
- Any new computed similarity/overlap/lift/performance number — the removal's whole point.
- The live news companion (serve_news/news_ground/news_store/news_fetch) — untouched.
- R3 (composition graph) — post-demo upgrade candidate, not tonight.

## Approach

Fix the three live-risk HIGHs first (cheapest, highest live cost). Then the lift beat: delete
the LIFT template, its bars, and the "Illustrative · pending calibration" tag; render the R2
composition-search-space — real inventory counts computed client-side from __CORPUS__ (covered
indicators in the committed signal's typology, across the contributing regulators), framed as
candidate composition partners feeding the promotion gate. Numbers on screen are plain counts
with their scope labeled — inventory facts, never performance claims, no ratio that smells like
the removed lift. Then extend the footer attribution to the two lens views; then the ranked
copy pass; then the user walkthrough freeze checkpoint; then the full regate. The presenter
story fix for the human gate is copy + stagecraft (deselect live), not interaction redesign.

Specific copy edits the exit criteria reference: the Signal screen's build-log step 4
(`corpus.html:1051`, `<div class="blstep" data-s="4">Backtest on population</div>`) currently
animates to a ✓ claiming a backtest that never ran; it becomes "Queue backtest on population" —
a handoff register, consistent with the E-23/Model-Validation routing step beside it. The
stagger fix is bounded: the LAST build-rec row is visible ≤2s on the largest doc
(fintrac-guid-securities, 173 rows; cap ≈ `Math.min(k*90, 1500)`), instant under
`prefers-reduced-motion`. The full ranked findings list (both reviews) lives in
`.dev-wiki/articles/decisions/phase-45-corpus-presentation-polish.md` — the copy pass works
from that list, not from memory. The T5 deferred list lives in the tasks.md T5 block.

### Domain Research Questions
1. On the lens views, which FINTRAC publications contribute *visible quoted text* per screen
   state — and does the attribution need to be a list (multiple docs on screen at once)?
2. What does the R2 copy look like at the boundaries — a single-regulator typology (elder: 5
   covered, FinCEN only) and the smallest typology a presenter could plausibly land on?
3. Where exactly do docs (HANDOFF.md, smoke-checklist) still describe the 18→64→83 template
   after the change — stale docs that contradict tomorrow's artifact confuse the presenter.

## Constraints (CRITICAL)

- NO fabricated or performance-shaped number anywhere on the lift screen: every displayed
  number is a plain count or honest union with its scope labeled on screen; indicators are NOT
  presented as de-duplicated across regulators — prevents replacing one fabrication with a
  subtler one.
- Test assertions for the new lift counts derive their EXPECTED values by recomputing from the
  committed data files (`data/*/derived/*.json` + the typology overlays) — never from
  `__CORPUS__` or the rendered DOM — prevents the harness pinning a wrong count (NaN→0,
  double-count) as truth via a tautological assertion.
- FINTRAC attribution carries ALL THREE licence elements (© His Majesty the King in Right of
  Canada + complete document title + "a copy of the version available at <URL>") for EVERY
  FINTRAC doc contributing visible quoted text on that screen, updating with the lens filter;
  footer stays EMPTY for US-only screens — prevents both licence breach and over-attribution
  misstating the US docs' public-domain basis, in front of the one audience guaranteed to notice.
- The four non-corpus dists stay byte-identical: `--check` on those targets runs LAST, after
  every edit — prevents a shared-convention ripple silently moving a frozen artifact.
- All edits confined to corpus-side files; the copy pass NEVER "harmonizes" lift language into
  showcase configs — prevents gutting the protected showcase wow beat or unfreezing it.
- The always-on "Illustrative data & outputs" badge stays on every screen state — removing the
  lift disclaimer does not touch the badge (different fixtures, different jobs).
- Code freeze at the T5 walkthrough: feedback arriving after freeze goes to an explicit
  deferred list, never the artifact — prevents an unbounded copy pass displacing the
  verification budget on presentation eve.
- Zero/empty slices render honestly: zero-build-now docs get a truthful empty state (no
  impossible advice); no "0 of 0", NaN, or unexplained cross-screen count mismatch.

## Success Vision

A presenter can walk any document tomorrow without a blank-screen wait, a dead end, or a
number they cannot defend. The combination-lift beat lands as a concept payoff — the corpus
itself (real covered-indicator inventory across regulators) is the evidence, the promotion
gate is the discipline — with one FEWER disclaimer on screen because nothing there is
fabricated. The human gate visibly belongs to the human. FINTRAC text is never on screen
without its licence-complete attribution. The vocabulary reads as one story from landing to
close: atoms seeded early, composed at the end. The story-review and sweep findings are
dispositioned (fixed or explicitly deferred by name), and the user's late feedback has a home.

## Exit Criteria (machine-checkable)

- [ ] `! grep -qE 'pending calibration|liftbar' corpus.html && ! grep -qE 'pending calibration|liftbar' dist/corpus/index.html`
- [ ] `node tests/corpus-explorer.test.mjs` exits 0 (assertions updated WITH the redesign: lift
      counts asserted against independently-derived expected values; FINTRAC lens attribution
      three-element + US-empty assertions; stagger cap; gate "proposed" copy; zero-build-now
      empty state)
- [ ] `python3 scripts/build.py corpus && python3 scripts/build.py --check all` → 5/5 (corpus
      baseline moved + re-frozen; the other four byte-identical) — run LAST
- [ ] `node tests/news-stream.test.mjs` exits 0 (untouched-green)
- [ ] `grep -c 'Queue backtest' corpus.html` = 1 (the Signal build-log step 4, see Approach) and
      `! grep -q '↺ Advisories' corpus.html && ! grep -q '↺ Advisories' dist/corpus/index.html`
- [ ] `grep -q 'candidate composition partner' dist/corpus/index.html` (a stable R2 marker —
      catches deleted-but-not-replaced)
- [ ] `! grep -qE '18→64→83|18 → 64 → 83' CLAUDE.md` (honesty section rewritten in place)
- [ ] tests/smoke-checklist.md contains the demo-path/presenter notes (route, deselect
      stagecraft, second-gate narration, docs-to-avoid, fonts cache warm)

## Checkpoints

- After T2 (lift R2) renders: rebuild + eyeball the screen on a big doc, a small/single-regulator
  typology doc, and a zero-build-now doc BEFORE proceeding — the beat must read as a payoff,
  not a regression.
- T5 user walkthrough = the FREEZE checkpoint: present the rebuilt dist, disposition feedback
  ranked + time-boxed; overflow → the deferred list by name. R1 fallback decision point: if R2
  reads wrong to the user here, flip to the zero-numbers ladder (copy-only change).
- If any non-corpus dist drifts under --check: STOP and surface — never re-freeze around it.
- If a fix appears to require touching derived data, build.py, or the grounding core: STOP and
  surface as a finding (different phase).

## Assumptions

- The R2 counts are computable client-side from __CORPUS__ as already injected (per-indicator
  typology + status + source registry present). If false: compute at build time into the
  config? NO — that's a build.py edit (out of scope); instead fall back to R1 (zero numbers)
  and surface the gap.
- The committed signal's typology is well-defined for every doc a presenter can land on
  (inherit-default + sparse override). If a doc yields no typology or an empty covered set:
  the copy degrades to the honest corpus-wide framing ("the corpus holds N covered indicators
  across M regulators") rather than a blank.
- The harness's existing lift block (P26-5) is the ONLY place pinning the fake values. If
  other assertions reference them: update those in the same commit (grep
  `liftbar|18→64→83|pending calibration|fill (weak|mid|strong)` across tests first — bare
  `18`/`83` greps are too noisy to be the check).
- FINTRAC source URLs needed for the three-element attribution exist in the corpus records or
  manifests. If absent for some doc: surface at T3 — do NOT invent a URL; fall back to the
  documented manifest URL or flag the doc to the user.
- The user is available tonight for the T5 walkthrough. If not: freeze at the agent's own
  pre-present sequence, leave T5 dispositions explicitly OPEN in tasks.md, and flag the R1
  fallback decision as undecided-defaults-to-R2.
