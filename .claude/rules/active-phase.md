# Active Phase Context

Phase: 31 — M8 walking skeleton: the adverse-media / negative-news stream. A SECOND atom stream (external/unstructured) added as a NEW STANDALONE offline artifact `dist/news/` (built from a new `news.html` template, mirroring how `dist/corpus` was added). The showcase and corpus stay byte-frozen. ACTIVE — planned 2026-06-08, direction approved at the goal gate; no task started yet.

Objective: prove ONE new muscle end-to-end, offline — unstructured news → grounded entity + red-flag extraction → fuzzy-match against a SYNTHETIC client/counterparty book → potential exposure → human disposition. Thinnest slice; the "compose with the transaction signal" payoff is the M8 north star, scoped OUT of this phase. The new beat is the fuzzy entity-match → exposure + human gate (article-reading / highlighting / build-time grounding are corpus-proven — don't let the skeleton be just another article reader).

User decisions at the goal gate (2026-06-08): (1) news source = SYNTHETIC illustrative, fictional entities (cleanest, controllable, zero defamation/copyright surface; lets the near-match + false-positive trap be designed in so the beat lands honestly under the badge). (2) shape = WALKING SKELETON as a new standalone artifact `dist/news` (not folded into the corpus; not full-M8-now).

Architecture (reuses the corpus discipline, adds one new runtime piece):
- Build-time, committed: `data/news/articles/*.md` (synthetic, fictional) → `data/news/derived/*.json` (entities + red-flags, each QUOTE-GROUNDED in its article via normalize-substring, + a natural-AML `red_flag` translation) + `data/news/book.json` (synthetic counterparty table seeded with ≥1 deliberate near-match + ≥1 exact match + ≥1 false-positive trap + clean rows). Grounding reuses the corpus's `normalize`-substring DISCIPLINE, validated at the BUILD BOUNDARY in `build.py` (new `validate_news_data`) — the grounding core `derive_signals.py` stays BYTE-FROZEN (the news validator does NOT live in it).
- Runtime (offline, single file, the new muscle): client-side fuzzy name match — normalize (strip titles/punct, token-sort) → Jaro-Winkler, REAL computed scores, thresholded. Pure JS, runs from `file://`. The only genuinely new code.
- Arc (`news.html` → `dist/news/`): Select article → Read (red-flags highlighted + entities tagged) → Screen (fuzzy-match vs book, ranked exposure, shows the near-match an exact-match screen would miss) → Disposition (human gate: keyboard-safe div-toggle confirm/dismiss; dismiss the trap) → Close (confirmed exposure counts; name the atoms/composition north star). Illustrative badge always on.

Scope (UNFREEZE — additive only): `data/news/**`, `news.html`, `dist/news/index.html`, `scripts/build.py` (ADDITIVE — a new `news` build target + `validate_news_data` + register `news` in `--check`; do NOT touch existing target code paths), `tests/news-stream.test.mjs`, `CLAUDE.md`, `HANDOFF.md`, `README.md`, `tests/smoke-checklist.md`.

FROZEN byte-clean: the six-act showcase (`index.html` + `config/**` + the 3 typology dists), the ENTIRE corpus (`corpus.html`, `dist/corpus/index.html`, all 4 source dirs `data/{fincen,fincen-alerts,ofac,fintrac}/**`, every `corpus-status.json`, all 42 derived records, `data/typology-map.json`, `data/capability-taxonomy.json`), and the grounding core `scripts/derive_signals.py`. `build.py` is edited ADDITIVELY — the existing dist outputs (3 typology + corpus) MUST stay byte-identical (`--check all` zero drift on them).

Key constraints (honesty / non-negotiables):
- The client/counterparty book MUST be synthetic (non-negotiable #4 — no real customer data, ever). Fictional news entities.
- Fuzzy scores are REAL computed similarity, displayed — never fabricated. Counts (entities, hits, exposure) are honest. The near-match + false-positive trap are DESIGNED INTO the synthetic data to teach the mechanism, not claimed as detection stats.
- Every derived entity name + red-flag `flag` must quote-ground in its synthetic article (normalize ⊂). The `red_flag` translation is the show-both AML phrasing beside the grounded verbatim.
- The shippable artifact MUST run by opening one file, offline, no server, no runtime LLM/fetch, no keys (HANDOFF §4). Engine generic / config-driven — no hardcoded entities in engine code. The always-on "Illustrative data & outputs" badge stays on `dist/news`.

Exit criteria:
- A self-contained offline `dist/news/index.html` running the arc: Read → fuzzy-match Screen → human-gate Disposition → exposure Close; illustrative badge always on; reduced-motion settles on the final state.
- `python3 scripts/build.py news` clean (self-contained guard 0 forbidden tokens; `node --check` on the inlined engine); `validate_news_data` fails loud on an ungrounded entity.
- `node tests/news-stream.test.mjs` green (arc screens; fuzzy-match fires on the seeded near-match; the trap is dismissable; honest exposure counts; reduced-motion).
- `python3 scripts/build.py --check all` reports ZERO DRIFT across all targets INCLUDING news (showcase + corpus byte-identical); `--selftest` PASS; all 42 `--check-derived` clean (corpus intact).
- Frozen set byte-clean; NO non-negotiable change.

Abort: if the fuzzy beat can't be made legible even with designed synthetic data (the near-match doesn't cleanly separate from the false-positive trap), DEGRADE to a static exposure table and flag it — never fabricate a score/threshold to force the beat. If any aggregate would need a fabricated number, cut it. If `build.py` can't add the `news` target without disturbing existing-target byte-output, surface it before proceeding. Blocked >3 attempts on a task → ask the user: skip or abort.

Gates:
- [x] Direction confirmed by user (synthetic source + walking-skeleton standalone artifact; approach approved 2026-06-08)
- [x] Delivery accepted (post-implementation report 2026-06-08 — news 38/38 + corpus 217/217, --check all 5/5 zero drift, reviewer SHIP, committed + pushed to main)
