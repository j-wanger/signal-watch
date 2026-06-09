# News stream — live local-model mode (Phase 35–38, M8)

Optional, dev/authoring-time **live mode** for the adverse-media news stream: paste an article and a
local model extracts entities + red flags in **real time**, grounded against the source. It is NOT part
of the ship artifact — the offline single-file `dist/news/index.html` stays the default and the scripted
fallback (it makes no network call; the live branch is build-time stripped from it).

## Architecture
```
http://localhost:8000/         serve_news.py (stdlib companion) — serves news.html WITH the live branch
  ├── GET  /                   the page (NEWS.live set → "＋ Process a new article" control on Select)
  ├── GET  /health             {"ok": true, "persist": <bool>}
  ├── GET  /watchlist          book ∪ escalated entities (reconciled + provenance) — the live screen surface
  ├── POST /extract            text → llama-cpp → JSON-schema → GROUND → 2nd-pass entity verify → record → PERSIST
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
3. Open **http://localhost:8000**, click **＋ Process a new article**, paste article text (a public-domain
   gov-enforcement record is the cleanest choice — see the compliance note), and **Run extraction**. The
   grounded record flows through the existing Read → Screen → Disposition → Exposure arc.

The offline demo still works with no companion: just open `dist/news/index.html`.

## Honesty / compliance
- Real client-side fuzzy scores; the counterparty **book is synthetic** (no real customer data); the
  always-on "Illustrative data & outputs" badge stays.
- The model's output is **grounded then shown** — ungrounded entities/flags drop; ungrounded attributes are
  stripped. If nothing grounds, `/extract` returns an honest error rather than an empty arc.
- Paste **public** text (e.g. US-federal enforcement records, public domain under 17 U.S.C. §105). No real
  customer/transaction data, ever.

## Tests (dep-free, no model; the DuckDB store parts run under `.venv`)
- `node tests/news-stream.test.mjs` — the offline arc + the fuzzy matcher + the companion-served live
  overrides: the **book ∪ watchlist** screen, the **escalate** Disposition gate, and (Phase 38) the
  **watchlist view + prune** panel (render + empty state) — plus the strip assertion that none of the
  live/watchlist/view code survives in the offline `dist/news`.
- `python3 tests/news_live_test.py` — `build_record` + grounding (CANNED), the **recorded-fixture replay**
  (7 real captured-Qwen outputs under `tests/fixtures/news-live/` → parse→build→ground→screen == committed
  goldens, **no model**), the keep-biased **second-pass verify** (model stubbed), and the `/extract`
  route. Run under **`.venv/bin/python`** to also drive `/watchlist` + `/disposition` + `/watchlist/prune`
  over a temp DuckDB store; under system python those SKIP. Add **`--live`** to hit a running model at
  `127.0.0.1:8080` (an opt-in smoke; OFF by default).
- `.venv/bin/python scripts/news_store.py --selftest` — the DuckDB store: append → escalate → watchlist
  union → parquet roundtrip.
- `python3 scripts/news_ground.py --selftest` — the shared grounding gate.
- `python3 scripts/serve_news.py --selftest` — the companion assembles the page with the live branch.
