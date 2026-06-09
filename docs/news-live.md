# News stream — live local-model mode (Phase 35–39, M8)

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

Structurally, a small deterministic pass (`news_ground.screen_entities`) still removes surname-alias
duplicates, source-attribution publishers, judicial officers, and `@handles` — the rules that *generalize*.

## Watchlist view + prune (Phase 38)
The escalated-only watchlist is now **visible and manageable** on the Select screen: a panel lists each
escalated entity with its provenance (*"escalated from &lt;article&gt;"*) and a **✕ Prune** control that
`POST`s `/watchlist/prune {name}` to un-escalate it (the audit row is retained; the book is never
touched). Companion-only — stripped from the offline `dist/news` like the rest of the live region.

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
  overrides: the **book ∪ watchlist** screen, the **escalate** Disposition gate, and (Phase 38) the
  **watchlist view + prune** panel (render + empty state) — plus the strip assertion that none of the
  live/watchlist/view code survives in the offline `dist/news`.
- `python3 tests/news_live_test.py` — `build_record` + grounding (CANNED), the **recorded-fixture replay**
  (7 real captured-Qwen outputs under `tests/fixtures/news-live/` → parse→build→ground→screen == committed
  goldens, **no model**), the keep-biased **second-pass verify** (model stubbed), the `/extract`
  route as an **NDJSON stage stream** (stages precede the payload; mid-stream failures → in-stream error
  events), and the **one-shot URL route** (acquisition stubbed: fetching→converted(text)→stages, text
  wins over url, verifier failure → in-stream paste suggestion). Run under **`.venv/bin/python`** to also
  drive `/watchlist` + `/disposition` + `/watchlist/prune` over a temp DuckDB store; under system python
  those SKIP. Add **`--live`** to hit a running model at `127.0.0.1:8080` (an opt-in smoke; OFF by default).
- `python3 scripts/news_fetch.py --selftest` — URL acquisition, dep-free + no network: the standardizer
  pinned byte-exact to a committed golden (`tests/fixtures/news-fetch/`), the verifier's pass/fail modes,
  the interstitial meta-refresh detector, and the ladder order incl. the verifier-advances-the-ladder rule.
  Under `.venv` it also converts the committed fixture HTML through real markitdown end-to-end.
- `.venv/bin/python scripts/news_store.py --selftest` — the DuckDB store: append → escalate → watchlist
  union → parquet roundtrip.
- `python3 scripts/news_ground.py --selftest` — the shared grounding gate.
- `python3 scripts/serve_news.py --selftest` — the companion assembles the page with the live branch.
