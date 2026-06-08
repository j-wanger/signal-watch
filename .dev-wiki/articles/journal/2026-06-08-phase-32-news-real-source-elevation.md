---
title: "Phase 32 — News stream: real gov-enforcement adverse-media source + presentation elevation"
aliases: []
category: journal
tags: [m8, adverse-media, negative-news, real-source, doj, ofac, gov-enforcement, public-domain, streaming-render, entity-cards, scan-process, presentation, walking-skeleton]
parents: [phase-32-news-real-source-elevation]
created: 2026-06-08
updated: 2026-06-08
source: debrief
duration: ~1 session
---

# Phase 32 — News stream: real gov-enforcement adverse-media source + presentation elevation

Planned **and** implemented in one session (lite, 5 tasks, one L = T3). The user reviewed the BUILT Phase-31 `dist/news` and judged it "very low effort … a poorly staged slide show … you are repeating the same mistakes" — the exact staged-render failure called out on the corpus in Phase 27 (a RESULT, never a PROCESS). Reframed Phase 32 from the four offered forward lanes (the M8 composition north star / AUSTRAC third jurisdiction / deepen-the-news-stream / corpus overlap-dedup guard) to FIXING THE BUILT ARTIFACTS; "do both" → split by frozen set into Phase 32 = news (this) + Phase 33 = corpus (queued). Delivered → READY FOR COMPLETION; commit handled by the delivery flow.

## What Happened

Elevated the news stream on TWO fronts at once, the six-act showcase AND the entire corpus staying BYTE-FROZEN.

