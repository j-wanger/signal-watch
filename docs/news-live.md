# News stream — live local-model mode (Phase 35–41, M8)

Optional, dev/authoring-time **live mode** for the adverse-media news stream: give an article URL (or
paste the text) and a local model extracts entities + red flags in **real time**, grounded against the
source, with **live stage progress** streamed back as it works. It is NOT part of the ship artifact —
the offline single-file `dist/news/index.html` stays the default and the scripted fallback (it makes no
network call; the live branch is build-time stripped from it).

## Architecture
```
http://localhost:8000/         serve_news.py (stdlib companion) — serves news.html WITH the live branch
  ├── GET  /                   the page (NEWS.live set → "＋ Process a new article" control on Select)
  ├── GET  /health             {"ok": true, "persist": <bool>}
  ├── GET  /watchlist          book ∪ escalated entities (reconciled + provenance) — the live screen surface
  ├── POST /extract            {url|text} → [acquire+convert] → llama-cpp → JSON-schema → GROUND → 2nd-pass
  │                            entity verify → record → PERSIST; answers an NDJSON STAGE STREAM (Phase 39)
  ├── POST /disposition        {scan_id, entity_id, decision} — 'escalate' adds the entity to the watchlist
  └── POST /watchlist/prune    {name} — un-escalate (remove) an entity from the watchlist (Phase 38)
          │  same-origin (no CORS)                         │
          ▼                                                ▼
  llama-cpp /v1 (your Qwen model) — proxied        data/news/.live/store.duckdb  (DuckDB; gitignored → parquet)
```
The model **proposes**; `news_ground.ground_record` **disposes** — every entity name, attribute, and
red-flag `flag` must quote-ground in the submitted article (the same gate `build.py` uses at build time),
or it is dropped. Nothing is shown that isn't in the source. Fuzzy screening stays the real client-side
Jaro-Winkler matcher against the **synthetic** book ∪ the escalated watchlist (Phase 36, below).

## Persistence + the feedback watchlist (Phase 36, escalated-only)
Each live scan is row-appended to a local **DuckDB** store (`data/news/.live/store.duckdb` — gitignored
runtime data, never committed, never on the ship path; DuckDB is a `.venv`-only dep, owned by the
companion-only `scripts/news_store.py`, which `build.py` never imports). The **Disposition gate is the
feedback loop**: escalating an entity (`POST /disposition … "escalate"`) marks it in the store, and
`GET /watchlist` then returns **book ∪ the escalated entities** (deduped by name, with provenance). The
Screen step scores each new article against that growing surface — so an entity you escalate from one
article is caught when it resurfaces in the next (shown as *"escalated from &lt;article&gt;"*). The
watchlist is **escalated-only** — a curated surface, not every name ever seen; dismissed / never-escalated
entities never join it. Export the store to parquet (the interchange format) any time:
```
.venv/bin/python scripts/serve_news.py --export-parquet data/news/.live/export
```
Persistence needs DuckDB, so run the companion under the `.venv` for the watchlist. Without it (or with
`--no-persist`) the companion still serves + extracts, screening the static book only (no growth).

## Entity precision (Phase 38)
A model asked for "every named org/person" over-extracts the **announcing officials, prosecutors,
investigating agencies, courts, and programs** named in an enforcement article — not the *subjects*. A
stress test over fresh DOJ/OFAC articles showed an enumerated denylist can't scale to that open
vocabulary (it overfit its calibration set). Two controls instead, in order of leverage:
1. **Context shaping — the lever.** The extraction system prompt carries a **SUBJECTS-ONLY** rule
   (extract only perpetrators / defendants / designated parties / the companies-accounts-aliases they
   used; exclude officials/prosecutors/agencies/courts/programs). One rule cut the institutional noise
   ~90% and *generalizes*.
2. **A keep-biased second pass — the backstop (on by default).** Each grounded entity is re-checked with
   a focused, **keep-biased** per-entity question (`serve_news.verify_entities`): drop only when *clearly*
   an official/agency/court; when in doubt, KEEP (missing a real subject is the costlier error). It
   **fail-OPENs** (an unreachable verifier keeps the entity) and only ever *drops* — so the grounding
   gate's faithfulness floor holds. Measured: it removes the residual the prompt misses with **zero
   subject loss**. Disable with `--no-verify-entities` (one extra model call per extracted entity).
   The verify is LIVE-only; it layers on top of the deterministic `build_record` core, which the offline
   replay fixtures pin.

