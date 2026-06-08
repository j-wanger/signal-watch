---
title: "Phase 31 — M8 walking skeleton: the adverse-media / negative-news stream"
date: 2026-06-08
phase: phase-31-adverse-media-stream
tags: [m8, adverse-media, negative-news, entity-resolution, fuzzy-matching, jaro-winkler, walking-skeleton, new-artifact]
---

# Phase 31 — M8 walking skeleton: the adverse-media / negative-news stream

Planned **and** implemented in one session (lite, 4 tasks, one L = T3). The user reframed the Phase-31 direction question — from the three offered lanes (a third jurisdiction / a corpus dedup-gate guard / eyeball-the-built-4-lens-demo) — to a **scope expansion**: open a SECOND atom stream over unstructured news. Delivered + accepted; committed to main.

## What shipped

A **third single-file ship artifact** `dist/news/index.html` (built from a new `news.html`, mirroring how `dist/corpus` was added) — a walking skeleton proving ONE new muscle end-to-end, offline: unstructured news → grounded entity + red-flag extraction → **fuzzy-match against a synthetic client/counterparty book** → potential exposure → human disposition.

- **T1** — 4 synthetic news articles (`data/news/articles/*.md`, fictional entities: trade-shell / mule-romance / sanctions-front / professional-ML) + per-article derived records (14 entities, 25 red-flags, each `normalize`-grounded via the real `derive_signals.normalize`) + `data/news/book.json` (12 synthetic rows). Seeded so the matcher demonstrates: exact (Aurelia ×2 articles, Greenfield), near (Volkoff 0.977, Dimitri 0.921, word-order Van Thanh 1.0, Bellwether 0.989), and a **common-name false-positive trap** (Andrei Petrov 1.0 — a different person).
- **T2** — `build.py news` target added ADDITIVELY (NEWS_* consts + `_news_normalize` [local, build.py never imports the authoring layer] + `validate_news_data` [build-boundary grounding gate, fail-loud] + `load_news`/`render_news`/`build_news`/`check_news`; wired into `news`/`all`/`--check`). Existing dist outputs byte-identical.
- **T3 (L)** — the screening arc in `news.html`: Select → Read (grounded red-flag + entity highlighting) → **Screen** (the new muscle — a client-side fuzzy matcher `normalize → token-sort → Jaro-Winkler`, REAL scores, thresholded at 0.85, surfacing the near-matches an exact-name screen misses) → **Disposition** (keyboard-safe `<button>` toggles, default-confirm; the analyst dismisses the trap) → Exposure (confirmed atoms; the compose-with-the-signal north star named). The matcher is a 1:1 JS port of a Python prototype run in T1.
- **T4** — `tests/news-stream.test.mjs` (dep-free vm + DOM-shim, both motion modes, 38 assertions) + docs (README dedicated M8 section + Run/Test/Status; CLAUDE.md How-to-run + state bullet + M8 milestone + header; HANDOFF.md §8 M8 entry; smoke-checklist news walk).

## Key decisions

