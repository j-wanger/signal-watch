<!-- nana:approved 2026-06-09 -->
# Spec: Phase 41 — Entity-resolution schema enrichment (live news)

## Objective
Enrich the live news companion's entity extraction into resolution-grade identity records — grounded identifying attributes, preserved aliases/name variations, and structured inter-entity relationships with a main-subject designation — persisted in an anchor-based local store that accumulates identities across scans, with alias-aware screening and zero change to any offline ship artifact.

## Context
The companion server (`scripts/serve_news.py`) extracts entities + red flags from a pasted or URL-acquired article via a local Qwen model (llama-cpp, 127.0.0.1:8080); the deterministic gate (`scripts/news_ground.py`, shared with `scripts/build.py`'s news validator) drops anything not verbatim-grounded. Today's entity schema is flat `{name, type, location, age, profession, context}`; name variants/subset names and @-handles are DROPPED as noise by `screen_entities`; relationships exist only as free-text `context` prose; persistence (`scripts/news_store.py`, local gitignored DuckDB) is per-scan rows; the watchlist/screen step matches names only (normalize → token-sort → Jaro-Winkler, 0.85). The Phase 41 direction gate (2026-06-09, `.dev-wiki/assumption-ledger.md` Phase 41 block) confirmed: the system's future input includes PRIVATE investigation notes carrying real client/account identifiers, so the schema is designed for that domain — and private data is confined to the local layer (local store + local 127.0.0.1 model; never committed, never fixture-promoted — fixtures stay US-federal public-domain only — never in the shipped offline file). Decisions D1–D4 (`.dev-wiki/_CURRENT_STATE.md` Recent Decisions; `.dev-wiki/articles/decisions/phase-41-entity-resolution-schema.md`): two-layer data model — nested per-scan extraction JSON (grounded-or-stripped) + DuckDB ANCHOR normalization (entity anchor table with source_type, ONE monolithic property association table with kind/value/detail/evidence/provenance/grounded + a RESERVED never-model-populated confidence column, relationship edge table); alias DROPs invert to FOLDs; exact-normalized-name cross-scan accumulation now, fuzzy merge adjudication deferred; relation labels from a small closed vocab, vocab-checked never correctness-checked (the C/D-code honest split).

## Scope
### In scope
- `scripts/serve_news.py` — EXTRACT_SCHEMA + SYSTEM_PROMPT enrichment (aliases, properties, relationships, main subject); watchlist route returns aliases + source_type provenance
- `scripts/news_ground.py` — gate extensions: alias grounding, property grounded-or-stripped (RAW spans), relationship evidence grounding + referential integrity + label vocab, main-subject shape, alias-fold inversion; `scripts/build.py` only as the shared-gate consequence on the build path
- `scripts/news_store.py` — anchor redesign: scans.source_type, anchor table, monolithic property association table, relationship edge table, exact-normalized-name accumulation, parquet export
- `news.html` — LIVE region only: source-type selector, property/alias entity cards, relationship view, alias-aware screening
- `tests/news_live_test.py`, `tests/news-stream.test.mjs` assertions, `tests/fixtures/news-live/**` (NEW `.ph41` US-federal captures; goldens regenerated deterministically)
- `docs/news-live.md`, `tests/smoke-checklist.md`, `CLAUDE.md` `## Current state` (in-place fact replacement)
### Out of scope
- Fuzzy cross-scan MERGE adjudication (deferred — exact-normalized-name accumulation only)
- The offline demo artifacts: ALL `dist/**` byte-identical; the 4 committed derived records + `data/news/book.json` unchanged; corpus explorer, showcase, `derive_signals.py`, `scripts/news_fetch.py` untouched
- Model-emitted confidence scores (column reserved NULL; population needs a future measured basis)
- Offline-demo enrichment (a later demo-polish phase); FINTRAC /intel/, third jurisdiction, CLAUDE.md trim (carried candidates)

## Approach
Extend the extraction contract so the model proposes richer nested records — per-entity `aliases[]` and `properties[]` (`{kind, value}` from a closed kind vocab: address, phone, email, client_number, account_number, dob, id_registration, wallet, domain, + existing location/age/profession), record-level `relationships[]` (`{from, to, label, evidence}`, closed ~8-term label vocab) and a main-subject designation — and extend the SHARED deterministic gate to dispose: every alias and property value grounds as a RAW verbatim span; every relationship needs a grounded evidence quote + referential integrity to extracted entities + a vocab-valid label. The frozen relation vocab's single authority is a module-level constant in `news_ground.py` (the shared gate — prompt and store reference it, never redefine it), frozen at the post-measurement DRQ3 decision and recorded in the decision article. Invert the alias-noise rules into folds (subset names/monikers attach to the fuller entity's alias list). Normalize persistence to the anchor design with non-destructive accumulation (every property row keeps scan provenance; anchors are splittable). Make screening alias-aware with class-aware match rules. Render the enrichment in the companion live region only. The implementer determines: prompt architecture (one extraction call vs a second pass for properties/relationships), exact table/column design within the decided anchor shape, matching corroboration rules, and UI layout — guided by the Domain Research Questions.