Structurally, a small deterministic pass (`news_ground.screen_entities`) still removes source-attribution
publishers and judicial officers. Since Phase 41 the surname-alias duplicates and *structurally adjacent*
`@handles` (printed right after a parent's name) **FOLD into the parent entity's `aliases`** instead of
dropping — the article's own name variations are entity-resolution signal, not noise (the fold is
audit-trailed with a `folded_into` key; an orphan handle with no adjacent parent still drops).

## Watchlist view + prune (Phase 38)
The escalated-only watchlist is now **visible and manageable** on the Select screen: a panel lists each
escalated entity with its provenance (*"escalated from &lt;article&gt;"*) and a **✕ Prune** control that
`POST`s `/watchlist/prune {name}` to un-escalate it (the audit row is retained; the book is never
touched). Companion-only — stripped from the offline `dist/news` like the rest of the live region.

## Red-flag quality (Phase 40, measure-first)
Flags always passed the deterministic faithfulness gate, but completeness / span quality / translation
register / granularity were unguarded — and on long **commercial** articles the model extracted only ~40%
of what a blind second rater found (vs 67% on federal enforcement summaries), with per-article flag counts
swinging 4–29. Measurement first (the Phase-38 playbook applied to flags):
- **Method.** A 12-article commercial stress corpus (selected deterministically from a local negative-news
  store; calibration/holdout split; **local-only, never committed**) + the 7 federal fixture articles, each
  extracted live and compared against a **blind second-rater reference extraction**. Reported as
  **inter-rater agreement / coverage-of-the-other-rater — consensus, never ground truth**; divergence
  clusters human-adjudicated. No accuracy number is real here.