- **Direction = a SECOND atom stream over news** (the user reframed past the three offered lanes). It extends — not bolts onto — the vision: the demo already opens on the "missed-monitoring / TD anxiety" (TD's 2024 penalty was a CDD/adverse-media failure); an adverse-media hit is an **atom** that composes with transaction signals; the aml-wiki backs the gap (~80% of intelligence is unstructured; entity-resolution fragmentation + the >90% FP wall = the fuzzy-match-then-human-disposition beat).
- **News source = SYNTHETIC illustrative (fictional entities)** over paraphrased-real / hybrid — cleanest, zero defamation/copyright surface, and it lets the near-match + false-positive trap be designed in so the beat lands honestly under the badge.
- **Shape = walking skeleton as a new standalone artifact** over folding into the corpus / building full-M8 now — keeps the showcase + corpus byte-frozen, proves only the new muscle (everything else is corpus-proven). The compose-with-the-transaction-signal payoff is the M8 north star, scoped OUT.
- **Grounding gate scope** — `validate_news_data` enforces faithfulness (the compliance-load-bearing invariant); the near-match/trap seeding is asserted by the harness (which runs the real matcher), not duplicated in the build gate (subtraction test).

## Verification

- Matcher de-risked BEFORE the UI: a Python prototype on the designed data showed clean separation at threshold 0.85 (near-matches surface, clean rows < 0.85, the trap surfaces at 1.0 for human disposition). The JS port matches to the thousandth (Volkoff 0.9766, Dmitri 0.9209). The phase's weakest assumption (the fuzzy beat must be legible) was thus retired early — the abort condition never fired.
- Gates: news harness **38/38** (both motion modes) · corpus harness **217/217** (no regression) · `build.py --check all` **5/5 ZERO DRIFT** · `--selftest` PASS · **42/42 `--check-derived`** clean (corpus intact) · `validate_news_data` fail-loud proven on a planted ungrounded entity · build deterministic (md5 stable).
- Frozen set byte-clean (git-confirmed): the showcase (index.html + config/** + 3 typology dists), the entire corpus (corpus.html, dist/corpus, all 4 source dirs, every corpus-status.json, all 42 derived records, data/typology-map.json, data/capability-taxonomy.json), and the grounding core derive_signals.py.

## Review Gate

A unified code reviewer (4 tasks + an L task → review dispatched) returned **SHIP**: Jaro-Winkler correctness confirmed against canonical pairs (MARTHA/MARHTA 0.9611, DWAYNE/DUANE 0.84, DIXON/DICKSONX 0.8133), escaping clean, non-negotiables clean. Four latent/cosmetic findings, all folded in before commit (exceeding the reviewer's "defer the MEDIUM"): (1) **MEDIUM** gate/highlighter normalization divergence → locked with a RAW-substring assertion in `validate_news_data` (the build now guarantees what the runtime highlighter relies on); (2) **LOW** raw markdown shown in the Read panel → added `_news_article_body` (strips the `# Title` + `*` emphasis at build time; grounding-safe); (3) **LOW** disposition keyed by book-row id → re-keyed per entity; (4) **NIT** unescaped tile count → `esc()`'d.

## Escape Hatches

None. Scope held (the change set == the declared scope; the compose-with-signal north star scoped out, not crept in). One in-scope scoping refinement: near-match/trap seeding lives in the harness, not the build gate.

## Health Delta

New harness `tests/news-stream.test.mjs` (+38 assertions, both motion modes). `build.py --check all` now guards 5 artifacts (was 4). No type/lint toolchain for this artifact (vanilla HTML/JS + stdlib Python, per project ethos). dist/news ~40.6 KB.

## Gate Compliance

`<!-- gate-log:phase-31 direction=approved delivery=accepted -->` — both boundary gates present.

## Soft Observations / Phase N+1 Candidates

- **The M8 north star: compose the adverse-media atom with the transaction-signal atom** (entity that tripped a signal AND has adverse media AND near-matches a counterparty = composite risk). The natural next M8 phase — the payoff this skeleton was built toward.
- **Corpus-wide exposure aggregate** — the Close screen is per-article; a book-wide "total adverse-media exposure across all screened news" view would be more compelling (and is honest union arithmetic, like the corpus synthesis).
- **A real / paraphrased-adjudicated news layer** — the hybrid option the user declined for the skeleton; real already-sanctioned (OFAC-SDN) entities could anchor a few cases for realism, under the existing compliance posture.
- **Streaming "agent reading" render for the news Read screen** — the corpus has the full-motion streaming read (Phase 28); the news Read screen is static. A parity polish.
- **(Carried) A third jurisdiction (AUSTRAC, CC BY)** — the confirmed corpus-scale frontier; and the corpus overlap/near-dup extraction-gate guard (exact-equality only) — both still open from Phase 30.

## Activation Quality

No `active-knowledge.md` in this phase (lite; cross-wiki knowledge was pulled inline from aml-wiki — adverse-media-screening + entity-resolution-and-network-analytics — and cited in the plan).
