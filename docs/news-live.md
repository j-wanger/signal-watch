# News stream — live local-model mode (Phase 35, M8)

Optional, dev/authoring-time **live mode** for the adverse-media news stream: paste an article and a
local model extracts entities + red flags in **real time**, grounded against the source. It is NOT part
of the ship artifact — the offline single-file `dist/news/index.html` stays the default and the scripted
fallback (it makes no network call; the live branch is build-time stripped from it).

## Architecture
```
http://localhost:8000/         serve_news.py (stdlib companion) — serves news.html WITH the live branch
  ├── GET  /                   the page (NEWS.live set → "＋ Process a new article" control on Select)
  ├── GET  /health             {"ok": true}
  └── POST /extract            text → llama-cpp → JSON-schema output → GROUND (drop ungrounded) → record
          │  same-origin (no CORS)
          ▼
  http://localhost:8080/v1/...  llama-cpp server (your Qwen model) — proxied; the browser never sees it
```
The model **proposes**; `news_ground.ground_record` **disposes** — every entity name, attribute, and
red-flag `flag` must quote-ground in the submitted article (the same gate `build.py` uses at build time),
or it is dropped. Nothing is shown that isn't in the source. Fuzzy screening stays the real client-side
Jaro-Winkler matcher against the **synthetic** book. Persistence + a feedback watchlist are Phase 36.

## Run it
1. **Start a local llama-cpp server** with an OpenAI-compatible endpoint, serving your model (e.g. a
   Qwen ~30B-A3B-class GGUF):
   ```
   llama-server -m /path/to/qwen.gguf --port 8080 --jinja
   ```
   (`--jinja` enables the chat template; the companion requests JSON-schema-constrained output and disables
   thinking. Any model behind `/v1/chat/completions` works — it's swappable.)
2. **Start the companion:**
   ```
   python3 scripts/serve_news.py --port 8000 \
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

## Tests (dep-free, no model)
- `python3 tests/news_live_test.py` — `build_record` + grounding over the committed OFAC article (real
  grounded items kept, planted ungrounded dropped) + the `/extract` route over HTTP with the model stubbed.
- `python3 scripts/news_ground.py --selftest` — the shared grounding gate.
- `python3 scripts/serve_news.py --selftest` — the companion assembles the page with the live branch.
