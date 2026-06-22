# Smoke Checklist — stage rehearsal

Run before any presentation, **per typology you intend to present**. Automated checks cover
structure / schema / self-containment (`scripts/build.py --check` validates the config at the build
boundary and fails loud) and the corpus explorer's 5-screen arc behavior
(`node tests/corpus-explorer.test.mjs` — see the corpus-explorer note below); this checklist covers
what only a human eye can confirm: live visuals, animation, pacing, keyboard control, and compliance
framing.

Engine chrome (header, badge, the six-act arc, both human gates, the gate labels) is **identical
across typologies** — it lives in the generic engine, not the config. Only the six values in the
**per-typology table** below change. Walk the arc once per typology, reading expected values from
that table.

## Per-typology expected values

| Act / element | `fentanyl` | `trade-based` |
|---|---|---|
| Act 0 — Coverage index gauge | **45%** | **35%** |
| Act 4 — Spec card signal name | `S-FLOW-THROUGH-RETAIL` | `S-PRICE-ANOMALY-TRADE` |
| Act 5 — Fire-stats (count / standalone / best-combo) | **1,240 / 18% / 83%** | **1,860 / 22% / 81%** |
| Act 5 — Lift bars (weak → mid → strong) | **18 → 64 → 83** | **22 → 58 → 81** |
| Act 6 — Gauge animates | **45% → 55%** | **35% → 45%** |
| Act 6 — Delta chip | ▲ flow-through now covered · courier queued | ▲ price-anomaly now covered · phantom-shipment queued |

> Source of truth: `config/typologies/<id>.json` (gauge % is derived by the engine as
> `round((covered·1 + partial·0.5) / N · 100)`; the rest are config fields). If you add a typology,
> add a column.

