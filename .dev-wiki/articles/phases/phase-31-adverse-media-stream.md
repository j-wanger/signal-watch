---
title: "Phase 31: M8 walking skeleton — the adverse-media / negative-news stream (a second atom stream)"
aliases: ["phase-31-adverse-media-stream"]
category: phases
tags: [m8, adverse-media, negative-news, entity-resolution, fuzzy-matching, screening, walking-skeleton, new-artifact]
parents: []
created: 2026-06-08
updated: 2026-06-08
source: plan
status: completed
delivery: accepted
scope: ["data/news/**", "news.html", "dist/news/index.html", "scripts/build.py", "tests/news-stream.test.mjs", "CLAUDE.md", "HANDOFF.md", "README.md", "tests/smoke-checklist.md"]
entry_criteria: "Phase 30 (data-source lens) delivered + accepted + committed to main (c997ace); the corpus is the primary demo. The user reframed Phase 31 to a scope EXPANSION: open a second stream over AML-relevant news — entity extraction + adverse-media red-flag identification + fuzzy-match against a client/counterparty table for exposure. Direction approved at the goal gate 2026-06-08: news source = SYNTHETIC illustrative (fictional entities); shape = walking skeleton as a new standalone artifact dist/news."
exit_criteria: "A self-contained offline dist/news/index.html running the arc (Read → fuzzy-match Screen → human-gate Disposition → exposure Close; illustrative badge always on; reduced-motion settles); build.py news clean + validate_news_data fails loud on an ungrounded entity; node tests/news-stream.test.mjs green; --check all ZERO DRIFT across all targets incl. news (showcase + corpus byte-identical); --selftest PASS; all 42 --check-derived clean; the frozen set byte-clean; NO non-negotiable change."
---

# Phase 31: M8 walking skeleton — the adverse-media / negative-news stream (a second atom stream)

## Objective

Open a SECOND atom stream in Signal Watch — adverse-media / negative-news screening — as a new standalone offline artifact `dist/news/` (built from a new `news.html` template, mirroring how `dist/corpus` was added). Prove ONE new muscle end-to-end, offline: unstructured news → grounded entity + red-flag extraction → fuzzy-match against a SYNTHETIC client/counterparty book → potential exposure → human disposition. The "compose with the transaction signal" payoff (an adverse-media atom composes with a transaction-signal atom → composite risk) is the M8 north star — NAMED here, scoped OUT of this phase.

## Why it extends the vision (not a bolt-on)

- The demo already opens on "the missed-monitoring / TD anxiety made visual" (HANDOFF §1.1). TD Bank's $3.09B 2024 penalty was a CDD/adverse-media failure — a negative-news stream is that anxiety made concrete.
- The thesis is unchanged — atoms compose; combination beats monolithic scenarios. An adverse-media hit is an ATOM. Entity X has a negative-news atom AND transaction-signal atoms → composite risk. This is a second atom stream (external/unstructured) composing with the existing internal/transactional one.
- aml-wiki grounding: ~80% of investigative intelligence is in UNSTRUCTURED text transaction systems can't touch ([[wiki:entity-resolution-and-network-analytics]]); entity-resolution fragmentation ("John D. Smith / J.D. Smith / J Smith") + the >90% false-positive wall are the core failure modes ([[wiki:adverse-media-screening]]) — exactly the fuzzy-match-then-human-disposition beat.

## Scope

- `data/news/**` — synthetic articles + grounded derived records + the seeded counterparty book (NEW).
- `news.html` + `dist/news/index.html` — the new standalone screening-arc template + built ship file (NEW).
- `scripts/build.py` — ADDITIVE: a new `news` build target + `validate_news_data` + register `news` in `--check`. Do NOT touch existing target code paths.
- `tests/news-stream.test.mjs` (NEW), `CLAUDE.md`, `HANDOFF.md`, `README.md`, `tests/smoke-checklist.md`.

## Architecture

