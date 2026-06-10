<!-- nana:approved 2026-06-10 -->
# Spec: Phase 44 — Live extraction quality (targeted harness, classified fixes, processing page)

## Objective

Reproduce, classify, and fix the two live-extraction quality failures the maintainer found in real-use
testing — missed high-risk-country wire red flags and aliases assigned to the wrong entity — measured
by a committed targeted harness; optimize processing speed only where the harness proves quality
holds; and move post-click processing onto a dedicated live screen.

## Context

The signal-watch LIVE mode (companion `scripts/serve_news.py` + local llama-cpp) extracts entities
(aliases/properties/relationships) and red flags from pasted articles or private investigation notes;
the deterministic gate `scripts/news_ground.py` grounds everything (grounded-or-stripped) and FOLDS
subset/moniker entity names into parent aliases. Quality was last worked in Phase 40 (red-flag prompt
iteration, measured by a gitignored scoring harness) and Phase 38 (entity precision via context
shaping); Phase 43 made the pipeline size-robust with staged progress rendering. The maintainer's
limited real testing now reports: (1) obvious high-risk-country wire flags missed; (2) aliases
attached to clearly-wrong entities; (3) wanting processing on a fresh page after clicking run;
(4) speed concerns, conditional on quality. "Prompt-regression discipline" below means the
Phase-41 ruling concretely: red_flags stays FIRST in EXTRACT_SCHEMA property order, a candidate
prompt never reduces the kept-flag count on the regression set, and holdout material is scored
once per candidate, never iterated against. The direction gate closed 2026-06-10 (assumption ledger
appended): sample SENTENCES only from the real material (never committed), measure-and-classify
before fixing, fixes through proven seams, speed quality-gated. A 13-fixture replay test pins the
deterministic core; goldens regenerate deterministically from pinned captures; the offline ship file
`dist/news` must stay byte-identical (live client code is build-time stripped).

## Scope

### In scope
- A COMMITTED targeted quality harness (promoted from the Phase-40 gitignored scratch): registry
  scoring + alias-ASSIGNMENT (ownership) scoring + per-stage wall-time profile; committed part runs
  on committed/fixture material only. The harness has GATE semantics, not report-only: a `--check`
  mode exits non-zero if any dimension drops below a committed baseline file
  (`tests/fixtures/news-live/quality-baseline.json`); a report mode stays for profiling.
- Local-only targeted stress material: synthetic high-risk-country wire notes (note-register, not
  just article-register) embedding the maintainer's sample sentences; local commercial articles.
- Classification of both failures, then per-class fixes: SYSTEM_PROMPT iteration and/or
  `news_ground.py` gate/fold repair (regate procedure mandatory).
- Quality-gated speed optimization at the measured hotspot (likely the verify loop).
- A dedicated live processing screen (in-page screen swap inside the LIVE region).
- Minimal anchor-store hygiene position. DONE = the local-store reset path documented in
  docs/news-live.md. Extending the existing prune route to anchor alias rows is OPTIONAL and taken
  only if it reuses the existing watchlist-prune route shape without new store-write semantics
  (the store is local/gitignored — a reset is legitimate).
- Bundled living-doc hygiene trim (tasks.md archival; _CURRENT_STATE/_ARCHITECTURE under cap).
- Full regate + docs.

### Out of scope
- Structural EXTRACT_SCHEMA changes (field add/remove/reorder) — if a fix demands one, STOP and
  surface as a finding (checkpoint), never silent.
- Fuzzy cross-scan merge adjudication; bulk scanning; new corpus sources; offline `dist/news` or
  committed-record changes; any non-negotiable change.
- A full anchor-store re-scan/repair story (only the minimal hygiene position above).
- Committing any real/commercial material as fixtures (US-federal-only `FIXTURE_META` allowlist).

## Approach