- **T1 — REAL-SOURCE SWITCH + grounded entity-attribute derivation + reseed the book.** Replaced the 4 SYNTHETIC fictional articles with 4 REAL US-federal gov-enforcement docs (verbatim-excerpted, each with a source + public-domain provenance line): DOJ Ravenell (attorney trust-account ML), DOJ Mullings (romance/BEC mule), DOJ Goltsev (Canadian export-control shells SH Brothers / SN Electronics), OFAC TGR Group (Russian shadow-finance). 14 entities (name + grounded location/age/profession), 29 red-flags + `red_flag` translations, all `normalize`-grounded. The 4 old synthetic articles + derived deleted. `data/news/book.json` reseeded SYNTHETIC against the REAL entities: 1 EXACT true-positive (Siam Expert ORG — a designated entity IS a counterparty, screening's canonical case) + 5 near-matches an exact-name screen misses (transliteration / suffix / word-order, 0.95–1.0) + a common-name FALSE-POSITIVE trap (George Rossi 1.0, a different person), every score VERIFIED with the real shipping matcher.
- **T2 — full corpus dossier theme + step rail + source attribution.** `news.html` brought to theme-token parity with the corpus (`:root` set + Newsreader / Archivo / JetBrains Mono + `--signal` #f6a623 + the dossier surface/panel/chip styles), a step rail labels the arc (Select › Read › Screen › Disposition › Exposure), per-doc source attribution rendered like the corpus.
- **T3 (L) — streaming "agent reading" Read + entity cards.** Ported the corpus `renderArticle` stream: the source streams in (caret + scroll-follow), each red-flag phrase + entity tag reveals only as the read reaches its position, entity CARDS (name / location / age / profession) + the typology + translate rows reveal alongside, both labels count UP from 0. Architecture = the corpus's Phase-28 convention: the template is the FINAL resting state (reduced-motion + the string-DOM harness settle on it), the stream a progressive ENHANCEMENT guarded by `insertAdjacentHTML`.
- **T4 — visible scan PROCESS on Screen (replace the jump-cut).** Each book row is swept + scored with the REAL Jaro-Winkler, ranked into exposure, a threshold line drawn, the near-match surfaced, the common-name trap flagged for the human. The runtime matcher is unchanged — only the presentation; NO fabricated number / fake progress bar.
- **T5 — harness + dist + docs + regate.** `tests/news-stream.test.mjs` REWRITTEN 38→**65** (the old one was tied to the deleted synthetic data): a reduced-motion final-state drive + a full-motion enriched-shim drive (`insertAdjacentHTML` + `classList` + drainable `setTimeout`) of the streaming Read + the scan PROCESS. dist rebuilt; CLAUDE.md / HANDOFF.md / README.md / smoke-checklist updated with the real-source compliance note.

## Decisions Made
- **Phase 32 = news-stream REAL-SOURCE switch + presentation elevation** — the user reframed away from the forward lanes to fixing the built artifacts; "do both" → Phase 32 news + Phase 33 corpus. (Lite — captured in _CURRENT_STATE Recent Decisions, no decision article.)
- **News source basis = REAL US-FEDERAL GOV-ENFORCEMENT (DOJ + OFAC), reproduced VERBATIM (excerpted) under 17 U.S.C. §105 public domain** — chosen over verbatim-commercial-news after PUSHBACK on the user's "use real online news, ignore copyright / non-commercial" (verbatim commercial news = copyright reproduction + defamation of real named persons + undercuts an AML-compliance demo's own credibility + needs a HANDOFF §4 non-negotiable edit). The clean path delivers REAL + verbatim + recognizable via gov-enforcement — the corpus's exact §105 basis (Phase 21). The COUNTERPARTY BOOK STAYS SYNTHETIC (#4 held) — REAL adverse-media entity × SYNTHETIC book. NOT a non-negotiable change (the existing US-federal verbatim basis applied to the news artifact). (Lite — _CURRENT_STATE Recent Decisions.)
- **SearXNG-backed authoring search/fetch = a FUTURE-PHASE CANDIDATE** (user request mid-session) — a self-hosted SearXNG meta-search + readability extraction for the BUILD-TIME authoring pipeline (more robust than WebFetch/curl, which hit gov-site bot-protection this phase); prototyped in the sibling nanaclaw project, not running here. Authoring-only, never in the ship artifact. (Recorded in _CURRENT_STATE Blockers as a `[CANDIDATE]`.)

## Problems Solved
- **DOJ bot-blocks WebFetch + curl (403).** Build-time acquisition routed via the Wayback Machine — a tooling workaround WITHIN T1's plan (WebFetch/curl → Wayback), authoring-only; the ship artifact stays offline/no-fetch. (A method discovery, NOT a formal escape hatch — no scope/plan deviation.)
- **`validate_news_data` only grounded names + flags, not the new rich attributes.** Extended ADDITIVELY (news path only) to quote-ground the entity attributes (location/age/profession) via the LOCAL `_news_normalize` — build.py STILL never imports the authoring layer; existing dist outputs byte-identical. Fail-loud proven on a planted ungrounded attribute.
- **The harness was tied to the deleted synthetic data** (it would have gone red on the real-entity switch). REWRITTEN to drive the real entities + both motion modes, +27 asserts.

## Artifacts Changed
- `data/news/articles/*.md` (4 REAL gov-enforcement docs; 4 old synthetic deleted) · `data/news/derived/*.json` (14 entities + grounded attributes + 29 red-flags + translations) · `data/news/book.json` (reseeded synthetic against the real entities)
- `news.html` + `dist/news/index.html` (full dossier theme + step rail + streaming Read + entity cards + visible scan process; ~40.6KB → ~70KB)
- `scripts/build.py` (`validate_news_data` extended for entity attributes — additive, news path only; existing targets byte-identical)
- `tests/news-stream.test.mjs` (rewritten, 38→65, both motion modes) · CLAUDE.md · HANDOFF.md · README.md · `tests/smoke-checklist.md`

## Verification
- Gates: news harness **65/65** (both motion modes; +27) · `build.py --check all` **5/5 ZERO DRIFT** (showcase + corpus byte-identical, news matches) · `--selftest` PASS · **42/42 `--check-derived`** clean (corpus intact) · `validate_news_data` fail-loud proven on a planted ungrounded attribute · build verified DETERMINISTIC (md5 stable across runs). dist/news ~40.6KB → ~70KB.
- Frozen set byte-clean (git-confirmed): the showcase (index.html + config/** + 3 typology dists), the ENTIRE corpus (corpus.html, dist/corpus, all 4 source dirs, every corpus-status.json, all 42 derived records, data/typology-map.json, data/capability-taxonomy.json), and the grounding core derive_signals.py. build.py edited ADDITIVELY. NO non-negotiable change.

## Escape Hatches
None. The Wayback-Machine acquisition was a tooling workaround within T1's plan (WebFetch/curl → Wayback), not a scope/plan deviation. No scope creep (the M8 composition north star NAMED + scoped OUT).

## Related
- [[phase-32-news-real-source-elevation|Phase 32: News stream — real gov-enforcement adverse-media source + presentation elevation]] — parent phase
- [[2026-06-08-phase-31-adverse-media-stream|Phase 31]] — the walking skeleton this elevates

## Soft Observations / Phase N+1 Candidates
- **The M8 NORTH STAR — compose the adverse-media atom with the transaction-signal atom** (composite risk) — the natural next phase; needs a synthetic transaction-signal layer on the book entities + an HONEST co-occurrence representation (no fabricated composite score; the Ph18/Ph24 honesty gate).
- **Phase 33 (QUEUED) — corpus completeness + typology re-segmentation** (missing FinCEN latest advisory + FINTRAC Obligations/Guidance section; TBML as its own typology), workflow-driven.
- **SearXNG-backed authoring search/fetch** — a future candidate; gov-site bot-protection drove the Wayback workaround this phase.
- **The book's near-match rows are deliberate VARIANTS of real charged persons' names** (inherent to demonstrating fuzzy matching against real adverse media; the book is synthetic/illustrative and the EXACT true-positive is an OFAC-designated ORG — screening's canonical case — not a person). A consideration if fully-synthetic near-match names are preferred.
- **A Canadian enforcement doc** (Crown-copyright non-commercial — the FINTRAC/Phase-22 basis) for the Canadian-bank audience, or 1–2 more US docs.

### Retro Check
Not triggered — 23 phases at `status: completed` (Phase 31 the last; Phase 32 not yet flipped); 23 % 5 ≠ 0.

## Activation Quality
No `active-knowledge.md` in this phase (lite; the adverse-media / entity-resolution domain grounding carried from Phase 31's aml-wiki pull). Hit rate n/a.