### Domain Research Questions
1. Can the local Qwen reliably emit the full nested schema in ONE JSON-schema-constrained call without degrading the measured Phase-40 red-flag quality, or does a second extraction pass (same text, properties/relationships only) protect the tuned surface better? Compare on the committed federal articles before committing.
2. What alias-class corroboration rules keep screening useful — when should a single-token alias ("Smith") match (exact only? only with a corroborating grounded attribute?), and do @-handles ever deserve more than exact-normalized matching? The synthetic book's seeded common-name trap is the test bed.
3. Does the ~8-term relation vocab actually cover federal enforcement articles, or does an honest `other`+evidence bucket dominate (a sign the vocab needs renaming/merging — measure label distribution on the new captures before freezing the vocab)?

## Constraints (CRITICAL)
- **Raw-span grounding for identifiers** — prevents the gate silently dropping every phone/account/wallet: identifiers appear in display form ("(212) 555-1234", line-wrapped wallets); the gate grounds the RAW span ONLY; any canonicalization is a deterministic POST-gate step stored beside the raw span, never gated. Gate selftests must include punctuation-varied and line-wrapped identifier fixtures.
- **Non-destructive accumulation** — prevents identity poisoning via wrong-merge: every property row carries scan provenance so any anchor splits back into its constituent scans; contradictory values for the same kind (two DOBs, two addresses) are BOTH kept and surfaced as a conflict for the analyst — never auto-resolved, no last-write-wins. Same-name-different-person collisions are an accepted, documented limitation of exact-name anchoring (fuzzy merge + split UI deferred).
- **No fabricated derivations** — prevents invented numbers: "45-year-old" is an age-at-publication, never converted to a DOB; the confidence column stays NULL (model-emitted confidence is a fabricated-shaped number); zero-attribute entities are valid records — the prompt must not pressure the model to fill slots.
- **Privacy boundary enforced by CHECK, not convention** — prevents an irreversible private-identifier leak into git: `tests/news_live_test.py` gains a fixture-provenance allowlist check (every fixture's article id must be a committed `data/news/articles/*.md` US-federal id); captured scans of private/commercial input stay under gitignored paths (`data/news/.live/`, `.dev-wiki/tmp/`).
- **Alias-class-aware screening** — prevents a false-positive flood at the 0.85 fuzzy threshold: single-token aliases and handles never enter generic fuzzy matching (exact-normalized or corroborated only); the seeded common-name trap must remain dismissable, asserted in the node harness BEFORE ship.
- **Honest main subject + bounded relationships** — prevents forced-pick distortion and quadratic blowup on mass-defendant articles: main subject allows none/multiple; relationships only between extracted subject entities, each requiring its own verbatim evidence span; no transitive closure, no pairwise enumeration pressure.
- **Prompt-regression gate** — prevents tripling the prompt's job from silently degrading the measured Phase-40 red-flag quality: capture the new `.ph41` federal fixtures and compare the red-flag layer against the `.ph40` captures (flag counts, dup-collapse survivors, grounded-drop rate); a regression is an adjudicated FINDING (rollback or user ruling), never silently accepted.
- **Frozen-surface discipline** — prevents ship drift: all client wiring inside `/*LIVE_START*/…/*LIVE_END*/`; gate extensions ADDITIVE (the 4 committed records re-validate unchanged — new fields optional); new extraction fields default-empty so the 10 pinned captures replay to green goldens WITHOUT re-capture; `build.py --check all` 5/5 byte-identical is the acceptance check.

## Success Vision
An analyst pastes an investigation note or fetches an enforcement article and gets back a subject-centric identity picture: the main subject named, each related party connected by an evidenced relationship, every identifying attribute (down to client/account numbers) shown with its verbatim source span — nothing displayed that isn't grounded. Scanning a second document about the same entity visibly enriches the same anchor (new properties accumulate with provenance; conflicts surface honestly). Screening catches an alias the old name-only matcher would have missed, while the common-name trap still gets dismissed at the human gate. The offline demo file is byte-identical to before; nothing private can reach git even by habit, because a check — not a convention — blocks it.

## Exit Criteria (machine-checkable)
- [ ] `python3 scripts/serve_news.py --selftest`
- [ ] `python3 scripts/news_ground.py --selftest` (the selftest must ASSERT ≥3 identifier-grounding cases — punctuation-varied + line-wrapped — and ≥2 alias-fold inversion cases, so an unextended selftest fails, not skips)
- [ ] `.venv/bin/python scripts/news_store.py --selftest` (incl. two scans same entity → one anchor with accumulated provenance; conflicting-value rows both kept)
- [ ] `python3 tests/news_live_test.py` (10 old goldens green WITHOUT re-capture; NEW `.ph41` fixtures; fixture-provenance allowlist check)
- [ ] `git diff --exit-code -- 'tests/fixtures/news-live/*.qwen.json' 'tests/fixtures/news-live/*.md'` (the pinned pre-Phase-41 CAPTURES + article texts byte-unchanged — re-capture is machine-detected, not promised; `*.golden.json` may change ONLY by deterministic regeneration from these pinned captures, e.g. the alias-fold inversion relocating a subset name from `dropped` into the parent's aliases)
- [ ] `node tests/news-stream.test.mjs` (alias-aware screen; common-name trap dismissable; offline strip assertion)
- [ ] `node tests/corpus-explorer.test.mjs` (frozen)
- [ ] `python3 scripts/derive_signals.py --selftest` (frozen)
- [ ] `python3 scripts/news_fetch.py --selftest` (frozen)
- [ ] `python3 scripts/build.py --check all` (5/5 dists byte-identical)

## Checkpoints
- After T2 (gate extensions): report the raw-span grounding design + the 4 committed records' validation result before building the store on top.
- After T3 (store redesign): report the anchor/accumulation selftest evidence before wiring watchlist/UI.
- After capturing the first `.ph41` federal fixture: report the red-flag-layer comparison vs the `.ph40` capture (the prompt-regression gate) before capturing the rest.
- If ANY committed record fails the extended gate: STOP — adjudicated finding, never a silent loosening.
- If the red-flag layer regresses under the enriched prompt: STOP — present the measurement; options are two-pass extraction or rollback (user ruling).

## Assumptions
- The 10 pinned `*.qwen.json` captures replay green once new fields default-empty in `build_record`. If false: fix the defaults — NEVER re-capture old fixtures.
- The local Qwen emits the richer nested schema reliably under JSON-schema constraint. If false: split into a two-pass extraction (entities+flags first, properties+relationships second) — DRQ1 decides early.
- The local DuckDB store can be recreated from scratch (schema redesign, no migration obligation — store is local-only scratch). If false (existing scans must survive): write a one-shot migration in `news_store.py`.
- The llama-cpp endpoint (127.0.0.1:8080) is available for `.ph41` fixture capture. If false: complete the deterministic work, mark fixture capture blocked, ask the user.
- `node` + the `.venv` (markitdown, duckdb) remain available as today. If false: the affected selftest is reported skipped, never silently passed.