Classification-first: the harness reproduces each reported failure and names its layer BEFORE any
fix is attempted. For "missed" flags, bucket every absent flag as model-miss vs gate-DROP with the
`dropped[]` audit — three known drop paths must be checked (the normalizer strips every `*`
character, so note-register bullets can fail the raw-substring check; the merge rule can collapse
repeated wires retold as anecdotes; non-contiguous stitched quotes fail `flag not in body`). For
wrong aliases, classify model-assigned vs fold-assigned: the gate's alias check verifies the string
exists in the article, never that it co-refers; fold rule (a) folds a strict token-subset into the
FIRST superset entity, type-blind (a bare shared surname folds into whichever parent extraction
order yields). Fixes follow the class: prompt iteration through the prompt-regression discipline
(holdout eval, never-reduce), deterministic gate/fold repair through the regate procedure
(selftest fixtures + 4 committed records + replay goldens). Speed work starts from the measured
per-stage profile and lands only with quality held. HOLDOUT SPLIT, defined now: the committed
fixtures are the REGRESSION set, never the tuning set; local stress material is split
calibration/holdout, and the holdout tier is never used during prompt iteration — it is scored
once per candidate prompt at evaluation. The processing screen is a stage-completion reveal
surface (grounded results only, never a token stream) that keeps the NDJSON stream consumer
alive.

### Domain Research Questions
1. Which normalizer/merge behaviors in the gate are hostile to note-register text (terse fragments,
   `*` bullets, abbreviations, bare country names) — and which need a deterministic fix vs honest
   documentation?
2. Does high-risk-jurisdiction recognition rest on the model's parametric FATF-list knowledge (a
   bare country name with no "high-risk" cue in text)? Should the registry family carry jurisdiction
   exemplars — and how is that honest (the model flags, the gate grounds, no fabricated risk list)?