Reuses the corpus discipline + adds ONE runtime piece:
- Build-time, committed: `data/news/articles/*.md` (synthetic, fictional) → `data/news/derived/*.json` (named `entities` + red-flag `flag` phrases, each QUOTE-GROUNDED in its article via normalize-substring, + a natural-AML `red_flag` translation) + `data/news/book.json` (synthetic counterparty table seeded with a near-match + an exact match + a false-positive trap + clean rows). Grounding reuses the corpus's `normalize`-substring DISCIPLINE, validated at the BUILD BOUNDARY (`validate_news_data` in build.py) — the grounding core `derive_signals.py` stays BYTE-FROZEN.
- Runtime (offline, single file, the new muscle): client-side fuzzy name match — normalize (strip titles/punct, token-sort) → Jaro-Winkler, REAL computed scores, thresholded. Pure JS, runs from `file://`. The only genuinely new code.
- Arc: Select article → Read (red-flags highlighted + entities tagged) → Screen (fuzzy-match vs book, ranked exposure, shows the near-match an exact-match screen would miss) → Disposition (human gate: keyboard-safe div-toggle confirm/dismiss; dismiss the trap) → Close (confirmed exposure counts).

## Exit Criteria

- [ ] A self-contained offline `dist/news/index.html` running the arc (Read → fuzzy-match Screen → human-gate Disposition → exposure Close); illustrative badge always on; reduced-motion settles on the final state.
- [ ] `python3 scripts/build.py news` clean (self-contained guard 0 forbidden tokens; `node --check` on the inlined engine); `validate_news_data` fails loud on an ungrounded entity.
- [ ] `node tests/news-stream.test.mjs` green (arc screens; fuzzy-match fires on the seeded near-match; the trap is dismissable; honest exposure counts; reduced-motion).
- [ ] `python3 scripts/build.py --check all` ZERO DRIFT across all targets incl. news (showcase + corpus byte-identical); `--selftest` PASS; all 42 `--check-derived` clean.

## Constraints

- The client/counterparty book MUST be synthetic (non-negotiable #4 — no real customer data, ever). Fictional news entities.
- Fuzzy scores are REAL computed similarity, displayed — never fabricated. Counts honest. The near-match + false-positive trap are DESIGNED INTO the synthetic data to teach the mechanism, not claimed as detection stats.
- Every derived entity name + red-flag `flag` quote-grounds in its synthetic article (normalize ⊂). `red_flag` is the show-both AML phrasing beside the grounded verbatim.
- The shippable artifact MUST run by opening one file, offline, no server, no runtime LLM/fetch, no keys (HANDOFF §4). Engine generic / config-driven — no hardcoded entities in engine code. The always-on badge stays on `dist/news`.
- FROZEN byte-clean: the six-act showcase (`index.html` + `config/**` + the 3 typology dists), the ENTIRE corpus (`corpus.html`, `dist/corpus`, all 4 source dirs, every `corpus-status.json`, all 42 derived records, `data/typology-map.json`, `data/capability-taxonomy.json`), and the grounding core `derive_signals.py`. `build.py` edited ADDITIVELY — existing dist outputs byte-identical.

## Assumptions

- Synthetic data means grounding is trivially satisfiable (I author both the article and the extraction), but the grounding DISCIPLINE still applies (derived strings are exact normalize-substrings of the article) — this proves the same gate carries to the news stream.
- A client-side Jaro-Winkler + token-sort matcher on a DESIGNED synthetic book produces a legible exposure beat (the near-match cleanly separates from the false-positive trap). If false: degrade to a static exposure table + flag it — never fabricate a score/threshold. (The weakest assumption; mitigated by designing the synthetic names to the chosen matcher.)

## Notes

Direction reframed by the user from the three offered Phase-31 lanes (third jurisdiction / dedup-gate guard / eyeball-the-demo) to a scope EXPANSION: a news/adverse-media stream. Feasibility grounded in-session: AUSTRAC was confirmed as the standout third jurisdiction (enumerated sector indicator guides, CC BY) but is NOT this phase; the aml-wiki carries the adverse-media + entity-resolution domain articles. Lite ceremony; 4 tasks (one L = T3, the runtime). The matcher direction is news-entity → book (the "we found exposure we weren't watching" beat the user asked for); the scorer is symmetric. North star (out of scope): the adverse-media atom composing with the transaction-signal atom.