## Build & open
- [ ] `python3 scripts/build.py <id>` prints `<id> -> dist/<id>/index.html` (or `all` to build every typology)
- [ ] **Drift guard:** `python3 scripts/build.py --check all` reports **zero drift** — every committed `dist/<id>/index.html` still equals a fresh build of its config (guards all 3 shipped typologies; non-mutating). Catches a stale-dist commit before it reaches the stage. Belt-and-suspenders: `git status --porcelain dist/` is also clean (flags a stray/untracked dist file that `--check` won't)
- [ ] Open `dist/<id>/index.html` by **double-clicking the file** (true `file://`, no server)
- [ ] Header shows **Signal Watch** / AML Detection · Vision Prototype *(shared chrome)*
- [ ] The amber **"Illustrative data & outputs"** badge is visible (top-right) on **every** act *(shared chrome)*

## Corpus explorer (`dist/corpus/`) — automated arc check + human walk
- [ ] **Automated arc (structural pre-present check):** `node tests/corpus-explorer.test.mjs` exits **0** —
  drives the committed `dist/corpus/index.html` through the 5-screen arc under a dep-free DOM shim and
  asserts the invariants (the human gate's div-toggle selection, the two honest Signal empty states, the
  close-the-loop coverage math + no indicator mutation, reduced-motion single-paint, 0-picked flat-hold).
  Run it after any `corpus.html` edit + rebuild; it doubles as a build-output smoke test for the corpus dist.
- [ ] Open `dist/corpus/index.html` (`file://`): pick a **derived** advisory → walk **Select → Coverage →
  Build recs (gate) → Signal → Close the loop**; deselect a build-now row and confirm the Signal cards +
  the closing coverage rise both shrink to match (the automated check pins this, but eyeball it on the
  presentation browser).
- [ ] **Capabilities mode (Phase 29):** on Select, click the **Capabilities** toggle (third button, after
  Documents / Typologies). Confirm: one card per detection capability, each with a posture chip
  (**in place / partial / not yet**), an honest indicator-demand count + a covered/partial/gap micro-bar;
  the list is **gap-priority** sorted (not-yet capabilities lead). Click a capability → its indicators
  appear grouped by source document with a coverage gauge + a "Depends on data" row; click a document row
  to **drill into that doc's per-doc arc**, then **Back** returns to the capability (not the picker). No
  fabricated number — only honest counts + the always-on "Illustrative data & outputs" badge.
- [ ] **Data sources mode (Phase 30):** on Select, click the **Data sources** toggle (fourth button, after
  Documents / Typologies / Capabilities). Confirm: one card per data source, each with a data-access posture
  chip (**available / partial / not yet**), an honest indicator-demand count + a covered/partial/gap micro-bar;
  the list is **gap-priority** sorted (not-yet feeds lead — the data-access exposure). Click a data source →
  its indicators appear grouped by source document with a coverage gauge + an **"Implements capabilities"** row
  (the inverse of the capability view); click a document row to **drill into that doc's per-doc arc**, then
  **Back** returns to the data source (not the picker). No fabricated number — only honest counts + the
  always-on badge. (Sanity: the lens is genuinely distinct — at least one feed reads **"not yet"**.)
- [ ] **Corpus completeness + typology re-segmentation (Phase 33):** on Select, confirm the menu now shows
  **five** source groups — the new **"FINTRAC Sector Guidance (ML/TF indicators)"** group with **10 derived**
  pages (Financial entities, MSB, Real estate, Securities, Life insurance, DPMS, Casinos, Accountants, BC
  notaries, Virtual currency; Agents of the Crown shows non-derivable). The header stat reads **62 publications
  · 56 derived**. Pick **Financial entities** → it walks the full per-doc arc (a dense ~150-indicator doc) and
  the page **footer carries the FINTRAC Crown-copyright attribution** (never the US "public domain" line). On the
  **Typologies** toggle, confirm **Trade-based money laundering** appears as its own cluster (the re-segmented
  `ofac-sham-transactions`). No fabricated number; the new source is verbatim FINTRAC under the
  non-commercial licence; the always-on badge stays.
- [ ] **Per-indicator typology (Phase 37):** on the **Typologies** toggle, confirm the clusters group by
  INDICATOR typology — **no `fintrac-sector-baselines` cluster** remains; instead **`corruption`** and
  **`terrorist-financing`** are now **cross-jurisdiction (US + Canada)** clusters that draw indicators from the
  FINTRAC sector pages, and a **`cross-cutting-indicators`** bucket holds the generic sector-baseline indicators.
  Open the **corruption** synthesis → its rows list multiple FINTRAC sector pages (each contributing only its
  corruption indicators) plus any US doc; the framenote still says indicators are NOT de-duplicated/matched
  across regulators (no lift/overlap). The 56 derived records are byte-frozen — the typology rides in
  `data/indicator-typology-map.json` (350 deterministic corruption/TF assignments; the rest inherit the doc typology).

### Presenter notes + demo path (Phase 45 — the stakeholder walk)
- [ ] **Recommended route:** open on the landing (atoms are now seeded in the lead — say the word once here,
  it pays off on the lift screen) → Documents lens → walk **fin-2024-a002** (FinCEN 2024 fentanyl advisory:
  5 build-nows, and its lift beat shows **28 covered partners across FinCEN + FINTRAC** — the
  cross-jurisdiction payoff for a Canadian room) → back → **Typologies** lens for the synthesis beat →
  **Capabilities** lens briefly (the FINTRAC Crown-copyright attribution now renders in the footer here —
  point to it if compliance is in the room). For Canadian depth, a FINTRAC sector page (Financial entities /
  Securities) now renders its build recs in ≤2s (the stagger is capped) — safe to open live.
- [ ] **The gate is YOURS — perform it:** on Build recs the copy now says the agent has *proposed all N,
  pre-selected*. **Visibly deselect 1–2 rows** before advancing — that's the human-gate beat, and it also
  keeps the Signal screen at a presentable 2–3 spec cards instead of 30.
- [ ] **The second gate is narrated, not clicked:** on Signal, name the build-log's last step aloud —
  "and nothing deploys from here: it queues a backtest and routes to **Model Validation under E-23**" —
  that's gate two, off-screen by design.
- [ ] **The lift beat carries REAL numbers now:** the counts are the corpus's own covered-indicator
  inventory (the same honesty class as the lens counts). If asked "is that number real?" the answer is
  **yes** — what's NOT claimed is any lift/precision figure; that's the promotion gate's job. (The old
  illustrative 18→64→83 bars and their "pending calibration" disclaimer are gone from the corpus demo;
  the six-act showcase still has its own illustrative Act-5 — don't cross-reference them.)
- [ ] **Avoid as walk targets:** `fin-2021-a004` and `fin-2023-alert003` (zero build-now → an honest but
  anticlimactic back half; their picker chips lack the "· N build-now" suffix — that's the tell).
- [ ] **On the presentation machine:** open `dist/corpus/index.html` once over network BEFORE the room
  (warms the Google-Fonts cache; offline it falls back to system fonts — acceptable but flatter), then
  confirm offline reload still walks clean. Use **Back** (not the stepper's step 1) to return into a lens.

### Corpus LIVE derivation mode (Phase 46 — companion-served, dev/authoring-time ONLY)
- [ ] **The offline artifact is untouched:** `dist/corpus/index.html` contains NO `LIVE_START` marker and
  no `fetch(` (the harness asserts both; `--check all` stays 5/5). The live branch exists ONLY when the
  page is served by `python3 scripts/serve_corpus.py` (port 8010; full doc: `docs/corpus-live.md`).
- [ ] **If demoing live derivation** (off the presentation path by default): llama-server up → companion
  up → Select shows "＋ Derive a new document" → paste a converted advisory md → the processing page
  shows staged progress (token counts, never content) → gate-green indicators only → the entry lands in
  the "Live derivations (this session — UNREVIEWED)" group and walks the normal 6-screen arc. ~80–90 s
  for a 22K-char OA on the measured setup. Esc twice abandons honestly; nothing is ever persisted.
- [ ] **Never claim live output is reviewed/committed** — it is a proposal surface; committing a record
  to `data/` stays a separate human-reviewed act under the licence rules.

## Adverse-media / negative-news stream (`dist/news/`) — M8, Phase 31 + Phase 32
- [ ] **Automated arc:** `node tests/news-stream.test.mjs` exits **0** — drives the committed
  `dist/news/index.html` through the screening arc (Select → Read → Screen → Disposition → Exposure) +
  the fuzzy matcher under a dep-free DOM shim, both motion modes (**65 assertions** — reduced-motion final
  state + a full-motion enriched-shim drive of the stream + scan). Run after any `news.html` edit + rebuild
  (`python3 scripts/build.py news`); it doubles as a build-output smoke test.
- [ ] Open `dist/news/index.html` (`file://`): the **"Illustrative data & outputs"** badge is visible; the
  Select screen lists the **real enforcement articles** with an honest source chip (DOJ / OFAC) and stat
  tiles. A **step rail** (Select › Read › Screen › Disposition › Exposure) shows where you are. Pick the
  **OFAC TGR Group** article.
- [ ] **Read (streaming):** under full motion the source **streams in** (a blinking caret trails the read);
  each red-flag phrase **highlights** (amber) as the read reaches it and each named entity is **tagged**
  (green); **entity cards** reveal alongside with grounded **location / age / profession**, the **typology**
  is shown, a natural-AML `red_flag` translation sits beside each verbatim quote, and the **source
  attribution** (public domain, 17 U.S.C. §105) is shown. Reduced-motion shows the same final state at once.
- [ ] **Screen (scan process):** the book is **swept** — each entity scored against every row, ranked across a
  **threshold line**. **Siam Expert Trading Company Limited = 1.000 (EXACT)** — a counterparty *is* a
  designated entity; near-matches an exact-name screen would miss surface too (**Pullman ≈ 1.000** suffix,
  **Ekaterina Zhdanova ≈ 0.989**). No percentage / precision figure is shown.
- [ ] **Disposition (the human gate):** hits default to **CONFIRMED**; the common-name collision
  **George Rossi (1.000)** is present with its dismiss note — click it to **DISMISS** it (a different person;
  high score ≠ confirmation). Toggles respond to click and to Space/Enter when focused; ←/→ still navigate.
- [ ] **Exposure:** after dismissing the trap, **confirmed = 3, dismissed = 1**; the confirmed hits are
  framed as adverse-media **atoms** (the compose-with-the-transaction-signal north star is named).
- [ ] Keyboard: **→ next · ← back · Esc** returns to the article list. No console errors (both motion modes).
- [ ] Compliance: the source **articles are real US-federal public-domain enforcement records** (DOJ + OFAC,
  verbatim under 17 U.S.C. §105); the client/counterparty **book is synthetic** (no real customer data);
  scores are real computed similarity; nothing reads as a real detection/precision rate.

### Live mode (Phase 35 extraction + 36 persistence + 38 entity-precision/watchlist-view + 39 progress/URL + 40 flag-quality + 41 entity-resolution + 42 network/dossier + 43 size-robustness/staged-rendering, optional — needs a local llama-cpp server; see `docs/news-live.md`)
- [ ] **Automated (no model):** `python3 tests/news_live_test.py`, `python3 scripts/news_ground.py --selftest`,
  `python3 scripts/news_fetch.py --selftest`, and `python3 scripts/serve_news.py --selftest` all exit **0**
  (the grounding gate, the build_record pipeline, the `/extract` NDJSON stage stream + one-shot URL route
  with the model/acquisition stubbed, the URL standardizer/verifier/ladder, and the served live page). Under
  the **`.venv`** (`.venv/bin/python tests/news_live_test.py` + `.venv/bin/python scripts/news_store.py --selftest`
  + `.venv/bin/python scripts/news_fetch.py --selftest`) the DuckDB store + the `/watchlist` + `/disposition`
  escalated-only loop + parquet roundtrip + a real markitdown fixture conversion are exercised too.
- [ ] **Offline artifact still pure:** `dist/news/index.html` contains **no** `fetch(` / `liveInit` /
  `LIVE_START` / `/watchlist` / `/disposition` / `NEWS._watch` / `watchpanel` / `livePrune` / `liveReadStream` /
  `live-url` / `live-stype` / `liveBestPair` / `Subject map` / `liveGraphLayout` / `netsvg` / `dosspanel` /
  `/anchor` (the live + persistence + watchlist-view + progress/URL + Phase-41 enrichment + Phase-42
  network/dossier code is build-time stripped); it opens
  standalone as the scripted fallback, screening the static book only.
- [ ] **Live (with a model):** start llama-cpp, then `python3 scripts/serve_news.py --llm-url <endpoint>
  --model <name>`; open **http://localhost:8000**, click **＋ Process a new article**, paste a public-domain
  enforcement article, **Run extraction** → entities + red flags appear in the streaming Read, each **grounded**
  in the pasted text (ungrounded items are dropped; the status line reports how many), then the normal
  Screen → Disposition → Exposure arc runs. Pasting gibberish returns an honest "nothing grounded" message,
  never a fabricated record.
- [ ] **Extraction progress (Phase 39):** during a run the status line paints **live stages** — model
  extraction → grounding → **"Verifying entity i of N — <name>"** per entity — with an **elapsed-seconds**
  counter ticking; on completion it reports counts + total seconds. No silent multi-minute wait.
- [ ] **Size robustness + staged rendering (Phase 43):** during the model call the status line ticks
  **"… N tokens generated"** (the transport streams; a long generation does NOT die at a fixed deadline —
  a 30K+-char document legitimately runs past 3 minutes and completes). The moment grounding completes,
  the **preview panel** under the form reveals the **red flags as FINAL** (badge: *final* — the gate has
  disposed) and the **entities as PROVISIONAL chips** that refine live through the verify pass (current
  chip highlighted; dropped chips strike through; kept chips turn amber). A second concurrent **Run
  extraction** (second tab) answers an honest **"another extraction is already running"** — never two
  silent half-speed runs. An absurdly oversized paste refuses up front with a **named token overage +
  the `--ctx-size` remedy** (when the model server is misconfigured small), never a silently truncated
  "clean" record.
- [ ] **Processing page + requote grounding (Phase 44):** clicking **Run extraction** takes over the
  viewport with the **dedicated processing page** (source line · live stage banner with elapsed/token
  counter · the staged grounded-flags/provisional-chips reveal); on completion it closes onto the Read
  screen. Mid-run, **←/→/Space do nothing** (presenter keys guarded) and **Esc warns first, Esc again
  abandons** ("nothing was saved"). Paste a HARD-WRAPPED note (or the committed synthetic
  `docs/demo-investigation-note.md` reflowed) containing a high-risk-country wire sentence spanning
  lines — the wire flag surfaces GROUNDED (pre-44 it silently dropped "not raw-grounded"); the
  highlighted quote in Read matches the article bytes exactly. A bare shared surname beside two full
  names is NOT folded as anyone's alias (an honest "ambiguous alias … not folded" drop in the
  companion log), and `python3 tests/news_quality_harness.py --check` reports CHECK OK.
- [ ] **Flag quality (Phase 40):** on a substantial enforcement article the extracted red flags read as
  **distinct mechanisms** (no same-quote duplicates — the gate collapses them; no per-anecdote flag storms),
  include **institutional/control-failure** flags where the article describes them (not only transactions),
  and each `red_flag` is a terse mechanism-named translation distinct from its verbatim quote.
- [ ] **One-shot URL (Phase 39):** put a public **article URL** (e.g. a justice.gov or treasury.gov press
  release) in the URL field, **Run extraction** → "Fetching + converting" paints, the **converted text fills
  the textarea** as the run proceeds, and the grounded record opens (source link = the URL). Trimming the
  textarea and re-running uses the trimmed text (paste wins over URL). A walled/non-article URL fails
  **honestly** with "…paste the article text instead" — never a loosened gate, never a fabricated record.
- [ ] **Persistence + the feedback watchlist (Phase 36, run the companion under `.venv/bin/python`):** scan
  an article, then at **Disposition** click **＋ WATCHLIST** to **escalate** an entity that is *not* in the
  book (its label flips to **ESCALATED**). Process a **second** article that re-mentions that entity → at
  **Screen** it now surfaces as a hit against the watchlist, provenance *"escalated from &lt;first article&gt;"* —
  the screen surface compounds. Dismissed / never-escalated entities do **not** join the watchlist. The store
  lives at `data/news/.live/store.duckdb` (gitignored); `--export-parquet <dir>` writes the parquet interchange.
- [ ] **Entity precision (Phase 38):** scan a real enforcement article (e.g. a DOJ press release) → the
  extracted **entities are the *subjects*** (defendants, designated parties, their companies), **not** the
  announcing officials / prosecutors / investigating agencies / courts named in the article (the subjects-only
  prompt + the keep-biased second pass; the companion prints `entity-verify ON`). `--no-verify-entities`
  disables the second pass.
- [ ] **Watchlist view + prune (Phase 38):** after escalating an entity, the **Feedback watchlist** panel on
  **Select** lists it with provenance *"escalated from &lt;article&gt;"*; click **✕ Prune** → it leaves the
  panel and the screening surface (the book is untouched). Empty surface shows "No escalated entities yet".
- [ ] **Entity resolution (Phase 41):** scan a real enforcement article with a.k.a. names → at
  **Disposition** the **Subject map** panel names the main subject(s) (multi-defendant cases show several;
  none is forced) and lists relationship edges (`A —label→ B`) each with its *verbatim evidence quote*;
  entity cards show an **a.k.a.** line + **property chips** (only values literally printed in the article —
  zero-property entities are normal, nothing invented). Pick a **source type** at submit
  (gov-enforcement / commercial-news / investigation-note) → an escalated entity's watchlist provenance
  carries it. Escalate an entity that has an alias, scan a second article mentioning **only the alias** →
  Screen hits via the alias (`via` shown); a single-token alias or @-handle hits on **exact** name only,
  never fuzzily. Private investigation notes stay local: gitignored DuckDB, 127.0.0.1 model — and the
  replay-fixture allowlist (`FIXTURE_META`) blocks any non-US-federal capture from being promoted.
- [ ] **Network view + anchor dossier (Phase 42, run under `.venv`):** scan an enforcement article → at
  **Disposition** the Subject map renders as an **SVG network** (main subjects highlighted + central;
  edges carry their vocab labels); clicking an **edge** (svg or list row) reveals its verbatim evidence
  quote (closed by default); clicking a **node** — or a watchlist row name on Select — opens the **Anchor
  dossier**: every scan that touched the entity with source-type provenance, properties grouped by kind
  with per-scan provenance, accumulated aliases, relationship edges. Run the **canonical demo flow**
  (`docs/news-live.md` "Demo: anchor accumulation"): article scan + `docs/demo-investigation-note.md` as
  *Investigation note* → the shared entity's dossier shows **2 scans**, the note's `client_number`, and
  the conflicting phone values flagged **"conflicting values — both kept"** (coexisting claims, never
  auto-resolved). An unscanned entity's dossier reports "No anchor yet" honestly; with persistence off
  the dossier reports the store unavailable (never a crash).

## Walk the six-act arc (Next / Back) — read values from the table
- [ ] **Act 0 — Blind spot:** coverage map renders; gauge animates to the **table value**; red (not-covered) rows visible
- [ ] **Act 1 — Read advisory:** advisory text streams with highlighted phrases; candidate signals appear staggered, count climbs
- [ ] **Act 2 — Assess coverage:** matrix renders; "build now" flags on the gap+data-available rows
- [ ] **Act 3 — Human review (GATE 1):** Next is **disabled with zero selected**; selecting a candidate enables it; label reads "Build selected (N) ›" *(shared)*
- [ ] **Act 4 — Agent builds (GATE 2):** spec card shows `PROPOSED · <table signal name>`; build log auto-advances to "Await human confirmation"; **Next confirms** → "Building…" → advances
- [ ] **Act 5 — Combination lift:** fire-stats animate to the **table values**; three lift bars grow weak→mid→strong to the **table values**
- [ ] **Act 6 — Loop closes:** gauge animates the **table delta**; the **table delta chip** shows; recap chips render

## Presenter controls (M3 — keyboard nav, reset)
- [ ] **→ / Space** advances; **←** goes back — but **both gates still hold** (→ does nothing on Act 3 with zero selected, or on Act 4 before confirm)
- [ ] **Esc** resets to a clean Act 0 (selection cleared, gauge back to the base table value)
- [ ] On-screen **↺ Reset** control does the same as Esc; the key legend is visible
- [ ] Stepper rail: clicking a reached step jumps to it
- [ ] On Act 6, Next reads "Run again ↺" and returns cleanly to Act 0 with selection reset

## Reduced motion (M3 — `prefers-reduced-motion`)
- [ ] With OS "Reduce motion" **on** (macOS: System Settings → Accessibility → Display), reload from `file://`
- [ ] Every act lands in its **final state in one paint** — no animation, gauge/stats/bars show final table values immediately; no pending timers left running

## Offline / reliability
- [ ] Disconnect network, reload `dist/<id>/index.html` from `file://` — still runs; fonts fall back to system serif/sans/mono (no layout break)
- [ ] No console errors during a full run (check with reduced-motion **on** and **off**)
- [ ] Cross-browser: confirm on the **actual presentation browser** (target: Chrome / macOS)

## Compliance (hard gate — see T3 / HANDOFF §4)
- [ ] Every figure is illustrative; nothing reads as a real customer/transaction number
- [ ] Advisory text is **paraphrased + public-source**, and the footer/source line attributes it:
  - `fentanyl`: FINTRAC Operational Alert on illicit synthetic opioids (Jan 2025)
  - `trade-based`: FinCEN Alert on fentanyl-linked trade-based laundering (Apr 2025) · FATF TBML trends & developments (2024)
- [ ] No secrets/keys anywhere in the shipped file

---

## M5 ship — compliance self-check record (automated, 2026-06-04)

Deterministic gate run against both shipped `dist/<id>/index.html`. **Result: PASS.**

- ✅ Zero drift — now an automated guard (see **Build & open** above): `build.py --check all` confirms every committed `dist/<id>/index.html` equals a fresh build; `git status --porcelain dist/` clean (shipped = source = HEAD).
- ✅ Badge `Illustrative data & outputs` present in both (persistent header chrome → on every act).
- ✅ Self-contained for `file://`: no `<script src>`, no `fetch()`, no unresolved `__CONFIG__`; `const CONFIG` inlined; boot `goto(0)` present. Only external ref is the Google Fonts `<link>` (degrades to system fonts offline).
- ✅ Advisories paraphrased + public-source, attributed in both (fentanyl: FINTRAC Jan-2025 · trade-based: FinCEN Apr-2025 / FATF TBML 2024).
- ✅ No secrets/keys; no real-data/PII (no emails, no ≥9-digit runs, no card/SSN patterns). All figures are config-sourced illustrative numbers.
- ↪ Runtime render (Act 0, no console errors) was verified on real Chrome 149 × both motion modes at **M3**; these dist bytes are unchanged since (zero drift), so that pass carries. Re-run the live walk above before any presentation.

---

## Gate console (Phase 47 — `dist/console/index.html`)

- [ ] Open `dist/console/index.html` offline from `file://` — Queue renders 213 cases grouped by changed axis (C / D / both); the "Illustrative data & outputs" badge is visible on every screen
- [ ] Walk one FINTRAC case end-to-end: Evidence shows the verbatim flag beside the red-flag translation, Assessment A/B presented NEUTRALLY (nothing hints which is the correction); the page footer carries the © His Majesty FINTRAC attribution for the on-screen doc
- [ ] Disposition with an EMPTY rationale is blocked with an honest message; a graded disposition + rationale records, and ONLY THEN does the adjudicated record reveal ("precedent, not a score" framing — no right/wrong language)
- [ ] The one US case (fin-2019-a006): footer renders exactly empty (public domain — no attribution required)
- [ ] Ledger accumulates the session's dispositions; Export produces valid JSON containing the typed rationale; reload loses everything ("persists nothing" stated on screen)
- [ ] Keys ←/→/Esc/↺ navigate; typing in the rationale textarea does NOT trigger key nav; reduced-motion mode lands each screen in one paint

---

## Triage console (Phase 49 — `dist/triage/index.html`)

- [ ] Open `dist/triage/index.html` offline from `file://` — Queue renders 20 scenarios grouped by the 4 §14 strata with honest stratum descriptions; the "Illustrative data & outputs" badge is visible on every screen; nothing on the queue reveals which scenarios are controls
- [ ] BELIEVABILITY READ (the A3 gate check): read 4 evidence panels, one per stratum (e.g. S-01 signal-fired · S-08 below-the-line · S-11 novel · S-15 random-population) — each should read like a real triage moment, not template filler; the divergent pair S-01/S-02 shows the IDENTICAL fact pattern (shared panel)
- [ ] Disposition gate: empty rationale blocks with an honest message; need-more-info without a C/D pick blocks; need-more-info + rationale + a D-code records and lands in the ledger's data-gap stream under that code
- [ ] The reveal appears ONLY post-disposition: history framed "decisions, not correctness"; S-01 or S-02 surfaces the process inconsistency (shared panel, divergent historical dispositions — "surfaced for adjudication, never auto-resolved"); a double-assigned scenario replays the SEEDED synthetic second rater with its label visible
- [ ] Discovery ledger: every number derived at render with a "definition:" line (signal gaps from fired-rule state; agreement X/Y vs the seeded raters — consensus-class wording); design parameters boxed "chosen, not measured"; Export produces valid JSON; reload loses everything ("persists nothing" stated on screen)
- [ ] Keys ←/→/Space/Esc navigate; typing in the rationale textarea or the C/D picker does NOT trigger key nav; reduced-motion mode lands each screen in one paint

---

## Launcher + cross-pillar chain (Phase 55 — `dist/index.html`)

- [ ] `python3 scripts/build.py launcher` builds; open `dist/index.html` offline from `file://` — the "Illustrative data & outputs" badge is visible; the five artifact cards link (relative) to fentanyl/trade-based/elder/corpus/news/console/triage and each opens its self-contained artifact
- [ ] The "3-pillar program chain" panel renders the three bridge states from the inlined `data/pillar-status.json` — today all read **pending** (honest: spine built, real chain gated); the meta line shows the spine state + both grounding HEADs
- [ ] `python3 scripts/e2e_chain_check.py --selftest` PASSES (good C4 fixture pair connects; the broken fixture is caught); `--real --substrate /nope --casework /nope` prints an honest `GATED: sibling output absent` and exits non-zero
- [ ] `python3 scripts/build.py --check all` → 8/8 zero drift (the 5 existing artifacts byte-identical; the launcher reproducible); `node tests/launcher.test.mjs` green
- [ ] Full presenter script: `docs/e2e-walkthrough.md` (the two beats); acceptance contract: `docs/e2e-acceptance.md`

---

## Chain workbench (Phase 56 — dev-time companion, dist-free)

> The analyst UI for the substrate→casework→verify chain. NOT a ship artifact — companion-served, never built into `dist/`. Full recipe + two-beat framing: `docs/chain-workbench.md`.

- [ ] `python3 scripts/serve_chain.py --selftest` PASSES offline (casework consume STUBBED): cases listed, a run streams `evidence → consume → verify → connected` to CONNECTED, audit walk grounds every alert, `data/pillar-status.json` byte-stable (no launcher drift), gated/unknown-case paths named
- [ ] `node tests/chain.test.mjs` green (stage-rendering contract, the four-node ledger, six completeness chips, CONNECTED payoff + flag→corpus walk, badge, XSS-escape, line-buffered NDJSON); `python3 scripts/validate_chain_cases.py --selftest` green (vendored library + tamper/drift catch)
- [ ] ISOLATION: `! grep -nE "chain\.html|serve_chain" scripts/build.py` · `! grep -nE "import aml_substrate|import aml_casework" scripts/serve_chain.py` · `python3 scripts/build.py --check all` → 8/8 (offline dists byte-identical; chain.html not in `dist/`)
- [ ] LIVE walk: start `serve_chain.py`, open `http://localhost:8020`, pick `CASE-P-0010361` → Run → the four stages reveal to CONNECTED; the always-on "Illustrative data & outputs" badge is visible; without creds the header chip reads **deterministic stub**; the key never appears in the page source

## Chain workbench — pluggable drafter backends (Phase 57)

> The neural draft goes multi-backend: claude (OAuth/key) · openai (`/v1`) · opencode (agent loop) · stub. serve_chain selects by NAME, creds stay server-side. Full table + recipe: `docs/chain-workbench.md`.

- [ ] `python3 scripts/serve_chain.py --selftest` PASSES the N-backend assertions: availability per server-side env, the name pass-through + honest fallback (unknown/unavailable → stub with a named note), and **no cred/endpoint leaks** into the served config or page (§4.5); the casework pin re-grounded to `@2381d71` in `data/pillar-status.json` + `e2e_chain_check.py`
- [ ] `node tests/chain.test.mjs` green incl. the Phase-57 set: the **picker** renders a button per backend (unavailable ones disabled + "n/a"), `pickBackend` selects only available backends, the picked NAME is POSTed to `/run`, the live-draft label + the honest requested→effective fallback note, the **stub-vs-neural comparison** (both narratives, each gated), XSS on a compared narrative
- [ ] LIVE backend walk (keyless): pick **stub** → Run → CONNECTED; then (with `ANTHROPIC_AUTH_TOKEN`/`ANTHROPIC_API_KEY` set) pick **claude** → Run → a real neural SAR, gated by the six verifiers → CONNECTED; run both on the same case → the **Drafts compared** panel shows both, each gated. The gate verdict line ("the gate is the oracle") shows on every consume stage
- [ ] GATED backends: with `OPENAI_BASE_URL` / `OPENCODE_SERVE_URL` set, the **openai** / **opencode** buttons become selectable; until the casework `drafter_openai.py` / `drafter_opencode.py` adapters land (briefs in `aml-casework/docs/`), a Run on them fails honestly in-stream (named "drafter error → fell back to the stub"), never a faked connection
- [ ] `python3 scripts/build.py --check all` → 8/8 (only `dist/index.html` moved with the re-grounded pin; the other 7 dists byte-identical); no cred/endpoint string ever appears in any `dist/` file

## Investigator case workbench (Phase 63 — dev-time companion, dist-free)

> The capstone demo: clutter → clarity → live decision over a REAL (synthetic) substrate alert population. NOT a ship artifact — `workbench.html` companion-served by `scripts/serve_workbench.py`, never built into `dist/`. Full walkthrough + the cross-pillar finding: `docs/case-workbench.md`.

- [ ] `python3 scripts/curate_workbench_cases.py --selftest` PASSES: the committed slice is schema-valid, the 4 exemplars (mule/ambiguous/fp_trap/thin) span the gate levels, `grounds_e2e` is present per case, and MEASURED `coverage` (57/200) matches the per-case `grounds_e2e` count; the confidence gate is monotone in the precedent sample size
- [ ] `python3 scripts/serve_workbench.py --selftest` PASSES offline (casework STUBBED): the queue (gate funnel + coverage, no txn bodies), a case detail's full clutter + the grounded signal walk, the live finale streams `evidence → consume → verify → connected` (signed → CONNECTED), the **fail-closed** path is a disposition (escalate, verify skipped, violations carried) NOT a crash, **no cred/endpoint leaks** (§4.5), `data/pillar-status.json` byte-stable
- [ ] `node tests/workbench.test.mjs` green: the population strip + gate-filtered queue, the dense clutter view (KYC/accounts/channels/counterparties/txn table), the **signals-on reveal** (risk picture + precedent read + audit walk + cited-txn highlight), the **live finale** (signed SAR + the fail-closed escalate climax), the grounds indicator, XSS-escape, both motion modes, and **NO catch-rate/precision/lift/% number** in any rendered surface
- [ ] ISOLATION: `! grep -nE "workbench\.html|serve_workbench|data/workbench" scripts/build.py` · `! grep -nE "import aml_substrate|import aml_casework" scripts/build.py` · `python3 scripts/build.py --check all` → 8/8 (workbench is dist-free; ZERO dist drift)
- [ ] LIVE walk: build the population (`curate_workbench_cases.py --from … --measure-casework ../aml-casework`), start `serve_workbench.py`, open `http://localhost:8030`; the queue shows ~200 cases + the gate funnel; toggle **Signals** on a composed mule → the risk picture + grounded audit walk reveal (badge visible, no catch-rate number); **Decide** the mule → fail-closed → escalate (the C3/C15 refusal reasons shown); Decide the **thin** signer → a signed SAR. Without creds the drafter chip reads **deterministic stub**; the key never appears in the page source

### Gating engine + elicitation loop (Phase 64 — the precedent-confidence display made a live control)

> The Phase-63 confidence display becomes a LIVE parameterized routing control + an adjudicate→grow-precedent→re-route loop. §12-grounded routing / §14-illustrative disposition. Companion-only; nothing persists. Detail: `docs/case-workbench.md` (the gating-engine section).

- [ ] `serve_workbench.py --selftest` (same run as above) ALSO covers the GATE engine: the live `route()` reproduces the baked **129/52/19** funnel from the policy defaults + is **monotone** (a larger precedent never yields a stricter gate); a custom-knob policy re-derives a complete funnel; an invalid knob (`high<medium`) is a NAMED 400. And the LOOP: one adjudication of a near-threshold combo re-routes human-gate→review, the session precedent grows by exactly 1, a bad disposition is rejected (no mutation), and **`cases.json`/bundles are byte-identical after the loop ran** (persists nothing)
- [ ] `node tests/workbench.test.mjs` ALSO green on the GATING arc: the gating panel + the two **policy knobs** (auto-clear/review thresholds, framed as "prior firings", "chosen, not measured"), the live funnel (reproduces the baked one), dragging a knob re-derives the funnel + re-routes the queue live, the **adjudication control** (cleared/escalated/needs-more-info), the loop re-route (human gate → review) + the grown precedent read + the session count, and the honesty re-check (**counts only — no %/lift/precision** on the gating surfaces)
- [ ] LIVE walk (gating): drag **Review at ≥** down a notch → watch the human-gate funnel shrink live (the queue dots re-route); select a **human-gate** case, Signals on → the gating read shows its real precedent + routing; click **Adjudicate → cleared** a few times on a near-threshold pattern (e.g. the `C3+C5` case, 45 prior firings) → it crosses to **review**, the funnel ticks 19→18, the read shows "N recorded this session". The disposition direction is labeled **illustrative**; nothing is written to disk (refresh resets the session)

### Agentic evidence-gathering loop (Phase 65 — the GATHER beat over a synthetic OSINT corpus)

> The GATHER beat: signal-watch's first multi-step tool-calling agent loop gathers counterparty/OSINT/sanctions evidence over a COMMITTED SYNTHETIC corpus; every finding is **grounded-or-stripped** (CONSISTENCY — the quote is a real substring of a synthetic record — NOT correctness). Companion-only; nothing persists. Detail: `docs/case-workbench.md` (the agentic evidence-gathering loop).

- [ ] `python3 scripts/osint_tools.py --selftest` PASSES: the committed `data/osint/corpus.json` validates (closed kinds, globally-unique ids, the synthetic disclaimer present, no banned metric token); the tools are deterministic + exact-normname; the gate KEEPS a grounded finding and DROPS every bypass (trivial/punctuation/one-token quote, ungrounded quote, cross-sentence bridge, ungrounded entity/link, wrong record-id); the stub loop chains registry→sanctions, the fp_trap is an honest negative, and a gather **persists nothing** + the transport error is sanitized (no host/url)
- [ ] `serve_workbench.py --selftest` ALSO covers the GATHER endpoint: a stub gather over the mule KEEPS grounded findings + DROPS the planted ungrounded one + builds a grounded network; the stages stream `backend → plan → tool → findings`; `cases.json`/`data/osint/corpus.json` byte-identical after (persists nothing); **no cred/endpoint reaches the browser via ANY gather NDJSON stage** (§4.5)
- [ ] `node tests/workbench.test.mjs` ALSO green on the GATHER arc: the **"Gather evidence (synthetic OSINT corpus)"** button + the always-visible synthetic-provenance string, per-tool **stage-completion** reveal (never a token stream), each grounded finding's **verbatim quote as evidence beside a labelled illustrative synthesis**, the gate's rejection shown WITH its reason, the **authored-not-discovered** network SVG (edge-click reveals evidence), the honest-empty payoff, XSS-escape, and the honesty re-check (**no %/lift/precision** over the gather HTML)
- [ ] ISOLATION: `! grep -nE "import (aml_substrate|aml_casework|news_store)" scripts/osint_tools.py` · `! grep -nE "osint_tools|serve_workbench" scripts/build.py` · `python3 scripts/build.py --check all` → 8/8 (the OSINT corpus is consumed by NO ship target; ZERO dist drift)
- [ ] LIVE walk (optional, a local `/v1` model up): set `OPENAI_BASE_URL`, pick the **openai** backend, **Gather** the mule → the chain fires (registry → the discovered affiliate → the sanctions hit); every finding shows a grounded quote, the synthesis is labelled **illustrative — not verified**, the badge is visible; without a model the stub runs deterministically and the key never appears in the page source
