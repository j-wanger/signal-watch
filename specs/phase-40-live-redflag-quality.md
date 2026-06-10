<!-- nana:approved 2026-06-09 -->
# Spec: Phase 40 — Live red-flag extraction quality (measure-first)

## Objective
Make the live news companion's red-flag extraction measurably more complete and consistent on long commercial articles — via prompt context-shaping (mechanism checklist + granularity contract), one measurement-earned deterministic gate check (duplicate-flag collapse), and a conditional sectioned-extraction fallback — with zero change to any offline ship artifact.

## Context
The companion server (`scripts/serve_news.py`) extracts entities + red flags from a pasted or URL-acquired article via a local Qwen model (llama-cpp, 127.0.0.1:8080); a deterministic gate (`scripts/news_ground.py`, shared with `scripts/build.py`'s news validator) drops anything not verbatim-grounded in the article. Faithfulness is guarded; completeness, span tightness, translation register, and granularity consistency were not. Phase-40 T1/T2 measured a baseline over 12 commercial stress articles (selected deterministically from a local negative-news corpus; licensed text, LOCAL-ONLY under `.dev-wiki/tmp/ph40/`) plus the 7 committed US-federal articles, against a BLIND second-rater reference extraction (consensus, never ground truth): positive agreement federal 0.73 vs commercial 0.51–0.54; `cov_of_ref` (the fraction of the blind reference's flags the model matched — the completeness measure) is ~0.40 on commercial longreads vs 0.67 federal, while `cov_of_qwen` (the fraction of the model's flags the reference backed — the precision-side measure) is 0.80–0.86 everywhere — the residue is RECALL, not precision. These two metric names are canonical throughout this spec and in the measurement artifacts. Failure clusters (user-adjudicated at the T2 checkpoint): early-stop on narratives with positional decay (miss-rate ~0.3 in the first two article deciles rising to 0.6–0.9 later; NOT hard truncation — largest article ≈7.5K tokens); an institutional/control-failure blind spot (the prompt's flag examples are transactional-only); granularity variance (4–29 flags per article; 1 exact-duplicate span pair); a latent prompt/gate bounds drift (prompt says 12–200 chars, gate enforces [12,240]). Checkpoint rulings: prompt = mechanism-registry checklist + granularity contract + exemplars; gate = duplicate-collapse ONLY (no span cap, no topic rules); the planned precision verify is DROPPED (nothing to fix); sectioned extraction replaces it as the conditional residue fix.

## Scope
### In scope
- `scripts/serve_news.py` — SYSTEM_PROMPT red_flags contract; sectioned extraction ONLY if the post-prompt holdout re-measure still lags
- `scripts/news_ground.py` — deterministic duplicate-flag collapse + extended `--selftest`; `scripts/build.py` only as needed to apply the shared check on the build path
- `tests/news_live_test.py` — fixture replay extensions; goldens regenerated deterministically from the pinned `*.qwen.json` captures (no model call); NEW US-federal fixtures captured under the new prompt
- `docs/news-live.md`, `tests/smoke-checklist.md`, `CLAUDE.md` `## Current state` (in-place fact replacement)
- `.dev-wiki/tmp/ph40/**` measurement scratch (gitignored, local-only)
### Out of scope
- `news.html` or ANY client change; ALL `dist/**` artifacts (byte-identical); the corpus explorer, showcase, `derive_signals.py`; the entity-side prompt and `verify_entities`; `scripts/news_fetch.py` + `scripts/news_store.py`; verify-latency batching; new corpus sources.

## Approach
Measure-first; the measurement and its human checkpoint are complete. Remaining work: (1) reshape the red_flags contract in SYSTEM_PROMPT — a canonical mechanism-family checklist (~20 families including institutional control failure and misrepresentation-to-regulators), a scan-per-family coverage protocol, a one-flag-per-distinct-behaviour granularity contract with tightest-span instruction, register exemplars from the committed gate-passing records, and the [12,240] bounds fix; iterate on the calibration split only, then spend a pre-registered holdout evaluation with registry-based scoring (existence agreement + category agreement + span tightness + mechanism-coverage, with covQ and gate drop-rate as the precision guard). (2) Add the duplicate-flag collapse to the shared gate with an explicit total survivor rule and a category-aware key. (3) Only if holdout completeness/mechanism-coverage still lags: deterministic sectioning of >12K-char articles, same prompt per segment, merged through the dup-collapse. (4) Regate, grow the federal fixture corpus, document the method.

### Domain Research Questions
1. Does positional decay persist under the checklist prompt (re-run the decile miss-rate check post-prompt)? If yes, sectioning attacks the true cause; if no, the instruction gap was primary.
2. Which mechanism families does the local model confuse at category level (confusion pairs in category agreement) — should adjacent families be renamed or merged?
3. Do real one-quote-two-mechanisms cases occur in the captures? (Informs documentation and family naming only — the category-aware key and its fixture are mandated by the No-over-merge constraint regardless, as the cheap-safe default.)