- **Findings.** The misses concentrated in (1) early-stop with positional decay on narrative longreads,
  (2) an **institutional/control-failure blind spot** (the old prompt's examples were transactional-only),
  (3) per-anecdote over-extraction on enumerated content, (4) a latent prompt/gate bounds drift
  (12–200 stated vs [12,240] enforced).
- **The fix is the prompt (context shaping, again the lever).** The red_flags contract now carries a
  **20-family mechanism CHECKLIST** (a coverage net: scan the whole article once per family — includes
  *institutional control failure* and *misrepresentation to regulators*), a **granularity contract** (one
  flag per distinct behaviour; retellings merge; narrow merge rule), tightest-span guidance, register
  exemplars, and the [12,240] bounds. Three calibration rounds; the accepted round measured on the
  **untouched holdout**: coverage-of-reference 0.40→0.55, agreement 0.54→0.62, mechanism-family coverage
  0.46→0.63, **positional decay eliminated** — with the federal layer unregressed (0.73→0.74 agreement).
  A planned per-flag precision verify was **dropped** (measurement showed the residue was recall, not
  precision); a sectioned-extraction fallback was **skipped-with-reason** (its trigger — persisting decay —
  did not fire).
- **One measurement-earned gate rule.** `news_ground.ground_record` now collapses **duplicate flags**
  (same quote + same category; the first survives — deterministic), and build.py's `validate_news_data`
  CHECKS the same key (fail loud, never rewrite). Same quote under a *different* category is kept — one
  sentence can ground two mechanisms. No span caps, no topic rules: semantic dedup of *reworded* retellings
  stays a known prompt-side residue, not a gate rule (the Phase-38 overfit lesson).

## Entity resolution (Phase 41)
The live scan now produces **resolution-grade identity records**, designed for the system's real input
domain — including **private investigation notes** — not just public articles:

- **Schema.** Entities carry `aliases[]` (verbatim) and `properties[]` `{kind, value}` from a closed
  kind vocab (`address, phone, email, client_number, account_number, dob, id_registration, wallet,
  domain` — authority: `news_ground.PROPERTY_KINDS`); the record carries `relationships[]
  `{from, to, label, evidence}` (closed label vocab `news_ground.RELATION_LABELS`; the **label** is
  vocab-checked, never correctness-checked — the C/D-code honest split) and `main_subjects` (honest
  none/multiple — never a forced single pick). `red_flags` come **FIRST in schema order**: measured,
  the enriched one-call prompt with flags last cost ~12.5% kept flags on a 3-article regression set;
  flags-first restored it (24→25 kept vs the Phase-40 captures).
- **Gate (shared, deterministic).** Aliases RAW-ground like names; property values NORMALIZE-ground
  (tolerant of the article's line-wrap/punctuation variance around an identifier, still rejects
  derived/canonicalized forms — canonicalization is post-gate work, never gated); relationship
  `evidence` RAW-grounds like a flag quote + `from`/`to` referential integrity; everything
  grounded-or-stripped.
- **Store (the anchor design).** `anchors` is the identity spine (exact-normalized name → ONE anchor;
  cross-scan properties ACCUMULATE; fuzzy merge adjudication deferred); ONE monolithic
  `entity_properties` association table — per-row scan provenance, NON-destructive (two conflicting
  DOBs are BOTH kept and surfaced, never auto-resolved), `confidence` RESERVED/NULL (no model-emitted
  confidence — a fabricated-shaped number); `entity_relationships` edges; `scans.source_type`
  (gov-enforcement / commercial-news / investigation-note — document types differ in significance).
- **Screen (alias-aware).** Matches **name ∪ aliases**, max pair score, CLASS-AWARE: a single-token
  alias ("Smith") or an `@handle` matches **exact-normalized only** — never fuzzy (guards the 0.85
  threshold against a false-positive flood); multi-token aliases fuzzy-score like names. Alias hits
  report the `via` pair for the analyst.
- **UI.** A source-type selector at submit; the Disposition gate renders the **subject map** (main
  subject(s) + evidence-quoted relationship edges) and identity cards (a.k.a. line + property chips).
- **Privacy boundary — by CHECK, not convention.** Private/client data stays in the local live layer
  (gitignored DuckDB; the 127.0.0.1 model means notes never leave the machine). Fixture promotion is
  blocked by an allowlist assert: every replay fixture's base id must be in the committed US-federal
  `FIXTURE_META` registry.
- **Honest residual.** The kind↔value semantic fit is neural and unguarded (a grounded value can sit
  under the wrong kind — observed once: `dob = "born in Russia"`); the gate guards vocabulary +
  grounding only, like relation-label correctness.

## Network view + anchor dossier (Phase 42)
Phase 42 CONSUMES the Phase-41 model (read-side only — no gate/schema/prompt/store-write change):

- **Per-scan network visualizer.** The Disposition subject map renders as an **SVG network**: nodes =
  the scan's entities (main subjects highlighted + central), edges = the gate-passed `relationships[]`
  with their vocab labels. Layout is `liveGraphLayout` — a PURE deterministic data→positions function
  (radial placement + a fixed number of relaxation iterations, no randomness, no vendored library;
  SVG is the initial implementation, revisited if the live tool outgrows demo scale). Clicking an
  edge (svg or list row) reveals its verbatim grounded **evidence quote** — closed by default.
  Degenerate shapes tolerated: 0-relationship scans render isolated nodes; an edge endpoint missing
  from the entity list is synthesized as a node; a from==to edge is skipped.
- **Anchor dossier.** Clicking a graph node — or a watchlist row name — fetches the NEW companion
  route `GET /anchor?name=<n>` (wraps `news_store.anchor_summary()`; read-only, name-keyed, honest
  404 on unknown names, 503 with persistence off) and renders the ACCUMULATED identity: every scan
  that touched the anchor (with `source_type` provenance), properties grouped by kind with per-scan
  provenance, accumulated aliases, and relationship edges. **Same-kind different values render BOTH,
  flagged "conflicting values — both kept"** — coexisting claims for the analyst, presentation-only,
  never auto-resolved (the Phase-41 store rule, now visible).
- Everything sits inside the `/*LIVE_START*/…/*LIVE_END*/` region; the offline `dist/news` is
  byte-identical (zero graph/dossier/route code ships).

## Demo: anchor accumulation (Phase 42)
The committed fixture articles are case-disjoint (zero cross-article entity overlap), so the dossier's
payoff — cross-scan accumulation + conflict surfacing — is demonstrated with a committed SYNTHETIC
investigation note: `docs/demo-investigation-note.md` (clearly labeled; fictional client/phone data;
subject names from a public OFAC release so it lands on the same demo anchor).

**Canonical flow** (fresh store, companion under `.venv`):
1. Paste a fixture article (e.g. `data/news/articles/ofac-tgr-group.md`) — source type
   *Government / enforcement release* — and Run. The Disposition step shows the network.
2. Paste the body of `docs/demo-investigation-note.md` — source type *Investigation note* — and Run.
3. Open the shared entity's dossier (click the **George Rossi** node, or the watchlist row after an
   escalate): TWO scans listed with their source types, the `client_number` from the note, the
   note's conflicting phone values flagged **"conflicting values — both kept"**, and the location
   claim sitting beside the article's nationality — coexisting claims, never resolved.

**Optional no-note variant:** re-scan the SAME article twice — the anchor accumulates two scan rows
(pure accumulation with provenance, no conflict). The DuckDB store stays local + gitignored either
way; the note is synthetic and the only thing committed.

## Extraction progress (Phase 39)
`POST /extract` answers an **NDJSON stage stream** instead of a single blocking JSON (a full run is tens
of seconds — measured 42.7s end-to-end on a 16-entity OFAC article): one line per pipeline stage —
`fetching → converted → extracting → grounding → verifying i/N (per entity — the wall-time majority) →
{done: payload}` — written + flushed as it happens (HTTP/1.0 body-until-close; no chunked framing
needed). The page reads it with `fetch` + a ReadableStream and paints the stage label, the verify
`i of N` with the entity name, and an elapsed-seconds counter. Pipeline failures after the stream opens
travel **in-stream** as `{error: …}` (the client reads events, not status codes); request-shape errors
are still plain 400s. Request-side, the existing `extract()` contract is untouched — progress is an
optional `on_progress=None` callback, so the Phase-38 replay fixtures pin the same deterministic core
with no re-capture.

## One-shot URL acquisition (Phase 39)
`POST /extract {url}` skips pasting entirely: the companion **acquires** the page server-side and runs
the same pipeline on the result. Acquisition lives in the companion-only `scripts/news_fetch.py` and is
the project spine applied to fetch — **acquisition proposes, a deterministic gate disposes**:
1. **The fetch LADDER** — bot guards are normal in the wild, so three clients are tried in order:
   `urllib` (browser-like headers + a cookie jar, following ONE same-host interstitial meta-refresh —
   the Akamai two-step seen live on justice.gov) → `curl` (a different TLS fingerprint, same cookie
   dance) → `markitdown convert_uri` (a third client). A rung only *wins* if its result **passes the
   verifier** — a "successful" fetch of a guard page advances the ladder like a connection error.
2. **The STANDARDIZER** — deterministic markdown cleanup of the converted page (drop images, nav/link
   furniture, bare-URL lines; unwrap inline links; collapse blanks). Purely structural; it never
   rewrites prose, because the result is both the model input AND the grounding surface.
3. **The VERIFIER** — article-shape checks (min prose length, running sentences, prose ratio,
   bot-guard/paywall marker detection on short results). A URL that can't produce a verified article is
   an **honest in-stream failure** ("…paste the article text instead") with every failed rung reported —
   never a loosened gate.

The converted text streams back EARLY (the `converted` event) and **fills the textarea as the run
proceeds** — the analyst sees exactly what the model saw, and can trim noise and re-run; **pasted text
wins over the URL** on that next run. HTML→markdown conversion needs `markitdown` (the same `.venv`
authoring dep `pdf_to_md.py` uses); without it URL mode degrades to an honest "run under the .venv or
paste" message while paste mode keeps working — `build.py` never imports any of this.

## Run it
1. **Start a local llama-cpp server** with an OpenAI-compatible endpoint, serving your model (e.g. a
   Qwen ~30B-A3B-class GGUF):
   ```
   llama-server -m /path/to/qwen.gguf --port 8080 --jinja
   ```
   (`--jinja` enables the chat template; the companion requests JSON-schema-constrained output and disables
   thinking. Any model behind `/v1/chat/completions` works — it's swappable.)
2. **Start the companion** (under the `.venv` so DuckDB persistence + the watchlist are active):
   ```
   .venv/bin/python scripts/serve_news.py --port 8000 \
       --llm-url http://127.0.0.1:8080/v1/chat/completions --model qwen
   ```
   (`--llm-url` defaults to `http://127.0.0.1:8080/v1/chat/completions`, so the bare
   `.venv/bin/python scripts/serve_news.py` already points at a local llama-cpp on 8080.)
