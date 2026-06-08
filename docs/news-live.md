# News stream — live local-model mode (Phase 35–36, M8)

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
  ├── POST /extract            text → llama-cpp → JSON-schema → GROUND (drop ungrounded) → record → PERSIST
  └── POST /disposition        {scan_id, entity_id, decision} — 'escalate' adds the entity to the watchlist
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
       --llm-url http://localhost:8080/v1/chat/completions --model qwen
   ```
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
- `node tests/news-stream.test.mjs` — the offline arc + the fuzzy matcher + (Phase 36) the companion-served
  live overrides: the **book ∪ watchlist** screen and the **escalate** Disposition gate.
- `python3 tests/news_live_test.py` — `build_record` + grounding over the committed OFAC article (real
  grounded items kept, planted ungrounded dropped) + the `/extract` route (model stubbed). Run under
  **`.venv/bin/python`** to also drive `/watchlist` + `/disposition` over a temp DuckDB store (the
  escalated-only loop); under system python the store test SKIPS.
- `.venv/bin/python scripts/news_store.py --selftest` — the DuckDB store: append → escalate → watchlist
  union → parquet roundtrip.
- `python3 scripts/news_ground.py --selftest` — the shared grounding gate.
- `python3 scripts/serve_news.py --selftest` — the companion assembles the page with the live branch.
