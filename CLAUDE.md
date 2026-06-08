# Signal Watch — AML Vision Demo

## What this project is
A presenter-driven, offline, browser-based VISION PROTOTYPE for AML stakeholder buy-in.
Not a real detection system — a scripted dramatization of the signal/atom loop.
See HANDOFF.md for full context; it dramatizes POC 5 → POC 1 → POC 3 of the
AML transformation framework. Keep vocabulary consistent with it
(atoms, composition, promotion gate, coverage index, etc.).

## Non-negotiables (do not violate — HANDOFF §4)
- The shippable artifact MUST run by opening one file, offline, no server.
- Do NOT split into ES modules / fetch()-loaded config in the ship target (file:// breaks).
  Develop modular if useful; the build inlines everything into a single self-contained file.
- Content is config-driven (the engine reads from data arrays / typology configs).
  The engine is generic — no hardcoded typology copy in engine code.
- Keep the six-act arc and the two wow beats (two human gates + combination-lift reveal)
  unless explicitly asked to change them.
- Keep the "Illustrative data & outputs" badge always visible. Never present synthetic
  numbers as real.
- NO real customer/transaction data, ever. Advisory text must be public-source and PARAPHRASED by
  default (e.g. the FINTRAC Jan-2025 Operational Alert behind the fentanyl SHOWCASE is paraphrased).
  TWO verbatim exceptions, each kept visually separate from the always-on "Illustrative data & outputs"
  badge: (1) US FEDERAL GOVERNMENT advisories are public domain (17 USC §105 — works of the US government
  carry no copyright) and may be reproduced VERBATIM with attribution (see Act 1's SOURCE DOCUMENT panel,
  EFE FIN-2022-A002). This US-federal exception covers FinCEN AND OFAC (both US Treasury — Phase 21 added
  OFAC as corpus source #3) and other US federal agencies. (2) FINTRAC (Phase 22, corpus source #4 — the
  FIRST cross-jurisdiction source) is Canadian Crown copyright — NOT public domain — but its publications
  MAY be reproduced VERBATIM for NON-COMMERCIAL use WITH FINTRAC's required attribution (© His Majesty the
  King in Right of Canada + complete title + "a copy of the version available at <URL>"), per FINTRAC's
  Terms & Conditions: a reproduction LICENCE, distinct from the US 17 USC §105 no-copyright basis. NOT
  commercial redistribution (needs FINTRAC's written permission). The verbatim relaxation is US-FEDERAL +
  FINTRAC ONLY — every OTHER non-US / non-FINTRAC / non-government source still paraphrases (the fentanyl
  showcase still paraphrases its FINTRAC OA). Phase 28 (the user's compliance call): in the corpus explorer the
  per-doc Source LABEL carries the document title only; the FINTRAC Crown-copyright attribution (© His Majesty…
  + complete title + source URL) renders in the PAGE FOOTER for the FINTRAC doc on screen (empty for US
  public-domain docs) — verbatim-with-attribution HELD, the attribution relocated, not removed.
- Live mode is optional, isolated, off by default, always has a scripted fallback.
  Never put keys/tokens in the frontend. Copilot is NOT a web backend (HANDOFF §4.5).

## Current state (M8 — adverse-media / negative-news stream: Phase 31 walking skeleton + Phase 32 real-source & presentation elevation; M7 corpus-backed derivation multi-source complete)
- Generic engine: `index.html` (vanilla HTML/CSS/JS) with a single `__CONFIG__` injection point.
  Typology-agnostic — adding a typology is one JSON file, no engine edits. Presenter controls (M3):
  keyboard nav (←/→/Space/Esc/↺), reset, `prefers-reduced-motion`.
- Content: `config/typologies/*.json` (fentanyl, trade-based, elder-financial-exploitation) against
  `config/schema.md`.
- Build: `scripts/build.py` validates a config against the schema (fails loud), resolves
  `text_file`→inline, and inlines everything → `dist/<id>/index.html`. Baseline preserved in `archive/`.
- Authoring pipeline (M6, build-time ONLY — never in the ship file): `crawl_fincen.py` (Phase 10:
  discover the FinCEN advisories listing → committed manifest `data/fincen/index.json`; pure
  `parse_index` + offline `--selftest`, thin live `--fetch`) → `acquire_fincen.py` (read the manifest,
  resolve each advisory's PDF from its detail page; EFE kept as a zero-hop direct-PDF override) →
  `pdf_to_md.py` (markitdown PDF→markdown, persisted to `data/fincen/<id>.md` as the source of truth)
  → `derive_signals.py` (the deterministic GATE — Phase 16 inverted the boundary, Phase 17 deleted the
  old extractor: the LLM backend reads `<id>.md` and EXTRACTS the red flags + per-indicator judgment into
  `data/fincen/derived/<id>.json`, and `--check-derived` DISPOSES — see the corpus-derivation bullet).
  `derive_signals.py` is now stdlib-only (no `anthropic` dep); only `markitdown` (convert) lives in a
  gitignored uv `.venv` — NO authoring tool is imported by the engine or `build.py`, and the ship artifact
  never fetches or calls an LLM. The elder typology renders the FULL verbatim EFE advisory (FinCEN
  FIN-2022-A002, public domain) in Act 1 via the `advisory_full` field.
- Corpus derivation (Phase 12+, M7 — backend for an expanded, singular corpus-backed demo where the
  user picks one of 14 advisories): the full 14-advisory FinCEN corpus is committed as md
  (`data/fincen/*.md`). The LLM backend (a live model session, no key) reads an advisory and EXTRACTS its
  red flags + per-indicator judgment (status, data, a build recommendation, build logic for the BUILD_NOW
  gaps) into `data/fincen/derived/<id>.json`; `--check-derived` DISPOSES — `build_rec` must follow the
  cover×data matrix (`build_rec_category`), every verbatim `flag` must QUOTE-GROUND in the source md
  (`normalize(flag)` ⊂ `normalize(md)`, inside the red-flag region `rf_region`), BUILD_NOW must carry a
  full definition. `--corpus` / `--corpus-status` are a cheap rf_region triage HINT (`derivable` = a
  red-flag region exists, false only for the 2 FATF advisories; + a coarse block count via `_rf_triage`) —
  never the derivation authority. The LLM proposes (extraction included); the deterministic gate + the two
  human gates dispose. Derived records are an LLM-derived + checked corpus dataset, NOT ship typology
  configs (the 3 hand-curated typologies stay the showcase).
- Corpus explorer (Phase 13, M7 — the demo scope expansion): a SECOND, separate ship artifact
  `dist/corpus/index.html`, built from a standalone template `corpus.html` (owns its own copy of the
  dossier theme — the six-act engine `index.html` is left byte-untouched). A staged 6-screen ARC
  (Phase 18 gave the explorer the showcase's two missing beats — a human gate + a close-the-loop payoff;
  Phase 25 added the article-processing beat):
  SELECT one of the 46 public publications (14 FinCEN advisories + 19 FinCEN alerts + 3 OFAC + 10 FINTRAC —
  Phase 20/21/22/23; honest `doc_type` chip Advisory/Alert/OFAC/FINTRAC + status chips: derived /
  clean-or-low-not-yet-derived / non-derivable) → READ ADVISORY (Phase 25 — the FULL source document with each
  verbatim red-flag phrase highlighted, then translated into a natural-AML `red_flag` shown BESIDE the verbatim
  quote) → COVERAGE gauge → BUILD RECOMMENDATIONS **= the human GATE** (per-indicator cover×data
  build_rec, sorted BUILD_NOW-first, each row src_line-traceable; the BUILD_NOW rows are SELECTABLE
  div-toggles [NOT `<input>`, so Space/arrow nav still works] — default all-selected, "agent proposes,
  human disposes"; non-BUILD_NOW rows read-only) → SIGNAL spec for the PICKED BUILD_NOW gaps → CLOSE THE
  LOOP (the coverage index animates before→after as the picked gaps flip gap→covered — same model as the
  showcase's Act 6; 0-picked / 0-BUILD_NOW holds coverage flat with a note, never a fake rise). The payoff
  is COVERAGE, NOT precision combination-lift: the derived records carry no precision/lift numbers, so
  porting the showcase lift beat would FABRICATE ~12 per-advisory stats — rejected (the "never present
  synthetic numbers as real" non-negotiable); coverage is already disclosed illustrative. Phase 18 unfroze
  ONLY `corpus.html` (the arc reuses existing data fields — no schema/data/`build.py` change). Built by
  `build.py corpus` (or `all`; guarded by `--check corpus`), which reads two COMMITTED data artifacts —
  the extraction manifest `data/fincen/corpus-status.json` (emitted by `derive_signals.py
  --corpus-status`) + the derived records `data/fincen/derived/*.json` — merges them by id, and
  validates the derived shape at the build boundary (build_rec ∈ matrix vocabulary; BUILD_NOW ⇒ full
  build_logic). build.py NEVER imports the authoring layer; ships with **12/14 derived** (Phase 17 added
  health-care fin-2026-a001 [glued, 24 flags] + COVID health-insurance fin-2021-a001 + Iran-terror
  fin-2024-a001 + ISIS fin-2025-a001 + the EFE corpus record fin-2022-a002 to the Phase-16 seven). Only
  the 2 FATF jurisdiction advisories (fin-2020-a009, fin-2021-a003 — no enumerated red-flag list) stay
  non-derivable. The glued advisories (ransomware fin-2021-a004, health-care fin-2026-a001) were
  unreachable by the deleted structural extractor yet ship derived via the inverted loop (the LLM reads
  them like a human, the gate grounds each verbatim flag). No fabricated lift/stats; the always-on badge
  stays, with the verbatim public-domain source attribution kept visually distinct from it.
- Multi-source corpus (Phase 20, M7 — scale beyond advisories): the corpus explorer is now MULTI-SOURCE.
  A thin `CORPUS_SOURCES` registry in `build.py` (source-id → {status, derived dir, doc_type}) lets
  `render_corpus` merge each FinCEN publication TYPE's committed `corpus-status.json` + `derived/*.json` by
  id into one `__CORPUS__`; the SELECT menu lists all of them with an honest `doc_type` chip (Advisory /
  Alert). FinCEN ALERTS are source #2 (`data/fincen-alerts/` — 19 alert md, 17 derived): acquired by
  `crawl_fincen.py --alerts` (the alerts hub lists each PDF DIRECTLY → zero-hop download) →
  `acquire_fincen.py`/`pdf_to_md.py --source data/fincen-alerts` → derived via the SAME inverted loop +
  gate. Phase 20 stayed STILL FinCEN, STILL verbatim, STILL public-domain (17 U.S.C. 105) — NO
  non-negotiable changed by it; the quote-grounding gate (`check_record`/`rf_region`/`normalize`) is
  source-agnostic. `data/fincen/` (the advisories source) stays byte-frozen — multi-source via the MERGE,
  not a migration. (Phase 21 then added OFAC as source #3 + Phase 22 added FINTRAC as source #4 + Phase 23
  DEEPENED FINTRAC 3→10 — see the next bullets; the corpus now ships **42 derived across 46 publications** =
  12 advisories + 17 alerts + 3 OFAC + 10 FINTRAC, only the 2 FATF advisories + 2 alerts with no enumerated
  red-flag list non-derivable.)
- OFAC as source #3 (Phase 21, M7 — cross-agency, US-federal): OFAC (US Treasury) added as the THIRD
  corpus source (`data/ofac/`, doc_type "OFAC"; 3 derived). Because 17 U.S.C. §105 covers ALL US federal
  works, the verbatim non-negotiable was extended FinCEN-only → US-federal (FinCEN + OFAC + US federal;
  at Phase 21 FINTRAC + non-US still paraphrased — Phase 22 then extended verbatim to FINTRAC too under a
  non-commercial licence, see next bullet). OFAC mostly uses sanctions-RISK vocab ("Risk Indicators" / "Deceptive
  Practices") rather than FinCEN's "red flags", so `rf_region`'s anchors were WIDENED (`_RF_HEADER_OFAC` +
  `_RF_INTRO_OFAC`), REGRESSION-GATED: every FinCEN md's rf_region stays byte-unchanged, all 29 FinCEN
  records + `--selftest` still clean (the new vocab is ~inert for FinCEN); grounding/`normalize` untouched.
  Acquisition is HAND-CURATED (OFAC's site is a JS SPA — no static crawl; `crawl_fincen.py` stays
  FinCEN-only): `data/ofac/index.json` lists /media/<id>/download PDFs, acquired via `acquire_fincen.py
  --source data/ofac`. OFAC content is sanctions/vessel-oriented → records are honestly enrichment/
  SOURCE_DATA-heavy with few BUILD_NOW (the maritime deceptive practices are vessel-behavior the FI can't
  observe → SOURCE_DATA, NOT fabricated signals). The cleanly-anchoring OFAC advisory set is small (3:
  sham-transactions, maritime, virtual-currency — each a different vocab form); most OFAC docs defer red
  flags to a co-issued FinCEN advisory or use non-anchoring framing (honestly skipped, not forced).
- FINTRAC as source #4 (Phase 22, M7 — the FIRST CROSS-JURISDICTION source): FINTRAC (Canada's FIU) added
  as the FOURTH corpus source (`data/fintrac/`, doc_type "FINTRAC"; 3 derived) — the demo's first move
  beyond US-federal (US Treasury → +Canada). Compliance basis is DIFFERENT from the US sources: FINTRAC is
  Canadian Crown copyright, NOT public domain, so the verbatim non-negotiable was extended to a SECOND basis
  — FINTRAC publications are reproducible verbatim for NON-COMMERCIAL use WITH FINTRAC's required attribution
  (© His Majesty the King in Right of Canada + title + "a copy of the version at <URL>"), per FINTRAC's Terms
  & Conditions: a reproduction LICENCE, not the US 17 U.S.C. §105 no-copyright basis (updated identically in
  CLAUDE.md + HANDOFF.md; every OTHER non-US/non-FINTRAC source still paraphrases). FINTRAC OAs head their
  list with "indicators" (not "red flags"/"risk indicators"), so `rf_region` was WIDENED (`_RF_HEADER_FINTRAC`
  + `_RF_INTRO_FINTRAC`, ML/TF-QUALIFIED + an optional section-title trailing clause so "Money laundering
  indicators of <topic>" anchors), REGRESSION-GATED: the ML/TF-qualified phrasing occurs 0× across all 36
  FinCEN+OFAC mds → every existing rf_region byte-unchanged, all 32 records + `--selftest` still clean;
  grounding/`normalize` untouched. Acquisition HAND-CURATED (no FINTRAC crawler): FINTRAC serves a PDF at
  `<page-url>.pdf`, so `data/fintrac/index.json` lists those (the existing `_to_pdf_url` direct-download
  branch handled them with NO tweak), acquired via `acquire_fincen.py --source data/fintrac` (the
  `pdf_to_md.py` provenance header was made source-aware so a FINTRAC md is never mislabeled public domain).
  3 OAs derived (underground-banking, synthetic-opioids [the Canadian counterpart to the fentanyl showcase],
  terrorist-financing) — 42 indicators / 11 BUILD_NOW; the TF alert is honestly SOURCE_DATA-heavy (4/13 hinge
  on external listed-entity/jurisdiction attribution a bank can't observe → SOURCE_DATA, never fabricated).
  corpus.html's source panel renders each doc's OWN basis (FINTRAC shows Crown-copyright, never "public
  domain"); the prior blanket "all public domain" SELECT/footer copy was corrected to the multi-jurisdiction
  reality. The always-on "Illustrative data & outputs" badge stays, distinct from the verbatim attribution.
- FINTRAC DEPTH (Phase 23, M7 — Canadian depth, NO new source/non-negotiable/architecture change): grew the
  FINTRAC source 3 → 10 by deriving 7 more anchorable FINTRAC strategic-intelligence products — 6 Operational
  Alerts (human-trafficking/Project Protect, online-child-exploitation/Project Shadow, romance-fraud/Project
  Chameleon, illegal-wildlife/Project Anton, professional-ML, cannabis/Project Legion) + the real-estate
  Operational BRIEF (FINTRAC-2016-OB001 — snow-washing, the marquee Canadian typology). The demo's audience is
  a Canadian bank, so depth weighted Canadian-relevant. Reused the registry + inverted loop + gate UNCHANGED;
  the ONLY gate touch was a regression-gated WIDENING for the new INVERTED "Indicators of <X>" heading form
  (Operational Briefs + some OAs lead with "indicators": `_RF_HEADER_FINTRAC_INV`, two narrow branches —
  "of <ML/TF>" with a CONNECTOR-gated `:?$` that EXCLUDES the boilerplate sentence "Indicators of <ML/TF> can
  be thought of as red flags …" [which opens the existing 3 OAs before their forward heading], + "relating
  to | associated with <topic>" using connectors the boilerplate never uses → 0 collision). 0 of 39
  prior FinCEN+OFAC+FINTRAC rf_regions shifted; grounding core `normalize`/`check_record` byte-UNTOUCHED.
  225 indicators / 50 BUILD_NOW; honest yield over count — OCSE + wildlife are honestly SOURCE_DATA/
  BUILD_ENRICH-heavy (external attribution a bank can't observe), cannabis/professional-ml BUILD_NOW-rich
  (bank-observable EMT/cheque/cash/utility patterns); the human-trafficking record drops its 2016 APPENDIX
  (a reproduction of a SEPARATE 2016 OA — faithfulness, not a count cap). FINTRAC OAs are far more
  indicator-dense than FinCEN advisories (house norm ≤24; new range 16-57) — honest, the demo shows real
  depth. build.py + corpus.html UNCHANGED (the 4-type menu/chips/counts are data-driven). The always-on
  badge + source-aware Crown-copyright attribution stay.
- CROSS-CORPUS SYNTHESIS (Phase 24, M7 — the corpus becomes ANALYTICAL; NO new source/non-negotiable change):
  the explorer can now GROUP the 42 derived docs by money-laundering TYPOLOGY and show COMBINED coverage across
  a cross-jurisdiction cluster — the new insight being **no single advisory covers a typology; the combined
  corpus does** (uniquely possible once the corpus spans FinCEN + OFAC + FINTRAC, US + Canada). THE OVERLAY is a
  SEPARATE committed artifact `data/typology-map.json` (doc-id → ONE closed-vocabulary typology; 22-term vocab;
  jurisdiction is NOT stored — it's derived from the source registry: FinCEN/OFAC = US, FINTRAC = Canada) — NOT
  edits to the 42 derived records, so all 4 source dirs + the grounding core `derive_signals.py` stay
  BYTE-FROZEN. Validated at the BUILD BOUNDARY in `build.py` (`load_typology_map` + `validate_typology` —
  closed vocab + referential integrity + total live-doc coverage, FAIL-LOUD, where derived-shape validation
  already lives; the grounding gate is untouched): agent proposes the map, the deterministic gate disposes, the
  human reviews. `build.py` merges `typology` + `jurisdiction` + the typology vocab into `__CORPUS__`;
  `corpus.html` adds a Documents/Typologies toggle on Select → a typology's cross-jurisdiction cluster +
  combined coverage + per-jurisdiction contribution → drill-through into each doc's existing 6-screen per-doc
  arc (the per-doc arc is the spine, unchanged; the lens is ADDITIVE). 5 cross-jurisdiction clusters
  (terrorist-financing, synthetic-opioids, human-trafficking, professional-money-laundering,
  romance-and-investment-fraud) + 2 cross-AGENCY US clusters (sanctions-evasion across Advisory/Alert/OFAC,
  public-benefits-fraud). HONESTY (ties to the Phase-18 precision-lift rejection): combined coverage is honest
  UNION arithmetic over the existing per-indicator status (disclosed-illustrative under the always-on badge),
  per-jurisdiction is an honest COUNT, every clustered indicator stays traceable to its source doc +
  jurisdiction — NO similarity / overlap / lift number is computed or claimed; indicators are NOT de-duplicated
  or matched across regulators (that would need fabricated matching). Harness 74 → 98 (24 synthesis asserts).
  index.html + config/** + the 3 typology dists + the 4 source dirs + 42 derived records + the showcase stay
  byte-frozen; NO non-negotiable change.
- RED-FLAG TRANSLATION + ARTICLE-PROCESSING (Phase 25, M7 — corpus OUTPUT QUALITY; NO new source / non-negotiable
  change): the corpus explorer's red flags were bare VERBATIM article extractions (the grounded `flag` substring) — not
  how an AML programme writes red flags — and it lacked the showcase's article-processing beat. Phase 25 brings the corpus
  to the showcase's two-layer model: keep step 1 = the grounded verbatim extraction (the EVIDENCE), ADD step 2 = a
  `red_flag` TRANSLATION (natural AML-term phrasing) BESIDE it. Every live derived indicator gained a `red_flag` field,
  re-derived across all 42 docs via the inverted loop (one extraction subagent per doc, self-gated then independently
  re-checked; the 3 hand-curated showcase typologies are untouched). A NEW per-doc screen (`renderArticle`, inserted
  AHEAD of Coverage so the arc is Select → Read advisory → Coverage → Build recs → Signal → Close) renders the FULL source
  article — `build.py` inlines each live doc's `source_md` body via a new `_inline_article`/`_strip_provenance` (mirroring
  `advisory_full`'s text_file resolution; `render_one` + the 3 typology dists stay BYTE-FROZEN) — with each verbatim
  red-flag phrase highlighted, then reveals the translation; downstream screens label indicators by `red_flag` with the
  verbatim kept as a traceable subline. HONESTY (load-bearing): the verbatim `flag` stays the GROUNDED AUTHORITY shown
  BESIDE the translation (never replaced); the grounding gate logic (`normalize`/`rf_region`/`flag⊂md`) is BYTE-UNCHANGED;
  the gate's new `red_flag` check is SHAPE only (present / non-empty / distinct-from-verbatim / 12–240 chars), enforced in
  BOTH `derive_signals.py check_record` AND `build.py validate_corpus_data`. Translation faithfulness is the one NEURAL
  step — mitigated by show-both + the always-on illustrative badge + the per-doc re-check; paraphrase is the compliance
  DEFAULT, so the translation ALIGNS with the non-negotiables. dist/corpus 635KB → 2.19MB (the inlined source articles);
  harness 98 → 108. index.html + config/** + the 3 typology dists + every source md + every corpus-status.json + the
  showcase + data/typology-map.json stay byte-frozen; NO non-negotiable change.
- SHOWCASE-QUALITY ELEVATION (Phase 26, M7 — corpus OUTPUT QUALITY raised to the six-act showcase bar; NO new source /
  non-negotiable change): Phase 25 shipped the two-layer model but the output was still weak — the `red_flag`s read like
  PROSE (never anchored to `config/typologies/fentanyl.json`), the article render was STATIC, the Signal screen didn't
  "wow", docs/red-flags weren't grouped, and there was no landing. Phase 26 elevates all of it, workflow-driven. (1)
  THE REGISTER: every live derived indicator's `red_flag` was RE-TRANSLATED to the showcase's terse, mechanism-named
  AML-indicator register (fentanyl.json style — "Receive-and-forward to no-relationship payees (mule pass-through)",
  "Multi-originator geographic funnel-in", "Round-dollar gift-card / prepaid-card retail spend") via a DYNAMIC WORKFLOW
  (`ph26-register-retranslate`: 84 agents — 42 translate → 42 INDEPENDENT adversarial verify; the LLM proposes, a
  byte-SURGICAL applier writes ONLY the `red_flag` value + `--check-derived` disposes). All 42 `--check-derived` clean;
  the verbatim `flag` + the grounding logic + the SHAPE gate are BYTE-UNCHANGED (only `red_flag` VALUES changed); the
  show-both honesty model holds. (2) PROGRESSIVE ARTICLE RENDER: the Read-advisory screen ports the showcase
  `streamAdvisory` "agent reading" beat as a progressive ENHANCEMENT (final state in the template → reduced-motion + the
  string-DOM harness settle on it; full motion types a capped opening → reveals highlights → staggers the translate list).
  (3) GROUPING/SORT: Select is grouped by SOURCE (FinCEN Advisories / Alerts / OFAC / FINTRAC), newest-first within each;
  red flags sub-group by `section` on Coverage (the 13 multi-section docs; single-section stays flat). (4) WOW BEATS: a
  build-log on Signal (Act-4 port — animates the REAL `build_logic`, structural, no numbers) + a NEW Combination-lift
  screen (Act-5 port) between Signal and Close. The per-doc arc is now Select → Read advisory → Coverage → Build recs →
  Signal → Combination lift → Close. WOW-NUMBERS HONESTY (a deliberate, user-approved, scoped reversal of the Phase-18
  no-lift call): the lift figures are a GENERIC illustrative template (18→64→83), IDENTICAL across every doc, behind a
  LOUD "Illustrative · pending calibration — NOT measured on this document" tag (rose, distinct from the always-on badge)
  — NEVER 42 fabricated per-doc findings, NEVER presented as real; the records still carry no lift numbers. (5) a
  story-driven LANDING is the new ENTRY (`renderLanding` before Select; honest data-derived stat tiles 46/42/4/2; "Enter
  the corpus" CTA; the showcase landing is roadmapped — index.html stays byte-frozen). dist/corpus 2.19MB → 2.17MB;
  harness 108 → 139. Scope was the 42 `derived/*.json` (`red_flag` VALUES only) + `corpus.html` + `dist/corpus` + tests +
  docs; FROZEN byte-clean: the showcase (index.html + config/** + the 3 typology dists), every source md, every
  corpus-status.json, data/typology-map.json, and the grounding core `derive_signals.py`. NO non-negotiable change.
- SHIPPABILITY FIXES (Phase 27, M7 — corpus OUTPUT QUALITY raised to SHIPPABLE; NO new source / non-negotiable
  change): the user reviewed the BUILT Phase-26 corpus and judged it NOT shippable — the Read-advisory
  extract/translate beat "brutally bad", the build animation "not in place". A READ-ONLY assessment (a 44-agent
  workflow + deterministic metrics) DISPOSED the framing: the brutality was PRESENTATION, not the grounding
  system (39/42 docs PRESENTATION_ONLY; register already held; the verbatim flags real). Fixes, evidence-led:
  (1) `cleanArticle()` (corpus.html) markitdown-sanitizes the DISPLAYED source — strips page-break form-feeds,
  running headers (FINCEN ADVISORY/ALERT, letter-spaced "F I N C E N", FINTRAC OPERATIONAL), bare page-numbers,
  tab-between-every-word soup — a DISPLAY transform only (source md + grounding byte-untouched; footnote-ref
  digits KEPT so the cleaned text still grounds 1:1). (2) `highlightArticle` rewritten to NORMALIZE BOTH SIDES
  (the gate's own `normalize()`) + an index map back to source positions → 634/634 flags highlight (100%, from
  95.3% raw; the literal matcher would've REGRESSED on cleaned text — so the cleaner + matcher are coupled).
  (3) the Signal build-log ports the showcase Act-4 ".run working-pulse" rhythm in a proposal grid + the
  combination-lift gets a lift-side rationale panel, `firestat` OMITTED (its stats would be fabricated). (4) the
  progressive "agent reading" types the WHOLE article (no 1600-char cap; length-scaled ~6s) — the demo's first
  wow, now complete. (5) a faithfulness-guarded re-extraction (a 72-agent tighten→verify workflow + a
  deterministic applier) tightened 121 over-long verbatim flags to crisp CONTIGUOUS SUB-SPANS of the current
  flag — grounding is transitive (a sub-span of an already-grounded quote can't fabricate), gated by
  `normalize(new) ⊂ normalize(current)` + ≥24 chars + red_flag-distinct, byte-surgical (only flag lines change);
  genuinely-long single-sentence advisory indicators KEPT WHOLE (forcing them crisp would drop the qualifying
  condition = fabricated brevity, rejected). (6) `fin-2022-a001`'s 2 prose-y red_flags re-translated to the
  mechanism-named register. dist/corpus 2.17MB → 2.15MB; harness 139 → 148; all 42 records `--check-derived`
  clean; `--check all` 4/4 ZERO DRIFT. FROZEN byte-clean: the showcase (index.html + config/** + the 3 typology
  dists), every source md, every corpus-status.json, data/typology-map.json, the grounding core `derive_signals.py`
  (the gate logic byte-UNCHANGED — re-extraction only shrank flag VALUES). NO non-negotiable change.
- COMPLETENESS + GROUNDED COVERAGE + STREAMING READ (Phase 28, M7 — the corpus made COMPLETE, HONEST, and
  presentation-finished; NO new source / non-negotiable change): the user found the CORE defect Phase-27's
  assessment MISSED — verbatim red-flag EXTRACTION was grossly INCOMPLETE (the grounding gate only ever checked
  each flag was REAL, never that we got them ALL; the opioid doc shipped 15 of ~80). (1) COMPLETE RE-EXTRACTION
  (the `ph28-complete-sweep` 84-agent LLM-enumerate + completeness-critic workflow — deterministic bullet-detect
  was too unreliable, glyphs vary per doc): 634 → 903 indicators, every flag re-grounds (terror 13→77,
  opioids 15→68, human-trafficking 57→98, maritime 7→40). (2) GROUNDED COVERAGE (replaces fabrication): a
  user-approved 28-capability + 20-data-source taxonomy → each indicator tagged capability/data_source → the
  user's 28+20 YES/NO/PARTIAL interview answers → deterministic apply (cap→status, data→availability, the
  cover×data matrix→build_rec); honest SOURCE_DATA where the bank can't observe; 28 capability spec-templates
  author the BUILD_NOW build_logic. NO fabricated coverage. (3) STREAMING READ (corpus.html, T10 — the
  Phase-27/T7 phrase-by-phrase render was "staged" + ~48s-hardcoded): `renderArticle` now STREAMS the source in
  as if read (caret + scroll-follow), each red-flag phrase highlighting ONLY as the read reaches its position +
  its translation extracting alongside; BOTH the "phrases extracted" and "red flags" labels count UP from 0 (no
  full count shown up-front); length-scaled ~0.9ms/char, capped ~45s. Reduced-motion + the string-DOM harness
  settle on the final template; a full-motion harness section (`__drain` + an enriched dynEl) drives the stream.
  (4) DISPLAY POLISH: `cleanArticle` de-pipes markitdown PIPE-GRID tables (`|---|` rule rows dropped, `|cell|cell|`
  → readable text) + strips stray `#`/`**` — normalize-INVARIANT (normalize drops `|`/`#`/`*`/spaces), so grounding
  + highlighting are byte-unchanged. (5) DEDUP: the completeness sweep double-extracted 5 docs (terror under two
  parallel section schemes = 24 dupes; 4 others 1 each — tab-soup / newline / prefix-truncation artifacts), all
  confirmed against the source mds; 28 genuine duplicates removed byte-surgically (json `indent=1` round-trip, only
  the dup objects removed) → 903 → **875 indicators**, terror 77→53, ZERO unique lost. (6) BRANDING "FinCEN Corpus
  Explorer" → "AML Corpus Explorer" (the `build.py` brand subtitle was overriding the template at runtime — fixed).
  (7) FINTRAC ATTRIBUTION RELOCATED to a per-doc PAGE FOOTER (the user's compliance call): the on-screen Source
  LABEL carries the title only; the full Crown-copyright attribution (© His Majesty… + complete title + source URL)
  renders in the footer for the FINTRAC doc on screen, EMPTY for US public-domain docs (build.py preserves the ©
  clause as `attribution` + surfaces `url`). The verbatim+attribution non-negotiable is HELD (attribution present,
  just relocated) — NO deviation. dist/corpus ~2.40MB; harness 148 → **165**. FROZEN byte-clean: the showcase
  (index.html + config/** + the 3 typology dists), every source md, every corpus-status.json, data/typology-map.json,
  the grounding core `derive_signals.py` (all 875 re-ground through it byte-UNCHANGED). NO non-negotiable change.
- CAPABILITY LENS (Phase 29, M7 — the corpus re-projected by DETECTION CAPABILITY; NO new source / non-negotiable
  change): the Phase-28 interview produced a per-indicator `capability` (C1–C28) + `data_source` (D1–D20) tag on
  every one of the 875 indicators, but the tags were UNUSED in the ship artifact (neither `corpus.html` nor
  `build.py` read them). Phase 29 surfaces them as the demo's executive view. (1) THE OVERLAY: a SEPARATE committed
  artifact `data/capability-taxonomy.json` (code → {name, desc, group, posture}) — labels from the Phase-28
  taxonomy + the institution's interview posture (y/partial/n) per code — the Phase-24 `data/typology-map.json`
  pattern; `build.py` must NEVER read `.dev-wiki/`. Validated at the BUILD BOUNDARY (`load_capability_taxonomy` +
  `validate_capability_taxonomy`: shape + posture vocab + closed-vocab referential integrity — every code a live
  indicator carries is declared + every live indicator carries both codes; fail-loud), where derived-shape +
  typology validation already live; the grounding core stays untouched. The per-indicator codes already ride in
  each derived record, so `build.py` only inlines the taxonomy object into `__CORPUS__`. (2) THE UI (`corpus.html`):
  a THIRD Select mode — Documents / Typologies / **Capabilities** (the Phase-24 toggle, extended). The capability
  picker lists one card per demanded capability (all 28): name, group, the institution's posture chip
  (in place / partial / not yet), honest demand count + docs/typologies + a covered/partial/gap micro-bar — sorted
  GAP-PRIORITY (not-yet first, then by demand: the exposure list). Drill a capability → `renderCapability`: its
  indicators pooled across every regulator/jurisdiction (grouped by source document, each a clickable drill row),
  the data sources it depends on (each with its own posture), and a coverage gauge — then drill into a doc's
  existing per-doc arc, Back returning to the capability (a new `fromCapability`, mirroring `fromTypology`).
  (3) HONESTY (the Phase-24 synthesis model): a pure RE-PROJECTION of already-grounded data — demand/coverage are
  honest counts over the existing per-indicator status, posture is the interview answer (already in the demo as
  per-doc coverage status, just re-grouped); NO similarity/overlap/lift number is computed or claimed; indicators
  are NOT de-duplicated across sources; the always-on "Illustrative data & outputs" badge stays. Harness 165→**190**
  (25 capability-lens asserts). FROZEN byte-clean: the showcase (index.html + config/** + the 3 typology dists),
  every source md, every corpus-status.json, data/typology-map.json, the grounding core `derive_signals.py`, and
  every derived `*.json` record (they already carried the codes — NO re-derivation). dist/corpus ~2.43MB; `--check
  all` 4/4 ZERO DRIFT, `--selftest` PASS, all 42 `--check-derived` clean. NO non-negotiable change.
- DATA-SOURCE LENS (Phase 30, M7 — the corpus re-projected by DATA SOURCE; the SYMMETRIC counterpart to the Phase-29
  capability lens, on the D1–D20 axis; NO new source / non-negotiable / data / build change): the Phase-28 interview
  tagged every indicator with a `data_source` (D1–D20) code AND Phase 29 ALREADY committed the `data_sources` block in
  `data/capability-taxonomy.json` + had `build.py` validate (referential integrity) + inline it into `__CORPUS__` —
  so only the capability (C) axis had a UI; the data (D) axis shipped INERT. Phase 30 surfaces it as the demo's
  data-access view, ENTIRELY in `corpus.html` (the TIGHTEST phase in the series — `build.py`, the taxonomy, and all
  42 derived records stay BYTE-FROZEN). (1) THE UI: a FOURTH Select mode — Documents / Typologies / Capabilities /
  **Data sources** (the Phase-24/29 toggle, extended). The data-source picker lists one card per demanded feed (all
  20): name, the institution's data-access posture chip (available / partial / not yet), honest demand count + docs/
  typologies + a covered/partial/gap micro-bar — sorted GAP-PRIORITY (not-yet first, the data-access exposure list).
  Cards OMIT the group line (data sources are a flat 20-item taxonomy — no D-axis group analogue). Drill a data source
  → `renderDataSource`: its indicators pooled across every regulator/jurisdiction (grouped by source document, each a
  clickable drill row), the detection CAPABILITIES those indicators implement (the INVERSE of the capability view's
  "depends on data" panel, each with its own posture), and a coverage gauge — then drill into a doc's existing per-doc
  arc, Back returning to the data source (a new `fromDataSource`, mirroring `fromCapability`). (2) THE DISTINCT STORY
  (why it's not "the same lens twice"): a capability is a BUILD problem ("do we have the detection logic"); a data
  source is an ACCESS problem ("do we even have the feed"). The payoff: **7 of 20 data sources have posture "not yet"**
  — those are exactly the SOURCE_DATA indicators (the bank can't action them until it acquires e.g. blockchain
  analytics / beneficial-ownership data), previously buried per-doc, now legible corpus-wide. (3) HONESTY (the Phase-24
  synthesis model): a pure RE-PROJECTION of already-grounded data — demand/coverage are honest counts over the existing
  per-indicator status, posture is the interview answer (already in the demo as per-doc coverage, just re-grouped); NO
  similarity/overlap/lift number; indicators are NOT de-duplicated across sources; the always-on "Illustrative data &
  outputs" badge stays. Harness 190→**217** (27 data-source-lens asserts). FROZEN byte-clean: the showcase (index.html
  + config/** + the 3 typology dists), every source md, every corpus-status.json, data/typology-map.json,
  **data/capability-taxonomy.json**, the grounding core `derive_signals.py`, **scripts/build.py**, AND every derived
  `*.json` record (the data_sources axis was already inlined/validated in Phase 29 — NO re-derivation, NO build change).
  dist/corpus ~2.46MB; `--check all` 4/4 ZERO DRIFT, `--selftest` PASS, all 42 `--check-derived` clean. NO non-negotiable change.
- ADVERSE-MEDIA / NEGATIVE-NEWS STREAM (Phase 31, M8 — a SECOND atom stream; a NEW standalone ship artifact, NOT a
  corpus/showcase change): Signal Watch was the advisory→signal loop (the six-act showcase + the corpus explorer);
  Phase 31 opens a SECOND stream over UNSTRUCTURED news as a third single-file artifact `dist/news/index.html` (built
  from a new `news.html`, mirroring how `dist/corpus` was added). The thesis is unchanged — an adverse-media hit is an
  ATOM that composes with a counterparty's transaction signals — and it makes concrete the "what aren't we watching?"
  TD-anxiety the showcase opens on (TD Bank's 2024 penalty was a CDD/adverse-media failure). The WALKING SKELETON proves
  ONE new muscle end-to-end, offline: unstructured news → grounded entity + red-flag extraction → fuzzy-match against a
  SYNTHETIC client/counterparty book → potential exposure → human disposition. ARC (in `news.html`): Select → Read
  (each grounded red-flag phrase highlighted + each named entity tagged, with the natural-AML `red_flag` translation
  beside the verbatim — the corpus's two-layer model reused) → Screen (the NEW muscle — a client-side fuzzy matcher
  `normalize → token-sort → Jaro-Winkler`, REAL string-similarity, thresholded at 0.85; it surfaces the NEAR-matches an
  exact-name screen would miss) → Disposition (the human gate — keyboard-safe `<button>` toggles, default-confirm, the
  analyst DISMISSES false positives: a common name can collide with an unrelated person at a perfect 1.0 score) →
  Exposure (confirmed hits framed as adverse-media atoms; the compose-with-the-transaction-signal payoff is the M8
  NORTH STAR, scoped OUT). DATA (committed, SYNTHETIC — non-negotiable #4): `data/news/articles/*.md` (4 fictional
  scenarios — trade-shell / mule-romance / sanctions-front / professional-ML) → `data/news/derived/*.json` (named
  `entities` + red-flag `flag` phrases, each QUOTE-GROUNDED in the article via normalize-substring, + a `red_flag`
  translation) + `data/news/book.json` (12-row synthetic book, SEEDED with exact matches, near-matches [Volkoff /
  Dimitri / word-order Van Thanh / Bellwether], and a common-name FALSE-POSITIVE trap [Andrei Petrov, score 1.0, a
  DIFFERENT person]). BUILD: `build.py news` (added ADDITIVELY — a new `news` target + `validate_news_data` [the
  build-boundary grounding gate, fail-loud, with a LOCAL `_news_normalize` so build.py STILL never imports the authoring
  layer] + `render_news`/`build_news`/`check_news`; `news`/`all`/`--check` wired). HONESTY: synthetic data under the
  always-on badge; fuzzy scores are REAL computed similarity (never fabricated); counts honest; the near-match + the
  trap are DESIGNED INTO the synthetic data to teach the mechanism, not claimed as detection rates. FROZEN byte-clean:
  the showcase (index.html + config/** + 3 typology dists), the ENTIRE corpus (corpus.html, dist/corpus, all 4 source
  dirs, every corpus-status.json, all 42 derived records, data/typology-map.json, data/capability-taxonomy.json), and
  the grounding core `derive_signals.py`; build.py edited ADDITIVELY (existing dist outputs byte-identical). Harness:
  `tests/news-stream.test.mjs` (+38, both motion modes). NO non-negotiable change.
- REAL-SOURCE + PRESENTATION ELEVATION (Phase 32, M8 — the news stream's articles switched SYNTHETIC→REAL + the
  presentation raised to the corpus's bar; NO new artifact, NO non-negotiable change): the user reviewed the BUILT
  Phase-31 dist/news and judged it "very low effort … a poorly staged slide show … repeating the same mistakes" (the
  Phase-27 corpus failure — a RESULT not a PROCESS), and asked to use REAL online news. PUSHBACK reframed "ignore
  copyright / non-commercial" (verbatim commercial news = copyright reproduction + defamation of real named persons +
  undercuts the demo's own compliance story) to the CLEAN path: REAL US-FEDERAL GOV-ENFORCEMENT adverse media (DOJ
  press releases + OFAC designations), PUBLIC DOMAIN under 17 U.S.C. §105 — the corpus's EXACT verbatim basis (Phase
  21), the MOST AML-relevant adverse media. NOT a non-negotiable change: the existing US-federal verbatim basis applied
  to the news artifact; the COUNTERPARTY BOOK STAYS SYNTHETIC (#4 held) — the bridge is REAL adverse-media entity ×
  SYNTHETIC book. (1) DATA: 4 real docs (`data/news/articles/*.md`, verbatim-excerpted with a source + public-domain
  provenance header; acquired BUILD-TIME via the Wayback Machine [DOJ bot-blocks WebFetch/curl] — authoring-only, the
  ship stays offline/no-fetch) — Ravenell (attorney trust-account ML), Mullings (romance/BEC mule), Goltsev (Canadian
  export-control shells SH Brothers / SN Electronics), OFAC TGR Group (Russian shadow-finance network); re-derived
  `data/news/derived/*.json` (14 entities with grounded name+location+age+profession, 29 red-flags + red_flag
  translations, all normalize-grounded); `validate_news_data` EXTENDED to ground the entity attributes (additive — news
  path only; build.py STILL never imports the authoring layer). The SYNTHETIC book reseeded against the REAL entities:
  1 EXACT true-positive (Siam Expert — a designated entity IS your counterparty) + 5 near-matches an exact-name screen
  misses (transliteration / suffix / word-order, 0.95–1.0) + a common-name FALSE-POSITIVE trap (George Rossi 1.0, a
  DIFFERENT person, dismissed at the gate). (2) PRESENTATION (`news.html`, rewritten): the FULL corpus dossier theme +
  a step rail (Select › Read › Screen › Disposition › Exposure) + per-doc source attribution; a STREAMING "agent
  reading" Read (the source streams in, each red-flag phrase + entity tag reveals as the read reaches it, entity CARDS
  [name/location/age/profession] + the typology + translate rows reveal alongside, the labels counting up from 0); a
  VISIBLE SCAN PROCESS on Screen (each book row swept + scored REAL Jaro-Winkler, ranked, threshold line, near-match
  surfaced, trap flagged) — the template renders the FINAL resting state (reduced-motion + the string-DOM harness settle
  on it), the stream/scan a progressive ENHANCEMENT guarded by `insertAdjacentHTML`. HONESTY: entity attributes ground
  or drop; the scan shows REAL computed scores (no fake progress bar); the book synthetic; the always-on badge stays.
  dist/news 40.6KB → ~70KB. Harness 38 → **65** (reduced-motion final state + a full-motion enriched-shim drive of the
  stream + scan). FROZEN byte-clean: the showcase (index.html + config/** + 3 typology dists), the ENTIRE corpus, and
  the grounding core `derive_signals.py`; build.py edited ADDITIVELY (existing dist outputs byte-identical). NO
  non-negotiable change.
- IMPORTANT — INVERTED extraction boundary (Phase 16) + the SUBTRACTION (Phase 17): the **LLM EXTRACTS, the
  deterministic layer GATES**, and the old extractor is **DELETED**. The earlier deterministic
  `extract_red_flags` accreted format special-casing every phase yet the LLM still had to author/prune its
  output, so the subtraction test inverted it: the LLM (the model session as backend) extracts the candidate
  red flags + per-indicator status/data judgment + build recommendation + signal logic; the deterministic
  layer DISPOSES via `check_record` — **quote-GROUNDING** (each verbatim `flag` is a substring of the source
  md under `normalize()`, the traceability authority, replacing src_line ∈ extractor) + a cheap section-cite
  RELEVANCE region (`rf_region`) + the cover×data matrix + BUILD_NOW⇒full-build_logic shape. Complexity moved
  from brittle section-PARSING (open problem — every advisory differs) to a closed-set md NORMALIZER and
  SHRANK. **Phase 17 then DELETED `extract_red_flags` and the whole `--scaffold` / `--draft` /
  `--scaffold-derived` authoring stack it fed** (`derive_signals.py` ~1200 → ~600 lines), leaving exactly the
  gate (`normalize` + `rf_region` + `check_record`) + a ~14-line `rf_region`-bounded triage counter
  (`_rf_triage` — the only counting role the extractor kept; it reuses the already-computed region span). The
  inverted loop is the SOLE derivation path; the LLM proposes (extraction too), the deterministic gate + the
  two human gates dispose.
- Extraction faithfulness (the LLM extracts; the gate grounds): faithfulness is now enforced by the gate, not
  a structural parser — every verbatim `flag` must QUOTE-GROUND in the source md. Two heterogeneous formats
  the deleted deterministic extractor could not parse are handled by the LLM reading like a human:
  **footnote-interrupted** lists (a clause split across a page-break footnote run — the LLM extracts a
  CONTIGUOUS grounded span and drops the across-the-break continuation rather than bridging it, e.g.
  fin-2021-a001 IND-01) and **glued-no-separator** advisories (fin-2021-a004 ransomware, fin-2026-a001
  health-care — markitdown dropped both bullets AND blank lines so flags fuse into one block; the `_rf_triage`
  counter sizes them as a few blocks, but the LLM extracts every genuine flag, e.g. health-care 24, and the
  gate grounds each). No structure-preserving converter and no post-hoc splitter were needed. Convention:
  derived records store RAW text; corpus.html's `esc()` is the sole escaper (never pre-escape `&gt;`/`&lt;`
  in a record — it double-escapes). `normalize()` drops the glued `FINCEN ADVISORY` running header and
  collapses smart quotes / hyphen-wraps / footnote digits, so a header-glued or marker-glued flag still
  grounds (keep an in-flag footnote marker verbatim where it falls mid-span, e.g. `NPO84`).

## How to run
- Build: `python3 scripts/build.py <id>` (or `all`) → `dist/<id>/index.html`.
- Corpus explorer (MULTI-SOURCE): `python3 scripts/build.py corpus` → `dist/corpus/index.html`, merging
  every source in `build.py`'s `CORPUS_SOURCES` registry — `data/fincen/` (advisories) + `data/fincen-alerts/`
  (alerts) + `data/ofac/` (OFAC) + `data/fintrac/` (FINTRAC), each contributing `corpus-status.json` +
  `derived/*.json`. The build also merges two committed overlays — `data/typology-map.json` (Phase 24) and
  `data/capability-taxonomy.json` (Phase 29: code→{name, group, interview posture} for the capability lens) —
  each validated at the build boundary (referential integrity against the live corpus; the grounding core is
  untouched). Regenerate a source's manifest with
  `python3 scripts/derive_signals.py --corpus-status [source_dir]` (default `data/fincen`) after its md set
  changes, then rebuild. Acquire a new FinCEN source: `crawl_fincen.py [--alerts] --fetch` then `--write` →
  `acquire_fincen.py --source <dir> <id>` → `pdf_to_md.py --source <dir> <id>` (raw PDFs are gitignored;
  the committed `<dir>/*.md` is the derivation surface).
- News stream (M8, Phase 31 + Phase 32): `python3 scripts/build.py news` → `dist/news/index.html` — a SEPARATE,
  standalone ship artifact (the adverse-media / negative-news stream, a SECOND atom stream), built from
  `news.html`. Reads the committed `data/news/{articles/*.md, derived/*.json, book.json}` — Phase 32: the
  `articles/*.md` are now REAL US-federal gov-enforcement docs (DOJ press releases + OFAC designations),
  reproduced VERBATIM (excerpted) under 17 U.S.C. §105 public domain (the corpus's basis, applied to news); the
  `book.json` STAYS SYNTHETIC (non-negotiable #4) — REAL adverse-media entity × SYNTHETIC book. Validates grounding
  at the build boundary (`validate_news_data` — every extracted entity name, each entity ATTRIBUTE
  [location/age/profession], and every red-flag `flag` must quote-ground in its article via a LOCAL normalizer;
  build.py never imports the authoring layer), inlines at `__NEWS__`. The runtime fuzzy matcher (normalize →
  token-sort → Jaro-Winkler, REAL scores) runs entirely CLIENT-SIDE (no LLM/fetch). Real-doc acquisition is
  BUILD-TIME/authoring ONLY (the Wayback Machine routes around DOJ bot-blocks; raw fetches gitignored, the committed
  `articles/*.md` is the surface). build.py is edited ADDITIVELY (existing dist outputs byte-identical); `--check
  all` and `all` include news.
- Present: open `dist/<id>/index.html` (or `dist/corpus/index.html`, or `dist/news/index.html`) — single
  self-contained file, offline, no server. Drift guard before presenting: `python3 scripts/build.py --check all`.
- Test (all dep-free, no install): `node tests/corpus-explorer.test.mjs` drives the story landing + the corpus explorer's
  6-screen per-doc arc (Select → Read advisory → Coverage → Build recs → Signal → Combination lift → Close) against the
  committed `dist/corpus/index.html` (gate toggle, the article screen + red_flag threading, Signal empty states,
  close-the-loop coverage math, reduced-motion) + the multi-source menu (advisories + alerts + OFAC +
  FINTRAC, doc_type chips; an alert, an OFAC advisory, AND a FINTRAC OA each walk the arc; the FINTRAC
  Crown-copyright attribution renders in the page FOOTER for the doc on screen — Phase 28, the on-screen
  Source label carries the title only; US public-domain docs show no footer attribution) + the cross-corpus synthesis view
  (Phase 24: typology-mode picker, a cross-jurisdiction cluster's combined coverage = honest union over
  the pooled indicators, the no-similarity/overlap/lift honesty gate, drill-through + Back-to-cluster)
  + the Phase-26 register beats (the story landing as entry; Select grouped by source / newest-first;
  red-flag section sub-grouping on Coverage; the Act-4 build-log + the Act-5 combination-lift with its LOUD
  "illustrative · pending calibration" honest-illustrative gate — a generic template, never per-doc fabricated)
  + the Phase-27 shippability fixes (the Read-advisory source panel is markitdown-CLEANED — no running
  headers / letter-spaced headers / tab-soup; normalize-both-sides highlighting lands ~every grounded flag;
  the Signal build-log runs in a proposal grid + the combination-lift carries a lift-side panel with firestat
  OMITTED) + the Phase-28 beats (the FULL-MOTION STREAMING read — the source streams in, each phrase highlights
  as the read reaches it, both labels count up from 0, settles with the caret removed; de-piped markdown tables;
  the FINTRAC footer attribution present for a FINTRAC doc / empty for a US doc)
  + the Phase-29 CAPABILITY LENS (a third Select mode Documents / Typologies / Capabilities; the per-capability
  card carries honest demand + the institution's interview posture + the covered/partial/gap split, gap-priority
  sorted; drilling a capability pools every indicator that depends on it as honest set arithmetic — NO
  similarity/overlap/lift — and drills into a doc's per-doc arc with Back returning to the capability)
  + the Phase-30 DATA-SOURCE LENS (a FOURTH Select mode Documents / Typologies / Capabilities / Data sources — the
  symmetric counterpart on the D1–D20 axis; the per-data-source card carries honest demand + the institution's
  data-access posture + the covered/partial/gap split, gap-priority sorted; drilling a data source pools every
  indicator that depends on that feed [with the inverse "Implements capabilities" panel] and drills into a doc's
  per-doc arc with Back returning to the data source); 217 assertions. `node tests/news-stream.test.mjs`
  (M8, Phase 31 + Phase 32) drives the adverse-media stream arc (Select → Read → Screen → Disposition → Exposure)
  + the fuzzy matcher against the committed `dist/news/index.html` — the seeded matches surface (Siam Expert EXACT
  1.0 = a designated entity IS your counterparty; near-matches an exact-name screen misses: Pullman suffix 1.0,
  Zhdanova 0.989, Nikolay translit 0.973, Puzyreva word-order 1.0, Malachi typo 0.962, Ravenell 0.950), the
  common-name FALSE-POSITIVE trap (George Rossi 1.0, a different person) is dismissable at the human gate
  (confirmed-count drops), the STREAMING Read highlights grounded flags + tags entities + shows entity cards with
  grounded attributes + the typology + the real-source attribution, the SCAN PROCESS sweeps real per-row scores, no
  fabricated precision number; both motion modes (reduced-motion final state + a full-motion enriched-shim drive of
  the stream + scan); 65 assertions. `python3 scripts/derive_signals.py --selftest`
  runs the derivation GATE checks. Pre-present sequence: `--check all` (drift) → `node tests/…` (arcs) → walk
  `tests/smoke-checklist.md` (the human-eye checks).
- Iterate: edit `index.html` / `corpus.html` / a config, rebuild. `python3 -m http.server` optional, never required.

## Knowledge wiki
Domain reference comes from the registered **aml-wiki** (central store at
`/Users/jwang/private-knowledge/aml-wiki`) — AML typologies, red-flag indicators,
FINTRAC/FinCEN + OSFI E-23 references, the atom/composition vocabulary. A machine-local
symlink `wiki/ → aml-wiki` (gitignored) makes the harness auto-select it in this dir;
the SessionStart hook activates the knowledge-wiki framework from it.
- Query domain knowledge before guessing: `/wiki-query <question>` (auto-scopes to aml-wiki).
- AML insights worth keeping go back to aml-wiki via `/wiki-add` — it is the canonical home.
- For authoring a new typology, pull paraphrased advisory specifics + indicators from the wiki
  rather than inventing them — or, for a FinCEN advisory, run the M6 pipeline (acquire→convert) and
  derive from the verbatim markdown. Retrieval over parametric guessing.

## Aesthetic
Dark "dossier" theme, amber `--signal` (#f6a623) accent; fonts Newsreader / Archivo /
JetBrains Mono. Theme lives in `:root` CSS variables. Refined, not flashy.

## Milestones
M0 bootstrap · M1 config-driven refactor · M2 multi-typology · M3 presenter polish ·
M4 (skipped) live/pre-gen mode · M5 ship · M6 Signal Watch ingestion pipeline (FinCEN verbatim) ·
M7 corpus-backed demo (Phase 12 derivation backend + Phase 13 corpus explorer `dist/corpus/` +
Phase 20 multi-source: FinCEN advisories + alerts; Phase 21: OFAC source #3; Phase 22: FINTRAC source #4
(first cross-jurisdiction, Crown-copyright non-commercial licence); Phase 23: FINTRAC depth 3→10 (OAs +
the real-estate Operational Brief; inverted-anchor widening) — 42 derived across 46 publications, 4 sources;
Phase 24: cross-corpus synthesis — a `data/typology-map.json` overlay groups the corpus by typology + shows
combined coverage across cross-jurisdiction clusters (honest union arithmetic, no fabricated cross-corpus metric);
Phase 25: red-flag translation + the article-processing screen — every derived indicator gains a natural-AML `red_flag`
beside its grounded verbatim quote, and the corpus explorer renders the full source document (highlight → translate)
ahead of Coverage (honest show-both; NO non-negotiable change);
Phase 26: showcase-quality elevation — all 42 `red_flag`s re-translated to the fentanyl-register AML-indicator style
(via a dynamic translate→adversarial-verify workflow; verbatim + grounding byte-unchanged), progressive "agent reading"
article render, Select grouped by source / newest-first + red-flag section sub-grouping, the Act-4 build-log + an Act-5
combination-lift wow beat (generic illustrative template, loud "pending calibration" tag — never per-doc fabricated),
and a story-driven landing as the entry (NO non-negotiable change);
Phase 27: shippability fixes — an assessment workflow disposed the framing (the brutality was PRESENTATION not
the grounding system), then markitdown-cleaned the Read-advisory source + normalize-both-sides highlighting (100%)
+ the Act-4 build-log in a proposal grid + a combination-lift lift-side panel (firestat omitted) + the whole-article
progressive read + a faithfulness-guarded re-extraction tightening 121 over-long verbatim flags to crisp grounded
sub-spans (grounding transitive; long single-sentence indicators kept whole) — corpus made SHIPPABLE, gate logic
byte-unchanged, NO non-negotiable change);
Phase 28: completeness + grounded coverage + streaming read — the user found EXTRACTION was grossly INCOMPLETE
(the gate checked each flag was REAL, never that we got them ALL): a complete re-extraction 634→903 indicators (every
flag re-grounds), coverage now GROUNDED in the user's 28-capability + 20-data-source YES/NO/PARTIAL interview (not
fabricated), a full-motion STREAMING "agent reading" render (source streams in, each phrase highlights as the read
reaches it, both labels count up from 0), de-piped markdown tables, "AML Corpus Explorer" branding, the FINTRAC
attribution relocated to a per-doc page footer (verbatim+attribution non-negotiable HELD), and a dedup of 28 genuine
duplicate indicators from the sweep (terror 77→53) → 875 indicators; grounding core byte-unchanged, NO non-negotiable change);
Phase 29: capability lens — the Phase-28 capability/data-source taxonomy (28 capabilities + 20 data sources), unused
in the ship artifact, is promoted to a committed build-validated `data/capability-taxonomy.json` (code→{name, group,
interview posture}) and surfaced as a THIRD Select mode (Documents / Typologies / Capabilities). The corpus is
re-projected by DETECTION CAPABILITY: per-capability honest demand count + the institution's interview posture
(have/partial/gap) + the covered/partial/gap split, gap-priority sorted; drill a capability → its indicators pooled
across every regulator/jurisdiction (honest set arithmetic, NO similarity/overlap/lift) grouped by source doc → drill
into a doc's per-doc arc, Back returns to the capability. Honest re-projection only (the Phase-24 synthesis model); the
derived records + the grounding core stay byte-frozen (they already carried the codes — no re-derivation); the always-on
badge stays; NO non-negotiable change. Harness 165→190.
Phase 30: data-source lens — the SYMMETRIC counterpart to the Phase-29 capability lens on the D1–D20 data-source
axis. The Phase-28 interview tagged every indicator with a `data_source` code AND Phase 29 already committed the
`data_sources` block in `data/capability-taxonomy.json` + had `build.py` validate/inline it — but only the capability
(C) axis had a UI. Phase 30 surfaces the D axis as a FOURTH Select mode (Documents / Typologies / Capabilities /
Data sources). The corpus is re-projected by DATA SOURCE: per-data-source honest demand count + the institution's
data-access posture (available/partial/not-yet) + the covered/partial/gap split, gap-priority sorted; drill a data
source → its indicators pooled across every regulator/jurisdiction (honest set arithmetic, NO similarity/overlap/lift)
grouped by source doc, with an inverse "Implements capabilities" panel → drill into a doc's per-doc arc, Back returns
to the data source. The DISTINCT story vs the capability lens: a capability is a build problem, a data source is an
ACCESS problem — 7 of 20 feeds are "not yet" available (the SOURCE_DATA indicators the bank can't action until it
acquires the data), surfaced corpus-wide. The TIGHTEST phase in the series: a pure `corpus.html` UI re-projection +
harness + docs — `scripts/build.py`, `data/capability-taxonomy.json`, AND all 42 derived records stay BYTE-FROZEN (the
data_sources axis was already inlined/validated in Phase 29 — no data/build change). Honest re-projection only (the
Phase-24/29 model); the always-on badge stays; NO non-negotiable change. Harness 190→217.
M8 the adverse-media / negative-news stream (Phase 31: a SECOND atom stream as a new standalone artifact
`dist/news/` from `news.html` — synthetic news → grounded entity + red-flag extraction → a client-side fuzzy
match (normalize → token-sort → Jaro-Winkler, REAL scores) against a synthetic client/counterparty book →
potential exposure → a human disposition gate. Surfaces the near-matches an exact-name screen misses (typo /
transliteration / word-order) and the common-name FALSE-POSITIVE trap, which the human dismisses. Build-time
data (`data/news/{articles,derived,book}`) grounded at the build boundary (`validate_news_data` — a LOCAL
normalizer, build.py never imports the authoring layer); runtime is pure client-side JS (no LLM/fetch). A
WALKING SKELETON — the compose-with-the-transaction-signal payoff is the M8 north star, scoped OUT. build.py
edited ADDITIVELY (a new `news` target; existing dist outputs byte-identical, `--check all` includes news); the
showcase + the entire corpus + the grounding core `derive_signals.py` stay byte-frozen. Harness +38
(`tests/news-stream.test.mjs`, both motion modes). HONEST: synthetic data under the always-on badge, REAL fuzzy
scores, no fabricated number. NO non-negotiable change. Phase 32: the news ARTICLES switched SYNTHETIC→REAL
US-federal gov-enforcement docs (DOJ + OFAC, verbatim-excerpted under 17 U.S.C. §105 public domain — the corpus's
basis applied to news; the BOOK stays synthetic, non-negotiable #4 held), and the presentation was raised to the
corpus's bar — the full dossier theme + a step rail + per-doc source attribution + a STREAMING "agent reading" Read
[entity cards with grounded name/location/age/profession + the typology, counts up from 0] + a VISIBLE SCAN PROCESS
[real per-row Jaro-Winkler sweep, threshold line, near-match surfaced, trap flagged]. The book reseeds against the
real entities: 1 exact true-positive [Siam Expert] + 5 near-matches an exact screen misses + a common-name trap
[George Rossi]. `validate_news_data` extended to ground the entity attributes (additive). Harness 38→65; dist/news
~70KB; NO non-negotiable change).
See HANDOFF.md §8.

## Definition of done
Reliable offline · multi-typology from config · presenter controls · compliance-clean ·
README written. See HANDOFF.md §1.2.