3. Open **http://localhost:8000**, click **＋ Process a new article**, then either drop an **article URL**
   in the URL field (one shot — the companion fetches, converts, verifies, and extracts; the converted
   text fills the textarea as it runs) or paste article text (a public-domain gov-enforcement record is
   the cleanest choice — see the compliance note), and **Run extraction**. Stage progress (fetch →
   convert → extract → ground → verify *i of N* + elapsed seconds) paints live; the grounded record then
   flows through the existing Read → Screen → Disposition → Exposure arc.

The offline demo still works with no companion: just open `dist/news/index.html`.

## Honesty / compliance
- Real client-side fuzzy scores; the counterparty **book is synthetic** (no real customer data); the
  always-on "Illustrative data & outputs" badge stays.
- The model's output is **grounded then shown** — ungrounded entities/flags drop; ungrounded attributes are
  stripped. If nothing grounds, `/extract` returns an honest error rather than an empty arc.
- Paste **public** text (e.g. US-federal enforcement records, public domain under 17 U.S.C. §105). No real
  customer/transaction data, ever.
- **URL mode (Phase 39) carries the same posture, not a new one.** Fetching happens locally at
  dev/authoring time; the fetched text is processed in your browser + local model session and is **never
  committed, redistributed, or shipped** (live scans land only in the gitignored local DuckDB store).
  Point it at public/US-federal sources by default. Anything you *promote* into the repo (a test fixture,
  a committed article) keeps the existing reproduction bases: US-federal public domain (17 U.S.C. §105),
  the FINTRAC attribution licence, or synthetic — a URL lowering the friction to fetch a commercial news
  page does not change what may be committed.