3. What alias-attachment check is honest and deterministic enough for the gate: structural adjacency,
   type-match on fold, ambiguity refusal (2+ superset parents → don't fold), or a verify-pass
   co-reference question?

## Constraints (CRITICAL)

- Classify before fixing — a prompt-only alias fix is FALSIFIED if `screen_entities` still misparents
  a synthetic two-entity shared-surname note run through it directly: prevents fixing the wrong
  layer while the deterministic fold keeps producing the failure.
- Bucket absent flags as model-miss vs `dropped[]`-with-reason before touching SYSTEM_PROMPT; only
  confirmed model-misses justify prompt work; each confirmed drop-path gets its own deterministic
  fix + selftest fixture: prevents prompt churn against gate drops.
- "Quality preserved" = harness scores ≥ the frozen baseline EXACTLY (kept-flag count
  never-reduce; alias-ownership and entity precision never-reduce), where the baseline is frozen
  into `tests/fixtures/news-live/quality-baseline.json` + the T1 matrix BEFORE any T4 edit; plus
  13/13 replay and the >180s long-note probe. Any speed change failing `--check` is reverted:
  prevents invisible quality-for-speed trades AND threshold-shopping after seeing a speed win
  (the Phase-41 schema ordering alone cost 12.5% kept flags — small changes regress measurably).
- Prompt edits go through the prompt-regression discipline: red_flags stays FIRST in EXTRACT_SCHEMA
  property order; never-reduce guard on kept flags; holdout evaluation: prevents the r3-style
  calibration overfit regression.
- Any `news_ground.py` edit runs the full regate: `--selftest` (with new fold fixtures), `build.py`
  (4 committed records pass), replay goldens regenerate deterministically (NO model re-capture),
  news-stream alias-matcher assertions: prevents silent shared-gate breakage (build.py imports it).
- The dedicated processing view is an IN-PAGE screen swap inside `/*LIVE_START*/…/*LIVE_END*/` that
  keeps the in-flight NDJSON fetch alive; real navigation is forbidden (it aborts the stream,
  discards the extraction, and a re-click hits the single-flight 409 with a ghost job draining the
  slot); presenter keys (Esc/↺/reset) firing mid-extraction and the 409 path are handled honestly;
  stage-completion rendering only, never a token stream: prevents the UX change from breaking the
  Phase-43 robustness contracts.
- Offline byte-identity: all new markup/CSS/JS inside the LIVE region; `build.py --check all` 5/5
  zero drift + the strip assertion green before any UI task is called done: prevents ship-artifact
  drift.
- Privacy: the maintainer's sample sentences + commercial captures live ONLY in gitignored local
  paths (`.dev-wiki/tmp/ph44*`); reproductions committed to the repo are SYNTHETIC reconstructions;
  fixture promotion stays US-federal-only (`FIXTURE_META` asserted): prevents the natural
  commit-the-failing-case move from breaching the no-real-data non-negotiable.
- The always-on "Illustrative data & outputs" badge stays; no non-negotiable changes.

## Success Vision

The maintainer pastes a note-register investigation text with high-risk-country wire content and the
live scan surfaces those flags grounded — or, where it can't, the harness names exactly which layer
loses them and why. Aliases attach only where the mechanism chosen by Domain Research Question 3
permits (refusal, type-match, adjacency, or verify co-reference — the research decides); the local
store has a documented hygiene path for history poisoned by the old behavior. Speed improvements are real measured numbers with quality provably held — or an honest
"no optimization preserved quality" finding. Clicking run extraction lands on a dedicated processing
screen that reveals grounded results progressively. The quality measurement is no longer scratch:
a committed harness any future phase can re-run. The wiki/state files are back under their caps with
nothing lost. Every exit gate (fixtures, regate, drift checks) is green, and what was fixed on
committed evidence is separately re-confirmed by the maintainer on the real material.

## Exit Criteria (machine-checkable)

- [ ] `python3 tests/news_quality_harness.py --check` — exits 0 only if every dimension (registry
      recall, alias-ownership, entity precision, kept-flag count) is ≥ the committed baseline
      `tests/fixtures/news-live/quality-baseline.json`
- [ ] `grep -Eq 'model-miss|gate-DROP|fold-assigned|model-assigned' .dev-wiki/tmp/ph44-results.md
      && grep -qi 'hotspot' .dev-wiki/tmp/ph44-results.md` — the classification matrix names each
      failure's class and the measured hotspot
- [ ] `python3 scripts/news_ground.py --selftest` — green, including new fold/drop-path fixtures
- [ ] `python3 tests/news_live_test.py` — 13/13 replay green with NO model re-capture
- [ ] `python3 scripts/build.py --check all` — 5/5 byte-identical (offline dist/news untouched)
- [ ] `node tests/news-stream.test.mjs` — green with assertion count ≥ 146 (from 140), the new
      assertions covering the processing-screen swap + staged reveal + mid-extraction
      presenter-key/409 handling
- [ ] `node tests/corpus-explorer.test.mjs` — green (untouched surface stays green)
- [ ] `python3 tests/news_live_test.py --live` — real-model smoke incl. a wire-note probe
- [ ] `wc -l < .dev-wiki/_CURRENT_STATE.md` ≤ 110 AND `wc -l < .dev-wiki/_ARCHITECTURE.md` ≤ 110
- [ ] `grep -c '^## Phase' .dev-wiki/tasks.md` returns 1 (active phase only) and tasks.md contains
      a pointer index to the archived blocks

## Checkpoints

- After T1 classification: report the matrix (failure classes + hotspot) to the maintainer BEFORE
  starting T2/T3 — the classes route the fixes, and the maintainer holds the real material.
- After T2/T3 fixes pass committed evidence: ask the maintainer to re-confirm on the real material
  locally (the privacy boundary means committed evidence can never include the actual failing cases).
- If a fix demands a structural EXTRACT_SCHEMA change: STOP and surface as a finding.
- If no speed optimization preserves quality: report the honest skip-with-reason and move on.
- If offline dist/news cannot stay byte-identical: STOP and surface.
- Blocked >3 attempts on a task: mark [blocked] and ask skip-or-abort.

## Assumptions

- The reported failures reproduce on constructible material seeded with the sample sentences. If
  false: report the non-reproduction honestly, ask the maintainer for more material or a guided
  local session — do not tune against an unvalidated proxy.
- The failures classify into actionable layers (model vs gate vs fold). If ambiguous after the
  harness run: present the ambiguity at the T1 checkpoint with the evidence, rather than burning
  eval rounds guessing.
- The Phase-40 scoring scratch is recoverable as the harness starting point. If missing: rebuild
  from the Phase-40 journal's measurement description (proxies + registry scoring) — the harness is
  a deliverable either way.
- The maintainer supplies sample sentences early in T1. If not yet available: build the synthetic
  tiers from the failure DESCRIPTION (high-risk-country wires, shared-surname aliases) and flag the
  unseeded status in the matrix.
- stream/verify behavior measured in Phase 43 still holds on the current llama-cpp build. If the
  wall-time profile shifted: the T1 profile is authoritative; re-derive the hotspot before T4.