## Constraints (CRITICAL)
- **Precision guard** — prevents checklist-induced grounded-but-wrong flags inflating recall: the post-prompt re-measure MUST report `cov_of_qwen` and gate drop-rate beside `cov_of_ref`; accept the prompt only if `cov_of_ref` rises while `cov_of_qwen` degrades ≤0.05 absolute and drop-rate stays ≤2× baseline.
- **Holdout discipline** — prevents holdout burn-through (the Phase-38 overfit trap): at most 2 holdout evaluations this phase, the count recorded in the measurement artifact; all iteration happens on calibration only.
- **Dedup determinism** — prevents nondeterministic golden regeneration: the collapse uses an explicit total survivor rule (earliest span start, then longest span, then first-in-list), pinned by a `--selftest` tie fixture.
- **No over-merge** — one verbatim quote CAN ground two distinct mechanisms: same-span flags with different categories are NOT collapsed; a fixture pins this case.
- **Committed-record integrity** — prevents silent ship-record mutation: the 4 committed news records must pass the extended gate; any failure is an adjudicated finding (fix-record vs grandfather), NEVER a threshold loosening; goldens regenerate from the pinned `*.qwen.json` with NO model invocation.
- **License containment** — prevents licensed-text leakage: committed files (prompt, fixtures, docs, this spec) carry NO quote, span, or slug from the 12 commercial stress articles (their identifiers live only in gitignored `.dev-wiki/tmp/ph40/` artifacts, including the `slugs.txt` pattern file the containment check greps from); prompt exemplars come from committed US-federal records (invented register strings allowed, quotes not).
- **Client/stream stability** — prevents breaking the frozen client and store: no new NDJSON stage names (the collapse runs inside the existing grounding stage); the DuckDB store schema is untouched.
- **Ship-path freeze** — `python3 scripts/build.py --check all` must return 5/5 byte-identical; the always-on "Illustrative data & outputs" badge stays; NO non-negotiable change.

## Success Vision
On articles never tuned on, the companion surfaces measurably more of the two-rater consensus flag surface — including institutional-failure mechanisms beside transactional ones — with stable precision, narrowed granularity variance (no per-anecdote flag storms, no duplicate spans), and translations that stay in the terse mechanism-named register. Every reported number is framed as inter-rater consensus, never accuracy. The deterministic gate gains exactly one structural rule, earned by measurement, behaving identically on the live and build paths. The replay corpus grows with federal articles captured under the new prompt. An engineer reading `docs/news-live.md` can reproduce the measurement end-to-end.

## Exit Criteria (machine-checkable)
- [ ] `python3 scripts/news_ground.py --selftest` — PASS with the dup-collapse, survivor-tie, and same-span-different-category fixtures
- [ ] `python3 tests/news_live_test.py` — PASS (replay green, goldens regenerated without any model call)
- [ ] `python3 scripts/build.py --check all` — 5/5 byte-identical
- [ ] `node tests/news-stream.test.mjs && node tests/corpus-explorer.test.mjs` — PASS
- [ ] `python3 scripts/serve_news.py --selftest && python3 scripts/news_fetch.py --selftest && python3 scripts/derive_signals.py --selftest` — PASS
- [ ] `bash -c "git grep -l -E -f .dev-wiki/tmp/ph40/slugs.txt -- ':!.dev-wiki' | wc -l"` — outputs 0 (no commercial-article slug in any committed file; the pattern file itself is gitignored so the check cannot leak what it checks)
- [ ] `python3 -c "import json; d=json.load(open('.dev-wiki/tmp/ph40/remeasure.json')); assert 1 <= d['holdout_evals'] <= 2; assert 'calibration_before' in d and 'calibration_after' in d; assert d['holdout']['cov_of_ref'] >= 0.40, d['holdout']"` — a holdout evaluation actually happened (within the 2-eval budget, calibration before/after recorded) and holdout completeness improves or holds vs the 0.40 baseline; "measurably more complete" beyond hold-the-line is enforced by the post-holdout human checkpoint, not this criterion

## Checkpoints
- After calibration iteration, BEFORE spending the holdout evaluation: report the calibration delta.
- After the holdout re-measure: report the full before/after table; the sectioning fallback fires or is skipped-with-reason here (the T2 checkpoint already delegated the trigger rule: holdout covR/mechanism-coverage still lagging → build it).
- If a committed record fails the extended gate: STOP and present the finding for adjudication.
- If holdout completeness degrades below the 0.40 baseline: roll the prompt back, report, abort per the phase abort rule.

## Assumptions
- The Qwen endpoint (127.0.0.1:8080, Qwen3.6-35B-A3B) stays available for re-capture. If false: the re-measure blocks — pause and ask rather than substituting a different model.
- The measured positional decay is attention/instruction-driven, not context truncation (largest article ≈7.5K tokens, far under the context limit). If false (the post-prompt decile check shows a hard tail cutoff): prompt-only is insufficient — sectioning becomes mandatory, report it.
- The blind reference extractions (`.dev-wiki/tmp/ph40/reference/`) are the FIXED comparison surface for before/after; both raters and the model read the identical standardized texts. If false (reference regenerated or texts changed mid-phase): the delta is invalid — freeze and re-pin before comparing.
- Prompt changes do not alter `build_record`/grounding logic, so existing goldens stay valid without re-capture. If false: regenerate goldens deterministically from the pinned `*.qwen.json`; if that also fails, STOP — the fixture contract is broken.