## Tests (dep-free, no model; the DuckDB store parts run under `.venv`)
- `node tests/news-stream.test.mjs` — the offline arc + the fuzzy matcher + the companion-served live
  overrides: the **book ∪ watchlist** screen, the **escalate** Disposition gate, (Phase 38) the
  **watchlist view + prune** panel (render + empty state), and (Phase 41) the **alias-aware matcher**
  (exact-yes/fuzzy-no per alias class, both directions) + the **subject map / identity cards** render —
  plus the strip assertion that none of the live/watchlist/view/enrichment code survives in the offline
  `dist/news`.
- `python3 tests/news_live_test.py` — `build_record` + grounding (CANNED, incl. the Phase-40 planted
  duplicate-flag collapse), the **recorded-fixture replay** (13 real captured-Qwen outputs under
  `tests/fixtures/news-live/` — 7 original + 3 `<id>.ph40.*` checklist-prompt re-captures + 3
  `<id>.ph41.*` enriched-schema re-captures → parse→build→ground→screen == committed goldens, **no
  model**; every base id asserted against the US-federal `FIXTURE_META` allowlist — the privacy check),
  the keep-biased **second-pass verify** (model stubbed), the `/extract`
  route as an **NDJSON stage stream** (stages precede the payload; mid-stream failures → in-stream error
  events), and the **one-shot URL route** (acquisition stubbed: fetching→converted(text)→stages, text
  wins over url, verifier failure → in-stream paste suggestion). Run under **`.venv/bin/python`** to also
  drive `/watchlist` + `/disposition` + `/watchlist/prune` over a temp DuckDB store (Phase 41: the
  escalated row carries the anchor's **aliases** + the scan's **source_type**); under system python
  those SKIP. Add **`--live`** to hit a running model at `127.0.0.1:8080` (an opt-in smoke; OFF by default).
- `python3 scripts/news_fetch.py --selftest` — URL acquisition, dep-free + no network: the standardizer
  pinned byte-exact to a committed golden (`tests/fixtures/news-fetch/`), the verifier's pass/fail modes,
  the interstitial meta-refresh detector, and the ladder order incl. the verifier-advances-the-ladder rule.
  Under `.venv` it also converts the committed fixture HTML through real markitdown end-to-end.
- `.venv/bin/python scripts/news_store.py --selftest` — the DuckDB store: append → escalate → watchlist
  union → parquet roundtrip; Phase 41: anchor accumulation (4 scans → 1 anchor), the both-kept conflict
  rule, alias/property/relationship edges, the NULL-confidence assert, and the legacy-store additive
  migration.
- `python3 scripts/news_ground.py --selftest` — the shared grounding gate.
- `python3 scripts/serve_news.py --selftest` — the companion assembles the page with the live branch.
